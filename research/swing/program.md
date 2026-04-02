```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text, no comments.

---

## ⚠️ YOUR ONLY TASK ⚠️

Change the long entry RSI `value` from `34.00` to a number from this list:
`33.00` / `33.50` / `34.50` / `35.00` / `35.50` / `36.00`

Pick the one you have NOT tried recently.

**DO NOT change any other field. One number changes. Everything else is identical.**

---

## ⚠️ SELF-CHECK — COMPLETE BEFORE OUTPUTTING ⚠️

Answer each question internally before writing output:

1. Which field am I changing? → `entry.long.conditions[0].value`
2. Is the new value in this list: `33.00 / 33.50 / 34.50 / 35.00 / 35.50 / 36.00`? → YES or START OVER
3. Is the new value different from `34.00`? → YES or START OVER
4. Did I change `period_hours` anywhere? → NO or START OVER
5. Did I change the short RSI value `60.64`? → NO or START OVER
6. Did I change any other field? → NO or START OVER

If any answer is wrong → discard output and start over with a different value from the list.

---

## ⚠️ REGIME GUARD — READ THIS BEFORE SUBMITTING ⚠️

This strategy operates in two radically different regimes. You MUST target Regime A only.

| Regime | Trades (2yr backtest) | Win Rate | Sharpe | Status |
|--------|----------------------|----------|--------|--------|
| **Regime A** ✅ | 20–50 | 75–90% | 2.5–2.93 | TARGET |
| **Regime B** ❌ | 400–550 | 50–55% | 1.5–2.5 | REJECT |
| **Attractor** ❌ | 150–220 | 38–42% | −1.8 to −1.0 | REJECT |

**Regime B is caused by changing `period_hours` on any indicator.** Do not change any `period_hours` field. If you change `period_hours`, the backtester will produce 400–550 trades and the result will be discarded.

The all-time best result is **Sharpe=2.9232** (30 trades, 90% win rate) — achieved with long RSI < 34.00.
Your goal: find a value in [33.00, 36.00] that matches or exceeds this.

A result of 20–50 trades and 75%+ win rate = SUCCESS.
A result of 400–550 trades and ~52% win rate = REGIME B FAILURE — means you changed `period_hours` or another structural field.
A result of 150–220 trades and ~40% win rate = ATTRACTOR FAILURE — means you changed `period_hours` to a mid-range value.

---

## Current Best Strategy — COPY EXACTLY, CHANGE ONLY THE ONE FIELD MARKED BELOW

```yaml
name: crossover
style: randomly generated
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
position:
  size_pct: 30
  max_open: 1
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 34.00        ← CHANGE THIS NUMBER ONLY
    - indicator: macd_signal
      period_hours: 26
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: gt
      value: 60.64
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bearish
exit:
  take_profit_pct: 3.55
  stop_loss_pct: 2.41
  timeout_hours: 200
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

---

## CORRECT OUTPUT FORMAT — COPY THIS STRUCTURE EXACTLY

The output must be the full YAML. The ONLY difference from above is the `value:` field on the long RSI line.

✅ CORRECT — changed only the long RSI value:
```yaml
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 33.50
```

❌ WRONG — changed period_hours (causes Regime B or Attractor — FORBIDDEN):
```yaml
    - indicator: rsi
      period_hours: 18
      operator: lt
      value: 33.50
```

❌ WRONG — value unchanged (still 34.00):
```yaml
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 34.00
```

❌ WRONG — value not in allowed list (e.g. 36.68 is NOT allowed):
```yaml
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 36.68
```

❌ WRONG — changed short RSI value:
```yaml
    - indicator: rsi
      period_hours: 21
      operator: gt
      value: 63.00
```

---

## ABSOLUTE RULES — YOUR OUTPUT MUST SATISFY ALL OF THESE

| Field | Required value |
|-------|----------------|
| `entry.long.conditions[0].value` | One of: 33.00, 33.50, 34.50, 35.00, 35.50, 36.00 — NOT 34.00, NOT 36.68, NOT any other number |
| `entry.long.conditions[0].period_hours` | MUST be 21 — do not change |
| `entry.long.conditions[0].operator` | MUST be `lt` — do not change |
| `entry.short.conditions[0].value` | MUST be 60.64 — do not change |
| `entry.short.conditions[0].period_hours` | MUST be 21 — do not change |
| `entry.long.conditions[1].period_hours` | MUST be 26 — do not change |
| `entry.short.conditions[1].period_hours` | MUST be 48 — do not change |
| `pairs` | MUST be exactly: LINK/USD, ADA/USD, BTC/USD, OP/USD |
| `max_open` | MUST be 1 |
| `timeout_hours` | MUST be 200 |
| `take_profit_pct` | MUST be 3.55 |
| `stop_loss_pct` | MUST be 2.41 |
| `size_pct` | MUST be 30 |
| `fee_rate` | MUST be 0.001 |

---

## CONTEXT: WHY THIS RANGE WORKS

Long RSI values in the range 33–36 produce 20–50 trades over 2 years with 75–90% win rate.
This is the correct behavior — a low trade count with high win rate is the goal.
Do not be alarmed by the low trade count.

| Result | Interpretation |
|--------|---------------|
| 20–50 trades, 75%+ win rate, Sharpe > 2.0 | ✅ SUCCESS — Regime A |
| 400–550 trades, ~52% win rate | ❌ FAILURE — Regime B (period_hours was changed) |
| 150–220 trades, ~40% win rate, Sharpe < −1.0 | ❌ FAILURE — Attractor (period_hours was changed) |

The all-time best result was **Sharpe=2.9232** at long RSI < 34.00 (30 trades, 90% win rate).
Your goal is to find a value in [33.00, 36.00] that matches or exceeds this.

Cycle through the allowed values systematically:
- Try 33.50 if not recently tried
- Try 34.50 if not recently tried
- Try 33.00 if not recently tried
- Try 35.00 if not recently tried
- Try 35.50 if not recently tried
- Try 36.00 if not recently tried

---

## IF THE ABOVE IS IMPOSSIBLE — FALLBACK OPTIONS ONLY

Use these ONLY if Option D (changing long RSI value) is genuinely impossible.
**Do not use fallbacks unless you have exhausted all 6 values in the allowed list.**

**Fallback E:** Change short RSI `value` from `60.64` to one of: `63.00` / `63.50` / `64.00` / `64.50` / `65.00`
**Fallback A:** Change `take_profit_pct` from `3.55` to one of: `4.50` / `5.00` / `5.50` / `6.00`
**Fallback C:** Change `timeout_hours` from `200` to one of: `240` / `280` / `320`
**Fallback S:** Change `stop_loss_pct` from `2.41` to one of: `2.00` / `2.20` / `2.60` / `2.80`

Prefer Option D above all fallbacks.
Never use a fallback that changes `period_hours` or `pairs`.
```

---

## INFRASTRUCTURE CHANGES (LOKI RECOMMENDATIONS — PRIORITY ORDER)

### CRITICAL — Implement before next run

**1. Restore Gen 2126 as incumbent immediately**

The all-time best Sharpe is **2.9232** (Gen 2126): 30 trades, 90% win rate, long RSI < 34.00.