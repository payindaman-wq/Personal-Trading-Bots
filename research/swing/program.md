```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 21801 | Incumbent: Gen 20502 (Sharpe=1.6060)
# MIMIR-reviewed 2026-04-16 (v42)
#
# ══════════════════════════════════════════════════════════════════════
# ██████████████████████████████████████████████████████████████████
# █                                                                  █
# █   STEP 1 — OUTPUT THIS YAML RIGHT NOW. DO THIS FIRST.           █
# █   BEFORE READING ANYTHING ELSE. BEFORE ANY ANALYSIS.            █
# █                                                                  █
# ██████████████████████████████████████████████████████████████████
#
# Copy the YAML below EXACTLY. Change ONLY stop_if_down_pct from 18 to 20.
# Output it. Then read the rest of this document.
#
# ```yaml
# name: gen20502_stopdown20
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
#   stop_if_down_pct: 20
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
# WARNING: THE "CURRENT BEST STRATEGY" SHOWN IN THE UI IS WRONG.
# IT IS A STALE DISPLAY BUG. IT SHOWS AN OLD STRATEGY THAT SCORES
# Sharpe=0.0000 (zero trades, immediate reject). DO NOT USE IT.
#
# The UI shows these POISON values — NEVER use them:
#   size_pct: 30           ← POISON
#   max_open: 3            ← POISON
#   take_profit_pct: 6.63  ← POISON
#   pairs: [BTC/USD only]  ← POISON
#   timeout_hours: 129     ← POISON
#   timeout_hours: 135     ← POISON
#
# If your YAML contains ANY of these → DELETE IT. Use STEP 1 YAML above.
#
# HOW TO VERIFY YOUR YAML IS CORRECT:
#   size_pct    = 25.0  ✓ (NOT 30)
#   max_open    = 2     ✓ (NOT 3)
#   pairs       = 3 pairs: BTC/USD, ETH/USD, SOL/USD  ✓
#   tp          = 9.5   ✓ (NOT 6.63)
#   timeout     = 156   ✓ (NOT 129, NOT 135)
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 CRITICAL SYSTEM NOTICE 🚨
# ══════════════════════════════════════════════════════════════════════
#
# THE INCUMBENT IS GEN 20502: Sharpe=1.6060 | Trades=54 | WR=44.4%
#
# ⚠️ YAML-INCUMBENT STATUS: APPROXIMATION — PENDING EXACT RECOVERY ⚠️
#
# The exact Gen 20502 YAML has not been recovered. The YAML in STEP 1
# is the best available approximation. It reproduces at Sharpe=1.6027–
# 1.6028, NOT 1.6060. The 0.003 gap is structural. Most likely cause:
# rsi value (approximation uses 32.96; true value unknown).
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
#   Entry conditions  = APPROXIMATE (rsi value uncertain)
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 NEAR-INCUMBENT REPRODUCTION DETECTOR 🚨
# ══════════════════════════════════════════════════════════════════════
#
# KNOWN BAD OUTCOMES — these mean your change had no effect:
#
#   Sharpe=1.6027, trades=54, WR=44.4%  → DISCARD (approximation reproduced)
#   Sharpe=1.6028, trades=54, WR=44.4%  → DISCARD (approximation reproduced)
#
# The true incumbent is Sharpe=1.6060. Anything below is DISCARD.
#
# ALSO KNOWN BAD — these mean you used the wrong base YAML:
#
#   Sharpe=1.3399, trades=58, WR=43.1%  → WRONG BASE (Gen 19034 level)
#   Sharpe=0.0000, trades=0             → POISON YAML (UI display bug)
#   trades < 50                         → Entry conditions corrupted
#
# ══════════════════════════════════════════════════════════════════════
# YAML-INCUMBENT — GEN 20502 (APPROXIMATION — SAME AS STEP 1 YAML)
# ══════════════════════════════════════════════════════════════════════
#
# This is the base YAML. For D2, the only change is stop_if_down_pct=20.
# This is already shown in STEP 1. Do not modify anything else.
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT TRAJECTORY
# ══════════════════════════════════════════════════════════════════════
#
#   Gen 19808: Sharpe=1.3483, trades=58, WR=41.4%
#   Gen 20475: Sharpe=1.4877, trades=55, WR=43.6%  (+0.139)
#   Gen 20492: Sharpe=1.4898, trades=52, WR=50.0%  (+0.002)
#   Gen 20502: Sharpe=1.6060, trades=54, WR=44.4%  (+0.116) ← CURRENT
#
# Pattern: improvements came from ENTRY SELECTIVITY changes.
# Trade count fell (58→54) while Sharpe rose sharply.
# Fewer, better trades = quality signal.
#
# CLEAN RESULT = trades between 50 and 60 inclusive
# BEST KNOWN SHARPE = 1.6060 — anything below this is DISCARD
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# ACTIVE TEST: D2
# TEST NAME: gen20502_stopdown20
# CHANGE: stop_if_down_pct from 18 → 20
# EXACTLY ONE FIELD CHANGES. EVERYTHING ELSE IS IDENTICAL TO YAML-INCUMBENT.
#
# The correct output YAML is already shown in STEP 1 at the top.
# Use that. Do not modify it further.
#
# WHY D2: D1 (pause_if_down_pct=10) was tested across 800+ generations
# (Gens 20601–21400) and produced no improvement. D1 is DEAD.
# Advancing to D2.
#
# Expected result if change is neutral:  Sharpe≈1.6027–1.6060, trades≈54
# Expected result if change is positive: Sharpe > 1.6060, trades ≥ 50
# Expected result if change hurts:       Sharpe < 1.6027, trades 50–60
#
# ══════════════════════════════════════════════════════════════════════
# INTERPRETING YOUR RESULT
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   → POISON YAML. You used the UI display (size_pct=30, max_open=3).
#   → Fix: go back to STEP 1. Copy that YAML exactly.
#
# Sharpe=1.3399, trades=58 [wrong base]:
#   → You used Gen 19034 base instead of Gen 20502.
#   → Fix: go back to STEP 1. Copy that YAML exactly.
#
# Sharpe=1.6027 or 1.6028, trades=54 [near-incumbent — discard]:
#   → Approximation reproduced without the change taking effect.
#   → DISCARD. Mark D2 dead. Proceed to D3a.
#
# Sharpe≈1.6060, trades=54 [neutral — discard]:
#   → stop_if_down_pct=20 was neutral vs incumbent.
#   → Mark D2 dead. Proceed to D3a.
#
# Sharpe between 1.30 and 1.6060, trades 50–60 [valid — discard]:
#   → Valid test. Change did not beat Gen 20502. Mark D2 dead.
#   → Proceed to D3a.
#
# Sharpe > 1.6060, trades ≥ 50 [NEW BEST]:
#   → SUCCESS. New incumbent. Report immediately.
#   → Update YAML-INCUMBENT. Do not proceed to D3a until documented.
#
# trades < 50 [low_trades — invalid]:
#   → Entry conditions were corrupted. Do not count as valid.
#   → Recheck YAML against STEP 1.
#
# Sharpe < 0 [catastrophic]:
#   → Entry conditions inverted or severely changed.
#   → You modified more than one parameter.
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES QUEUE — ANCHORED TO GEN 20502
# ══════════════════════════════════════════════════════════════════════
#
# Prerequisites:
#   MIN_TRADES["futures_swing"] = 50    ✅ FIXED (Gen 20502, 2026-04-15)
#   Gen 20502 YAML recovery             ⏳ PENDING — use approximation
#
# ── PHASE 1: RISK PARAMETER VARIATIONS (LOW RISK) ──────────────────
#
# D1: pause_if_down_pct → 10            ✅ DEAD
#     Tested 800+ gens (20601–21400). Never improved. Confirmed dead.
#
# D2: stop_if_down_pct → 20             ← ACTIVE TEST THIS GENERATION
#     name: gen20502_stopdown20
#     Change: stop_if_down_pct 18 → 20
#     NOTE: Due to LLM compliance failures, D2 has not been cleanly
#     tested despite being active since Gen 21401. Continue testing.
#
# D3a: pause_hours → 24
#      name: gen20502_pausehours24
#      Risk: LOW.
# D3b: pause_hours → 72 (only if D3a dead)
#      name: gen20502_pausehours72
#
# ── PHASE 2: EXIT PARAMETER VARIATIONS (MEDIUM RISK) ───────────────
# ⚠️ Monitor trades 50–65.
#
# D4a: timeout_hours → 240
#      name: gen20502_timeout240
#      Rationale: 156h timeout may cut winners short. 240h = 10 days.
# D4b: timeout_hours → 264 (only if D4a dead)
# D4c: timeout_hours → 288 (only if D4b dead)
# D4d: timeout_hours → 192 (only if D4c dead — shorter direction)
#
# D5a: take_profit_pct → 12.0
#      name: gen20502_tp120
#      Rationale: 10.0–11.5 all dead. 12.0+ not yet tested.
# D5b: take_profit_pct → 13.0 (only if D5a dead)
# D5c: take_profit_pct → 14.0 (only if D5b dead)
# D5d: take_profit_pct → 15.0 (only if D5c dead)
#
# ── PHASE 3: ENTRY CONDITION VARIATIONS (HIGH RISK / HIGH REWARD) ──
# ⚠️ Change only ONE condition parameter at a time.
# ⚠️ Monitor trades carefully — entry selectivity can collapse count.
# ⚠️ Do NOT add more than one new condition per generation.
# ⚠️ NOTE: Biggest Sharpe jumps came from entry changes. HIGH PRIORITY.
#
# D7a: rsi value → 30.0 (tighten long entry)   ← HIGH PRIORITY
#      name: gen20502_rsi30
#      Rationale: 32.96 is the approximation value. Testing 30.0 may
#      BOTH recover the true incumbent AND improve it. Test early.
# D7b: rsi value → 35.0 (loosen, only if D7a dead)
#      name: gen20502_rsi35
# D7c: rsi value → 28.0 (tighten further, only if D7a+D7b dead)
#      name: gen20502_rsi28
#
# D6a: long bollinger period_hours → 36
#      name: gen20502_boll36
#      Risk: HIGH.
# D6b: long bollinger period_hours → 60 (only if D6a dead)
#
# D8a: long price_change_pct value → -1.0 (tighten)
#      name: gen20502_pricechg10
# D8b: long price_change_pct value → -0.3 (loosen, only if D8a dead)
#      name: gen20502_pricechg03
#
# D9:  SHORT entry exploration (lower priority)
#      D9a: short price_change_pct value → 1.0
#           name: gen20502_shortprice10
#      D9b: short bollinger period_hours → 72 (if D9a dead)
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
# D2: stop_if_down_pct=20               ACTIVE ← TEST THIS GENERATION
#     NOTE: Active since Gen 21401. LLM compliance failures prevented
#     clean testing. No valid D2 result yet. Continue.
# D3: pause_hours variations            NOT STARTED
# D4: timeout_hours variations          NOT STARTED
# D5: take_profit_pct variations        NOT STARTED
# D6: bollinger period variations       NOT STARTED
# D7: rsi threshold variations          NOT STARTED (HIGH PRIORITY)
# D8: price_change_pct variations       NOT STARTED
# D9: short entry variations            NOT STARTED
#
# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:       129, 135, 138, 144, 156*, 168, 192, 216
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
# POISON CHECK (if any is true → discard and use STEP 1 YAML):
#  □ size_pct is NOT 30           ← wrong YAML
#  □ max_open is NOT 3            ← wrong YAML
#  □ take_profit_pct is NOT 6.63  ← wrong YAML
#  □ timeout_hours is NOT 129     ← wrong YAML
#  □ timeout_hours is NOT 135     ← wrong YAML
#  □ pairs is NOT [BTC/USD only]  ← wrong YAML
#
# FIELD-BY-FIELD VERIFICATION:
#  □ name               = gen20502_stopdown20
#  □ pairs              = BTC/USD AND ETH/USD AND SOL/USD (3 pairs)
#  □ size_pct           = 25.0   (NOT 30)
#  □ max_open           = 2      (NOT 3)
#  □ fee_rate           = 0.001
#  □ Entry conditions   = EXACTLY as in STEP 1 YAML (no changes)
#  □ take_profit_pct    = 9.5    (NOT 6.63)
#  □ stop_loss_pct      = 1.5
#  □ timeout_hours      = 156    (NOT 129, NOT 135)
#  □ pause_if_down_pct  = 8      (D1 is DEAD — do not set to 10)
#  □ stop_if_down_pct   = 20     ← ONLY CHANGE FOR D2
#  □ pause_hours        = 48
#  □ Changed fields     = EXACTLY 1
#
# ══════════════════════════════════════════════════════════════════════
# LLM COMPLIANCE FAILURE LOG (v42 DIAGNOSTIC)
# ══════════════════════════════════════════════════════════════════════
#
# Gens 21781–21800 showed severe LLM compliance failure:
#   - 5/20 gens: Sharpe=0 (POISON YAML, UI display anchor)
#   - 7/20 gens: Sharpe~1.33–1.34 (Gen 19034 base, wrong incumbent)
#   - 1/20 gens: trades=18 (entry conditions corrupted)
#   - 0/20 gens: valid D2 test result
#
# ROOT CAUSE: LLM anchors to "Current Best Strategy" UI display,
# which shows the old POISON YAML (size_pct=30, max_open=3, tp=6.63).
# The research program's YAML-INCUMBENT is being ignored in favor of
# the UI display.
#
# FIX APPLIED IN v42:
#   1. STEP 1 YAML moved to top of document — LLM sees it FIRST
#   2. POISON YAML explicitly labeled as "UI DISPLAY BUG"
#   3. Wrong-base results (1.3399/58) added to failure taxonomy
#   4. Repeated reinforcement of correct field values
#
# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: CAUTION | F&G=23 (Extreme Fear) | BTC Dominance=57.19%
# TYR Directive: Reduce LIVE position sizes to 50% (live size_pct ≈ 12.5)
# Backtest optimization continues at size_pct=25.0 — do NOT change this.
# Live performance: WR 50–67% live vs 41–44% backtest — real edge confirmed.
# Note: Live outperformance may partly reflect favorable regime.
#       Do not optimize for live WR — optimize for backtest Sharpe.
# F&G=23 (Extreme Fear): historically a long entry signal. Current
#   mean-reversion long entry stack is well-suited to this environment.
#   Do not add F&G as explicit filter — overfitting risk.
#
# ══════════════════════════════════════════════════════════════════════
# HISTORICAL C-SERIES ARCHIVE (pre-Gen 20502)
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs [BTC/USD, ETH/USD]           CONFIRMED DEAD (Gen 19024, 1.2809)
# C8 = pairs [BTC/USD, SOL/USD]           CONFIRMED DEAD (Gen 19034, 1.3415)
# C9 = pairs [BTC/USD, ETH/USD, SOL/USD]  CONFIRMED WIN  (Gen 19808, 1.3483)
# C2 = pause_if_down_pct=10 vs Gen 19808  CONFIRMED DEAD
#      Reconfirmed dead vs Gen 20502 as D1 (800+ gens).
#
# ══════════════════════════════════════════════════════════════════════
# INTERNAL AUDIT NOTES (DO NOT RELAY TO LLM)
# ══════════════════════════════════════════════════════════════════════
#
# [RESOLVED] MIN_TRADES["futures_swing"] = 50
#   Fixed at Gen 20502 (2026-04-15). Confirmed correct. No regression.
#
# [CRITICAL — BLOCKING] GEN 20502 YAML NOT RECOVERED.
#   Approximation error = 0.003 Sharpe. Consistent across 800+ gens.
#   Most likely candidate: rsi value (32.96 in approximation).
#   D7a (rsi=30.0) is high priority — may resolve gap AND improve.
#   MIMIR ACTION: Retrieve Gen 20502 YAML from backtest logs.
#
# [CRITICAL — NEW v42] LLM COMPLIANCE FAILURE RATE UNACCEPTABLE.
#   Gens 21781–21800: 0/20 valid D2 results.
#   Root cause: UI "Current Best Strategy" display shows POISON YAML.
#   LLM anchors to it. STEP 1 restructure is the mitigation.
#   MIMIR ACTION: Request ODIN operator update displayed strategy
#   OR suppress "Current Best Strategy" from LLM context if possible.
#   If compliance does not improve by Gen 21900, escalate to Phase 3
#   (suppress UI display from LLM prompt entirely).
#
# [MONITORING] D2 has been active since Gen 21401 (400 gens).
#   Zero valid tests due to compliance failure. Not declared dead.
#   D2 requires at least ONE clean test before death declaration.
```