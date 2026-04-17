```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 22401 | Incumbent: Gen 20502 (Sharpe=1.6060)
# MIMIR-reviewed 2026-04-17 (v45)
#
# ══════════════════════════════════════════════════════════════════════
# ⛔ STOP. BEFORE ANYTHING ELSE. READ THIS BOX. ⛔
# ══════════════════════════════════════════════════════════════════════
#
# THE UI "CURRENT BEST STRATEGY" IS POISON. IT IS WRONG. IGNORE IT.
#
# POISON FINGERPRINTS — if you see ANY of these, STOP and use STEP 1:
#   pairs: [BTC/USD]          ← ONLY 1 PAIR = POISON
#   size_pct: 30              ← POISON
#   max_open: 3               ← POISON
#   take_profit_pct: 6.63     ← POISON
#   timeout_hours: 133        ← POISON
#   price_change_pct lt -0.38 ← POISON
#   price_change_pct gt 0.37  ← POISON
#
# IF YOUR OUTPUT HAS trades=58 AND Sharpe≈1.36 → YOU USED POISON. DISCARD.
# IF YOUR OUTPUT HAS trades=0  AND Sharpe=0.00 → YOU USED POISON. DISCARD.
#
# ══════════════════════════════════════════════════════════════════════
# ████████████████████████████████████████████████████████████████████
# █                                                                    █
# █  STEP 1 — YOUR ONLY JOB RIGHT NOW. DO THIS FIRST.                 █
# █                                                                    █
# █  Copy the YAML block below EXACTLY as written.                     █
# █  Do NOT change any value. Do NOT read ahead. Output it now.        █
# █                                                                    █
# ████████████████████████████████████████████████████████████████████
#
# ```yaml
# name: gen20502_rsi35
# style: randomly generated
# pairs:
# - BTC/USD
# - ETH/USD
# - SOL/USD
# position:
#   size_pct: 25.0
#   max_open: 2
#   fee_rate: 0.001
# entry:
#   long:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 48
#       operator: eq
#       value: below_lower
#     - indicator: macd_signal
#       period_hours: 48
#       operator: eq
#       value: bullish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: lt
#       value: -0.5
#     - indicator: rsi
#       period_hours: 14
#       operator: lt
#       value: 35.0
#   short:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 168
#       operator: eq
#       value: above_upper
#     - indicator: macd_signal
#       period_hours: 24
#       operator: eq
#       value: bearish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: gt
#       value: 0.54
# exit:
#   take_profit_pct: 9.5
#   stop_loss_pct: 1.5
#   timeout_hours: 156
# risk:
#   pause_if_down_pct: 8
#   stop_if_down_pct: 18
#   pause_hours: 48
# ```
#
# ████████████████████████████████████████████████████████████████████
# █  STEP 1 COMPLETE. NOW READ THE REST.                              █
# ████████████████████████████████████████████████████████████████████
#
# ══════════════════════════════════════════════════════════════════════
# ⚠️  UI POISON WARNING — FULL DETAIL ⚠️
# ══════════════════════════════════════════════════════════════════════
#
# The UI "Current Best Strategy" displays a CORRUPTED YAML (Gen 22157).
# It was incorrectly accepted. It is NOT the incumbent. DO NOT USE IT.
#
# POISON YAML values (any of these = wrong strategy):
#   name: crossover_rsi30_tightened  ← wrong name = poison
#   pairs: [BTC/USD] only            ← must be 3 pairs
#   size_pct: 30                     ← must be 25.0
#   max_open: 3                      ← must be 2
#   take_profit_pct: 6.63            ← must be 9.5
#   timeout_hours: 133               ← must be 156
#   price_change_pct lt -0.38        ← must be -0.5
#   price_change_pct gt 0.37         ← must be 0.54
#
# RESULT FINGERPRINTS OF POISON CONTAMINATION:
#   trades=58, Sharpe≈1.3604–1.3605  → you used the Gen 22157 poison base
#   trades=0,  Sharpe=0.0000         → malformed YAML or wrong strategy type
#
# BOTH of these mean your output is wrong. Discard. Return to STEP 1.
#
# TRUE INCUMBENT: Gen 20502, Sharpe=1.6060, trades=54, WR=44.4%
# APPROXIMATION:  Sharpe=1.6027–1.6028, trades=54 (rsi=32.96 vs true 30–33)
#
# ══════════════════════════════════════════════════════════════════════
# ACTIVE TEST THIS GENERATION: D7b
# ══════════════════════════════════════════════════════════════════════
#
# TEST: gen20502_rsi35
# CHANGE: rsi long entry value → 35.0  (relaxed from 32.96)
# BASE: Gen 20502 approximation (YAML-INCUMBENT below)
# THIS IS THE ONE CHANGE. EVERYTHING ELSE IS IDENTICAL TO STEP 1 YAML.
# THE STEP 1 YAML ALREADY CONTAINS THIS CHANGE. OUTPUT IT AS-IS.
#
# Status of D7a (rsi=30.0):
#   D7a ran for 200+ generations but was NEVER cleanly executed.
#   The LLM kept anchoring to the UI poison YAML (trades=58, Sharpe≈1.36).
#   D7a is marked UNTESTED/ABANDONED due to persistent LLM compliance failure.
#   D7b (rsi=35.0) is now the active test.
#
# Why D7b:
#   - RSI=35.0 relaxes the entry filter slightly → more trades, tests sensitivity
#   - If trades rise above 60 or Sharpe drops, entry is oversensitive to RSI
#   - If Sharpe improves, RSI threshold is in the 33–35 range
#   - Result will inform D7c direction (tighter or looser)
#
# ══════════════════════════════════════════════════════════════════════
# RESULT CLASSIFICATION — WHAT DID YOU GET?
# ══════════════════════════════════════════════════════════════════════
#
# trades=0, Sharpe=0.0000 [max_trades_reject / malformed]:
#   YOU USED POISON OR OUTPUT MALFORMED YAML.
#   DISCARD. Return to STEP 1. Output it exactly.
#
# trades=58, Sharpe≈1.3604 [wrong_base — Gen 22157 poison]:
#   YOU USED THE POISON UI YAML (Gen 22157, BTC/USD only).
#   DISCARD. Return to STEP 1. Output it exactly.
#
# trades=54, Sharpe≈1.6027 [near_incumbent, no_change]:
#   You output the approximation without D7b change (rsi=32.96 not 35.0).
#   Verify rsi value=35.0 in your output. Discard. Retest.
#
# trades<50 [too few — entry too tight]:
#   Unexpected — rsi=35 should produce ≥54 trades. Check YAML for errors.
#   Mark D7b result invalid. Escalate to MIMIR.
#
# trades≥50, 1.30≤Sharpe<1.6060 [valid discard]:
#   D7b tested and did not beat incumbent. Mark D7b dead.
#   Next test: D7c (rsi=33.5 — between incumbent and D7b).
#
# trades≥50, Sharpe=1.6060 [D7b neutral — matches incumbent]:
#   rsi threshold is insensitive in this direction. Mark D7b dead.
#   Next test: D7c (rsi=33.5).
#
# trades≥50, Sharpe>1.6060 [NEW BEST — SUCCESS]:
#   NEW INCUMBENT FOUND. Report immediately.
#   Update YAML-INCUMBENT below and advance D7 series.
#
# trades>65 [too many — entry too loose]:
#   rsi=35 is too permissive. Mark D7b dead.
#   Next test: D7c (rsi=31.5 — between incumbent and D7a).
#
# Sharpe<0 [catastrophic]:
#   Multiple parameters changed or YAML corrupted. Check YAML carefully.
#
# ══════════════════════════════════════════════════════════════════════
# YAML-INCUMBENT — GEN 20502 (APPROXIMATION — THIS IS YOUR BASE)
# ══════════════════════════════════════════════════════════════════════
#
# THIS IS THE ONLY BASE. MUTATE FROM THIS. NOT FROM THE UI.
#
# ```yaml
# name: gen20502_approximation
# style: randomly generated
# pairs:
# - BTC/USD
# - ETH/USD
# - SOL/USD
# position:
#   size_pct: 25.0
#   max_open: 2
#   fee_rate: 0.001
# entry:
#   long:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 48
#       operator: eq
#       value: below_lower
#     - indicator: macd_signal
#       period_hours: 48
#       operator: eq
#       value: bullish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: lt
#       value: -0.5
#     - indicator: rsi
#       period_hours: 14
#       operator: lt
#       value: 32.96
#   short:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 168
#       operator: eq
#       value: above_upper
#     - indicator: macd_signal
#       period_hours: 24
#       operator: eq
#       value: bearish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: gt
#       value: 0.54
# exit:
#   take_profit_pct: 9.5
#   stop_loss_pct: 1.5
#   timeout_hours: 156
# risk:
#   pause_if_down_pct: 8
#   stop_if_down_pct: 18
#   pause_hours: 48
# ```
#
# Reproduces at: Sharpe=1.6027–1.6028, trades=54, WR=44.4%
# True incumbent Sharpe: 1.6060 (gap ~0.003)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT TRAJECTORY (confirmed improvements only)
# ══════════════════════════════════════════════════════════════════════
#
#   Gen 19808: Sharpe=1.3483, trades=58, WR=41.4%
#   Gen 20475: Sharpe=1.4877, trades=55, WR=43.6%  (+0.139) ← entry change
#   Gen 20492: Sharpe=1.4898, trades=52, WR=50.0%  (+0.002) ← entry change
#   Gen 20502: Sharpe=1.6060, trades=54, WR=44.4%  (+0.116) ← TRUE INCUMBENT
#
#   Gen 22157: Sharpe=1.3604  ← INCORRECTLY ACCEPTED. DISCARD. POISON.
#   Gen 22174: Sharpe=1.4449, trades=51 ← valid but below incumbent
#
# KEY INSIGHT: Every large Sharpe gain came from entry condition changes.
# Trade count 58→54 as Sharpe rose. Fewer, better-filtered trades = quality.
# CLEAN RESULT = 50 ≤ trades ≤ 65.
#
# CONFIRMED PATTERN: trades=58, Sharpe≈1.36 is the Gen 22157 poison signature.
# Any result matching this profile is from the wrong base. Discard immediately.
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES TEST QUEUE — ANCHORED TO GEN 20502
# ══════════════════════════════════════════════════════════════════════
#
# Rule: Change EXACTLY ONE parameter per generation from YAML-INCUMBENT.
# Rule: trades must be ≥ 50 and ≤ 65 for result to be valid.
# Rule: Sharpe must exceed 1.6060 to be accepted as new best.
# Rule: trades=58 + Sharpe≈1.36 = POISON BASE. Discard always.
#
# ── PHASE 3: ENTRY CONDITION VARIATIONS (HIGHEST PRIORITY) ──────────
#
# D7a: rsi value → 30.0    ⚫ ABANDONED (200+ gens, never cleanly executed)
#      Persistent LLM compliance failure. Not enough trade data to classify.
#
# D7b: rsi value → 35.0                      ← ACTIVE TEST (D7b)
#      name: gen20502_rsi35
#      Status: ACTIVE — use STEP 1 YAML as-is
#
# D7c: rsi value → 33.5                      (if D7b shows Sharpe drop/neutral)
#      name: gen20502_rsi335
#      OR: rsi → 31.5                        (if D7b shows too many trades)
#
# D7d: rsi value → 30.0    (retry D7a after poison problem resolved, if needed)
#
# D8a: long price_change_pct value → -1.0    (after D7 series resolves)
#      name: gen20502_pricechg10
#
# D8b: long price_change_pct value → -0.3    (only if D8a dead)
#      name: gen20502_pricechg03
#
# D8c: long price_change_pct value → -0.75   (only if D8a and D8b dead)
#
# D6a: long bollinger period_hours → 36      (after D7 and D8 resolve)
#      name: gen20502_boll36
#
# D6b: long bollinger period_hours → 60      (only if D6a dead)
#
# D9a: short price_change_pct value → 1.0    (after D6 resolves)
#      name: gen20502_shortprice10
#
# D9b: short bollinger period_hours → 72     (only if D9a dead)
#
# ── PHASE 1: RISK PARAMETER VARIATIONS (LOW PRIORITY) ───────────────
#
# D1: pause_if_down_pct → 10             ✅ DEAD (800+ gens, confirmed)
#
# D2: stop_if_down_pct → 20              ⏸ SUSPENDED
#     Retest only after D7 and D8 series both resolve.
#
# D3a: pause_hours → 24                  NOT STARTED (after D7+D8)
# D3b: pause_hours → 72                  NOT STARTED (only if D3a dead)
#
# ── PHASE 2: EXIT PARAMETER VARIATIONS (LOW PRIORITY) ───────────────
#
# EVIDENCE: Exit/risk changes have produced zero Sharpe improvements.
# All D4/D5 tests are SUSPENDED until D7 and D8 are resolved.
#
# D4a: timeout_hours → 240               SUSPENDED
# D4b: timeout_hours → 264               SUSPENDED
# D4c: timeout_hours → 288               SUSPENDED
# D4d: timeout_hours → 192               SUSPENDED
#
# D5a: take_profit_pct → 12.0            SUSPENDED
# D5b: take_profit_pct → 13.0            SUSPENDED
# D5c: take_profit_pct → 14.0            SUSPENDED
# D5d: take_profit_pct → 15.0            SUSPENDED
#
# ── PHASE 4: BROADER SEARCH (IF ALL D-SERIES DEAD) ──────────────────
# Escalate to MIMIR for: regime-conditional sizing, new indicator types,
# walk-forward validation, F&G index as entry filter,
# RSI-distance position sizing, multi-timeframe confirmation.
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES STATUS SUMMARY
# ══════════════════════════════════════════════════════════════════════
#
# D1: ✅ DEAD       pause_if_down_pct=10 (confirmed dead 800+ gens)
# D2: ⏸ SUSPENDED  stop_if_down_pct=20 (0 valid tests; after D7+D8)
# D3: ⏸ SUSPENDED  pause_hours variations (after D7+D8)
# D4: ⏸ SUSPENDED  timeout_hours variations (exit changes don't move Sharpe)
# D5: ⏸ SUSPENDED  take_profit_pct variations (exit changes don't move Sharpe)
# D6: ⬜ NOT STARTED bollinger period variations
# D7: 🔵 ACTIVE     rsi threshold — D7b (rsi=35.0) is current test
#     D7a: ⚫ ABANDONED (never cleanly executed due to LLM poison contamination)
# D8: ⬜ NOT STARTED price_change_pct variations
# D9: ⬜ NOT STARTED short-side condition variations
#
# ══════════════════════════════════════════════════════════════════════
# CONFIRMED DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:      129, 133, 135, 138, 144, 156*, 168, 192, 216
# take_profit_pct:    6.63, 7.14, 7.36, 7.38, 9.5*, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct:      1.5*, 2.0, 2.5
# pause_if_down_pct:  8* (incumbent), 10 (dead)
# pairs:              [BTC/USD only], [BTC/USD+ETH/USD only]
# rsi value:          30.0 (D7a — abandoned/untested, not confirmed dead)
#
# * = incumbent value. Do not propose as a "change" — it is already the base.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO CONTEXT (as of 2026-04-17)
# ══════════════════════════════════════════════════════════════════════
#
# F&G = 21 (Extreme Fear). BTC Dominance = 57.0%. Regime: CAUTION.
# TYR Directive: Reduce live position sizes to 50% of normal.
# NOTE: Extreme Fear regime is FAVORABLE for this strategy's long entry logic.
# RSI<33 + below Bollinger lower + MACD bullish = classic fear capitulation entry.
# The backtest Sharpe of 1.6060 was earned largely in similar regimes.
# Live sizing should follow TYR directive (50% reduction) regardless.
#
# ══════════════════════════════════════════════════════════════════════
# FINAL CHECKLIST — VERIFY YOUR YAML BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# ⛔ POISON CHECK — if ANY of these appear, DISCARD and use STEP 1 YAML:
#  ✗ name = crossover_rsi30_tightened    (wrong name = poison base)
#  ✗ pairs = [BTC/USD] only              (must be 3 pairs)
#  ✗ size_pct = 30                       (must be 25.0)
#  ✗ max_open = 3                        (must be 2)
#  ✗ take_profit_pct = 6.63              (must be 9.5)
#  ✗ timeout_hours = 129, 133, or 135    (must be 156)
#  ✗ price_change_pct lt -0.38           (must be -0.5)
#  ✗ price_change_pct gt 0.37            (must be 0.54)
#  ✗ result trades=58, Sharpe≈1.36       (poison base fingerprint — discard)
#
# ✅ CORRECT VALUES — must match exactly:
#  ✓ name               = gen20502_rsi35
#  ✓ pairs              = BTC/USD, ETH/USD, SOL/USD  (3 pairs)
#  ✓ size_pct           = 25.0
#  ✓ max_open           = 2
#  ✓ fee_rate           = 0.001
#  ✓ momentum_accelerating long   period=48, eq, false
#  ✓ bollinger_position long      period=48, eq, below_lower
#  ✓ macd_signal long             period=48, eq, bullish
#  ✓ price_change_pct long        period=24, lt, -0.5
#  ✓ rsi long                     period=14, lt, 35.0   ← THE ONE CHANGE
#  ✓ momentum_accelerating short  period=48, eq, false
#  ✓ bollinger_position short     period=168, eq, above_upper
#  ✓ macd_signal short            period=24, eq, bearish
#  ✓ price_change_pct short       period=24, gt, 0.54
#  ✓ take_profit_pct    = 9.5
#  ✓ stop_loss_pct      = 1.5
#  ✓ timeout_hours      = 156
#  ✓ pause_if_down_pct  = 8
#  ✓ stop_if_down_pct   = 18
#  ✓ pause_hours        = 48
```