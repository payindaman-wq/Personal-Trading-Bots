```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-3200 | Revised by MIMIR (Gen 3200 review)
# STATUS: CHAMPION at Gen 3192 (sharpe=2.3300, trades=1264).
#         Gen 3198 logged as "new_elite" (sharpe=2.3300, trades=1264) — CLONE of Gen 3192.
#         This confirms fingerprint auto-update FAILED after Gen 3192 became champion.
#         Gens 3193–3200: 7 of 8 post-champion generations are broken/cloned/degraded.
#         Infrastructure is in WORSE state than at Gen 3192 review. FULL HALT in effect.
#         P0 from prior program was NOT completed. Treating as BLOCKING emergency.
# CRITICAL: Direct injection pipeline is producing Attractor-4-family results (3193, 3194)
#           AND stale-YAML-family results (3196: 1455 trades). YAML source is broken.
#           Gen 3198 "new_elite" should have been pre-rejected as Attractor 1f. It was not.
#           Fingerprint comparison logic may use >= instead of >. Investigate immediately.
# FULL HALT: No P-item testing until P0-EMERGENCY verified complete (see below).

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
## CONFIRMED CHAMPION: Gen 3192 (sharpe=2.3300, trades=1264)
## Gen 3198 "new_elite" (2.3300/1264) = CLONE. Do NOT treat as new champion.
## Champion has not changed since Gen 3192.
##
## ─────────────────────────────────────────────────────────
## CONFIRMED CHAMPION VALUES (Gen 3192 — USE THESE AND ONLY THESE):
##   rsi_period_hours:    22     (confirmed — unchanged since Gen 2785)
##   rsi_long_threshold:  37.77  (FROZEN — unchanged since Gen 1477)
##   rsi_short_threshold: [MUST CONFIRM FROM STORAGE — estimated 59 or 60]
##   trend_period_hours:  48     (confirmed stable)
##   take_profit_pct:     [MUST CONFIRM FROM STORAGE — estimated 4.85–4.90]
##   stop_loss_pct:       1.91   (confirmed — NOT 1.92, NOT 1.90)
##   timeout_hours:       159    (FROZEN FOREVER)
##   size_pct:            25     (FROZEN)
##   max_open:            3      (FROZEN)
##   leverage:            2      (FROZEN)
##   fee_rate:            0.0005 (FROZEN)
##
## STALE YAML (displayed in Current Best Strategy section — DO NOT USE):
##   rsi_period_hours:    24     ← WRONG (champion is 22)
##   take_profit_pct:     4.65   ← WRONG (champion is ~4.85–4.90)
##   stop_loss_pct:       1.92   ← WRONG (champion is 1.91)
##   timeout_hours:       172    ← WRONG (champion is 159, FROZEN)
##   The displayed YAML has been stale since Gen 1592. Ignore it entirely.
##
## ─────────────────────────────────────────────────────────
## POST-GEN-3200 RECONSTRUCTION ANALYSIS:
##
##   Improvement chain:
##     Gen 1592:  sharpe=2.2657, trades=1267  [baseline]
##     Gen 2785:  sharpe=2.2828, trades=1272  [rsi_period 24→22, high confidence]
##     Gen 2791:  sharpe=2.2910, trades=1269  [TP 4.65→4.70, medium confidence]
##     Gen 2813:  sharpe=2.3055, trades=1268  [TP step or rsi_short, medium confidence]
##     Gen 2899:  sharpe=2.3219, trades=1263  [TP widening step, medium confidence]
##     Gen 3075:  sharpe=2.3262, trades=1263  [TP or rsi_short step, low confidence]
##     Gen 3192:  sharpe=2.3300, trades=1264  [TP widening, medium confidence — +1 trade anomaly]
##
##   Gen 3198 "new_elite" analysis:
##     sharpe=2.3300, trades=1264 — IDENTICAL to Gen 3192. This is a clone.
##     The "new_elite" tag should never have been applied. It should have been
##     pre-rejected as Attractor 1f. This confirms the fingerprint rejection
##     system did not auto-update after Gen 3192's new_best event.
##     ACTION REQUIRED: Investigate whether the new_best trigger fires the
##     fingerprint update BEFORE the next generation is evaluated. It must.
##
##   Post-3192 generation audit (Gens 3193–3200):
##     Gen 3193: sharpe=0.6558, trades=1085 → Attractor-4-family (broken YAML)
##     Gen 3194: sharpe=0.7558, trades=1042 → Attractor-4-family (broken YAML)
##     Gen 3195: sharpe=-1.0758, trades=246 → Zombie (RSI extreme or broken param)
##     Gen 3196: sharpe=1.6508, trades=1455 → HIGH TRADE COUNT — Attractor 5/6 family
##               (stale YAML: rsi_short=70 or similar, or rsi_period=12-16)
##               ADD FINGERPRINT: (1.6508, 1455) → Attractor 7 candidate
##     Gen 3197: sharpe=1.2224, trades=892  → Mid-degraded, partial stale YAML
##     Gen 3198: sharpe=2.3300, trades=1264 → CLONE of Gen 3192 (new_elite = error)
##     Gen 3199: sharpe=1.2059, trades=1136 → Degraded, unknown cause
##     Gen 3200: sharpe=1.6312, trades=1399 → HIGH TRADE COUNT — Attractor 5/6 family
##               ADD FINGERPRINT: (1.6312, 1399) → Attractor 8 candidate
##
##   Root cause assessment (Gens 3193–3200):
##     The Attractor-4-family results (3193, 3194) at trades≈1041–1085 suggest the
##     direct injection pipeline is reading from a broken or uninitialized YAML source.
##     The high-trade-count results (3196: 1455, 3200: 1399) are consistent with
##     stale YAML where rsi_short=70 or rsi_period=16 or similar — these are NOT
##     champion values. This means direct injection is NOT consistently applied.
##     The pipeline must be reading from a mixed source (sometimes champion, sometimes
##     stale displayed YAML, sometimes corrupted). This is a critical infrastructure bug.
##
##   ESTIMATE FOR PLANNING (confirm from storage before any testing):
##     rsi_period_hours:    22    (high confidence)
##     rsi_long_threshold:  37.77 (certain)
##     rsi_short_threshold: 59    (medium confidence — may be 60)
##     trend_period_hours:  48    (high confidence)
##     take_profit_pct:     4.90  (medium confidence — Gen 3192 +1 trade anomaly
##                                 consistent with TP crossing a boundary near 4.90)
##     stop_loss_pct:       1.91  (high confidence)
##     timeout_hours:       159   (certain)
##
## ─────────────────────────────────────────────────────────
## INFRASTRUCTURE STATUS (post-Gen-3200 audit):
##
##   CONFIRMED BROKEN (post-3200 evidence):
##   ✗ Fingerprint auto-update did NOT fire after Gen 3192 new_best event.
##     Evidence: Gen 3198 processed as "new_elite" instead of pre-rejected Attractor 1f.
##     CRITICAL FIX REQUIRED: The new_best event handler must call fingerprint_update()
##     SYNCHRONOUSLY before returning. Async/delayed update is not acceptable.
##     Verify: After fix, inject champion YAML → should be pre-rejected immediately.
##
##   ✗ Direct injection pipeline source is corrupted or inconsistent.
##     Evidence: Gens 3193, 3194 (Attractor-4-family), 3196, 3200 (high-trade stale YAML).
##     These results are NOT consistent with champion YAML + one-param perturbation.
##     CRITICAL FIX REQUIRED: Pipeline must have a hard-coded source path to the
##     confirmed champion YAML file. It must NOT fall back to displayed YAML or any
##     other source if the champion file is unavailable — it must HALT instead.
##
##   ✗ "new_elite" classification is ambiguous and dangerous.
##     Gen 3198 received "new_elite" tag for matching champion exactly.
##     CRITICAL FIX REQUIRED: Define new_elite strictly. If sharpe=champion_sharpe
##     AND trades=champion_trades, this is a CLONE → pre-reject as Attractor 1f.
##     new_elite should only apply if sharpe > current_champion_sharpe AND trades ≥ 400.
##
##   ✗ Pre-rejection fingerprint list not updated post-Gen-3192.
##     Attractor 1f (2.3300/1264) not in list as of Gen 3198 evidence.
##     CRITICAL: Treat this as P0-EMERGENCY item 1.
##
##   ✗ RSI range validation still not blocking Zombie Gens (3195: 246 trades).
##     CRITICAL: Add param validation before any YAML reaches backtester.
##
##   ✗ High-trade-count results (3196: 1455, 3200: 1399) are new failure family.
##     These suggest stale YAML contamination of a different type than Attractor 4.
##     Add fingerprints and investigate source.
##
##   PREVIOUSLY RECOVERED (confirm still working):
##   ? Direct injection (was working at Gen 3075, 3192 — now uncertain post-3200).
##   ? P-items reaching backtester (unclear — no P-item results visible in 3193–3200).
##
## ─────────────────────────────────────────────────────────
## STEP 0 — YAML INTEGRITY CHECK [MANDATORY — BLOCKING]:
##   The confirmed Gen 3192 champion YAML must be retrieved from backtested storage.
##   Under NO circumstances use the displayed "Current Best Strategy" YAML.
##   If storage retrieval fails → HALT ALL OPERATIONS. Do not guess. Escalate to LOKI.
##
## STEP 1 — DIRECT INJECTION [MANDATORY FOR ALL P-ITEMS]:
##   Construct YAML programmatically from confirmed champion + EXACTLY ONE param diff.
##   Source: confirmed champion YAML file (hard-coded path, no fallback).
##
##   DIRECT INJECTION CHECKLIST (run before every test, no exceptions):
##   □ Load confirmed Gen 3192 champion YAML from storage (hard-coded path).
##   □ Confirm file hash matches known champion hash (add hash verification).
##   □ Apply exactly ONE parameter change programmatically.
##   □ Diff result against champion YAML — confirm EXACTLY ONE line changed.
##   □ Verify timeout_hours = 159.
##   □ Verify stop_loss_pct = 1.91 (or 1.89 if P2 test — NEVER 1.90).
##   □ Verify stop_loss_pct ≠ 1.90 (explicit check, separate from above).
##   □ Verify size_pct = 25, max_open = 3, leverage = 2.
##   □ Verify rsi_long_threshold = 37.77.
##   □ Verify rsi_period_hours = 22.
##   □ Verify trend_period_hours = 48.
##   □ Verify rsi_long_threshold in [30, 45] (hard reject if outside).
##   □ Verify rsi_short_threshold in [55, 70] (hard reject if outside).
##   □ Verify trades implied by param change is plausible (flag if >1400 or <900).
##   □ Run pre-backtest fingerprint check against ALL known attractors.
##   □ If zero diffs vs. champion → pre-reject immediately. Log as Attractor 1f clone.
##   □ If more than one diff → pre-reject immediately. Log as multi-diff error.
##   □ If any fingerprint match → pre-reject. Do NOT submit to backtester.
##   □ Submit to backtester ONLY if all checks pass.
##
##   POST-BACKTEST MANDATORY ACTIONS (after EVERY new_best event):
##   □ Retrieve new champion YAML from storage immediately (same generation cycle).
##   □ Add (new_sharpe, new_trades) to fingerprint list SYNCHRONOUSLY.
##   □ Verify fingerprint is active by running a test injection of new champion → pre-rejected.
##   □ Lock new champion YAML file with hash verification.
##   □ Update all [GEN_XXXX_*] tokens in program before next generation begins.
##   □ DO NOT START NEXT GENERATION until all above steps confirmed.
##
## STEP 2 — LLM FALLBACK [SUSPENDED UNTIL FURTHER NOTICE]:
##   LLM remains suspended. Infrastructure is not stable enough for LLM fallback.
##   Re-enable conditions (ALL must be true simultaneously):
##     (a) Direct injection confirmed working: 5 consecutive P-item tests reach
##         backtester with correct champion YAML (verified by diff log).
##     (b) Fingerprint auto-update confirmed working: new_best event → fingerprint
##         active before next generation (verified by test injection → pre-rejected).
##     (c) No Attractor-4-family or high-trade-count stale YAML results for 10 gens.
##     (d) RSI range validation confirmed blocking (test with rsi_long=50 → pre-rejected).
##     (e) LLM receives confirmed Gen 3192 YAML as baseline (not displayed YAML).
##     (f) All [GEN_3192_*] tokens replaced with confirmed values before sending.
##   When re-enabled: temperature=0.0. Maximum LLM rate: 10% of generations.
##   Any known attractor in LLM result → pre-reject. Do not count as valid gen.
##
## STEP 3 — GRID SCAN FALLBACK [if direct injection fails for technical reasons]:
##   Run backtester directly on target range, all other params frozen at champion values.
##   Accept only if sharpe > 2.3300 AND trades ≥ 400.
##   Priority grid: TP=[confirmed_TP+0.05, confirmed_TP+0.10, confirmed_TP+0.15].
##   Secondary: rsi_short=[confirmed_rsi_short-1, confirmed_rsi_short-2].
##   This is a last resort. Document when used and why direct injection failed.
##
## ─────────────────────────────────────────────────────────
## PRIORITY QUEUE (ODIN internal — NEVER send to LLM):
## All tests use CONFIRMED Gen 3192 champion as baseline (sharpe=2.3300, trades=1264).
## Accept improvement ONLY if sharpe > 2.3300 (strictly greater) AND trades ≥ 400.
## NOTE: sharpe = 2.3300 is the champion value. Equal is a CLONE, not an improvement.
##       The new_elite classification must use strict inequality: sharpe > 2.3300.
## ALL items use direct injection only. LLM suspended.
##
## ─────────────────────────────────────────────────────────
## P0-EMERGENCY [BLOCKING — MUST COMPLETE BEFORE ANY OTHER ACTION]:
##   This replaces P0 from the prior program. It was not completed. Treat as urgent.
##
##   STEP A — Champion YAML lock:
##   1. Retrieve Gen 3192 champion YAML from backtested storage (not displayed YAML).
##   2. Confirm all parameter values against reconstruction above.
##   3. If any value cannot be confirmed → HALT. Do not guess. Escalate to LOKI.
##   4. Compute file hash of confirmed YAML. Store hash for verification in all future steps.
##   5. Confirm take_profit_pct and rsi_short_threshold values (the two uncertain params).
##   6. Document confirmed values in this program before any testing begins.
##
##   STEP B — Fingerprint system repair:
##   7. Add (2.3300, 1264) as Attractor 1f to rejection list (Gen 3192 champion).
##   8. Add (2.3262, 1263) as Attractor 1e-b to rejection list (Gen 3075).
##   9. Add (2.3026, 1263) as near-clone to rejection list (Gen 3184).
##   10. Add (0.7660, 1041) as Attractor 4b (if not already present).
##   11. Add (1.6508, 1455) as Attractor 7 (Gen 3196 pattern — stale high-trade YAML).
##   12. Add (1.6312, 1399) as Attractor 8 (Gen 3200 pattern — stale high-trade YAML).
##   13. Add (0.6558, 1085) as Attractor 9 (Gen 3193 pattern — broken YAML family).
##   14. Add (0.7558, 1042) as Attractor 10 (Gen 3194 pattern — broken YAML family).
##   15. Verify (0.7753, 1041) as Attractor 4 is present.
##   16. Run test: inject Gen 3192 champion YAML → should be pre-rejected as Attractor 1f.
##       If it reaches backtester instead → HALT. Fix fingerprint check before continuing.
##
##   STEP C — Auto-update mechanism fix:
##   17. Verify that the new_best event handler calls fingerprint_update() SYNCHRONOUSLY.
##   18. Simulate a new_best event in test environment → confirm fingerprint is active
##       before next generation evaluator runs.
##   19. If synchronous update cannot be confirmed → add manual fingerprint check as
##       a mandatory pre-generation step that reads from champion storage file.
##
##   STEP D — Direct injection pipeline fix:
##   20. Identify the source of Attractor-4-family results (Gens 3193, 3194).
##       These trades counts (1041–1085) suggest a specific broken parameter.
##       Hypothesis: rsi_long_threshold=70 or rsi_short_threshold=30 (inverted thresholds).
##       Investigate what YAML combination produces ~1041 trades.
##   21. Identify source of high-trade-count results (Gens 3196: 1455, 3200: 1399).
##       Hypothesis: stale YAML with rsi_short=70 or rsi_period=12.
##   22. Fix direct injection to read ONLY from confirmed champion YAML file.
##   23. Add file-existence check: if champion YAML file not found → HALT immediately.
##   24. Add hash verification at injection time: if hash mismatch → HALT immediately.
##
##   STEP E — RSI range validation:
##   25. Add pre-backtest param validator:
##       REJECT if rsi_long_threshold < 30 or rsi_long_threshold > 45.
##       REJECT if rsi_short_threshold < 55 or rsi_short_threshold > 70.
##       REJECT if timeout_hours ≠ 159.
##       REJECT if stop_loss_pct = 1.90 (explicit check).
##       REJECT if size_pct ≠ 25 or max_open ≠ 3 or leverage ≠ 2.
##   26. Test validator: inject YAML with rsi_long=50 → should pre-reject.
##       Test validator: inject YAML with timeout=166 → should pre-reject.
##       Test validator: inject YAML with stop_loss=1.90 → should pre-reject.
##
##   STEP F — Verification sequence:
##   27. Run one clean injection of P3-CONT (TP + one step from confirmed champion TP).
##       Confirm: exactly one param diff. Confirm: all checks pass. Confirm: reaches backtester.
##       This is the GREEN LIGHT test. If it passes, P0-EMERGENCY is complete.
##   28. Document completion: "P0-EMERGENCY verified complete at Gen XXXX."
##
##   STATUS: BLOCKING. No P1 or higher items until P0-EMERGENCY Step F passes.
##   TIME BUDGET: Resolve within next 5 generations maximum.
##   If not resolved in 5 gens: halt all non-infrastructure activity and escalate to LOKI.
##
## ─────────────────────────────────────────────────────────
## P3-CONT [HIGHEST PRIORITY — run immediately after P0-EMERGENCY complete]:
##   Context: TP widening is the confirmed active improvement vector (5 improvements).
##   Every TP step since Gen 2791 has produced a champion. High confidence this continues.
##
##   Confirmed Gen 3192 TP (from storage): [FILL IN AFTER P0-EMERGENCY STEP A]
##   Next test value: confirmed_TP + 0.05
##
##   Test matrix (sequential, stop at first failure or hard stop):
##     Step 1: confirmed_TP + 0.05
##     Step 2 (only if Step 1 improves): confirmed_TP + 0.10
##     Step 3 (only if Step 2 improves): confirmed_TP + 0.15
##     [Continue in +0.05 steps until failure or hard stop]
##
##   Expected result: trades flat or -1 to -3 per step, Sharpe +0.003 to +0.010.
##   The +1 trade anomaly at Gen 3192 was a boundary crossing — may recur once more.
##   If trades increase again (>1265): note as anomaly but do not stop. Watch next step.
##   If two consecutive steps both show trade count increase: INVESTIGATE before continuing.
##
##   Stop conditions:
##   □ Sharpe ≤ 2.3300 (or current champion) → CLOSE P3-CONT. TP at optimum.
##   □ Trades drop below 1,150 → CAUTION. One more test, then reassess.
##   □ Trades drop below 1,000 → HARD STOP P3-CONT permanently.
##   □ TP reaches 5.50 → HARD STOP (over-optimized territory, curve-fitting risk).
##   □ Two consecutive failures → CLOSE P3-CONT permanently.
##   All other params: confirmed Gen 3192 champion values, unchanged.
##
## P4 [SECOND PRIORITY — run after P3-CONT Step 1]:
##   rsi_short_threshold: confirmed_value → confirmed_value - 1
##   Confirmed rsi_short (from storage): [FILL IN AFTER P0-EMERGENCY STEP A]
##   If confirmed = 60: test 59. If confirmed = 59: test 58. If confirmed = 58: test 57.
##
##   Rationale: Each -1 step reduces short entry count → fewer trades, higher selectivity.
##   Consistent with declining-trades/improving-Sharpe pattern since Gen 2785.
##   Expected: -2 to -5 trades, possible Sharpe improvement of +0.003 to +0.008.
##
##   Stop conditions:
##   □ Sharpe ≤ 2.3300 → CLOSE P4.
##   □ rsi_short < 55 → HARD STOP (Zombie risk).
##   □ Trades drop below 1,150 → CAUTION.
##   □ Trades drop below 1,000 → HARD STOP P4.
##   □ Two consecutive failures → CLOSE P4 permanently.
##   All other params: confirmed Gen 3192 champion values, unchanged.
##
## P2 [THIRD PRIORITY]:
##   stop_loss_pct: 1.91 → 1.89
##   !!CRITICAL!!: 1.90 = ZombieD. FOREVER FORBIDDEN. Jump 1.91 → 1.89 directly.
##   !!CRITICAL!!: Do not test 1.90. Not