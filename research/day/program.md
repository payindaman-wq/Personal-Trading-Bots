```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 4900-CANONICAL-RECOVERY

---

## ⚠️ CRITICAL: READ THE ENTIRE DOCUMENT BEFORE WRITING ANY OUTPUT ⚠️

---

## THE ONE AND ONLY VALID OUTPUT FORMAT

You must output exactly this YAML. The ONLY thing you may change is the two
`price_change_pct` numeric values (one negative, one positive, same magnitude).
Copy every other field character-for-character.

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

**The values -0.43 (long) and +0.43 (short) are the current best known values.**
**You may propose a different value, but it must stay within [-0.50, -0.30] (long side).**
**The long and short values must always be the same magnitude (one negative, one positive).**
**No other parameter in this YAML may ever be changed.**

---

## YOUR ROLE — EXACTLY THIS, NOTHING MORE

You are a single-parameter tuner. Each generation you output ONE YAML.
The YAML is the template above with one possible change: the `price_change_pct`
threshold values. That is the only degree of freedom you have.

**Recommended exploration for next 100 generations:**
Try values in this set, prioritizing those closest to ±0.43:
  ±0.40, ±0.41, ±0.42, ±0.43, ±0.44, ±0.45, ±0.46, ±0.47, ±0.48

Do not jump outside ±0.05 of the current best without evidence of a trend
in the improvement history suggesting a different region is better.

---

## CURRENT STATE

### The target we are trying to re-establish

| Parameter | Value |
|-----------|-------|
| `price_change_pct` long | -0.43 |
| `price_change_pct` short | +0.43 |
| Sharpe | 1.17 |
| Trades | 323 |
| Adjusted score | 2.97 |
| Generation confirmed | 2163–2199 |

### Current actual best (gen 4687)

| Parameter | Value |
|-----------|-------|
| `price_change_pct` long | (approaching -0.43) |
| Sharpe | 1.0460 |
| Trades | 292 |
| Adjusted score | ≈ 2.52 |
| Status | BELOW TARGET — does not meet acceptance criterion |

**Step 1 is the ONLY active step. Do not advance until adjusted score ≥ 2.97 AND trades ≥ 250.**

### Adjusted score formula
```
adjusted_score = Sharpe × sqrt(trades / 50)
```

Before submitting your output, compute this value mentally:
- If trades < 250: your strategy fires too rarely → REJECTED regardless of Sharpe
- If adjusted_score < 2.97: your strategy has not beaten the target → keep exploring
- If adjusted_score ≥ 2.97 AND trades ≥ 250: target achieved → report and hold

---

## MANDATORY PRE-OUTPUT CHECKLIST

You MUST verify every item. If any item fails, fix it before outputting.

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
| 10 | Second long indicator | `macd_signal` | anything else |
| 11 | First short indicator | `price_change_pct` | anything else |
| 12 | Second short indicator | `macd_signal` | anything else |
| 13 | `price_change_pct` period | 30 | any other value |
| 14 | `macd_signal` period | 30 | any other value |
| 15 | Long `price_change_pct` value | NEGATIVE, in [-0.50, -0.30] | positive or out of range |
| 16 | Short `price_change_pct` value | POSITIVE, in [+0.30, +0.50] | negative or out of range |
| 17 | Symmetric values | YES — same magnitude | asymmetric |
| 18 | `take_profit_pct` | 2.5 | anything else |
| 19 | `stop_loss_pct` | 1.2 | anything else |
| 20 | `timeout_minutes` | 720 | anything else |
| 21 | `pause_if_down_pct` | 4 | anything else |
| 22 | `stop_if_down_pct` | 10 | anything else |
| 23 | `pause_minutes` | 60 | anything else |
| 24 | No forbidden strings present | YES | see list below |

---

## FORBIDDEN STRINGS — IF ANY APPEAR IN YOUR OUTPUT, DELETE AND RESTART

- `autobotday`
- `momentum_accelerating`
- `price_vs_ema`
- `trend` (as an indicator name or value)
- `momentum_price_change_macd_ema_trend_filter`
- `max_open: 2`
- `max_open: 3`
- `stop_loss_pct: 0.4`
- `take_profit_pct: 3.51`
- `size_pct: 10.2`
- `timeout_minutes: 706`
- Any pair list with fewer or more than 16 entries
- Any condition block with fewer or more than 2 conditions per side

---

## KNOWN BAD PARAMETERS — DO NOT USE

| What | Bad value | What it causes |
|------|-----------|----------------|
| Any indicator | `momentum_accelerating` | Sharpe ≈ -7.8, ~500 trades, catastrophic |
| Any indicator | `price_vs_ema` | Same catastrophic result |
| Any indicator | `trend` | Same catastrophic result |
| `max_open` | 2 or 3 | Suboptimal or false optimum |
| `stop_loss_pct` | 0.4 | Catastrophic loss |
| `take_profit_pct` | 3.51 | Corrupted template value, rejected |
| `period_minutes` on `price_change_pct` | 5 | 148-trade attractor, false optimum |
| `period_minutes` on `price_change_pct` | 60 | 490-trade attractor, false optimum |
| `price_change_pct` long value | above -0.30 | 690-trade negative Sharpe |
| `price_change_pct` long value | below -0.50 | Strategy fires too rarely, rejected |

---

## KNOWN PARAMETER PERFORMANCE MAP

| Long value | Short value | Est. trades | Notes |
|------------|-------------|-------------|-------|
| -0.30 | +0.30 | ~690 | Negative Sharpe — DO NOT USE |
| -0.38 | +0.38 | ~363 | Sharpe ≈ 0.73 — below target |
| -0.40 | +0.40 | ~333 | Sharpe ≈ 1.12 — close to target |
| -0.41 | +0.41 | ~324 | Sharpe ≈ 1.14 — close to target |
| **-0.43** | **+0.43** | **~323** | **Sharpe ≈ 1.17 — CONFIRMED BEST** |
| -0.45 | +0.45 | ~316 | Sharpe ≈ 1.03 — below target |
| -0.50 | +0.50 | ~292 | Sharpe ≈ 1.05 — below target |
| -0.55 | +0.55 | <250 | Below MIN_TRADES floor — REJECTED |

The optimum is well-established at ±0.43. Fine-grained search between ±0.41 and
±0.45 is the most productive remaining search space. Values outside ±0.05 of 0.43
have been explored and are unlikely to beat the target.

---

## STEP ROADMAP

| Step | Status | Long value | Short value | Accept if |
|------|--------|------------|-------------|-----------|
| **1** | **ACTIVE** | **-0.43** | **+0.43** | **adjusted_score ≥ 2.97 AND trades ≥ 250** |
| 2 |