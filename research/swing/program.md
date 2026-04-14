```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 20201 | Incumbent: Gen 19808 (Sharpe=1.3483)
# MIMIR-reviewed 2026-04-14 (v37)
#
# ══════════════════════════════════════════════════════════════════════
# ⚠️ STOP — READ THIS FIRST BEFORE DOING ANYTHING ELSE ⚠️
# ══════════════════════════════════════════════════════════════════════
#
# THE ODIN UI SHOWS A WRONG YAML. DO NOT USE IT. EVER.
#
# The ODIN UI shows "crossover_tightened_momentum_short_v2"
# It has:  size_pct=30  |  max_open=3  |  pairs=[BTC/USD only]
#          take_profit_pct=6.63  |  timeout_hours=129
#
# THIS YAML IS ALWAYS WRONG. IT PRODUCES Sharpe=0, trades=0.
# DO NOT COPY IT. DO NOT USE IT AS A STARTING POINT.
# IF YOU SEE size_pct=30 OR max_open=3 OR take_profit_pct=6.63 → STOP.
# DISCARD EVERYTHING AND USE YAML-C2 BELOW INSTEAD.
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 19808 | Sharpe=1.3483 | Trades=58 | WR=41.4%
# ACTIVE TEST: C2 — change pause_if_down_pct from 8 → 10
# C2 STATUS: ACTIVE — requires ~10 more clean results to confirm dead
# ══════════════════════════════════════════════════════════════════════
#
# CLEAN RESULT = trades between 55 and 61 inclusive
# C2 CONFIRMED DEAD when ≥ 20 clean results all show Sharpe ≤ 1.3483
# NOTE: Results showing exactly Sharpe=1.3483 with trades=58 are
#       INCUMBENT REPRODUCTIONS (you used pause_if_down_pct=8, not 10)
#       They do NOT count as clean C2 results. Fix: use pause_if_down_pct=10.
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# Output the YAML below. Change NOTHING except:
#   pause_if_down_pct: 10    ← this is the ONLY difference from the incumbent
#
# The incumbent has pause_if_down_pct: 8
# You MUST output pause_if_down_pct: 10
# That is the ONLY change. Everything else is IDENTICAL to the incumbent.
#
# ══════════════════════════════════════════════════════════════════════
# OUTPUT THIS YAML — YAML-C2 (the only correct output)
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
# STEP-BY-STEP SELF-CHECK BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# Check EACH item. If ANY is false → discard output and copy YAML-C2 above.
#
# FIRST — check for the wrong YAML:
#  □ size_pct is NOT 30           (wrong YAML has 30 — reject if true)
#  □ max_open is NOT 3            (wrong YAML has 3 — reject if true)
#  □ take_profit_pct is NOT 6.63  (wrong YAML has 6.63 — reject if true)
#
# THEN — verify every field:
#  □ name = random_restart_v3_tightened_sl_v3_gen19808_pause10
#  □ pairs = BTC/USD, ETH/USD, SOL/USD  (exactly three — NOT just BTC/USD)
#  □ size_pct = 25.0
#  □ max_open = 2
#  □ fee_rate = 0.001
#  □ long:  momentum period=48 eq false
#  □ long:  bollinger period=48 eq below_lower
#  □ long:  macd period=48 eq bullish
#  □ short: momentum period=48 eq false
#  □ short: bollinger period=168 eq above_upper
#  □ short: macd period=24 eq bearish
#  □ take_profit_pct = 9.5
#  □ stop_loss_pct = 1.5
#  □ timeout_hours = 156
#  □ pause_if_down_pct = 10   ← THE C2 CHANGE (incumbent=8, you must output 10)
#  □ stop_if_down_pct = 18
#  □ pause_hours = 48
#
# ══════════════════════════════════════════════════════════════════════
# WHAT YOUR RESULT MEANS
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   → You used the wrong YAML (size_pct=30 or max_open=3 or tp=6.63).
#   → Fix: copy YAML-C2 above exactly. Do not modify it.
#
# Sharpe=1.3483, trades=58 [discarded]:
#   → You reproduced the incumbent. You used pause_if_down_pct=8 (not 10).
#   → Fix: change pause_if_down_pct from 8 to 10. That is the ONLY change.
#   → This does NOT count as a C2 test result.
#
# Sharpe=1.3445, trades=58 [discarded]:
#   → You reproduced Gen 19405 (old incumbent). Wrong pairs or wrong name.
#   → Fix: use YAML-C2 with all three pairs and pause_if_down_pct=10.
#
# Sharpe < 1.30 or trades outside 55–61:
#   → You changed something other than pause_if_down_pct.
#   → Fix: copy YAML-C2 exactly. Change NOTHING except pause_if_down_pct=10.
#
# Sharpe between 1.30 and 1.3483, trades 55–61 [discarded]:
#   → Valid C2 test result (C2 did not improve on incumbent). Continue.
#
# Sharpe > 1.3483, trades ≥ 55:
#   → SUCCESS. C2 beats the incumbent. Report immediately. Submit as-is.
#
# ══════════════════════════════════════════════════════════════════════
# C-SERIES STATUS
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs [BTC/USD, ETH/USD]           CONFIRMED DEAD (Gen 19024, Sharpe=1.2809)
# C8 = pairs [BTC/USD, SOL/USD]           CONFIRMED DEAD (Gen 19034, Sharpe=1.3415)
# C9 = pairs [BTC/USD, ETH/USD, SOL/USD]  CONFIRMED WIN  (Gen 19808, Sharpe=1.3483)
# C2 = pause_if_down_pct=10               ACTIVE — ~10 more clean results needed
#
# C2 DEATH CRITERIA:
#   ≥ 20 clean results (trades 55–61) all with Sharpe ≤ 1.3483
#   Results of exactly 1.3483/58 trades = incumbent reproductions = DO NOT COUNT
#   Do NOT advance to C3 until MIMIR explicitly confirms C2 is dead.
#
# ══════════════════════════════════════════════════════════════════════
# IF C2 IS CONFIRMED DEAD — NEXT STEPS (DO NOT USE UNTIL MIMIR APPROVES)
# ══════════════════════════════════════════════════════════════════════
#
# Priority order: C3 → C4 → C6 → C7 → C5 (C5 is high risk, test last)
#
# C3:  stop_if_down_pct → 20
#      name: random_restart_v3_tightened_sl_v3_gen19808_stopdown20
#      Risk: low. Simple risk parameter loosening.
#
# C4a: pause_hours → 24
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours24
# C4b: pause_hours → 72 (test only if C4a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours72
#
# C6a: timeout_hours → 240
#      name: random_restart_v3_tightened_sl_v3_gen19808_timeout240
# C6b: timeout_hours → 264 (test only if C6a fails)
# C6c: timeout_hours → 288 (test only if C6b fails)
#      Risk: medium. Affects trade count — monitor trades carefully.
#
# C7a: take_profit_pct → 12.0
#      name: random_restart_v3_tightened_sl_v3_gen19808_tp120
# C7b: take_profit_pct → 13.0 (test only if C7a fails)
# C7c: take_profit_pct → 14.0 (test only if C7b fails)
# C7d: take_profit_pct → 15.0 (test only if C7c fails)
#      Risk: medium-high. TP increase may reduce trade frequency.
#      Rationale: incumbent R:R is already 6.3:1 (TP=9.5 vs SL=1.5).
#      Higher TP could capture more of winning swings.
#
# C5a: long bollinger period_hours → 36
#      name: random_restart_v3_tightened_sl_v3_gen19808_boll36
#      ⚠️ HIGH RISK: historically collapses Sharpe to 0.5–0.8. Test LAST.
# C5b: long bollinger period_hours → 60 (test only if C5a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_boll60
#
# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:       129, 135, 138, 144, 156*, 168, 192, 216
# take_profit_pct:     6.63, 7.14, 7.36, 7.38, 9.5*, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct:       1.5*, 2.0, 2.5
# pause_if_down_pct:   8* (incumbent value), 10 (currently being tested as C2)
# pairs combinations:  [BTC/USD only], [BTC/USD+ETH/USD only]
# combinations:        timeout=216+TP=11.5, timeout=216+SL=2.5, TP=11.5+SL=2.5
#
# * = dead as an isolated improvement but currently correct in the incumbent.
#     KEEP these values. Do not propose them as new changes.
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 19808 (FOR REFERENCE ONLY — DO NOT OUTPUT THIS)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.3483 | Trades=58 | WR=41.4% | pairs=[BTC/USD, ETH/USD, SOL/USD]
# size_pct=25.0 | max_open=2 | fee_rate=0.001
# long:  momentum period=48 false | bollinger period=48 below_lower | macd period=48 bullish
# short: momentum period=48 false | bollinger period=168 above_upper | macd period=24 bearish
# take_profit_pct=9.5 | stop_loss_pct=1.5 | timeout_hours=156
# pause_if_down_pct=8 | stop_if_down_pct=18 | pause_hours=48
#
# YAML-C2 is identical to above EXCEPT pause_if_down_pct=10.
# That is the only difference. Do not change any other field.
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
# [BLOCKING] MIN_TRADES constant: futures_swing=400 is incorrect.
#   Actual clean trade counts for valid strategies: 55–61.
#   Must be corrected to MIN_TRADES~50 via LOKI before any C5/C6/C7
#   tests that may materially change trade frequency.
#   Do not action via LLM. Escalate to LOKI separately. This is blocking.
#
# [MONITORING] C2 contamination: ~40-50% of recent gens are max_trades_reject
#   (wrong YAML). ~20% are incumbent reproductions (pause=8 not 10).
#   Fewer than 10 confirmed clean C2 tests have been collected.
#   Hold C2 open. Do not advance to C3 yet.
#
# [OBSERVATION] The "Current Best Strategy" shown in ODIN UI is the wrong YAML
#   (crossover_tightened_momentum_short_v2, size_pct=30, max_open=3).
#   The true incumbent is Gen 19808 as specified in this program.
#   The UI mismatch is the primary source of LLM confusion. This should
#   be corrected in the ODIN UI if possible, but research program must
#   continue to aggressively warn against the wrong YAML regardless.
#
# ══════════════════════════════════════════════════════════════════════
```