```markdown
# ODIN Research Program — FUTURES SWING
# GROUND TRUTH (elite_0.yaml): Sharpe=0.9038 | Trades=707
# OOS gate ACTIVE: candidates must achieve OOS sharpe ≥ 2.3434 to be accepted as new_best.
# new_elite insertions do NOT require OOS gate — focus on populating elites first.

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
      value: 42.42
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
  take_profit_pct: 3.96
  stop_loss_pct: 1.64
  timeout_hours: 113
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

- Champion: TP=3.96, SL=1.64, ratio=2.41. RSI long=42.42, RSI short=60, timeout=113h, rsi_period=24, trend_period=48
- OOS Sharpe=2.3434 >> in-sample=0.9038 — OOS gate is very tight; most new_best attempts will fail it
- Win rate ~34–37%. Trade count ~707. Both healthy — do not try to change these dramatically.
- OOS gate floor = 2.3434. Changes that improve in-sample but hurt OOS will be REJECTED as new_best.
- new_elite (population slot) does NOT require OOS gate — aim to improve population diversity first.
- OOS stability is helped by: higher TP/SL ratio, cleaner RSI thresholds, appropriate timeout.
- Recent dedup/oos_rejects mean the search space near current params is crowded — try slightly larger steps.

---
## WHAT TO CHANGE — PICK EXACTLY ONE

**Current: TP=3.96, SL=1.64, ratio=2.41. RSI long=42.42, RSI short=60, timeout=113h, rsi_period=24, trend_period=48, size_pct=25.**

### PRIORITY 1 — take_profit_pct (current: 3.96) — raising TP improves ratio → better OOS
Try: **4.20 | 4.40 | 4.60 | 4.80 | 5.00 | 5.20 | 5.40 | 3.70 | 3.50**

### PRIORITY 2 — stop_loss_pct (current: 1.64) — tightening SL improves ratio
Try: **1.55 | 1.50 | 1.48 | 1.45 | 1.70 | 1.75 | 1.80**

### PRIORITY 3 — timeout_hours (current: 113) — adjust to find better exit timing
Try: **100 | 105 | 110 | 120 | 125 | 130 | 140 | 150 | 160**

### PRIORITY 4 — RSI long lt (current: 42.42) — round to clean value or tighten
Try: **42.0 | 41.0 | 40.0 | 39.0 | 38.0 | 43.0 | 44.0 | 45.0**

### PRIORITY 5 — RSI short gt (current: 60) — higher = cleaner short signal
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
  take_profit_pct=3.96, stop_loss_pct=1.64, timeout_hours=113,
  rsi_lt=42.42, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=25

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template above
- [ ] Changed value is NOT in KNOWN BAD list
- [ ] stop_loss_pct between 1.45 and 2.50
- [ ] take_profit_pct between 3.0 and 8.0
- [ ] rsi long lt between 35 and 45
- [ ] rsi short gt between 55 and 70
- [ ] timeout_hours between 48 and 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```