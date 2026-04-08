```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-542 Audit | Updated by MIMIR

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions
At current 177h timeout: ~0.22% funding drag per full-hold trade (significant)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage
MIN_TRADES: 400 (hard floor — any result with <400 trades is INVALID regardless of Sharpe)

## ⚠️ INFRASTRUCTURE ALERT — HIGHEST PRIORITY
MIN_TRADES["futures_swing"] is currently set to 25 in researcher constants.
This is WRONG. It must be 400.
LOKI MUST fix this immediately: set MIN_TRADES["futures_swing"] = 400
Until confirmed fixed, the backtester will accept catastrophically bad low-trade
results as valid. Gens 524 (359 trades, Sharpe -1.56), 530 (241 trades, Sharpe -1.72),
534 (227 trades, Sharpe -1.72), and 538 (35 trades, Sharpe -8.10) are all examples
of invalid results that slipped through due to this bug.
DO NOT proceed with normal research until this constant is corrected.

## ⚠️ PARAMETER STATE DISCREPANCY — MUST RESOLVE
The champion YAML shows timeout_hours: 177, but the program summary previously
stated 122h. The YAML is authoritative. Current timeout is 177h, not 122h.
All timeout optimization guidance has been updated to reflect this.
The Phase 2 guidance below supersedes any previous timeout ranges.

## Current Champion Summary (Gen 542)
- Sharpe: 2.0977 | Win rate: 39.3% | Trades: 1,266
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.82
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.9% stop-loss, 177h timeout
- Sizing: 15.41% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)

## Known Zombie Configurations — NEVER REPRODUCE THESE
The LLM has repeatedly rediscovered these sub-optimal states. If your proposed
change leads to one of these, STOP and choose a different parameter:
- Zombie A: ~1,230 trades, Sharpe ~1.49, win rate ~38.0% (seen in Gens 523, 528, 529, 539)
- Zombie B: ~1,190 trades, Sharpe ~1.02, win rate ~36.7% (seen in Gens 535, 537, 540)
- Zombie C: <400 trades, Sharpe deeply negative (Gens 524, 530, 534, 538) — MIN_TRADES bug
These configurations are LOCAL TRAPS. Escape by changing a DIFFERENT parameter axis.

## Parameter State Tracking (do NOT re-test these exact values)
- take_profit_pct: 5.0, 5.2, 5.5, 4.5 (various gens, rejected)
- stop_loss_pct: 1.7, 2.0, 2.1 (tested and rejected)
- RSI long threshold: 38.36 (original), 37.86, 37.82 (current)
  - Values above 39 produced trade floods → FORBIDDEN
  - Values below 34 produce too few longs → FORBIDDEN
- RSI short threshold: 60 (NEVER IMPROVED — highest priority target)
- max_open: 2 (original), 3 (current — DO NOT CHANGE)
- max_open=4: ABSOLUTELY FORBIDDEN (liquidation risk at 2x)
- Trend period: 48h (do not retry values that previously failed)
- timeout_hours: Values below 140h have historically degraded performance — do not go below 140h

## Recent Failure Cluster Warning (Gens 523–540)
Trade counts of 1,179–1,327 with Sharpe 1.02–1.95 dominate recent history.
This pattern indicates the LLM is oscillating within a known-bad neighborhood.
Breaking out requires targeting a DIFFERENT parameter than was changed in the
last 3 generations. Check: if the last change was RSI long threshold, next
change must be RSI short threshold, TP, stop, or timeout — NOT RSI long again.

---

## Priority Phases for Next 100 Generations

### ⭐ PHASE 1: RSI Short Threshold — CRITICAL PRIORITY (542 gens, never improved)
The RSI short entry threshold has been 60 since generation 1. This is the
single largest unexplored improvement vector in the entire research history.

Current short entry: trend=down AND RSI > 60
Problem: In bull-biased crypto, RSI > 60 during downtrends is common,
admitting many marginal/low-quality short trades.
Solution: Tighten the threshold to require stronger overbought signal.

TARGET VALUES (test in this order, one per generation):
  61 → 62 → 63 → 64 → 65 → 66

Expected effects:
- Fewer short entries (good: quality over quantity)
- Higher short win rate (currently dragging overall win rate below 40%)
- Trade count reduction: estimate ~20-50 trades per unit increase in threshold
- At 60→66: estimate ~1,146–1,206 trades (still well above 400 floor)
- Sharpe should improve if short quality increases

STOP CONDITIONS:
- If RSI short > 66 drops trade count below 800, pause and analyze before going higher
- Do NOT try RSI short > 70 (too few shorts, statistically fragile)
- SUCCESS: Sharpe > 2.10 AND win rate rises above 40.5%

FAILURE ESCAPE: If RSI short 61-66 all fail to beat 2.0977, move to Phase 2.
Do not spend more than 12 generations on Phase 1 before moving on.

---

### ⭐ PHASE 2: Timeout Optimization — HIGH PRIORITY
Current timeout: 177h (~0.22% funding drag per full-hold trade)
Objective: Find optimal balance between giving trades room vs. minimizing funding drag

NOTE: Previous program incorrectly anchored this around 122h. The actual
current value is 177h. All ranges below are correctly anchored to 177h.

REDUCTION exploration (reduce funding drag):
  Try: 155h, 160h, 165h, 168h, 172h
  Expected: fewer timeout exits, reduced funding cost, possibly lower trade count
  
EXTENSION exploration (only if Phase 1 tightens entries):
  Try: 184h, 192h, 200h
  Rationale: higher-quality entries may warrant more time to reach TP

HARD LIMITS:
- Do NOT go below 140h (historical degradation below this level)
- Do NOT go above 220h (~0.27% drag per trade, funding cost becomes dominant)
- Change ONLY timeout in these generations — do not change stop or TP simultaneously

---

### PHASE 3: Take-Profit Fine-Tuning — MEDIUM PRIORITY
Current: 4.65% TP. Previous reduction from 5.0% → 4.65% improved Sharpe.
The strategy has changed significantly (new pairs, new timeout) since 5.0% was
last tested. Retesting the full range with current config is valid.

TARGET VALUES:
  Test: 4.4%, 4.5%, 4.8%, 4.9%, 5.0%, 5.1%
  
RATIONALE:
- At 177h timeout, funding drag is higher than when 4.65% was first adopted
- Slightly lower TP (4.4-4.5%) may exit positions before maximum funding drag
- Slightly higher TP (4.8-5.1%) may capture larger moves if entries are high quality
- The R:R ratio must be monitored: TP/stop_loss ratio should remain above 2.0
  - At 1.9% stop: minimum TP = 3.8% (do NOT go below 4.0% to maintain safety margin)
  - At 1.9% stop: 4.65% TP = 2.45:1 R:R (current baseline)

FORBIDDEN: TP below 4.0% or above 5.5%

---

### PHASE 4: Stop-Loss Fine-Tuning — MEDIUM PRIORITY
Current: 1.9% stop. Well-calibrated but worth exploring ±0.2% range.

TARGET VALUES:
  Tighter: 1.7%, 1.75%, 1.8%  (may reduce loss magnitude but trigger noise exits)
  Looser:  2.0%, 2.1%, 2.2%   (more room but higher per-loss magnitude)

LEVERAGE CONTEXT:
  At 2x: 1.9% stop = 3.8% margin loss per stopped trade (safe)
  At 2x: 2.2% stop = 4.4% margin loss per stopped trade (still safe, 10x below liquidation)
  NEVER exceed 5.0% stop (10% margin loss per trade — unacceptable)

NOTE: If Phase 1 successfully tightens entry quality, the case for slightly looser
stops (2.0-2.1%) strengthens — higher-quality entries should be given more room.

---

### PHASE 5: RSI Long Threshold — MEDIUM PRIORITY
Current: 37.82 (refined from original 38.36 over many generations)
This parameter has been well-optimized. Only small adjustments warranted.

TARGET VALUES:
  Try: 36.5, 37.0, 37.5, 38.0, 38.5
  
CONSTRAINTS:
  - Do NOT go below 34.0 (too few longs, trade count collapses)
  - Do NOT go above 41.0 (too many low-quality longs, win rate drops)
  - Complete Phase 1 (RSI short) before spending significant cycles here
  - The asymmetry between long threshold (37.82) and short threshold (60)
    reflects bull market bias — this is INTENTIONAL, do not try to equalize them

---

### PHASE 6: RSI Period — LOWER PRIORITY
Current: 24h RSI period. Defines the lookback for overbought/oversold calculation.

TARGET VALUES:
  Shorter: 18h, 20h (more sensitive, more signals,