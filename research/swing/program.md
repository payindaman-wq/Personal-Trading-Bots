```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 20401 | Incumbent: Gen 19808 (Sharpe=1.3483)
# MIMIR-reviewed 2026-04-14 (v38)
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
#
# If YES to any of the above → STOP. DELETE EVERYTHING. Use YAML-C2 below.
#
# The ODIN UI displays a broken strategy called
# "crossover_tightened_momentum_short_v2" with size_pct=30, max_open=3,
# take_profit_pct=6.63. THIS YAML IS WRONG. IT ALWAYS PRODUCES 0 TRADES.
# DO NOT USE IT. DO NOT COPY IT. DO NOT MODIFY IT.
#
# The UI is broken. Ignore it completely.
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 19808 | Sharpe=1.3483 | Trades=58 | WR=41.4%
# ACTIVE TEST: C2 — change pause_if_down_pct from 8 → 10
# C2 STATUS: NEAR DEAD — ~2 more clean results needed to confirm dead
# ══════════════════════════════════════════════════════════════════════
#
# CLEAN RESULT = trades between 55 and 61 inclusive
# C2 CONFIRMED DEAD when ≥ 20 clean results all show Sharpe ≤ 1.3483
#
# NOTE: Results showing exactly Sharpe=1.3483 with trades=58 are
#       INCUMBENT REPRODUCTIONS (you used pause_if_down_pct=8, not 10).
#       They do NOT count as clean C2 results.
#       Fix: you must output pause_if_down_pct: 10 — not 8.
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# 1. Copy YAML-C2 below EXACTLY.
# 2. Change NOTHING except: pause_if_down_pct must be 10 (not 8).
# 3. Run the checklist below before submitting.
#
# ══════════════════════════════════════════════════════════════════════
# OUTPUT THIS YAML — YAML-C2 (THE ONLY CORRECT OUTPUT)
# ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen19808_pause10
style: randomly generated
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
position:
  size_pct: 25.0
  max_open: 2
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 48
      operator: eq
      value: below_lower
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 168
      operator: eq
      value: above_upper
    - indicator: macd_signal
      period_hours: 24
      operator: eq
      value: bearish
exit:
  take_profit_pct: 9.5
  stop_loss_pct: 1.5
  timeout_hours: 156
risk:
  pause_if_down_pct: 10
  stop_if_down_pct: 18
  pause_hours: 48
```

