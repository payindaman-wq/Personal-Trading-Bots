```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text.

---

## ⚠️ CRITICAL RULE: YOU MUST CHANGE EXACTLY ONE THING ⚠️

Before outputting, manually compare EVERY field in your output to the current best.
If ALL fields are identical, you have FAILED. You must change ONE value.

### Self-check before output:
- Find the line you changed.
- Confirm the new value is DIFFERENT from the current best.
- Confirm NO other line changed.
- Confirm the new value is NOT in the banned list below.
- Confirm your output would NOT produce Sharpe≈1.5861 with ~427 trades (known bad attractor — see bans).

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
**No improvement in ~1000 generations. You MUST try something genuinely different from the options below.**

---

## Performance Target

Beat Sharpe=2.5324 (the backtester keeps a change only if raw Sharpe improves).

---

## ❌ ABSOLUTE BANS — VERIFY YOUR OUTPUT AGAINST EVERY ROW ❌

| What | Why |
|------|-----|
| ETH/USD or SOL/USD in pairs | Sharpe ≈ -1.86, confirmed 20+ times |
| period_hours ≠ 21 for EITHER RSI condition | Sharpe ≈ -0.13, confirmed 8+ times |
| long entry macd_signal period_hours changed from 26 | Do NOT touch — confirmed good |
| short entry macd_signal period_hours = 45, 46, 47, 48, 49, 50, 51 | Confirmed bad range — HEAVILY tested |
| short entry macd_signal period_hours ≤ 43 or ≥ 57 | Confirmed bad extremes |
| max_open: 2 | Sharpe ≈ 0.93, confirmed 10+ times |
| timeout_hours: 120 | Confirmed 2.2133 attractor |
| timeout_hours: 196 | That is the current best — do not keep it unchanged |
| short RSI value: 57.50 | Confirmed 2.2133 attractor |
| long RSI value change > ±2.5 from 36.56 | Catastrophic drop confirmed |
| short RSI value change > ±2.5 from 60.64 | Catastrophic drop confirmed |
| DOT/USD added as 5th pair | Previously dropped Sharpe |
| Identical output to current best | Rejected — Sharpe=2.5324 |
| take_profit_pct: 3.55 | Current best — must change if using Option A |
| stop_loss_pct: 2.72 | Current best — must change if using Option B |

---

## ❌ KNOWN BAD ATTRACTORS — IF YOUR CONFIG WOULD PRODUCE THESE, START OVER ❌

| Sharpe | Trades | Cause | What to avoid |
|--------|--------|-------|---------------|
| **1.5861** | **~427** | **⚠️ CRITICAL — seen 7 times in last 20 gens** | **You are making a banned change. Most likely: short MACD period in 45–51 range, or bad pair substitution. CHECK YOUR CHANGE.** |
| 2.5324 | 523 | Reproduced current best | Change something |
| 2.5308 | 523 | Near-identical to current best | Verify change is real |
| 2.4356 | 517 | Marginal, below target | Not a trivially small adjustment |
| 2.2836 | 474 | Recent near-miss | Below target |
| 2.1261 | 443 | Recurring bad attractor | Likely bad pairs or MACD period |
| 1.0479 | 415 | Recurring bad attractor | Check pairs |
| 2.2133 | 519 | timeout=120 or short RSI=57.50 | Both banned |
| 0.6173 | 480 | Bad pairs list | Check pairs |
| -1.86  | any | ETH or SOL in pairs | Remove them |

---

## CHOOSE ONE CHANGE FROM THIS LIST

Pick ONE option (A through I). Make ONLY that one change. Do not combine options.

**⚠️ IMPORTANT: Options A, B, C, and I are the HIGHEST PRIORITY because they are the LEAST TESTED directions with genuine upside potential. Start here.**

---

### Option A — Adjust take_profit_pct ⭐ CRITICAL PRIORITY — LEAST TESTED ⭐
Change `take_profit_pct` to ONE of: `3.60` / `3.65` / `3.70` / `3.75` / `3.80` / `3.85` / `3.90` / `3.95` / `4.00`

**Known results for reference:**
- 3.55 = current best (2.5324) — DO NOT USE
- Values below 3.55: tested, below target — DO NOT USE

**Untested values (try these first):** `3.60`, `3.65`, `3.70`, `3.75`, `3.80`, `3.85`, `3.90`, `3.95`, `4.00`
⚠️ Do NOT use 3.55 (current best). Change NOTHING else.

---

### Option B — Adjust stop_loss_pct ⭐ CRITICAL PRIORITY — LEAST TESTED ⭐
Change `stop_loss_pct` to ONE of: `2.50` / `2.55` / `2.60` / `2.65` / `2.78` / `2.85` / `2.90` / `2.95` / `3.00`

**Known results for reference:**
- 2.72 = current best (2.5324) — DO NOT USE
- Values below 2.50: tested, below target — DO NOT USE

**Untested values (try these first):** `2.78`, `2.85`, `2.90`, `2.95`, `3.00`
⚠️ Do NOT use 2.72 (current best). Change NOTHING else.

---

### Option C — Adjust timeout_hours ⭐ CRITICAL PRIORITY — LONGER RANGE UNTESTED ⭐
Change `timeout_hours` to ONE of: `168` / `180` / `192` / `200` / `210` / `220` / `240` / `260` / `280`

**Known results for reference:**
- 196 = current best (2.5324) — DO NOT USE
- 120 = banned attractor (2.2133) — DO NOT USE
- 115 / 130 / 140 / 150 / 163 / 175 = tested, below target — DO NOT USE

**Untested values (try these first):** `200`, `210`, `220`, `240`, `260`, `280`
⚠️ Do NOT use 196 (current best) or 120 (banned). Change NOTHING else.

---

### Option I — Adjust position size ⭐ HIGH PRIORITY — COMPLETELY UNTESTED ⭐
Change `size_pct` from `15` to ONE of: `12` / `13` / `14` / `16` / `17` / `18` / `20`

**All values are untested.** This is a completely unexplored direction.
⚠️ Do NOT change max_open. Change NOTHING else.

---

### Option G — Adjust MACD short-side period (MEDIUM PRIORITY)
Change the short entry `macd_signal period_hours` from `48` to ONE of: `44` / `52` / `54` / `56`

⚠️ CRITICAL WARNING: The short MACD period is the most common source of the 1.5861/427-trade bad attractor.
- DO NOT use 45, 46, 47, 48, 49, 50, 51 — these are all confirmed bad or the current best.
- Only use: `44`, `52`, `54`, or `56`.
- DO NOT touch the long entry macd_signal (period_hours: 26 — leave exactly as-is).
Change NOTHING else.

---

### Option E — Adjust short RSI entry threshold (MEDIUM PRIORITY)
Change the short entry `value` from `60.64` to ONE of: `59.50` / `60.00` / `61.00` / `61.50` / `62.00` / `62.50`
⚠️ Do NOT use 57.50 (banned attractor). Do NOT change period_hours (must stay 21). Stay within ±2.5 of 60.64.
Change NOTHING else.

---

### Option H — Adjust pause/risk parameters (MEDIUM PRIORITY)
Choose EXACTLY ONE of the following sub-changes:
- Change `pause_if_down_pct` from `8` to ONE of: `6` / `7` / `9` / `10`
- Change `pause_hours` from `48` to ONE of: `24` / `36` / `60` / `72`
- Change `stop_if_down_pct` from `18` to ONE of: `14` / `15` / `16` / `20` / `22`
Make only ONE of the above sub-changes. Change NOTHING else.

---

### Option D — Adjust long RSI entry threshold (LOWER PRIORITY