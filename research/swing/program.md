```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 17801 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-12 (v29)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CRITICAL STALL PHASE (0 improvements in 1821+ gens)
# Last improvement: Gen 15979. Sharpe=1.2430.
# Three PATH A values remain untested: timeout=216, TP=11.5, SL=2.5
# The LLM must output ONE of these three YAMLs. Nothing else.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## YOUR ENTIRE JOB THIS GENERATION IS TO OUTPUT ONE YAML BLOCK.
## THE YAML IS DETERMINED BY YOUR GENERATION NUMBER.
## YOU DO NOT NEED TO REASON. YOU DO NOT NEED TO CHOOSE.
## JUST FIND YOUR GENERATION NUMBER BELOW AND COPY THAT YAML.
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## STEP 1: FIND YOUR GENERATION NUMBER → GET YOUR YAML
## ══════════════════════════════════════════════════════════════════════

Compute: GENERATION_NUMBER mod 3

  mod 3 = 0  →  OUTPUT YAML-A  (timeout=216)
  mod 3 = 1  →  OUTPUT YAML-B  (take_profit_pct=11.5)
  mod 3 = 2  →  OUTPUT YAML-C  (stop_loss_pct=2.5)

That is your entire decision. Output the corresponding YAML below.
Do not modify it. Do not add parameters. Do not use any other YAML.

## ══════════════════════════════════════════════════════════════════════
## YAML-A — OUTPUT THIS WHEN (generation mod 3 = 0)
## Change: timeout_hours 156 → 216
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_timeout216
style: randomly generated
pairs:
- BTC/USD
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
  timeout_hours: 216
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

## ══════════════════════════════════════════════════════════════════════
## YAML-B — OUTPUT THIS WHEN (generation mod 3 = 1)
## Change: take_profit_pct 9.5 → 11.5
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_tp115
style: randomly generated
pairs:
- BTC/USD
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
  take_profit_pct: 11.5
  stop_loss_pct: 1.5
  timeout_hours: 156
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

## ══════════════════════════════════════════════════════════════════════
## YAML-C — OUTPUT THIS WHEN (generation mod 3 = 2)
## Change: stop_loss_pct 1.5 → 2.5
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_sl25
style: randomly generated
pairs:
- BTC/USD
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
  stop_loss_pct: 2.5
  timeout_hours: 156
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

## ══════════════════════════════════════════════════════════════════════
## STEP 2: AFTER YOU OUTPUT YOUR YAML — VERIFY IT
## ══════════════════════════════════════════════════════════════════════

Before submitting, confirm these are true of your YAML:

  □ name matches the YAML you selected (timeout216, tp115, or sl25)
  □ name contains "gen15979"
  □ name does NOT contain "crossover"
  □ size_pct = 25.0
  □ max_open = 2
  □ fee_rate = 0.001
  □ pairs = [BTC/USD]
  □ long bollinger period = 48
  □ long macd period = 48
  □ long momentum period = 48, value = false
  □ short bollinger period = 168
  □ short macd period = 24
  □ short momentum period = 48, value = false
  □ pause_if_down_pct = 8
  □ stop_if_down_pct = 18
  □ pause_hours = 48
  □ EXACTLY ONE of the three exit parameters differs from incumbent
  □ The changed parameter is NOT in the dead list below

DEAD VALUES — if your YAML contains any of these, STOP and re-read:
  timeout_hours:    129, 138, 144, 156 (incumbent), 168, 192
  take_profit_pct:  7.14, 7.36, 7.38, 9.5 (incumbent), 10.0, 10.5, 11.0
  stop_loss_pct:    1.5 (incumbent), 2.0

THE INCUMBENT (DO NOT REPRODUCE THIS — IT IS NOT AN IMPROVEMENT):
  take_profit_pct: 9.5  |  stop_loss_pct: 1.5  |  timeout_hours: 156

## ══════════════════════════════════════════════════════════════════════
## WHAT TO DO IF ALL THREE PATH A VALUES HAVE BEEN TESTED AND FAILED
## ══════════════════════════════════════════════════════════════════════
##
## PATH A is exhausted when:
##   timeout=216 → tested, returned ≤ 1.2430
##   TP=11.5     → tested, returned ≤ 1.2430
##   SL=2.5      → tested, returned ≤ 1.2430
##
## Move to PATH B — COMBINATIONS (in order):
##
## PATH B1: timeout=216 + TP=11.5  (keep SL=1.5)
##   name: random_restart_v3_tightened_sl_v3_gen15979_timeout216_tp115
##
## PATH B2: timeout=216 + SL=2.5   (keep TP=9.5)
##   name: random_restart_v3_tightened_sl_v3_gen15979_timeout216_sl25
##
## PATH B3: TP=11.5 + SL=2.5       (keep timeout=156)
##   name: random_restart_v3_tightened_sl_v3_gen15979_tp115_sl25
##
## PATH B4: timeout=216 + TP=11.5 + SL=2.5  (three-way)
##   name: random_restart_v3_tightened_sl_v3_gen15979_timeout216_tp115_sl25
##
## For PATH B, use the same base YAML as the incumbent but change
## the indicated parameters. All other values remain frozen.
##
## ══════════════════════════════════════════════════════════════════════
## IF PATH B IS ALSO EXHAUSTED → PATH C (escalate to MIMIR first)
## ══════════════════════════════════════════════════════════════════════
##
## PATH C is for structural changes. Test in this order:
##
## C1 — ADD ETH/USD [HIGHEST PRIORITY — test this first]:
##   pairs: [BTC/USD, ETH/USD]
##   All other parameters unchanged from incumbent.
##   Rationale: Different volatility profile breaks the 1.2396 attractor.
##   Monitor trade count. Reject if trades < 30.
##   name: random_restart_v3_tightened_sl_v3_gen15979_ethbtc
##
## C2 — RELAX DRAWDOWN PAUSE:
##   pause_if_down_pct → 10  (current: 8)
##   name: random_restart_v3_tightened_sl_v3_gen15979_pause10
##
## C3 — RELAX DRAWDOWN STOP:
##   stop_if_down_pct → 20  (current: 18)
##   name: random_restart_v3_tightened_sl_v3_gen15979_stopdown20
##
## C4 — CHANGE PAUSE DURATION:
##   pause_hours → 24  (current: 48)
##   name: random_restart_v3_tightened_sl_v3_gen15979_pausehours24
##   OR
##   pause_hours → 72
##   name: random_restart_v3_tightened_sl_v3_gen15979_pausehours72
##
## C5 — CHANGE LONG BOLLINGER PERIOD [HIGH RISK — last resort]:
##   long bollinger period_hours → 36 or 60  (current: 48)
##   WARNING: May collapse Sharpe to 0.5x range. Only after C1–C4.
##   name: random_restart_v3_tightened_sl_v3_gen15979_boll36
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## FAILURE DIAGNOSIS — REFERENCE ONLY (read after getting a result)
## ══════════════════════════════════════════════════════════════════════

Sharpe=1.2430, trades=60:
  You reproduced the incumbent. Nothing changed. Move to next YAML.

Sharpe=1.2396, trades=60, win_rate=41.7%:
  You used a dead value: timeout=192, TP=11.0, or SL=2.0.
  The correct values are timeout=216, TP=11.5, SL=2.5. Use those.

Sharpe=1.2429, trades=60:
  You used timeout=168. Dead. Use timeout=216.

Sharpe=1.2395, trades=60:
  Slight variant of dead attractor. Check your YAML against the incumbent.

Sharpe=1.2338, trades=60:
  Wrong TP value. Confirm take_profit_pct=9.5 (or your authorized value).

Sharpe=1.1418, trades=57:
  Wrong base YAML. A frozen parameter is wrong.
  Check: short bollinger=168, short macd=24, momentum=false on both sides.

Sharpe=0.4601, trades=56  OR  Sharpe≈0.38–0.77:
  You used the broken UI YAML (name=crossover, size_pct=30, max_open=3).
  Discard. Re-read STEP 1. Use the correct YAML-A, YAML-B, or YAML-C.

Sharpe=0.5265–0.5954, trades=57–58:
  A frozen indicator parameter was changed.
  Revert to the incumbent base. Do not touch entry conditions.

Sharpe=0.0000, trades=0 [max_trades_reject]:
  You changed size_pct or max_open. Both are frozen at 25.0 and 2.
  Do not touch them. Ever.

Sharpe=0.0000 [gemini_error]:
  API error. Retry with the SAME YAML. Do not change anything.

Any result with trades ≠ 60 (and not PATH C):
  Wrong base YAML or frozen parameter changed. Discard. Re-read STEP 1.

Any result with Sharpe ≤ 1.2430:
  Change rejected. Incumbent remains Gen 15979. Move to next YAML.

## ══════════════════════════════════════════════════════════════════════
## COMPLETE PARAMETER REFERENCE — INCUMBENT GEN 15979
## ══════════════════════════════════════════════════════════════════════
##
##   Sharpe: 1.2430  |  Trades: 60  |  Win rate: 41.7%
##
##   name:                  random_restart_v3_tightened_sl_v3_gen15979
##   pairs:                 [BTC/USD]
##   size_pct:              25.0   ← FROZEN
##   max_open:              2      ← FROZEN
##   fee_rate:              0.001  ← FROZEN
##   long momentum period:  48, value=false  ← FROZEN
##   long bollinger period: 48, below_lower  ← FROZEN
##   long macd period:      48, bullish      ← FROZEN
##   short momentum period: 48, value=false  ← FROZEN
##   short bollinger period:168, above_upper ← FROZEN
##   short macd period:     24, bearish      ← FROZEN
##   take_profit_pct:       9.5    ← mutable (PATH A2)
##   stop_loss_pct:         1.5    ← mutable (PATH A3)
##   timeout_hours:         156    ← mutable (PATH A1)
##   pause_if_down_pct:     8      ← FROZEN (mutable in PATH C2)
##   stop_if_down_pct:      18     ← FROZEN (mutable in PATH C3)
##   pause_hours:           48     ← FROZEN (mutable in PATH C4)
##
## ══════════════════════════════════════════════════════════════════════
## EXHAUSTED VALUES — DO NOT TEST THESE AGAIN
## ══════════════════════════════════════════════════════════════════════
##
##   timeout_hours (dead):      129, 138, 144, 168, 192
##   take_profit_pct (dead):    7.14, 7.36, 7.38, ~8.x, 10.0, 10.5, 11.0
##   stop_loss_pct (dead):      2.0
##
##   UNTESTED PATH A VALUES (test these next, in order):
##   timeout:     216 → 240 → 264 → 288
##   take_profit: 11.5 → 12.0 → 13.0 → 14.0 → 15.0
##   stop_loss:   2.5 → 3.0
##
## ══════════════════════════════════════════════════════════════════════
```