```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 5600-CLEAN

---

## ⚠️ READ THIS ENTIRE DOCUMENT BEFORE WRITING ANY OUTPUT ⚠️

---

## 🚨 CRITICAL: FORBIDDEN STRINGS — INSTANT CATASTROPHIC FAILURE 🚨

If your output contains ANY of these strings, the backtest produces Sharpe ≈ -11
and the generation is wasted. These strings are FORBIDDEN **everywhere** in your
output — including in comments, examples, or copied blocks:

  ❌  momentum_accelerating
  ❌  price_vs_ema
  ❌  trend
  ❌  stop_loss_pct: 0.4
  ❌  timeout_minutes: 706
  ❌  take_profit_pct: 3.51
  ❌  max_open: 3
  ❌  style: momentum_price_change_macd_ema_trend_filter

**If you are about to write any of these strings anywhere in your output, STOP.**
**Delete everything. Start over from the template below.**
**Do NOT copy from any strategy you have seen that contained these strings.**
**Do NOT use any strategy other than the template below as a reference.**

---

## THE ONE AND ONLY VALID OUTPUT FORMAT

You must output EXACTLY this YAML block. Copy it character-for-character.
The **ONLY** values you may change are the two `price_change_pct` threshold
values marked with ← CHANGE THIS.
Every other field must be copied exactly as shown.

```yaml
name: crossover
style: momentum_optimized
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
- XRP/USD
- DOGE/USD
- AVAX/USD
- LINK/USD
- UNI/USD
- AAVE/USD
- NEAR/USD
- APT/USD
- SUI/USD
- ARB/USD
- OP/USD
- ADA/USD
- POL/USD
position:
  size_pct: 10
  max_open: 4
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: lt
      value: -0.43        ← CHANGE THIS (must be between -0.50 and -0.40, negative)
    - indicator: macd_signal
      period_minutes: 30
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43         ← CHANGE THIS (must equal the long value with sign flipped)
    - indicator: macd_signal
      period_minutes: 30
      operator: eq
      value: bearish
exit:
  take_profit_pct: 2.5
  stop_loss_pct: 1.2
  timeout_minutes: 720
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

**Rules for the threshold values — read carefully:**
- Long value: must be between -0.50 and -0.40 inclusive (e.g., -0.43)
- Short value: must be the exact same number with the sign flipped (e.g., +0.43)
- They must always be the same magnitude
- Use exactly 2 decimal places
- Values outside [-0.50, -0.40] are known to perform worse — do not use them

---

## YOUR ROLE — SINGLE-PARAMETER TUNER

Each generation you output ONE YAML block.
The **only** thing you change is the `price_change_pct` threshold value.
That is your **only** degree of freedom.
Do not change anything else. Do not add conditions. Do not add indicators.
Do not change pairs, position sizing, exit parameters, or risk parameters.

---

## STEP-BY-STEP INSTRUCTIONS FOR THIS GENERATION

Follow these steps in order:

**Step 1:** Read the "Target value this generation" section below.
**Step 2:** Copy the YAML template above exactly.
**Step 3:** Replace -0.43 (long) and +0.43 (short) with the target values.
**Step 4:** Double-check: does your output contain any forbidden string?
  - If YES: delete everything, start over from the template.
  - If NO: output the YAML block.

That is all. Do not write explanations. Do not write analysis. Output only the YAML.

---

## TARGET VALUE THIS GENERATION

**Propose: long value = -0.43, short value = +0.43**

This is the historical high-water mark. It must be re-confirmed.
If the backtest returns Sharpe ≥ 1.17 with ~323 trades, it will set a new best.

After ±0.43 has been confirmed or rejected, try values in this priority order:
1. **-0.43 / +0.43** — primary target (try at least 20 times)
2. **-0.42 / +0.42** — second priority (try at least 15 times)
3. **-0.44 / +0.44** — third priority (try at least 10 times)
4. **-0.41 / +0.41** — fourth priority (try at least 10 times)
5. **-0.40 / +0.40** — fifth priority (try at least 10 times)
6. **-0.45 / +0.45** — sixth priority (try at least 5 times)

