```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-5253-sync-fix (2026-04-22)
# Champion: Sharpe=0.9644 | Trades=494 | elite_0.yaml is canonical ground truth.

## UNIVERSE CONSTRAINT — DO NOT VIOLATE
Kraken Derivatives US perpetuals: **BTC/USD, ETH/USD, SOL/USD only.**
Never add or remove pairs. Any other pair is untradable and silently dropped.

---
## OUTPUT RULE
Output ONLY the modified YAML. ONE value changed. Nothing else.

---
## TEMPLATE — THIS IS THE CURRENT CHAMPION. COPY EXACTLY, CHANGE ONE VALUE.

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
  take_profit_pct: 4.98
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
| stop_loss_pct | 1.70 – 2.30 ONLY |
| rsi long (lt) | 33 – 44 ONLY |
| rsi_period_hours | 18 – 30 ONLY |
| timeout_hours | ≤ 210 |
| Pairs | must be exactly [BTC/USD, ETH/USD, SOL/USD] |
| fee_rate / size_pct / max_open / leverage | DO NOT CHANGE |
| Minimum trades | ≥ 150 |

---
## WHAT TO CHANGE — PICK EXACTLY ONE

### PRIORITY 1 — take_profit_pct (current: 4.98)
Try these in order (first untried wins):
5.05 | 5.10 | 5.15 | 4.90 | 4.85 | 5.20 | 4.80 | 5.25 | 5.30 | 4.75 | 5.40 | 4.70 | 5.50 | 4.65 | 4.60 | 5.60 | 5.70

### PRIORITY 2 — stop_loss_pct (current: 1.92)
Try these in order:
1.95 | 2.00 | 2.05 | 2.10 | 1.90 | 1.85 | 2.15 | 1.80 | 2.20 | 1.75 | 1.70 | 2.25 | 2.30

### PRIORITY 3 — timeout_hours (current: 192)
Try these in order:
184 | 196 | 200 | 180 | 176 | 204 | 208 | 172 | 168 | 164 | 160 | 156

### PRIORITY 4 — RSI thresholds
rsi long lt (current: 37.77) — STAY in 33–44:
38.0 | 37.5 | 38.5 | 37.0 | 39.0 | 36.5 | 39.5 | 36.0 | 40.0 | 35.5 | 40.5 | 41.0 | 33.5 | 43.0 | 44.0

rsi short gt (current: 60):
59 | 61 | 58 | 62 | 57 | 63 | 56 | 55

rsi_period_hours (current: 24) — STAY in 18–30:
22 | 23 | 25 | 26 | 20 | 21 | 27 | 28 | 18 | 30

### PRIORITY 5 — Last resort only
trend period_hours (current: 48): 36 | 42 | 54 | 60 | 72
pause_if_down_pct (current: 8): 6 | 7 | 9 | 10
stop_if_down_pct (current: 18): 15 | 16 | 17 | 20 | 22

---
## KNOWN BAD — DO NOT REPRODUCE THESE

- stop_loss_pct < 1.70 → always fails
- stop_loss_pct > 2.30 → too few trades
- rsi long lt < 33 → poison attractor, always fails
- rsi long lt > 44 → too few trades
- timeout_hours > 210 → rejected
- Pairs list differing from [BTC/USD, ETH/USD, SOL/USD] → reject
- These exact values are the CURRENT CHAMPION — do not reproduce them unchanged:
  take_profit_pct=4.98, stop_loss_pct=1.92, timeout_hours=192,
  rsi_lt=37.77, rsi_gt=60, rsi_period=24, trend_period=48

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template above
- [ ] Changed value is NOT the current champion value listed in KNOWN BAD
- [ ] stop_loss_pct is between 1.70 and 2.30
- [ ] rsi long lt is between 33 and 44
- [ ] timeout_hours ≤ 210
- [ ] fee_rate, size_pct, max_open, leverage unchanged
- [ ] Expected trade count ≥ 150

Output ONLY the YAML. No explanation. No comments.
```

---