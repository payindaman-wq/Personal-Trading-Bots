```markdown
# ODIN Day League — v11680

## TEMPLATE — COPY THIS EXACTLY, THEN CHANGE ONLY MARKED VALUES

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

## STEP 1 — VERIFY BEFORE SUBMITTING (all 4 must pass)

1. long price_change_pct value is NEGATIVE ✓
2. short price_change_pct value is POSITIVE ✓
3. long operator = lt, short operator = gt ✓
4. All 5 values come from ONE row in the table below ✓

**If any check fails → DELETE output and restart.**

---

## STEP 2 — PICK EXACTLY ONE ROW

**Champion: Sharpe=1.1731, trades=310**
**Goal: Sharpe > 1.1731 AND trades ≥ 280**

**PICK FROM PRIORITY OR NEW ROWS ONLY. Do NOT repeat the champion row (A1) or any "tested" row.**

| ID | long.value | short.value | take_profit | stop_loss | timeout | Status |
|----|------------|-------------|-------------|-----------|---------|--------|
| A1 | -1.21 | 1.16 | 3.51 | 0.37 | 706 | CHAMPION — DO NOT PICK |
| B5 | -1.21 | 1.16 | 3.51 | 0.31 | 706 | PRIORITY |
| B6 | -1.21 | 1.16 | 4.00 | 0.37 | 706 | PRIORITY |
| B7 | -1.21 | 1.16 | 3.51 | 0.43 | 706 | PRIORITY |
| C3 | -1.18 | 1.13 | 3.75 | 0.37 | 706 | PRIORITY |
| C4 | -1.24 | 1.19 | 3.25 | 0.40 | 706 | PRIORITY |
| C5 | -1.21 | 1.16 | 3.51 | 0.37 | 800 | PRIORITY |
| C6 | -1.21 | 1.16 | 3.51 | 0.37 | 600 | PRIORITY |
| D2 | -1.24 | 1.16 | 3.25 | 0.37 | 706 | PRIORITY |
| D3 | -1.21 | 1.13 | 3.51 | 0.34 | 706 | PRIORITY |
| D4 | -1.21 | 1.19 | 3.51 | 0.40 | 706 | PRIORITY |
| D6 | -1.24 | 1.16 | 3.51 | 0.40 | 660 | PRIORITY |
| D7 | -1.21 | 1.13 | 3.75 | 0.37 | 750 | PRIORITY |
| D8 | -1.21 | 1.19 | 3.25 | 0.37 | 660 | PRIORITY |
| E1 | -1.21 | 1.16 | 3.51 | 0.28 | 706 | NEW ← EXPLORE FIRST |
| E2 | -1.21 | 1.16 | 3.51 | 0.46 | 706 | NEW |
| E3 | -1.21 | 1.16 | 3.51 | 0.37 | 850 | NEW |
| E4 | -1.21 | 1.16 | 3.51 | 0.37 | 550 | NEW |
| E5 | -1.21 | 1.16 | 4.25 | 0.37 | 706 | NEW ← EXPLORE FIRST |
| E6 | -1.21 | 1.16 | 3.00 | 0.34 | 706 | NEW |
| E7 | -1.18 | 1.13 | 3.51 | 0.37 | 750 | NEW |
| E8 | -1.24 | 1.19 | 3.51 | 0.37 | 660 | NEW |
| F1 | -1.15 | 1.16 | 3.51 | 0.37 | 706 | NEW |
| F2 | -1.27 | 1.16 | 3.51 | 0.37 | 706 | NEW |
| F3 | -1.21 | 1.10 | 3.51 | 0.37 | 706 | NEW |
| F4 | -1.21 | 1.22 | 3.51 | 0.37 | 706 | NEW |
| F5 | -1.18 | 1.16 | 3.75 | 0.34 | 750 | NEW |
| F6 | -1.24 | 1.16 | 3.25 | 0.40 | 660 | NEW |

**RECENTLY SUBMITTED (DO NOT RESUBMIT THESE):**
- A1: -1.21 / 1.16 / 3.51 / 0.37 / 706 (champion)
- Any row already marked "tested" in the full history

**If you are unsure which rows have been tried: pick E1, E5, F1, F2, F3, or F4 — these are confirmed untested.**

---

## STEP 3 — RESULT TAGS

| Result | Tag | Rep? |
|--------|-----|------|
| trades > 450 | [structural_failure] — DELETE, restart | NO |
| trades < 280 | [low_trades] — discard | YES |
| 280 ≤ trades ≤ 450, Sharpe ≤ 1.1731 | [discarded] | YES |
| 280 ≤ trades ≤ 450, Sharpe > 1.1731 | [new_best] → deploy | YES |

**trades > 450 means you used an out-of-table value. Delete and use a table row.**

---

## LOCKED — NEVER CHANGE

name · style · all 10 pairs · max_open=3 · size_pct=10 · fee_rate=0.001
All operators (lt / gt / eq) · all indicator types · all period_minutes
All eq values (true / bullish / bearish / above / below / up / down)
Condition count: exactly 5 long + 5 short
```

---