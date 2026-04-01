# crypto-trading-toolkit

A paper trading competition framework for systematic crypto strategy development. Multiple bots compete in daily and weekly sprints. Winners get funded on Kraken.

## How It Works

The engine is pure Python with deterministic YAML rule evaluation — zero LLM cost per tick. Bots define their logic entirely in `strategy.yaml` files. A cron-driven tick loop evaluates every bot's rules against live price data, executes paper trades, and updates leaderboards.

Research agents (ODIN, FREYA) run continuously in the background, evolving strategies via LLM-guided mutation and backtesting against historical data. MIMIR reviews results at generation milestones. LOKI applies safe constant changes autonomously.

## Leagues

| League | Tick | Sprint | Pairs |
|--------|------|--------|-------|
| Day | 5 min | 24h | 16 crypto/USD |
| Swing | 30 min | 7 days | 16 crypto/USD |
| Arb | 30 min | 7 days | Cross-pair statistical arb |
| Spread | 30 min | 7 days | Cointegrated pair spreads |
| Polymarket | 15 min | 7 days | Prediction markets (USDC) |

Starting capital: $1,000 per bot per sprint.

## Bot Fleet

**Day league** (12 bots): Floki, Bjorn, Lagertha, Ragnar, Leif, Gunnar, Harald, Freydis, Sigurd, Astrid, Ulf, Bjarne

**Swing league** (9 bots): Egil, Solveig, Orm, Gudrid, Halfdan, Thyra, Valdis, Runa, Ivar

**Polymarket** (12 bots): Hermod, Tora, Njal, Skadi, Hlin, Gerd, Var, Eir, Muninn, Mist, Kara, Thrud

## Research Layer (Executive Staff)

| Agent | Role | Model |
|-------|------|-------|
| ODIN | Crypto Strategy Officer — evolves day/swing strategies | Gemini 2.5 Flash Lite |
| FREYA | Prediction Markets Strategy Officer — evolves PM strategies | Gemini 2.5 Flash Lite |
| MIMIR | Analysis Officer — deep review at generation milestones | Claude Sonnet 4.6 |
| LOKI | Implementation Officer — applies safe changes autonomously | Claude Haiku |
| SYN | Operations Officer — monitors fleet, alerts via Telegram | Claude Haiku |

## Architecture

```
competition_tick.py       — day league tick (cron, every 5 min)
swing_competition_tick.py — swing league tick (cron, every 30 min)
polymarket_syn_tick.py    — polymarket tick (systemd, every 15 min)
sys_heartbeat.py          — health monitor + auto-remediation (every 30 min)
league_watchdog.py        — stale sprint detection + restart (every 10 min)
day_daily_restart.py      — daily sprint reset at 09:00 UTC
weekly_league_restart.py  — weekly reset, injects ODIN swing strategy

research/
  odin_researcher_v2.py   — ODIN mutation loop (day + swing)
  freya_researcher.py     — FREYA mutation loop (prediction markets)
  mimir.py                — deep analysis at generation milestones
  loki.py                 — autonomous safe-change implementation

fleet/{bot}/strategy.yaml — per-bot strategy definitions
```

## Strategy Format

Each bot's behavior is fully defined by its `strategy.yaml`. No code changes needed for strategy tuning.

```yaml
name: floki
style: momentum_scalper
pairs:
  - BTC/USD
  - ETH/USD
  # ...
position:
  size_pct: 15
  max_open: 3
entry:
  long:
    conditions:
      - indicator: trend
        operator: eq
        value: up
      # ...
exit:
  # ...
```

See `fleet/floki/strategy.yaml` for a fully documented example.

## Available Indicators (Day League)

`price_change_pct`, `trend`, `momentum_accelerating`, `price_vs_vwap`, `rsi`, `price_vs_ema`, `bollinger_position`, `macd_signal`

History window: 360 minutes rolling.

## Deployment

See [DEPLOY.md](DEPLOY.md) for full setup instructions including VPS requirements, cron configuration, and the live trading checklist.

## Live Trading Checklist (Before Funding Any Bot)

- [ ] LLC formed and EIN obtained
- [ ] Kraken business account opened under LLC
- [ ] Bot has 10+ sprint history with consistent profitability
- [ ] Kill switch configured (15% drawdown from peak = auto-pause)
- [ ] `trade-execute` skill tested in dry-run mode

## Operations

Monitoring is handled by SYN via Telegram. SYN alerts on problems only — no routine status spam.

```bash
# Manual leaderboard check
python3 leaderboard.py

# Backtest a specific bot
python3 backtest.py --bot floki --days 30

# Recover a broken sprint
python3 sprint_backfill.py
```
