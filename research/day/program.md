```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 9000-MIMIR-AUDIT-6

---

## CRITICAL FAILURE PATTERNS — READ BEFORE ANYTHING ELSE

The following are NOT parameter misses. They are STRUCTURAL FAILURES
caused by ignoring the template. If your result matches any pattern
below, your submission was malformed. DELETE and start over.

STRUCTURAL FAILURE SIGNATURES:
  - trades > 450  → price_change_pct condition missing or operator wrong
  - Sharpe < -1.0 → catastrophic overtrading, structural failure
  - trades < 100  → thresholds too tight or conditions duplicated

Recent confirmed failures (do NOT repeat these errors):
  Gen 8985: trades=469, sharpe=-0.17  ← threshold missing or near-zero
  Gen 8987: trades=818, sharpe=-4.78  ← operator inverted or condition absent
  Gen 8992: trades=812, sharpe=-4.80  ← same failure
  Gen 9000: trades=1006, sharpe=-0.34 ← complete threshold collapse

If you are about to submit something with a threshold value of 0,
near-zero, or positive for the LONG side: STOP. You have made an error.

---

## YOUR ONLY JOB

1. State your current target (copy from CURRENT TARGET section).
2. State which rep number this is (e.g., "This is rep 3 of 8 for A1").
3. Copy the TEMPLATE exactly.
4. Replace LONG_VALUE, SHORT_VALUE, and MACD_PERIOD from the target.
5. Run the checklist. Verify every item.
6. Submit.

Nothing else. No other changes. No other indicators. No creativity.

---

## MANDATORY STATE DECLARATION

Before your YAML output, you MUST write exactly this:

  Current target: [e.g., A1]
  LONG_VALUE: [e.g., -0.43]
  SHORT_VALUE: [e.g., 0.43]
  MACD_PERIOD: [e.g., 45]
  Rep number: [e.g., 3 of 8]

If you cannot determine your rep number, write rep=UNKNOWN and proceed
with the current target. Do not skip ahead.

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
  LONG_VALUE  = the negative number from CURRENT TARGET (e.g. -0.43)
  SHORT_VALUE = same magnitude, positive sign (e.g. 0.43)
  MACD_PERIOD = the macd value from CURRENT TARGET (e.g. 45)

LONG_VALUE is always negative. SHORT_VALUE is always positive.
SHORT_VALUE = LONG_VALUE × (-1). Always. No exceptions.

---

## CURRENT TARGET

**Block A, Target A1: LONG_VALUE = -0.43, MACD_PERIOD = 45**
(SHORT_VALUE = 0.43)

See QUEUE section for full sequence.

---

## COMPLETE TARGET QUEUE

You must execute targets in order. Do not skip. Do not repeat.
Track rep count carefully.

```
BLOCK A — macd=45 exploration (35 gens total)
  A1: -0.43 / macd=45  → 8 reps
  A2: -0.42 / macd=45  → 8 reps
  A3: -0.41 / macd=45  → 6 reps
  A4: -0.44 / macd=45  → 4 reps  [only if A1–A3 median trades < 280]
  A5: -0.40 / macd=45  → 4 reps  [only if A4 median trades still < 280]
  A6: -0.40 / macd=45  → 3 reps  [run if any A1–A3 config gets trades ≥ 280]
  A7: -0.47 / macd=45  → 3 reps  [run if A6 trades ≥ 280]

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

Current position: **Block A, Target A1** (begin here, rep 1 of 8).

---

## FIXED VALUES — NEVER CHANGE THESE

| Field                           | Value              |
|---------------------------------|--------------------|
| name                            | crossover          |
| style                           | momentum_optimized |
| max_open                        | 4                  |
| take_profit_pct                 | 2.5                |
| stop_loss_pct                   | 1.2                |
| timeout_minutes                 | 720                |
| size_pct                        | 10                 |
| fee_rate                        | 0.001              |
| pairs                           | all 16 listed      |
| price_change_pct period_minutes | 30                 |
| Total conditions                | exactly 4          |

These values are locked. Changing any of them constitutes a malformed
submission. Delete and restart from the template if you changed any.

---

## VALID PARAMETER VALUES

price_change_pct value (LONG side — MUST be negative):
  -0.40, -0.41, -0.42, -0.43, -0.44, -0.46, -0.47, -0.48, -0.50
  NEVER use: -0.45 or -0.49 (confirmed underperformers)
  NEVER use: 0 or any positive number on the long side

SHORT_VALUE rules:
  = LONG_VALUE × (-1)
  Always exactly 2 decimal places
  Always positive
  Example: LONG=-0.43 → SHORT=0.43

macd_signal period_minutes: 15, 30, or 45 ONLY.
Both macd_signal conditions must use the SAME period_minutes value.

