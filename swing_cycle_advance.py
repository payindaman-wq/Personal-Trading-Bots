#!/usr/bin/env python3
"""
swing_cycle_advance.py - Advance to the next swing competition cycle.

Run after reviewing and adjusting non-profitable bot strategies.
Archives current cycle results, increments cycle number, resets sprint count.

Usage: python3 swing_cycle_advance.py
"""
import json
import os
import shutil
from datetime import datetime, timezone
import cycle_ledger

WORKSPACE   = "/root/.openclaw/workspace"
CYCLE_STATE = os.path.join(WORKSPACE, "competition", "swing", "swing_cycle_state.json")
RESULTS_DIR = os.path.join(WORKSPACE, "competition", "swing", "results")
ARCHIVE_DIR = os.path.join(WORKSPACE, "competition", "swing", "archive")

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
    print(f"Archived Swing Cycle {old_cycle} results to {archive_dest}")

state["cycle"]            = new_cycle
state["sprint_in_cycle"]  = 0
state["cycle_started_at"] = None
state["status"]           = "active"
state["sprints"]          = []

with open(CYCLE_STATE, "w") as f:
    json.dump(state, f, indent=2)
try:
    cycle_ledger.emit("swing", "cycle_advanced",
                      **{"from": old_cycle, "to": new_cycle})
except Exception as _e:
    print(f"  [ledger] emit failed (cycle_advanced swing): {_e}")

print(f"Swing cycle advanced: {old_cycle} -> {new_cycle}")
print(f"Start next sprint manually: python3 {WORKSPACE}/swing_competition_start.py --cycle {new_cycle} --sprint-in-cycle 1")
