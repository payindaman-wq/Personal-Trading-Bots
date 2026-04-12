```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-3400 | Revised by MIMIR (Gen 3400 review)
# STATUS: CHAMPION UNCHANGED at Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%).
#         Gen 3382 logged as "new_elite" (sharpe=2.3330/1270) — below champion. NOT accepted.
#         Gen 3400 logged as "new_elite" (sharpe=2.3428/1265) — below champion. NOT accepted.
#         Gen 3400 is significant: same trades as champion, sharpe only -0.0066 below.
#         Hypothesis: Gen 3400 = confirmed_TP - 0.05. Confirms current TP is local maximum.
# CRITICAL: P0-EMERGENCY deadline was Gen 3343 (3 gens from Gen 3340). NOW AT GEN 3400.
#           P0-EMERGENCY is 57 generations overdue. LOKI ESCALATION IS MANDATORY NOW.
#           Log: "P0-EMERGENCY not completed by Gen 3343. Escalating to LOKI per program rules."
#           No P-item testing until P0-EMERGENCY Step F verified complete.
# FULL HALT: No P-item testing until P0-EMERGENCY verified complete.
# NEW CRITICAL: Attractor (0.5854, 1010, 34.5%) appeared 5 times in last 20 gens (25% waste).
#               This MUST be added to fingerprint list and pre-rejected before any other action.
# NEW CRITICAL: (−0.9664, 179, 30.2%) appeared twice (Gens 3383 and 3389) — clone not rejected.
#               Confirms fingerprint pre-rejection is NOT RUNNING for low_trades results either.

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
## All prior champions are SUPERSEDED. Do NOT use any prior champion as baseline.
## Gen 3382 "new_elite" (2.3330/1270) = below champion. Discarded.
## Gen 3394 "discarded" (2.3295/1266) = near-clone family. Discarded.
## Gen 3400 "new_elite" (2.3428/1265) = below champion. Significant — see analysis below.
##
## ─────────────────────────────────────────────────────────
## CONFIRMED CHAMPION VALUES (Gen 3340 — USE THESE AND ONLY THESE):
##   rsi_period_hours:    22     (confirmed — unchanged since Gen 2785)
##   rsi_long_threshold:  37.77  (FROZEN — unchanged since Gen 1477)
##   rsi_short_threshold: [MUST CONFIRM FROM STORAGE — estimated 59 or 60]
##   trend_period_hours:  48     (confirmed stable)
##   take_profit_pct:     [MUST CONFIRM FROM STORAGE — estimated 4.90–5.05 range]
##                        NOTE: Gen 3400 (2.3428/1265, same trade count as champion)
##                        is consistent with TP = confirmed_TP - 0.05 (one step below).
##                        This strengthens the estimate: confirmed_TP is a local maximum.
##                        Gen 3382 (2.3330/1270, +5 trades) suggests a different family
##                        (possibly TP too low causing more timeout exits → more trades).
##                        Confirmed estimate range remains: 4.90–5.05. MUST confirm from storage.
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
##   Under NO circumstances use displayed YAML as source for any injection.
##
## ─────────────────────────────────────────────────────────
## POST-GEN-3400 RECONSTRUCTION ANALYSIS:
##
##   Full improvement chain (unchanged — Gen 3340 remains champion):
##     Gen 1:     sharpe=1.0218, trades=822   [baseline]
##     Gen 1477:  sharpe=2.2496, trades=1267  [rsi_long=37.77, high confidence]
##     Gen 1592:  sharpe=2.2657, trades=1267  [structural improvement]
##     Gen 2785:  sharpe=2.2828, trades=1272  [rsi_period 24→22, high confidence]
##     Gen 2791:  sharpe=2.2910, trades=1269  [TP 4.65→4.70, medium confidence]
##     Gen 2813:  sharpe=2.3055, trades=1268  [TP step, medium confidence]
##     Gen 2899:  sharpe=2.3219, trades=1263  [TP widening step, medium confidence]
##     Gen 3075:  sharpe=2.3262, trades=1263  [TP step, low confidence]
##     Gen 3192:  sharpe=2.3300, trades=1264  [TP widening, medium confidence]
##     Gen 3340:  sharpe=2.3494, trades=1265  [TP widening, high confidence — CHAMPION]
##
##   Last 20 generation analysis (Gens 3381–3400):
##
##   CRITICAL ATTRACTOR IDENTIFIED: (0.5854, 1010, 34.5%)
##     Appeared at: Gen 3381, Gen 3387, Gen 3390, Gen 3392, Gen 3393 — FIVE TIMES.
##     25% of all backtester capacity in last 20 gens wasted on this single attractor.
##     This fingerprint was NEVER added to the rejection list. Add IMMEDIATELY as Attractor 12.
##     Source: likely stale YAML with rsi_long=37.77 but wrong TP/SL/period combination.
##     MUST be pre-rejected before any other work proceeds.
##
##   CRITICAL CLONE IDENTIFIED: (−0.9664, 179, 30.2%)
##     Appeared at: Gen 3383 AND Gen 3389 — identical results, not pre-rejected.
##     Confirms fingerprint pre-rejection is NOT running for low_trades results.
##     Fingerprint check must cover ALL results, not only those above MIN_TRADES.
##     Add (−0.9664, 179) as Attractor 13.
##
##   OTHER NOTABLE RESULTS (last 20 gens):
##     Gen 3382: (2.3330, 1270) — new_elite, below champion. +5 trades suggests TP too low
##               OR rsi_short slightly lower (more signals, more trades). Add to fingerprint.
##     Gen 3394: (2.3295, 1266) — discarded. Near-clone family. Add to fingerprint.
##     Gen 3400: (2.3428, 1265) — new_elite, below champion. Same trade count as champion.
##               HIGH SIGNIFICANCE: If this is confirmed_TP - 0.05, it confirms the current
##               TP is the local maximum and confirmed_TP + 0.05 is the correct next test.
##               Add to fingerprint as Attractor 1h.
##     Gen 3388: (1.6934, 1450) — stale YAML, high trade count. Different family from Gen 3339.
##               Add as Attractor 14.
##     Gen 3391: (2.0227, 1320) — stale YAML, elevated trade count. Add as Attractor 15.
##     Gen 3398: (−1.4023, 424) — passed MIN_TRADES but deeply negative. Add as Attractor 16.
##               424 trades at −1.4023 Sharpe suggests inverted signals (rsi_long > rsi_short).
##
##   ZOMBIE ANALYSIS (last 20 gens):
##     Gen 3383: 179 trades [low_trades]
##     Gen 3389: 179 trades [low_trades] ← CLONE OF Gen 3383
##     Zombie rate: 2/20 = 10%. Improved from 20% but still unacceptable.
##     RSI range validation appears to have blocked some extremes but not the 179-trade family.
##     Note: 179 trades suggests rsi_long and rsi_short are inverted or very close together.
##     Add explicit check: REJECT if rsi_long_threshold >= rsi_short_threshold - 10.
##     (i.e., the gap between thresholds must be at least 10 points to prevent near-inversion)
##
##   ESTIMATE FOR PLANNING (confirm from storage before any testing):
##     rsi_period_hours:    22    (high confidence)
##     rsi_long_threshold:  37.77 (certain)
##     rsi_short_threshold: 59    (medium confidence — may be 60)
##     trend_period_hours:  48    (high confidence)
##     take_profit_pct:     4.90–5.05 (medium confidence — Gen 3400 analysis supports this)
##     stop_loss_pct:       1.91  (high confidence)
##     timeout_hours:       159   (certain)
##
## ─────────────────────────────────────────────────────────
## INFRASTRUCTURE STATUS (post-Gen-3400 audit):
##
##   CONFIRMED BROKEN (persistent failures — now 5 review cycles with same failures):
##   ✗ Fingerprint auto-update NEVER successfully fixed.
##     Evidence (new): Gen 3400 (2.3428/1265) classified "new_elite" and processed.
##     Evidence (new): (0.5854/1010) appeared 5 times without pre-rejection.
##     Evidence (new): (−0.9664/179) appeared twice without pre-rejection.
##     This is no longer a rare bug — it is total fingerprint system failure.
##     The fingerprint check is not running at all, or its rejection list is empty/stale.
##
##   ✗ RSI range validation still NOT blocking all zombies.
##     Evidence: Gen 3383/3389 (179 trades) still reaching backtester.
##     Improved from 20% to 10% zombie rate — some fix may be partially active.
##     However, the 179-trade family is still not blocked.
##     Add gap-check: REJECT if (rsi_short_threshold - rsi_long_threshold) < 10.
##
##   ✗ Stale YAML contamination still active.
##     Evidence: Gen 3388 (1450 trades), Gen 3391 (1320 trades).
##     Multiple stale YAML families confirmed active. Direct injection pipeline not clean.
##
##   ✗ Clone detection not running.
##     Evidence: (0.5854/1010) × 5, (−0.9664/179) × 2 in 20 gens.
##     The fingerprint list must be checked BEFORE backtester submission, not after.
##
##   NEWLY CONFIRMED WORKING (partial):
##   ✓ Zombie rate reduced: 20% → 10% in last 20 gens. Some RSI validation active.
##   ✓ New_elite classification is being applied (Gen 3382, Gen 3400 caught as below champion).
##     However: "new_elite" label is being applied to results BELOW champion (< 2.3494).
##     new_elite should mean sharpe > champion AND sharpe < prior_elite_threshold.
##     Currently being used as "close but not champion" — this is acceptable IF documented.
##     FIX: new_elite = sharpe in (champion_sharpe × 0.99, champion_sharpe). Otherwise discard.
##
##   MANDATORY LOKI ESCALATION STATUS:
##   ✗ P0-EMERGENCY deadline: Gen 3343. Current gen: 3400. Overdue by 57 generations.
##     Per program rules: LOKI escalation is MANDATORY. Log this NOW.
##     Log: "P0-EMERGENCY not completed by Gen 3343. Escalating to LOKI at Gen 3400."
##     LOKI must be given full infrastructure failure report (see STEP 0 below).
##
## ─────────────────────────────────────────────────────────
## STEP 0 — LOKI ESCALATION [MANDATORY — EXECUTE BEFORE ANY OTHER ACTION]:
##   Log: "LOKI ESCALATION TRIGGERED at Gen 3400. P0-EMERGENCY 57 generations overdue."
##   Provide LOKI with:
##     1. Full list of confirmed broken systems (fingerprint, RSI validation, direct injection).
##     2. Evidence: (0.5854/1010) × 5 in 20 gens. (−0.9664/179) × 2 in 20 gens.
##     3. Champion values (Gen 3340) that MUST be locked before any testing resumes.
##     4. Full attractor list (see STEP B below) that MUST be loaded into rejection system.
##     5. Request: LOKI to confirm each P0-EMERGENCY step complete before returning control.
##   Do NOT resume testing until LOKI confirms P0-EMERGENCY complete.
##   Do NOT accept "in progress" as complete. Each step requires explicit confirmation log.
##
## STEP 1 — YAML INTEGRITY CHECK [MANDATORY — BLOCKING]:
##   The confirmed Gen 3340 champion YAML must be retrieved from backtested storage.
##   Under NO circumstances use the displayed "Current Best Strategy" YAML.
##   If storage retrieval fails → HALT ALL OPERATIONS. Escalate to LOKI.
##
## STEP 2 — DIRECT INJECTION [MANDATORY FOR ALL P-ITEMS]:
##   Construct YAML programmatically from confirmed champion + EXACTLY ONE param diff.
##   Source: confirmed champion YAML file (hard-coded path, no fallback).
##
##   DIRECT INJECTION CHECKLIST (run before every test, no exceptions):
##   □ Load confirmed Gen 3340 champion YAML from storage (hard-coded path).
##   □ Confirm file hash matches known champion hash.
##   □ Apply exactly ONE parameter change programmatically.
##   □ Diff result against champion YAML — confirm EXACTLY ONE line changed.
##   □ Verify timeout_hours = 159.
##   □ Verify stop_loss_pct = 1.91 (unless explicit P2-SL test — NEVER 1.90).
##   □ Verify stop_loss_pct ≠ 1.90 (explicit separate check).
##   □ Verify size_pct = 25, max_open = 3, leverage = 2.
##   □ Verify rsi_long_threshold = 37.77.
##   □ Verify rsi_period_hours = 22.
##   □ Verify trend_period_hours = 48.
##   □ Verify rsi_long_threshold in [30, 45].
##   □ Verify rsi_short_threshold in [55, 70].
##   □ Verify (rsi_short_threshold - rsi_long_threshold) >= 10 [NEW — prevents 179-trade family].
##   □ Verify trades estimate is plausible (flag if > 1400 or < 900).
##   □ Verify trades estimate ≠ 1010 ± 20 [NEW — blocks Attractor 12 family].
##   □ Verify trades estimate ≠ 179 ± 10 [NEW — blocks Attractor 13 family].
##   □ Run pre-backtest fingerprint check against ALL known attractors (full list below).
##   □ If zero diffs vs champion → pre-reject. Log as Gen 3340 clone.
##   □ If more than one diff → pre-reject. Log as multi-diff error.
##   □ If ANY fingerprint match → pre-reject. Do NOT submit to backtester.
##   □ Submit to backtester ONLY if ALL checks pass.
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
## STEP 3 — LLM FALLBACK [SUSPENDED UNTIL FURTHER NOTICE]:
##   LLM remains suspended. Infrastructure not stable.
##   Re-enable conditions (ALL must be true simultaneously):
##     (a) Direct injection confirmed working: 5 consecutive P-item tests reach
##         backtester with correct champion YAML (verified by diff log).
##     (b) Fingerprint auto-update confirmed working: new_best event → fingerprint
##         active before next generation (verified by test injection → pre-rejected).
##     (c) No stale YAML or high-trade-count attractor results for 10 consecutive gens.
##     (d) RSI range validation confirmed blocking zombies:
##         Test rsi_long=50 → pre-rejected.
##         Test rsi_short=40 → pre-rejected.
##         Test rsi_gap < 10 → pre-rejected. [NEW]
##     (e) LLM receives confirmed Gen 3340 YAML as baseline (not displayed YAML).
##     (f) All [GEN_3340_*] tokens replaced with confirmed values before sending.
##     (g) Zero zombie generations (trades < 400) for 10 consecutive gens.
##     (h) (0.5854/1010) does NOT appear in any of the 10 consecutive gens. [NEW]
##   When re-enabled: temperature=0.0. Maximum LLM rate: 10% of generations.
##   Any known attractor in LLM result → pre-reject. Do not count as valid gen.
##
## STEP 4 — GRID SCAN FALLBACK [if direct injection fails for technical reasons]:
##   Run backtester directly on target range, all other params frozen at champion values.
##   Accept only if sharpe > 2.3494 AND trades ≥ 400.
##   Priority grid: TP=[confirmed_TP+0.05, confirmed_TP+0.10, confirmed_TP+0.15].
##   Secondary: rsi_short=[confirmed_rsi_short-1, confirmed_rsi_short-2].
##   Tertiary: rsi_period=[21, 23].
##   Quaternary: trend_period=[36, 42, 54, 60]. [NEW — never systematically tested]
##   Document when used and why direct injection failed.
##
## ─────────────────────────────────────────────────────────
## COMPLETE ATTRACTOR / FINGERPRINT REJECTION LIST
## (ALL entries must be loaded into fingerprint system before any testing resumes)
##
##   Attractor 1a:  (1.0218, 822)    — Gen 1 baseline
##   Attractor 1b:  (2.2496, 1267)   — Gen 1477 champion
##   Attractor 1c:  (2.2657, 1267)   — Gen 1592 champion
##   Attractor 1d:  (2.2828, 1272)   — Gen 2785 champion
##   Attractor 1d2: (2.2910, 1269)   — Gen 2791 champion
##   Attractor 1d3: (2.3055, 1268)   — Gen 2813 champion
##   Attractor 1d4: (2.3219, 1263)   — Gen 2899 champion
##   Attractor 1e:  (2.3262, 1263)   — Gen 3075 champion
##   Attractor 1e-b:(2.3026, 1263)   — Gen 3184 near-clone
##   Attractor 1f:  (2.3300, 1264)   — Gen 3192 champion (never properly added)
##   Attractor 1f-near:(2.3295, 1266)— Gen 3325 near-clone
##   Attractor 1g:  (2.3494, 1265)   — Gen 3340 CURRENT CHAMPION
##   Attractor 1h:  (2.3428, 1265)   — Gen 3400 new_elite (same trades, just below champion)
##   Attractor 1i:  (2.3330, 1270)   — Gen 3382 new_elite
##   Attractor 1j:  (2.3295, 1266)   — Gen 3394 discarded near-clone
##   Attractor 4:   (0.7753, 1041)   — original stale YAML family
##   Attractor 4b:  (0.7660, 1041)   — stale YAML variant
##   Attractor 7:   (1.6508, 1455)   — Gen 3196 stale high-trade YAML
##   Attractor 8:   (1.6312, 1399)   — Gen 3200 stale high-trade YAML
##   Attractor 9:   (0.6558, 1085)   — Gen 3193 broken YAML family
##   Attractor 10:  (0.7558, 1042)   — Gen 3194 broken YAML family
##   Attractor 11:  (−0.7496, 1706)  — Gen 3339 extreme stale YAML (new worst-case)
##   Attractor 12:  (0.5854, 1010)   — FIVE appearances in last 20 gens [NEW URGENT]
##   Attractor 13:  (−0.9664, 179)   — TWO appearances (Gens 3383/3389) [NEW URGENT]
##   Attractor 14:  (1.6934, 1450)   — Gen 3388 stale YAML high-trade [NEW]
##   Attractor 15:  (2.0227, 1320)   — Gen 3391 stale YAML elevated trade [NEW]
##   Attractor 16:  (−1.4023, 424)   — Gen 3398 inverted-signal family [NEW]
##
##   VERIFICATION REQUIRED (after loading):
##   □ Inject Gen 3340 champion YAML → pre-rejected as Attractor 1g. If not → HALT.
##   □ Inject Gen 3192 YAML (2.3300/1264) → pre-rejected as Attractor 1f. If not → HALT.
##   □ Inject Gen 3400 YAML (2.3428/1265) → pre-rejected as Attractor 1h. If not → HALT.
##   □ Generate test YAML producing ~1010 trades → pre-rejected as Att