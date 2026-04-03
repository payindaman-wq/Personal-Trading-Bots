```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 3800-RESET

---

## ══════════════════════════════════════════════════════
## CRITICAL RESET NOTICE (Read Before Anything Else)
## ══════════════════════════════════════════════════════

**The research loop has been reset to the verified canonical baseline.**

- True current best: Sharpe=1.17, trades=323, adjusted score=**2.97**
- All 148-trade results (gens 2422–2932) were FALSE OPTIMA caused by MIN_TRADES=80. They are rejected.
- All 490-trade results are CATASTROPHIC FAILURES. They are rejected.
- The ONLY valid improvement target is: adjusted score > 2.97 WITH trades ≥ 250.

---

## YOUR ONLY JOB

**Copy the CANONICAL YAML below exactly. Change ONLY the two price_change_pct values as instructed.**

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

**This is the ONLY valid template. Do not use any other YAML you see in this document.**

---

## The One Change You Are Allowed to Make

Change the `price_change_pct` values symmetrically. Current target: **±0.43**.

**Try values in this order (one per generation):**

```
Next to try: ±0.43 → ±0.40 → ±0.38 → ±0.35
```

- If ±0.43 produces adjusted score > 2.97 with ≥ 250 trades → keep it, try ±0.40 next
- If ±0.43 fails → try ±0.40
- Never go below ±0.30
- Never go above ±0.50 (canonical baseline — no improvement possible there)
- Never jump more than ±0.05 in one step

**Rules:**
- Long `value` must be NEGATIVE (e.g., `-0.43`)
- Short `value` must be POSITIVE (e.g., `+0.43`)
- Both must be the SAME absolute magnitude
- Only change these two numbers — nothing else

---

## What "Adjusted Score" Means

**Adjusted score = Sharpe × sqrt(trades / 50)**

| Sharpe | Trades | Adjusted Score | Verdict |
|--------|--------|----------------|---------|
| 1.17   | 323    | **2.97**       | ← TRUE CURRENT BEST (canonical) |
| 1.19   | 148    | 2.05           | ✗ FALSE OPTIMUM — REJECTED |
| 1.10   | 350    | 3.08           | ✓ IMPROVEMENT |
| 1.10   | 400    | 3.11           | ✓ CLEAR IMPROVEMENT |
| 1.05   | 420    | 3.04           | ✓ IMPROVEMENT |
| 1.00   | 450    | 3.00           | ✓ IMPROVEMENT |
| 1.00   | 500    | 3.16           | ✓ GOOD — watch for attractor |
| 0.80   | 500    | 2.53           | ✗ NOT ACCEPTABLE |
| -7.31  | 490    | CATASTROPHIC   | ✗ NEVER APPROACH |

**Hard rules:**
- Minimum trades: **250**. Any result below 250 is automatically rejected regardless of Sharpe.
- Minimum adjusted score: **2.97**. Anything lower is rejected.
- The 148-trade cluster (Sharpe ~1.18, adjusted ~2.05) is NOT an improvement. Do not accept it.

---

## Known Attractors — Memorize These

### 🔴 Attractor A: 490-Trade Catastrophe
- **Signature:** exactly 490 trades, Sharpe ≈ -7.30, win_rate ≈ 38.4%
- **Cause:** using any YAML other than the canonical one above, OR price_change_pct below ±0.30
- **Recovery:** output the canonical YAML with ±0.43

### 🟡 Attractor B: 148-Trade False Optimum
- **Signature:** ~148 trades, Sharpe ~1.17–1.19, adjusted score ~2.05
- **Cause:** price_change_pct tighter than ±0.50, or wrong period_minutes on price_change_pct
- **Why it's bad:** adjusted score 2.05 < canonical 2.97. It is WORSE than the baseline.
- **Recovery:** loosen price_change_pct (e.g., try ±0.43, then ±0.40)

### 🔴 Attractor C: 690–1322 Trade Negative Sharpe
- **Signature:** 690–1322 trades, Sharpe -1.0 to -2.2
- **Cause:** price_change_pct below ±0.25
- **Recovery:** return to canonical ±0.43, never go below ±0.30

---

## ❌ Absolute Prohibitions — These Have All Failed Catastrophically

Every item below has been tested hundreds of times. None produce improvements. Adding them triggers attractors.

1. **`indicator: trend`** → Always Sharpe -6 to -14. Never use.
2. **`indicator: momentum_accelerating`** → Not a real indicator. Never use.
3. **`indicator: price_vs_ema` with `value: above` for LONG** → Catastrophic.
4. **`period_minutes: 5` on price_change_pct** → Too noisy. Destroys Sharpe.
5. **`size_pct` other than 10** → Out of bounds. Rejected.
6. **`max_open` other than 4** → Kills trade count. Rejected.
7. **Fewer than 16 pairs** → Immediately discarded.
8. **More than 2 conditions per entry side** → Immediately discarded.
9. **`stop_loss_pct` outside [1.0, 1.5]** → Out of bounds. Rejected.
10. **`take_profit_pct` outside [2.0, 3.5]** → Out of bounds. Rejected.
11. **Asymmetric price_change_pct** (different magnitudes for long vs short) → Bad results.
12. **Any change other than price_change_pct values** → All other parameters are at optimum.
13. **price_change_pct above ±0.50** → That is the original baseline. No improvement possible.
14. **`period_minutes` other than 30 on price_change_pct** → Produces 148-trade or 490-trade attractor.

---

## Why Only price_change_pct?

After 3800 generations across 16 pairs:
- All exit parameters (take_profit_pct, stop_loss_pct, timeout_minutes) exhaustively tested. Canonical values are optimal.
- All position sizing changes exhaustively tested. size_pct=10, max_open=4 is optimal.
- All additional indicators exhaustively tested. All reduce performance or cause catastrophic failure.
- **The only productive direction:** relaxing price_change_pct entry filter from ±0.45 toward ±0.35 to increase trade count from ~323 toward ~400 while maintaining Sharpe above 1.0.

The hypothesis: the 22–25% win rate at ±0.45 can be partially traded off for volume. If ±0.40 produces ~380 trades at Sharpe 1.05, adjusted score = 1.05 × sqrt(380/50) = 1.05 × 2.76 = **2.90** — marginal. If Sharpe stays at 1.10, adjusted score = **3.03** — a clear improvement. This is the only unresolved question in the research space.

---

## Verification Checklist — Check Every Item Before Outputting

- [ ] Exactly 16 pairs listed in canonical order (BTC/USD through POL/USD)
- [ ] `size_pct: 10` (integer, exactly)
- [ ] `max_open: 4` (exactly)
- [ ] `fee_rate: 0.001` (exactly)
- [ ] Exactly **2** conditions for long entry (no more, no fewer)
- [ ] Exactly **2** conditions for short entry (no more, no fewer)
- [ ] Long condition 1: `indicator: price_change_pct`, `period_minutes: 30`, `operator: lt`, value is NEGATIVE
- [ ] Short condition 1: `indicator: price_change_pct`, `period_minutes: 30`, `operator: gt`, value is POSITIVE
- [ ] Long condition 2: `indicator: macd_signal`, `period_