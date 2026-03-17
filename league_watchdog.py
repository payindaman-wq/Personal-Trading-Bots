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


POLY_STATE  = os.path.join(WORKSPACE, "competition", "polymarket", "auto_state.json")
POLY_CYCLE  = os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_cycle_state.json")


def find_active(active_dir):
    """Return (meta, has_multiple) if an active sprint exists, else (None, False).
    If multiple entries exist, logs a warning and picks the newest."""
    if not os.path.isdir(active_dir):
        return None, False
    entries = sorted(os.listdir(active_dir))
    if not entries:
        return None, False
    has_multiple = len(entries) > 1
    if has_multiple:
        print(f"  WARNING: {len(entries)} entries in {active_dir} — orphaned sprints detected: {entries[:-1]}")
    comp_dir  = os.path.join(active_dir, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None, has_multiple
    with open(meta_path) as f:
        meta = json.load(f)
    result = meta if meta.get("status") == "active" else None
    return result, has_multiple


def find_polymarket_active():
    """Return sprint_id if Polymarket has an active non-expired sprint, else None.
    Returns 'awaiting_review' if cycle needs manual review (do not auto-restart)."""
    if not os.path.isfile(POLY_STATE):
        return None
    if os.path.isfile(POLY_CYCLE):
        with open(POLY_CYCLE) as f:
            cs = json.load(f)
        if cs.get("status") == "awaiting_review":
            return "awaiting_review"
    with open(POLY_STATE) as f:
        state = json.load(f)
    if state.get("status") != "active":
        return None
    ends_at = state.get("sprint_ends_at")
    if ends_at:
        end_dt = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))
        if datetime.now(timezone.utc) > end_dt:
            return None
    return state.get("sprint_id", "active")


def start_league(league):
    result = subprocess.run(
        league["start_cmd"],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            print(f"  [{league['name']}] started: {data.get('comp_id', data.get('sprint_id', '?'))}")
        except Exception:
            print(f"  [{league['name']}] started OK")
    else:
        print(f"  [{league['name']}] ERROR: {result.stderr[:300]}")


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[league_watchdog] {now}")

    for league in LEAGUES:
        meta, has_multiple = find_active(league["active_dir"])
        if meta:
            print(f"  [{league['name']}] OK — {meta['comp_id']}")
        else:
            # Guard: if active/ has any entries (even orphaned), skip restart
            active_dir = league["active_dir"]
            if os.path.isdir(active_dir) and os.listdir(active_dir):
                print(f"  [{league['name']}] WARNING: no active sprint but active/ is non-empty — skipping restart to avoid stacking")
            else:
                print(f"  [{league['name']}] IDLE — restarting...")
                start_league(league)

    # Polymarket — different active check (uses auto_state.json, not active/ dir)
    poly = find_polymarket_active()
    if poly == "awaiting_review":
        print(f"  [polymarket] awaiting_review — skipping auto-restart")
    elif poly:
        print(f"  [polymarket] OK — {poly}")
    else:
        print(f"  [polymarket] IDLE — restarting...")
        start_league({
            "name":      "polymarket",
            "start_cmd": ["python3", os.path.join(WORKSPACE, "polymarket_sprint_start.py")],
        })


if __name__ == "__main__":
    main()
