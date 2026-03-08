---
name: swing-start
description: Start a new swing trading competition (7-day sprint). All swing bots compete with hourly candle data. Use this when the user asks to start a swing competition or swing sprint.
---

# swing-start

Initializes a 7-day swing trading competition for the Viking Fleet swing bots.
Runs in parallel with the day trading league — completely independent.

## Usage

```bash
# Start a 7-day sprint (default)
python3 /root/.openclaw/workspace/swing_competition_start.py

# Custom duration
python3 /root/.openclaw/workspace/swing_competition_start.py 336  # 14 days

# Custom pairs
python3 /root/.openclaw/workspace/swing_competition_start.py --pairs BTC/USD ETH/USD SOL/USD
```

## Notes

- Swing bots live in: /root/.openclaw/workspace/fleet/swing/
- Active comp: /root/.openclaw/workspace/competition/swing/active/
- Results:     /root/.openclaw/workspace/competition/swing/results/
- Tick runs every 30 min automatically via cron
- Default duration: 168 hours (7 days)
- Default pairs: BTC/USD ETH/USD SOL/USD XRP/USD AVAX/USD LINK/USD AAVE/USD
