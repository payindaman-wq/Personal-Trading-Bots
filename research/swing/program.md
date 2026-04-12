```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 18201 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-12 (v30)
#
# ══════════════════════════════════════════════════════════════════════
# CRITICAL CORRECTION (v30):
#   The "Current Best Strategy" block shown by ODIN UI still displays
#   the broken "crossover" YAML (size_pct=30, max_open=3, TP=7.36).
#   IGNORE THAT YAML ENTIRELY. It is wrong and outdated.
#   The TRUE incumbent is Gen 15979, defined in full below.
#   Use ONLY the YAMLs defined in this document.
# ══════════════════════════════════════════════════════════════════════
#
# STATUS: PATH A DECLARED EXHAUSTED | NOW EXECUTING PATH B+C
#
# PATH A RESULTS (all tested, all failed to beat 1.2430):
#   timeout=216  → tested, returned ≤ 1.2430 [DEAD]
#   TP=11.5      → tested, returned ≤ 1.2430 [DEAD]
#   SL=2.5       → tested, returned ≤ 1.2430 [DEAD]
#
# CURRENT PRIORITY ORDER:
#   PHASE 1 (now):  PATH B combinations (B1 → B2 → B3 → B4)
#   PHASE 2 (next): PATH C structural (C1=ETH first, highest priority)
#
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## !! READ THIS FIRST — THE ONLY THING THAT MATTERS !!
## ══════════════════════════════════════════════════════════════════════
##
## YOUR JOB: Output ONE YAML block. That's it.
##
## WHICH YAML: Determined by your generation number. See the table below.
##
## DO NOT copy the "Current Best Strategy" shown by the ODIN UI.
## That YAML is WRONG (crossover, size_pct=30). It will score ~0.46.
## Use ONLY the YAMLs in this document.
##
## DO NOT reason about what might work. DO NOT invent parameters.
## DO NOT modify the YAML you select. Copy it exactly.
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## STEP 1 — FIND YOUR GENERATION NUMBER → SELECT YOUR YAML
## ══════════════════════════════════════════════════════════════════════
##
## Compute: GENERATION_NUMBER mod 4
##
##   mod 4 = 0  →  OUTPUT YAML-B1  (timeout=216 + TP=11.5)
##   mod 4 = 1  →  OUTPUT YAML-B2  (timeout=216 + SL=2.5)
##   mod 4 = 2  →  OUTPUT YAML-B3  (TP=11.5 + SL=2.5)
##   mod 4 = 3  →  OUTPUT YAML-B4  (timeout=216 + TP=11.5 + SL=2.5)
##
## That is your entire decision. Find your YAML below. Copy it exactly.
## Do not modify it. Do not add parameters. Do not use any other YAML.
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
## YAML-B1 — OUTPUT THIS WHEN (generation mod 4 = 0)
## Change: timeout_hours=216, take_profit_pct=11.5  (SL stays 1.5)
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_timeout216_tp115
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
  timeout_hours: 216
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

## ══════════════════════════════════════════════════════════════════════
## YAML-B2 — OUTPUT THIS WHEN (generation mod 4 = 1)
## Change: timeout_hours=216, stop_loss_pct=2.5  (TP stays 9.5)
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_timeout216_sl25
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
  timeout_hours: 216
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

## ══════════════════════════════════════════════════════════════════════
## YAML-B3 — OUTPUT THIS WHEN (generation mod 4 = 2)
## Change: take_profit_pct=11.5, stop_loss_pct=2.5  (timeout stays 156)
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_tp115_sl25
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
  stop_loss_pct: 2.5
  timeout_hours: 156
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

## ══════════════════════════════════════════════════════════════════════
## YAML-B4 — OUTPUT THIS WHEN (generation mod 4 = 3)
## Change: timeout_hours=216, take_profit_pct=11.5, stop_loss_pct=2.5
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979_timeout216_tp115_sl25
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
  stop_loss_pct: 2.5
  timeout_hours: 216
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

## ══════════════════════════════════════════════════════════════════════
## STEP 2 — VERIFY YOUR YAML BEFORE SUBMITTING
## ══════════════════════════════════════════════════════════════════════

Confirm ALL of these are true before submitting:

  □ name contains "gen15979"
  □ name does NOT contain "crossover"
  □ name matches the YAML you selected (timeout216_tp115, timeout216_sl25,
    tp115_sl25, or timeout216_tp115_sl25)
  □ size_pct = 25.0  (NOT 30 — that is the broken crossover value)
  □ max_open = 2     (NOT 3 — that is the broken crossover value)
  □ fee_rate = 0.001
  □ pairs = [BTC/USD]
  □ long momentum: period=48, value=false
  □ long bollinger: period=48, below_lower
  □ long macd: period=48, bullish
  □ short momentum: period=48, value=false
  □ short bollinger: period=168, above_upper
  □ short macd: period=24, bearish
  □ pause_if_down_pct = 8
  □ stop_if_down_pct = 18
  □ pause_hours = 48
  □ Your exit values are from the PATH B combinations (not incumbent values)

DEAD EXIT VALUES — if your YAML contains any of these, STOP:
  timeout_hours:    129, 138, 144, 156 (incumbent), 168, 192
  take_profit_pct:  7.14, 7.36, 7.38, 9.5 (incumbent), 10.0, 10.5, 11.0
  stop_loss_pct:    1.5 (incumbent), 2.0

THE INCUMBENT (DO NOT REPRODUCE THIS):
  take_profit_pct: 9.5  |  stop_loss_pct: 1.5  |  timeout_hours: 156

## ══════════════════════════════════════════════════════════════════════
## IF PATH B IS EXHAUSTED — MOVE TO PATH C
## (All four B YAMLs returned Sharpe ≤ 1.2430)
## ══════════════════════════════════════════════════════════════════════
##
## PATH C — STRUCTURAL CHANGES (test in this exact order):
##
## ── C1 — ADD ETH/USD [HIGHEST PRIORITY — TEST THIS FIRST] ────────────
##
##   pairs: [BTC/USD, ETH/USD]
##   All other parameters unchanged from incumbent.
##   Rationale: Different volatility profile may break the 1.2430 ceiling.
##   Reject if trades < 30.
##   name: random_restart_v3_tightened_sl_v3_gen15979_ethbtc
##
## ```yaml
## name: random_restart_v3_tightened_sl_v3_gen15979_ethbtc
## style: randomly generated
## pairs:
## - BTC/USD
## - ETH/USD
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
##   pause_if_down_pct: 8
##   stop_if_down_pct: 18
##   pause_hours: 48
## ```
##
## ── C2 — RELAX DRAWDOWN PAUSE ────────────────────────────────────────
##   pause_if_down_pct → 10  (current: 8)
##   All other parameters unchanged from incumbent.
##   name: random_restart_v3_tightened_sl_v3_gen15979_pause10
##
## ── C3 — RELAX DRAWDOWN STOP ─────────────────────────────────────────
##   stop_if_down_pct → 20  (current: 18)
##   name: random_restart_v3_tightened_sl_v3_gen15979_stopdown20
##
## ── C4 — CHANGE PAUSE DURATION ───────────────────────────────────────
##   pause_hours → 24  (current: 48)
##   name: random_restart_v3_tightened_sl_v3_gen15979_pausehours24
##   OR
##   pause_hours → 72
##   name: random_restart_v3_tightened_sl_v3_gen15979_pausehours72
##
## ── C5 — CHANGE LONG BOLLINGER PERIOD [LAST RESORT] ──────────────────
##   long bollinger period_hours → 36 or 60  (current: 48)
##   WARNING: Historically collapses Sharpe to 0.5–0.8 range.
##   Only test after C1–C4 are all exhausted.
##   name: random_restart_v3_tightened_sl_v3_gen15979_boll36
##
## ── C6 — EXTEND TIMEOUT FURTHER ──────────────────────────────────────
##   timeout_hours → 240  (if 216 failed as singleton)
##   name: random_restart_v3_tightened_sl_v3_gen15979_timeout240
##
## ── C7 — HIGHER TAKE PROFIT ──────────────────────────────────────────
##   take_profit_pct → 12.0 or 13.0  (if 11.5 failed as singleton)
##   name: random_restart_v3_tightened_sl_v3_gen15979_tp120
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## FAILURE DIAGNOSIS — WHAT YOUR RESULT MEANS
## ══════════════════════════════════════════════════════════════════════

