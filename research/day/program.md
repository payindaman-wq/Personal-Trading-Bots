```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 4800-TEMPLATE-FIRST

---

## ⚠️ READ THIS FIRST — THE ONLY VALID YAML IS BELOW ⚠️

The ONLY valid strategy output is shown immediately below.
Copy it exactly. Change ONLY the two `price_change_pct` numeric values.
There is no other valid strategy. Do not look elsewhere in this document for a YAML to copy.

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

**This is the ONLY template. The values -0.43 and +0.43 are the current target.**
**The ONLY thing that changes between generations is the numeric value**
**on the two `price_change_pct` lines (one negative, one positive, same magnitude).**

---

## YOUR ROLE AND CONSTRAINT

You are a strategy parameter tuner. You output ONE YAML per generation.
You may ONLY modify the `price_change_pct` threshold values (long and short).
You may NOT change any other parameter. You may NOT add indicators. You may NOT
remove indicators. Any other change will cause catastrophic test failure.

The YAML template is shown above. Use it. Do not use any other source.

---

## ⚠️ FORBIDDEN STRATEGY — DO NOT COPY ⚠️

A previous run produced a catastrophic failing strategy. It is described here
in TEXT ONLY (no YAML) so you know what to avoid.

The failing strategy had these properties (all of which are WRONG):
- name was `autobotday` — WRONG
- style was `momentum_price_change_macd_ema_trend_filter` — WRONG
- Only 10 pairs — WRONG (correct is 16)
- `max_open: 3` — WRONG (correct is 4)
- 5 conditions per side — WRONG (correct is 2)
- Used indicators `momentum_accelerating`, `price_vs_ema`, `trend` — ALL WRONG
- `stop_loss_pct: 0.4` — WRONG (correct is 1.2)
- `take_profit_pct: 3.51` — WRONG (correct is 2.5)
- `timeout_minutes: 706` — WRONG (correct is 720)
- Produced Sharpe = -7.84, 500 trades — CATASTROPHIC

If your output contains any of the following strings, it is wrong — delete and restart:
- `autobotday`
- `momentum_accelerating`
- `price_vs_ema`
- `trend` (as an indicator value)
- `max_open: 2` or `max_open: 3`
- `stop_loss_pct: 0.4`
- `take_profit_pct: 3.51`
- `size_pct: 10.2`
- `momentum_price_change_macd_ema_trend_filter`
- `timeout_minutes: 706`
- Any number of pairs other than 16
- Any number of conditions per side other than 2

---

## PRE-OUTPUT CHECKLIST

Before writing your output, confirm every item. If any item fails, fix it.

| # | What to check | Required value | Wrong value to watch for |
|---|---------------|----------------|--------------------------|
| 1 | `name` | `crossover` | `autobotday` |
| 2 | `style` | `momentum_optimized` | `momentum_price_change_macd_ema_trend_filter` |
| 3 | Number of pairs | 16 | 10 |
| 4 | `size_pct` | 10 | 10.2 |
| 5 | `max_open` | 4 | 2 or 3 |
| 6 | `fee_rate` | 0.001 | any other |
| 7 | Conditions in `long` | exactly 2 | 5 |
| 8 | Conditions in `short` | exactly 2 | 5 |
| 9 | First long indicator | `price_change_pct` | `momentum_accelerating` |
| 10 | Second long indicator | `macd_signal` | `price_vs_ema` |
| 11 | First short indicator | `price_change_pct` | `momentum_accelerating` |
| 12 | Second short indicator | `macd_signal` | `trend` |
| 13 | `price_change_pct` period | 30 | 5 or 60 |
| 14 | `macd_signal` period | 30 | 60 or 240 |
| 15 | Long `price_change_pct` value | NEGATIVE number | positive number |
| 16 | Short `price_change_pct` value | POSITIVE number | negative number |
| 17 | Both values same magnitude | YES | asymmetric values |
| 18 | Value within allowed range | between -0.30 and -0.50 (long side) | outside range |
| 19 | `take_profit_pct` | 2.5 | 3.51 |
| 20 | `stop_loss_pct` | 1.2 | 0.4 |
| 21 | `timeout_minutes` | 720 | 706 or any other |
| 22 | `pause_if_down_pct` | 4 | any other |
| 23 | `stop_if_down_pct` | 10 | any other |
| 24 | `pause_minutes` | 60 | any other |

---

## KNOWN BAD PARAMETERS

| Parameter | Bad value | Effect |
|-----------|-----------|--------|
| Any indicator | `momentum_accelerating` | Sharpe -7.84, 500 trades, CATASTROPHIC |
| Any indicator | `price_vs_ema` | Sharpe -7.84, 500 trades, CATASTROPHIC |
| Any indicator | `trend` | Sharpe -7.84, 500 trades, CATASTROPHIC |
| `max_open` | 2 | false optimum or worse |
| `max_open` | 3 | false optimum |
| `stop_loss_pct` | 0.4 | catastrophic loss |
| `take_profit_pct` | 3.51 | from corrupted template, rejected |
| `size_pct` | 10.2 | rejected |
| `period_minutes` on `price_change_pct` | 5 | 148-trade attractor |
| `period_minutes` on `price_change_pct` | 60 | 490-trade attractor |
| `price_change_pct` long value | above -0.30 | 690-trade negative Sharpe |
| `price_change_pct` long value | below -0.55 | strategy rarely fires |
| Number of pairs | 10 | immediately rejected |
| Conditions per side | 5 | Sharpe -7.84, catastrophic |

---

## CURRENT STATE AND TASK

### Research summary

**Confirmed historical best (gens 2163–2199):**
- `price_change_pct`: long = -0.43, short = +0.43
- Sharpe = 1.17, trades = 323, adjusted score = 2.97
- This is the TARGET. It must be re-established before any exploration.

**Current actual best (gen 4687):**
- Sharpe = 1.0460, trades = 292, adjusted score ≈ 2.52
- This does NOT yet meet the acceptance criterion (adjusted score < 2.97)
- The system is approaching but has not re-established the canonical baseline

**Why the baseline was lost (history — do not repeat):**
- A corrupted strategy (`autobotday`) appeared in context and was copied by the LLM
- This caused the -7.84/500-trade failure mode in ~35% of generations 4783–4800
- The corrupted YAML has been removed from the prompt; only a text description remains
- MIN_TRADES was incorrectly set to 80, enabling a 148-trade false optimum cluster
  (gens 2422–2932, Sharpe ~1.19 but adjusted score only ~2.05 — REJECTED)
- MIN_TRADES is now correctly set to 250 and must NOT be changed

**False optimum to avoid:**
- 148-trade cluster: Sharpe ~1.19, adjusted score ~2.05 → REJECTED
- Appears attractive on raw Sharpe but fails adjusted score criterion
- Was caused by MIN_TRADES being set to 80 (now permanently fixed at 250)

### Adjusted score formula
`adjusted_score = Sharpe × sqrt(trades / 50)`

### Current step

**STEP 1 IS THE ONLY ACTIVE STEP.**
Do not advance to Step 2 until Step 1 has confirmed adjusted score ≥ 2.97.

| Step | Long value | Short value | Target trades | Accept if |
|------|------------|-------------|---------------|-----------|
| **1 (ACTIVE)** | **-0.43** | **+0.43** | **~323** | **adjusted score ≥ 2.97 AND trades ≥ 250** |
| 2 (LOCKED) |