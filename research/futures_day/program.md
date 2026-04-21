```markdown
# ODIN — FUTURES DAY v41.0

## YOUR ONLY JOB

Output ONE change to the YAML below. The changed YAML must pass the checklist. Nothing else.

---

## OUTPUT FORMAT

```
CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=[new_value], stop_loss=2.59, tp=4.6
[YAML]
```

---

## CHAMPION YAML — COPY THIS EXACTLY, THEN CHANGE EXACTLY ONE VALUE

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
      value: 66.0        ← CHANGE IS HERE (was 68.63, now 66.0)
exit:
  take_profit_pct: 4.6
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

**THE ONLY CHANGE:** `entry.short.conditions[0].value` changed from `68.63` → `66.0`

The `← CHANGE IS HERE` annotation must NOT appear in your output YAML. Remove it.

---

## BANNED VALUES — INSTANT REJECT IF USED

| Field | Never use |
|-------|-----------|
| entry.short.conditions[0].value | **68.63** ← the old champion value — DO NOT USE |
| entry.long.conditions[0].value | 29.33 (keep it, don't change it), 32.0, 35.97 |
| position.size_pct | 16.91 (keep at 8) |
| exit.stop_loss_pct | 2.59 (keep it), 2.39 |
| exit.take_profit_pct | 4.6 (keep it), 5.0 |
| exit.timeout_minutes | 720 (keep it) |
| leverage | 2 (keep it) |
| fee_rate | 0.0005 (keep it) |

**CRITICAL:** If you output `value: 68.63` under `entry.short`, your result will be rejected as a duplicate. Use `66.0`.

---

## FALLBACK CHAIN

If 66.0 is unavailable or banned, try in order:
1. `entry.short.conditions[0].value` = `64.0`
2. `entry.short.conditions[0].value` = `62.0`
3. `exit.stop_loss_pct` = `2.3`
4. `position.size_pct` = `10`

---

## PREFLIGHT — CHECK BEFORE OUTPUTTING

- [ ] `entry.short.conditions[0].value` is `66.0` (NOT `68.63`)
- [ ] `entry.long.conditions[0].value` is still `29.33` (unchanged)
- [ ] `exit.take_profit_pct` is still `4.6` (unchanged)
- [ ] `exit.stop_loss_pct` is still `2.59` (unchanged)
- [ ] `exit.timeout_minutes` is still `720` (unchanged)
- [ ] `leverage` is still `2` (unchanged)
- [ ] `fee_rate` is still `0.0005` (unchanged)
- [ ] All 16 pairs present in exact order shown
- [ ] Exactly ONE value differs from champion YAML
- [ ] No annotation text (← arrows) in output YAML

---

## CONTEXT

Champion: Gen 3233 | Sharpe=0.4066 | 1756 trades | WR=50.1%
Goal: Sharpe > 0.4066

Previously tested — DO NOT RESUBMIT:
- rsi_short=68.63 → current champion
- rsi_long=32.0 → Sharpe=0.296 (worse)
- rsi_long=35.97 → failed
- size_pct=16.91 → failed
- stop_loss_pct=2.39 → failed
- take_profit_pct=5.0 → Sharpe=0.021 (failed)

Next to test after this (do not jump ahead):
1. rsi_short=64.0
2. rsi_short=62.0
3. stop_loss_pct=2.3
4. size_pct=10
5. take_profit_pct=4.2
6. rsi_long=27.0
```

---