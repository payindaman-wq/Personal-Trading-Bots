# Cross-Pair Spread Trader

## Position
**Rank:** League Competitor (Specialist)
**Reports To:** SYN (Commander) via swing competition engine
**Oversees:** Nothing — executes only
**League:** Swing Trading — 7-day sprints (specialist division)
**Exchange:** Kraken (spot, multiple pairs)
**Status:** Pending

## Primary Objective
Exploit persistent pricing inefficiencies and relative strength differentials
across multiple crypto pairs within a single market session. Unlike stat arb
(which trades mean-reversion of a stable ratio), the cross-pair spread trader
actively rotates capital toward the strongest-performing assets in the fleet's
pair universe and away from the weakest.

## Core Concept
At any given time within a sprint, some assets in the pair universe are
outperforming others on a relative basis. The cross-pair spread trader:
1. Ranks all available pairs by relative momentum (e.g., 4h return vs BTC)
2. Goes long the top N assets
3. Exits positions that fall out of the top N
4. Hedges total crypto exposure by sizing against BTC (the benchmark)

This is a relative value strategy — the bet is always "this asset beats BTC"
or "this asset beats the pair average", not "crypto goes up."

## Pair Universe
Same 16 pairs as day/swing leagues. BTC/USD serves as the benchmark for
relative performance calculations.

## Responsibilities
- Calculate relative performance of each pair vs BTC on each tick
- Maintain ranked list of pairs by relative momentum
- Enter long positions in top-ranked pairs (above threshold)
- Exit positions in pairs that fall below threshold
- Never exceed 3 concurrent positions
- Track entry vs BTC price at time of entry for relative P&L calculation

## Rotation Logic (Proposed)
- Ranking metric: (pair_return_4h - BTC_return_4h) — excess return vs BTC
- Entry threshold: excess return > +2% over 4h
- Exit threshold: excess return falls below 0% (losing to BTC)
- Rebalance frequency: every 30 minutes (matches swing tick)

## Risk Parameters (Proposed)
- Max concurrent positions: 3
- Max single position: 33% of portfolio
- Stop loss per position: 5% vs entry price
- Max drawdown: 15%
- BTC correlation override: if all pairs are down >3% in 1h, go to cash

## Key Differences from Other Strategies
- No fixed directional bias — can end a sprint 100% in cash if nothing
  clears the relative threshold
- High turnover potential vs other swing bots — more like systematic
  day trading with swing sizing
- Accounting tracks each rotation as a separate trade (frequent taxable events)
- Does not require short-selling — all positions are spot long vs BTC benchmark

## Chain of Command Note
Competes in swing league for scoring consistency, but the rotation cadence
may behave more like a day bot in active markets. SYN monitors position
count and flags to operator if bot is churning excessively (sign of
over-fitting or noisy signals).

## Prerequisites Before Building
- Relative performance calculation infrastructure
- Clear ranking/threshold rules validated in backtest
- Accounting configured to handle high-frequency position rotation
