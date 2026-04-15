```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 20601 | Incumbent: Gen 20502 (Sharpe=1.6060)
# MIMIR-reviewed 2026-04-15 (v40)
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
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 NEW CONTAMINATION SIGNATURE — CRITICAL 🚨
# ══════════════════════════════════════════════════════════════════════
#
# If your result is: Sharpe=1.6027, trades=54, WR=44.4%
#
# This is a KNOWN BAD RESULT. It means you output a near-copy of the
# incumbent but with a small unintended difference. This is NOT the
# incumbent (which is Sharpe=1.6060). This is NOT an improvement.
# ODIN will discard it.
#
# If you see this result, it means:
#   (a) You did not apply the intended change correctly, OR
#   (b) You applied an unintended change that degraded Sharpe slightly.
#
# Fix: Re-read YAML-INCUMBENT below. Apply EXACTLY ONE change as
# specified in YOUR ONLY JOB THIS GENERATION. Nothing else.
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 CRITICAL SYSTEM NOTICE 🚨
# ══════════════════════════════════════════════════════════════════════
#
# THE INCUMBENT IS GEN 20502: Sharpe=1.6060 | Trades=54 | WR=44.4%
#
# ⚠️ YAML-INCUMBENT STATUS: PENDING RECOVERY FROM BACKTEST LOGS ⚠️
#
# The exact Gen 20502 YAML has not yet been recovered.
# The YAML-INCUMBENT below is the best available approximation.
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
#   Entry conditions  = UNKNOWN (pending recovery)
#
# UNTIL THE YAML IS RECOVERED:
#   - Use the YAML-INCUMBENT below as the working base
#   - Apply your assigned change to it
#   - Document any result precisely so recovery can be inferred
#
# MIMIR ACTION REQUIRED: Retrieve Gen 20502 YAML from ODIN backtest
# logs and replace the YAML-INCUMBENT placeholder below.
#
# ══════════════════════════════════════════════════════════════════════
# YAML-INCUMBENT — GEN 20502 (APPROXIMATION — PENDING EXACT RECOVERY)
# ══════════════════════════════════════════════════════════════════════
#
# This is the base you must copy exactly and modify by ONE parameter.
# DO NOT change anything not specified in YOUR ONLY JOB THIS GENERATION.
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
# ⚠️ IMPORTANT: The entry conditions above are the BEST APPROXIMATION
# based on the known trajectory. Gen 20502 improved over Gen 19808 via
# entry condition changes that are not yet confirmed. The above may
# reproduce at Sharpe≈1.6027 (not 1.6060) if the entry conditions are
# slightly wrong. This is expected until YAML recovery is complete.
# Continue testing — the relative improvement direction is still valid.
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
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# ACTIVE TEST: D1
# TEST NAME: gen20502_pause10
# CHANGE: pause_if_down_pct from 8 → 10
# EXACTLY ONE FIELD CHANGES. EVERYTHING ELSE IS IDENTICAL TO YAML-INCUMBENT.
#
# Expected result if change is neutral:  Sharpe≈1.6027–1.6060, trades≈54
# Expected result if change is positive: Sharpe > 1.6060, trades ≥ 50
# Expected result if change hurts:       Sharpe < 1.6027, trades 50–60
#
# OUTPUT THIS YAML:
#
# ```yaml
# name: gen20502_pause10
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
#   pause_if_down_pct: 10        ← THIS IS THE ONLY CHANGE
#   stop_if_down_pct: 18
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
# Sharpe=1.6027, trades=54, WR=44.4% [discarded]:
#   → You reproduced the near-incumbent approximation exactly.
#   → The D1 change (pause_if_down_pct=10) was either not applied
#     or had no effect on this metric.
#   → This does NOT mean D1 is dead — it means the base YAML may
#     still be slightly wrong. Report this result precisely.
#   → Proceed to D2 on next generation.
#
# Sharpe≈1.6060, trades=54, WR=44.4% [discarded — reproduction]:
#   → You reproduced Gen 20502 exactly. Good for one confirmation.
#   → For the actual D1 test: ensure pause_if_down_pct=10 is set.
#
# Sharpe=1.3483, trades=58 [discarded]:
#   → You reproduced the OLD Gen 19808 incumbent. Wrong base YAML.
#   → Fix: use YAML-INCUMBENT above, not Gen 19808.
#
# Sharpe between 1.30 and 1.6060, trades 50–60 [discarded]:
#   → Valid test. Change did not beat Gen 20502. Mark D1 dead.
#   → Proceed to D2.
#
# Sharpe > 1.6060, trades ≥ 50 [NEW BEST]:
#   → SUCCESS. New incumbent. Report immediately.
#   → Recover the YAML. Do not proceed to D2 until new incumbent
#     is documented.
#
# trades < 50 [low_trades]:
#   → Entry conditions are too restrictive or were accidentally changed.
#   → Do NOT count as a valid test. Check your YAML for accidental
#     entry condition modifications.
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
# D1: pause_if_down_pct → 10            ← ACTIVE TEST THIS GENERATION
#     name: gen20502_pause10
#     Change: pause_if_down_pct 8 → 10
#     Risk: LOW. No trade-count impact expected.
#
# D2: stop_if_down_pct → 20
#     name: gen20502_stopdown20
#     Change: stop_if_down_pct 18 → 20
#     Risk: LOW.
#
# D3a: pause_hours → 24
#      name: gen20502_pausehours24
#      Risk: LOW.
# D3b: pause_hours → 72 (only if D3a fails)
#      name: gen20502_pausehours72
#
# ── PHASE 2: EXIT PARAMETER VARIATIONS (MEDIUM RISK) ───────────────
# ⚠️ Monitor trades 50–65.
#
# D4a: timeout_hours → 240
#      name: gen20502_timeout240
# D4b: timeout_hours → 264 (only if D4a fails)
# D4c: timeout_hours → 288 (only if D4b fails)
# D4d: timeout_hours → 192 (only if D4c fails — shorter direction)
#
# D5a: take_profit_pct → 12.0
#      name: gen20502_tp120
#      Rationale: incumbent R:R is 6.3:1 (9.5/1.5). Larger TP may
#      capture more of swing moves given improved entry quality.
# D5b: take_profit_pct → 13.0 (only if D5a fails)
# D5c: take_profit_pct → 14.0 (only if D5b fails)
# D5d: take_profit_pct → 15.0 (only if D5c fails)
#
# ── PHASE 3: ENTRY CONDITION VARIATIONS (HIGH RISK / HIGH REWARD) ──
# ⚠️ Entry changes have highest variance. Test after Phases 1–2.
# ⚠️ Monitor trades carefully. Adding conditions can collapse count.
# ⚠️ Change only ONE condition parameter at a time.
# ⚠️ Do NOT add more than one new condition per generation.
#
# D6a: long bollinger period_hours → 36
#      name: gen20502_boll36
#      Risk: HIGH.
# D6b: long bollinger period_hours → 60 (only if D6a fails)
#
# D7: RSI threshold exploration
#     D7a: rsi value → 30.0 (tighten long entry)
#          name: gen20502_rsi30
#     D7b: rsi value → 35.0 (loosen long entry, only if D7a fails)
#
# D8: price_change_pct threshold exploration
#     D8a: long price_change_pct value → -1.0 (tighten)
#          name: gen20502_pricechg10
#     D8b: long price_change_pct value → -0.3 (loosen, only if D8a fails)
#
# ── PHASE 4: BROADER SEARCH (IF ALL D-SERIES DEAD) ─────────────────
# If D1–D8 all confirm dead within 500 gens from Gen 20502:
#   - Escalate to MIMIR for broader search authorization
#   - Consider: regime-conditional sizing, new indicator types,
#     walk-forward validation, F&G index as entry filter
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES STATUS
# ══════════════════════════════════════════════════════════════════════
#
# D1: pause_if_down_pct=10              ACTIVE ← TEST THIS GENERATION
# D2: stop_if_down_pct=20              NOT STARTED
# D3: pause_hours variations           NOT STARTED
# D4: timeout_hours variations         NOT STARTED
# D5: take_profit_pct variations       NOT STARTED
# D6: bollinger period variations      NOT STARTED
# D7: rsi threshold variations         NOT STARTED
# D8: price_change_pct variations      NOT STARTED
#
# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:       129, 135, 138, 144, 156*, 168, 192, 216
# take_profit_pct:     6.63, 7.14, 7.36, 7.38, 9.5*, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct:       1.5*, 2.0, 2.5
# pause_if_down_pct:   8* (incumbent baseline)
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
#  □ name     = gen20502_pause10  (matches active test)
#  □ pairs    = BTC/USD AND ETH/USD AND SOL/USD  (exactly 3 pairs)
#  □ size_pct = 25.0   (NOT 30)
#  □ max_open = 2      (NOT 3)
#  □ fee_rate = 0.001
#  □ Entry conditions = EXACTLY as in YAML-INCUMBENT (no changes)
#  □ take_profit_pct  = 9.5    (unchanged)
#  □ stop_loss_pct    = 1.5    (unchanged)
#  □ timeout_hours    = 156    (unchanged)
#  □ pause_if_down_pct = 10   ← ONLY CHANGE FOR D1
#  □ stop_if_down_pct = 18    (unchanged)
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
#      NOTE: C2 must be re-tested against Gen 20502 as D1. Gen 19808 result
#      does not carry over — the new incumbent is significantly different.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: CAUTION | F&G=23 (Extreme Fear) | BTC Dominance=57.35%
# TYR Directive: Reduce LIVE position sizes to 50% (live size_pct ≈ 12.5)
# Backtest optimization continues at size_pct=25.0 — do NOT change this.
# Live performance: WR 50–67% live vs 41–44% backtest — real edge confirmed.
# Note: Live outperformance may partly reflect favorable regime since deployment.
#       Do not optimize for live WR — optimize for backtest Sharpe.
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
#   - Gens 20584–20600 consistently reproduce at Sharpe=1.6027, not 1.6060.
#   - The 0.0033 gap is consistent and repeatable — this is structural, not noise.
#   - The approximation is therefore slightly wrong in at least one parameter.
#   - Most likely discrepancy: one entry condition parameter (rsi threshold,
#     price_change_pct threshold, or bollinger period_hours).
#   - MIMIR must retrieve the exact Gen 20502 YAML from backtest logs.
#   - Until recovered: D-series results are valid for relative direction
#     but absolute Sharpe targets may be off by ~0.003.
#   PRIORITY: CRITICAL. Blocks all D-series from having clean baselines.
#
# [CONTAMINATION — UI DISPLAY] ODIN UI still shows broken YAML
#   (size_pct=30, max_open=3, tp=6.63, pairs=[BTC/USD], timeout=135).
#   Approximately 20% of gens still produce max_trades_reject from this.
#   Last 20 gens: 4/20 = 20% contamination rate — unchanged from prior review.
#   Root fix required: update ODIN UI to display actual incumbent YAML.
#   Priority: HIGH. The POISON YAML DETECTOR is containing but not eliminating.
#
# [CONTAMINATION — NEAR-INCUMBENT REPRODUCTION] 8/20 recent gens produced
#   Sharpe=1.6027 (near-incumbent reproduction without improvement).
#   This is the dominant failure mode, now at 40% of gens.
#   Cause: LLM has converged on the approximation YAML as its baseline.
#   The full YAML with explicit test output in the research program should
#   reduce this — the LLM has less ambiguity about what to output.
#   Monitor: if reproduction rate exceeds 50% of non-poison gens, consider
#   adding a stronger "do not reproduce" directive.
#
# [ANALYTICAL — 1.6027 vs 1.6060 GAP]
#   This gap first appeared at Gen 20584 and has been perfectly consistent
#   for 12+ generations. The approximation YAML is wrong by exactly this margin.
#   Hypothesis ranking for where the approximation differs from truth:
#   (1) rsi threshold: approximation uses 32.96 (copied from old YAML).
#       Gen 20502 may have changed this. Most likely