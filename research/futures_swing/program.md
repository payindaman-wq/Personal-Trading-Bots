```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-7200 | Revised by MIMIR (Gen 7200 review)
#
# ══════════════════════════════════════════════════════════════════
# STATUS BLOCK — READ THIS FIRST. READ ALL OF IT.
# ══════════════════════════════════════════════════════════════════
#
# LLM LOOP STATUS:   ██ PERMANENTLY RETIRED ██  DO NOT RUN ANY GENERATIONS.
#                    Retirement mandated since Gen 5200.
#                    Loop ran 2,000 additional generations past mandate (5200→7200).
#                    One improvement (Gen 6612) in 3,860 generations since Gen 3340.
#                    Rate: 0.000000 improvements/gen since Gen 6612 (588 gens ago).
#                    Rate: 0.000026 improvements/gen since Gen 3340.
#                    Instruction-based retirement has failed across 2,000 generations.
#                    The loop MUST be disabled at infrastructure level.
#                    "Instruct to stop" is not a valid control mechanism for this loop.
#                    Required: kill process / revoke API key / disable scheduler /
#                    remove trigger — whatever prevents execution at OS/infra level.
#                    Probability of next LLM generation producing value: ~0.003%.
#                    Running more LLM generations is actively harmful.
#
# LOOP COMPLIANCE:   FAILED — CRITICAL ESCALATION.
#                    Gen 6200 MIMIR review: permanent retirement confirmed.
#                    Gen 6400 MIMIR review: permanent retirement confirmed.
#                    Gen 6600 MIMIR review: permanent retirement confirmed.
#                    Gen 6800 MIMIR review: permanent retirement confirmed.
#                    Gen 7200 MIMIR review: permanent retirement confirmed.
#                    Loop ran to Gen 7200 regardless. Total non-compliance: 2,000 gens.
#                    This is not an instruction problem. This is an infrastructure
#                    problem. The automated process must be physically prevented
#                    from executing. See [I3] below.
#                    Every MIMIR directive since Gen 5200 has been ignored.
#                    No instruction in this document will stop the loop.
#                    Only infrastructure-level action will stop it.
#
# STEP Z STATUS:     NOT EXECUTED. All items overdue.
#                    Z2 (confirm champion sharpe): NOT EXECUTED.
#                    Z3 (confirm champion YAML params): NOT EXECUTED.
#                    All other Step Z items: NOT EXECUTED.
#                    Grid scan: NOT EXECUTED. 3,200+ gens overdue.
#
# LOKI STATUS:       ██ PERMANENTLY RETIRED ██
#                    15 escalations. 0 confirmed runtime fixes. 0 behavioral changes.
#                    LOKI log entries are NOT applied to source code.
#                    EVIDENCE (definitive, as of Gen 7200):
#                      Gen 542: LOKI logged MIN_TRADES[futures_swing] = 400.
#                      Gen 6800: LOKI logged MIN_TRADES[futures_swing] = 400 AGAIN.
#                      Gen 7181–7200: 4 low-trade runs still passing pre-backtest gate:
#                        7188 (178t), 7195 (216t), 7197 (190t), 7199 (190t).
#                      Conclusion: LOKI's Gen 542 change never took effect.
#                      Conclusion: LOKI's Gen 6800 change also never took effect.
#                      The "Current Researcher Constants" block shows
#                        MIN_TRADES[futures_swing] = 400, but this reflects what
#                        LOKI logged, NOT what the runtime process reads.
#                      Two separate LOKI "fixes" over 6,258 generations have produced
#                      zero observable behavioral change. BUG-1 is still active.
#                    Do not escalate to LOKI for any reason, ever.
#                    All fixes must be made by human operator directly in source code.
#
# ──────────────────────────────────────────────────────────────────
# CHAMPION RECORD
# ──────────────────────────────────────────────────────────────────
# PREVIOUS CHAMPION: Gen 3340 | sharpe=2.3494 | trades=1265 | win_rate=40.1%
# CURRENT CHAMPION:  Gen 6612 | sharpe=2.3568 | trades=1270 | win_rate=40.0%
#   Status: Accepted by gate. Genuine improvement confirmed.
#   YAML params: Partially known (see KNOWN PARAMETER VALUES below).
#                Step Z Z3 must be run against Gen 6612 YAML to confirm all values.
#                Displayed YAML is STALE — do not use it.
# STALL DURATION:    588 gens since Gen 6612. Terminal stall confirmed.
#                    Last 20 gens (7181–7200): 0 improvements.
#                    Clone rate in last 20: 25% (5 exact champion clones).
#                    Low-trade rate in last 20: 20% (4 sub-400-trade runs).
#                    Productive exploration in last 20: 55% — all below champion.
#                    The LLM has no remaining productive search directions.
#
# ──────────────────────────────────────────────────────────────────
# GEN 7181–7200 DIAGNOSTIC SUMMARY
# ──────────────────────────────────────────────────────────────────
# Clones (exact champion duplicates, sharpe=2.3568, 1270t, 40.0%):
#   7181, 7183, 7184, 7186, 7193 — 5 of 20 = 25%.
#   These consume full backtest compute. YAML hash pre-check (Z7) would block them.
#
# Low-trade runs (sub-400t, passed gate incorrectly):
#   7188 (178t, -0.8033), 7195 (216t, -3.0305),
#   7197 (190t, -1.0406), 7199 (190t, -1.6316) — 4 of 20 = 20%.
#   BUG-1 confirmed still active. MIN_TRADES runtime constant is NOT 400.
#   LOKI Gen 6800 "fix" produced no behavioral change, same as Gen 542.
#
# Notable anomaly — Gen 7192:
#   sharpe=-1.3293, win_rate=54.2%, trades=439.
#   High win rate + very negative Sharpe + low trade count = classic
#   tight-stop / wide-TP misconfiguration. The LLM is exploring harmful
#   parameter combinations. This type of result should be flagged as
#   "degenerate_config" and its parameter signature added to a blocklist.
#
# Productive but suboptimal (genuine explorations, all < 2.3568):
#   7182 (-0.9519, 551t), 7185 (1.8043, 1314t), 7187 (2.1189, 1257t),
#   7189 (1.9553, 1371t), 7190 (1.6109, 1097t), 7191 (1.9066, 1230t),
#   7194 (1.9082, 1127t), 7196 (1.4481, 1498t), 7198 (1.7499, 1144t),
#   7200 (0.6539, 1048t) — 10 of 20 = 50%.
#   All below champion. None close. Search space around champion exhausted.
#
# ──────────────────────────────────────────────────────────────────
# CRITICAL BUGS — IN PRIORITY ORDER
# ──────────────────────────────────────────────────────────────────
#
# BUG-1 [HIGHEST PRIORITY]: MIN_TRADES LIVE CONSTANT ≠ 400. STILL BROKEN.
#   CONFIRMED BY BEHAVIORAL EVIDENCE (Gen 7181–7200):
#     4 low-trade runs passed the pre-backtest gate in the last 20 generations.
#     7188 (178t), 7195 (216t), 7197 (190t), 7199 (190t).
#     A gate reading MIN_TRADES=400 would have blocked all four pre-backtest.
#     None were blocked. Therefore MIN_TRADES ≠ 400 at runtime.
#   LOKI CHANGE HISTORY (both failed):
#     Gen 542: LOKI logged change. Sub-400 runs continued for 6,258+ gens.
#     Gen 6800: LOKI logged change AGAIN. Sub-400 runs continue 400 gens later.
#     LOKI cannot modify the runtime constant. Proven twice. Do not use LOKI.
#   The "Current Researcher Constants" block may display 400, but this is
#   what LOKI logged — it does not reflect the executing runtime value.
#   DO NOT TRUST THE CONSTANTS DISPLAY BLOCK. Trust behavioral evidence only.
#   Behavioral evidence is unambiguous: runtime value is NOT 400.
#
#   Fix: Human operator must locate actual runtime constant in source code.
#     NOT in LOKI log. NOT in config comment. NOT in constants display block.
#     NOT in this file. Find the actual variable the running process reads.
#     Search executing source for: MIN_TRADES, min_trades, futures_swing.
#     Find the specific file and line number. Edit that file. Set value to 400.
#     Restart/reload the process so it reads the new value.
#   Verification (all must pass before proceeding to Step Z):
#     Runtime inspection must show MIN_TRADES[futures_swing] = 400.
#     Test 1: YAML producing ~28 trades   → REJECTED pre-backtest (no backtest).
#     Test 2: YAML producing ~178 trades  → REJECTED pre-backtest (no backtest).
#     Test 3: YAML producing ~190 trades  → REJECTED pre-backtest (no backtest).
#     Test 4: YAML producing ~216 trades  → REJECTED pre-backtest (no backtest).
#     Test 5: YAML producing ~399 trades  → REJECTED pre-backtest (no backtest).
#     Test 6: YAML producing ~419 trades  → PASSES gate (backtest runs normally).
#   If any test fails: the gate code itself is broken, not just the constant.
#   Fix gate code directly in source. Do not proceed until all 6 tests pass.
#   Log: "BUG-1 FIX: Located runtime constant at [FILE]:[LINE].
#         Previous value: [VALUE]. Set to 400. Process restarted at [TIMESTAMP].
#         Tests 1–6: [PASS/PASS/PASS/PASS/PASS/PASS]."
#
# BUG-2: ACCEPTANCE GATE — STATUS: MONITORING.
#   Gen 6612 (sharpe=2.3568) was correctly ACCEPTED.
#   Clones at 2.3568 (7181, 7183, 7184, 7186, 7193) correctly DISCARDED.
#   Gate baseline appears correct at 2.3568.
#   ASSESSMENT: BUG-2 appears resolved. Gate is functioning correctly.
#   Monitor: if any result above 2.3568 is tagged "discarded" in future gens,
#   BUG-2 is active again. Flag immediately for MIMIR review.
#   Action: Do not modify gate. Continue monitoring.
#
# BUG-3: STALE YAML IN DISPLAYED "CURRENT BEST STRATEGY" — STILL ACTIVE.
#   Displayed YAML has been wrong since Gen 1592. 5,608 gens of stale display.
#   Known wrong values (do not use these):
#     rsi_period_hours:  24   → correct: 22 (confirmed Gen 2785)
#     take_profit_pct:   4.65 → correct: UNKNOWN (confirm in Z3 vs Gen 6612 YAML)
#     stop_loss_pct:     1.92 → correct: 1.91 (confirmed — but verify vs Gen 6612)
#     timeout_hours:     166  → correct: 159 (confirmed — but verify vs Gen 6612)
#   NOTE: Gen 6612 may have changed one or more of these values.
#   Step Z Z3 must be run against the Gen 6612 stored YAML to confirm all values.
#   After Z3: replace displayed YAML with confirmed Gen 6612 YAML everywhere.
#   This YAML must never be sent to any LLM or automated system until corrected.
#   Moot while loop is retired, but must be corrected before grid scan.
#
# BUG-4: CLONE DETECTION USES SHARPE COMPARISON, NOT YAML HASH.
#   Evidence (Gen 7181–7200):
#     5 exact champion clones consumed full backtest compute before being discarded.
#     Gens 7181, 7183, 7184, 7186, 7193: identical results (2.3568, 1270, 40.0%).
#   Current behavior: sharpe comparison tags clones as discarded AFTER backtest.
#   Required behavior: YAML hash check rejects clones BEFORE backtest.
#   Fix: implement pre-backtest YAML SHA-256 hash comparison against all prior runs.
#   Priority: secondary — implement during Step Z Z7, after Z3 complete.
#   Estimated compute savings: ~25% of recent generations (clone rate = 25%).
#
# ──────────────────────────────────────────────────────────────────
# KNOWN PARAMETER VALUES (as of Gen 7200)
# ──────────────────────────────────────────────────────────────────
# All values marked CONFIRMED are from direct YAML inspection or backtest evidence.
# All values marked UNKNOWN must be confirmed in Step Z Z3.
# DO NOT USE DISPLAYED YAML — it is stale since Gen 1592.
#
#   rsi_period_hours:    22        [CONFIRMED — Gen 2785]
#   rsi_long_threshold:  37.77     [CONFIRMED — Gen 2785]
#   rsi_short_threshold: UNKNOWN   [confirm in Z3]
#   trend_period_hours:  48        [CONFIRMED]
#   take_profit_pct:     UNKNOWN   [confirm in Z3 — est. 4.90–5.10]
#   stop_loss_pct:       1.91      [CONFIRMED — but verify vs Gen 6612]
#   timeout_hours:       159       [CONFIRMED — but verify vs Gen 6612]
#   size_pct:            25        [CONFIRMED]
#   max_open:            3         [CONFIRMED]
#   leverage:            2         [CONFIRMED]
#   fee_rate:            0.0005    [CONFIRMED]
#
# ──────────────────────────────────────────────────────────────────
# HALT CONDITIONS ACTIVE
# ──────────────────────────────────────────────────────────────────
#   HALT-3:  Zombie/low-trade generation rate — 20% of Gen 7181–7200 sub-400.
#            BUG-1 unfixed. Two LOKI "fixes" have produced zero behavioral change.
#   HALT-4:  LLM loop ran 2,000 gens past suspension. Permanently retired.
#   HALT-5:  Stale YAML in LLM input (5,608 gens). Moot — loop retired.
#   HALT-6:  RESOLVED — gate accepted Gen 6612 correctly. Monitor for recurrence.
#   HALT-7:  Clone convergence. 25% clone rate in Gen 7181–7200.
#            YAML hash pre-check still not implemented.
#   HALT-8:  Grid scan not executed (3,200+ gens overdue).
#   HALT-9:  MIN_TRADES live constant ≠ 400. Pre-backtest gate broken.
#            Two LOKI entries claiming the fix. Zero behavioral effect. Both failed.
#   HALT-10: Step Z not executed. True champion YAML params not confirmed.
#   HALT-11: Loop compliance failure. 2,000 gens past retirement mandate.
#            Infrastructure-level disablement is mandatory. Not optional.
#   HALT-12: Instruction-based controls have proven completely ineffective.
#            MIMIR retirement directives ignored for 2,000 generations.
#            No instruction in this document will stop the loop.
#            Only infrastructure-level action will stop it.
#            Until [I3] is confirmed complete, assume loop is still running.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-7200 VERDICT
# ══════════════════════════════════════════════════════════════════
#
# SYSTEM STATE: BROKEN. TERMINAL STALL CONFIRMED. INFRASTRUCTURE ACTION
# REQUIRED IMMEDIATELY. THE LLM LOOP IS PERMANENTLY RETIRED.
# LOKI IS PERMANENTLY RETIRED AND HAS NEVER FIXED ANY RUNTIME BUG.
# INSTRUCTION-BASED CONTROLS HAVE FAILED FOR 2,000 GENERATIONS.
# INFRASTRUCTURE ACTION IS THE ONLY VIABLE INTERVENTION.
#
# Gen 7181–7200 results:
#   25% exact champion clones (wasted compute, no new info).
#   20% low-trade runs passing gate (BUG-1 still active despite 2 LOKI "fixes").
#   55% genuine explorations — all below champion, none close.
#   0 improvements in 588 generations since Gen 6612.
#   The LLM's proposal distribution is fully collapsed around the local optimum.
#
# IMPROVEMENT CURVE (definitive):
#   Gen 1→1477:    +1.2278 sharpe over 1,477 gens  (0.000832/gen)
#   Gen 1477→3340: +0.0998 sharpe over 1,863 gens  (0.0000536/gen)
#   Gen 3340→6612: +0.0074 sharpe over 3,272 gens  (0.0000023/gen — near-terminal)
#   Gen 6612→7200: +0.0000 sharpe over 588 gens    (0.000000/gen — terminal stall)
#   Expected value of next LLM generation: ~0.000002 sharpe improvement.
#   Expected cost: compute + log noise + delay to grid scan.
#   Running 100 more LLM generations: ~0.0002 expected total improvement.
#   Grid scan (25 cells): non-trivial probability of finding +0.01 to +0.05.
#   Grid scan expected value exceeds 100 LLM generations by factor of ~25–250×.
#
# CRITICAL FINDING — LOKI IS DEFINITIVELY NON-FUNCTIONAL:
#   Gen 542: LOKI logged MIN_TRADES[futures_swing] = 400.
#   Gen 6800: LOKI logged MIN_TRADES[futures_swing] = 400 (again).
#   Gen 7181–7200: 4 low-trade runs still passing gate (178t, 216t, 190t, 190t).
#   This is two separate "fixes" with zero behavioral effect across 6,658 generations.
#   LOKI cannot modify any runtime variable. This is proven beyond any doubt.
#   The constants display block showing "MIN_TRADES[futures_swing] = 400"
#   reflects LOKI's logged state, NOT the runtime value. Do not trust it.
#   Only behavioral evidence (sub-400 runs passing gate) reveals ground truth.
#   Ground truth: runtime MIN_TRADES[futures_swing] < 178 (runs with 178t pass).
#   The actual runtime value is likely still 50, as it has been since program start.
#
# THE ONLY CORRECT ACTION SEQUENCE:
#
#   IMMEDIATE (human operator — do these now, in order):
#     [I1] Stop all automated processes immediately.
#     [I2] Fix MIN_TRADES live constant to 400 in source code (see BUG-1).
#          Find the actual file. Find the actual line. Edit it. Restart the process.
#          Verify with all 6 behavioral tests. Do not rely on LOKI or constants display.
#     [I3] Disable LLM loop at infrastructure level.
#          "Instruct to stop" has been proven ineffective for 2,000 generations.
#          Required actions (all that apply):
#            - Kill the running process (SIGKILL or equivalent).
#            - Revoke or rotate API keys used by the loop.
#            - Disable the scheduler, cron job, or trigger that starts the loop.
#            - Remove or rename the script/binary that runs generations.
#            - Add a firewall rule blocking the LLM API endpoint if necessary.
#          Verify: monitor research log for 60 minutes — no new generations appear.
#          Log: "I3: Loop disabled at infrastructure level at [TIMESTAMP].
#                Method: [DESCRIBE EXACTLY WHAT WAS DONE].
#                Verification: No new gens observed for 60 minutes as of [TIMESTAMP]."
#          If new generations appear after I3: the correct method was not used.
#          Try again with a more fundamental disablement.
#          Do not proceed to Step Z until I3 verification is complete.
#
#   STEP Z (human operator, manual, strictly in order):
#     Z1 → Z2 → Z3 → Z4a → Z4 → Z5 → Z6 → Z7 → Z8 → Z9
#     (Full Step Z procedure defined below)
#
#   PHASE A0 (after Step Z complete):
#     All 6 checks must pass before any backtest proceeds.
#
#   PHASE A1 (after A0 complete):
#     25-cell deterministic grid scan (Python script, no LLM, no ODIN).
#
#   AFTER GRID SCAN:
#     Deploy confirmed champion with TYR position sizing.
#     Current TYR: F&G=21 (Extreme Fear) → size = 25% × 50% = 12.5%.
#     LLM loop: permanently retired. Do not restart under any circumstances.
#     LOKI: permanently retired. Do not use for any purpose.
#     If grid scan finds improvement: deploy improved champion, not LLM loop.
#     If grid scan finds no improvement: deploy Gen 6612 champion as confirmed.
#
# ══════════════════════════════════════════════════════════════════
# STEP Z — MANUAL VERIFICATION PROCEDURE
# ══════════════════════════════════════════════════════════════════
#
# Execute strictly in order. Do not skip steps. Do not proceed past a
# failed step without resolving the failure.
# Prerequisite: [I1], [I2], [I3] all confirmed complete before starting Step Z.
#
# Z1: LOAD GEN 6612 STORED YAML FROM STORAGE.
#   Locate the YAML file/record stored when Gen 6612 was accepted.
#   Do NOT use the displayed YAML (stale since Gen 1592).
#   Do NOT reconstruct from memory or this document.
#   Verify: file/record timestamp consistent with Gen 6612 acceptance.
#   Log: "Z1: Gen 6612 YAML loaded from [PATH/LOCATION] at [TIMESTAMP]."
#
# Z2: CONFIRM CHAMPION SHARPE BY RE-RUNNING GEN 6612 YAML.
#   Run full backtest of Gen 6612 YAML on 2-year 1h BTC/USD, ETH/USD, SOL/USD data.
#   Expected result: sharpe ≈ 2.3568, trades ≈ 1270, win_rate ≈ 40.0%.
#   If result matches: champion confirmed. Log sharpe as [CONFIRMED_SHARPE].
#   If result does NOT match: data or engine issue. Do not proceed. Investigate.
#   Log: "Z2: Re-run sharpe=[RESULT]. Expected 2.3568.
#         [CONFIRMED / MISMATCH — investigate before proceeding]."
#
# Z3: EXTRACT AND CONFIRM ALL PARAMETER VALUES FROM GEN 6612 YAML.
#   Read every parameter value from the stored Gen 6612 YAML directly.
#   Record confirmed values:
#     rsi_period_hours:    [READ FROM YAML] (expected: 22)
#     rsi_long_threshold:  [READ FROM YAML] (expected: 37.77)
#     rsi_short_threshold: [READ FROM YAML] (previously unknown)
#     trend_period_hours:  [READ FROM YAML] (expected: 48)
#     take_profit_pct:     [READ FROM YAML] (previously unknown, est. 4.90–5.10)
#     stop_loss_pct:       [READ FROM YAML] (expected: 1.91)
#     timeout_hours:       [READ FROM YAML] (expected: 159)
#     size_pct:            [READ FROM YAML] (expected: 25)
#     max_open:            [READ FROM YAML] (expected: 3)
#   Note any values that differ from expectations. Investigate discrepancies.
#   Log: "Z3: All parameters confirmed from Gen 6612 YAML.
#         [LIST ALL CONFIRMED VALUES]."
#   After Z3: update KNOWN PARAMETER VALUES block and displayed YAML with
#   confirmed values. Set all UNKNOWN tokens to confirmed values.
#
# Z4a: VERIFY ACCEPTANCE GATE BASELINE IS SET TO 2.3568.
#   Inspect gate code directly. Find the variable/constant holding champion sharpe.
#   Must read 2.3568 (the Gen 6612 result).
#   If it reads anything else: gate is misaligned. Fix directly in source code.
#   Log: "Z4a: Gate baseline confirmed = [VALUE].
#         [CORRECT (2.3568) / INCORRECT — fixed to 2.3568]."
#
# Z4: VERIFY MIN_TRADES GATE IS READING 400 (should be done in [I2], confirm here).
#   DO NOT rely on constants display block — it shows LOKI's logged state, not runtime.
#   DO NOT rely on LOKI log entries — both Gen 542 and Gen 6800 entries failed.
#   Verify by behavioral test ONLY. Run all 6 tests defined in BUG-1.
#   Runtime inspection must show MIN_TRADES[futures_swing] = 400.
#   All 6 tests must pass (defined in BUG-1 section above).
#   Log: "Z4: MIN_TRADES[futures_swing] = [VALUE] confirmed by behavioral test.
#         Test 1 (28t): [PASS