Sharpe=1.2430, trades=60:
  You reproduced the incumbent exactly. Nothing changed.
  Check: Did you copy the crossover YAML? Did you use incumbent exit values?
  Fix: Use the correct PATH B YAML for your generation number.

Sharpe=1.2396, trades=60, win_rate=41.7%:
  You used a DEAD singleton value: timeout=192, TP=11.0, or SL=2.0.
  These are NOT the PATH B values. PATH B uses COMBINATIONS.
  Fix: Use YAML-B1 through YAML-B4 as defined above.

Sharpe=1.2429, trades=60:
  You used timeout=168. Dead. PATH B uses timeout=216 in combinations.

Sharpe=0.4601, trades=56:
  You copied the broken "crossover" YAML from the ODIN UI.
  That YAML is WRONG. Ignore it. Use only the YAMLs in this document.

Sharpe=0.0000, trades=0 [max_trades_reject]:
  size_pct or max_open was changed.
  BOTH ARE FROZEN: size_pct=25.0, max_open=2. Never change these.
  Do NOT use size_pct=30 or max_open=3 (those are crossover values).

Sharpe=0.0000 [gemini_error]:
  API error. Retry with the EXACT SAME YAML. Do not change anything.

Sharpe=0.5265–0.5954, trades=57–58:
  A frozen entry indicator parameter was changed.
  Do not touch any entry conditions. They are all frozen.

Sharpe=1.1418, trades=57:
  Wrong base YAML. Check short bollinger=168, short macd=24.

Any Sharpe ≤ 1.2430:
  Change rejected. Incumbent remains Gen 15979. Move to next YAML.

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
## PATH B COMBINATIONS (test these — not yet confirmed dead):
##   B1: timeout=216 + TP=11.5      → YAML-B1
##   B2: timeout=216 + SL=2.5       → YAML-B2
##   B3: TP=11.5 + SL=2.5           → YAML-B3
##   B4: timeout=216 + TP=11.5 + SL=2.5 → YAML-B4
##
## NEXT SINGLETON VALUES TO TRY (if PATH B also fails, use in PATH C):
##   timeout:     240 → 264 → 288
##   take_profit: 12.0 → 13.0 → 14.0 → 15.0
##   stop_loss:   3.0
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
##   take_profit_pct:       9.5    ← PATH A exhausted; use PATH B combos
##   stop_loss_pct:         1.5    ← PATH A exhausted; use PATH B combos
##   timeout_hours:         156    ← PATH A exhausted; use PATH B combos
##   pause_if_down_pct:     8      ← FROZEN (mutable in PATH C2 only)
##   stop_if_down_pct:      18     ← FROZEN (mutable in PATH C3 only)
##   pause_hours:           48     ← FROZEN (mutable in PATH C4 only)
##
## ══════════════════════════════════════════════════════════════════════
```