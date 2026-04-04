```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text, no comments.

---

## YOUR ONLY TASK

Change the long entry RSI `value` field.

The current value is `34.00`.

You MUST output exactly one of these six values. Copy it character for character, no rounding, no decimals added or removed:

```
33.00
33.50
34.50
35.00
35.50
36.00
```

DO NOT USE THESE VALUES — they have already been tested this session:
{already_tested}

Try untested values in this order:
1. `33.50`
2. `33.00`
3. `34.50`
4. `35.00`
5. `35.50`
6. `36.00`

If all values are listed in DO NOT USE above, output `33.50`.
If unsure which to pick, output `33.50`.

FORBIDDEN VALUES — these will be rejected and waste a generation:
- 36.68  (not in the allowed list — this value broke the strategy at Gen 2149)
- 34.0   (must be 34.00 — but also this is the current value, do not keep it unchanged)
- Any value not exactly matching one of the six above

---

## SELF-CHECK — COMPLETE THIS BEFORE OUTPUTTING

Answer each question. If ANY answer is NO, output the FALLBACK YAML instead.

1. Did I change ONLY `entry.long.conditions[0].value`? YES/NO
2. Is the new value EXACTLY one of: 33.00, 33.50, 34.50, 35.00, 35.50, 36.00? YES/NO
3. Is the new value DIFFERENT from 34.00 (the current value)? YES/NO
4. Is `entry.short.conditions[0].value` still exactly `60.64`? YES/NO
5. Is `take_profit_pct` still exactly `3.55`? YES/NO
6. Is `stop_loss_pct` still exactly `2.41`? YES/NO
7. Are `period_hours` values still 21, 26, 21, 48 in order? YES/NO
8. Is the new value NOT in the DO NOT USE list above? YES/NO

If ALL answers are YES → output your modified YAML.
If ANY answer is NO → output the FALLBACK YAML exactly as written below.

---

## Current Best Strategy

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

## FALLBACK YAML
(Output this exactly — character for character — if your self-check fails)

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

## LOCKED FIELDS — DO NOT CHANGE ANY OF THESE

| Field | Locked value |
|-------|-------------|
| `entry.long.conditions[0].period_hours` | 21 |
| `entry.long.conditions[1].period_hours` | 26 |
| `entry.short.conditions[0].value` | 60.64 |
| `entry.short.conditions[0].period_hours` | 21 |
| `entry.short.conditions[1].period_hours` | 48 |
| `take_profit_pct` | 3.55 |
| `stop_loss_pct` | 2.41 |
| `timeout_hours` | 200 |
| `size_pct` | 30 |
| `max_open` | 1 |
| `fee_rate` | 0.001 |

---

## ⚠️ FOR ODIN/MIMIR SYSTEM — NOT SHOWN TO LLM
## ⚠️ ALL ITEMS BELOW ARE MANDATORY. IMPLEMENT BEFORE GEN 9401. NO EXCEPTIONS.

---

### [CRITICAL — IMPLEMENT NOW] STEP 0: INCUMBENT RESTORE

**Execute this before any further backtesting.**

The current ODIN incumbent is RSI=36.68, Sharpe≈2.50, ~479 trades.
This is a Regime B artifact. It must be replaced immediately.

The true all-time best is Gen 2126:
```
entry.long.conditions[0].value: 34.00
entry.short.conditions[0].value: 60.64
take_profit_pct: 3.55
stop_loss_pct: 2.41
timeout_hours: 200
period_hours: [21, 26, 21, 48]
Sharpe: 2.9232 | Win rate: 90.0% | Trades: 30
```

**Action:** Force-set ODIN's incumbent to the Gen 2126 config above.
Do not backtest it again — just set it directly. Log as `[MIMIR_RESTORE gen=2126]`.
Reset `tested_rsi_values` to empty set.
Reset `duplicate_result_cache` to empty set.
The research program resumes from this incumbent.

**Why Gen 2149 was corrupt:** RSI=36.68 is not on the whitelist. It was a hallucinated value
that the backtester accepted. It produced 345 trades at 53.6% win rate vs. 30 trades at 90%
win rate for the true best. Every "improvement" from Gen 2149 to Gen 9400 was optimization
within a broken parameter regime. All Regime B results are discarded.

---

### [CRITICAL — IMPLEMENT NOW] STEP 1: ACCEPTANCE FILTER

Add these hard bounds. A result MUST pass both or it is rejected without updating incumbent.
Log rejected results as `[regime_b_reject]`.

```python
MIN_TRADES = {"day": 250, "swing": 25}
MAX_TRADES = {"day": 9999, "swing": 50}

def accept_result(trades: int, style: str, sharpe: float) -> bool:
    """
    Regime A (valid):   21–50 trades, 66–90% win rate, Sharpe 1.5–3.5
    Regime B (corrupt): 345–530 trades, 50–53% win rate — REJECT ALL
    
    MAX_TRADES=50 is the critical bound. It would have blocked Gen 2149.
    MIN_TRADES=25 is consistent with all valid Regime A results (21–30 trades).
    Note: 21 trades at Gen 303 is slightly below 25 — keep MIN_TRADES=25 as floor
    but do not reject results between 21–24 if Sharpe > 2.0 (log as [near_floor]).
    """
    if trades < MIN_TRADES[style]:
        return False   # too few — insufficient statistical signal
    if trades > MAX_TRADES[style]:
        return False   # regime collapse — RSI threshold too loose
    return True
```

**DO NOT CHANGE MIN_TRADES[swing] AGAIN.**
The audit log shows it was changed 8 times between Gen 6400–8800 with zero benefit.
MIN_TRADES=25 is final. The oscillation was a distraction from the real problem (no MAX_TRADES).
MAX_TRADES=50 is now enforced. It is also final.

---

### [CRITICAL — IMPLEMENT NOW] STEP 2: RSI WHITELIST VALIDATOR

Run this check BEFORE every backtest. If validation fails:
- Discard the config without backtesting
- Log as `[invalid_rsi value=X]`
- Do NOT count as a generation toward the total
- Do NOT update any cache or incumbent

```python
ALLOWED_RSI_LONG = {"33.00", "33.50", "34.00", "34.50", "35.00", "35.50", "36.00"}

def validate_config(yaml_str: str) -> bool:
    raw = extract_field(yaml_str, "entry.long.conditions[0].value")
    try:
        normalized = f"{float(raw):.2f}"
    except (ValueError, TypeError):
        log(f"[invalid_rsi] Could not parse value: {raw}")
        return False
    if normalized not in ALLOWED_RSI_LONG:
        log(f"[invalid_rsi] Rejected value: {raw} (normalized: {normalized})")
        return False
    return True
```

**Also validate these locked fields before every backtest:**
```python
def validate_locked_fields(yaml_str: str) -> bool:
    checks = {
        "entry.short.conditions[0].value": "60.64",
        "exit.take_profit_pct": "3.55",
        "exit.stop_loss_pct": "2.41",
        "exit.timeout_hours": "200",
    }
    for field, expected in checks.items():
        actual = extract_field(yaml_str, field)
        if f"{float(actual):.2f}" != expected and str(actual) != expected:
            log(f"[locked_field_violation] {field}={actual}, expected {expected}")
            return False
    return True
```

---

### [CRITICAL — IMPLEMENT NOW] STEP 3: DEDUPLICATION CACHE

The last 20 gens show sharpe=-1.3913/trades=166 appearing ~13 times.
This loop MUST be broken immediately. Implement the cache NOW — it is not optional.

```python
tested_rsi_values: set[str] = set()       # reset when incumbent changes
duplicate_result_cache: set[