```markdown
# ODIN Research Program — FUTURES SWING
# GROUND TRUTH (elite_0.yaml): Sharpe=0.9057 | Trades=678 | OOS_Sharpe=2.3434
# OOS gate ACTIVE: candidates must achieve OOS sharpe ≥ 2.3434 to be accepted.
# Most discards fail OOS — optimize for OOS stability, not in-sample Sharpe.

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
      value: 42.0
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
  stop_loss_pct: 1.5
  timeout_hours: 120
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
## KEY FACTS

- Champion: TP=5.20, SL=1.50, ratio=3.47. RSI long=42.0, RSI short=60.0, timeout=120h
- OOS Sharpe=2.3434 >> in-sample=0.9057 — strategy already has strong OOS quality
- Win rate ~33–34%. Trade count ~678. Both are healthy — do not try to change these.
- OOS gate floor = 2.3434. Changes that improve in-sample but hurt OOS will be REJECTED.
- OOS stability is helped by: higher TP/SL ratio, tighter RSI, longer timeout
- Recent oos_rejects at sharpe~0.99 mean those changes degraded OOS — avoid repeating them

---
## WHAT TO CHANGE — PICK EXACTLY ONE

**Current: TP=5.20, SL=1.50, ratio=3.47. RSI long=42.0, RSI short=60.0, timeout=120h, rsi_period=24, trend_period=48.**

### PRIORITY 1 — take_profit_pct (current: 5.20) — improves TP/SL ratio → better OOS
Try: **5.40 | 5.50 | 5.60 | 5.80 | 6.00 | 6.20 | 5.00 | 4.80**

### PRIORITY 2 — timeout_hours (current: 120) — longer timeout may improve OOS
Try: **130 | 140 | 150 | 160 | 166 | 172 | 180 | 110 | 100**

### PRIORITY 3 — RSI long lt (current: 42.0) — tighter = fewer but cleaner trades
Try: **40.0 | 39.0 | 38.0 | 37.0 | 36.0 | 43.0 | 44.0 | 45.0**

### PRIORITY 4 — stop_loss_pct (current: 1.50) — tighter improves ratio
Try: **1.45 | 1.55 | 1.60 | 1.65 | 1.70 | 1.75 | 1.80**

### PRIORITY 5 — RSI short gt (current: 60.0) — higher = cleaner short signal
Try: **61 | 62 | 63 | 64 | 65 | 58 | 57**

### PRIORITY 6 — rsi_period_hours (current: 24)
Try: **20 | 21 | 22 | 23 | 25 | 26 | 27 | 28**

### PRIORITY 7 — trend period_hours (current: 48)
Try: **36 | 42 | 54 | 60 | 72**

### PRIORITY 8 — size_pct (current: 25)
Try: **24 | 23 | 22 | 21 | 20 | 18**

---
## KNOWN BAD — DO NOT USE

- stop_loss_pct < 1.45 → below noise floor
- rsi long lt < 35 → too few trades (< 400)
- rsi long lt > 45 → too many noisy entries
- timeout_hours > 210 or < 48 → rejected
- Any pairs other than [BTC/USD, ETH/USD, SOL/USD] → rejected
- DO NOT reproduce champion unchanged:
  take_profit_pct=5.2, stop_loss_pct=1.5, timeout_hours=120,
  rsi_lt=42.0, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=25

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