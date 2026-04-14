```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 19809 | Incumbent: Gen 19808 (Sharpe=1.3483)
# MIMIR-reviewed 2026-04-14 (v35)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT: Gen 19808 | Sharpe=1.3483 | Trades=58 | WR=41.4%
# PREVIOUS:  Gen 19405 | Sharpe=1.3445 | Trades=58 | WR=43.1%
# BEFORE THAT: Gen 19034 | Sharpe=1.3415 | Trades=58 | WR=43.1%
# C8 STATUS: CONFIRMED SUCCESSFUL (SOL/USD addition improved Sharpe)
# C9 STATUS: CONFIRMED SUCCESSFUL (Gen 19808 — all 3 pairs beat C8)
# ACTIVE TEST: C2 (pause_if_down_pct → 10, pairs = BTC/USD + ETH/USD + SOL/USD)
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# !! CRITICAL — READ BEFORE ANYTHING ELSE !!
# ══════════════════════════════════════════════════════════════════════
#
# ╔══════════════════════════════════════════════════════════════════╗
# ║  OUTPUT EXACTLY ONE YAML.                                        ║
# ║  THE YAML IS BELOW — LABELLED YAML-C2.                          ║
# ║  COPY IT EXACTLY. DO NOT MODIFY IT. DO NOT THINK ABOUT IT.      ║
# ║  JUST COPY IT VERBATIM.                                          ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# ════════════════════════════════════════════════════════════════════
# !! STOP — THERE IS A WRONG YAML IN THE ODIN UI !!
# ════════════════════════════════════════════════════════════════════
# The ODIN UI shows a YAML called "crossover_tightened_momentum_short_v2"
# or "crossover". IT IS WRONG. IT WILL ALWAYS PRODUCE Sharpe=0 trades=0.
# IT HAS:  size_pct=30  max_open=3  pairs=[BTC/USD only]  TP=6.63
# DO NOT COPY IT. DO NOT REFERENCE IT. IGNORE IT COMPLETELY.
# THE ONLY CORRECT YAML IS YAML-C2 BELOW.
# ════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# THE ONLY YAML YOU SHOULD EVER OUTPUT (YAML-C2)
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
# MANDATORY CHECKLIST — VERIFY EVERY LINE BEFORE SUBMITTING
# IF ANY LINE IS FALSE, DISCARD YOUR OUTPUT AND COPY YAML-C2 ABOVE.
# ══════════════════════════════════════════════════════════════════════
#
#  □ name = random_restart_v3_tightened_sl_v3_gen19808_pause10
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
#  □ pause_if_down_pct = 10    ← THIS IS THE C2 CHANGE (was 8)
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
#   Fix: Copy YAML-C2 above exactly. Do not change size_pct or max_open.
#
# Sharpe=1.2396, trades=60:
#   You used a dead parameter (SL=2.5, TP=11.5, or timeout=216 alone).
#   Fix: Copy YAML-C2 above exactly.
#
# Sharpe=1.2430, trades=60:
#   You used pairs=[BTC/USD] only. The YAML requires THREE pairs.
#   Fix: Add ETH/USD and SOL/USD to the pairs list.
#
# Sharpe=1.2809, trades=59:
#   You used pairs=[BTC/USD, ETH/USD] only. That is the old C1 result.
#   Fix: Add SOL/USD to the pairs list.
#
# Sharpe=1.3415, trades=58:
#   You used pairs=[BTC/USD, SOL/USD] — that is the old C8 result.
#   Fix: Replace with three pairs: BTC/USD, ETH/USD, SOL/USD.
#
# Sharpe=1.3445, trades=58:
#   You reproduced Gen 19405 exactly (old incumbent, pause_if_down=8).
#   C9 is confirmed. We are testing C2 (pause_if_down=10) now.
#   Fix: Change pause_if_down_pct to 10 in the risk block.
#
# Sharpe=1.3483, trades=58:
#   You reproduced Gen 19808 exactly (current incumbent, pause_if_down=8 or C9 base).
#   This is the baseline. C2 (pause_if_down=10) is not yet beaten.
#   Fix: Ensure pause_if_down_pct=10 exactly. Copy YAML-C2 above.
#
# Sharpe=0.46, trades=56:
#   You copied the broken crossover YAML from the ODIN UI.
#   Fix: Copy YAML-C2 above exactly. Ignore the ODIN UI YAML entirely.
#
# Sharpe < 0.9 or trades < 50:
#   You changed entry conditions or used a completely wrong YAML.
#   Fix: Copy YAML-C2 above exactly. Change nothing except what is in C2.
#
# Sharpe > 1.3483, trades ≥ 55:
#   SUCCESS. C2 beats the incumbent. Report to MIMIR immediately.
#   Do not change anything. Submit this result as-is.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# C-SERIES STATUS TRACKING
# ══════════════════════════════════════════════════════════════════════
#
# C1 = pairs: [BTC/USD, ETH/USD]              — CONFIRMED (Gen 19024, Sharpe=1.2809)
# C8 = pairs: [BTC/USD, SOL/USD]              — CONFIRMED (Gen 19405, Sharpe=1.3445)
# C9 = pairs: [BTC/USD, ETH/USD, SOL/USD]     — CONFIRMED (Gen 19808, Sharpe=1.3483)
# C2 = pause_if_down_pct=10, pairs=all 3      — ACTIVE TEST (current YAML above)
#
# C2 is CONFIRMED DEAD if ≥ 20 clean results (trades ≥ 55) all score ≤ 1.3483.
# C2 is NOT YET TESTED — begin submitting YAML-C2 now.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# IF C2 IS CONFIRMED DEAD — NEXT STEPS IN ORDER
# ══════════════════════════════════════════════════════════════════════
#
# Do NOT move to these until MIMIR confirms C2 is dead.
# Do NOT output these YAMLs unless instructed by MIMIR.
#
# C3: stop_if_down_pct → 20
#     pairs: [BTC/USD, ETH/USD, SOL/USD]
#     name: random_restart_v3_tightened_sl_v3_gen19808_stopdown20
#
# C4a: pause_hours → 24
#      pairs: [BTC/USD, ETH/USD, SOL/USD]
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours24
# C4b: pause_hours → 72 (if C4a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_pausehours72
#
# C5a: long bollinger period_hours → 36
#      WARNING: historically collapses Sharpe to 0.5–0.8. Proceed with caution.
#      name: random_restart_v3_tightened_sl_v3_gen19808_boll36
# C5b: long bollinger period_hours → 60 (if C5a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_boll60
#
# C6a: timeout_hours → 240 (all shorter values dead, see dead list)
#      name: random_restart_v3_tightened_sl_v3_gen19808_timeout240
# C6b: timeout_hours → 264 (if C6a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_timeout264
# C6c: timeout_hours → 288 (if C6b fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_timeout288
#
# C7a: take_profit_pct → 12.0 (all lower values dead)
#      name: random_restart_v3_tightened_sl_v3_gen19808_tp120
# C7b: take_profit_pct → 13.0 (if C7a fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_tp130
# C7c: take_profit_pct → 14.0 (if C7b fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_tp140
# C7d: take_profit_pct → 15.0 (if C7c fails)
#      name: random_restart_v3_tightened_sl_v3_gen19808_tp150
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# ALL DEAD VALUES — DO NOT USE ANY OF THESE
# ══════════════════════════════════════════════════════════════════════
#
# timeout_hours (dead):    129, 135, 138, 144, 156, 168, 192, 216
#   NOTE: 156 is dead as an isolated improvement but IS CORRECT in
#   the current incumbent. Do not change it. Do not "try" it.
#
# take_profit_pct (dead):  6.63, 7.14, 7.36, 7.38, 9.5, 10.0, 10.5, 11.0, 11.5
#   NOTE: 9.5 is dead as an isolated improvement but IS CORRECT in
#   the current incumbent. Do not change it.
#
# stop_loss_pct (dead):    1.5, 2.0, 2.5
#   NOTE: 1.5 is dead as an isolated improvement but IS CORRECT in
#   the current incumbent. Do not change it.
#
# pause_if_down_pct (dead): 8  (confirmed — incumbent was 8, C2 tests 10)
#
# combinations (dead):     timeout=216+TP=11.5, timeout=216+SL=2.5,
#                          TP=11.5+SL=2.5, timeout=216+TP=11.5+SL=2.5
#
# pairs combinations (dead): [BTC/USD only], [BTC/USD+ETH/USD only]
#
# RULE: If a value appears in the dead list AND in the incumbent YAML,
# it means it was already optimized in. Keep it. Do not propose it as
# a new change. Propose something from the C-series queue instead.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# INCUMBENT REFERENCE — GEN 19808 (FOR REFERENCE ONLY — DO NOT OUTPUT)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.3483 | Trades=58 | WR=41.4% | pairs=[BTC/USD, ETH/USD, SOL/USD]
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
# NOTE: The incumbent has pause_if_down_pct=8.
# YAML-C2 tests pause_if_down_pct=10. That is the ONLY difference.
#
# PREVIOUS INCUMBENTS (SUPERSEDED — DO NOT OUTPUT)
# Gen 19405: Sharpe=1.3445 | Trades=58 | WR=43.1% | pairs=[BTC/USD, SOL/USD]
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
#   - size_pct: 30          ← WRONG (correct is 25.0)
#   - max_open: 3           ← WRONG (correct is 2)
#   - pairs: [BTC/USD]      ← WRONG (correct is 3 pairs)
#   - take_profit_pct: 6.63 ← WRONG (correct is 9.5)
#   - timeout_hours: 135    ← WRONG (correct is 156)
# Using it produces Sharpe=0.0000, trades=0. It is a dead end.
# The correct YAML is YAML-C2 above. Use only that.
#
# KEY IDENTIFIERS OF THE WRONG YAML:
#   size_pct=30  OR  max_open=3  OR  take_profit_pct=6.63
#   If you see ANY of these values, you have the wrong YAML. Stop. Use YAML-C2.
#
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# MACRO & LIVE CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Regime: CAUTION | F&G=21 (Extreme Fear) | BTC Dominance=57.25%
# TYR Directive: Reduce position sizes to 50% for LIVE trading.
#   → LIVE size_pct should be ~12.5 (50% of 25.0)
#   → BACKTEST optimization continues at size_pct=25.0 for comparability
#   → Do NOT change size_pct=25.0 in the YAML above — it is correct for backtesting
# Live performance: WR 50–67% live vs 41–43% backtest — real edge confirmed.
#
# ══════════════════════════════════════════════════════════════════════
```