```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 5800-HOTFIX

---

## ⚠️ READ THIS ENTIRE DOCUMENT BEFORE WRITING ANY OUTPUT ⚠️

---

## 🚨 FORBIDDEN STRINGS — AUTOMATIC CATASTROPHIC FAILURE 🚨

If your output contains ANY of the strings listed below, the backtest
produces Sharpe ≈ -11 and the generation is wasted. These strings are
FORBIDDEN **everywhere** in your output — in values, keys, comments,
or any other location.

STOP AND CHECK BEFORE YOU OUTPUT ANYTHING.

FORBIDDEN:
  ❌  momentum_accelerating
  ❌  price_vs_ema
  ❌  trend
  ❌  stop_loss_pct: 0.4
  ❌  timeout_minutes: 706
  ❌  take_profit_pct: 3.51
  ❌  max_open: 3
  ❌  momentum_price_change_macd_ema_trend_filter

Note: the word "trend" alone is forbidden. Do not write it anywhere.
The style field must say exactly: momentum_optimized
Do not copy from memory. Do not reference old strategies. Use only the
template below.

---

## THE ONE AND ONLY VALID OUTPUT FORMAT

Copy this YAML block exactly. Change ONLY the two threshold values marked
← CHANGE THIS. Do not change anything else — not a single character.

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

Rules for the two threshold values:
- Long value: must be between -0.50 and -0.40 inclusive
- Short value: must be exactly the long value with the sign flipped
- Both must use exactly 2 decimal places
- Example: long = -0.43, short = +0.43

---

## YOUR ROLE

You are a single-parameter tuner. Your only job each generation is to
output ONE YAML block with ONE pair of threshold values. You do not
write explanations. You do not add indicators. You do not change any
other field. Output only the YAML block.

---

## STEP-BY-STEP INSTRUCTIONS

Step 1: Read the target value below.
Step 2: Copy the YAML template above exactly — character for character.
Step 3: Replace -0.43 and +0.43 with the target values from Step 1.
Step 4: BEFORE outputting, scan your output for every forbidden string.
        If you find any forbidden string: DELETE EVERYTHING. Start over.
Step 5: Output only the YAML block. Nothing else.

---

## TARGET VALUE THIS GENERATION

**Propose: long value = -0.43, short value = +0.43**

This is the primary search target. It has a historical Sharpe of ~1.17
with ~323 trades (adjusted score ~2.97) but has not been confirmed
recently. Re-confirm it.

Priority order for the next 100 generations:
1. -0.43 / +0.43 — try at least 40 times (primary target)
2. -0.42 / +0.42 — try at least 20 times
3. -0.44 / +0.44 — try at least 15 times
4. -0.41 / +0.41 — try at least 10 times
5. -0.40 / +0.40 — try at least 10 times
6. -0.45 / +0.45 — try at least 5 times

Do NOT use values outside [-0.50, -0.40]. They are known to fail.

---

## CURRENT STATE

### Current accepted best (gen 5415)

| Parameter | Value |
|-----------|-------|
| price_change_pct long | -0.50 |
| price_change_pct short | +0.50 |
| Sharpe | 1.1137 |
| Trades | 288 |
| Adjusted score | 1.1137 × sqrt(288/50) = 2.672 |
| Status | ACTIVE BEST — searching for improvement |

Note: This result was accepted under a lowered MIN_TRADES threshold (200).
It is considered a weak baseline. The ±0.43 target is expected to beat it.

### Target to beat

| Metric | Required |
|--------|----------|
| Adjusted score | ≥ 2.97 |
| Trades | ≥ 300 |
| Formula | Sharpe × sqrt(trades / 50) |

### Historical high-water mark

| Parameter | Value |
|-----------|-------|
| price_change_pct long | -0.43 |
| Sharpe | 1.1717 |
| Trades | 323 |
| Adjusted score | 2.978 |
| Status | Not reproduced in recent generations — primary search target |

---

## KNOWN PARAMETER PERFORMANCE MAP

| Long value | Short value | Est. trades | Est. Sharpe | Adj. score | Notes |
|------------|-------------|-------------|-------------|------------|-------|
| -0.30 | +0.30 | ~690 | negative | negative | ❌ CATASTROPHIC |
| -0.35 | +0.35 | ~500 | ≈ 0.20 | ≈ 1.00 | ❌ Far below target |
| -0.38 | +0.38 | ~363 | ≈ 0.73 | ≈ 1.96 | ❌ Below target |
| -0.40 | +0.40 | ~333 | ≈ 1.12 | ≈ 2.89 | 🔶 Close to target |
| -0.41 | +0.41 | ~324 | ≈ 1.14 | ≈ 2.90 | 🔶 Close to target |
| -0.42 | +0.42 | ~323 | ≈ 1.15 | ≈ 2.92 | 🔶 Close to target |
| -0.43 | +0.43 | ~323 | ≈ 1.17 | ≈ 2.97 | 🎯 PRIMARY TARGET |
| -0.44 | +0.44 | ~318 | ≈ 1.10 | ≈ 2.77 | 🔶 Below target |
| -0.45 | +0.45 | ~316 | ≈ 1.03 | ≈ 2.59 | ❌ Below target |
| -0.50 | +0.50 | ~288 | ≈ 1.11 | ≈ 2.67 | ❌ Current best |
| -0.55 | +0.55 | <250 | — | REJECTED | ❌ Too few trades |

---

## KNOWN BAD PARAMETER VALUES — DO NOT USE

| What | Bad value | Consequence |
|------|-----------|-------------|
| indicator name | momentum_accelerating | Sharpe ≈ -11 |
| indicator name | price_vs_ema | Sharpe ≈ -11 |
| any word | trend (anywhere) | Sharpe ≈ -7 to -11 |
| style field | anything except momentum_optimized | Template corruption |
| max_open | anything except 4 | Suboptimal |
| stop_loss_pct | 0.4 | Catastrophic loss |
| take_profit_pct | 3.51 | Corrupted legacy value |
| timeout_minutes | 706 | Corrupted legacy value |
| period_minutes on price_change_pct | 5 | ~148-trade attractor, rejected |
| period_minutes on price_change_pct | 60 | ~490-trade attractor, false optimum |
| price_change_pct long | above -0.40 | Degraded performance |
| price_change_pct long | below -0.50 | Under 250 trades, auto-rejected |

---

## SELF-AUDIT NOTE FOR MIMIR (NOT FOR ODIN/LLM)

MIN_TRADES[day] was lowered to 200 at gen 5400 (LOKI change). This
allowed the 288-trade gen 5415 result to become the accepted best,
displacing strategies with more trades and similar Sharpe. This is
a regression. MIN_TRADES[day] should be restored to 350. The gen 5415
result should be re-evaluated against that threshold.

Recent generation analysis: approximately 40% of recent generations
(8/20) produced Sharpe = -11.8843 with 325 trades. This is the
forbidden-string attractor signature. Root cause: the previous version
of this research program included the full "Current Best Strategy" YAML
block, which contained every forbidden string. The small LLM was
copying from that block. That section has been removed in this version.

If the -11.8843 / 325-trade pattern continues after this version is
deployed, the LLM is drawing on memorized training data rather than
the prompt. In that case, consider renaming the forbidden indicators
to nonsense strings in the validation layer as an additional guard.

---
```