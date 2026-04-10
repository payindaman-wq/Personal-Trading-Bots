```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 16401 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-10 (v22)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — DEEP CEILING PHASE (14 improvements in 3,662 gens)
# Sharpe has climbed from 0.0799 → 1.2430 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE AND FROZEN.
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v22 CRITICAL UPDATES:
#    1. INCUMBENT UNCHANGED: Gen 15979 (Sharpe=1.2430) remains the
#       incumbent. No new_best event has occurred since gen 15979.
#       Gens 16386, 16387, 16396, 16400 produced [discarded] at 1.2430
#       — these are REPRODUCTIONS, not improvements. Target: ABOVE 1.2430.
#    2. DOMINANT FAILURE MODE (last 20 gens, ~50% of attempts):
#       Sharpe=0.5761, 57 trades. ROOT CAUSE: LLM mutated short bollinger
#       (168) or short MACD (24) or flipped momentum value. This has
#       appeared 7 times in the last 20 generations. DO NOT TOUCH THESE.
#    3. PATH PRIORITY SWITCH: PATH A1 (timeout) is now RECOMMENDED
#       because PATH A2 (TP) was recommended last session AND TP=10.x
#       tested worse than TP=9.5 (Sharpe=1.1882), suggesting the TP
#       improvement curve is non-monotone. PATH A1 next value: 168.
#       PATH A2 remains available: next value 11.0.
#    4. INCUMBENT YAML: The only valid incumbent has:
#         take_profit_pct: 9.5   (UNCHANGED)
#         timeout_hours:   156   (UNCHANGED — not 144, not 138, not 129)
#       If you see ANY other values, you have the WRONG YAML.
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

⚠️ MOST DANGEROUS UI VARIANT: timeout=144, TP=9.5 — this is the OLD
gen 15480 YAML. Using it produces Sharpe=1.2288. It is DEAD.
The real incumbent has timeout=156, TP=9.5.

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
  □ stop_loss_pct = 1.5                (FROZEN — do not change)
  □ size_pct = 25.0                    (FROZEN — do not change)
  □ pairs = [BTC/USD]                  (do not add ETH/USD or SOL/USD)
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

⚠️ MOST COMMON MISTAKE #3: Producing Sharpe=1.2430 (no-op
reproduction). This means your proposed value is the same as the
incumbent. The incumbent TP is 9.5 and timeout is 156. Change one
of these to a NEW value: TP→11.0 or timeout→168.

If ANY value above does not match the YAML below, STOP.
You have a stale or wrong YAML. Re-read the CURRENT INCUMBENT block.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ 0.5761 FAILURE DIAGNOSIS — IF YOU SEE THIS OUTPUT, READ THIS
## ══════════════════════════════════════════════════════════════════════

IF YOUR BACKTEST PRODUCES Sharpe=0.5761, trades=57:
  YOU CHANGED THE SHORT BOLLINGER PERIOD (must be 168)
  OR YOU CHANGED THE SHORT MACD PERIOD (must be 24)
  OR YOU FLIPPED momentum_accelerating FROM false TO true
  THIS IS THE #1 FAILURE MODE. It happened 7 times in the last 20 gens.

HOW TO FIX: Revert ALL indicator changes. Keep all indicators exactly
as they are in the gen15979 incumbent YAML. The ONLY parameters you
are allowed to change are take_profit_pct and timeout_hours.

DO NOT CHANGE ANY INDICATOR. DO NOT CHANGE ANY PERIOD. DO NOT FLIP
ANY VALUE. CHANGE ONLY TP OR TIMEOUT. NOTHING ELSE.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ MUTATION DISCIPLINE — FOLLOW THESE STEPS EXACTLY
## ══════════════════════════════════════════════════════════════════════

STEP 1: Read the CURRENT INCUMBENT YAML block below.
        Explicitly write out:
          INCUMBENT TP: [value]       ← must be 9.5
          INCUMBENT TIMEOUT: [value]  ← must be 156
        If these are not 9.5 and 156, STOP — you have the wrong YAML.

STEP 2: Write the single parameter you are changing, before/after:
          CHANGING: [parameter] from [old value] to [new value]
          Example: CHANGING: timeout_hours from 156 to 168
          Example: CHANGING: take_profit_pct from 9.5 to 11.0

STEP 3: Confirm the new value is NOT in the "already tested" lists.

STEP 4: Write the complete mutated YAML with ONLY that one change.
        Every other value must be IDENTICAL to the incumbent.

STEP 5: Name the strategy:
          random_restart_v3_tightened_sl_v3_gen15979_[descriptor]
          Example: random_restart_v3_tightened_sl_v3_gen15979_timeout168
          Example: random_restart_v3_tightened_sl_v3_gen15979_tp11

If you cannot identify a valid untested mutation, write
"NO VALID MUTATION AVAILABLE" and explain why.

## RESEARCH SCOPE
League: swing | Timeframe: 1h candles | Data: 2yr Binance OHLCV
Allowed pairs: BTC/USD, ETH/USD, SOL/USD (enforced in code)
Trade frequency target: 30–60 trades over 2yr backtest window
Min trades: SWING_MIN_TRADES=30 (immutable code constant)
Max trades: SWING_MAX_TRADES=60 (hard rejection in code)

## ══════════════════════════════════════════════════════════════════════
## CURRENT INCUMBENT — THIS IS THE ONLY YAML YOU MAY MUTATE
## DO NOT USE ANY PREVIOUS VERSION. DO NOT USE THE UI DISPLAY BOX.
## THE UI DISPLAY IS BROKEN. The real incumbent has:
##   name=gen15979, timeout=156, TP=9.5, size_pct=25.0
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
  take_profit_pct  = 9.5   ← INCUMBENT. Change to 11.0 if using PATH A2.
  timeout_hours    = 156   ← INCUMBENT. Change to 168 if using PATH A1.
                             DO NOT use 144 (gen 15480 DEAD).
  stop_loss_pct    = 1.5   ← FROZEN.
  size_pct         = 25.0  ← FROZEN.
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
  TP=10.0  → Sharpe≈1.1882, 60 trades  [WORSE than 9.5 — DO NOT USE]
  TP=10.5  → Sharpe≈1.1882, 60 trades  [WORSE than 9.5 — DO NOT USE]

⚠️ CRITICAL: TP=10.0 and TP=10.5 were tested and returned Sharpe=1.1882,
which is WORSE than the current incumbent. The TP improvement curve is
NON-MONOTONE. Skip 10.0 and 10.5. Start at 11.0.

### NEXT UNTESTED TP VALUES (try in this order):
  → 11.0  ← PATH A2 (available if not using PATH A1 this session)
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

### NEXT UNTESTED TIMEOUT VALUES (try in this order):
  → 168  ← PATH A1 — RECOMMENDED THIS SESSION (primary)
  → 192
  → 216
  → 240
  → 264
  → 288

### STOP LOSS VALUES (FROZEN — DO NOT TEST):
  SL=1.5 → CURRENT INCUMBENT (frozen — do not change)

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

  DEAD: Sharpe=0.5279 (57 trades) — short-side indicator mutation.
  DEAD: Sharpe=0.5761 (57 trades) — ⚠️ DOMINANT FAILURE (7/20 gens).
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
  DEAD: Sharpe≈1.1450 (57 trades) — corrupt/partial YAML
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1708 (60 trades) — gen 15998, discarded
  DEAD: Sharpe≈1.1882 (60 trades) — TP=10.0 or 10.5, inferior to 9.5
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded
  DEAD: Sharpe=1.2287 (60 trades) — float duplicate of gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, timeout=144 DEAD
  DEAD: Sharpe=1.2430 (60 trades) — gen 15979, CURRENT INCUMBENT
        Reproducing this = no-op. Your mutation had no effect.

Diagnostic guide:
  Got 0.5761 or 0.5279: you changed short bollinger/MACD or flipped
        momentum. ONLY change TP or timeout. Nothing else.
  Got 0.6911: you used the broken UI YAML (name: crossover).
  Got 0.7734: you used the stale UI YAML (timeout=129).
  Got 1.1882: you tested TP=10.0 or 10.5. Already done. Use 11.0+.
  Got 1.2063: you mutated from gen 15062 YAML (timeout=138). DEAD.
  Got 1.2288: YOUR TIMEOUT WAS 144, NOT 156. Fix it immediately.
  Got 1.2430: your mutation was a no-op. The value you used is the
        same as the incumbent (TP=9.5 or timeout=156). Use the NEXT
        untested value: TP→11.0 or timeout→168.

Your target is Sharpe STRICTLY ABOVE 1.2430.

## ══════════════════════════════════════════════════════════════════════
## FOR THE NEXT 100 GENERATIONS: ONLY TWO MUTATION TYPES PERMITTED
## ══════════════════════════════════════════════════════════════════════

  TYPE 1 (PATH A1): Change timeout_hours ← RECOMMENDED THIS SESSION
    Incumbent value: 156
    Already tested:  129, 138, 144, 156
    Next untested (in order): 168, 192, 216, 240, 264, 288
    Do NOT go below 156. Do NOT exceed 300.
    ⚠️ PRIMARY RECOMMENDATION: timeout=168

  TYPE 2 (PATH A2): Change take_profit_pct
    Incumbent value: 9.5
    Already tested:  7.14, 7.38, ~8.x, 9.5, ~10.0, ~10.5
    Next untested (in order): 11.0, 11.5, 12.0, 13.0, 14.0, 15.0
    Do NOT use 10.0 or 10.5 — tested, inferior (Sharpe=1.1882).
    Do NOT go below 9.5. Start at 11.0.
    ⚠️ NOTE: TP=10.x was WORSE than TP=9.5. Curve is non-monotone.
    ⚠️ SECONDARY RECOMMENDATION: TP=11.0 (if not doing PATH A1)

PRIORITY THIS SESSION: PATH A1 (timeout=168) because:
  - PATH A2 was recommended last session
  - TP=10.x tested inferior, suggesting TP curve may be flattening
  - Timeout increases have been the most reliable improvement path
  Alternate paths each session.

DO NOT attempt any other mutation type. These are the ONLY two
permitted mutations for the next 100 generations.

## ══════════════════════════════════════════════════════════════════════
## THE MOST IMPORTANT CONSTRAINT RIGHT NOW
## ══════════════════════════════════════════════════════════════════════

THE CURRENT STRATEGY HITS EXACTLY 60 TRADES — THE HARD CEILING.

This means:
  - ANY mutation that loosens entry conditions → [max_trades_reject]
  - ANY mutation that tightens exits (lower TP, lower SL, lower timeout)
    → trades close sooner → more re-entries → [max_trades_reject]
  - ONLY mutations that reduce or maintain trade count are viable

SAFE mutations (trade-count neutral or reducing):
  ✓ Increasing timeout_hours above 156 (fewer time-outs, fewer re-entries)
  ✓ Increasing take_profit_pct above 9.5 (fewer TP hits, fewer re-entries)

DANGEROUS mutations (WILL cause max_trades_reject or 0.5761):
  ✗ Decreasing any period_hours
  ✗ Decreasing take_profit_pct (below 9.5)
  ✗ Decreasing timeout_hours (below 156)
  ✗ Removing any entry condition
  ✗ Adding a second pair
  ✗ Changing short bollinger 168 → ANYTHING  (causes 0.5761)
  ✗ Changing short macd 24 → ANYTHING        (causes 0.5761)
  ✗ Flipping momentum_accelerating false→true (causes 0.5761)
  ✗ Changing size_pct (frozen at 25.0)
  ✗ Changing stop_loss_pct (frozen at 1.5)
  ✗ Changing max_open (frozen at 2)

## ══════════════════════════════════════════════════════════════════════
## KEY DIFFERENCE: GEN 15480 (DEAD) vs GEN 15979 (INCUMBENT)
## ══════════════════════════════════════════════════════════════════════

  Gen 15480 (DEAD):      take_profit_pct=9.5, timeout_hours=144 → 1.2288
  Gen 15979 (INCUMBENT): take_profit_pct=9.5, timeout_hours=156 → 1.2430

  THE ONLY DIFFERENCE IS timeout_hours: 144 vs 156.
  If your YAML has timeout=144, you are mutating from the DEAD incumbent.
  If your YAML has timeout=156, you are mutating from the correct one.

## ══════════════════════════════════════════════════════════════════════
## STRUCTURAL REASSESSMENT TRIGGER
## ══════════════════════════════════════════════════════════════════════

If neither PATH A1 (timeout) nor PATH A2 (TP) produces improvement
through gen 16500, escalate to MIMIR for structural reassessment.
Potential future directions (NOT permitted yet):
  - Adding a second confirmation indicator on the long side
  - Pair expansion (ETH/USD) with tight controls
  - Risk parameter adjustment (pause_if_down_pct, pause_hours)
  - Stop loss relaxation trial (SL=2.0) as a single test
These are BLOCKED until the current two paths are exhausted.

## ══════════════════════════════════════════════════════════════════════
## GIT COMMIT REMINDER
## ══════════════════════════════════════════════════════════════════════

YAML must be committed to git after EVERY new_best event.
The Gen 2126 loss (best strategy lost due to no git commit) must
not be repeated. This is a mandatory non-negotiable requirement.
⚠️ COMMIT THE Gen 15979 YAML TO GIT NOW IF NOT ALREADY DONE.
After any future new_best event, commit IMMEDIATELY before proceeding.
```