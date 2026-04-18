#!/usr/bin/env python3
"""
kraken_killswitch.py — Live 15% drawdown kill-switch for Kraken.

Dormant until Phase 1 Kraken funding lands (/root/.openclaw/secrets/kraken.json).
Once active, runs every 5 min via cron:
  - Fetches current Kraken account equity (ZUSD + USD value of open positions).
  - Tracks peak_equity in killswitch_state.json.
  - If current <= 0.85 * peak:
      * Writes KILLSWITCH_TRIGGERED flag file (bots refuse to trade).
      * Stops live trading services.
      * Fires ACTIONABLE Telegram alert (call to action — user must review).
  - Flag is NOT auto-cleared on recovery — manual reset required after review.
"""
import base64
import hashlib
import hmac
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE     = "/root/.openclaw/workspace"
SECRETS_FILE  = "/root/.openclaw/secrets/kraken.json"
STATE_FILE    = f"{WORKSPACE}/competition/killswitch_state.json"
FLAG_FILE     = f"{WORKSPACE}/KILLSWITCH_TRIGGERED"
LOG_FILE      = f"{WORKSPACE}/competition/killswitch.log"
BOT_TOKEN     = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID       = "8154505910"

DRAWDOWN_THRESHOLD = 0.15  # 15%
LIVE_SERVICES      = ["kalshi_copy.service", "polymarket_syn.service"]

KRAKEN_API = "https://api.kraken.com"


def ts():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M PST")


def log(msg):
    line = f"[{ts()}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def tg_actionable(msg):
    """Telegram alert — reserved for calls-to-action only (per user rule)."""
    try:
        payload = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10).read()
    except Exception as e:
        log(f"[tg] {e}")


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"peak_equity": 0.0, "last_equity": 0.0, "last_check": None, "triggered": False}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)


def kraken_private(path, key, secret, data=None):
    data = dict(data or {})
    data["nonce"] = str(int(time.time() * 1000))
    post = urllib.parse.urlencode(data)
    sha = hashlib.sha256((data["nonce"] + post).encode()).digest()
    sig = hmac.new(base64.b64decode(secret), path.encode() + sha, hashlib.sha512)
    headers = {
        "API-Key": key,
        "API-Sign": base64.b64encode(sig.digest()).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "SYN-killswitch/1.0",
    }
    req = urllib.request.Request(KRAKEN_API + path, data=post.encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def fetch_equity(key, secret):
    """Return total account equity in USD. Uses TradeBalance for margin-aware value."""
    resp = kraken_private("/0/private/TradeBalance", key, secret, {"asset": "ZUSD"})
    if resp.get("error"):
        raise RuntimeError(f"Kraken error: {resp['error']}")
    result = resp.get("result", {})
    # 'eb' = equivalent balance (combined), 'e' = equity (incl. unrealized P/L)
    return float(result.get("e", result.get("eb", 0.0)))


def stop_live_services():
    stopped = []
    for svc in LIVE_SERVICES:
        try:
            subprocess.run(["systemctl", "stop", svc], check=False, timeout=15)
            stopped.append(svc)
        except Exception as e:
            log(f"[stop] {svc} failed: {e}")
    return stopped


def trigger_killswitch(peak, current, drawdown_pct):
    # Write flag file — bots should check this before any live order
    with open(FLAG_FILE, "w") as f:
        f.write(json.dumps({
            "triggered_at": datetime.now(PST).isoformat(),
            "peak_equity":  peak,
            "current_equity": current,
            "drawdown_pct": drawdown_pct,
        }, indent=2))
    log(f"[KILL] Flag file written: {FLAG_FILE}")

    stopped = stop_live_services()
    log(f"[KILL] Stopped services: {stopped}")

    tg_actionable(
        f"<b>KILL-SWITCH TRIGGERED</b>\n"
        f"Peak:    ${peak:,.2f}\n"
        f"Current: ${current:,.2f}\n"
        f"Drawdown: {drawdown_pct*100:.2f}%\n"
        f"Services stopped: {', '.join(stopped) or 'none'}\n"
        f"Flag: {FLAG_FILE}\n\n"
        f"ACTION REQUIRED: review losses, then delete flag + restart services to resume."
    )


def main():
    # Dormant check — no Kraken funding yet
    if not os.path.isfile(SECRETS_FILE):
        log("dormant: kraken.json not present (Phase 1 funding pending)")
        return

    try:
        with open(SECRETS_FILE) as f:
            creds = json.load(f)
        key    = creds.get("api_key") or creds.get("kraken_api_key")
        secret = creds.get("api_secret") or creds.get("kraken_api_secret")
        if not key or not secret:
            log("error: kraken.json present but missing api_key/api_secret — cannot query equity")
            return
    except Exception as e:
        log(f"error reading secrets: {e}")
        return

    state = load_state()

    # Already-triggered short-circuit — don't re-alert, just log
    if state.get("triggered") and os.path.isfile(FLAG_FILE):
        log(f"already-triggered: flag present, peak=${state.get('peak_equity', 0):.2f}")
        return

    try:
        equity = fetch_equity(key, secret)
    except Exception as e:
        log(f"error fetching equity: {e}")
        return

    peak = max(state.get("peak_equity", 0.0), equity)
    drawdown = (peak - equity) / peak if peak > 0 else 0.0

    log(f"equity=${equity:.2f} peak=${peak:.2f} drawdown={drawdown*100:.2f}%")

    state.update({
        "peak_equity": peak,
        "last_equity": equity,
        "last_check":  datetime.now(PST).isoformat(),
    })

    if drawdown >= DRAWDOWN_THRESHOLD:
        state["triggered"] = True
        save_state(state)
        trigger_killswitch(peak, equity, drawdown)
    else:
        save_state(state)


if __name__ == "__main__":
    main()
