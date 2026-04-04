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

If ALL six values appear in DO NOT USE above, output the FALLBACK YAML exactly.
If unsure which to pick, output the FALLBACK YAML exactly.

PERMANENTLY FORBIDDEN VALUES — these will be rejected, discarded without backtesting, and will NOT count as a generation:
- `36.68` — hallucinated at Gen 2149, destroyed 7000+ generations of work, not on whitelist
- `36.56` — Regime B artifact, not on whitelist
- `34.0` — must be written as `34.00`; also this is the current value, do not keep it unchanged
- Any value with more or fewer decimal places than shown (e.g. `33.5` not allowed — must be `33.50`)
- Any value not exactly matching one of the six listed above

---

## SELF-CHECK — COMPLETE THIS BEFORE OUTPUTTING

Read each question carefully against the YAML you are about to output. If ANY answer is NO, output the FALLBACK YAML instead — do not output your modified version.

1. Did I change ONLY `entry.long.conditions[0].value`? YES/NO
2. Is the new value EXACTLY one of: `33.00`, `33.50`, `34.50`, `35.00`, `35.50`, `36.00`? YES/NO
3. Is the new value DIFFERENT from `34.00` (the current value)? YES/NO
4. Is `entry.short.conditions[0].value` still exactly `60.64`? YES/NO
5. Is `exit.take_profit_pct` still exactly `3.55`? YES/NO
6. Is `exit.stop_loss_pct` still exactly `2.41`? YES/NO
7. Is `exit.timeout_hours` still exactly `200`? YES/NO
8. Is `position.size_pct` still exactly `30`? YES/NO
9. Are `period_hours` values still `21`, `26`, `21`, `48` in that order? YES/NO
10. Is the new value NOT in the DO NOT USE list above? YES/NO
11. Is the new value NOT `36.68` and NOT `36.56`? YES/NO

If ALL 11 answers are YES → output your modified YAML.
If ANY answer is NO → output the FALLBACK YAML exactly as written below.

---

## Current Best Strategy
## ⚠️ THIS IS THE REGIME A INCUMBENT — GEN 2126 — DO NOT MODIFY LOCKED FIELDS ⚠️

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
(Output this exactly — character for character, including all spacing — if your self-check fails for any reason)

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

## LOCKED FIELDS — DO NOT CHANGE ANY OF THESE UNDER ANY CIRCUMSTANCES

| Field | Locked value | Why locked |
|-------|-------------|------------|
| `entry.long.conditions[0].period_hours` | `21` | Gen 2126 optimal |
| `entry.long.conditions[1].period_hours` | `26` | Gen 2126 optimal |
| `entry.short.conditions[0].value` | `60.64` | Gen 2126 optimal |
| `entry.short.conditions[0].period_hours` | `21` | Gen 2126 optimal |
| `entry.short.conditions[1].period_hours` | `48` | Gen 2126 optimal |
| `exit.take_profit_pct` | `3.55` | Gen 2126 optimal |
| `exit.stop_loss_pct` | `2.41` | Gen 2126 optimal |
| `exit.timeout_hours` | `200` | Gen 2126 optimal |
| `position.size_pct` | `30` | Gen 2126 optimal — do NOT use 15 |
| `position.max_open` | `1` | Gen 2126 optimal |
| `position.fee_rate` | `0.001` | Gen 2126 optimal |

⚠️ WARNING: A previous session changed size_pct to 15, stop_loss_pct to 2.72, and timeout_hours to 196.
These are Regime B artifacts. They are WRONG. The values above are the ONLY correct values.

---

## ⚠️ FOR ODIN/MIMIR SYSTEM — NOT SHOWN TO LLM
## ⚠️ ALL ITEMS BELOW ARE MANDATORY. IMPLEMENT BEFORE GEN 9601. NO EXCEPTIONS.

---

### [CRITICAL — IMPLEMENT NOW] STEP 0: INCUMBENT RESTORE

**Execute this before any further backtesting. This is not optional.**

The current ODIN incumbent is RSI=36.56, size_pct=15, stop_loss=2.72, timeout=196.
This is a deeply corrupted Regime B artifact. It must be replaced immediately.
Do not backtest anything until this restore is complete.

The true all-time best is Gen 2126:
```
entry.long.conditions[0].value: 34.00
entry.short.conditions[0].value: 60.64
take_profit_pct: 3.55
stop_loss_pct: 2.41
timeout_hours: 200
size_pct: 30
period_hours: [21, 26, 21, 48]
Sharpe: 2.9232 | Win rate: 90.0% | Trades: 30
```

**Action required:**
1. Force-set ODIN's incumbent to the Gen 2126 config above — do not backtest it again
2. Log as `[MIMIR_RESTORE gen=2126 sharpe=2.9232]`
3. Reset `tested_rsi_values` to empty set `{}`
4. Reset `duplicate_result_cache` to empty set `{}`
5. Confirm all locked fields match the table above before resuming

**Regime B history (for the record):**
- Gen 2149: RSI=36.68 hallucinated (not on whitelist). Trade count 30→345, win rate 90%→53.6%. Sharpe collapsed from 2.92 to 0.88. This single event invalidated Gens 2149–9600.
- Gens 2149–9600: All "improvements" were Regime B optimization — tuning parameters within a broken RSI regime. All results discarded.
- Current incumbent (RSI=36.56, size_pct=15) is the end state of 7,000+ generations of corrupted optimization.

---

### [CRITICAL — IMPLEMENT NOW] STEP 1: ACCEPTANCE FILTER

Add these hard bounds. A result MUST pass ALL checks or it is rejected without updating incumbent.
Log rejected results as `[regime_b_reject trades=X sharpe=Y]`.

```python
# Regime A bounds — derived from all valid improvements (Gen 303–2126)
# Valid range: 21–30 trades, 66–90% win rate, Sharpe 1.5–3.5
# Regime B signature: >50 trades, <60% win rate — reject all

MIN_TRADES = {"day": 250, "swing": 25}
MAX_TRADES = {"day": 9999, "swing": 50}  # MAX_TRADES=50 is the critical guard that would have blocked Gen 2149