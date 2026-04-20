```markdown
# ODIN — FUTURES DAY v39.0

## YOUR ONLY JOB
Output EXACTLY: a CHANGE line, a USING line, then the YAML below with ONE value changed. Nothing else.

---

## CHAMPION YAML — copy exactly, change ONE value only

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

## THIS GENERATION: MAKE THIS EXACT CHANGE

**Change `entry.short.conditions[0].value` from `68.63` to `66.0`**

If `66.0` is in the BANNED list below, use `64.0` instead.
If `64.0` is also banned, use `62.0`.
If all three are banned, change `exit.stop_loss_pct` from `2.59` to `2.3`.

---

## BANNED — DO NOT USE (instant reject if you use any of these)

| Field | Banned values |
|-------|--------------|
| entry.short.conditions[0].value | 68.63 |
| entry.long.conditions[0].value | 29.33, 32.0, 35.97 |
| position.size_pct | 8, 16.91 |
| exit.stop_loss_pct | 2.59, 2.39 |
| exit.take_profit_pct | 4.6, 5.0 |
| timeout_minutes | 720 |
| leverage | 2 |
| fee_rate | 0.0005 |

**Note:** `position.size_pct=8` and most other champion values are banned as the "change target" — they must stay at their champion values unless you are specifically changing them per the instruction above.

---

## TESTED AND FAILED (do not resubmit)

- rsi_short=68.63 — champion, do not resubmit
- rsi_long=32.0 — Sharpe=0.296 (worse)
- rsi_long=35.97 — failed
- size_pct=16.91 — failed
- stop_loss_pct=2.39 — failed
- take_profit_pct=5.0 — Sharpe=0.021 (much worse)

---

## PREFLIGHT — verify before output

- [ ] Exactly ONE value differs from champion YAML
- [ ] Changed value is NOT in BANNED list
- [ ] Changed value is NOT in TESTED AND FAILED list
- [ ] All 16 pairs present, same order
- [ ] fee_rate=0.0005, leverage=2 (unchanged)
- [ ] YAML structure identical to champion

---

## OUTPUT FORMAT (exactly this, nothing else)

CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=[value], stop_loss=2.59, tp=4.6
[YAML]

---

## CONTEXT

Champion: Gen 3233 | Sharpe=0.4066 | 1756 trades | WR=50.1%
Goal: Sharpe > 0.4066
League: futures_day | MIN_TRADES=50

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