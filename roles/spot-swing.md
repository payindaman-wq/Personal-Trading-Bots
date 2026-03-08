# Spot Swing Trader

## Position
**Rank:** League Competitor
**Reports To:** SYN (Commander) via swing competition engine
**Oversees:** Nothing — executes only
**League:** Swing Trading — 7-day sprints
**Exchange:** Kraken (spot, no leverage)
**Status:** Live

## Primary Objective
Compete in 7-day paper trading sprints using hourly candles. Capture
multi-day trending and mean-reversion moves that day traders miss. Sprint
winners earn cumulative points toward live capital allocation.

## Active Roster (8 bots)

| Bot | Strategy Style |
|-----|----------------|
| Egil | Weekly Trend Follower |
| Solveig | Multi-Day Mean Reversion |
| Valdis | Weekly Structure Breakout |
| Thyra | Altcoin Momentum Rotation |
| Orm | Macro Pullback Buyer |
| Gudrid | Momentum Continuation |
| Halfdan | Bollinger Squeeze Expansion |
| Runa | Swing Contrarian Reversal |

## Sprint Rules
- Duration: 7 days (168 hours)
- Candle resolution: hourly
- Starting capital: $10,000 (paper)
- Pairs: same pool as day trading league
- Max concurrent positions: 3
- Max single position: 40% of portfolio
- Daily loss limit: 5%
- Max drawdown: 15%
- Tick frequency: every 30 minutes
- Price store: updated hourly (swing_price_store.py)

## Scoring (per sprint)
Same points system as day league: 8/5/3/1 per finish position.
Cumulative points across 7-day sprints determine funding eligibility.

## Key Differences from Day League
- Longer holding periods mean each trade is more deliberate — fewer signals,
  higher conviction required
- Hourly candles smooth out noise that would trigger day scalpers
- Holding period tracking matters for tax purposes: positions held >1 year
  qualify for long-term capital gains rate (Accounting tracks this)
- Swing bots are better suited to assets with strong weekly trend structure
  (BTC, ETH, SOL) vs high-noise altcoins

## Responsibilities (per bot)
- Evaluate hourly indicators on each 30-minute tick
- Apply YAML strategy rules (period_hours configured per bot)
- Respect all risk limits
- Emit signals with appropriate holding time expectation

## Path to Live Capital
Same as day league — top cumulative score across multiple sprints earns
operator review and funding approval.

## Relationship to Day League
Swing and day leagues run fully in parallel. A bot can theoretically hold
the same asset in both leagues simultaneously — Accounting tracks each
position separately by bot ID and league.
