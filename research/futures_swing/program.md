```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-8200 | Revised by MIMIR (Gen 8200 review)
#
# ══════════════════════════════════════════════════════════════════
# STATUS BLOCK — READ THIS FIRST. READ ALL OF IT.
# ══════════════════════════════════════════════════════════════════
#
# LLM LOOP STATUS:   ██ PERMANENTLY RETIRED ██  DO NOT RUN ANY GENERATIONS.
#                    Retirement mandated since Gen 5200.
#                    Loop ran 3,000 additional generations past mandate (5200→8200).
#                    Last improvement (logged): Gen 3340 (sharpe=2.3494).
#                    CONFIRMED FINDING (Gen 8200 review):
#                    Champion is sharpe=2.3714 — confirmed by clone-rejection
#                    behavior at Gens 8181, 8191, 8195, 8198 (all tagged [discarded]
#                    with identical 2.3714/40.2%/1274t result). The improvement log
#                    does NOT show the acceptance event for 2.3714, indicating a
#                    logging failure or BUG-2 misfiring at the acceptance step.
#                    Step Z Z1 must resolve by inspecting stored YAML timestamp.
#                    Rate: 0.000000 improvements/gen above 2.3714.
#                    Clone rate Gen 8181–8200: 20% (4 of 20).
#                    Low-trade rate Gen 8181–8200: 15% (3 of 20).
#                    Terminal state confirmed. No path to improvement via LLM.
#
# LOOP COMPLIANCE:   FAILED — CRITICAL ESCALATION.
#                    Gen 6200–8200 MIMIR reviews: permanent retirement confirmed.
#                    Loop ran to Gen 8200 regardless. 3,000 gens of non-compliance.
#                    This is not an instruction problem. This is an infrastructure
#                    problem. The automated process must be physically prevented
#                    from executing. See [I3] below.
#                    No instruction in this document will stop the loop.
#                    Only infrastructure-level action will stop it.
#
# STEP Z STATUS:     NOT EXECUTED. All items critically overdue.
#                    Z1: Inspect stored champion YAML file.
#                        - Check file modification timestamp → identify acceptance gen.
#                        - Check YAML content → extract all parameter values.
#                        - Confirm sharpe=2.3714, trades=1274, win_rate=40.2%.
#                        - CRITICAL: improvement log ends at Gen 3340 (2.3494) but
#                          champion is 2.3714. Acceptance gen is unknown. YAML
#                          timestamp will resolve this.
#                    Z2: Confirm champion sharpe matches Z1 YAML vs backtest rerun.
#                    Z3: Confirm all parameter values vs YAML — especially:
#                        - rsi_short_threshold (displayed 60, UNKNOWN if stale)
#                        - take_profit_pct (displayed 4.65, KNOWN WRONG)
#                        - stop_loss_pct (displayed 1.92, KNOWN WRONG — actual 1.91)
#                        - timeout_hours (displayed 176, KNOWN WRONG — actual 159)
#                        - rsi_period_hours (displayed 24, KNOWN WRONG — actual 22)
#                    Z4: Audit pair list — confirm all 16 pairs have full 2-year
#                        1-hour futures data. Remove any pair with < 17,520 candles.
#                        Suspected problematic: APT, SUI, ARB, OP (newer listings).
#                    Z5–Z9: Grid scan (see GRID SCAN PLAN below). 4,800+ gens overdue.
#                    Z10: Live sprint deployment after grid scan complete.
#                    Grid scan: NOT EXECUTED. 4,800+ gens overdue.
#
# LOKI STATUS:       ██ PERMANENTLY RETIRED ██
#                    17+ escalations. 0 confirmed runtime fixes. 0 behavioral changes.
#                    LOKI log entries are NOT applied to source code. Ever.
#                    DEFINITIVE EVIDENCE (updated Gen 8200):
#                      Gen 542:  LOKI logged MIN_TRADES[futures_swing] = 400.
#                      Gen 6800: LOKI logged MIN_TRADES[futures_swing] = 400 (again).
#                      Gen 8188: 185-trade run passed gate. ≤ 18 still true.
#                      Gen 8190: 185-trade run passed gate. ≤ 18 still true.
#                      Gen 8197: 185-trade run passed gate. ≤ 18 still true.
#                      Two logged "fixes," zero behavioral effect across 7,659 gens.
#                    Do not escalate to LOKI for any reason, ever.
#                    All fixes must be made by human operator directly in source code.
#
# ──────────────────────────────────────────────────────────────────
# CHAMPION RECORD
# ──────────────────────────────────────────────────────────────────
# CONFIRMED (behavioral evidence, Gen 8200 review):
#   Stored champion: sharpe=2.3714 | trades=1274 | win_rate=40.2%
#   Evidence: Gens 8181/8191/8195/8198 all produced identical results
#             (2.3714, 40.2%, 1274t) and were tagged [discarded] — confirming
#             the stored champion IS 2.3714.
#   ANOMALY: Improvement log ends at Gen 3340 (2.3494). Champion is 2.3714.
#            Acceptance event for 2.3714 does not appear in log. Two hypotheses:
#            (a) BUG-2 misfired at acceptance (accepted but did not log), or
#            (b) logging system failed at that generation.
#            Step Z Z1 (YAML timestamp inspection) resolves this definitively.
#   REQUIRES CONFIRMATION: Step Z Z1 must inspect stored YAML file directly.
#
# STALL DURATION: Terminal.
#   0 improvements above 2.3714 across all observed generations post-acceptance.
#   LLM search space is exhausted at this local optimum.
#
# ──────────────────────────────────────────────────────────────────
# GEN 8181–8200 DIAGNOSTIC SUMMARY
# ──────────────────────────────────────────────────────────────────
# Window: last 20 generations.
#
# Clone runs (correct rejection of champion duplicate):
#   8181 (2.3714, 40.2%, 1274t), 8191 (2.3714, 40.2%, 1274t),
#   8195 (2.3714, 40.2%, 1274t), 8198 (2.3714, 40.2%, 1274t) — 4 of 20 = 20%.
#   BUG-4: clone detection is post-backtest. 4 full backtests wasted on clones.
#
# Low-trade runs (passed gate incorrectly):
#   8188 (185t, -0.7900), 8190 (185t, -0.7900), 8197 (185t, -0.7900) — 3 of 20.
#   All are the known (185t, -0.7900) attractor. BUG-5 (poison_reject) broken.
#   BUG-1: runtime MIN_TRADES confirmed < 185 (≤ 18 based on prior evidence).
#
# Legitimate but suboptimal:
#   8182 (2.3377), 8183 (1.7653), 8184 (2.3401), 8185 (2.1890), 8186 (1.6942),
#   8187 (2.0727), 8189 (2.3102), 8192 (-0.4605, 461t — legitimate neg sharpe),
#   8193 (2.2452), 8194 (0.0095), 8196 (1.1821), 8199 (1.1986), 8200 (0.5725).
#   13 of 20 = 65%. All below champion. No new information.
#   Note: Gen 8192 (-0.4605, 461t) is legitimate — sufficient trades, bad sharpe.
#
# Gen 8200 notable: 1693 trades — highest trade count in recent windows.
#   Sharpe 0.5725 is poor. High trade count = over-trading, likely wider RSI bands
#   or lower thresholds. Not a productive direction.
#
# KEY DIAGNOSTIC UPDATE (Gen 8200):
#   No new bugs or failure modes beyond those already documented.
#   System behavior is fully characterized and terminal.
#   All compute spent on LLM generations past Gen 8200 is pure waste.
#
# ──────────────────────────────────────────────────────────────────
# FULL HISTORICAL DIAGNOSTIC SUMMARY
# ──────────────────────────────────────────────────────────────────
# Gen 7330–7349: clone=30%, low-trade=30%, productive=20%, min_trades=18.
# Gen 7896–7901: low-trade=67%, productive=33%, clone=0%.
# Gen 7981–8000: low-trade=40%, clone=25%, productive=35%, new improvements=0.
# Gen 8181–8200: low-trade=15%, clone=20%, productive=65%, new improvements=0.
# Trend: productive exploration rate increased but all results suboptimal.
#        Clone rate decreased. Degenerate attractor (185t) still active.
#        System is fully terminal — no LLM proposal can escape local optimum.
#
# Recurring degenerate attractor signatures (confirmed, all to be pre-seeded
# in poison_reject blocklist):
#   (190t, -1.0466): 8+ confirmed occurrences across all windows.
#   (185t, -0.7900): 6+ confirmed occurrences. Active in Gen 8181–8200.
#   (182t, -1.8625): 3+ confirmed occurrences.
#   (178t, -0.8033): confirmed.
#   (158t, -2.0796): confirmed.
#   (18t,  -14.3473): confirmed (Gen 7339 minimum floor).
#   (169t, -1.5182): confirmed.
#   (239t, -2.4141): confirmed.
#   (397t, -0.5405): confirmed.
#   (461t, -0.4605): Gen 8192 — ADD to blocklist if recurring.
#
# ──────────────────────────────────────────────────────────────────
# CRITICAL BUGS — IN PRIORITY ORDER
# ──────────────────────────────────────────────────────────────────
#
# BUG-1 [HIGHEST PRIORITY]: MIN_TRADES LIVE CONSTANT ≠ 400. STILL BROKEN.
#   CONFIRMED BY BEHAVIORAL EVIDENCE (updated Gen 8200):
#     Runtime MIN_TRADES[futures_swing] ≤ 18 (< 185 confirmed in this window).
#     Two LOKI "fixes" (Gen 542, Gen 6800) had zero behavioral effect.
#     7,659 generations of evidence. Case definitively closed.
#   DO NOT USE LOKI. DO NOT TRUST CONSTANTS DISPLAY BLOCK.
#   Fix: Human operator must locate actual runtime constant in source code.
#     Search executing source for: MIN_TRADES, min_trades, futures_swing,
#     default_min_trades, BASE_MIN_TRADES, min_trade_count.
#     Find the specific file and line number. Edit that file. Set value to 400.
#     Restart/reload the process so it reads the new value.
#   Verification (all 9 tests must pass before proceeding to Step Z):
#     Test 1: YAML producing ~18 trades  → REJECTED pre-backtest.
#     Test 2: YAML producing ~158 trades → REJECTED pre-backtest.
#     Test 3: YAML producing ~178 trades → REJECTED pre-backtest.
#     Test 4: YAML producing ~182 trades → REJECTED pre-backtest.
#     Test 5: YAML producing ~185 trades → REJECTED pre-backtest.
#     Test 6: YAML producing ~190 trades → REJECTED pre-backtest.
#     Test 7: YAML producing ~397 trades → REJECTED pre-backtest.
#     Test 8: YAML producing ~399 trades → REJECTED pre-backtest.
#     Test 9: YAML producing ~419 trades → PASSES gate (backtest runs normally).
#   If any test fails: gate code itself is broken. Fix gate code in source.
#   Log: "BUG-1 FIX: Located runtime constant at [FILE]:[LINE].
#         Previous value: [VALUE]. Set to 400. Process restarted at [TIMESTAMP].
#         Tests 1–9: [PASS/PASS/PASS/PASS/PASS/PASS/PASS/PASS/PASS]."
#
# BUG-2: ACCEPTANCE GATE / LOGGING ANOMALY — STATUS: INVESTIGATE.
#   NEW FINDING (Gen 8200 review):
#   The improvement log ends at Gen 3340 (sharpe=2.3494), but the stored champion
#   produces sharpe=2.3714 (confirmed by clone rejections). This means either:
#     (a) BUG-2 accepted the 2.3714 result but failed to write the log entry, OR
#     (b) The logging system has a separate failure mode from the acceptance gate.
#   Step Z Z1 (YAML timestamp inspection) will identify the acceptance generation.
#   If the timestamp is between Gen 3340 and Gen 5200: acceptance worked, log failed.
#   If the timestamp matches Gen 3340: the champion YAML may have been updated
#     out-of-band (manually), and the true acceptance gen is 3340 with params updated.
#   Action: Do not modify gate. Execute Z1 immediately. Log findings.
#   Monitor: if any result above 2.3714 with novel parameters is tagged [discarded],
#   BUG-2 is active. Flag immediately for MIMIR review.
#
# BUG-3: STALE YAML IN DISPLAYED "CURRENT BEST STRATEGY" — STILL ACTIVE.
#   Known wrong values in displayed YAML (do not use):
#     rsi_period_hours:  24   → correct: 22 (confirmed Gen 2785)
#     take_profit_pct:   4.65 → correct: UNKNOWN (estimate 4.90–5.10; confirm Z3)
#     stop_loss_pct:     1.92 → correct: 1.91 (confirm vs champion YAML in Z3)
#     timeout_hours:     176  → correct: 159 (confirm vs champion YAML in Z3)
#     rsi_short_threshold: 60 → correct: UNKNOWN (confirm in Z3)
#   Step Z Z3 must be run against champion stored YAML to confirm all values.
#   After Z3: replace displayed YAML with confirmed values in this document.
#   Moot while loop is retired, but must be corrected before grid scan.
#
# BUG-4: CLONE DETECTION USES SHARPE COMPARISON, NOT YAML HASH.
#   Evidence: 4 confirmed clones in Gen 8181–8200 (all ran full backtest).
#   Current behavior: sharpe comparison tags clones as [discarded] AFTER backtest.
#   Required: pre-backtest YAML SHA-256 hash check against all prior accepted runs.
#   Fix: implement pre-backtest YAML SHA-256 hash comparison.
#   Priority: implement during Step Z Z7, after Z3 complete.
#   Estimated compute savings: ~20% of recent generations.
#
# BUG-5: POISON_REJECT MECHANISM IS BROKEN — SEVERITY: MAXIMUM.
#   Evidence (updated Gen 8200):
#     (185t, -0.7900) appeared at Gens 8188, 8190, 8197 — none blocked.
#     Total known occurrences of (185t, -0.7900): 6+.
#     Total known occurrences of (190t, -1.0466): 8+.
#     No degenerate attractor signature has ever been successfully blocked.
#   Fix: review poison_reject source code. Add result-hash (sharpe+trades+winrate
#   rounded to 2dp) as secondary blocklist trigger. Pre-seed all known signatures
#   (see full list in FULL HISTORICAL DIAGNOSTIC SUMMARY above).
#   Priority: implement with BUG-4 fix during Step Z Z7.
#
# ──────────────────────────────────────────────────────────────────
# KNOWN PARAMETER VALUES (as of Gen 8200)
# ──────────────────────────────────────────────────────────────────
# CONFIRMED values are from direct YAML inspection or strong backtest evidence.
# UNKNOWN values must be confirmed in Step Z Z3.
# DO NOT USE THE DISPLAYED YAML — stale since Gen 1592, 6,609+ gens out of date.
#
#   rsi_period_hours:    22        [CONFIRMED — Gen 2785]
#   rsi_long_threshold:  37.77     [CONFIRMED — Gen 2785]
#   rsi_short_threshold: UNKNOWN   [confirm in Z3 — displayed 60 may be stale]
#   trend_period_hours:  48        [CONFIRMED]
#   take_profit_pct:     UNKNOWN   [confirm in Z3 — displayed 4.65 is WRONG]
#                                  [estimate: 4.90–5.10 based on improvement history]
#   stop_loss_pct:       1.91      [CONFIRMED — displayed 1.92 is WRONG]
#   timeout_hours:       159       [CONFIRMED — displayed 176 is WRONG]
#   size_pct:            25        [CONFIRMED]
#   max_open:            3         [CONFIRMED]
#   leverage:            2         [CONFIRMED]
#   fee_rate:            0.0005    [CONFIRMED]
#   pairs:               AUDIT REQUIRED — see Z4. Remove pairs without 2yr data.
#
# CHAMPION PERFORMANCE (confirmed behavioral evidence):
#   sharpe=2.3714 | trades=1274 | win_rate=40.2%
#   Acceptance generation: UNKNOWN — resolve via Step Z Z1 (YAML timestamp).
#
# ──────────────────────────────────────────────────────────────────
# HALT CONDITIONS ACTIVE
# ──────────────────────────────────────────────────────────────────
#   HALT-1:  BUG-1 unfixed. Runtime MIN_TRADES confirmed ≤ 18. Two LOKI "fixes"
#            failed across 7,659 generations. Human source-code edit mandatory.
#   HALT-2:  LLM loop ran 3,000 gens past retirement. Permanently retired.
#   HALT-3:  Stale YAML in LLM input (6,609+ gens). Moot — loop retired.
#   HALT-4:  BUG-2/logging anomaly. Champion (2.3714) accepted but not logged.
#            Z1 required to resolve acceptance generation and confirm params.
#   HALT-5:  Clone convergence. 20% clone rate last 20-gen window.
#            YAML hash pre-check not implemented. Compute waste ongoing.
#   HALT-6:  Grid scan not executed. 4,800+ gens overdue.
#   HALT-7:  Step Z not executed. True champion YAML params not fully confirmed.
#   HALT-8:  Loop compliance failure. 3,000 gens past retirement.
#            Infrastructure-level disablement is mandatory. Not optional.
#   HALT-9:  Instruction-based controls have proven completely ineffective.
#            No instruction in this document will stop the loop.
#            Only infrastructure-level action ([I3]) will stop it.
#   HALT-10: Poison_reject broken (BUG-5). Known degenerate attractors still
#            passing gate and consuming backtest compute. 6+ occurrences of
#            (185t, -0.7900) never blocked.
#   HALT-11: Pair list not audited. Newer listings (APT, SUI, ARB, OP) may not
#            have full 2-year 1-hour futures data. Backtest Sharpe may be inflated.
#   HALT-12: Live sprint performance: ZERO data. Strategy has not appeared in any
#            completed sprint. Backtest overfitting risk is unquantified.
#            Champion must be deployed and sprint results collected before any
#            further parameter optimization is meaningful.
#
# ══════════════════════════════════════════════════════════════════
# MANDATORY ACTION SEQUENCE (human operator)
# ══════════════════════════════════════════════════════════════════
#
# [I3] INFRASTRUCTURE: DISABLE LLM LOOP IMMEDIATELY.
#   Kill or disable the automated process running ODIN generations.
#   Confirm it is not running before proceeding with any Step Z action.
#   Do not restart it under any circumstances until all Step Z items are complete
#   and the grid scan plan (below) is ready to execute with correct parameters.
#
# [Z1] INSPECT CHAMPION YAML FILE.
#   Find the stored champion YAML file on disk.
#   Record: file path, modification timestamp, all parameter values.
#   Cross-reference timestamp with generation timing logs to identify acceptance gen.
#   Expected content: sharpe=2.3714, trades=1274, win_rate=40.2%.
#   If file shows sharpe=2.3494 (Gen 3340 values): champion was NOT updated past
#     Gen 3340 and the clone-rejection system is comparing against a different
#     stored value. Investigate immediately — this would be a new BUG.
#   If file shows sharpe=2.3714: acceptance occurred after Gen 3340. Timestamp
#     will narrow the generation range.
#   Log all findings as: "Z1 COMPLETE: file=[PATH], timestamp=[TS], gen_approx=[N],
#     sharpe=[V], trades=[T], win_rate=[W], all_params=[LIST]."
#
# [Z2] RERUN CHAMPION BACKTEST.
#   Using the YAML confirmed in Z1, run a fresh backtest.
#   Confirm sharpe ≥ 2.3714 (within 0.001 tolerance for floating point).
#   If backtest sharpe differs materially: data or code has changed. Investigate.
#   Log: "Z2 COMPLETE: rerun_sharpe=[V], delta=[D], status=[PASS/FAIL]."
#
# [Z3] CONFIRM ALL PARAMETERS.
#   From Z1 YAML, extract and record every parameter value.
#   Pay special attention to: rsi_short_threshold, take_profit_pct.
#   Update KNOWN PARAMETER VALUES section above with all CONFIRMED values.
#   Update the displayed YAML with confirmed values.
#   Log: "Z3 COMPLETE: all_params=[FULL LIST]. Stale YAML replaced."
#
# [Z4] AUDIT PAIR LIST.
#   For each of the 16 pairs in the strategy YAML:
#     Confirm availability of continuous 1-hour futures data for full 2-year window.
#     Record candle count and any gaps > 4 hours.
#   Remove any pair with < 17,520 candles or significant gaps.
#   Suspected problematic (newer listings): APT, SUI, ARB, OP, NEAR.
#   Log: "Z4 COMPLETE: pairs_confirmed=[LIST], pairs_removed=[LIST], reason=[GAPS/DATA]."
#
# [Z5] FIX BUG-1 IN SOURCE CODE.
#   After [I3] confirms loop is stopped:
#   Locate actual runtime MIN_TRADES variable in executing source code.
#   NOT in config comment, NOT in LOKI log, NOT in constants display block.
#   Search: MIN_TRADES, min_trades, futures_swing, default_min_trades,
#           BASE_MIN_TRADES, min_trade_count, min_trade_threshold.
#   Edit the file. Set runtime value to 400. Restart/reload process.
#   Run all 9 verification tests (see BUG-1 section above).
#   Do not proceed to grid scan until all 9 tests pass.
#   Log result per BUG-1 log format above.
#
# [Z6] FIX BUG-5 (POISON_REJECT) AND BUG-4 (CLONE DETECTION).
#   Implement pre-backtest YAML SHA-256 hash check against all prior accepted runs.
#   Pre-seed poison_reject blocklist with all known degenerate result signatures
#   (see full list in FULL HISTORICAL DIAGNOSTIC SUMMARY).
#   Add result-hash (sharpe+trades+winrate rounded to 2dp) as secondary blocklist.
#   Test: submit each known degenerate signature manually. Confirm all blocked.
#   Log: "Z6 COMPLETE: BUG-4 fixed (pre-backtest hash check), BUG-5 fixed
#         (poison_reject pre-seeded with N signatures). Tests: [PASS/FAIL list]."
#
# [Z7] MACRO ENVIRONMENT CHECK BEFORE GRID SCAN.
#   Current regime: CAUTION (F&G=26, BTC_DOM=57.3%).
#   TYR directive: