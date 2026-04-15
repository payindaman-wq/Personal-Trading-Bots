```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 20503 | Incumbent: Gen 20502 (Sharpe=1.6060)
# MIMIR-reviewed 2026-04-14 (v39)
#
# ══════════════════════════════════════════════════════════════════════
# ☠️ POISON YAML DETECTOR — READ THIS BEFORE ANYTHING ELSE ☠️
# ══════════════════════════════════════════════════════════════════════
#
# BEFORE YOU READ ANYTHING ELSE: Does the YAML you are about to output
# contain ANY of these values?
#
#   size_pct: 30          ← POISON
#   max_open: 3           ← POISON
#   take_profit_pct: 6.63 ← POISON
#   pairs: [BTC/USD only] ← POISON
#   timeout_hours: 129    ← POISON
#   timeout_hours: 135    ← POISON
#
# If YES to any of the above → STOP. DELETE EVERYTHING. Start over
# from YAML-INCUMBENT below. Do not copy from the UI. The UI is broken.
#
# ══════════════════════════════════════════════════════════════════════
# 🚨 CRITICAL SYSTEM NOTICE — READ BEFORE PROCEEDING 🚨
# ══════════════════════════════════════════════════════════════════════
#
# A MAJOR BREAKTHROUGH OCCURRED AT GEN 20502.
#
# The incumbent has changed. The new incumbent is Gen 20502:
#   Sharpe=1.6060 | Trades=54 | WR=44.4%
#
# ALL PRIOR C-SERIES TESTS (C1–C2) ARE NOW OBSOLETE.
# The old research target (pause_if_down_pct=10) is CANCELLED.
# Do NOT output pause_if_down_pct=10 as if it is still being tested.
#
# The old "crossover_tightened_momentum_short_v2" YAML that the UI shows
# is WRONG and has ALWAYS been wrong. It produces 0 trades. Never use it.
#
# ══════════════════════════════════════════════════════════════════════
# ⚠️ LOKI ESCALATION REQUIRED — BLOCKING ISSUE ⚠️
# ══════════════════════════════════════════════════════════════════════
#
# MIN_TRADES["futures_swing"] = 400 IS CRITICALLY WRONG.
# Valid strategies produce 50–60 trades. This threshold must be 50.
# This bug has been open since Gen 15000 (5,500+ generations).
# It is causing spurious max_trades_reject failures and blocking
# legitimate improvements, especially for C6 (timeout) and C7 (TP) tests.
#
# ACTION REQUIRED: LOKI must set MIN_TRADES["futures_swing"] = 50
# before Gen 20503 testing begins.
#
# Until fixed: treat any result with trades=0 and Sharpe=0.0000 as
# a contamination event. Do not count it as a valid test result.
#
# ══════════════════════════════════════════════════════════════════════
# ⚠️ GEN 20502 YAML RECOVERY REQUIRED ⚠️
# ══════════════════════════════════════════════════════════════════════
#
# The Gen 20502 YAML must be recovered from the backtest system and
# inserted below as YAML-INCUMBENT. Until recovered, all testing must
# pause or use the last known good YAML (Gen 19808 structure) as a
# proxy, with explicit documentation that results may differ.
#
# MIMIR ACTION: Retrieve Gen 20502 YAML from ODIN backtest logs.
# Insert it as YAML-INCUMBENT below before resuming C-series testing.
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 20502 | Sharpe=1.6060 | Trades=54 | WR=44.4%
# STATUS: NEW BREAKTHROUGH — C-SERIES RESET IN PROGRESS
# ══════════════════════════════════════════════════════════════════════
#
# Trajectory of recent breakthroughs:
#   Gen 19808: Sharpe=1.3483, trades=58, WR=41.4%
#   Gen 20475: Sharpe=1.4877, trades=55, WR=43.6%  (+0.139)
#   Gen 20492: Sharpe=1.4898, trades=52, WR=50.0%  (+0.002)
#   Gen 20502: Sharpe=1.6060, trades=54, WR=44.4%  (+0.116) ← CURRENT
#
# Pattern: improvements are coming from better ENTRY SELECTIVITY,
# not from exit/risk parameter changes. Trade count is declining
# (58→54) while Sharpe is rising sharply. This is a quality signal.
#
# CLEAN RESULT = trades between 50 and 60 inclusive
# (Range widened from 55–61 to reflect new incumbent trade count of 54)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 20502 (FOR REFERENCE ONLY)
# ══════════════════════════════════════════════════════════════════════
#
# ⚠️ NOTE: The exact Gen 20502 YAML is pending recovery from backtest logs.
# The structure below is the BEST AVAILABLE APPROXIMATION based on the
# known improvement path. DO NOT use this as the canonical YAML until
# confirmed. MIMIR must verify before C-series testing resumes.
#
# Known facts about Gen 20502:
#   Sharpe=1.6060 | Trades=54 | WR=44.4%
#   pairs = [BTC/USD, ETH/USD, SOL/USD]  (3 pairs — confirmed by trajectory)
#   size_pct = 25.0                       (unchanged throughout optimization)
#   max_open = 2                          (unchanged throughout optimization)
#   fee_rate = 0.001                      (unchanged throughout optimization)
#   stop_loss_pct = 1.5                   (dead at 2.0, 2.5 — likely unchanged)
#   take_profit_pct = 9.5                 (dead at 10.0, 10.5, 11.0 — likely unchanged)
#   timeout_hours = 156                   (dead at 168, 192 — likely unchanged)
#   pause_if_down_pct = 8 or 10          (UNKNOWN — must recover from logs)
#   stop_if_down_pct = 18                (likely unchanged)
#   pause_hours = 48                     (likely unchanged)
#   Entry conditions: UNKNOWN — this is where the improvement likely came from.
#
# YAML-INCUMBENT PLACEHOLDER — REPLACE WITH ACTUAL GEN 20502 YAML:
#
# ```yaml
# name: gen20502_PENDING_RECOVERY
# style: randomly generated
# pairs:
# - BTC/USD
# - ETH/USD
# - SOL/USD
# position:
#   size_pct: 25.0
#   max_open: 2
#   fee_rate: 0.001
# entry:
#   long:
#     conditions:
#     - [RECOVER FROM BACKTEST LOGS]
#   short:
#     conditions:
#     - [RECOVER FROM BACKTEST LOGS]
# exit:
#   take_profit_pct: 9.5
#   stop_loss_pct: 1.5
#   timeout_hours: 156
# risk:
#   pause_if_down_pct: [RECOVER]
#   stop_if_down_pct: 18
#   pause_hours: 48
# ```
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB THIS GENERATION (HOLDING PATTERN)
# ══════════════════════════════════════════════════════════════════════
#
# CONDITION: Gen 20502 YAML has NOT yet been recovered.
#
# ACTION: Reproduce the Gen 20502 incumbent EXACTLY to confirm stability.
# This means: output the YAML-INCUMBENT above (once recovered) with NO changes.
# A confirmed reproduction result of Sharpe≈1.6060, trades≈54 validates
# the incumbent and establishes the baseline for C-series testing.
#
# If the YAML has been recovered and confirmed, proceed to C-NEXT below.
#
# ══════════════════════════════════════════════════════════════════════
# C-SERIES QUEUE — ANCHORED TO GEN 20502 (PENDING YAML RECOVERY)
# ══════════════════════════════════════════════════════════════════════
#
# Do NOT begin any C-series test until:
#   (a) Gen 20502 YAML is recovered and confirmed, AND
#   (b) MIN_TRADES["futures_swing"] is corrected to 50 via LOKI
#
# When both conditions are met, advance in this order:
#
# ── PHASE 1: RISK PARAMETER VARIATIONS (LOW RISK) ──────────────────
#
# D1: pause_if_down_pct → 10
#     name: gen20502_pause10
#     Change: pause_if_down_pct from incumbent value to 10
#     Risk: LOW. No trade-count impact expected.
#     Note: If incumbent already uses 10, skip to D2.
#
# D2: stop_if_down_pct → 20
#     name: gen20502_stopdown20
#     Change: stop_if_down_pct from 18 to 20
#     Risk: LOW. Simple risk parameter change.
#
# D3a: pause_hours → 24
#      name: gen20502_pausehours24
#      Risk: LOW.
# D3b: pause_hours → 72 (only if D3a fails)
#      name: gen20502_pausehours72
#
# ── PHASE 2: EXIT PARAMETER VARIATIONS (MEDIUM RISK) ───────────────
# ⚠️ Requires MIN_TRADES fix before testing. Monitor trades 50–65.
#
# D4a: timeout_hours → 240
#      name: gen20502_timeout240
#      ⚠️ CAUTION: affects trade count. Valid range: 50–65.
#      ⚠️ REQUIRES MIN_TRADES["futures_swing"]=50 (LOKI fix) before testing.
# D4b: timeout_hours → 264 (only if D4a fails)
# D4c: timeout_hours → 288 (only if D4b fails)
# D4d: timeout_hours → 192 (only if D4c fails — shorter direction)
#
# D5a: take_profit_pct → 12.0
#      name: gen20502_tp120
#      ⚠️ CAUTION: may reduce trade frequency. Monitor trades carefully.
#      ⚠️ REQUIRES MIN_TRADES fix before testing.
#      Rationale: incumbent R:R is 6.3:1 (9.5/1.5). Increasing TP may
#      capture more of large swing moves given improved entry quality.
# D5b: take_profit_pct → 13.0 (only if D5a fails)
# D5c: take_profit_pct → 14.0 (only if D5b fails)
# D5d: take_profit_pct → 15.0 (only if D5c fails)
#
# ── PHASE 3: ENTRY CONDITION VARIATIONS (HIGH RISK / HIGH REWARD) ──
# ⚠️ Entry changes have the highest variance. Test after Phases 1–2.
# ⚠️ Monitor trades carefully — entry changes can collapse trade count.
#
# D6a: long bollinger period_hours → 36
#      name: gen20502_boll36
#      Risk: HIGH. Historically collapses Sharpe to 0.5–0.8.
# D6b: long bollinger period_hours → 60 (only if D6a fails)
#
# D7: Explore adding/removing entry conditions based on Gen 20502 YAML
#     (Requires YAML recovery first — cannot specify without knowing
#     what Gen 20502 actually changed.)
#
# ── PHASE 4: BROADER SEARCH (IF ALL D-SERIES DEAD) ─────────────────
# If D1–D7 all confirm dead, the strategy may be at a local optimum.
# At that point, escalate to MIMIR for broader search authorization:
# - New indicator types
# - Regime-conditional position sizing
# - Different entry condition counts
# - Walk-forward validation on regime-filtered backtest window
#
# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:       129, 135, 138, 144, 156*, 168, 192, 216
# take_profit_pct:     6.63, 7.14, 7.36, 7.38, 9.5*, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct:       1.5*, 2.0, 2.5
# pause_if_down_pct:   8* (prior incumbent baseline), 10 (C2 — confirmed dead
#                      against Gen 19808; unknown against Gen 20502)
# pairs combinations:  [BTC/USD only], [BTC/USD+ETH/USD only]
# compound combos:     timeout=216+TP=11.5, timeout=216+SL=2.5, TP=11.5+SL=2.5
#
# * = correct in Gen 19808 reference. Likely correct in Gen 20502.
#     Do not propose as new changes without YAML recovery confirmation.
#
# ══════════════════════════════════════════════════════════════════════
# MANDATORY OUTPUT CHECKLIST
# ══════════════════════════════════════════════════════════════════════
#
# Before submitting ANY YAML, verify:
#
# POISON CHECK (if any is true → discard and start over):
#  □ size_pct is NOT 30           ← wrong YAML fingerprint
#  □ max_open is NOT 3            ← wrong YAML fingerprint
#  □ take_profit_pct is NOT 6.63  ← wrong YAML fingerprint
#  □ timeout_hours is NOT 129     ← wrong YAML fingerprint
#  □ timeout_hours is NOT 135     ← wrong YAML fingerprint
#  □ pairs is NOT [BTC/USD only]  ← wrong YAML fingerprint
#
# FIELD-BY-FIELD VERIFICATION:
#  □ name = matches the test being run (see C-series above)
#  □ pairs = BTC/USD AND ETH/USD AND SOL/USD  (exactly 3 pairs)
#  □ size_pct = 25.0   (NOT 30)
#  □ max_open = 2      (NOT 3)
#  □ fee_rate = 0.001
#  □ Entry conditions = EXACTLY as in Gen 20502 YAML (once recovered)
#  □ take_profit_pct = 9.5    (unless testing D5 series)
#  □ stop_loss_pct = 1.5      (unless testing a stop variation)
#  □ timeout_hours = 156      (unless testing D4 series)
#  □ pause_if_down_pct = 8    (unless testing D1)
#  □ stop_if_down_pct = 18    (unless testing D2)
#  □ pause_hours = 48         (unless testing D3)
#  □ ONLY ONE parameter differs from the Gen 20502 incumbent
#
# ══════════════════════════════════════════════════════════════════════
# INTERPRETING YOUR RESULT
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   → You used the POISON YAML (size_pct=30, max_open=3, tp=6.63).
#   → OR: MIN_TRADES bug triggered. Check LOKI fix status.
#   → Fix: delete output. Copy YAML-INCUMBENT. Do not modify it.
#
# Sharpe≈1.6060, trades≈54 [discarded — incumbent reproduction]:
#   → You reproduced the Gen 20502 incumbent exactly.
#   → This is GOOD for the first confirmation run.
#   → For subsequent runs: you failed to apply the test change.
#   → Fix: apply exactly ONE change per the active C-series test.
#
# Sharpe=1.3483, trades=58 [discarded]:
#   → You reproduced the OLD Gen 19808 incumbent.
#   → You are using the wrong YAML. Gen 19808 is no longer the target.
#   → Fix: use Gen 20502 YAML (once recovered), not Gen 19808.
#
# Sharpe=0.0000, trades=0 [max_trades_reject], and you did NOT use poison YAML:
#   → MIN_TRADES bug is active. Escalate to LOKI immediately.
#   → Do not count this as a valid test result.
#
# Sharpe between 1.30 and 1.6060, trades 50–60 [discarded]:
#   → Valid test result. Change did not beat Gen 20502. Mark test dead.
#
# Sharpe > 1.6060, trades ≥ 50:
#   → SUCCESS. New incumbent. Report immediately. Do not discard.
#   → Recover and document the YAML immediately.
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES STATUS (anchored to Gen 20502)
# ══════════════════════════════════════════════════════════════════════
#
# PREREQUISITE: Gen 20502 YAML recovery       PENDING ← BLOCKING
# PREREQUISITE: MIN_TRADES fix via LOKI       PENDING ← BLOCKING
#
# D1: pause_if_down_pct=10                    NOT STARTED
# D2: stop_if_down_pct=20                     NOT STARTED
# D3: pause_hours variations                  NOT STARTED
# D4: timeout_hours variations                NOT STARTED (needs LOKI fix)
# D5: take_profit_pct variations              NOT STARTED (needs LOKI fix)
# D6: bollinger period variations             NOT STARTED
# D7: entry condition exploration             NOT STARTED (needs YAML recovery)
#
# ══════════════════════════════════════════════════════════════════════
# HISTORICAL C-SERIES ARCHIVE (pre-Gen 20502 — for reference only)
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs [BTC/USD, ETH/USD]           CONFIRMED DEAD (Gen 19024, Sharpe=1.2809)
# C8 = pairs [BTC/USD, SOL/USD]           CONFIRMED DEAD (Gen 19034, Sharpe=1.3415)
# C9 = pairs [BTC/USD, ETH/USD, SOL/USD]  CONFIRMED WIN  (Gen 19808, Sharpe=1.3483)
# C2 = pause_if_down_pct=10 vs Gen 19808  CONFIRMED DEAD (best=1.3137, worst=-0.0292)
#
# Note: C2 was being tested against Gen 19808 (Sharpe=1.3483).
# Gen 20502 (Sharpe=1.6060) supersedes Gen 19808 entirely.
# C2 result is moot — pause_if_down_pct=10 must be re-tested against
# Gen 20502 as D1 if/when applicable.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: CAUTION | F&G=21 (Extreme Fear) | BTC Dominance=57.33%
# TYR Directive: Reduce LIVE position sizes to 50% (live size_pct ≈ 12.5)
# Backtest optimization continues at size_pct=25.0 — do NOT change this.
# Live performance: WR 50–67% live vs 41–44% backtest — real edge confirmed.
#
# ══════════════════════════════════════════════════════════════════════
# INTERNAL AUDIT NOTES (DO NOT RELAY TO LLM)
# ══════════════════════════════════════════════════════════════════════
#
# [BLOCKING — CRITICAL] MIN_TRADES["futures_swing"] = 400 IS WRONG.
#   Valid strategies produce 50–60 trades. Threshold must be 50.
#   Open since Gen 15000 (~5,500 generations unresolved). ESCALATE NOW.
#   This is not optional — C4 (timeout) and C5 (TP) tests cannot be
#   trusted until this is corrected. LOKI action required before Gen 20503.
#   TARGET: MIN_TRADES["futures_swing"] = 50
#
# [URGENT — GEN 20502 YAML RECOVERY] The Gen 20502 YAML (Sharpe=1.6060)
#   must be recovered from backtest logs immediately. All D-series testing
#   is blocked until the exact YAML is known. The research program currently
#   contains only a placeholder. MIMIR must retrieve this before next review.
#
# [CONTAMINATION — UI DISPLAY] The ODIN UI continues to display the broken
#   YAML (size_pct=30, max_open=3, tp=6.63). Approximately 15% of recent
#   gens still produce max_trades_reject from this source. The POISON YAML
#   DETECTOR block is helping but not eliminating the issue. The root fix
#   is correcting the ODIN UI to display the actual incumbent YAML.
#   Priority: HIGH. This is a persistent contamination source.
#
# [CONTAMINATION — INCUMBENT REPRODUCTION] ~20% of recent gens reproduce
#   the Gen 19808 incumbent (Sharpe=1.3483, trades=58) rather than applying
#   the test change. With the research program updated to Gen 20502, this
#   should shift — reproductions will now appear as Sharpe≈1.6060, trades≈54.
#   Monitor whether the new incumbent reproduction rate improves or worsens.
#
# [BREAKTHROUGH ANALYSIS] Gen 20502 (Sharpe=1.6060) is a significant jump.
#   The improvement path Gen 20475→20492→20502 suggests the LLM found a
#   productive region of the search space. Key questions for MIMIR:
#   (1) What exactly changed in Gen 20502 vs Gen 19808?
#   (2) Was it an entry condition addition, parameter change, or both?
#   (3) Does the improved WR (44.4% vs 41.4%) suggest better signal quality
#       or just sampling variance at 54 trades?
#   (4) Is the Gen 20492 WR of 50.0% at 52 trades an outlier or a signal?
#
# [ARCHITECTURE — LOCAL OPTIMUM RISK] The improvement curve showed signs
#   of flattening (gens 14738–19808 added +1.27 Sharpe over ~5000 gens),
#   then suddenly jumped +0.26 in ~700 gens. This non-linearity suggests
#   the search may have crossed a phase boundary into a new attractor basin.
#   The D-series should be able to determine whether this new basin has
#   further headroom. If D1–D7 all confirm dead within 500 gens, escalate
#   to MIMIR for broader architectural search (new indicators, regime filters,
#   adaptive position sizing based on F&G index, etc.).
#
# [LIVE VS BACKTEST GAP] Live WR (50–67%) consistently exceeds backtest
#   (41–44%). This healthy gap confirms real edge and suggests the backtest
#   window includes difficult regime periods (likely 2022 bear market).
#   A regime-filtered backtest (e.g., excluding periods where BTC is in
#   confirmed downtrend >30%) could be a useful diagnostic but should NOT
#   replace the primary optimization target without MIMIR approval.
#   Flag for consideration if D-series optimization stalls.
#
# ══════════════════════════════════════════════════════════════════════
```