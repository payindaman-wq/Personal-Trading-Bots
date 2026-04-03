```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text, no comments.

---

## YOUR ONLY TASK

Change the long entry RSI `value` field.

The current value is `34.00`.

You must output ONE of these six values. Copy it exactly, character for character:

```
33.00
33.50
34.50
35.00
35.50
36.00
```

Try them in this order (prefer values not recently tested):
1. `33.50`
2. `33.00`
3. `34.50`
4. `35.00`
5. `35.50`
6. `36.00`

If unsure, output `33.50`.

---

## SELF-CHECK — DO THIS BEFORE OUTPUTTING

1. Did I change ONLY `entry.long.conditions[0].value`? YES/NO
2. Is the new value exactly one of: 33.00, 33.50, 34.50, 35.00, 35.50, 36.00? YES/NO
3. Is `entry.short.conditions[0].value` still `60.64`? YES/NO
4. Is `take_profit_pct` still `3.55` and `stop_loss_pct` still `2.41`? YES/NO
5. Are all `period_hours` values still 21, 26, 21, 48 in order? YES/NO

If ANY answer is NO → output the FALLBACK YAML below, exactly as written, unchanged.

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
(Output this exactly if your self-check fails)

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

## LOCKED FIELDS — DO NOT TOUCH THESE

| Field | Must equal |
|-------|------------|
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

## OPERATOR NOTES
## ⚠️ FOR ODIN/MIMIR SYSTEM — NOT SHOWN TO LLM

### MANDATORY BEFORE GEN 9001 — EXECUTE NOW

**[RESTORE] Set incumbent to Gen 2126:**
```yaml
entry.long.conditions[0].value: 34.00
entry.short.conditions[0].value: 60.64
take_profit_pct: 3.55
stop_loss_pct: 2.41
timeout_hours: 200
period_hours: [21, 26, 21, 48]
# Sharpe: 2.9232 | Win rate: 90.0% | Trades: 30
```
Gen 2126 is the true all-time best. The current incumbent (36.68, 479 trades, Sharpe 2.50)
is a Regime B artifact from a hallucinated RSI value. All Gen 2149–9000 improvements
are improvements within a corrupt regime, not over the true best. Discard them.

**[ENFORCE] Add MAX_TRADES hard bound immediately:**
```python
MIN_TRADES = {"day": 250, "swing": 25}
MAX_TRADES = {"day": 9999, "swing": 50}

def accept_result(trades: int, style: str, sharpe: float) -> bool:
    if trades < MIN_TRADES[style]:
        return False  # too few trades
    if trades > MAX_TRADES[style]:
        return False  # regime collapse — reject hard, do not update incumbent
    return True

# This would have rejected Gen 2149 (345 trades) and all Regime B configs.
# It MUST be in place before any further backtesting.
```

**[VALIDATE] Pre-backtest RSI whitelist check:**
```python
ALLOWED_RSI_LONG = {"33.00", "33.50", "34.00", "34.50", "35.00", "35.50", "36.00"}

def validate_config(yaml_str: str) -> bool:
    value = extract_field(yaml_str, "entry.long.conditions[0].value")
    return str(round(float(value), 2)) in ALLOWED_RSI_LONG
    # If False: discard without backtesting, log as [invalid_rsi], do not count as generation
```

**[DO NOT CHANGE] MIN_TRADES[swing] must stay at 25:**
The oscillation of MIN_TRADES between 10–30 was ineffective and caused no improvement.
The real filter gap was always MAX_TRADES. Do not change MIN_TRADES again.
All Regime A incumbents (Gen 303–2126) had 21–30 trades — all pass MIN_TRADES=25.

**[NEXT PHASE — after RSI space exhausted]**
Once all six RSI values {33.00, 33.50, 34.50, 35.00, 35.50, 36.00} have been tested
against the restored Gen 2126 incumbent, pivot to exploring:
1. `take_profit_pct`: try {3.25, 3.40, 3.55, 3.70, 3.85, 4.00} — keep RSI at best found
2. `stop_loss_pct`: try {2.00, 2.20, 2.41, 2.60, 2.80} — keep others at best found
3. `timeout_hours`: try {150, 175, 200, 225, 250} — keep others at best found
4. `entry.short.conditions[0].value`: try {59.00, 59.50, 60.00, 60.64, 61.00, 61.50}
These parameters have never been systematically explored within Regime A.
They are the next highest-value optimization targets.

**[LIVE PERFORMANCE NOTE]**
Current live result (rank 3/10, +3.21%, 3 trades, 50% win rate) has too small a sample
to validate backtest Sharpe 2.92. Monitor for at least 5 more sprints before drawing
conclusions about backtest-to-live gap. The 50% live win rate vs 90% backtest win rate
is a red flag worth watching — possible overfitting to 2-year BTC/ETH/SOL regime.

**[DEDUPLICATION — fix the looping problem]**
Recent gens show identical results appearing 4+ times (sharpe=-1.3913, trades=166).
The LLM is looping on the same output. Add a result cache:
```python
tested_values = set()  # track all RSI values tested this session
def get_next_value(tested: set) -> str:
    candidates = ["33.50", "33.00", "34.50", "35.00", "35.50", "36.00"]
    for v in candidates:
        if v not in tested:
            return v
    return None  # all values tested — pivot to next parameter
```
Pass the set of already-tested values to ODIN so it can inject them into the prompt
as "DO NOT USE THESE: {already_tested}" to prevent redundant generations.
```