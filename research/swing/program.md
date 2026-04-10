```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 15601 | Incumbent: Gen 15480 (Sharpe=1.2288)
# MIMIR-reviewed 2026-04-10 (v18)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — DEEP CEILING PHASE (13 improvements in 2,876 gens)
# Sharpe has climbed from 0.0799 → 1.2288 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v18 CRITICAL UPDATES:
#    1. NEW INCUMBENT: Gen 15480 achieved Sharpe=1.2288 (up from 1.2063).
#       The program was NOT updated after this event — now corrected.
#       The YAML below reflects gen 15480. DO NOT use gen 15062 values.
#    2. DUPLICATE LOOP DETECTED: Last 20 gens show Sharpe=1.2288
#       appearing 6 times as [discarded]. The small LLM is reproducing
#       the incumbent instead of mutating it. This means the YAML anchor
#       is correct but mutations are not being applied. READ the mutation
#       instructions carefully and change EXACTLY ONE parameter.
#    3. NEW DEAD CLUSTER: Sharpe=0.6911 (57 trades) — seen 4 times in
#       last 20 gens. Caused by small LLM reading the broken UI YAML
#       (name: crossover, TP=7.24, timeout=129, size_pct=28.54).
#       IGNORE THE UI. USE ONLY THE YAML IN THIS PROGRAM.
#    4. INCUMBENT TIMEOUT LIKELY = 144h: Gen 15480's improvement is
#       consistent with timeout escalation from 138→144 (PATH A1).
#       If confirmed, the next test in sequence is timeout=156h.
#    5. STALL WARNING: 120 generations since last improvement (gen 15480).
#       The duplicate-reproduction loop is the primary blocker.
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
  □ timeout_hours = 144         (not 129, not 138, not 120)
  □ stop_loss_pct = 1.5         (not 1.2, not 1.0, not 2.0)
  □ size_pct = 25.0             (not 28.54, not 28.18, not 25.87, not 20.0)
  □ pairs = [BTC/USD]           (not ETH/USD, not SOL/USD)
  □ long bollinger period = 48  (not 168, not 72)
  □ short bollinger period = 168 (not 48, not 96)
  □ long macd period = 48       (not 24)
  □ short macd period = 24      (not 48)
  □ name contains "gen15480"

If ANY value above does not match, STOP. You have a stale or wrong YAML.
Re-read the CURRENT INCUMBENT block and start over.

⚠️ SPECIAL WARNING: If you see timeout_hours=138 in the YAML you are
reading, you have the OLD gen 15062 YAML. It is outdated. The correct
value is timeout_hours=144. Stop and re-read the block below.

Only after confirming all values above should you propose ONE change.

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
timeout_hours: 144     ← VERIFY THIS VALUE BEFORE MUTATING (NOT 138)
stop_loss_pct: 1.5     ← VERIFY THIS VALUE BEFORE MUTATING
size_pct: 25.0         ← VERIFY THIS VALUE BEFORE MUTATING

⚠️ NOTE: size_pct is 25.0% — at the DANGER regime cap. Do not exceed.
⚠️ NOTE: Trades = 60, which is the HARD CEILING. Any mutation that
increases signal frequency WILL be rejected [max_trades_reject].
Every mutation must be trade-count neutral or trade-count reducing.
⚠️ NOTE: timeout_hours is NOW 144, not 138. If you see 138 anywhere,
you are reading an old YAML. Stop and re-read this block.

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

⚠️ CRITICAL: TP≈10.x was tested (gen 15382) and returned Sharpe=1.1882,
which is WORSE than the prior incumbent 1.2063. Simple TP escalation
above 9.5 has already been shown to HURT performance at 10.x.
Do NOT propose TP=10.0 or TP=10.5 — already tested and inferior.
Next TP values to test (if pursuing PATH A2): 11.0, 11.5, 12.0, 13.0.

### TIMEOUT VALUES ALREADY TESTED:
  timeout=129 → associated with dead stale YAML, Sharpe≈0.7734
  timeout=138 → gen 15062 (Sharpe=1.2063, superseded)
  timeout=144 → gen 15480 (Sharpe=1.2288, CURRENT INCUMBENT)
  (No values above 144 have been tested yet — this is the open frontier)

### STOP LOSS VALUES ALREADY TESTED:
  SL=1.5 → CURRENT INCUMBENT value

### DEAD CLUSTERS — SHARPE VALUES THAT INDICATE SOMETHING WENT WRONG:
  DEAD: Sharpe≈0.7734 (59 trades) — stale YAML (TP=7.14, timeout=129,
        size_pct=28.18). ROOT CAUSE: reading broken UI.
  DEAD: Sharpe=0.6911 (57 trades) — NEW IN V18. Seen 4 times in
        last 20 gens. ROOT CAUSE: reading the broken UI YAML
        (name: crossover, TP=7.24, timeout=129, size_pct=28.54).
        If you see this, you used the WRONG base YAML. Fix it.
  DEAD: Sharpe=0.5954 (58 trades) — slightly wrong YAML variant.
        If you see this, your base YAML had incorrect parameters.
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
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, CURRENT INCUMBENT
        (reproducing this means your mutation was a no-op — try again)

If you produce 0.6911: you used the broken UI YAML (name: crossover). Fix it.
If you produce 0.7734: you used the stale UI display YAML. Fix it.
If you produce 1.1882: you tested TP≈10.0–10.5. Already done.
If you produce 1.2063: you mutated from the OLD gen 15062 YAML. Fix it.
If you produce 1.2288: your mutation was a duplicate. Try again.
Your target is Sharpe STRICTLY ABOVE 1.2288.

## ══════════════════════════════════════════════════════════════════════
## CRITICAL INSTRUCTION — READ THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

You MUST propose exactly ONE small change to the CURRENT INCUMBENT YAML
above. Do NOT generate a new strategy from scratch. Do NOT change more
than one parameter at a time. Do NOT use any older YAML versions.
Do NOT use the UI "Current Best Strategy" display — it shows
"name: crossover" with WRONG values. It is broken. Ignore it.

A "small change" means ONE of the following:
  (a) Change one numeric value (e.g., period_hours, take_profit_pct,
      stop_loss_pct, timeout_hours, size_pct)
  (b) Change one condition's operator or value
  (c) Replace one condition with a different indicator
  (d) Add one pair (ETH/USD or SOL/USD) alongside BTC/USD
  (e) Remove one condition (if currently 3 conditions)
  (f) Change one exit parameter

DO NOT: replace all conditions, change pairs and conditions
simultaneously, add more than one new condition, or generate a
completely different strategy.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ THE MOST IMPORTANT CONSTRAINT RIGHT NOW
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
  ✓ Increasing period_hours on any indicator (fewer signals)
  ✓ Increasing stop_loss_pct slightly (fewer stops triggered)
  ✓ Replacing momentum_accelerating with RSI (may reduce signal count)

DANGEROUS mutations (will likely cause [max_trades_reject]):
  ✗ Decreasing any period_hours
  ✗ Decreasing take_profit_pct at or below 9.5
  ✗ Decreasing timeout_hours below 144
  ✗ Removing any condition
  ✗ Adding a second pair
  ✗ Loosening any operator threshold

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CRITICAL CONSTRAINTS — DO NOT VIOLATE THESE
## ══════════════════════════════════════════════════════════════════════

### STOP LOSS IS AT THE FLOOR — DO NOT TOUCH IT (unless increasing)
stop_loss_pct is currently 1.5%. This is the minimum allowed value.
DO NOT decrease stop_loss_pct. DO NOT set it below 1.5%.
If you change stop_loss_pct, you MUST increase it (e.g., 1.8, 2.0, 2.5).

### TRADE COUNT IS AT THE CEILING — THIS IS THE PRIMARY CONSTRAINT
The incumbent has 60 trades — AT the hard rejection ceiling.
This is NOT "near" the ceiling. It IS the ceiling.
Any mutation that could increase trade count WILL be rejected.
Prefer mutations with high confidence of reducing trade count.

### SIZE_PCT CAP
Do NOT set size_pct > 25.0%. DANGER regime directive is active.
Minimum size_pct is 10.0%.

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
(144 is the incumbent — do not reproduce it, do not go below it.)

## ══════════════════════════════════════════════════════════════════════
## EXAMPLE OF A VALID MUTATION (follow this format exactly)
## ══════════════════════════════════════════════════════════════════════

VALID MUTATION EXAMPLE A — increase timeout_hours to 156:

BASE (incumbent, gen 15480):
  exit:
    take_profit_pct: 9.5    ← unchanged
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 144      ← current value

MUTATED:
  exit:
    take_profit_pct: 9.5    ← unchanged
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 156      ← changed from 144 to 156

Name: random_restart_v3_tightened_sl_v3_gen15480_timeout156

Everything else in the YAML stays exactly the same.

---

VALID MUTATION EXAMPLE B — increase take_profit_pct to 11.0:

BASE (incumbent, gen 15480):
  exit:
    take_profit_pct: 9.5    ← current value
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 144      ← unchanged

MUTATED:
  exit:
    take_profit_pct: 11.0   ← changed from 9.5, skipping 10.0–10.5
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 144      ← unchanged

Name: random_restart_v3_tightened_sl_v3_gen15480_tp11

Note: TP=10.0–10.5 was already tested (gen 15382, Sharpe=1.1882,
WORSE than prior incumbent). Skip those values. Start at 11.0.

---

VALID MUTATION EXAMPLE C — extend long Bollinger period:

BASE (incumbent, gen 15480):
  entry:
    long:
      - indicator: bollinger_position
        period_hours: 48    ← current value

MUTATED:
  entry:
    long:
      - indicator: bollinger_position
        period_hours: 72    ← changed from 48 to 72

Name: random_restart_v3_tightened_sl_v3_gen15480_boll72

Note: Longer period = fewer below_lower signals = fewer long entries.
This may reduce trades below 60, creating room for further tuning.

## ══════════════════════════════════════════════════════════════════════
## RESEARCH DIRECTION (v18)
## ══════════════════════════════════════════════════════════════════════

### CONTEXT: WHERE WE ARE
The strategy has a clear identity: low win rate (41.7%), asymmetric payoff.
- SL = 1.5% (floor — do not reduce further)
- TP = 9.5% → reward:risk ratio ≈ 6.3:1
- timeout = 144h (recently improved from 138h at gen 15480)
- Trades = 60 (AT THE HARD CEILING)
- 120 generations since last improvement (gen 15480)
- The last 20 gens show a duplicate-reproduction loop (1.2288 appearing
  6 times as [discarded]) — the LLM anchors correctly but doesn't mutate.
- New dead cluster: 0.6911/57 trades (broken UI YAML contamination).
- Timeout escalation to 144h improved Sharpe. Continuing this path is
  the highest priority. Values 156h+ have never been tested.

### PATH A1 — INCREASE TIMEOUT_HOURS (HIGHEST PRIORITY — OPEN FRONTIER)

timeout=144h just improved Sharpe from 1.2063 → 1.2288. This confirms
the timeout escalation path is LIVE and productive. Continue escalating.

Try these values IN ORDER, one per generation:
  - timeout_hours: 156   ← TRY THIS FIRST — next increment after 144
  - timeout_hours: 168   ← 1 week — natural swing trading boundary
  - timeout_hours: 192
  - timeout_hours: 216
  - timeout_hours: 240
  - timeout_hours: 264
  - timeout_hours: 288

DO NOT go below 144h (will increase trade count or reproduce incumbent).
DO NOT go above 300h (program hard limit).
DO NOT change any other parameter when testing timeout.

If timeout=156 improves Sharpe: keep it, then test timeout=168, etc.
If timeout=156 is worse: try timeout=168 (non-monotonic behavior possible).
If all timeout values tested up to 240 show no improvement: move to PATH A2.

### PATH A2 — INCREASE TAKE_PROFIT_PCT ABOVE 10.5 (CO-EQUAL PRIORITY)

⚠️ IMPORTANT: TP=10.0–10.5 has already been tested (gen 15382, Sharpe=1.1882,
WORSE than prior incumbent 1.2063). Do NOT propose TP=10.0 or TP=10.5.
There may be a local dip at TP=10.x. The curve may recover at 11.0+.

Try these values IN ORDER, one per generation, starting at 11.0:
  - take_profit_pct: 11.0   ← skip 10.0–10.5, start here
  - take_profit_pct: 11.5
  - take_profit_pct: 12.0
  - take_profit_pct: 13.0
  - take_profit_pct: 14.0
  - take_profit_pct: 15.0

Upper limit consideration: TP above 15% may become unreachable in
practice, causing most trades to timeout rather than hit TP. If
win rate drops below 30% or trades drop below 30, TP has overshot.

DO NOT propose TP values at or below 9.5.
DO NOT propose TP=10.0 or TP=10.5 — already tested and inferior.

### PATH A3 — COMBINED TIMEOUT + TP ESCALATION (SECONDARY)
Once a better timeout is found (e.g., timeout=168 improves Sharpe),
test that timeout value COMBINED with higher TP values.
Only test combinations after both individual paths have been explored.
Do NOT test combinations prematurely — change ONE parameter at a time.

### PATH B — BOLLINGER PERIOD EXTENSION (TERTIARY)

Longer Bollinger lookback → fewer signals → fewer long entries →
trade count may drop below 60 (creating room for further mutations).

  - Long side bollinger_position period_hours: 72 (currently 48)
  - Long side bollinger_position period_hours: 96
  - Long side bollinger_position period_hours: 120

Do NOT change the short-side Bollinger (period_hours: 168 — already long).
Try only if PATH A1 and A2 both stall for 100+ gens with no improvements.

### PATH C — MOMENTUM PERIOD EXTENSION (QUATERNARY)

  - momentum_accelerating period_hours: 72 (long side, currently 48)
  - momentum_accelerating period_hours: 96 (long side)

Longer period = fewer momentum signals = fewer entries = trade count
may drop below 60. Try only if PATH A and B stall.

### PATH D — REPLACE MOMENTUM_ACCELERATING WITH RSI

If TP and timeout tuning stall for 200+ gens with no improvements:
  Long: replace momentum_accelerating=false with
    indicator: rsi, period_hours: 48, operator: lt, value: 35
  Short: replace momentum_accelerating=false with
    indicator: rsi, period_hours: 48, operator: gt, value: 65

RSI is more predictable. Tighter RSI thresholds (35/65) should
maintain or reduce trade count vs. the current setup.
DO NOT use looser thresholds (e.g., RSI < 45 or > 55) — too many trades.
DO NOT change any other conditions when making this swap.

### PATH E — SLIGHT stop_loss_pct INCREASE (MINOR)
SL is at the floor (1.