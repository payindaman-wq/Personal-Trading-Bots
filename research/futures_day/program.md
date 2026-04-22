```markdown
# ODIN — FUTURES DAY v43.0

## YAML TEMPLATE — copy verbatim, change EXACTLY ONE value

```yaml
name: crossover
style: mean_reversion_swing
league: futures_day
leverage: 2
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
- XRP/USD
- DOGE/USD
- AVAX/USD
- LINK/USD
- UNI/USD
- AAVE/USD
- NEAR/USD
- APT/USD
- SUI/USD
- ARB/USD
- OP/USD
- ADA/USD
- POL/USD
position:
  size_pct: 8
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 29.33
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 68.63
exit:
  take_profit_pct: 4.6
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

---

## ⚡ ONE CHANGE — DO THIS NOW

**Set `entry.short.conditions[0].value` = `66.0`**

Fallback chain (if 66.0 is banned or already tested):
1. `entry.short.conditions[0].value` = `64.0`
2. `entry.short.conditions[0].value` = `62.0`
3. `exit.stop_loss_pct` = `3.0`
4. `exit.take_profit_pct` = `5.5`
5. `entry.long.conditions[0].value` = `27.0`

---

## BANNED VALUES — instant reject, do not use under any circumstances

| Field | Banned values |
|-------|--------------|
| entry.short.conditions[0].value | 68.63 |
| entry.long.conditions[0].value | 29.33, 32.0, 35.97 |
| position.size_pct | 16.91 |
| exit.stop_loss_pct | 2.59, 2.39 |
| exit.take_profit_pct | 4.6, 5.0 |
| exit.timeout_minutes | 720 (do not change) |
| leverage | 2 (do not change) |
| fee_rate | 0.0005 (do not change) |

**ALSO BANNED — configurations that produced trades < 500 or Sharpe < -3.0 are invalid. If your change would tighten both RSI thresholds simultaneously or set rsi_long < 18 or rsi_short > 80, do not submit.**

---

## OUTPUT FORMAT

```
CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=[new_value], stop_loss=2.59, tp=4.6
[FULL YAML BELOW]
```

Output the complete YAML with exactly one value changed from the template above.

---

## PREFLIGHT — verify before output

- [ ] Exactly ONE value differs from champion YAML above
- [ ] Changed value is NOT in banned list
- [ ] All 16 pairs present, same order
- [ ] leverage=2, fee_rate=0.0005, timeout_minutes=720 unchanged
- [ ] YAML is complete — no lines removed or added

---

## CONTEXT

Champion: Gen 3233 | Sharpe=0.4066 | 1756 trades | WR=50.1%
Goal: Sharpe > 0.4066

Previously tested — DO NOT RESUBMIT:
| Field | Value | Result |
|-------|-------|--------|
| entry.short.conditions[0].value | 68.63 | Champion (banned) |
| entry.long.conditions[0].value | 32.0 | Sharpe=0.296 (worse) |
| entry.long.conditions[0].value | 35.97 | Failed |
| position.size_pct | 16.91 | Failed |
| exit.stop_loss_pct | 2.39 | Failed |
| exit.take_profit_pct | 5.0 | Sharpe=0.021 (failed) |

Next priority queue (in order):
1. **rsi_short → 66.0** ← DO THIS NOW
2. rsi_short → 64.0
3. rsi_short → 62.0
4. stop_loss_pct → 3.0
5. take_profit_pct → 5.5
6. rsi_long → 27.0
7. rsi_long → 25.0
8. size_pct → 10
9. take_profit_pct → 4.2
10. stop_loss_pct → 2.8
```

---