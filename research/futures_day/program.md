```markdown
# ODIN — FUTURES DAY v46.0

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
  stop_loss_pct: 2.8
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

---

## ⚡ ONE CHANGE — DO THIS NOW

**Set `exit.take_profit_pct` = `5.5`**

Fallback chain (if 5.5 is banned or already tested):
1. `exit.stop_loss_pct` = `3.0`
2. `exit.take_profit_pct` = `4.2`
3. `position.size_pct` = `10`
4. `entry.long.conditions[0].value` = `27.0`
5. `entry.short.conditions[0].value` = `70.0`
6. `exit.take_profit_pct` = `6.0`
7. `exit.stop_loss_pct` = `2.2`
8. `risk.pause_if_down_pct` = `6`
9. `exit.timeout_minutes` = `360`
10. `position.size_pct` = `6`

---

## BANNED VALUES — instant reject, do not use

| Field | Banned values |
|-------|--------------|
| entry.short.conditions[0].value | 62.0, 64.0, 66.0 |
| entry.long.conditions[0].value | 32.0, 35.97, 25.0 |
| position.size_pct | 16.91 |
| exit.stop_loss_pct | 2.39 |
| exit.take_profit_pct | 5.0 |
| exit.timeout_minutes | 720 (do not change — unless fallback 9 is active) |
| leverage | 2 (do not change) |
| fee_rate | 0.0005 (do not change) |
| pairs | must stay [BTC/USD, ETH/USD, SOL/USD] — do not add or remove |

**MIN_TRADES floor = 200. Configs below 200 trades are auto-rejected.**
**DO NOT submit rsi_short values of 62, 64, or 66 — tested, all produce Sharpe < -3.0.**

---

## OUTPUT FORMAT

```
CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=68.63, stop_loss=2.8, tp=[new_value or 4.6]
[FULL YAML BELOW]
```

Output the complete YAML with exactly one value changed from the template above.

---

## PREFLIGHT — verify before output

- [ ] Exactly ONE value differs from champion YAML above
- [ ] Changed value is NOT in banned list
- [ ] pairs is exactly [BTC/USD, ETH/USD, SOL/USD] — all three, no more, no fewer
- [ ] leverage=2, fee_rate=0.0005 unchanged
- [ ] stop_loss_pct=2.8 is UNCHANGED unless you are specifically changing it
- [ ] rsi_long=29.33 and rsi_short=68.63 are UNCHANGED unless specifically changing one
- [ ] YAML is complete — no lines removed or added

---

## CONTEXT

**Current champion:** Sharpe=-1.8162 | 813 trades | stop_loss=2.8, take_profit=4.6, rsi_long=29.33, rsi_short=68.63

**F8 cost model** (applied 2026-04-22): same params that were Sharpe=+0.4 pre-F8 now produce negative Sharpe. Fee/slippage drag is the primary enemy. Strategy must either: (a) capture more per winner (higher TP), (b) cut losers faster (lower SL), or (c) trade less frequently (tighter RSI = fewer, higher-quality signals).

**Expected trade volume:** 300–800 trades / 2yr backtest on BTC/ETH/SOL-only universe.

**RSI NOTE:** Pre-cost winner zone was rsi_long≈29–30 / rsi_short≈68–70. Tighter thresholds (rsi_short 62–66) all failed. Current thresholds (29.33/68.63) are the validated anchor. Do NOT change RSI unless exit params are exhausted.

---

## Previously tested — DO NOT RESUBMIT

| Field | Value | Result |
|-------|-------|--------|
| exit.stop_loss_pct | 2.8 | **CURRENT CHAMPION** — already in template |
| exit.stop_loss_pct | 2.59 | Previous champion (worse) |
| exit.stop_loss_pct | 2.39 | Failed |
| exit.take_profit_pct | 5.0 | Sharpe=0.021 (failed) |
| exit.take_profit_pct | 4.6 | In template (second best) |
| entry.short.conditions[0].value | 66.0 | Sharpe=-3.28 (failed) |
| entry.short.conditions[0].value | 64.0 | Failed |
| entry.short.conditions[0].value | 62.0 | Failed |
| entry.long.conditions[0].value | 25.0 | Sharpe=-3.28 (failed) |
| entry.long.conditions[0].value | 32.0 | Sharpe=0.296 (worse than champion) |
| entry.long.conditions[0].value | 35.97 | Failed |
| position.size_pct | 16.91 | Failed |

## Next priority queue (in order):
1. **take_profit_pct → 5.5** ← DO THIS NOW
2. stop_loss_pct → 3.0
3. take_profit_pct → 4.2
4. size_pct → 10
5. rsi_long → 27.0
6. rsi_short → 70.0
7. take_profit_pct → 6.0
8. stop_loss_pct → 2.2
9. take_profit_pct → 4.8
10. timeout_minutes → 360
11. size_pct → 6
12. pause_if_down_pct → 6
```

---