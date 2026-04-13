```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 18801 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-13 (v32)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 15979 | Sharpe=1.2430 | Trades=60 | WR=41.7%
# ACTIVE TEST: YAML-C1 (pairs = BTC/USD + ETH/USD)
# STATUS: C1 unconfirmed — LLM compliance rate ~35% last 20 gens
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
# THE ONLY YAML YOU SHOULD EVER OUTPUT (YAML-C1)
# ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_ethbtc
style: randomly generated
pairs:
- BTC/USD
- ETH/USD
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
#  □ name = random_restart_v3_tightened_sl_v3_gen15979_ethbtc
#  □ pairs has EXACTLY TWO entries: BTC/USD and ETH/USD
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
#   Fix: Copy the YAML above exactly. pairs must have BOTH BTC/USD AND ETH/USD.
#
# Sharpe=1.2430, trades=60:
#   You used only pairs=[BTC/USD]. You reproduced the incumbent exactly.
#   Fix: The YAML above has TWO pairs. Make sure both are present.
#
# Sharpe=0.46, trades=56:
#   You copied the broken crossover YAML from the ODIN UI. Stop.
#   Fix: Copy the YAML above exactly. Ignore the ODIN UI YAML entirely.
#
# Sharpe < 0.9 or trades < 50:
#   You changed entry conditions or used a completely wrong YAML.
#   Fix: Copy the YAML above exactly. Change nothing.
#
# Sharpe > 1.2430:
#   SUCCESS. C1 beats the incumbent. Report to MIMIR. Do not change anything.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# C1 STATUS TRACKING
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs: [BTC/USD, ETH/USD], all other parameters from Gen 15979.
#
# C1 is CONFIRMED DEAD if ≥ 20 clean results (trades > 60) all score ≤ 1.2430.
# C1 is NOT YET CONFIRMED — most recent failures are LLM compliance errors,
# not genuine C1 test results. Continue submitting YAML-C1 every generation.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# IF C1 IS CONFIRMED DEAD — NEXT STEPS IN ORDER
# ══════════════════════════════════════════════════════════════════════
#
# Do NOT move to these until MIMIR confirms C1 is dead.
# Do NOT output these YAMLs unless instructed by MIMIR.
#
# C2: pause_if_down_pct → 10  (all else from Gen 15979, pairs=[BTC/USD])
#     name: random_restart_v3_tightened_sl_v3_gen15979_pause10
#
# C3: stop_if_down_pct → 20  (all else from Gen 15979, pairs=[BTC/USD])
#     name: random_restart_v3_tightened_sl_v3_gen15979_stopdown20
#
# C4a: pause_hours → 24  (all else from Gen 15979, pairs=[BTC/USD])
#      name: random_restart_v3_tightened_sl_v3_gen15979_pausehours24
# C4b: pause_hours → 72  (if C4a fails)
#      name: random_restart_v3_tightened_sl_v3_gen15979_pausehours72
#
# C5a: long bollinger period_hours → 36  (WARNING: historically collapses to 0.5–0.8)
#      name: random_restart_v3_tightened_sl_v3_gen15979_boll36
# C5b: long bollinger period_hours → 60  (if C5a fails)
#      name: random_restart_v3_tightened_sl_v3_gen15979_boll60
#
# C6a: timeout_hours → 240  (all shorter values dead)
#      name: random_restart_v3_tightened_sl_v3_gen15979_timeout240
# C6b: timeout_hours → 264  (if C6a fails)
#      name: random_restart_v3_tightened_sl_v3_gen15979_timeout264
# C6c: timeout_hours → 288  (if C6b fails)
#      name: random_restart_v3_tightened_sl_v3_gen15979_timeout288
#
# C7a: take_profit_pct → 12.0  (all lower values dead)
#      name: random_restart_v3_tightened_sl_v3_gen15979_tp120
# C7b: take_profit_pct → 13.0  (if C7a fails)
#      name: random_restart_v3_tightened_sl_v3_gen15979_tp130
# C7c: take_profit_pct → 14.0  (if C7b fails)
# C7d: take_profit_pct → 15.0  (if C7c fails)
#
# C8: pairs: [BTC/USD, SOL/USD]
#     name: random_restart_v3_tightened_sl_v3_gen15979_solbtc
#
# C9: pairs: [BTC/USD, ETH/USD, SOL/USD]
#     name: random_restart_v3_tightened_sl_v3_gen15979_allpairs
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
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 15979 (FOR REFERENCE ONLY — DO NOT OUTPUT)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.2430 | Trades=60 | WR=41.7% | pairs=[BTC/USD]
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
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: DANGER | F&G=12 (Extreme Fear) | BTC Dominance=56.91%
# TYR Directive: size_pct=25.0 (already compliant — do not change)
# Live performance: WR 50–67% live vs 41.7% backtest — real edge confirmed.
#
# ══════════════════════════════════════════════════════════════════════
```