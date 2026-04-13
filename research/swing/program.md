```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 19406 | Incumbent: Gen 19405 (Sharpe=1.3445)
# MIMIR-reviewed 2026-04-13 (v34)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 19405 | Sharpe=1.3445 | Trades=58 | WR=43.1%
# PREVIOUS:  Gen 19034 | Sharpe=1.3415 | Trades=58 | WR=43.1%
# BEFORE THAT: Gen 19024 | Sharpe=1.2809 | Trades=59 | WR=42.4%
# C8 STATUS: CONFIRMED SUCCESSFUL (SOL/USD addition improved Sharpe)
# ACTIVE TEST: YAML-C9 (pairs = BTC/USD + ETH/USD + SOL/USD)
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# !! CRITICAL — READ BEFORE ANYTHING ELSE !!
# ══════════════════════════════════════════════════════════════════════
#
# ╔══════════════════════════════════════════════════════════════════╗
# ║  OUTPUT EXACTLY ONE YAML.                                        ║
# ║  THE YAML IS BELOW — LABELLED YAML-C9.                          ║
# ║  COPY IT EXACTLY. DO NOT MODIFY IT. DO NOT THINK ABOUT IT.      ║
# ║  JUST COPY IT VERBATIM.                                          ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# THERE IS A WRONG YAML IN THE ODIN UI CALLED "crossover".
# IT HAS size_pct=30 AND max_open=3.
# DO NOT COPY THAT YAML. DO NOT USE IT. IGNORE IT COMPLETELY.
# USING IT PRODUCES Sharpe=0.0000, trades=0. IT IS ALWAYS WRONG.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# THE ONLY YAML YOU SHOULD EVER OUTPUT (YAML-C9)
# ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen19405_allpairs
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
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

# ══════════════════════════════════════════════════════════════════════
# MANDATORY CHECKLIST — VERIFY EVERY LINE BEFORE SUBMITTING
# IF ANY LINE IS FALSE, DISCARD YOUR OUTPUT AND COPY THE YAML ABOVE.
# ══════════════════════════════════════════════════════════════════════
#
#  □ name = random_restart_v3_tightened_sl_v3_gen19405_allpairs
#  □ pairs has EXACTLY THREE entries: BTC/USD, ETH/USD, SOL/USD
#  □ size_pct = 25.0     (NOT 30 — 30 is the wrong crossover YAML)
#  □ max_open = 2        (NOT 3 — 3 is the wrong crossover YAML)
#  □ fee_rate = 0.001
#  □ long momentum:  period_hours=48, value=false
#  □ long bollinger: period_hours=48, value=below_lower
#  □ long macd:      period_hours=48, value=bullish
#  □ short momentum:  period_hours=48, value=false
#  □ short bollinger: period_hours=168, value=above_upper
#  □ short macd:      period_hours=24, value=bearish
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
#   YOU COPIED THE WRONG YAML. You used size_pct=30 or max_open=3.
#   The crossover YAML in the ODIN UI is ALWAYS WRONG. Never use it.
#   Fix: Copy YAML-C9 above exactly. Do not change size_pct or max_open.
#
# Sharpe=1.2396, trades=60:
#   You used a dead parameter (SL=2.5, TP=11.5, or timeout=216 alone).
#   Fix: Copy YAML-C9 above exactly.
#
# Sharpe=1.2430, trades=60:
#   You used pairs=[BTC/USD] only. The YAML requires THREE pairs.
#   Fix: Add ETH/USD and SOL/USD to the pairs list.
#
# Sharpe=1.2809, trades=59:
#   You used pairs=[BTC/USD, ETH/USD] only. That is the old C1 result.
#   C1 is confirmed. C8 is confirmed. We are now testing C9 (all 3 pairs).
#   Fix: Add SOL/USD to the pairs list.
#
# Sharpe=1.3415, trades=58:
#   You used pairs=[BTC/USD, SOL/USD] — that is the old C8 result.
#   C8 is confirmed. We are now testing C9 (BTC + ETH + SOL).
#   Fix: Replace with three pairs: BTC/USD, ETH/USD, SOL/USD.
#
# Sharpe=1.3445, trades=58:
#   You reproduced the current incumbent exactly. This is the baseline.
#   C9 is not yet beaten. Keep submitting YAML-C9 to test it.
#
# Sharpe=0.46, trades=56:
#   You copied the broken crossover YAML from the ODIN UI.
#   Fix: Copy YAML-C9 above exactly. Ignore the ODIN UI YAML entirely.
#
# Sharpe < 0.9 or trades < 50:
#   You changed entry conditions or used a completely wrong YAML.
#   Fix: Copy YAML-C9 above exactly. Change nothing.
#
# Sharpe > 1.3445, trades ≥ 55:
#   SUCCESS. C9 beats the incumbent. Report to MIMIR immediately.
#   Do not change anything. Submit this result as-is.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# C-SERIES STATUS TRACKING
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs: [BTC/USD, ETH/USD]         — CONFIRMED SUCCESSFUL (Gen 19024, Sharpe=1.2809)
# C8 = pairs: [BTC/USD, SOL/USD]         — CONFIRMED SUCCESSFUL (Gen 19405, Sharpe=1.3445)
# C9 = pairs: [BTC/USD, ETH/USD, SOL/USD]— ACTIVE TEST (current YAML above)
#
# C9 is CONFIRMED DEAD if ≥ 20 clean results (trades ≥ 55) all score ≤ 1.3445.
# C9 is NOT YET TESTED — begin submitting YAML-C9 now.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# IF C9 IS CONFIRMED DEAD — NEXT STEPS IN ORDER
# ══════════════════════════════════════════════════════════════════════
#
# Do NOT move to these until MIMIR confirms C9 is dead.
# Do NOT output these YAMLs unless instructed by MIMIR.
#
# C2: pause_if_down_pct → 10
#     pairs: [BTC/USD, SOL/USD] (incumbent pair set)
#     name: random_restart_v3_tightened_sl_v3_gen19405_pause10
#
# C3: stop_if_down_pct → 20
#     pairs: [BTC/USD, SOL/USD]
#     name: random_restart_v3_tightened_sl_v3_gen19405_stopdown20
#
# C4a: pause_hours → 24
#      pairs: [BTC/USD, SOL/USD]
#      name: random_restart_v3_tightened_sl_v3_gen19405_pausehours24
# C4b: pause_hours → 72 (if C4a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19405_pausehours72
#
# C5a: long bollinger period_hours → 36
#      WARNING: historically collapses Sharpe to 0.5–0.8. Proceed with caution.
#      name: random_restart_v3_tightened_sl_v3_gen19405_boll36
# C5b: long bollinger period_hours → 60 (if C5a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19405_boll60
#
# C6a: timeout_hours → 240 (all shorter values dead, see dead list)
#      name: random_restart_v3_tightened_sl_v3_gen19405_timeout240
# C6b: timeout_hours → 264 (if C6a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19405_timeout264
# C6c: timeout_hours → 288 (if C6b fails)
#      name: random_restart_v3_tightened_sl_v3_gen19405_timeout288
#
# C7a: take_profit_pct → 12.0 (all lower values dead)
#      name: random_restart_v3_tightened_sl_v3_gen19405_tp120
# C7b: take_profit_pct → 13.0 (if C7a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19405_tp130
# C7c: take_profit_pct → 14.0 (if C7b fails)
#      name: random_restart_v3_tightened_sl_v3_gen19405_tp140
# C7d: take_profit_pct → 15.0 (if C7c fails)
#      name: random_restart_v3_tightened_sl_v3_gen19405_tp150
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT USE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours (dead):    129, 138, 144, 156, 168, 192, 216
#   NOTE: 156 is dead as an isolated improvement but IS CORRECT in
#   the current incumbent. Do not change it. Do not "try" it.
#
# take_profit_pct (dead):  7.14, 7.36, 7.38, 9.5, 10.0, 10.5, 11.0, 11.5
#   NOTE: 9.5 is dead as an isolated improvement but IS CORRECT in
#   the current incumbent. Do not change it.
#
# stop_loss_pct (dead):    1.5, 2.0, 2.5
#   NOTE: 1.5 is dead as an isolated improvement but IS CORRECT in
#   the current incumbent. Do not change it.
#
# combinations (dead):     timeout=216+TP=11.5, timeout=216+SL=2.5,
#                          TP=11.5+SL=2.5, timeout=216+TP=11.5+SL=2.5
#
# RULE: If a value appears in the dead list AND in the incumbent YAML,
# it means it was already optimized in. Keep it. Do not propose it as
# a new change. Propose something from the C-series queue instead.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 19405 (FOR REFERENCE ONLY — DO NOT OUTPUT)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.3445 | Trades=58 | WR=43.1% | pairs=[BTC/USD, SOL/USD]
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
# PREVIOUS INCUMBENTS (SUPERSEDED — DO NOT OUTPUT)
# Gen 19034: Sharpe=1.3415 | Trades=58 | WR=43.1% | pairs=[BTC/USD, SOL/USD]
# Gen 19024: Sharpe=1.2809 | Trades=59 | WR=42.4% | pairs=[BTC/USD, ETH/USD]
# Gen 15979: Sharpe=1.2430 | Trades=60 | WR=41.7% | pairs=[BTC/USD] only
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# CRITICAL: WHY THE ODIN UI YAML IS WRONG
# ══════════════════════════════════════════════════════════════════════
#
# The ODIN UI shows a YAML called "crossover_tightened_momentum_short_v2".
# THIS YAML IS WRONG. DO NOT USE IT. EVER.
# It has:
#   - size_pct: 30         ← WRONG (correct is 25.0)
#   - max_open: 3          ← WRONG (correct is 2)
#   - pairs: [BTC/USD]     ← WRONG (correct is 3 pairs)
#   - take_profit_pct: 6.63 ← WRONG (correct is 9.5)
#   - timeout_hours: 129   ← WRONG (correct is 156)
# Using it produces Sharpe=0.0000, trades=0. It is a dead end.
# The correct YAML is YAML-C9 above. Use only that.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: DANGER | F&G=12 (Extreme Fear) | BTC Dominance=57.26%
# TYR Directive: size_pct=25.0 (already compliant — do not change)
# Live performance: WR 50–67% live vs 43.1% backtest — real edge confirmed.
#
# ══════════════════════════════════════════════════════════════════════
```