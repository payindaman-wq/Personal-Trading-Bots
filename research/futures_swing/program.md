```markdown
# ODIN Research Program — FUTURES SWING

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (~0.36% per 96h hold — real drag)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage
MIN_TRADES: 400 (proposals producing fewer than 400 trades over 2 years are statistically invalid — do NOT propose changes that would reduce trade count below this floor)

## Research Objective
Evolve strategies that are profitable net of leverage costs and survive real futures mechanics.
Target: Sharpe > 1.7 after all costs. Current champion: Sharpe 1.6988.
Leverage amplifies returns AND losses — every parameter choice must account for this.

## Current Champion Summary
The current best strategy works as follows:
- Entry: trend filter (48h) confirms direction, then RSI (24h) signals mean-reversion entry
  - Long: trend=up AND RSI < 38.36
  - Short: trend=down AND RSI > 60
- Exit: 5.0% take-profit, 1.9% stop-loss, 96h timeout
- Sizing: 15.09% per position, max 2 open
- Risk controls: pause if down 8% (120 min), stop if down 18%
- Performance: Sharpe 1.6988, win rate 37.9%, ~894 trades over 2 years

## What Has Worked (DO MORE OF THIS)
- Small numerical adjustments to existing parameters (±5-15% of current value)
- Tightening RSI entry bands slightly (improves quality, reduces noise)
- Fine-tuning the stop/TP ratio — current 1.9% stop / 5.0% TP = 2.6:1 R:R supports 37.9% win rate
- Keeping max_open at 1-3 (more concurrent positions increases correlation risk at 2x)
- The trend filter (48h) is critical — do NOT remove it, it prevents counter-trend entries

## What Has Failed (AVOID THESE)
- Removing or replacing the 48h trend filter → Sharpe collapses to 0.6 or below
- Extreme RSI thresholds (RSI < 20 for long or RSI > 80 for short) → too few trades (<150), Sharpe artifacts
- Adding unproven new indicators or complex conditions → structural failures, extreme negative Sharpe
- Widening entries too aggressively → trade count exceeds 1,000, win rate drops, Sharpe ~0.6
- Making multiple simultaneous changes → impossible to know what helped
- Changing timeout or stop in isolation without adjusting the other → breaks R:R coherence

## Critical Constraint: ONE Small Change Per Generation
You MUST propose exactly ONE change. Choose from:
1. Adjust a single numeric threshold by a small amount (e.g., RSI from 38.36 → 39.5, or stop from 1.9% → 2.1%)
2. Adjust position_size_pct slightly (e.g., 15.09 → 14.0 or 16.5)
3. Adjust take_profit_pct (explore range 4.5–6.5%)
4. Adjust stop_loss_pct (explore range 1.5–2.8%) — must remain << 45% liquidation threshold
5. Adjust timeout_hours (explore range 72–144h, but watch funding drag above 120h)
6. Adjust the trend period_hours (explore 36–72h)
7. Adjust the RSI period_hours (explore 18–36h)
8. Adjust max_open (try 1 or 3, not higher)

Do NOT: add new indicators, add new conditions, change both entry AND exit in same generation,
propose anything that would logically result in <400 trades over 2 years.

## Priority Focus for Next 100 Generations

### Phase 1: Fine-tune the Stop/TP/Timeout Triad (HIGH PRIORITY)
The 1.9% stop / 5.0% TP / 96h timeout is the current optimum. Explore:
- stop_loss_pct: 1.7, 1.8, 2.0, 2.1, 2.2, 2.4, 2.5
- take_profit_pct: 4.5, 4.7, 5.2, 5.5, 5.8, 6.0, 6.5
- timeout_hours: 72, 84, 108, 120 (note: each 8h adds ~0.01% funding cost at 2x)
Always change only ONE of these three at a time.

### Phase 2: Refine RSI Thresholds (MEDIUM PRIORITY)
- Long RSI threshold: explore 35–42 range (current: 38.36)
- Short RSI threshold: explore 58–68 range (current: 60)
  Note: RSI > 60 for shorts may be too loose in bull-biased data — try 62, 64, 65
- RSI period: explore 20h, 22h, 26h, 28h (current: 24h)

### Phase 3: Trend Filter Tuning (MEDIUM PRIORITY)
- Trend period: explore 36h, 42h, 54h, 60h, 72h (current: 48h)
  Shorter periods = more trades but more false signals
  Longer periods = fewer, higher-quality trades

### Phase 4: Position Sizing (LOW PRIORITY — only if Sharpe plateaus)
- Current: 15.09% with max_open=2 → ~30% gross exposure
- Try: 13%, 14%, 16%, 17% with max_open=2
- Try: 12%, 13% with max_open=3 (more diversification, lower per-trade size)
- Do NOT exceed 20% per position at 2x leverage

## Risk & Regime Awareness
Current macro regime: DANGER (Fear & Greed = 11, Extreme Fear)
TYR Directive: Reduce position sizes to 25% of normal during DANGER regime.
This is handled automatically by the risk layer — but it means in live trading,
the effective position size will be ~3.77% (25% of 15.09%), which is very conservative.
Strategies should still be designed for normal market conditions in backtest;
the regime overlay is applied at runtime.

## Evaluation Standards
A generation is only meaningful if:
- Trade count ≥ 400 over 2-year backtest (HARD MINIMUM — below this is statistical noise)
- Sharpe > 1.6988 to be accepted as new best
- Win rate in range 30–55% (outside this range suggests something is broken)
- Trades in range 400–1,200 (extreme values signal overfitting or parameter collapse)

## Key Insight — Leverage Mechanics
At 2x leverage:
- A 1.9% stop-loss = 3.8% actual margin loss per losing trade
- A 5.0% TP = 10% actual margin gain per winning trade
- Funding cost over 96h hold = ~0.12% of position value = ~0.24% margin drag
- Liquidation at 45% margin loss means a single 22.5% adverse price move kills the position
- The current 1.9% stop provides 11.8× margin of safety vs. liquidation — this is GOOD
- Never propose stop-losses above 5% (that would be 10% margin loss, reducing safety margin)

## Style Reminder
Prefer strategies with:
- Consistent, modest wins (current 5% TP) over infrequent large wins
- Tight stops that cut losses fast (current 1.9%)
- Moderate trade frequency (800–1,000 trades/2yr = ~1-2 trades/day across 15 pairs)
- Limited concurrent exposure (max_open ≤ 3 at 2x leverage)
A Sharpe of 1.8–2.0 is the realistic ceiling for this style; do not sacrifice robustness chasing 2.5+.
```