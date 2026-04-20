```markdown
# ODIN — FUTURES DAY v40.0

## STEP 1 — MAKE EXACTLY THIS CHANGE

**Change `entry.short.conditions[0].value` from `68.63` to `66.0`**

Fallback chain (if value is BANNED):
- Try `64.0` → if banned, try `62.0` → if banned, change `exit.stop_loss_pct` to `2.3`

## STEP 2 — OUTPUT FORMAT (nothing else)

CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=[value], stop_loss=2.59, tp=4.6
[YAML below with exactly ONE value changed]

## STEP 3 — CHAMPION YAML (copy exactly, change ONE value only)

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
  take_profit_pct: 4.6
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

## BANNED VALUES — instant reject if used

| Field | Banned values |
|-------|--------------|
| entry.short.conditions[0].value | 68.63 |
| entry.long.conditions[0].value | 29.33, 32.0, 35.97 |
| position.size_pct | 8, 16.91 |
| exit.stop_loss_pct | 2.59, 2.39 |
| exit.take_profit_pct | 4.6, 5.0 |
| timeout_minutes | 720 |
| leverage | 2 |
| fee_rate | 0.0005 |

## TESTED AND FAILED — do not resubmit

| Change | Result |
|--------|--------|
| rsi_short=68.63 | champion (banned) |
| rsi_long=32.0 | Sharpe=0.296 |
| rsi_long=35.97 | failed |
| size_pct=16.91 | failed |
| stop_loss_pct=2.39 | failed |
| take_profit_pct=5.0 | Sharpe=0.021 |

## PREFLIGHT (check all before outputting)

- [ ] Exactly ONE value differs from champion YAML
- [ ] Changed value NOT in BANNED list
- [ ] Changed value NOT in TESTED AND FAILED list
- [ ] All 16 pairs present, same order
- [ ] fee_rate=0.0005, leverage=2 (never change these)
- [ ] timeout_minutes=720 (never change)
- [ ] YAML structure identical to champion

## CONTEXT

Champion: Gen 3233 | Sharpe=0.4066 | 1756 trades | WR=50.1%
Goal: Sharpe > 0.4066
League: futures_day | MIN_TRADES=50

Priority ladder (first untested wins — pick ONE):
1. rsi_short → 66.0
2. rsi_short → 64.0
3. rsi_short → 62.0
4. stop_loss_pct → 2.3
5. size_pct → 10
6. take_profit_pct → 4.2
7. rsi_long → 27.0
8. stop_loss_pct → 2.8
9. rsi_short → 70.0
10. take_profit_pct → 4.8
```

---