```markdown
# ODIN Research Program — FUTURES SWING
# GROUND TRUTH (elite_0.yaml): Sharpe=0.7001 | Trades=486 | OOS_Sharpe=1.8971
# WARNING: OOS gate compares candidate OOS vs champion_oos=1.8971
# OOS gate is enforced automatically by code. Do NOT try to game it manually.

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
      value: 60.0
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
## KEY FACTS

- Champion: TP=5.2, SL=1.92, ratio=2.71. RSI long=37.77, RSI short=60.0, timeout=166h, rsi_period=24, trend_period=48, size_pct=25
- Win rate ~34–38%. Trade count ~486. Sharpe=0.7001. OOS_Sharpe=1.8971.
- OOS gate requires candidate OOS ≥ 1.8971 — this is the binding constraint.
- TP/SL ratio of 2.71 is adequate. Raising TP further or tightening RSI thresholds may improve OOS.
- High dedup pressure — do not repeat values already tried. Explore fresh values only.
- RSI long is already tight at 37.77 — explore range 35.0–41.0 carefully.
- RSI short is at 60.0 — raising to 62–66 may improve signal quality.

---
## WHAT TO CHANGE — PICK EXACTLY ONE

**Current: TP=5.2, SL=1.92, ratio=2.71. RSI long=37.77, RSI short=60.0, timeout=166h, rsi_period=24, trend_period=48, size_pct=25.**

### PRIORITY 1 — RSI short gt (current: 60.0) — raising threshold → cleaner shorts, better OOS
Try: **62.0 | 63.0 | 64.0 | 65.0 | 61.0 | 66.0 | 67.0 | 59.0 | 58.0 | 57.0 | 56.0**

### PRIORITY 2 — take_profit_pct (current: 5.2) — raising TP improves ratio → better OOS
Try: **5.5 | 5.8 | 6.0 | 6.2 | 6.5 | 7.0 | 4.8 | 4.5 | 5.0 | 5.3 | 5.6**

### PRIORITY 3 — RSI long lt (current: 37.77) — tighter = fewer but cleaner trades → better OOS
Try: **36.0 | 35.5 | 37.0 | 38.0 | 39.0 | 40.0 | 41.0 | 35.0**

### PRIORITY 4 — stop_loss_pct (current: 1.92) — adjusting SL changes ratio
Try: **1.80 | 1.75 | 1.70 | 1.65 | 1.60 | 1.55 | 1.50 | 2.00 | 2.10 | 2.20**

### PRIORITY 5 — timeout_hours (current: 166) — explore nearby values
Try: **150 | 155 | 160 | 170 | 175 | 180 | 140 | 130 | 120 | 200 | 210**

### PRIORITY 6 — rsi_period_hours (current: 24)
Try: **20 | 21 | 22 | 23 | 25 | 26 | 27 | 28 | 18 | 30**

### PRIORITY 7 — trend period_hours (current: 48)
Try: **36 | 42 | 54 | 60 | 72 | 24**

### PRIORITY 8 — size_pct (current: 25)
Try: **24 | 23 | 22 | 21 | 20 | 19 | 18**

---
## KNOWN BAD — DO NOT USE

- stop_loss_pct < 1.45 → below noise floor
- rsi long lt < 35 → too few trades (< 400)
- rsi long lt > 45 → too many noisy entries
- timeout_hours > 210 or < 48 → rejected
- Any pairs other than [BTC/USD, ETH/USD, SOL/USD] → rejected
- DO NOT reproduce champion unchanged:
  take_profit_pct=5.2, stop_loss_pct=1.92, timeout_hours=166,
  rsi_lt=37.77, rsi_gt=60.0, rsi_period=24, trend_period=48, size_pct=25

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