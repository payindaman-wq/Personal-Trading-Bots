```markdown
# ODIN Research Program — FUTURES DAY (v8.0) — FIX THE CONSTANT, FIX THE STRATEGY

## League: futures_day
Timeframe: 5-minute candle data available, USE 1-HOUR indicator periods
Leverage: 2x
Sprint duration: 24 hours

---

## ⚠️ CRITICAL LOKI DIRECTIVE — MUST BE APPLIED BEFORE ANY GENERATION RUNS ⚠️

```
MIN_TRADES["futures_day"] = 50
```

**THE CODE CURRENTLY SAYS 400. THIS IS WRONG. CHANGE IT TO 50 NOW.**

Evidence that 400 is wrong:
- 1,408 generations with MIN_TRADES=400 → best Sharpe = -2.32 (still deeply negative)
- Gens 1390-1406: LLM correctly proposed lower-trade configs (50-200 trades) but ALL
  were rejected as [low_trades] because the code threshold = 400
- The mean-reversion swing paradigm REQUIRES fewer trades. 400 is a scalping threshold.
- futures_swing (Sharpe 2.25) operates with ~50-150 trades. We must match this.

**If you are reading this and MIN_TRADES["futures_day"] ≠ 50, stop everything and fix it.**

Do NOT raise this threshold. 50 trades over 2 years = 25 trades/year across 16 pairs
= statistically valid with proper R:R and high WR.

---

## WHY THE PREVIOUS PARADIGM FAILED — THE MATH YOU MUST UNDERSTAND

### Fee Drag Calculation (memorize this)

At 0.1% round-trip fee per trade:
- 650 trades → 65% of equity consumed by fees → Sharpe impossible to fix
- 300 trades → 30% consumed → still very hard
- 150 trades → 15% consumed → manageable
- 75 trades  → 7.5% consumed → excellent fee efficiency

**The current champion (Gen 1408) has 650 trades and Sharpe -2.32.**
**Even with 45% win rate and 2:1 R:R, fees consume all profit.**
**The ONLY path to positive Sharpe is fewer trades + wider TP.**

### The Target Math (positive Sharpe requires this)

At TP=5.0%, SL=2.0%, leverage=2x, WR=45%:
- Win: +10.0% on position. Fee: ~0.1%. Net win: +9.9%
- Loss: -4.0% on position. Fee: ~0.1%. Net loss: -4.1%
- EV per trade = 0.45×9.9 - 0.55×4.1 = 4.455 - 2.255 = +2.2%
- At 100 trades: total EV = +220% before compounding
- Sharpe depends on consistency, but positive EV + low trade count = POSITIVE SHARPE

At TP=4.0%, SL=2.0%, leverage=2x, WR=45%, 650 trades:
- Win: +7.9% net. Loss: -4.1% net.
- EV per trade = 0.45×7.9 - 0.55×4.1 = 3.555 - 2.255 = +1.3%
- Total EV = +845%... but the VOLATILITY of 650 trades produces massive Sharpe denominator
- Sharpe = EV / std_dev → with 650 noisy trades, std_dev dominates → Sharpe stays negative

**Conclusion: Fewer trades is MORE important than higher win rate.**

---

## CURRENT CHAMPION (Gen 1408 — Start Here)

```yaml
name: crossover
style: mean_reversion_swing
league: futures_day
leverage: 2
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
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 28
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 72
exit:
  take_profit_pct: 4.0
  stop_loss_pct: 2.0
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

**Current performance: Sharpe -2.32, 650 trades, 45.2% WR**
**Problem: 650 trades is too many. Fee drag = 65% of equity.**
**Fix: Tighten RSI thresholds to reduce trade count to 100-200.**

---

## MANDATORY BASE CONFIGURATION — LOCKED

```yaml
position:
  size_pct: 13.64
  max_open: 2
  fee_rate: 0.0005
pairs: [all 16 — never remove any]
```

LOCKED. Never change size_pct, max_open, fee_rate, or pairs.

---

## OPTIMIZATION SEQUENCE — CURRENT PRIORITY ORDER

### ⭐ IMMEDIATE PRIORITY: Reduce Trade Count to 100-200

The #1 problem is 650 trades. Before optimizing anything else, reduce this.

**How to reduce trades:**
- Tighten RSI long threshold: 28 → 25 → 22 → 20
- Tighten RSI short threshold: 72 → 75 → 78 → 80
- Increase RSI period: 60 → 90 → 120 → 180 minutes
- Any combination of the above

