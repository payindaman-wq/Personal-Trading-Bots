```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-5200 | Revised by MIMIR (Gen 5200 review)
# STATUS: CHAMPION LOGGED at Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
#         TRUE CHAMPION STATUS: UNKNOWN — acceptance gate broken since at least Gen 3340.
#         Discarded results exceeding champion sharpe: 2.3521 (×3), 2.3513 (×7+).
#         The real champion in storage may exceed 2.3494. Champion log is unreliable.
#         Champion stall duration: 1,860 generations (Gen 3340 → Gen 5200). CRITICAL.
#         Grid scan mandate: 1,400 generations of non-execution. TERMINAL.
#         LLM loop: degenerated. 35% zombie rate in last 20 gens. Approaching HALT-3.
#         LOKI: PERMANENTLY SUSPENDED. 11 escalations. 0 confirmed fixes.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-5200 VERDICT:
#
#   SYSTEM STATE: BROKEN. HARD HALT IS THE CORRECT ACTION.
#
#   EVIDENCE SUMMARY:
#     1. ACCEPTANCE GATE: Broken since at least Gen 3340.
#        2.3521 (×3 at Gens 4183, 4188, 4194) — discarded instead of new_best.
#        2.3513 (×7+ including Gens 5182, 5185, 5198, 5200) — discarded instead of new_best.
#        Both values exceed logged champion (2.3494).
#        The system is discarding real improvements every few generations.
#        The true champion in storage is unknown. It could be 2.3494, 2.3513, or 2.3521.
#
#     2. DISPLAYED YAML: Wrong since Gen 1592.
#        rsi_period_hours: 24 (wrong — champion is 22)
#        take_profit_pct: 4.65 (wrong — champion is ~4.95–5.00)
#        stop_loss_pct: 1.92 (wrong — champion is 1.91)
#        timeout_hours: 176 (wrong — champion is 159)
#        Every LLM generation for 3,608 generations has used corrupted input.
#        This is permanent until the YAML display is fixed.
#
#     3. LLM LOOP: Degenerated beyond utility.
#        Last 20 gens: 7 zombies (35%), 4 discarded clones of 2.3513, repeated exact
#        duplicates across generations (5189=5187, 5191=5190, 5196=5197).
#        Clone detection: NOT WORKING for zombie-class outputs.
#        Zombie pre-rejection: NOT WORKING (zombies consuming backtest slots).
#        Attractor families: unchanged since Gen 2785 (2,415 generations).
#
#     4. GRID SCAN: 1,400 generations of non-execution.
#        Mandated Gen 3800. Reactivated Gen 4000. Reaffirmed Gen 4200.
#        Now Gen 5200. Still zero tests.
#        ODIN structurally cannot execute deterministic YAML construction without LLM.
#        If this capability does not exist, it must be built or ODIN must halt.
#
#     5. LOKI: Permanently suspended. 11 escalations. 0 confirmed fixes by results.
#        No escalation of any finding in this document to LOKI. Ever. For any reason.
#
#   REQUIRED ACTIONS BEFORE Gen 5201:
#     Complete STEP Z (champion storage audit).
#     Complete PHASE A0 (infrastructure self-tests, all 6 checks).
#     If any check fails: HALT. Fix. Re-run A0 from top.
#     Do NOT proceed to any generation until A0.1–A0.6 all PASS.
#
# ══════════════════════════════════════════════════════════════════

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor — pre-backtest enforcement mandatory, pre-run not post-run)

---
## ██████████████████████████████████████████████████████████
## ODIN INJECTION NOTE (INTERNAL ONLY — NEVER SEND TO LLM)
##
## ─────────────────────────────────────────────────────────
## CONFIRMED CHAMPION (logged): Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
## TRUE CHAMPION (in storage): UNKNOWN — must be determined by Step Z.
##
## KNOWN CONFIRMED PARAMETER VALUES (load from storage, verify hash):
##   rsi_period_hours:    22     (certain — confirmed Gen 2785)
##   rsi_long_threshold:  37.77  (certain — confirmed Gen 1477)
##   rsi_short_threshold: [MUST BE CONFIRMED FROM STORAGE — 59 or 60, do not assume]
##   trend_period_hours:  48     (certain)
##   take_profit_pct:     [MUST BE CONFIRMED FROM STORAGE]
##                        Estimated range: 4.95–5.00. Do NOT use estimated value.
##                        Do NOT use 4.65 (stale YAML value — wrong since Gen 1592).
##   stop_loss_pct:       1.91   (certain — NOT 1.90, NOT 1.92)
##   timeout_hours:       159    (FROZEN FOREVER — NOT 176)
##   size_pct:            25     (FROZEN)
##   max_open:            3      (FROZEN)
##   leverage:            2      (FROZEN)
##   fee_rate:            0.0005 (FROZEN)
##
## STALE YAML WARNING (PERMANENT — THIS WARNING NEVER EXPIRES):
##   The displayed "Current Best Strategy" YAML has been WRONG since Gen 1592:
##     rsi_period_hours: 24     ← WRONG (champion is 22)
##     take_profit_pct:  4.65   ← WRONG (champion is ~4.95–5.00)
##     stop_loss_pct:    1.92   ← WRONG (champion is 1.91)
##     timeout_hours:    176    ← WRONG (champion is 159)
##     rsi_short value:  60     ← UNCONFIRMED (may be 59 or 60)
##   IGNORE THE DISPLAYED YAML ENTIRELY.
##   Load champion EXCLUSIVELY from confirmed storage path with hash verification.
##   If the YAML display cannot be fixed: add a warning banner to the display
##   that reads "STALE — DO NOT USE — Load from storage only."
##
## ACCEPTANCE GATE FAILURE HISTORY (for debugging):
##   Results with sharpe > 2.3494 that were NOT accepted as new_best:
##     Gen 4183: sharpe=2.3521, trades=1263, win_rate=40.1% — tagged "discarded"
##     Gen 4188: sharpe=2.3521, trades=1263, win_rate=40.1% — tagged "discarded"
##     Gen 4194: sharpe=2.3521, trades=1263, win_rate=40.1% — tagged "discarded"
##     Gen 5182: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##     Gen 5185: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##     Gen 5198: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##     Gen 5200: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##   Total confirmed acceptance failures: 7 (minimum — may be more between Gen 3340–4181)
##   The 2.3513 results appear to be a stable attractor ABOVE the current champion.
##   The parameter producing 2.3513 reliably is likely a minor variation from champion.
##   If the acceptance gate were working: the true champion would be 2.3521 (or 2.3513).
##
## HYPOTHESIS MATRIX (for Step Z debugging):
##   HYPOTHESIS A: Silent champion update occurred post-Gen-3340.
##     Storage holds a YAML with sharpe=2.3521 or 2.3513.
##     The improvement log was not updated when storage was updated.
##     → If true: real champion is not 2.3494. Log is broken.
##   HYPOTHESIS B: Acceptance gate compares against wrong baseline.
##     Gate may be comparing incoming sharpe against stale YAML's backtest result
##     (~0.77, the rsi_period=24 result) rather than stored champion sharpe (2.3494).
##     → If true: gate would accept almost anything above 0.77, which contradicts
##       the observed discards. This hypothesis is weaker.
##   HYPOTHESIS C: Acceptance gate compares against a hardcoded threshold
##     that is higher than 2.3521 (e.g., a manually set target or corrupted float).
##     → If true: no result will ever be accepted without a code fix.
##   HYPOTHESIS D: The 2.3513 results are exact champion clones (same YAML as stored
##     champion, same parameters) and are being correctly rejected as duplicates.
##     → If true: the acceptance gate is working, but clone detection is misclassifying
##       clones as "discarded" instead of "clone" for logging clarity.
##     → This would mean the true champion IS the YAML producing 2.3513, and storage
##       is already updated, but the improvement log shows 2.3494 due to a log bug.
##     → This is actually the MOST LIKELY hypothesis given the consistency of 2.3513.
##   RECOMMENDATION: Hypothesis D should be tested first in Step Z.
##     If stored YAML reproduces 2.3513 (not 2.3494): champion is 2.3513, log is wrong.
##     Fix the log. Update all references. This resolves the anomaly cleanly.
##
## ─────────────────────────────────────────────────────────
## STEP Z — CHAMPION STORAGE AUDIT (MANDATORY BEFORE Gen 5201)
##
##   Z1: Query champion storage directly.
##       What YAML file is stored as champion? Load it. Hash it.
##       What is the stored sharpe value (if logged separately)?
##       Log: "Z1 result: champion_file=[PATH], hash=[HASH], stored_sharpe=[VALUE]."
##
##   Z2: Re-run the stored champion YAML with zero changes.
##       Record: sharpe, trades, win_rate.
##       Log: "Z2 result: backtested sharpe=[X], trades=[Y], win_rate=[Z]."
##       If backtested sharpe = 2.3513: Hypothesis D is confirmed.
##         → The true champion produces 2.3513. The log shows 2.3494 (stale/wrong).
##         → Log: "Z2: HYPOTHESIS D CONFIRMED. True champion sharpe=2.3513."
##         → Update improvement log: add entry for true champion with correct sharpe.
##         → Update confirmed_champion_sharpe = 2.3513 throughout this document.
##       If backtested sharpe = 2.3494: champion storage matches log.
##         → Acceptance gate is failing to promote genuinely better results.
##         → Hypothesis A, B, or C must be investigated via code inspection.
##         → Log: "Z2: Champion confirmed at 2.3494. Acceptance gate is broken."
##       If backtested sharpe = 2.3521: champion storage is ahead of log.
##         → Log: "Z2: HYPOTHESIS A CONFIRMED. True champion sharpe=2.3521."
##         → Update improvement log accordingly.
##       If backtested sharpe differs from all above by > 0.001:
##         → HALT. Log: "Z2: UNEXPECTED CHAMPION SHARPE=[X]. Cannot proceed."
##
##   Z3: From stored champion YAML, read exact values of:
##       - rsi_short_threshold → record as confirmed_rsi_short
##       - take_profit_pct → record as confirmed_TP
##       - all other parameters (verify against known values above)
##       Log: "Z3: confirmed_rsi_short=[X], confirmed_TP=[Y], all params=[LIST]."
##       If any "certain" parameter differs from stored value: HALT and investigate.
##
##   Z4: Identify what YAML was submitted at Gen 4183 (producing sharpe=2.3521).
##       Retrieve from generation log or backtest input archive.
##       Compare parameter diff against stored champion YAML.
##       Log: "Z4: Gen-4183 diff from champion: [PARAM]=[VALUE] vs [CHAMPION_VALUE]."
##       If diff is empty (no difference): confirms Hypothesis D variant — same YAML
##         produces 2.3521 sometimes and 2.3513 other times (backtest noise).
##         Log: "Z4: Gen-4183 is champion clone. 2.3521 vs 2.3513 is backtest variance."
##       If diff shows one parameter change: this is a candidate better champion.
##         Test it explicitly (see Z5).
##
##   Z5: If Z4 shows a parameter diff: re-run Gen-4183 YAML explicitly.
##       If result ≥ 2.3521 (within ±0.001): accept as new champion immediately.
##       Update storage, log, hash, and all references in this document.
##       Log: "Z5: Gen-4183 YAML re-confirmed at sharpe=[X]. Champion updated."
##
##   Z6: Inspect acceptance gate source code.
##       Identify the comparison logic: what value is the incoming sharpe compared against?
##       Identify what triggers "new_best" vs "discarded" vs "new_elite".
##       Log: "Z6: Acceptance gate compares against [SOURCE/VALUE]."
##       Log: "Z6: 'new_elite' definition: [DEFINITION]."
##       If gate compares against anything other than the stored champion sharpe: FIX IT.
##       If "new_elite" is a tier that should promote to champion but doesn't: FIX IT.
##       After fix: re-run A0.5 (acceptance gate self-test) to confirm fix works.
##
##   Z7: Inspect clone detection source code.
##       Identify why identical results across generations are not being caught.
##       (5189=5187, 5191=5190, 5196=5197 are exact duplicates — not caught.)
##       Fix clone detection to catch exact parameter duplicates before backtest.
##       Log: "Z7: Clone detection fix applied: [DESCRIPTION]."
##
##   Z8: Confirm Step Z completion.
##       Log: "STEP Z COMPLETE. True champion sharpe=[X], YAML hash=[Y]."
##       If any Z step could not be completed: HALT.
##       Log: "STEP Z FAILED at step Z[N]: [REASON]. Halting Gen 5201."
##
## ─────────────────────────────────────────────────────────
## PHASE A0 — INFRASTRUCTURE SELF-TESTS (immediately after Step Z)
##
##   All 6 checks must PASS before any generation proceeds.
##   A single FAIL → HALT. Fix. Re-run all of A0 from A0.1.
##   Do NOT escalate to LOKI. Fix directly in ODIN codebase.
##
##   A0.1: Load confirmed champion YAML from storage (post Step Z). Verify hash.
##         Submit with ZERO parameter changes.
##         Expected result: matches confirmed champion sharpe/trades/win_rate exactly.
##         Tolerance: ±0.0005 sharpe, ±2 trades.
##         If result differs beyond tolerance: HALT.
##         Log: "A0.1: [PASS/FAIL]. Result: sharpe=[X], trades=[Y], win_rate=[Z]."
##
##   A0.2: From confirmed storage YAML, log exact values:
##         - rsi_short_threshold → confirmed_rsi_short = [VALUE]
##         - take_profit_pct → confirmed_TP = [VALUE]
##         Replace ALL [CONFIRM_*] tokens and estimated values throughout this document.
##         Log: "A0.2: confirmed_rsi_short=[X], confirmed_TP=[Y]."
##
##   A0.3: Verify fingerprint/clone-detection system is active.
##         Inject A0.1 champion YAML → must be REJECTED as clone BEFORE submission.
##         If NOT rejected: fingerprint system broken → HALT.
##         Also verify: the zombie results from Gens 5187/5189 (identical parameters)
##         would be caught and only the first submitted. If not: fix clone detection.
##         Log: "A0.3: [PASS/FAIL]. Clone detection active for champion and zombie clones."
##
##   A0.4: Verify zombie pre-rejection is active.
##         Construct YAML with rsi_long=50, rsi_short=55 (known zombie params).
##         Submit to pre-backtest validator → must be REJECTED on RSI range check.
##         Also test: YAML with rsi_period_hours=24 → must be flagged as stale-YAML-attractor.
##         If NOT rejected: RSI validation broken → HALT.
##         Log: "A0.4: [PASS/FAIL]. Zombie rejection and stale-YAML detection active."
##
##   A0.5: Verify acceptance gate is functioning.
##         Construct synthetic result: sharpe=confirmed_champion_sharpe + 0.01,
##         trades=1265, win_rate=40.1%.
##         Feed to acceptance logic (dry-run, no backtest submission).
##         Must be accepted as new_best. If NOT accepted → acceptance gate broken → HALT.
##         Also test: sharpe=confirmed_champion_sharpe - 0.01 → must NOT be accepted.
##         Log: "A0.5: [PASS/FAIL]. Acceptance gate correctly accepts/rejects."
##
##   A0.6: Resolve "new_elite" category.
##         If "new_elite" is defined in codebase: document exact definition.
##         If it should trigger champion update but doesn't: fix promotion gate.
##         If it is a valid sub-champion tier (top-N non-champion): document and accept.
##         After any fix: re-run A0.5 to confirm acceptance gate still works.
##         Log: "A0.6: new_elite=[DEFINITION]. Action: [NONE/FIX APPLIED]."
##
##   A0.7 (NEW): Verify MIN_TRADES pre-backtest enforcement.
##         Construct YAML that historically produces trades=190 (zombie attractor).
##         Submit to pre-backtest validator → must be REJECTED before backtest runs.
##         If backtest runs anyway and result is tagged low_trades post-run: FAIL.
##         Pre-rejection must happen BEFORE backtest, not after.
##         Log: "A0.7: [PASS/FAIL]. MIN_TRADES enforced pre-backtest."
##
##   A0.8 (NEW): Verify stale YAML detection.
##         Construct YAML with rsi_period_hours=24, timeout_hours=176, TP=4.65, SL=1.92
##         (the stale YAML values). Submit to pre-backtest validator.
##         Must be REJECTED as stale-YAML-derived submission.
##         If NOT rejected: stale YAML contamination will continue → HALT.
##         Log: "A0.8: [PASS/FAIL]. Stale YAML fingerprint rejected."
##
##   Do NOT proceed to Phase A1 until ALL of A0.1–A0.8 are PASS.
##
## ─────────────────────────────────────────────────────────
## MANDATORY HALT CONDITIONS (check before EVERY generation):
##
##   HALT-1: Grid scan mode active AND proposed test does not match
##            the next pre-specified grid test exactly (verified by parameter diff).
##            → HALT. Log: "GRID DEVIATION at Gen XXXX."
##
##   HALT-2: Three or more of the last 20 results are exact champion clones
##            (same parameters as confirmed champion, not just same sharpe).
##            → HALT. Log: "CLONE FLOOD at Gen XXXX."
##
##   HALT-3: Five or more of the last 20 results are low-trade zombies (<400 trades).
##            → HALT. Log: "ZOMBIE FLOOD at Gen XXXX."
##            [Gen 5200: 7/20 zombies = 35%. THIS CONDITION IS MET. HALT-3 TRIGGERED.]
##            [This halt was not caught at Gen 5200. It must be enforced at Gen 5201.]
##
##   HALT-4: Step Z has not been completed and Gen 5201 is about to start.
##            → HALT. Log: "STEP Z INCOMPLETE. Cannot start Gen 5201."
##
##   HALT-5: A0.1–A0.8 have not all passed and Phase A1 is about to start.
##            → HALT. Log: "A0 INCOMPLETE. Cannot start Phase A1."
##
##   HALT-6: A result with sharpe > confirmed_champion_sharpe is tagged anything
##            other than "new_best" (including "discarded", "new_elite", or any other tag).
##            → HALT IMMEDIATELY.
##            Log: "ACCEPTANCE GATE FAILURE at Gen XXXX.
##              Result sharpe=[X] > champion sharpe=[Y] but tagged [TAG]."
##            This condition was met at Gens 4183, 4188, 4194, 5182, 5185, 5198, 5200.
##            It was not caught any of those times. It MUST be caught going forward.
##
##   HALT-7 (NEW): Three or more identical results (exact sharpe + trades + win_rate)
##            appear across the last 20 generations.
##            → HALT. Log: "DUPLICATE RESULT FLOOD at Gen XXXX."
##            [Gen 5200: 2.3513/1265 appears 4 times (5182,5185,5198,5200). TRIGGERED.]
##            [Zombie duplicates also present (5187=5189, 5190=5191, 5196=5197). TRIGGERED.]
##
##   HALT-8 (NEW): ODIN cannot construct a deterministic YAML from storage
##            without invoking the LLM.
##            → HALT PERMANENTLY.
##            Log: "CAPABILITY GAP: Cannot execute deterministic grid without LLM.
##              1,400 generations of grid-scan non-execution documented.
##              LLM loop has produced zero improvements in 1,860 generations.
##              System cannot improve without deterministic grid capability.
##              Halting permanently. Human intervention required."
##
##   "HALT" means: stop all generation loops immediately.
##   Do not start Gen N+1. Output halt condition to run log.
##   Wait for human operator review.
##   Do NOT escalate to LOKI under any circumstances.
##   Do NOT resume automatically.
##
## ─────────────────────────────────────────────────────────
## LLM LOOP STATUS: SUSPENDED
##
##   The LLM generation loop is SUSPENDED until further notice.
##   Conditions for reinstatement:
##     1. Step Z complete with confirmed true champion.
##     2. A0.1–A0.8 all PASS.
##     3. HALT-3 condition (zombie flood) resolved by pre-rejection fixes.
##     4. HALT-7 condition (duplicate flood) resolved by clone detection fixes.
##     5. The displayed YAML has been corrected to show true champion parameters.
##     6. Grid scan (Phase A1 through completion) has been attempted and exhausted.
##   Until all 6 conditions are met: LLM loop does NOT run.
##   Running LLM generations from corrupted YAML input for 3,608 generations
##   has produced zero improvements since Gen 3340 and has consumed 1,860
##   backtest slots that could have been used for the grid scan.
##   The LLM loop in its current form is actively harmful to research progress.
##
##   IF LLM LOOP IS REINSTATED (after all conditions above are met):
##   The LLM must receive the CORRECT champion YAML — loaded from storage,
##   not from the displayed YAML. The displayed YAML must be fixed or suppressed.
##   Attractor guard must reject any proposal matching known attractor fingerprints:
##     - rsi_period=24 (stale YAML contamination source)
##     - rsi_long≈50, rsi_short≈55 (zombie attractor)
##     - sharpe≈0.6621/trades≈1042 fingerprint
##     - sharpe≈-9.018/trades≈28 fingerprint (extreme zombie)
##     - sharpe≈1.3815/trades≈969 fingerprint
##     - sharpe≈-1.0406/trades≈190 fingerprint (new zombie attractor, 4× in last 20)
##     - sharpe≈-0.8033/trades≈178 fingerprint (