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

**Pick the first untested value from this priority order:**
1. `33.50`
2. `33.00`
3. `34.50`
4. `35.00`
5. `35.50`
6. `36.00`

If ALL six values are in the DO NOT USE list above → output the FALLBACK YAML exactly.
If you are unsure what to pick → output the FALLBACK YAML exactly.

---

## FORBIDDEN VALUES — output FALLBACK if you would use any of these

- `36.68` — hallucinated, permanently banned
- `36.56` — Regime B artifact, permanently banned
- `36.7` — Regime B artifact, permanently banned
- `34.00` — this is the current value, do not keep it unchanged
- `34.0` — wrong decimal format
- `33.5` — wrong decimal format (must be `33.50`)
- `35.5` — wrong decimal format (must be `35.50`)
- Any value not exactly matching one of the six listed above

---

## SELF-CHECK

Before outputting, answer YES or NO to each question:

1. Is `entry.long.conditions[0].value` set to a value from the whitelist above? YES/NO
2. Is the new value DIFFERENT from `34.00`? YES/NO
3. Is the new value NOT in the DO NOT USE list? YES/NO
4. Is `entry.short.conditions[0].value` still `60.64`? YES/NO
5. Is `exit.take_profit_pct` still `3.55`? YES/NO
6. Is `exit.stop_loss_pct` still `2.41`? YES/NO
7. Is `exit.timeout_hours` still `200`? YES/NO
8. Is `position.size_pct` still `30`? YES/NO
9. Are period_hours still `21`, `26`, `21`, `48` in that order? YES/NO
10. Does the new value have EXACTLY two decimal places? YES/NO

If ALL 10 answers are YES → output your modified YAML.
If ANY answer is NO → output the FALLBACK YAML.

---

## Current Best Strategy
## ⚠️ GEN 2126 INCUMBENT — DO NOT MODIFY ANY FIELD EXCEPT THE ONE MARKED BELOW ⚠️

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
(Output this exactly if your self-check fails for any reason)

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

---

## ⚠️ FOR ODIN/MIMIR SYSTEM ONLY — NOT SHOWN TO LLM

### [CRITICAL — MANDATORY BEFORE RESUMING] STEP 0: INCUMBENT RESTORE

The current ODIN incumbent is RSI=36.7, stop_loss=2.43. This is a Regime B artifact.
The "Current Best Strategy" block shown to the LLM has been corrected above to Gen 2126.
ODIN's internal incumbent must also be corrected NOW.

**Execute in order:**
1. Force-set ODIN incumbent to Gen 2126 config:
   - `entry.long.conditions[0].value: 34.00`
   - `entry.short.conditions[0].value: 60.64`
   - `take_profit_pct: 3.55`
   - `stop_loss_pct: 2.41`
   - `timeout_hours: 200`
   - `size_pct: 30`
   - `period_hours: [21, 26, 21, 48]`
   - `Sharpe: 2.9232 | Win rate: 90.0% | Trades: 30`
2. Log: `[MIMIR_RESTORE gen=2126 sharpe=2.9232]`
3. Reset `tested_rsi_values` to `{}`
4. Reset `duplicate_result_cache` to `{}`
5. Add fallback value `33.50` to `duplicate_result_cache` if it has been submitted this session
6. Confirm all locked fields match the table above before resuming

### [CRITICAL] STEP 1: SYSTEM CONSTANTS — SET THESE NOW

```
MIN_TRADES[swing] = 30       ← DO NOT LOWER THIS. Lowering enabled Regime B.
MAX_TRADES[swing] = 60       ← Hard reject anything above this. 300-500 trade results are noise.
DEDUPLICATION_CACHE = active ← Must block identical configs including repeated fallback
STALL_ALERT_GENS = 200       ← Alert if no improvement in 200 generations
```

**Why MIN_TRADES must stay at 30:**
Gen 2126 has 30 trades and Sharpe 2.9232 at 90% win rate.
Every time MIN_TRADES was lowered below 30, Regime B results (300-500 trades, 50-53% win rate)
were allowed to pass and eventually displaced the true incumbent.
Do NOT lower MIN_TRADES again under any circumstances.

**Why MAX_TRADES must be enforced:**
Any result with trades > 60 is a Regime B signal.
Gen 2149 (RSI=36.68 hallucination) had 345 trades. It should have been rejected.
A MAX_TRADES hard cap of 60 would have prevented the entire Regime B collapse.

### [CRITICAL] STEP 2: DEDUPLICATION FIX

The last 20 generations show sharpe=-1.3913 repeating 13 times.
This is the same config being submitted and evaluated repeatedly.
The deduplication cache is not functioning.

**Fix required:**
- Cache must store the full config hash, not just the RSI value
- The fallback config (RSI=33.50) must also be cached after first submission
- Any config already in cache must be REJECTED before backtesting, not after
- Log rejected duplicates as `[DEDUP_REJECTED]` to track frequency

### [CONTEXT] Why Regime B Was Catastrophic

Timeline:
- Gen 2126: True peak. RSI=34.00, 30 trades, 90% win rate, Sharpe=2.9232
- Gen 2149: LLM hallucinated RSI=36.68 (not on whitelist). MIN_TRADES had been lowered to ~20.
  This produced 345 trades / 53.6% win rate / Sharpe=0.8798.
  ODIN accepted it because Sharpe > incumbent? No — this means the incumbent was already corrupted
  before Gen 2149, OR the backtest comparison logic failed.
- Gen 2149–5316: ~3,000 generations spent optimizing a broken strategy.
  Peak Regime B Sharpe was 2.5324 (Gen 5316) — never matched Gen 2126's 2.9232.
- Gen 5316–10200: ODIN appears to be running a different (also corrupted) incumbent.
  The current "best" shown is RSI=36.7/stop_loss=2.43.

**Root cause:** The whitelist enforcement failed at Gen 2149. The fix (explicit whitelist with
self-check) was added after the damage was done. Ensure whitelist enforcement is also
implemented in ODIN's acceptance logic, not just in the LLM prompt.

### [CONTEXT] Six-Value RSI Search — What We Know

The goal of the current research phase is to find whether RSI=34.00 is truly optimal
among {33.00, 33.50, 34.00, 34.50, 35.00, 35.50, 36.00} for the Gen 2126 config.

Due to Regime B contamination, none of the six values have been cleanly tested
against the true Gen 2126 incumbent. After the STEP 0 restore, all six are candidates.

Expected behavior: results should show 20-40 trades, 80-95% win rate, Sharpe 2.5-3.2.
If a result shows >60 trades: reject immediately (Regime B).
If a result shows <15 trades: reject (insufficient sample, MIN_TRADES=30 should catch this).

### [CONTEXT] Live Performance Note

Current live sprint (RSI=36.7 incumbent): rank 3/10, +3.21%, 3 trades, 50