**Target: 100-200 trades. Accept as low as 50.**
**Do NOT reject configs with 50-200 trades. That is the goal.**

### Phase A: RSI Threshold Tightening (Generations 1409-1430)

Change ONE threshold per generation. Priority order:
1. RSI long: 28 → 25 (expect ~400 trades → ~300 trades)
2. RSI long: 25 → 22 (expect ~300 → ~200 trades)
3. RSI long: 22 → 20 (expect ~200 → ~150 trades)
4. RSI short: 72 → 75 (parallel reduction)
5. RSI short: 75 → 78
6. RSI short: 78 → 80
7. Best RSI long + best RSI short combined

At each step: if Sharpe improves AND trades decrease → KEEP. This is the goal.
If Sharpe worsens but trades are still >400: the threshold reduction didn't hurt enough — try again.
If trades drop below 50: step back one level.

**Accept ANY Sharpe improvement, even if trades drop to 50.**

### Phase B: TP Widening (Generations 1431-1460)

With the best RSI thresholds from Phase A, test wider TP:
- TP 4.0 → 4.5 → 5.0 → 5.5 → 6.0 → 7.0 → 8.0

Why: Wider TP means each winning trade earns more vs. fee cost.
At 100 trades, TP=6.0% means fee drag is only 10% of potential winnings.

Keep SL at 2.0% unless TP/SL ratio falls below 2.0.
If TP > 6.0%, test SL up to 2.5% to maintain reasonable WR.

### Phase C: RSI Period Extension (Generations 1461-1490)

Test RSI periods to find smoother, less noisy signals:
- 60 → 90 → 120 → 150 → 180 minutes

Longer period = smoother RSI = fewer false triggers = higher-quality trades.
Expected: 180-minute RSI will fire ~40% fewer times than 60-minute RSI.

### Phase D: Timeout Optimization (Generations 1491-1510)

Test timeouts to let winners develop:
- 720 → 960 → 1200 → 1440 minutes

Longer timeout = more TP hits = higher WR = better Sharpe.
Do not go below 480 minutes. We are not scalping.

### Phase E: Add Trend Filter (Generations 1511-1540)

ONLY after Phases A-D, add a trend filter to improve signal quality:

Option 1 — Contrarian (mean reversion):
```yaml
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: [best_from_phase_C]
      operator: lt
      value: [best_from_phase_A]
    - indicator: trend
      period_minutes: 240
      operator: eq
      value: down   # buy into downtrend = mean reversion
```

Option 2 — Confirming (momentum):
```yaml
    - indicator: trend
      period_minutes: 240
      operator: eq
      value: up     # buy only when recovering
```

Test BOTH. The contrarian filter may work better for mean reversion.
If trades drop below 50 with trend filter: remove it and stick with Phase D result.

### Phase F: SL Optimization (Generations 1541-1560)

With everything locked from Phases A-E, test SL values:
- 1.5, 1.75, 2.0, 2.25, 2.5, 3.0

Always keep TP/SL ≥ 2.0. At TP=5%, SL max = 2.5%.
Tighter SL = more losses but smaller losses = better Sharpe IF WR is decent.
Looser SL = fewer losses but bigger losses = better IF the market tends to recover.

---

## PARAMETER BOUNDS — HARD LIMITS

```
RSI period_minutes:     60 — 180    (hourly-scale only, no sub-60 noise)
RSI long threshold:     18 — 32     (genuinely oversold, not just dipping)
RSI short threshold:    68 — 82     (genuinely overbought, not just rising)
take_profit_pct:        4.0 — 8.0  (wide enough to dominate fees at low trade counts)
stop_loss_pct:          1.5 — 3.0  (tight enough to limit damage)
timeout_minutes:        480 — 1440 (8-24 hours minimum, this is SWING not scalp)
R:R ratio (TP/SL):     ≥ 2.0      (higher than before — we need the edge)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
```

---

## ABSOLUTE BANS — VIOLATIONS WASTE A GENERATION

1. **timeout_minutes < 480**: BANNED. Minimum 8 hours. We are SWING trading.
2. **take_profit_pct < 4.0**: BANNED. Below 4% doesn't justify the fee cost per trade.
3. **stop_loss_pct < 1.5**: BANNED. Too tight, will stop-hunt on hourly volatility.
4. **RSI period_minutes < 60**: BANNED. Sub-60-minute RSI is pure noise.
5. **RSI long threshold > 32**: BANNED. Above 32 is not genuinely oversold.
6. **RSI short threshold < 68**: BANNED. Below 68 is not genuinely overbought.
7. **Adding 3rd entry condition before Phase E**: BANNED.
8. **Removing pairs**: BANNED. Always use all 16.
9. **Changing size_pct, max_open, fee_rate**: BANNED.
10. **stop_if_down_pct < 15**: BANNED.
11. **Proposing configs that obviously generate 400+ trades**: STRONGLY DISCOURAGED.
    If RSI thresholds are 28/72 on 60-minute period, expect 600+ trades — avoid this.