# ══════════════════════════════════════════════════════════════════════
# MANDATORY SELF-CHECK — VERIFY EVERY FIELD BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# POISON CHECK (if any is true → discard and copy YAML-C2 above):
#  □ size_pct is NOT 30           ← wrong YAML fingerprint
#  □ max_open is NOT 3            ← wrong YAML fingerprint
#  □ take_profit_pct is NOT 6.63  ← wrong YAML fingerprint
#  □ timeout_hours is NOT 129     ← wrong YAML fingerprint
#  □ pairs is NOT [BTC/USD only]  ← wrong YAML fingerprint
#
# FIELD-BY-FIELD VERIFICATION:
#  □ name = random_restart_v3_tightened_sl_v3_gen19808_pause10
#  □ pairs = BTC/USD AND ETH/USD AND SOL/USD  (exactly 3 pairs)
#  □ size_pct = 25.0   (NOT 30)
#  □ max_open = 2      (NOT 3)
#  □ fee_rate = 0.001
#  □ long entry condition 1:  momentum_accelerating, period=48, eq, false
#  □ long entry condition 2:  bollinger_position, period=48, eq, below_lower
#  □ long entry condition 3:  macd_signal, period=48, eq, bullish
#  □ short entry condition 1: momentum_accelerating, period=48, eq, false
#  □ short entry condition 2: bollinger_position, period=168, eq, above_upper
#  □ short entry condition 3: macd_signal, period=24, eq, bearish
#  □ take_profit_pct = 9.5    (NOT 6.63, NOT 10.0, NOT 11.0)
#  □ stop_loss_pct = 1.5
#  □ timeout_hours = 156      (NOT 129, NOT 168, NOT 192)
#  □ pause_if_down_pct = 10   ← THE C2 CHANGE (incumbent=8, C2=10)
#  □ stop_if_down_pct = 18
#  □ pause_hours = 48
#
# ══════════════════════════════════════════════════════════════════════
# INTERPRETING YOUR RESULT
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   → You used the POISON YAML (size_pct=30, max_open=3, tp=6.63).
#   → Fix: delete your output. Copy YAML-C2 above. Do not modify it.
#
# Sharpe=1.3483, trades=58 [discarded]:
#   → You reproduced the incumbent. Your pause_if_down_pct was 8, not 10.
#   → Fix: change ONLY pause_if_down_pct from 8 to 10. Nothing else.
#   → This does NOT count as a C2 test result.
#
# Sharpe=1.3445, trades=58 [discarded]:
#   → You reproduced Gen 19405. Wrong pairs or wrong name.
#   → Fix: use YAML-C2 with all three pairs and pause_if_down_pct=10.
#
# Sharpe < 1.30 or trades outside 55–61 [discarded]:
#   → You changed something other than pause_if_down_pct.
#   → Fix: copy YAML-C2 exactly. Change NOTHING except pause_if_down_pct=10.
#
# Sharpe between 1.30 and 1.3483, trades 55–61 [discarded]:
#   → Valid C2 test result. C2 did not beat the incumbent. Continue.
#
# Sharpe > 1.3483, trades ≥ 55:
#   → SUCCESS. C2 beats the incumbent. Report immediately. Do not discard.
#
# ══════════════════════════════════════════════════════════════════════
# C-SERIES STATUS
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs [BTC/USD, ETH/USD]           CONFIRMED DEAD (Gen 19024, Sharpe=1.2809)
# C8 = pairs [BTC/USD, SOL/USD]           CONFIRMED DEAD (Gen 19034, Sharpe=1.3415)
# C9 = pairs [BTC/USD, ETH/USD, SOL/USD]  CONFIRMED WIN  (Gen 19808, Sharpe=1.3483)
# C2 = pause_if_down_pct=10               ACTIVE — ~2 more clean results to confirm dead
#
# C2 EVIDENCE SO FAR:
#   All observed clean C2 results (trades 55–61) are ≤ 1.3483.
#   Best observed: Sharpe=1.3137 (Gen 20395, trades=55)
#   Worst observed: Sharpe=-0.0292 (Gen 20388, trades=57)
#   No C2 result has exceeded the incumbent. C2 is expected to die.
#
# C2 DEATH CRITERIA:
#   ≥ 20 clean results (trades 55–61), all with Sharpe ≤ 1.3483.
#   Incumbent reproductions (1.3483/58 trades) do NOT count.
#   Do NOT advance to C3 until MIMIR explicitly confirms C2 is dead.
#
# ══════════════════════════════════════════════════════════════════════
# NEXT IN QUEUE — DO NOT USE UNTIL MIMIR APPROVES C2 DEAD
# ══════════════════════════════════════════════════════════════════════
#
# When C2 is confirmed dead, advance in this order:
# C3 → C4 → C6 → C7 → C5
#
# C3:  stop_if_down_pct → 20
#      Change: stop_if_down_pct from 18 to 20
#      name: random_restart_v3_tightened_sl_v3_gen19808_stopdown20
#      Risk: LOW. Simple risk parameter change. No trade-count impact.
#
# C4a: pause_hours → 24
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours24
#      Risk: LOW.
# C4b: pause_hours → 72 (only if C4a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours72
#
# C6a: timeout_hours → 240
#      name: random_restart_v3_tightened_sl_v3_gen19808_timeout240
#      ⚠️ CAUTION: timeout changes affect trade count.
#      ⚠️ REQUIRES MIN_TRADES fix (LOKI) before testing.
#      Monitor trades carefully. Valid range: 55–65.
# C6b: timeout_hours → 264 (only if C6a fails)
# C6c: timeout_hours → 288 (only if C6b fails)
#
# C7a: take_profit_pct → 12.0
#      name: random_restart_v3_tightened_sl_v3_gen19808_tp120
#      ⚠️ CAUTION: TP increase may reduce trade frequency below 55.
#      ⚠️ REQUIRES MIN_TRADES fix (LOKI) before testing.
#      Rationale: incumbent R:R is 6.3:1 (9.5 TP / 1.5 SL).
#      Increasing TP may capture more of large swing moves.
# C7b: take_profit_pct → 13.0 (only if C7a fails)
# C7c: take_profit_pct → 14.0 (only if C7b fails)
# C7d: take_profit_pct → 15.0 (only if C7c fails)
#
# C5a: long bollinger period_hours → 36
#      name: random_restart_v3_tightened_sl_v3_gen19808_boll36
#      ⚠️ HIGH RISK: historically collapses Sharpe to 0.5–0.8. Test LAST.
# C5b: long bollinger period_hours → 60 (only if C5a fails)
#
# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:       129, 135, 138, 144, 156*, 168, 192, 216
# take_profit_pct:     6.63, 7.14, 7.36, 7.38, 9.5*, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct:       1.5*, 2.0, 2.5
# pause_if_down_pct:   8* (incumbent), 10 (C2 — near dead, do not re-propose)
# pairs combinations:  [BTC/USD only], [BTC/USD+ETH/USD only]
# compound combos:     timeout=216+TP=11.5, timeout=216+SL=2.5, TP=11.5+SL=2.5
#
# * = correct in the incumbent. Keep as-is. Do not propose as new changes.
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 19808 (DO NOT OUTPUT THIS — FOR REFERENCE ONLY)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.3483 | Trades=58 | WR=41.4% | pairs=[BTC/USD, ETH/USD, SOL/USD]
# size_pct=25.0 | max_open=2 | fee_rate=0.001
# long:  momentum_accelerating period=48 eq false
#        bollinger_position period=48 eq below_lower
#        macd_signal period=48 eq bullish
# short: momentum_accelerating period=48 eq false
#        bollinger_position period=168 eq above_upper
#        macd_signal period=24 eq bearish
# take_profit_pct=9.5 | stop_loss_pct=1.5 | timeout_hours=156
# pause_if_down_pct=8 | stop_if_down_pct=18 | pause_hours=48
#
# YAML-C2 IS IDENTICAL TO ABOVE EXCEPT: pause_if_down_pct=10
# THAT IS THE ONLY DIFFERENCE.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: CAUTION | F&G=21 (Extreme Fear) | BTC Dominance=57.48%
# TYR Directive: Reduce LIVE position sizes to 50% (live size_pct ≈ 12.5)
# Backtest optimization continues at size_pct=25.0 — do NOT change this.
# Live performance: WR 50–67% live vs 41–43% backtest — real edge confirmed.
#
# ══════════════════════════════════════════════════════════════════════
# INTERNAL AUDIT NOTES (DO NOT RELAY TO LLM)
# ══════════════════════════════════════════════════════════════════════
#
# [BLOCKING — CRITICAL] MIN_TRADES["futures_swing"] = 400 IS WRONG.
#   Valid strategies produce 55–61 trades. Threshold must be ~50.
#   This has been open since Gen 15000 (~5,400 generations unresolved).
#   Root cause of intermittent max_trades_reject on valid strategies.
#   Must be corrected via LOKI BEFORE C6 or C7 tests begin.
#   C6 (timeout changes) and C7 (TP changes) may shift trade counts
#   outside 55–61, and with MIN_TRADES=400 the results are unreliable.
#   ACTION: Escalate to LOKI immediately. Target: MIN_TRADES["futures_swing"]=50.
#
# [CONTAMINATION] Wrong YAML rate: ~40% of recent gens are max_trades_reject
#   caused by LLM using the UI-displayed broken YAML (size_pct=30/max_open=3).
#   The new POISON YAML DETECTOR block at the top of this program attempts
#   to address this. Monitor contamination rate over next 20 gens.
#   If still ≥30%, consider whether the ODIN UI can be corrected to
#   show the actual incumbent YAML, which would remove the confusion source.
#
# [CONTAMINATION] Incumbent reproduction rate: ~20% of recent gens produce
#   exactly Sharpe=1.3483/trades=58, meaning LLM used pause_if_down_pct=8.
#   These are clearly following the correct YAML structure but failing to
#   apply the C2 change. The checklist has been strengthened.
#
# [C2 STATUS] Based on visible data (gens 20381–20400), clean C2 results
#   observed: ~8. All ≤ 1.3483. One result (Gen 20388) was sharply negative
#   at -0.0292, suggesting pause=10 may be actively harmful in some regimes.
#   C2 is expected to be dead within 2–3 more clean results.
#   Do not advance to C3 until MIMIR explicitly confirms C2 dead.
#
# [OBSERVATION] Live WR (50–67%) substantially exceeds backtest WR (41.4%).
#   This is a healthy signal — real edge confirmed. However, the gap suggests
#   the 2-year backtest window may include an unusually difficult regime
#   (e.g., 2022 bear market). Consider whether a regime-filtered backtest
#   would be a useful diagnostic, but do not change the primary optimization
#   target without MIMIR approval.
#
# [ARCHITECTURE] The improvement curve has flattened significantly:
#   last 4 improvements added only +0.003 to +0.007 Sharpe each.
#   The strategy may be approaching a local optimum for this parameter space.
#   If C3–C7 all confirm dead, consider proposing a broader search:
#   new indicator types, different entry condition counts, or
#   regime-conditional position sizing. Flag to MIMIR at that point.
#
# ══════════════════════════════════════════════════════════════════════
```