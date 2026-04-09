```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 15401 | Incumbent: Gen 15062 (Sharpe=1.2063)
# MIMIR-reviewed 2026-04-09 (v17)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — DEEP CEILING PHASE (12 improvements in 2,676 gens)
# Sharpe has climbed from 0.0799 → 1.2063 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v17 CRITICAL UPDATES:
#    1. STALL CONFIRMED: 339 generations since last improvement (gen 15062).
#    2. NEW DEAD CLUSTER: Sharpe=0.5954 (58 trades) — seen 9 times in
#       last 20 gens. Now added to the dead cluster list. This is likely
#       caused by a stale YAML with slightly wrong parameters.
#    3. TP ESCALATION WARNING: Gen 15382 returned Sharpe=1.1882 (60 trades),
#       which is WORSE than the incumbent 1.2063. This means TP values
#       around 10.0–10.5 have been tested implicitly and are inferior.
#       TP escalation alone is no longer the clear primary path.
#    4. PIVOT: timeout_hours escalation is now CO-EQUAL PRIORITY with TP.
#    5. NEW: Pre-mutation checklist added (mandatory — read before mutating).
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DISPLAY INTEGRITY ALERT — READ THIS FIRST, BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

THE "CURRENT BEST STRATEGY" BOX IN THE UI IS KNOWN TO BE BROKEN.
It may display an old YAML with values such as:
  - name: crossover
  - TP=7.14 or TP=5.95 or TP=7.38 or TP=8.x
  - timeout=129 or timeout=138 (note: 138 IS correct for incumbent)
  - size_pct=28.18 or size_pct=25.87 or size_pct=25.0

The UI box showing size_pct=28.18 and TP=7.14 is DEAD. IGNORE IT.
The UI box showing size_pct=25.0 and TP=7.38 is ALSO DEAD. IGNORE IT.

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

  □ take_profit_pct = 9.5       (not 7.14, not 7.38, not 8.x, not 10.x)
  □ timeout_hours = 138         (not 129, not 120, not 144)
  □ stop_loss_pct = 1.5         (not 1.2, not 1.0, not 2.0)
  □ size_pct = 25.0             (not 28.18, not 25.87, not 20.0)
  □ pairs = [BTC/USD]           (not ETH/USD, not SOL/USD)
  □ long bollinger period = 48  (not 168, not 72)
  □ short bollinger period = 168 (not 48, not 96)
  □ long macd period = 48       (not 24)
  □ short macd period = 24      (not 48)
  □ name contains "gen15062"

If ANY value above does not match, STOP. You have a stale or wrong YAML.
Re-read the CURRENT INCUMBENT block and start over.

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
## THE UI DISPLAY IS BROKEN AND SHOWS STALE DATA. IGNORE IT.
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3_gen15062
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
  timeout_hours: 138
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

Sharpe: 1.2063 | Trades: 60 | Win rate: 41.7%
take_profit_pct: 9.5   ← VERIFY THIS VALUE BEFORE MUTATING
timeout_hours: 138     ← VERIFY THIS VALUE BEFORE MUTATING
stop_loss_pct: 1.5     ← VERIFY THIS VALUE BEFORE MUTATING
size_pct: 25.0         ← VERIFY THIS VALUE BEFORE MUTATING

⚠️ NOTE: size_pct is 25.0% — at the DANGER regime cap. Do not exceed.
⚠️ NOTE: Trades = 60, which is the HARD CEILING. Any mutation that
increases signal frequency WILL be rejected [max_trades_reject].
Every mutation must be trade-count neutral or trade-count reducing.

## ══════════════════════════════════════════════════════════════════════
## KNOWN TESTED VALUES — DO NOT REPEAT ANY OF THESE
## ══════════════════════════════════════════════════════════════════════

### TAKE PROFIT VALUES ALREADY TESTED:
  TP=7.14  → Sharpe≈0.7734, 59 trades [DEAD — stale YAML artifact]
  TP=7.38  → Sharpe=1.1311, 60 trades [gen 14993 — superseded]
  TP≈8.x   → Sharpe=1.1426, 60 trades [gen 15042 — superseded]
  TP=9.5   → Sharpe=1.2063, 60 trades [gen 15062 — CURRENT INCUMBENT]
  TP≈10.x  → Sharpe≈1.1882, 60 trades [gen 15382 — WORSE than incumbent]

⚠️ CRITICAL: TP≈10.x was tested (gen 15382) and returned Sharpe=1.1882,
which is WORSE than the incumbent 1.2063. This means simple TP
escalation above 9.5 has already been shown to HURT performance.
Do NOT blindly continue TP escalation without also testing other paths.

If testing higher TP values, skip 10.0–10.5 (already inferior) and
jump to: 11.0, 11.5, 12.0, 13.0, 14.0 — these may clear the 10.x dip.
But timeout escalation is now the HIGHER PRIORITY path.

### TIMEOUT VALUES ALREADY TESTED:
  timeout=129 → associated with dead stale YAML, Sharpe≈0.7734
  timeout=138 → CURRENT INCUMBENT (Sharpe=1.2063)
  (No values above 138 have been tested yet — this is the open frontier)

### STOP LOSS VALUES ALREADY TESTED:
  SL=1.5 → CURRENT INCUMBENT

## ══════════════════════════════════════════════════════════════════════
## CRITICAL INSTRUCTION — READ THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

You MUST propose exactly ONE small change to the CURRENT INCUMBENT YAML
above. Do NOT generate a new strategy from scratch. Do NOT change more
than one parameter at a time. Do NOT use any older YAML versions.
Do NOT use the UI "Current Best Strategy" display — it is broken.

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
  ✓ Increasing timeout_hours above 138 (trades hold longer, fewer re-entries)
  ✓ Increasing take_profit_pct above 10.5 (winners hold longer)
  ✓ Increasing period_hours on any indicator (fewer signals)
  ✓ Increasing stop_loss_pct slightly (fewer stops triggered)
  ✓ Replacing momentum_accelerating with RSI (may reduce signal count)

DANGEROUS mutations (will likely cause [max_trades_reject]):
  ✗ Decreasing any period_hours
  ✗ Decreasing take_profit_pct at or below 9.5
  ✗ Decreasing timeout_hours below 138
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
TP=10.0–10.5 has already been implicitly tested and is worse.
Next recommended TP values to try: 11.0, 11.5, 12.0, 13.0, 14.0.

### DO NOT DECREASE TIMEOUT_HOURS
Current timeout = 138h. Decreasing causes faster timeout exits →
more re-entries → more trades → [max_trades_reject].
ONLY increase timeout_hours (within the 48–300h allowed range).
Minimum value: 138. Maximum value: 300.
NEXT RECOMMENDED VALUES (in order): 144, 156, 168, 192, 216, 240.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CLUSTERING ALERT — DO NOT REPRODUCE THESE KNOWN SHARPE VALUES
## ══════════════════════════════════════════════════════════════════════

The following Sharpe values are CONFIRMED DEAD ENDS.
If your mutation produces any of these values, something went wrong.

  DEAD: Sharpe≈0.7734 (59 trades) — caused by stale YAML (TP=7.14,
        timeout=129, size_pct=28.18). ROOT CAUSE: reading broken UI.
        USE ONLY THE YAML PRINTED IN THIS PROGRAM.

  DEAD: Sharpe=0.5954 (58 trades) — NEW IN V17. Seen 9 times in
        last 20 generations. Likely caused by a slightly wrong YAML
        variant (possibly TP or period_hours slightly off from incumbent).
        If you see this result, your base YAML was incorrect.
        STOP and re-read the CURRENT INCUMBENT block above.

  DEAD: Sharpe≈1.0182 (60 trades) — dead end
  DEAD: Sharpe≈1.0325 (57 trades) — dead end
  DEAD: Sharpe≈1.0642 (56 trades) — plateau from gen 14784
  DEAD: Sharpe≈1.0952 (57 trades) — seen twice recently, dead end
  DEAD: Sharpe≈1.1090 (60 trades) — dead end
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1882 (60 trades) — gen 15382, TP escalation
        attempt that came back WORSE than incumbent. This means TP
        values around 10.0–10.5 are INFERIOR to 9.5.
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, CURRENT INCUMBENT
        (do not reproduce — it means your mutation was a no-op)

If you produce 0.5954: your base YAML was wrong. Fix it.
If you produce 0.7734: you used the stale UI display YAML. Fix it.
If you produce 1.1882: you tested TP≈10.0–10.5. Already done.
If you produce 1.2063: your mutation was a duplicate. Try again.
Your target is Sharpe STRICTLY ABOVE 1.2063.

## ══════════════════════════════════════════════════════════════════════
## EXAMPLE OF A VALID MUTATION (follow this format exactly)
## ══════════════════════════════════════════════════════════════════════

VALID MUTATION EXAMPLE A — increase timeout_hours to 144:

BASE (incumbent, gen 15062):
  exit:
    take_profit_pct: 9.5    ← unchanged
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 138      ← current value

MUTATED:
  exit:
    take_profit_pct: 9.5    ← unchanged
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 144      ← changed from 138 to 144

Name: random_restart_v3_tightened_sl_v3_gen15062_timeout144

Everything else in the YAML stays exactly the same.

---

VALID MUTATION EXAMPLE B — increase take_profit_pct to 11.0:

BASE (incumbent, gen 15062):
  exit:
    take_profit_pct: 9.5    ← current value
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 138      ← unchanged

MUTATED:
  exit:
    take_profit_pct: 11.0   ← changed from 9.5, skipping 10.0–10.5
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 138      ← unchanged

Name: random_restart_v3_tightened_sl_v3_gen15062_tp11

Note: TP=10.0–10.5 was already tested (gen 15382, Sharpe=1.1882,
WORSE than incumbent). Skip those values. Start at 11.0.

## ══════════════════════════════════════════════════════════════════════
## RESEARCH DIRECTION (v17)
## ══════════════════════════════════════════════════════════════════════

### CONTEXT: WHERE WE ARE
The strategy has a clear identity: low win rate (41.7%), asymmetric payoff.
- SL = 1.5% (floor — do not reduce further)
- TP = 9.5% → reward:risk ratio ≈ 6.3:1
- Trades = 60 (AT THE HARD CEILING)
- 339 generations without improvement — deep stall
- TP escalation to 10.x was tested (gen 15382) and returned Sharpe=1.1882,
  which is WORSE than 1.2063. Simple TP escalation is no longer reliable.
- timeout_hours has NEVER been escalated above 138. This is the open frontier.

### PATH A1 — INCREASE TIMEOUT_HOURS (HIGHEST PRIORITY — UNTESTED FRONTIER)

This path has NEVER been explored. It is the highest-expected-value mutation.
Longer timeout allows trades to breathe, reduces timeout-based exits,
and may convert some timeout losers into TP winners.

Try these values IN ORDER, one per generation:
  - timeout_hours: 144   ← TRY THIS FIRST — smallest safe increment
  - timeout_hours: 156
  - timeout_hours: 168   ← 1 week — natural swing trading boundary
  - timeout_hours: 192
  - timeout_hours: 216
  - timeout_hours: 240
  - timeout_hours: 264
  - timeout_hours: 288

DO NOT go below 138h (will increase trade count).
DO NOT go above 300h (program hard limit).
DO NOT change any other parameter when testing timeout.

If timeout=144 improves Sharpe: keep it, then test timeout=156, etc.
If timeout=144 is worse: try timeout=156 (non-monotonic behavior possible).
If all timeout values tested up to 240 show no improvement: move to PATH A2.

### PATH A2 — INCREASE TAKE_PROFIT_PCT ABOVE 10.5 (CO-EQUAL PRIORITY)

⚠️ IMPORTANT: TP=10.0–10.5 has already been tested implicitly (gen 15382
returned 1.1882). Do NOT propose TP values of 10.0 or 10.5.
There may be a local minimum at TP=10.x. The curve may recover at 11.0+.

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
SL is at the floor (1.5%). A small increase may:
  - Reduce the number of stops triggered → slightly fewer trades
  - Improve win rate by giving trades more room
  Test: stop_loss_pct: 1.8, then 2.0, then 2.5
  Risk: wider SL reduces per-trade risk-adjusted return.
  Only test if PATH A–D all fail to produce improvements.

### PATH F — size_pct (DO NOT TOUCH IN DANGER REGIME)
  size_pct is at 25.0% (DANGER cap). Do not increase above 25.0%.
  Do not touch until macro regime improves (F&G > 30).

### PATH G — RSI+MACD+EMA RECONSTRUCTION (LAST RESORT)
Only attempt if ALL paths above stall for 400+ consecutive gens with
zero improvements. The all-time benchmark (Sharpe=2.9232) used this.
Template:
  Long: RSI < 35, MACD bullish, price > EMA(period=50)
  Short: RSI > 65, MACD bearish, price < EMA(period=50)
  Exit: TP=9.5%, SL=1.5%, timeout=138h (match current exit structure)
  Pairs: BTC/USD only first
  This is a full indicator swap — last resort only.

## ══════════════════════════════════════════════════════════════════════
## WHAT HAS FAILED — DO NOT REPEAT
## ══════════════════════════════════════════════════════════════════