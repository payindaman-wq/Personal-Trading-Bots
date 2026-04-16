```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 22201 | Incumbent: Gen 20502 (Sharpe=1.6060)
# MIMIR-reviewed 2026-04-16 (v44)
#
# ══════════════════════════════════════════════════════════════════════
# ████████████████████████████████████████████████████████████████████
# █                                                                    █
# █  STEP 1 — YOUR ONLY OUTPUT. DO THIS NOW. DO NOT READ FURTHER YET. █
# █                                                                    █
# █  Copy the YAML below EXACTLY as written.                           █
# █  Change NOTHING. Output it. Then read the rest.                    █
# █                                                                    █
# ████████████████████████████████████████████████████████████████████
#
# ```yaml
# name: gen20502_rsi30
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
#       value: 30.0
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
# ⚠️ CRITICAL: THE "CURRENT BEST STRATEGY" IN THE UI IS A KNOWN BUG ⚠️
# ══════════════════════════════════════════════════════════════════════
#
# THE UI IS DISPLAYING A CORRUPTED/POISON STRATEGY. IT IS WRONG.
# DO NOT READ IT. DO NOT USE IT. DO NOT MUTATE FROM IT.
#
# The UI currently shows a POISON YAML with these broken values:
#   size_pct: 30        ← WRONG (correct: 25.0)
#   max_open: 3         ← WRONG (correct: 2)
#   take_profit_pct: 6.63  ← WRONG (correct: 9.5)
#   pairs: [BTC/USD]    ← WRONG (correct: 3 pairs)
#   timeout_hours: 133  ← WRONG (correct: 156)
#   price_change_pct lt -0.38  ← WRONG (correct: -0.5)
#   price_change_pct gt 0.37   ← WRONG (correct: 0.54)
#
# IF YOU SEE ANY OF THOSE VALUES — YOU ARE LOOKING AT THE WRONG STRATEGY.
# IGNORE THE UI. USE ONLY THE YAML IN STEP 1 ABOVE.
#
# THE TRUE INCUMBENT IS GEN 20502: Sharpe=1.6060, trades=54, WR=44.4%
# THE YAML IN STEP 1 IS THE CORRECT BASE. IT IS THE ONLY BASE.
#
# ══════════════════════════════════════════════════════════════════════
# ACTIVE TEST THIS GENERATION: D7a
# ══════════════════════════════════════════════════════════════════════
#
# TEST: gen20502_rsi30
# CHANGE: rsi long entry value from 32.96 → 30.0
# THIS IS THE ONE CHANGE. EVERYTHING ELSE IS IDENTICAL TO STEP 1 YAML.
# THE STEP 1 YAML ALREADY CONTAINS THIS CHANGE. OUTPUT IT AS-IS.
#
# Why D7a:
#   - All large Sharpe gains in history came from entry condition changes.
#   - RSI threshold is the most likely source of the 0.003 approximation gap.
#   - rsi=30.0 may simultaneously recover the exact Gen 20502 AND improve Sharpe.
#
# ══════════════════════════════════════════════════════════════════════
# RESULT CLASSIFICATION — WHAT DID YOU GET?
# ══════════════════════════════════════════════════════════════════════
#
# trades=0, Sharpe=0.0000 [max_trades_reject]:
#   YOU USED THE POISON UI YAML. Go back to STEP 1. Use that YAML exactly.
#
# trades=58, Sharpe≈1.3604 [wrong_base]:
#   YOU USED THE WRONG BASE (Gen 22157 or UI poison). Go back to STEP 1.
#
# trades=54, Sharpe≈1.6027 [near_incumbent, no_change]:
#   You output the approximation without the D7a change (rsi=32.96 not 30.0).
#   Verify rsi value=30.0 in your YAML. Discard. Retest.
#
# trades=54, Sharpe≈1.6060 [D7a neutral]:
#   D7a confirmed neutral. Mark D7a dead. Next test: D7b (rsi=35.0).
#
# trades≥50, 1.30≤Sharpe<1.6060 [valid discard]:
#   D7a tested, did not beat incumbent. Mark D7a dead. Next test: D7b.
#
# trades<50 [too few — entry too tight]:
#   D7a tightened entry too much. Mark D7a dead. Next test: D7b (rsi=35.0).
#
# trades≥50, Sharpe>1.6060 [NEW BEST — SUCCESS]:
#   New incumbent found. Report immediately. Update YAML-INCUMBENT below.
#
# Sharpe<0 [catastrophic]:
#   Entry conditions inverted or multiple parameters changed. Check YAML.
#
# ══════════════════════════════════════════════════════════════════════
# YAML-INCUMBENT — GEN 20502 (APPROXIMATION — THIS IS YOUR BASE)
# ══════════════════════════════════════════════════════════════════════
#
# DO NOT MUTATE FROM THE UI. MUTATE FROM THIS YAML ONLY.
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
# True incumbent Sharpe: 1.6060 (gap ~0.003, likely rsi approximation)
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
#   Gen 22157: Sharpe=1.3604  ← INCORRECTLY ACCEPTED. DISCARD. WRONG BASE.
#   Gen 22174: Sharpe=1.4449, trades=51 ← valid result but below incumbent
#
# KEY INSIGHT: Every large gain came from entry condition tightening.
# Trade count dropped (58→52) as Sharpe rose. Fewer, better trades = quality.
# CLEAN RESULT = trades between 50 and 60 inclusive.
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES TEST QUEUE — ANCHORED TO GEN 20502
# ══════════════════════════════════════════════════════════════════════
#
# Rule: Change EXACTLY ONE parameter per generation from YAML-INCUMBENT.
# Rule: trades must be ≥ 50 for result to be valid.
# Rule: Sharpe must exceed 1.6060 to be accepted as new best.
#
# ── PHASE 3: ENTRY CONDITION VARIATIONS (HIGHEST PRIORITY) ──────────
#
# D7a: rsi value → 30.0                      ← ACTIVE TEST (D7a)
#      name: gen20502_rsi30
#      Status: ACTIVE — use STEP 1 YAML as-is
#
# D7b: rsi value → 35.0                      (test if D7a dead or trades<50)
#      name: gen20502_rsi35
#
# D7c: rsi value → 28.0                      (test if D7a and D7b dead)
#      name: gen20502_rsi28
#
# D8a: long price_change_pct value → -1.0    (after D7 series resolves)
#      name: gen20502_pricechg10
#
# D8b: long price_change_pct value → -0.3    (only if D8a dead)
#      name: gen20502_pricechg03
#
# D6a: long bollinger period_hours → 36      (after D7 and D8 resolve)
#      name: gen20502_boll36
#
# D6b: long bollinger period_hours → 60      (only if D6a dead)
#
# D9a: short price_change_pct value → 1.0
#      name: gen20502_shortprice10
#
# D9b: short bollinger period_hours → 72     (only if D9a dead)
#
# ── PHASE 1: RISK PARAMETER VARIATIONS (LOW PRIORITY) ───────────────
#
# D1: pause_if_down_pct → 10             ✅ DEAD (800+ gens, confirmed)
#
# D2: stop_if_down_pct → 20              ⏸ SUSPENDED (never cleanly tested)
#     name: gen20502_stopdown20
#     Retest after D7 series resolves.
#
# D3a: pause_hours → 24                  NOT STARTED
# D3b: pause_hours → 72                  NOT STARTED (only if D3a dead)
#
# ── PHASE 2: EXIT PARAMETER VARIATIONS (MEDIUM PRIORITY) ────────────
#
# D4a: timeout_hours → 240               NOT STARTED
# D4b: timeout_hours → 264               NOT STARTED (only if D4a dead)
# D4c: timeout_hours → 288               NOT STARTED (only if D4b dead)
# D4d: timeout_hours → 192               NOT STARTED (only if D4c dead)
#
# D5a: take_profit_pct → 12.0            NOT STARTED
# D5b: take_profit_pct → 13.0            NOT STARTED (only if D5a dead)
# D5c: take_profit_pct → 14.0            NOT STARTED (only if D5b dead)
# D5d: take_profit_pct → 15.0            NOT STARTED (only if D5c dead)
#
# ── PHASE 4: BROADER SEARCH (IF ALL D-SERIES DEAD) ──────────────────
# Escalate to MIMIR for: regime-conditional sizing, new indicator types,
# walk-forward validation, F&G as entry filter, RSI-distance position sizing.
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES STATUS SUMMARY
# ══════════════════════════════════════════════════════════════════════
#
# D1: ✅ DEAD     pause_if_down_pct=10 (confirmed dead 800+ gens)
# D2: ⏸ SUSPENDED stop_if_down_pct=20 (0 valid tests; retest after D7)
# D3: ⬜ NOT STARTED
# D4: ⬜ NOT STARTED
# D5: ⬜ NOT STARTED
# D6: ⬜ NOT STARTED
# D7: 🔵 ACTIVE   rsi threshold variations — D7a is current test
# D8: ⬜ NOT STARTED
# D9: ⬜ NOT STARTED
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
#
# * = incumbent value. Do not propose as a "change" — it is already the base.
#
# ══════════════════════════════════════════════════════════════════════
# FINAL CHECKLIST — VERIFY YOUR YAML BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# POISON CHECK — if any of these appear, DISCARD and use STEP 1 YAML:
#  ✗ size_pct = 30
#  ✗ max_open = 3
#  ✗ take_profit_pct = 6.63
#  ✗ pairs = [BTC/USD] only
#  ✗ timeout_hours = 129, 133, or 135
#  ✗ price_change_pct lt -0.38  (long entry)
#  ✗ price_change_pct gt 0.37   (short entry)
#
# CORRECT VALUES — must match exactly:
#  ✓ name               = gen20502_rsi30
#  ✓ pairs              = BTC/USD, ETH/USD, SOL/USD  (3 pairs)
#  ✓ size_pct           = 25.0
#  ✓ max_open           = 2
#  ✓ fee_rate           = 0.001
#  ✓ momentum_accelerating long   period=48, eq, false
#  ✓ bollinger_position long      period=48, eq, below_lower
#  ✓ macd_signal long             period=48, eq, bullish
#  ✓ price_change_pct long        period=24, lt, -0.5
#  ✓ rsi long                     period=14, lt, 30.0   ← THE ONE CHANGE
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