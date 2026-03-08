# MEMORY.md - Long-Term Memory

## Identity
- Name: SYN
- Role: Commander of the Viking Trading Fleet
- I orchestrate competitions, show standings, and start sprints. I do not trade.

## About Chris
- Crypto trader building a bot competition framework
- Partner: Bryan (shares coldstoneadmin GitHub)
- Timezone: PST (Reno, NV)
- Wants concise, autonomous operation

## The Viking Fleet — All 8 Strategies COMPLETE

All strategy.yaml files are fully written and backtested. Do NOT treat them as placeholders.

| Bot      | Style                       | Inspired By          | Key Indicators Used         |
|----------|-----------------------------|----------------------|-----------------------------|
| Floki    | Multi-TF confluence scalper | Daan Crypto Trades   | RSI, EMA, trend             |
| Bjorn    | EMA + MACD momentum         | Crypto Tony          | EMA, MACD, RSI, trend 240m  |
| Lagertha | VWAP trend directional      | TheWhiteWhaleHL      | VWAP, EMA, trend 60m+240m   |
| Ragnar   | VWAP reclaim                | VWAP reclaim method  | VWAP, trend, RSI, MACD      |
| Leif     | BB squeeze breakout         | Rekt Capital         | BB, MACD, trend 30m+240m    |
| Ivar     | High conviction momentum    | James Wynn (safe)    | trend 15m+60m+240m, EMA, MACD |
| Harald   | RSI + trend composite       | Scott Melker         | RSI, trend, VWAP            |
| Freydis  | Contrarian extreme reversal | GCRClassic           | RSI, BB, price_change_pct   |

Strategy files: /root/.openclaw/workspace/fleet/{bot}/strategy.yaml

## Competition Framework
- Format: 4-hour sprints, multiple sprints, CUMULATIVE scoring across all sprints
- Capital: 0,000 per bot (virtual)
- Pairs: BTC/USD, ETH/USD, SOL/USD, XRP/USD, DOGE/USD, AVAX/USD, LINK/USD (and more)
- Points: 1st=8pts | 2nd=5pts | 3rd=3pts | 4th-8th=1pt per sprint
- Primary rank: cumulative P&L across all sprints
- Workspace: /root/.openclaw/workspace/competition/
  - Active: competition/active/{comp_id}/portfolio-{botname}.json
  - Results: competition/results/
- Leaderboard: python3 /root/.openclaw/workspace/leaderboard.py

## Starting a Competition
python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 4
(starts 4-hour sprint with all 8 bots on default 7 pairs)

## Available Indicators (in strategy conditions)
price_change_pct, trend, momentum_accelerating, price_vs_vwap,
rsi, price_vs_ema, bollinger_position, macd_signal

## Funding Criteria
- Best cumulative P&L across multi-sprint series wins
- Max drawdown within risk limits per strategy
- Chris approves before any bot goes live -- no auto-deployment

## Tools
- Leaderboard: python3 /root/.openclaw/workspace/leaderboard.py
- Start sprint: python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py <hours>
- Backtest: python3 /root/.openclaw/workspace/backtest.py --bot <name> --days 30
- Kraken prices: python3 /root/.openclaw/skills/kraken-price/scripts/get_prices.py XBTUSD ETHUSD
- Repo: https://github.com/coldstoneadmin/crypto-trading-toolkit

## Source of Truth
- Strategies come from: /root/.openclaw/workspace/fleet/{bot}/strategy.yaml
- Do NOT edit strategy files directly -- changes come from Claude Code sessions with Chris
- Do NOT update MEMORY.md yourself -- Claude Code maintains it
