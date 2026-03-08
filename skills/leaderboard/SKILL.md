---
name: leaderboard
description: Show the Viking Fleet cumulative leaderboard across all competition sprints. Displays bot rankings by P&L, sprint wins, podiums, points, win rate, and trade count. Also shows the live active sprint standings if one is running. Use this whenever the user asks how the bots are doing, who is winning, or to see standings.
---

# leaderboard

Displays the cumulative competition leaderboard for the Viking Fleet bot competition.

## Usage

```bash
python3 /root/.openclaw/skills/leaderboard/scripts/leaderboard.py
```

## Options

```bash
# Show leaderboard (default)
python3 /root/.openclaw/skills/leaderboard/scripts/leaderboard.py

# Exclude active sprint from cumulative totals
python3 /root/.openclaw/skills/leaderboard/scripts/leaderboard.py --no-live

# Detail for one specific sprint
python3 /root/.openclaw/skills/leaderboard/scripts/leaderboard.py --sprint comp-20260308-1200
```

## The 8 Bots (Viking Fleet)

| Bot      | Style                     | Inspired By         |
|----------|---------------------------|---------------------|
| Floki    | Multi-TF confluence scalper | Daan Crypto Trades |
| Bjorn    | EMA + MACD momentum       | Crypto Tony         |
| Lagertha | VWAP trend directional    | TheWhiteWhaleHL     |
| Ragnar   | VWAP reclaim              | VWAP reclaim method |
| Leif     | BB squeeze breakout       | Rekt Capital        |
| Ivar     | High conviction momentum  | James Wynn          |
| Harald   | RSI + trend composite     | Scott Melker        |
| Freydis  | Contrarian extreme reversal | GCRClassic        |

## Points System

Sprint placements award: 1st=8pts | 2nd=5pts | 3rd=3pts | 4th-8th=1pt

The bot with the highest cumulative P&L across all sprints is the winner.
