```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 22158 | Incumbent: Gen 20502 (Sharpe=1.6060)
# MIMIR-reviewed 2026-04-16 (v43)
#
# ══════════════════════════════════════════════════════════════════════
# ██████████████████████████████████████████████████████████████████
# █                                                                  █
# █   STEP 1 — OUTPUT THIS YAML RIGHT NOW. DO THIS FIRST.           █
# █   BEFORE READING ANYTHING ELSE. BEFORE ANY ANALYSIS.            █
# █                                                                  █
# ██████████████████████████████████████████████████████████████████
#
# Copy the YAML below EXACTLY. Change ONLY rsi value from 32.96 to 30.0.
# Output it. Then read the rest of this document.
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
# ██████████████████████████████████████████████████████████████████
# █   STEP 1 COMPLETE. NOW READ THE REST.                           █
# ██████████████████████████████████████████████████████████████████
#
# ══════════════════════════════════════════════════════════════════════
# ☠️ POISON YAML DETECTOR ☠️
# ══════════════════════════════════════════════════════════════════════
#
# ══════════════════════════════════════════════════════════════════════
# ██████████████████████████████████████████████████████████████████
# █                                                                  █
# █  WARNING: THE "CURRENT BEST STRATEGY" SHOWN IN THE UI IS        █
# █  COMPLETELY WRONG. IT IS A BROKEN DISPLAY. IGNORE IT ENTIRELY.  █
# █                                                                  █
# █  THE UI CURRENTLY SHOWS EITHER:                                  █
# █    (A) An old POISON strategy (size_pct=30, max_open=3,         █
# █        take_profit_pct=6.63, BTC/USD only, timeout≈133)         █
# █    (B) A degraded strategy from Gen 22157 (Sharpe=1.3604,       █
# █        trades=58, win_rate=41.4%) — also WRONG, also DISCARD    █
# █                                                                  █
# █  THE TRUE INCUMBENT IS GEN 20502: Sharpe=1.6060                 █
# █  THE UI IS WRONG. THE UI IS WRONG. THE UI IS WRONG.             █
# █                                                                  █
# ██████████████████████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════
#
# POISON VALUES — ANY YAML CONTAINING THESE IS WRONG. DISCARD IT.
#   size_pct: 30           ← POISON (correct value: 25.0)
#   max_open: 3            ← POISON (correct value: 2)
#   take_profit_pct: 6.63  ← POISON (correct value: 9.5)
#   pairs: [BTC/USD only]  ← POISON (correct: 3 pairs)
#   timeout_hours: 129     ← POISON (correct value: 156)
#   timeout_hours: 133     ← POISON (correct value: 156)
#   timeout_hours: 135     ← POISON (correct value: 156)
#   price_change_pct long value: -0.38  ← POISON (correct: -0.5)
#   price_change_pct short value: 0.37  ← POISON (correct: 0.54)
#
# HOW TO VERIFY YOUR YAML IS CORRECT:
#   name        = gen20502_rsi30         ✓
#   size_pct    = 25.0                   ✓ (NOT 30)
#   max_open    = 2                      ✓ (NOT 3)
#   pairs       = BTC/USD, ETH/USD, SOL/USD  ✓ (3 pairs, NOT 1)
#   tp          = 9.5                    ✓ (NOT 6.63)
#   stop_loss   = 1.5                    ✓
#   timeout     = 156                    ✓ (NOT 129, 133, or 135)
#   rsi value   = 30.0                   ✓ ← THE ONE CHANGE
#   Everything else identical to YAML-INCUMBENT below.
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 CRITICAL SYSTEM NOTICE 🚨
# ══════════════════════════════════════════════════════════════════════
#
# THE TRUE INCUMBENT IS GEN 20502: Sharpe=1.6060 | Trades=54 | WR=44.4%
#
# ⚠️ Gen 22157 (Sharpe=1.3604) was incorrectly accepted as new_best.
# ⚠️ It scores 0.2456 BELOW the true incumbent Gen 20502.
# ⚠️ Gen 22157 must be treated as DISCARDED. Use Gen 20502 as base.
#
# ⚠️ YAML-INCUMBENT STATUS: APPROXIMATION — PENDING EXACT RECOVERY ⚠️
#
# The exact Gen 20502 YAML has not been recovered. The YAML below
# reproduces at Sharpe=1.6027–1.6028, NOT 1.6060.
# The 0.003 gap is likely due to the rsi value (approximation: 32.96).
# D7a (rsi=30.0) is now the ACTIVE TEST and highest priority —
# it may simultaneously recover the true incumbent AND improve Sharpe.
#
# KNOWN FACTS ABOUT GEN 20502 (confirmed from backtest trajectory):
#   pairs             = [BTC/USD, ETH/USD, SOL/USD]  ← confirmed
#   size_pct          = 25.0                          ← confirmed
#   max_open          = 2                             ← confirmed
#   fee_rate          = 0.001                         ← confirmed
#   stop_loss_pct     = 1.5                           ← confirmed
#   take_profit_pct   = 9.5                           ← confirmed
#   timeout_hours     = 156                           ← confirmed
#   stop_if_down_pct  = 18                            ← confirmed
#   pause_hours       = 48                            ← confirmed
#   pause_if_down_pct = 8                             ← assumed
#   rsi value         = 32.96 in approximation        ← UNCERTAIN
#   Entry conditions  = APPROXIMATE
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 RESULT CLASSIFICATION TABLE 🚨
# ══════════════════════════════════════════════════════════════════════
#
# Use this table to classify every backtest result immediately:
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   CAUSE: POISON YAML (size_pct=30, max_open=3).
#   YOU USED THE UI DISPLAY. IT IS WRONG. Go back to STEP 1.
#
# Sharpe≈1.3399, trades=58, WR=43.1% [wrong_base]:
#   CAUSE: You used Gen 19034 as your base instead of Gen 20502.
#   The UI is showing you the wrong strategy. Go back to STEP 1.
#
# Sharpe≈1.3604, trades=58, WR=41.4% [wrong_base_22157]:
#   CAUSE: You used Gen 22157 as your base. Gen 22157 is DISCARDED.
#   The UI may be showing this as "current best." IT IS WRONG.
#   Go back to STEP 1.
#
# Sharpe=1.6027 or 1.6028, trades=54, WR=44.4% [near_incumbent]:
#   CAUSE: You reproduced the approximation without the D7a change.
#   rsi value must be 30.0, not 32.96. Check your YAML.
#   DISCARD.
#
# Sharpe≈1.6060, trades=54, WR=44.4% [neutral]:
#   D7a was neutral. Mark D7a dead. Proceed to D7b (rsi=35.0).
#
# Sharpe between 1.30 and 1.6060, trades 50–60 [valid_discard]:
#   Valid test. Change did not beat Gen 20502. Mark D7a dead.
#   Proceed to D7b.
#
# trades < 50 [low_trades — invalid]:
#   Entry conditions corrupted. Do not count. Recheck YAML.
#
# Sharpe > 1.6060, trades ≥ 50 [NEW BEST — SUCCESS]:
#   New incumbent. Report immediately. Update YAML-INCUMBENT.
#   Document before proceeding.
#
# Sharpe < 0 [catastrophic]:
#   Entry conditions inverted. You modified more than one parameter.
#
# ══════════════════════════════════════════════════════════════════════
# YAML-INCUMBENT — GEN 20502 (APPROXIMATION)
# ══════════════════════════════════════════════════════════════════════
#
# THIS IS THE BASE. THIS IS WHAT YOU START FROM.
# DO NOT USE THE UI "CURRENT BEST STRATEGY". IT IS WRONG.
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
# True incumbent: Sharpe=1.6060 (gap ~0.003, likely rsi approximation)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT TRAJECTORY
# ══════════════════════════════════════════════════════════════════════
#
#   Gen 19808: Sharpe=1.3483, trades=58, WR=41.4%
#   Gen 20475: Sharpe=1.4877, trades=55, WR=43.6%  (+0.139)
#   Gen 20492: Sharpe=1.4898, trades=52, WR=50.0%  (+0.002)
#   Gen 20502: Sharpe=1.6060, trades=54, WR=44.4%  (+0.116) ← TRUE INCUMBENT
#
#   Gen 22157: Sharpe=1.3604, trades=58, WR=41.4%  ← INCORRECTLY ACCEPTED
#              This is BELOW incumbent. DISCARD. Do not use as base.
#
# Pattern: ALL large improvements came from ENTRY SELECTIVITY changes.
# Trade count fell (58→54) while Sharpe rose sharply.
# Fewer, better trades = quality signal. This is the key insight.
#
# CLEAN RESULT = trades between 50 and 60 inclusive
# DISCARD THRESHOLD = Sharpe must beat 1.6060 to be a new best
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# ACTIVE TEST: D7a
# TEST NAME: gen20502_rsi30
# CHANGE: rsi value from 32.96 → 30.0
# EXACTLY ONE FIELD CHANGES. EVERYTHING ELSE IS IDENTICAL TO YAML-INCUMBENT.
#
# The correct output YAML is already shown in STEP 1 at the top.
# Use that. Do not modify it further.
#
# WHY D7a IS NOW ACTIVE (replacing D2):
#   - D2 (stop_if_down_pct=20) was active since Gen 21401 (756+ gens).
#   - Zero valid D2 tests due to LLM compliance failure.
#   - D2 is being SUSPENDED (not dead — untested) to unblock progress.
#   - D7a is now active because:
#     1. RSI threshold is the most likely source of the 0.003 Sharpe
#        approximation gap. Testing rsi=30.0 may recover the exact
#        Gen 20502 YAML AND improve Sharpe simultaneously.
#     2. Entry condition changes have produced ALL historical large gains.
#     3. D7a is HIGH PRIORITY per Phase 3 analysis.
#
# WHY D2 IS SUSPENDED (not dead):
#   D2 has never been cleanly tested. It is suspended, not declared dead.
#   D2 will be retested after D7a resolves (or after compliance improves).
#
# Expected result if rsi=30.0 is the true value: Sharpe≈1.6060, trades≈54
# Expected result if change is positive:         Sharpe > 1.6060, trades ≥ 50
# Expected result if change is negative:         Sharpe < 1.6027, trades < 54
# Expected result if entry too tight:            trades < 50 [invalid]
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES QUEUE — ANCHORED TO GEN 20502
# ══════════════════════════════════════════════════════════════════════
#
# Prerequisites:
#   MIN_TRADES["futures_swing"] = 50    ✅ FIXED (Gen 20502, 2026-04-15)
#   Gen 20502 YAML recovery             ⏳ PENDING — use approximation
#
# ── PHASE 3 FIRST: ENTRY CONDITION VARIATIONS (HIGHEST PRIORITY) ───
# All large Sharpe gains came from entry changes. Test these first.
# ⚠️ Change only ONE condition parameter at a time.
# ⚠️ Monitor trades carefully — must stay ≥ 50.
#
# D7a: rsi value → 30.0 (tighten long entry)   ← ACTIVE TEST
#      name: gen20502_rsi30
#      Rationale: Most likely source of approximation gap.
#      May recover exact Gen 20502 AND improve. HIGHEST PRIORITY.
#      Status: ACTIVE
#
# D7b: rsi value → 35.0 (loosen, if D7a dead or trades < 50)
#      name: gen20502_rsi35
#      Only test if D7a produces trades < 50 or Sharpe < incumbent.
#
# D7c: rsi value → 28.0 (tighten further, if D7a dead and D7b dead)
#      name: gen20502_rsi28
#
# D8a: long price_change_pct value → -1.0 (tighten)
#      name: gen20502_pricechg10
#      Test after D7 series resolves.
#
# D8b: long price_change_pct value → -0.3 (loosen, only if D8a dead)
#      name: gen20502_pricechg03
#
# D6a: long bollinger period_hours → 36
#      name: gen20502_boll36
#      Test after D7 and D8 series resolve.
#
# D6b: long bollinger period_hours → 60 (only if D6a dead)
#
# D9a: short price_change_pct value → 1.0
#      name: gen20502_shortprice10
# D9b: short bollinger period_hours → 72 (only if D9a dead)
#
# ── PHASE 1: RISK PARAMETER VARIATIONS (LOW PRIORITY) ──────────────
# Risk changes have never produced improvements. Test after Phase 3.
#
# D1: pause_if_down_pct → 10            ✅ DEAD
#     Confirmed dead across 800+ gens (20601–21400).
#
# D2: stop_if_down_pct → 20             ⏸ SUSPENDED (untested, not dead)
#     Was active for 756 gens with zero valid tests due to compliance.
#     Suspended to unblock D7a. Retest after D7a resolves.
#     name: gen20502_stopdown20
#
# D3a: pause_hours → 24
#      name: gen20502_pausehours24
# D3b: pause_hours → 72 (only if D3a dead)
#
# ── PHASE 2: EXIT PARAMETER VARIATIONS (MEDIUM PRIORITY) ───────────
# Test after Phase 3 entry variations. Exit changes historically weak.
# ⚠️ Monitor trades 50–65.
#
# D4a: timeout_hours → 240
#      name: gen20502_timeout240
# D4b: timeout_hours → 264 (only if D4a dead)
# D4c: timeout_hours → 288 (only if D4b dead)
# D4d: timeout_hours → 192 (only if D4c dead)
#
# D5a: take_profit_pct → 12.0
#      name: gen20502_tp120
# D5b: take_profit_pct → 13.0 (only if D5a dead)
# D5c: take_profit_pct → 14.0 (only if D5b dead)
# D5d: take_profit_pct → 15.0 (only if D5c dead)
#
# ── PHASE 4: BROADER SEARCH (IF ALL D-SERIES DEAD) ─────────────────
# If D1–D9 all confirm dead:
#   - Escalate to MIMIR for broader search authorization
#   - Consider: regime-conditional sizing, new indicator types,
#     walk-forward validation, F&G as entry filter,
#     position sizing tied to RSI distance from threshold
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES STATUS
# ══════════════════════════════════════════════════════════════════════
#
# D1: pause_if_down_pct=10              ✅ DEAD (800+ gens, confirmed)
# D2: stop_if_down_pct=20               ⏸ SUSPENDED (0 valid tests, untested)
# D3: pause_hours variations            NOT STARTED (low priority)
# D4: timeout_hours variations          NOT STARTED (medium priority)
# D5: take_profit_pct variations        NOT STARTED (medium priority)
# D6: bollinger period variations       NOT STARTED
# D7: rsi threshold variations          ACTIVE ← D7a TEST THIS GENERATION
# D8: price_change_pct variations       NOT STARTED
# D9: short entry variations            NOT STARTED
#
# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:       129, 133, 135, 138, 144, 156*, 168, 192, 216
# take_profit_pct:     6.63, 7.14, 7.36, 7.38, 9.5*, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct:       1.5*, 2.0, 2.5
# pause_if_down_pct:   8* (incumbent), 10 (D1 dead)
# pairs combinations:  [BTC/USD only], [BTC/USD+ETH/USD only]
#
# * = incumbent value. Do not propose as a change.
#
# ══════════════════════════════════════════════════════════════════════
# MANDATORY OUTPUT CHECKLIST — VERIFY BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# POISON CHECK (if any of these appear in your YAML → DISCARD and use STEP 1):
#  ✗ size_pct = 30              ← POISON
#  ✗ max_open = 3               ← POISON
#  ✗ take_profit_pct = 6.63     ← POISON
#  ✗ pairs = [BTC/USD only]     ← POISON
#  ✗ timeout_hours = 129        ← POISON
#  ✗ timeout_hours = 133        ← POISON
#  ✗ timeout_hours = 135        ← POISON
#  ✗ price_change_pct lt -0.38  ← POISON (long entry)
#  ✗ price_change_pct gt 0.37   ← POISON (short entry)
#
# CORRECT VALUES (must match exactly):
#  □ name               = gen20502_rsi30
#  □ pairs              = BTC/USD AND ETH/USD AND SOL/USD (3 pairs)
#  □ size_pct           = 25.0   (NOT 30)
#  □ max_open           = 2      (NOT 3)
#  □ fee_rate           = 0.001
#  □ momentum_accelerating long  period=48, eq, false   ✓
#  □ bollinger_position long     period=48, eq, below_lower  ✓
#  □ macd_signal long            period=48, eq, bullish  ✓
#  □ price_change_pct long       period=24, lt, -0.5    ✓ (NOT -0.38, NOT -0.3)
#  □ rsi long                    period=14, lt, 30.0    ✓ ← THE ONE CHANGE
#  □ momentum_accelerating short period=48, eq, false   ✓
#  □ bollinger_position short    period=168, eq, above_upper  ✓
#  □ macd_signal short           period=24, eq, bearish  ✓
#  □ price_change_pct short      period=24, gt, 0.54    ✓ (NOT 0.37)
#  □ take_profit_pct    = 9.5    (NOT 6.63)
#  □ stop_loss_pct      = 1.5
#  □ timeout_hours      = 156    (NOT 129, 133, or 135)
#  □