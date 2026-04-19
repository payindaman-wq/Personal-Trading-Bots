#!/usr/bin/env python3
"""
session_watchdog.py - Prevents OpenClaw session context bloat.

Runs hourly via cron. Any session file exceeding SIZE_THRESHOLD_KB
is archived and its entry removed from sessions.json. OpenClaw is
then restarted so it picks up clean state.
"""

import json
import os
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_JSON   = "/root/.openclaw/agents/main/sessions/sessions.json"
ARCHIVE_DIR     = "/root/.openclaw/agents/main/sessions/archive"
LOG_FILE        = "/root/.openclaw/workspace/session_watchdog.log"
SIZE_THRESHOLD_KB = 100          # rotate sessions larger than this
BOT_TOKEN       = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID         = "8154505910"


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"{ts} {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


INBOX = "/root/.openclaw/workspace/syn_inbox.jsonl"


def send_telegram(msg: str, severity: str = "warning") -> None:
    """Write to SYN inbox. sys_heartbeat is the sole Telegram gateway."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "session_watchdog",
            "severity": severity,
            "msg":      msg[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        log(f"syn_inbox write failed: {e}")


def main() -> None:
    if not os.path.exists(SESSIONS_JSON):
        log("sessions.json not found — nothing to do")
        return

    with open(SESSIONS_JSON) as f:
        sessions: dict = json.load(f)

    Path(ARCHIVE_DIR).mkdir(parents=True, exist_ok=True)

    rotated: list[tuple[str, float]] = []

    for key, data in list(sessions.items()):
        session_file = data.get("sessionFile", "")
        if not session_file or not os.path.exists(session_file):
            continue

        size_kb = os.path.getsize(session_file) / 1024
        if size_kb < SIZE_THRESHOLD_KB:
            continue

        # Archive the bloated session file
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        archive_name = f"{os.path.basename(session_file)}.{ts}.archived"
        shutil.move(session_file, os.path.join(ARCHIVE_DIR, archive_name))
        log(f"Archived {key}: {size_kb:.1f}KB -> archive/{archive_name}")

        # Drop the entry so OpenClaw starts a fresh session next interaction
        del sessions[key]
        rotated.append((key, size_kb))

    if not rotated:
        log(f"All sessions within {SIZE_THRESHOLD_KB}KB limit — no action needed")
        return

    # Write updated sessions.json
    with open(SESSIONS_JSON, "w") as f:
        json.dump(sessions, f, indent=2)
    log("Updated sessions.json")

    # Restart OpenClaw gateway so it re-reads sessions.json from disk
    try:
        result = subprocess.run(
            ["systemctl", "--user", "restart", "openclaw-gateway.service"],
            capture_output=True, text=True, timeout=15,
            env={**os.environ, "DBUS_SESSION_BUS_ADDRESS": f"unix:path=/run/user/0/bus",
                 "XDG_RUNTIME_DIR": "/run/user/0"}
        )
        if result.returncode == 0:
            log("Restarted openclaw-gateway.service")
        else:
            log(f"Restart returned {result.returncode}: {result.stderr.strip()}")
    except Exception as e:
        log(f"Restart failed: {e}")

    # Alert
    lines = [f"  {k}: {s:.0f}KB" for k, s in rotated]
    msg = "Session watchdog rotated bloated sessions:\n" + "\n".join(lines)
    log(msg)
    # send_telegram(msg)  # silenced — routine maintenance, not actionable


if __name__ == "__main__":
    main()
