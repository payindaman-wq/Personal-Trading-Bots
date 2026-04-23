```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-5760 (2026-04-22)
# Champion: Sharpe=1.0922 | Trades=491 | elite_0.yaml is canonical ground truth.
# NOTE: elite_0.yaml has SL=1.62, size_pct=25, rsi_lt=36.5 — these ARE the champion values.

## UNIVERSE CONSTRAINT — DO NOT VIOLATE
Kraken Derivatives US perpetuals: **BTC/USD, ETH/USD, SOL/USD only.**
Never add or remove pairs. Any other pair is untradable and silently dropped.

---
## OUTPUT RULE
Output ONLY the modified YAML. ONE value changed. Nothing else.

---
## TEMPLATE — CURRENT CHAMPION. COPY EXACTLY, CHANGE ONE VALUE.

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
## HARD LIMITS — VIOLATION = IMMEDIATE DISCARD

| Parameter | Rule |
|---|---|
| stop_loss_pct | 1.50 – 2.50 ONLY |
| rsi long (lt) | 33 – 46 ONLY |
| rsi short (gt) | 52 – 68 ONLY |
| rsi_period_hours | 18 – 30 ONLY |
| timeout_hours | ≤ 210 |
| Pairs | must be exactly [BTC/USD, ETH/USD, SOL/USD] |
| fee_rate / max_open / leverage | DO NOT CHANGE |
| size_pct | 18 – 25 ONLY |
| Minimum trades | ≥ 400 |

---
## WHAT TO CHANGE — PICK EXACTLY ONE

### PRIORITY 1 — take_profit_pct (current: 4.87)
Try these in order (first untried wins):
5.00 | 5.10 | 5.20 | 5.30 | 5.40 | 5.50 | 4.75 | 4.65 | 5.60 | 5.70 | 5.80 | 4.55 | 5.90 | 6.00 | 4.45 | 6.10 | 4.35 | 6.20

### PRIORITY 2 — stop_loss_pct (current: 1.62)
Try these in order:
1.65 | 1.58 | 1.55 | 1.70 | 1.52 | 1.75 | 1.50 | 1.80 | 1.85 | 1.90 | 1.95 | 2.00 | 2.05 | 2.10

### PRIORITY 3 — RSI long lt (current: 36.5)
STAY in 33–46:
36.0 | 35.5 | 37.0 | 35.0 | 37.5 | 34.5 | 38.0 | 34.0 | 38.5 | 39.0 | 33.5 | 39.5 | 40.0 | 33.0

### PRIORITY 4 — RSI short gt (current: 60)
Try these in order:
58 | 62 | 56 | 64 | 54 | 66 | 52 | 68 | 57 | 55 | 53

### PRIORITY 5 — timeout_hours (current: 192)
Try these in order:
180 | 176 | 184 | 196 | 200 | 172 | 168 | 204 | 208 | 164 | 160

### PRIORITY 6 — rsi_period_hours (current: 24)
STAY in 18–30:
22 | 23 | 25 | 26 | 20 | 21 | 27 | 28 | 18 | 30

### PRIORITY 7 — Last resort only
trend period_hours (current: 48): 36 | 42 | 54 | 60 | 72
size_pct (current: 25): 24 | 23 | 22 | 21 | 20 | 19 | 18
pause_if_down_pct (current: 8): 6 | 7 | 9 | 10
stop_if_down_pct (current: 18): 15 | 16 | 17 | 20 | 22

---
## KNOWN BAD — DO NOT REPRODUCE THESE

- stop_loss_pct < 1.50 → always fails
- rsi long lt < 33 → poison attractor, always fails
- rsi long lt > 46 → too few trades
- timeout_hours > 210 → rejected
- Pairs list differing from [BTC/USD, ETH/USD, SOL/USD] → reject
- These exact values are the CURRENT CHAMPION — do not reproduce them unchanged:
  take_profit_pct=4.87, stop_loss_pct=1.62, timeout_hours=192,
  rsi_lt=36.5, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=25

---
## KEY CONTEXT

- Win rate is stable at ~35–38% across variants — structural property of the entry signal
- Trade count is stable at ~491 for the current parameter region; changes below 400 are rejected
- The OOS gate is active: new champions must also pass out-of-sample validation. Modest, stable improvements are more likely to pass than aggressive changes.
- Higher Sharpe was observed at trades~1265 in earlier research; current constraints prevent that region
- RSI short threshold (gt 60) is UNDER-EXPLORED — try loosening (lower values like 56–58)
- The TP/SL ratio (currently 4.87/1.62 = 3.01) is the primary driver — higher TP same SL, or slightly lower SL
- stop_loss_pct near 1.62 is the CONFIRMED CHAMPION value — explore 1.50–1.70 range first
- size_pct=25 is already at the upper limit — do not try to increase it

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template above
- [ ] Changed value is NOT in the KNOWN BAD list
- [ ] stop_loss_pct is between 1.50 and 2.50
- [ ] rsi long lt is between 33 and 46
- [ ] rsi short gt is between 52 and 68
- [ ] timeout_hours ≤ 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```

---