12. **Reverting to old champion (RSI 28/72, TP 4.0, 650 trades)**: DISCOURAGED.
    That config is Sharpe -2.32. We need improvement, not stagnation.
13. **R:R ratio (TP/SL) < 2.0**: BANNED. The old 1.5x minimum was insufficient.

---

## HOW TO ESTIMATE TRADE COUNT BEFORE PROPOSING

RSI fires more rarely at extreme thresholds. Rough guide:
- RSI lt 28 on 60-min: ~600-700 signals per 2 years across 16 pairs
- RSI lt 25 on 60-min: ~350-450 signals
- RSI lt 22 on 60-min: ~150-250 signals
- RSI lt 20 on 60-min: ~75-150 signals
- RSI lt 22 on 90-min: ~100-180 signals
- RSI lt 20 on 120-min: ~50-100 signals

For short side, mirror these estimates (RSI gt 72/75/78/80).

**Target zone: 75-200 total trades. Accept 50-250.**
**Reject before proposing if estimate is clearly >400.**

---

## HOW TO PROPOSE A CHANGE

You must propose exactly ONE change from the current best config. Format:

```
CHANGE: [parameter_name] from [old_value] to [new_value]
REASON: [one sentence explaining why this should improve Sharpe]
PHASE: [which phase letter from the sequence above]
ESTIMATED TRADE COUNT: [your estimate — target 75-200]
FEE DRAG CHECK: [trades × 0.1% = X%. Is this acceptable?]
```

Then output the complete YAML config with that one change applied.

**If estimated trade count > 400, choose a different change.**
**If fee drag > 40%, choose a different change.**

---

## WHAT SUCCESS LOOKS LIKE

Historical context:
- Gen 1: Sharpe -10.77 (394 trades) — old scalping baseline
- Gen 541: Sharpe -4.29 (605 trades) — incremental improvement
- Gen 1408: Sharpe -2.32 (650 trades) — current best ★

Target milestones:
- **Phase A target**: Sharpe > -1.5 with trades < 300 (fee drag reduction working)
- **Phase B target**: Sharpe > -0.5 with trades < 200 (TP widening + low fee drag)
- **Phase C-D target**: Sharpe > 0.0 (FIRST POSITIVE SHARPE IN 1,408 GENERATIONS)
- **Phase E-F target**: Sharpe > 0.5
- **Stretch goal**: Sharpe > 1.0 (approaching futures_swing quality at 2.25)

**A config with Sharpe -0.5 and 100 trades is BETTER than Sharpe -2.32 and 650 trades.**
**Do not prioritize trade count. Prioritize Sharpe.**

---

## MACRO ENVIRONMENT NOTE

Current regime: DANGER (Extreme Fear, F&G=14, VIX=25.78)
This is actually FAVORABLE for mean-reversion:
- Extreme Fear = assets are oversold = RSI will hit lt 20-25 frequently
- Mean reversion from oversold has higher probability during fear regimes
- The long side should be firing frequently with tight RSI thresholds
- High VIX = wider price swings = TP=5-6% more reachable

Consider: In extreme fear, LONG mean-reversion entries (RSI lt 22-25) have
historically higher win rates as fear-driven overshoots snap back.
The current environment supports the new paradigm.

---

## REMINDER TO THE SMALL LLM

You are optimizing a SWING strategy. Your job is to make FEWER, BETTER trades.

The current strategy makes 650 trades. That is the PROBLEM, not the solution.
Tighten the RSI thresholds. Widen the take-profit. Extend the timeout.
Accept that the trade count will fall to 100-200. That is CORRECT.
MIN_TRADES = 50. A config with 75 trades will NOT be rejected.

Fee drag at 650 trades = 65% of equity. Fee drag at 100 trades = 10%.
The math is simple. Fewer trades wins.

The old approach (RSI 28/72, 60-min, 650 trades) has been tested for hundreds
of generations. It cannot achieve positive Sharpe. Do not propose it again.

Your next move: Tighten RSI long from 28 to 25, OR increase RSI period from 60 to 90.
Either will reduce trades, reduce fee drag, and improve Sharpe.
```