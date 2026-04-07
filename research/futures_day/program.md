```markdown
# ODIN Research Program — FUTURES DAY (v3)

## League: futures_day
Timeframe: 5-minute candles, 24h sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (applied automatically in backtest)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage

---

## ⚠️ CRITICAL SITUATION REPORT — READ EVERY WORD

**After 200 generations, the best Sharpe ever achieved is −6.15. Zero generations have
reached positive Sharpe. The strategy is fundamentally broken.**

**The current YAML champion (Sharpe −10.31) is WORSE than the research elite cluster.
The true best-performing configuration discovered so far is Gen 140: Sharpe −6.15,
623 trades, 41.7% win rate. The key insight from Gen 140: MORE TRADES = BETTER SHARPE,
even with a LOWER win rate. Do not tighten entry conditions. Loosen them.**

**Root cause identified: The timeout exit (60 minutes) is killing profitability.**
Most trades are not reaching TP or SL — they are timing out at small losses. This
collapses the real R:R ratio regardless of what the TP/SL parameters say. You MUST
address timeout exits. Target: timeout ≤ 25 minutes OR increase TP to guarantee
most winners resolve before timeout.

**TRADE COUNT REQUIREMENT: ANY strategy producing fewer than 350 trades in backtest
is statistically unreliable and will be discarded. When proposing changes, bias
toward MORE entries, not fewer. Wider RSI windows, fewer conditions, more pairs.**

---

## What Has Been Tried and Failed (Do Not Repeat)

### Entry Conditions — Exhausted
- RSI thresholds in the 35–42 range for longs: all tested, no improvement
- RSI period 14–20 combined with 15-min trend: structural ceiling hit at ~44% WR
- Adding 3rd entry condition (volume, pivot, etc.): reduces trade count, hurts Sharpe
- Tightening stop_loss by 0.1–0.2% without other changes: no improvement
- Reducing pairs from 16 to 8: reduces trade count below 300, hurts Sharpe

### Exit Conditions — Partially Explored
- TP 1.15% / SL 0.8% / timeout 60min: original, Sharpe ≈ −10.3
- TP 1.5% / SL 0.73% / timeout 60min: current champion, still −10.3 (timeout kills it)
- The 60-minute timeout is a confirmed problem. Do not keep it.

### Structural Alternatives — NOT YET PROPERLY TESTED
The small LLM has ignored these suggestions and kept tweaking RSI thresholds.
The next 100 generations MUST test these. They are listed in priority order.

---

## GENERATION ASSIGNMENTS — Follow This Rotation

To prevent the small LLM from defaulting to minor tweaks, each generation should
test ONE specific template from the priority list below. Cycle through them.

---

### PRIORITY 1: Fix the Timeout Problem (Generations 201–220)

**The single most important fix is reducing timeout_minutes.**

The current 60-minute timeout means most trades expire at a small loss. Cut it to
15–20 minutes. This forces faster trade resolution and minimizes funding drag.

**Target configuration (scalp mode):**
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
      value: 42      # slightly wider than 38 to maintain trade count
  short:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: down
    - indicator: rsi
      period_minutes: 14
      operator: gt
      value: 58      # symmetric with long threshold
exit:
  take_profit_pct: 0.8
  stop_loss_pct: 0.5
  timeout_minutes: 20
```

**Why this works mathematically:**
- R:R = 0.8/0.5 = 1.6x → breakeven WR = 39.3% after fees
- Current WR is consistently 40–44% → this is ABOVE breakeven
- 20-min timeout means fewer timeout losses, more clean TP/SL resolution
- Smaller TP/SL means faster resolution in volatile conditions
- Expected trade count: 400–700 (sufficient for reliable Sharpe)

**Variants to explore within Priority 1:**
- TP 0.7% / SL 0.45% / timeout 15min → R:R 1.56x, breakeven 39.5%
- TP 0.9% / SL 0.5% / timeout 25min → R:R 1.8x, breakeven 36.4%
- TP 1.0% / SL 0.55% / timeout 20min → R:R 1.82x, breakeven 35.5%

