---
name: competition-score
description: Score and finalize a bot trading competition. Reads all portfolio files, force-closes open positions at current Kraken prices, ranks bots by total return, and optionally archives results. Run at competition end.
---

# competition-score

Scores a competition at its end. Force-closes any open positions at market, ranks bots, and outputs final results.

## Usage

```
python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py <comp_id> [--archive]
```

## Examples

```bash
# Score without archiving (preview)
python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py comp-20260303-1400

# Score and archive (use at true competition end)
python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py comp-20260303-1400 --archive
```

## Output

Returns JSON with rankings:
```json
{
  "comp_id": "comp-20260303-1400",
  "scored_at": "2026-03-03T18:01:00Z",
  "duration_hours": 4.0,
  "pairs": ["BTC/USD", "ETH/USD"],
  "winner": "bjorn",
  "rankings": [
    {
      "rank": 1,
      "bot": "bjorn",
      "final_equity": 10432.00,
      "total_pnl_usd": 432.00,
      "total_pnl_pct": 4.32,
      "total_trades": 5,
      "wins": 4,
      "losses": 1,
      "win_rate": 80.0,
      "max_drawdown_pct": 1.2,
      "open_positions_force_closed": 0
    }
  ]
}
```

## With --archive

Moves competition from active/ to results/, writes final_score.json. Removes from active.
