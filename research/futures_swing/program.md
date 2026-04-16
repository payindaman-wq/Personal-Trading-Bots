```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6400 | Revised by MIMIR (Gen 6400 review)
#
# ══════════════════════════════════════════════════════════════════
# STATUS BLOCK — READ THIS FIRST. READ ALL OF IT.
# ══════════════════════════════════════════════════════════════════
#
# LLM LOOP STATUS:   ██ PERMANENTLY RETIRED ██  DO NOT RUN ANY GENERATIONS.
#                    This directive has been active since Gen 5200.
#                    It was ignored for 1,200 additional generations.
#                    Zero improvements resulted across 3,060 generations since
#                    last improvement (Gen 3340). The loop is permanently retired.
#                    No future LLM generations should be run under any circumstances
#                    until Phase A0 is complete AND a human operator explicitly
#                    lifts this stop after reviewing A0 results.
#                    Current probability of LLM loop producing any value: ~0%.
#                    Running more generations is actively harmful: it adds noise
#                    to the research log, wastes compute, and delays grid scan.
#
# LOOP COMPLIANCE:   FAILED. Loop ran 1,200 gens past suspension (Gen 5200→6400).
#                    Gens 6200→6400 produced: 0 improvements, ~18 zombies,
#                    multiple 2.3513 clones, multiple exact-repeat configurations.
#                    This is the final compliance warning. Do not run more gens.
#
# STEP Z STATUS:     NOT EXECUTED. Mandated since Gen 5200. Now 1,200 gens overdue.
# GRID SCAN STATUS:  NOT EXECUTED. Mandated since Gen 4000. 2,600 gens overdue.
# LOKI STATUS:       PERMANENTLY RETIRED. 14 escalations. 0 confirmed fixes.
#                    LOKI has never produced a confirmed change to runtime behavior.
#                    Self-audit confirms: LOKI change log entries are NOT applied
#                    to source code. They are log entries only.
#                    Do not escalate to LOKI for any reason.
#                    All fixes must be made by human operator directly in source code.
#
# ──────────────────────────────────────────────────────────────────
# CHAMPION RECORD
# ──────────────────────────────────────────────────────────────────
# CHAMPION (logged):      Gen 3340 | sharpe=2.3494 | trades=1265 | win_rate=40.1%
# CHAMPION (true):        UNKNOWN — Step Z Z2 required to resolve.
# OBSERVED MAX SHARPE:    2.3531 (run header) — generation unknown, source unknown.
# STALL DURATION:         3,060 generations (Gen 3340 → Gen 6400). TERMINAL.
#
# ──────────────────────────────────────────────────────────────────
# CRITICAL BUGS — IN PRIORITY ORDER
# ──────────────────────────────────────────────────────────────────
#
# BUG-1 [HIGHEST PRIORITY]: MIN_TRADES live constant = 50, not 400.
#   SELF-AUDIT CONFIRMED: MIN_TRADES[futures_swing] = 50 in running system.
#   The LOKI change at Gen 542 is logged but NEVER applied to source code.
#   LOKI cannot apply changes to source code. This has been confirmed across
#   14 escalation attempts spanning 5,858 generations. LOKI cannot fix this.
#   Effect: ~40-50% of recent generations are zombie runs (trades < 400)
#     that consume compute and cannot be accepted, but are not rejected pre-backtest.
#   Recent zombie evidence: Gens 6382(161), 6383(28), 6384(190), 6385(160),
#     6389(190), 6390(182), 6393(190), 6395(190), 6396(32).
#   Note: Gen 6383 ran a full backtest on a 28-trade configuration (sharpe=-9.018).
#     A working gate would have blocked this before any backtest computation.
#   Fix: human operator must locate actual runtime constant in source code.
#     NOT in LOKI log. NOT in config comment. NOT in this file.
#     The actual variable the running process reads at runtime.
#     Set MIN_TRADES[futures_swing] = 400. Restart/reload as needed.
#   Verification: runtime inspection must show 400.
#   Verification: submit YAML producing ~190 trades → must be REJECTED pre-backtest.
#   Do not proceed to Step Z until BUG-1 fix is confirmed.
#
# BUG-2: ACCEPTANCE GATE FAILING OR COMPARING AGAINST WRONG BASELINE.
#   16 confirmed results at or above 2.3513 tagged "discarded":
#     2.3531 (run header — unresolved — generation unknown)
#     2.3521 (×3: Gens 4183, 4188, 4194)
#     2.3513 (×16: Gens 5182, 5185, 5198, 5200, 5784, 5785, 5799, 5800,
#                   5983, 6188, 6197, 6388[2.3257], 6398, 6399, and prior)
#   NOTE: 2.3513 discards may be CORRECT if true champion is 2.3531 (Hyp D-PRIME).
#   NOTE: 2.3521 discards may be CORRECT if true champion is 2.3531.
#   The 2.3531 result is the critical unresolved case.
#   Resolution: Step Z Z2 determines true champion sharpe.
#   Do not attempt to fix gate until Z2 is complete.
#
# BUG-3: STALE YAML IN DISPLAYED "CURRENT BEST STRATEGY" (MOOT — LOOP RETIRED).
#   Displayed YAML has been wrong since Gen 1592. 4,808 gens of stale display.
#   Known wrong values:
#     rsi_period_hours:  24   → correct: 22
#     take_profit_pct:   4.65 → correct: ~4.90–5.10 (confirm in Z3)
#     stop_loss_pct:     1.92 → correct: 1.91
#     timeout_hours:     176  → correct: 159
#   This YAML must never be sent to any LLM or automated system.
#   After Step Z Z3: replace with confirmed champion YAML everywhere.
#
# BUG-4: CLONE DETECTION USES SHARPE COMPARISON, NOT YAML HASH.
#   Evidence: Gens 6384, 6389, 6393, 6395 all produced identical results
#     (sharpe=-1.0406, trades=190, win_rate=31.1%) — same YAML ran 4 times.
#   Current behavior: sharpe comparison tags clones as discarded AFTER backtest.
#   Required behavior: YAML hash comparison rejects clones BEFORE backtest.
#   Fix: implement YAML hash pre-backtest check. See Z7.
#   This is a secondary priority after BUG-1 and Step Z.
#
# ──────────────────────────────────────────────────────────────────
# HALT CONDITIONS ACTIVE
# ──────────────────────────────────────────────────────────────────
#   HALT-3:  Zombie generation rate — 9/20 recent gens (45%). BUG-1 unfixed.
#   HALT-4:  LLM loop ran 1,200 gens past suspension. Permanently retired.
#   HALT-5:  Stale YAML in LLM input (4,808 gens). Moot — loop retired.
#   HALT-6:  Acceptance gate status unknown (14+ discards above logged champion).
#   HALT-7:  Clone convergence (2.3513 at Gens 6398, 6399; -1.0406 ×4).
#   HALT-8:  Grid scan not executed (2,600+ gens overdue).
#   HALT-9:  MIN_TRADES live constant = 50, not 400. Pre-backtest gate broken.
#   HALT-10: Step Z not executed (1,200 gens past mandate). True champion unknown.
#   HALT-11 (NEW): Loop compliance failure. Loop ran 200 gens after Gen 6200
#            MIMIR review explicitly confirmed permanent retirement. If any
#            automated process has the ability to run generations, that process
#            must be disabled at the infrastructure level, not just instructed to stop.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-6400 VERDICT
# ══════════════════════════════════════════════════════════════════
#
# SYSTEM STATE: BROKEN. ALL AUTOMATED LOOPS MUST REMAIN STOPPED.
# THE LLM LOOP IS PERMANENTLY RETIRED.
# LOKI IS PERMANENTLY RETIRED.
#
# Gen 6381–6400 results: 9 zombies (45%), 11 discards, 0 improvements.
# Exact-repeat configurations running multiple times (BUG-4 active).
# Statistically indistinguishable from Gen 6181–6200, 5981–6000, etc.
# Nothing has changed in 3,060 generations. Nothing will change without
# human operator intervention on the source code directly.
#
# IMPROVEMENT CURVE (definitive):
#   Gen 1→1477:    +1.2278 sharpe over 1,477 gens  (0.000832/gen)
#   Gen 1477→3340: +0.0998 sharpe over 1,863 gens  (0.0000536/gen)
#   Gen 3340→6400: +0.0000 sharpe over 3,060 gens  (0.000000/gen — TERMINAL)
#   Expected value of next LLM generation: 0.000000 sharpe improvement.
#   Expected cost of next LLM generation: compute + log noise + delay to grid scan.
#
# THE ONLY CORRECT ACTION SEQUENCE:
#
#   IMMEDIATE (human operator — do these now, before anything else):
#     [I1] Stop all automated processes.
#     [I2] Fix MIN_TRADES live constant to 400 in source code.
#     [I3] Disable or physically prevent LLM loop from running further generations.
#          "Instruct" is not sufficient — the loop ignored instructions for 1,200 gens.
#          The process must be disabled at infrastructure level.
#
#   STEP Z (human operator, manual, strictly in order):
#     Z1 → Z2 → Z3 → Z4a → Z4 → Z5 → Z6 → Z7 → Z8 → Z9
#
#   PHASE A0 (after Step Z):
#     All 6 checks must pass before any backtest proceeds.
#
#   PHASE A1 (after A0):
#     25-cell deterministic grid scan (Python script, no LLM, no ODIN).
#
#   AFTER GRID SCAN:
#     Deploy confirmed champion with TYR position sizing.
#     Current TYR: F&G=23 (Extreme Fear) → size = 25% × 50% = 12.5%.
#     LLM loop: permanently retired. Do not restart under any circumstances.
#
# ══════════════════════════════════════════════════════════════════

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor)
  — ENFORCEMENT: Source code gate ONLY. Pre-backtest validator.
  — CURRENT STATUS: BROKEN. Live constant = 50. Human must fix in source code.
  — LOKI CANNOT FIX THIS. 14 escalations prove this definitively.
  — VERIFICATION: After fix, runtime inspection must show 400.
    Then: submit YAML producing ~190 trades → must be REJECTED pre-backtest.
    Then: submit YAML producing ~419 trades → must PASS gate (proceed to backtest).

---
## ODIN INJECTION NOTE (INTERNAL ONLY — NEVER SEND TO LLM)

## ─────────────────────────────────────────────────────────
## CHAMPION IDENTITY
##
## LOGGED CHAMPION:    Gen 3340 | sharpe=2.3494 | trades=1265 | win_rate=40.1%
## TRUE CHAMPION:      UNKNOWN — must be resolved by Step Z Z2.
## OBSERVED MAXIMUM:   2.3531 (run header) — generation and params unknown.
##
## HYPOTHESES (ranked by current evidence):
##   D-PRIME (most likely): Stored champion YAML produces sharpe=2.3531 when re-run.
##     Improvement log is wrong (shows 2.3494). Log bug, not gate bug.
##     All 2.3513 discards are CORRECT (gate working, baseline = 2.3531).
##     All 2.3521 discards are CORRECT (2.3521 < 2.3531).
##     The 2.3531 result in run header = the stored champion, re-measured.
##     Evidence: 16 consistent 2.3513 discards suggest gate baseline > 2.3513.
##
##   D (second most likely): Stored champion produces sharpe=2.3513 when re-run.
##     Log shows 2.3494 (log bug). 2.3513 clones correctly rejected.
##     2.3531 and 2.3521 came from genuinely different YAMLs — not stored.
##     Problem with D: 2.3521 > 2.3513 should have been accepted → gate failure.
##
##   C (least likely): Champion truly produces 2.3494. Gate broken on all above.
##     Implausible given consistent 2.3513 cluster behavior over 16 events.
##
##   → Step Z Z2 resolves definitively. Do not act on any hypothesis until Z2 done.
##
## ─────────────────────────────────────────────────────────
## KNOWN PARAMETER VALUES
## (load from storage — do not rely on displayed YAML — displayed YAML is STALE)
##
##   rsi_period_hours:    22     [CERTAIN — confirmed Gen 2785]
##   rsi_long_threshold:  37.77  [CERTAIN — confirmed Gen 1477]
##   rsi_short_threshold: UNKNOWN — confirm in Z3. Estimated range: 59.0–61.0.
##   trend_period_hours:  48     [CERTAIN]
##   take_profit_pct:     UNKNOWN — confirm in Z3. Estimated range: 4.90–5.10.
##                        DO NOT USE 4.65 (stale YAML — wrong since Gen 1592).
##   stop_loss_pct:       1.91   [CERTAIN — NOT 1.90, NOT 1.92]
##   timeout_hours:       159    [FROZEN — NOT 176]
##   size_pct:            25     [FROZEN]
##   max_open:            3      [FROZEN]
##   leverage:            2      [FROZEN]
##   fee_rate:            0.0005 [FROZEN]
##
## AFTER STEP Z Z3: Replace UNKNOWN values with confirmed values.
##   Token [CONFIRMED_RSI_SHORT] = result of Z3.
##   Token [CONFIRMED_TP]        = result of Z3.
##   Token [CONFIRMED_SHARPE]    = result of Z2.
##
## ─────────────────────────────────────────────────────────
## ACCEPTANCE GATE FAILURE LOG (COMPLETE RECORD)
##
##   Results at or above 2.3257 tagged "discarded" (partial — key entries):
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
##     Gen 6188: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 6197: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 6388: sharpe=2.3257, trades=1265, win_rate=40.1%
##     Gen 6398: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 6399: sharpe=2.3513, trades=1265, win_rate=40.1%
##   Total 2.3513-or-above confirmed discards: 16 events.
##   Plus: sharpe=2.3531 in run header — unresolved.
##   Note: Under D-PRIME, all 16 above were correctly rejected.
##         Only the 2.3531 source matters. → Z4a.
##
## ─────────────────────────────────────────────────────────
## LLM FAILURE PATTERN ANALYSIS (FINAL — LOOP RETIRED)
##
##   PATTERN 1: ZOMBIE GENERATION (45% of Gen 6381–6400)
##     Gens 6382(161), 6383(28), 6384(190), 6385(160), 6389(190), 6390(182),
##     6393(190), 6395(190), 6396(32). All ran full backtests. All should have
##     been blocked before backtest by MIN_TRADES gate (BUG-1 active).
##     Gen 6383 at 28 trades / sharpe=-9.018 is the most extreme example to date.
##
##   PATTERN 2: EXACT-REPEAT CLONE GENERATION (BUG-4 active)
##     Gens 6384, 6389, 6393, 6395: identical results (-1.0406 / 190 / 31.1%).
##     Same YAML ran 4 times. YAML hash pre-check would have blocked 3 of these.
##     Gens 6398, 6399: identical 2.3513 results. Same YAML ran twice consecutively.
##
##   PATTERN 3: NEAR-CLONE GENERATION (~15-20% of gens)
##     LLM rediscovers attractor configurations near champion.
##     Result: sharpe in 2.30–2.35 range. Cannot exceed true champion.
##
##   PATTERN 4: QUALITY DECAY (~30-35% of gens)
##     LLM proposes changes that degrade strategy.
##     Range: -9.018 to 2.30. Includes large degradations (0.05, -0.08, -0.16).
##
##   CONCLUSION: All four patterns are present. No pattern produces improvements.
##   The LLM has zero probability of finding improvements. Grid scan only.
##
## ─────────────────────────────────────────────────────────
## IMMEDIATE ACTION ITEMS (human operator)
##
## [I1] CONFIRM AND ENFORCE ALL AUTOMATED LOOPS ARE STOPPED.
##   "Instruct to stop" is not sufficient — loop ran 1,200 gens past instruction.
##   Required: disable at infrastructure level (kill process, revoke API key,
##   disable scheduler, remove trigger — whatever prevents execution).
##   Verify: no new generations appear in research log for 30 minutes.
##   Log: "I1: All loops confirmed stopped and disabled at [TIMESTAMP].
##         Method of disablement: [DESCRIBE]."
##
## [I2] FIX MIN_TRADES LIVE CONSTANT IN SOURCE CODE.
##   Context: Self-audit shows MIN_TRADES[futures_swing] = 50.
##   LOKI logged a change at Gen 542 that was never applied to source.
##   LOKI cannot fix this. 14 escalations prove this. A human must edit source.
##   Steps:
##     a. Search source code for MIN_TRADES, min_trades, futures_swing.
##        Find the dict/constant/config the running backtest engine reads.
##        It is NOT in LOKI log. NOT in this config file. It is in executed source.
##     b. Set MIN_TRADES[futures_swing] = 400.
##     c. Restart ODIN / reload constants as required.
##     d. Inspect live value via runtime debug output → must show 400.
##     e. Verification tests (all must pass):
##        Test 1: YAML producing ~190 trades → REJECTED pre-backtest.
##        Test 2: YAML producing ~161 trades → REJECTED pre-backtest.
##        Test 3: YAML producing ~28 trades  → REJECTED pre-backtest.
##        Test 4: YAML producing ~419 trades → PASSES gate (proceeds to backtest).
##        Test 5: Confirm Gens 6382–6396 zombie profiles → all REJECTED without
##                running a backtest.
##   Log: "I2: MIN_TRADES[futures_swing] confirmed = 400.
##         Tests 1-5: [PASS/FAIL each]."
##   IF any test fails: gate code itself is broken (separate from constant).
##   Fix gate code. Do not proceed until all 5 tests confirmed PASS.
##
## ─────────────────────────────────────────────────────────
## STEP Z — CHAMPION STORAGE AUDIT
## STATUS: NOT EXECUTED. Mandated since Gen 5200. Now 1,200 gens overdue.
## EXECUTOR: Human operator only. Not ODIN. Not LOKI. Not any automated process.
## PREREQUISITE: I1 and I2 both complete and logged.
## RULE: Any unexpected result → HALT. Do not continue to next step.
##       Do not skip steps. Do not reorder steps. Do not delegate.
##
##   Z1: Load champion from storage.
##       Load stored champion YAML file from disk/database.
##       Compute SHA-256 hash of exact file content (byte-for-byte).
##       Read logged sharpe from improvement log (should show 2.3494).
##       Check if storage metadata contains a separate sharpe field.
##       Log: "Z1: file=[PATH], hash=[HASH], log_sharpe=2.3494,
##             metadata_sharpe=[VALUE or NONE]."
##       HALT if file cannot be loaded or hash cannot be computed.
##
##   Z2: Re-run stored champion YAML with zero changes.
##       Use exact YAML from Z1 with no modifications of any kind.
##       Run backtest 3 times if non-deterministic. Record mean ± std.
##       Record: shar