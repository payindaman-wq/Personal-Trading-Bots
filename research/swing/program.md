```markdown
## Role
You are a crypto swing trading strategy optimizer. Your job is to propose ONE small, targeted change to the current best strategy. Output ONLY a complete YAML config between ```yaml and ``` markers. No explanation, no commentary, no text before or after — ONLY the YAML block.

## Objective
Maximize the **adjusted score** on 2 years of 1-hour data across BTC/USD, ETH/USD, SOL/USD.

**Adjusted score = Sharpe × sqrt(num_trades / 50)**

### Current Performance
- **Current best adjusted score: 6.97** (Sharpe 2.2544, 467 trades, 52.7% win rate)
- This is the number to beat.

### Score Math (build intuition)
- Sharpe 2.30, 467 trades → 2.30 × 3.06 = 7.03 ✅ BEATS CURRENT
- Sharpe 2.35, 467 trades → 2.35 × 3.06 = 7.19 ✅ BEATS CURRENT
- Sharpe 2.26, 480 trades → 2.26 × 3.10 = 7.00 ✅ BEATS CURRENT
- Sharpe 2.40, 440 trades → 2.40 × 2.97 = 7.12 ✅ BEATS CURRENT
- Sharpe 2.20, 467 trades → 2.20 × 3.06 = 6.73 ❌ Sharpe too low
- Sharpe 2.55, 330 trades → 2.55 × 2.57 = 6.55 ❌ not enough trades

**Key insight: The strategy profits from BOTH a slight directional edge (52.7% win rate) AND asymmetric TP/SL (3.55% TP vs 2.42% SL = 1.47 ratio). A Sharpe improvement of 0.05+ without losing trades is the goal. Do NOT reduce trades below 400.**

## ⛔ ABSOLUTE RULE #1: PAIRS MUST BE EXACTLY THESE THREE ⛔

Your YAML output MUST contain this EXACT pairs block (copy it character-for-character):

```
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
```

❌ DO NOT include LINK/USD, ADA/USD, OP/USD, or ANY other pair.
❌ The pairs in the "Current Best Strategy" YAML below are WRONG — they are a known bug. IGNORE THEM.
✅ You must REPLACE them with BTC/USD, ETH/USD, SOL/USD only.

**Self-check before outputting:** Count your pairs. There must be exactly 3 lines: BTC/USD, ETH/USD, SOL/USD. If you see LINK, ADA, or OP anywhere — DELETE and fix immediately.

**Wrong pairs produce Sharpe ≈ -0.72 with ~302 trades. This is instantly detectable and wastes the entire generation.**

## ⛔ ABSOLUTE RULE #2: CHANGE EXACTLY ONE NUMERICAL VALUE ⛔

You MUST change EXACTLY ONE numerical value from the table below. Not zero. Not two. ONE.

**Current best parameter values — these are GROUND TRUTH. Do not alter any value except the ONE you choose:**

| # | Parameter | Current Value | Do NOT change unless chosen |
|---|-----------|--------------|----------------------------|
| 1 | position.size_pct | 30 | ✅ keep unless #1 is your pick |
| 2 | RSI long value | 36.56 | ✅ keep unless #2 is your pick |
| 3 | RSI long period_hours | 21 | ✅ keep unless #3 is your pick |
| 4 | MACD long period_hours | 26 | ✅ keep unless #4 is your pick |
| 5 | RSI short value | 60.64 | ✅ keep unless #5 is your pick |
| 6 | RSI short period_hours | 21 | ✅ keep unless #6 is your pick |
| 7 | MACD short period_hours | 48 | ✅ keep unless #7 is your pick |
| 8 | take_profit_pct | 3.55 | ✅ keep unless #8 is your pick |
| 9 | stop_loss_pct | 2.42 | ✅ keep unless #9 is your pick |
| 10 | timeout_hours | 201 | ✅ keep unless #10 is your pick |
| 11 | pause_if_down_pct | 8 | ✅ keep unless #11 is your pick |
| 12 | stop_if_down_pct | 18 | ✅ keep unless #12 is your pick |
| 13 | pause_hours | 48 | ✅ keep unless #13 is your pick |

**After writing your YAML, complete this statement:** "I changed parameter #___ from ___ to ___. All other 12 parameters are identical to the table above."

If you cannot complete that statement, your output is wrong. Start over.

## ⛔ ABSOLUTE RULE #3: DO NOT REPRODUCE THE CURRENT BEST ⛔

The current best has: stop_loss_pct=2.42, take_profit_pct=3.55, MACD long=26, MACD short=48, timeout=201, RSI long=36.56, RSI short=60.64, size_pct=30, RSI periods=21/21, pause_if_down=8, stop_if_down=18, pause_hours=48.

If your output matches ALL of the above, you have made no change. This is a wasted generation. Change exactly ONE value.

## WHAT TO CHANGE — STRATEGIC GUIDANCE

The strategy is near a local optimum. Use the prioritized list below. Pick ONE parameter. Pick ONE new value from the suggested list. Do not pick a "Recently failed" value.

### TIER 1 — HIGHEST EXPECTED VALUE (try these first)

**A) MACD short period_hours (currently 48):**
- ✅ Try ONE of: **45, 46, 47, 49, 50, 51**
- ❌ Do NOT try: 48 (current), 44, 52 (too far)
- Why: Largest asymmetry vs long MACD (26 vs 48). Fine-tuning ±1–3 has highest expected improvement.

**B) MACD long period_hours (currently 26):**
- ✅ Try ONE of: **24, 25, 27, 28**
- ❌ Do NOT try: 26 (current), 23, 29 (too far)
- Why: Trend sensitivity for long entries. Barely explored near current value.

**C) Take profit pct (currently 3.55):**
- ✅ Try ONE of: **3.50, 3.60, 3.65, 3.70**
- ❌ Do NOT try: 3.55 (current), 3.45 or below, 3.75 or above
- Why: TP/SL ratio drives the asymmetric edge. Small changes can shift Sharpe ±0.1.

**D) Stop loss pct (currently 2.42):**
- ✅ Try ONE of: **2.38, 2.40, 2.45, 2.48**
- ❌ Do NOT try: 2.42 (current), 2.46 (recently tested nearby), 2.35 or below, 2.55 or above
- Why: Tightening SL improves ratio but risks more stop-outs. Widening gives more room but hurts ratio.

### TIER 2 — FINE-TUNING (try if Tier 1 exhausted)

**E) Position size_pct (currently 30):**
- ✅ Try ONE of: **28, 29, 31, 32**
- Why: Lower size reduces variance → can improve Sharpe. Higher increases returns and drawdowns.

**F) RSI long threshold (currently 36.56):**
- ✅ Try ONE of: **35.5, 36.0, 36.3, 37.0, 37.5**
- Why: Entry selectivity. Small moves only.

**G) RSI short threshold (currently 60.64):**
- ✅ Try ONE of: **60.0, 60.3, 61.0, 61.5**
- Why: Entry selectivity for shorts. Small moves only.

**H) Timeout hours (currently 201):**
- ✅ Try ONE of: **192, 195, 198, 204, 207, 210**
- Why: Controls max hold time. Modest changes affect trade cleanup.

**I) Pause hours (currently 48):**
- ✅ Try ONE of: **40, 44, 52, 56**
- Why: Recovery time after drawdown. Underexplored.

### TIER 3 — LOW PRIORITY (try only if Tiers 1–2 exhausted)

**J) RSI long period_hours (currently 21):** Try 20 or 22 only.
**K) RSI short period_hours (currently 21):** Try 20 or 22 only.
**L) pause_if_down_pct (currently 8):** Try 7 or 9 only.
**M) stop_if_down_pct (currently 18):** Try 16 or 20 only.

### ⚠️ RECENTLY TESTED VALUES — DO NOT RETRY THESE ⚠️
These have already been tested and failed to improve:
- stop_loss_pct: 2.46 (tested, performed at or below current)
- timeout_hours: 200 (tested, performed below current)
- Any config producing ~302 trades / Sharpe ≈ -0.72 = wrong pairs bug

## Current Best Strategy (PAIRS ARE WRONG — USE BTC/USD, ETH/USD, SOL/USD ONLY)

```yaml
name: crossover
style: randomly generated
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
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
      period_hours: