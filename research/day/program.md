```markdown
# ODIN Day League Research Program
# v11100-champion-refine

═══════════════════════════════════════════════════════════════
CANONICAL CHAMPION — DO NOT MODIFY THIS BLOCK
═══════════════════════════════════════════════════════════════

Sharpe = 1.1227 | Trades = 309 | Gen 9325
Beat it: Sharpe > 1.1227 AND trades ≥ 280

═══════════════════════════════════════════════════════════════
TEMPLATE — COPY EXACTLY, CHANGE ONLY STEP 2 VALUES
═══════════════════════════════════════════════════════════════

```yaml
name: crossover
style: momentum_optimized
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
      value: LONG_PCT       # ← REPLACE with negative number from table
    - indicator: macd_signal
      period_minutes: MACD_PERIOD   # ← REPLACE with period from table
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
      value: SHORT_PCT      # ← REPLACE with positive number from table
    - indicator: macd_signal
      period_minutes: MACD_PERIOD   # ← REPLACE with period from table
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
  take_profit_pct: 3.51
  stop_loss_pct: 0.37
  timeout_minutes: 706
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

═══════════════════════════════════════════════════════════════
STEP 1 — VERIFY BEFORE SUBMITTING (mandatory)
═══════════════════════════════════════════════════════════════

  long  price_change_pct operator  = lt    (NOT gt — if gt, DELETE and restart)
  long  price_change_pct value     < 0     (NEGATIVE — if zero or positive, DELETE)
  short price_change_pct operator  = gt    (NOT lt — if lt, DELETE and restart)
  short price_change_pct value     > 0     (POSITIVE — if zero or negative, DELETE)

═══════════════════════════════════════════════════════════════
STEP 2 — ONLY THESE THREE VALUES CHANGE
═══════════════════════════════════════════════════════════════

| Target | LONG_PCT | SHORT_PCT | MACD_PERIOD |
|--------|----------|-----------|-------------|
| A1     | -1.21    | 1.16      | 30          | ← CURRENT CHAMPION
| A2     | -1.10    | 1.10      | 30          |
| A3     | -1.30    | 1.30      | 30          |
| A4     | -1.00    | 1.00      | 30          |
| A5     | -1.40    | 1.40      | 30          |
| B1     | -1.21    | 1.16      | 45          |
| B2     | -1.10    | 1.10      | 45          |
| B3     | -1.30    | 1.30      | 45          |
| C1     | -1.21    | 1.16      | 60          |
| C2     | -1.00    | 1.00      | 60          |

Run 8 reps per target before advancing. A rep = any result with trades ≤ 450.

═══════════════════════════════════════════════════════════════
STEP 3 — ACCEPTANCE RULES
═══════════════════════════════════════════════════════════════

MIN_TRADES = 280. FINAL. DO NOT CHANGE.

| Result                              | Tag                  | Rep? |
|-------------------------------------|----------------------|------|
| trades > 450                        | [structural_failure] | NO   |
| trades < 280                        | [low_trades]         | YES  |
| 280 ≤ trades ≤ 450, Sharpe < 1.1227 | [discarded]          | YES  |
| 280 ≤ trades ≤ 450, Sharpe > 1.1227 | [new_best] → deploy  | YES  |

═══════════════════════════════════════════════════════════════
NEVER CHANGE THESE FIELDS
═══════════════════════════════════════════════════════════════

name, style, pairs (exactly 10 listed), max_open=3, size_pct=10,
fee_rate=0.001, take_profit_pct=3.51, stop_loss_pct=0.37,
timeout_minutes=706, momentum_accelerating period=60,
price_vs_ema long period=60, price_vs_ema short period=120,
trend period=240, total conditions=5 long + 5 short = 10 total.

═══════════════════════════════════════════════════════════════
FAILURE FINGERPRINTS
═══════════════════════════════════════════════════════════════

  trades=1011, sharpe=-0.2625 → long operator is gt (should be lt). DELETE.
  trades > 450                → operator error or extra conditions. DELETE.
  trades < 140, sharpe < 0   → long value is 0 or positive. DELETE.
  trades = 0                  → YAML malformed.
  Sharpe > 1.17, trades < 280 → promising but low_trades; tighten nothing further.
```

---