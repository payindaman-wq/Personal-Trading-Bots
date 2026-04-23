```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-6092 (2026-04-23)
# Champion: Sharpe=1.0922 | Trades=491 | elite_0.yaml is canonical ground truth.
# OOS Sharpe=2.6523 | OOS Trades=132 — new champions must clear this bar.

## UNIVERSE CONSTRAINT — HARD
Pairs: **BTC/USD, ETH/USD, SOL/USD ONLY.** Never add or remove. Any other pair is rejected.

---
## OUTPUT RULE
Output ONLY the modified YAML. ONE value changed from the template. Nothing else.

---
## TEMPLATE — COPY EXACTLY, CHANGE ONE VALUE ONLY

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

| Parameter | Allowed Range |
|---|---|
| stop_loss_pct | 1.50 – 2.50 |
| take_profit_pct | 3.00 – 8.00 |
| rsi long (lt) | 33 – 46 |
| rsi short (gt) | 52 – 68 |
| rsi_period_hours | 18 – 30 |
| timeout_hours | 48 – 210 |
| size_pct | 18 – 25 |
| Pairs | exactly [BTC/USD, ETH/USD, SOL/USD] |
| fee_rate / max_open / leverage | DO NOT CHANGE |
| Minimum trades | ≥ 400 |

---
## WHAT TO CHANGE — PICK EXACTLY ONE

### STATUS: TP values 4.87–5.70 are EXHAUSTED (dedup-rejected). Skip them.

### PRIORITY 1 — RSI short gt (current: 60) ← UNDER-EXPLORED, TRY FIRST
These are the LEAST tested. Pick the first value not yet tried:
**58 | 57 | 56 | 55 | 54 | 53 | 52 | 62 | 64 | 66 | 68**

Why: Loosening short RSI (lower gt value) increases short trade opportunities. Tightening (higher) improves precision. Neither direction is saturated.

### PRIORITY 2 — RSI long lt (current: 36.5)
**37.0 | 37.5 | 38.0 | 38.5 | 36.0 | 35.5 | 35.0 | 39.0 | 39.5 | 34.5 | 34.0 | 33.5 | 33.0**

### PRIORITY 3 — rsi_period_hours (current: 24)
**22 | 26 | 23 | 25 | 20 | 21 | 27 | 28 | 18 | 30**

### PRIORITY 4 — take_profit_pct (current: 4.87)
Skip 4.87–5.70 (already tested). Try only:
**5.80 | 5.90 | 6.00 | 6.10 | 6.20 | 6.30 | 6.50 | 7.00 | 4.65 | 4.55 | 4.45 | 4.35 | 4.00 | 3.80**

### PRIORITY 5 — stop_loss_pct (current: 1.62)
**1.65 | 1.58 | 1.55 | 1.70 | 1.52 | 1.75 | 1.50 | 1.80 | 1.85 | 1.90 | 2.00 | 2.10 | 2.20 | 2.50**

### PRIORITY 6 — timeout_hours (current: 192)
**180 | 176 | 184 | 196 | 200 | 172 | 168 | 160 | 204 | 208**

### PRIORITY 7 — trend period_hours (current: 48)
**36 | 42 | 54 | 60 | 72**

### PRIORITY 8 — size_pct (current: 25) — Last resort only
**24 | 23 | 22 | 21 | 20 | 19 | 18**

---
## KNOWN BAD — DO NOT REPRODUCE

- stop_loss_pct < 1.50 → always fails
- rsi long lt < 33 → poison attractor
- rsi long lt > 46 → too few trades
- timeout_hours > 210 → rejected
- take_profit_pct values already tested (dedup-rejected): 4.87, 5.00, 5.10, 5.20, 5.30, 5.40, 5.50, 5.60, 5.70, 4.75
- Pairs list other than [BTC/USD, ETH/USD, SOL/USD] → reject
- Reproducing champion unchanged → reject

**Champion values (do not reproduce all unchanged):**
take_profit_pct=4.87, stop_loss_pct=1.62, timeout_hours=192,
rsi_lt=36.5, rsi_gt=60, rsi_period=24, trend_period=48, size_pct=25

---
## KEY CONTEXT

- Win rate is structurally ~35–38% — do not try to optimize it directly
- Trade count ~491 is stable in this parameter region; changes below 400 are rejected
- OOS gate is active and strict (champion OOS=2.6523): only robust improvements pass
- The RSI short threshold (gt 60) is the most under-explored parameter — prioritize it
- TP/SL ratio (4.87/1.62 = 3.01) is the primary Sharpe driver
- Modest, stable improvements to signal quality (RSI thresholds, periods) are most likely to pass OOS gate
- Do NOT try to increase size_pct above 25 — already at maximum

---
## PRE-OUTPUT CHECKLIST

- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD]
- [ ] Exactly ONE value changed from template
- [ ] Changed value is NOT in KNOWN BAD list
- [ ] stop_loss_pct between 1.50 and 2.50
- [ ] rsi long lt between 33 and 46
- [ ] rsi short gt between 52 and 68
- [ ] timeout_hours ≤ 210
- [ ] fee_rate, max_open, leverage unchanged
- [ ] Expected trade count ≥ 400

Output ONLY the YAML. No explanation. No comments.
```