```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 17401 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-11 (v27)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CRITICAL STALL PHASE (0 improvements in 1421+ gens)
# Last improvement: Gen 15979. Sharpe climbed 0.0799 → 1.2430.
# The core indicator triplet is CONFIRMED VIABLE AND FROZEN.
#
# ⚠️ TRADE COUNT CEILING: 60 (HARD). Minimum: 30.
# ⚠️ size_pct=25.0 and max_open=2 are FROZEN. Changing either → 0 trades.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ MANDATORY FIRST READ: THE UI IS BROKEN. IGNORE IT COMPLETELY. ⚠️
## ══════════════════════════════════════════════════════════════════════
##
## The UI shows: name=crossover, size_pct=30, max_open=3, TP=7.36,
## timeout=129. THIS IS WRONG. USING THIS YAML WILL WASTE A GENERATION.
## DO NOT USE THE UI YAML. DO NOT USE name=crossover. EVER.
##
## THE ONLY VALID INCUMBENT IS IN STEP 0 BELOW.
##
## IF YOUR YAML CONTAINS ANY OF:
##   name: crossover
##   size_pct: 30
##   max_open: 3
##   take_profit_pct: 7.36
##   timeout_hours: 129
## YOU HAVE THE WRONG YAML. STOP. RE-READ STEP 0.
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## CRITICAL: EXHAUSTED VALUES — DO NOT TEST THESE AGAIN. EVER.
## ══════════════════════════════════════════════════════════════════════
##
## These single-parameter values have ALL been tested and confirmed
## inferior (Sharpe ≤ 1.2430). Testing them again wastes a generation
## and produces exactly Sharpe=1.2396, trades=60. DO NOT DO THIS.
##
##   timeout_hours EXHAUSTED:  129, 138, 144, 156, 168, 192
##     → NEXT UNTESTED: 216, then 240, 264, 288
##
##   take_profit_pct EXHAUSTED: 7.14, 7.36, 7.38, ~8.x, 9.5,
##                               10.0, 10.5, 11.0
##     → NEXT UNTESTED: 11.5, then 12.0, 13.0, 14.0, 15.0
##
##   stop_loss_pct EXHAUSTED:  1.5, 2.0
##     → NEXT UNTESTED: 2.5, then 3.0
##
## IF YOUR PROPOSED YAML CONTAINS ANY EXHAUSTED VALUE, STOP.
## Replace it with the NEXT UNTESTED value from the list above.
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## STEP 0: THE INCUMBENT YAML — COPY THIS EXACTLY AS YOUR BASE
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979
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
  timeout_hours: 156
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

INCUMBENT KEY VALUES — MEMORIZE BEFORE PROCEEDING:
  name:            random_restart_v3_tightened_sl_v3_gen15979
  take_profit_pct: 9.5       ← NOT 7.36. NOT 11.0. EXACTLY 9.5.
  stop_loss_pct:   1.5       ← NOT 2.0. EXACTLY 1.5.
  timeout_hours:   156       ← NOT 129. NOT 192. EXACTLY 156.
  size_pct:        25.0      ← FROZEN. NOT 30. EXACTLY 25.0.
  max_open:        2         ← FROZEN. NOT 3. EXACTLY 2.
  short bollinger: 168       ← FROZEN
  short macd:      24        ← FROZEN
  momentum value:  false     ← FROZEN on BOTH long AND short sides
  pairs:           [BTC/USD]
  Sharpe:          1.2430 | Trades: 60 | Win rate: 41.7%

## ══════════════════════════════════════════════════════════════════════
## STEP 1: PRE-MUTATION CHECKLIST — WRITE THESE OUT BEFORE ANY YAML
## ══════════════════════════════════════════════════════════════════════

Copy and fill in exactly:

  INCUMBENT NAME:           random_restart_v3_tightened_sl_v3_gen15979
  INCUMBENT TP:             9.5
  INCUMBENT TIMEOUT:        156
  INCUMBENT SL:             1.5
  INCUMBENT SIZE:           25.0
  INCUMBENT MAX_OPEN:       2
  INCUMBENT SHORT BOLLINGER: 168
  INCUMBENT SHORT MACD:     24

If ANY value you wrote does not match the above, STOP.
Re-read STEP 0 until all values match. Then continue.

## ══════════════════════════════════════════════════════════════════════
## STEP 2: DETERMINE YOUR GENERATION NUMBER AND MUTATION
## ══════════════════════════════════════════════════════════════════════

Use the ROTATION SCHEDULE below to determine which PATH to use.
The rotation is strictly mechanical — no discretion.

  Generation mod 3 = 0 → PATH A1 (timeout)
  Generation mod 3 = 1 → PATH A2 (take_profit_pct)
  Generation mod 3 = 2 → PATH A3 (stop_loss_pct)

Within each path, always use the LOWEST UNTESTED value from that path's
list. Do not skip ahead. Do not re-test exhausted values.

Write out before writing any YAML:

  MY GENERATION NUMBER: [number]
  GENERATION MOD 3: [0, 1, or 2]
  ASSIGNED PATH: [A1, A2, or A3]
  CHANGING: [parameter] from [old value] to [new value]
  CONFIRM new value is NOT in the EXHAUSTED list: [yes/no]
  CONFIRM new value is NOT the same as incumbent: [yes/no]

If either CONFIRM is "no", stop and use the next untested value.

## ══════════════════════════════════════════════════════════════════════
## AUTHORIZED MUTATION PATHS
## ══════════════════════════════════════════════════════════════════════

### PATH A1 — TIMEOUT (use when gen mod 3 = 0):

  EXHAUSTED (do not test): 129, 138, 144, 156, 168, 192
  NEXT TO TEST IN ORDER:   216, 240, 264, 288

  Current next value: 216
  (If 216 already tested this session and returned ≤1.2430, use 240.)

  All known results:
    129 → stale UI artifact (dead)
    138 → 1.2063 (superseded)
    144 → 1.2288 (dead)
    156 → 1.2430 (INCUMBENT)
    168 → 1.2429 (inferior — one step below incumbent)
    192 → 1.2396 (EXHAUSTED — tested ~8 times, always 1.2396)
    216 → UNTESTED ← USE THIS NEXT
    240 → UNTESTED
    264 → UNTESTED
    288 → UNTESTED

  Naming: random_restart_v3_tightened_sl_v3_gen15979_timeout216

### PATH A2 — TAKE PROFIT (use when gen mod 3 = 1):

  EXHAUSTED (do not test): 7.14, 7.36, 7.38, ~8.x, 9.5, 10.0, 10.5, 11.0
  NEXT TO TEST IN ORDER:   11.5, 12.0, 13.0, 14.0, 15.0

  Current next value: 11.5
  ⚠️ TP curve is NON-MONOTONE. Values above 9.5 have not improved linearly.
  ⚠️ 10.0 and 10.5 both returned ~1.1882. 11.0 returned 1.2396.
  ⚠️ Higher TP reduces trade count by allowing more trades to time out.
     Monitor trade count. Reject if trades < 30 or > 60.

  All known results:
    7.14 → ~0.7734 (dead)
    7.36 → dead (UI artifact)
    7.38 → 1.1311 (superseded)
    ~8.x → 1.1426 (superseded)
    9.5  → 1.2430 (INCUMBENT)
    10.0 → ~1.1882 (dead)
    10.5 → ~1.1882 (dead)
    11.0 → 1.2396 (EXHAUSTED)
    11.5 → UNTESTED ← USE THIS NEXT
    12.0 → UNTESTED
    13.0 → UNTESTED

  Naming: random_restart_v3_tightened_sl_v3_gen15979_tp115

### PATH A3 — STOP LOSS (use when gen mod 3 = 2):

  EXHAUSTED (do not test): 1.5, 2.0
  NEXT TO TEST IN ORDER:   2.5, 3.0

  Current next value: 2.5
  ⚠️ SL changes affect which trades are stopped out vs. timed out.
  ⚠️ Wider SL may increase trade duration, affecting timeout interactions.
  ⚠️ Monitor trade count. Reject if trades < 30 or > 60.

  All known results:
    1.5 → 1.2430 (INCUMBENT)
    2.0 → 1.2396 (EXHAUSTED)
    2.5 → UNTESTED ← USE THIS NEXT
    3.0 → UNTESTED

  Naming: random_restart_v3_tightened_sl_v3_gen15979_sl25

## ══════════════════════════════════════════════════════════════════════
## PATH B — COMBINATIONS
## (Use only after A1 next value, A2 next value, AND A3 next value
##  have each been individually tested and returned ≤ 1.2430)
## ══════════════════════════════════════════════════════════════════════

PATH B is authorized ONLY if timeout=216, TP=11.5, and SL=2.5 have
all been tested individually and all returned ≤ 1.2430.

Do NOT jump to PATH B before testing those three individual values.

Combinations to test (in order):
  B1: timeout=216 + TP=11.5
      name: ...gen15979_timeout216_tp115
  B2: timeout=216 + SL=2.5
      name: ...gen15979_timeout216_sl25
  B3: TP=11.5 + SL=2.5
      name: ...gen15979_tp115_sl25
  B4: timeout=216 + TP=11.5 + SL=2.5 (three changes — last resort)
      name: ...gen15979_timeout216_tp115_sl25

## ══════════════════════════════════════════════════════════════════════
## PATH C — NEW DIMENSIONS
## (Use only after PATH B is exhausted — escalate to MIMIR first)
## ══════════════════════════════════════════════════════════════════════

C1: Add ETH/USD to pairs: pairs: [BTC/USD, ETH/USD]
    ⚠️ Will significantly change trade count. Monitor carefully.
    ⚠️ This is the HIGHEST PRIORITY PATH C option — different asset
       volatility may escape the 1.2396 attractor entirely.
    name: ...gen15979_ethbtc

C2: pause_if_down_pct → 10 (current: 8)
    Rationale: less aggressive pausing may allow more winning trades
    during volatile regimes.
    name: ...gen15979_pause10

C3: stop_if_down_pct → 20 (current: 18)
    name: ...gen15979_stopdown20

C4: pause_hours → 24 or 72 (current: 48)
    name: ...gen15979_pausehours24

C5: long bollinger period → 36 or 60 (current: 48)
    ⚠️ HIGH RISK — indicator change may collapse Sharpe to 0.5x range.
    ⚠️ Only test if C1–C4 are exhausted.
    name: ...gen15979_boll36

## ══════════════════════════════════════════════════════════════════════
## STEP 3: WRITE THE MUTATED YAML
## ══════════════════════════════════════════════════════════════════════

1. Copy the INCUMBENT YAML from STEP 0 word-for-word.
2. Change ONLY the ONE parameter identified in STEP 2.
3. Every other value must be character-for-character identical.
4. Update the name field using the naming convention for your path.

REMINDER: Only these values are mutable in PATH A:
  take_profit_pct, stop_loss_pct, timeout_hours

Everything else is FROZEN:
  size_pct=25.0, max_open=2, fee_rate=0.001,
  short bollinger period=168, short macd period=24,
  momentum_accelerating value=false (BOTH sides),
  long bollinger period=48, long macd period=48,
  long momentum period=48, short momentum period=48,
  pause_if_down_pct=8, stop_if_down_pct=18, pause_hours=48,
  pairs=[BTC/USD]

## ══════════════════════════════════════════════════════════════════════
## STEP 4: VERIFY BEFORE SUBMITTING
## ══════════════════════════════════════════════════════════════════════

Check each item. If ANY fails, fix before submitting.

  □ name contains "gen15979"
  □ name does NOT contain "crossover"
  □ take_profit_pct = 9.5 OR your one authorized new value
  □ stop_loss_pct   = 1.5 OR your one authorized new value
  □ timeout_hours   = 156 OR your one authorized new value
  □ size_pct        = 25.0  ← FROZEN. Must be exactly 25.0. Not 30.
  □ max_open        = 2     ← FROZEN. Must be exactly 2. Not 3.
  □ short bollinger period = 168  ← FROZEN
  □ short macd period      = 24   ← FROZEN
  □ momentum_accelerating value = false on LONG side  ← FROZEN
  □ momentum_accelerating value = false on SHORT side ← FROZEN
  □ pairs = [BTC/USD]  ← do not change except in PATH C1
  □ fee_rate = 0.001
  □ pause_if_down_pct = 8
  □ stop_if_down_pct  = 18
  □ pause_hours       = 48
  □ New value NOT in the EXHAUSTED list
  □ Exactly ONE parameter changed from incumbent (PATH A)
     OR exactly two (PATH B1/B2/B3) or three (PATH B4)

  COUNT OF PARAMETERS CHANGED: [write the exact number here]

  If count ≠ 1 (for PATH A), STOP. Fix the YAML.

## ══════════════════════════════════════════════════════════════════════
## FAILURE DIAGNOSIS — READ THIS IF YOUR RESULT MATCHES ONE OF THESE
## ══════════════════════════════════════════════════════════════════════

Sharpe=1.2396, trades=60, win_rate=41.7%:
  ⚠️ EXHAUSTED VALUE. The parameter you tested is confirmed inferior.
  Add it to the EXHAUSTED list. DO NOT TEST IT AGAIN.
  Move to the NEXT untested value in your current PATH.
  Common causes: timeout=192, TP=11.0, SL=2.0. ALL are DEAD.
  Use timeout=216, TP=11.5, SL=2.5 instead.

Sharpe=1.2430, trades=60:
  No-op. You reproduced the incumbent exactly.
  You changed nothing, or changed a frozen param to the same value.
  Go to STEP 2 and select an untested mutation.

Sharpe=1.2429, trades=60:
  timeout=168. This is ONE STEP below incumbent. CLOSED.
  Use timeout=216 instead.

Sharpe=1.2288, trades=60:
  timeout=144. CLOSED. Use timeout=216 instead.

Sharpe≈0.38, 0.40, 0.69, 0.77 (any trade count):
  ⚠️ YOU USED THE BROKEN UI YAML (name=crossover).
  Discard entirely. Re-read STEP 0. Start over.

Sharpe≈0.57, 0.53, 0.58 (trades=56–58):
  ⚠️ YOU CHANGED A FROZEN INDICATOR PARAMETER.
  Likely: short bollinger ≠ 168, short macd ≠ 24, or momentum=true.
  Revert immediately. Re-read STEP 0.

Sharpe=1.1418, trades=57:
  ⚠️ WRONG YAML producing wrong trade count.
  The correct incumbent produces exactly 60 trades.
  Discard. Re-read STEP 0. Start from scratch.

Sharpe≈1.1611, 1.1676, 1.1864 (trades=60):
  Wrong YAML variant — you have a subtly incorrect base.
  Discard. Re-read STEP 0. Start from scratch.

Sharpe=0.0000, trades=0 [max_trades_reject]:
  ⚠️ YOU CHANGED max_open OR size_pct. BOTH ARE FROZEN.
  Set max_open=2, size_pct=25.0. Do not touch either. Ever.

Sharpe=0.0000 [gemini_error]:
  API error. Retry with the SAME mutation — do not change anything.

Any result with trades ≠ 60 (and not PATH C):
  You have the wrong base YAML or changed a frozen parameter.
  Discard. Re-read STEP 0.

Any result with Sharpe ≤ 1.2430:
  The change is rejected. The incumbent remains Gen 15979.
  Do not commit this YAML. Move to the next untested value.

## ══════════════════════════════════════════════════════════════════════
## COMPLETE DEAD CLUSTER REFERENCE
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.3154–0.4070 (55–56 trades) — wrong YAML (UI artifact)
  DEAD: Sharpe=0.4601 (56 trades) — wrong YAML variant
  DEAD: Sharpe=0.5265–0.5954 (57–58 trades) — indicator mutations
  DEAD: Sharpe=0.5279 (57 trades) — indicator mutation
  DEAD: Sharpe=0.5325 (57 trades) — wrong YAML variant
  DEAD: Sharpe=0.5745 (57 trades) — short bollinger/MACD/momentum flip
  DEAD: Sharpe=0.5761 (57 trades) — short bollinger/MACD/momentum flip
  DEAD: Sharpe=0.6911 (57 trades) — broken UI YAML (name: crossover)
  DEAD: Sharpe=0.9795 (60 trades) — wrong parameter combination
  DEAD: Sharpe≈0.7734 (59 trades) — stale UI YAML (TP=7.14, timeout=129)
  DEAD: Sharpe≈1.0182–1.0952 — various dead ends
  DEAD: Sharpe≈1.1090 (60 trades) — gen 14907, superseded
  DEAD: Sharpe≈1.1160–1.1181 (57–58 trades) — corrupt YAML
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — corrupt YAML variant
  DEAD: Sharpe≈1.1418 (57 trades) — wrong trade count (must be 60)
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1450 (57 trades) — wrong trade count
  DEAD: Sharpe≈1.1611 (60 trades) — discarded gen 17182
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1676 (60 trades) — discarded gen 17189
  DEAD: Sharpe≈1.1708 (60 trades) — gen 15998, discarded
  DEAD: Sharpe≈1.1864 (60 trades) — discarded
  DEAD: Sharpe≈1.1882 (60 trades) — TP=10.0 or 10.5, inferior
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, timeout=138
  DEAD: Sharpe=1.2287 (60 trades) — float duplicate of gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, timeout=144
  DEAD: Sharpe=1.2396 (60 trades) — ⚠️ EXHAUSTED (~10+ occurrences)
        Caused by: timeout=192, TP=11.0, SL=2.0 — ALL CONFIRMED DEAD.
        Do NOT test any of these values. Not even once more.
  DEAD: Sharpe=1.2429 (60 trades) — timeout=168, confirmed inferior
  DEAD: Sharpe=1.2430 (60 trades) — INCUMBENT (no-op if reproduced)
  DEAD: Sharpe=0.0000 (0 trades) — changed max_open or size_pct

## ══════════════════════════════════════════════════════════════════════
## CONTEXT — WHAT THIS STRATEGY IS AND WHY IT WORKS
## ══════════════════════════════════════════════════════════════════════

Swing trading on BTC/USD (1-hour candles, 2-year backtest).

Long entry: momentum NOT accelerating + price below Bollinger lower
band (48h) + MACD (48h) bullish → mean-reversion long.

Short entry: momentum NOT accelerating + price above Bollinger upper
band (168h) + MACD (24h) bearish → trend-exhaustion short.

Exit: TP=9.5%, SL=1.5%, timeout=156h.
Reward:risk = 6.3:1. Win rate = 41.7%. Sharpe = 1.2430.
Expected return per trade: (0.417 × 9.5%) − (0.583 × 1.5%) ≈ +3.1%

The indicator triplet is FROZEN AND CONFIRMED VIABLE.
Only exit parameters (TP, SL, timeout) and risk parameters are mutable
in PATH A. Entry conditions require PATH C authorization.

Live validation: rank 3/10 in last 2 sprints, positive PnL both times.
Win rates in live (50–67%) exceed backtest (41.7%) → no overfit concern.
Macro: DANGER regime (F&G=15). size_pct=25.0 is correct for this regime.

The strategy appears to have entered a DISCRETE ATTRACTOR near the
incumbent. Most exit parameter perturbations return exactly 1.2396
(same 60 trades, slightly worse P&L distribution). Escape may require
PATH B combinations or PATH C new dimensions.

##