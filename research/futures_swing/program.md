```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-5428-analysis (2026-04-22)
# Champion: Sharpe=0.9689 | Trades=494 | elite_0.yaml is canonical ground truth.
# NOTE: OOS Sharpe=2.1726 — new champion must beat this OOS threshold.

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
| rsi short (gt) | 55 – 65 ONLY |
| rsi_period_hours | 18 – 30 ONLY |
| timeout_hours | 96 – 210 ONLY |
| Pairs | must be exactly [BTC/USD, ETH/USD, SOL/USD] |
| fee_rate / size_pct / max_open / leverage | DO NOT CHANGE |
| Minimum trades | ≥ 150 |

---
## SEARCH PRIORITY — TAKE_PROFIT IS EXHAUSTED. START FROM PRIORITY 1.

### PRIORITY 1 — stop_loss_pct (current: 1.92)
⚠️ take_profit_pct neighborhood is EXHAUSTED after 5000+ generations. Do NOT try take_profit values near 4.98.
Try stop_loss in this order (first untried wins):
1.95 | 2.00 | 2.05 | 1.90 | 2.10 | 1.85 | 2.15 | 1.80 | 2.20 | 1.75 | 1.70 | 2.25 | 2.30

### PRIORITY 2 — RSI long threshold (current: 37.77) — STAY in 33–44
38.5 | 39.0 | 37.5 | 39.5 | 37.0 | 40.0 | 36.5 | 40.5 | 36.0 | 41.0 | 35.5 | 42.0 | 43.0 | 35.0 | 33.5

### PRIORITY 3 — RSI short threshold (current: 60) — STAY in 55–65
61 | 59 | 62 | 58 | 63 | 57 | 64 | 56 | 65 | 55

### PRIORITY 4 — rsi_period_hours (current: 24) — STAY in 18–30
22 | 26 | 20 | 28 | 18 | 30 | 21 | 27 | 23 | 25

### PRIORITY 5 — timeout_hours (current: 192)
168 | 180 | 200 | 160 | 204 | 156 | 208 | 144 | 210 | 120 | 96

### PRIORITY 6 — take_profit_pct (LAST RESORT ONLY — mostly exhausted)
5.20 | 5.30 | 5.40 | 5.50 | 4.70 | 4.60 | 5.60 | 5.70 | 4.50 | 5.80

### PRIORITY 7 — trend period_hours (current: 48)
36 | 42 | 54 | 60 | 72

---
## KNOWN BAD — DO NOT REPRODUCE

- stop_loss_pct < 1.70 → always fails (too few trades or negative Sharpe)
- stop_loss_pct > 2.30 → too few trades
- rsi long lt < 33 → poison attractor, always fails
- rsi long lt > 44 → too many trades, degrades Sharpe
- timeout_hours > 210 → rejected by engine
- timeout_hours < 96 → too few trades
- Pairs list differing from [BTC/USD, ETH/USD, SOL/USD] → immediate reject
- take_profit_pct values 4.75–5.15 → EXHAUSTED, extremely high dedup rate, skip unless nothing else to try
- These exact values are the CURRENT CHAMPION — do not reproduce unchanged:
  take_profit_pct=4.98, stop_loss_pct=1.92, timeout_hours=192,
  rsi_lt=37.77, rsi_gt=60, rsi_period=24, trend_period=48

---
## WHY STOP_LOSS IS PRIORITY 1

The take_profit search space (4.60–5.70) has been saturated over 5000+ generations.
Recent gens show ~40% dedup rejects because the LLM keeps revisiting exhausted take_profit values.
Stop_loss_pct has NOT been thoroughly explored in the current RSI/trend regime.
Higher stop_loss (2.05–2.20) may allow more trades to survive to take_profit, improving Sharpe.
Lower stop_loss (1.75–1.85) may filter more noise trades, improving win rate.

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template above
- [ ] Changed value is NOT the current champion value listed in KNOWN BAD
- [ ] stop_loss_pct is between 1.70 and 2.30 (inclusive)
- [ ] rsi long lt is between 33 and 44 (inclusive)
- [ ] rsi short gt is between 55 and 65 (inclusive)
- [ ] rsi_period_hours is between 18 and 30 (inclusive)
- [ ] timeout_hours is between 96 and 210 (inclusive)
- [ ] fee_rate, size_pct, max_open, leverage unchanged
- [ ] Expected trade count ≥ 150

Output ONLY the YAML. No explanation. No comments.
```

---