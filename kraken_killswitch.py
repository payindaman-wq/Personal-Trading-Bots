#!/usr/bin/env python3
"""
kraken_killswitch.py — Live drawdown kill-switch + graduated alerts for Kraken.

Dormant until Phase 1 Kraken funding lands (/root/.openclaw/secrets/kraken.json).
Once active, runs every 5 min via cron:
  - Fetches current Kraken account equity (ZUSD + USD value of open positions).
  - Tracks peak_equity in killswitch_state.json.
  - Graduated thresholds (P1.1, 2026-04-19):
      *  5% drawdown: info-level inbox entry (dashboard only, no Telegram).
      * 10% drawdown: warning-level inbox entry (Telegram — early warning).
      * 15% drawdown: CRITICAL. Writes KILLSWITCH_TRIGGERED flag, stops live
        services, actionable Telegram alert.
  - Auto-recovery (P1.2, 2026-04-19): when triggered, if drawdown recovers to
    <=5% AND flag has been present for >=48h, auto-clears flag, restarts live
    services, and logs recovery event. Gives set-and-forget operation while
    keeping a genuine loss window for Chris to review.
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
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE     = "/root/.openclaw/workspace"
SECRETS_FILE  = "/root/.openclaw/secrets/kraken.json"
STATE_FILE    = f"{WORKSPACE}/competition/killswitch_state.json"
FLAG_FILE     = f"{WORKSPACE}/KILLSWITCH_TRIGGERED"
LOG_FILE      = f"{WORKSPACE}/competition/killswitch.log"
BOT_TOKEN     = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID       = "8154505910"

DRAWDOWN_THRESHOLD = 0.15  # 15% = hard kill
DRAWDOWN_WARNING   = 0.10  # 10% = Telegram warning
DRAWDOWN_INFO      = 0.05  # 5%  = dashboard-only info

# Auto-recovery: if flag has been up this long AND drawdown is back under this
# much, auto-clear flag + restart services. Both conditions required.
RECOVERY_HOLD_HOURS     = 48
RECOVERY_DRAWDOWN_MAX   = 0.05

# Cooldowns to avoid spamming graduated warnings on every 5-min tick
SOFT_ALERT_COOLDOWN_HOURS = 6

LIVE_SERVICES      = ["polymarket_syn.service"]

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


INBOX = f"{WORKSPACE}/syn_inbox.jsonl"


def tg_actionable(msg, severity="critical"):
    """Write to SYN inbox. sys_heartbeat is the sole Telegram gateway."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "kraken_killswitch",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        log(f"[killswitch/inbox] {e}")


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


def soft_alert(state, equity, peak, drawdown, severity, key):
    """Fire a graduated pre-kill alert with per-threshold cooldown."""
    from datetime import timedelta
    last = state.get(f"soft_alert_{key}")
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if datetime.now(timezone.utc) - last_dt < timedelta(hours=SOFT_ALERT_COOLDOWN_HOURS):
                return
        except Exception:
            pass
    # severity: "info" stays on dashboard; "warning" doesn't Telegram under
    # current allowlist either. To reach Telegram, upgrade to "error".
    send_severity = "error" if severity == "warning" else severity
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "kraken_killswitch",
            "severity": send_severity,
            "msg":      (
                f"<b>SYN: drawdown {drawdown*100:.1f}% ({key})</b>\n"
                f"Peak:    ${peak:,.2f}\n"
                f"Current: ${equity:,.2f}\n"
                f"Kill threshold: {DRAWDOWN_THRESHOLD*100:.0f}% — still trading."
            ),
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + chr(10))
    except Exception as e:
        log(f"[soft_alert] inbox write failed: {e}")
    state[f"soft_alert_{key}"] = datetime.now(timezone.utc).isoformat()
    log(f"[soft_alert] {key} @ drawdown {drawdown*100:.2f}%")


def auto_recover(state, peak, equity, drawdown, hold_hours):
    """Clear flag + restart services when drawdown has recovered."""
    try:
        os.remove(FLAG_FILE)
    except FileNotFoundError:
        pass
    except Exception as e:
        log(f"[recover] flag removal failed: {e}")
    restarted = []
    for svc in LIVE_SERVICES:
        try:
            subprocess.run(["systemctl", "start", svc], check=False, timeout=15)
            restarted.append(svc)
        except Exception as e:
            log(f"[recover] {svc} start failed: {e}")
    state["triggered"]      = False
    state["triggered_at"]   = None
    state["recovered_at"]   = datetime.now(timezone.utc).isoformat()
    save_state(state)
    log(f"[RECOVER] cleared flag, restarted {restarted}, drawdown={drawdown*100:.2f}% hold={hold_hours:.1f}h")
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "kraken_killswitch",
            "severity": "error",  # surfaces to Telegram — Chris should know recovery happened
            "msg":      (
                f"<b>SYN: kill-switch AUTO-RECOVERED</b>\n"
                f"Peak:    ${peak:,.2f}\n"
                f"Current: ${equity:,.2f}\n"
                f"Drawdown: {drawdown*100:.2f}% (recovery threshold {RECOVERY_DRAWDOWN_MAX*100:.0f}%)\n"
                f"Held paused: {hold_hours:.1f}h (min {RECOVERY_HOLD_HOURS}h)\n"
                f"Restarted: {', '.join(restarted) or 'none'}"
            ),
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + chr(10))
    except Exception as e:
        log(f"[recover] inbox write failed: {e}")


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

    # Already-triggered: evaluate auto-recovery window + threshold.
    if state.get("triggered") and os.path.isfile(FLAG_FILE):
        peak_now = state.get("peak_equity", 0.0)
        try:
            equity_now = fetch_equity(key, secret)
        except Exception as e:
            log(f"already-triggered: equity fetch failed: {e}")
            return
        dd_now = (peak_now - equity_now) / peak_now if peak_now > 0 else 0.0
        triggered_at_iso = state.get("triggered_at")
        hold_hours = 0.0
        if triggered_at_iso:
            try:
                t0 = datetime.fromisoformat(triggered_at_iso)
                hold_hours = (datetime.now(timezone.utc) - t0).total_seconds() / 3600
            except Exception:
                hold_hours = 0.0
        state["last_equity"] = equity_now
        state["last_check"]  = datetime.now(PST).isoformat()
        log(f"already-triggered: equity=${equity_now:.2f} peak=${peak_now:.2f} "
            f"dd={dd_now*100:.2f}% hold={hold_hours:.1f}h")
        if dd_now <= RECOVERY_DRAWDOWN_MAX and hold_hours >= RECOVERY_HOLD_HOURS:
            auto_recover(state, peak_now, equity_now, dd_now, hold_hours)
        else:
            save_state(state)
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
        state["triggered"]    = True
        state["triggered_at"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
        trigger_killswitch(peak, equity, drawdown)
    elif drawdown >= DRAWDOWN_WARNING:
        soft_alert(state, equity, peak, drawdown, "warning", "DRAWDOWN_WARNING")
        save_state(state)
    elif drawdown >= DRAWDOWN_INFO:
        soft_alert(state, equity, peak, drawdown, "info", "DRAWDOWN_INFO")
        save_state(state)
    else:
        # Clear graduated-alert cooldowns when drawdown recovers under 5%
        state.pop("soft_alert_DRAWDOWN_WARNING", None)
        state.pop("soft_alert_DRAWDOWN_INFO", None)
        save_state(state)


if __name__ == "__main__":
    main()
