```markdown
# ODIN Research Program — FUTURES DAY (v4)

## League: futures_day
Timeframe: 5-minute candles, 24h sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (applied automatically in backtest)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage

---

## ⚠️ CRITICAL SITUATION REPORT — READ EVERY WORD BEFORE PROPOSING ANY CHANGE

**After 400 generations, the best Sharpe ever achieved is −6.15. Zero generations have
reached positive Sharpe. The strategy is fundamentally broken at its current
configuration. Every minor RSI tweak you propose makes things worse.**

**THE SINGLE RULE: Do not touch RSI thresholds. Do not add entry conditions.
Do not reduce pairs. Your ONLY job is to follow the templates below, one at a time.**

**All-time best: Gen 140 — Sharpe −6.15, 623 trades, 41.7% WR**
**Near-champion: Gen 387 — Sharpe −6.23, 630 trades, 46.2% WR (just missed)**

**The pattern is clear: HIGH TRADE COUNT = BETTER SHARPE. Every strategy below
500 trades has performed worse. Your proposals MUST produce 500+ trades.**

---

## CONFIRMED DEAD ENDS — DO NOT REPEAT ANY OF THESE

### Entry Conditions
- RSI < 38, < 40, < 42, < 45 combined with 15-min trend: ALL EXHAUSTED
- RSI period 14–20 variations: no improvement found
- Adding volume, pivot, or any 3rd entry condition: always reduces trade count below 500
- Removing pairs: always hurts trade count and Sharpe
- Tightening stop_loss by small amounts (±0.1–0.2%): no improvement

### Exit Conditions
- 60-minute timeout: CONFIRMED BROKEN. Never use timeout > 30 minutes again.
- TP 1.5% / SL 0.73% / timeout 60min: the current champion but structurally limited
- TP 1.15% / SL 0.8% / timeout 60min: tested, no improvement

### What You Keep Doing Wrong
1. You return to RSI 38–42 threshold tweaks. STOP. This is exhausted.
2. You add a 3rd entry condition when stuck. STOP. It always hurts trade count.
3. You make ±0.1% changes to TP/SL without changing timeout. STOP.
4. You reduce the number of pairs below 16. STOP.
5. You ignore the templates below and freelance. STOP. Follow the templates.

---

## MANDATORY BASE CONFIGURATION

**This is the non-negotiable starting point. All proposals must use these 16 pairs,
2x leverage, max_open: 2, fee_rate: 0.0005.**

```yaml
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
  size_pct: 13.64
  max_open: 2
  fee_rate: 0.0005
```

**TRADE COUNT REQUIREMENT: Any strategy producing fewer than 400 trades is
statistically unreliable. If your proposed change reduces trades below 400,
the proposal is invalid. Loosen conditions until trades ≥ 400.**

---

## GENERATION ASSIGNMENTS — MANDATORY ROTATION

You will cycle through these templates IN ORDER. Do not skip. Do not freestyle.
Each template corresponds to a block of generations. After you exhaust the variants
in one block, move to the next template.

---

### TEMPLATE A: Scalp Mode — Fix the Timeout (Generations 401–430)
**This is the highest-priority fix. The 60-minute timeout is the confirmed root cause
of negative Sharpe. Shorter timeout = fewer bleed-out losses = better Sharpe.**

**Why this works mathematically:**
- R:R = 0.8/0.5 = 1.6x → breakeven WR = 38.5% (after fees ≈ 39.5%)
- Current WR is consistently 40–46% → this is ABOVE breakeven
- 15–20 min timeout means most trades resolve at TP or SL, not timeout bleed
- Smaller TP/SL targets are hit more often in high-volatility (VIX 25+) conditions
- Expected trade count: 500–800 (sufficient for reliable Sharpe)

**Primary target (start here):**
```yaml
entry:
  long:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: up
    - indicator: rsi
      period_minutes: 14
      operator: lt
      value: 42
  short:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: down
    - indicator: rsi
      period_minutes: 14
      operator: gt
      value: 58
exit:
  take_profit_pct: 0.8
  stop_loss_pct: 0.5
  timeout_minutes: 20
risk:
  pause_if_down_pct: 5
  pause_minutes: 30
  stop_if_down_pct: 12
```

**Variants to test in order (one per generation):**
1. TP 0.7% / SL 0.45% / timeout 15min → R:R 1.56x, breakeven 39.5%
2. TP 0.9% / SL 0.5% / timeout 20min → R:R 1.8x, breakeven 36.4%
3. TP 1.0% / SL 0.55% / timeout 20min → R:R 1.82x, breakeven 35.5%
4. TP 0.8% / SL 0.5% / timeout 15min → tightest timeout variant
5. TP 0.8% / SL 0.5% / timeout 25min → relaxed timeout variant
6. TP 1.0% / SL 0.5% / timeout 20min → R:R 2.0x, asymmetric
7. TP 0.75% / SL 0.5% / timeout 18min → intermediate
8. TP 0.9% / SL 0.55% / timeout 20min → slight SL widening
9. TP 1.1% / SL 0.6% / timeout 25min → moderate scalp
10. RSI threshold 44/56 (wider) with TP 0.8% / SL 0.5% / timeout 20min → more trades

**If ANY variant beats −6.15 Sharpe, immediately explore ±0.05% around that variant's
TP/SL and ±3min around its timeout. Do not jump to Template B until Template A is
exhausted or a winner is found and mined.**

---

### TEMPLATE B: Short-Only Bias (Generations 431–445)
**Current regime: F&G = 11 (Extreme Fear), sustained for weeks. In Extreme Fear,
downward momentum is structurally dominant. Short-only strategies have not been
tested. This is a major gap.**

**Primary target:**
```yaml
entry:
  short:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: down
    - indicator: rsi
      period_minutes: 14
      operator: gt
      value: 55
exit:
  take_profit_pct: 0.9
  stop_loss_pct: 0.5
  timeout_minutes: 20
risk:
  pause_if_down_pct: 5
  pause_minutes: 30
  stop_if_down_pct: 12
```
*(No long entry block — short only)*

**Variants:**
1. RSI > 58 / TP 0.8% / SL 0.5% / timeout 20min
2. RSI > 52 / TP 0.9% / SL 0.5% / timeout 20min (looser → more trades)
3. RSI > 55 / TP 1.0% / SL 0.55% / timeout 25min
4. trend 30min down + RSI > 55 / TP 0.9% / SL 0.5% / timeout 20min
5. No RSI condition, just trend 15min down / TP 0.8% / SL 0.5% / timeout 15min

**Warning:** Short-only reduces trade count. If trades fall below 400, loosen the
RSI threshold (e.g., from >58 to >52) or add SOL/USD and DOGE/USD extra weight
by duplicating them in the pairs list if the system supports it.

---

### TEMPLATE C: EMA Crossover (Generations 446–460)
**Replace RSI pullback entry entirely. EMA crossovers generate momentum signals
without the threshold calibration problem that has plagued the RSI approach.**

**Primary target:**
```yaml
entry:
  long:
    conditions:
    - indicator: ema_cross
      fast: 5
      slow: 20
      operator: crossed_above
  short:
    conditions:
    - indicator: ema_cross
      fast: 5
      slow: 20
      operator: crossed_below
exit:
  take_profit_pct: 0.9
  stop_loss_pct: 0.5
  timeout_minutes: 20
risk:
  pause_if_down_pct: 5
  pause_minutes: 30
  stop_if_down_pct: 12
```

**Variants:**
1. fast=3, slow=15 → faster signals, more trades
2. fast=8, slow=21 → slower signals, potentially higher quality
3. fast=5, slow=20 + TP 0.8% / SL