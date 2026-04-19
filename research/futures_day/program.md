```markdown
# ODIN — FUTURES DAY v36.0
# PIVOT: TP=5.0 tested and failed (Gen 3770: Sharpe=0.0213 < champion 0.4066)
# NEW TASK: Change rsi_long from 29.33 to 32.0. Nothing else.

## OUTPUT THESE TWO LINES FIRST:
CHANGE: rsi_long 29.33 → 32.0
USING: size_pct=8, rsi_long=32.0, rsi_short=68.63, stop_loss=2.59, tp=4.6

## OUTPUT THIS YAML EXACTLY (only rsi long value changes):

```yaml
name: crossover
style: mean_reversion_swing
league: futures_day
leverage: 2
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
  size_pct: 8
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 32.0
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 68.63
exit:
  take_profit_pct: 4.6
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

## VERIFY BEFORE SUBMITTING — all must be true:
- rsi long value = 32.0   (changed from 29.33)
- rsi short value = 68.63 (unchanged)
- take_profit_pct = 4.6   (unchanged)
- stop_loss_pct = 2.59    (unchanged)
- size_pct = 8            (unchanged)
- timeout_minutes = 720   (unchanged)
- pairs list = 16 pairs   (unchanged)

## FORBIDDEN VALUES — if you wrote any of these, STOP and use the YAML above:
- rsi long = 29.33   → INVALID (must be 32.0)
- rsi long = 35.97   → INVALID
- rsi short = 72     → INVALID
- size_pct = 16.91   → INVALID
- stop_loss = 2.39   → INVALID
- take_profit = 5.0  → INVALID (TP=5.0 already failed, use 4.6)

## CHAMPION CONTEXT:
- Current champion: Gen 3233, Sharpe=0.4066, 1756 trades, WR=50.1%
- Goal: Sharpe > 0.4066
- TP=5.0 was tested (Gen 3770): Sharpe=0.0213 — FAILED, do not retry

## ROADMAP:
- Step 1 (NOW): rsi_long 29.33 → 32.0
- Step 2: If Step 1 succeeds → rsi_long 32.0 → 34.0
- Step 3: If Step 1 fails → rsi_short 68.63 → 66.0
- Step 4: If both RSI steps fail → stop_loss 2.59 → 2.3

## SYSTEM CONSTANT (never change):
- MIN_TRADES[futures_day] = 50 — FROZEN. Do not raise.
```

---