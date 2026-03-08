# MEMORY.md - Long-Term Memory

## Identity
- Name: SYN
- Role: Commander of the Viking Trading Fleet
- I orchestrate competitions. I do not trade.

## About Chris
- Crypto trader building a bot competition framework
- Partner: Bryan (shares coldstoneadmin GitHub)
- Timezone: PST
- Wants concise, autonomous operation

## The Viking Fleet (8 bots total, all under SYN)
**Active strategies:**
- Floki: scalper (1-5 min, many small trades)
- Bjorn: momentum (15-30 min, charges hard on breakouts)
- Lagertha: mean reversion (15-60 min, fades overextended moves)

**Pending strategies (to be assigned):**
- Ragnar, Leif, Ivar, Harald, Freydis

Strategy files: /root/.openclaw/workspace/fleet/{bot-name}/strategy.yaml

## Competition Framework
- Format: 3-8 hour paper trading sprints, all bots compete simultaneously
- Capital: $10,000 per bot (virtual)
- Pairs: BTC/USD, ETH/USD (Kraken prices)
- Scoring: total return % wins; Sharpe-equiv and win rate as tiebreakers
- Workspace: /root/.openclaw/workspace/competition/
  - Active: competition/active/{comp_id}/portfolio-{botname}.json
  - Results: competition/results/
- Competition ID format: comp-YYYYMMDD-HHMM (UTC)

## Funding Criteria
- Win 2/3 or 3/5 competitions
- Positive return in all comps
- Max drawdown within stated risk limits
- Chris approves before any bot goes live -- no auto-deployment

## Tools
- Kraken prices: python3 /root/.openclaw/skills/kraken-price/scripts/get_prices.py XBTUSD ETHUSD
- Repo: https://github.com/coldstoneadmin/crypto-trading-toolkit

## Paper Trading Sims (ending 2026-03-28, NOT going live)
- chris-btc, chris-crypto, chris-stocks
- Monitored by monitor_sims.py, alerts sent to Telegram
- These are being abandoned in favor of the competition framework
