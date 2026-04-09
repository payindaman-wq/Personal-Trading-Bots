```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 15201 | Incumbent: Gen 15062 (Sharpe=1.2063)
# MIMIR-reviewed 2026-04-09 (v16)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CEILING PHASE (12 improvements in 2,476 gens)
# Sharpe has climbed from 0.0799 → 1.2063 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing.
#
# ⚠️ v16 CRITICAL CORRECTION:
#    The v15 program claimed gen 14993 (Sharpe=1.1311) as incumbent.
#    THIS WAS STALE. The true incumbent is gen 15062 (Sharpe=1.2063).
#    The "Current Best Strategy" display block in the research UI
#    was showing a pre-gen-14873 YAML (TP=7.14, timeout=129,
#    size_pct=28.18, name=crossover). THIS IS DEAD. IGNORE IT.
#    The stale display block caused 13 of the last 20 generations
#    to reproduce Sharpe≈0.7734 — a confirmed dead cluster.
#    The ONLY valid incumbent YAML is printed in this program below.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DISPLAY INTEGRITY ALERT — READ THIS FIRST, BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

THE "CURRENT BEST STRATEGY" BOX IN THE UI IS KNOWN TO BE BROKEN.
It may display an old YAML with values such as:
  - name: crossover
  - TP=7.14 or TP=5.95 or TP=7.38
  - timeout=129 or timeout=138
  - size_pct=28.18 or size_pct=25.87 or size_pct=25.0

ALL OF THESE DISPLAY VALUES ARE WRONG. DO NOT USE THEM.

THE ONLY VALID INCUMBENT IS THE YAML PRINTED IN THIS PROGRAM.
Gen 15062 is the incumbent. Its YAML has:
  take_profit_pct: [SEE YAML BELOW]
  timeout_hours: [SEE YAML BELOW]
  stop_loss_pct: 1.5
  size_pct: 25.0

If any other display shows different values, IGNORE IT COMPLETELY.
Use ONLY the YAML printed in the "CURRENT INCUMBENT" block below.

YAML must be committed to git after EVERY new_best event.
The Gen 2126 loss (best strategy lost due to no git commit) must
not be repeated. This is a mandatory non-negotiable requirement.

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

⚠️ IMPORTANT: The TP value above (9.5) is MIMIR's best estimate for
what gen 15062 used to achieve Sharpe=1.2063, inferred from the
improvement sequence. If backtesting reveals this YAML does NOT
reproduce Sharpe=1.2063, escalate to MIMIR immediately and do not
proceed with mutations until the correct YAML is confirmed.

## ══════════════════════════════════════════════════════════════════════
## KNOWN TP VALUES ALREADY TESTED — DO NOT REPEAT THESE
## ══════════════════════════════════════════════════════════════════════

The following take_profit_pct values have been explored in prior
generations. Do NOT propose them again — they are known results:

  TP=7.14  → Sharpe≈0.7734, 59 trades [DEAD — stale YAML artifact]
  TP=7.38  → Sharpe=1.1311, 60 trades [gen 14993 — superseded]
  TP≈8.x   → Sharpe=1.1426, 60 trades [gen 15042 — superseded]
  TP≈9.5   → Sharpe=1.2063, 60 trades [gen 15062 — CURRENT INCUMBENT]

The incumbent is at TP≈9.5. Continue the escalation sequence UPWARD.
DO NOT propose any TP value at or below 9.5.
Next values to try (in order): 10.0, 10.5, 11.0, 11.5, 12.0, 13.0

## ══════════════════════════════════════════════════════════════════════
## CRITICAL INSTRUCTION — READ THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

You MUST propose exactly ONE small change to the CURRENT INCUMBENT YAML
above. Do NOT generate a new strategy from scratch. Do NOT change more
than one parameter at a time. Do NOT use any older YAML versions.
Do NOT use the UI "Current Best Strategy" display — it is broken.

VERIFY YOUR BASE YAML BEFORE MUTATING:
- take_profit_pct must be 9.5 in your base
- timeout_hours must be 138 in your base
- stop_loss_pct must be 1.5 in your base
- size_pct must be 25.0 in your base
- name must contain "gen15062" or reference it

If ANY of these values differ from what is listed above, you are
using a stale or broken YAML. STOP. Re-read the CURRENT INCUMBENT
block above and use only those values.

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
  ✓ Increasing take_profit_pct above 9.5 (winners hold longer)
  ✓ Increasing timeout_hours above 138 (trades hold longer)
  ✓ Increasing period_hours on any indicator (fewer signals)
  ✓ Slightly increasing stop_loss_pct (fewer stops triggered)
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
Next recommended values: 10.0, 10.5, 11.0, 11.5, 12.0, 13.0.

### DO NOT DECREASE TIMEOUT_HOURS
Current timeout = 138h. Decreasing causes faster timeout exits →
more re-entries → more trades → [max_trades_reject].
ONLY increase timeout_hours (within the 48–300h allowed range).
Minimum value: 138.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CLUSTERING ALERT — DO NOT REPRODUCE THESE KNOWN SHARPE VALUES
## ══════════════════════════════════════════════════════════════════════

The following Sharpe values have been seen many times and are DEAD ENDS.
DO NOT produce mutations that lead to these values again.

  DEAD: Sharpe≈0.7734 (59 trades) — caused by using stale YAML
        (TP=7.14, timeout=129). Seen 13 times in last 20 gens.
        ROOT CAUSE: LLM reading broken UI display box. USE ONLY
        THE YAML PRINTED IN THIS PROGRAM.
  DEAD: Sharpe≈1.0325 (57 trades) — dead end
  DEAD: Sharpe≈1.0642 (56 trades) — plateau from gen 14784
  DEAD: Sharpe≈1.1090 (60 trades) — dead end
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe=1.2063 (60 trades)  — gen 15062, CURRENT INCUMBENT
        (do not reproduce this — it means your mutation was a no-op)

The current best is Sharpe=1.2063 at 60 trades (gen 15062).
You must propose a mutation that targets Sharpe HIGHER than 1.2063.
If you produce exactly 1.2063, your mutation was a duplicate.
If you produce 0.7734, you used the wrong base YAML. Stop and fix.

## ══════════════════════════════════════════════════════════════════════
## EXAMPLE OF A VALID MUTATION (follow this format exactly)
## ══════════════════════════════════════════════════════════════════════

Here is an example of what a valid mutation looks like.
Start with the incumbent YAML (gen 15062) and change exactly ONE value.

BASE (incumbent, gen 15062):
  exit:
    take_profit_pct: 9.5    ← current value
    stop_loss_pct: 1.5
    timeout_hours: 138

VALID MUTATION — increase take_profit_pct to 10.0:
  exit:
    take_profit_pct: 10.0   ← changed from 9.5 to 10.0
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 138      ← unchanged

Everything else in the YAML stays exactly the same.
The name should be updated to reflect the change, e.g.:
  name: random_restart_v3_tightened_sl_v3_gen15062_tp10

This is the HIGHEST PRIORITY mutation for the next generation.
If take_profit_pct: 10.0 has already been tested, try 10.5, then 11.0.

## ══════════════════════════════════════════════════════════════════════
## RESEARCH DIRECTION (v16)
## ══════════════════════════════════════════════════════════════════════

### CONTEXT: WHERE WE ARE
The strategy has a clear identity: low win rate (41.7%), asymmetric payoff.
- SL = 1.5% (floor — do not reduce further)
- TP = 9.5% → reward:risk ratio ≈ 6.3:1
- Trades = 60 (AT THE HARD CEILING — this is the binding constraint)
- The TP escalation path has delivered consistent improvements.
  Continue escalating TP upward from 9.5.

### PATH A — REFINE THE INCUMBENT (PRIMARY, ACTIVE)

**PRIORITY 1: INCREASE take_profit_pct (HIGHEST EXPECTED VALUE)**
The most proven mutation path. Every major improvement since gen 14993
has come from exit refinement. Continue in order, one per generation:
  - take_profit_pct: 10.0   ← TRY THIS FIRST
  - take_profit_pct: 10.5
  - take_profit_pct: 11.0
  - take_profit_pct: 11.5
  - take_profit_pct: 12.0
  - take_profit_pct: 13.0
  - take_profit_pct: 14.0
  - take_profit_pct: 15.0

Do NOT skip values. Do NOT repeat values already tested.
Do NOT go below 9.5 under any circumstances.

Each test must be ONE value only. Higher TP reduces trade count
(beneficial) and improves Sharpe if the market delivers extended
trends. Win rate will likely decrease slightly but payoff ratio
increases further. This is the confirmed working path.

Upper limit consideration: TP above 15% may become unreachable in
practice, causing most trades to timeout rather than hit TP. If
win rate drops below 30% or trades drop below 30, TP has overshot.
The SUSPICIOUS_WINRATE filter at 90% is not a concern here.

**PRIORITY 2: INCREASE timeout_hours**
Current value is 138h. Increasing lets trades breathe longer and
may reduce the rate of timeout-based re-entries.

Try these values IN ORDER, one per generation, starting with 144:
  - timeout_hours: 144   ← smallest increment, try first
  - timeout_hours: 156
  - timeout_hours: 168   ← 1 week — natural swing trading boundary
  - timeout_hours: 192
  - timeout_hours: 216
  - timeout_hours: 240

DO NOT go below 138h (current value). That will increase trade count.
DO NOT go above 300h (program hard limit).
NOTE: Try this path only AFTER TP escalation stalls or if running
TP and timeout tests in parallel across generations.

**PRIORITY 3: INCREASE BOLLINGER PERIOD ON LONG SIDE**
Longer lookback → fewer Bollinger signals → fewer long entries →
trade count may drop below 60 (creating room for further mutations).
  - bollinger_position period_hours: 72 (long side, currently 48)
  - bollinger_position period_hours: 96 (long side)
  - bollinger_position period_hours: 120 (long side)

Do NOT change the short-side Bollinger (period_hours: 168 — already long).
Try only if PRIORITY 1 and 2 both stall.

**PRIORITY 4: INCREASE MOMENTUM_ACCELERATING PERIOD ON LONG SIDE**
  - momentum_accelerating period_hours: 72 (long side, currently 48)
  - momentum_accelerating period_hours: 96 (long side)
Longer period = fewer momentum signals = fewer entries = trade count
may drop below 60. Try only if PRIORITY 1–3 stall.

**PRIORITY 5: REPLACE momentum_accelerating WITH RSI**
If TP and timeout tuning stall for 100+ gens with no improvements:
  Long: replace momentum_accelerating=false with
    indicator: rsi, period_hours: 48, operator: lt, value: 35
  Short: replace momentum_accelerating=false with
    indicator: rsi, period_hours: 48, operator: gt, value: 65

RSI is more predictable. Tighter RSI thresholds (35/65) should
maintain or reduce trade count vs. the current setup.
DO NOT use looser thresholds (e.g., RSI < 45 or > 55) — too many trades.
DO NOT change any other conditions when making this swap.

**PRIORITY 6: SLIGHT stop_loss_pct INCREASE (MINOR)**
SL is at the floor (1.5%). A small increase may:
  - Reduce the number of stops triggered → slightly fewer trades
  - Improve win rate by giving trades more room
  Test: stop_loss_pct: 1.8, then 2.0, then 2.5
  Risk: wider SL reduces per-trade risk-adjusted return.
  Only test if PRIORITY 1–5 all fail to produce improvements.

**PRIORITY 7: size_pct (DO NOT TOUCH IN DANGER REGIME)**
  size_pct is at 25.0% (DANGER cap). Do not increase above 25.0%.
  Do not touch until macro regime improves (F&G > 30).

### PATH B — RSI+MACD+EMA RECONSTRUCTION (SECONDARY)
Only attempt if PATH A stalls for 300+ consecutive gens with 0 improvements.
The all-time benchmark (Sharpe=2.9232) used this combination.
Template:
  Long: RSI < 35, MACD bullish, price > EMA(period=50)
  Short: RSI > 65, MACD bearish, price < EMA(period=50)
  Exit: TP=9.5%, SL=1.5%, timeout=138h (match current exit structure)
  Pairs: BTC/USD only first
  This is a full indicator swap. Use only as a reset if PATH A
  definitively stalls for 300+ gens.

## ══════════════════════════════════════════════════════════════════════
## WHAT HAS FAILED — DO NOT REPEAT
## ══════════════════════════════════════════════════════════════════════

1. DO NOT use the UI "Current Best Strategy" display box.
   IT IS BROKEN. It shows stale YAMLs (e.g., name=crossover,
   TP=7.14, timeout=129, size_pct=28.18). These are DEAD.
   Using this display caused 13 of the last 20 gens to waste on
   Sharpe≈0.7734. USE ONLY THE YAML IN THIS PROGRAM DOCUMENT.

2. DO NOT generate strategies with 0 or 1 conditions per side.
   These produce >60 trades every time. [max_trades_reject]

3. DO NOT combine multiple boolean eq/neq conditions on exotic
   indicators. Collapses signal count to near zero. [low_trades]

4. DO NOT change pairs to anything outside BTC/USD, ETH/USD, SOL/USD.
   Hard rejection in code.

5. DO NOT propose size_pct > 25.0% (DANGER regime cap) or < 10%.

6. DO NOT set timeout_hours < 138 (current value — decreasing will
   increase trade count and cause [max_trades_reject]).
   DO NOT set timeout_hours > 300 (program hard limit).

7. DO NOT add a 4th condition. Will likely produce [low_trades].

8. DO NOT propose RSI thresholds looser than: long < 40, short > 60.
   Loose RSI → too many trades → [max_trades_reject].
   Recommended thresholds: long < 35, short > 65.

9. DO NOT set take_profit_pct ≤ 9.5% (current value — decreasing
   will increase trade count and cause [max_trades_reject]).
   Minimum TP: 9.5. Only increase TP.

10. DO NOT set stop_loss_pct below 1.5%. It is at the floor.
    If changing SL, only increase it.

11. DO NOT reproduce near-identical variants of known dead values:
    - Sharpe≈0.7734 (59 trades) — stale YAML artifact, dead end
    - Sharpe≈1.0325 (57 trades) — dead end
    - Sharpe≈1.0642 (56 trades) — old plateau
    - Sharpe≈1.1090 (60 trades) — dead end
    - Sharpe=1.1311 (60 trades) — superseded
    - Sharpe=1.1426 (60 trades) — superseded
    - Sharpe=1.2063 (60 trades) — CURRENT INCUMBENT (must beat this)
    If you produce 1.2063, your mutation was a no-op (duplicate).
    If you produce 0.7734, you used the wrong base YAML. Fix it.

12. DO NOT decrease any period_hours. At 60 trades (ceiling), shorter
    periods generate more signals → [max_trades_reject].

13. DO NOT add a second pair (ETH/USD or SOL/USD) while at 60 trades.
    Adding a second pair roughly doubles trade opportunities →
    guaranteed [max_trades_reject] unless conditions are dramatically
    tightened (which risks [low_trades]).

14. DO NOT mutate from any YAML where TP < 9.5 or timeout < 138.
    Those are stale values from old YAMLs. If you see those values
    in your base, stop and re-read the CURRENT INCUMBENT YAML above.

15. DO NOT propose TP values that have already been tested:
    TP=7.14 (dead), TP=7.38 (gen 14993), TP≈8.x (gen 15042),
    TP=9.5 (gen 15062, current). Only propose TP > 9.5.

## ══════════════════════════════════════════════════════════════════════
## MACRO ENVIRONMENT AWARENESS (as of 2026-04-09)
## ══════════════════════════════════════════════════════════════════════

Current Regime: DANGER | Fear & Greed: 14 (Extreme Fear)
BTC Dominance: 57.07% (elevated — BTC outperforming alts)
VIX