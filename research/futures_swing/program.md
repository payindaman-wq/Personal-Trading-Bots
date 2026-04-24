```markdown
# ODIN Research Program — FUTURES SWING
# GROUND TRUTH (elite_0.yaml): Sharpe=0.7001 | Trades=486 | OOS_Sharpe=1.8971
# OOS gate is ACTIVE: candidates must achieve OOS sharpe ≥ 1.8971 to be accepted.
# This is the BINDING constraint — most discards fail OOS, not in-sample.

## OUTPUT RULE
Output ONLY the modified YAML. ONE value changed. Nothing else.

---
## TEMPLATE — ACTUAL CURRENT CHAMPION — COPY EXACTLY, CHANGE EXACTLY ONE VALUE

```yaml
name: crossover
style: swing_momentum
league: futures_swing
leverage: 2
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
position:
  size_pct: 25
  max_open: 3
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: up
    - indicator: rsi
      period_hours: 24
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24
      operator: gt
      value: 60
exit:
  take_profit_pct: 5.2
  stop_loss_pct: 1.92
  timeout_hours: 166
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

---
## HARD LIMITS — VIOLATION = DISCARD

| Parameter | Allowed Range |
|---|---|
| stop_loss_pct | 1.45 – 2.50 |
| take_profit_pct | 3.0 – 8.0 |
| rsi long (lt) | 35 – 45 |
| rsi short (gt) | 55 – 70 |
| rsi_period_hours | 18 – 30 |
| timeout_hours | 48 – 210 |
| size_pct | 18 – 25 |
| pairs | exactly [BTC/USD, ETH/USD, SOL/USD] |
| fee_rate / max_open / leverage | DO NOT CHANGE |
| Minimum trades | ≥ 400 |

---
## KEY FACTS — READ BEFORE CHOOSING

- Champion: TP=5.20, SL=1.92, ratio=2.71. RSI long=37.77, RSI short=60.0, timeout=166h
- Win rate is structurally ~33–38% — do not try to change this
- Trade count ~486 — stay above 400
- OOS sharpe ≥ 1.8971 is REQUIRED for any improvement to be accepted
- OOS stability favors: higher TP/SL ratio, tighter RSI thresholds, longer timeouts
- Recent best: Gen 6436 sharpe=1.1223 with 435 trades — tighter RSI helps quality

---
## WHAT TO CHANGE — PICK EXACTLY ONE

**Current: TP=5.20, SL=1.92, ratio=2.71. RSI long=37.77, RSI short=60.0, timeout=166h.**

### PRIORITY 1 — take_profit_pct (current: 5.20) — HIGHEST PRIORITY
Higher TP improves ratio and OOS stability. Try:
**5.40 | 5.50 | 5.60 | 5.70 | 5.80 | 6.00 | 5.00 | 4.90**

### PRIORITY 2 — stop_loss_pct (current: 1.92)
Tighter SL improves ratio. Minimum allowed 1.45.
**1.45 | 1.50 | 1.55 | 1.60 | 1.65 | 1.70 | 1.75 | 1.80**

### PRIORITY 3 — RSI long lt (current: 37.77)
Lower = fewer but cleaner trades (better OOS). Higher = more trades (watch 400 floor).
**35.0 | 36.0 | 37.0 | 38.0 | 39.0 | 40.0 | 41.0 | 42.0**

### PRIORITY 4 — RSI short gt (current: 60.0)
Higher = cleaner short signal.
**61 | 62 | 63 | 64 | 65 | 58 | 57 | 56**

### PRIORITY 5 — timeout_hours (current: 166)
Longer timeout may recover missed trades.
**172 | 176 | 180 | 184 | 188 | 192 | 156 | 148**

### PRIORITY 6 — rsi_period_hours (current: 24)
**20 | 21 | 22 | 23 | 25 | 26 | 27 | 28**

### PRIORITY 7 — trend period_hours (current: 48)
**36 | 42 | 54 | 60 | 72**

### PRIORITY 8 — size_pct (current: 25)
**24 | 23 | 22 | 21 | 20**

---
## KNOWN BAD — DO NOT USE

- stop_loss_pct < 1.45 → below noise floor
- rsi long lt < 35 → too few trades (< 400)
- rsi long lt > 45 → too many noisy entries
- timeout_hours > 210 or < 48 → rejected
- Any pairs other than [BTC/USD, ETH/USD, SOL/USD] → rejected
- DO NOT reproduce champion unchanged:
  take_profit_pct=5.2, stop_loss_pct=1.92, timeout_hours=166,
  rsi_lt=37.77, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=25

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template
- [ ] Changed value is NOT in KNOWN BAD list
- [ ] stop_loss_pct between 1.45 and 2.50
- [ ] rsi long lt between 35 and 45
- [ ] rsi short gt between 55 and 70
- [ ] timeout_hours between 48 and 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```