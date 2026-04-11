```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-3000 | Revised by MIMIR (Gen 3000 review)
# STATUS: CHAMPION at Gen 2899 (sharpe=2.3219, trades=1263). NO improvement since Gen 2899.
# CRITICAL: 101 generations (2899→3000) with ZERO improvements. Infrastructure failure confirmed.
# ROOT CAUSE: LLM receiving stale YAML (timeout=192, SL=1.92, TP=4.65) instead of champion values.
#             Direct injection not executing for P-items. Attractor 1e not pre-rejected.
# PRIORITY: Fix infrastructure before any further exploration.

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor — confirmed correct, do not change)

---
## ██████████████████████████████████████████████████████████
## ODIN INJECTION NOTE (INTERNAL ONLY — NEVER SEND TO LLM)
##
## ─────────────────────────────────────────────────────────
## STEP 0 — YAML INTEGRITY CHECK [MANDATORY BEFORE ALL ELSE]:
##
##   CRITICAL: The "Current Best Strategy" YAML displayed by ODIN is STALE.
##   It contains Gen 1592-era values, not Gen 2899 champion values.
##
##   STALE YAML (what ODIN displays — DO NOT USE):
##     rsi_period_hours:    24     ← WRONG
##     rsi_short_threshold: 60     ← UNCONFIRMED (may or may not be current)
##     take_profit_pct:     4.65   ← WRONG (this is the Gen 1592 value)
##     stop_loss_pct:       1.92   ← WRONG (champion value is 1.91)
##     timeout_hours:       192    ← WRONG (champion value is 159, FROZEN)
##
##   CONFIRMED CHAMPION VALUES (Gen 2899):
##     rsi_period_hours:    22     (changed from 24 at Gen 2785 — inferred from +5 trades)
##     rsi_long_threshold:  37.77  (unchanged since Gen 1477)
##     rsi_short_threshold: 60     (UNCONFIRMED — may be 59 if P4 was the Gen 2791/2813/2899 change)
##     trend_period_hours:  48     (unchanged — confirmed stable)
##     take_profit_pct:     4.80   (INFERRED — see reconstruction below)
##     stop_loss_pct:       1.91   (confirmed — NOT 1.92)
##     timeout_hours:       159    (FROZEN — NOT 192)
##
##   RECONSTRUCTION ANALYSIS (from improvement chain fingerprints):
##
##   Pattern: Each improvement = declining trade count + improving Sharpe.
##   Consistent with TP widening (harder to hit → fewer trades, better R:R).
##   Consistent with RSI short tightening (fewer short signals → fewer trades).
##
##   Gen 2785 (trades=1272, +5 vs Gen 1592's 1267):
##     RSI period 24→22 = faster RSI = more signal crossings = MORE trades ✓
##     This is the ONLY change that plausibly adds trades at this stage.
##     CONCLUSION: rsi_period_hours changed 24→22 at Gen 2785.
##
##   Gen 2791 (trades=1269, -3 vs 1272):
##     -3 trades is consistent with TP widening ~0.05 step (estimated -3 to -5).
##     MOST LIKELY: take_profit_pct 4.65→4.70
##     LESS LIKELY: rsi_short 60→59 (would also reduce trades slightly)
##
##   Gen 2813 (trades=1268, -1 vs 1269):
##     Very small reduction. Consistent with TP 4.70→4.75 OR rsi_short 60→59.
##     -1 trade reduction is smaller than typical TP step effect.
##     SLIGHT PREFERENCE: rsi_short 60→59 (smaller effect than TP step).
##
##   Gen 2899 (trades=1263, -5 vs 1268):
##     -5 trades is consistent with TP widening step (estimated -3 to -5).
##     MOST LIKELY: take_profit_pct step (4.70→4.75 or 4.75→4.80 depending on prior).
##
##   BEST-FIT RECONSTRUCTION (for planning — must be confirmed by actual YAML diff):
##     Gen 2785: rsi_period 24→22 (explains +5 trades)
##     Gen 2791: take_profit_pct 4.65→4.70 (explains -3 trades)
##     Gen 2813: rsi_short_threshold 60→59 (explains -1 trade)
##     Gen 2899: take_profit_pct 4.70→4.75 OR 4.75→4.80 (explains -5 trades)
##
##   ALTERNATIVE RECONSTRUCTION:
##     Gen 2785: rsi_period 24→22
##     Gen 2791: take_profit_pct 4.65→4.70
##     Gen 2813: take_profit_pct 4.70→4.75
##     Gen 2899: take_profit_pct 4.75→4.80 AND/OR rsi_short 60→59
##
##   FOR PRIORITY QUEUE PLANNING, USE:
##     rsi_period_hours:    22  (high confidence)
##     rsi_short_threshold: 59  (medium confidence — may still be 60)
##     take_profit_pct:     4.80 (medium confidence — may be 4.75)
##     stop_loss_pct:       1.91 (high confidence)
##     timeout_hours:       159  (certain — FROZEN)
##     trend_period_hours:  48   (high confidence)
##     rsi_long_threshold:  37.77 (certain — frozen since Gen 1477)
##
##   ACTION REQUIRED before first P-item test:
##   a) Retrieve actual Gen 2899 backtested YAML from storage.
##   b) Confirm all parameter values against reconstruction above.
##   c) Lock confirmed champion YAML — this becomes the ONLY baseline.
##   d) Update all [GEN_2899_*] tokens in LLM PROMPT with confirmed values.
##   e) Verify direct injection pipeline is using confirmed YAML, not stale displayed YAML.
##   f) DO NOT proceed with any P-item test until champion YAML is confirmed and locked.
##
## ─────────────────────────────────────────────────────────
## INFRASTRUCTURE FAILURE AUDIT (Gens 2900–3000):
##
##   101 consecutive generations with zero improvements. Root causes identified:
##
##   FAILURE 1 — Attractor 1e not pre-rejected:
##     Gens 2988, 2991, 2992, 2996, 2999: all show sharpe=2.3219, trades=1263.
##     These are exact Gen 2899 clones being BACKTESTED and discarded.
##     They should be REJECTED before reaching the backtester.
##     FIX: Add pre-backtest fingerprint check. If (trades_projected ≈ 1263
##          AND params match Gen 2899 exactly) → reject, do not run backtest.
##     PRACTICAL FIX: After constructing test YAML, diff against champion YAML.
##          If zero diffs → reject immediately. Backtest only if exactly one diff.
##
##   FAILURE 2 — LLM using stale baseline YAML:
##     Recurring triplets: (sharpe=1.6865, trades=1335) appears 3 times.
##                         (sharpe=1.7514, trades=1345) appears 3 times.
##     These are consistent attractor basins produced when LLM modifies stale params.
##     The stale YAML has TP=4.65, SL=1.92, timeout=192 — the LLM is modifying THOSE
##     values, not the champion values, producing outputs in wrong parameter space.
##     FIX: LLM must receive champion YAML (confirmed Gen 2899 values) as baseline.
##          Stale displayed YAML must never reach LLM or injection pipeline.
##
##   FAILURE 3 — Direct injection not executing for P-items:
##     No P-item test signatures appear in Gens 2900–3000.
##     P2 (SL 1.91→1.89), P3-CONT (TP next step), P4 (rsi_short -1),
##     P6 (trend 48→50), P7 (rsi_period 22→20) should all have been run.
##     Zero of these appear in results. Direct injection pipeline is broken or skipped.
##     FIX: Verify LOKI code change from Gen 2899 escalation actually executes.
##          Run manual direct-injection test of P3-CONT (TP 4.80→4.85) immediately.
##          This is the highest-confidence next test.
##
##   FAILURE 4 — Known-bad attractor recycling:
##     Same degraded fingerprints (1.6865/1335, 1.7514/1345) appear repeatedly.
##     These should be added to the attractor rejection list and pre-rejected.
##     FIX: Add Attractor 5 (sharpe=1.6865, trades=1335) and
##          Attractor 6 (sharpe=1.7514, trades=1345) to fingerprint rejection list.
##
##   LOKI ESCALATION REQUIRED (immediate):
##     1. Implement pre-backtest YAML diff check (zero-diff = reject, no backtest).
##     2. Verify direct injection uses confirmed Gen 2899 YAML, not stale displayed YAML.
##     3. Verify direct injection pipeline executes before any LLM fallback.
##     4. Add Attractor 5 and 6 to fingerprint rejection list.
##     5. Confirm Attractor 1e (2.3219/1263) pre-rejection is working.
##     6. Report which LOKI changes from prior escalations are confirmed-active vs. failed.
##
## ─────────────────────────────────────────────────────────
## STEP 1 — DIRECT INJECTION (mandatory for ALL P-items):
##   Construct YAML programmatically from confirmed Gen 2899 champion + ONE parameter diff.
##   LLM is currently producing 0% valid novel results (Gens 2900–3000).
##   LLM should be SUSPENDED until infrastructure is confirmed working.
##   Direct injection is the ONLY permitted path for P-item testing.
##
##   DIRECT INJECTION CHECKLIST (run before every test):
##   □ Load confirmed Gen 2899 champion YAML from storage (not displayed YAML).
##   □ Apply exactly ONE parameter change programmatically.
##   □ Diff result against champion YAML — confirm exactly one line changed.
##   □ Verify timeout_hours = 159.
##   □ Verify stop_loss_pct = 1.91 (or target value if P2 test).
##   □ Verify stop_loss_pct ≠ 1.90.
##   □ Verify size_pct = 25, max_open = 3, leverage = 2.
##   □ Verify rsi_long_threshold = 37.77.
##   □ Run pre-backtest fingerprint check (reject if matches any known attractor).
##   □ Submit to backtester.
##
## STEP 2 — LLM FALLBACK (SUSPENDED until infrastructure confirmed):
##   LLM produced 0 valid novel results in last 101 generations.
##   Clone rate in recent gens is near 100% (every valid-looking result is a clone).
##   LLM fallback re-enabled only when:
##     (a) Direct injection confirmed working (at least one P-item tested successfully), AND
##     (b) Pre-backtest diff check confirmed working, AND
##     (c) LLM receives confirmed Gen 2899 YAML as baseline (not stale YAML).
##   When re-enabled: temperature=0.0, strip all non-LLM-PROMPT sections,
##   replace ALL [GEN_2899_*] tokens before sending.
##   If Attractor 1, 1b, 1c, 1d, 1e, 3, 4, 5, or 6 appears → reject, do not count as valid gen.
##
## STEP 3 — GRID SCAN FALLBACK (if direct injection fails for technical reasons):
##   Run backtester directly on target parameter range, all other params frozen.
##   Accept best result only if sharpe > 2.3219 AND trades ≥ 400.
##   Use this to confirm the TP improvement vector by scanning TP=[4.75, 4.80, 4.85, 4.90].
##   (If confirmed Gen 2899 TP is 4.80, scan [4.85, 4.90, 4.95, 5.00].)
##
## ─────────────────────────────────────────────────────────
## PRIORITY QUEUE (ODIN internal — NEVER send to LLM):
## All tests use CONFIRMED Gen 2899 champion as baseline (sharpe=2.3219, trades=1263).
## Accept improvement only if sharpe > 2.3219 AND trades ≥ 400.
## ALL items use direct injection only. LLM suspended.
##
## P0 [IMMEDIATE — blocking all other P-items]:
##   ACTION: Infrastructure repair. Complete before any P-item testing.
##   1. Confirm Gen 2899 champion YAML from actual backtested storage.
##   2. Verify direct injection pipeline uses confirmed YAML.
##   3. Verify pre-backtest diff check is active.
##   4. Add Attractor 5 (1.6865/1335) and Attractor 6 (1.7514/1345) to rejection list.
##   5. Confirm Attractor 1e pre-rejection is active.
##   6. Run one test injection of champion YAML (should produce Attractor 1e → pre-rejected).
##   7. Run one test injection of P3-CONT (TP step) to confirm pipeline executes.
##   STATUS: BLOCKING. Do not proceed to P1+ until P0 verified.
##
## P3-CONT [FIRST ACTIVE TEST — highest confidence, run immediately after P0]:
##   Context: TP widening is the most likely active improvement vector.
##   Inferred TP progression: 4.65 → 4.70 → (4.75?) → (4.80?) → NEXT
##   Test matrix (run in order, stop at first failure):
##     If confirmed Gen 2899 TP = 4.80: test 4.85 first.
##     If confirmed Gen 2899 TP = 4.75: test 4.80 first.
##     If confirmed Gen 2899 TP = 4.70: test 4.75 first (implies P3 stalled earlier).
##   Expected result per +0.05 step: -3 to -5 trades, +0.005 to +0.015 Sharpe.
##   Stop conditions:
##     □ Sharpe fails to improve (< 2.3219) → CLOSE P3-CONT, TP at optimum.
##     □ Trades drop below 1,150 → CAUTION (approaching thin-data territory), one more test.
##     □ Trades drop below 1,000 → HARD STOP P3-CONT.
##     □ TP reaches 5.50 → HARD STOP (over-optimized, too few trades expected).
##   All other params: confirmed Gen 2899 champion values.
##   Use direct injection only.
##
## P4 [ACTIVE — second priority after P3-CONT first test]:
##   rsi_short_threshold: current_value → current_value - 1
##   If confirmed rsi_short = 60: test 59.
##   If confirmed rsi_short = 59: test 58.
##   Rationale: Each -1 step reduces short entry count → fewer trades, higher selectivity.
##   Aligns with declining-trades/improving-Sharpe pattern.
##   Expected result: -2 to -5 trades, possible Sharpe improvement.
##   Floor: rsi_short ≥ 55 (below = too restrictive, Zombie risk).
##   Stop conditions:
##     □ Sharpe fails to improve → CLOSE P4, rsi_short at optimum.
##     □ Trades drop below 1,150 → CAUTION.
##   All other params: confirmed Gen 2899 champion values.
##   Use direct injection only.
##
## P2 [ACTIVE — two attempts maximum, direct injection only]:
##   stop_loss_pct: 1.91 → 1.89
##   CRITICAL: 1.90 = ZombieD (FOREVER FORBIDDEN). Jump directly to 1.89.
##   CRITICAL: Do not test 1.90 under any circumstances. Ever.
##   Floor: 1.88 (below = ZombieC territory).
##   Expected result: uncertain. Tighter SL = earlier exits = trade count unpredictable.
##   If 1.89 improves: test 1.88 (one attempt, absolute floor). Stop there regardless.
##   If 1.89 fails: CLOSE P2 permanently. SL stays at 1.91.
##   Maximum attempts: 2 (1.89, then 1.88 if first succeeds). Both via direct injection.
##   All other params: confirmed Gen 2899 champion values.
##
## P7 [ACTIVE — medium priority]:
##   rsi_period_hours: confirmed_value → confirmed_value - 2
##   If confirmed rsi_period = 22: test 20.
##   If confirmed rsi_period = 20: test 18.
##   Rationale: Faster RSI = more responsive signals = potentially better entries.
##   Warning: Below 18h RSI → high-frequency noise, Zombie risk.
##   Monitor: If trades INCREASE above 1,300 → stop (noise signal, wrong direction).
##   Monitor: If trades DECREASE below 1,150 → caution.
##   All other params: confirmed Gen 2899 champion values.
##   Use direct injection only.
##
## P6 [ACTIVE — lower priority]:
##   trend_period_hours: 48 → 50
##   Rationale: Slower trend filter may reduce false signals, improve R:R.
##   If 50 improves: test 52. If 52 improves: test 54. Stop at first failure.
##   If 50 fails: test 46 (one attempt, opposite direction only). Then close P6.
##   All other params: confirmed Gen 2899 champion values.
##   Use direct injection only.
##
## P5 [SUSPENDED — do not test]:
##   rsi_long_threshold: 37.77 → any change.
##   Frozen since Gen 1477 (>1,400 generations of stability).
##   Contamination risk far exceeds potential upside.
##   Do not resurrect until ALL other P-items exhausted and infrastructure confirmed robust.
##
## ─────────────────────────────────────────────────────────
## P-ITEM EXECUTION ORDER (post-P0):
##   Sprint 1 (Gens 3001–3010): P3-CONT first test + P4 first test.
##   Sprint 2 (Gens 3011–3020): P2 test (1.89) + P7 first test.
##   Sprint 3 (Gens 3021–3030): P6 first test + any P3-CONT continuation.
##   Compound tests: only after at least two independent P-item improvements confirmed.
##
## ─────────────────────────────────────────────────────────
## COMPOUND TESTING (only after two Px items independently confirm improvement):
##   Rule: Never combine two untested changes.
##   Rule: Each compound test = exactly TWO confirmed improvements combined.
##   Rule: Compound tests require direct injection only.
##   Rule: Accept compound test only if sharpe > best individual improvement.
##
##   Priority compound candidates (pending individual results):
##   C1: P3-CONT + P4 both improve → test combined (highest priority compound).
##   C2: P7 + P4 both improve → test combined.
##   C3: P2 + any Px improve → test P2+Px combined.
##   C4: P3-CONT + P6 both improve → test combined.
##   C5: P3-CONT + P7 both improve → test combined.
##
## ─────────────────────────────────────────────────────────
## KNOWN FAILURE FINGERPRINTS (pre-backtest validator — reject ALL of these before backtesting):
##
## Attractor 1   [STALE CLONE]:   trades=1267, sharpe=2.2657 → Gen 1592 config
## Attractor 1b  [GEN2785 CLONE]: trades=1272, sharpe=2.2828 → Gen 2785 clone
## Attractor 1c  [GEN2791 CLONE]: trades=1269, sharpe=2.2910 → Gen 2791 clone
## Attractor 1d  [GEN2813 CLONE]: trades=1268, sharpe=2.3055 → Gen 2813 clone
## Attractor 1e  [GEN2899 CLONE]: trades=1263, sharpe=2.3219 → Gen 2899 clone (nothing changed)
## Attractor 3   [RSI DRIFT]:     trades=1272, sharpe=2.2015 → RSI/param contaminated
## Attractor 4   [BROKEN YAML]:   trades=1041, sharpe=0.7753 → placeholder/invalid param
## Attractor 5   [DEGRADED-A]:    trades=1335, sharpe=1.6865 → LLM modifying stale YAML
## Attractor 6   [DEGRADED-B]:    trades=1345, sharpe=1.7514 → LLM modifying stale YAML
## Ghost Echo    [TIMEOUT-166]:   trades=1264, sharpe=2.1998 → timeout=166h used
## Zombie C      [EXTREME SL]:    trades<400                 → RSI extreme or stop<1.88
## Zombie D      [SL=1.90]:       trades≈1228, sharpe≈1.59  → stop_loss=1.90 (NEVER)
## Zombie G-adj  [TIMEOUT-155]:   trades≈888,  sharpe≈2.00  → timeout=155h used
##
## PRE-BACKTEST REJECTION RULES:
##   1. If YAML params exactly match any historical champion → reject (Attractor 1x family).
##      Implementation: diff test YAML against champion YAML. If zero diffs → reject.
##   2. If timeout_hours ≠ 159 → reject immediately.
##   3. If stop_loss_pct = 1.90 → reject immediately (ZombieD).
##   4. If stop_loss_pct < 1.88 → reject immediately (ZombieC floor).
##   5. If size_pct ≠ 25 → reject immediately.
##   6. If more than ONE parameter differs from champion YAML → reject (compound change).
##   7. If rsi_long_threshold ≠ 37.77 → reject immediately.
##   8. If leverage ≠ 2 → reject immediately.
##
## POST-BACKTEST REJECTION RULES (in addition to pre-backtest):
##   9. If result matches any known attractor fingerprint exactly → reject (stale clone).
##   10. If sharpe ≤ 2.3219 → discard (not an improvement).
##   11. If trades < 400 → reject (Zombie, below MIN_TRADES).
##
## ─────────────────────────────────────────────────────────
## FROZEN PARAMETERS (hard-reject any YAML violating these):
##   size_pct              = 25       (FOREVER)
##   timeout_hours         = 159      (FOREVER — 155=ZombieG, 166=GhostEcho, 192=STALE/WRONG)
##   max_open              = 3        (FOREVER)
##   leverage              = 2        (FOREVER)
##   fee_rate              = 0.0005   (FOREVER)
##   stop_loss_pct         ≥ 1.88     (floor — below = ZombieC territory)
##   stop_loss_pct         ≠ 1.90     (FORBIDDEN — ZombieD — NEVER TEST THIS VALUE)
##   rsi_long_threshold    = 37.77    (do not touch — frozen since Gen 1477)
##   MIN_TRADES            = 400      (correct — do not change)
##
##   ⚠ DISPLAYED YAML IS WRONG: timeout=192, SL=1.92, TP=4.65, rsi_period=24 are ALL stale.
##   ⚠ DO NOT USE DISPLAYED YAML AS BASELINE FOR ANYTHING.
##   ⚠ USE ONLY CONFIRMED GEN 2899 BACKTESTED YAML.
##
## ─────────────────────────────────────────────────────────
## LLM FAILURE RATE SUMMARY (operational awareness):
##   Clone rate (any Attractor 1x):        ~35% historical / ~60% Gens 2900-3000
##   Known-bad attractor recycling (5/6):  ~30% Gens 2900-3000 (NEW HIGH — stale YAML)
##   Zombie rate (trades<400):              ~15% historical / observed in recent