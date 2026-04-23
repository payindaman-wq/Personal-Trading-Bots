```markdown
# ODIN Day League — v11681

## TEMPLATE — OUTPUT THIS EXACT STRUCTURE, CHANGE ONLY MARKED VALUES

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
      period_minutes: 60
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

## LOCKED — NEVER CHANGE THESE (violation = structural_failure)

- name, style, all 10 pairs, max_open=3, size_pct=10, fee_rate=0.001
- All operators (lt / gt / eq)
- All indicator types and period_minutes values
- All eq values (true / bullish / bearish / above / below / up / down)
- Condition count: exactly 5 long + 5 short

**You may ONLY change the 5 values marked with ← CHANGE THIS.**

---

## STEP 1 — VERIFY (all 3 must pass before submitting)

1. long price_change_pct value is NEGATIVE ✓
2. short price_change_pct value is POSITIVE ✓
3. All 5 changed values come from ONE row in the table below ✓

**If any check fails → DELETE output and restart from template.**

---

## STEP 2 — PICK EXACTLY ONE ROW

**Champion: Sharpe=1.1227, trades=309**
**Goal: Sharpe > 1.1227 AND trades ≥ 280**

| ID | long.value | short.value | take_profit | stop_loss | timeout | Status |
|----|------------|-------------|-------------|-----------|---------|--------|
| A1 | -1.21 | 1.16 | 3.51 | 0.37 | 706 | CHAMPION — DO NOT PICK |
| E1 | -1.21 | 1.16 | 3.51 | 0.28 | 706 | PRIORITY |
| E2 | -1.21 | 1.16 | 3.51 | 0.46 | 706 | PRIORITY |
| E3 | -1.21 | 1.16 | 3.51 | 0.37 | 850 | PRIORITY |
| E4 | -1.21 | 1.16 | 3.51 | 0.37 | 550 | PRIORITY |
| E5 | -1.21 | 1.16 | 4.25 | 0.37 | 706 | PRIORITY |
| E6 | -1.21 | 1.16 | 3.00 | 0.34 | 706 | PRIORITY |
| E7 | -1.18 | 1.13 | 3.51 | 0.37 | 750 | PRIORITY |
| E8 | -1.24 | 1.19 | 3.51 | 0.37 | 660 | PRIORITY |
| F1 | -1.15 | 1.16 | 3.51 | 0.37 | 706 | PRIORITY |
| F2 | -1.27 | 1.16 | 3.51 | 0.37 | 706 | PRIORITY |
| F3 | -1.21 | 1.10 | 3.51 | 0.37 | 706 | PRIORITY |
| F4 | -1.21 | 1.22 | 3.51 | 0.37 | 706 | PRIORITY |
| F5 | -1.18 | 1.16 | 3.75 | 0.34 | 750 | PRIORITY |
| F6 | -1.24 | 1.16 | 3.25 | 0.40 | 660 | PRIORITY |
| G1 | -1.21 | 1.16 | 3.75 | 0.34 | 706 | NEW |
| G2 | -1.21 | 1.16 | 3.25 | 0.40 | 706 | NEW |
| G3 | -1.21 | 1.16 | 4.00 | 0.34 | 706 | NEW |
| G4 | -1.21 | 1.16 | 3.51 | 0.31 | 750 | NEW |
| G5 | -1.18 | 1.19 | 3.51 | 0.37 | 706 | NEW |
| G6 | -1.24 | 1.13 | 3.51 | 0.37 | 706 | NEW |
| G7 | -1.21 | 1.16 | 4.50 | 0.37 | 706 | NEW |
| G8 | -1.21 | 1.16 | 3.51 | 0.43 | 800 | NEW |

**If unsure which rows are untested: pick E1, E2, E5, F1, F2, F3, or F4 — confirmed untested.**

**DO NOT pick A1. DO NOT invent values outside this table.**

---

## STEP 3 — RESULT TAGS

| Result | Tag |
|--------|-----|
| trades > 450 | [structural_failure] — you changed a LOCKED value. DELETE and restart. |
| trades < 280 | [low_trades] |
| 280 ≤ trades ≤ 450, Sharpe ≤ 1.1227 | [discarded] |
| 280 ≤ trades ≤ 450, Sharpe > 1.1227 | [new_best] → deploy |

**trades > 450 = structural failure. You changed something locked. Start over.**
```