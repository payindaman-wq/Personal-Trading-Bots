```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 20001 | Incumbent: Gen 19808 (Sharpe=1.3483)
# MIMIR-reviewed 2026-04-14 (v36)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 19808 | Sharpe=1.3483 | Trades=58 | WR=41.4%
# ACTIVE TEST: C2 — change pause_if_down_pct from 8 → 10
# C2 STATUS: NOT YET CONFIRMED DEAD — continue testing
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# Output the YAML below. Change NOTHING except:
#   pause_if_down_pct: 10    ← this is the only difference from the incumbent
#
# The incumbent has pause_if_down_pct: 8
# You must output pause_if_down_pct: 10
# That is the ONLY change. Everything else is identical to the incumbent.
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
# VERIFY BEFORE SUBMITTING — ALL MUST BE TRUE
# ══════════════════════════════════════════════════════════════════════
#
#  □ name = random_restart_v3_tightened_sl_v3_gen19808_pause10
#  □ pairs = BTC/USD, ETH/USD, SOL/USD  (exactly three)
#  □ size_pct = 25.0   ← NOT 30
#  □ max_open = 2      ← NOT 3
#  □ fee_rate = 0.001
#  □ long:  momentum period=48 false | bollinger period=48 below_lower | macd period=48 bullish
#  □ short: momentum period=48 false | bollinger period=168 above_upper | macd period=24 bearish
#  □ take_profit_pct = 9.5
#  □ stop_loss_pct = 1.5
#  □ timeout_hours = 156
#  □ pause_if_down_pct = 10   ← THIS IS THE C2 CHANGE (incumbent has 8)
#  □ stop_if_down_pct = 18
#  □ pause_hours = 48
#
# If ANY line is false → discard your output and copy YAML-C2 above exactly.
#
# ══════════════════════════════════════════════════════════════════════
# WARNING: THERE IS A WRONG YAML IN THE ODIN UI — DO NOT USE IT
# ══════════════════════════════════════════════════════════════════════
#
# The ODIN UI shows "crossover_tightened_momentum_short_v2".
# It has size_pct=30, max_open=3, pairs=[BTC/USD only], take_profit_pct=6.63
# Using it produces Sharpe=0, trades=0. It is always wrong. Ignore it entirely.
# If you see size_pct=30 OR max_open=3 OR take_profit_pct=6.63 → wrong YAML. Stop.
#
# ══════════════════════════════════════════════════════════════════════
# WHAT YOUR RESULT MEANS
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   You used the wrong YAML (size_pct=30 or max_open=3). Fix: use YAML-C2.
#
# Sharpe=1.3483, trades=58:
#   You reproduced the incumbent exactly. You likely used pause_if_down_pct=8.
#   Fix: Change pause_if_down_pct to 10. That is the ONLY change needed.
#
# Sharpe=1.3445, trades=58:
#   You reproduced Gen 19405 (old incumbent). Fix: use YAML-C2 with three pairs
#   and pause_if_down_pct=10.
#
# Sharpe < 1.30 or trades ≠ 58:
#   You changed something other than pause_if_down_pct. Fix: use YAML-C2 exactly.
#
# Sharpe > 1.3483, trades ≥ 55:
#   SUCCESS. C2 beats the incumbent. Report immediately. Submit as-is.
#
# ══════════════════════════════════════════════════════════════════════
# C-SERIES STATUS
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs [BTC/USD, ETH/USD]           CONFIRMED (Gen 19024, Sharpe=1.2809)
# C8 = pairs [BTC/USD, SOL/USD]           CONFIRMED (Gen 19034, Sharpe=1.3415)
# C9 = pairs [BTC/USD, ETH/USD, SOL/USD]  CONFIRMED (Gen 19808, Sharpe=1.3483)
# C2 = pause_if_down_pct=10              ACTIVE — not yet confirmed dead
#
# C2 is confirmed dead only after ≥ 20 clean results (trades ≥ 55) all ≤ 1.3483.
# Do NOT move to C3 until MIMIR confirms C2 is dead.
#
# ══════════════════════════════════════════════════════════════════════
# IF C2 IS CONFIRMED DEAD — NEXT STEPS (DO NOT USE UNTIL MIMIR APPROVES)
# ══════════════════════════════════════════════════════════════════════
#
# C3:  stop_if_down_pct → 20
#      name: random_restart_v3_tightened_sl_v3_gen19808_stopdown20
#
# C4a: pause_hours → 24
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours24
# C4b: pause_hours → 72 (if C4a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours72
#
# C5a: long bollinger period_hours → 36
#      WARNING: historically collapses Sharpe to 0.5–0.8. High risk.
#      name: random_restart_v3_tightened_sl_v3_gen19808_boll36
# C5b: long bollinger period_hours → 60 (if C5a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_boll60
#
# C6a: timeout_hours → 240
#      name: random_restart_v3_tightened_sl_v3_gen19808_timeout240
# C6b: timeout_hours → 264 (if C6a fails)
# C6c: timeout_hours → 288 (if C6b fails)
#
# C7a: take_profit_pct → 12.0
#      name: random_restart_v3_tightened_sl_v3_gen19808_tp120
# C7b: take_profit_pct → 13.0 (if C7a fails)
# C7c: take_profit_pct → 14.0 (if C7b fails)
# C7d: take_profit_pct → 15.0 (if C7c fails)
#
# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT PROPOSE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours:       129, 135, 138, 144, 156*, 168, 192, 216
# take_profit_pct:     6.63, 7.14, 7.36, 7.38, 9.5*, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct:       1.5*, 2.0, 2.5
# pause_if_down_pct:   8 (incumbent value — C2 tests 10)
# pairs combinations:  [BTC/USD only], [BTC/USD+ETH/USD only]
# combinations:        timeout=216+TP=11.5, timeout=216+SL=2.5, TP=11.5+SL=2.5
#
# * = dead as an isolated improvement but correct in the current incumbent.
#     Keep these values. Do not propose them as new changes.
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 19808 (DO NOT OUTPUT THIS — FOR REFERENCE ONLY)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.3483 | Trades=58 | WR=41.4% | pairs=[BTC/USD, ETH/USD, SOL/USD]
# size_pct=25.0 | max_open=2 | fee_rate=0.001
# long:  momentum period=48 false | bollinger period=48 below_lower | macd period=48 bullish
# short: momentum period=48 false | bollinger period=168 above_upper | macd period=24 bearish
# take_profit_pct=9.5 | stop_loss_pct=1.5 | timeout_hours=156
# pause_if_down_pct=8 | stop_if_down_pct=18 | pause_hours=48
#
# YAML-C2 is identical to above except pause_if_down_pct=10.
# That is the only difference. Change only that field.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: CAUTION | F&G=21 (Extreme Fear) | BTC Dominance=57.16%
# TYR Directive: Reduce LIVE position sizes to 50% (live size_pct ≈ 12.5)
# Backtest optimization continues at size_pct=25.0 — do NOT change this.
# Live performance: WR 50–67% live vs 41–43% backtest — real edge confirmed.
#
# ══════════════════════════════════════════════════════════════════════
# MIMIR NOTE ON MIN_TRADES CONSTANT (INTERNAL — DO NOT RELAY TO LLM)
# ══════════════════════════════════════════════════════════════════════
#
# futures_swing MIN_TRADES=400 is incorrect vs actual trade counts of 55–60.
# This appears dormant (not enforced on this strategy path) but must be
# audited and corrected to MIN_TRADES~50 via LOKI before any structural
# strategy change that might alter trade frequency significantly.
# Do not action via LLM — escalate to LOKI separately.
#
# ══════════════════════════════════════════════════════════════════════
```