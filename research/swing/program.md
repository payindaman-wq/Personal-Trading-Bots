```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation. No comments. No other text.

---

## YOUR ONLY TASK

Change the long entry RSI `value` field (the one under `entry.long.conditions[0]`).

The current value is `34.00`. You must change it to a DIFFERENT value.

You MUST pick EXACTLY one value from this list. Copy it character for character:

```
33.00
33.50
34.50
35.00
35.50
36.00
```

**DO NOT USE these values — already tested this session:**
{already_tested}

**Pick the LOWEST-NUMBERED untested value from this priority order:**
1. `33.00`
2. `33.50`
3. `34.50`
4. `35.00`
5. `35.50`
6. `36.00`

If ALL six values are in the DO NOT USE list above → output the FALLBACK YAML exactly.
If you are unsure what to pick → output the FALLBACK YAML exactly.
If the value you would pick does not appear CHARACTER FOR CHARACTER in the whitelist above → output the FALLBACK YAML exactly.

---

## FORBIDDEN VALUES — output FALLBACK if you would use any of these

- `36.68` — hallucinated, permanently banned
- `36.56` — Regime B artifact, permanently banned
- `36.7` — Regime B artifact, permanently banned
- `36.70` — Regime B artifact, permanently banned
- `34.00` — this is the current value, do not keep it unchanged
- `34.0` — wrong decimal format
- `33.5` — wrong decimal format (must be `33.50`)
- `35.5` — wrong decimal format (must be `35.50`)
- Any value with only one decimal place
- Any value not exactly matching one of the six listed above
- Any value that contains letters or special characters

---

## MANDATORY SELF-CHECK

Before outputting, answer YES or NO to each question.
If you cannot answer YES to ALL 10 → output FALLBACK YAML.

1. Is `entry.long.conditions[0].value` set to a value that appears EXACTLY in the whitelist above? YES/NO
2. Is the new value DIFFERENT from `34.00`? YES/NO
3. Is the new value NOT in the DO NOT USE list? YES/NO
4. Is `entry.short.conditions[0].value` still `60.64`? YES/NO
5. Is `exit.take_profit_pct` still `3.55`? YES/NO
6. Is `exit.stop_loss_pct` still `2.41`? YES/NO
7. Is `exit.timeout_hours` still `200`? YES/NO
8. Is `position.size_pct` still `30`? YES/NO
9. Are period_hours still `21`, `26`, `21`, `48` in that order? YES/NO
10. Does the new value have EXACTLY two decimal places (e.g. `33.00` not `33` or `33.0`)? YES/NO

If ALL 10 answers are YES → output your modified YAML.
If ANY answer is NO → output the FALLBACK YAML.

---

## Current Best Strategy
## ⚠️ GEN 2126 INCUMBENT — DO NOT MODIFY ANY FIELD EXCEPT THE ONE MARKED BELOW ⚠️
## ⚠️ ALL OTHER FIELDS ARE LOCKED. CHANGING ANY OTHER FIELD WILL CAUSE FALLBACK. ⚠️

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
(Output this exactly — character for character — if your self-check fails for ANY reason)

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
      value: 33.00
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

## LOCKED FIELDS — DO NOT CHANGE THESE UNDER ANY CIRCUMSTANCES

| Field | Locked value |
|-------|-------------|
| `entry.long.conditions[0].period_hours` | `21` |
| `entry.long.conditions[1].period_hours` | `26` |
| `entry.short.conditions[0].value` | `60.64` |
| `entry.short.conditions[0].period_hours` | `21` |
| `entry.short.conditions[1].period_hours` | `48` |
| `exit.take_profit_pct` | `3.55` |
| `exit.stop_loss_pct` | `2.41` |
| `exit.timeout_hours` | `200` |
| `position.size_pct` | `30` |
| `position.max_open` | `1` |
| `position.fee_rate` | `0.001` |
| `pairs` | `[LINK/USD, ADA/USD, BTC/USD, OP/USD]` |
| `risk.pause_if_down_pct` | `8` |
| `risk.stop_if_down_pct` | `18` |
| `risk.pause_hours` | `48` |

---

## ⚠️ FOR ODIN/MIMIR SYSTEM ONLY — NOT SHOWN TO LLM

### [CRITICAL — EXECUTE BEFORE ANY OTHER ACTION] STEP 0: INCUMBENT RESTORE

The current ODIN internal incumbent is a Regime B artifact (RSI=36.56 or RSI=36.7, stop_loss≠2.41, size_pct=15).
This MUST be overwritten NOW before any backtesting resumes.

**Execute in this exact order — do not skip any step:**

1. Force-set ODIN incumbent to Gen 2126 config:
   - `entry.long.conditions[0].value: 34.00`
   - `entry.short.conditions[0].value: 60.64`
   - `take_profit_pct: 3.55`
   - `stop_loss_pct: 2.41`
   - `timeout_hours: 200`
   - `size_pct: 30`
   - `max_open: 1`
   - `fee_rate: 0.001`
   - `period_hours: [21, 26, 21, 48]`
   - `pairs: [LINK/USD, ADA/USD, BTC/USD, OP/USD]`
   - `Sharpe: 2.9232 | Win rate: 90.0% | Trades: 30`
2. Log: `[MIMIR_RESTORE gen=2126 sharpe=2.9232 win_rate=0.90 trades=30]`
3. Verify restore by reading back all fields above — abort and alert if any mismatch
4. Reset `tested_rsi_values` to `{}`
5. Reset `duplicate_result_cache` to `{}` then immediately add the hash of RSI=33.50 config (fallback from previous session)
6. Confirm all locked fields match the table above
7. Log: `[STEP0_COMPLETE — resuming from gen=2126 incumbent]`

**If STEP 0 cannot be completed, halt ODIN and escalate to human operator. Do not run generation 10401 until STEP 0 is confirmed complete.**

### [CRITICAL] STEP 1: SYSTEM CONSTANTS — VERIFY AND LOCK

```
MIN_TRADES[swing] = 30       ← LOCKED. Do not change. Ever.
MAX_TRADES[swing] = 60       ← LOCKED. Hard-reject results above this threshold.
DEDUPLICATION_CACHE = active ← Must block identical configs BEFORE backtesting
STALL_ALERT_GENS = 200       ← Alert if no improvement in 200 generations
```

**Why MIN_TRADES[swing] = 30 is permanently locked:**
- Gen 2126: 30 trades, 90% win rate, Sharpe=2.9232 — the true peak
- Every MIN_TRADES reduction below 30 allowed Regime