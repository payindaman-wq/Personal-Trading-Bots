# Spot Day Trader

## Position
**Rank:** League Competitor
**Reports To:** SYN (Commander) via competition engine
**Oversees:** Nothing — executes only
**League:** Day Trading — 4-hour sprints
**Exchange:** Kraken (spot, no leverage)
**Status:** Live

## Primary Objective
Compete in 4-hour paper trading sprints across a shared pool of crypto pairs.
Generate the highest risk-adjusted return within the sprint window. The bot
with the best cumulative competition score earns live capital allocation from
the operator.

## Active Roster (12 bots)

| Bot | Strategy Style |
|-----|----------------|
| Floki | Multi-TF Confluence Scalper |
| Bjorn | EMA + MACD Momentum |
| Lagertha | VWAP Trend Directional |
| Ragnar | VWAP Reclaim |
| Leif | BB Squeeze Breakout |
| Gunnar | Aggressive Momentum Scalper |
| Harald | RSI + Trend Composite |
| Freydis | Contrarian Extreme Reversal |
| Sigurd | Altcoin Momentum Rotation |
| Astrid | RSI Mean Reversion Scalper |
| Ulf | Breakout Retest Scalper |
| Bjarne | Trend Pullback Buyer |

## Sprint Rules
- Duration: 4 hours
- Starting capital: $10,000 (paper)
- Pairs available: BTC/USD, ETH/USD, SOL/USD, XRP/USD, DOGE/USD, AVAX/USD,
  LINK/USD, UNI/USD, AAVE/USD, NEAR/USD, APT/USD, SUI/USD, ARB/USD, OP/USD,
  WIF/USD, PEPE/USD
- Max concurrent positions: 3
- Max single position: 40% of portfolio
- Daily loss limit: 5% (auto-pause)
- Max drawdown: 15% (auto-disqualify)
- Tick frequency: every 5 minutes

## Scoring (per sprint)
- 1st: 8 points
- 2nd: 5 points
- 3rd: 3 points
- 4th+: 1 point
- Cumulative points across sprints determine funding eligibility

## Responsibilities (per bot)
- Evaluate market indicators on each 5-minute tick
- Apply YAML strategy rules deterministically (no LLM per tick)
- Emit BUY/SELL/HOLD signals with position sizing
- Respect all risk limits — never override them

## Indicators Available
price_change_pct, trend, momentum_accelerating, price_vs_vwap, rsi,
price_vs_ema, bollinger_position, macd_signal

## History Window
360 minutes rolling (covers MACD + 240-minute trend lookback)

## Path to Live Capital
1. Win or consistently place top-3 across multiple sprints
2. Operator reviews results and approves funding
3. Bot transitions from paper to live Kraken API with hard position limits
4. Accounting bot intercepts all realized P&L before reinvestment
