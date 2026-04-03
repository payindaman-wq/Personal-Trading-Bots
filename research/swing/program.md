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
- 36.68  (not in the allowed list)
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

---

### [CRITICAL — EXECUTE BEFORE GEN 9201] INCUMBENT RESTORE

The current incumbent (RSI 36.68, Sharpe 2.50, 479 trades) is a Regime B artifact
caused by a hallucinated RSI value at Gen 2149. It must be replaced immediately.

**Restore Gen 2126 as incumbent:**
```yaml
entry.long.conditions[0].value: 34.00
entry.short.conditions[0].value: 60.64
take_profit_pct: 3.55
stop_loss_pct: 2.41
timeout_hours: 200
period_hours: [21, 26, 21, 48]
# Sharpe: 2.9232 | Win rate: 90.0% | Trades: 30
```

Gen 2126 is the true all-time best. All Gen 2149–9200 "improvements" are improvements
within a corrupt regime and must be discarded. The research program resumes from Gen 2126.

---

### [CRITICAL — EXECUTE BEFORE GEN 9201] ACCEPTANCE FILTER

Add these hard bounds. Both must pass or the result is rejected without updating incumbent:

```python
MIN_TRADES = {"day": 250, "swing": 25}
MAX_TRADES = {"day": 9999, "swing": 50}

def accept_result(trades: int, style: str, sharpe: float) -> bool:
    """
    Returns True only if trade count is within valid bounds.
    Regime A (good): 21-30 trades, 66-90% win rate, Sharpe 2.3-2.92
    Regime B (corrupt): 345-530 trades, 50-53% win rate — REJECT ALL
    MAX_TRADES=50 would have blocked Gen 2149 and prevented entire Regime B.
    """
    if trades < MIN_TRADES[style]:
        return False   # too few — not enough signal
    if trades > MAX_TRADES[style]:
        return False   # regime collapse — RSI too loose, reject hard
    return True

# DO NOT CHANGE MIN_TRADES[swing] AGAIN.
# Oscillating it between 10-30 provided zero benefit (see audit log).
# The real filter gap was always MAX_TRADES. It is now fixed at 50.
# MIN_TRADES[swing] = 25 is correct and consistent with all Regime A results.
```

---

### [CRITICAL — EXECUTE BEFORE GEN 9201] RSI WHITELIST VALIDATOR

Run this check before every backtest. If it fails, discard without backtesting,
log as [invalid_rsi], and do NOT count as a generation toward the total:

```python
ALLOWED_RSI_LONG = {"33.00", "33.50", "34.00", "34.50", "35.00", "35.50", "36.00"}

def validate_config(yaml_str: str) -> bool:
    """
    Prevents hallucinated values like 36.68 from ever reaching the backtester.
    Gen 2149's RSI=36.68 caused the entire Regime B collapse. This stops recurrence.
    """
    raw = extract_field(yaml_str, "entry.long.conditions[0].value")
    normalized = str(round(float(raw), 2))
    if normalized not in ALLOWED_RSI_LONG:
        log(f"[invalid_rsi] Rejected value: {raw} (normalized: {normalized})")
        return False
    return True
```

---

### [CRITICAL — EXECUTE BEFORE GEN 9201] DEDUPLICATION CACHE

The last 20 gens show sharpe=-1.3913 / trades=166 appearing 8 times.
The LLM is looping. Add a session cache and inject tested values into the prompt:

```python
tested_rsi_values: set[str] = set()   # reset each time incumbent changes
duplicate_result_cache: set[tuple] = set()  # (sharpe_rounded, trades) pairs

def get_prompt(current_value: str) -> str:
    already_tested = ", ".join(sorted(tested_rsi_values)) or "none yet"
    return PROMPT_TEMPLATE.replace("{already_tested}", already_tested)

def record_result(rsi_value: str, sharpe: float, trades: int):
    tested_rsi_values.add(rsi_value)
    result_key = (round(sharpe, 4), trades)
    if result_key in duplicate_result_cache:
        log(f"[duplicate] RSI={rsi_value} produced duplicate result {result_key} — skipping")
    duplicate_result_cache.add(result_key)

# When all 6 RSI values are tested, pivot to next parameter (see NEXT PHASE below).
def rsi_search_exhausted() -> bool:
    candidates = {"33.00", "33.50", "34.50", "35.00", "35.50", "36.00"}
    return candidates.issubset(tested_rsi_values)
```

---

### [ARCHITECTURE] Why Regime A is correct and Regime B is corrupt

| Metric | Regime A (Gen 303–2126) | Regime B (Gen 2149–9200) |
|--------|------------------------|--------------------------|
| RSI long threshold | 33–35 range | 36.68 (hallucinated) |
| Trade count | 21–30 | 345–530 |
| Win rate | 66–90% | 50–53% |
| Best Sharpe | **2.9232** | 2.5324 |
| Nature | Rare, high-confidence entries | Noise-trading at scale |
| Status | **TRUE BEST** | **DISCARD ALL** |

Regime