```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 19025 | Incumbent: Gen 19024 (Sharpe=1.2809)
# MIMIR-reviewed 2026-04-13 (v33)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 19024 | Sharpe=1.2809 | Trades=59 | WR=42.4%
# PREVIOUS:  Gen 15979 | Sharpe=1.2430 | Trades=60 | WR=41.7%
# ACTIVE TEST: YAML-C8 (pairs = BTC/USD + SOL/USD)
# C1 STATUS: CONFIRMED SUCCESSFUL (ETH/USD addition improved Sharpe)
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# !! CRITICAL — READ BEFORE ANYTHING ELSE !!
# ══════════════════════════════════════════════════════════════════════
#
# OUTPUT EXACTLY ONE YAML. THE YAML IS BELOW. COPY IT EXACTLY.
# DO NOT MODIFY IT. DO NOT THINK ABOUT IT. JUST COPY IT.
#
# THE YAML LABELLED "Current Best Strategy" IN THE ODIN UI IS WRONG.
# IT IS CALLED "crossover". IT HAS size_pct=30 AND max_open=3.
# DO NOT COPY THAT YAML. DO NOT USE IT. IGNORE IT COMPLETELY.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# THE ONLY YAML YOU SHOULD EVER OUTPUT (YAML-C8)
# ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen19024_solbtc
style: randomly generated
pairs:
- BTC/USD
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
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

# ══════════════════════════════════════════════════════════════════════
# MANDATORY CHECKLIST — VERIFY BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# Check every line. If ANY is false, go back and copy the YAML above.
#
#  □ name = random_restart_v3_tightened_sl_v3_gen19024_solbtc
#  □ pairs has EXACTLY TWO entries: BTC/USD and SOL/USD
#  □ size_pct = 25.0   (NOT 30 — that is the wrong crossover YAML)
#  □ max_open = 2      (NOT 3 — that is the wrong crossover YAML)
#  □ fee_rate = 0.001
#  □ long momentum: period_hours=48, value=false
#  □ long bollinger: period_hours=48, value=below_lower
#  □ long macd: period_hours=48, value=bullish
#  □ short momentum: period_hours=48, value=false
#  □ short bollinger: period_hours=168, value=above_upper
#  □ short macd: period_hours=24, value=bearish
#  □ take_profit_pct = 9.5
#  □ stop_loss_pct = 1.5
#  □ timeout_hours = 156
#  □ pause_if_down_pct = 8
#  □ stop_if_down_pct = 18
#  □ pause_hours = 48
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# WHAT YOUR RESULT MEANS
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=0.0000, trades=0 [max_trades_reject]:
#   YOU CHANGED size_pct OR max_open. Do not do this. Ever.
#   The crossover YAML has size_pct=30 and max_open=3. Do not use it.
#   Fix: Copy the YAML above exactly.
#
# Sharpe=1.2396, trades=60:
#   You used a dead parameter (SL=2.5, TP=11.5, or timeout=216 alone).
#   These are all dead. Do not use any of them.
#   Fix: Copy the YAML above exactly.
#
# Sharpe=1.2430, trades=60:
#   You used only pairs=[BTC/USD] with Gen 15979 parameters.
#   Fix: The YAML above has TWO pairs: BTC/USD and SOL/USD.
#
# Sharpe=1.2809, trades=59:
#   You used pairs=[BTC/USD, ETH/USD] — that is the old C1 test.
#   C1 is confirmed. We are now testing C8 (SOL/USD).
#   Fix: Replace ETH/USD with SOL/USD in the pairs list.
#
# Sharpe=0.46, trades=56:
#   You copied the broken crossover YAML from the ODIN UI. Stop.
#   Fix: Copy the YAML above exactly. Ignore the ODIN UI YAML entirely.
#
# Sharpe < 0.9 or trades < 50:
#   You changed entry conditions or used a completely wrong YAML.
#   Fix: Copy the YAML above exactly. Change nothing.
#
# Sharpe > 1.2809:
#   SUCCESS. C8 beats the incumbent. Report to MIMIR. Do not change anything.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# C-SERIES STATUS TRACKING
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs: [BTC/USD, ETH/USD]  — CONFIRMED SUCCESSFUL (Gen 19024, Sharpe=1.2809)
# C8 = pairs: [BTC/USD, SOL/USD]  — ACTIVE TEST (current YAML above)
#
# C8 is CONFIRMED DEAD if ≥ 20 clean results (trades ≥ 55) all score ≤ 1.2809.
# C8 is NOT YET TESTED — begin submitting YAML-C8 now.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# IF C8 IS CONFIRMED DEAD — NEXT STEPS IN ORDER
# ══════════════════════════════════════════════════════════════════════
#
# Do NOT move to these until MIMIR confirms C8 is dead.
# Do NOT output these YAMLs unless instructed by MIMIR.
#
# C9: pairs: [BTC/USD, ETH/USD, SOL/USD]
#     name: random_restart_v3_tightened_sl_v3_gen19024_allpairs
#     (All other parameters from Gen 19024 incumbent)
#
# C2: pause_if_down_pct → 10  (all else from Gen 19024, pairs=[BTC/USD, ETH/USD])
#     name: random_restart_v3_tightened_sl_v3_gen19024_pause10
#
# C3: stop_if_down_pct → 20  (all else from Gen 19024, pairs=[BTC/USD, ETH/USD])
#     name: random_restart_v3_tightened_sl_v3_gen19024_stopdown20
#
# C4a: pause_hours → 24  (all else from Gen 19024, pairs=[BTC/USD, ETH/USD])
#      name: random_restart_v3_tightened_sl_v3_gen19024_pausehours24
# C4b: pause_hours → 72  (if C4a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19024_pausehours72
#
# C5a: long bollinger period_hours → 36
#      WARNING: historically collapses Sharpe to 0.5–0.8. Proceed with caution.
#      name: random_restart_v3_tightened_sl_v3_gen19024_boll36
# C5b: long bollinger period_hours → 60  (if C5a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19024_boll60
#
# C6a: timeout_hours → 240  (all shorter values dead, see dead list)
#      name: random_restart_v3_tightened_sl_v3_gen19024_timeout240
# C6b: timeout_hours → 264  (if C6a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19024_timeout264
# C6c: timeout_hours → 288  (if C6b fails)
#      name: random_restart_v3_tightened_sl_v3_gen19024_timeout288
#
# C7a: take_profit_pct → 12.0  (all lower values dead)
#      name: random_restart_v3_tightened_sl_v3_gen19024_tp120
# C7b: take_profit_pct → 13.0  (if C7a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19024_tp130
# C7c: take_profit_pct → 14.0  (if C7b fails)
#      name: random_restart_v3_tightened_sl_v3_gen19024_tp140
# C7d: take_profit_pct → 15.0  (if C7c fails)
#      name: random_restart_v3_tightened_sl_v3_gen19024_tp150
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT USE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours (dead):    129, 138, 144, 156, 168, 192, 216
# take_profit_pct (dead):  7.14, 7.36, 7.38, 9.5, 10.0, 10.5, 11.0, 11.5
# stop_loss_pct (dead):    1.5, 2.0, 2.5
# combinations (dead):     timeout=216+TP=11.5, timeout=216+SL=2.5,
#                          TP=11.5+SL=2.5, timeout=216+TP=11.5+SL=2.5
#
# NOTE: 9.5 TP and 1.5 SL are "dead" as isolated improvements but are
# CORRECT values in the current incumbent. Do not change them.
# Do not use them as your proposed change — propose something else.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 19024 (FOR REFERENCE ONLY — DO NOT OUTPUT)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.2809 | Trades=59 | WR=42.4% | pairs=[BTC/USD, ETH/USD]
# size_pct=25.0 | max_open=2 | fee_rate=0.001
# long:  momentum period=48 value=false
#        bollinger period=48 below_lower
#        macd period=48 bullish
# short: momentum period=48 value=false
#        bollinger period=168 above_upper
#        macd period=24 bearish
# take_profit_pct=9.5 | stop_loss_pct=1.5 | timeout_hours=156
# pause_if_down_pct=8 | stop_if_down_pct=18 | pause_hours=48
#
# PREVIOUS INCUMBENT — GEN 15979 (SUPERSEDED — DO NOT OUTPUT)
# Sharpe=1.2430 | Trades=60 | WR=41.7% | pairs=[BTC/USD] only
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: DANGER | F&G=12 (Extreme Fear) | BTC Dominance=56.91%
# TYR Directive: size_pct=25.0 (already compliant — do not change)
# Live performance: WR 50–67% live vs 42.4% backtest — real edge confirmed.
#
# ══════════════════════════════════════════════════════════════════════
```