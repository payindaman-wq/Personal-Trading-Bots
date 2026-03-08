---
name: competition-tick
description: Core rule engine for bot competitions. Runs every 5 minutes via cron. Finds the active competition, fetches live Kraken prices, evaluates each bot's strategy.yaml rules, executes trades, and auto-scores when the competition window expires. No API calls required -- pure Python rule evaluation.
---

# competition-tick

Runs automatically via cron every 5 minutes. You do not call this manually.

## What it does each tick

1. Checks for an active competition in `competition/active/`
2. Fetches live prices from Kraken
3. Appends prices to `price_history.json` (used for indicator calculation)
4. For each bot (floki, bjorn, lagertha):
   - Checks risk limits (paused/stopped state)
   - Checks open positions for exit conditions (target / stop / timeout)
   - Checks entry conditions against strategy.yaml rules
   - Executes trades via trade-execute skill
5. At competition end: auto-runs competition-score --archive

## Cron schedule

*/5 * * * * python3 /root/.openclaw/skills/competition-tick/scripts/competition_tick.py >> /root/.openclaw/workspace/competition/cron.log 2>&1

## Log files

- Per-competition: `competition/active/{comp_id}/tick.log`
- Cron output: `competition/cron.log`

## Dry run (test without executing trades)

python3 /root/.openclaw/skills/competition-tick/scripts/competition_tick.py --dry-run

## Adding a new bot

1. Create `fleet/{bot-name}/strategy.yaml` following the schema
2. Add bot name to meta.json bots list when starting the next competition
No code changes needed.

## strategy.yaml schema

name: bot-name
style: scalper | momentum | mean_reversion
pairs: [BTC/USD, ETH/USD]
position:
  size_pct: 20        # % of cash per trade
  max_open: 1         # max simultaneous positions
  fee_rate: 0.001     # 0.1% per leg
entry:
  long:
    conditions:
      - indicator: price_change_pct | trend | momentum_accelerating
        period_minutes: 5
        operator: lt | gt | eq | in
        value: -0.4
  short:
    conditions: [...]
exit:
  take_profit_pct: 0.5
  stop_loss_pct: 0.3
  timeout_minutes: 30
risk:
  pause_if_down_pct: 3
  pause_minutes: 60
  stop_if_down_pct: 8
