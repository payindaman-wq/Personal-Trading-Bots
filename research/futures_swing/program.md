```markdown
# ODIN Research Program — FUTURES SWING
# Champion: Sharpe=1.0922 | Trades=491 | elite_0.yaml is ground truth.

## OUTPUT RULE
Output ONLY the modified YAML. ONE value changed. Nothing else.

---
## TEMPLATE — COPY EXACTLY, CHANGE EXACTLY ONE VALUE

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
      value: 36.5
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
  take_profit_pct: 4.87
  stop_loss_pct: 1.62
  timeout_hours: 192
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
## WHAT TO CHANGE — PICK EXACTLY ONE FROM THE PRIORITY LIST

**TP/SL ratio drives Sharpe. Higher ratio = better. Current ratio = 4.87/1.62 = 3.01.**

### PRIORITY 1 — stop_loss_pct (current: 1.62) — HIGHEST PRIORITY
Pick ONE of these values (choose randomly from this list):
**1.55 | 1.58 | 1.60 | 1.65 | 1.68 | 1.70 | 1.75 | 1.80**

Tighter stop = higher ratio = better Sharpe. Stay ≥ 1.55.

### PRIORITY 2 — take_profit_pct (current: 4.87)
Pick ONE of these values (choose randomly):
**5.00 | 5.10 | 5.20 | 5.30 | 5.40 | 5.50 | 4.75 | 4.65**

### PRIORITY 3 — RSI short gt (current: 60) — UNDER-EXPLORED
Pick ONE of these values:
**56 | 57 | 58 | 62 | 54 | 64 | 66**

Lower threshold = more short trades. Current short signal may be too restrictive.

### PRIORITY 4 — RSI long lt (current: 36.5)
Pick ONE (stay 33–46):
**37.0 | 36.0 | 37.5 | 35.5 | 38.0 | 35.0 | 38.5 | 39.0**

### PRIORITY 5 — size_pct (current: 25)
Pick ONE (stay 18–25):
**24 | 23 | 22 | 21 | 20**

### PRIORITY 6 — timeout_hours (current: 192)
Pick ONE (stay 48–210):
**180 | 184 | 196 | 200 | 176 | 204 | 208**

### PRIORITY 7 — rsi_period_hours (current: 24)
Pick ONE (stay 18–30):
**22 | 23 | 25 | 26 | 20 | 21 | 27 | 28**

### PRIORITY 8 — Last resort
trend period_hours (current: 48): **36 | 42 | 54 | 60 | 72**
pause_if_down_pct (current: 8): **6 | 7 | 9 | 10**

---
## KNOWN BAD — DO NOT USE THESE

- stop_loss_pct < 1.55 → always fails minimum trade count
- rsi long lt < 33 → poison attractor
- rsi long lt > 46 → too few trades (< 400)
- timeout_hours > 210 → rejected
- Any pairs other than [BTC/USD, ETH/USD, SOL/USD] → rejected
- DO NOT reproduce the champion unchanged:
  take_profit_pct=4.87, stop_loss_pct=1.62, timeout_hours=192,
  rsi_lt=36.5, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=25

---
## KEY FACTS

- Win rate is structurally ~35–38% — do not try to change this
- Trade count ~491 in current region — below 400 = rejected
- TP/SL ratio is the PRIMARY Sharpe driver
- RSI short (gt 60) is under-explored — loosening to 56–58 adds short trades
- OOS gate is active: must beat champion in both in-sample AND out-of-sample

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template
- [ ] Changed value is NOT in KNOWN BAD list
- [ ] stop_loss_pct between 1.55 and 2.50
- [ ] rsi long lt between 33 and 46
- [ ] rsi short gt between 52 and 68
- [ ] timeout_hours ≤ 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```