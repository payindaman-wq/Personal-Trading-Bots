```markdown
# ODIN Research Program — FUTURES SWING
# Champion: Sharpe=1.0431 | Trades=640 | elite_0.yaml is ground truth.
# NOTE: OOS gate is active. Champion _oos_sharpe=2.4617. Candidates improving
# in-sample must also achieve OOS sharpe ≥ 2.4617. This is a HIGH bar.

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
      value: 42.85
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24
      operator: gt
      value: 62.68
exit:
  take_profit_pct: 4.75
  stop_loss_pct: 1.5
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
| rsi long (lt) | 38 – 48 |
| rsi short (gt) | 55 – 70 |
| rsi_period_hours | 18 – 30 |
| timeout_hours | 48 – 210 |
| size_pct | 18 – 25 |
| pairs | exactly [BTC/USD, ETH/USD, SOL/USD] |
| fee_rate / max_open / leverage | DO NOT CHANGE |
| Minimum trades | ≥ 400 |

---
## WHAT TO CHANGE — PICK EXACTLY ONE

**Current champion: TP=4.75, SL=1.50, ratio=3.17. RSI long=42.85, RSI short=62.68, timeout=166h.**

### PRIORITY 1 — take_profit_pct (current: 4.75) — HIGHEST PRIORITY
Higher TP = higher ratio = better Sharpe. Current ratio 3.17 has room to grow.
Pick ONE:
**5.00 | 5.10 | 5.20 | 5.30 | 5.40 | 5.50 | 5.60 | 4.60 | 4.50**

### PRIORITY 2 — stop_loss_pct (current: 1.50)
Tighter stop = higher ratio. Minimum allowed is 1.45.
Pick ONE:
**1.45 | 1.47 | 1.48 | 1.52 | 1.55 | 1.58 | 1.60 | 1.62**

### PRIORITY 3 — timeout_hours (current: 166)
Increasing may recover missed trades and improve OOS stability.
Pick ONE:
**172 | 176 | 180 | 184 | 188 | 192 | 156 | 160 | 148**

### PRIORITY 4 — RSI short gt (current: 62.68)
Lower threshold = more short trades. Higher = cleaner signal.
Pick ONE:
**58 | 59 | 60 | 61 | 62 | 63 | 64 | 65 | 66**

### PRIORITY 5 — RSI long lt (current: 42.85)
Higher = more trades (be careful of trade count ceiling). Lower = cleaner signal.
Pick ONE:
**40.0 | 41.0 | 42.0 | 43.0 | 44.0 | 45.0 | 39.0 | 38.5**

### PRIORITY 6 — rsi_period_hours (current: 24)
Pick ONE (stay 18–30):
**20 | 21 | 22 | 23 | 25 | 26 | 27 | 28**

### PRIORITY 7 — trend period_hours (current: 48)
Pick ONE:
**36 | 42 | 54 | 60 | 72**

### PRIORITY 8 — size_pct (current: 25)
Pick ONE (stay 18–25):
**24 | 23 | 22 | 21 | 20**

---
## KNOWN BAD — DO NOT USE THESE

- stop_loss_pct < 1.45 → below noise floor
- rsi long lt < 38 → too few trades (< 400)
- rsi long lt > 48 → too many trades / noisy entries
- timeout_hours > 210 → rejected
- timeout_hours < 48 → rejected
- Any pairs other than [BTC/USD, ETH/USD, SOL/USD] → rejected
- DO NOT reproduce the champion unchanged:
  take_profit_pct=4.75, stop_loss_pct=1.5, timeout_hours=166,
  rsi_lt=42.85, rsi_gt=62.68, rsi_period=24, trend_period=48, size_pct=25

---
## KEY FACTS

- Win rate is structurally ~33–38% — do not try to change this
- Trade count ~640 in current region — stay above 400
- TP/SL ratio is the PRIMARY in-sample Sharpe driver (current: 3.17)
- OOS gate requires OOS sharpe ≥ 2.4617 for any improvement to be accepted
- RSI long at 42.85 and RSI short at 62.68 are the current working thresholds
- SL=1.50 is the current champion value — exploring 1.45–1.48 may improve ratio

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template
- [ ] Changed value is NOT in KNOWN BAD list
- [ ] stop_loss_pct between 1.45 and 2.50
- [ ] rsi long lt between 38 and 48
- [ ] rsi short gt between 55 and 70
- [ ] timeout_hours between 48 and 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```

---