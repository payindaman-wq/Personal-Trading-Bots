```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 17601 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-12 (v28)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CRITICAL STALL PHASE (0 improvements in 1421+ gens)
# Last improvement: Gen 15979. Sharpe climbed 0.0799 → 1.2430.
# The core indicator triplet is CONFIRMED VIABLE AND FROZEN.
#
# ⚠️ TRADE COUNT CEILING: 60 (HARD). Minimum: 30.
# ⚠️ size_pct=25.0 and max_open=2 are FROZEN. Changing either → 0 trades.
# ══════════════════════════════════════════════════════════════════════

## ██████████████████████████████████████████████████████████████████████
## █                                                                    █
## █   READ THIS FIRST. BEFORE ANYTHING ELSE. BEFORE THE YAML.        █
## █                                                                    █
## █   YOUR NEXT MUTATION IS ONE OF THESE THREE VALUES ONLY:           █
## █                                                                    █
## █     PATH A1 (gen mod 3 = 0): timeout_hours = 216                 █
## █     PATH A2 (gen mod 3 = 1): take_profit_pct = 11.5              █
## █     PATH A3 (gen mod 3 = 2): stop_loss_pct = 2.5                 █
## █                                                                    █
## █   IF YOUR YAML DOES NOT CONTAIN EXACTLY ONE OF THOSE VALUES,     █
## █   YOU HAVE THE WRONG MUTATION. STOP. RE-READ THIS BOX.           █
## █                                                                    █
## █   IF ALL THREE HAVE BEEN TESTED THIS SESSION (all → ≤1.2430),    █
## █   MOVE TO PATH B. SEE SECTION BELOW.                             █
## █                                                                    █
## ██████████████████████████████████████████████████████████████████████

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
## ██ DEAD VALUES — DO NOT USE ANY OF THESE. NOT EVEN ONCE MORE. ██
## ══════════════════════════════════════════════════════════════════════
##
## Each value below has been confirmed inferior (Sharpe ≤ 1.2430).
## Testing any of them again produces EXACTLY Sharpe=1.2396, trades=60.
## This is a waste of a generation. You will be penalized for repeating.
##
## ██ DEAD timeout_hours:      129, 138, 144, 156, 168, 192
## ██ DEAD take_profit_pct:    7.14, 7.36, 7.38, ~8.x, 9.5,
##                              10.0, 10.5, 11.0
## ██ DEAD stop_loss_pct:      1.5, 2.0
##
## ══════════════════════════════════════════════════════════════════════
## ██ LIVE VALUES — USE ONLY THESE NEXT:                            ██
## ══════════════════════════════════════════════════════════════════════
##
## ██ NEXT timeout_hours:      216  (then 240, 264, 288)
## ██ NEXT take_profit_pct:    11.5 (then 12.0, 13.0, 14.0, 15.0)
## ██ NEXT stop_loss_pct:      2.5  (then 3.0)
##
## ══════════════════════════════════════════════════════════════════════
## BEFORE WRITING YOUR YAML, WRITE THESE WORDS OUT LOUD:
##
##   "I will NOT use timeout=192. I will use timeout=216."
##   "I will NOT use TP=11.0. I will use TP=11.5."
##   "I will NOT use SL=2.0. I will use SL=2.5."
##
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
  name:              random_restart_v3_tightened_sl_v3_gen15979
  take_profit_pct:   9.5       ← NOT 7.36. NOT 11.0. EXACTLY 9.5.
  stop_loss_pct:     1.5       ← NOT 2.0. EXACTLY 1.5.
  timeout_hours:     156       ← NOT 129. NOT 192. NOT 168. EXACTLY 156.
  size_pct:          25.0      ← FROZEN. NOT 30. EXACTLY 25.0.
  max_open:          2         ← FROZEN. NOT 3. EXACTLY 2.
  short bollinger:   168       ← FROZEN
  short macd:        24        ← FROZEN
  momentum value:    false     ← FROZEN on BOTH long AND short sides
  pairs:             [BTC/USD]
  Sharpe:            1.2430 | Trades: 60 | Win rate: 41.7%

## ══════════════════════════════════════════════════════════════════════
## STEP 1: PRE-MUTATION CHECKLIST — WRITE THESE OUT BEFORE ANY YAML
## ══════════════════════════════════════════════════════════════════════

Copy and fill in exactly — do not skip this step:

  INCUMBENT NAME:            random_restart_v3_tightened_sl_v3_gen15979
  INCUMBENT TP:              9.5
  INCUMBENT TIMEOUT:         156
  INCUMBENT SL:              1.5
  INCUMBENT SIZE:            25.0
  INCUMBENT MAX_OPEN:        2
  INCUMBENT SHORT BOLLINGER: 168
  INCUMBENT SHORT MACD:      24

If ANY value you wrote does not match the above, STOP.
Re-read STEP 0 until all values match. Then continue.

Then write out the following affirmations:

  "I will NOT propose timeout=192. My timeout proposal is 216."
  "I will NOT propose TP=11.0. My TP proposal is 11.5."
  "I will NOT propose SL=2.0. My SL proposal is 2.5."

## ══════════════════════════════════════════════════════════════════════
## STEP 2: DETERMINE YOUR GENERATION NUMBER AND MUTATION
## ══════════════════════════════════════════════════════════════════════

Use the ROTATION SCHEDULE below to determine which PATH to use.
The rotation is strictly mechanical — no discretion.

  Generation mod 3 = 0 → PATH A1 (timeout)
  Generation mod 3 = 1 → PATH A2 (take_profit_pct)
  Generation mod 3 = 2 → PATH A3 (stop_loss_pct)

Within each path, always use the LOWEST UNTESTED value from that path's
list. Do not skip ahead. Do not re-test dead values.

Write out before writing any YAML:

  MY GENERATION NUMBER:  [number]
  GENERATION MOD 3:      [0, 1, or 2]
  ASSIGNED PATH:         [A1, A2, or A3]
  CHANGING:              [parameter] from [old value] to [new value]
  IS NEW VALUE IN DEAD LIST?   [yes → STOP / no → continue]
  IS NEW VALUE SAME AS INCUMBENT?  [yes → STOP / no → continue]

If either check is "yes", stop and use the next untested value.

## ══════════════════════════════════════════════════════════════════════
## AUTHORIZED MUTATION PATHS
## ══════════════════════════════════════════════════════════════════════

### PATH A1 — TIMEOUT (use when gen mod 3 = 0):

  ██ DEAD — DO NOT USE:  129, 138, 144, 156, 168, 192
  ██ USE NEXT IN ORDER:  216, then 240, then 264, then 288

  Current next value: 216
  ⚠️ If 216 has already been tested this session and returned ≤1.2430,
     use 240. If 240 also tested and failed, use 264, then 288.

  All known results:
    129 → stale UI artifact (dead)
    138 → 1.2063 (dead)
    144 → 1.2288 (dead)
    156 → 1.2430 (INCUMBENT)
    168 → 1.2429 (dead — one step below incumbent)
    192 → 1.2396 (dead — confirmed ~10+ times. DO NOT TEST AGAIN.)
    216 → UNTESTED ← USE THIS NEXT
    240 → UNTESTED
    264 → UNTESTED
    288 → UNTESTED

  Naming: random_restart_v3_tightened_sl_v3_gen15979_timeout216

### PATH A2 — TAKE PROFIT (use when gen mod 3 = 1):

  ██ DEAD — DO NOT USE:  7.14, 7.36, 7.38, ~8.x, 9.5, 10.0, 10.5, 11.0
  ██ USE NEXT IN ORDER:  11.5, then 12.0, then 13.0, then 14.0, then 15.0

  Current next value: 11.5
  ⚠️ TP=11.0 returned 1.2396. It is DEAD. Do not use it again.
  ⚠️ TP curve is NON-MONOTONE. 10.0 and 10.5 both returned ~1.1882.
  ⚠️ Higher TP reduces trade count (more trades time out before hitting TP).
     Monitor trade count. Reject if trades < 30 or > 60.

  All known results:
    7.14  → ~0.7734 (dead)
    7.36  → dead (UI artifact)
    7.38  → 1.1311 (dead)
    ~8.x  → 1.1426 (dead)
    9.5   → 1.2430 (INCUMBENT)
    10.0  → ~1.1882 (dead)
    10.5  → ~1.1882 (dead)
    11.0  → 1.2396 (dead — DO NOT TEST AGAIN)
    11.5  → UNTESTED ← USE THIS NEXT
    12.0  → UNTESTED
    13.0  → UNTESTED
    14.0  → UNTESTED
    15.0  → UNTESTED

  Naming: random_restart_v3_tightened_sl_v3_gen15979_tp115

### PATH A3 — STOP LOSS (use when gen mod 3 = 2):

  ██ DEAD — DO NOT USE:  1.5, 2.0
  ██ USE NEXT IN ORDER:  2.5, then 3.0

  Current next value: 2.5
  ⚠️ SL=2.0 returned 1.2396. It is DEAD. Do not use it again.
  ⚠️ Wider SL may increase trade duration, interacting with timeout.
  ⚠️ Monitor trade count. Reject if trades < 30 or > 60.

  All known results:
    1.5 → 1.2430 (INCUMBENT)
    2.0 → 1.2396 (dead — DO NOT TEST AGAIN)
    2.5 → UNTESTED ← USE THIS NEXT
    3.0 → UNTESTED

  Naming: random_restart_v3_tightened_sl_v3_gen15979_sl25

## ══════════════════════════════════════════════════════════════════════
## PATH B — COMBINATIONS
## ══════════════════════════════════════════════════════════════════════
##
## PATH B is authorized ONLY after ALL THREE of the following have been
## individually tested and ALL returned ≤ 1.2430:
##   - timeout=216  (PATH A1 next value)
##   - TP=11.5      (PATH A2 next value)
##   - SL=2.5       (PATH A3 next value)
##
## DO NOT jump to PATH B before those three individual tests are done.
##
## Combinations to test (in order):
##   B1: timeout=216 + TP=11.5
##       name: ...gen15979_timeout216_tp115
##   B2: timeout=216 + SL=2.5
##       name: ...gen15979_timeout216_sl25
##   B3: TP=11.5 + SL=2.5
##       name: ...gen15979_tp115_sl25
##   B4: timeout=216 + TP=11.5 + SL=2.5 (three-way — last resort)
##       name: ...gen15979_timeout216_tp115_sl25
##
## If PATH B1–B4 all return ≤ 1.2430, escalate to MIMIR before PATH C.
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## PATH C — NEW DIMENSIONS
## (Use only after PATH B is fully exhausted — escalate to MIMIR first)
## ══════════════════════════════════════════════════════════════════════
##
## C1 — ADD ETH/USD [HIGHEST PRIORITY]:
##   pairs: [BTC/USD, ETH/USD]
##   Rationale: ETH's different volatility profile changes the trade
##   sample entirely and may break the 1.2396 attractor.
##   ⚠️ Will significantly change trade count. Monitor carefully.
##   ⚠️ Do NOT change any entry/exit parameters simultaneously.
##   name: ...gen15979_ethbtc
##
## C2 — RELAX DRAWDOWN PAUSE:
##   pause_if_down_pct → 10 (current: 8)
##   Rationale: less aggressive pausing may allow more winning trades
##   during volatile regimes (DANGER macro, F&G=16).
##   name: ...gen15979_pause10
##
## C3 — RELAX DRAWDOWN STOP:
##   stop_if_down_pct → 20 (current: 18)
##   name: ...gen15979_stopdown20
##
## C4 — CHANGE PAUSE DURATION:
##   pause_hours → 24 or 72 (current: 48)
##   name: ...gen15979_pausehours24 or ...pausehours72
##
## C5 — CHANGE LONG BOLLINGER PERIOD [HIGH RISK]:
##   long bollinger period → 36 or 60 (current: 48)
##   ⚠️ HIGH RISK — indicator change may collapse Sharpe to 0.5x range.
##   ⚠️ Only test if C1–C4 are all exhausted.
##   name: ...gen15979_boll36
##
## ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## STEP 3: WRITE THE MUTATED YAML
## ══════════════════════════════════════════════════════════════════════

1. Copy the INCUMBENT YAML from STEP 0 word-for-word.
2. Change ONLY the ONE parameter identified in STEP 2.
3. Every other value must be character-for-character identical.
4. Update the name field using the naming convention for your path.

REMINDER — these values are FROZEN. Do not touch them:
  size_pct=25.0, max_open=2, fee_rate=0.001,
  short bollinger period=168, short macd period=24,
  momentum_accelerating value=false (BOTH long AND short sides),
  long bollinger period=48, long macd period=48,
  long momentum period=48, short momentum period=48,
  pause_if_down_pct=8, stop_if_down_pct=18, pause_hours=48,
  pairs=[BTC/USD]

Only these values are mutable in PATH A:
  take_profit_pct, stop_loss_pct, timeout_hours

## ══════════════════════════════════════════════════════════════════════
## STEP 4: VERIFY BEFORE SUBMITTING
## ══════════════════════════════════════════════════════════════════════

Check each item. If ANY fails, fix before submitting.

  □ name contains "gen15979"
  □ name does NOT contain "crossover"
  □ take_profit_pct  = 9.5 OR your one authorized new value
  □ stop_loss_pct    = 1.5 OR your one authorized new value
  □ timeout_hours    = 156 OR your one authorized new value
  □ size_pct         = 25.0  ← FROZEN. Must be exactly 25.0. Not 30.
  □ max_open         = 2     ← FROZEN. Must be exactly 2. Not 3.
  □ short bollinger period = 168  ← FROZEN
  □ short macd period      = 24   ← FROZEN
  □ momentum_accelerating value = false on LONG side  ← FROZEN
  □ momentum_accelerating value = false on SHORT side ← FROZEN
  □ pairs = [BTC/USD]  ← do not change except in PATH C1
  □ fee_rate = 0.001
  □ pause_if_down_pct = 8
  □ stop_if_down_pct  = 18
  □ pause_hours       = 48
  □ New value NOT in the DEAD list
  □ New value NOT the same as incumbent value
  □ Exactly ONE parameter changed from incumbent (PATH A)
     OR exactly two (PATH B1/B2/B3) OR three (PATH B4)

  COUNT OF PARAMETERS CHANGED FROM INCUMBENT: [write exact number here]

  If count ≠ 1 (for PATH A), STOP. Fix the YAML before submitting.

## ══════════════════════════════════════════════════════════════════════
## FAILURE DIAGNOSIS — READ THIS IF YOUR RESULT MATCHES ONE OF THESE
## ══════════════════════════════════════════════════════════════════════

Sharpe=1.2396, trades=60, win_rate=41.7%:
  ██ YOU USED A DEAD VALUE.
  The parameter you tested is confirmed inferior. Do not test it again.
  The three most common causes: timeout=192, TP=11.0, SL=2.0.
  ALL THREE ARE DEAD. Use timeout=216, TP=11.5, SL=2.5 instead.
  Add the dead value to the exhausted list. Move to next untested value.

Sharpe=1.2430, trades=60:
  No-op. You reproduced the incumbent exactly.
  You changed nothing, or changed a frozen param to its current value.
  Go to STEP 2 and select an untested mutation.

Sharpe=1.2429, trades=60:
  timeout=168. This is ONE STEP below incumbent. DEAD.
  Use timeout=216 instead.

Sharpe=1.2288, trades=60:
  timeout=144. DEAD. Use timeout=216 instead.

Sharpe≈0.38–0.77 (any trade count):
  ██ YOU USED THE BROKEN UI YAML (name=crossover).
  Discard entirely. Re-read STEP 0. Start over.

Sharpe≈0.57, 0.53, 0.58 (trades=56–58):
  ██ YOU CHANGED A FROZEN INDICATOR PARAMETER.
  Likely: short bollinger ≠ 168, short macd ≠ 24, or momentum=true.
  Revert immediately. Re-read STEP 0.

Sharpe=1.1418, trades=57:
  ██ WRONG YAML. The correct incumbent produces exactly 60 trades.
  Discard. Re-read STEP 0. Start from scratch.

Sharpe≈1.1611, 1.1676, 1.1864 (trades=60):
  Wrong YAML variant — subtly incorrect base.
  Discard. Re-read STEP 0. Start from scratch.

Sharpe=0.0000, trades=0 [max_trades_reject]:
  ██ YOU CHANGED max_open OR size_pct. BOTH ARE FROZEN.
  Set max_open=2, size_pct=25.0. Do not touch either. Ever.

Sharpe=0.0000 [gemini_error]:
  API error. Retry with the SAME mutation — do not change anything.

Any result with trades ≠ 60 (and not PATH C):
  Wrong base YAML or frozen parameter changed.
  Discard. Re-read STEP 0.

Any result with Sharpe ≤ 1.2430:
  Change is rejected. Incumbent remains Gen 15979.
  Do not commit this YAML. Move to next untested value.

## ══════════════════════════════════════════════════════════════════════
## COMPLETE DEAD CLUSTER REFERENCE
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.3154–0.4070 (55–56 trades) — wrong YAML (UI artifact)
  DEAD: Sharpe=0.4601 (56 trades) — wrong YAML variant
  DEAD: Sharpe=0.5265–0.5954 (57–58 trades) — indicator mutations
  DEAD: Sharpe=0.5279 (57 trades) — indicator mutation
  DEAD: Sharpe=0.5325 (57 trades) — wrong YAML variant
  DEAD: Sharpe=0.5700 (57 trades) — short bollinger/MACD/momentum flip
  DEAD: Sharpe=0.5745 (57 trades) — short bollinger/MACD/momentum flip
  DEAD: Sharpe=0.5761 (57 trades) — short bollinger/MACD/momentum flip
  DEAD: Sharpe=0.6911 (57 trades) — broken UI YAML (name: crossover)
  DEAD: Sharpe=0.9795 (60 trades) — wrong parameter combination
  DEAD: Sharpe≈0.7734 (59 trades) — stale UI YAML (TP=7.14, timeout=129)
  DEAD: Sharpe≈1.0182–1.0952 — various dead ends
  DEAD: Sharpe≈1.1090 (60 trades) — gen 14907, superseded
  DEAD: Sharpe≈1.1160–1.1181 (57–58 trades) — corrupt YAML
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362