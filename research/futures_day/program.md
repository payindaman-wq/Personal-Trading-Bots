```markdown
# ODIN — FUTURES DAY v40.0

## STEP 1 — OUTPUT FORMAT (do this, nothing else)

CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=[value], stop_loss=2.59, tp=4.6
[YAML]

---

## STEP 2 — CHAMPION YAML (copy exactly, change ONE value only)

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

## STEP 3 — MAKE EXACTLY THIS CHANGE

**Set `entry.short.conditions[0].value` = `66.0`**

Fallback chain (use first value NOT in the BANNED column below):
1. `66.0`
2. `64.0`
3. `62.0`
4. If all banned → set `exit.stop_loss_pct` = `2.3`

---

## STEP 4 — BANNED VALUES (instant reject if used)

| Field | BANNED — never use these |
|-------|--------------------------|
| entry.short.conditions[0].value | 68.63 |
| entry.long.conditions[0].value | 29.33, 32.0, 35.97 |
| position.size_pct | 8, 16.91 |
| exit.stop_loss_pct | 2.59, 2.39 |
| exit.take_profit_pct | 4.6, 5.0 |
| exit.timeout_minutes | 720 |
| leverage | 2 |
| fee_rate | 0.0005 |

**Note:** `position.size_pct` MUST remain 8 (it is banned as a *change target*, not as a yaml value — keep it at 8).
**Note:** `leverage`, `fee_rate`, `timeout_minutes` must remain at their champion values above.

---

## STEP 5 — PREFLIGHT (check before outputting)

- [ ] Exactly ONE value changed from champion YAML
- [ ] Changed value is NOT in BANNED list
- [ ] All 16 pairs present, same order
- [ ] leverage=2, fee_rate=0.0005, timeout_minutes=720 (unchanged)
- [ ] YAML structure identical to champion

---

## CONTEXT

Champion: Gen 3233 | Sharpe=0.4066 | 1756 trades | WR=50.1%
Goal: Sharpe > 0.4066
League: futures_day | MIN_TRADES=50

Previously tested (do not resubmit):
- rsi_short=68.63 → champion (current)
- rsi_long=32.0 → Sharpe=0.296 (worse)
- rsi_long=35.97 → failed
- size_pct=16.91 → failed
- stop_loss_pct=2.39 → failed
- take_profit_pct=5.0 → Sharpe=0.021 (failed)

Priority ladder (first untested wins):
1. rsi_short → 66.0
2. rsi_short → 64.0
3. rsi_short → 62.0
4. stop_loss_pct → 2.3
5. size_pct → 10
6. take_profit_pct → 4.2
7. rsi_long → 27.0
```

---