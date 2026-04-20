#!/usr/bin/env python3
"""
service_crashloop_watch.py — Tier 2 self-heal rule #1 (SYN/crashloop).

Runs every 15 min via cron. For each critical systemd service:
  - Read NRestarts (systemctl show).
  - Compare against last snapshot.
  - If NRestarts increased by >= CRASHLOOP_THRESHOLD in the window, alert.

This fills the "systemd crash-loop undetected" gap from the 2026-04-19 audit —
systemd respawns a crashing service forever but nobody was watching the count.

Tier 2 rule. Safe today (no calibration needed; 3 restarts/window is
objectively bad regardless of baseline).
"""
import json
import os
import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/crashloop_state.json"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"

SERVICES = [
    "odin_day",
    "odin_swing",
    "odin_futures_day",
    "odin_futures_swing",
    "freya",
    "kalshi_copy",
    "polymarket_syn",
]

CRASHLOOP_THRESHOLD = 3   # restarts per window
COOLDOWN_MIN = 360        # 6h dedup per service


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"last_restarts": {}, "last_alerted": {}}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)


def cooldown_elapsed(state, key, minutes):
    from datetime import timedelta
    last = state["last_alerted"].get(key)
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return True
    return datetime.now(timezone.utc) - last_dt > timedelta(minutes=minutes)


def inbox_write(msg, severity="error"):
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "crashloop",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + chr(10))
    except Exception as e:
        print(f"[crashloop/inbox] {e}")


def service_nrestarts(service):
    try:
        out = subprocess.check_output(
            ["systemctl", "show", "--property=NRestarts", "--property=ActiveState", service],
            timeout=5,
        ).decode()
        props = dict(line.split("=", 1) for line in out.strip().splitlines() if "=" in line)
        return int(props.get("NRestarts", 0)), props.get("ActiveState", "unknown")
    except Exception:
        return None, None


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def main():
    state = load_state()
    summary = []

    for svc in SERVICES:
        nrestarts, active = service_nrestarts(svc)
        if nrestarts is None:
            summary.append(f"{svc}: unreadable")
            continue
        prev = state["last_restarts"].get(svc, nrestarts)
        delta = nrestarts - prev
        state["last_restarts"][svc] = nrestarts

        if delta >= CRASHLOOP_THRESHOLD:
            if cooldown_elapsed(state, svc, COOLDOWN_MIN):
                inbox_write(
                    f"<b>SYN: {svc} crash-loop detected</b>\n"
                    f"Time: {pst_now()}\n"
                    f"Restarts this window: {delta}\n"
                    f"Total restarts: {nrestarts}\n"
                    f"ActiveState: {active}\n"
                    f"Threshold: {CRASHLOOP_THRESHOLD} restarts/{COOLDOWN_MIN // 60}h\n"
                    f"Action: investigate — systemd is masking repeated failures.",
                    severity="error",
                )
                state["last_alerted"][svc] = datetime.now(timezone.utc).isoformat()
            summary.append(f"{svc}: CRASHLOOP delta={delta} total={nrestarts}")
        else:
            summary.append(f"{svc}: ok (delta={delta}, total={nrestarts}, {active})")

    save_state(state)
    print(f"[{pst_now()}] " + " | ".join(summary))


if __name__ == "__main__":
    main()
