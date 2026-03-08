---
name: swing-leaderboard
description: Show the Viking Fleet swing trading leaderboard. Displays cumulative rankings across all 7-day swing sprints by P&L, sprint wins, podiums, points, and win rate. Also shows the live active sprint if one is running. Use this when the user asks about swing bot standings or how the swing league is doing.
---

# swing-leaderboard

Displays the cumulative swing trading leaderboard for the Viking Fleet.

## Usage

```bash
# Show leaderboard (default)
python3 /root/.openclaw/workspace/swing_leaderboard.py

# Exclude active sprint from totals
python3 /root/.openclaw/workspace/swing_leaderboard.py --no-live

# Detail for one sprint
python3 /root/.openclaw/workspace/swing_leaderboard.py --sprint swing-20260310-1300
```

## The 8 Swing Bots

| Bot      | Style                        | Inspired By       |
|----------|------------------------------|-------------------|
| TBD x8   | See fleet/swing/ for roster  | Various           |

(Bots added in Stop 4 — strategy design session)

## Points System

Sprint placements award: 1st=8pts | 2nd=5pts | 3rd=3pts | 4th-8th=1pt
7-day sprints. Ranked by cumulative P&L across all sprints.
