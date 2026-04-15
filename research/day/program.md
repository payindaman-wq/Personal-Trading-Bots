```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 8600-MIMIR-AUDIT-4

---

## YOUR ONLY JOB

Copy the template below. Insert the TWO values from the CURRENT TARGET.
Run the checklist. Submit. That is all.

Do not read the legacy strategy. Do not improvise. Do not add indicators.
Do not use the emergency default unless explicitly told to.

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

Replace:
- LONG_VALUE  → the negative price_change_pct value from CURRENT TARGET
- SHORT_VALUE → same number, positive (sign-flipped)
- MACD_PERIOD → the macd period_minutes from CURRENT TARGET

Example: if CURRENT TARGET is -0.42 / macd=45:
  LONG_VALUE  = -0.42
  SHORT_VALUE = 0.42
  MACD_PERIOD = 45

---

## FIXED VALUES — THESE NEVER CHANGE — DO NOT TOUCH

| Field               | Value              |
|---------------------|--------------------|
| name                | crossover          |
| style               | momentum_optimized |
| max_open            | 4  ← NOT 3         |
| take_profit_pct     | 2.5 ← NOT 3.51     |
| stop_loss_pct       | 1.2 ← NOT 0.4      |
| timeout_minutes     | 720                |
| size_pct            | 10                 |
| fee_rate            | 0.001              |
| pairs               | ALL 16 listed above|
| price_change_pct period_minutes | 30 ← ALWAYS 30 |
| Total conditions    | EXACTLY 4          |

---

## CURRENT TARGET QUEUE

Process targets IN ORDER. Each target runs for the specified number of
generations before moving to the next. Do not skip. Do not repeat
characterized targets.

### QUEUE (execute in order, one target per generation)

```
BLOCK A — macd=45 exploration (HIGHEST PRIORITY — 35 gens)
Target A1:  -0.43 / macd=45    → run 8 times
Target A2:  -0.42 / macd=45    → run 8 times
Target A3:  -0.41 / macd=45    → 6 times
Target A4:  -0.44 / macd=45    → 4 times  [if A1-A3 median trades < 280]
Target A5:  -0.46 / macd=45    → 3 times  [if A4 median trades still < 280]
Target A6:  -0.40 / macd=45    → 3 times  [bonus if trades are healthy]
Target A7:  -0.47 / macd=45    → 3 times  [bonus if trades are healthy]

BLOCK B — macd=30 threshold sweep (30 gens)
Target B1:  -0.42 / macd=30    → 7 times
Target B2:  -0.41 / macd=30    → 7 times
Target B3:  -0.40 / macd=30    → 5 times
Target B4:  -0.44 / macd=30    → 4 times
Target B5:  -0.46 / macd=30    → 4 times
Target B6:  -0.47 / macd=30    → 2 times
Target B7:  -0.48 / macd=30    → 1 time

BLOCK C — cross-MACD validation (20 gens)
  After Block B: take the top 2 thresholds by median Sharpe (≥280 trades)
  Call them BEST and SECOND.
  BEST   / macd=45 → 7 times
  SECOND / macd=45 → 7 times
  BEST   / macd=30 → 3 times  (validation)
  SECOND / macd=30 → 3 times  (validation)
