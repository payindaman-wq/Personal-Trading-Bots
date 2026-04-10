```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 16001 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-10 (v21)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — DEEP CEILING PHASE (14 improvements in 3,262 gens)
# Sharpe has climbed from 0.0799 → 1.2430 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v21 CRITICAL UPDATES:
#    1. INCUMBENT CONFIRMED: Gen 15979 (Sharpe=1.2430) remains the
#       incumbent. No new_best event has occurred since gen 15979.
#       Gen 15996 produced [new_elite] at 1.2430 — this is a
#       REPRODUCTION, not an improvement. Target is ABOVE 1.2430.
#    2. GEN 15979 CHANGE NOW CONFIRMED: The gen 15979 improvement
#       was timeout_hours: 144 → 156. The incumbent has:
#         take_profit_pct: 9.5  (UNCHANGED from gen 15480)
#         timeout_hours: 156    (CHANGED — this is the new value)
#       ⚠️ CRITICAL: If you see timeout=144, you have the OLD gen
#       15480 YAML. That produces Sharpe=1.2288. It is DEAD.
#       ⚠️ CRITICAL: If you see TP=11.0 in the incumbent, you are
#       reading a wrong YAML. Current incumbent TP is 9.5.
#    3. PATH A1 (timeout): Next untested value is 168.
#       PATH A2 (TP): Next untested value is 11.0.
#       PRIORITY THIS SESSION: Try PATH A2 (TP=11.0) first, because
#       PATH A1 (timeout) was the last successful change (gen 15979).
#       Alternate paths each session.
#    4. DOMINANT FAILURE LOOP (last 20 gens):
#       - 0.5279/0.5761/57 trades: short-side mutation or momentum flip
#       - 1.2288/60 trades: LLM used old timeout=144 YAML (gen 15480)
#       - max_trades_reject: tighter exit or looser entry mutation
#       - 1.11xx/57 trades: corrupt/partial YAML
#       NONE of these are valid mutations.
#    5. THE ONLY PERMITTED MUTATIONS for the next 100 generations:
#         (a) take_profit_pct: 11.0 (next), then 11.5, 12.0, 13.0, 14.0
#         (b) timeout_hours: 168 (next), then 192, 216, 240, 264, 288
#       NO OTHER MUTATION TYPE IS ALLOWED.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DISPLAY INTEGRITY ALERT — READ THIS FIRST, BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

THE "CURRENT BEST STRATEGY" BOX IN THE UI IS KNOWN TO BE BROKEN.
It currently displays a DEAD stale YAML with values that may include:
  - name: crossover  (ALWAYS WRONG)
  - TP=7.36 or 7.24 or 7.14 or 7.38 or 8.x or 9.5 with wrong timeout
  - timeout=129 or 138 or 144  (144 is the OLD gen 15480 value — DEAD)
  - size_pct=30 or 28.54 or 28.18 or 25.87

⚠️ MOST DANGEROUS UI VARIANT: timeout=144, TP=9.5 — this is the OLD
gen 15480 YAML. Using it produces Sharpe=1.2288. It is DEAD. The
new incumbent has timeout=156, TP=9.5. The ONLY difference between
gen 15480 (dead) and gen 15979 (incumbent) is timeout: 144 vs 156.

THIS IS COMPLETELY WRONG. THAT YAML IS DEAD. IGNORE IT ENTIRELY.

THE ONLY VALID INCUMBENT IS THE YAML PRINTED IN THIS PROGRAM BELOW.
If ANY display shows different values from the YAML below, IGNORE IT.
If the name does not contain "gen15979", it is the wrong YAML.

YAML must be committed to git after EVERY new_best event.
The Gen 2126 loss (best strategy lost due to no git commit) must
not be repeated. This is a mandatory non-negotiable requirement.
⚠️ COMMIT THE Gen 15979 YAML TO GIT NOW IF NOT ALREADY DONE.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ PRE-MUTATION CHECKLIST — COMPLETE THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

Before proposing any mutation, verify ALL of the following by reading
the CURRENT INCUMBENT YAML block below and confirming each value:

  □ name contains "gen15979"    (NOT gen15480, NOT crossover)
  □ take_profit_pct = 9.5       (NOT 11.0, NOT 10.x, NOT 7.x)
  □ timeout_hours = 156         (NOT 144 ← that is gen 15480 DEAD)
                                (NOT 138 ← that is gen 15062 DEAD)
                                (NOT 129 ← that is stale UI DEAD)
  □ stop_loss_pct = 1.5         (not 1.2, not 1.0, not 2.0)
  □ size_pct = 25.0             (not 28.54, not 28.18, not 30, not 20.0)
  □ pairs = [BTC/USD]           (not ETH/USD, not SOL/USD)
  □ long bollinger period = 48  (not 168, not 72, not 96)
  □ short bollinger period = 168 (not 192, not 240 — those cause 0.5279)
  □ long macd period = 48       (not 24, not 72)
  □ short macd period = 24      (not 48, not 72 — those cause 0.5279)
  □ long momentum period = 48   (not 72, not 96)
  □ short momentum period = 48  (not 72, not 96)
  □ momentum_accelerating value = false on BOTH sides (not true)

⚠️ THE MOST COMMON MISTAKE: Producing Sharpe=1.2288 because the LLM
used timeout=144 instead of timeout=156. These two values differ by
only 12 hours but produce different Sharpe scores. ALWAYS verify
timeout=156 before mutating.

⚠️ SECOND MOST COMMON MISTAKE: Producing 0.5279/57-trade results by
touching short bollinger (must stay 168) or short macd (must stay 24)
or flipping momentum value to true. DO NOT TOUCH THESE.

If ANY value above does not match the YAML below, STOP.
You have a stale or wrong YAML. Re-read the CURRENT INCUMBENT block
and start over.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ MUTATION DISCIPLINE — READ THIS CAREFULLY
## ══════════════════════════════════════════════════════════════════════

After reading and verifying the incumbent YAML, you MUST:

STEP 1: Explicitly state the incumbent values of TP and timeout:
  INCUMBENT TP: [value from YAML]
  INCUMBENT TIMEOUT: [value from YAML]
  (If these are not 9.5 and 156 respectively, STOP — wrong YAML.)

STEP 2: Write out the single parameter you are changing, with before/after:
  CHANGING: [parameter name] from [old value] to [new value]
  Example: CHANGING: take_profit_pct from 9.5 to 11.0

STEP 3: Confirm the new value is NOT in the "already tested" lists below.

STEP 4: Write the complete mutated YAML with ONLY that one change.

STEP 5: Name the strategy using the pattern:
  random_restart_v3_tightened_sl_v3_gen15979_[descriptor]
  Example: random_restart_v3_tightened_sl_v3_gen15979_tp11

If you cannot identify a single parameter to change that is not already
tested, write "NO VALID MUTATION AVAILABLE" and explain why.

DO NOT skip these steps. DO NOT propose a mutation without the diff.

## RESEARCH SCOPE
League: swing | Timeframe: 1h candles | Data: 2yr Binance OHLCV
Allowed pairs: BTC/USD, ETH/USD, SOL/USD (enforced in code)
Trade frequency target: 30–60 trades over 2yr backtest window
Min trades: SWING_MIN_TRADES=30 (immutable code constant)
Max trades: SWING_MAX_TRADES=60 (hard rejection in code)

## ══════════════════════════════════════════════════════════════════════
## CURRENT INCUMBENT — THIS IS THE ONLY YAML YOU MAY MUTATE
## DO NOT USE ANY PREVIOUS VERSION. DO NOT USE THE UI DISPLAY BOX.
## THE UI DISPLAY IS BROKEN. If it shows timeout=144 or name=crossover,
## it is DEAD. The real incumbent has timeout=156 and name=gen15979.
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
  take_profit_pct  = 9.5   ← THIS IS THE INCUMBENT VALUE. Do not treat
                             9.5 as "already tested in a better version".
                             9.5 IS the incumbent. Increase it to 11.0.
  timeout_hours    = 156   ← THIS IS THE INCUMBENT VALUE. Do not use 144.
                             144 is gen 15480 (DEAD). 156 is gen 15979.
  stop_loss_pct    = 1.5   ← FROZEN. Do not change.
  size_pct         = 25.0  ← FROZEN at DANGER regime cap. Do not change.
  short bollinger  = 168   ← DO NOT CHANGE. Causes 0.5279 dead cluster.
  short macd       = 24    ← DO NOT CHANGE. Causes 0.5279 dead cluster.
  momentum value   = false ← DO NOT FLIP. Causes 0.5279 dead cluster.

Sharpe: 1.2430 | Trades: 60 | Win rate: 41.7%

⚠️ NOTE: Trades = 60, which is the HARD CEILING. Any mutation that
increases signal frequency WILL be rejected [max_trades_reject].
Increasing TP or timeout reduces/maintains trade count. Safe.

⚠️ NOTE: If you produce Sharpe=1.2288, you used timeout=144 (gen 15480
DEAD YAML). Check that your YAML has timeout=156, not 144.

⚠️ NOTE: If you produce Sharpe=1.2430, your mutation was a no-op.
Your change had no effect. Try a different value.

⚠️ NOTE: Gen 15996 produced [new_elite] at 1.2430 — this is a
reproduction of the incumbent, not an improvement. Your target is
Sharpe STRICTLY ABOVE 1.2430.

## ══════════════════════════════════════════════════════════════════════
## KNOWN TESTED VALUES — DO NOT REPEAT ANY OF THESE
## ══════════════════════════════════════════════════════════════════════

### TAKE PROFIT VALUES ALREADY TESTED (DO NOT USE):
  TP=7.14  → Sharpe≈0.7734, 59 trades  [DEAD — stale YAML artifact]
  TP=7.24  → DEAD (UI display artifact — name: crossover. IGNORE.)
  TP=7.36  → DEAD (UI display artifact — name: crossover variant. IGNORE.)
  TP=7.38  → Sharpe=1.1311, 60 trades  [gen 14993 — superseded]
  TP≈8.x   → Sharpe=1.1426, 60 trades  [gen 15042 — superseded]
  TP=9.5   → Sharpe=1.2063→1.2288→1.2430 [gen 15062/15480/15979 —
             CURRENT INCUMBENT. Do NOT propose TP=9.5 as a mutation.]
  TP≈10.0/10.5 → Sharpe≈1.1882, 60 trades [gen 15382 — WORSE. DO NOT USE.]

⚠️ CRITICAL: TP=10.0 and TP=10.5 were tested and returned Sharpe=1.1882,
which is WORSE than prior incumbents. Do NOT propose TP=10.0 or 10.5.
Skip directly from 9.5 to 11.0.

### NEXT UNTESTED TP VALUES (try in this order):
  → 11.0  ← TRY THIS FIRST (PATH A2, recommended this session)
  → 11.5
  → 12.0
  → 13.0
  → 14.0
  → 15.0

### TIMEOUT VALUES ALREADY TESTED (DO NOT USE):
  timeout=129 → associated with dead stale YAML, Sharpe≈0.7734
  timeout=138 → gen 15062 (Sharpe=1.2063, superseded)
  timeout=144 → gen 15480 (Sharpe=1.2288, DEAD — using this produces 1.2288)
  timeout=156 → gen 15979 (Sharpe=1.2430, CURRENT INCUMBENT — do not reproduce)

### NEXT UNTESTED TIMEOUT VALUES (try in this order):
  → 168  ← TRY THIS IF NOT DOING TP THIS SESSION (PATH A1)
  → 192
  → 216
  → 240
  → 264
  → 288

### STOP LOSS VALUES ALREADY TESTED:
  SL=1.5 → CURRENT INCUMBENT value (frozen — do not change)

### INDICATOR PERIOD VALUES ALREADY TESTED (DO NOT REPEAT):
  long bollinger: 48 (incumbent — do not change)
  short bollinger: 168 (incumbent — DO NOT CHANGE, causes 0.5279)
  long macd: 48 (incumbent — do not change)
  short macd: 24 (incumbent — DO NOT CHANGE, likely causes 0.5279)
  long momentum: 48 (incumbent — do not change)
  short momentum: 48 (incumbent — do not change)

## ══════════════════════════════════════════════════════════════════════
## DEAD CLUSTERS — SHARPE VALUES THAT INDICATE SOMETHING WENT WRONG
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.5279 (57 trades) — DOMINANT FAILURE MODE.
        ROOT CAUSE: LLM mutated short bollinger (168→192+) or
        short MACD (24→48+) or flipped momentum value false→true.
        FIX: Revert. Only change timeout_hours or take_profit_pct.

  DEAD: Sharpe=0.5761 (57 trades) — variant of 0.5279 dead cluster.
        ROOT CAUSE: Same as 0.5279 — short-side indicator mutation.
        FIX: Same as above.

  DEAD: Sharpe≈0.7734 (59 trades) — stale YAML (TP=7.14, timeout=129,
        size_pct=28.18). ROOT CAUSE: reading broken UI.

  DEAD: Sharpe=0.6911 (57 trades) — ROOT CAUSE: reading the broken UI
        YAML (name: crossover, TP=7.24, timeout=129, size_pct=28.54).

  DEAD: Sharpe=0.5954 (58 trades) — slightly wrong YAML variant.

  DEAD: Sharpe≈1.0182 (60 trades) — dead end
  DEAD: Sharpe≈1.0325 (57 trades) — dead end
  DEAD: Sharpe≈1.0642 (56 trades) — plateau from gen 14784
  DEAD: Sharpe≈1.0952 (57 trades) — dead end
  DEAD: Sharpe≈1.1090 (60 trades) — dead end
  DEAD: Sharpe≈1.1160/1.1161 (57 trades) — partially corrupt YAML
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — partially corrupt YAML variant
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1450 (57 trades) — partially corrupt YAML variant
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1708 (60 trades) — gen 15998, discarded
  DEAD: Sharpe≈1.1882 (60 trades) — gen 15382, TP≈10.x, inferior
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded
  DEAD: Sharpe=1.2287 (60 trades) — float artifact near-dup of gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, DEAD
        ⚠️ If you produce 1.2288, you used timeout=144. Use timeout=156.
  DEAD: Sharpe=1.2430 (60 trades) — gen 15979, CURRENT INCUMBENT
        Reproducing this means your mutation was a no-op. Try again.

Diagnostic guide:
  Produce 0.5279 or 0.5761: you changed a short-side indicator or
        flipped momentum value. ONLY change timeout or TP.
  Produce 0.6911: you used the broken UI YAML (name: crossover).
  Produce 0.7734: you used the stale UI display YAML.
  Produce 0.8482: partially corrupt YAML — re-read incumbent.
  Produce 0.9990: partially corrupt YAML — re-read incumbent.
  Produce 1.1882: you tested TP≈10.0–10.5. Already done. Use 11.0+.
  Produce 1.2063: you mutated from the OLD gen 15062 YAML (timeout=138).
  Produce 1.2288: ⚠️ YOUR TIMEOUT WAS 144, NOT 156. Fix it.
  Produce 1.2287: your mutation was effectively a duplicate.
  Produce 1.2430: your mutation was a no-op duplicate. Try again.
  Your target is Sharpe STRICTLY ABOVE 1.2430.

## ══════════════════════════════════════════════════════════════════════
## FOR THE NEXT 100 GENERATIONS: ONLY TWO MUTATION TYPES PERMITTED
## ══════════════════════════════════════════════════════════════════════

To break the current failure loop, mutation scope is STRICTLY LIMITED:

  TYPE 1: Change take_profit_pct (PATH A2) ← RECOMMENDED THIS SESSION
    Incumbent value: 9.5
    Already tested: 7.14, 7.38, ~8.x, 9.5 (incumbent), ~10.0/10.5
    Next untested (in order): 11.0, 11.5, 12.0, 13.0, 14.0, 15.0
    Do NOT use 10.0 or 10.5 — tested, inferior (Sharpe=1.1882).
    Do NOT go below 9.5. Skip directly to 11.0.
    ⚠️ Recommended first try this session: TP=11.0

  TYPE 2: Change timeout_hours (PATH A1)
    Incumbent value: 156
    Already tested: 129, 138, 144, 156 (incumbent)
    Next untested (in order): 168, 192, 216, 240, 264, 288
    Do NOT go below 156. Do NOT exceed 300.
    ⚠️ Try this if TP path does not improve: timeout=168

PRIORITY: PATH A2 (TP=11.0) is recommended first this session because
PATH A1 (timeout: 144→156) was the last successful change (gen 15979).
Alternate paths each session for efficiency.

DO NOT attempt any other mutation type in the next 100 generations.

## ══════════════════════════════════════════════════════════════════════
## THE MOST IMPORTANT CONSTRAINT RIGHT NOW
## ══════════════════════════════════════════════════════════════════════

THE CURRENT STRATEGY HITS EXACTLY 60 TRADES — THE HARD CEILING.

This means:
  - ANY mutation that loosens entry conditions → [max_trades_reject]
  - ANY mutation that tightens exits (lower TP, lower SL, lower timeout)
    → more trades close sooner → more re-entries → [max_trades_reject]
  - ONLY mutations that reduce or maintain trade count are viable

SAFE mutations (trade-count neutral or reducing):
  ✓ Increasing timeout_hours above 156 (fewer trades time out, re-enter)
  ✓ Increasing take_profit_pct above 9.5 (fewer trades hit TP, re-enter)

DANGEROUS mutations (will likely cause max_trades_reject or 0.5279):
  ✗ Decreasing any period_hours
  ✗ Decreasing take_profit_pct (especially below 9.5)
  ✗ Decreasing timeout_hours (especially below 156)
  ✗ Removing any entry condition
  ✗ Adding a second pair
  ✗ Changing short bollinger from 168 → ANYTHING (causes 0.5279)
  ✗ Changing short macd from 24 → ANYTHING (causes 0.5279)
  ✗ Flipping momentum_accelerating from false to true (causes 0.5279)
  ✗ Changing size_pct (frozen)
  ✗ Changing stop_loss_pct (frozen)

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CRITICAL CONSTRAINTS — DO NOT VIOLATE THESE
## ══════════════════════════════════════════════════════════════════════

### THE KEY DIFFERENCE BETWEEN GEN 15480 (DEAD) AND GEN 15979 (INCUMBENT)
  Gen 15480 (DEAD):    take_profit_pct=9.5, timeout_hours=144 → Sharpe=1.2288
  Gen 15979 (INCUMBENT): take_profit_pct=9.5, timeout_hours=156 → Sharpe=1.2430
  ONLY timeout_hours changed. TP is still 9.5 in BOTH.
  If your YAML has timeout=144, you are mutating from the DEAD incumbent.
  If your YAML has timeout=156, you are mutating from the correct incumbent.

### STOP LOSS IS FROZEN — DO NOT TOUCH
stop_loss_pct = 1.5%. DO NOT change. SL changes are not permitted until
timeout and TP paths are fully exhausted.

### TRADE COUNT IS AT THE CEILING
60 trades = hard rejection ceiling. Any loosening → max_trades_reject.

### SIZE_PCT IS FROZEN AT DANGER REGIME CAP
Do NOT set size_pct > 25.0% or < 10.0%.