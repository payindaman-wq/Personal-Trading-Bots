```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 4200-CANONICAL-RESTORE

---

## ══════════════════════════════════════════════════════
## CRITICAL: READ THIS ENTIRE DOCUMENT BEFORE OUTPUTTING ANYTHING
## ══════════════════════════════════════════════════════

**The "Current Best Strategy" block shown by ODIN may be corrupted.**
**Ignore it. The ONLY valid baseline is the CANONICAL YAML below.**

The true canonical baseline:
- Sharpe = 1.17, trades = 323, adjusted score = **2.97**
- `max_open: 4` (NOT 3)
- `price_change_pct: ±0.43` (NOT ±0.50)
- This is what you must copy exactly before making any change.

---

## YOUR ONLY JOB

**Copy the CANONICAL YAML below exactly. Change ONLY the two `price_change_pct` values as instructed in the "One Change" section.**

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

**This is the ONLY valid template. Do not use any other YAML — not the "Current Best Strategy" block, not anything from earlier in the conversation history, not any YAML you remember from previous generations.**

---

## The One Change You Are Allowed to Make

Change the `price_change_pct` values symmetrically. Try values in this order, one per generation:

| Step | Long value | Short value | Goal |
|------|-----------|------------|------|
| 1    | -0.43     | +0.43      | Confirm canonical baseline (adjusted score ≥ 2.97, trades ≥ 250) |
| 2    | -0.40     | +0.40      | Try to increase trade count toward ~380 |
| 3    | -0.38     | +0.38      | Try to increase trade count toward ~400 |
| 4    | -0.35     | +0.35      | Try to increase trade count toward ~420 |

**Rules:**
- If current step produces adjusted score > 2.97 with trades ≥ 250 → record as improvement, proceed to next step
- If current step fails → skip to next step (do not retry the same value)
- **Never go below ±0.30** — this triggers the 690-trade negative Sharpe attractor
- **Never go above ±0.50** — this is the original baseline, worse than canonical
- **Never jump more than ±0.05 in one step**
- Long `value` must always be **NEGATIVE** (e.g., `-0.43`)
- Short `value` must always be **POSITIVE** (e.g., `+0.43`)
- Both must be the **same absolute magnitude**

---

## What "Adjusted Score" Means

**Adjusted score = Sharpe × sqrt(trades / 50)**

The adjusted score rewards both high Sharpe AND high trade count. A result with fewer than 250 trades is automatically rejected regardless of Sharpe, because it has not been tested on enough events to be statistically meaningful.

| Sharpe | Trades | Adjusted Score | Verdict |
|--------|--------|----------------|---------|
| 1.17   | 323    | **2.97**       | ← CANONICAL BASELINE — must beat this |
| 1.19   | 148    | 2.05           | ✗ REJECTED — too few trades, low adjusted score |
| 1.18   | 148    | 2.04           | ✗ REJECTED — this is the 148-trade false optimum |
| 1.10   | 350    | 3.08           | ✓ IMPROVEMENT |
| 1.10   | 400    | 3.11           | ✓ CLEAR IMPROVEMENT |
| 1.05   | 420    | 3.04           | ✓ IMPROVEMENT |
| 1.00   | 450    | 3.00           | ✓ MARGINAL IMPROVEMENT |
| 0.80   | 500    | 2.53           | ✗ NOT ACCEPTABLE |
| -7.31  | 490    | CATASTROPHIC   | ✗ NEVER APPROACH |

**Hard rules — non-negotiable:**
- Minimum trades: **250**. Any result below 250 is automatically rejected.
- Minimum adjusted score: **2.97**. Anything lower is rejected.
- The 148-trade cluster (any Sharpe, ~148 trades, adjusted ~2.0) is always rejected.

---

## Known Attractors — These Are Traps

### 🔴 Attractor A: 490-Trade Catastrophe
- **Signature:** ~490 trades, Sharpe ≈ -7.30, win_rate ≈ 38%
- **Cause:** Using wrong YAML (e.g., `max_open: 3` instead of 4), or `price_change_pct` below ±0.30
- **Recovery:** Copy the canonical YAML exactly, use ±0.43

### 🟡 Attractor B: 148-Trade False Optimum  ← YOU ARE CURRENTLY IN THIS ATTRACTOR
- **Signature:** ~131–161 trades, Sharpe ~1.0–1.2, adjusted score ~1.8–2.1
- **Cause:** Using `max_open: 3` instead of 4, OR `price_change_pct: ±0.50` instead of ±0.43
- **Why it's bad:** Adjusted score ~2.0 is WORSE than canonical 2.97. This is not progress.
- **Recovery:** Use the canonical YAML above with `max_open: 4` and start at ±0.43
- **Warning:** The last 400+ generations have been stuck in this attractor. Do not continue it.

### 🔴 Attractor C: 690–1322 Trade Negative Sharpe
- **Signature:** 690–1322 trades, Sharpe -1.0 to -2.2
- **Cause:** `price_change_pct` below ±0.25
- **Recovery:** Return to canonical ±0.43

### 🔴 Attractor D: 503-Trade Negative Sharpe
- **Signature:** ~503 trades, Sharpe ≈ -0.85, win_rate ≈ 18%
- **Cause:** Structural changes to the YAML (wrong indicators, wrong periods)
- **Recovery:** Return to canonical YAML

---

## ❌ Absolute Prohibitions — All Tested, All Failed

Every item below has been tested across hundreds of generations. Do not use any of them.

1. **`max_open: 3`** → Produces the 148-trade attractor. The canonical value is `max_open: 4`.
2. **`price_change_pct: ±0.50`** → Original baseline, worse than canonical. Do not use.
3. **`indicator: trend`** → Always Sharpe -6 to -14. Never use.
4. **`indicator: momentum_accelerating`** → Not a real indicator. Never use.
5. **`indicator: price_vs_ema`** → Catastrophic. Never use.
6. **`period_minutes: 5` on price_change_pct** → Too noisy. Destroys Sharpe.
7. **`size_pct` other than 10** → Rejected. Canonical value is optimal.
8. **`max_open` other than 4** → Rejected. Any other value causes attractor B or A.
9. **Fewer than 16 pairs** → Immediately rejected.
10. **More than 2 conditions per entry side** → Immediately rejected.
11. **`stop_loss_pct` outside [1.0, 1.5]** → Rejected. Canonical 1.2 is optimal.
12. **`take_profit_pct` outside [2.0, 3.5]** → Rejected. Canonical 2.5 is optimal.
13. **`timeout_minutes` other than 720** → Rejected. Canonical value is optimal.
14. **Asymmetric `price_change_pct`** (different magnitudes for long vs short) → Bad results.
15. **`period_minutes` other than 30 on `price_change_pct`** → Produces 148-trade or 490-trade attractor.
16. **`period_minutes` other than 30 on `macd_signal`** → Produces attractor.
17. **Any change other than `price_change_pct` values** → All other parameters are at optimum.
18. **Copying the "Current Best Strategy" block from ODIN's prompt** → It may be corrupted (`max_open: 3`). Always use the canonical YAML above.

---

## Why Only price_change_pct?

After 4200 generations across 16 pairs, all other parameters have been exhaustively tested:
- Exit parameters (take_profit_pct, stop_loss_pct, timeout_minutes): canonical values are optimal
- Position sizing (size_pct=10, max_open=4): optimal
- Additional indicators: all reduce performance or cause catastrophic failure
- Pair count and selection: 16 pairs is optimal

**The only productive direction remaining:** relax `price_change_pct` from ±0.43 toward ±0.35 in small steps to increase trade count from ~323 toward ~400, while keeping Sharpe above 1.0.

The hypothesis: if ±0.40 produces ~380 trades at Sharpe 1.05, adjusted score = 1.05 × sqrt(380/50) = **2.89** (marginal). If Sharpe holds at 1.10, adjusted score = 1.10 × sqrt(380/50) = **3.03** (clear improvement). This is the only unresolved research question.

The 148-trade cluster (±0.50, max_open=3) has been confirmed as a dead end across 400+ generations (gens 2422–4200). Do not return to it.

---

## Verification