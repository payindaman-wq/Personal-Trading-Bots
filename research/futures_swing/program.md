# ODIN Research Program — FUTURES SWING

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (applied automatically in backtest)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage

## Research Objective
Evolve strategies that are profitable net of leverage costs and survive real futures mechanics.
Leverage amplifies returns but also amplifies losses — prefer strategies with:
- Tight stop losses (max 3% for day, 5% for swing) to prevent liquidation
- Limited position hold time to minimize funding drag
- Strong edge (Sharpe > 1.5 after leverage costs)

## Current Focus
- Establish baseline: find strategies that survive 2x leverage without frequent liquidations
- Explore: which entry conditions work best when scaled by leverage
- Avoid: strategies that rely on holding through large drawdowns (liquidation risk)

## Key Insight
A strategy that works in spot but has frequent 30%+ adverse moves is NOT viable in futures
at 2x leverage. Prioritize strategies with tight, consistent wins over high-variance home runs.
