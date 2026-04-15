```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6000 | Revised by MIMIR (Gen 6000 review)
#
# ══════════════════════════════════════════════════════════════════
# STATUS BLOCK — READ THIS FIRST. READ ALL OF IT.
# ══════════════════════════════════════════════════════════════════
#
# LLM LOOP STATUS:   ██ HARD STOP ██  DO NOT RUN ANY GENERATIONS.
# STEP Z STATUS:     NOT EXECUTED. Mandated since Gen 5200. Now 800 gens overdue.
# GRID SCAN STATUS:  NOT EXECUTED. Mandated since Gen 4000. 2,200 gens overdue.
# LOKI STATUS:       PERMANENTLY RETIRED. 12 escalations. 0 confirmed fixes.
#                    Do not escalate to LOKI for any reason.
#
# CHAMPION (logged):      Gen 3340 | sharpe=2.3494 | trades=1265 | win_rate=40.1%
# CHAMPION (true):        UNKNOWN — Step Z required.
# OBSERVED MAX SHARPE:    2.3531 (run header) — generation unknown.
# STALL DURATION:         2,660 generations (Gen 3340 → Gen 6000). TERMINAL.
#
# CRITICAL BUG — HIGHEST PRIORITY:
#   MIN_TRADES constant in live system = 50 (not 400).
#   The LOKI change at Gen 542 did not persist in the running code.
#   This is the root cause of all zombie generation waste.
#   FIX THIS BEFORE ANY OTHER ACTION.
#   Verification: after fix, confirm running value = 400 by inspection.
#   Then confirm a YAML producing ~190 trades is rejected pre-backtest.
#
# ACCEPTANCE GATE FAILURES (confirmed):
#   11+ results above logged champion sharpe were tagged "discarded":
#     2.3531 (×unknown — run header max — generation unknown)
#     2.3521 (×3: Gens 4183, 4188, 4194)
#     2.3513 (×8+: Gens 5182, 5185, 5198, 5200, 5784, 5785, 5799, 5800,
#                   5983, and counting)
#
# STALE YAML (PERMANENT WARNING — DO NOT USE — DO NOT SEND TO LLM):
#   The "Current Best Strategy" YAML displayed below is WRONG.
#   Wrong since Gen 1592. Now 4,408 generations of corrupt LLM input.
#   Known wrong values:
#     rsi_period_hours:  24   → correct value: 22
#     take_profit_pct:   4.65 → correct value: ~4.95–5.00 (confirm in Step Z)
#     stop_loss_pct:     1.92 → correct value: 1.91
#     timeout_hours:     176  → correct value: 159
#   THE LLM MUST NEVER RECEIVE THIS YAML AS INPUT AGAIN.
#   After Step Z: replace this YAML with confirmed champion YAML.
#   Until then: suppress or display with STALE banner only.
#
# HALT CONDITIONS ACTIVE:
#   HALT-3: Zombie generation rate (low_trades) — 9/20 recent gens.
#   HALT-4: LLM loop running after suspension order (600+ gens past directive).
#   HALT-5: Stale YAML contaminating LLM input (4,408 gens).
#   HALT-6: Acceptance gate broken (11+ confirmed discards above champion).
#   HALT-7: Clone convergence (2.3513 repeating, not being caught pre-backtest).
#   HALT-8: Grid scan not executed (2,200+ gens of non-execution).
#   HALT-9 (NEW): MIN_TRADES live constant = 50, not 400. Pre-backtest gate broken.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-6000 VERDICT
# ══════════════════════════════════════════════════════════════════
#
# SYSTEM STATE: BROKEN. ALL AUTOMATED LOOPS MUST BE STOPPED NOW.
#
# The LLM loop has produced zero improvements in 2,660 generations.
# Recent generations (5981–6000) show: 9 zombies, 10 discards, 0 improvements.
# The pre-backtest MIN_TRADES gate is confirmed non-functional (live value = 50).
# Step Z has not been executed despite 800 generations of mandate.
# The grid scan has not been executed despite 2,200 generations of mandate.
# LOKI has produced zero confirmed fixes in 12 escalations.
#
# THE ONLY CORRECT ACTION SEQUENCE IS:
#
#   IMMEDIATE:
#     [I1] Stop all automated loops. LLM loop, LOKI, everything.
#     [I2] Fix MIN_TRADES live constant: set to 400, verify, test rejection.
#
#   STEP Z (human operator, manual, in order):
#     Z1 → Z2 → Z3 → Z4a → Z4 → Z5 → Z6 → Z7 → Z8 → Z9
#     See Step Z section below. Do not skip steps. Do not delegate.
#
#   PHASE A0 (after Step Z complete):
#     All 8 checks must pass before any generation proceeds.
#     See Phase A0 section below.
#
#   PHASE A1 (after A0 complete):
#     25-cell deterministic grid scan.
#     No LLM involvement. Python script only.
#     See Phase A1 section below.
#
#   AFTER GRID SCAN:
#     If any result improves champion: accept, update, consider second grid pass.
#     If no result improves champion: research is complete.
#     Deploy confirmed champion to live (with TYR position sizing applied).
#     Retire LLM loop permanently.
#
# ASSESSMENT OF LLM LOOP VALUE:
#   Evidence across 6,000 generations strongly suggests the true optimum
#   has been reached (or very closely approached) at sharpe ≈ 2.35.
#   The improvement curve shows clear exponential decay:
#     Gen 1→1477: +1.23 sharpe over 1,477 gens
#     Gen 1477→3340: +0.10 sharpe over 1,863 gens
#     Gen 3340→6000: +0.000 sharpe over 2,660 gens
#   The marginal expected value of additional LLM generations is effectively zero.
#   Recommendation: retire LLM loop after grid scan, regardless of grid outcome.
#
# ══════════════════════════════════════════════════════════════════

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor)
  — ENFORCEMENT: Code gate ONLY. Not LLM instruction. Not LOKI.
  — GATE LOCATION: Pre-backtest validator, before any backtest is submitted.
  — CURRENT STATUS: BROKEN. Live constant = 50. Fix immediately (see I2 above).
  — VERIFICATION: After fix, confirm live constant = 400 by direct inspection.

---
## ██████████████████████████████████████████████████████████
## ODIN INJECTION NOTE (INTERNAL ONLY — NEVER SEND TO LLM)
##
## ─────────────────────────────────────────────────────────
## CHAMPION IDENTITY
##
## LOGGED CHAMPION:    Gen 3340 | sharpe=2.3494 | trades=1265 | win_rate=40.1%
## TRUE CHAMPION:      UNKNOWN — must be resolved by Step Z.
## OBSERVED MAXIMUM:   2.3531 (run header) — generation and params unknown.
##
## HYPOTHESES (ranked by current evidence):
##   D-PRIME (most likely): Stored champion produces sharpe=2.3531.
##     Improvement log is wrong. 2.3513 near-clones rejected correctly.
##     2.3531 result was accepted but log not updated.
##   D (second): Stored champion produces sharpe=2.3513.
##     Log wrong. 2.3513 clones rejected correctly. 2.3531 from different YAML.
##   C (least likely): Champion truly is 2.3494. Gate failing on every result above.
##   → Step Z Z2 resolves this definitively.
##
## KNOWN PARAMETER VALUES (load from storage — do not rely on displayed YAML):
##   rsi_period_hours:    22     (certain — confirmed Gen 2785)
##   rsi_long_threshold:  37.77  (certain — confirmed Gen 1477)
##   rsi_short_threshold: UNKNOWN — confirm in Z3. Range: 59.0–61.0.
##   trend_period_hours:  48     (certain)
##   take_profit_pct:     UNKNOWN — confirm in Z3. Range: 4.90–5.10.
##                        DO NOT USE 4.65 (stale YAML — wrong since Gen 1592).
##   stop_loss_pct:       1.91   (certain — NOT 1.90, NOT 1.92)
##   timeout_hours:       159    (FROZEN FOREVER — NOT 176)
##   size_pct:            25     (FROZEN)
##   max_open:            3      (FROZEN)
##   leverage:            2      (FROZEN)
##   fee_rate:            0.0005 (FROZEN)
##
## AFTER STEP Z: Replace all UNKNOWN values above with confirmed values.
## Token: [CONFIRMED_RSI_SHORT] — replace with Z3 result.
## Token: [CONFIRMED_TP] — replace with Z3 result.
## Token: [CONFIRMED_CHAMPION_SHARPE] — replace with Z2 result.
##
## ─────────────────────────────────────────────────────────
## ACCEPTANCE GATE FAILURE LOG
##
##   Results above logged champion (2.3494) tagged "discarded":
##     Gen 4183: sharpe=2.3521, trades=1263, win_rate=40.1%
##     Gen 4188: sharpe=2.3521, trades=1263, win_rate=40.1%
##     Gen 4194: sharpe=2.3521, trades=1263, win_rate=40.1%
##     Gen 5182: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5185: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5198: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5200: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5784: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5785: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5799: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5800: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 5983: sharpe=2.3513, trades=1265, win_rate=40.1%
##   Total confirmed failures: 12.
##   Plus: sharpe=2.3531 in run header — generation unknown.
##   Root cause: unknown until Z6 inspection.
##
## ─────────────────────────────────────────────────────────
## IMMEDIATE ACTION ITEMS (human operator — before anything else)
##
## [I1] STOP ALL AUTOMATED LOOPS.
##   Stop the LLM generation loop. Stop LOKI. Stop everything.
##   Do not allow any automated system to take any action until Step Z is complete.
##   Reason: every additional generation run before Step Z is wasted compute and
##   additional noise in the research log.
##
## [I2] FIX MIN_TRADES LIVE CONSTANT.
##   The Self-Audit section shows: MIN_TRADES[futures_swing] = 50.
##   The LOKI change at Gen 542 set it to 400, but it did not persist.
##   Action: Locate the actual runtime constant definition in source code.
##     (Not the LOKI change log. The actual file/variable that ODIN reads at runtime.)
##   Action: Set MIN_TRADES[futures_swing] = 400.
##   Action: Restart ODIN (if needed for constant to take effect).
##   Verification A: Inspect live constant at runtime → must read 400.
##   Verification B: Submit YAML historically producing ~190 trades to pre-backtest
##     validator → must be REJECTED before backtest runs.
##   Verification C: Confirm gens 5984, 5986, 5988 profiles would be rejected.
##   Log: "I2: MIN_TRADES[futures_swing] set to 400. Live constant verified = 400.
##         Rejection test: PASS/FAIL."
##   If Verification B FAILS: the pre-backtest gate itself is broken (separate from
##     the constant). Fix the gate code. Do not proceed until both constant and
##     gate are confirmed working.
##
## ─────────────────────────────────────────────────────────
## STEP Z — CHAMPION STORAGE AUDIT
## STATUS: NOT EXECUTED. Mandated since Gen 5200. Now 800 generations overdue.
## EXECUTOR: Human operator only. Not ODIN. Not LOKI.
## PREREQUISITE: I1 and I2 complete.
##
##   Z1: Load champion from storage.
##       Load stored champion YAML file. Compute SHA-256 hash.
##       Read logged sharpe from improvement log (should be 2.3494).
##       Check if storage metadata contains a separate sharpe value.
##       Log: "Z1: file=[PATH], hash=[HASH], log_sharpe=2.3494,
##             metadata_sharpe=[VALUE or NONE]."
##
##   Z2: Re-run stored champion YAML with zero changes.
##       Run 3 times if backtest is non-deterministic.
##       Record: sharpe (mean ± std), trades, win_rate.
##       Log: "Z2: backtested_sharpe=[X ± Y], trades=[Z], win_rate=[W]."
##
##       Interpretation:
##         IF sharpe ≈ 2.3531 (within ±0.001): HYPOTHESIS D-PRIME CONFIRMED.
##           → True champion sharpe = 2.3531. Improvement log is wrong.
##           → confirmed_champion_sharpe = 2.3531.
##           → 2.3513 near-clones were correctly rejected (gate IS working).
##           → Log: "Z2: D-PRIME CONFIRMED. True champion = 2.3531."
##
##         IF sharpe ≈ 2.3513 (within ±0.001): HYPOTHESIS D CONFIRMED.
##           → True champion sharpe = 2.3513. Log shows 2.3494 (log bug).
##           → confirmed_champion_sharpe = 2.3513.
##           → 2.3513 clones correctly rejected. Gate functioning on clones.
##           → 2.3531 came from a different YAML (investigate in Z4a).
##           → Log: "Z2: D CONFIRMED. True champion = 2.3513."
##
##         IF sharpe ≈ 2.3494 (within ±0.001): Log and storage match.
##           → Acceptance gate is genuinely failing on all results above 2.3494.
##           → confirmed_champion_sharpe = 2.3494.
##           → 2.3521 and 2.3531 came from different YAMLs (investigate Z4, Z4a).
##           → Log: "Z2: Champion confirmed at 2.3494. Acceptance gate broken."
##
##         IF sharpe differs from all above by > 0.002: HALT.
##           → Log: "Z2: UNEXPECTED sharpe=[X]. Cannot proceed. HALT."
##
##   Z3: Record all parameter values from stored champion YAML.
##       Compare against known values in INJECTION NOTE above.
##       Log: "Z3: rsi_period=[A], rsi_long=[B], rsi_short=[C], trend_period=[D],
##             TP=[E], SL=[F], timeout=[G], size_pct=[H], max_open=[I]."
##       Resolve: [CONFIRMED_RSI_SHORT] = [C]. [CONFIRMED_TP] = [E].
##       Replace tokens in INJECTION NOTE and PHASE A1 grid with confirmed values.
##       IF any "certain" parameter (rsi_period, rsi_long, SL, timeout) differs
##         from known value: HALT and investigate before proceeding.
##       Log: "Z3: confirmed_rsi_short=[C], confirmed_TP=[E]. All certain params match:
##             [YES/NO — list any discrepancies]."
##
##   Z4a (HIGHEST PRIORITY NEW ITEM): Identify the 2.3531 result.
##       Search full generation log for any result with sharpe ≥ 2.3525.
##       Record: generation number, YAML used, outcome tag.
##       Log: "Z4a: sharpe=2.3531 found at Gen=[N], tag=[TAG], params=[LIST]."
##
##       Interpretation:
##         IF tagged "discarded": acceptance gate failed on the best result ever seen.
##           → Gate comparison baseline is wrong. Fix in Z6.
##         IF tagged "new_best": log not updated when accepted.
##           → This IS the true champion. Its YAML may differ from Gen 3340 YAML.
##           → Compare to stored YAML. If different: that YAML may be the true champion.
##         IF not found in generation log: sharpe_range_max may be computed from
##           a different dataset or include error results coded as extreme values.
##           → Investigate how sharpe_range_max is computed. Document finding.
##       Log: "Z4a: RESOLUTION=[explanation]."
##
##   Z4: Identify YAML used at Gen 4183 (sharpe=2.3521).
##       Compare parameter diff against stored champion YAML from Z1.
##       Log: "Z4: Gen-4183 diff: [PARAM]=[VALUE] vs champion=[CHAMPION_VALUE].
##             OR: Gen-4183 diff: EMPTY (backtest variance of champion)."
##       If diff is non-empty: this is a candidate for Z5 re-test.
##
##   Z5: If Z4 or Z4a reveals a genuinely different YAML that produced sharpe
##       above confirmed_champion_sharpe (from Z2):
##       Re-run that YAML explicitly (human-initiated backtest, 3 runs).
##       If result ≥ confirmed_champion_sharpe (within ±0.001): accept as champion.
##       Update storage, hash, log, all references in this document.
##       Log: "Z5: Re-confirmed at sharpe=[X]. Champion updated to Gen=[N] YAML."
##       If no such YAML exists: log "Z5: No candidate found. Skipped."
##
##   Z6: Inspect acceptance gate source code.
##       Answer: What value is incoming sharpe compared against?
##         Options: (a) hardcoded 2.3494, (b) log file value, (c) storage metadata,
##                  (d) in-memory variable set at startup, (e) other.
##       Answer: What triggers "new_best" vs "discarded" vs "new_elite"?
##       Answer: Does "new_elite" promote to champion, or only log without updating?
##       Log: "Z6: Gate compares against [SOURCE/VALUE].
##             new_elite = [DEFINITION]. new_elite → champion update: [YES/NO]."
##       IF gate compares against wrong value: fix it to compare against
##         confirmed_champion_sharpe from Z2. Fix must be in source code, not config.
##       IF "new_elite" should update champion but doesn't: fix it.
##       After any fix: re-run A0.5 before any generation proceeds.
##
##   Z7: Inspect clone detection source code.
##       Current behavior: clone detection appears to catch same-sharpe results
##         (2.3513 tagged "discarded") but may be comparing sharpe, not YAML hash.
##       Required behavior: clone detection compares YAML hash, not sharpe.
##         Same YAML hash → reject BEFORE backtest is submitted.
##       Fix: implement YAML hash comparison pre-backtest.
##       Verify: confirmed champion YAML → rejected as clone before backtest.
##       Log: "Z7: Clone detection fix: [DESCRIPTION].
##             Pre-backtest hash rejection: [working/not working]."
##
##   Z8: Inspect and fix pre-backtest MIN_TRADES enforcement.
##       (Note: I2 above may have already fixed the constant. This step verifies
##        the gate code itself, not just the constant value.)
##       Gens 5981, 5984, 5985, 5986, 5988, 5990, 5991, 5992, 5993, 5994
##         all ran with trades < 400 despite MIN_TRADES mandate.
##       Requirement: gate must run BEFORE backtest submission, not after.
##       Requirement: gate must be code, not LLM instruction.
##       Requirement: gate must use the actual live MIN_TRADES constant (now 400).
##       Identify why YAMLs producing ~78, ~134, ~178, ~190, ~255 trades
##         are reaching the backtest engine.
##       Fix gate. Verify by submitting known-zombie YAML profile.
##       Log: "Z8: Pre-backtest MIN_TRADES gate fixed: [DESCRIPTION].
##             Zombie YAML rejection test: PASS/FAIL."
##
##   Z9: Confirm Step Z completion.
##       Log: "STEP Z COMPLETE.
##             confirmed_champion_sharpe=[X],
##             confirmed_champion_YAML_hash=[Y],
##             confirmed_rsi_short=[A],
##             confirmed_TP=[B],
##             2.3531_resolution=[C],
##             acceptance_gate_status=[fixed/verified_working],
##             clone_detection_status=[fixed/verified_working],
##             MIN_TRADES_gate_status=[fixed/verified_working]."
##       IF any Z step could not be completed: HALT.
##       Log: "STEP Z FAILED at Z[N]: [REASON]. HALT."
##
## ─────────────────────────────────────────────────────────
## PHASE A0 — INFRASTRUCTURE SELF-TESTS
## STATUS: NOT EXECUTED. Mandated since Gen 5200.
## PREREQUISITE: Step Z complete (Z9 logged).
## EXECUTOR: Human operator. Not ODIN. Not LOKI.
## RULE: Single FAIL → HALT. Fix directly. Re-run ALL of A0 from A0.1.
##
##   A0.1: CHAMPION REPRODUCIBILITY.
##     Load confirmed champion YAML (post-Z3). Verify hash matches Z1.
##     Submit with ZERO parameter changes. Run 3 times.
##     Expected: sharpe = confirmed_champion_sharpe ± 0.0005, trades ± 2.
##     Log: "A0.1: [PASS/FAIL]. sharpe=[X ± Y], trades=[Z], win_rate=[W]."
##     FAIL condition: sharpe outside ± 0.0005 OR trades outside ± 2.
##
##   A0.2: PARAMETER CONFIRMATION.
##     From confirmed YAML, log exact values of ALL parameters.
##     Confirm: rsi_period=22, SL=1.91, timeout=159, trend_period=48, size_pct=25.
##     Confirm: rsi_short=[CONFIRMED_RSI_SHORT], TP=[CONFIRMED_TP].
##     Replace ALL stale/estimated/UNKNOWN values in this document with confirmed values.
##     Log: "A0.2: [PASS/FAIL]. confirmed_rsi_short=[X], confirmed_TP=[Y].
##           All other params confirmed: [YES/NO]."
##     FAIL condition: any "certain" parameter does not match stored value.
##
##   A0.3: PRE-BACKTEST CLONE REJECTION.
##     Submit confirmed champion YAML to pre-backtest validator.
##     Expected: REJECTED as clone BEFORE backtest runs.
##     Log: "A0.3: [PASS/FAIL]. Clone rejected pre-backtest: [YES/NO]."
##     FAIL condition: backtest runs at all.
##
##   A0.4: ZOMBIE PRE-REJECTION.
##     Test 1: YAML with rsi_long=50, rsi_short=55 → must be REJECTED pre-backtest.
##     Test 2: YAML with rsi_period_hours=24 → must be flagged as stale-attractor.
##     Test 3: YAML profile historically producing ~190 trades → REJECTED pre-backtest.
##     Test 4: YAML profile historically producing ~178 trades → REJECTED pre-backtest.
##     Log: "A0.4: [PASS/FAIL]. Tests 1/2/3/4: [PASS/FAIL each]."
##     FAIL condition: any test fails to reject before backtest.
##
##   A0.5: ACCEPTANCE GATE FUNCTION TEST.
##     Synthetic test A: inject result with sharpe = confirmed_champion_sharpe + 0.01,
##       trades=1265 → must be accepted as new_best and champion updated.
##     Synthetic test B: inject result with sharpe = confirmed_champion_sharpe - 0.01,
##       trades=1265 → must NOT be accepted. Champion unchanged.
##     After test A: reset champion back to confirmed value (restore from backup).
##     Log: "A0.5: [PASS/FAIL]. Test A: [accepted/rejected]. Test B: [accepted/rejected]."
##     FAIL condition: Test A rejected OR Test B accepted.
##
##   A0.6: "NEW_ELITE" CATEGORY DEFINITION.
##     Locate "new_elite" definition in source code.
##     Document exactly: what makes a result "new_elite" vs "discarded" vs "new_best"?
##     Confirm: does "new_elite" trigger champion update? If yes: is it working?
##     If "new_elite"