price_change_pct period_minutes: 30 ONLY.
Never 5, 15, 45, or 60. Always 30.

---

## ACCEPTANCE CRITERIA

| Metric | Threshold                        |
|--------|----------------------------------|
| Trades | ≥ 280 (hard floor — never lower) |
| Sharpe | > 1.1137 (current formal best)   |

Hard reject conditions (log and discard):
  - trades > 450 → structural failure, do not count as valid rep
  - trades < 280 → log as [low_trades], do not accept
  - Sharpe < 0   → structural failure if trades also > 450

Special logging:
  - trades < 280 AND Sharpe > 1.10 → log as [high_signal_low_volume]
  - trades > 450 → log as [structural_failure], flag for review

If result beats Sharpe=1.1137 AND trades ≥ 280:
  → Flag for IMMEDIATE deployment review. Do not wait for Block C.

If no result beats 1.1137 after all phases:
  → Accept best observed result. Do not revert to legacy strategy.

NOTE ON MIN_TRADES STABILITY:
  MIN_TRADES=280 is fixed for this entire research program.
  It was previously changed three times (200→350→280), causing
  acceptance criteria inconsistency. It will NOT be changed again.
  The formal best (Sharpe=1.1137, trades=288) was accepted under
  the 200-threshold era but remains valid at 280. It is the floor,
  not the target.

---

## SKIP LIST — DO NOT TEST THESE

| Threshold | MACD | Reason                               |
|-----------|------|--------------------------------------|
| -0.43     | 30   | Fully characterized. Skip.           |
| -0.50     | 30   | Artifact. Skip.                      |
| -0.45     | any  | Confirmed underperformer. Skip.      |
| -0.49     | any  | Confirmed underperformer. Skip.      |
| any       | 15   | Deprioritized. Zero budget.          |

---

## KEY PRIOR RESULTS

Formal best (current deployment target):
  Sharpe=1.1137, threshold=-0.50, macd=30, trades=288
  Accepted under old MIN_TRADES=200. Valid at MIN_TRADES=280 (trades=288).
  This is the floor, not the ceiling.
  True target: median Sharpe > 1.08 at ≥ 305 trades.

High-signal anomalies (macd=45, insufficient trades):
  Sharpe=1.3614, trades=176  → threshold unknown, likely -0.43 or tighter
  Sharpe=1.3082, trades=148  → threshold likely -0.43 or tighter
  Sharpe=1.1626, trades=164  → threshold likely -0.42 or tighter
  Interpretation: macd=45 sharply improves signal quality.
  Trade count deficit is caused by tight threshold. Block A finds the
  threshold that brings macd=45 configurations to ≥280 trades.
  Expected crossover: somewhere between -0.40 and -0.42.

Near-floor valid results (macd=30):
  -0.43 / macd=30: Sharpe 1.07–1.08, 305–326 trades (fully characterized)
  -0.42 / macd=30: Sharpe ~1.07–1.08, ~308 trades (promising, Block B)

Recent repeated configuration (likely -0.42 or -0.43 / macd=45):
  Gens 8993–8999: Sharpe=1.0775, trades=308 (repeated 5× — not advancing)
  Cause: LLM not tracking queue position. Fix: state declaration above.

---

## THE ONLY 4 CONDITIONS THAT EXIST

Your strategy must contain exactly these 4 conditions and no others.
Any other indicator name is invalid and will cause a backtest error.

  1. price_change_pct   period=30   operator=lt   value=LONG_VALUE (negative)
  2. macd_signal        period=MACD  operator=eq   value=bullish
  3. price_change_pct   period=30   operator=gt   value=SHORT_VALUE (positive)
  4. macd_signal        period=MACD  operator=eq   value=bearish

Conditions 1 and 3 use DIFFERENT operators (lt vs gt) and DIFFERENT
values (negative vs positive) but the SAME period (30).

Conditions 2 and 4 use DIFFERENT values (bullish vs bearish) but the
SAME period (MACD_PERIOD).

---

## PRE-SUBMIT CHECKLIST

Run every check. If ANY item fails: DELETE output, copy template fresh,
start over. Do not attempt to patch a malformed output.

STRUCTURE CHECKS:
✓ name = crossover
✓ style = momentum_optimized
✓ max_open = 4
✓ stop_loss_pct = 1.2
✓ take_profit_pct = 2.5
✓ timeout_minutes = 720
✓ size_pct = 10
✓ fee_rate = 0.001
✓ All 16 pairs present: BTC ETH SOL XRP DOGE AVAX LINK UNI AAVE NEAR APT SUI ARB OP ADA POL
✓ Exactly 4 conditions total (2 long, 2 short)