---

### PRIORITY 2: EMA Crossover Entry (Generations 221–235)

Replace the RSI pullback entry entirely with EMA crossover. This is a trend-momentum
signal that does not suffer from the RSI threshold calibration problem.

**Target configuration:**
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
```

**Why try this:** EMA crossovers on 5-min data in high-volatility conditions (VIX 26+)
generate clean momentum signals. The fast/slow ratio (5/20) captures short-term momentum
without the lag of longer EMAs. No RSI threshold calibration needed.

**Variants:**
- fast=3, slow=15 → faster signals, more trades
- fast=8, slow=21 → slower signals, higher quality
- Add trend filter: only cross_above if 30-min trend = up

---

### PRIORITY 3: Deep Mean Reversion (Generations 236–250)

Use extreme RSI values (not the moderate 38/42 range that has failed). RSI < 25 or
RSI > 75 captures genuinely oversold/overbought conditions with snap-back potential.

**Target configuration:**
```yaml
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 14
      operator: lt
      value: 25
  short:
    conditions:
    - indicator: rsi
      period_minutes: 14
      operator: gt
      value: 75
exit:
  take_profit_pct: 0.8
  stop_loss_pct: 0.5
  timeout_minutes: 20
```

**Important:** RSI < 25 is rare — check that trade count stays above 350. If it drops
below 350, loosen to RSI < 28 for longs, RSI > 72 for shorts.

**In Extreme Fear regime (current):** RSI < 25 on a 5-min chart during fear conditions
often signals a local capitulation bottom — high probability snap-back within 15–20 min.
This is one of the highest-probability setups available right now.

---

### PRIORITY 4: Breakout Style (Generations 251–265)

Price breakout above recent high with volume confirmation. Captures momentum breakouts
which are common in high-volatility regimes (VIX 26+).

**Target configuration:**
```yaml
entry:
  long:
    conditions:
    - indicator: price_vs_high
      period_minutes: 60
      operator: breakout_above
    - indicator: volume
      operator: gt
      value: 1.5x_avg
  short:
    conditions:
    - indicator: price_vs_low
      period_minutes: 60
      operator: breakout_below
    - indicator: volume
      operator: gt
      value: 1.5x_avg
exit:
  take_profit_pct: 1.2
  stop_loss_pct: 0.6
  timeout_minutes: 30
```

**Note:** Breakouts often generate fewer signals. If trade count drops below 350,
reduce period_minutes to 30 or remove the volume condition.

---

### PRIORITY 5: Trend Continuation Multi-Timeframe (Generations 266–280)

Align 60-min and 15-min trend, enter on RSI momentum confirmation. Higher conviction
entries but fewer of them — only viable if TP is wide enough.

**Target configuration:**
```yaml
entry:
  long:
    conditions:
    - indicator: trend
      period_minutes: 60
      operator: eq
      value: up
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: up
    - indicator: rsi
      period_minutes: 10
      operator: gt
      value: 50
  short:
    conditions:
    - indicator: trend
      period_minutes: 60
      operator: eq
      value: down
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: down
    - indicator: rsi
      period_minutes: 10
      operator: lt
      value: 50
exit:
  take_profit_pct: 2.0
  stop_loss_pct: 1.0
  timeout_minutes: 45
```

**Warning:** This 3-condition entry will reduce trade count. Only accept if trades ≥ 350.
The wide TP (2.0%) compensates for lower win rate: R:R = 2.0x, breakeven = 35% WR.

---

## Macro Environment Adaptation

**Current Regime: DANGER — Extreme Fear (F&G = 11), VIX 26.86**

This is not purely a risk-off signal. High volatility creates opportunity:
- Intraday price swings are LARGER → TP targets hit more often
- Mean reversion snaps are MORE violent → deep RSI setups work better
- Breakouts are MORE decisive → breakout entries have cleaner follow-through

**Regime adaptations:**
- SHORT bias: in Extreme Fear, short setups have historically higher win rates
- For asymmetric testing, try short-only versions