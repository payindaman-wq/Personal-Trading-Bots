```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 17001 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-11 (v25)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CRITICAL STALL PHASE (0 improvements in 821+ gens)
# Last improvement: Gen 15979 (821+ generations ago).
# Sharpe has climbed from 0.0799 → 1.2430.
# The core indicator triplet is CONFIRMED VIABLE AND FROZEN.
#
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing (minimum 30 trades).
#
# ⚠️ v25 CRITICAL UPDATES:
#    1. NEW DEAD CLUSTER IDENTIFIED: Sharpe=1.2396, 60 trades.
#       This appeared 5 TIMES in the last 20 generations (gens 16981-17000).
#       This is now the second most common failure mode after 0.3815.
#       ROOT CAUSE: One or more of the authorized PATH mutations
#       (timeout=192, TP=11.0, SL=2.0) likely produce this result.
#       IF YOU SEE 1.2396/60 TRADES: Record the parameter you tested.
#       That parameter value is EXHAUSTED. Move to the next value.
#    2. DOMINANT FAILURE CLUSTER (0.3815, 56 trades): Appeared 6 TIMES
#       in last 20 gens. This is the most common failure mode.
#       ROOT CAUSE UNKNOWN — you have the WRONG YAML.
#       FIX: Discard entirely. Start fresh from incumbent below.
#    3. ZERO-TRADE REJECTIONS (2 times in last 20 gens): Gens 16984,
#       16998 produced 0 trades. You changed max_open or size_pct.
#       Both are FROZEN. max_open=2, size_pct=25.0. DO NOT TOUCH.
#    4. ALL THREE PRIMARY PATHS MAY BE EXHAUSTED. If timeout=192,
#       TP=11.0, and SL=2.0 all return 1.2396, escalate to PATH B
#       (combinations) or PATH C (new dimensions). See below.
#    5. PROMPT IS TOO LONG. Read the incumbent YAML first. Change
#       ONE thing. Verify. That is all.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## STEP 0: READ THE INCUMBENT YAML FIRST — EVERYTHING ELSE COMES AFTER
## ══════════════════════════════════════════════════════════════════════

THIS IS THE ONLY VALID INCUMBENT. IT IS THE ONLY YAML YOU MAY MUTATE.
DO NOT USE THE UI. THE UI IS BROKEN. THE UI SHOWS A DEAD YAML.
THE UI YAML HAS: name=crossover, size_pct=30, max_open=3, TP=7.36,
timeout=129. ALL OF THESE ARE WRONG. IGNORE THE UI ENTIRELY.

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

INCUMBENT KEY VALUES (memorize these before proceeding):
  name:            random_restart_v3_tightened_sl_v3_gen15979
  take_profit_pct: 9.5
  stop_loss_pct:   1.5
  timeout_hours:   156
  size_pct:        25.0   ← FROZEN — changing causes 0 trades
  max_open:        2      ← FROZEN — changing causes 0 trades
  short bollinger: 168    ← FROZEN — changing causes Sharpe=0.5761
  short macd:      24     ← FROZEN — changing causes Sharpe=0.5761
  momentum value:  false  ← FROZEN — flipping causes Sharpe=0.5761
  pairs:           [BTC/USD]
  Sharpe:          1.2430 | Trades: 60 | Win rate: 41.7%

## ══════════════════════════════════════════════════════════════════════
## STEP 1: COMPLETE THE PRE-MUTATION CHECKLIST
## ══════════════════════════════════════════════════════════════════════

Write out ALL of the following before proposing any YAML:

  INCUMBENT NAME: [must contain "gen15979"]
  INCUMBENT TP: [must be 9.5]
  INCUMBENT TIMEOUT: [must be 156]
  INCUMBENT SL: [must be 1.5]
  INCUMBENT SIZE: [must be 25.0]
  INCUMBENT MAX_OPEN: [must be 2]
  INCUMBENT SHORT BOLLINGER: [must be 168]
  INCUMBENT SHORT MACD: [must be 24]

If ANY of these values does not match, STOP. You have the wrong YAML.
Discard it. Re-read the CURRENT INCUMBENT block above. Start over.

## ══════════════════════════════════════════════════════════════════════
## STEP 2: SELECT YOUR MUTATION — ONE CHANGE ONLY
## ══════════════════════════════════════════════════════════════════════

Write this out before writing the YAML:
  CHANGING: [parameter] from [old value] to [new value]
  Example: CHANGING: timeout_hours from 156 to 192
  Example: CHANGING: take_profit_pct from 9.5 to 11.0
  Example: CHANGING: stop_loss_pct from 1.5 to 2.0

The new value MUST NOT be in the TESTED VALUES lists below.
The new value MUST NOT be the same as the incumbent value.

## ══════════════════════════════════════════════════════════════════════
## AUTHORIZED MUTATIONS — CURRENT PRIORITY ORDER
## ══════════════════════════════════════════════════════════════════════

### PATH A1 — TIMEOUT (primary):
  NEXT VALUE: 192  ← TEST THIS FIRST THIS SESSION
  If 192 → 1.2396: record it as tested, move to 216
  If 192 → anything else: follow failure diagnosis below

  Tested (DO NOT REPEAT):
    timeout=129 → DEAD (stale UI artifact)
    timeout=138 → Sharpe=1.2063 (gen 15062, superseded)
    timeout=144 → Sharpe=1.2288 (gen 15480, DEAD)
    timeout=156 → Sharpe=1.2430 (CURRENT INCUMBENT)
    timeout=168 → Sharpe=1.2429 (INFERIOR by 0.0001, CLOSED)

  Next untested values (in order):
    192, 216, 240, 264, 288

### PATH A2 — TAKE PROFIT:
  NEXT VALUE: 11.0  ← TEST IF A1 FAILS OR ROTATES HERE
  If 11.0 → 1.2396: record it as tested, move to 11.5
  
  Tested (DO NOT REPEAT):
    TP=7.14  → Sharpe≈0.7734 (dead)
    TP=7.38  → Sharpe=1.1311 (gen 14993, superseded)
    TP≈8.x   → Sharpe=1.1426 (gen 15042, superseded)
    TP=9.5   → Sharpe=1.2430 (CURRENT INCUMBENT)
    TP=10.0  → Sharpe≈1.1882 (WORSE — skip)
    TP=10.5  → Sharpe≈1.1882 (WORSE — skip)

  ⚠️ TP curve is NON-MONOTONE. 10.0 and 10.5 are WORSE than 9.5.
  Next untested values (in order):
    11.0, 11.5, 12.0, 13.0, 14.0, 15.0

### PATH A3 — STOP LOSS:
  NEXT VALUE: 2.0  ← TEST IF A1 AND A2 FAIL OR ROTATE HERE
  If 2.0 → 1.2396: record it as tested, move to 2.5
  ⚠️ SL relaxation may change trade count. Reject if trades > 60 or < 30.

  Tested (DO NOT REPEAT):
    SL=1.5 → CURRENT INCUMBENT

  Next untested values (in order):
    2.0, 2.5, 3.0

  Name: random_restart_v3_tightened_sl_v3_gen15979_sl20

### PATH B — COMBINATIONS (escalate here if A1+A2+A3 all return 1.2396):
  If ALL of timeout=192, TP=11.0, SL=2.0 produce Sharpe=1.2396:
  The strategy may be at a local maximum that requires simultaneous
  changes to escape. Try:
    B1: timeout=192 + TP=11.0 (two changes simultaneously)
    B2: timeout=192 + SL=2.0
    B3: TP=11.0 + SL=2.0
  These are ONLY authorized if all single-parameter paths are exhausted.

### PATH C — NEW DIMENSIONS (escalate here if PATH B also fails):
  C1: Add ETH/USD to pairs (pairs: [BTC/USD, ETH/USD])
      ⚠️ This will change trade count significantly. Monitor carefully.
  C2: Modify pause_if_down_pct (test 10 or 12 instead of 8)
  C3: Modify stop_if_down_pct (test 20 or 22 instead of 18)
  C4: Modify pause_hours (test 24 or 72 instead of 48)
  These are only authorized if PATH B is exhausted.

### ROTATION RULE:
  Do not repeat the same PATH twice in a row.
  Rotate: A1 → A2 → A3 → A1 → A2 → A3 (or escalate to B/C if needed).

## ══════════════════════════════════════════════════════════════════════
## STEP 3: WRITE THE MUTATED YAML
## ══════════════════════════════════════════════════════════════════════

Copy the CURRENT INCUMBENT block above exactly.
Change ONLY the ONE parameter you identified in STEP 2.
Every other value must be identical to the incumbent.

Name the strategy:
  random_restart_v3_tightened_sl_v3_gen15979_[descriptor]
  Examples:
    random_restart_v3_tightened_sl_v3_gen15979_timeout192
    random_restart_v3_tightened_sl_v3_gen15979_tp11
    random_restart_v3_tightened_sl_v3_gen15979_sl20

## ══════════════════════════════════════════════════════════════════════
## STEP 4: VERIFY YOUR YAML BEFORE SUBMITTING
## ══════════════════════════════════════════════════════════════════════

After writing the YAML, verify ALL of the following:
  □ name contains "gen15979"
  □ take_profit_pct = [9.5 OR your authorized new value]
  □ timeout_hours = [156 OR your authorized new value]
  □ stop_loss_pct = [1.5 OR your authorized new value]
  □ size_pct = 25.0          (FROZEN — must be exactly this)
  □ max_open = 2             (FROZEN — must be exactly this)
  □ short bollinger = 168    (FROZEN — must be exactly this)
  □ short macd = 24          (FROZEN — must be exactly this)
  □ momentum value = false   (FROZEN — on BOTH long and short sides)
  □ pairs = [BTC/USD]        (do not add other pairs yet)
  □ fee_rate = 0.001         (do not change)
  □ pause_if_down_pct = 8    (do not change)
  □ stop_if_down_pct = 18    (do not change)
  □ pause_hours = 48         (do not change)
  □ Exactly ONE parameter changed from incumbent
  □ The changed value is NOT in the tested lists above

Count of parameters changed from incumbent: [must be exactly 1]

If any check fails, STOP. Fix the YAML before submitting.

## ══════════════════════════════════════════════════════════════════════
## FAILURE DIAGNOSIS — IF YOUR BACKTEST PRODUCES THESE RESULTS
## ══════════════════════════════════════════════════════════════════════

Sharpe=1.2396, trades=60:
  ⚠️ NEW DOMINANT NEAR-MISS (5 times in last 20 gens).
  The parameter value you tested is INFERIOR to incumbent.
  HOW TO FIX: Record which parameter you tested as EXHAUSTED.
  Move to the next value in the same PATH.
  DO NOT re-test the same value again.

Sharpe=0.3815, trades=56:
  ⚠️ DOMINANT FAILURE (6 times in last 20 gens). Wrong YAML entirely.
  HOW TO FIX: Discard your ENTIRE YAML. Start completely fresh from
  the CURRENT INCUMBENT block above. Copy it character-for-character.
  Change only ONE parameter. Verify all values match the checklist.

Sharpe=0.0000, trades=0 (max_trades_reject):
  You changed max_open OR size_pct. Both are FROZEN.
  HOW TO FIX: Set max_open=2, size_pct=25.0. Do not touch either.

Sharpe=0.5761, trades=57:
  You changed short bollinger (must be 168), short MACD (must be 24),
  OR flipped momentum_accelerating to true.
  HOW TO FIX: Revert ALL indicator changes immediately.

Sharpe=1.2430, trades=60:
  Your mutation was a no-op. You reproduced the incumbent exactly.
  HOW TO FIX: Verify you changed exactly ONE parameter to a NEW,
  untested value. Check the tested lists. Choose a new value.

Sharpe=1.2429, trades=60:
  You tested timeout=168 (confirmed inferior). This is CLOSED.
  HOW TO FIX: Use timeout=192 instead.

Sharpe=1.2288, trades=60:
  Your timeout was 144. You used the DEAD gen 15480 YAML.
  HOW TO FIX: Start from gen15979 incumbent. timeout must be 156.

Sharpe=1.1450, trades=57:
  Wrong YAML producing 57 trades. Incumbent has 60 trades.
  HOW TO FIX: Discard entirely. Re-read incumbent YAML above.

Sharpe=0.3154, trades=56:
  Wrong YAML. HOW TO FIX: Discard entirely. Re-read incumbent.

Sharpe=0.5279, trades=57:
  Wrong YAML. HOW TO FIX: Discard entirely. Re-read incumbent.

Any other result not listed above:
  Check that you changed ONLY ONE parameter from the incumbent.
  Check that max_open=2 and size_pct=25.0 are present.
  If still wrong, discard and start fresh from incumbent block.

## ══════════════════════════════════════════════════════════════════════
## COMPLETE DEAD CLUSTER REFERENCE
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.3815 (56 trades) — ⚠️ DOMINANT FAILURE (6/last 20 gens)
  DEAD: Sharpe=0.3825 (56 trades) — prior dominant failure cluster
  DEAD: Sharpe=0.3154 (56 trades) — wrong YAML cluster
  DEAD: Sharpe=0.5279 (57 trades) — indicator mutation
  DEAD: Sharpe=0.5761 (57 trades) — short bollinger/MACD/momentum flip
  DEAD: Sharpe=0.5954 (58 trades) — wrong YAML variant
  DEAD: Sharpe=0.6911 (57 trades) — broken UI YAML (name: crossover)
  DEAD: Sharpe≈0.7734 (59 trades) — stale UI YAML (TP=7.14, timeout=129)
  DEAD: Sharpe≈1.0182/1.0325/1.0642/1.0952/1.1090 — dead ends
  DEAD: Sharpe≈1.1160/1.1161 (57 trades) — corrupt YAML
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — corrupt YAML variant
  DEAD: Sharpe≈1.1418 (57 trades) — wrong YAML (appeared 2/last 20)
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1450 (57 trades) — wrong YAML (57 trades, not 60)
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1708 (60 trades) — gen 15998, discarded
  DEAD: Sharpe≈1.1864 (60 trades) — appeared 1/last 20, discarded
  DEAD: Sharpe≈1.1882 (60 trades) — TP=10.0 or 10.5, inferior
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded
  DEAD: Sharpe=1.2287 (60 trades) — float duplicate of gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, timeout=144 DEAD
  DEAD: Sharpe=1.2396 (60 trades) — ⚠️ NEW NEAR-MISS (5/last 20 gens)
        Likely produced by timeout=192, TP=11.0, or SL=2.0.
        If you see this: record what you tested, move to next value.
  DEAD: Sharpe=1.2429 (60 trades) — timeout=168, CONFIRMED INFERIOR
  DEAD: Sharpe=1.2430 (60 trades) — CURRENT INCUMBENT (no-op if reproduced)
  DEAD: Sharpe=0.0000 (0 trades) — changed max_open or size_pct

## ══════════════════════════════════════════════════════════════════════
## CONTEXT — WHAT THIS STRATEGY IS AND WHY IT WORKS
## ══════════════════════════════════════════════════════════════════════

This is a swing trading strategy on BTC/USD (1-hour candles, 2-year
backtest). It enters long when momentum is NOT accelerating, price is
below the Bollinger lower band (48h), and MACD (48h) is bullish —
a mean-reversion long signal. It enters short when momentum is NOT
accelerating, price is above the Bollinger upper band (168h), and
MACD (24h) is bearish — a trend-exhaustion short signal.

Exit logic: TP=9.5%, SL=1.5%, timeout=156h (6.5 days).
The reward:risk ratio is ~6.3:1. Win rate 41.7% with Sharpe=1.2430.
This is a positive expectancy system: (0.417 × 9.5%) − (0.583 × 1.5%)
≈ 3.96% − 0.87% ≈ +3.08% expected return per trade before fees.

The strategy is optimized for exit parameters only. The indicator
triplet is frozen and confirmed viable. Do not touch indicators.

Live performance confirms viability: rank 3/10 in both recent sprints,
positive PnL in both. The backtest Sharpe appears to translate to
live edge, validating the optimization direction.

## ══════════════════════════════════════════════════════════════════════
## IF NO VALID MUTATION IS AVAILABLE
## ══════════════════════════════════════════════════════════════════════

If all values in PATH A1, A2, A3 have been tested (i.e., timeout=192,
216, 240, 264, 288 all tested; TP=11.0, 11.5, 12.0, 13.0, 14.0, 15.0
all tested; SL=2.0, 2.5, 3.0 all tested), then:

1. Escalate to PATH B (combinations — two simultaneous changes).
2. If PATH B exhausted, escalate to PATH C (new dimensions).
3. If PATH C exhausted, write "NO VALID MUTATION AVAILABLE" and
   request MIMIR review for a new research direction.

YAML must be committed to git after EVERY new_best event.
Target: STRICTLY ABOVE 1.2430. Any result ≤ 1.2430 is rejected.
```