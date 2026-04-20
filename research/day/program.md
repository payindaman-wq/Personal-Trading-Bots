```markdown
# ODIN Day League Research Program
# v11200-table-expand

═══════════════════════════════════════════════════════════════
TEMPLATE — COPY EXACTLY, THEN CHANGE ONLY STEP 2 VALUES
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
      value: -1.21        # ← LONG THRESHOLD
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
      value: 1.16         # ← SHORT THRESHOLD
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
CRITICAL CHECKS — VERIFY BEFORE SUBMITTING
═══════════════════════════════════════════════════════════════

  long price_change_pct operator  = lt     (NOT gt)
  long price_change_pct value     = NEGATIVE number (e.g. -1.21)
  short price_change_pct operator = gt     (NOT lt)
  short price_change_pct value    = POSITIVE number (e.g. 1.16)
  pairs count = 10 (unchanged)
  conditions = 5 long, 5 short (unchanged)
  Values MUST come from the table below — no invented values

If ANY check fails → DELETE and restart from template above.

═══════════════════════════════════════════════════════════════
STEP 2 — USE EXACTLY ONE ROW FROM THIS TABLE
═══════════════════════════════════════════════════════════════

Champion: Sharpe=1.1739, trades=310 (A1) — beat with Sharpe > 1.1739 AND trades ≥ 280

| Target | long.value | short.value | take_profit | stop_loss | timeout |
|--------|------------|-------------|-------------|-----------|---------|
| A1     | -1.21      | 1.16        | 3.51        | 0.37      | 706     | ← CHAMPION
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

Run 8 reps per target before advancing. A rep = any result with trades ≤ 450.

═══════════════════════════════════════════════════════════════
STEP 3 — ACCEPTANCE RULES
═══════════════════════════════════════════════════════════════

| Result                        | Tag                  | Counts as rep? |
|-------------------------------|----------------------|----------------|
| trades > 450                  | [structural_failure] | NO             |
| trades < 280                  | [low_trades]         | YES            |
| 280 ≤ trades ≤ 450, S ≤ 1.1739 | [discarded]        | YES            |
| 280 ≤ trades ≤ 450, S > 1.1739 | [new_best] → deploy | YES           |

MIN_TRADES = 280. Final. Do not change.

═══════════════════════════════════════════════════════════════
FAILURE FINGERPRINTS — IF YOU SEE THESE, DELETE AND RESTART
═══════════════════════════════════════════════════════════════

  trades > 450        → threshold outside table range; DELETE, restart
  trades = 0          → YAML malformed; DELETE, restart
  sharpe < -10        → entry conditions broken; DELETE, restart
  long.value > 0      → sign error; DELETE, restart
  dedup_reject        → pick a different row from the table (never invent values)

═══════════════════════════════════════════════════════════════
NEVER CHANGE THESE (LOCKED)
═══════════════════════════════════════════════════════════════

name, style, all 10 pairs, max_open=3, size_pct=10, fee_rate=0.001,
all operators (lt/gt/eq), all indicator types, all period_minutes,
all eq values (true/bullish/bearish/above/below/up/down),
condition count = 5 long + 5 short.
```

---