```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 8800-MIMIR-AUDIT-5

---

## YOUR ONLY JOB

1. Look up the CURRENT TARGET below.
2. Copy the TEMPLATE exactly.
3. Replace LONG_VALUE, SHORT_VALUE, and MACD_PERIOD.
4. Run the checklist.
5. Submit.

Nothing else. No other changes. No other indicators.

---

## THE TEMPLATE

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
      value: LONG_VALUE
    - indicator: macd_signal
      period_minutes: MACD_PERIOD
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: SHORT_VALUE
    - indicator: macd_signal
      period_minutes: MACD_PERIOD
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

Substitution rules:
- LONG_VALUE  = the negative number from CURRENT TARGET (e.g. -0.43)
- SHORT_VALUE = same number, sign flipped (e.g. 0.43)
- MACD_PERIOD = the macd value from CURRENT TARGET (e.g. 45)

---

## CURRENT TARGET

**Block A, Target A1: LONG_VALUE = -0.43, MACD_PERIOD = 45**
(SHORT_VALUE = 0.43)

See QUEUE section for full sequence. Advance target after completing
the specified number of repetitions.

---

## COMPLETE TARGET QUEUE

Track your position. Advance when rep count is reached.

```
BLOCK A — macd=45 exploration (35 gens total)
  A1: -0.43 / macd=45  → 8 reps
  A2: -0.42 / macd=45  → 8 reps
  A3: -0.41 / macd=45  → 6 reps
  A4: -0.44 / macd=45  → 4 reps  [run only if A1-A3 median trades < 280]
  A5: -0.46 / macd=45  → 3 reps  [run only if A4 median trades still < 280]
  A6: -0.40 / macd=45  → 3 reps  [run if trades are ≥280]
  A7: -0.47 / macd=45  → 3 reps  [run if trades are ≥280]

BLOCK B — macd=30 threshold sweep (30 gens total)
  B1: -0.42 / macd=30  → 7 reps
  B2: -0.41 / macd=30  → 7 reps
  B3: -0.40 / macd=30  → 5 reps
  B4: -0.44 / macd=30  → 4 reps
  B5: -0.46 / macd=30  → 4 reps
  B6: -0.47 / macd=30  → 2 reps
  B7: -0.48 / macd=30  → 1 rep

BLOCK C — cross-MACD validation (20 gens total)
  Take top 2 thresholds by median Sharpe (≥280 trades) from Blocks A+B.
  Call them BEST and SECOND.
  BEST   / macd=45 → 7 reps
  SECOND / macd=45 → 7 reps
  BEST   / macd=30 → 3 reps
  SECOND / macd=30 → 3 reps
