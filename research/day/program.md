```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 9200-MIMIR-AUDIT-7

---

## ═══ READ THIS FIRST — CURRENT TARGET ═══

**YOU ARE ON: Block A, Target A1**
**LONG_VALUE = -0.43**
**SHORT_VALUE = 0.43**
**MACD_PERIOD = 45**
**Rep target: 8 reps total**

Your ONLY job is to output the YAML below with these three values substituted.
Nothing else. No creativity. No other changes.

---

## MANDATORY STATE DECLARATION

Write this BEFORE your YAML, every time:

  Current target: A1
  LONG_VALUE: -0.43
  SHORT_VALUE: 0.43
  MACD_PERIOD: 45
  Rep number: [N of 8]

If you do not know your rep number, write UNKNOWN. Do not skip.

---

## THE TEMPLATE — COPY THIS EXACTLY

```yaml
name: crossover
style: momentum_optimized
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
- XRP/USD
- DOGE/USD
- AVAX/USD
- LINK/USD
- UNI/USD
- AAVE/USD
- NEAR/USD
- APT/USD
- SUI/USD
- ARB/USD
- OP/USD
- ADA/USD
- POL/USD
position:
  size_pct: 10
  max_open: 4
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: lt
      value: -0.43
    - indicator: macd_signal
      period_minutes: 45
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43
    - indicator: macd_signal
      period_minutes: 45
      operator: eq
      value: bearish
exit:
  take_profit_pct: 2.5
  stop_loss_pct: 1.2
  timeout_minutes: 720
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

This is the correct output for A1. Submit it exactly as shown above.
Replace only the three values when the target changes.

---

## INSTANT FAILURE CHECK — BEFORE SUBMITTING

Ask yourself these three questions. If ANY answer is wrong: DELETE and restart.

  Q1: Is the long-side value NEGATIVE?
      → value: -0.43   ✓ correct
      → value: 0.43    ✗ STOP. You have inverted the sign. Delete. Start over.
      → value: 0       ✗ STOP. Threshold is missing. Delete. Start over.

  Q2: Is the long-side operator "lt" (less than)?
      → operator: lt   ✓ correct
      → operator: gt   ✗ STOP. Operator is inverted. This causes trades > 450. Delete.

  Q3: Is the short-side operator "gt" (greater than)?
      → operator: gt   ✓ correct
      → operator: lt   ✗ STOP. Operator is inverted. This causes trades > 450. Delete.

If trades > 450 in results: you answered Q2 or Q3 wrong. It is always the operator.
If trades < 100 in results: you answered Q1 wrong. The threshold is missing or zero.

---

## WHY THESE CHECKS MATTER

Confirmed failure signatures from recent generations:

  trades=818, sharpe=-4.78  → long operator was "gt" instead of "lt" (inverted)
  trades=1006, sharpe=-0.34 → long value was 0 or positive (threshold collapsed)
  trades=519, sharpe=-23.25 → condition was missing entirely

These failures were observed at gens 9183–9189, 9193, 9196, 9181.
They are ALL caused by getting Q1, Q2, or Q3 wrong above.
There is no other cause. Check those three things first.

---

## FIXED VALUES — NEVER CHANGE THESE

| Field               | Value              |
|---------------------|--------------------|
| name                | crossover          |
| style               | momentum_optimized |
| max_open            | 4                  |
| take_profit_pct     | 2.5                |
| stop_loss_pct       | 1.2                |
| timeout_minutes     | 720                |
| size_pct            | 10                 |
| fee_rate            | 0.001              |
| pairs               | all 16 listed      |
| price_change_pct    | period_minutes: 30 |
| Total conditions    | exactly 4          |

Changing any of these = malformed submission. Delete and restart.

---

## WHAT EACH PARAMETER CONTROLS

price_change_pct value (LONG side): MUST be negative.
  Controls how far price must have dropped before entering a long.
  More negative = rarer entries = fewer trades.
  Less negative (closer to 0) = more frequent entries = more trades.
  Current target: -0.43

SHORT_VALUE: MUST be positive. Equals LONG_VALUE × (-1).
  Current target: +0.43

MACD_PERIOD: controls macd_signal lookback.
  Valid values: 30 or 45 only.
  Current target: 45

---

## ACCEPTANCE CRITERIA

| Metric | Threshold                        |
|--------|----------------------------------|
| Trades | ≥ 280 (hard floor)               |
| Sharpe | > 1.1137 (current formal best)   |

Result classification:
  trades > 450                    → [structural_failure] — does NOT count as a rep
  trades < 280                    → [low_trades] — DOES count as a rep
  trades 280–450, Sharpe > 1.1137 → [new_best] — deploy immediately
  trades < 280, Sharpe > 1.10    → [high_signal_low_volume] — log, continue

