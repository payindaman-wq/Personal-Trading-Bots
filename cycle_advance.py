#!/usr/bin/env python3
"""
cycle_advance.py - Advance to the next competition cycle.

Run after reviewing and adjusting non-profitable bot strategies.
Resets sprint_in_cycle to 0, increments cycle number, archives previous cycle results.

Usage: python3 cycle_advance.py
"""
import json
import os
import shutil
from datetime import datetime, timezone

WORKSPACE    = "/root/.openclaw/workspace"
CYCLE_STATE  = os.path.join(WORKSPACE, "competition", "cycle_state.json")
RESULTS_DIR  = os.path.join(WORKSPACE, "competition", "results")
ARCHIVE_DIR  = os.path.join(WORKSPACE, "competition", "archive")

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
    print(f"Archived Cycle {old_cycle} results to {archive_dest}")

# Update state
state["cycle"]            = new_cycle
state["sprint_in_cycle"]  = 0
state["cycle_started_at"] = None
state["status"]           = "active"
state["sprints"]          = []

with open(CYCLE_STATE, "w") as f:
    json.dump(state, f, indent=2)

print(f"Cycle advanced: {old_cycle} -> {new_cycle}")
print(f"Next sprint starts at 2:00 AM PST (10:00 UTC)")
