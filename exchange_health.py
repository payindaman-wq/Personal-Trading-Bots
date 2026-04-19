#!/usr/bin/env python3
"""
exchange_health.py — Kraken + Kalshi API reachability monitor.

Runs every 5 min via cron. Pings public status endpoints for both exchanges.
After 3 consecutive failures on Kalshi, stops trading services
(kalshi_copy, polymarket_syn) and writes a pause flag. On recovery,
restarts them and fires a SYN alert. Kraken failure alerts but does not
auto-pause (no live Kraken trading yet — Phase 1 funding pending).
"""
import json, os, subprocess, urllib.request, urllib.error, ssl
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/exchange_health_state.json"
PAUSE_FLAG = f"{WORKSPACE}/competition/exchange_paused"
BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID = "8154505910"

FAIL_THRESHOLD = 3

KALSHI_TRADING_SERVICES = ["kalshi_copy.service", "polymarket_syn.service"]

EXCHANGES = {
    "kraken": {
        "url": "https://api.kraken.com/0/public/SystemStatus",
        "timeout": 10,
        "check": lambda r: r.get("result", {}).get("status") == "online",
        "pause_services": [],
    },
    "kalshi": {
        "url": "https://api.elections.kalshi.com/trade-api/v2/exchange/status",
        "timeout": 10,
        "check": lambda r: r.get("exchange_active") is True and r.get("trading_active") is True,
        "pause_services": KALSHI_TRADING_SERVICES,
    },
}


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"fail_count": {}, "paused": {}}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)


INBOX = "/root/.openclaw/workspace/syn_inbox.jsonl"


def tg_send(msg, severity="error"):
    """Write to SYN inbox. sys_heartbeat is the sole Telegram gateway."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "exchange_health",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[exchange_health/inbox] {e}")


def ping(name, cfg):
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(cfg["url"], headers={"User-Agent": "SYN-health/1.0"})
        with urllib.request.urlopen(req, timeout=cfg["timeout"], context=ctx) as resp:
            if resp.status != 200:
                return False, f"HTTP {resp.status}"
            body = json.loads(resp.read().decode())
            if not cfg["check"](body):
                return False, f"payload not healthy: {json.dumps(body)[:200]}"
            return True, "ok"
    except urllib.error.HTTPError as e:
        return False, f"HTTPError {e.code}"
    except urllib.error.URLError as e:
        return False, f"URLError {e.reason}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def svc_action(action, unit):
    try:
        r = subprocess.run(
            ["systemctl", action, unit], capture_output=True, text=True, timeout=30
        )
        return r.returncode == 0, (r.stderr or r.stdout).strip()
    except Exception as e:
        return False, str(e)


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def fmt_svc_result(unit, ok, msg):
    return unit if ok else f"{unit} ({msg})"


def main():
    state = load_state()
    results = {}
    for name, cfg in EXCHANGES.items():
        ok, detail = ping(name, cfg)
        results[name] = (ok, detail)
        prev_fails = state["fail_count"].get(name, 0)
        was_paused = state["paused"].get(name, False)

        if ok:
            if prev_fails >= FAIL_THRESHOLD and was_paused:
                restarted, failed = [], []
                for unit in cfg["pause_services"]:
                    r_ok, r_msg = svc_action("start", unit)
                    (restarted if r_ok else failed).append(fmt_svc_result(unit, r_ok, r_msg))
                state["paused"][name] = False
                try:
                    if os.path.exists(PAUSE_FLAG):
                        os.remove(PAUSE_FLAG)
                except Exception:
                    pass
                msg = (
                    f"<b>SYN: {name.upper()} API recovered</b>\n"
                    f"Time: {pst_now()}\n"
                    f"Resumed: {', '.join(restarted) or 'none'}"
                )
                if failed:
                    msg += f"\nRestart failed: {', '.join(failed)}"
                tg_send(msg, severity="info")  # recovery is good news, not actionable
            elif prev_fails >= FAIL_THRESHOLD:
                tg_send(f"<b>SYN: {name.upper()} API recovered</b>\nTime: {pst_now()}", severity="info")
            state["fail_count"][name] = 0
        else:
            new_count = prev_fails + 1
            state["fail_count"][name] = new_count
            print(f"[{name}] fail #{new_count}: {detail}")
            if new_count == FAIL_THRESHOLD:
                paused, failed = [], []
                for unit in cfg["pause_services"]:
                    r_ok, r_msg = svc_action("stop", unit)
                    (paused if r_ok else failed).append(fmt_svc_result(unit, r_ok, r_msg))
                if cfg["pause_services"]:
                    state["paused"][name] = True
                    with open(PAUSE_FLAG, "w") as f:
                        f.write(f"{name} down at {pst_now()}: {detail}\n")
                msg = (
                    f"<b>SYN: {name.upper()} API DOWN</b>\n"
                    f"Time: {pst_now()}\n"
                    f"Reason: {detail[:200]}\n"
                    f"Consecutive failures: {new_count}\n"
                )
                if cfg["pause_services"]:
                    msg += f"Paused: {', '.join(paused) or 'none'}\n"
                else:
                    msg += "No auto-pause (no live trading yet)\n"
                if failed:
                    msg += f"Stop failed: {', '.join(failed)}"
                tg_send(msg)

    save_state(state)
    line = " | ".join(f"{n}={'OK' if ok else 'FAIL'}" for n, (ok, _) in results.items())
    print(f"[{pst_now()}] {line}")


if __name__ == "__main__":
    main()