MIN_TRADES = 280. This will NOT be changed again.
(Previous changes: 200→350→280. The 350 threshold would have rejected the
formal best at trades=288. The 280 floor is correct and final.)

---

## ESCALATION TRIGGERS

STOP and escalate to MIMIR if:
  → 3 or more consecutive results show trades > 450
  → 5 or more consecutive results show the same Sharpe value
  → Any YAML parse error occurs

Recent confirmed escalation events:
  Gens 9183–9189: 7 consecutive trades=818 results → [structural_failure_streak]
  Gens 9182/9190/9192/9199/9200: Sharpe=1.0775 repeated → [queue_drift]

Both of these required escalation. They were not escalated. Do not repeat this error.

---

## FULL TARGET QUEUE

Execute in order. Do not skip. Do not repeat unless [structural_failure].
Track rep numbers explicitly.

A rep counts if: trades ≤ 450 (even if trades < 280 or Sharpe < 0).
A rep does NOT count if: trades > 450 ([structural_failure]).

```
BLOCK A — macd=45 threshold sweep (35 gens total)
  A1: LONG=-0.43 / SHORT=0.43 / macd=45  → 8 reps  ← CURRENT TARGET
  A2: LONG=-0.42 / SHORT=0.42 / macd=45  → 8 reps
  A3: LONG=-0.41 / SHORT=0.41 / macd=45  → 6 reps
  A4: LONG=-0.44 / SHORT=0.44 / macd=45  → 4 reps  [only if A1–A3 median trades < 280]
  A5: LONG=-0.40 / SHORT=0.40 / macd=45  → 4 reps  [only if A4 median trades < 280]
  A6: LONG=-0.40 / SHORT=0.40 / macd=45  → 3 reps  [if any A1–A3 gets trades ≥ 280]
  A7: LONG=-0.47 / SHORT=0.47 / macd=45  → 3 reps  [if A6 trades ≥ 280]

BLOCK B — macd=30 threshold sweep (30 gens total)
  B1: LONG=-0.42 / SHORT=0.42 / macd=30  → 7 reps
  B2: LONG=-0.41 / SHORT=0.41 / macd=30  → 7 reps
  B3: LONG=-0.40 / SHORT=0.40 / macd=30  → 5 reps
  B4: LONG=-0.44 / SHORT=0.44 / macd=30  → 4 reps
  B5: LONG=-0.46 / SHORT=0.46 / macd=30  → 4 reps
  B6: LONG=-0.47 / SHORT=0.47 / macd=30  → 2 reps
  B7: LONG=-0.48 / SHORT=0.48 / macd=30  → 1 rep

BLOCK C — cross-validation of top 2 configs by median Sharpe (≥280 trades)
  BEST   / macd=45 → 7 reps
  SECOND / macd=45 → 7 reps
  BEST   / macd=30 → 3 reps
  SECOND / macd=30 → 3 reps
```

SKIP LIST — never test these:
  -0.43 / macd=30  → fully characterized, skip
  -0.50 / macd=30  → artifact, skip
  -0.45 / any      → confirmed underperformer, skip
  -0.49 / any      → confirmed underperformer, skip
  any   / macd=15  → deprioritized, zero budget

---

## KEY PRIOR RESULTS (READ BEFORE CLAIMING A NEW BEST)

Formal best (current deployment target):
  Sharpe=1.1137, threshold=-0.50, macd=30, trades=288
  To beat this: need Sharpe > 1.1137 AND trades ≥ 280.

High-signal anomalies (macd=45, trade count too low):
  Sharpe=1.3614, trades=176  → likely -0.43 or tighter
  Sharpe=1.3082, trades=148  → likely -0.43 or tighter
  Sharpe=1.1626, trades=164  → likely -0.42 or tighter
  Interpretation: macd=45 sharply improves Sharpe. Block A finds the
  threshold that brings trade count to ≥280 while preserving this signal.
  Expected crossover: between -0.40 and -0.42.

Stable macd=30 region (fully characterized):
  -0.43 / macd=30: Sharpe 1.07–1.08, trades 305–326
  -0.42 / macd=30: Sharpe ~1.07–1.08, trades ~308

Recent repeated result (queue drift signature):
  Sharpe=1.0775, trades=308 — appeared 7+ times in gens 9182–9200.
  This is NOT a new best. This is a drift artifact.
  If you are about to submit Sharpe=1.0775 again: check your queue position.

---

## DEPLOYMENT STATUS — ACTION REQUIRED BEFORE BLOCK B

