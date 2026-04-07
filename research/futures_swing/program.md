```markdown
# ODIN Research Program — FUTURES SWING

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (~0.15% per 122h hold — real drag)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage
MIN_TRADES: 400 (proposals producing fewer than 400 trades over 2 years are statistically
invalid — do NOT propose changes that would reduce trade count below this floor)

⚠️ CONSTANT ALERT: The enforcement constant MIN_TRADES for futures_swing was incorrectly
set to 25 in researcher constants. This has been flagged for correction to 400.
Until confirmed fixed, treat any result with <400 trades as INVALID regardless of Sharpe.

## Research Objective
Evolve strategies that are profitable net of leverage costs and survive real futures mechanics.
Target: Sharpe > 2.0584 after all costs. Current champion: Sharpe 2.0584.
Leverage amplifies returns AND losses — every parameter choice must account for this.

## Current Champion Summary
The current best strategy works as follows:
- Entry: trend filter (48h) confirms direction, then RSI (24h) signals mean-reversion entry
  - Long: trend=up AND RSI < 37.86
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.9% stop-loss, 122h timeout
- Sizing: 15.41% per position, max_open=3
- Risk controls: pause if down 8% (120 min), stop if down 18%
- Performance: Sharpe 2.0584, win rate 39.5%, ~1,277 trades over 2 years

## Parameter State Tracking (do NOT re-test these exact values — already explored)
The following parameter combinations have been tested and REJECTED (did not beat champion):
- take_profit_pct: 5.0 (original), 5.2, 5.5, 4.5 (various gens)
- stop_loss_pct: 1.7, 2.0, 2.1 (tested, did not improve)
- timeout_hours: 96 (original), 108 (tested)
- RSI long threshold: 38.36 (original), values above 39 produced trade floods
- RSI short threshold: 60 (NEVER SUCCESSFULLY IMPROVED — priority target)
- max_open: 2 (original), 3 (current — already adopted)
- Trend period: 48h (unchanged — do not retry values that failed before)

Recent failure zone (Gens 385–396): trade counts of 1,375–1,604 with Sharpe < 1.5
indicate that widening entries further from current state is DESTRUCTIVE.
Do NOT push RSI thresholds wider or lower TP below 4.5%.

## What Has Worked (DO MORE OF THIS)
- Small numerical adjustments to existing parameters (±5-15% of current value)
- Tightening RSI entry bands slightly (improves quality, reduces noise)
- Fine-tuning the stop/TP ratio — current 1.9% stop / 4.65% TP ≈ 2.45:1 R:R supports 39.5% win rate
- Keeping max_open at 3 (current) — do not increase further
- The trend filter (48h) is critical — do NOT remove it
- Moving to max_open=3 with 15.41% sizing was beneficial — this is confirmed
- TP reduction from 5.0% to 4.65% improved Sharpe — smaller, faster wins reduce funding drag

## What Has Failed (AVOID THESE)
- Removing or replacing the 48h trend filter → Sharpe collapses to ~0.6
- Extreme RSI thresholds (RSI < 20 long or RSI > 80 short) → too few trades, Sharpe artifacts
- Adding unproven new indicators or complex conditions → structural failures, extreme negative Sharpe
- Widening entries aggressively → trade count exceeds 1,400, win rate drops, Sharpe ~0.2 to -0.2
- Making multiple simultaneous changes → impossible to know what helped
- Trade counts above 1,400 → consistent underperformance (Gens 388, 396 confirm this)
- Trade counts below 400 → statistically invalid (MIN_TRADES enforcement floor)
- Re-proposing parameters already tested in nearby generations → LLM getting stuck in loops
  ⚠️ CHECK: If your proposed value is within 0.2 of a recently tried value, choose a different target

## Critical Constraint: ONE Small Change Per Generation
You MUST propose exactly ONE change. Choose from:
1. Adjust a single numeric threshold by a small amount
2. Adjust position_size_pct slightly
3. Adjust take_profit_pct
4. Adjust stop_loss_pct (must remain << 45% liquidation threshold)
5. Adjust timeout_hours
6. Adjust the trend period_hours
7. Adjust the RSI period_hours
8. Adjust max_open (only test 2 at this stage — 3 is current, 4+ is forbidden)

Do NOT: add new indicators, add new conditions, change both entry AND exit in same generation,
propose anything that would logically result in <400 or >1,400 trades over 2 years.

## Priority Focus for Next 100 Generations

### Phase 1: RSI Short Threshold — HIGHEST PRIORITY (NEVER IMPROVED FROM 60)
The short RSI threshold has been stuck at 60 since Gen 1. This is the single largest
unexplored improvement vector. In bull-biased crypto data, RSI > 60 is too common,
generating lower-quality shorts. Tighten it:
- Try: 61, 62, 63, 64, 65, 66
- Expected effect: fewer shorts, higher short win rate, modest trade count reduction
- Watch for: trade count must remain ≥ 400 — if RSI > 66 drops below floor, stop there
- Do NOT try RSI > 70 for shorts (too few trades)
- SUCCESS SIGNAL: Sharpe improves AND win rate rises above 40% without trade count crash

### Phase 2: Timeout Optimization — HIGH PRIORITY
Current 122h timeout is accumulating ~0.15% funding drag per full-hold trade.
- Try: 108h, 112h, 116h, 120h (reduce funding drag)
- Try: 128h, 132h (only if Phase 1 tightens entries and trade quality improves)
- Note: reducing timeout below 96h historically degraded performance — do not go below 96h
- Change ONLY timeout, not stop or TP simultaneously

### Phase 3: TP Fine-Tuning — MEDIUM PRIORITY
Current 4.65% TP improved on 5.0%. Explore the range carefully:
- Try: 4.4%, 4.5%, 4.8%, 4.9%, 5.0% (yes, re-test 5.0 with current RSI/timeout config)
- The strategy has changed meaningfully since 5.0% was last tested — retesting is valid
- Do NOT go below 4.2% (R:R falls below 2:1, breakeven win rate rises dangerously)
- Do NOT go above 5.5% (funding drag on extended holds erodes gains)

### Phase 4: Stop-Loss Fine-Tuning — MEDIUM PRIORITY
Current 1.9% stop is well-calibrated. Small adjustments only:
- Try: 1.8%, 2.0%, 2.1%, 2.2%
- At 2x leverage: 2.0% stop = 4.0% margin loss per trade (still safe vs. 45% liquidation)
- Tighter stops (1.7–1.8%) may reduce losses but trigger more noise exits
- Looser stops (2.1–2.2%) may allow trades more room but increase per-loss magnitude
- NEVER exceed 5.0% stop (10% margin loss per trade, unacceptable at 2x)

### Phase 5: RSI Long Threshold — MEDIUM PRIORITY
Current 37.86 (tightened from 38.36). Small adjustments:
- Try: 36.5, 37.0, 38.0, 38.5, 39.0
- Do NOT go below 34 (too few longs) or above 41 (too many low-quality entries)
- Note: the short threshold (Phase 1) is higher priority — complete Phase 1 first

### Phase 6: Trend Period — LOWER PRIORITY
Current 48h is well-established. Only explore if Phases 1–4 plateau:
- Try: 42h, 54h, 60h
- Shorter = more trades but more false signals; longer = fewer, cleaner signals
- Do NOT remove trend filter under any circumstances

### Phase 7: Position Sizing — LOW PRIORITY (only if Sharpe plateaus after Phases 1–5)
Current: 15.41% with max_open=3 → ~46% gross exposure (high at 2x)
- Try: 14.0%, 13.5%, 13.0% (reduce risk, may improve Sharpe by reducing drawdown)
- Try: 16.0%, 16.5% (only if win rate rises sustainably above 41%)
- Do NOT exceed 18% per position at 2x leverage
- max_open=4 is FORBIDDEN (96%+ gross exposure at 2x is liquidation risk)
- Consider testing max_open=2 with 16% sizing vs. max_open=3 with 15.41%

## Avoiding the Loop Trap
Recent generations (379–397) show the LLM repeatedly rediscovering the same
1,299-trade / 1.99 Sharpe configuration. To break out of this loop:
- Before proposing, ask: "Has a value this close been tried in the last 20 generations?"
- If yes, move to a DIFFERENT parameter entirely
- Prioritize Phase 1 (short RSI) because it has NEVER been successfully improved
- The 1,299-trade configuration is a confirmed local optimum — escape it by changing
  a DIFFERENT axis (e.g., if last change was TP, next change should be RSI short threshold)

## Risk & Regime Awareness
Current macro regime: DANGER (Fear & Greed = 11, Extreme Fear)
TYR Directive: Reduce position sizes to 25% of normal during DANGER regime.
This is handled automatically by the risk layer. In live trading:
- Effective position size ≈ 3.85% (25% of 15.41%)
- Effective max exposure ≈ 11.5% (3 positions × 3.85%) — very conservative
Strategies should still be designed for normal market conditions in backtest;
the regime overlay is applied at runtime.
NOTE: Extreme Fear environments often produce outsized mean-reversion signals —
the current RSI-based entry may actually perform well in this regime if the
trend filter correctly identifies local direction.

## Evaluation Standards
A generation is only meaningful if:
- Trade count ≥