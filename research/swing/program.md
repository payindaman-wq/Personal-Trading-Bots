```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text.

---

## ⚠️ CRITICAL RULE: YOU MUST CHANGE EXACTLY ONE THING ⚠️

Compare your output to the current best. If they are identical, you have failed. Change ONE value.

---

## Current Best Strategy (COPY THIS — CHANGE ONE VALUE)

```yaml
name: crossover
style: randomly generated
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
position:
  size_pct: 15
  max_open: 1
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 36.56
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
  stop_loss_pct: 2.72
  timeout_hours: 196
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

**Current performance: Sharpe=2.5324, 523 trades, 52.0% win rate**

---

## Performance Target

Beat Sharpe=2.5324 (the backtester keeps a change only if raw Sharpe improves).

---

## CHOOSE ONE CHANGE FROM THIS LIST

Pick one option below. Do not invent new changes outside this list.

### Option A — Tighten take_profit_pct (HIGHEST PRIORITY — UNTESTED)
Change `take_profit_pct` to ONE of: `3.20` / `3.25` / `3.30` / `3.35` / `3.40` / `3.45`
Change NOTHING else.

### Option B — Tighten stop_loss_pct
Change `stop_loss_pct` to ONE of: `2.40` / `2.45` / `2.50` / `2.55` / `2.60`
Change NOTHING else.

### Option C — Reduce timeout_hours
Change `timeout_hours` to ONE of: `115` / `130` / `140` / `150` / `163` / `175`
⚠️ DO NOT use 120 (banned).
Change NOTHING else.

### Option D — Adjust long RSI entry threshold
Change the long entry `value` from `36.56` to ONE of: `35.00` / `35.50` / `36.00` / `37.00` / `37.50` / `38.00`
⚠️ DO NOT change period_hours (must stay 21). Change NOTHING else.

### Option E — Adjust short RSI entry threshold
Change the short entry `value` from `60.64` to ONE of: `59.00` / `59.50` / `60.00` / `61.00` / `61.50` / `62.00`
⚠️ DO NOT change period_hours (must stay 21). Change NOTHING else.

### Option F — Add a 5th pair
Add ONE pair to the pairs list: `AVAX/USD` OR `ATOM/USD` OR `MATIC/USD`
⚠️ Do NOT add DOT/USD, ETH/USD, or SOL/USD. Change NOTHING else.

### Option G — Adjust MACD short-side period
Change the short entry `macd_signal period_hours` from `48` to ONE of: `44` / `46` / `50` / `52` / `54` / `56`
⚠️ Do NOT touch the long entry macd_signal (period_hours: 26). Change NOTHING else.

### Option H — Adjust pause risk parameters
Change `pause_if_down_pct` from `8` to ONE of: `6` / `7` / `9` / `10`
OR change `pause_hours` from `48` to ONE of: `24` / `36` / `60` / `72`
Change ONLY ONE of these. Change NOTHING else.

---

## ❌ ABSOLUTE BANS — IF YOUR OUTPUT MATCHES ANY OF THESE, DELETE IT AND START OVER ❌

| What | Why |
|------|-----|
| ETH/USD or SOL/USD in pairs | Sharpe ≈ -1.86, confirmed 20+ times |
| period_hours: anything other than 21 for RSI | Sharpe ≈ -0.13, confirmed 8+ times |
| macd_signal period_hours: 45–51 for long entry | Only 45–51 is allowed for long MACD (currently 26 — do not change long MACD period) |
| macd_signal period_hours ≤ 44 or ≥ 57 for short entry | Confirmed bad |
| max_open: 2 (without other changes) | Sharpe ≈ 0.93, confirmed 10+ times |
| timeout_hours: 120 | Confirmed 2.2133 attractor |
| short RSI value: 57.50 | Confirmed 2.2133 attractor |
| Identical to current best | Rejected by backtester |
| RSI value change > ±2.5 from current values | Confirmed catastrophic |
| DOT/USD added as 5th pair | Previously dropped, hurt Sharpe |

---

## KNOWN RESULT SIGNATURES — IF YOUR CONFIG WOULD PRODUCE THESE, START OVER

- Sharpe ≈ 2.5324, trades ≈ 523 → You reproduced the current best. Change something.
- Sharpe ≈ 2.2133, trades ≈ 519 → Known attractor. Avoid timeout=120 and short RSI=57.50.
- Sharpe ≈ 0.6173, trades ≈ 480 → Known bad attractor. Check your pairs list.
- Sharpe ≈ -1.86 → ETH or SOL is in your pairs. Remove them.

---

## INSTRUCTIONS SUMMARY

1. Copy the current best YAML exactly.
2. Pick ONE option (A through H) from the list above.
3. Make exactly that one change.
4. Verify your output differs from the current best in exactly one place.
5. Output ONLY the YAML block. Nothing else.

---

## Current Best Strategy (repeated for reference)

```yaml
name: crossover
style: randomly generated
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
position:
  size_pct: 15
  max_open: 1
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 36.56
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
  stop_loss_pct: 2.72
  timeout_hours: 196
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```
```