# Statistical Arbitrage Trader

## Position
**Rank:** League Competitor (Specialist)
**Reports To:** SYN (Commander) via swing competition engine
**Oversees:** Nothing — executes only
**League:** Swing Trading — 7-day sprints (specialist division)
**Exchange:** Kraken (spot, both legs)
**Status:** Pending

## Primary Objective
Identify and exploit statistical pricing relationships between correlated
crypto asset pairs. Enter market-neutral positions (long one asset, short
the correlated asset) when the spread between them deviates beyond historical
norms, and exit when the spread reverts. Profit is derived from the
relationship, not the direction of either asset.

## Core Concept
If BTC and ETH historically move together with a stable price ratio, and
that ratio temporarily breaks down, the stat arb bot:
1. Buys the underperformer
2. Shorts the outperformer (requires futures or margin for the short leg)
3. Holds until the ratio normalizes
4. Exits both legs simultaneously

This is directionally neutral — macro moves that hit both assets equally
do not hurt the position.

## Target Pair Relationships (Research Required)
- BTC/ETH spread (most liquid, tightest relationship)
- ETH/SOL spread
- SOL/AVAX spread
- Large-cap vs mid-cap basket spreads

## Responsibilities
- Continuously monitor spread Z-score between target pairs
- Enter when Z-score exceeds entry threshold (e.g. ±2.0 standard deviations)
- Exit when Z-score reverts to mean (e.g. ±0.5)
- Track both legs of every trade — Accounting records each leg separately
- Monitor correlation stability — if correlation breaks down, exit and pause

## Risk Parameters (Proposed)
- Max spread deviation before forced exit: ±4.0 standard deviations
- Max holding period: 7 days (if no reversion, cut the trade)
- Position sizing: equal notional on each leg (true market neutrality)
- Correlation lookback: 30-day rolling window
- Min correlation threshold to enter: 0.75 (don't trade low-correlation pairs)

## Key Differences from Directional Strategies
- Two-legged trades — Accounting must track both legs for each trade ID
- P&L depends on spread convergence, not asset price direction
- Lower expected return per trade, but lower variance (market neutral)
- Macro Governor signals are less critical — RED macro still means caution,
  but stat arb is less exposed to directional moves than trend followers

## Chain of Command Note
Competes in swing league but operates on a fundamentally different model
than directional swing bots. SYN scores on same P&L basis (return on
capital) but evaluates separately for funding (different risk profile,
requires margin/futures capability for short leg).

## Prerequisites Before Building
- Proven correlation data for selected pairs
- Access to short-selling (Kraken margin or futures for short leg)
- Accounting bot configured to handle two-legged trade pairs
- Spread Z-score calculation infrastructure
