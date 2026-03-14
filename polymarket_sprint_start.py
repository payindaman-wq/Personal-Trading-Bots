#!/usr/bin/env python3
"""
polymarket_sprint_start.py - Start the next Polymarket sprint.
Called by the weekly Sunday cron. Resets all bot portfolios and sets
new sprint timing in auto_state.json. Updates polymarket_cycle_state.json.

Usage: python3 polymarket_sprint_start.py
"""
import json
import os
from datetime import datetime, timezone, timedelta

WORKSPACE    = "/root/.openclaw/workspace"
AUTO_STATE   = os.path.join(WORKSPACE, "competition", "polymarket", "auto_state.json")
CYCLE_STATE  = os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_cycle_state.json")
SPRINT_HOURS = 168  # 7 days

with open(AUTO_STATE) as f:
    state = json.load(f)

with open(CYCLE_STATE) as f:
    cs = json.load(f)

if cs.get("status") == "awaiting_review":
    print("ERROR: Cycle is awaiting strategy review. Run polymarket_cycle_advance.py first.")
    raise SystemExit(1)

now       = datetime.now(timezone.utc)
sprint_id = f"poly-auto-{now.strftime('%Y%m%d-%H%M')}"
ends_at   = now + timedelta(hours=SPRINT_HOURS)

next_sprint_num = cs["sprint_in_cycle"] + 1

# Reset all bots
for bot in state["bots"]:
    bot["cash"]          = bot.get("starting_capital", 1000.0)
    bot["equity"]        = bot.get("starting_capital", 1000.0)
    bot["pnl_usd"]       = 0.0
    bot["pnl_pct"]       = 0.0
    bot["total_trades"]  = 0
    bot["wins"]          = 0
    bot["losses"]        = 0
    bot["positions"]     = {}
    bot["closed_trades"] = []
    bot["scan_count"]    = 0
    bot["gemini_calls"]  = 0
    bot["last_scan_at"]  = None

state["sprint_id"]         = sprint_id
state["sprint_started_at"] = now.isoformat()
state["sprint_ends_at"]    = ends_at.isoformat()
state["status"]            = "active"
state["cycle"]             = cs["cycle"]
state["sprint_in_cycle"]   = next_sprint_num
state["generated_at"]      = now.isoformat()

with open(AUTO_STATE, "w") as f:
    json.dump(state, f, indent=2)

# Update cycle state
cs["sprint_in_cycle"] = next_sprint_num
if cs.get("cycle_started_at") is None:
    cs["cycle_started_at"] = now.isoformat()
cs.setdefault("sprints", []).append(sprint_id)

with open(CYCLE_STATE, "w") as f:
    json.dump(cs, f, indent=2)

print(json.dumps({
    "sprint_id":       sprint_id,
    "sprint_ends_at":  ends_at.isoformat(),
    "cycle":           cs["cycle"],
    "sprint_in_cycle": next_sprint_num,
    "sprints_per_cycle": cs["sprints_per_cycle"],
}))
