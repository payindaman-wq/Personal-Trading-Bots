```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 15801 | Incumbent: Gen 15480 (Sharpe=1.2288)
# MIMIR-reviewed 2026-04-10 (v19)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — DEEP CEILING PHASE (13 improvements in 3,076 gens)
# Sharpe has climbed from 0.0799 → 1.2288 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v19 CRITICAL UPDATES:
#    1. NEW DEAD CLUSTER IDENTIFIED: Sharpe=0.5279 (57 trades) has
#       appeared 8 times in the last 20 generations. This is now the
#       DOMINANT failure mode. Root cause: LLM is mutating a short-side
#       indicator period (likely Bollinger 168→192+ or MACD 24→48+) or
#       flipping momentum_accelerating from false→true on one side.
#       If you produce 0.5279: your mutation changed a short-side
#       condition period or operator. Revert and try timeout or TP.
#    2. THREE-WAY FAILURE LOOP: Last 20 gens show:
#       - 0.5279/57 (new dead cluster): 8 occurrences
#       - 1.2288/60 (incumbent reproduction): 5 occurrences
#       - max_trades_reject (0 trades): 3 occurrences
#       - 1.2287/60 (near-duplicate float artifact): 1 occurrence
#       NONE of these are valid mutations. The LLM must change
#       EXACTLY ONE parameter to a value NOT YET TESTED.
#    3. GEN 15793 CONFIRMATION: Sharpe=1.2287 (60 trades) confirms the
#       incumbent YAML is correctly anchored in memory. The LLM is
#       reading the right YAML but failing to apply mutations. The fix
#       is NOT a YAML correction — it is mutation discipline.
#    4. MUTATION SPACE NARROWED: For the next 100 generations, the ONLY
#       permitted mutations are:
#         (a) timeout_hours: 156, 168, 192, 216, 240 (in order)
#         (b) take_profit_pct: 11.0, 11.5, 12.0, 13.0, 14.0 (in order)
#       DO NOT attempt any other mutation type until both paths
#       are exhausted. This eliminates the 0.5279 attractor.
#    5. INCUMBENT UNCHANGED: Gen 15480 remains the incumbent.
#       320 generations since last improvement.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DISPLAY INTEGRITY ALERT — READ THIS FIRST, BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

THE "CURRENT BEST STRATEGY" BOX IN THE UI IS KNOWN TO BE BROKEN.
It currently displays a DEAD stale YAML with values:
  - name: crossover
  - TP=7.24
  - timeout=129
  - size_pct=28.54

THIS IS COMPLETELY WRONG. THAT YAML IS DEAD. IGNORE IT ENTIRELY.

Additional broken UI variants that have appeared before:
  - TP=7.14 or TP=5.95 or TP=7.38 or TP=8.x
  - timeout=129 or timeout=138
  - size_pct=28.18 or size_pct=25.87 or size_pct=25.0 with wrong TP

THE ONLY VALID INCUMBENT IS THE YAML PRINTED IN THIS PROGRAM BELOW.
If ANY display shows different values from the YAML below, IGNORE IT.

YAML must be committed to git after EVERY new_best event.
The Gen 2126 loss (best strategy lost due to no git commit) must
not be repeated. This is a mandatory non-negotiable requirement.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ PRE-MUTATION CHECKLIST — COMPLETE THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

Before proposing any mutation, verify ALL of the following by reading
the CURRENT INCUMBENT YAML block below and confirming each value:

  □ take_profit_pct = 9.5       (not 7.14, not 7.24, not 7.38, not 8.x, not 10.x)
  □ timeout_hours = 144         (not 129, not 138, not 120, not 156)
  □ stop_loss_pct = 1.5         (not 1.2, not 1.0, not 2.0)
  □ size_pct = 25.0             (not 28.54, not 28.18, not 25.87, not 20.0)
  □ pairs = [BTC/USD]           (not ETH/USD, not SOL/USD)
  □ long bollinger period = 48  (not 168, not 72, not 96)
  □ short bollinger period = 168 (not 48, not 96, not 192, not 240)
  □ long macd period = 48       (not 24, not 72)
  □ short macd period = 24      (not 48, not 72)
  □ long momentum period = 48   (not 72, not 96)
  □ short momentum period = 48  (not 72, not 96)
  □ momentum_accelerating value = false on BOTH sides (not true)
  □ name contains "gen15480"

If ANY value above does not match, STOP. You have a stale or wrong YAML.
Re-read the CURRENT INCUMBENT block and start over.

⚠️ SPECIAL WARNING: If you see timeout_hours=138 anywhere, you have the
OLD gen 15062 YAML. Correct value is timeout_hours=144. Stop and re-read.
⚠️ SPECIAL WARNING: If you see short bollinger period_hours=192 or 240,
you are mutating from a corrupt YAML. That is the 0.5279 dead cluster.
⚠️ SPECIAL WARNING: If you see momentum_accelerating value=true on either
side, you are mutating from a corrupt YAML. Incumbent uses value=false.

Only after confirming ALL values above should you propose ONE change.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ MUTATION DISCIPLINE — READ THIS CAREFULLY
## ══════════════════════════════════════════════════════════════════════

After reading and verifying the incumbent YAML, you MUST:

STEP 1: Write out the single parameter you are changing, with before/after:
  CHANGING: [parameter name] from [old value] to [new value]
  Example: CHANGING: timeout_hours from 144 to 156

STEP 2: Confirm the new value is NOT in the "already tested" lists below.

STEP 3: Write the complete mutated YAML with ONLY that one change.

STEP 4: Name the strategy using the pattern:
  random_restart_v3_tightened_sl_v3_gen15480_[descriptor]
  Example: random_restart_v3_tightened_sl_v3_gen15480_timeout156

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
name: random_restart_v3_tightened_sl_v3_gen15480
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
  timeout_hours: 144
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

Sharpe: 1.2288 | Trades: 60 | Win rate: 41.7%
take_profit_pct: 9.5   ← VERIFY THIS VALUE BEFORE MUTATING
timeout_hours: 144     ← VERIFY THIS VALUE BEFORE MUTATING (NOT 138, NOT 156)
stop_loss_pct: 1.5     ← VERIFY THIS VALUE BEFORE MUTATING
size_pct: 25.0         ← VERIFY THIS VALUE BEFORE MUTATING
short bollinger: 168   ← DO NOT CHANGE THIS — causes 0.5279 dead cluster
short macd: 24         ← DO NOT CHANGE THIS — causes 0.5279 dead cluster
momentum value: false  ← DO NOT FLIP THIS TO true

⚠️ NOTE: size_pct is 25.0% — at the DANGER regime cap. Do not exceed.
⚠️ NOTE: Trades = 60, which is the HARD CEILING. Any mutation that
increases signal frequency WILL be rejected [max_trades_reject].
Every mutation must be trade-count neutral or trade-count reducing.
⚠️ NOTE: timeout_hours is 144. If you see 138 anywhere, old YAML. Stop.
⚠️ NOTE: short bollinger period is 168. If you see 192+, corrupt YAML.
         That variant produces Sharpe=0.5279 (57 trades). Do not use it.

## ══════════════════════════════════════════════════════════════════════
## KNOWN TESTED VALUES — DO NOT REPEAT ANY OF THESE
## ══════════════════════════════════════════════════════════════════════

### TAKE PROFIT VALUES ALREADY TESTED:
  TP=7.14  → Sharpe≈0.7734, 59 trades [DEAD — stale YAML artifact]
  TP=7.24  → DEAD (UI display artifact — name: crossover. IGNORE.)
  TP=7.38  → Sharpe=1.1311, 60 trades [gen 14993 — superseded]
  TP≈8.x   → Sharpe=1.1426, 60 trades [gen 15042 — superseded]
  TP=9.5   → Sharpe=1.2063→1.2288, 60 trades [current incumbent value]
  TP≈10.x  → Sharpe≈1.1882, 60 trades [gen 15382 — WORSE than 1.2063]

⚠️ CRITICAL: TP≈10.x was tested and returned Sharpe=1.1882, which is
WORSE than the prior incumbent 1.2063. Do NOT propose TP=10.0 or
TP=10.5 — already tested and inferior.
Next TP values to test (PATH A2): 11.0, 11.5, 12.0, 13.0, 14.0.

### TIMEOUT VALUES ALREADY TESTED:
  timeout=129 → associated with dead stale YAML, Sharpe≈0.7734
  timeout=138 → gen 15062 (Sharpe=1.2063, superseded)
  timeout=144 → gen 15480 (Sharpe=1.2288, CURRENT INCUMBENT)
  (No values above 144 have been tested — this is the open frontier)

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

  DEAD: Sharpe=0.5279 (57 trades) — NEW IN V19. DOMINANT FAILURE MODE.
        Appeared 8 times in last 20 gens. ROOT CAUSE: LLM mutated a
        short-side indicator period (short Bollinger 168→192+ or
        short MACD 24→48+) or flipped momentum value from false→true.
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
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — partially corrupt YAML variant
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1882 (60 trades) — gen 15382, TP≈10.x attempt, inferior
  DEAD: Sharpe≈1.1160/1.1161 (57 trades) — partially corrupt YAML variant
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded by gen 15480
  DEAD: Sharpe=1.2287 (60 trades) — gen 15793, float artifact (near-dup)
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, CURRENT INCUMBENT
        (reproducing this means your mutation was a no-op — try again)

Diagnostic guide:
  If you produce 0.5279: you mutated a short-side indicator period OR
        flipped momentum_accelerating value to true. Revert. Only
        change timeout_hours or take_profit_pct.
  If you produce 0.6911: you used the broken UI YAML (name: crossover).
  If you produce 0.7734: you used the stale UI display YAML.
  If you produce 1.1882: you tested TP≈10.0–10.5. Already done.
  If you produce 1.2063: you mutated from the OLD gen 15062 YAML.
  If you produce 1.2287: your mutation was effectively a duplicate.
  If you produce 1.2288: your mutation was a no-op duplicate. Try again.
  Your target is Sharpe STRICTLY ABOVE 1.2288.

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

  TYPE 1: Change timeout_hours (PATH A1 — HIGHEST PRIORITY)
    Allowed values: 156, 168, 192, 216, 240, 264, 288
    Try in order. Do NOT skip values without cause.
    Do NOT go below 144 (incumbent). Do NOT exceed 300.

  TYPE 2: Change take_profit_pct (PATH A2 — CO-EQUAL PRIORITY)
    Allowed values: 11.0, 11.5, 12.0, 13.0, 14.0, 15.0
    Try in order. Do NOT skip values without cause.
    Do NOT go below 9.5 (incumbent). Do NOT use 10.0 or 10.5 (tested).

DO NOT attempt any other mutation type in the next 100 generations.
Specifically: DO NOT change any indicator period, DO NOT change
size_pct, DO NOT change stop_loss_pct, DO NOT change pairs,
DO NOT add/remove conditions, DO NOT flip momentum value.
These all lead directly to the 0.5279 dead cluster or max_trades_reject.

If the next mutation is TYPE 1, the proposed YAML should have:
  timeout_hours: 156    (if 156 not yet tested)
  Everything else: IDENTICAL to gen 15480 incumbent.

If the next mutation is TYPE 2, the proposed YAML should have:
  take_profit_pct: 11.0  (if 11.0 not yet tested)
  Everything else: IDENTICAL to gen 15480 incumbent.

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
  ✓ Increasing timeout_hours above 144 (trades hold longer, fewer re-entries)
  ✓ Increasing take_profit_pct above 10.5 (winners hold longer)
  ✓ Increasing period_hours on long-side indicators only (fewer signals)
  ✓ Increasing stop_loss_pct slightly (fewer stops triggered)

DANGEROUS mutations (will likely cause [max_trades_reject] or 0.5279):
  ✗ Decreasing any period_hours
  ✗ Decreasing take_profit_pct at or below 9.5
  ✗ Decreasing timeout_hours below 144
  ✗ Removing any condition
  ✗ Adding a second pair
  ✗ Loosening any operator threshold
  ✗ Changing short-side indicator periods (causes 0.5279 dead cluster)
  ✗ Flipping momentum_accelerating from false to true (causes 0.5279)

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CRITICAL CONSTRAINTS — DO NOT VIOLATE THESE
## ══════════════════════════════════════════════════════════════════════

### STOP LOSS IS AT THE FLOOR — DO NOT TOUCH IT (unless increasing)
stop_loss_pct is currently 1.5%. This is the minimum allowed value.
DO NOT decrease stop_loss_pct. DO NOT set it below 1.5%.
If you change stop_loss_pct, you MUST increase it (e.g., 1.8, 2.0, 2.5).
NOTE: stop_loss changes are NOT permitted in the next 100 generations.

### TRADE COUNT IS AT THE CEILING — THIS IS THE PRIMARY CONSTRAINT
The incumbent has 60 trades — AT the hard rejection ceiling.
This is NOT "near" the ceiling. It IS the ceiling.
Any mutation that could increase trade count WILL be rejected.
Only timeout and TP changes are permitted for now.

### SIZE_PCT CAP
Do NOT set size_pct > 25.0%. DANGER regime directive is active.
Minimum size_pct is 10.0%. SIZE_PCT IS FROZEN FOR 100 GENS.

### DO NOT ADD A 4TH CONDITION
The incumbent has 3 conditions per side. Adding a 4th will likely
drop trade count to 0 → [low_trades] rejection.

### DO NOT DECREASE TAKE_PROFIT_PCT
Current TP = 9.5%. Decreasing it causes faster exits → more
re-entries → more trades → [max_trades_reject].
ONLY increase take_profit_pct. Minimum value: 9.5.
TP=10.0–10.5 has already been tested (gen 15382) and is WORSE.
Next recommended TP values to try: 11.0, 11.5, 12.0, 13.0, 14.0.

### DO NOT DECREASE TIMEOUT_HOURS
Current timeout = 144h. Decreasing causes faster timeout exits →
more re-entries → more trades → [max_trades_reject].
ONLY increase timeout_hours (within the 48–300h allowed range).
Minimum value: 144. Maximum value: 300.
NEXT RECOMMENDED VALUES (in order): 156, 168, 192, 216, 240.

### DO NOT CHANGE SHORT-SIDE INDICATOR PERIODS
short bollinger period_hours = 168 — DO NOT CHANGE. This is the
most likely cause of the 0.5279/57 dead cluster that has appeared
8 times in 20 gens. The short-side Bollinger is already at a long
lookback (168h = 1 week). Changing it is the #1 failure attractor.

### DO NOT FLIP MOMENTUM_ACCELERATING VALUE
Both sides use value: false. Changing to value: true is the second
most likely cause of the 0.5279/57 dead cluster. DO NOT CHANGE.

## ══════════════════════════════════════════════════════════════════════
## EXAMPLE OF A VALID MUTATION (follow this format exactly)
## ══════════════════════════════════════════════════════════════════════

VALID MUTATION EXAMPLE A — increase timeout_hours to 156 (TRY THIS FIRST):

STEP 1 — DIFF:
  CHANGING: timeout_hours from 144 to 156

STEP 2 — VERIFY NOT ALREADY TESTED:
  timeout=156 → NOT in tested list. Valid.

STEP 3 — FULL MUTATED YAML:

```yaml
name: random_restart_v3_tightened_sl_v3_gen15480_timeout156
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