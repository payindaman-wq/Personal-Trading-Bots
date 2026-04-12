```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-3340 | Revised by MIMIR (Gen 3340 review)
# STATUS: NEW CHAMPION at Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%).
#         Prior champion Gen 3192 (sharpe=2.3300, trades=1264) is SUPERSEDED.
#         Gen 3325 logged as "new_elite" (sharpe=2.3295, trades=1266) — near-clone, NOT champion.
#         P0-EMERGENCY from prior program was NOT completed (4th review cycle failure).
#         Fingerprint for Gen 3192 (2.3300/1264) was still active as "discarded" at Gen 3338.
#         This confirms fingerprint auto-update has NEVER been fixed. FULL HALT in effect.
#         RSI range validation is still NOT blocking zombies (4 zombie gens in last 20).
#         Gen 3339 produced 1706 trades — new worst-case stale YAML. Must be fingerprinted.
# CRITICAL: P0-EMERGENCY must complete within 3 generations or LOKI escalation is mandatory.
#           No P-item testing until P0-EMERGENCY Step F verified complete.
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
## CONFIRMED CHAMPION: Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
## Prior champion Gen 3192 (2.3300/1264) is SUPERSEDED. Do NOT use Gen 3192 as baseline.
## Gen 3325 "new_elite" (2.3295/1266) = near-clone of prior champion. NOT accepted.
## Gen 3338 "discarded" (2.3300/1264) = old champion clone. Fingerprint was absent. BUG.
##
## ─────────────────────────────────────────────────────────
## CONFIRMED CHAMPION VALUES (Gen 3340 — USE THESE AND ONLY THESE):
##   rsi_period_hours:    22     (confirmed — unchanged since Gen 2785)
##   rsi_long_threshold:  37.77  (FROZEN — unchanged since Gen 1477)
##   rsi_short_threshold: [MUST CONFIRM FROM STORAGE — estimated 59 or 60]
##   trend_period_hours:  48     (confirmed stable)
##   take_profit_pct:     [MUST CONFIRM FROM STORAGE — estimated 4.90–5.05 range]
##                        NOTE: Gen 3340 produced +1 trade vs Gen 3192, consistent with
##                        TP boundary crossing. Estimated 1–2 steps of +0.05 beyond
##                        Gen 3192 TP (which was itself estimated at 4.85–4.90).
##                        Range estimate: 4.90–5.05. MUST confirm from storage.
##   stop_loss_pct:       1.91   (confirmed — NOT 1.92, NOT 1.90)
##   timeout_hours:       159    (FROZEN FOREVER)
##   size_pct:            25     (FROZEN)
##   max_open:            3      (FROZEN)
##   leverage:            2      (FROZEN)
##   fee_rate:            0.0005 (FROZEN)
##
## STALE YAML (displayed in Current Best Strategy section — DO NOT USE):
##   rsi_period_hours:    24     ← WRONG (champion is 22)
##   take_profit_pct:     4.65   ← WRONG (champion is ~4.90–5.05)
##   stop_loss_pct:       1.92   ← WRONG (champion is 1.91)
##   timeout_hours:       176    ← WRONG (champion is 159, FROZEN)
##   The displayed YAML has been stale since Gen 1592. IGNORE IT ENTIRELY.
##   Under NO circumstances use displayed YAML as a source for any injection.
##
## ─────────────────────────────────────────────────────────
## POST-GEN-3340 RECONSTRUCTION ANALYSIS:
##
##   Full improvement chain:
##     Gen 1:     sharpe=1.0218, trades=822   [baseline]
##     Gen 1477:  sharpe=2.2496, trades=1267  [rsi_long=37.77, high confidence]
##     Gen 1592:  sharpe=2.2657, trades=1267  [structural improvement]
##     Gen 2785:  sharpe=2.2828, trades=1272  [rsi_period 24→22, high confidence]
##     Gen 2791:  sharpe=2.2910, trades=1269  [TP 4.65→4.70, medium confidence]
##     Gen 2813:  sharpe=2.3055, trades=1268  [TP step, medium confidence]
##     Gen 2899:  sharpe=2.3219, trades=1263  [TP widening step, medium confidence]
##     Gen 3075:  sharpe=2.3262, trades=1263  [TP step, low confidence]
##     Gen 3192:  sharpe=2.3300, trades=1264  [TP widening, medium confidence — +1 trade]
##     Gen 3340:  sharpe=2.3494, trades=1265  [TP widening, high confidence — +1 trade again]
##
##   Gen 3340 analysis:
##     +0.0194 Sharpe gain. Largest single-step gain since Gen 2813 (+0.0145).
##     +1 trade anomaly recurred (1264→1265) — second consecutive boundary crossing.
##     Two consecutive +1 trade anomalies is notable. Per prior guidance: watch next step.
##     If next TP step ALSO shows +1 or more trades: INVESTIGATE before continuing P3-CONT.
##     Win rate improved: 40.0% → 40.1%. Consistent with TP widening capturing better exits.
##
##   Gen 3325 "new_elite" analysis:
##     sharpe=2.3295, trades=1266 — below Gen 3192 champion (2.3300). Not an improvement.
##     The "new_elite" tag is incorrect by strict definition (sharpe < 2.3300 at time of eval).
##     Should have been classified "discarded". Add (2.3295, 1266) to fingerprint list.
##     This result (trades=1266, +2 vs Gen 3192) suggests a slight TP decrease from Gen 3192
##     OR a minor RSI shift. Do not investigate further.
##
##   Gen 3339 analysis (1706 trades — new worst-case):
##     sharpe=-0.7496, win_rate=39.7%, trades=1706. Highest trade count ever seen.
##     Hypothesis: rsi_short=50 or rsi_period=6 or both. Extremely permissive thresholds.
##     This is a new stale-YAML family. Add (−0.7496, 1706) as Attractor 11.
##     Must investigate what YAML produces 1706 trades. Likely rsi_short much lower than 55.
##
##   Zombie rate in last 20 gens: 4/20 = 20%. Unacceptable. RSI validation not working.
##     Gen 3321: 192 trades. Gen 3332: 26 trades. Gen 3335: 343 trades. Gen 3337: 29 trades.
##     Zombies at 26 and 29 trades suggest rsi thresholds are inverted or extreme.
##     This MUST be fixed by RSI range validation before any P-item testing.
##
##   ESTIMATE FOR PLANNING (confirm from storage before any testing):
##     rsi_period_hours:    22    (high confidence)
##     rsi_long_threshold:  37.77 (certain)
##     rsi_short_threshold: 59    (medium confidence — may be 60)
##     trend_period_hours:  48    (high confidence)
##     take_profit_pct:     4.90–5.05 (medium confidence — confirm from storage)
##     stop_loss_pct:       1.91  (high confidence)
##     timeout_hours:       159   (certain)
##
## ─────────────────────────────────────────────────────────
## INFRASTRUCTURE STATUS (post-Gen-3340 audit):
##
##   CONFIRMED BROKEN (persistent failures across 4 review cycles):
##   ✗ Fingerprint auto-update NEVER successfully fixed.
##     Evidence: Gen 3338 (2.3300/1264) processed as "discarded" — not pre-rejected.
##     This means Gen 3192's fingerprint (2.3300/1264) was absent from rejection list at Gen 3338.
##     Evidence: Gen 3323 (2.3300/1264) and Gen 3331 (2.3300/1264) also processed as "discarded".
##     The new champion Gen 3340 (2.3494/1265) fingerprint MUST be added synchronously NOW.
##     CRITICAL FIX REQUIRED: new_best event → fingerprint_update() SYNCHRONOUSLY, blocking.
##     Verify: inject Gen 3340 YAML → pre-rejected immediately. If not → HALT.
##
##   ✗ RSI range validation still NOT blocking zombie generations.
##     Evidence: Gen 3332 (26 trades), Gen 3337 (29 trades) — extreme RSI values.
##     CRITICAL FIX REQUIRED: Hard validator before backtester. See STEP E below.
##     20% zombie rate in last 20 gens is unacceptable and wastes backtester capacity.
##
##   ✗ Stale YAML contamination producing high-trade-count attractors (still active).
##     Evidence: Gen 3329 (1364), Gen 3330 (1309), Gen 3333 (1340), Gen 3339 (1706).
##     Gen 3339 (1706) is new worst-case. Suggests rsi_short much lower than 55 in stale YAML.
##     CRITICAL FIX REQUIRED: Direct injection must read ONLY from confirmed champion file.
##
##   ✗ "new_elite" classification applied to Gen 3325 (2.3295/1266 < prior champion 2.3300).
##     Classification logic error: new_elite should require sharpe > current_champion_sharpe.
##     CRITICAL FIX REQUIRED: new_elite if and only if sharpe > champion_sharpe (strict >).
##
##   PREVIOUSLY BROKEN (status uncertain — reverify):
##   ? Direct injection pipeline (Attractor-4-family absent from last 20 gens — possible fix).
##     However, high-trade-count stale YAML still appearing. Pipeline not fully clean.
##   ? P-items reaching backtester (no confirmed P-item results visible in last 20 gens).
##
##   NEWLY CONFIRMED WORKING:
##   ✓ Gen 3340 genuine improvement reached backtester and was accepted as new champion.
##     This is the only confirmed working element. Do not assume anything else is fixed.
##
## ─────────────────────────────────────────────────────────
## STEP 0 — YAML INTEGRITY CHECK [MANDATORY — BLOCKING]:
##   The confirmed Gen 3340 champion YAML must be retrieved from backtested storage.
##   Under NO circumstances use the displayed "Current Best Strategy" YAML.
##   If storage retrieval fails → HALT ALL OPERATIONS. Do not guess. Escalate to LOKI.
##
## STEP 1 — DIRECT INJECTION [MANDATORY FOR ALL P-ITEMS]:
##   Construct YAML programmatically from confirmed champion + EXACTLY ONE param diff.
##   Source: confirmed champion YAML file (hard-coded path, no fallback).
##
##   DIRECT INJECTION CHECKLIST (run before every test, no exceptions):
##   □ Load confirmed Gen 3340 champion YAML from storage (hard-coded path).
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
##   □ EXTRA CHECK: Verify trades implied ≠ 1706 or close (flag if >1500 — new worst-case).
##   □ Run pre-backtest fingerprint check against ALL known attractors.
##   □ If zero diffs vs. champion → pre-reject immediately. Log as Gen 3340 clone.
##   □ If more than one diff → pre-reject immediately. Log as multi-diff error.
##   □ If any fingerprint match → pre-reject. Do NOT submit to backtester.
##   □ Submit to backtester ONLY if all checks pass.
##
##   POST-BACKTEST MANDATORY ACTIONS (after EVERY new_best event):
##   □ Retrieve new champion YAML from storage immediately (same generation cycle).
##   □ Add (new_sharpe, new_trades) to fingerprint list SYNCHRONOUSLY (blocking call).
##   □ Verify fingerprint is active: inject new champion → pre-rejected immediately.
##      If not pre-rejected → HALT. Do not start next generation.
##   □ Lock new champion YAML file with hash verification.
##   □ Update ALL [GEN_XXXX_*] tokens in program before next generation begins.
##   □ DO NOT START NEXT GENERATION until all above steps confirmed complete.
##   □ Log: "Post-new_best fingerprint verified at Gen XXXX. New champion locked."
##
## STEP 2 — LLM FALLBACK [SUSPENDED UNTIL FURTHER NOTICE]:
##   LLM remains suspended. Infrastructure not stable. 20% zombie rate confirms this.
##   Re-enable conditions (ALL must be true simultaneously):
##     (a) Direct injection confirmed working: 5 consecutive P-item tests reach
##         backtester with correct champion YAML (verified by diff log).
##     (b) Fingerprint auto-update confirmed working: new_best event → fingerprint
##         active before next generation (verified by test injection → pre-rejected).
##     (c) No Attractor-4-family or high-trade-count stale YAML results for 10 gens.
##     (d) RSI range validation confirmed blocking zombies (test with rsi_long=50 → pre-rejected).
##         AND confirmed blocking (test with rsi_short=40 → pre-rejected).
##     (e) LLM receives confirmed Gen 3340 YAML as baseline (not displayed YAML).
##     (f) All [GEN_3340_*] tokens replaced with confirmed values before sending.
##     (g) Zero zombie generations (trades < 400) for 10 consecutive gens.
##   When re-enabled: temperature=0.0. Maximum LLM rate: 10% of generations.
##   Any known attractor in LLM result → pre-reject. Do not count as valid gen.
##
## STEP 3 — GRID SCAN FALLBACK [if direct injection fails for technical reasons]:
##   Run backtester directly on target range, all other params frozen at champion values.
##   Accept only if sharpe > 2.3494 AND trades ≥ 400.
##   Priority grid: TP=[confirmed_TP+0.05, confirmed_TP+0.10, confirmed_TP+0.15].
##   Secondary: rsi_short=[confirmed_rsi_short-1, confirmed_rsi_short-2].
##   This is a last resort. Document when used and why direct injection failed.
##
## ─────────────────────────────────────────────────────────
## PRIORITY QUEUE (ODIN internal — NEVER send to LLM):
## All tests use CONFIRMED Gen 3340 champion as baseline (sharpe=2.3494, trades=1265).
## Accept improvement ONLY if sharpe > 2.3494 (strictly greater) AND trades ≥ 400.
## NOTE: sharpe = 2.3494 is the champion value. Equal is a CLONE, not an improvement.
##       The new_elite classification must use strict inequality: sharpe > 2.3494.
##       new_elite should ONLY apply if sharpe > 2.3494. Any equal result = clone = pre-reject.
## ALL items use direct injection only. LLM suspended.
##
## ─────────────────────────────────────────────────────────
## P0-EMERGENCY [BLOCKING — MUST COMPLETE BEFORE ANY OTHER ACTION]:
##   THIS IS THE FOURTH REVIEW CYCLE WITH THIS EMERGENCY ACTIVE.
##   If not completed within 3 generations from Gen 3340: MANDATORY LOKI ESCALATION.
##   Log: "P0-EMERGENCY not completed by Gen [3340+3]. Escalating to LOKI per program rules."
##
##   STEP A — Champion YAML lock:
##   1. Retrieve Gen 3340 champion YAML from backtested storage (not displayed YAML).
##   2. Confirm all parameter values against reconstruction estimates above.
##   3. Specifically confirm: take_profit_pct (estimated 4.90–5.05) and rsi_short_threshold
##      (estimated 59 or 60). These are the two uncertain parameters. MUST be confirmed.
##   4. If any value cannot be confirmed → HALT. Do not guess. Escalate to LOKI.
##   5. Compute file hash of confirmed YAML. Store hash for verification in all future steps.
##   6. Document confirmed values in this program before any testing begins.
##   7. Supersede all Gen 3192 champion references with Gen 3340 confirmed values.
##
##   STEP B — Fingerprint system repair:
##   8.  Add (2.3494, 1265) as Attractor 1g to rejection list (Gen 3340 champion — URGENT).
##   9.  Add (2.3300, 1264) as Attractor 1f to rejection list (Gen 3192 — was never added).
##   10. Add (2.3295, 1266) as Attractor 1f-near to rejection list (Gen 3325 near-clone).
##   11. Add (2.3262, 1263) as Attractor 1e-b to rejection list (Gen 3075).
##   12. Add (2.3026, 1263) as near-clone to rejection list (Gen 3184).
##   13. Add (0.7660, 1041) as Attractor 4b (if not already present).
##   14. Add (1.6508, 1455) as Attractor 7 (Gen 3196 — stale high-trade YAML).
##   15. Add (1.6312, 1399) as Attractor 8 (Gen 3200 — stale high-trade YAML).
##   16. Add (0.6558, 1085) as Attractor 9 (Gen 3193 — broken YAML family).
##   17. Add (0.7558, 1042) as Attractor 10 (Gen 3194 — broken YAML family).
##   18. Add (−0.7496, 1706) as Attractor 11 (Gen 3339 — extreme stale YAML, new worst-case).
##   19. Verify (0.7753, 1041) as Attractor 4 is present.
##   20. Run test: inject Gen 3340 champion YAML → should be pre-rejected as Attractor 1g.
##       If it reaches backtester instead → HALT. Fix fingerprint check before continuing.
##   21. Run test: inject Gen 3192 YAML (2.3300/1264) → should be pre-rejected as Attractor 1f.
##       If it reaches backtester → HALT. Both tests must pass before proceeding.
##
##   STEP C — Auto-update mechanism fix:
##   22. Verify that the new_best event handler calls fingerprint_update() SYNCHRONOUSLY.
##       "Synchronously" means: fingerprint is queryable BEFORE the handler returns.
##       Async, queued, or delayed updates are NOT acceptable.
##   23. Simulate a new_best event in test environment → confirm fingerprint is active
##       before next generation evaluator runs. Log confirmation with timestamp.
##   24. If synchronous update cannot be confirmed → add MANDATORY PRE-GENERATION step:
##       Read champion fingerprint from storage file at the START of every generation.
##       This is a fallback, not a substitute for fixing the async bug.
##   25. Add explicit log: "Fingerprint for (sharpe, trades) active at timestamp T."
##       This log must appear BEFORE next generation evaluation begins.
##
##   STEP D — Direct injection pipeline fix:
##   26. Identify source of stale YAML producing high-trade-count results.
##       Gen 3339 (1706 trades) suggests rsi_short≈50 or rsi_period≈6 in stale YAML.
##       Gen 3329 (1364), Gen 3330 (1309), Gen 3333 (1340) suggest rsi_short≈65–68.
##       These are different stale YAML families. Both sources must be identified and blocked.
##   27. Fix direct injection to read ONLY from confirmed champion YAML file (hard-coded path).
##   28. Add file-existence check: if champion YAML file not found → HALT immediately.
##       Do NOT fall back to displayed YAML. Do NOT fall back to any other file. HALT only.
##   29. Add hash verification at injection time: if hash mismatch → HALT immediately.
##   30. Add source-path logging: every injection must log which file it read from.
##
##   STEP E — RSI range validation (URGENT — 20% zombie rate):
##   31. Add pre-backtest param validator with hard rejects:
##       REJECT if rsi_long_threshold < 30 or rsi_long_threshold > 45.
##       REJECT if rsi_short_threshold < 55 or rsi_short_threshold > 70.
##       REJECT if timeout_hours ≠ 159.
##       REJECT if stop_loss_pct = 1.90 (explicit check — ZombieD zone).
##       REJECT if size_pct ≠ 25 or max_open ≠ 3 or leverage ≠ 2.
##       REJECT if rsi_period_hours < 12 or rsi_period_hours > 36.
##       REJECT if trades_estimate > 1500 (use simple heuristic if available).
##   32. Test validator with each of the following — ALL must be pre-rejected:
##       □ rsi_long = 50 → REJECT (too high)
##       □ rsi_long = 25 → REJECT (too low)
##       □ rsi_short = 40 → REJECT (too low — would produce extreme stale YAML results)
##       □ rsi_short = 75 → REJECT (too high)
##       □ timeout = 166 → REJECT (wrong value)
##       □ stop_loss = 1.90 → REJECT (ZombieD)
##       □ rsi_period = 6 → REJECT (too low — likely source of 1706-trade zombie)
##   33. All 7 tests must pass before P0-EMERGENCY is considered complete.
##
##   STEP F — Verification sequence (GREEN LIGHT test):
##   34. Run one clean injection of P3-CONT Step 1 (confirmed_Gen3340_TP + 0.05).
##       Confirm: source file is confirmed Gen 3340 champion YAML.
##       Confirm: exactly one param diff (take_profit_pct only).
##       Confirm: all checklist items pass.
##       Confirm: all validator checks pass.
##       Confirm: fingerprint check passes (not a known attractor).
##       Confirm: reaches backtester with correct YAML.
##       Log result. If sharpe > 2.3494 AND trades ≥ 400 → new champion. Update everything.
##   35. Document: "P0-EMERGENCY verified complete at Gen XXXX."