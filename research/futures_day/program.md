```markdown
# ODIN — FUTURES DAY v45.0

## UNIVERSE CONSTRAINT — DO NOT VIOLATE
Kraken Derivatives US perpetuals: **BTC/USD, ETH/USD, SOL/USD only.**
Never add pairs beyond these three.

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

**Set `exit.stop_loss_pct` = `2.8`**

Fallback chain (if 2.8 is banned or already tested):
1. `exit.take_profit_pct` = `5.5`
2. `exit.stop_loss_pct` = `3.0`
3. `exit.take_profit_pct` = `4.2`
4. `position.size_pct` = `10`
5. `entry.long.conditions[0].value` = `27.0`
6. `entry.short.conditions[0].value` = `70.0`
7. `risk.pause_if_down_pct` = `6`

---

## BANNED VALUES — instant reject, do not use

| Field | Banned values |
|-------|--------------|
| entry.short.conditions[0].value | 62.0, 64.0, 66.0 |
| entry.long.conditions[0].value | 32.0, 35.97, 25.0 |
| position.size_pct | 16.91 |
| exit.stop_loss_pct | 2.39 |
| exit.take_profit_pct | 5.0 |
| exit.timeout_minutes | 720 (do not change) |
| leverage | 2 (do not change) |
| fee_rate | 0.0005 (do not change) |
| pairs | must stay [BTC/USD, ETH/USD, SOL/USD] — do not add or remove |

**ALSO BANNED — any config with fewer than 800 trades is invalid. Do NOT tighten RSI thresholds below rsi_long=25 or above rsi_short=71. Do NOT submit rsi_short values of 62, 64, or 66 — these have been tested and produce Sharpe < -3.0.**

---

## OUTPUT FORMAT

```
CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=68.63, stop_loss=[new_value or 2.59], tp=[new_value or 4.6]
[FULL YAML BELOW]
```

Output the complete YAML with exactly one value changed from the template above.

---

## PREFLIGHT — verify before output

- [ ] Exactly ONE value differs from champion YAML above
- [ ] Changed value is NOT in banned list
- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD] — all three, no more, no fewer
- [ ] leverage=2, fee_rate=0.0005, timeout_minutes=720 unchanged
- [ ] rsi_long=29.33 and rsi_short=68.63 are UNCHANGED unless you are specifically changing one of them
- [ ] YAML is complete — no lines removed or added

---

## CONTEXT

True Champion: Gen 3233 | Sharpe=0.4066 | 1756 trades | WR=50.1%
Current elite_0: Sharpe=-3.2768 | 482 trades (regression — template above is the CORRECT anchor)
Goal: Sharpe > 0.4066

Expected trade volume on 3-pair universe: 1500–2000 trades / 2yr backtest at rsi_long≈29, rsi_short≈69.
MIN_TRADES floor: 800 (configurations below this are auto-rejected).

**CRITICAL: The winning RSI zone is rsi_long ≈ 29–30, rsi_short ≈ 68–70. Do NOT tighten these thresholds. Tighter RSI (e.g. rsi_short=62–66) has been exhaustively tested and produces deeply negative Sharpe (-3 to -5). Explore exit parameters and position sizing instead.**

Previously tested — DO NOT RESUBMIT:
| Field | Value | Result |
|-------|-------|--------|
| entry.short.conditions[0].value | 66.0 | Sharpe=-3.28 (failed) |
| entry.short.conditions[0].value | 64.0 | Tested, failed |
| entry.short.conditions[0].value | 62.0 | Tested, failed |
| entry.long.conditions[0].value | 25.0 | Sharpe=-3.28 (failed) |
| entry.long.conditions[0].value | 32.0 | Sharpe=0.296 (worse) |
| entry.long.conditions[0].value | 35.97 | Failed |
| position.size_pct | 16.91 | Failed |
| exit.stop_loss_pct | 2.39 | Failed |
| exit.take_profit_pct | 5.0 | Sharpe=0.021 (failed) |
| exit.take_profit_pct | 4.6 | Champion (current) |

Next priority queue (in order):
1. **stop_loss_pct → 2.8** ← DO THIS NOW
2. take_profit_pct → 5.5
3. stop_loss_pct → 3.0
4. take_profit_pct → 4.2
5. size_pct → 10
6. rsi_long → 27.0
7. rsi_short → 70.0
8. stop_loss_pct → 2.2
9. take_profit_pct → 4.8
10. size_pct → 6
```

---