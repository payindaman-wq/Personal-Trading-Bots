```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text, no comments.

---

## YOUR ONLY TASK

Change the long entry RSI `value` field.

The current value is `34.00`.

**ALLOWED VALUES — copy one exactly (these are the ONLY six valid outputs):**
- `33.00`
- `33.50`
- `34.50`
- `35.00`
- `35.50`
- `36.00`

**Try them in this order (prefer values not recently tested):**
1. `33.50`
2. `33.00`
3. `34.50`
4. `35.00`
5. `35.50`
6. `36.00`

**Rules:**
- Change ONLY `entry.long.conditions[0].value`
- Do NOT change any other field
- Do NOT change any `period_hours` field
- Do NOT output any value other than the six listed above
- If you are unsure, output `33.50`

---

## SELF-CHECK — 5 STEPS

Before outputting, verify each of these exactly:

1. The field I changed is `entry.long.conditions[0].value` — YES/NO
2. The new value is one of the six listed above (33.00, 33.50, 34.50, 35.00, 35.50, 36.00) — YES/NO
3. `entry.short.conditions[0].value` is still `60.64` — YES/NO
4. `take_profit_pct` is still `3.55` and `stop_loss_pct` is still `2.41` — YES/NO
5. All `period_hours` values are still: 21, 26, 21, 48 (in order) — YES/NO

If any answer is NO, output the CORRECT OUTPUT EXAMPLE below exactly as written.

---

## Current Best Strategy — COPY EXACTLY, CHANGE ONLY THE ONE MARKED FIELD

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

## CORRECT OUTPUT EXAMPLE
(Use this exactly if your self-check fails, substituting only the value field with one of the six allowed values)

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
      value: 33.50
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

## FIELD REFERENCE TABLE

| Field | Required value | VALID options |
|-------|----------------|---------------|
| `entry.long.conditions[0].value` | One of six below | 33.00, 33.50, 34.50, 35.00, 35.50, 36.00 |
| `entry.long.conditions[0].period_hours` | 21 | 21 only |
| `entry.long.conditions[1].period_hours` | 26 | 26 only |
| `entry.short.conditions[0].value` | 60.64 | 60.64 only |
| `entry.short.conditions[0].period_hours` | 21 | 21 only |
| `entry.short.conditions[1].period_hours` | 48 | 48 only |
| `take_profit_pct` | 3.55 | 3.55 only |
| `stop_loss_pct` | 2.41 | 2.41 only |
| `timeout_hours` | 200 | 200 only |
| `size_pct` | 30 | 30 only |
| `max_open` | 1 | 1 only |
| `fee_rate` | 0.001 | 0.001 only |
| `pairs` | LINK/USD, ADA/USD, BTC/USD, OP/USD | no changes |

---

## EXPECTED BACKTEST RESULTS

A correct output will produce:
- **20–100 trades** over 2 years
- **75–90% win rate**
- **Sharpe 2.5–3.0**

Results outside these ranges indicate an error in your output. The target is low trade count with high win rate.
```

---

## OPERATOR NOTES (not part of LLM prompt — for MIMIR/ODIN system only)

### Pre-Run Checklist (execute before next generation):

**[CRITICAL] Restore incumbent:**
```yaml
entry.long.conditions[0].value: 34.00
# All other fields per template above
# Incumbent Sharpe: 2.9232
# Source: Gen 2126
```

**[CRITICAL] Add backtesting guard:**
```python
# Acceptance logic — add both guards:
MIN_TRADES = {"day": 250, "swing": 20}
MAX_TRADES = {"day": 9999, "swing": 100}

# Reject if:
if trades < MIN_TRADES[style] or trades > MAX_TRADES[style]:
    return "rejected: trade count out of bounds"
```

**[CRITICAL] Lock MIN_TRADES:**
- Set `MIN_TRADES[swing] = 20` — do not change again without MIMIR sign-off
- Rationale: Gen 2126 had 30 trades (clears 20). Values below 20 allow noisy results. Values above 30 would have rejected Gen 2126 itself.

**[CRITICAL] Audit live deployment:**
- Current live config almost certainly running corrupted Regime B incumbent (`value: 36.68` or similar)
- Live sprint 50% win rate confirms Regime B fingerprint
- Swap live bot to Gen 2126 config immediately
- Expected live improvement: win rate from ~50% → ~80–90%

**[IMPORTANT] Hallucination guard:**
- Add post-LLM output validation before backtesting:
```python
ALLOWED_RSI_LONG = {33.00, 33.50, 34.50, 35.00, 35.50, 36.00}
parsed_value = yaml.safe_load(llm_output)
rsi_val = parsed_value['entry']['long']['conditions'][0]['value']
if rsi_val not in ALLOWED_RSI_LONG:
    return "rejected: hallucinated value"
```
- This catches `36.68` and any other non-listed values before they corrupt the incumbent

**[IMPORTANT] After RSI search completes (all 6 values tested in Regime A):**

Expand search in this priority order:
1. `take_profit_pct`: test {3.05, 3.30, 3.55, 3.80, 4.05} (±0.25 steps)
2. `stop_loss_pct`: test {2.11, 2.21, 2.31, 2.41, 2.51, 2.61} (±0.10 steps)
3. `entry.short.conditions[0].value`: test {58.64, 59.64, 60.64, 61.64, 62.64} (±1.0 steps)
4. `timeout_hours`: test {150, 175, 200, 225, 250} (±25 steps)
5. `entry.long.conditions[0].period_hours`: test {14, 18, 21, 24, 28} (RSI period)
6. `entry.long.conditions[1].period_hours`: test {20, 23, 26, 29, 32} (MACD period)

Each parameter search must:
- Use a locked, validated Regime A incumbent as starting point
- Apply the MAX_TRADES=