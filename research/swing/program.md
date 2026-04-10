```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 15980 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-10 (v20)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — DEEP CEILING PHASE (14 improvements in 3,255 gens)
# Sharpe has climbed from 0.0799 → 1.2430 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v20 CRITICAL UPDATES:
#    1. NEW INCUMBENT: Gen 15979 (Sharpe=1.2430) is now the incumbent.
#       The prior incumbent was Gen 15480 (Sharpe=1.2288). The YAML
#       below reflects the NEW incumbent. Do NOT use the old YAML.
#    2. THREE-WAY FAILURE LOOP CONTINUES: Last 20 gens before 15979:
#       - 0.5279/57 (dead cluster): 4 occurrences
#       - 1.2288/60 (old incumbent reproduction): 5 occurrences
#       - max_trades_reject (0 trades): 5 occurrences
#       - corrupt variants (1.1160, 0.8482, 0.9990, 1.1643): 4 occ.
#       NONE of these are valid mutations. The LLM must change
#       EXACTLY ONE parameter to a value NOT YET TESTED.
#    3. MUTATION SPACE REMAINS NARROWED: For the next 100 generations,
#       the ONLY permitted mutations are:
#         (a) timeout_hours: values not yet tested (see list below)
#         (b) take_profit_pct: values not yet tested (see list below)
#       DO NOT attempt any other mutation type.
#    4. INCUMBENT IS NOW Gen 15979. The old Gen 15480 incumbent
#       (Sharpe=1.2288) is now DEAD. Do not reproduce it.
#    5. ⚠️ CRITICAL: If you produce Sharpe=1.2288, you have reproduced
#       the OLD incumbent. Your YAML is wrong. The new incumbent has
#       Sharpe=1.2430. Re-read the YAML below and try again.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DISPLAY INTEGRITY ALERT — READ THIS FIRST, BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

THE "CURRENT BEST STRATEGY" BOX IN THE UI IS KNOWN TO BE BROKEN.
It currently displays a DEAD stale YAML with values:
  - name: crossover
  - TP=7.36 (or 7.24, or 7.14, or 7.38, or 8.x)
  - timeout=129 (or 138)
  - size_pct=30 (or 28.54, or 28.18, or 25.87)

THIS IS COMPLETELY WRONG. THAT YAML IS DEAD. IGNORE IT ENTIRELY.

Additional broken UI variants that have appeared before:
  - TP=7.14 or TP=5.95 or TP=7.38 or TP=8.x or TP=9.5 or TP=10.x
  - timeout=129 or timeout=138 or timeout=144
  - size_pct=28.18 or size_pct=25.87 or size_pct=25.0 with wrong TP
  - name: crossover (this is ALWAYS wrong — incumbent name contains gen15979)

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
  □ take_profit_pct = [READ FROM YAML BELOW — verify exact value]
  □ timeout_hours = [READ FROM YAML BELOW — verify exact value]
  □ stop_loss_pct = 1.5         (not 1.2, not 1.0, not 2.0)
  □ size_pct = 25.0             (not 28.54, not 28.18, not 30, not 20.0)
  □ pairs = [BTC/USD]           (not ETH/USD, not SOL/USD)
  □ long bollinger period = 48  (not 168, not 72, not 96)
  □ short bollinger period = 168 (not 48, not 96, not 192, not 240)
  □ long macd period = 48       (not 24, not 72)
  □ short macd period = 24      (not 48, not 72)
  □ long momentum period = 48   (not 72, not 96)
  □ short momentum period = 48  (not 72, not 96)
  □ momentum_accelerating value = false on BOTH sides (not true)

If ANY value above does not match the YAML below, STOP.
You have a stale or wrong YAML. Re-read the CURRENT INCUMBENT block
and start over.

⚠️ SPECIAL WARNING: If you see timeout_hours=144 and TP=9.5, you have
the OLD gen 15480 YAML. That is DEAD. The new incumbent has different
exit parameters. Stop and re-read the YAML below.
⚠️ SPECIAL WARNING: If you see timeout_hours=138, you have the even
older gen 15062 YAML. Correct value is in the YAML below. Stop.
⚠️ SPECIAL WARNING: If you see short bollinger period=192 or 240,
you are mutating from a corrupt YAML. That produces Sharpe=0.5279.
⚠️ SPECIAL WARNING: If you see momentum_accelerating value=true,
you are mutating from a corrupt YAML. Incumbent uses value=false.
⚠️ SPECIAL WARNING: If the name says "crossover", it is the broken
UI YAML. Ignore it entirely. The real incumbent name has "gen15979".

Only after confirming ALL values above should you propose ONE change.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ MUTATION DISCIPLINE — READ THIS CAREFULLY
## ══════════════════════════════════════════════════════════════════════

After reading and verifying the incumbent YAML, you MUST:

STEP 1: Write out the single parameter you are changing, with before/after:
  CHANGING: [parameter name] from [old value] to [new value]
  Example: CHANGING: timeout_hours from [incumbent value] to [new value]

STEP 2: Confirm the new value is NOT in the "already tested" lists below.

STEP 3: Write the complete mutated YAML with ONLY that one change.

STEP 4: Name the strategy using the pattern:
  random_restart_v3_tightened_sl_v3_gen15979_[descriptor]
  Example: random_restart_v3_tightened_sl_v3_gen15979_timeout168

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
## THE UI DISPLAY IS BROKEN AND SHOWS STALE DATA (name: crossover). IGNORE IT.
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

⚠️ NOTE: The exit parameters above show the MOST LIKELY values for
Gen 15979 based on the permitted mutation paths. However, because the
exact parameter changed in Gen 15979 is not yet confirmed in this
program version, MIMIR instructs you to:
  - Read the YAML above carefully
  - Verify take_profit_pct and timeout_hours against the checklist
  - Cross-reference with the "already tested" lists below
  - The one that was NOT in the old tested list but IS in the new
    YAML is the parameter that was just changed

Sharpe: 1.2430 | Trades: 60 | Win rate: 41.7%
stop_loss_pct: 1.5     ← VERIFY THIS VALUE BEFORE MUTATING
size_pct: 25.0         ← VERIFY THIS VALUE BEFORE MUTATING
short bollinger: 168   ← DO NOT CHANGE THIS — causes 0.5279 dead cluster
short macd: 24         ← DO NOT CHANGE THIS — causes 0.5279 dead cluster
momentum value: false  ← DO NOT FLIP THIS TO true

⚠️ NOTE: size_pct is 25.0% — at the DANGER regime cap. Do not exceed.
⚠️ NOTE: Trades = 60, which is the HARD CEILING. Any mutation that
increases signal frequency WILL be rejected [max_trades_reject].
Every mutation must be trade-count neutral or trade-count reducing.
⚠️ NOTE: short bollinger period is 168. If you see 192+, corrupt YAML.
         That variant produces Sharpe=0.5279 (57 trades). Do not use it.
⚠️ NOTE: If you produce Sharpe=1.2288 (60 trades), you have reproduced
         the OLD gen 15480 incumbent. Your YAML was wrong. Try again.

## ══════════════════════════════════════════════════════════════════════
## KNOWN TESTED VALUES — DO NOT REPEAT ANY OF THESE
## ══════════════════════════════════════════════════════════════════════

### TAKE PROFIT VALUES ALREADY TESTED:
  TP=7.14  → Sharpe≈0.7734, 59 trades [DEAD — stale YAML artifact]
  TP=7.24  → DEAD (UI display artifact — name: crossover. IGNORE.)
  TP=7.36  → DEAD (UI display artifact — name: crossover variant. IGNORE.)
  TP=7.38  → Sharpe=1.1311, 60 trades [gen 14993 — superseded]
  TP≈8.x   → Sharpe=1.1426, 60 trades [gen 15042 — superseded]
  TP=9.5   → Sharpe=1.2063→1.2288, 60 trades [gen 15480 — superseded]
  TP≈10.x  → Sharpe≈1.1882, 60 trades [gen 15382 — WORSE than 1.2063]

⚠️ CRITICAL: TP≈10.x was tested and returned Sharpe=1.1882, which is
WORSE than prior incumbent 1.2063. Do NOT propose TP=10.0 or TP=10.5.
⚠️ NOTE: TP=11.0 may already be the Gen 15979 incumbent value (if PATH
A2 was the successful mutation). Check the incumbent YAML above.
If TP=11.0 is in the incumbent, it is tested. Next would be 11.5.
If TP=9.5 is still in the incumbent, then timeout was the change.
Next TP values to test (PATH A2, in order): 11.0, 11.5, 12.0, 13.0, 14.0
(Skip any that match the incumbent value — it is already tested.)

### TIMEOUT VALUES ALREADY TESTED:
  timeout=129 → associated with dead stale YAML, Sharpe≈0.7734
  timeout=138 → gen 15062 (Sharpe=1.2063, superseded)
  timeout=144 → gen 15480 (Sharpe=1.2288, superseded — NOW DEAD)
  timeout=156 → likely Gen 15979 incumbent value (PATH A1 success)
               IF this is in the incumbent YAML, it is tested.
               Next value would be 168.
               IF this is NOT in the incumbent, 156 is still untested.

⚠️ NOTE: Check the incumbent YAML above. Whichever of {timeout=156,
TP=11.0} appears in the incumbent YAML is the parameter that was just
tested and improved. The other path remains fully open.

### STOP LOSS VALUES ALREADY TESTED:
  SL=1.5 → CURRENT INCUMBENT value (do not decrease)

### INDICATOR PERIOD VALUES ALREADY TESTED (DO NOT REPEAT):
  long bollinger: 48 (incumbent)
  short bollinger: 168 (incumbent — DO NOT CHANGE, causes 0.5279)
  long macd: 48 (incumbent)
  short macd: 24 (incumbent — DO NOT CHANGE, likely causes 0.5279)
  long momentum: 48 (incumbent)
  short momentum: 48 (incumbent)

## ══════════════════════════════════════════════════════════════════════
## DEAD CLUSTERS — SHARPE VALUES THAT INDICATE SOMETHING WENT WRONG
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.5279 (57 trades) — DOMINANT FAILURE MODE.
        ROOT CAUSE: LLM mutated a short-side indicator period
        (short Bollinger 168→192+ or short MACD 24→48+) OR flipped
        momentum_accelerating value from false→true.
        If you produce 0.5279: your mutation changed a short-side
        condition. DO NOT touch short-side indicator periods or the
        momentum value field. Only change timeout_hours or TP.

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
  DEAD: Sharpe≈1.1160/1.1161 (57 trades) — partially corrupt YAML variant
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — partially corrupt YAML variant
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1882 (60 trades) — gen 15382, TP≈10.x attempt, inferior
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded by gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, SUPERSEDED BY GEN 15979
        ⚠️ CRITICAL: If you produce 1.2288, you reproduced the OLD
        incumbent. Your YAML had wrong exit parameters. Try again.
  DEAD: Sharpe=1.2287 (60 trades) — float artifact near-dup of gen 15480
  DEAD: Sharpe=1.2430 (60 trades) — gen 15979, CURRENT INCUMBENT
        (reproducing this means your mutation was a no-op — try again)

Diagnostic guide:
  If you produce 0.5279: you mutated a short-side indicator period OR
        flipped momentum_accelerating value to true. Revert. Only
        change timeout_hours or take_profit_pct.
  If you produce 0.6911: you used the broken UI YAML (name: crossover).
  If you produce 0.7734: you used the stale UI display YAML.
  If you produce 0.8482: partially corrupt YAML — re-read incumbent.
  If you produce 0.9990: partially corrupt YAML — re-read incumbent.
  If you produce 1.1882: you tested TP≈10.0–10.5. Already done.
  If you produce 1.2063: you mutated from the OLD gen 15062 YAML.
  If you produce 1.2288: you reproduced the OLD gen 15480 YAML.
        Your exit parameters were wrong. Check TP and timeout.
  If you produce 1.2287: your mutation was effectively a duplicate.
  If you produce 1.2430: your mutation was a no-op duplicate. Try again.
  Your target is Sharpe STRICTLY ABOVE 1.2430.

## ══════════════════════════════════════════════════════════════════════
## CRITICAL INSTRUCTION — READ THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

You MUST propose exactly ONE small change to the CURRENT INCUMBENT YAML
above. Do NOT generate a new strategy from scratch. Do NOT change more
than one parameter at a time. Do NOT use any older YAML versions.
Do NOT use the UI "Current Best Strategy" display — it shows
"name: crossover" with WRONG values. It is broken. Ignore it.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ FOR THE NEXT 100 GENERATIONS: ONLY TWO MUTATION TYPES PERMITTED
## ══════════════════════════════════════════════════════════════════════

To break the current three-way failure loop (0.5279 / reproduction /
max_trades_reject), mutation scope is STRICTLY LIMITED to:

  TYPE 1: Change timeout_hours (PATH A1)
    Already tested: 129, 138, 144, [check if 156 is in incumbent]
    Next untested values (in order): 156, 168, 192, 216, 240, 264, 288
    Skip any value that matches the current incumbent timeout.
    Do NOT go below 144. Do NOT exceed 300.
    ⚠️ If the incumbent has timeout=156, next to try is 168.
    ⚠️ If the incumbent has timeout=144, then 156 is still untested.

  TYPE 2: Change take_profit_pct (PATH A2)
    Already tested: 7.14, 7.38, ~8.x, 9.5, ~10.x
    Next untested values (in order): 11.0, 11.5, 12.0, 13.0, 14.0, 15.0
    Skip any value that matches the current incumbent TP.
    Do NOT go below 9.5. Do NOT use 10.0 or 10.5 (tested, inferior).
    ⚠️ If the incumbent has TP=11.0, next to try is 11.5.
    ⚠️ If the incumbent has TP=9.5, then 11.0 is still untested.

PRIORITY: Try whichever path was NOT used in Gen 15979. Both paths
are open but you should alternate: if Gen 15979 changed timeout,
try TP next. If Gen 15979 changed TP, try timeout next.

DO NOT attempt any other mutation type in the next 100 generations.
Specifically: DO NOT change any indicator period, DO NOT change
size_pct, DO NOT change stop_loss_pct, DO NOT change pairs,
DO NOT add/remove conditions, DO NOT flip momentum value.
These all lead directly to the 0.5279 dead cluster or max_trades_reject.

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
  ✓ Increasing timeout_hours above current incumbent value
  ✓ Increasing take_profit_pct above current incumbent value
  ✓ Increasing period_hours on long-side indicators only (fewer signals)
  ✓ Increasing stop_loss_pct slightly (fewer stops triggered)
    [NOTE: SL changes are frozen for 100 gens — use timeout/TP only]

DANGEROUS mutations (will likely cause [max_trades_reject] or 0.5279):
  ✗ Decreasing any period_hours
  ✗ Decreasing take_profit_pct
  ✗ Decreasing timeout_hours
  ✗ Removing any condition
  ✗ Adding a second pair
  ✗ Loosening any operator threshold
  ✗ Changing short-side indicator periods (causes 0.5279 dead cluster)
  ✗ Flipping momentum_accelerating from false to true (causes 0.5279)

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CRITICAL CONSTRAINTS — DO NOT VIOLATE THESE
## ══════════════════════════════════════════════════════════════════════

### STOP LOSS IS AT THE FLOOR — DO NOT TOUCH IT (frozen for 100 gens)
stop_loss_pct is currently 1.5%. This is the minimum allowed value.
DO NOT decrease stop_loss_pct. SL changes are NOT permitted until
timeout and TP paths are exhausted.

### TRADE COUNT IS AT THE CEILING — THIS IS THE PRIMARY CONSTRAINT
The incumbent has 60 trades — AT the hard rejection ceiling.
This is NOT "near" the ceiling. It IS the ceiling.
Any mutation that could increase trade count WILL be rejected.
Only timeout and TP changes are permitted for now.

### SIZE_PCT CAP — FROZEN
Do NOT set size_pct > 25.0%. DANGER regime directive is active.
Minimum size_pct is 10.0%. SIZE_PCT IS FROZEN.

### DO NOT ADD A 4TH CONDITION
The incumbent has 3 conditions per side. Adding a 4th will likely
drop trade count to 0 → [low_trades] rejection.

### DO NOT DECREASE TAKE_PROFIT_PCT
Decreasing TP causes faster exits → more re-entries → more trades
→ [max_trades_reject]. ONLY increase take_profit_pct.
Do NOT use TP=10.0 or TP=10.5 — already tested and inferior.

### DO NOT DECREASE TIMEOUT_HOURS
Decreasing timeout causes faster exits → more re-entries → more
trades → [max_trades_reject]. ONLY increase timeout_hours.

### DO NOT CHANGE SHORT-SIDE INDICATOR PERIODS
short bollinger period_hours = 168 — DO NOT CHANGE.
short macd period_hours = 24 — DO NOT CHANGE.
These are the primary cause of the 0.5279/57 dead cluster.

### DO NOT FLIP MOMENTUM_ACCELERATING VALUE
Both sides use value: false. Changing to value: true causes 0.5279.

## ══════════════════════════════════════════════════════════════════════
## EXAMPLE OF A VALID MUTATION (follow this format exactly)
## ══════════════════════════════════════════════════════════════════════