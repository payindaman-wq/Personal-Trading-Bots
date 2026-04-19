```markdown
# ODIN Day League Research Program
# v11100-champion-tune

═══════════════════════════════════════════════════════════════
COPY THIS YAML EXACTLY. Change ONLY the values listed in Step 2.
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
      value: -1.21        # ← LONG THRESHOLD (negative, see table)
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
      value: 1.16         # ← SHORT THRESHOLD (positive, see table)
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
  take_profit_pct: 3.51   # ← TP (see table)
  stop_loss_pct: 0.37     # ← SL (see table)
  timeout_minutes: 706    # ← TIMEOUT (see table)
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

═══════════════════════════════════════════════════════════════
STEP 1 — VERIFY BEFORE SUBMITTING
═══════════════════════════════════════════════════════════════

  long price_change_pct operator  = lt     (NOT gt)
  long price_change_pct value     = negative number
  short price_change_pct operator = gt     (NOT lt)
  short price_change_pct value    = positive number
  pairs count = 10 (do NOT add or remove pairs)
  conditions count = 5 long, 5 short (do NOT add or remove)

If ANY are wrong → DELETE and restart from the YAML above.

═══════════════════════════════════════════════════════════════
STEP 2 — FIVE VALUES THAT CHANGE BY TARGET
═══════════════════════════════════════════════════════════════

Only these five values change. Nothing else, ever.

| Target | long.value | short.value | take_profit | stop_loss | timeout |
|--------|------------|-------------|-------------|-----------|---------|
| A1     | -1.21      | 1.16        | 3.51        | 0.37      | 706     | ← CURRENT CHAMPION
| A2     | -1.18      | 1.16        | 3.51        | 0.37      | 706     |
| A3     | -1.24      | 1.16        | 3.51        | 0.37      | 706     |
| A4     | -1.21      | 1.13        | 3.51        | 0.37      | 706     |
| A5     | -1.21      | 1.19        | 3.51        | 0.37      | 706     |
| B1     | -1.21      | 1.16        | 3.75        | 0.37      | 706     |
| B2     | -1.21      | 1.16        | 3.25        | 0.37      | 706     |
| B3     | -1.21      | 1.16        | 3.51        | 0.40      | 706     |
| B4     | -1.21      | 1.16        | 3.51        | 0.34      | 706     |
| C1     | -1.21      | 1.16        | 3.51        | 0.37      | 660     |
| C2     | -1.21      | 1.16        | 3.51        | 0.37      | 750     |
| C3     | -1.18      | 1.13        | 3.75        | 0.37      | 706     |
| C4     | -1.24      | 1.19        | 3.25        | 0.40      | 706     |

Run 8 reps per target before advancing. A rep = any result with trades ≤ 450.

═══════════════════════════════════════════════════════════════
STEP 3 — ACCEPTANCE
═══════════════════════════════════════════════════════════════

Champion: Sharpe = 1.1739, trades = 310 (gen 10391).
Beat it: Sharpe > 1.1739 AND trades ≥ 280.

| Result                      | Tag                   | Counts as rep? |
|-----------------------------|-----------------------|----------------|
| trades > 450                | [structural_failure]  | NO             |
| trades < 280                | [low_trades]          | YES            |
| 280 ≤ trades ≤ 450, S<1.17 | [discarded]           | YES            |
| 280 ≤ trades ≤ 450, S>1.17 | [new_best] — deploy   | YES            |

MIN_TRADES = 280. Final. Do not change.

═══════════════════════════════════════════════════════════════
NEVER CHANGE THESE FIELDS
═══════════════════════════════════════════════════════════════

name, style, pairs (all 10 above), max_open=3, size_pct=10, fee_rate=0.001,
all operators (lt/gt/eq), all indicator types, all period_minutes values,
all eq values (true/bullish/bearish/above/below/up/down),
total conditions = 5 long + 5 short.

═══════════════════════════════════════════════════════════════
FAILURE FINGERPRINTS — DIAGNOSE FAST
═══════════════════════════════════════════════════════════════

  trades > 450            → operator inverted or threshold loosened; DELETE, restart
  trades < 140, sharpe<0  → long.value is 0 or positive; DELETE, restart
  trades = 0              → YAML malformed; DELETE, restart
  sharpe < -10            → entry conditions destroyed; DELETE, restart
  dedup_reject            → choose a different target row from the table above
```

---