CONDITION CHECKS:
✓ Condition 1: indicator=price_change_pct, period=30, operator=lt, value=LONG_VALUE
✓ Condition 2: indicator=macd_signal, period=MACD_PERIOD, operator=eq, value=bullish
✓ Condition 3: indicator=price_change_pct, period=30, operator=gt, value=SHORT_VALUE
✓ Condition 4: indicator=macd_signal, period=MACD_PERIOD, operator=eq, value=bearish

VALUE CHECKS:
✓ LONG_VALUE is negative (e.g., -0.43). If positive: STOP. Restart.
✓ SHORT_VALUE is positive (e.g., 0.43). If negative: STOP. Restart.
✓ SHORT_VALUE = LONG_VALUE × (-1). Same magnitude, opposite sign.
✓ LONG_VALUE is one of: -0.40 -0.41 -0.42 -0.43 -0.44 -0.46 -0.47 -0.48 -0.50
✓ SHORT_VALUE has exactly 2 decimal places
✓ Both price_change_pct use period_minutes: 30
✓ Both macd_signal use the same period_minutes value

QUEUE CHECKS:
✓ State declaration is written above the YAML
✓ Current target matches CURRENT TARGET section
✓ Rep number is stated and tracked

FAILURE PREVENTION CHECKS:
✓ No condition uses period_minutes: 5, 15, or 60 for price_change_pct
✓ No condition uses period_minutes: 15 for macd_signal
✓ No additional indicators added (momentum_accelerating, ema, trend, etc.)
✓ Long side uses operator: lt (not gt)
✓ Short side uses operator: gt (not lt)
✓ LONG_VALUE is NOT -0.45 or -0.49

---

## CORRECT OUTPUT EXAMPLE

State declaration:
  Current target: A2
  LONG_VALUE: -0.42
  SHORT_VALUE: 0.42
  MACD_PERIOD: 45
  Rep number: 1 of 8

YAML output:

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

Your output must look exactly like this example, with only the
parameter values changed per the current target.

---

## STRUCTURAL FAILURE ESCALATION PROTOCOL

If 3 or more consecutive generations produce trades > 450:
  → Stop the queue. Escalate to MIMIR immediately.
  → Do not continue submitting until root cause is identified.
  → Log as [structural_failure_streak].

If 5 or more consecutive generations return the same Sharpe value:
  → The LLM is stuck in a loop. Escalate to MIMIR.
  → Reset queue position to start of current target.
  → Log as [queue_drift].

Recent queue drift detected:
  Gens 8993–8999: Sharpe=1.0775 repeated 5 times.
  This is [queue_drift]. Reset to A1, rep 1.

---

## DEPLOYMENT STATUS — ACTION REQUIRED

CURRENT DEPLOYMENT: Legacy artifact (style: momentum_price_change_macd_ema_trend_filter)
RESEARCH BEST:      Sharpe=1.1137, threshold=-0.50, macd=30, trades=288
STATUS:             GAP NOT RESOLVED (flagged at gens 8000 and 8200)

ACTION:
  → Deploy research best (Sharpe=1.1137) IMMEDIATELY.
  → The legacy artifact is architecturally different and unvalidated
    against the research best in live conditions.
  → The CAUTION regime (F&G=23) means low live trade volume, making
    this a low-risk deployment window.
  → Do not continue Block A research under the legacy artifact.

If new result beats Sharpe=1.1137 AND trades ≥ 280 during Block A:
  → Replace deployed strategy immediately. Do not wait for Block C.

If Block A concludes without beating 1.1137:
  → Research best remains deployed. Begin Block B.

---

## LIVE MONITORING

Current Regime: CAUTION (F&G=23, BTC_DOM=57.21%)
Directive: Zero live trades expected. This is correct behavior.

Resume trigger: F&G > 25 AND BTC dominance < 54%.
If zero trades persist 2+ sprints after regime shifts to NEUTRAL:
  → Escalate to MIMIR immediately.

Competition performance note:
  6 of last 7 sprints: zero trades, ranking by default (2nd–6th).
  1 trade on comp-20260415: -0.07% PnL (regime-appropriate caution).
  Performance is consistent with CAUTION directive. No action required.

---

## QUEUE INTEGRITY RULES

1. Never test the same (threshold, macd) pair twice in the same block
   unless the queue explicitly calls for it.
2. Never advance past the current target without completing its rep count.
3. If backtest returns [structural_failure] (trades > 450), that rep
   does NOT count toward the target's rep count. Repeat the same target.
4. If backtest returns [low_trades] (trades < 280), that rep DOES count.
   The data point is still useful for characterizing the threshold.
5. Log every result with its target label (e.g., A1-rep3) for tracking.
```