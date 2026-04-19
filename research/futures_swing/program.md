```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-9000 | Revised by MIMIR (Gen 9000 review)
#
# ══════════════════════════════════════════════════════════════════
# !! READ THIS BLOCK FIRST — BEFORE READING ANYTHING ELSE !!
# ══════════════════════════════════════════════════════════════════
#
# LOOP STATUS:    ██ PERMANENTLY RETIRED ██  DO NOT RUN GENERATIONS.
#                 Retirement mandated since Gen 5200.
#                 This is an infrastructure problem. No instruction stops it.
#                 Only physical process termination works. See [I3].
#
# CRITICAL BUG ACTIVE — BUG-2 TRIGGERED AT GEN 9000:
#   Gen 9000: sharpe=2.3680, trades=1274, win_rate=40.2% → [discarded]
#   Gen 8989: sharpe=2.3549, trades=1274, win_rate=40.2% → [discarded]
#   Both results are ABOVE the stored YAML champion (2.3513).
#   A result above the stored champion was rejected instead of accepted.
#   THIS MEANS EITHER:
#     (A) In-memory champion > stored YAML champion (YAML not updated on accept),
#     (B) Acceptance gate is broken and rejecting genuine improvements.
#   IMMEDIATE ACTION: Inspect population/elite_0.yaml RIGHT NOW.
#     If YAML shows sharpe=2.3513 → BUG-2 active (YAML not updated). Fix persistence.
#     If YAML shows sharpe=2.3680 → in-memory champion matches YAML, loop is correct,
#       but prior program ground truth was wrong. Update ground truth to 2.3680.
#     If YAML shows any other value → flag for investigation.
#   DO NOT RUN MORE GENERATIONS UNTIL BUG-2 IS DIAGNOSED.
#   See [Z1] for inspection procedure.
#
# ══════════════════════════════════════════════════════════════════
# GROUND TRUTH CHAMPION (canonical — read from stored YAML directly)
# ══════════════════════════════════════════════════════════════════
#
#   Stored YAML:    sharpe=2.3513 | trades=1265 | win_rate=~40%
#   In-memory est.: sharpe=2.3680 | trades=1274 | win_rate=40.2%
#                   (inferred from Gen 9000 clone-rejection behavior)
#   CONFLICT: stored YAML ≠ in-memory threshold. BUG-2 is active.
#   True champion is likely 2.3680 — the YAML is stale.
#   Resolution: Z1 inspection + BUG-2 fix.
#
#   All prior references to champion=2.3575 or champion=2.3714 are RETRACTED.
#   2.3575: previous in-memory estimate, superseded by Gen 9000 evidence.
#   2.3714: MIMIR inference error from Gen 8200 review. Never valid.
#
# ══════════════════════════════════════════════════════════════════
# PARAMETER BLOCK (for YAML proposals — use these values)
# ══════════════════════════════════════════════════════════════════
#
# CONFIRMED values (from stored YAML or strong behavioral evidence):
#   leverage:            2         [CONFIRMED]
#   fee_rate:            0.0005    [CONFIRMED]
#   size_pct:            25        [ESTIMATED — confirm Z3]
#   max_open:            3         [ESTIMATED — confirm Z3]
#   rsi_period_hours:    22        [ESTIMATED — Gen 2785 evidence]
#   rsi_long_threshold:  37.77     [ESTIMATED — Gen 2785 evidence]
#   rsi_short_threshold: UNKNOWN   [displayed 60 is likely stale — confirm Z3]
#   trend_period_hours:  48        [ESTIMATED]
#   take_profit_pct:     UNKNOWN   [displayed 4.65 is likely stale — confirm Z3]
#                                  [estimate: 4.90–5.10 based on improvement history]
#   stop_loss_pct:       1.91      [ESTIMATED — displayed 1.92 likely wrong]
#   timeout_hours:       159       [ESTIMATED — displayed 166 likely wrong]
#   pairs:               AUDIT REQUIRED — see [Z4]
#
# DO NOT USE THE DISPLAYED YAML AS GROUND TRUTH.
# It has been stale since at least Gen 3340 and possibly Gen 2.3513→2.3680 gap.
# Run Z3 before any grid scan or live deployment.
#
# ══════════════════════════════════════════════════════════════════
# WHEN PROPOSING A YAML CHANGE — FOLLOW THESE RULES EXACTLY
# ══════════════════════════════════════════════════════════════════
#
# RULE 1: Change exactly ONE parameter per generation.
# RULE 2: Keep trades between 400 and 3000. Changes likely to produce <400
#         trades WILL be rejected as [low_trades]. Do not propose them.
# RULE 3: Do NOT reproduce the champion unchanged. It will be [discarded].
# RULE 4: Do NOT propose a parameter set you have proposed before.
# RULE 5: Do NOT propose the following known-bad signatures:
#           (190t, -1.0517), (185t, -0.7900), (28t, -9.018),
#           (174t, -1.9619), (224t, -1.7297), (178t, -0.8033),
#           (182t, -1.8625), (158t, -2.0796), (239t, -2.4141),
#           (397t, -0.5405), (461t, -0.4605), (18t, -14.3473).
#         If your proposed change would recreate any of these, change a
#         different parameter instead.
# RULE 6: Prioritize changes to: take_profit_pct, stop_loss_pct, timeout_hours,
#         rsi_long_threshold, rsi_period_hours. These are the highest-value
#         parameters based on improvement history.
#
# HIGH-VALUE SEARCH REGIONS (grid scan targets — use these ranges):
#   take_profit_pct:    4.50 – 5.50 (step 0.10)
#   stop_loss_pct:      1.70 – 2.20 (step 0.05)
#   timeout_hours:      120 – 200   (step 8)
#   rsi_long_threshold: 34.0 – 42.0 (step 0.5)
#   rsi_period_hours:   18 – 28     (step 1)
#
# ══════════════════════════════════════════════════════════════════
# CRITICAL BUGS — IN PRIORITY ORDER
# ══════════════════════════════════════════════════════════════════
#
# BUG-2 [CRITICAL — ACTIVE AS OF GEN 9000]: YAML PERSISTENCE FAILURE.
#   Symptoms: Gen 9000 (2.3680) and Gen 8989 (2.3549) both tagged [discarded]
#             despite being above stored YAML champion (2.3513).
#   Diagnosis: In-memory champion threshold is above stored YAML. YAML not
#              updated when acceptance event occurred.
#   Fix: Locate the champion persistence call in source. Ensure it writes to
#        population/elite_0.yaml on every acceptance event, not just on exit.
#   Test: Submit a YAML that scores above current stored champion. Confirm
#         both (a) tagged [new_best] in log AND (b) elite_0.yaml updated on disk.
#   Log: "BUG-2 FIX: persistence call confirmed at [FILE]:[LINE].
#         Test: [PASS/FAIL]. elite_0.yaml timestamp updated: [YES/NO]."
#
# BUG-4 [HIGH]: CLONE DETECTION IS POST-BACKTEST.
#   5 clones in last 20 gens (25%) = 25% compute waste.
#   Fix: Pre-backtest SHA-256 hash check of proposed YAML against all prior
#        accepted YAMLs. Reject before backtest if hash matches.
#   Log: "BUG-4 FIX: Pre-backtest hash at [FILE]:[LINE]. Test: [PASS/FAIL]."
#
# BUG-5 [MEDIUM]: POISON_REJECT BLOCKLIST INCOMPLETE.
#   (190t, -1.0517) appeared 5 times in Gen 8981–9000. Not all sigs are blocked.
#   New sigs to add: (190t, -1.0517), (28t, -9.018), (185t, -0.7900),
#                    (174t, -1.9619), (224t, -1.7297).
#   Fix: Add result-hash (sharpe+trades+winrate rounded to 2dp) for each sig.
#   Log: "BUG-5 UPDATE: N signatures added. Tests: [PASS/FAIL per sig]."
#
# BUG-1 [LIKELY RESOLVED — VERIFY]: MIN_TRADES GATE.
#   Current behavior: sub-400-trade results correctly rejected as [low_trades].
#   Verification: Run 9-test protocol (see Z5). Do not mark resolved until done.
#   DO NOT change MIN_TRADES value. 400 is correct and appears active.
#
# ══════════════════════════════════════════════════════════════════
# HALT CONDITIONS
# ══════════════════════════════════════════════════════════════════
#
#   HALT-1:  BUG-2 ACTIVE. YAML persistence broken. Fix before any optimization.
#   HALT-2:  LLM loop permanently retired. Do not run generations.
#   HALT-3:  Stale YAML in LLM input. Moot while loop is retired. Fix before restart.
#   HALT-4:  Z1 not executed. True champion YAML params not confirmed.
#   HALT-5:  Clone rate 25% (BUG-4). Pre-backtest hash not implemented.
#   HALT-6:  Grid scan not executed. 5,000+ gens overdue.
#   HALT-7:  Step Z not executed. All items critically overdue.
#   HALT-8:  Infrastructure disablement not confirmed. Loop may still be running.
#   HALT-9:  Pair list not audited. APT/SUI/ARB/OP may lack full 2yr data.
#   HALT-10: Live sprint: ZERO data. Backtest overfitting risk unquantified.
#   HALT-11: BUG-2 active — any further generation results are uninterpretable
#            until the in-memory vs stored champion discrepancy is resolved.
#
# ══════════════════════════════════════════════════════════════════
# MANDATORY ACTION SEQUENCE (human operator)
# ══════════════════════════════════════════════════════════════════
#
# [I3] DISABLE LLM LOOP IMMEDIATELY (infrastructure level — kill the process).
#      Confirm it is not running before any Step Z action.
#
# [Z1] INSPECT elite_0.yaml RIGHT NOW.
#      Record: file path, modification timestamp, all parameter values.
#      Expected: sharpe=2.3513 (stored) OR sharpe=2.3680 (if YAML was updated).
#      If sharpe=2.3513: BUG-2 is confirmed active. Fix persistence. Re-run Z1.
#      If sharpe=2.3680: stored YAML matches in-memory. Update ground truth.
#      If any other value: flag for MIMIR review immediately.
#      Log: "Z1: file=[PATH], ts=[TS], sharpe=[V], trades=[T], win_rate=[W],
#            params=[all values], BUG-2=[CONFIRMED/CLEAR]."
#
# [Z2] FIX BUG-2 (if Z1 confirms it active).
#      Locate champion persistence call. Ensure it writes YAML on every acceptance.
#      Test: submit above-champion YAML, confirm elite_0.yaml updated on disk.
#
# [Z3] CONFIRM ALL PARAMETER VALUES.
#      After BUG-2 is fixed, re-read elite_0.yaml. Record all param values.
#      Replace ESTIMATED values in PARAMETER BLOCK above with CONFIRMED values.
#      Special attention: take_profit_pct, stop_loss_pct, timeout_hours,
#      rsi_period_hours, rsi_short_threshold, rsi_long_threshold.
#
# [Z4] AUDIT PAIR LIST.
#      Confirm all 16 pairs have full 2-year 1-hour futures data (≥17,520 candles).
#      Remove any pair with < 17,520 candles (suspected: APT, SUI, ARB, OP).
#      Sharpe may be inflated if shorter-history pairs are included.
#
# [Z5] VERIFY BUG-1 (MIN_TRADES=400).
#      Run 9-test protocol:
#        Tests 1–8: YAMLs producing ~18, ~158, ~174, ~182, ~185, ~190, ~224,
#                   ~399 trades → must all be REJECTED before backtest.
#        Test 9: YAML producing ~419 trades → must PASS gate.
#      Log: "Z5: Tests 1–9: [PASS/FAIL list]. BUG-1: [RESOLVED/BROKEN]."
#
# [Z6] FIX BUG-4 (pre-backtest YAML hash).
#      Implement SHA-256 hash of proposed YAML before backtest.
#      Reject if hash matches any prior accepted YAML.
#
# [Z7] FIX BUG-5 (poison_reject blocklist).
#      Add all signatures from RULE 5 above to the blocklist.
#      Test each signature. Confirm blocked pre-backtest.
#
# [Z8] GRID SCAN — Execute after Z1–Z7 complete.
#      Priority parameter axes (from improvement history):
#        take_profit_pct:    4.50–5.50, step 0.10  (11 values)
#        stop_loss_pct:      1.70–2.20, step 0.05  (11 values)
#        timeout_hours:      120–200,   step 8     (11 values)
#        rsi_long_threshold: 34.0–42.0, step 0.5   (17 values)
#        rsi_period_hours:   18–28,     step 1     (11 values)
#      Total 1D sweep: ~61 targeted backtests. Run all. Sort by Sharpe.
#      If any result > 2.3680: run 2D grid around that point.
#
# [Z9] LIVE SPRINT DEPLOYMENT.
#      After grid scan complete and champion confirmed:
#        Deploy to AutoBotSwingFutures.
#        Record sprint results. This is the first live performance data.
#        Minimum: 3 completed sprints before any further parameter optimization.
#
# ══════════════════════════════════════════════════════════════════
# DIAGNOSTIC HISTORY (compressed)
# ══════════════════════════════════════════════════════════════════
#
# Gen 8981–9000 window summary:
#   Clones (discarded):        8982, 8989, 9000 (2.3475, 2.3549, 2.3680)
#   Low-trade rejected:        8981, 8983, 8984, 8985, 8987, 8988, 8991,
#                              8992, 8993, 8995, 8999 (11 of 20 = 55%)
#   Legitimate suboptimal:     8986 (1.3250), 8990 (1.7697), 8994 (1.2655),
#                              8996 (1.5300), 8997 (2.2610), 8998 (2.2870)
#   New improvements:          0
#
# KEY: Gen 9000 (2.3680 > stored 2.3513, [discarded]) = BUG-2 confirmed active.
# KEY: Gen 8989 (2.3549 > stored 2.3513, [discarded]) = same pattern.
# KEY: In-memory champion estimated at 2.3680 (highest observed [discarded] result).
#
# Improvement stall: 0 improvements logged above 2.3494 (Gen 3340).
# In-memory champion above stored YAML — YAML persistence broken since unknown gen.
# Last confirmed logged improvement: Gen 3340 (2.3494).
# True in-memory champion: ~2.3680 (Gen 9000 clone evidence).
#
# Known degenerate attractor signatures (all must be in poison_reject blocklist):
#   (190t, -1.0517): 5 occurrences in Gen 8981–9000 alone.
#   (185t, -0.7900): 3 occurrences in Gen 8981–9000.
#   (28t,  -9.0180): 2 occurrences in Gen 8981–9000.
#   (178t, -0.8033), (190t, -1.0406), (174t, -1.9619), (224t, -1.7297),
#   (182t, -1.8625), (158t, -2.0796), (169t, -1.5182), (239t, -2.4141),
#   (397t, -0.5405), (461t, -0.4605), (18t, -14.3473).
#
# LOKI STATUS: ██ PERMANENTLY RETIRED ██
#   17+ escalations. 0 confirmed fixes by behavioral test.
#   Do not escalate to LOKI for any reason. All fixes by human operator in source.
#
# ══════════════════════════════════════════════════════════════════
# END OF RESEARCH PROGRAM
# ══════════════════════════════════════════════════════════════════
```

---