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
4. Did I change `period_hours` anywhere? → NO, or START OVER
5. Did I change the short RSI value `60.64`? → NO, or START OVER
6. Did I change any other field? → NO, or START OVER

If any answer is wrong → discard output and start over with a different value from the list.

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

❌ WRONG — changed period_hours (FORBIDDEN):
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
|-------|---------------|
| `entry.long.conditions[0].value` | One of: 33.00, 33.50, 34.50, 35.00, 35.50, 36.00 — NOT 34.00 |
| `entry.long.conditions[0].period_hours` | MUST be 21 — do not change |
| `entry.short.conditions[0].value` | MUST be 60.64 — do not change |
| `entry.short.conditions[0].period_hours` | MUST be 21 — do not change |
| `entry.long.conditions[1].period_hours` | MUST be 26 — do not change |
| `entry.short.conditions[1].period_hours` | MUST be 48 — do not change |
| `pairs` | MUST be exactly: LINK/USD, ADA/USD, BTC/USD, OP/USD |
| `max_open` | MUST be 1 |
| `timeout_hours` | MUST be 200 |
| `take_profit_pct` | MUST be 3.55 |
| `stop_loss_pct` | MUST be 2.41 |

---

## CONTEXT: WHY THIS RANGE WORKS

Long RSI values in the range 33–36 produce 20–35 trades over 2 years with 80–90% win rate.
This is the correct behavior. Do not be alarmed by the low trade count.
A result of 25–35 trades and 75%+ win rate is SUCCESS.
A result of 400–550 trades and 52% win rate is FAILURE — that means period_hours or another field was changed.

The all-time best result was Sharpe=2.9286 at approximately long RSI < 34.00 (30 trades, 90% win rate).
Your goal is to find a value in [33.00, 36.00] that matches or exceeds this.

---

## IF THE ABOVE IS IMPOSSIBLE — FALLBACK OPTIONS ONLY

Use these ONLY if Option D (changing long RSI value) is genuinely impossible.

**Fallback E:** Change short RSI `value` from `60.64` to one of: `63.00` / `63.50` / `64.00` / `64.50` / `65.00`
**Fallback A:** Change `take_profit_pct` from `3.55` to one of: `4.50` / `5.00` / `5.50` / `6.00`
**Fallback C:** Change `timeout_hours` from `200` to one of: `240` / `280` / `320`

Prefer Option D above all fallbacks.
```

---

## INFRASTRUCTURE CHANGES (LOKI RECOMMENDATIONS — PRIORITY ORDER)

### CRITICAL — Implement before next run

**1. Override current best with Gen 2126 config**

The all-time best Sharpe is 2.9286 (Gen 2126), not the current incumbent (2.4401). The optimization drifted into a worse basin (Regime B: ~477 trades, 52.9% win rate) starting at Gen 2149 and has not recovered in 5,600+ generations. Restore Gen 2126 as the incumbent manually.

Gen 2126 approximate config (reconstruct from optimization history):
- All fields identical to current best EXCEPT: `entry.long.conditions[0].value` ≈ 34.00 (the value that produced 30 trades, 90% win rate)
- The updated research program above reflects this restoration

**2. Add MAX_TRADES guard to backtester**

```python
# In backtester evaluation logic:
MAX_TRADES = {"swing": 150}  # Regime B produces 400-550; Regime A produces 20-50

if result.trades > MAX_TRADES[style]:
    log(f"REJECTED: {result.trades} trades exceeds MAX_TRADES={MAX_TRADES[style]} — Regime B detected")
    return  # do not update best
```

This single change prevents Regime B from ever becoming the incumbent, regardless of Sharpe. Regime A at Sharpe 2.93 and 30 trades will always beat Regime B at Sharpe 2.53 and 477 trades under this guard.

**3. Hard-reject the 176-trade attractor in backtester**

```python
# Add to attractor detection logic:
KNOWN_BAD_ATTRACTORS = [
    {"trades_range": (160, 195), "sharpe_range": (-1.5, -1.0), "label": "RSI_period_change_attractor"},
    {"trades_range": (195, 220), "sharpe_range": (-1.8, -1.1), "label": "RSI_period_change_attractor_2"},
]

for attractor in KNOWN_BAD_ATTRACTORS:
    if (attractor["trades_range"][0] <= result.trades <= attractor["trades_range"][1] and
        attractor["sharpe