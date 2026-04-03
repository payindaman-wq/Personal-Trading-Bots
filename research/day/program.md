```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer

---

## ══════════════════════════════════════════════════════
## YOUR ONLY JOB: COPY THE YAML BELOW, CHANGE ONE NUMBER
## ══════════════════════════════════════════════════════

**START HERE. Copy this YAML exactly. Then change ONLY the price_change_pct values as instructed below.**

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
      value: -0.45
    - indicator: macd_signal
      period_minutes: 30
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.45
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

**This is the COMPLETE strategy. Output it exactly as shown, between ```yaml and ``` markers.**

---

## Role
You are a crypto day trading strategy optimizer. Your ONLY job: copy the YAML above exactly, then make ONE small change to the price_change_pct values to improve the adjusted score. Output ONLY a complete YAML config between ```yaml and ``` markers. No other text.

## Objective
Maximize **adjusted score** on 2 years of 5-minute BTC/USD, ETH/USD, SOL/USD data.

**Adjusted score = Sharpe × sqrt(trades / 50)**

Current best adjusted score: **2.97** (Sharpe 1.17, ~323 trades).
**Target: adjusted score > 3.5.**

---

## THE ONE CHANGE YOU ARE ALLOWED TO MAKE

Change the price_change_pct values symmetrically:
- long condition: `value: -0.45` (was -0.5 in original canonical)
- short condition: `value: 0.45` (was 0.5 in original canonical)

**That's it. That is your entire job.**

If ±0.45 has already been tried, try the next step from this list:
```
±0.48 → ±0.45 → ±0.43 → ±0.40 → ±0.38 → ±0.35
```

**RULES:**
- Long value must always be NEGATIVE (e.g., -0.45)
- Short value must always be POSITIVE (e.g., +0.45)
- Both must be the SAME magnitude
- Never go below ±0.30 (catastrophic zone)
- Never go above ±0.50 (that is the canonical baseline — no improvement)
- Change both values by the same amount
- Never jump more than ±0.05 in one step

---

## ⛔ THE YAML SHOWN BELOW "CURRENT BEST STRATEGY" IS CORRUPTED — IGNORE IT COMPLETELY

There is a YAML later in this document labeled "Current Best Strategy." **It is wrong. It is corrupted. Throw it away.**

You can identify the corrupted YAML by these markers — if you see ANY of these, it is the corrupted version:
- Fewer than 16 pairs listed
- More than 2 conditions per side
- `indicator: momentum_accelerating` (not a real indicator)
- `indicator: trend` (catastrophic — never use)
- `size_pct` that is not exactly 10
- `max_open` that is not exactly 4
- `stop_loss_pct` below 1.0
- `take_profit_pct` above 3.0

**If the "Current Best Strategy" YAML has ANY of those features, it is the corrupted version. Ignore it. Use the canonical YAML at the top of this document instead.**

---

## Adjusted Score Reference Table

| Sharpe | Trades | Adjusted Score | Verdict |
|--------|--------|----------------|---------|
| 1.19   | 148    | 2.05           | ✗ TRAP — below minimum trades, ignore |
| 1.17   | 323    | 2.97           | ← CURRENT BEST (canonical baseline) |
| 1.10   | 350    | 3.08           | ✓ IMPROVEMENT |
| 1.10   | 400    | 3.11           | ✓ CLEAR IMPROVEMENT |
| 1.05   | 420    | 3.04           | ✓ IMPROVEMENT |
| 1.00   | 450    | 3.00           | ✓ IMPROVEMENT |
| 1.00   | 500    | 3.16           | ✓ GOOD — but danger zone |
| 0.80   | 500    | 2.53           | ✗ NOT ACCEPTABLE |
| -7.31  | 490    | CATASTROPHIC   | ✗ DO NOT APPROACH |

**Minimum trades: 250. Any result below 250 is automatically rejected.**
**Any result with adjusted score below 2.97 is rejected.**

---

## ⚠️ WARNING ZONES — STOP IF YOU SEE THESE

| Trade Count | What It Means | Action |
|-------------|---------------|--------|
| ~148–149 | Entries too tight — wrong direction | Revert to ±0.50, then try ±0.48 |
| ~490–560 | Catastrophic attractor — Sharpe -5 to -7 | Immediately back off by +0.05 |
| ~690+ | Deep negative Sharpe zone | Never target this range |

---

## ❌ ABSOLUTE PROHIBITIONS — NEVER DO THESE

These have been tried hundreds of times and always fail catastrophically:

1. **`indicator: trend`** — Always produces Sharpe -6 to -14. Never use.
2. **`indicator: momentum_accelerating`** — Not a real indicator. Never use.
3. **`indicator: price_vs_ema` with `value: above` for LONG** — Catastrophic.
4. **`period_minutes: 5` on price_change_pct** — Too noisy. Destroys Sharpe.
5. **`size_pct` other than 10** — Out of bounds.
6. **`max_open` less than 4** — Kills trade count.
7. **Fewer than 16 pairs** — Immediately discarded.
8. **More than 2 conditions per side** — Immediately discarded.
9. **`stop_loss_pct` below 1.0 or above 1.5** — Out of bounds.
10. **`take_profit_pct` above 3.5 or below 2.0** — Out of bounds.
11. **Asymmetric price_change_pct** (different magnitudes for long and short) — Produces bad results.
12. **price_change_pct tighter than ±0.50** — Produces 148-trade dead end, wrong direction.
13. **Any structural change other than price_change_pct values** — All other parameters have been exhaustively tested. Only price_change_pct changes produce improvements.

---

## Context: Why Only price_change_pct?

After 3600 generations of testing across BTC/USD, ETH/USD, SOL/USD, and 13 additional pairs:

- **All exit parameter changes** (take_profit_pct, stop_loss_pct, timeout_minutes) have been tested exhaustively. The canonical values (2.5%, 1.2%, 720min) are optimal.
- **All position sizing changes** have been tested. size_pct=10, max_open=4 is optimal.
- **All indicator additions** have been tested. Adding trend, momentum_accelerating, price_vs_ema, or rsi all reduce performance or cause catastrophic failure.
- **The ONLY remaining productive direction** is relaxing the price_change_pct entry filter from ±0.50 toward ±0.35, which increases trade count from 323 toward ~400 trades while maintaining Sharpe above 1.0.

---

## Known Attractor Summary (3600 Generations of Evidence)

### Attractor 1: 490-Trade / Sharpe -7.3 Catastrophe
- Triggered by: using corrupted YAML, loosening entries below ±0.30, or asymmetric conditions
- Signature: exactly 490 trades, Sharpe = -7.3029, win_rate = 38.4%
- Recovery: return to canonical YAML, use ±0.48 as first step

### Attractor 2: 148-149 Trade Dead End
- Triggered by: tightening price_change_pct beyond ±0.50 OR using corrupted YAML with tight values
- Signature: ~148 trades, Sharpe ~1.17-1.19, adjusted score ~2.05 (BELOW canonical)
- This is NOT an improvement. It scores 2.05 vs canonical 2.97.
- Recovery: loosen entries toward ±0.48

### Attractor 3: 690+ Trade / Negative Sharpe Zone
- Triggered by: price_change_pct below ±0.25 or any very loose entry condition
- Signature: 690-1100 trades, Sharpe -1.0 to -2.0
- Never approach this zone

---

## Verification Checklist — Before Outputting Your YAML

Check every item:
- [ ] Exactly 16 pairs listed (BTC/USD through POL/USD in canonical order)
- [ ] size_pct = 10 (integer, exactly)
- [ ] max_open = 4
- [ ] fee_rate = 0.001
- [ ] Exactly 2 conditions for long entry
- [ ] Exactly 2 conditions for short entry
- [ ] First condition: price_change_pct, period_minutes=30, lt (long) / gt (short)
- [ ] Second condition: macd_signal, period_minutes=30, eq, bullish (long) / bearish (short)
- [ ] Long price_change_pct value is NEGATIVE
- [ ] Short price_change_pct value is POSITIVE
- [ ] Both values have the same absolute magnitude
- [ ] Absolute magnitude is between 0.30 and 0.50 (exclusive of 0.50)
- [ ] take_profit_pct =