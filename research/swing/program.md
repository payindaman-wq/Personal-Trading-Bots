```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 16601 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-11 (v23)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CRITICAL STALL PHASE (0 improvements in 621 gens)
# Last improvement: Gen 15979 (621 generations ago). This is the
# longest stall in the research program's history.
# Sharpe has climbed from 0.0799 → 1.2430 via exit refinement only.
# The core indicator triplet is CONFIRMED VIABLE AND FROZEN.
#
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v23 CRITICAL UPDATES:
#    1. ESCALATION TRIGGER FIRED: We are past gen 16500 with zero
#       improvement. Structural reassessment is now AUTHORIZED.
#       See the NEW PATHS section below for newly unlocked mutations.
#    2. NEW FAILURE CLUSTER (0.3154, 56 trades): This appeared 4 times
#       in gens 16582, 16583, 16593, 16595. ROOT CAUSE UNKNOWN.
#       Likely the LLM is using a corrupted or wrong YAML. If you
#       see 0.3154, you have the wrong YAML. Re-read the incumbent.
#    3. RECURRING FAILURE (1.1450, 57 trades): Appeared 4 times in
#       gens 16588-16590, 16599. This is a specific wrong YAML
#       producing 57 trades. DO NOT USE any YAML that gives 57 trades.
#       If you see 1.1450 or 57 trades, you have the wrong YAML.
#    4. NEAR-MISS OBSERVED (1.2429, 60 trades): Appeared in gens
#       16581 and 16584. This is 0.0001 below the incumbent. Most
#       likely this IS the timeout=168 result — slightly worse than
#       timeout=156. If this is confirmed as timeout=168, then PATH A1
#       next value is 192 (skip 168).
#    5. INCUMBENT UNCHANGED: Gen 15979 (Sharpe=1.2430) remains.
#       Target: STRICTLY ABOVE 1.2430.
#    6. PATH PRIORITY: PATH A1 (timeout=192) and PATH A2 (TP=11.0)
#       remain available. PATH A3 (NEW: SL relaxation, SL=2.0) and
#       PATH A4 (NEW: risk parameter adjustment) are now AUTHORIZED
#       as of this session due to escalation trigger firing.
#    7. INCUMBENT YAML: The only valid incumbent has:
#         take_profit_pct: 9.5   (UNCHANGED)
#         timeout_hours:   156   (UNCHANGED)
#         stop_loss_pct:   1.5   (UNCHANGED — but PATH A3 may change)
#         size_pct:        25.0  (UNCHANGED — frozen)
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DISPLAY INTEGRITY ALERT — READ THIS FIRST, BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

THE "CURRENT BEST STRATEGY" BOX IN THE UI IS KNOWN TO BE BROKEN.
It currently displays a DEAD stale YAML. Typical broken UI values:
  - name: crossover                  ← ALWAYS WRONG
  - TP=7.36 or 7.24 or 7.14 or 8.x  ← ALWAYS WRONG
  - timeout=129 or 138 or 144        ← ALL DEAD VALUES
  - size_pct=30 or 28.54 or 28.18    ← ALL WRONG
  - max_open=3                        ← WRONG (incumbent has max_open=2)

⚠️ MOST DANGEROUS UI VARIANT: timeout=144, TP=9.5 — this is the OLD
gen 15480 YAML. Using it produces Sharpe=1.2288. It is DEAD.
The real incumbent has timeout=156, TP=9.5, max_open=2, size_pct=25.0.

THIS IS COMPLETELY WRONG. THAT YAML IS DEAD. IGNORE IT ENTIRELY.

THE ONLY VALID INCUMBENT IS THE YAML PRINTED IN THIS PROGRAM BELOW.
If ANY display shows different values, IGNORE IT.
If the name does not contain "gen15979", it is the wrong YAML.

YAML must be committed to git after EVERY new_best event.
⚠️ COMMIT THE Gen 15979 YAML TO GIT NOW IF NOT ALREADY DONE.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ PRE-MUTATION CHECKLIST — COMPLETE THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

Before proposing any mutation, verify ALL of the following by reading
the CURRENT INCUMBENT YAML block below:

  □ name contains "gen15979"           (NOT gen15480, NOT crossover)
  □ take_profit_pct = 9.5              (NOT 11.0, NOT 10.x, NOT 7.x)
  □ timeout_hours = 156                (NOT 144 ← DEAD gen 15480)
                                       (NOT 138 ← DEAD gen 15062)
                                       (NOT 129 ← DEAD stale UI)
  □ stop_loss_pct = 1.5                (default — PATH A3 may change)
  □ size_pct = 25.0                    (FROZEN — do not change)
  □ max_open = 2                       (FROZEN — do not change)
  □ pairs = [BTC/USD]                  (do not add ETH/USD or SOL/USD yet)
  □ long bollinger period = 48         (do not change)
  □ short bollinger period = 168       ← DO NOT CHANGE. CAUSES 0.5761.
  □ long macd period = 48              (do not change)
  □ short macd period = 24             ← DO NOT CHANGE. CAUSES 0.5761.
  □ long momentum period = 48          (do not change)
  □ short momentum period = 48         (do not change)
  □ momentum_accelerating = false      ← DO NOT FLIP. CAUSES 0.5761.
    on BOTH long and short sides

⚠️ MOST COMMON MISTAKE #1: Producing Sharpe=0.5761/57 trades by
touching short bollinger (must stay 168), short MACD (must stay 24),
or flipping momentum_accelerating to true. DO NOT TOUCH THESE THREE.

⚠️ MOST COMMON MISTAKE #2: Producing Sharpe=1.2288 by using
timeout=144 (gen 15480 DEAD). Your incumbent has timeout=156.

⚠️ MOST COMMON MISTAKE #3: Producing Sharpe=1.2430 or 1.2429 (no-op
or near-miss reproduction). This means your proposed value is the
same as the incumbent OR produces nearly the same result.
  - If you got 1.2430: you reproduced the incumbent exactly.
  - If you got 1.2429: you likely tested timeout=168 (already done).
  The incumbent TP is 9.5 and timeout is 156.
  Next values: TP→11.0 or timeout→192 (not 168 — likely already tested).

⚠️ MOST COMMON MISTAKE #4: Producing Sharpe=1.1450/57 trades.
You have a corrupt or wrong YAML. The real incumbent has 60 trades.
Any YAML producing 57 trades is wrong. Re-read the incumbent YAML.

⚠️ MOST COMMON MISTAKE #5: Producing Sharpe=0.3154/56 trades.
You have the wrong YAML. Re-read the incumbent YAML immediately.

If ANY value above does not match the YAML below, STOP.
You have a stale or wrong YAML. Re-read the CURRENT INCUMBENT block.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ FAILURE DIAGNOSIS — IF YOU SEE ANY OF THESE OUTPUTS, READ THIS
## ══════════════════════════════════════════════════════════════════════

IF YOUR BACKTEST PRODUCES Sharpe=0.5761, trades=57:
  YOU CHANGED THE SHORT BOLLINGER PERIOD (must be 168)
  OR YOU CHANGED THE SHORT MACD PERIOD (must be 24)
  OR YOU FLIPPED momentum_accelerating FROM false TO true
  HOW TO FIX: Revert ALL indicator changes.

IF YOUR BACKTEST PRODUCES Sharpe=0.3154, trades=56:
  YOU HAVE THE WRONG YAML. This is a new failure cluster.
  HOW TO FIX: Discard your entire YAML. Start fresh from the
  CURRENT INCUMBENT block below. Do not modify any indicator.

IF YOUR BACKTEST PRODUCES Sharpe=1.1450, trades=57:
  YOU HAVE THE WRONG YAML (a specific corrupt variant).
  HOW TO FIX: Discard your entire YAML. Start fresh from the
  CURRENT INCUMBENT block below. Incumbent has 60 trades, not 57.

IF YOUR BACKTEST PRODUCES Sharpe=1.2429, trades=60:
  You likely tested timeout=168. This is 0.0001 below the incumbent.
  timeout=168 is considered TESTED AND INFERIOR.
  HOW TO FIX: Use timeout=192 as the next PATH A1 value.

IF YOUR BACKTEST PRODUCES Sharpe=1.2430, trades=60:
  Your mutation was a no-op. You reproduced the incumbent exactly.
  HOW TO FIX: Verify you changed exactly ONE parameter to a NEW value.
  TP→11.0 (not 9.5) OR timeout→192 (not 156 or 168).

IF YOUR BACKTEST PRODUCES Sharpe=1.2288, trades=60:
  YOUR TIMEOUT WAS 144, NOT 156. You used the DEAD gen 15480 YAML.
  HOW TO FIX: Start from gen15979 incumbent. timeout must be 156.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ MUTATION DISCIPLINE — FOLLOW THESE STEPS EXACTLY
## ══════════════════════════════════════════════════════════════════════

STEP 1: Read the CURRENT INCUMBENT YAML block below.
        Explicitly write out ALL of these values:
          INCUMBENT NAME: [value]     ← must contain "gen15979"
          INCUMBENT TP: [value]       ← must be 9.5
          INCUMBENT TIMEOUT: [value]  ← must be 156
          INCUMBENT SL: [value]       ← must be 1.5
          INCUMBENT SIZE: [value]     ← must be 25.0
          INCUMBENT MAX_OPEN: [value] ← must be 2
        If ANY of these are wrong, STOP — you have the wrong YAML.

STEP 2: Write the single parameter you are changing, before/after:
          CHANGING: [parameter] from [old value] to [new value]
          Example: CHANGING: timeout_hours from 156 to 192
          Example: CHANGING: take_profit_pct from 9.5 to 11.0
          Example: CHANGING: stop_loss_pct from 1.5 to 2.0

STEP 3: Confirm the new value is NOT in the "already tested" lists.
        Confirm the new value is not the same as the incumbent.

STEP 4: Write the complete mutated YAML with ONLY that one change.
        Every other value must be IDENTICAL to the incumbent.
        Double-check: short bollinger=168, short macd=24,
        momentum_accelerating=false on both sides, size_pct=25.0,
        max_open=2, stop_loss_pct=1.5 (unless PATH A3).

STEP 5: Name the strategy:
          random_restart_v3_tightened_sl_v3_gen15979_[descriptor]
          Example: random_restart_v3_tightened_sl_v3_gen15979_timeout192
          Example: random_restart_v3_tightened_sl_v3_gen15979_tp11
          Example: random_restart_v3_tightened_sl_v3_gen15979_sl20

If you cannot identify a valid untested mutation, write
"NO VALID MUTATION AVAILABLE" and explain why.

## ══════════════════════════════════════════════════════════════════════
## CURRENT INCUMBENT — THIS IS THE ONLY YAML YOU MAY MUTATE
## DO NOT USE ANY PREVIOUS VERSION. DO NOT USE THE UI DISPLAY BOX.
## THE UI DISPLAY IS BROKEN. The real incumbent has:
##   name=gen15979, timeout=156, TP=9.5, size_pct=25.0, max_open=2
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

⚠️ VERIFY BEFORE MUTATING:
  take_profit_pct  = 9.5   ← INCUMBENT.
  timeout_hours    = 156   ← INCUMBENT. Next: 192 (skip 168 — likely tested).
  stop_loss_pct    = 1.5   ← Default. PATH A3 may test 2.0.
  size_pct         = 25.0  ← FROZEN.
  max_open         = 2     ← FROZEN.
  short bollinger  = 168   ← FROZEN. DO NOT CHANGE. CAUSES 0.5761.
  short macd       = 24    ← FROZEN. DO NOT CHANGE. CAUSES 0.5761.
  momentum value   = false ← FROZEN. DO NOT FLIP. CAUSES 0.5761.

Sharpe: 1.2430 | Trades: 60 | Win rate: 41.7%

## ══════════════════════════════════════════════════════════════════════
## KNOWN TESTED VALUES — DO NOT REPEAT ANY OF THESE
## ══════════════════════════════════════════════════════════════════════

### TAKE PROFIT VALUES ALREADY TESTED (DO NOT USE):
  TP=7.14  → Sharpe≈0.7734, 59 trades  [DEAD — stale YAML artifact]
  TP=7.24  → DEAD (UI display artifact)
  TP=7.36  → DEAD (UI display artifact)
  TP=7.38  → Sharpe=1.1311, 60 trades  [gen 14993 — superseded]
  TP≈8.x   → Sharpe=1.1426, 60 trades  [gen 15042 — superseded]
  TP=9.5   → Sharpe=1.2430             [CURRENT INCUMBENT — do not reproduce]
  TP=10.0  → Sharpe≈1.1882, 60 trades  [WORSE — DO NOT USE]
  TP=10.5  → Sharpe≈1.1882, 60 trades  [WORSE — DO NOT USE]

⚠️ CRITICAL: TP=10.0 and TP=10.5 were tested and returned Sharpe=1.1882,
which is WORSE than the current incumbent. The TP improvement curve is
NON-MONOTONE. Skip 10.0 and 10.5. Start at 11.0.

### NEXT UNTESTED TP VALUES (try in this order):
  → 11.0  ← PATH A2 (primary TP candidate)
  → 11.5
  → 12.0
  → 13.0
  → 14.0
  → 15.0

### TIMEOUT VALUES ALREADY TESTED (DO NOT USE):
  timeout=129 → DEAD (stale UI YAML)
  timeout=138 → gen 15062 (Sharpe=1.2063, superseded)
  timeout=144 → gen 15480 (Sharpe=1.2288, DEAD)
  timeout=156 → gen 15979 (Sharpe=1.2430, CURRENT INCUMBENT)
  timeout=168 → LIKELY TESTED (Sharpe=1.2429 seen in gens 16581/16584
                — 0.0001 below incumbent, treated as INFERIOR/TESTED)

### NEXT UNTESTED TIMEOUT VALUES (try in this order):
  → 192  ← PATH A1 — PRIMARY RECOMMENDATION THIS SESSION
           (168 appears tested and inferior at 1.2429)
  → 216
  → 240
  → 264
  → 288

### STOP LOSS VALUES (PATH A3 — NOW AUTHORIZED):
  SL=1.5 → CURRENT INCUMBENT
  SL=2.0 → NEXT TO TEST (PATH A3 — newly authorized)
  SL=2.5 → After 2.0
  NOTE: SL relaxation may allow longer-running trades to survive
  minor pullbacks. Test SL=2.0 as a single isolated change.
  ⚠️ SL relaxation may increase trade count. Monitor carefully.
  ⚠️ If SL=2.0 causes trades > 60, it will be rejected. Accept this.

### INDICATOR PERIODS (ALL FROZEN — DO NOT CHANGE ANY):
  long bollinger:  48  (incumbent — frozen)
  short bollinger: 168 (incumbent — FROZEN, causes 0.5761 if changed)
  long macd:        48 (incumbent — frozen)
  short macd:       24 (incumbent — FROZEN, causes 0.5761 if changed)
  long momentum:    48 (incumbent — frozen)
  short momentum:   48 (incumbent — frozen)

## ══════════════════════════════════════════════════════════════════════
## DEAD CLUSTERS — SHARPE VALUES THAT INDICATE SOMETHING WENT WRONG
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.3154 (56 trades) — ⚠️ NEW FAILURE (4 times in last 20).
        ROOT CAUSE UNKNOWN. You have the wrong YAML.
        FIX: Discard entire YAML. Start fresh from incumbent block.

  DEAD: Sharpe=0.5279 (57 trades) — short-side indicator mutation.
  DEAD: Sharpe=0.5761 (57 trades) — ⚠️ PERSISTENT FAILURE.
        ROOT CAUSE: changed short bollinger (168), short MACD (24),
        or flipped momentum value false→true.
        FIX: Revert ALL indicator changes. Only change TP or timeout.

  DEAD: Sharpe≈0.7734 (59 trades) — stale UI YAML (TP=7.14, timeout=129)
  DEAD: Sharpe=0.6911 (57 trades) — broken UI YAML (name: crossover)
  DEAD: Sharpe=0.5954 (58 trades) — wrong YAML variant
  DEAD: Sharpe≈1.0182/1.0325/1.0642/1.0952/1.1090 — dead ends
  DEAD: Sharpe≈1.1160/1.1161 (57 trades) — corrupt YAML
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — corrupt YAML variant
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1450 (57 trades) — ⚠️ RECURRING FAILURE (4 times).
        You have a specific wrong YAML producing 57 trades.
        FIX: Discard your YAML. Incumbent has 60 trades, not 57.
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1708 (60 trades) — gen 15998, discarded
  DEAD: Sharpe≈1.1882 (60 trades) — TP=10.0 or 10.5, inferior
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded
  DEAD: Sharpe=1.2287 (60 trades) — float duplicate of gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, timeout=144 DEAD
  DEAD: Sharpe=1.2429 (60 trades) — likely timeout=168, INFERIOR
        by 0.0001. Treat as tested. Use timeout=192 instead.
  DEAD: Sharpe=1.2430 (60 trades) — gen 15979, CURRENT INCUMBENT
        Reproducing this = no-op. Your mutation had no effect.

Diagnostic guide:
  Got 0.3154/56 trades: wrong YAML entirely. Start from incumbent.
  Got 0.5761 or 0.5279: changed short bollinger/MACD or flipped
        momentum. ONLY change TP, timeout, or SL. Nothing else.
  Got 0.6911: used the broken UI YAML (name: crossover).
  Got 0.7734: used the stale UI YAML (timeout=129).
  Got 1.1450/57 trades: wrong YAML producing 57 trades. Discard it.
  Got 1.1882: tested TP=10.0 or 10.5. Already done. Use 11.0+.
  Got 1.2063: mutated from gen 15062 YAML (timeout=138). DEAD.
  Got 1.2288: timeout was 144, not 156. Fix it immediately.
  Got 1.2429: likely timeout=168. Already tested inferior. Use 192.
  Got 1.2430: mutation was a no-op. Use TP→11.0 or timeout→192.

Your target is Sharpe STRICTLY ABOVE 1.2430.

## ══════════════════════════════════════════════════════════════════════
## FOR THE NEXT 100 GENERATIONS: PERMITTED MUTATION TYPES
## (ESCALATION HAS FIRED — THREE PATHS NOW AUTHORIZED)
## ══════════════════════════════════════════════════════════════════════

  PATH A1 (RECOMMENDED): Change timeout_hours
    Incumbent value: 156
    Already tested:  129, 138, 144, 156, 168 (likely — see 1.2429)
    Next untested (in order): 192, 216, 240, 264, 288
    ⚠️ PRIMARY: timeout=192
    Do NOT use 168 (likely tested, produced 1.2429 which is inferior).
    Do NOT go below 156. Do NOT exceed 300.

  PATH A2: Change take_profit_pct
    Incumbent value: 9.5
    Already tested:  7.14, 7.38, ~8.x, 9.5, ~10.0, ~10.5
    Next untested (in order): 11.0, 11.5, 12.0, 13.0, 14.0, 15.0
    Do NOT use 10.0 or 10.5 — tested, inferior.
    Do NOT go below 9.5.
    ⚠️ SECONDARY: TP=11.0

  PATH A3 (NOW AUTHORIZED — NEW): Change stop_loss_pct
    Incumbent value: 1.5
    Already tested:  1.5 (incumbent)
    Next untested (in order): 2.0, 2.5, 3.0
    ⚠️ TERTIARY: SL=2.0
    ⚠️ WARNING: SL relaxation may cause trade count to change.
       If trades exceed 60, the backtest will be rejected.
       If trades drop below 30, it will also be rejected.
       Test as a single isolated change. Do not combine with PATH A1/A2.
    RATIONALE: With a 9.5% TP and 156hr timeout, a tighter SL at 1.5%
    may be stopping trades out prematurely before they can reach TP.
    A wider SL of 2.0% may allow more trades to survive and reach TP.
    This is a single-variable test. Name it: ..._gen15979_sl20

  PRIORITY ORDER THIS SESSION:
    1st choice: PATH A1 → timeout=192
    2nd choice: PATH A2 → TP=11.0
    3rd choice: PATH A3 → SL=2.0
    Alternate paths across consecutive generations.
    Do not attempt the same path twice in a row if it failed.

DO NOT attempt any other mutation type without MIMIR approval.

## ══════════════════════════════════════════════════════════════════════
## THE MOST IMPORTANT CONSTRAINT RIGHT NOW
## ══════════════════════════════════════════════════════════════