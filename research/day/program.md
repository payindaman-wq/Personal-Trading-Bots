```markdown
# ODIN Day League — v11300
# Champion: Sharpe=1.1731 | trades=310 | Beat target: Sharpe > 1.1739 AND trades ≥ 280

═══════════════════════════════════════════════════════════════
STEP 1 — COPY THIS TEMPLATE EXACTLY, THEN CHANGE ONLY STEP 2 VALUES
═══════════════════════════════════════════════════════════════

```yaml
name: crossover
style: momentum_price_change_macd_ema_trend_filter
pairs:
- UNI/USD
- AAVE/USD
- XRP/USD
- SOL/USD
- DOGE/USD
- NEAR/USD
- BTC/USD
- ETH/USD
- AVAX/USD
- LINK/USD
position:
  size_pct: 10
  max_open: 3
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: momentum_accelerating
      period_minutes: 120
      operator: eq
      value: true
    - indicator: price_change_pct
      period_minutes: 5
      operator: lt
      value: -1.21        # ← LONG THRESHOLD (MUST be negative)
    - indicator: macd_signal
      period_minutes: 30
      operator: eq
      value: bullish
    - indicator: price_vs_ema
      period_minutes: 60
      operator: eq
      value: above
    - indicator: trend
      period_minutes: 240
      operator: eq
      value: up
  short:
    conditions:
    - indicator: momentum_accelerating
      period_minutes: 60
      operator: eq
      value: true
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 1.16         # ← SHORT THRESHOLD (MUST be positive)
    - indicator: macd_signal
      period_minutes: 30
      operator: eq
      value: bearish
    - indicator: price_vs_ema
      period_minutes: 120
      operator: eq
      value: below
    - indicator: trend
      period_minutes: 240
      operator: eq
      value: down
exit:
  take_profit_pct: 3.51   # ← TP
  stop_loss_pct: 0.37     # ← SL
  timeout_minutes: 706    # ← TIMEOUT
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

═══════════════════════════════════════════════════════════════
STEP 2 — PICK ONE ROW FROM THE TABLE BELOW
═══════════════════════════════════════════════════════════════

MANDATORY: Pick a row you have NOT used in this session.
If you get [dedup_reject], you picked a duplicate — choose a DIFFERENT row.
PRIORITY: Try D-rows and E-rows first (least tested, most likely novel).

Champion (A1) — do not reuse: long=-1.21, short=1.16, tp=3.51, sl=0.37, timeout=706

| Target | long.value | short.value | take_profit | stop_loss | timeout |
|--------|------------|-------------|-------------|-----------|---------|
| A2     | -1.18      | 1.16        | 3.51        | 0.37      | 706     |
| A3     | -1.24      | 1.16        | 3.51        | 0.37      | 706     |
| A4     | -1.21      | 1.13        | 3.51        | 0.37      | 706     |
| A5     | -1.21      | 1.19        | 3.51        | 0.37      | 706     |
| B1     | -1.21      | 1.16        | 3.75        | 0.37      | 706     |
| B2     | -1.21      | 1.16        | 3.25        | 0.37      | 706     |
| B3     | -1.21      | 1.16        | 3.51        | 0.40      | 706     |
| B4     | -1.21      | 1.16        | 3.51        | 0.34      | 706     |
| B5     | -1.21      | 1.16        | 3.51        | 0.31      | 706     |
| B6     | -1.21      | 1.16        | 4.00        | 0.37      | 706     |
| B7     | -1.21      | 1.16        | 3.51        | 0.43      | 706     |
| C1     | -1.21      | 1.16        | 3.51        | 0.37      | 660     |
| C2     | -1.21      | 1.16        | 3.51        | 0.37      | 750     |
| C3     | -1.18      | 1.13        | 3.75        | 0.37      | 706     |
| C4     | -1.24      | 1.19        | 3.25        | 0.40      | 706     |
| C5     | -1.21      | 1.16        | 3.51        | 0.37      | 800     |
| C6     | -1.21      | 1.16        | 3.51        | 0.37      | 600     |
| D1     | -1.18      | 1.16        | 3.75        | 0.37      | 706     |
| D2     | -1.24      | 1.16        | 3.25        | 0.37      | 706     |
| D3     | -1.21      | 1.13        | 3.51        | 0.34      | 706     |
| D4     | -1.21      | 1.19        | 3.51        | 0.40      | 706     |
| D5     | -1.18      | 1.16        | 3.51        | 0.34      | 750     |
| D6     | -1.24      | 1.16        | 3.51        | 0.40      | 660     |
| D7     | -1.21      | 1.13        | 3.75        | 0.37      | 750     |
| D8     | -1.21      | 1.19        | 3.25        | 0.37      | 660     |
| E1     | -1.18      | 1.19        | 3.75        | 0.34      | 750     |
| E2     | -1.24      | 1.13        | 3.25        | 0.40      | 660     |
| E3     | -1.18      | 1.16        | 4.00        | 0.34      | 750     |
| E4     | -1.24      | 1.16        | 4.00        | 0.40      | 660     |
| E5     | -1.21      | 1.13        | 4.00        | 0.31      | 750     |
| E6     | -1.21      | 1.19        | 4.00        | 0.43      | 660     |
| E7     | -1.18      | 1.13        | 3.51        | 0.31      | 800     |
| E8     | -1.24      | 1.19        | 3.51        | 0.43      | 600     |

Run 8 valid reps per target. Valid rep = trades ≤ 450. Rotate targets each rep.

═══════════════════════════════════════════════════════════════
STEP 3 — ACCEPTANCE RULES
═══════════════════════════════════════════════════════════════

| Result                              | Tag                | Rep? |
|-------------------------------------|--------------------|------|
| trades > 450                        | [structural_fail]  | NO   |
| trades < 280                        | [low_trades]       | YES  |
| 280 ≤ trades ≤ 450, S ≤ 1.1739     | [discarded]        | YES  |
| 280 ≤ trades ≤ 450, S > 1.1739     | [new_best] deploy  | YES  |
| [dedup_reject]                      | pick different row | NO   |

═══════════════════════════════════════════════════════════════
STEP 4 — CRITICAL CHECKS (verify before submitting)
═══════════════════════════════════════════════════════════════

  ✓ long price_change_pct value  = NEGATIVE (e.g. -1.21)
  ✓ short price_change_pct value = POSITIVE (e.g. 1.16)
  ✓ long operator = lt | short operator = gt
  ✓ pairs count = 10 (unchanged)
  ✓ conditions = 5 long, 5 short (unchanged)
  ✓ all values from table above — no invented values
  ✓ row not previously used this session

If any check fails → DELETE and restart from Step 1.

═══════════════════════════════════════════════════════════════
LOCKED — DO NOT CHANGE
═══════════════════════════════════════════════════════════════

name, style, all 10 pairs, max_open=3, size_pct=10, fee_rate=0.001,
all operators, all indicator types, all period_minutes,
all eq values (true/bullish/bearish/above/below/up/down),
condition count, risk block values.
```

---