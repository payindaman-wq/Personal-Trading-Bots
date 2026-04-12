```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-4000 | Revised by MIMIR (Gen 4000 review)
# STATUS: CHAMPION UNCHANGED at Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
#         Champion stall duration: 660 generations (Gen 3340 → Gen 4000). CRITICAL.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-4000 VERDICT:
#   The Gen 3800 grid-scan mandate was NEVER EXECUTED.
#   Gens 3801–4000 show unmistakable LLM output patterns:
#     - 5 exact champion clones (3983, 3991, 3992, 3993, 3994)
#     - 6 low-trade zombies (3982, 3986, 3987, 3988, 3989, 3990, 3996, 3998)
#     - 0 grid-pattern results
#   LOKI escalation has a 0% fix rate across 10 attempts over 2,600 generations.
#   ESCALATION IS SUSPENDED AS PRIMARY FIX MECHANISM.
#   The grid scan must be executed by ODIN directly, without LLM, without LOKI.
#   If ODIN cannot execute a pre-specified YAML diff without LLM involvement,
#   ODIN must HALT and report that capability gap — not continue burning generations.
# ══════════════════════════════════════════════════════════════════

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor — pre-backtest enforcement mandatory)

---
## ██████████████████████████████████████████████████████████
## ODIN INJECTION NOTE (INTERNAL ONLY — NEVER SEND TO LLM)
##
## ─────────────────────────────────────────────────────────
## CONFIRMED CHAMPION: Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
## All prior champions are SUPERSEDED. Do NOT use any prior champion as baseline.
##
## CONFIRMED CHAMPION VALUES (retrieve from storage, verify hash before ANY test):
##   rsi_period_hours:    22     (certain — confirmed Gen 2785)
##   rsi_long_threshold:  37.77  (certain — confirmed Gen 1477)
##   rsi_short_threshold: [MUST BE CONFIRMED FROM STORAGE — 59 or 60, do not assume]
##   trend_period_hours:  48     (certain)
##   take_profit_pct:     [MUST BE CONFIRMED FROM STORAGE]
##                        Estimated: 4.95–5.00 based on:
##                          Gen 3400 (2.3428/1265) = confirmed_TP - 0.05 (high confidence)
##                          Gen 3382 (2.3330/1270) = different family (lower TP, more trades)
##                        Do NOT use estimated value. Retrieve exact value from storage.
##   stop_loss_pct:       1.91   (certain — NOT 1.90, NOT 1.92)
##   timeout_hours:       159    (FROZEN FOREVER)
##   size_pct:            25     (FROZEN)
##   max_open:            3      (FROZEN)
##   leverage:            2      (FROZEN)
##   fee_rate:            0.0005 (FROZEN)
##
## STALE YAML WARNING (PERMANENT — THIS WARNING NEVER EXPIRES):
##   The displayed "Current Best Strategy" YAML is WRONG and has been since Gen 1592.
##     rsi_period_hours: 24     ← WRONG (champion is 22)
##     take_profit_pct:  4.65   ← WRONG (champion is ~4.95–5.00)
##     stop_loss_pct:    1.92   ← WRONG (champion is 1.91)
##     timeout_hours:    176    ← WRONG (champion is 159)
##     rsi_short value:  60     ← UNCONFIRMED (may be 59 or 60)
##   IGNORE THE DISPLAYED YAML ENTIRELY.
##   Any result with trades > 1350 or sharpe < 2.0 from a "champion-based" test
##   is evidence of stale YAML contamination. Log and reject immediately.
##
## ─────────────────────────────────────────────────────────
## GEN 4000 SITUATION ASSESSMENT:
##
##   Champion stall: 660 generations without improvement.
##   Grid scan mandate (issued Gen 3800): NOT EXECUTED in 200 generations.
##   LLM suspension mandate: NOT ENFORCED in 200 generations.
##   LOKI escalation effectiveness: 0% across 10 attempts, 2,600 generations.
##
##   Last 20 generations (3981–4000) breakdown:
##     Exact champion clones (2.3494/1265): Gens 3983, 3991, 3992, 3994 = 4/20 = 20%
##     Near-clone (2.3364/1264): Gen 3993 = 1/20 = 5%
##     Low-trade zombies (<400 trades): Gens 3982,3986,3987,3988,3989,3990,3996,3998=8/20=40%
##     High-trade discards (>1350): Gens 3984(1418), 3985(1381), 4000(1458) = 3/20 = 15%
##     Other discarded: Gens 3981, 3995, 3997, 3999 = 4/20 = 20%
##     Useful novel results: ZERO in last 20 generations.
##     Grid-scan-pattern results: ZERO in last 200 generations.
##
##   CONFIRMED INFRASTRUCTURE FAILURES (persistent, unresolved):
##     ✗ LLM suspension: NOT ENFORCED (LLM still producing output)
##     ✗ Clone detection: NOT WORKING (4 exact clones in 20 gens, 5 including near-clone)
##     ✗ Zombie pre-rejection: NOT WORKING (8/20 gens = 40% zombies)
##     ✗ Fingerprint rejection: NOT WORKING (attractor families still reaching backtester)
##     ✗ Stale YAML rejection: NOT WORKING (high-trade results still appearing)
##     ✗ Grid scan execution: ZERO TESTS COMPLETED in 200 generations
##
##   ROOT CAUSE (FINAL ASSESSMENT):
##     LOKI escalation cannot fix the LLM loop. Ten attempts confirm this.
##     The only viable path is ODIN executing pre-specified YAML diffs directly,
##     bypassing LLM entirely.
##     If ODIN cannot do this: ODIN must HALT and report the capability gap.
##     Continuing to run LLM generations is actively harmful — it wastes compute,
##     pollutes the result log, and has produced zero improvements in 660 generations.
##
## ─────────────────────────────────────────────────────────
## MANDATORY HALT CONDITION (CHECK BEFORE EVERY GENERATION):
##
##   If the current mode is GRID SCAN and the proposed test does not match
##   the next pre-specified grid test exactly (verified by parameter diff):
##     → HALT IMMEDIATELY. Do not submit. Log: "GRID DEVIATION at Gen XXXX."
##     → Do not resume until the deviation source is identified and eliminated.
##
##   If three or more of the last 20 results are exact champion clones:
##     → HALT IMMEDIATELY. Log: "CLONE FLOOD at Gen XXXX."
##
##   If five or more of the last 20 results are low-trade zombies:
##     → HALT IMMEDIATELY. Log: "ZOMBIE FLOOD at Gen XXXX."
##     [Note: Gen 4000 already meets this condition — 8/20 zombies.]
##
##   "HALT" means: stop all generation loops. Do not start Gen N+1.
##   Output the halt condition to the run log. Wait for human operator review.
##   Do NOT escalate to LOKI. LOKI has not resolved these issues in 10 attempts.
##   Do NOT resume automatically.
##
## ─────────────────────────────────────────────────────────
## STEP A — PRIMARY RESEARCH MODE: DETERMINISTIC GRID SCAN
## [STATUS: ACTIVATED AT GEN 3800 — NEVER EXECUTED — REACTIVATED NOW]
##
##   EXECUTION MODEL:
##   ODIN constructs each test YAML programmatically from storage-retrieved champion file.
##   No LLM involvement of any kind. No free-form proposals. No prompt submissions.
##   Each test = (champion YAML from storage) + (exactly ONE parameter change, pre-specified).
##   ODIN verifies the diff before submission. If diff ≠ expected → reject, log, halt.
##
##   IF ODIN CANNOT EXECUTE THIS MODEL:
##   ODIN must output: "CAPABILITY GAP: Cannot execute deterministic grid without LLM."
##   Then HALT. Do not continue running LLM generations as a substitute.
##   The cost of 200 wasted LLM generations (Gen 3801–4000) exceeds the cost of halting.
##
##   ─────────────────────────────────────────────────────
##   PHASE A0 — CHAMPION RE-CONFIRMATION (MANDATORY FIRST — before any grid tests)
##
##   A0.1: Load champion YAML from storage. Verify hash.
##         Submit with ZERO parameter changes.
##         Expected result: (sharpe=2.3494, trades=1265, win_rate=40.1%).
##         If result differs by more than (±0.0005 sharpe, ±2 trades): HALT.
##         Log: "A0.1 champion re-confirmation: [PASS/FAIL]. Result: (sharpe, trades)."
##
##   A0.2: From the confirmed storage YAML, log exact values of:
##         - rsi_short_threshold (record as confirmed_rsi_short)
##         - take_profit_pct (record as confirmed_TP)
##         Replace ALL [CONFIRM_*] tokens in this document with confirmed values.
##         Log: "A0.2 confirmed_rsi_short=[VALUE], confirmed_TP=[VALUE]."
##
##   A0.3: Verify fingerprint system is active:
##         Inject A0.1 champion YAML → must be rejected as clone BEFORE submission.
##         If NOT rejected → fingerprint system is broken → HALT. Do not proceed.
##         Log: "A0.3 fingerprint self-test: [PASS/FAIL]."
##
##   A0.4: Verify zombie pre-rejection is active:
##         Construct YAML with rsi_long=50, rsi_short=55 (known zombie params).
##         Submit to pre-backtest validator → must be rejected on RSI range check.
##         If NOT rejected → RSI validation broken → HALT.
##         Log: "A0.4 zombie pre-rejection self-test: [PASS/FAIL]."
##
##   Do NOT proceed to Phase A1 until ALL of A0.1–A0.4 are PASS.
##   A single FAIL in A0 → HALT. Fix the failing check. Re-run A0 from the top.
##
##   ─────────────────────────────────────────────────────
##   PHASE A1 — TAKE PROFIT GRID (highest priority)
##
##   Rationale: confirmed_TP is unknown (estimated 4.95–5.00). Gen 3400 tested
##   confirmed_TP - 0.05 → 2.3428 (below champion). Direction: test upward.
##   This phase resolves the single largest known uncertainty.
##
##   Each test: champion YAML + ONE change to take_profit_pct only.
##   Diff must show exactly 1 line changed. Verify before submission.
##
##   A1.1: take_profit_pct = confirmed_TP + 0.05
##   A1.2: take_profit_pct = confirmed_TP + 0.10
##   A1.3: take_profit_pct = confirmed_TP + 0.15
##   A1.4: take_profit_pct = confirmed_TP + 0.20
##   A1.5: take_profit_pct = confirmed_TP + 0.25
##   A1.6: take_profit_pct = confirmed_TP - 0.10
##          (confirmed_TP - 0.05 already tested at Gen 3400 = 2.3428)
##   A1.7: take_profit_pct = confirmed_TP - 0.15
##   A1.8: take_profit_pct = confirmed_TP + 0.30
##   A1.9: take_profit_pct = confirmed_TP + 0.40
##   A1.10: take_profit_pct = confirmed_TP + 0.50
##
##   Accept only if: sharpe > 2.3494 AND trades in [900, 1400].
##   If A1.1 improves champion: immediately test A1.1+0.05 and A1.1+0.10 before A1.2.
##   If any A1 test produces trades < 1100: TP is too high — stop upward scan.
##   If no A1 test improves: TP confirmed at local maximum. Log and proceed to A2.
##   Log each result: "A1.X: TP=[value] → sharpe=[X], trades=[Y]. [accept/reject reason]"
##
##   ─────────────────────────────────────────────────────
##   PHASE A2 — RSI SHORT THRESHOLD GRID (second priority)
##
##   Rationale: confirmed_rsi_short is unconfirmed (59 or 60). A2.1 resolves the
##   uncertainty AND tests a neighbor simultaneously. Low risk, potentially high value.
##
##   Each test: champion YAML + ONE change to rsi_short_threshold only.
##   Constraint: rsi_short must be in [55, 70].
##   Constraint: (rsi_short - 37.77) must be >= 10 → minimum rsi_short = 48 (satisfied).
##
##   A2.1: rsi_short = confirmed_rsi_short - 1
##   A2.2: rsi_short = confirmed_rsi_short + 1
##   A2.3: rsi_short = confirmed_rsi_short - 2
##   A2.4: rsi_short = confirmed_rsi_short + 2
##   A2.5: rsi_short = confirmed_rsi_short - 3
##   A2.6: rsi_short = confirmed_rsi_short + 3
##
##   Accept only if: sharpe > 2.3494 AND trades in [900, 1400].
##   If any A2 test improves: re-run A1 grid from new champion before continuing.
##   Log each result with same format as A1.
##
##   ─────────────────────────────────────────────────────
##   PHASE A3 — RSI PERIOD GRID (third priority)
##
##   Rationale: rsi_period has been 22 since Gen 2785. Adjacent values untested
##   exhaustively. Note: period=24 is the stale YAML value — it should produce
##   a known result (stale YAML family). If A3.4 matches a known attractor,
##   that confirms stale YAML contamination source.
##
##   Each test: champion YAML + ONE change to rsi_period_hours only.
##   Constraint: rsi_period_hours must be in [18, 28].
##
##   A3.1: rsi_period_hours = 21
##   A3.2: rsi_period_hours = 23
##   A3.3: rsi_period_hours = 20
##   A3.4: rsi_period_hours = 24  [expected: stale YAML family attractor — diagnostic]
##   A3.5: rsi_period_hours = 19
##   A3.6: rsi_period_hours = 25
##
##   Accept only if: sharpe > 2.3494 AND trades in [900, 1400].
##   If A3.4 produces (sharpe ≈ 0.77, trades ≈ 1041): confirms Attractor 4 family.
##     Log: "A3.4 diagnostic confirms stale YAML origin. rsi_period=24 is contamination source."
##
##   ─────────────────────────────────────────────────────
##   PHASE A4 — TREND PERIOD GRID (fourth priority)
##
##   Rationale: trend_period=48 has never been systematically tested. This parameter
##   controls the regime filter and could have significant impact on trade quality.
##
##   Each test: champion YAML + ONE change to trend_period_hours only.
##   Constraint: trend_period_hours must be in [24, 96].
##
##   A4.1: trend_period_hours = 36
##   A4.2: trend_period_hours = 42
##   A4.3: trend_period_hours = 54
##   A4.4: trend_period_hours = 60
##   A4.5: trend_period_hours = 72
##   A4.6: trend_period_hours = 30
##   A4.7: trend_period_hours = 84
##
##   Accept only if: sharpe > 2.3494 AND trades in [900, 1400].
##
##   ─────────────────────────────────────────────────────
##   PHASE A5 — RSI LONG THRESHOLD GRID (fifth priority)
##
##   Rationale: rsi_long = 37.77 has been frozen since Gen 1477 (2,500+ generations).
##   The non-integer value (37.77) suggests it was arrived at by decimal search, but
##   neighbors have never been tested. Potential for meaningful improvement exists.
##
##   Each test: champion YAML + ONE change to rsi_long_threshold only.
##   Constraint: rsi_long must be in [30, 45].
##   Constraint: (confirmed_rsi_short - rsi_long) must be >= 10.
##
##   A5.1: rsi_long = 37.00
##   A5.2: rsi_long = 38.00
##   A5.3: rsi_long = 36.50
##   A5.4: rsi_long = 38.50
##   A5.5: rsi_long = 36.00
##   A5.6: rsi_long = 39.00
##   A5.7: rsi_long = 35.50
##   A5.8: rsi_long = 37.50
##
##   Accept only if: sharpe > 2.3494 AND trades in [900, 1400].
##   Note: higher rsi_long → more long entries → higher trade count.
##         lower rsi_long → fewer long entries → lower trade count.
##   If A5.2–A5.4 produce trades > 1350: rsi_long is near a trade-count cliff.
##
##   ─────────────────────────────────────────────────────
##   PHASE A6 — STOP LOSS GRID (sixth priority)
##
##   Rationale: SL=1.91 confirmed since early optimization. Fine-grained neighbors
##   around 1.91 have not been tested at non-integer precision.
##
##   Each test: champion YAML + ONE change to stop_loss_pct only.
##   Constraint: stop_loss_pct must NOT be 1.90 or 1.92 (known non-optimal neighbors).
##
##   A6.1: stop_loss_pct = 1.85
##   A6.2: stop_loss_pct = 1.88
##   A6.3: stop_loss_pct = 1.93
##   A6.4: stop_loss_pct = 1.94
##   A6.5: stop_loss_pct = 1.97
##   A6.6: stop_loss_pct = 2.00
##   A6.7: stop_loss_pct = 1.80
##   A6.8: stop_loss_pct = 1.75
##
##   Accept only if: sharpe > 2.3494 AND trades in [900, 1400].
##
##   ─────────────────────────────────────────────────────
##   PHASE A7 — COMBINED BEST (only after all single-param phases complete)
##
##   If 0 improvements found in A1–A6:
##     Log: "Phase A grid complete. No improvements. Strategy is at local maximum
##           for all tested single-parameter changes. Champion remains Gen 3340."
##     Proceed to Phase B (structural changes).
##
##   If 1 improvement found:
##     The new champion is the baseline. Re-run A1–A6 from new champion.
##     (New champion may open new neighbors that were previously sub-threshold.)
##
##   If 2+ improvements found:
##     Test top-2 single-param improvements combined (one YAML, two changes from
##     original Gen 3340 champion — or from new champion if one was already accepted).
##     Accept only if combined result beats the best single-param result.
##
##   Total Phase A tests: ~41 backtests (including A7). Target: < 50 generations.
##
##   ─────────────────────────────────────────────────────
##   PHASE B — STRUCTURAL EXPLORATION (only if Phase A yields no improvement)
##
##   Rationale: If Phase A confirms a local maximum across all 6 parameters, the
##   strategy may require structural change rather than parameter tuning.
##   These tests modify strategy logic, not just parameter values.
##
##   B1 — MULTI-ASSET FILTER: Test restricting pairs to [BTC/USD, ETH/USD, SOL/USD]
##        (the backtest universe). Current pair list includes 16 pairs but backtest
##        only tests 3. Confirm pair list alignment.
##        Note: If backtest only uses BTC/USD, ETH/USD, SOL/USD regardless of pair list,
##        then the pair list in the YAML is cosmetic and B1 is irrelevant. Confirm this.
##
##   B2 — FUNDING COST SENSITIVITY: At 2x leverage, funding = ~0.01% per 8h = 0.03%/day.
##        For a 159h max timeout, funding drag = ~0.60% per position.
##        Test timeout_hours = 120 (funding drag reduction ~0.46%) to see if reduced
##        drag improves Sharpe despite fewer trade completions.
##        NOTE: timeout_hours was "FROZEN FOREVER" — this freeze is now reconsidered
##        given 660-generation stall. A frozen parameter that was never re-examined
##        is a research gap, not a confirmed optimum.
##
##   B3 — WIN RATE CEILING ANALYSIS: Champion win rate is ~40.1% across all champions
##        since Gen 2785. This is suspiciously stable and suggests the win rate is
##        structurally bounded. The Sharpe improvement since Gen 2785 comes from
##        trade quality (profit factor), not win rate improvement. Test whether
##        a tighter RSI entry (rsi_long = 32, rsi_short = 63) improves profit factor
##        at the cost of trade count.
##
##   B4 — RISK ASYMMETRY TEST: Current TP/SL ratio = confirmed_TP / 1.91 ≈ 2.6:1.
##        Test TP + 0.50 with SL - 0.10 simultaneously (wider reward, tighter risk).
##        This is a 2-parameter change, permitted only in Phase B.
##
##   Phase B tests are exploratory and do not follow the strict single-change rule.
##   Each B test must still pass the pre-backtest validation checklist (Step C).
##   Phase B results that improve champion → execute Step D (post-new_best protocol).
##
## ─────────────────────────────────────────────────────────
## STEP B — GRID TEST EXECUTION PROTOCOL (renamed from Step B in prior version)
## [Renamed to avoid collision with Phase B above — this is the PRE-BACKTEST CHECKLIST]
##
##   PRE-SUBMISSION VALIDATION (run before EVERY backtester submission):
##
##   SOURCE VALIDATION:
##   □ Load champion YAML from confirmed storage path (hard-coded path, no fallback).
##   □ Verify file hash matches confirmed Gen 3340 champion hash.
##   □ If hash mismatch → HALT. Do not submit. Do not escalate to LOKI.
##     Output: "HASH MISMATCH at Gen XXXX. Halting." Wait for human operator.
##
##   PARAMETER INTEGRITY (Phase A tests):
##   □ Apply exactly the pre-specified parameter change for the current grid step.
##   □ Diff result against champion YAML. Confirm exactly 0 lines changed (A0 test)
##     or exactly 1 line changed (A1–A6 tests) or exactly 2 lines changed (A7/B4 only).
##   □ If diff shows wrong number of changes → reject. Log "multi-diff error." HALT.
##   □ Verify timeout_hours = 159 (FROZEN — reject if any other value, including 176).
##   □ Verify size_pct = 25, max_open = 3, leverage = 2, fee_rate = 0.0005.
##   □ Verify stop_loss_pct ≠ 1.90 (explicit check).
##   □ Verify rsi_long_threshold in [30, 45].
##   □ Verify rsi_short_threshold in [55, 70].
##   □ Verify (rsi_short_threshold - rsi_long_threshold) >= 10.
##   □ Verify rsi_period_hours in [18, 28] (unless Phase A3 test — then verify in range).
##   □ Verify trend_period_hours in [24,