**Do NOT propose values outside [-0.50, -0.40].** Values above -0.40 produce
degraded performance. Values below -0.50 produce fewer than 250 trades and are
auto-rejected.

---

## CURRENT STATE

### Current actual best (gen 5415)

| Parameter | Value |
|-----------|-------|
| `price_change_pct` long | -0.50 |
| `price_change_pct` short | +0.50 |
| Sharpe | 1.1137 |
| Trades | 288 |
| Adjusted score | 1.1137 × sqrt(288/50) = **2.672** |
| Status | ACTIVE BEST — searching for improvement |

> **Note:** This replaced the prior best from gen 4687 (Sharpe=1.0460, 292 trades,
> adj score 2.528). The optimizer accepted the gen 5415 result correctly.

### Target to beat

| Metric | Required value |
|--------|---------------|
| Adjusted score | ≥ 2.97 |
| Trades | ≥ 250 |
| Formula | Sharpe × sqrt(trades / 50) |

### Historical high-water mark (gen 2163–2199, unconfirmed in recent runs)

| Parameter | Value |
|-----------|-------|
| `price_change_pct` long | -0.43 |
| Sharpe | 1.1717 |
| Trades | 323 |
| Adjusted score | **2.978** |
| Status | NOT REPRODUCED in gens 5234–5600 — treat as unconfirmed hypothesis |

**The ±0.43 result has not been reproduced in 367 recent generations.**
**It must be actively proposed and re-confirmed by the backtest.**
**Do not assume it is guaranteed — but it remains the primary search target.**

---

## KNOWN PARAMETER PERFORMANCE MAP

| Long value | Short value | Est. trades | Est. Sharpe | Adj. score | Notes |
|------------|-------------|-------------|-------------|------------|-------|
| -0.30 | +0.30 | ~690 | negative | negative | ❌ CATASTROPHIC — DO NOT USE |
| -0.35 | +0.35 | ~500 | ≈ 0.20 | ≈ 1.00 | ❌ Far below target |
| -0.38 | +0.38 | ~363 | ≈ 0.73 | ≈ 1.96 | ❌ Below target |
| -0.40 | +0.40 | ~333 | ≈ 1.12 | ≈ 2.89 | 🔶 Close, below target |
| -0.41 | +0.41 | ~324 | ≈ 1.14 | ≈ 2.90 | 🔶 Close, below target |
| -0.42 | +0.42 | ~323 | ≈ 1.15 | ≈ 2.92 | 🔶 Close, below target |
| **-0.43** | **+0.43** | **~323** | **≈ 1.17** | **≈ 2.97** | **🎯 Unconfirmed historical best — PRIMARY TARGET** |
| -0.44 | +0.44 | ~318 | ≈ 1.10 | ≈ 2.77 | 🔶 Below target |
| -0.45 | +0.45 | ~316 | ≈ 1.03 | ≈ 2.59 | ❌ Below target |
| -0.50 | +0.50 | ~288 | ≈ 1.11 | ≈ 2.67 | ❌ Current best, below target |
| -0.55 | +0.55 | <250 | — | REJECTED | ❌ Too few trades — auto-rejected |

---

## KNOWN BAD PARAMETERS — DO NOT USE UNDER ANY CIRCUMSTANCES

| What | Bad value | What happens |
|------|-----------|--------------|
| Any indicator name | `momentum_accelerating` | Sharpe ≈ -11, catastrophic |
| Any indicator name | `price_vs_ema` | Sharpe ≈ -11, catastrophic |
| Any word containing | `trend` | Sharpe ≈ -7 to -11, catastrophic |
| `style` field | anything except `momentum_optimized` | Template corruption |
| `max_open` | anything except 4 | Suboptimal / false optimum |
| `stop_loss_pct` | 0.4 | Catastrophic loss profile |
| `take_profit_pct` | 3.51 | Corrupted legacy value |
| `timeout_minutes` | 706 | Corrupted legacy value |
| `period_minutes` on `price_change_pct` | 5 | ~148-trade attractor, auto-rejected |
| `period_minutes` on `price_change_pct` | 60 | ~490-trade attractor, false optimum |
| `price_change_pct` long | above -0.40 | Degraded performance zone |
| `price_change_pct` long | above -0.30