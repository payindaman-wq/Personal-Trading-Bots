```markdown
# ODIN Day League — v12001

## CRITICAL: READ BEFORE ANYTHING ELSE

**True Champion (elite_0.yaml):** Sharpe=1.1205 | trades=316 | stop_loss=0.28 | size_pct=13.98
**Goal:** Sharpe > 1.1205 AND trades ≥ 280

**LIVE ALERT:** Zero trades in last 2 sprints. Entry conditions may be too tight for current market.
Priority: find configs that fire more reliably while maintaining Sharpe > 1.12.

---

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
  size_pct: 13.98
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
      value: -1.21        # ← CHANGE THIS (MUST be negative, range -2.0 to -0.80)
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
      value: 1.16         # ← CHANGE THIS (MUST be positive, range 0.80 to 2.0)
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
  take_profit_pct: 3.51   # ← CHANGE THIS (range 2.50 to 5.00)
  stop_loss_pct: 0.28     # ← CHANGE THIS (range 0.22 to 0.55)
  timeout_minutes: 706    # ← CHANGE THIS (range 400 to 900)
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

---

## LOCKED — NEVER CHANGE (violation = structural_failure, trades > 450)

- name, style, ALL 10 pairs, max_open=3, size_pct=13.98, fee_rate=0.001
- All operators (lt / gt / eq)
- All indicator types and ALL period_minutes values
- All eq values (true / bullish / bearish / above / below / up / down)
- Condition count: exactly 5 long + 5 short

**You may ONLY change the 5 values marked with ← CHANGE THIS.**

---

## STEP 1 — VERIFY BEFORE SUBMITTING (all 3 must pass)

1. long price_change_pct value is NEGATIVE ✓
2. short price_change_pct value is POSITIVE ✓
3. All 5 changed values come from ONE row in the table below ✓

**If any check fails → DELETE output and restart from template.**

---

## STEP 2 — PICK EXACTLY ONE ROW

| ID | long.value | short.value | take_profit | stop_loss | timeout | Status |
|----|------------|-------------|-------------|-----------|---------|--------|
| A1 | -1.21 | 1.16 | 3.51 | 0.28 | 706 | CHAMPION — DO NOT PICK |
| H1 | -1.10 | 1.16 | 3.51 | 0.28 | 706 | PRIORITY — loosen long entry |
| H2 | -1.15 | 1.16 | 3.51 | 0.28 | 706 | PRIORITY — loosen long entry |
| H3 | -1.10 | 1.10 | 3.51 | 0.28 | 706 | PRIORITY — loosen both entries |
| H4 | -1.10 | 1.16 | 3.75 | 0.28 | 600 | PRIORITY — loosen + tighter timeout |
| H5 | -1.15 | 1.13 | 3.51 | 0.32 | 706 | PRIORITY — coordinated relax |
| H6 | -1.21 | 1.16 | 3.51 | 0.24 | 706 | PRIORITY — tighter stop |
| H7 | -1.21 | 1.16 | 3.51 | 0.32 | 550 | PRIORITY — shorter timeout |
| H8 | -1.10 | 1.16 | 3.51 | 0.32 | 550 | PRIORITY — loosen + short TO |
| H9 | -1.21 | 1.16 | 4.00 | 0.28 | 706 | PRIORITY — higher TP |
| H10 | -1.21 | 1.16 | 3.00 | 0.28 | 500 | PRIORITY — lower TP, short TO |
| H11 | -0.90 | 1.16 | 3.51 | 0.28 | 706 | NEW — very loose long |
| H12 | -1.10 | 1.20 | 3.75 | 0.25 | 650 | NEW — coordinated |
| H13 | -1.21 | 1.16 | 3.51 | 0.22 | 800 | NEW — very tight stop |
| H14 | -1.15 | 1.15 | 4.25 | 0.30 | 600 | NEW — balanced relax |
| H15 | -1.10 | 1.10 | 4.00 | 0.30 | 650 | NEW — symmetric loosen |
| H16 | -1.21 | 1.16 | 2.75 | 0.28 | 450 | NEW — quick exits |
| H17 | -1.05 | 1.16 | 3.51 | 0.28 | 706 | NEW — aggressive long relax |
| H18 | -1.21 | 1.05 | 3.51 | 0.28 | 706 | NEW — aggressive short relax |
| H19 | -1.15 | 1.16 | 3.51 | 0.28 | 500 | NEW — loosen + 500 TO |
| H20 | -1.10 | 1.16 | 3.25 | 0.26 | 750 | NEW — loosen + tight stop/TP |

**Pick any PRIORITY row first. If all PRIORITY tested, pick any NEW row.**
**DO NOT pick A1. DO NOT invent values outside this table.**

---

## DESIGN RATIONALE (why these rows)

The champion uses stop_loss=0.28 (tight). Previous table explored stop_loss=0.37 (wrong baseline).
Key hypothesis: entry conditions are too restrictive → zero live trades in 2 sprints.
Loosening price_change_pct (long toward -1.10, short toward 1.10) should increase trade frequency
while maintaining signal quality if paired with the tight 0.28 stop.
Target: 310-380 trades in backtest (current: 316). Sharpe must beat 1.1205.

---

## STEP 3 — RESULT TAGS

| Result | Tag |
|--------|-----|
| trades > 450 | [structural_failure] — you changed a LOCKED value. DELETE and restart. |
| trades < 280 | [low_trades] |
| 280 ≤ trades ≤ 450, Sharpe ≤ 1.1205 | [discarded] |
| 280 ≤ trades ≤ 450, Sharpe > 1.1205 | [new_best] → deploy |
```