```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text, no comments.

---

## ⚠️ REGIME LOCK — READ FIRST

This strategy operates in **Regime A**: 20–50 trades over 2 years, 80–90% win rate, Sharpe ~2.9.
Any config producing more than 100 trades or less than 20 trades is **wrong** and will be auto-rejected.
Do NOT increase RSI values above 36.00 — doing so breaks the regime and destroys win rate.
Do NOT output any value not listed in the allowed values below.

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
- Do NOT output any value not in the six listed above — not 36.68, not 34.2, not anything else
- If you are unsure, output `33.50`

---

## SELF-CHECK — 5 STEPS

Before outputting, verify each of these exactly:

1. The field I changed is `entry.long.conditions[0].value` — YES/NO
2. The new value is one of exactly these six: 33.00, 33.50, 34.50, 35.00, 35.50, 36.00 — YES/NO
3. `entry.short.conditions[0].value` is still `60.64` — YES/NO
4. `take_profit_pct` is still `3.55` and `stop_loss_pct` is still `2.41` — YES/NO
5. All `period_hours` values are still: 21, 26, 21, 48 (in order) — YES/NO

If ANY answer is NO → output the CORRECT OUTPUT EXAMPLE below exactly as written.

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
(Use this exactly if your self-check fails)

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

## EXPECTED BACKTEST RESULTS (REGIME A)

A correct output will produce:
- **20–50 trades** over 2 years
- **80–90% win rate**
- **Sharpe 2.5–3.1**

If your output produces >100 trades or <20 trades, it is **wrong**.
If win rate is below 75%, the value you chose is **too high** — try a lower value next time.
The goal is selective, high-confidence entries — not frequent trading.
```

---

## OPERATOR NOTES (not part of LLM prompt — for MIMIR/ODIN system only)

### ⚠️ CRITICAL: Pre-Run Actions Required Before Next Generation

**[CRITICAL — DO IMMEDIATELY] Restore Gen 2126 incumbent:**
```yaml
# Restore this as the active incumbent before any further backtesting
entry.long.conditions[0].value: 34.00
entry.short.conditions[0].value: 60.64
take_profit_pct: 3.55
stop_loss_pct: 2.41
timeout_hours: 200
period_hours: 21, 26, 21, 48 (in order)
# Incumbent Sharpe: 2.9232 | Win rate: 90.0% | Trades: 30
# Source: Gen 2126
# All other fields per template above
```
The current incumbent (`value: 36.68`, Sharpe 2.44, 477 trades) is a **Regime B artifact caused by a hallucinated RSI value that bypassed validation.** It must not be used as a starting point.

**[CRITICAL — DO IMMEDIATELY] Set and lock trade count bounds:**
```python
MIN_TRADES = {"day": 250, "swing": 25}
MAX_TRADES = {"day": 9999, "swing": 100}

# Reject if outside bounds:
if trades < MIN_TRADES[style] or trades > MAX_TRADES[style]:
    return f"rejected: trade count {trades} out of bounds [{MIN_TRADES[style]}, {MAX_TRADES[style]}]"
```
- MIN_TRADES[swing] = 25. **Do not change without documented MIMIR sign-off.**
- Rationale: Gen 2126 had 30 trades (clears 25). Regime B has 345–523 trades (correctly rejected). Any value below 20 allows noisy low-trade configs; any value above 30 would have rejected Gen 2126 itself.
- History of oscillation (10→20→25→20→25→20) caused the Regime B corruption. This ends now.

**[CRITICAL — DO IMMEDIATELY] Activate hallucination guard:**
```python
ALLOWED_RSI_LONG = {33.00, 33.50, 34.00, 34.50, 35.00, 35.50, 36.00}

def validate_llm_output(llm_output: str, current_incumbent: dict) -> dict | str:
    try:
        parsed = yaml.safe_load(llm_output)
    except Exception:
        return "rejected: invalid yaml"
    
    rsi_val = parsed['entry']['long']['conditions'][0]['value']
    if rsi_val not in ALLOWED_RSI_LONG:
        return f"rejected: hallucinated RSI value {rsi_val}"
    
    # Validate all locked fields match incumbent
    locked_fields = {
        ('entry', 'short', 'conditions', 0, 'value'): 60.64,
        ('exit', 'take_profit_pct'): 3.55,
        ('exit', 'stop_loss_pct'): 2.41,
        ('exit', 'timeout_hours'): 200,
    }
    for field_path, expected in locked_fields.items():
        # (implement path traversal)
        if get_nested(parsed, field_path) != expected:
            return f"rejected: locked field {field_