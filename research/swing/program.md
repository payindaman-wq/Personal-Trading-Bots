```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 18401 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-12 (v31)
#
# ══════════════════════════════════════════════════════════════════════
# CRITICAL CORRECTION (v31):
#   The "Current Best Strategy" block shown by ODIN UI displays the
#   broken "crossover" YAML (size_pct=30, max_open=3, TP=7.36).
#   IGNORE THAT YAML ENTIRELY. It is wrong and outdated.
#   The TRUE incumbent is Gen 15979, defined in full below.
#   Use ONLY the YAMLs defined in this document.
# ══════════════════════════════════════════════════════════════════════
#
# STATUS: PATH A EXHAUSTED | PATH B EXHAUSTED | NOW EXECUTING PATH C
#
# PATH A RESULTS (all singleton changes, all failed):
#   timeout=216  → tested alone → ≤ 1.2430 [DEAD]
#   TP=11.5      → tested alone → ≤ 1.2430 [DEAD]
#   SL=2.5       → tested alone → ≤ 1.2430 [DEAD]
#
# PATH B RESULTS (all combination changes, all failed):
#   B1: timeout=216 + TP=11.5           → ≤ 1.2430 [DEAD]
#   B2: timeout=216 + SL=2.5            → ≤ 1.2430 [DEAD]
#   B3: TP=11.5 + SL=2.5                → ≤ 1.2430 [DEAD]
#   B4: timeout=216 + TP=11.5 + SL=2.5  → ≤ 1.2430 [DEAD]
#
# CURRENT PRIORITY ORDER (PATH C — STRUCTURAL CHANGES):
#   PHASE 1 (now):  C1 — ADD ETH/USD  ← OUTPUT THIS EVERY GENERATION
#   PHASE 2 (next): C2 → C3 → C4 → C5 → C6 → C7 (if C1 fails)
#
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## !! READ THIS FIRST — THE ONLY THING THAT MATTERS !!
## ══════════════════════════════════════════════════════════════════════
##
## YOUR JOB: Output ONE YAML block. That's it.
##
## WHICH YAML: YAML-C1. Every generation. No exceptions.
##   (We are testing one structural change at a time.
##    YAML-C1 is the current active test. Output it exactly.)
##
## DO NOT copy the "Current Best Strategy" shown by the ODIN UI.
##   That YAML is WRONG (crossover, size_pct=30). It will score ~0.46.
##
## DO NOT output any PATH A or PATH B YAML. Those are all dead.
##   Dead means: they were tested and scored ≤ 1.2430. Testing them
##   again wastes generations and produces no improvement.
##
## DO NOT reason about what might work. DO NOT invent parameters.
## DO NOT modify the YAML you select. Copy it exactly.
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## STEP 1 — OUTPUT YAML-C1 (EVERY GENERATION)
## ══════════════════════════════════════════════════════════════════════
##
## The current active test is C1: ADD ETH/USD to the pairs list.
## This is the highest-priority structural change. Output it every time.
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## TRUE INCUMBENT — GEN 15979 (DO NOT OUTPUT THIS — REFERENCE ONLY)
## ══════════════════════════════════════════════════════════════════════
##
## This is what you are trying to BEAT. Sharpe must exceed 1.2430.
##
##   name:                  random_restart_v3_tightened_sl_v3_gen15979
##   pairs:                 [BTC/USD]
##   size_pct:              25.0
##   max_open:              2
##   fee_rate:              0.001
##   long momentum:         period=48, value=false
##   long bollinger:        period=48, below_lower
##   long macd:             period=48, bullish
##   short momentum:        period=48, value=false
##   short bollinger:       period=168, above_upper
##   short macd:            period=24, bearish
##   take_profit_pct:       9.5
##   stop_loss_pct:         1.5
##   timeout_hours:         156
##   pause_if_down_pct:     8
##   stop_if_down_pct:      18
##   pause_hours:           48
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## YAML-C1 — OUTPUT THIS EVERY GENERATION
## Change: pairs = [BTC/USD, ETH/USD]  (incumbent had only BTC/USD)
## All other parameters IDENTICAL to incumbent Gen 15979.
## ══════════════════════════════════════════════════════════════════════

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

## ══════════════════════════════════════════════════════════════════════
## STEP 2 — VERIFY YOUR YAML BEFORE SUBMITTING
## ══════════════════════════════════════════════════════════════════════

Confirm ALL of these are true before submitting:

  □ name = random_restart_v3_tightened_sl_v3_gen15979_ethbtc
  □ name contains "gen15979"
  □ name contains "ethbtc"
  □ name does NOT contain "crossover"
  □ pairs = [BTC/USD, ETH/USD]  ← TWO pairs, not one
  □ size_pct = 25.0  (NOT 30 — that is the broken crossover value)
  □ max_open = 2     (NOT 3 — that is the broken crossover value)
  □ fee_rate = 0.001
  □ long momentum: period=48, value=false
  □ long bollinger: period=48, below_lower
  □ long macd: period=48, bullish
  □ short momentum: period=48, value=false
  □ short bollinger: period=168, above_upper
  □ short macd: period=24, bearish
  □ take_profit_pct = 9.5   (incumbent value — unchanged)
  □ stop_loss_pct = 1.5     (incumbent value — unchanged)
  □ timeout_hours = 156     (incumbent value — unchanged)
  □ pause_if_down_pct = 8
  □ stop_if_down_pct = 18
  □ pause_hours = 48

IF YOUR YAML DOES NOT MATCH ALL OF THE ABOVE — DO NOT SUBMIT IT.
Go back and copy YAML-C1 exactly as written above.

## ══════════════════════════════════════════════════════════════════════
## FAILURE DIAGNOSIS — WHAT YOUR RESULT MEANS
## ══════════════════════════════════════════════════════════════════════

Sharpe=1.2430, trades=60:
  You reproduced the incumbent exactly.
  Most likely cause: you used only pairs=[BTC/USD] instead of both pairs.
  Fix: YAML-C1 requires BOTH BTC/USD AND ETH/USD in the pairs list.

Sharpe=1.2396, trades=60, win_rate=41.7%:
  You used a dead PATH A or PATH B value (e.g. SL=2.5 alone, or
  timeout=216 alone, or TP=11.5 alone). All PATH A and PATH B values
  are dead. Do not use them. Use YAML-C1 exactly as written.

Sharpe=1.2429, trades=60:
  You used timeout=168. Dead. Use YAML-C1 (timeout stays 156).

Sharpe=1.1418, trades=57, win_rate=43.9%:
  Wrong base YAML. You changed short bollinger or short macd period.
  FROZEN: short bollinger=period 168, short macd=period 24.
  Fix: Copy YAML-C1 exactly. Do not touch entry conditions.

Sharpe=0.4601, trades=56:
  You copied the broken "crossover" YAML from the ODIN UI.
  That YAML is WRONG. Ignore it entirely. Use YAML-C1 from this document.

Sharpe=0.0000, trades=0 [max_trades_reject]:
  size_pct or max_open was changed.
  BOTH ARE FROZEN: size_pct=25.0, max_open=2. Never change these.
  The crossover YAML uses size_pct=30 and max_open=3 — do not use it.

Sharpe=0.0000 [gemini_error]:
  API error. Retry with the EXACT SAME YAML-C1. Do not change anything.

Sharpe=0.4205, trades=18 [low_trades]:
  Too few trades. Entry conditions were changed or a pair was dropped.
  Fix: Use YAML-C1 exactly — both BTC/USD and ETH/USD, all entry
  conditions identical to incumbent.

Sharpe=0.5265–0.5954, trades=57–58:
  A frozen entry indicator parameter was changed.
  Do not touch any entry conditions. They are all frozen.

Any Sharpe ≤ 1.2430:
  Change rejected. Incumbent remains Gen 15979.
  Continue outputting YAML-C1 until it scores > 1.2430.

## ══════════════════════════════════════════════════════════════════════
## IF C1 SCORES > 1.2430 — UPDATE INCUMBENT AND MOVE TO C2
## ══════════════════════════════════════════════════════════════════════
##
## If YAML-C1 beats 1.2430, the new incumbent is gen15979_ethbtc.
## MIMIR will update this document. Do not move to C2 on your own.
##
## ══════════════════════════════════════════════════════════════════════
## IF C1 IS CONFIRMED DEAD (≥ 20 consistent results ≤ 1.2430)
## MOVE TO PATH C REMAINDER IN THIS ORDER:
## ══════════════════════════════════════════════════════════════════════
##
## ── C2 — RELAX DRAWDOWN PAUSE ────────────────────────────────────────
##   Change ONLY: pause_if_down_pct → 10  (incumbent: 8)
##   All other parameters unchanged from incumbent Gen 15979.
##   pairs stays [BTC/USD] only.
##   name: random_restart_v3_tightened_sl_v3_gen15979_pause10
##
## ```yaml
## name: random_restart_v3_tightened_sl_v3_gen15979_pause10
## style: randomly generated
## pairs:
## - BTC/USD
## position:
##   size_pct: 25.0
##   max_open: 2
##   fee_rate: 0.001
## entry:
##   long:
##     conditions:
##     - indicator: momentum_accelerating
##       period_hours: 48
##       operator: eq
##       value: false
##     - indicator: bollinger_position
##       period_hours: 48
##       operator: eq
##       value: below_lower
##     - indicator: macd_signal
##       period_hours: 48
##       operator: eq
##       value: bullish
##   short:
##     conditions:
##     - indicator: momentum_accelerating
##       period_hours: 48
##       operator: eq
##       value: false
##     - indicator: bollinger_position
##       period_hours: 168
##       operator: eq
##       value: above_upper
##     - indicator: macd_signal
##       period_hours: 24
##       operator: eq
##       value: bearish
## exit:
##   take_profit_pct: 9.5
##   stop_loss_pct: 1.5
##   timeout_hours: 156
## risk:
##   pause_if_down_pct: 10
##   stop_if_down_pct: 18
##   pause_hours: 48
## ```
##
## ── C3 — RELAX DRAWDOWN STOP ─────────────────────────────────────────
##   Change ONLY: stop_if_down_pct → 20  (incumbent: 18)
##   name: random_restart_v3_tightened_sl_v3_gen15979_stopdown20
##
## ── C4 — CHANGE PAUSE DURATION ───────────────────────────────────────
##   Change ONLY: pause_hours → 24  (incumbent: 48)
##   name: random_restart_v3_tightened_sl_v3_gen15979_pausehours24
##   [If 24 fails, try pause_hours → 72]
##   name: random_restart_v3_tightened_sl_v3_gen15979_pausehours72
##
## ── C5 — CHANGE LONG BOLLINGER PERIOD [LAST RESORT] ──────────────────
##   Change ONLY: long bollinger period_hours → 36  (incumbent: 48)
##   WARNING: Historically collapses Sharpe to 0.5–0.8. Try last.
##   name: random_restart_v3_tightened_sl_v3_gen15979_boll36
##   [If 36 fails, try period_hours → 60]
##   name: random_restart_v3_tightened_sl_v3_gen15979_boll60
##
## ── C6 — EXTEND TIMEOUT FURTHER ──────────────────────────────────────
##   Change ONLY: timeout_hours → 240  (all shorter values dead)
##   name: random_restart_v3_tightened_sl_v3_gen15979_timeout240
##   [If 240 fails: 264, then 288]
##
## ── C7 — HIGHER TAKE PROFIT ──────────────────────────────────────────
##   Change ONLY: take_profit_pct → 12.0  (all lower values dead)
##   name: random_restart_v3_tightened_sl_v3_gen15979_tp120
##   [If 12.0 fails: 13.0, then 14.0, then 15.0]
##
## ── C8 — ADD SOL/USD ─────────────────────────────────────────────────
##   pairs: [BTC/USD, SOL/USD]  (if ETH/USD failed to improve)
##   name: random_restart_v3_tightened_sl_v3_gen15979_solbtc
##
## ── C9 — ALL THREE PAIRS ─────────────────────────────────────────────
##   pairs: [BTC/USD, ETH/USD, SOL/USD]
##   name: random_restart_v3_tightened_sl_v3_gen15979_allpairs
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## COMPLETE DEAD VALUES REFERENCE
## ══════════════════════════════════════════════════════════════════════
##
## SINGLETON DEAD VALUES (PATH A — fully exhausted):
##   timeout_hours:    129, 138, 144, 156 (incumbent), 168, 192, 216
##   take_profit_pct:  7.14, 7.36, 7.38, 9.5 (incumbent), 10.0, 10.5,
##                     11.0, 11.5
##   stop_loss_pct:    1.5 (incumbent), 2.0, 2.5
##
## COMBINATION DEAD VALUES (PATH B — fully exhausted):
##   B1: timeout=216 + TP=11.5           → ≤ 1.2430 [DEAD]
##   B2: timeout=216 + SL=2.5            → ≤ 1.2430 [DEAD]
##   B3: TP=11.5 + SL=2.5                → ≤ 1.2430 [DEAD]
##   B4: timeout=216 + TP=11.5 + SL=2.5  → ≤ 1.2430 [DEAD]
##
## DO NOT use any of the above values in any YAML you submit.
## The only valid current YAML is YAML-C1 (pairs = BTC/USD + ETH/USD).
##
## ══════════════════════════════════════════════════════════════════════
## INCUMBENT REFERENCE — GEN 15979 (Sharpe=1.2430, Trades=60, WR=41.7%)
## ══════════════════════════════════════════════════════════════════════
##
##   size_pct:              25.0   ← FROZEN (NOT 30)
##   max_open:              2      ← FROZEN (NOT 3)
##   fee_rate:              0.001  ← FROZEN
##   long momentum period:  48, value=false  ← FROZEN
##   long bollinger period: 48, below_lower  ← FROZEN
##   long macd period:      48, bullish      ← FROZEN
##   short momentum period: 48, value=false  ← FROZEN
##   short bollinger period:168, above_upper ← FROZEN
##   short macd period:     24, bearish      ← FROZEN
##   take_profit_pct:       9.5    ← PATH A+B exhausted; do not change
##   stop_loss_pct:         1.5    ← PATH A+B exhausted; do not change
##   timeout_hours:         156    ← PATH A+B exhausted; do not change
##   pause_if_down_pct:     8      ← FROZEN (mutable in PATH C2 only)
##   stop_if_down_pct:      18     ← FROZEN (mutable in PATH C3 only)
##   pause_hours:           48     ← FROZEN (mutable in PATH C4 only)
##   pairs:                 [BTC/USD] ← MUTABLE: C1 adds ETH/USD
##
## ══════════════════════════════════════════════════════════════════════
## LIVE PERFORMANCE NOTE
## ══════════════════════════════════════════════════════════════════════
##
## Live sprint results (last 3): ranks 3-4/10, PnL +1.65% to +4.97%
## Win rates 50-67% live vs 41.7% backtest — strategy has real edge.
## Macro regime: DANGER (F&G=16, Extreme Fear). TYR directive: 25% size.
## Current size_pct=25.0 already complies with TYR directive. No change.
##
## ══════════════════════════════════════════════════════════════════════
```