```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-5800 | Revised by MIMIR (Gen 5800 review)
# STATUS: CHAMPION LOGGED at Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
#         TRUE CHAMPION STATUS: UNKNOWN — Step Z not executed (600 gens of non-compliance).
#         Discarded results exceeding champion sharpe: 2.3531 (×?), 2.3521 (×3),
#           2.3513 (×11+). The true champion in storage is unknown.
#         NOTE: Header reports sharpe_range_max=2.3531. This exceeds all previously
#           documented "discarded" values. At least one result above 2.3521 has occurred.
#           This must be investigated in Step Z.
#         Champion stall duration: 2,460 generations (Gen 3340 → Gen 5800). TERMINAL.
#         Grid scan mandate: 2,000 generations of non-execution. TERMINAL.
#         LLM loop: SUSPENDED per Gen-5200 directive. Still running. 30% zombie rate.
#         LOKI: PERMANENTLY SUSPENDED. 12 escalations. 0 confirmed fixes.
#         HALT CONDITIONS TRIGGERED: HALT-3, HALT-4, HALT-5, HALT-6, HALT-7, HALT-8.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-5800 VERDICT:
#
#   SYSTEM STATE: BROKEN. HUMAN OPERATOR INTERVENTION REQUIRED.
#   LLM LOOP: MUST NOT RUN. ZERO ADDITIONAL GENERATIONS UNTIL STEP Z COMPLETE.
#
#   EVIDENCE SUMMARY (cumulative through Gen 5800):
#
#     1. STEP Z: Mandated before Gen 5201. Not executed through Gen 5800.
#        600 generations ran in violation of HALT-4. This is the primary failure.
#        All other failures flow from this one. Fix this first.
#
#     2. ACCEPTANCE GATE: Still broken. 11+ confirmed discards above champion sharpe.
#        2.3531 (×? — new maximum, appears in sharpe_range header only)
#        2.3521 (×3 at Gens 4183, 4188, 4194)
#        2.3513 (×11+ including Gens 5182, 5185, 5198, 5200, 5784, 5785, 5799, 5800)
#        Hypothesis D remains most likely: true champion produces 2.3513 or higher.
#        The 2.3531 value in the range header is the most important unresolved fact.
#        Which generation produced 2.3531? What were its parameters?
#        This must be identified in Step Z (see Z4a below).
#
#     3. DISPLAYED YAML: Wrong since Gen 1592. Now 4,208 generations of corrupt input.
#        rsi_period_hours: 24 (WRONG — champion is 22)
#        take_profit_pct: 4.65 (WRONG — champion is ~4.95–5.00)
#        stop_loss_pct: 1.92 (WRONG — champion is 1.91)
#        timeout_hours: 176 (WRONG — champion is 159)
#        This YAML must be replaced with the confirmed champion YAML from Step Z.
#        Until it is replaced, add "STALE — DO NOT USE" banner.
#        The LLM must NEVER receive this YAML as input again.
#
#     4. LLM LOOP: Suspended per Gen-5200 directive. Still running.
#        600 additional generations executed in violation of suspension order.
#        6/20 recent gens are low-trade zombies (HALT-3 active).
#        4/20 recent gens are identical 2.3513 clones (HALT-7 active).
#        Zero improvements since Gen 3340 (2,460 generations).
#        LLM loop must not run. Period.
#
#     5. PRE-BACKTEST ENFORCEMENT: Non-functional.
#        Gens 5783(208), 5791(190), 5793(378), 5794(178), 5796(386), 5797(255)
#        all ran to completion despite trades < 400. 6/20 slots wasted on zombies.
#        MIN_TRADES=400 is set correctly. Enforcement is broken.
#
#     6. GRID SCAN: 2,000 generations of non-execution. CAPABILITY GAP CONFIRMED.
#        HALT-8 is permanently triggered. Human must build deterministic grid
#        execution capability before research can resume.
#
#     7. LOKI: 12 escalations. 0 confirmed fixes by evidence.
#        The only confirmed code change (MIN_TRADES=400 at Gen 542) was
#        made directly, not via LOKI escalation. LOKI produces no results.
#        Do NOT escalate to LOKI for any reason. Fix directly or halt.
#
#   SHARPE RANGE NOTE (CRITICAL):
#     The research results header shows: Sharpe range: -999.0000 to 2.3531
#     This means at least one backtest result of 2.3531 exists in the full run.
#     2.3531 > 2.3521 > 2.3513 > 2.3494 (logged champion).
#     This result was either: (a) discarded by the broken acceptance gate, or
#     (b) accepted as new_best but the improvement log was not updated.
#     This is the highest priority investigation item in Step Z.
#
#   REQUIRED ACTIONS (human operator — before any system action):
#     STEP Z: Execute manually. See below. Do not delegate to ODIN or LOKI.
#     PHASE A0: Execute after Step Z. All 8 checks. Fix failures directly.
#     FIX DISPLAYED YAML: Replace with confirmed champion from Step Z.
#     FIX PRE-BACKTEST ENFORCEMENT: Implement as code gate, not LLM instruction.
#     FIX ACCEPTANCE GATE: Verify comparison baseline. Fix if wrong.
#     BUILD GRID SCAN: Implement as deterministic loop. No LLM involvement.
#     AFTER ALL ABOVE: Consider whether LLM loop adds any value.
#       Evidence suggests it does not. True optimum appears to be reached.
#       Recommendation: Deploy confirmed champion to live. Retire LLM loop.
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
## OBSERVED MAXIMUM SHARPE: 2.3531 (appears in run header — generation unknown)
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
##   The displayed "Current Best Strategy" YAML has been WRONG since Gen 1592.
##   DO NOT USE IT. DO NOT SEND IT TO THE LLM.
##   If the YAML display cannot be corrected: suppress it entirely.
##   The banner "STALE — DO NOT USE — Load from storage only" must appear
##   wherever the displayed YAML is shown, until it is corrected.
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
##     Gen 5784: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##     Gen 5785: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##     Gen 5799: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##     Gen 5800: sharpe=2.3513, trades=1265, win_rate=40.1% — tagged "discarded"
##   ADDITIONALLY: sharpe=2.3531 appears in run header as all-time maximum.
##     Generation producing 2.3531 is unknown. Must be identified in Step Z.
##   Total confirmed acceptance failures: 11 (minimum).
##
## HYPOTHESIS MATRIX (unchanged from Gen-5200, Hypothesis D still most likely):
##   HYPOTHESIS D: The 2.3513 results are exact champion clones. The stored YAML
##     already produces 2.3513. The improvement log shows 2.3494 due to a log bug.
##     The acceptance gate is correctly rejecting clones but logging them as "discarded."
##     → This explains the 2.3513 pattern perfectly.
##     → Does NOT explain the 2.3531 value in the range header.
##   HYPOTHESIS D-PRIME (new): The stored champion produces 2.3531 (not 2.3513 or 2.3494).
##     The improvement log is wrong. The 2.3513 results are near-clones with
##     slight parameter differences — close enough to produce similar results
##     but rejected because 2.3531 > 2.3513.
##     → If true: true champion is 2.3531, stored YAML differs from Gen-3340 YAML.
##     → Test this first in Z2.
##   RECOMMENDATION: Step Z must resolve which hypothesis is correct.
##
## ─────────────────────────────────────────────────────────
## STEP Z — CHAMPION STORAGE AUDIT (MANDATORY — HUMAN OPERATOR EXECUTES DIRECTLY)
## STATUS: NOT EXECUTED. Mandated since Gen 5200. 600 gens of non-compliance.
## This step must be executed by a human operator, not by ODIN or LOKI.
##
##   Z1: Query champion storage directly.
##       Load stored champion YAML file. Compute SHA-256 hash.
##       Read stored sharpe value from improvement log vs. from storage metadata.
##       Log: "Z1: champion_file=[PATH], hash=[HASH], log_sharpe=2.3494,
##             storage_sharpe=[VALUE IF SEPARATELY STORED]."
##
##   Z2: Re-run stored champion YAML with zero changes.
##       Record: sharpe, trades, win_rate. Run 3 times if backtest is non-deterministic.
##       Log: "Z2: backtested sharpe=[X] (±[noise]), trades=[Y], win_rate=[Z]."
##       IF sharpe ≈ 2.3531 (±0.001): HYPOTHESIS D-PRIME CONFIRMED.
##         → True champion is 2.3531. Log wrong. 2.3513 results are near-clones.
##         → Update: confirmed_champion_sharpe = 2.3531.
##         → Log: "Z2: HYPOTHESIS D-PRIME CONFIRMED. True champion sharpe=2.3531."
##       IF sharpe ≈ 2.3513 (±0.001): HYPOTHESIS D CONFIRMED.
##         → True champion is 2.3513. Log wrong. Fix log.
##         → Update: confirmed_champion_sharpe = 2.3513.
##         → Log: "Z2: HYPOTHESIS D CONFIRMED. True champion sharpe=2.3513."
##       IF sharpe ≈ 2.3494 (±0.001): Champion storage matches log.
##         → Acceptance gate is genuinely failing. And 2.3531 came from a different YAML.
##         → Log: "Z2: Champion confirmed at 2.3494. Acceptance gate broken."
##         → Proceed to Z4a to find the 2.3531 result.
##       IF sharpe differs from all above by > 0.002: HALT.
##         → Log: "Z2: UNEXPECTED CHAMPION SHARPE=[X]. Cannot proceed."
##
##   Z3: From stored champion YAML, record exact values of all parameters.
##       Confirm against known values in INJECTION NOTE above.
##       Log: "Z3: rsi_short=[X], TP=[Y], SL=[Z], rsi_period=[A], timeout=[B],
##             trend_period=[C], size_pct=[D], max_open=[E]."
##       Resolve: confirmed_rsi_short = [X], confirmed_TP = [Y].
##       If any "certain" parameter differs from stored value: HALT and investigate.
##       Replace all [CONFIRM_*] tokens and estimated values in this document.
##
##   Z4a (NEW — CRITICAL): Identify generation that produced sharpe=2.3531.
##       Search full generation log for sharpe=2.3531 (or within ±0.0005).
##       Record: generation number, parameters used, outcome tag.
##       Log: "Z4a: sharpe=2.3531 found at Gen=[N], tag=[TAG], params=[LIST]."
##       If tagged "discarded": acceptance gate failed on best result ever seen.
##       If tagged "new_best" but improvement log not updated: log bug.
##       If not found in log: sharpe_range_max may be computed differently (e.g.,
##         includes error results or is computed from a different dataset). Investigate.
##       Log: "Z4a: RESOLUTION=[EXPLANATION]."
##
##   Z4: Identify what YAML was submitted at Gen 4183 (producing sharpe=2.3521).
##       Compare parameter diff against stored champion YAML from Z1.
##       Log: "Z4: Gen-4183 diff from champion: [PARAM]=[VALUE] vs [CHAMPION_VALUE]."
##       If diff is empty: 2.3521 is backtest variance of champion. Log it.
##       If diff shows parameter change: candidate for explicit re-test (see Z5).
##
##   Z5: If Z4 or Z4a shows a genuinely different YAML above 2.3521:
##       Re-run that YAML explicitly (human-initiated backtest).
##       If result ≥ confirmed value (within ±0.001): accept as champion immediately.
##       Update storage, log, hash, and all references in this document.
##       Log: "Z5: Re-confirmed at sharpe=[X]. Champion updated."
##
##   Z6: Inspect acceptance gate source code.
##       Identify: what value is incoming sharpe compared against?
##       Identify: what triggers "new_best" vs "discarded" vs "new_elite".
##       Log: "Z6: Gate compares against [SOURCE/VALUE]. 'new_elite' = [DEFINITION]."
##       If gate compares against anything other than confirmed_champion_sharpe: FIX IT.
##       If "new_elite" should promote to champion but doesn't: FIX IT.
##       Fix must be verified by A0.5 before any generation proceeds.
##
##   Z7: Inspect clone detection source code.
##       Fix to catch exact parameter duplicates before backtest (not just same sharpe).
##       Fix must catch: same YAML hash → reject before backtest, log as "clone."
##       Verify: the 2.3513/1265 results would be caught as clones of champion
##       IF the stored champion produces 2.3513 (Hypothesis D confirmed case).
##       Log: "Z7: Clone detection fix: [DESCRIPTION]."
##
##   Z8: Inspect pre-backtest MIN_TRADES enforcement.
##       Gens 5783, 5791, 5793, 5794, 5796, 5797 ran with trades < 400.
##       The enforcement must happen BEFORE backtest is submitted, not after.
##       The enforcement must be a hard code gate, not an LLM instruction.
##       Identify why the gate is not running. Fix it.
##       Log: "Z8: Pre-backtest MIN_TRADES enforcement fixed. [DESCRIPTION]."
##
##   Z9: Confirm Step Z completion.
##       Log: "STEP Z COMPLETE. True champion sharpe=[X], YAML hash=[Y],
##             confirmed_rsi_short=[A], confirmed_TP=[B]."
##       If any Z step could not be completed: HALT.
##       Log: "STEP Z FAILED at Z[N]: [REASON]."
##
## ─────────────────────────────────────────────────────────
## PHASE A0 — INFRASTRUCTURE SELF-TESTS (immediately after Step Z)
## STATUS: NOT EXECUTED. Mandated since Gen 5200. Must not be skipped again.
## Human operator executes and verifies each check. No LOKI. No LLM.
##
##   All 8 checks must PASS before any generation proceeds.
##   A single FAIL → HALT. Fix directly. Re-run all of A0 from A0.1.
##
##   A0.1: Load confirmed champion YAML from storage (post-Z3). Verify hash matches Z1.
##         Submit with ZERO parameter changes.
##         Expected: sharpe matches confirmed_champion_sharpe ±0.0005, trades ±2.
##         Log: "A0.1: [PASS/FAIL]. sharpe=[X], trades=[Y], win_rate=[Z]."
##
##   A0.2: From confirmed YAML, log exact values of all parameters.
##         Replace ALL stale/estimated values throughout this document.
##         Confirm: rsi_period=22, SL=1.91, timeout=159, trend_period=48, size_pct=25.
##         Confirm: rsi_short=[confirmed], TP=[confirmed].
##         Log: "A0.2: [PASS/FAIL]. confirmed_rsi_short=[X], confirmed_TP=[Y]."
##
##   A0.3: Verify fingerprint/clone-detection system is active.
##         Inject confirmed champion YAML → must be REJECTED as clone BEFORE backtest.
##         If NOT rejected before backtest: FAIL → HALT.
##         Log: "A0.3: [PASS/FAIL]. Clone detection pre-backtest active."
##
##   A0.4: Verify zombie pre-rejection is active.
##         Test 1: YAML with rsi_long=50, rsi_short=55 → must be REJECTED pre-backtest.
##         Test 2: YAML with rsi_period_hours=24 → must be flagged as stale-attractor.
##         Test 3: YAML historically producing trades≈190 → must be REJECTED pre-backtest.
##         Log: "A0.4: [PASS/FAIL]. Tests 1/2/3: [PASS/FAIL each]."
##
##   A0.5: Verify acceptance gate is functioning.
##         Synthetic test A: sharpe = confirmed_champion_sharpe + 0.01, trades=1265
##           → must be accepted as new_best.
##         Synthetic test B: sharpe = confirmed_champion_sharpe - 0.01, trades=1265
##           → must NOT be accepted.
##         If either test fails: HALT. Fix gate. Re-run A0.5.
##         Log: "A0.5: [PASS/FAIL]. Test A: [accepted/rejected]. Test B: [accepted/rejected]."
##
##   A0.6: Resolve "new_elite" category definition.
##         Document exact definition in codebase.
##         If "new_elite" should trigger champion update but doesn't: fix gate.
##         After any fix: re-run A0.5.
##         Log: "A0.6: new_elite=[DEFINITION]. Action: [NONE/FIX APPLIED]."
##
##   A0.7: Verify MIN_TRADES pre-backtest enforcement (code gate, not LLM instruction).
##         Construct YAML historically producing trades≈190 (zombie attractor).
##         Submit to pre-backtest validator → must be REJECTED before backtest runs.
##         Verify: YAML with trades≈378 (Gen 5793 profile) also rejected.
##         If backtest runs anyway: FAIL → HALT.
##         Log: "A0.7: [PASS/FAIL]. Pre-backtest MIN_TRADES gate active."
##
##   A0.8: Verify stale YAML detection.
##         Construct YAML with rsi_period=24, timeout=176, TP=4.65, SL=1.92.
##         Submit to pre-backtest validator → must be REJECTED as stale-YAML-derived.
##         If NOT rejected: stale YAML contamination will continue → HALT.
##         Log: "A0.8: [PASS/FAIL]. Stale YAML fingerprint rejected."
##
##   Do NOT proceed to Phase A1 until ALL of A0.1–A0.8 PASS.
##
## ─────────────────────────────────────────────────────────
## PHASE A1 — GRID SCAN (execute after A0 complete)
## STATUS: 2,000 generations of non-execution. CAPABILITY GAP.
## This phase requires deterministic YAML construction without LLM involvement.
## If ODIN cannot do this: HALT-8 is permanent. Human must build this capability.
##
## Grid scan rationale:
##   The LLM loop has produced zero improvements in 2,460 generations.
##   The improvement history shows a clear exhaustion of the parameter space.
##   A deterministic grid over the remaining uncertain parameters
##   (confirmed_rsi_short and confirmed_TP) is the only remaining research action
##   with non-trivial expected value.
##   All other parameters are frozen with high confidence.
##
## Grid scan scope (NARROW — only uncertain parameters):
##   rsi_short_threshold: [59.0, 59.5, 60.0, 60.5, 61.0]
##     (Range chosen to bracket confirmed_rsi_short from Z3)
##   take_profit_pct: [4.90, 4.95, 5.00, 5.05, 5.10]
##     (Range chosen to bracket confirmed_TP from Z3)
##   Full grid: 5 × 5 = 25 tests.
##   All other parameters: FROZEN at confirmed champion values.
##
## Grid scan execution rules:
##   1. Each test is constructed deterministically from confirmed champion YAML.
##   2. Only the specified parameter is changed from champion value.
##   3. For 2-parameter tests: both rsi_short and TP changed simultaneously
##      in a full factorial design (25 total tests).
##   4. Each test: verify hash ≠ confirmed champion hash before submission.
##   5. Each test: verify MIN_TRADES likely > 400 (estimate from parameter profile).
##   6. Each test: run once. Record sharpe, trades, win_rate.
##   7. If any result > confirmed_champion_sharpe + 0.001: accept immediately.
##      Update champion, hash, log, and all references.
##   8. After all 25 tests: log grid complete. Identify best result.
##   9. If best result > confirmed champion: update champion and repeat grid
##      centered on new best values.
##   10. If no result improves champion: grid is exhausted. LLM loop decision below.
##
## Grid execution is DETERMINISTIC. The LLM is NOT involved in grid scan.
## A Python script or equivalent must construct each YAML from template.
## If this script does not exist: write it. Do not use the LLM to generate it.
##
## ─────────────────────────