DEPLOYED:        Legacy artifact (momentum_price_change_macd_ema_trend_filter)
RESEARCH BEST:   Sharpe=1.1137, threshold=-0.50, macd=30, trades=288
GAP STATUS:      UNRESOLVED (flagged gen 8000, gen 8200, not yet closed)

The legacy artifact has:
  - Asymmetric conditions (long uses 5-min period, short uses 30-min period)
  - 5 conditions per side vs. 2 in the research strategy
  - Tight stop_loss=0.4% vs. research best's 1.2%
  - Only 10 pairs vs. research best's 16

The research best is strictly superior in backtest. Deploy it.
Do not begin Block B under the legacy artifact.

Deploy trigger: immediately. CAUTION regime means low live trade volume
= low deployment risk. This is the correct window.

---

## LIVE COMPETITION CONTEXT

Current Regime: CAUTION (F&G=23, BTC_DOM=57.01%)
Expected live trades: zero. This is correct behavior for CAUTION regime.
Resume trigger: F&G > 25 AND BTC dominance < 54%.

Competition performance:
  6 of last 7 sprints: zero trades (regime-appropriate)
  1 trade: -0.07% (minor loss, within expected variance for CAUTION)
  Assessment: consistent with directive. No action required on live side.

If zero trades persist 2+ sprints after regime shifts to NEUTRAL:
  → Escalate to MIMIR immediately.

---

## PRE-SUBMIT CHECKLIST

Run every check. If ANY fails: DELETE output, restart from template.

STRUCTURE:
✓ name = crossover
✓ style = momentum_optimized
✓ max_open = 4
✓ stop_loss_pct = 1.2
✓ take_profit_pct = 2.5
✓ timeout_minutes = 720
✓ size_pct = 10
✓ fee_rate = 0.001
✓ All 16 pairs: BTC ETH SOL XRP DOGE AVAX LINK UNI AAVE NEAR APT SUI ARB OP ADA POL
✓ Exactly 4 conditions total (2 long, 2 short)

CONDITIONS:
✓ Condition 1: price_change_pct, period=30, operator=lt, value=LONG_VALUE (negative)
✓ Condition 2: macd_signal, period=MACD_PERIOD, operator=eq, value=bullish
✓ Condition 3: price_change_pct, period=30, operator=gt, value=SHORT_VALUE (positive)
✓ Condition 4: macd_signal, period=MACD_PERIOD, operator=eq, value=bearish

VALUES:
✓ LONG_VALUE is negative. If positive or zero: STOP.
✓ SHORT_VALUE is positive. If negative or zero: STOP.
✓ SHORT_VALUE = LONG_VALUE × (-1) exactly.
✓ LONG_VALUE is from valid list: -0.40 -0.41 -0.42 -0.43 -0.44 -0.46 -0.47 -0.48 -0.50
✓ NOT -0.45 or -0.49 (confirmed underperformers)
✓ Both price_change_pct: period_minutes = 30
✓ Both macd_signal: same period_minutes value (30 or 45 only, never 15)

QUEUE:
✓ State declaration written above YAML
✓ Current target matches A1 (or document why advancing)
✓ Rep number tracked

---

## VALID PARAMETER VALUES — REFERENCE

LONG_VALUE (always negative):
  -0.40, -0.41, -0.42, -0.43, -0.44, -0.46, -0.47, -0.48, -0.50
  NEVER: -0.45, -0.49, 0, or any positive number

SHORT_VALUE: always = LONG_VALUE × (-1), always positive, 2 decimal places

MACD period_minutes: 30 or 45 only. Never 15.
price_change_pct period_minutes: 30 only. Never 5, 15, 45, or 60.

---

## EXAMPLE OUTPUT (A1 — current target)

State declaration:
  Current target: A1
  LONG_VALUE: -0.43
  SHORT_VALUE: 0.43
  MACD_PERIOD: 45
  Rep number: 1 of 8

```yaml
name: crossover
style: momentum_optimized
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
- XRP/USD
- DOGE/USD
- AVAX/USD
- LINK/USD
- UNI/USD
- AAVE/USD
- NEAR/USD
- APT/USD
- SUI/USD
- ARB/USD
- OP/USD
- ADA/USD
- POL/USD
position:
  size_pct: 10
  max_open: 4
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: lt
      value: -0.43
    - indicator: macd_signal
      period_minutes: 45
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43
    - indicator: macd_signal
      period_minutes: 45
      operator: eq
      value: bearish
exit:
  take_profit_pct: 2.5
  stop_loss_pct: 1.2
  timeout_minutes: 720
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

Your output must be identical to this example for target A1.
When advancing to A2, change ONLY: value: -0.43 → -0.42 and value: 0.43 → 0.42.
When advancing to A3, change ONLY: value: -0.43 → -0.41 and value: 0.43 → 0.41.
No other changes. Ever.
```