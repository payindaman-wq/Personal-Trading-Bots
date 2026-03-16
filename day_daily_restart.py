#!/usr/bin/env python3
"""
day_daily_restart.py - Daily 10:00 UTC (2:00am PST) restart for Day Trading League.

Called by cron: 0 10 * * *

Logic:
  - If no active sprint: start new 24h sprint immediately.
  - If active sprint >= 20h old: expire it by patching duration_hours so the
    tick archives it on its next run; watchdog restarts within 10 min.
  - If active sprint < 20h old: skip (sprint started recently today, keep it).
"""
import os
import json
import subprocess
from datetime import datetime, timezone

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
ACTIVE_DIR   = os.path.join(WORKSPACE, "competition", "active")
START_SCRIPT = "/root/.openclaw/skills/competition-start/scripts/competition_start.py"


def find_active():
    if not os.path.isdir(ACTIVE_DIR):
        return None, None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None, None
    comp_dir  = os.path.join(ACTIVE_DIR, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None, None
    with open(meta_path) as f:
        meta = json.load(f)
    return (comp_dir, meta) if meta.get("status") == "active" else (None, None)


def hours_running(meta):
    started = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - started).total_seconds() / 3600


def start_new():
    result = subprocess.run(
        ["python3", START_SCRIPT, "24"],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        print(f"  Started: {data['comp_id']}")
    else:
        print(f"  ERROR starting: {result.stderr[:300]}")


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[day_daily_restart] {now}")

    comp_dir, meta = find_active()

    if meta is None:
        print("  No active sprint — starting new 24h sprint.")
        start_new()
        return

    elapsed = hours_running(meta)
    print(f"  Active: {meta['comp_id']}  ({elapsed:.1f}h elapsed)")

    if elapsed >= 20.0:
        print(f"  Sprint >= 20h — patching to expire now. Tick will archive; watchdog restarts.")
        meta["duration_hours"] = round(elapsed - 0.01, 4)
        with open(os.path.join(comp_dir, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)
    else:
        print(f"  Sprint < 20h old — keeping current sprint.")


if __name__ == "__main__":
    main()
