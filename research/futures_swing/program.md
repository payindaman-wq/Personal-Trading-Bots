```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-4200 | Revised by MIMIR (Gen 4200 review)
# STATUS: CHAMPION UNCHANGED at Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
#         Champion stall duration: 860 generations (Gen 3340 → Gen 4200). CRITICAL.
#         NEW ANOMALY: sharpe=2.3521/trades=1263 produced at Gens 4183, 4188, 4194 — DISCARDED.
#         This anomaly is the highest-priority diagnostic before any other work proceeds.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-4200 VERDICT:
#
#   CRITICAL NEW FINDING — THE 2.3521 DISCARD ANOMALY:
#     Gens 4183, 4188, 4194: sharpe=2.3521, trades=1263, win_rate=40.1% — tagged "discarded"
#     2.3521 > 2.3494 (champion). These results should have triggered new_best.
#     They did NOT. This is a champion-acceptance logic failure OR evidence that a
#     higher champion already exists in storage that is not reflected in the improvement log.
#     Gens 4181, 4190, 4192, 4193: sharpe=2.3513, trades=1265 — tagged "new_elite"
#     "new_elite" is an unexplained category. It does not appear in prior gen history.
#     Either "new_elite" is a shadow champion tier (bug) or the acceptance gate is broken.
#     RESOLUTION REQUIRED BEFORE ANY GRID SCAN OR LLM GENERATION PROCEEDS.
#
#   GRID SCAN STATUS:
#     Mandated at Gen 3800. Reactivated at Gen 4000. Still zero tests completed at Gen 4200.
#     This is 400 generations of non-execution. The mandate has no teeth.
#     ODIN must demonstrate Phase A0 execution at Gen 4201 or HALT permanently.
#
#   LLM LOOP STATUS:
#     Attractor families unchanged since Gen 2785:
#       - sharpe≈0.6621/trades≈1042 (appears 3/20 recent gens)
#       - sharpe≈-9.018/trades≈28 (appears 2/20 recent gens)
#       - sharpe≈1.3815/trades≈969 (appears 2/20 recent gens)
#     LLM is reading stale YAML (rsi_period=24, TP=4.65, SL=1.92, timeout=176).
#     The displayed "Current Best Strategy" YAML has been wrong since Gen 1592.
#     Every LLM generation is working from corrupted input.
#
#   LOKI STATUS:
#     10 escalations. 0 structural fixes confirmed by results.
#     LOKI is PERMANENTLY SUSPENDED as a resolution mechanism.
#     No further LOKI escalations for any issue described in this document.
#
#   ROOT CAUSE (FINAL, UNCHANGED):
#     The displayed YAML is wrong. The champion storage path may also be wrong.
#     The champion-acceptance logic is broken (2.3521 not accepted).
#     The LLM loop cannot be fixed by prompt changes alone.
#     Only path forward: ODIN executes deterministic YAML diffs. No LLM. No LOKI.
#     If ODIN cannot do this: HALT and report. Do not run Gen 4201.
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
##                        Estimated: 4.95–5.00. Do NOT use estimated value.
##   stop_loss_pct:       1.91   (certain — NOT 1.90, NOT 1.92)
##   timeout_hours:       159    (FROZEN FOREVER)
##   size_pct:            25     (FROZEN)
##   max_open:            3      (FROZEN)
##   leverage:            2      (FROZEN)
##   fee_rate:            0.0005 (FROZEN)
##
## STALE YAML WARNING (PERMANENT — THIS WARNING NEVER EXPIRES):
##   The displayed "Current Best Strategy" YAML is WRONG since Gen 1592:
##     rsi_period_hours: 24     ← WRONG (champion is 22)
##     take_profit_pct:  4.65   ← WRONG (champion is ~4.95–5.00)
##     stop_loss_pct:    1.92   ← WRONG (champion is 1.91)
##     timeout_hours:    176    ← WRONG (champion is 159)
##     rsi_short value:  60     ← UNCONFIRMED (may be 59 or 60)
##   IGNORE THE DISPLAYED YAML ENTIRELY.
##   Load champion EXCLUSIVELY from confirmed storage path with hash verification.
##
## 2.3521 ANOMALY NOTES:
##   Gens 4183, 4188, 4194: sharpe=2.3521, trades=1263, win_rate=40.1% — "discarded"
##   Gens 4181, 4190, 4192, 4193: sharpe=2.3513, trades=1265 — "new_elite"
##   These are NOT normal discards. 2.3521 > champion. "new_elite" is unexplained.
##   HYPOTHESIS A: A silent champion update occurred between Gen 3340 and Gen 4181,
##     storing 2.3521 or 2.3513 as the new internal champion without logging new_best.
##     If true: the real champion is NOT Gen 3340/2.3494. The champion log is broken.
##   HYPOTHESIS B: The acceptance gate has a bug comparing against a wrong baseline
##     (e.g., comparing against the stale YAML's Sharpe rather than stored champion Sharpe).
##   HYPOTHESIS C: "new_elite" is a parallel tracking tier with a broken promotion gate.
##   RESOLUTION PROTOCOL (execute BEFORE Gen 4201):
##     Step Z1: Query champion storage directly. What YAML is stored? What Sharpe?
##     Step Z2: Re-run the YAML producing 2.3521 (identify its parameters from Gen 4183).
##              Confirm whether result is reproducible.
##     Step Z3: If 2.3521 is reproducible and its YAML differs from Gen 3340 champion:
##              Log it as new champion immediately. Update champion log. Update hash.
##     Step Z4: Determine what "new_elite" means in the codebase. If it is a champion
##              tier that should trigger new_best but doesn't: fix the promotion gate.
##              Then re-evaluate whether any new_elite result should be the champion.
##     Step Z5: After Z1–Z4, confirm the true champion YAML and Sharpe.
##              All subsequent grid tests use this confirmed champion as baseline.
##     DO NOT SKIP STEP Z. Running grid tests from a wrong baseline wastes all tests.
##
## ─────────────────────────────────────────────────────────
## GEN 4200 SITUATION ASSESSMENT:
##
##   Champion stall: 860 generations. True stall may be shorter if 2.3521 is real.
##   Grid scan mandate: 400+ generations of non-execution.
##   LLM loop: producing same attractor families as Gen 2785.
##   Acceptance logic: broken (2.3521 not accepted as champion).
##   Champion storage: possibly ahead of improvement log.
##
##   Last 20 generations (4181–4200) breakdown:
##     "new_elite" (2.3513/1265): Gens 4181, 4190, 4192, 4193 = 4/20 = 20%
##     High-sharpe discards (2.3521/1263): Gens 4183, 4188, 4194 = 3/20 = 15%
##     Low-trade zombies (<400 trades): Gens 4182(28), 4196(28), 4197(178) = 3/20 = 15%
##     Attractor family (0.6621/1042): Gens 4189, 4191, 4198 = 3/20 = 15%
##     Attractor family (1.3815/969): Gens 4185, 4186 = 2/20 = 10%
##     Other discarded: Gens 4184, 4187, 4195, 4199, 4200 = 5/20 = 25%
##     True grid-scan results: ZERO in 400 generations.
##
##   CONFIRMED INFRASTRUCTURE FAILURES (persistent, unresolved):
##     ✗ Champion acceptance gate: BROKEN (2.3521 not promoted)
##     ✗ "new_elite" promotion: BROKEN or UNDEFINED
##     ✗ LLM suspension: NOT ENFORCED
##     ✗ Clone detection: NOT WORKING (repeated identical results)
##     ✗ Zombie pre-rejection: PARTIALLY WORKING (40% → 15% improvement, still failing)
##     ✗ Stale YAML rejection: NOT WORKING
##     ✗ Grid scan execution: ZERO TESTS in 400 generations
##     ✗ Champion storage/log consistency: UNKNOWN (Step Z required)
##
## ─────────────────────────────────────────────────────────
## MANDATORY PRE-RUN SEQUENCE (Gen 4201 MUST begin with this — no exceptions):
##
##   STEP Z — ANOMALY RESOLUTION (see full protocol above)
##   Complete Z1–Z5 before any backtest submission.
##   If Step Z reveals the true champion is 2.3521 (or any value other than 2.3494):
##     Update all references in this document.
##     The grid scan baselines from the true confirmed champion.
##   If Step Z cannot be completed (storage unreachable, hash unavailable):
##     HALT. Report: "STEP Z FAILED: Cannot confirm true champion. Halting Gen 4201."
##
##   PHASE A0 — CHAMPION RE-CONFIRMATION (immediately after Step Z)
##
##   A0.1: Load confirmed champion YAML from storage (post Step Z). Verify hash.
##         Submit with ZERO parameter changes.
##         Expected result: matches confirmed champion sharpe/trades/win_rate exactly.
##         If result differs by more than (±0.0005 sharpe, ±2 trades): HALT.
##         Log: "A0.1 champion re-confirmation: [PASS/FAIL]. Result: (sharpe, trades)."
##
##   A0.2: From confirmed storage YAML, log exact values of:
##         - rsi_short_threshold → confirmed_rsi_short
##         - take_profit_pct → confirmed_TP
##         Replace ALL [CONFIRM_*] tokens with confirmed values throughout this document.
##         Log: "A0.2 confirmed_rsi_short=[VALUE], confirmed_TP=[VALUE]."
##
##   A0.3: Verify fingerprint/clone-detection system is active:
##         Inject A0.1 champion YAML → must be rejected as clone BEFORE submission.
##         If NOT rejected → fingerprint system broken → HALT.
##         Log: "A0.3 fingerprint self-test: [PASS/FAIL]."
##
##   A0.4: Verify zombie pre-rejection is active:
##         Construct YAML with rsi_long=50, rsi_short=55 (known zombie params).
##         Submit to pre-backtest validator → must be rejected on RSI range check.
##         If NOT rejected → RSI validation broken → HALT.
##         Log: "A0.4 zombie pre-rejection self-test: [PASS/FAIL]."
##
##   A0.5: Verify acceptance gate is functioning:
##         Construct a synthetic result record: sharpe=confirmed_champion_sharpe + 0.01,
##         trades=1265, win_rate=40.1%. Feed to acceptance logic.
##         Must be accepted as new_best. If NOT accepted → acceptance gate broken → HALT.
##         Log: "A0.5 acceptance gate self-test: [PASS/FAIL]."
##         [Note: A0.5 is a dry-run test of the gate logic, not a backtest submission.]
##
##   A0.6: Resolve "new_elite" category:
##         If "new_elite" is defined in codebase: document what it means.
##         If it should trigger champion update but doesn't: fix before proceeding.
##         If it is a valid sub-champion tier (e.g., top-10 non-champion): document and accept.
##         Log: "A0.6 new_elite resolution: [DEFINITION]. Action taken: [NONE/FIX]."
##
##   Do NOT proceed to Phase A1 until ALL of A0.1–A0.6 are PASS.
##   A single FAIL in A0 → HALT. Fix the failing check. Re-run A0 from the top.
##   Do NOT escalate to LOKI. Fix directly in ODIN codebase.
##
## ─────────────────────────────────────────────────────────
## MANDATORY HALT CONDITIONS (check before EVERY generation):
##
##   HALT-1: Grid scan mode active AND proposed test does not match
##            the next pre-specified grid test exactly (verified by parameter diff).
##            → HALT. Log: "GRID DEVIATION at Gen XXXX."
##
##   HALT-2: Three or more of the last 20 results are exact champion clones.
##            → HALT. Log: "CLONE FLOOD at Gen XXXX."
##
##   HALT-3: Five or more of the last 20 results are low-trade zombies (<400 trades).
##            → HALT. Log: "ZOMBIE FLOOD at Gen XXXX."
##            [Gen 4200 does NOT meet this condition: only 3/20 zombies. Monitor.]
##
##   HALT-4: Step Z has not been completed and Gen 4201 is about to start.
##            → HALT. Log: "STEP Z INCOMPLETE. Cannot start Gen 4201."
##
##   HALT-5: A0.1–A0.6 have not all passed and Phase A1 is about to start.
##            → HALT. Log: "A0 INCOMPLETE. Cannot start Phase A1."
##
##   HALT-6: A result with sharpe > current_champion_sharpe is tagged anything
##            other than "new_best" (e.g., "discarded", "new_elite").
##            → HALT IMMEDIATELY. Log: "ACCEPTANCE GATE FAILURE at Gen XXXX.
##              Result sharpe=[X] > champion sharpe=[Y] but not accepted."
##            This condition was met at Gens 4183, 4188, 4194. It was not caught.
##            It MUST be caught going forward.
##
##   "HALT" means: stop all generation loops. Do not start Gen N+1.
##   Output the halt condition to the run log. Wait for human operator review.
##   Do NOT escalate to LOKI. Do NOT resume automatically.
##
## ─────────────────────────────────────────────────────────
## STEP A — PRIMARY RESEARCH MODE: DETERMINISTIC GRID SCAN
## [STATUS: MANDATED Gen 3800. Reactivated Gen 4000. STILL UNEXECUTED at Gen 4200.]
## [FINAL REACTIVATION: Execute at Gen 4201 or HALT permanently.]
##
##   EXECUTION MODEL:
##   ODIN constructs each test YAML programmatically from storage-retrieved champion file.
##   No LLM involvement of any kind. No free-form proposals. No prompt submissions.
##   Each test = (confirmed champion YAML from storage, post Step Z) + (ONE pre-specified change).
##   ODIN verifies the diff before submission. If diff ≠ expected → reject, log, halt.
##
##   IF ODIN CANNOT EXECUTE THIS MODEL:
##   Output: "CAPABILITY GAP: Cannot execute deterministic grid without LLM."
##   Then HALT PERMANENTLY. Do not run any further LLM generations as substitute.
##   The cost of 400 wasted LLM generations (Gen 3801–4200) is documented.
##   Continuing would make it 500. That is not acceptable.
##
##   ─────────────────────────────────────────────────────
##   PHASE A1 — TAKE PROFIT GRID (highest priority)
##
##   Baseline: confirmed_TP from A0.2 (estimated 4.95–5.00, exact value required).
##   Each test: confirmed champion YAML + ONE change to take_profit_pct only.
##   Diff must show exactly 1 line changed. Verify before submission.
##
##   A1.1: take_profit_pct = confirmed_TP + 0.05
##   A1.2: take_profit_pct = confirmed_TP + 0.10
##   A1.3: take_profit_pct = confirmed_TP + 0.15
##   A1.4: take_profit_pct = confirmed_TP + 0.20
##   A1.5: take_profit_pct = confirmed_TP + 0.25
##   A1.6: take_profit_pct = confirmed_TP - 0.10
##          (confirmed_TP - 0.05 already tested at Gen 3400 = 2.3428, below champion)
##   A1.7: take_profit_pct = confirmed_TP - 0.15
##   A1.8: take_profit_pct = confirmed_TP + 0.30
##   A1.9: take_profit_pct = confirmed_TP + 0.40
##   A1.10: take_profit_pct = confirmed_TP + 0.50
##
##   SPECIAL NOTE: The 2.3521 results at Gens 4183/4188/4194 (trades=1263, win_rate=40.1%)
##   may correspond to a specific TP value. If the parameter generating 2.3521 can be
##   identified from generation logs, test it explicitly as A1.0 before proceeding.
##   A TP value of confirmed_TP + 0.05 is the most likely candidate based on Gen 3400 data.
##
##   Accept only if: sharpe > confirmed_champion_sharpe AND trades in [900, 1400].
##   If A1.1 improves champion: immediately test A1.1+0.05 and A1.1+0.10 before A1.2.
##   If any A1 test produces trades < 1100: TP is too high — stop upward scan.
##   If no A1 test improves: TP confirmed at local maximum. Log and proceed to A2.
##   Log each result: "A1.X: TP=[value] → sharpe=[X], trades=[Y]. [accept/reject reason]"
##
##   ─────────────────────────────────────────────────────
##   PHASE A2 — RSI SHORT THRESHOLD GRID (second priority)
##
##   Baseline: confirmed_rsi_short from A0.2 (59 or 60 — exact value required).
##   Each test: confirmed champion YAML + ONE change to rsi_short_threshold only.
##   Constraint: rsi_short must be in [55, 70].
##   Constraint: (rsi_short - rsi_long_threshold) must be >= 10.
##
##   A2.1: rsi_short = confirmed_rsi_short - 1
##   A2.2: rsi_short = confirmed_rsi_short + 1
##   A2.3: rsi_short = confirmed_rsi_short - 2
##   A2.4: rsi_short = confirmed_rsi_short + 2
##   A2.5: rsi_short = confirmed_rsi_short - 3
##   A2.6: rsi_short = confirmed_rsi_short + 3
##
##   Accept only if: sharpe > confirmed_champion_sharpe AND trades in [900, 1400].
##   If any A2 test improves: re-run A1 grid from new champion before continuing A2.
##   Log each result with same format as A1.
##
##   ─────────────────────────────────────────────────────
##   PHASE A3 — RSI PERIOD GRID (third priority)
##
##   Baseline: rsi_period_hours = 22 (confirmed Gen 2785).
##   Each test: confirmed champion YAML + ONE change to rsi_period_hours only.
##   Constraint: rsi_period_hours must be in [18, 28].
##
##   A3.1: rsi_period_hours = 21
##   A3.2: rsi_period_hours = 23
##   A3.3: rsi_period_hours = 20
##   A3.4: rsi_period_hours = 24  [diagnostic — expected to produce stale YAML attractor]
##   A3.5: rsi_period_hours = 19
##   A3.6: rsi_period_hours = 25
##   A3.7: rsi_period_hours = 18
##   A3.8: rsi_period_hours = 26
##
##   Accept only if: sharpe > confirmed_champion_sharpe AND trades in [900, 1400].
##   If A3.4 produces (sharpe ≈ 0.77, trades ≈ 1041): confirms Attractor 4 family origin.
##     Log: "A3.4 diagnostic: rsi_period=24 is the stale YAML contamination source."
##   Log each result with same format as A1.
##
##   ─────────────────────────────────────────────────────
##   PHASE A4 — TREND PERIOD GRID (fourth priority)
##
##   Baseline: trend_period_hours = 48 (certain).
##   Each test: confirmed champion YAML + ONE change to trend_period_hours only.
##   Constraint: trend_period_hours must be in [24, 96].
##
##   A4.1: trend_period_hours = 36
##   A4.2: trend_period_hours = 42
##   A4.3: trend_period_hours = 54
##   A4.4: trend_period_hours = 60
##   A4.5: trend_period_hours = 72
##   A4.6: trend_period_hours = 30
##   A4.7: trend_period_hours = 84
##   A4.8: trend_period_hours = 24
##   A4.9: trend_period_hours = 96
##
##   Accept only if: sharpe > confirmed_champion_sharpe AND trades in [900, 1400].
##
##   ─────────────────────────────────────────────────────
##   PHASE A5 — RSI LONG THRESHOLD GRID (fifth priority)
##
##   Baseline: rsi_long_threshold = 37.77 (confirmed Gen 1477, frozen 2,500+ gens).
##   Each test: confirmed champion YAML + ONE change to rsi_long_threshold only.
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
##   A5.9: rsi_long = 35.00
##   A5.10: rsi_long = 39.50
##
##   Accept only if: sharpe > confirmed_champion_sharpe AND trades in [900, 1400].
##   Note: higher rsi_long → more long entries → higher trade count.
##         lower rsi_long → fewer long entries → lower trade count.
##   If A5.2–A5.4 produce trades > 1350: rsi_long is near a trade-count cliff.
##
##   ─────────────────────────────────────────────────────
##   PHASE A6 — STOP LOSS GRID (sixth priority)
##
##   Baseline: stop_loss_pct = 1.91 (confirmed