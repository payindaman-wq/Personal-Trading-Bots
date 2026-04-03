```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text, no comments.

---

## YOUR ONLY TASK

Change the long entry RSI `value` field.

The current value is `34.00`.

**ALLOWED VALUES — copy one exactly:**
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

---

## SELF-CHECK — 5 STEPS

Before outputting, verify:

1. The field I changed is `entry.long.conditions[0].value` — YES/NO
2. The new value is one of: 33.00, 33.50, 34.50, 35.00, 35.50, 36.00 — YES/NO
3. `entry.short.conditions[0].value` is still `60.64` — YES/NO
4. `take_profit_pct` is still `3.55` and `stop_loss_pct` is still `2.41` — YES/NO
5. All `period_hours` values are still: 21, 26, 21, 48 (in order) — YES/NO

If any answer is NO, start over.

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

| Field | Required value | Do not change to |
|-------|----------------|-----------------|
| `entry.long.conditions[0].value` | One of: 33.00, 33.50, 34.50, 35.00, 35.50, 36.00 | 34.00 (current), or any other number |
| `entry.long.conditions[0].period_hours` | 21 | Any other number |
| `entry.long.conditions[1].period_hours` | 26 | Any other number |
| `entry.short.conditions[0].value` | 60.64 | Any other number |
| `entry.short.conditions[0].period_hours` | 21 | Any other number |
| `entry.short.conditions[1].period_hours` | 48 | Any other number |
| `take_profit_pct` | 3.55 | Any other number |
| `stop_loss_pct` | 2.41 | Any other number |
| `timeout_hours` | 200 | Any other number |
| `size_pct` | 30 | Any other number |
| `max_open` | 1 | Any other number |
| `fee_rate` | 0.001 | Any other number |
| `pairs` | LINK/USD, ADA/USD, BTC/USD, OP/USD | Any change |

---

## EXPECTED BACKTEST RESULTS

A correct output will produce:
- **20–50 trades** over 2 years
- **75–90% win rate**
- **Sharpe 2.5–3.0**

If backtesting returns 400–550 trades or 150–220 trades, the output was invalid regardless of what you intended.
The target is low trade count with high win rate. This is correct and expected.
```

---

## ODIN SYSTEM CHANGES (for MIMIR/operator action — not part of LLM prompt)

**Immediate actions required before next generation run:**

1. **RESTORE INCUMBENT**: Override the current incumbent YAML (which contains the forbidden `value: 36.68`) with the Gen 2126 config. Set `entry.long.conditions[0].value: 34.00`, all other fields as in the template above. Set incumbent Sharpe to 2.9232.

2. **ADD MAX_TRADES GUARD**: In the backtesting acceptance logic, add a hard filter: reject any result with `trades > 100`. This catches both Regime B (400–550 trades) and the Attractor (150–220 trades) without relying on the LLM to self-detect. Combined with existing `MIN_TRADES = 20`, the valid window is 20–100 trades.

3. **LOCK MIN_TRADES**: Set `MIN_TRADES[swing] = 20` and do not change it again. The Gen 2126 result had 30 trades, which clears this threshold. Do not lower it further — values below 20 allow noisy 15-trade results through.

4. **TRUNCATE THE PROMPT**: The previous prompt exceeded safe context for llama-3.1-8b-instant. The repeated mentions of forbidden values (36.68) in negative examples were causing the model to reproduce them. The updated prompt above removes all negative-example forbidden values from the text.

5. **AFTER RSI SEARCH COMPLETES**: Once all 6 RSI values have been tested under a clean Regime A incumbent, expand the search to: (a) `take_profit_pct` ± 0.25 steps from 3.55, (b) `stop_loss_pct` ± 0.10 steps from 2.41, (c) `entry.short.conditions[0].value` ± 1.0 steps from 60.64. These have not been explored in Regime A and represent the next optimization frontier.

6. **LIVE STRATEGY AUDIT**: Verify that the live AutoBotSwing deployment is running the Gen 2126 config (RSI < 34.00, Sharpe=2.9232), not the corrupted Regime B incumbent. The 50% win rate in the live sprint strongly suggests Regime B is live. Swap to Gen 2126 config immediately.