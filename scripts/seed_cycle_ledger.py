"""
seed_cycle_ledger.py — one-shot migration: write a `cycle_baseline` event per
league capturing the current on-disk cycle_state.json. Ledger starts "from now"
with no historical backfill.

Idempotent: running twice just appends another baseline event; materialize()
uses the MOST RECENT baseline as the starting point.

Usage:
  python3 scripts/seed_cycle_ledger.py              # seed all 5 leagues
  python3 scripts/seed_cycle_ledger.py day swing    # seed subset
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cycle_ledger


def seed_league(league: str) -> dict:
    cs_path = cycle_ledger._cycle_state_path(league)
    if not os.path.isfile(cs_path):
        raise FileNotFoundError(f"no cycle_state file for {league}: {cs_path}")
    with open(cs_path) as f:
        cs = json.load(f)
    ev = cycle_ledger.emit(
        league,
        "cycle_baseline",
        cycle=cs.get("cycle", 1),
        sprint_in_cycle=cs.get("sprint_in_cycle", 0),
        sprints_per_cycle=cs.get("sprints_per_cycle", 7),
        status=cs.get("status", "active"),
        cycle_started_at=cs.get("cycle_started_at"),
        sprints=cs.get("sprints", []),
    )
    return ev


def main():
    leagues = sys.argv[1:] or list(cycle_ledger.LEAGUE_PATHS.keys())
    for lg in leagues:
        try:
            ev = seed_league(lg)
            # Verify materialize produces same state as on-disk
            drift = cycle_ledger.drift(lg)
            status = "OK" if not drift else f"DRIFT: {drift}"
            print(f"[seed] {lg}: cycle={ev['cycle']} "
                  f"sprint_in_cycle={ev['sprint_in_cycle']} "
                  f"sprints={ev['sprints']} -> {status}")
        except Exception as e:
            print(f"[seed] {lg}: FAILED — {e}")


if __name__ == "__main__":
    main()
