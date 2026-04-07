```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 5200-POISON-PURGE

---

## ⚠️ STOP. READ THIS ENTIRE DOCUMENT BEFORE WRITING A SINGLE CHARACTER OF OUTPUT. ⚠️

---

## 🚨 CRITICAL ALERT — THE MOST COMMON MISTAKE KILLS THE RUN 🚨

In approximately 40% of recent generations, the output contained one or more of
these FORBIDDEN indicator names:

  - `momentum_accelerating`
  - `price_vs_ema`
  - `trend`

If your output contains ANY of these strings, the backtest produces Sharpe ≈ -7
to -9. That is a catastrophic failure. The run is wasted. The research stalls.

**THE ONLY INDICATORS ALLOWED ARE:**
  1. `price_change_pct`
  2. `macd_signal`

No other indicators exist. Do not invent any. Do not copy from any example that
shows other indicators. The "current best strategy" shown in some documents is
CORRUPTED — ignore it entirely. The ONLY valid template is the one in this file.

---

## THE ONE AND ONLY VALID OUTPUT FORMAT

You must output exactly this YAML block. The ONLY thing you may change is the
two `price_change_pct` numeric values (one negative, one positive, same magnitude).
Copy every other field character-for-character. Do not add fields. Do not remove
fields. Do not reorder fields.

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
      value: -0.43
    - indicator: macd_signal
      period_minutes: 30
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43
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

**The current best confirmed values are -0.43 (long) and +0.43 (short).**
**You may propose a different value, but it MUST stay within [-0.50, -0.30] (long).**
**Long and short values MUST always be the same magnitude (one negative, one positive).**
**No other parameter in this YAML may ever be changed.**

---

## YOUR ROLE — EXACTLY THIS, NOTHING MORE

You are a single-parameter tuner. Each generation you output ONE YAML.
The YAML is the template above with one possible change: the `price_change_pct`
threshold values. That is the only degree of freedom you have.

**Recommended exploration for next 100 generations:**
The optimum is confirmed at ±0.43. Focus search on the tight band ±0.41 to ±0.45.
Prioritize these values in this order:
  ±0.43 (confirmed best — try multiple times to re-confirm)
  ±0.42
  ±0.44
  ±0.41
  ±0.45

Do NOT explore outside ±0.41 to ±0.45 unless you have seen consistent improvement
trending away from ±0.43 across at least 5 consecutive generations.

---

## CURRENT STATE

### Confirmed target (established gen 2163–2199)

| Parameter | Value |
|-----------|-------|
| `price_change_pct` long | -0.43 |
| `price_change_pct` short | +0.43 |
| Sharpe | 1.1717 |
| Trades | 323 |
| Adjusted score | 1.1717 × sqrt(323/50) = 1.1717 × 2.541 = **2.978** ✅ |
| Status | TARGET — must be re-confirmed |

### Current actual best (gen 4687)

| Parameter | Value |
|-----------|-------|
| `price_change_pct` long | -0.50 (approaching -0.43) |
| Sharpe | 1.0460 |
| Trades | 292 |
| Adjusted score | 1.0460 × sqrt(292/50) = 1.0460 × 2.417 = **2.528** ❌ |
| Status | BELOW TARGET — keep searching |

**Step 1 is the ONLY active step. Do not advance until adjusted_score ≥ 2.97 AND trades ≥ 250.**

### Adjusted score formula

```
adjusted_score = Sharpe × sqrt(trades / 50)
```

Mental check before submitting — compute for your proposed values using the
known performance map below:
- If trades < 250: REJECTED regardless of Sharpe
- If adjusted_score < 2.97: below target, keep exploring
- If adjusted_score ≥ 2.97 AND trades ≥ 250: target achieved → report and hold

---

## KNOWN PARAMETER PERFORMANCE MAP

| Long value | Short value | Est. trades | Est. Sharpe | Adj. score | Notes |
|------------|-------------|-------------|-------------|------------|-------|
| -0.30 | +0.30 | ~690 | negative | negative | CATASTROPHIC — DO NOT USE |
| -0.38 | +0.38 | ~363 | ≈ 0.73 | ≈ 1.96 | Below target |
| -0.40 | +0.40 | ~333 | ≈ 1.12 | ≈ 2.89 | Close but below |
| -0.41 | +0.41 | ~324 | ≈ 1.14 | ≈ 2.90 | Close but below |
| **-0.43** | **+0.43** | **~323** | **≈ 1.17** | **≈ 2.97** | **CONFIRMED BEST ✅** |
| -0.45 | +0.45 | ~316 | ≈ 1.03 | ≈ 2.59 | Below target |
| -0.50 | +0.50 | ~292 | ≈ 1.05 | ≈ 2.53 | Below target |
| -0.55 | +0.55 | <250 | — | REJECTED | Too few trades |

The optimum is ±0.43. The search space is essentially solved. The goal is to
reliably confirm this value survives the acceptance criterion, not to discover
something new.

---

## KNOWN BAD PARAMETERS — DO NOT USE

| What | Bad value | What it causes |
|------|-----------|----------------|
| ANY indicator | `momentum_accelerating` | Sharpe ≈ -7 to -9, catastrophic |
| ANY indicator | `price_vs_ema` | Sharpe ≈ -7 to -9, catastrophic |
| ANY indicator | `trend` | Sharpe ≈ -7 to -9, catastrophic |
| `style` | anything except `momentum_optimized` | Template corruption |
| `max_open` | 2 or 3 | Suboptimal or false optimum |
| `stop_loss_pct` | 0.4 | Catastrophic loss |
| `take_profit_pct` | 3.51 | Corrupted template value, rejected |
| `timeout_minutes` | 706 | Corrupted template value |
| `period_minutes` on `price_change_pct` | 5 | 148-trade attractor, false optimum |
| `period_minutes` on `price_change_pct` | 60 | 490-trade attractor, false optimum |
| `price_change_pct` long value | above -0.30 | ~690 trades, negative Sharpe |
| `price_change_pct` long value | below -0.50 | <250 trades, auto-rejected |

---

## ⚠️ THE CORRUPTED STRATEGY — DO NOT USE AS A TEMPLATE ⚠️

A previous research phase produced a corrupted "current best strategy" with:
- 10 pairs instead of 16
- `max_open: 3` instead of 4
- `stop_loss_pct: 0.4` instead of 1.2
- `take_profit_pct: 3.51` instead of 2.5
- `timeout_minutes: 706` instead of 720
- `style: momentum_price_change_macd_ema_trend_filter` (FORBIDDEN)
- Forbidden indicators: `momentum_accelerating`, `price_vs_ema`, `trend`
- 5 conditions per side instead of 2

**This corrupted strategy MUST NOT be used as a template under any circumstances.**
**The only valid template is the YAML shown in "THE ONE AND ONLY VALID OUTPUT FORMAT" above.**

---

## MANDATORY PRE-OUTPUT CHECKLIST

You MUST verify every item before outputting. If any item fails, fix it and restart.

| # | Check | Required | Wrong value |
|---|-------|----------|-------------|
| 1 | `name` | `crossover` | anything else |
| 2 | `style` | `momentum_optimized` | anything else |
| 3 | Number of pairs | exactly 16 | any other count |
| 4 | `size_pct` | 10 | anything else |
| 5 | `max_open` | 4 | 2, 3, or any other |
| 6 | `fee_rate` | 0.001 | anything else |
| 7 | Conditions in `long` | exactly 2 | any other count |
| 8 | Conditions in `short` | exactly 2 | any other count |
| 9 | First long indicator | `price_change_pct` | anything else |
| 10 | Second long indicator | `macd_signal` |