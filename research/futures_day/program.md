```markdown
# ODIN — FUTURES DAY v35.0
# ONE TASK: change take_profit_pct from 4.6 to 5.0. Nothing else.

## OUTPUT THESE TWO LINES FIRST:
CHANGE: take_profit_pct 4.6 → 5.0
USING: size_pct=8, rsi_long=29.33, rsi_short=68.63, stop_loss=2.59, tp=5.0

## THEN OUTPUT THIS YAML EXACTLY (only take_profit_pct changes):

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
      value: 29.33
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 68.63
exit:
  take_profit_pct: 5.0
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

## VERIFY BEFORE SUBMITTING — all must be true:
- take_profit_pct = 5.0  (changed from 4.6)
- stop_loss_pct = 2.59   (unchanged)
- size_pct = 8           (unchanged)
- rsi long value = 29.33 (unchanged)
- rsi short value = 68.63 (unchanged)
- timeout_minutes = 720  (unchanged)
- pairs list = 16 pairs  (unchanged)

## FORBIDDEN VALUES — if you wrote any of these, STOP and use the YAML above:
- size_pct = 16.91   → INVALID
- rsi long = 35.97   → INVALID
- rsi short = 72     → INVALID
- stop_loss = 2.39   → INVALID
- take_profit = 4.6  → INVALID (must be 5.0)

## CHAMPION CONTEXT:
- Current champion: Gen 3233, Sharpe=0.4066, 1756 trades, WR=50.1%
- Your goal: Sharpe > 0.4066 with take_profit_pct=5.0

## ROADMAP (after this step succeeds):
- Step 2: TP 5.0 → 5.5
- Step 3: TP 5.5 → 6.0
- Step 4: TP 6.0 → 7.0
- If 3 TP steps fail: test rsi_long 29.33 → 32.0

## SYSTEM CONSTANT (never change):
- MIN_TRADES[futures_day] = 50 — FROZEN. Do not raise.
```

---