```

Current position: **Block A, Target A1** (begin here).

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
| price_change_pct period_minutes | 30   |
| Total conditions    | exactly 4          |

---

## VALID PARAMETER VALUES

price_change_pct value (long side — must be negative):
  -0.40, -0.41, -0.42, -0.43, -0.44, -0.46, -0.47, -0.48, -0.50
  NEVER use: -0.45 or -0.49

short value = long value with sign flipped. Always 2 decimal places.

macd_signal period_minutes: 15, 30, or 45 only.
Both macd_signal conditions must use the same period.

price_change_pct period_minutes: 30. Always. Never 5, 15, 45, or 60.

---

## ACCEPTANCE CRITERIA

| Metric | Threshold                       |
|--------|---------------------------------|
| Trades | ≥ 280 (locked — never change)   |
| Sharpe | > 1.1137 (current formal best)  |

Reject if trades > 450 (structural failure) regardless of Sharpe.
Reject if trades < 280 regardless of Sharpe.
Log (do not accept) if trades < 280 AND Sharpe > 1.10.

If result beats Sharpe=1.1137 AND trades ≥ 280:
  → Flag for immediate deployment review.

If no result beats 1.1137 after all phases:
  → Accept best observed result. Do not revert to legacy strategy.

---

## SKIP LIST — DO NOT TEST THESE

| Threshold | MACD | Reason                              |
|-----------|------|-------------------------------------|
| -0.43     | 30   | Fully characterized. Skip.          |
| -0.50     | 30   | Artifact. Skip.                     |
| -0.45     | any  | Confirmed underperformer. Skip.     |
| -0.49     | any  | Confirmed underperformer. Skip.     |
| any       | 15   | Deprioritized. Zero budget.         |

---

## KEY PRIOR RESULTS

Formal best:
  Sharpe=1.1137, threshold=-0.50, macd=30, trades=288
  (Accepted under old MIN_TRADES=200. Treat as floor, not ceiling.)
  True target: median Sharpe > 1.08 at ≥305 trades.

High-signal anomalies (macd=45, too few trades to accept):
  Sharpe=1.3614, trades=176
  Sharpe=1.3082, trades=148
  Sharpe=1.1626, trades=164
  Interpretation: macd=45 produces superior signal quality.
  Block A aims to find threshold that brings trades ≥280.

Valid results near floor:
  -0.43 / macd=30: Sharpe 1.07–1.08, 305–326 trades (characterized, skip)
  -0.42 / macd=30: Sharpe ~1.07–1.08, ~308 trades (promising, continue)

---

## THE ONLY 4 INDICATORS THAT EXIST

Your strategy must contain exactly these 4 conditions and no others:

  1. price_change_pct  (period=30, operator=lt,  value=LONG_VALUE)
  2. macd_signal       (period=MACD_PERIOD, operator=eq, value=bullish)
  3. price_change_pct  (period=30, operator=gt,  value=SHORT_VALUE)
  4. macd_signal       (period=MACD_PERIOD, operator=eq, value=bearish)

Any other indicator name is invalid. Do not use it.

---

## PRE-SUBMIT CHECKLIST

Verify every item before submitting. If any item fails, delete your
output, copy the template from scratch, and start over.

✓ name = crossover
✓ style = momentum_optimized
✓ max_open = 4
✓ stop_loss_pct = 1.2
✓ take_profit_pct = 2.5
✓ timeout_minutes = 720
✓ size_pct = 10
✓ fee_rate = 0.001
✓ All 16 pairs present:
    BTC ETH SOL XRP DOGE AVAX LINK UNI AAVE NEAR APT SUI ARB OP ADA POL
✓ Exactly 4 conditions total (2 long, 2 short)
✓ Condition 1: price_change_pct, period=30, lt, LONG_VALUE (negative)
✓ Condition 2: macd_signal, period=MACD_PERIOD, eq, bullish
✓ Condition 3: price_change_pct, period=30, gt, SHORT_VALUE (positive)
✓ Condition 4: macd_signal, period=MACD_PERIOD, eq, bearish
✓ LONG_VALUE is one of: -0.40 -0.41 -0.42 -0.43 -0.44 -0.46 -0.47 -0.48 -0.50
✓ SHORT_VALUE = LONG_VALUE sign-flipped, 2 decimal places
✓ Both price_change_pct use period_minutes: 30
✓ Both macd_signal use the same period_minutes value

---

## CORRECT OUTPUT EXAMPLE

For target: -0.42 / macd=45

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
      value: -0.42
    - indicator: macd_signal
      period_minutes: 45
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.42
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

Your output must look exactly like this with only the two values changed.

---

## LIVE MONITORING

Zero live trades are expected while F&G < 25 and BTC dominance > 54%.
Current regime: CAUTION, F&G=23, BTC_DOM=57.25%.
Do not modify strategy to force trades. This is correct behavior.

Resume trigger: if F&G > 25 AND BTC dominance < 54%, expect trades.
If zero trades persist 2+ sprints after regime shifts to NEUTRAL:
  escalate to MIMIR.

---

## DEPLOYMENT GAP — ACTION REQUIRED

The currently deployed strategy is the legacy artifact (style:
momentum_price_change_macd_ema_trend_filter). It does not match the
research best. This gap must be resolved.

If any result achieves Sharpe > 1.1137 AND trades ≥ 280:
  → Replace deployed strategy immediately. Do not wait for Block C.

If Block A concludes without beating 1.1137:
  → Deploy current best (Sharpe=1.1137 config) before starting Block B.
  → The research best is strictly superior to the legacy artifact.
  → Do not keep the legacy artifact deployed during ongoing research.
```