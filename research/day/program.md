```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 5400-CLEAN

---

## ⚠️ READ THIS ENTIRE DOCUMENT BEFORE WRITING ANY OUTPUT ⚠️

---

## 🚨 CRITICAL: FORBIDDEN STRINGS — INSTANT CATASTROPHIC FAILURE 🚨

If your output contains ANY of these strings, the backtest produces Sharpe ≈ -8.86
and the generation is wasted. These strings are FORBIDDEN everywhere in your output:

  ❌  momentum_accelerating
  ❌  price_vs_ema
  ❌  trend
  ❌  stop_loss_pct: 0.4
  ❌  timeout_minutes: 706
  ❌  take_profit_pct: 3.51
  ❌  max_open: 3
  ❌  style: momentum_price_change_macd_ema_trend_filter

If you are about to write any of these, STOP. Delete everything and restart from
the template below.

---

## THE ONE AND ONLY VALID OUTPUT FORMAT

You must output EXACTLY this YAML. The ONLY values you may change are the
`price_change_pct` threshold values (marked with ← CHANGE THIS).
Every other field must be copied character-for-character.

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
      value: -0.43        ← CHANGE THIS (must be between -0.50 and -0.30, negative)
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

**Rules for the threshold values:**
- Long value: must be between -0.50 and -0.30 (e.g., -0.43)
- Short value: must equal the long value with the sign flipped (e.g., +0.43)
- They must always be the same magnitude
- Use exactly 2 decimal places

---

## YOUR ROLE — SINGLE-PARAMETER TUNER

Each generation you output ONE YAML block. The only thing you change is the
`price_change_pct` threshold. That is your only degree of freedom.

---

## CURRENT STATE

### Current actual best (gen 4687)

| Parameter | Value |
|-----------|-------|
| `price_change_pct` long | -0.50 |
| `price_change_pct` short | +0.50 |
| Sharpe | 1.0460 |
| Trades | 292 |
| Adjusted score | 1.0460 × sqrt(292/50) = **2.528** |
| Status | ACTIVE BEST — searching for improvement |

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
| Status | NOT REPRODUCED in gens 5234–5400 — treat as unconfirmed hypothesis |

**The ±0.43 result has not been reproduced in 167 recent generations.**
**Do not assume it is guaranteed — it must be re-confirmed by the backtest.**
**If ±0.43 does not reproduce Sharpe ≥ 1.17 when you propose it, try nearby values.**

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
| **-0.43** | **+0.43** | **~323** | **≈ 1.17** | **≈ 2.97** | **🎯 Unconfirmed historical best** |
| -0.44 | +0.44 | ~318 | ≈ 1.10 | ≈ 2.77 | 🔶 Below target |
| -0.45 | +0.45 | ~316 | ≈ 1.03 | ≈ 2.59 | ❌ Below target |
| -0.50 | +0.50 | ~292 | ≈ 1.05 | ≈ 2.53 | ❌ Current best, below target |
| -0.55 | +0.55 | <250 | — | REJECTED | ❌ Too few trades |

---

## RECOMMENDED SEARCH SEQUENCE FOR NEXT 100 GENERATIONS

The search should focus tightly on the region most likely to reproduce or surpass
the historical high-water mark of ±0.43. Work inward from the current best.

**Priority order for next 100 generations:**
1. ±0.43 — attempt to re-confirm historical best (try at least 20 times)
2. ±0.42 — second priority (try at least 15 times)
3. ±0.44 — third priority (try at least 10 times)
4. ±0.41 — fourth priority (try at least 10 times)
5. ±0.40 — fifth priority (try at least 10 times)

**Do NOT propose values outside the range [-0.50, -0.30].**
**Do NOT propose values below -0.50 — they produce fewer than 250 trades and are auto-rejected.**
**Do NOT propose values above -0.30 — they produce ~690 trades with catastrophic negative Sharpe.**

---

## KNOWN BAD PARAMETERS — DO NOT USE UNDER ANY CIRCUMSTANCES

| What | Bad value | What happens |
|------|-----------|--------------|
| Any indicator name | `momentum_accelerating` | Sharpe ≈ -8.86, catastrophic |
| Any indicator name | `price_vs_ema` | Sharpe ≈ -8.86, catastrophic |
| Any indicator name | `trend` | Sharpe ≈ -7 to -9, catastrophic |
| `style` | anything except `momentum_optimized` | Template corruption |
| `max_open` | anything except 4 | Suboptimal / false optimum |
| `stop_loss_pct` | 0.4 | Catastrophic loss profile |
| `take_profit_pct` | 3.51 | Corrupted template value |
| `timeout_minutes` | 706 | Corrupted template value |
| `period_minutes` on `price_change_pct` | 5 | 148-trade attractor, too few trades |
| `period_minutes` on `price_change_pct` | 60 | 490-trade attractor, false optimum |
| `price_change_pct` long | above -0.30 | ~690 trades, negative Sharpe |
| `price_change_pct` long | below -0.50 | <250 trades, auto-rejected |
| Number of pairs | anything except 16 | Template corruption |
| Conditions per side | anything except 2 | Template corruption |

---

## FAILURE PATTERN ALERT — CORRUPTED TEMPLATE SIGNATURES

If a generation produces ANY of these results, the LLM used a corrupted template:

| Signature | Cause | How to avoid |
|-----------|-------|--------------|
| Sharpe ≈ -8.86, trades ≈ 514 | Used forbidden indicators from old strategy | Use ONLY `price_change_pct` and `macd_signal` |
| Sharpe ≈ -7.39, trades ≈ 509 | Partial corruption — some forbidden indicators | Same — check all indicator names |
| trades = 0 | YAML parse error | Check YAML syntax carefully |
| trades ≈ 148 | Used `period_minutes: 5` on price_change_pct | Use `period_minutes: 30` only |
| trades ≈ 490 | Used `period_minutes: 60` on price_change_pct | Use `period_minutes: 30` only |

**The -8.86 / 514-trade result has appeared 7 times in the last 20 generations.**
**This means the LLM is copying from a corrupted source