```markdown
# ODIN Research Program — FUTURES SWING
# Champion: Sharpe=0.9386 | Trades=512 | elite_0.yaml is ground truth.
# NOTE: OOS gate is active. Champion _oos_sharpe=2.4479. Candidates improving
# in-sample must also achieve OOS sharpe ≥ 2.4479. This is a HIGH bar.
# Focus on configs that score well on BOTH windows.

## OUTPUT RULE
Output ONLY the modified YAML. ONE value changed. Nothing else.

---
## TEMPLATE — THIS IS THE ACTUAL CURRENT CHAMPION — COPY EXACTLY, CHANGE EXACTLY ONE VALUE

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
  stop_loss_pct: 1.65
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
| stop_loss_pct | 1.55 – 2.50 |
| take_profit_pct | 3.0 – 8.0 |
| rsi long (lt) | 33 – 46 |
| rsi short (gt) | 52 – 68 |
| rsi_period_hours | 18 – 30 |
| timeout_hours | 48 – 210 |
| size_pct | 18 – 25 |
| pairs | exactly [BTC/USD, ETH/USD, SOL/USD] |
| fee_rate / max_open / leverage | DO NOT CHANGE |
| Minimum trades | ≥ 400 |

---
## WHAT TO CHANGE — PICK EXACTLY ONE

**TP/SL ratio drives Sharpe. Current ratio = 5.2/1.65 = 3.15.**

### PRIORITY 1 — timeout_hours (current: 166) — HIGHEST PRIORITY
This is SHORT vs the old regime (192h). Increasing it may recover lost trades and improve OOS.
Pick ONE:
**172 | 176 | 180 | 184 | 188 | 192 | 196 | 200 | 156 | 160**

### PRIORITY 2 — stop_loss_pct (current: 1.65)
Tighter stop = higher TP/SL ratio = better Sharpe.
Pick ONE:
**1.55 | 1.58 | 1.60 | 1.62 | 1.68 | 1.70 | 1.72 | 1.75**

### PRIORITY 3 — take_profit_pct (current: 5.2)
Pick ONE:
**5.30 | 5.40 | 5.50 | 5.60 | 5.70 | 5.00 | 4.90 | 4.75**

### PRIORITY 4 — RSI short gt (current: 60) — UNDER-EXPLORED
Lower threshold = more short trades = better OOS coverage.
Pick ONE:
**56 | 57 | 58 | 59 | 62 | 63 | 64 | 66**

### PRIORITY 5 — RSI long lt (current: 37.77)
Pick ONE (stay 33–46):
**36.5 | 37.0 | 38.0 | 38.5 | 39.0 | 39.5 | 36.0 | 35.5**

### PRIORITY 6 — rsi_period_hours (current: 24)
Pick ONE (stay 18–30):
**20 | 21 | 22 | 23 | 25 | 26 | 27 | 28**

### PRIORITY 7 — size_pct (current: 25)
Pick ONE (stay 18–25):
**24 | 23 | 22 | 21 | 20**

### PRIORITY 8 — trend period_hours (current: 48)
Pick ONE:
**36 | 42 | 54 | 60 | 72**

---
## KNOWN BAD — DO NOT USE THESE

- stop_loss_pct < 1.55 → always fails minimum trade count
- rsi long lt < 33 → poison attractor
- rsi long lt > 46 → too few trades (< 400)
- timeout_hours > 210 → rejected
- timeout_hours < 48 → rejected
- Any pairs other than [BTC/USD, ETH/USD, SOL/USD] → rejected
- DO NOT reproduce the champion unchanged:
  take_profit_pct=5.2, stop_loss_pct=1.65, timeout_hours=166,
  rsi_lt=37.77, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=25

---
## KEY FACTS

- Win rate is structurally ~33–38% — do not try to change this
- Trade count ~512 in current region — below 400 = rejected
- TP/SL ratio is the PRIMARY in-sample Sharpe driver
- OOS gate requires OOS sharpe ≥ 2.4479 for any improvement to be accepted
- timeout_hours=166 is unusually short — increasing may improve OOS stability
- RSI short (gt 60) is under-explored — loosening to 56–59 adds short trades

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template
- [ ] Changed value is NOT in KNOWN BAD list
- [ ] stop_loss_pct between 1.55 and 2.50
- [ ] rsi long lt between 33 and 46
- [ ] rsi short gt between 52 and 68
- [ ] timeout_hours between 48 and 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```

---