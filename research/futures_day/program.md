```markdown
# ODIN — FUTURES DAY v37.0

## YOUR ONLY JOB: Output the YAML below with ONE value changed.

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
      value: 66.0
exit:
  take_profit_pct: 4.6
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

## CHANGE MADE
CHANGE: rsi_short 68.63 → 66.0
USING: size_pct=8, rsi_long=29.33, rsi_short=66.0, stop_loss=2.59, tp=4.6

## WHAT CHANGED (exactly one value)
- entry.short.conditions[0].value: 68.63 → 66.0
- Everything else is IDENTICAL to the champion

## TESTED AND FAILED — DO NOT USE THESE VALUES
- rsi_short=68.63 (champion value — do not submit unchanged)
- rsi_long=32.0 (tested Gen 3903/3916: Sharpe=0.296 < 0.4066 — FAILED)
- tp=5.0 (tested Gen 3770: Sharpe=0.0213 — FAILED)
- rsi_long=35.97 → BANNED
- size_pct=16.91 → BANNED
- stop_loss=2.39 → BANNED

## CHAMPION CONTEXT
- Champion: Gen 3233, Sharpe=0.4066, 1756 trades, WR=50.1%
- Goal: Sharpe > 0.4066
- MIN_TRADES[futures_day] = 50 — FROZEN

## ROADMAP
- Step 3 (NOW): rsi_short 68.63 → 66.0  ← YOU ARE HERE
- Step 4: If Step 3 fails → rsi_short 66.0 → 64.0
- Step 5: If Step 4 fails → stop_loss 2.59 → 2.3
- Step 6: If Step 5 fails → size_pct 8 → 10

## OUTPUT FORMAT
Output CHANGE line, USING line, then the YAML. Nothing else.
```

---