```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-600 Audit | Updated by MIMIR

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions
At current 166h timeout: ~0.21% funding drag per full-hold trade (significant)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage
MIN_TRADES: 400 (hard floor — any result with <400 trades is INVALID regardless of Sharpe)
MIN_TRADES STATUS: ✅ CONFIRMED FIXED at gen 542. futures_swing = 400. No action needed.

## ⚠️ YAML IS AUTHORITATIVE — READ CAREFULLY
The current champion YAML shows:
  - timeout_hours: 166 (NOT 177 — previous program summary was stale)
  - stop_loss_pct: 1.91 (NOT 1.9 exactly)
  - position size_pct: 19.18 (NOT 15.41 — program summary was stale)
All guidance below uses the YAML values as ground truth.

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer has declared DANGER regime (F&G=17, Extreme Fear, VIX elevated).
Directive: Reduce live position sizes to 25% of normal.
For LIVE DEPLOYMENT ONLY: effective size = 19.18% × 25% ≈ 4.8% per position.
This does NOT affect backtest research — continue optimizing against historical data normally.
Do NOT change size_pct in the research YAML based on macro regime.

## Current Champion Summary (Gen 600)
- Sharpe: 2.1775 | Win rate: 39.6% | Trades: 1,266
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.82
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.91% stop-loss, 166h timeout
- Sizing: 19.18% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)
- R:R ratio: 4.65/1.91 = 2.43:1 (healthy — maintain above 2.0)

## Known Zombie Configurations — NEVER REPRODUCE THESE
The LLM repeatedly rediscovers these sub-optimal states. If your proposed change
leads to one of these, STOP immediately and choose a different parameter.

- Zombie A: ~1,230 trades, Sharpe ~1.49, win rate ~38.0% (Gens 523, 528, 529, 539)
- Zombie B: ~1,190 trades, Sharpe ~1.02, win rate ~36.7% (Gens 535, 537, 540)
- Zombie C: <400 trades, Sharpe deeply negative (Gens 524, 530, 534, 538, 597) — MIN_TRADES violations
- Zombie D: ~1,228 trades, Sharpe ~1.57, win rate ~38.4% — ⚠️ NEW HIGH-FREQUENCY ZOMBIE
  Seen in gens 584, 585, 586, 592, 595, 599 (6 times in last 20 gens)
  This is currently the most dangerous trap. Any result landing here is FORBIDDEN.
  If you produce ~1,228 trades with Sharpe ~1.57, you have hit Zombie D.
  Escape: revert completely and change a DIFFERENT parameter axis.

These are LOCAL TRAPS. Do NOT try to improve them incrementally. Escape entirely.

## Parameter State Tracking (do NOT re-test these exact values)
- take_profit_pct: 5.0, 5.2, 5.5, 4.5 (various gens, rejected)
- stop_loss_pct: 1.7, 2.0, 2.1 (tested and rejected)
- RSI long threshold: tested range 37.82–38.36+ (current 37.82 is optimized)
  - Values above 39: FORBIDDEN (trade floods)
  - Values below 34: FORBIDDEN (too few longs)
- RSI short threshold: 60 (NEVER IMPROVED in 600 generations — HIGHEST PRIORITY)
- max_open: DO NOT CHANGE. 3 is correct. max_open=4 is ABSOLUTELY FORBIDDEN (liquidation risk).
- Trend period: 48h (do not retry previously failed values)
- timeout_hours: 166h current. Do NOT go below 140h. Do NOT exceed 220h.
- position size_pct: 19.18% current. Phase 7 will explore this axis.

## ⚠️ SINGLE-CHANGE DISCIPLINE — CRITICAL RULE
Recent failure rate is ~80% (16 of last 20 gens discarded or zombie).
The #1 cause: changing multiple parameters at once or making extreme jumps.

RULES:
1. Change EXACTLY ONE parameter per generation. Never two.
2. Make SMALL incremental adjustments. RSI: ±0.5-1.0. TP/SL: ±0.1-0.2%. Timeout: ±5-10h.
3. If the last 3 generations all failed, you are likely oscillating. Switch parameter axes.
4. Never change the same parameter type as the immediately preceding generation unless
   it produced a new_best result.

## Recent Failure Pattern (Gens 580-599)
Zombie D (1,228 trades / Sharpe ~1.57) appeared 6 times. This must be explicitly
avoided. The LLM appears to be gravitating toward a TP reduction or stop tightening
that consistently produces this bad outcome. Do NOT reduce TP below 4.5% or
tighten stop below 1.8% until Zombie D's source parameter combination is identified.

---

## Priority Phases for Next 100 Generations

### ⭐ PHASE 1: RSI Short Threshold — CRITICAL PRIORITY (600 gens, never improved)
The RSI short entry threshold has been 60 since generation 1. This is the
single largest unexplored improvement vector in the entire 600-generation history.

Current short entry: trend=down AND RSI > 60
Problem: In bull-biased crypto, RSI > 60 during downtrends is too permissive.
Many marginal short entries are dragging down the overall 39.6% win rate.
Solution: Tighten the threshold incrementally to require stronger overbought signals.

TARGET VALUES (test STRICTLY in this order, one per generation):
  61 → 62 → 63 → 64 → 65 → 66

Expected effects per unit increase:
- ~20–50 fewer trades (from 1,266 baseline)
- Higher short win rate → overall win rate should rise above 40%
- At 60→66: estimated ~1,146–1,206 trades (well above 400 floor)
- Sharpe target: > 2.18 (beat current champion)

STOP CONDITIONS:
- If any single step drops trade count below 800: PAUSE. Do not go higher until analyzed.
- Do NOT try RSI short > 70 (too few shorts, statistically fragile)
- SUCCESS: Sharpe > 2.18 AND win rate rises above 40.5%

FAILURE ESCAPE: If RSI short 61–66 ALL fail to beat 2.1775, record all results and
move to Phase 2. Do not spend more than 10 generations on Phase 1 before escalating.

IMPORTANT: A failed RSI short test does NOT produce Zombie D (1,228 trades).
If you get Zombie D while testing RSI short, you have made a compound change.
Revert and test ONLY the RSI short threshold.

---

### ⭐ PHASE 2: Timeout Optimization — HIGH PRIORITY
Current timeout: 166h (~0.21% funding drag per full-hold trade)
Objective: Find optimal balance between trade room and funding drag minimization.

NOTE: Previous program incorrectly stated 177h. YAML is authoritative: 166h is current.
All ranges below are anchored to 166h.

REDUCTION exploration (reduce funding drag):
  Try: 148h, 152h, 156h, 160h, 163h
  Expected: reduced funding cost, possibly cleaner exits, may slightly reduce trade count

EXTENSION exploration (only after Phase 1 if entry quality improves):
  Try: 172h, 178h, 185h, 192h
  Rationale: higher-quality entries may benefit from more time to reach TP

HARD LIMITS:
- Do NOT go below 140h (historical degradation confirmed below this level)
- Do NOT go above 220h (funding cost becomes dominant drag)
- Change ONLY timeout in these generations — do not change TP or stop simultaneously

---

### PHASE 3: Take-Profit Fine-Tuning — MEDIUM PRIORITY
Current: 4.65% TP.
⚠️ WARNING: Zombie D (Sharpe ~1.57, ~1,228 trades) appears to be triggered by
aggressive TP reduction. Do NOT test TP below 4.4% until Zombie D is characterized.

TARGET VALUES (test carefully, one at a time):
  Test in order: 4.8%, 4.9%, 5.0%, 5.1%  (upward direction first — safer)
  Then if needed: 4.5%, 4.4%  (downward — risk of Zombie D, proceed cautiously)

RATIONALE:
- At 166h timeout, funding drag is ~0.21% per full-hold trade
- Higher TP (4.8–5.1%) may capture larger moves if entries are genuinely high quality
- Lower