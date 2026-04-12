```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-3800 | Revised by MIMIR (Gen 3800 review)
# STATUS: CHAMPION UNCHANGED at Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%).
#         Champion stall duration: 460 generations (Gen 3340 → Gen 3800). CRITICAL.
#         Last 20 gens analysis: 35% zombies, 20% champion clones, 10% attractors.
#         Effective research yield: ~35% of generations. Unacceptable.
#         LLM IS SUSPENDED UNCONDITIONALLY. Grid scan is the ONLY permitted test mode.
#         Do NOT re-enable LLM until grid scan is complete AND 10 clean gens verified.

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor — pre-backtest enforcement mandatory)

---
## ██████████████████████████████████████████████████████████
## ODIN INJECTION NOTE (INTERNAL ONLY — NEVER SEND TO LLM)
##
## ─────────────────────────────────────────────────────────
## CONFIRMED CHAMPION: Gen 3340 (sharpe=2.3494, trades=1265, win_rate=40.1%)
## All prior champions are SUPERSEDED. Do NOT use any prior champion as baseline.
##
## CONFIRMED CHAMPION VALUES (Gen 3340 — retrieve from storage, verify hash):
##   rsi_period_hours:    22     (certain — confirmed Gen 2785)
##   rsi_long_threshold:  37.77  (certain — confirmed Gen 1477)
##   rsi_short_threshold: 59     (medium confidence — MUST be confirmed from storage)
##                        NOTE: If storage shows 60, use 60. Do not assume.
##   trend_period_hours:  48     (certain)
##   take_profit_pct:     [MUST BE CONFIRMED FROM STORAGE]
##                        Estimated range: 4.90–5.05 based on Gen 3400 analysis.
##                        Gen 3400 (2.3428/1265) = confirmed_TP - 0.05 (high confidence).
##                        Gen 3382 (2.3330/1270) = different family (TP too low, more trades).
##                        Confirm exact value before any grid test proceeds.
##   stop_loss_pct:       1.91   (certain — NOT 1.90, NOT 1.92)
##   timeout_hours:       159    (FROZEN FOREVER — do not test, do not change)
##   size_pct:            25     (FROZEN)
##   max_open:            3      (FROZEN)
##   leverage:            2      (FROZEN)
##   fee_rate:            0.0005 (FROZEN)
##
## STALE YAML WARNING:
##   The displayed "Current Best Strategy" YAML shows stale values:
##     rsi_period_hours: 24     ← WRONG (champion is 22)
##     take_profit_pct:  4.65   ← WRONG (champion is ~4.90–5.05)
##     stop_loss_pct:    1.92   ← WRONG (champion is 1.91)
##     timeout_hours:    176    ← WRONG (champion is 159)
##     rsi_short value:  60     ← UNCONFIRMED (may be correct or may be 59)
##   IGNORE THE DISPLAYED YAML ENTIRELY. Use only storage-retrieved champion file.
##   This YAML has been stale since Gen 1592. It must never be used as a source.
##
## ─────────────────────────────────────────────────────────
## GEN 3800 SITUATION ASSESSMENT:
##
##   Champion stall: 460 generations without improvement. Research is stalled.
##
##   Last 20 generations breakdown (Gens 3781–3800):
##     Champion clones (2.3494/1265): Gens 3785, 3791, 3792, 3798 = 4/20 = 20%
##     Zombie (trades < 400): Gens 3781, 3783, 3786, 3788, 3789, 3794, 3795 = 7/20 = 35%
##     Attractor 12 (0.5854/1010): Gens 3799, 3800 = 2/20 = 10%
##     Attractor 13 (−0.9664/179): Gen 3789 = 1/20 = 5%
##     Prior champion family: Gens 3784 (~1d), 3796 (1d4) = 2/20 = 10%
##     Other stale/discarded: Gens 3782, 3787, 3790, 3793, 3797 = 5/20 = 25%
##     Useful novel results: ZERO in last 20 generations.
##
##   Infrastructure failure confirmed (persistent across 10+ LOKI escalations):
##     ✗ Fingerprint pre-rejection: NOT WORKING (Attractor 12 appeared Gen 3799–3800)
##     ✗ Clone detection: NOT WORKING (4 exact champion clones in 20 gens)
##     ✗ RSI range validation: NOT WORKING (7 zombie gens in 20 gens = 35%)
##     ✗ Stale YAML contamination: STILL ACTIVE (Gens 3784, 3787, 3793, 3796, 3797)
##     ✗ LLM producing pathological params: UNCONTROLLED
##
##   Root cause conclusion:
##     The LLM cannot be trusted to propose valid single-parameter changes.
##     Infrastructure fixes have been escalated 10+ times since Gen 1400.
##     None have resolved the root cause.
##     SOLUTION: Eliminate LLM from the loop entirely. Run deterministic grid.
##
## ─────────────────────────────────────────────────────────
## MANDATORY LOKI ESCALATION (Gen 3800):
##
##   Log: "LOKI ESCALATION at Gen 3800. Champion stalled 460 gens. LLM suspended
##         unconditionally. Grid scan mode activated. P0-EMERGENCY infrastructure
##         failures persistent across 10 escalation cycles. New approach required."
##
##   Provide LOKI with:
##     1. This full infrastructure failure report.
##     2. Request: Confirm Gen 3340 champion YAML retrieved from storage and hash locked.
##     3. Request: Confirm ALL attractor fingerprints loaded (full list in STEP B below).
##     4. Request: Confirm pre-backtest fingerprint check is active (test injection → rejected).
##     5. Request: Confirm pre-backtest MIN_TRADES estimate check is active.
##     6. Request: Confirm clone detection is active (inject champion → rejected as clone).
##     7. Request: Confirm RSI range validation active (rsi_long=50 → rejected pre-backtest).
##     8. Authorize grid scan mode (STEP A below) as primary research mode.
##     9. Explicit confirmation required for each item. "In progress" is NOT accepted.
##
##   Do NOT resume any testing until LOKI provides explicit confirmation of items 2–8.
##
## ─────────────────────────────────────────────────────────
## STEP A — PRIMARY RESEARCH MODE: DETERMINISTIC GRID SCAN [ACTIVE NOW]
##
##   The LLM is suspended unconditionally. All parameter tests are pre-specified below.
##   ODIN executes each test in order. No LLM involvement. No free-form proposals.
##   Each test = confirmed champion YAML + EXACTLY ONE parameter change.
##   YAML is constructed programmatically from storage-retrieved champion file.
##
##   PHASE A0 — CHAMPION CONFIRMATION (execute FIRST, before any grid tests):
##     A0.1: Submit confirmed champion YAML with zero changes.
##           Expected: (2.3494, 1265). If result differs → HALT. Investigate storage.
##           This establishes that the backtester is running correctly.
##     A0.2: Confirm rsi_short_threshold from storage. Log exact value.
##     A0.3: Confirm take_profit_pct from storage. Log exact value.
##     A0.4: Lock confirmed values. Replace all [CONFIRM_*] tokens below.
##     Do NOT proceed to Phase A1 until A0 complete and logged.
##
##   PHASE A1 — TAKE PROFIT GRID (highest priority — Gen 3400 analysis supports TP+0.05):
##     Note: "confirmed_TP" = value retrieved in Phase A0.
##     A1.1: TP = confirmed_TP + 0.05   [expected: near-champion or improvement]
##     A1.2: TP = confirmed_TP + 0.10
##     A1.3: TP = confirmed_TP + 0.15
##     A1.4: TP = confirmed_TP + 0.20
##     A1.5: TP = confirmed_TP + 0.25
##     A1.6: TP = confirmed_TP - 0.10   [already tested at -0.05 = Gen 3400, 2.3428]
##     Accept only if sharpe > 2.3494 AND trades in [900, 1400].
##     If A1.1 improves: immediately test A1.1+0.05 and A1.1+0.10 before proceeding.
##     If no A1 test improves: TP is confirmed at local maximum. Proceed to Phase A2.
##
##   PHASE A2 — RSI SHORT THRESHOLD GRID (second priority):
##     Note: "confirmed_rsi_short" = value retrieved in Phase A0.
##     A2.1: rsi_short = confirmed_rsi_short - 1
##     A2.2: rsi_short = confirmed_rsi_short - 2
##     A2.3: rsi_short = confirmed_rsi_short + 1
##     A2.4: rsi_short = confirmed_rsi_short + 2
##     A2.5: rsi_short = confirmed_rsi_short - 3
##     Constraint: rsi_short must remain in [55, 70].
##     Constraint: (rsi_short - rsi_long_threshold) must be >= 10.
##             rsi_long_threshold = 37.77, so rsi_short minimum = 48 (well satisfied above).
##     Accept only if sharpe > 2.3494 AND trades in [900, 1400].
##     If any A2 test improves: test A1 grid again from new champion before continuing.
##
##   PHASE A3 — RSI PERIOD GRID (third priority — never exhaustively tested):
##     A3.1: rsi_period_hours = 21
##     A3.2: rsi_period_hours = 23
##     A3.3: rsi_period_hours = 20
##     A3.4: rsi_period_hours = 24   [note: this is what stale YAML shows — useful baseline]
##     Accept only if sharpe > 2.3494 AND trades in [900, 1400].
##
##   PHASE A4 — TREND PERIOD GRID (fourth priority — never tested):
##     A4.1: trend_period_hours = 36
##     A4.2: trend_period_hours = 42
##     A4.3: trend_period_hours = 54
##     A4.4: trend_period_hours = 60
##     A4.5: trend_period_hours = 72
##     Accept only if sharpe > 2.3494 AND trades in [900, 1400].
##
##   PHASE A5 — RSI LONG THRESHOLD GRID (fifth priority — frozen since Gen 1477):
##     Note: rsi_long = 37.77 has been frozen for 2,300+ generations. Worth re-examining.
##     A5.1: rsi_long = 37.00
##     A5.2: rsi_long = 38.00
##     A5.3: rsi_long = 36.50
##     A5.4: rsi_long = 38.50
##     A5.5: rsi_long = 36.00
##     Constraint: rsi_long must remain in [30, 45].
##     Accept only if sharpe > 2.3494 AND trades in [900, 1400].
##
##   PHASE A6 — STOP LOSS GRID (sixth priority — confirmed 1.91 but neighbors untested):
##     A6.1: stop_loss_pct = 1.85
##     A6.2: stop_loss_pct = 1.88
##     A6.3: stop_loss_pct = 1.94
##     A6.4: stop_loss_pct = 1.97
##     A6.5: stop_loss_pct = 2.00
##     Constraint: stop_loss_pct must NOT be 1.90 or 1.92 (known non-optimal neighbors).
##     Accept only if sharpe > 2.3494 AND trades in [900, 1400].
##
##   PHASE A7 — COMBINED BEST (only after all single-param phases complete):
##     If any single-param improvements found: test top-2 improvements combined.
##     If no single-param improvements: strategy is at local maximum for tested params.
##     Log: "Phase A grid complete. X improvements found. Champion = [new or unchanged]."
##
##   Total Phase A tests: ~26 backtests. Should complete in < 30 generations.
##   This is the entire productive research agenda. Execute it cleanly.
##
## ─────────────────────────────────────────────────────────
## STEP B — PRE-BACKTEST VALIDATION CHECKLIST
## (Run before EVERY backtester submission — no exceptions — hard reject if any fail)
##
##   SOURCE VALIDATION:
##   □ Load champion YAML from confirmed storage path (hard-coded, no fallback).
##   □ Verify file hash matches known Gen 3340 champion hash.
##   □ If hash mismatch → HALT. Do not submit. Escalate to LOKI.
##
##   PARAMETER INTEGRITY:
##   □ Apply exactly ONE parameter change from the Phase A grid (or zero for A0 test).
##   □ Diff result against champion YAML. Confirm exactly 0 or 1 lines changed.
##   □ If diff shows 2+ changes → reject. Log as "multi-diff error."
##   □ Verify timeout_hours = 159 (FROZEN — reject if any other value).
##   □ Verify stop_loss_pct ≠ 1.90 (explicit check — separate from range check).
##   □ Verify size_pct = 25, max_open = 3, leverage = 2, fee_rate = 0.0005.
##   □ Verify rsi_long_threshold = 37.77 (unless Phase A5 test — then verify in [30,45]).
##   □ Verify rsi_period_hours = 22 (unless Phase A3 test — then verify in [18, 28]).
##   □ Verify trend_period_hours = 48 (unless Phase A4 test — then verify in [24, 96]).
##   □ Verify rsi_long_threshold in [30, 45].
##   □ Verify rsi_short_threshold in [55, 70].
##   □ Verify (rsi_short_threshold - rsi_long_threshold) >= 10.
##
##   TRADE ESTIMATE PRE-CHECK (estimate based on param change direction):
##   □ Flag if estimated trades > 1400 or < 900 (warn, do not auto-reject — log reason).
##   □ Reject if estimated trades ≈ 1010 ± 20 (Attractor 12 family).
##   □ Reject if estimated trades ≈ 179 ± 15 (Attractor 13 family).
##   □ Reject if estimated trades < 400 (MIN_TRADES — pre-backtest enforcement).
##
##   FINGERPRINT PRE-REJECTION:
##   □ Check (expected_sharpe_estimate, expected_trades) against ALL entries below.
##   □ Check known exact champion value (2.3494, 1265) — reject as clone if zero diff.
##   □ If ANY match within tolerance → reject. Log. Do NOT submit to backtester.
##   □ Tolerance: sharpe ± 0.005, trades ± 5.
##
##   FINGERPRINT SYSTEM VERIFICATION (run once before Phase A begins):
##   □ Inject Gen 3340 champion YAML (zero diff) → must be rejected as Attractor 1g.
##   □ Inject param producing ~1010 trades → must be rejected as Attractor 12.
##   □ If either test fails → HALT ALL TESTING. Escalate to LOKI. Fix first.
##
## ─────────────────────────────────────────────────────────
## STEP C — POST-BACKTEST MANDATORY ACTIONS (after EVERY new_best event)
##
##   □ Retrieve new champion YAML from storage immediately (same generation cycle).
##   □ Verify new champion YAML hash matches backtester output record.
##   □ Add (new_sharpe, new_trades, win_rate) to fingerprint list (blocking call).
##   □ Verify fingerprint active: inject new champion YAML → pre-rejected immediately.
##      If NOT pre-rejected → HALT. Do not start next generation. Fix fingerprint first.
##   □ Lock new champion YAML with hash. Update champion hash constant.
##   □ Update ALL champion value references in this program (sharpe, trades, params).
##   □ Update Phase A grid: mark completed tests, update "confirmed_TP" references.
##   □ Log: "Post-new_best fingerprint verified at Gen XXXX. New champion locked."
##   □ Do NOT start next generation until all above confirmed complete.
##
## ─────────────────────────────────────────────────────────
## STEP D — RESULT CLASSIFICATION (post-backtest)
##
##   new_best:    sharpe > 2.3494 AND trades >= 400. New champion. Execute STEP C.
##   new_elite:   sharpe in [2.3494 × 0.990, 2.3494) AND trades >= 400.
##                = sharpe in [2.3259, 2.3494). Log, add to fingerprint, discard.
##   discarded:   sharpe < 2.3259 OR trades < 400. Log fingerprint, discard.
##   low_trades:  trades < 400. Pre-rejected if MIN_TRADES check working.
##                If reaching backtester: infrastructure failure. Log and investigate.
##   attractor:   Result matches fingerprint list within tolerance. Should be pre-rejected.
##                If reaching backtester: fingerprint system failure. Log and investigate.
##   clone:       Exact champion result (2.3494, 1265). Should be pre-rejected as zero-diff.
##                If reaching backtester: clone detection failure. Log and investigate.
##
##   CRITICAL: "clone" appearing at backtester = the test submitted was the champion unchanged.
##   Three clone results in any 20-gen window → HALT. Something is injecting without diffs.
##
## ─────────────────────────────────────────────────────────
## STEP E — LLM RE-ENABLE CONDITIONS [SUSPENDED — do not re-enable until ALL met]
##
##   LLM remains suspended until Phase A grid is COMPLETE and ALL conditions below are true:
##   (a) Phase A grid complete: all 26 tests executed, results logged.
##   (b) Direct injection verified: 5 consecutive grid tests reached backtester with
##       correct champion YAML confirmed by diff log.
##   (c) Fingerprint system verified: new_best event → fingerprint active before next gen.
##   (d) No stale YAML results for 10 consecutive gens (no trades > 1400 from wrong params).
##   (e) RSI validation verified: rsi_long=50 → pre-rejected. rsi_short=40 → pre-rejected.
##       rsi_gap=5 (e.g., rsi_long=55, rsi_short=60) → pre-rejected.
##   (f) Zero clones in 10 consecutive gens.
##   (g) Zero zombies (trades < 400) in 10 consecutive gens.
##   (h) Attractor 12 (0.5854/1010) not appearing in 10 consecutive gens.
##   When re-enabled: temperature=0.0. LLM rate: maximum 10% of generations.
##   LLM receives confirmed champion YAML (from storage) as baseline. Never displayed YAML.
##   LLM output subject to STEP B checklist before any backtester submission.
##
## ─────────────────────────────────────────────────────────
## COMPLETE ATTRACTOR / FINGERPRINT REJECTION LIST
## (All entries must be loaded and verified active before any testing resumes)
##
##   CHAMPION HISTORY:
##   Attractor 1a:  (1.0218,  822,  41.0%) — Gen 1 baseline
##   Attractor 1b:  (2.2496, 1267,  39.8%) — Gen 1477
##   Attractor 1c:  (2.2657, 1267,  39.9%) — Gen 1592
##   Attractor 1d:  (2.2828, 1272,  40.0%) — Gen 2785
##   Attractor 1d2: (2.2910, 1269,  39.9%) — Gen 2791
##   Attractor 1d3: (2.3055, 1268,  39.8%) — Gen 2813
##   Attractor 1d4: (2.3219, 1263,  39.9%) — Gen 2899
##   Attractor 1e:  (2.3262, 1263,  40.0%) — Gen 3075
##   Attractor 1e-b:(2.3026, 1263,  n/a  ) — Gen 3184 near-clone
##   Attractor 1f:  (2.3300, 1264,  40.0%) — Gen 3192
##   Attractor 1f-n:(2.3295, 1266,  n/a  ) — Gen 3325 near-clone
##   Attractor 1g:  (2.3494, 1265,  40.1%) — Gen 3340 CURRENT CHAMPION
##   Attractor 1h:  (2.3428, 1265,  n/a  ) — Gen 3400 new_elite
##   Attractor 1i:  (2.3330, 1270,  n/a  ) — Gen 3382 new_elite
##   Attractor 1j:  (2.3295, 1266,  n/a  ) — Gen 3394 near-clone
##   Attractor 1k:  (2.2791, 1274,  39.7%) — Gen 3784 [NEW — stale YAML family]
##   Attractor 1l:  (1.9853, 1232,  40.3%) — Gen 3790 [NEW]
##
##   STALE YAML / HIGH-TRADE FAMILIES:
##   Attractor 4:   (0.7753, 1041,  n/a  ) — original stale YAML
##   Attractor 4b:  (0.7660, 1041,  n/a  ) — stale YAML variant
##   Attractor 7:   (1.6508, 1455,  n/a  ) — Gen 3196 stale high-trade
##   Attractor 8:   (1.6312, 1399,  n/a  ) — Gen 3200 stale high-trade
##   Attractor 9:   (0.6558, 1085,  n/a  ) — Gen 3193 broken YAML
##   Attractor 10:  (0.7558, 1042,  n/a  ) — Gen 3194 broken YAML
##   Attractor 11:  (−0.7496,1706,  n/a  ) — Gen 3339 extreme stale YAML
##   Attractor 14:  (1.6934, 1450,  n/a  ) — Gen 3388 stale high-trade
##   Attractor 15:  (2.0227, 1320,  n/a  ) — Gen 3391 stale elevated-trade
##   Attractor 16:  (−1.4023, 424,  n/a  ) — Gen 3398 inverted-signal
##
##   CRITICAL ATTRACTORS (high recurrence — highest priority to block):
##   Attractor 12:  (0.5854, 1010, 34.5%) — 7+ appearances total [URGENT]
##   Attractor 13:  (−0.9664, 179, 30.2%) — 3+ appearances total [URGENT]
##
##   NEW (Gen 3781–3800):
##   Attractor 17:  (0.7057,    1, 100.0%)— Gen 3781 [single trade — extreme params]
##   Attractor 18:  (1.3535,  915,  38.7%) — Gen 3782 [stale YAML family]
##   Attractor 19:  (−4.3765,  60,  25.0%)— Gen 3783 [extreme zombie]
##   Attractor 20:  (1.2069, 1189,  37.2%) — Gen 3787 [stale YAML family]
##   Attractor 21:  (−1.9813, 107,  21.5%) — Gen 3786 [zombie