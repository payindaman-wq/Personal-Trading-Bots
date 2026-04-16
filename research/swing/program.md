```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 21401 | Incumbent: Gen 20502 (Sharpe=1.6060)
# MIMIR-reviewed 2026-04-15 (v41)
#
# ══════════════════════════════════════════════════════════════════════
# ☠️ POISON YAML DETECTOR — READ THIS BEFORE ANYTHING ELSE ☠️
# ══════════════════════════════════════════════════════════════════════
#
# BEFORE YOU READ ANYTHING ELSE: Does the YAML you are about to output
# contain ANY of these values?
#
#   size_pct: 30           ← POISON — wrong YAML fingerprint
#   max_open: 3            ← POISON — wrong YAML fingerprint
#   take_profit_pct: 6.63  ← POISON — wrong YAML fingerprint
#   pairs: [BTC/USD only]  ← POISON — wrong YAML fingerprint
#   timeout_hours: 129     ← POISON — dead value
#   timeout_hours: 135     ← POISON — dead value
#
# If YES to any of the above → STOP. DELETE EVERYTHING. Start over
# from YAML-INCUMBENT below. Do not copy from the UI. The UI is broken.
# The UI has ALWAYS shown the wrong YAML. Ignore it completely.
# The correct YAML is ONLY the one printed below as YAML-INCUMBENT.
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 NEAR-INCUMBENT REPRODUCTION DETECTOR 🚨
# ══════════════════════════════════════════════════════════════════════
#
# The following results are KNOWN BAD OUTCOMES — NOT improvements:
#
#   Sharpe=1.6027, trades=54, WR=44.4%  → DISCARD (near-incumbent)
#   Sharpe=1.6028, trades=54, WR=44.4%  → DISCARD (near-incumbent)
#
# These are NOT the incumbent (Sharpe=1.6060). They appear when:
#   (a) You reproduced the approximation YAML without applying the
#       intended change, OR
#   (b) The intended change had no measurable effect.
#
# The true incumbent is Sharpe=1.6060. Anything below that is DISCARD.
#
# If you see 1.6027 or 1.6028: your change did not improve the strategy.
# ODIN will discard it. Move to the next D-series item.
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 CRITICAL SYSTEM NOTICE 🚨
# ══════════════════════════════════════════════════════════════════════
#
# THE INCUMBENT IS GEN 20502: Sharpe=1.6060 | Trades=54 | WR=44.4%
#
# ⚠️ YAML-INCUMBENT STATUS: APPROXIMATION — PENDING EXACT RECOVERY ⚠️
#
# The exact Gen 20502 YAML has not been recovered. The YAML below is
# the best available approximation. It reproduces at Sharpe=1.6027–1.6028,
# NOT 1.6060. This 0.003 gap is structural and consistent across 800+
# generations. The approximation is wrong in at least one entry condition
# parameter. Most likely candidate: rsi value (currently 32.96 in
# approximation; Gen 20502 may have changed this).
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
#   pause_if_down_pct = 8                             ← assumed (pending recovery)
#   Entry conditions  = APPROXIMATE (see YAML below)
#
# MIMIR ACTION REQUIRED: Retrieve Gen 20502 YAML from ODIN backtest
# logs to resolve the 0.003 Sharpe gap before D-series results can be
# compared to a clean baseline.
#
# ══════════════════════════════════════════════════════════════════════
# YAML-INCUMBENT — GEN 20502 (APPROXIMATION — PENDING EXACT RECOVERY)
# ══════════════════════════════════════════════════════════════════════
#
# This is the base you must copy EXACTLY and modify by EXACTLY ONE
# parameter as specified in YOUR ONLY JOB THIS GENERATION.
# DO NOT change anything not specified. DO NOT copy from the UI.
#
# ```yaml
# name: gen20502_base
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
# This is a quality signal — fewer, better trades.
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
# WHY D2: D1 (pause_if_down_pct=10) was tested across 800+ generations
# (Gens 20601–21400) and produced no improvement over the approximation
# baseline. D1 is formally closed as DEAD. Advancing to D2.
# NOTE: C2 (same pause_if_down_pct=10 test) was also dead vs Gen 19808.
# This is consistent — D1 is genuinely dead.
#
# Expected result if change is neutral:  Sharpe≈1.6027–1.6060, trades≈54
# Expected result if change is positive: Sharpe > 1.6060, trades ≥ 50
# Expected result if change hurts:       Sharpe < 1.6027, trades 50–60
#
# OUTPUT THIS YAML:
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
#   stop_if_down_pct: 20        ← THIS IS THE ONLY CHANGE
#   pause_hours: 48
# ```
#
# ══════════════════════════════════════════════════════════════════════
# INTERPRETING YOUR RESULT
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   → You used the POISON YAML (size_pct=30, max_open=3, tp=6.63).
#   → Fix: delete output. Copy YAML-INCUMBENT above exactly. Apply
#     only the one change specified in YOUR ONLY JOB THIS GENERATION.
#
# Sharpe=1.6027 or 1.6028, trades=54, WR=44.4% [near-incumbent — discard]:
#   → You reproduced the approximation without applying the change, OR
#     the change (stop_if_down_pct=20) had no effect.
#   → Either way: DISCARD. Mark D2 dead. Proceed to D3.
#
# Sharpe≈1.6060, trades=54, WR=44.4% [reproduction — discard]:
#   → You reproduced the approximation at its upper bound.
#   → This means stop_if_down_pct=20 was neutral vs incumbent.
#   → Mark D2 dead. Proceed to D3.
#
# Sharpe between 1.30 and 1.6060, trades 50–60 [valid — discard]:
#   → Valid test. Change did not beat Gen 20502. Mark D2 dead.
#   → Proceed to D3.
#
# Sharpe > 1.6060, trades ≥ 50 [NEW BEST]:
#   → SUCCESS. New incumbent. Report immediately.
#   → Recover the YAML. Update YAML-INCUMBENT. Do not proceed to D3
#     until new incumbent is documented.
#
# trades < 50 [low_trades — invalid]:
#   → Entry conditions were accidentally changed or are too restrictive.
#   → Do NOT count as valid. Check YAML for accidental entry changes.
#
# Sharpe < 0 [catastrophic]:
#   → Entry conditions were accidentally inverted or severely changed.
#   → Check your YAML. You modified more than one parameter.
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES QUEUE — ANCHORED TO GEN 20502
# ══════════════════════════════════════════════════════════════════════
#
# Prerequisites status:
#   MIN_TRADES["futures_swing"] = 50    ✅ FIXED (Gen 20502, 2026-04-15)
#   Gen 20502 YAML recovery             ⏳ PENDING — use approximation
#
# ── PHASE 1: RISK PARAMETER VARIATIONS (LOW RISK) ──────────────────
#
# D1: pause_if_down_pct → 10            ✅ DEAD
#     Tested 800+ gens (20601–21400). Never improved over baseline.
#     Also dead vs Gen 19808 (C2). Confirmed dead. Do not re-test.
#
# D2: stop_if_down_pct → 20             ← ACTIVE TEST THIS GENERATION
#     name: gen20502_stopdown20
#     Change: stop_if_down_pct 18 → 20
#     Risk: LOW.
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
#      Rationale: 156h timeout may be cutting winners short. 240h = 10 days,
#      consistent with BTC swing cycle lengths.
# D4b: timeout_hours → 264 (only if D4a dead)
# D4c: timeout_hours → 288 (only if D4b dead)
# D4d: timeout_hours → 192 (only if D4c dead — shorter direction)
#
# D5a: take_profit_pct → 12.0
#      name: gen20502_tp120
#      Rationale: incumbent R:R is 6.3:1 (9.5/1.5). Larger TP may
#      capture more of swing moves given improved entry quality.
#      The dead list shows 10.0, 10.5, 11.0, 11.5 are all dead —
#      but 12.0+ has not been tested and is a meaningful step change.
# D5b: take_profit_pct → 13.0 (only if D5a dead)
# D5c: take_profit_pct → 14.0 (only if D5b dead)
# D5d: take_profit_pct → 15.0 (only if D5c dead)
#
# ── PHASE 3: ENTRY CONDITION VARIATIONS (HIGH RISK / HIGH REWARD) ──
# ⚠️ Entry changes have highest variance. Test after Phases 1–2.
# ⚠️ Change only ONE condition parameter at a time.
# ⚠️ Monitor trades carefully — adding selectivity can collapse count.
# ⚠️ Do NOT add more than one new condition per generation.
# ⚠️ NOTE: The biggest Sharpe jumps in this run came from entry changes.
#    Phase 3 is HIGH PRIORITY once Phases 1–2 are exhausted.
#
# D6a: long bollinger period_hours → 36
#      name: gen20502_boll36
#      Risk: HIGH.
# D6b: long bollinger period_hours → 60 (only if D6a dead)
#
# D7a: rsi value → 30.0 (tighten long entry)
#      name: gen20502_rsi30
#      Rationale: 32.96 may be the approximation error. Testing 30.0
#      may both recover the true incumbent AND improve it.
# D7b: rsi value → 35.0 (loosen, only if D7a dead)
#      name: gen20502_rsi35
# D7c: rsi value → 28.0 (tighten further, only if D7a dead + D7b dead)
#      name: gen20502_rsi28
#
# D8a: long price_change_pct value → -1.0 (tighten)
#      name: gen20502_pricechg10
# D8b: long price_change_pct value → -0.3 (loosen, only if D8a dead)
#      name: gen20502_pricechg03
#
# D9:  SHORT entry exploration (lower priority — longs drive performance)
#      D9a: short price_change_pct value → 1.0 (tighten short trigger)
#           name: gen20502_shortprice10
#      D9b: short bollinger period_hours → 72 (if D9a dead)
#
# ── PHASE 4: BROADER SEARCH (IF ALL D-SERIES DEAD) ─────────────────
# If D1–D9 all confirm dead within 500 gens from this update:
#   - Escalate to MIMIR for broader search authorization
#   - Consider: regime-conditional sizing, new indicator types,
#     walk-forward validation, F&G index as entry filter,
#     position sizing tied to RSI distance from threshold
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES STATUS
# ══════════════════════════════════════════════════════════════════════
#
# D1: pause_if_down_pct=10              ✅ DEAD (800+ gens, no improvement)
# D2: stop_if_down_pct=20               ACTIVE ← TEST THIS GENERATION
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
# POISON CHECK (if any is true → discard and restart from YAML-INCUMBENT):
#  □ size_pct is NOT 30           ← wrong YAML
#  □ max_open is NOT 3            ← wrong YAML
#  □ take_profit_pct is NOT 6.63  ← wrong YAML
#  □ timeout_hours is NOT 129     ← wrong YAML
#  □ timeout_hours is NOT 135     ← wrong YAML
#  □ pairs is NOT [BTC/USD only]  ← wrong YAML
#
# FIELD-BY-FIELD VERIFICATION:
#  □ name     = gen20502_stopdown20  (matches active test)
#  □ pairs    = BTC/USD AND ETH/USD AND SOL/USD  (exactly 3 pairs)
#  □ size_pct = 25.0   (NOT 30)
#  □ max_open = 2      (NOT 3)
#  □ fee_rate = 0.001
#  □ Entry conditions = EXACTLY as in YAML-INCUMBENT (no changes)
#  □ take_profit_pct  = 9.5    (unchanged)
#  □ stop_loss_pct    = 1.5    (unchanged)
#  □ timeout_hours    = 156    (unchanged)
#  □ pause_if_down_pct = 8    (unchanged — D1 is DEAD, do not set to 10)
#  □ stop_if_down_pct = 20   ← ONLY CHANGE FOR D2
#  □ pause_hours      = 48    (unchanged)
#  □ Count of changed fields = EXACTLY 1
#
# ══════════════════════════════════════════════════════════════════════
# HISTORICAL C-SERIES ARCHIVE (pre-Gen 20502)
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs [BTC/USD, ETH/USD]           CONFIRMED DEAD (Gen 19024, Sharpe=1.2809)
# C8 = pairs [BTC/USD, SOL/USD]           CONFIRMED DEAD (Gen 19034, Sharpe=1.3415)
# C9 = pairs [BTC/USD, ETH/USD, SOL/USD]  CONFIRMED WIN  (Gen 19808, Sharpe=1.3483)
# C2 = pause_if_down_pct=10 vs Gen 19808  CONFIRMED DEAD vs 19808 (best=1.3137)
#      Reconfirmed dead vs Gen 20502 as D1. 800+ gens, no improvement.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: CAUTION | F&G=23 (Extreme Fear) | BTC Dominance=57.29%
# TYR Directive: Reduce LIVE position sizes to 50% (live size_pct ≈ 12.5)
# Backtest optimization continues at size_pct=25.0 — do NOT change this.
# Live performance: WR 50–67% live vs 41–44% backtest — real edge confirmed.
# Note: Live outperformance may partly reflect favorable regime since deployment.
#       Do not optimize for live WR — optimize for backtest Sharpe.
# F&G Extreme Fear (23): historically a long entry signal. Current strategy's
#   mean-reversion long entry stack may be well-suited to this environment.
#   Do not add F&G as an explicit filter — risk of overfitting to current regime.
#
# ══════════════════════════════════════════════════════════════════════
# INTERNAL AUDIT NOTES (DO NOT RELAY TO LLM)
# ══════════════════════════════════════════════════════════════════════
#
# [RESOLVED] MIN_TRADES["futures_swing"] = 50
#   Fixed at Gen 20502 (2026-04-15). No regression observed. Confirmed correct.
#
# [CRITICAL — BLOCKING] GEN 20502 YAML NOT RECOVERED.
#   The YAML-INCUMBENT contains an approximation only. Evidence:
#   - Gens 20584–21400 consistently reproduce at Sharpe=1.6027–1.6028, not 1.6060.
#   - The 0.003–