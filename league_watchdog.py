#!/usr/bin/env python3
"""
league_watchdog.py - Auto-restart leagues when no active sprint exists.

Run every 10 minutes via cron. Starts a new sprint for any league that
has no active competition running.

Cron entry:
  */10 * * * * python3 /root/.openclaw/workspace/league_watchdog.py >> /root/.openclaw/workspace/competition/watchdog.log 2>&1
"""
import os
import json
import subprocess
from datetime import datetime, timezone

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")

LEAGUES = [
    {
        "name":       "day",
        "active_dir": os.path.join(WORKSPACE, "competition", "active"),
        "start_cmd":  ["python3",
                       "/root/.openclaw/skills/competition-start/scripts/competition_start.py",
                       "24"],
    },
    {
        "name":       "swing",
        "active_dir": os.path.join(WORKSPACE, "competition", "swing", "active"),
        "start_cmd":  ["python3", os.path.join(WORKSPACE, "swing_competition_start.py")],
    },
    {
        "name":       "arb",
        "active_dir": os.path.join(WORKSPACE, "competition", "arb", "active"),
        "start_cmd":  ["python3", os.path.join(WORKSPACE, "arb_competition_start.py")],
    },
    {
        "name":       "spread",
        "active_dir": os.path.join(WORKSPACE, "competition", "spread", "active"),
        "start_cmd":  ["python3", os.path.join(WORKSPACE, "spread_competition_start.py")],
    },
]


def find_active(active_dir):
    """Return meta dict if an active sprint exists, else None."""
    if not os.path.isdir(active_dir):
        return None
    entries = sorted(os.listdir(active_dir))
    if not entries:
        return None
    comp_dir  = os.path.join(active_dir, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None
    with open(meta_path) as f:
        meta = json.load(f)
    return meta if meta.get("status") == "active" else None


def start_league(league):
    result = subprocess.run(
        league["start_cmd"],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            print(f"  [{league['name']}] started: {data.get('comp_id', '?')}")
        except Exception:
            print(f"  [{league['name']}] started OK")
    else:
        print(f"  [{league['name']}] ERROR: {result.stderr[:300]}")


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[league_watchdog] {now}")
    for league in LEAGUES:
        meta = find_active(league["active_dir"])
        if meta:
            print(f"  [{league['name']}] OK — {meta['comp_id']}")
        else:
            print(f"  [{league['name']}] IDLE — restarting...")
            start_league(league)


if __name__ == "__main__":
    main()
