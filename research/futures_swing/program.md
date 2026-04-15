```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6200 | Revised by MIMIR (Gen 6200 review)
#
# ══════════════════════════════════════════════════════════════════
# STATUS BLOCK — READ THIS FIRST. READ ALL OF IT.
# ══════════════════════════════════════════════════════════════════
#
# LLM LOOP STATUS:   ██ HARD STOP ██  DO NOT RUN ANY GENERATIONS.
#                    This directive has been active since Gen 5200.
#                    It was ignored for 1,000 additional generations.
#                    Zero improvements resulted. The loop is permanently retired.
#                    No future LLM generations should be run under any circumstances
#                    until Phase A0 is complete and a human operator explicitly
#                    lifts this stop after reviewing A0 results.
#                    Current probability of LLM loop producing any value: ~0%.
#
# STEP Z STATUS:     NOT EXECUTED. Mandated since Gen 5200. Now 1,000 gens overdue.
# GRID SCAN STATUS:  NOT EXECUTED. Mandated since Gen 4000. 2,400 gens overdue.
# LOKI STATUS:       PERMANENTLY RETIRED. 13 escalations. 0 confirmed fixes.
#                    LOKI has no confirmed positive effect on the running system.
#                    Do not escalate to LOKI for any reason.
#                    All fixes must be made by human operator directly in source code.
#
# ──────────────────────────────────────────────────────────────────
# CHAMPION RECORD
# ──────────────────────────────────────────────────────────────────
# CHAMPION (logged):      Gen 3340 | sharpe=2.3494 | trades=1265 | win_rate=40.1%
# CHAMPION (true):        UNKNOWN — Step Z required to resolve.
# OBSERVED MAX SHARPE:    2.3531 (run header) — generation unknown, source unknown.
# STALL DURATION:         2,860 generations (Gen 3340 → Gen 6200). TERMINAL.
#
# ──────────────────────────────────────────────────────────────────
# CRITICAL BUGS — IN PRIORITY ORDER
# ──────────────────────────────────────────────────────────────────
#
# BUG-1 [HIGHEST PRIORITY]: MIN_TRADES live constant = 50, not 400.
#   Self-audit confirms: MIN_TRADES[futures_swing] = 50 in running system.
#   This has been wrong since Gen 542 (5,658 generations of broken zombie filtering).
#   LOKI change at Gen 542 is logged but never persisted in source code.
#   Effect: ~25-30% of all generations are zombie runs (trades < 400) that
#     consume compute and cannot be accepted, but are not rejected pre-backtest.
#   Recent zombie evidence: Gens 6182(178), 6184(255), 6186(192),
#     6187(255), 6195(255), 6199(190) — all ran full backtests unnecessarily.
#   Fix: locate actual runtime constant definition in source code (not LOKI log,
#     not config comment — the actual variable the running process reads).
#     Set MIN_TRADES[futures_swing] = 400. Restart if needed.
#   Verification: inspect live value at runtime → must read 400.
#   Verification: submit YAML producing ~190 trades → must be REJECTED pre-backtest.
#   Do not proceed to Step Z until this is confirmed fixed.
#
# BUG-2: ACCEPTANCE GATE FAILING OR COMPARING AGAINST WRONG BASELINE.
#   14+ confirmed results above logged champion (2.3494) tagged "discarded":
#     2.3531 (×unknown — run header max — generation unknown)
#     2.3521 (×3: Gens 4183, 4188, 4194)
#     2.3513 (×10+: Gens 5182, 5185, 5198, 5200, 5784, 5785, 5799, 5800,
#                    5983, 6188, 6197, and counting)
#   Note: 2.3513 discards may be CORRECT if true champion is 2.3531 (Hyp D-PRIME).
#   Note: 2.3521 discards may be CORRECT if true champion is 2.3531.
#   The 2.3531 result is the critical unresolved case.
#   Resolution: Step Z Z2 will determine true champion sharpe.
#     If true champion = 2.3531: gate is working, log is wrong. Fix log.
#     If true champion = 2.3494: gate is broken on everything above. Fix gate.
#   Do not attempt to fix gate until Z2 is complete.
#
# BUG-3: STALE YAML CONTAMINATING LLM INPUT (NOW MOOT — LOOP RETIRED).
#   The displayed "Current Best Strategy" YAML has been wrong since Gen 1592.
#   4,608 generations of LLM input were based on wrong parameter values.
#   This YAML must never be sent to any LLM or automated system.
#   After Step Z: replace with confirmed champion YAML.
#   Known wrong values in displayed YAML:
#     rsi_period_hours:  24   → correct: 22
#     take_profit_pct:   4.65 → correct: ~4.95–5.00 (confirm in Z3)
#     stop_loss_pct:     1.92 → correct: 1.91
#     timeout_hours:     176  → correct: 159
#
# BUG-4: CLONE DETECTION USES SHARPE COMPARISON, NOT YAML HASH.
#   Current behavior: same sharpe value → tagged discarded (possibly correct).
#   Required behavior: same YAML hash → rejected BEFORE backtest is submitted.
#   Effect: identical YAMLs are running full backtests unnecessarily.
#   Fix: implement YAML hash pre-backtest check. See Z7.
#
# ──────────────────────────────────────────────────────────────────
# HALT CONDITIONS ACTIVE
# ──────────────────────────────────────────────────────────────────
#   HALT-3: Zombie generation rate — 6/20 recent gens (6182,6184,6186,6187,6195,6199).
#   HALT-4: LLM loop ran 1,000 gens past suspension order. Now permanently retired.
#   HALT-5: Stale YAML in LLM input (4,608 gens). Moot — loop retired.
#   HALT-6: Acceptance gate status unknown (14+ discards above logged champion).
#   HALT-7: Clone convergence (2.3513 repeating in Gens 6188, 6197).
#   HALT-8: Grid scan not executed (2,400+ gens overdue).
#   HALT-9: MIN_TRADES live constant = 50, not 400. Pre-backtest gate broken.
#   HALT-10 (NEW): Step Z not executed (1,000 gens past mandate). True champion unknown.
#
# ══════════════════════════════════════════════════════════════════
# MIMIR GEN-6200 VERDICT
# ══════════════════════════════════════════════════════════════════
#
# SYSTEM STATE: BROKEN. ALL AUTOMATED LOOPS MUST REMAIN STOPPED.
# THE LLM LOOP IS PERMANENTLY RETIRED.
#
# Gen 6181–6200 results: 6 zombies, 13 discards (including 2 more 2.3513 clones),
# 0 improvements. This is statistically indistinguishable from Gen 5981–6000.
# Nothing has changed. Nothing will change without human operator intervention.
#
# IMPROVEMENT CURVE (definitive):
#   Gen 1→1477:    +1.2278 sharpe over 1,477 gens  (0.000832/gen)
#   Gen 1477→3340: +0.0998 sharpe over 1,863 gens  (0.0000536/gen)
#   Gen 3340→6200: +0.0000 sharpe over 2,860 gens  (0.000000/gen — TERMINAL)
#   Expected value of next LLM generation: ~0.000000 sharpe improvement.
#   Expected cost of next LLM generation: compute + noise in research log.
#   Decision: LLM loop permanently retired. Grid scan is the only remaining action.
#
# THE ONLY CORRECT ACTION SEQUENCE:
#
#   IMMEDIATE (human operator — do these now, before anything else):
#     [I1] Confirm all automated loops are stopped: LLM loop, LOKI, everything.
#          Log: "I1: All loops confirmed stopped at [TIMESTAMP]."
#
#     [I2] Fix MIN_TRADES live constant to 400:
#          a. Locate runtime constant in source code (not LOKI log, not config comment).
#          b. Set MIN_TRADES[futures_swing] = 400.
#          c. Restart ODIN or reload constants as needed.
#          d. Inspect live value at runtime → verify reads 400.
#          e. Submit YAML producing ~190 trades to pre-backtest validator → verify REJECTED.
#          f. Submit YAML producing ~255 trades → verify REJECTED.
#          g. Submit YAML producing ~419 trades → verify ACCEPTED past gate (proceeds to backtest).
#          Log: "I2: MIN_TRADES[futures_swing] = 400 confirmed. Rejection tests: [PASS/FAIL each]."
#          IF verification fails: the gate code itself is broken (not just the constant).
#            Fix gate code. Do not proceed until both constant and gate verified working.
#
#   STEP Z (human operator, manual, strictly in order):
#     Z1 → Z2 → Z3 → Z4a → Z4 → Z5 → Z6 → Z7 → Z8 → Z9
#     See Step Z section below. No skipping. No delegating to LOKI or ODIN.
#
#   PHASE A0 (after Step Z complete):
#     All 6 checks must pass before any backtest proceeds.
#     See Phase A0 section below.
#
#   PHASE A1 (after A0 complete):
#     25-cell deterministic grid scan.
#     Python script only. No LLM. No ODIN automation beyond script execution.
#     See Phase A1 section below.
#
#   AFTER GRID SCAN:
#     IF any result improves confirmed champion: accept, update all records,
#       consider one additional targeted grid pass around new champion.
#     IF no result improves confirmed champion: research is complete.
#     Deploy confirmed champion to live with TYR position sizing applied.
#     Current TYR directive: F&G=23 (Extreme Fear) → 50% position size.
#       Apply: size_pct = 25 × 0.50 = 12.5% for live deployment until regime changes.
#     LLM loop: permanently retired. Do not restart.
#
# ══════════════════════════════════════════════════════════════════

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor — currently BROKEN in live system, see BUG-1)
  — ENFORCEMENT: Code gate ONLY. Pre-backtest validator. Not LLM instruction. Not LOKI.
  — GATE LOCATION: Pre-backtest validator, before ANY backtest is submitted.
  — CURRENT STATUS: BROKEN. Live constant = 50. Fix required (see I2 above).
  — VERIFICATION REQUIRED: After fix, confirm live constant = 400 by direct
    inspection of runtime value. Then confirm rejection test passes.

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
##   D-PRIME (most likely): Stored champion produces sharpe=2.3531 when re-run.
##     Improvement log is wrong (shows 2.3494 instead of 2.3531).
##     2.3513 near-clones are being rejected correctly (gate IS working on these).
##     2.3521 results from Gens 4183/4188/4194 also correctly rejected if true > 2.3521.
##     The 2.3531 result was accepted and stored, but improvement log not updated.
##     Evidence: consistent 2.3513 rejects suggest gate baseline is above 2.3513.
##
##   D (second most likely): Stored champion produces sharpe=2.3513 when re-run.
##     Log shows 2.3494 (log bug — stored at wrong value).
##     2.3513 clones correctly rejected by gate (comparing against 2.3513).
##     2.3531 came from a genuinely different YAML — lost, discarded, or not stored.
##
##   C (least likely): Champion truly produces 2.3494. Gate broken on all above.
##     2.3513 discards are gate failures. 2.3521 discards are gate failures.
##     2.3531 is also a gate failure or from a different YAML.
##     Evidence against: implausible that gate fails consistently on every result
##       above 2.3494 across hundreds of generations.
##
##   → Step Z Z2 resolves this definitively. Do not act on hypotheses until Z2 done.
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
##                        DO NOT USE 4.65 (stale YAML value — wrong since Gen 1592).
##   stop_loss_pct:       1.91   [CERTAIN — NOT 1.90, NOT 1.92]
##   timeout_hours:       159    [FROZEN FOREVER — NOT 176]
##   size_pct:            25     [FROZEN]
##   max_open:            3      [FROZEN]
##   leverage:            2      [FROZEN]
##   fee_rate:            0.0005 [FROZEN]
##
## AFTER STEP Z Z3: Replace UNKNOWN values above with confirmed values.
##   Token [CONFIRMED_RSI_SHORT] = result of Z3.
##   Token [CONFIRMED_TP]        = result of Z3.
##   Token [CONFIRMED_SHARPE]    = result of Z2.
##
## ─────────────────────────────────────────────────────────
## ACCEPTANCE GATE FAILURE LOG (COMPLETE RECORD)
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
##     Gen 6188: sharpe=2.3513, trades=1265, win_rate=40.1%
##     Gen 6197: sharpe=2.3513, trades=1265, win_rate=40.1%
##   Total confirmed: 14 events.
##   Plus: sharpe=2.3531 in run header — unresolved.
##   Note: If D-PRIME is correct, all 14 above were correctly rejected.
##         Only the 2.3531 resolution matters. → Z4a.
##
## ─────────────────────────────────────────────────────────
## LLM FAILURE PATTERN ANALYSIS (FINAL — LOOP RETIRED)
##
##   PATTERN 1: ZOMBIE GENERATION (~25-30% of recent gens)
##     The LLM proposes RSI threshold changes or period length increases that
##     collapse trade count below 400. These run full backtests (BUG-1) and
##     produce low_trades tags. Examples: rsi_long < 30, rsi_short > 70,
##     rsi_period > 30, trend_period > 72.
##     Examples from recent gens: 6182(178), 6184(255), 6186(192),
##       6187(255), 6195(255), 6199(190).
##
##   PATTERN 2: NEAR-CLONE GENERATION (~30-40% of recent gens)
##     The LLM proposes micro-changes that produce strategies virtually identical
##     to the champion. Result: sharpe in 2.34–2.35 range, tagged discarded.
##     These are structurally correct but cannot improve on the optimum.
##     Examples: 2.3513 at Gens 6188, 6197; 2.3489 at Gen 6189; 2.3493 at Gen 6192.
##
##   PATTERN 3: QUALITY DECAY (~30-40% of recent gens)
##     The LLM proposes changes that genuinely degrade the strategy.
##     Result: sharpe in 0.44–2.30 range. Strategy diverges from optimum.
##     Examples: 0.44 (Gen 6183), 0.68 (Gen 6181), 1.36 (Gen 6191).
##
##   CONCLUSION: No remaining pattern produces improvements. The search space
##   near the optimum is exhausted for this model/approach. Grid scan is the
##   only tool that can confirm or marginally improve the result.
##
## ─────────────────────────────────────────────────────────
## IMMEDIATE ACTION ITEMS (human operator)
##
## [I1] CONFIRM ALL AUTOMATED LOOPS ARE STOPPED.
##   Verify: LLM generation loop is not running.
##   Verify: LOKI is not running.
##   Verify: No automated process is submitting backtests.
##   Log: "I1: All loops confirmed stopped at [TIMESTAMP]."
##
## [I2] FIX MIN_TRADES LIVE CONSTANT.
##   Context: Self-audit shows MIN_TRADES[futures_swing] = 50 in live system.
##   The LOKI change at Gen 542 is logged but never persisted in source code.
##   13 subsequent LOKI escalations did not fix this. LOKI cannot fix this.
##   A human must edit the source code directly.
##   Steps:
##     a. Search source code for: MIN_TRADES, min_trades, futures_swing
##        Find the actual variable that the running backtest engine reads at runtime.
##        It is NOT in the LOKI change log. It is NOT in this config file.
##        It is in the source code that ODIN executes.
##     b. Set MIN_TRADES[futures_swing] = 400 in that location.
##     c. Restart ODIN / reload constants as required for change to take effect.
##     d. Inspect live value via runtime inspection / debug output → must read 400.
##     e. Verification tests:
##        Test 1: YAML historically producing ~190 trades → REJECTED pre-backtest.
##        Test 2: YAML historically producing ~255 trades → REJECTED pre-backtest.
##        Test 3: YAML historically producing ~419 trades → PASSES gate (runs backtest).
##        Test 4: Confirm Gens 6182, 6184, 6186, 6187, 6195, 6199 profiles
##                would be rejected without running a backtest.
##   Log: "I2: MIN_TRADES[futures_swing] confirmed = 400.
##         Test 1: [PASS/FAIL]. Test 2: [PASS/FAIL]. Test 3: [PASS/FAIL].
##         Test 4: [PASS/FAIL]."
##   IF any verification fails: gate code itself is broken (separate from constant).
##   Fix gate code. Do not proceed to Step Z until I2 is fully verified.
##
## ─────────────────────────────────────────────────────────
## STEP Z — CHAMPION STORAGE AUDIT
## STATUS: NOT EXECUTED. Mandated since Gen 5200. Now 1,000 gens overdue.
## EXECUTOR: Human operator only. Not ODIN. Not LOKI.
## PREREQUISITE: I1 and I2 both complete and logged.
## RULE: Any unexpected result → HALT. Do not continue to next step.
##       Do not skip steps. Do not reorder steps. Do not delegate.
##
##   Z1: Load champion from storage.
##       Load stored champion YAML file from disk/database.
##       Compute SHA-256 hash of the exact file content.
##       Read logged sharpe from improvement log (should show 2.3494).
##       Check if storage metadata contains a separate sharpe field.
##       Log: "Z1: file=[PATH], hash=[HASH], log_sharpe=2.3494,
##             metadata_sharpe=[VALUE or NONE]."
##
##   Z2: Re-run stored champion YAML with zero changes.
##       Use the exact YAML loaded in Z1 with no modifications.
##       Run 3 times if backtest is non-deterministic. Record mean ± std.
##       Record: sharpe (mean ± std), trades, win_rate.
##       Log: "Z2: backtested_sharpe=[X ± Y], trades=[Z], win_rate=[W]."
##
##       Interpretation:
##         IF sharpe ≈ 2.3531 (within ±0.002): HYPOTHESIS D-PRIME CONFIRMED.
##           → True champion sharpe = 2.3531. Improvement log is wrong (shows 2.3494).
##           → confirmed_champion_sharpe = 2.3531.
##           → All 2.3513 discards were CORRECT (gate working normally).
##           → All 2.3521 discards were CORRECT (gate working normally).
##           → Only outstanding issue: 2.3531 in run header (investigate Z4a).
##           → Log: "Z2: D-PRIME CONFIRMED. True champion = 2.3531."
##
##         IF sharpe ≈ 2.3513 (within ±0.002): HYPOTHESIS D CONFIRMED.
##           → True champion sharpe = 2.3513. Log shows 2.3494 (log bug).
##           → confirmed_champion_sharpe = 2.3513.
##           → 2.3513 clones correctly rejected. Gate functioning.
##           → 2.3531 and 2.3521 came from different YAMLs (investigate Z4a, Z4).
##           → Log: "Z2: D CONFIRMED. True champion = 2.3513."
##
##         IF sharpe ≈ 2.3494 (within ±0.002): HYPOTHESIS C CONFIRMED.
##           → True champion = 2.3494. Acceptance gate broken on all results above.
##           → confirmed_champion_sharpe = 2.3494.
##           → Gate fix mandatory before any generation proceeds (see Z6).
##           → Log: "Z2: C CONFIRMED. Champion = 2.3494. Gate is broken."
##
##         IF sharpe differs from ALL above by > 0.003: HALT.
##           → Log: "Z2: UNEXPECTED sharpe=[X]. Cannot proceed. HALT."
##           → Investigate data integrity, backtest engine version, parameter loading.
##
##   Z3: Record all parameter values from stored champion YAML.
##       Read every parameter from the file loaded in Z1.
##       Compare against known values in INJECTION NOTE above.
##       Log: "Z3: rsi_period=[A], rsi_long=[B], rsi_short=[C], trend_period=[D],
##             TP=[E], SL=[F], timeout=[G], size_pct=[H], max_open=[I]."
##       Resolve tokens:
##         [CONFIRMED_RSI_SHORT] = [C]
##         [CONFIRMED_TP]        = [E]
##       Replace tokens everywhere in this document with confirmed values.
##       IF any CERTAIN parameter differs from known value:
##         (rsi_period≠22, rsi_long≠37.77, SL