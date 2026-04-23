```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-5585-sync (2026-04-22)
# Champion: Sharpe=1.0356 | Trades=499 | elite_0.yaml is canonical ground truth.

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
  size_pct: 21.77
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
  take_profit_pct: 4.87
  stop_loss_pct: 1.92
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
| stop_loss_pct | 1.70 – 2.50 ONLY |
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

### PRIORITY 2 — stop_loss_pct (current: 1.92)
Try these in order:
1.95 | 2.00 | 2.05 | 2.10 | 1.88 | 1.85 | 2.15 | 1.80 | 2.20 | 1.75 | 1.70 | 2.25 | 2.30 | 2.35 | 2.40 | 2.45 | 2.50

### PRIORITY 3 — RSI short gt (current: 60)
Try these in order:
58 | 56 | 62 | 54 | 64 | 52 | 66 | 68 | 57 | 55 | 53

### PRIORITY 4 — RSI long lt (current: 37.77)
STAY in 33–46:
38.5 | 39.0 | 39.5 | 40.0 | 37.0 | 36.5 | 40.5 | 36.0 | 41.0 | 35.5 | 41.5 | 42.0 | 35.0 | 42.5 | 43.0 | 34.5 | 44.0 | 44.5 | 45.0 | 34.0 | 33.5

### PRIORITY 5 — timeout_hours (current: 192)
Try these in order:
180 | 176 | 184 | 196 | 200 | 172 | 168 | 204 | 208 | 164 | 160

### PRIORITY 6 — rsi_period_hours (current: 24)
STAY in 18–30:
22 | 23 | 25 | 26 | 20 | 21 | 27 | 28 | 18 | 30

### PRIORITY 7 — Last resort only
trend period_hours (current: 48): 36 | 42 | 54 | 60 | 72
size_pct (current: 21.77): 20 | 22 | 23 | 19 | 24 | 18 | 25
pause_if_down_pct (current: 8): 6 | 7 | 9 | 10
stop_if_down_pct (current: 18): 15 | 16 | 17 | 20 | 22

---
## KNOWN BAD — DO NOT REPRODUCE THESE

- stop_loss_pct < 1.70 → always fails
- rsi long lt < 33 → poison attractor, always fails
- rsi long lt > 46 → too few trades
- timeout_hours > 210 → rejected
- Pairs list differing from [BTC/USD, ETH/USD, SOL/USD] → reject
- These exact values are the CURRENT CHAMPION — do not reproduce them unchanged:
  take_profit_pct=4.87, stop_loss_pct=1.92, timeout_hours=192,
  rsi_lt=37.77, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=21.77

---
## KEY CONTEXT

- Win rate is stable at ~37.7% across many variants — this is a structural property of the entry signal, not a tunable parameter
- Trade count is stable at ~499 for the current parameter region — changes that reduce below 400 are rejected
- Higher Sharpe was observed at trades~1265 in earlier research (different parameter region); current constraints prevent reaching that region
- RSI short threshold (gt 60) is UNDER-EXPLORED — try loosening it (lower values like 56–58) to see if more short trades improve Sharpe
- The TP/SL ratio (currently 4.87/1.92 = 2.53) is the primary driver — try higher TP with same SL, or higher SL with proportionally higher TP

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template above
- [ ] Changed value is NOT in the KNOWN BAD list
- [ ] stop_loss_pct is between 1.70 and 2.50
- [ ] rsi long lt is between 33 and 46
- [ ] rsi short gt is between 52 and 68
- [ ] timeout_hours ≤ 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```

---