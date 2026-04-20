```markdown
# ODIN Day League — v11300-escape

## PASTE THIS YAML, THEN CHANGE ONLY THE MARKED VALUES

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
      value: -1.21        # ← CHANGE THIS (MUST be negative)
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
      value: 1.16         # ← CHANGE THIS (MUST be positive)
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
  take_profit_pct: 3.51   # ← CHANGE THIS
  stop_loss_pct: 0.37     # ← CHANGE THIS
  timeout_minutes: 706    # ← CHANGE THIS
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

---

## MANDATORY CHECKS (verify all 5 before submitting)

1. long price_change_pct value is NEGATIVE (e.g. -1.21) ✓
2. short price_change_pct value is POSITIVE (e.g. 1.16) ✓
3. long operator = lt, short operator = gt ✓
4. pairs count = 10 (unchanged) ✓
5. Values come from the table below — NO invented values ✓

If any check fails → DELETE and restart from template.

---

## STEP 2 — PICK EXACTLY ONE ROW FROM THIS TABLE

**Champion: Sharpe=1.1731, trades=310 — beat with Sharpe > 1.1731 AND trades ≥ 280**

**HEAVILY TESTED (avoid unless completing 8-rep quota):** A1, A2, A3, B1, B2, B3, B4, C1, C2, D1, D5

| Target | long.value | short.value | take_profit | stop_loss | timeout | Status |
|--------|------------|-------------|-------------|-----------|---------|--------|
| A1     | -1.21      | 1.16        | 3.51        | 0.37      | 706     | CHAMPION |
| A2     | -1.18      | 1.16        | 3.51        | 0.37      | 706     | tested |
| A3     | -1.24      | 1.16        | 3.51        | 0.37      | 706     | tested |
| A4     | -1.21      | 1.13        | 3.51        | 0.37      | 706     | tested |
| A5     | -1.21      | 1.19        | 3.51        | 0.37      | 706     | tested |
| B1     | -1.21      | 1.16        | 3.75        | 0.37      | 706     | tested |
| B2     | -1.21      | 1.16        | 3.25        | 0.37      | 706     | tested |
| B3     | -1.21      | 1.16        | 3.51        | 0.40      | 706     | tested |
| B4     | -1.21      | 1.16        | 3.51        | 0.34      | 706     | tested |
| B5     | -1.21      | 1.16        | 3.51        | 0.31      | 706     | PRIORITY |
| B6     | -1.21      | 1.16        | 4.00        | 0.37      | 706     | PRIORITY |
| B7     | -1.21      | 1.16        | 3.51        | 0.43      | 706     | PRIORITY |
| C1     | -1.21      | 1.16        | 3.51        | 0.37      | 660     | tested |
| C2     | -1.21      | 1.16        | 3.51        | 0.37      | 750     | tested |
| C3     | -1.18      | 1.13        | 3.75        | 0.37      | 706     | PRIORITY |
| C4     | -1.24      | 1.19        | 3.25        | 0.40      | 706     | PRIORITY |
| C5     | -1.21      | 1.16        | 3.51        | 0.37      | 800     | PRIORITY |
| C6     | -1.21      | 1.16        | 3.51        | 0.37      | 600     | PRIORITY |
| D1     | -1.18      | 1.16        | 3.75        | 0.37      | 706     | tested |
| D2     | -1.24      | 1.16        | 3.25        | 0.37      | 706     | PRIORITY |
| D3     | -1.21      | 1.13        | 3.51        | 0.34      | 706     | PRIORITY |
| D4     | -1.21      | 1.19        | 3.51        | 0.40      | 706     | PRIORITY |
| D5     | -1.18      | 1.16        | 3.51        | 0.34      | 750     | tested |
| D6     | -1.24      | 1.16        | 3.51        | 0.40      | 660     | PRIORITY |
| D7     | -1.21      | 1.13        | 3.75        | 0.37      | 750     | PRIORITY |
| D8     | -1.21      | 1.19        | 3.25        | 0.37      | 660     | PRIORITY |
| E1     | -1.21      | 1.16        | 3.51        | 0.28      | 706     | NEW |
| E2     | -1.21      | 1.16        | 3.51        | 0.46      | 706     | NEW |
| E3     | -1.21      | 1.16        | 3.51        | 0.37      | 850     | NEW |
| E4     | -1.21      | 1.16        | 3.51        | 0.37      | 550     | NEW |
| E5     | -1.21      | 1.16        | 4.25        | 0.37      | 706     | NEW |
| E6     | -1.21      | 1.16        | 3.00        | 0.34      | 706     | NEW |
| E7     | -1.18      | 1.13        | 3.51        | 0.37      | 750     | NEW |
| E8     | -1.24      | 1.19        | 3.51        | 0.37      | 660     | NEW |
| F1     | -1.15      | 1.16        | 3.51        | 0.37      | 706     | NEW |
| F2     | -1.27      | 1.16        | 3.51        | 0.37      | 706     | NEW |
| F3     | -1.21      | 1.10        | 3.51        | 0.37      | 706     | NEW |
| F4     | -1.21      | 1.22        | 3.51        | 0.37      | 706     | NEW |
| F5     | -1.18      | 1.16        | 3.75        | 0.34      | 750     | NEW |
| F6     | -1.24      | 1.16        | 3.25        | 0.40      | 660     | NEW |

**PREFER rows marked PRIORITY or NEW. Avoid rows marked "tested" unless filling an incomplete 8-rep quota.**

Run 8 reps per target before advancing. A rep = any result with trades ≤ 450.

---

## STEP 3 — ACCEPTANCE RULES

| Result                              | Tag                  | Counts as rep? |
|-------------------------------------|----------------------|----------------|
| trades > 450                        | [structural_failure] | NO — DELETE, restart |
| trades < 280                        | [low_trades]         | YES — discard  |
| 280 ≤ trades ≤ 450, S ≤ 1.1731     | [discarded]          | YES            |
| 280 ≤ trades ≤ 450, S > 1.1731     | [new_best] → deploy  | YES            |

MIN_TRADES = 280. Final. Do not change.

---

## FAILURE FINGERPRINTS — DELETE AND RESTART IF YOU SEE:

- trades > 450       → threshold outside table range
- trades = 0         → YAML malformed (likely dedup or syntax error)
- sharpe < -10       → entry conditions broken
- long.value > 0     → sign error on long threshold
- dedup_reject       → you picked a row already submitted; pick a DIFFERENT row, preferably PRIORITY or NEW

---

## LOCKED (NEVER CHANGE)

name · style · all 10 pairs · max_open=3 · size_pct=10 · fee_rate=0.001
all operators (lt / gt / eq) · all indicator types · all period_minutes
all eq values (true / bullish / bearish / above / below / up / down)
condition count = 5 long + 5 short
```

---