```

### CURRENT POSITION IN QUEUE
Block A, Target A1: -0.43 / macd=45
(Begin here. Track completions. Advance when rep count is reached.)

---

## VALID PARAMETER VALUES

### price_change_pct value (long side)
VALID:   -0.40  -0.41  -0.42  -0.43  -0.44  -0.46  -0.47  -0.48  -0.50
INVALID: -0.45  -0.49  (never use these — confirmed underperformers)

Short value is ALWAYS long value with sign flipped:
  -0.42 → 0.42    -0.43 → 0.43    -0.41 → 0.41

price_change_pct period_minutes is ALWAYS 30. Never 5, 15, 45, 60.

### macd_signal period_minutes
VALID: 15, 30, 45
Long and short must use the SAME value.

---

## CHARACTERIZED REGIONS — DO NOT REPEAT

| Threshold | MACD | Status                                    |
|-----------|------|-------------------------------------------|
| -0.43     | 30   | ✅ Done. Median ≈1.07-1.08, 305-326 trades |
| -0.50     | 30   | ⚠️ Artifact. Done.                        |
| any       | 15   | ❌ Deprioritized. Zero budget.            |
| -0.45     | any  | ❌ NEVER TEST                             |
| -0.49     | any  | ❌ NEVER TEST                             |

---

## KEY DATA FROM PRIOR RESEARCH

### Formal Best (treat as floor, not ceiling)
  Sharpe=1.1137, -0.50/macd=30, 288 trades
  NOTE: Accepted under MIN_TRADES=200. Likely statistical artifact.
  True target: median Sharpe > 1.08 at ≥305 trades.

### High-Value Low-Trade Anomalies (macd=45 signal)
  Gen 8384: Sharpe=1.3614, trades=176  [macd=45 related — too few trades]
  Gen 8194: Sharpe=1.3082, trades=148  [macd=45 related — too few trades]
  Gen 8197: Sharpe=1.1626, trades=164  [macd=45 related — too few trades]
  INTERPRETATION: macd=45 produces genuinely superior signal quality.
  Need looser thresholds (-0.44, -0.46) to bring trades ≥280.

### Recent Valid Results (≥280 trades)
  -0.43 / macd=30: Sharpe 1.07-1.08, 305-326 trades (fully characterized)

---

## ACCEPTANCE CRITERIA

| Metric   | Threshold                      |
|----------|-------------------------------|
| Trades   | ≥ 280 (LOCKED — never change) |
| Sharpe   | > 1.1137 (current formal best)|

Trades > 450: structural failure — reject regardless of Sharpe.
Trades < 280: automatic rejection — log if Sharpe > 1.10.

Immediate replacement trigger:
  Sharpe > 1.1137 AND trades ≥ 280 → replace deployed strategy now.

If no result beats 1.1137 after all phases:
  Accept best observed result. The 2-indicator strategy is still
  superior to the legacy artifact. Do NOT revert to legacy.

---

## WHAT STRUCTURAL FAILURE LOOKS LIKE

If your output causes ANY of these results, you used the wrong template:

| Trades | Sharpe    | Cause                          |
|--------|-----------|-------------------------------|
| 560    | -6.18     | Legacy template / no macd     |
| 818    | -4.78     | No MACD confirmation          |
| 325    | -11.88    | Extra forbidden indicators    |
| 1006   | -0.34     | No conditions / wrong format  |
| 478    | -6.11     | Wrong template                |

If you see these results: DO NOT adjust parameters. COPY THE TEMPLATE
FROM SCRATCH. The problem is format, not values.

---

## FORBIDDEN INDICATORS — IF YOU WRITE THESE, DELETE EVERYTHING

- `momentum_accelerating`  ← legacy artifact. Causes -6 to -18 Sharpe.
- `price_vs_ema`           ← legacy artifact.
- `trend`                  ← legacy artifact.
- `period_minutes: 5`      ← wrong period for price_change_pct.
- `period_minutes: 15`     ← wrong period for price_change_pct.
- `period_minutes: 60`     ← wrong period for price_change_pct.

If any of these appear in your output: DELETE IT. Copy template. Restart.

---

## FORBIDDEN STRUCTURAL VALUES

- max_open: 3       ← legacy artifact (must be 4)
- stop_loss_pct: 0.4 ← legacy artifact (must be 1.2)
- take_profit_pct: 3.51 ← legacy artifact (must be 2.5)
- style: momentum_price_change_macd_ema_trend_filter ← legacy

---

## LIVE PERFORMANCE NOTE

Zero live trades are EXPECTED.
  F&G = 23 (Extreme Fear), BTC Dominance = 57.26%
  Strategy requires 0.43%+ move in 30min + MACD confirmation.
  Fear regime suppresses volatility → no triggers → no trades.
  This is CORRECT behavior. Do not modify strategy to force trades.

MONITORING TRIGGER: If F&G > 25 AND BTC dominance < 54%:
  Expect trades to resume. If zero trades persist 2+ sprints after
  regime shift to NEUTRAL, escalate to MIMIR.

DO NOT reduce price_change_pct toward 0 to force trades.
DO NOT switch to macd=15 for faster signals.
DO NOT change max_open, stop_loss, or take_profit.

---

## MIN_TRADES = 280 — LOCKED FOREVER

Do not change this constant.
Do not adjust it to accept low-trade results.
Do not change it even if Sharpe is very high.

The 288-trade result (Sharpe=1.1137) was accepted under MIN_TRADES=200
and is treated as an artifact. We do not lower the bar to match it.

---

## PRE-SUBMIT CHECKLIST — VERIFY EVERY ITEM BEFORE SUBMITTING

Count your conditions. You must have EXACTLY 4.

✓ name = crossover
✓ style = momentum_optimized
✓ max_open = 4
✓ stop_loss_pct = 1.2
✓ take_profit_pct = 2.5
✓ timeout_minutes = 720
✓ size_pct = 10
✓ fee_rate = 0.001
✓ All 16 pairs present (BTC ETH SOL XRP DOGE AVAX LINK UNI AAVE NEAR APT SUI ARB OP ADA POL)
✓ Condition 1: price_change_pct, period=30, operator=lt, value=LONG_VALUE (negative)
✓ Condition 2: macd_signal, period=MACD_PERIOD, operator=eq, value=bullish
✓ Condition 3: price_change_pct, period=30, operator=gt, value=SHORT_VALUE (positive)
✓ Condition 4: macd_signal, period=MACD_PERIOD, operator=eq, value=bearish
✓ Total conditions = 4 (not 3, not 5, not 6)
✓ LONG_VALUE is in: -0.40,-0.41,-0.42,-0.43,-0.44,-0.46,-0.47,-0.48,-0.50
✓ SHORT_VALUE = LONG_VALUE with sign flipped, 2 decimal places
✓ Both price_change_pct period_minutes = 30
✓ Both macd_signal period_minutes = same value (15, 30, or 45)
✓ No momentum_accelerating, price_vs_ema, trend, or any other indicator
✓ No max_open=3, stop_loss_pct=0.4, take_profit_pct=3.51

If ANY item fails: DELETE YOUR OUTPUT. COPY THE TEMPLATE. START OVER.
Do not fix in place. Do not patch. Delete and copy.

---

## EXAMPLE OUTPUT (for -0.42 / macd=45)

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

This is what a correct output looks like.
Your output for the current target should look exactly like this,
with the two values changed to match the CURRENT TARGET.
```