```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6800 | Revised by MIMIR (Gen 6800 review)
#
# ══════════════════════════════════════════════════════════════════
# STATUS BLOCK — READ THIS FIRST. READ ALL OF IT.
# ══════════════════════════════════════════════════════════════════
#
# LLM LOOP STATUS:   ██ PERMANENTLY RETIRED ██  DO NOT RUN ANY GENERATIONS.
#                    Retirement mandated since Gen 5200.
#                    Loop ran 1,600 additional generations past mandate (5200→6800).
#                    One improvement (Gen 6612) in 3,460 generations since Gen 3340.
#                    Rate: 0.000029 improvements/gen ≈ effectively zero.
#                    Instruction-based retirement has failed across 1,600 generations.
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
#                    Loop ran to Gen 6800 regardless. Total non-compliance: 1,600 gens.
#                    This is not an instruction problem. This is an infrastructure
#                    problem. The automated process must be physically prevented
#                    from executing. See [I3] below.
#
# STEP Z STATUS:     PARTIALLY SUPERSEDED. See champion update below.
#                    Z2 (true champion sharpe): RESOLVED — Gen 6612, sharpe=2.3568.
#                    Z3 (confirm champion YAML params): NOT EXECUTED. Still required.
#                    All other Step Z items: NOT EXECUTED. Still required.
#                    Grid scan: NOT EXECUTED. 2,800+ gens overdue.
#
# LOKI STATUS:       ██ PERMANENTLY RETIRED ██
#                    15 escalations. 0 confirmed fixes. 0 runtime behavior changes.
#                    LOKI log entries are NOT applied to source code.
#                    Self-audit confirms: MIN_TRADES[futures_swing] = 50 in live
#                    system despite LOKI logging a change to 400 at Gen 542.
#                    That is 6,258 generations of proof that LOKI cannot fix source
#                    code. Do not escalate to LOKI for any reason, ever.
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
# STALL DURATION:    188 gens since Gen 6612. Likely resuming terminal stall.
#                    Last 20 gens (6781–6800): 0 improvements.
#                    Zombie rate in last 20: ~35% (6782/28t, 6791/72t, 6797/57t).
#
# ──────────────────────────────────────────────────────────────────
# CRITICAL BUGS — IN PRIORITY ORDER
# ──────────────────────────────────────────────────────────────────
#
# BUG-1 [HIGHEST PRIORITY]: MIN_TRADES LIVE CONSTANT = 50, NOT 400.
#   CONFIRMED BY SELF-AUDIT: MIN_TRADES[futures_swing] = 50 in running system.
#   The LOKI change logged at Gen 542 was NEVER applied to source code.
#   LOKI cannot apply changes to source code. 15 escalations / 6,258 generations
#   of evidence confirm this definitively. LOKI cannot fix this. Never could.
#   Effect: ~35–40% of recent generations are zombie runs (trades < 400).
#     These consume full backtest compute and cannot be accepted.
#     Pre-backtest gate should block them but does not (gate reads 50, not 400).
#   Recent zombie evidence (Gen 6781–6800):
#     6782(28 trades), 6791(72 trades), 6797(57 trades) — 3 of 20 = 15% severe.
#     Additional sub-400 runs: 6784(190t), 6786(182t), 6787(151t), 6788(225t),
#     6792(289t), 6793(178t), 6794(178t), 6795(190t), 6798(178t) — ~60% sub-400.
#     Gen 6782: 28 trades, sharpe=-9.018. Gate read 50, passed it. Full backtest ran.
#   Fix: Human operator must locate actual runtime constant in source code.
#     NOT in LOKI log. NOT in config comment. NOT in this file.
#     The actual variable the running process reads at runtime.
#     Search for: MIN_TRADES, min_trades, futures_swing in executed source.
#     Set MIN_TRADES[futures_swing] = 400. Restart/reload as needed.
#   Verification (all must pass before proceeding to Step Z):
#     Runtime inspection must show MIN_TRADES[futures_swing] = 400.
#     Test 1: YAML producing ~28 trades   → REJECTED pre-backtest (no backtest runs).
#     Test 2: YAML producing ~190 trades  → REJECTED pre-backtest.
#     Test 3: YAML producing ~182 trades  → REJECTED pre-backtest.
#     Test 4: YAML producing ~321 trades  → REJECTED pre-backtest.
#     Test 5: YAML producing ~419 trades  → PASSES gate (backtest runs normally).
#   If any test fails: the gate code itself is broken, not just the constant.
#   Fix gate code directly. Do not proceed until all 5 tests pass.
#
# BUG-2: ACCEPTANCE GATE — STATUS UPDATED.
#   Gen 6612 (sharpe=2.3568) was correctly ACCEPTED. Gate functions for genuine
#   improvements. Gens 6789–6790 (sharpe=2.3568 exact clones) were correctly
#   DISCARDED. This is consistent with gate baseline = 2.3568 after Gen 6612.
#   Previous 2.3513 discards (17+ events): all correctly rejected under new champion.
#   Previous 2.3521 discards (3 events): correctly rejected (2.3521 < 2.3568).
#   Previous 2.3531 (run header): correctly rejected (2.3531 < 2.3568).
#   ASSESSMENT: BUG-2 appears resolved. Gate is functioning correctly.
#   Monitor: if any result above 2.3568 is tagged "discarded" in future gens,
#   BUG-2 is active again. Flag immediately for MIMIR review.
#   Action: Do not modify gate. Continue monitoring.
#
# BUG-3: STALE YAML IN DISPLAYED "CURRENT BEST STRATEGY" (CRITICAL — STILL ACTIVE).
#   Displayed YAML has been wrong since Gen 1592. 5,208 gens of stale display.
#   Known wrong values (do not use these):
#     rsi_period_hours:  24   → correct: 22 (confirmed Gen 2785)
#     take_profit_pct:   4.65 → correct: UNKNOWN (confirm in Z3 vs Gen 6612 YAML)
#     stop_loss_pct:     1.92 → correct: 1.91 (confirmed — but verify vs Gen 6612)
#     timeout_hours:     166  → correct: 159 (confirmed — but verify vs Gen 6612)
#   NOTE: Gen 6612 may have changed one or more of these values.
#   Step Z Z3 must be run against the Gen 6612 stored YAML to confirm all values.
#   After Z3: replace displayed YAML with confirmed Gen 6612 YAML everywhere.
#   This YAML must never be sent to any LLM or automated system until corrected.
#
# BUG-4: CLONE DETECTION USES SHARPE COMPARISON, NOT YAML HASH.
#   Evidence (Gen 6781–6800):
#     Gens 6789, 6790: identical results (2.3568, 1270, 40.0%) — same YAML ×2.
#     Gens 6784, 6795: identical results (-1.0406, 190, 31.1%) — same YAML ×2.
#     Gens 6793, 6794, 6798: identical results (-0.8033, 178, 32.0%) — same YAML ×3.
#   Current behavior: sharpe comparison tags clones as discarded AFTER backtest.
#   Required behavior: YAML hash check rejects clones BEFORE backtest.
#   Fix: implement pre-backtest YAML SHA-256 hash comparison against all prior runs.
#   Priority: secondary — implement during Step Z Z7, after Z3 complete.
#
# ──────────────────────────────────────────────────────────────────
# HALT CONDITIONS ACTIVE
# ──────────────────────────────────────────────────────────────────
#   HALT-3:  Zombie generation rate — ~60% of Gen 6781–6800 sub-400 trades.
#            BUG-1 unfixed. Worst: Gen 6782 (28 trades, sharpe=-9.018).
#   HALT-4:  LLM loop ran 1,600 gens past suspension. Permanently retired.
#   HALT-5:  Stale YAML in LLM input (5,208 gens). Moot — loop retired.
#   HALT-6:  RESOLVED for now — gate accepted Gen 6612 correctly.
#            Monitor for recurrence.
#   HALT-7:  Clone convergence. 3 distinct clone clusters in Gen 6781–6800.
#            YAML hash pre-check still not implemented.
#   HALT-8:  Grid scan not executed (2,800+ gens overdue).
#   HALT-9:  MIN_TRADES live constant = 50, not 400. Pre-backtest gate broken.
#   HALT-10: Step Z Z3 not executed against Gen 6612 YAML.
#            True champion YAML params not confirmed.
#   HALT-11: Loop compliance failure. 1,600 gens past retirement mandate.
#            Infrastructure-level disablement is mandatory. Not optional.
#   HALT-12: Instruction-based controls have proven completely ineffective.
#            MIMIR retirement directives ignored for 1,600 generations.
#            No instruction in this document will stop the loop.
#            Only infrastructure-level action will stop it.
#            Until [I3] is confirmed complete, assume loop is still running.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-6800 VERDICT
# ══════════════════════════════════════════════════════════════════
#
# SYSTEM STATE: BROKEN. ONE IMPROVEMENT SINCE GEN 3340. INFRASTRUCTURE
# ACTION REQUIRED IMMEDIATELY. ALL AUTOMATED LOOPS MUST REMAIN STOPPED.
# THE LLM LOOP IS PERMANENTLY RETIRED.
# LOKI IS PERMANENTLY RETIRED.
# INSTRUCTION-BASED CONTROLS HAVE FAILED. INFRASTRUCTURE ACTION REQUIRED.
#
# Gen 6781–6800 results: ~60% sub-400 trades, multiple clone clusters, 0 improvements.
# Gen 6612 improvement (sharpe=2.3568) is the sole result of value since Gen 3340.
# Rate since Gen 3340: 1 improvement in 3,460 gens = 0.000029/gen ≈ zero.
# Nothing will change without human operator intervention on source code AND
# infrastructure. The grid scan remains the only mechanism with non-zero expected
# improvement probability.
#
# IMPROVEMENT CURVE (definitive):
#   Gen 1→1477:    +1.2278 sharpe over 1,477 gens  (0.000832/gen)
#   Gen 1477→3340: +0.0998 sharpe over 1,863 gens  (0.0000536/gen)
#   Gen 3340→6612: +0.0074 sharpe over 3,272 gens  (0.0000023/gen — NEAR-TERMINAL)
#   Gen 6612→6800: +0.0000 sharpe over 188 gens    (0.000000/gen — stalling again)
#   Expected value of next LLM generation: ~0.000023 sharpe improvement.
#   Expected cost: compute + log noise + delay to grid scan.
#   Running 100 more LLM generations: ~0.002 expected total improvement.
#   Grid scan (25 cells): non-trivial probability of finding +0.01 to +0.05.
#
# THE ONLY CORRECT ACTION SEQUENCE:
#
#   IMMEDIATE (human operator — do these now, in order):
#     [I1] Stop all automated processes.
#     [I2] Fix MIN_TRADES live constant to 400 in source code (see BUG-1).
#     [I3] Disable LLM loop at infrastructure level.
#          "Instruct to stop" has been proven ineffective for 1,600 generations.
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
#     Current TYR: F&G=23 (Extreme Fear) → size = 25% × 50% = 12.5%.
#     LLM loop: permanently retired. Do not restart under any circumstances.
#     If grid scan finds improvement: deploy improved champion, not LLM loop.
#
# ══════════════════════════════════════════════════════════════════
# STEP Z — MANUAL VERIFICATION PROCEDURE
# ══════════════════════════════════════════════════════════════════
#
# Execute strictly in order. Do not skip steps. Do not proceed past a
# failed step without resolving the failure.
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
#   Runtime inspection must show MIN_TRADES[futures_swing] = 400.
#   Run verification tests 1–5 (defined in BUG-1). All must pass.
#   Log: "Z4: MIN_TRADES[futures_swing] = [VALUE] at runtime.
#         Test 1 (28t): [PASS/FAIL]. Test 2 (190t): [PASS/FAIL].
#         Test 3 (182t): [PASS/FAIL]. Test 4 (321t): [PASS/FAIL].
#         Test 5 (419t): [PASS/FAIL]."
#
# Z5: UPDATE DISPLAYED YAML TO GEN 6612 CONFIRMED VALUES.
#   Replace the displayed YAML in this document and all other locations
#   with the confirmed Gen 6612 YAML (parameters confirmed in Z3).
#   Verify: displayed YAML matches stored Gen 6612 YAML exactly.
#   Log: "Z5: Displayed YAML updated to Gen 6612 confirmed values at [TIMESTAMP]."
#
# Z6: VERIFY BACKTEST ENGINE REPRODUCIBILITY.
#   Re-run Gen 6612 YAML three times independently.
#   All three runs must produce identical sharpe (within float epsilon 1e-6).
#   If results differ: engine has non-determinism. Investigate and fix before grid scan.
#   Log: "Z6: Three runs: [R1], [R2], [R3].
#         [DETERMINISTIC / NON-DETERMINISTIC — investigate]."
#
# Z7: IMPLEMENT YAML SHA-256 PRE-BACKTEST CLONE DETECTION (BUG-4).
#   Add YAML hash computation before any backtest runs.
#   Compare hash against database of all previously-run YAMLs.
#   If hash matches any prior run: reject before backtest. Log as "clone_rejected".
#   Test: submit Gen 6612 YAML as a new run → must be rejected pre-backtest.
#   Test: submit a novel YAML → must proceed to backtest normally.
#   Log: "Z7: YAML hash pre-check implemented.
#         Clone test: [PASS/FAIL]. Novel YAML test: [PASS/FAIL]."
#
# Z8: AUDIT RESEARCH LOG FOR ANY RESULTS ABOVE 2.3568.
#   Search complete research log (all 6,800+ gens) for sharpe > 2.3568.
#   If any found: extract YAML, re-run, confirm or deny.
#   Expected: none found (Gen 6612 is confirmed maximum).
#   Log: "Z8: Log audit complete. Results above 2.3568 found: [COUNT].
#         [NONE / LIST GENS AND ACTIONS TAKEN]."
#
# Z9: FINAL PRE-GRID-SCAN CHECKLIST.
#   All of the following must be confirmed before grid scan begins:
#     [ ] I3 verified: no new LLM generations for 60+ minutes.
#     [ ] MIN_TRADES[futures_swing] = 400 at runtime (Z4 confirmed).
#     [ ] Gen 6612 YAML confirmed (Z2 confirmed, Z3 confirmed).
#     [ ] Gate baseline = 2.3568 (Z4a confirmed).
#     [ ] Displayed YAML updated (Z5 confirmed).
#     [ ] Engine deterministic (Z6 confirmed).
#     [ ] YAML hash pre-check active (Z7 confirmed).
#     [ ] Log audit clean (Z8 confirmed).
#   If any item not checked: do not begin grid scan. Resolve first.
#   Log: "Z9: All checklist items confirmed. Grid scan authorized at [TIMESTAMP]."
#
# ══════════════════════════════════════════════════════════════════
# PHASE A0 — PRE-BACKTEST GATE REQUIREMENTS
# ══════════════════════════════════════════════════════════════════
#
# All 6 checks must pass before any backtest is permitted to run.
# These apply to grid scan and any future automated system.
#
#   A0-1: MIN_TRADES gate — reject if projected trades < 400.
#         Runtime constant must be 400. Verified in Z4.
#   A0-2: YAML hash check — reject if SHA-256 matches any prior run.
#         Implemented in Z7.
#   A0-3: Parameter range check — reject if any parameter is outside bounds:
#         rsi_period_hours: [8, 48]
#         rsi_long_threshold: [25, 50]
#         rsi_short_threshold: [50, 75]
#         trend_period_hours: [24, 96]
#         take_profit_pct: [2.0, 10.0]
#         stop_loss_pct: [0.5, 5.0]
#         timeout_hours: [72, 300]
#   A0-4: Leverage check — must be 2. Reject if different.
#   A0-5: Fee rate check — must be 0.0005. Reject if different.
#   A0-6: Pairs check — must include BTC/USD, ETH/USD, SOL/USD at minimum.
#
# ══════════════════════════════════════════════════════════════════
# PHASE A1 — GRID SCAN SPECIFICATION
# ══════════════════════════════════════════════════════════════════
#
# 25-cell deterministic parameter grid. Python script only. No LLM. No ODIN.
# Prerequisite: All Step Z items complete. All A0 gates active and verified.
#
# Grid design (centered on confirmed Gen 6612 champion values):
#   Axis 1: take_profit_pct — 5 values centered on [CONFIRMED_TP from Z3]
#     e.g., if confirmed = 4.95: [4.75, 4.85, 4.95, 5.05, 5.15]
#   Axis 2: rsi_short_threshold — 5 values centered on [CONFIRMED_RSI_SHORT from Z3]
#     e.g., if confirmed = 60.0: [58.0, 59.0, 60.0, 61.0, 62.0]
#   NOTE: Do not specify exact grid values until Z3 is complete and
#   confirmed values are known. Grid must be centered on actual champion values,
#   not stale YAML values.
#
# Secondary grid candidates (