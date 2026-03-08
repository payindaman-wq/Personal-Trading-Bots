---
name: competition-start
description: Initialize a new bot trading competition. Creates portfolio files for Floki, Bjorn, and Lagertha, and returns the competition ID. Run this before spawning bot subagents.
---

# competition-start

Initializes a paper trading competition. Call this first, then spawn the bot subagents.

## Usage

```
python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py <duration_hours> [pair1 pair2 ...]
```

## Examples

```bash
# 4-hour competition on BTC and ETH (default)
python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 4

# 6-hour competition on BTC only
python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 6 BTC/USD
```

## Output

Returns JSON:
```json
{
  "comp_id": "comp-20260303-1400",
  "comp_dir": "/root/.openclaw/workspace/competition/active/comp-20260303-1400",
  "duration_hours": 4.0,
  "started_at": "2026-03-03T14:00:00Z",
  "pairs": ["BTC/USD", "ETH/USD"],
  "bots": ["floki", "bjorn", "lagertha"]
}
```

## What It Creates

For each bot, a portfolio file at:
  competition/active/{comp_id}/portfolio-{botname}.json

Starting capital: $10,000 per bot. Fee rate: 0.1% per trade.

## After Running This

1. Send competition start message to Telegram
2. Spawn Floki, Bjorn, Lagertha as subagents with their persona files
3. Tell each subagent their portfolio path and the comp_id
