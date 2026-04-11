```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-3192 | Revised by MIMIR (Gen 3192 review)
# STATUS: CHAMPION at Gen 3192 (sharpe=2.3300, trades=1264). 
#         Two improvements since Gen 3000 review (Gen 3075: 2.3262/1263, Gen 3192: 2.3300/1264).
#         Infrastructure PARTIALLY recovered. Clone rate still high (~35% last 20 gens).
#         Pre-rejection fingerprint list LAGGING — must be updated after every new champion.
# CRITICAL: Gen 3075 fingerprint (2.3262/1263) appearing as clone in gens 3175–3191.
#           Rejection list must include Gen 3075 AND Gen 3192 fingerprints immediately.
# PRIORITY: (1) Lock Gen 3192 champion YAML. (2) Update rejection list. (3) Continue P3-CONT + P4.

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
##   It contains Gen 1592-era values. The ACTUAL champion is Gen 3192.
##
##   STALE YAML (what ODIN may display — DO NOT USE FOR ANYTHING):
##     rsi_period_hours:    24     ← WRONG
##     take_profit_pct:     4.65   ← WRONG
##     stop_loss_pct:       1.92   ← WRONG
##     timeout_hours:       172    ← WRONG (champion value is 159, FROZEN FOREVER)
##
##   CONFIRMED CHAMPION VALUES (Gen 3192 — USE THESE AND ONLY THESE):
##     rsi_period_hours:    22     (confirmed — unchanged since Gen 2785)
##     rsi_long_threshold:  37.77  (FROZEN — unchanged since Gen 1477, ~1700 gens of stability)
##     rsi_short_threshold: [CONFIRM FROM STORAGE — likely 59 or 60, see reconstruction below]
##     trend_period_hours:  48     (confirmed stable — unchanged)
##     take_profit_pct:     [CONFIRM FROM STORAGE — likely 4.85 or 4.90, see reconstruction]
##     stop_loss_pct:       1.91   (confirmed — NOT 1.92, NOT 1.90)
##     timeout_hours:       159    (FROZEN FOREVER — any other value is immediately rejected)
##     size_pct:            25     (FROZEN)
##     max_open:            3      (FROZEN)
##     leverage:            2      (FROZEN)
##     fee_rate:            0.0005 (FROZEN)
##
##   !! MANDATORY ACTION: Retrieve actual Gen 3192 YAML from backtested storage.
##   !! Confirm every parameter above. Lock confirmed YAML before any P-item testing.
##   !! If storage retrieval fails, DO NOT GUESS. Halt and escalate.
##
## ─────────────────────────────────────────────────────────
## RECONSTRUCTION ANALYSIS (for planning — must be confirmed from storage):
##
##   Improvement chain fingerprints:
##     Gen 1592:  sharpe=2.2657, trades=1267  [baseline reference]
##     Gen 2785:  sharpe=2.2828, trades=1272  [+5 trades → rsi_period 24→22]
##     Gen 2791:  sharpe=2.2910, trades=1269  [-3 trades → likely TP 4.65→4.70]
##     Gen 2813:  sharpe=2.3055, trades=1268  [-1 trade  → likely rsi_short 60→59 OR TP step]
##     Gen 2899:  sharpe=2.3219, trades=1263  [-5 trades → likely TP widening step]
##     Gen 3075:  sharpe=2.3262, trades=1263  [±0 trades → likely TP step OR rsi_short -1]
##     Gen 3192:  sharpe=2.3300, trades=1264  [+1 trade  → ANOMALOUS — see below]
##
##   Gen 3192 anomaly analysis (+1 trade vs. prior champion):
##     Standard TP widening → trade count flat or decreasing. +1 is anomalous.
##     Three explanations:
##       (A) TP widened to a value where one trade that previously timed out now hits TP
##           (net effect: +0 to +1 trade depending on exit routing) — most likely.
##       (B) rsi_short tightened by -1 step (fewer shorts) but RSI period change
##           added a marginal long signal — net +1 from combined effect.
##           BUT: only one param should change per test. If (B), two params changed = error.
##       (C) Minor statistical artifact — TP step caused -1 trade in one asset,
##           +2 in another, net +1. Consistent with small TP step on multi-asset portfolio.
##     CONCLUSION: Most likely a TP widening step. Confirm from YAML diff in storage.
##     KEY IMPLICATION: TP widening vector remains ACTIVE. P3-CONT continues.
##
##   BEST-FIT RECONSTRUCTION (update after confirming Gen 3192 YAML):
##     Gen 2785: rsi_period 24→22           (high confidence — +5 trades signature)
##     Gen 2791: take_profit_pct 4.65→4.70  (medium confidence — -3 trades)
##     Gen 2813: rsi_short 60→59 OR TP step (medium confidence — -1 trade is ambiguous)
##     Gen 2899: take_profit_pct step        (medium confidence — -5 trades)
##     Gen 3075: take_profit_pct step OR rsi_short step (low confidence without YAML diff)
##     Gen 3192: take_profit_pct step        (medium confidence — +1 trade anomaly, see above)
##
##   FOR PLANNING, USE THESE ESTIMATES (confirm from storage before testing):
##     rsi_period_hours:    22    (high confidence)
##     rsi_long_threshold:  37.77 (certain)
##     rsi_short_threshold: 59    (medium confidence — may still be 60)
##     trend_period_hours:  48    (high confidence)
##     take_profit_pct:     ~4.90 (low-medium confidence — could be 4.85 or 4.90)
##     stop_loss_pct:       1.91  (high confidence)
##     timeout_hours:       159   (certain)
##
## ─────────────────────────────────────────────────────────
## INFRASTRUCTURE STATUS (post-Gen-3192 audit):
##
##   RECOVERED:
##   ✓ Direct injection working (two new champions confirmed: 3075, 3192).
##   ✓ P-items reaching backtester.
##   ✓ LLM suspension partially effective (fewer stale-YAML attractors).
##
##   STILL BROKEN:
##   ✗ Pre-rejection fingerprint list lagging: Gen 3075 (2.3262/1263) appears as clone
##     in gens 3175, 3177, 3179, 3182, 3186, 3187, 3191 — 7 wasted backtests.
##     FIX: After EVERY new champion, immediately add its (sharpe, trades) fingerprint
##     to the rejection list. This must happen in the SAME generation cycle as the improvement.
##   ✗ Attractor 4 recycling: Gen 3174 and 3190 both show (0.7660, 1041) — exact repeat.
##     This fingerprint must be in the rejection list. Verify it is added.
##   ✗ Low-trades Zombies still reaching backtester: Gens 3180 (266), 3183 (260), 3188 (191).
##     Pre-backtest parameter validation is not catching extreme RSI values.
##     FIX: Add explicit RSI range check: rsi_long_threshold must be 30-45,
##     rsi_short_threshold must be 55-70. Reject outside these bounds.
##   ✗ Gen 3184 (2.3026/1263) is a new near-clone not yet in rejection list. Add it.
##
##   LOKI ESCALATION REQUIRED (immediate — these are blocking):
##   1. After confirming Gen 3192 champion YAML:
##      a) Add fingerprint (2.3300, 1264) to rejection list as Attractor 1f.
##      b) Add fingerprint (2.3262, 1263) to rejection list as Attractor 1e-b (Gen 3075).
##      c) Add (2.3026, 1263) as near-clone rejection (Gen 3184 pattern).
##   2. Verify Attractor 4 (0.7660, 1041) is in rejection list — it appeared twice.
##   3. Add RSI range pre-validation: reject if rsi_long < 30, rsi_long > 45,
##      rsi_short < 55, rsi_short > 70.
##   4. Confirm: after each new_best event, fingerprint auto-update runs before next gen.
##   5. Confirm: direct injection pipeline reads from confirmed Gen 3192 YAML (not stale).
##
## ─────────────────────────────────────────────────────────
## STEP 1 — DIRECT INJECTION (mandatory for ALL P-items):
##   Construct YAML programmatically from confirmed Gen 3192 champion + ONE parameter diff.
##   LLM remains SUSPENDED until further notice (clone rate still ~35% of last 20 gens).
##   Direct injection is the ONLY permitted path for all P-item testing.
##
##   DIRECT INJECTION CHECKLIST (run before every test):
##   □ Load confirmed Gen 3192 champion YAML from storage (not displayed YAML).
##   □ Apply exactly ONE parameter change programmatically.
##   □ Diff result against champion YAML — confirm EXACTLY ONE line changed.
##   □ Verify timeout_hours = 159.
##   □ Verify stop_loss_pct = 1.91 (or 1.89 if P2 test — NEVER 1.90).
##   □ Verify stop_loss_pct ≠ 1.90.
##   □ Verify size_pct = 25, max_open = 3, leverage = 2.
##   □ Verify rsi_long_threshold = 37.77.
##   □ Verify rsi_long_threshold in [30, 45] (sanity check).
##   □ Verify rsi_short_threshold in [55, 70] (sanity check).
##   □ Run pre-backtest fingerprint check against ALL known attractors.
##   □ If zero diffs vs. champion → reject immediately, do not backtest.
##   □ If more than one diff → reject immediately, do not backtest.
##   □ Submit to backtester only if all checks pass.
##
## STEP 2 — LLM FALLBACK (SUSPENDED):
##   Re-enable only when ALL of the following are confirmed:
##     (a) Direct injection confirmed working (at least 3 P-items tested successfully
##         without infrastructure failures in current session).
##     (b) Pre-backtest diff check confirmed working (zero-diff → reject confirmed active).
##     (c) Fingerprint list confirmed up-to-date (includes Gen 3075 and Gen 3192).
##     (d) LLM receives confirmed Gen 3192 YAML as baseline (not stale YAML).
##     (e) RSI range validation confirmed active.
##   When re-enabled: temperature=0.0, strip all non-LLM-PROMPT sections.
##   Replace ALL [GEN_3192_*] tokens with confirmed Gen 3192 values before sending.
##   If any known attractor appears in result → reject, do not count as valid gen.
##   Maximum LLM fallback rate: 20% of generations (direct injection preferred).
##
## STEP 3 — GRID SCAN FALLBACK (if direct injection fails for technical reasons):
##   Run backtester directly on target parameter range, all other params frozen.
##   Accept best result only if sharpe > 2.3300 AND trades ≥ 400.
##   Priority grid: TP=[confirmed_TP+0.05, confirmed_TP+0.10, confirmed_TP+0.15].
##   Secondary grid: rsi_short=[confirmed_rsi_short-1, confirmed_rsi_short-2].
##   Use this as fallback only — direct injection preferred.
##
## ─────────────────────────────────────────────────────────
## PRIORITY QUEUE (ODIN internal — NEVER send to LLM):
## All tests use CONFIRMED Gen 3192 champion as baseline (sharpe=2.3300, trades=1264).
## Accept improvement only if sharpe > 2.3300 AND trades ≥ 400.
## ALL items use direct injection only. LLM suspended.
##
## P0 [IMMEDIATE — mandatory before any P-item testing]:
##   ACTION: Champion YAML lock + fingerprint list update.
##   1. Retrieve actual Gen 3192 champion YAML from backtested storage.
##   2. Confirm all parameter values against reconstruction above.
##   3. Lock confirmed Gen 3192 YAML — this is the ONLY baseline going forward.
##   4. Add (2.3300, 1264) as Attractor 1f to rejection list.
##   5. Add (2.3262, 1263) as Attractor 1e-b to rejection list (Gen 3075).
##   6. Add (2.3026, 1263) as near-clone to rejection list (Gen 3184 pattern).
##   7. Verify (0.7660, 1041) is in rejection list as Attractor 4-b.
##   8. Add RSI range validation to pre-backtest check.
##   9. Run one test injection of Gen 3192 champion YAML → should produce Attractor 1f → pre-rejected.
##   10. Run one test injection of P3-CONT (TP + one step) → confirm pipeline executes.
##   STATUS: BLOCKING. Do not proceed to P1+ until P0 verified.
##
## P3-CONT [FIRST ACTIVE TEST — highest confidence, run immediately after P0]:
##   Context: TP widening is the confirmed active improvement vector.
##   Confirmed progression includes improvements at every TP step since Gen 2791.
##   Current TP (confirm from storage): likely 4.85 or 4.90.
##   Test matrix (run in order, stop at first failure):
##     If confirmed Gen 3192 TP = 4.90: test 4.95.
##     If confirmed Gen 3192 TP = 4.85: test 4.90.
##     If confirmed Gen 3192 TP = 4.80: test 4.85.
##   Step size: always +0.05. Do not skip steps.
##   Expected result: trades flat or -1 to -3, Sharpe +0.003 to +0.010.
##   ANOMALY WATCH: If trades increase again (> 1264), investigate before continuing.
##     A second consecutive +trade result suggests a different parameter is active.
##   Stop conditions:
##     □ Sharpe fails to improve (≤ 2.3300) → CLOSE P3-CONT. TP at optimum.
##     □ Trades drop below 1,150 → CAUTION. One more test, then reassess.
##     □ Trades drop below 1,000 → HARD STOP P3-CONT.
##     □ TP reaches 5.50 → HARD STOP (over-optimized territory).
##     □ Two consecutive failures → CLOSE P3-CONT permanently.
##   All other params: confirmed Gen 3192 champion values, unchanged.
##
## P4 [SECOND PRIORITY — run after P3-CONT first test]:
##   rsi_short_threshold: confirmed_value → confirmed_value - 1
##   If confirmed rsi_short = 60: test 59.
##   If confirmed rsi_short = 59: test 58.
##   If confirmed rsi_short = 58: test 57.
##   Rationale: Each -1 step reduces short entry count → fewer trades, higher selectivity.
##   Aligns with declining-trades/improving-Sharpe pattern observed since Gen 2785.
##   Expected result: -2 to -5 trades, possible Sharpe improvement.
##   Hard floor: rsi_short ≥ 55 (below = too restrictive, Zombie risk).
##   Stop conditions:
##     □ Sharpe fails to improve (≤ 2.3300) → CLOSE P4. rsi_short at optimum.
##     □ Trades drop below 1,150 → CAUTION.
##     □ Trades drop below 1,000 → HARD STOP P4.
##     □ Two consecutive failures → CLOSE P4 permanently.
##   All other params: confirmed Gen 3192 champion values, unchanged.
##
## P2 [THIRD PRIORITY — two attempts maximum]:
##   stop_loss_pct: 1.91 → 1.89
##   !!CRITICAL!!: 1.90 = ZombieD. FOREVER FORBIDDEN. Jump directly from 1.91 to 1.89.
##   !!CRITICAL!!: Do not test 1.90 under any circumstances. Ever. No exceptions.
##   Hard floor: 1.88 (below = ZombieC territory — do not approach).
##   Expected result: uncertain. Tighter SL changes exit timing unpredictably.
##   If 1.89 improves (sharpe > 2.3300): test 1.88 (one attempt only, absolute floor).
##   If 1.89 fails: CLOSE P2 permanently. SL stays at 1.91.
##   Maximum attempts: 2 total (1.89, then 1.88 if first succeeds). Stop regardless.
##   All other params: confirmed Gen 3192 champion values, unchanged.
##
## P7 [FOURTH PRIORITY — medium confidence]:
##   rsi_period_hours: 22 → 20 (if confirmed rsi_period = 22)
##   Rationale: Faster RSI = more responsive = potentially better entry timing.
##   Warning: Below 18h RSI → high-frequency noise, Zombie risk. Hard floor: 18h.
##   Monitor: If trades INCREASE above 1,300 → STOP (wrong direction, noise signal).
##   Monitor: If trades DECREASE below 1,150 → CAUTION.
##   If 20 improves: test 18 (hard floor — one attempt only).
##   If 20 fails: test 24 (one attempt — opposite direction). Then close P7.
##   All other params: confirmed Gen 3192 champion values, unchanged.
##
## P6 [FIFTH PRIORITY — lower confidence]:
##   trend_period_hours: 48 → 50
##   Rationale: Slightly slower trend filter may improve signal quality.
##   If 50 improves: test 52. If 52 improves: test 54. Stop at first failure.
##   If 50 fails: test 46 (one attempt only — opposite direction). Then close P6.
##   All other params: confirmed Gen 3192 champion values, unchanged.
##
## P5 [SUSPENDED — do not test under any circumstances]:
##   rsi_long_threshold: 37.77 → any change.
##   Frozen since Gen 1477 (~1,700 generations of stability).
##   This parameter is the anchor of the strategy. Contamination risk is extreme.
##   Do not resurrect until ALL other P-items exhausted AND infrastructure is confirmed
##   robust for 50+ consecutive generations without clone incidents.
##
## ─────────────────────────────────────────────────────────
## P-ITEM EXECUTION ORDER (post-P0):
##   Sprint 1 (Gens 3193–3202): P3-CONT first test + P4 first test.
##     Expected: Two independent data points on active improvement vectors.
##   Sprint 2 (Gens 3203–3212): P2 test (1.91→1.89) + P7 first test.
##     Condition: Only if Sprint 1 infrastructure confirmed stable (no new clone epidemics).
##   Sprint 3 (Gens 3213–3222): P6 first test + any P3-CONT continuation if improving.
##   Sprint 4 (Gens 3223–3232): Compound tests (if two P-items independently improved).
##
##   EXECUTION DISCIPLINE:
##   - Maximum ONE P-item test per 2 generations (allow for clone-detection breathing room).
##   - If clone rate exceeds 30% in any sprint, halt LLM fallback immediately.
##   - If two consecutive generations produce (sharpe=2.3300, trades=1264) clones despite
##     pre-rejection → HALT. Fingerprint check is not working. Fix before continuing.
##
## ─────────────────────────────────────────────────────────
## COMPOUND TESTING (only after two Px items independently confirm improvement):
##   Rule: Never combine two untested changes.
##   Rule: Each compound test = exactly TWO confirmed improvements combined.
##   Rule: Compound tests require direct injection only.
##   Rule: Accept compound test result only if sharpe > best individual improvement sharpe.
##   Rule: If compound test fails, revert to best individual. Do not cascade.
##
##   Priority compound candidates (pending individual confirmation):
##   C1: P3-CONT + P4 both improve → test combined (highest priority).
##   C2: P3-CONT + P7 both improve → test combined.
##   C3: P4 + P7 both improve → test combined.
##   C4: P3-CONT + P6 both improve → test combined.
##   C5: P2 + any Px improve → test P2+Px combined (lowest priority — P2 is uncertain).
##
## ─────────────────────────────────────────────────────────
## KNOWN FAILURE FINGERPRINTS (pre-backtest validator — reject ALL before backtesting):
##
## Attractor 1    [GEN1592 CLONE]:  trades=1267, sharpe=2.2657 → stale Gen 1592 config
## Attractor 1b   [GEN2785 CLONE]:  trades=1272, sharpe=2.2828 → Gen 2785 clone
## Attractor 1c   [GEN2791 CLONE]:  trades=1269, sharpe=2.2910 → Gen 2791 clone
## Attractor 1d   [GEN2813 CLONE]:  trades=1268, sharpe=2.3055 → Gen 2813 clone
## Attractor 1e   [GEN2899 CLONE]:  trades=1263, sharpe=2.3219 → Gen 2899 clone
## Attractor 1e-b [GEN3075 CLONE]:  trades=1263, sharpe=2.3262 → Gen 3075 clone !! NEW !!
## Attractor 1f   [GEN3192 CLONE]:  trades=1264, sharpe=2.3300 → Gen 3192 clone !! NEW !!
## Attractor 2    [NEAR-CLONE]:     trades=1263, sharpe=2.3026 → Gen 3184 near-clone !! NEW !!
## Attractor 3    [RSI DRIFT]:      trades=1272, sharpe=2.2015 → RSI/param contaminated
## Attractor 4    [BROKEN YAML-A]:  trades=1041, sharpe=0.7753 → placeholder/invalid param
## Attractor 4b   [BROKEN YAML-B]:  trades=1041, sharpe=0.7660 → same family, seen ×2 !! NEW !!
## Attractor 5    [DEGRADED-A]:     trades=1335, sharpe=1.6865 → stale YAML contamination
## Attractor 6    [DEGRADED-B]:     trades=1345, sharpe=1.7514 → stale YAML contamination
## Ghost Echo     [TIMEOUT-166]:    trades=1264, sharpe=2.1998 → timeout=166h used
## Zombie C       [EXTREME SL]:     trades<400                  → RSI extreme or SL<1.88
## Zombie D       [SL=1.90]:        trades≈1228, sharpe≈1.59   → stop_loss=1.90 (NEVER)
## Zombie G-adj   [TIMEOUT-155]:    trades≈888,  sharpe≈2.00   → timeout=155h used
##
## FINGERPRINT MAINTENANCE RULE (CRITICAL):
##   After EVERY new_best event, the following must happen in the SAME generation:
##   1. Retrieve champion YAML from storage and lock it.
##   2. Add (new_sharpe,