#!/usr/bin/env python3
"""
polymarket_cycle_advance.py - Advance to the next Polymarket competition cycle.

Run after reviewing and adjusting non-profitable bot strategies.
Archives current cycle results, increments cycle number, resets sprint count,
then immediately starts Sprint 1 of the new cycle so the tick has valid
sprint timing and cannot re-archive the old expired sprint.

Usage: python3 polymarket_cycle_advance.py
"""
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
import cycle_ledger

WORKSPACE    = "/root/.openclaw/workspace"
CYCLE_STATE  = os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_cycle_state.json")
RESULTS_DIR  = os.path.join(WORKSPACE, "competition", "polymarket", "auto_results")
ARCHIVE_DIR  = os.path.join(WORKSPACE, "competition", "polymarket", "archive")
SPRINT_START = os.path.join(WORKSPACE, "polymarket_sprint_start.py")

with open(CYCLE_STATE) as f:
    state = json.load(f)

old_cycle = state["cycle"]
new_cycle = old_cycle + 1

# Archive current cycle results
archive_dest = os.path.join(ARCHIVE_DIR, f"cycle-{old_cycle}")
if os.path.isdir(RESULTS_DIR) and os.listdir(RESULTS_DIR):
    os.makedirs(archive_dest, exist_ok=True)
    for entry in os.listdir(RESULTS_DIR):
        shutil.move(os.path.join(RESULTS_DIR, entry), os.path.join(archive_dest, entry))
    print(f"Archived Polymarket Cycle {old_cycle} results to {archive_dest}")

# Advance cycle state
state["cycle"]            = new_cycle
state["sprint_in_cycle"]  = 0
state["cycle_started_at"] = None
state["status"]           = "active"
state["sprints"]          = []

with open(CYCLE_STATE, "w") as f:
    json.dump(state, f, indent=2)
try:
    cycle_ledger.emit("polymarket", "cycle_advanced",
                      **{"from": old_cycle, "to": new_cycle})
except Exception as _e:
    print(f"  [ledger] emit failed (cycle_advanced polymarket): {_e}")

print(f"Polymarket cycle advanced: {old_cycle} -> {new_cycle}")

# Immediately start Sprint 1 so the tick sees valid sprint_ends_at
# and cannot fall into a re-archive loop on the old expired sprint.
print("Starting Cycle " + str(new_cycle) + " Sprint 1...")
result = subprocess.run(["python3", SPRINT_START], capture_output=True, text=True)
if result.returncode == 0:
    data = json.loads(result.stdout)
    print(f"Sprint 1 started: {data['sprint_id']} — ends {data['sprint_ends_at'][:16]} UTC")
else:
    print(f"ERROR starting sprint: {result.stderr}")
    raise SystemExit(1)
