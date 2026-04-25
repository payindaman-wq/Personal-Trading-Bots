```markdown
# ODIN Research Program — FUTURES SWING
# GROUND TRUTH (elite_0.yaml): Sharpe=0.9170 | Trades=748 | OOS_Sharpe=2.3434
# WARNING: OOS gate compares candidate OOS vs champion_oos=2.3434 — this is the
# primary rejection reason. Focus on changes that preserve OOS stability.
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
      value: 58.32
exit:
  take_profit_pct: 3.96
  stop_loss_pct: 1.64
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

- Champion: TP=3.96, SL=1.64, ratio=2.41. RSI long=42.0, RSI short=58.32, timeout=120h, rsi_period=24, trend_period=48, size_pct=25
- Win rate ~34–38%. Trade count ~748. Sharpe=0.9170. OOS_Sharpe=2.3434.
- OOS gate requires candidate OOS ≥ 2.3434 — this is strict. Changes that RAISE TP/SL ratio or TIGHTEN RSI thresholds improve OOS.
- Recent oos_reject events at sharpe=1.03 and 0.97 confirm OOS is the bottleneck, not IS Sharpe.
- High dedup pressure — do not repeat values already tried. Explore fresh values.
- TP/SL ratio of 2.41 is LOW — raising TP or lowering SL improves OOS stability.

---
## WHAT TO CHANGE — PICK EXACTLY ONE

**Current: TP=3.96, SL=1.64, ratio=2.41. RSI long=42.0, RSI short=58.32, timeout=120h, rsi_period=24, trend_period=48, size_pct=25.**

### PRIORITY 1 — take_profit_pct (current: 3.96) — raising TP improves ratio → better OOS
Try: **5.00 | 5.20 | 5.40 | 5.60 | 5.80 | 6.00 | 4.50 | 4.80 | 4.20**

### PRIORITY 2 — RSI short gt (current: 58.32) — raising threshold → cleaner shorts, better OOS
Try: **60.0 | 61.0 | 62.0 | 63.0 | 64.0 | 65.0 | 59.0 | 57.0 | 56.0**

### PRIORITY 3 — stop_loss_pct (current: 1.64) — lowering SL improves ratio → better OOS
Try: **1.45 | 1.50 | 1.55 | 1.58 | 1.60 | 1.70 | 1.75 | 1.80**

### PRIORITY 4 — RSI long lt (current: 42.0) — tighter = fewer but cleaner trades → better OOS
Try: **40.0 | 41.0 | 43.0 | 44.0 | 39.0 | 38.0 | 37.0 | 36.0**

### PRIORITY 5 — timeout_hours (current: 120) — longer timeout may improve OOS
Try: **130 | 140 | 150 | 160 | 110 | 100 | 90 | 72 | 168**

### PRIORITY 6 — rsi_period_hours (current: 24)
Try: **20 | 21 | 22 | 23 | 25 | 26 | 27 | 28 | 18 | 30**

### PRIORITY 7 — trend period_hours (current: 48)
Try: **36 | 42 | 54 | 60 | 72 | 24**

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
  take_profit_pct=3.96, stop_loss_pct=1.64, timeout_hours=120,
  rsi_lt=42.0, rsi_gt=58.32, rsi_period=24, trend_period=48, size_pct=25

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

---