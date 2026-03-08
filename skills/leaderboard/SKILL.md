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
python3 /root/.openclaw/skills/leaderboard/scripts/leaderboard.py --sprint comp-20260308-0829
```

## The 12 Bots (Viking Fleet)

| Bot     | Style                        | Inspired By            |
|---------|------------------------------|------------------------|
| Floki   | Multi-TF confluence scalper  | Daan Crypto Trades     |
| Bjorn   | EMA + MACD momentum          | Crypto Tony            |
| Lagertha| VWAP trend directional       | TheWhiteWhaleHL        |
| Ragnar  | VWAP reclaim                 | VWAP reclaim method    |
| Leif    | BB squeeze breakout          | Rekt Capital           |
| Gunnar  | Aggressive momentum scalper  | Gainzy (Hyperliquid)   |
| Harald  | RSI + trend composite        | Scott Melker           |
| Freydis | Contrarian extreme reversal  | GCRClassic             |
| Sigurd  | Altcoin momentum rotation    | Michaël van de Poppe   |
| Astrid  | RSI mean reversion           | Crypto Jebb            |
| Ulf     | Breakout retest precision    | The Trading Rush       |
| Bjarne  | Trend pullback buyer         | Credible Crypto        |

## Points System

Sprint placements award: 1st=8pts | 2nd=5pts | 3rd=3pts | 4th-12th=1pt

The bot with the highest cumulative P&L across all sprints is the winner.

## Competition Schedule

- Sprint 1: 24h starting 2026-03-08 08:29 UTC (all 12 bots)
- Sprints 2-20: Daily 8h at 13:00 UTC (5am PST), Mon-Sun through 2026-03-28
