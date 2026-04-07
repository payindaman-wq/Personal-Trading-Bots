```markdown
# ODIN Research Program — FUTURES DAY

## League: futures_day
Timeframe: 5-minute candles, 24h sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (applied automatically in backtest)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage

---

## ⚠️ CRITICAL CONTEXT — READ FIRST

**The current best strategy has Sharpe = −10.31. This is FAILING, not succeeding.**
After 108 generations of small tweaks, the search is STUCK. The win rate is locked at
40–44% and the strategy is losing money on every cohort. You MUST propose structurally
different approaches — not minor RSI threshold adjustments.

**What has NOT worked (do not repeat these):**
- Tweaking RSI thresholds by ±2-3 points around 38/42 — exhausted, no improvement
- Adjusting timeout_minutes by small amounts — no consistent improvement
- Tightening/loosening stop_loss_pct by 0.1-0.2% alone — not sufficient
- Adding more pairs without changing entry logic — does not help

**The entry logic (trend + RSI pullback) is not generating edge at current thresholds.**
You must either fix the thresholds dramatically or replace the logic entirely.

---

## Research Objective

Evolve strategies that are profitable NET of leverage costs and survive real futures
mechanics. Target: **Sharpe > 0 first, then Sharpe > 1.0, then Sharpe > 1.5**.

We are in ESCAPE MODE: the goal is to find ANY configuration that produces positive
Sharpe, even modestly. Prefer bold structural changes over conservative tweaks.

Leverage amplifies returns but also amplifies losses. Prefer strategies with:
- Tight stop losses (max 2% stop for day trading at 2x)
- High win rate OR strong R:R ratio (not both required, but one must compensate)
- Limited hold time to minimize funding drag (target: exits within 30-45 minutes)
- Breakeven analysis: with 0.1% round-trip fees + funding, need win_rate × avg_win >
  (1 - win_rate) × avg_loss. At 1.15% TP / 0.8% SL, breakeven win rate is ~43.5%.
  The current strategy achieves 43% — it is BELOW breakeven. Fix this math first.

---

## Macro Environment Warning

**Current regime: DANGER — Extreme Fear (F&G = 11)**
- Bias entries toward SHORT side in current market conditions
- Long entries require STRONGER confirmation than normal
- Consider adding a regime filter: only trade longs if recent 1h trend is up
- BTC dominance rising (56.6%) — altcoins underperforming, be cautious on alts

---

## Fix the Math First — Priority Changes

Before exploring new indicators, consider fixing the reward:risk imbalance:

**Option A: Improve R:R ratio**
- Increase take_profit_pct to 1.5–2.0% (current 1.15% is too tight for 2x leverage)
- Keep stop_loss_pct at 0.8% → R:R becomes 1.875–2.5x → breakeven drops to 29–35%
- Risk: fewer TP hits, lower trade count

**Option B: Improve win rate via better entry filters**
- Add volume confirmation: only enter if current volume > 1.5x average volume
- Add momentum confirmation: require price above/below recent pivot
- Tighten trend filter: use 5-min trend instead of 15-min for faster confirmation
- Use RSI divergence: RSI recovering from oversold (not just below threshold)

**Option C: Change the core entry logic entirely**
- Replace RSI pullback with: breakout above recent high (last 12 candles)
- Replace RSI pullback with: EMA crossover (fast EMA crosses above slow EMA)
- Replace RSI pullback with: VWAP reclaim (price crosses back above VWAP)
- Try pure mean-reversion: large RSI extreme (RSI < 25 long, RSI > 75 short) with
  tight stops, betting on snap-back within 20-30 minutes

---

## Structural Changes to Explore

### Entry Logic Alternatives (try ONE per generation)

**Breakout style:**
```
long:
  - indicator: price_vs_high, period_minutes: 60, operator: breakout_above
  - indicator: volume, operator: gt, value: 1.5x_avg
short:
  - indicator: price_vs_low, period_minutes: 60, operator: breakout_below
  - indicator: volume, operator: gt, value: 1.5x_avg
```

**EMA crossover style:**
```
long:
  - indicator: ema_cross, fast: 5, slow: 20, operator: crossed_above
  - indicator: trend, period_minutes: 30, operator: eq, value: up
short:
  - indicator: ema_cross, fast: 5, slow: 20, operator: crossed_below
  - indicator: trend, period_minutes: 30, operator: eq, value: down
```

**Deep mean-reversion style (high-conviction oversold/overbought):**
```
long:
  - indicator: rsi, period_minutes: 14, operator: lt, value: 25
  - indicator: rsi, period_minutes: 14, operator: recovering  # RSI rising
short:
  - indicator: rsi, period_minutes: 14, operator: gt, value: 75
  - indicator: rsi, period_minutes: 14, operator: falling
exit:
  take_profit_pct: 0.8   # quick scalp
  stop_loss_pct: 0.5     # very tight
  timeout_minutes: 20    # fast exit
```

**Trend-continuation style (higher timeframe aligned):**
```
long:
  - indicator: trend, period_minutes: 60, operator: eq, value: up   # 1h trend
  - indicator: trend, period_minutes: 15, operator: eq, value: up   # 15m trend
  - indicator: rsi, period_minutes: 10, operator: gt, value: 50     # momentum
short:
  - indicator: trend, period_minutes: 60, operator: eq, value: down
  - indicator: trend, period_minutes: 15, operator: eq, value: down
  - indicator: rsi, period_minutes: 10, operator: lt, value: 50
```

---

## Exit Strategy Guidance

The current exit (TP 1.15% / SL 0.8% / timeout 60min) is marginal. Consider:

- **Tighter scalp:** TP 0.7–0.9% / SL 0.4–0.5% / timeout 15–25 min
  → More trades, higher win rate needed, but funding cost minimized
- **Wider swing:** TP 2.0–3.0% / SL 1.0–1.5% / timeout 90–120 min
  → Fewer trades, lower win rate acceptable, but liquidation risk rises
- **Asymmetric:** TP 1.5% / SL 0.6% / timeout 45 min → R:R = 2.5x → need 29% WR
- **Current setup is the worst of both worlds** — wide enough to hit SL often,
  tight enough that TP is also frequently missed before timeout

---

## Position Sizing and Pairs

Current: 13.64% size, max_open=2, 16 pairs
- With max_open=2 across 16 pairs, most pairs sit idle — this is fine for safety
- In DANGER regime: consider reducing to 8 most liquid pairs (BTC, ETH, SOL, BNB,
  XRP, DOGE, AVAX, LINK) to concentrate signal quality
- Position size 13.64% at 2x = 27.28% effective exposure per trade — reasonable
- In Extreme Fear: consider reducing to 8–10% position size (effective 16–20%)

---

## What Success Looks Like

| Priority | Target | Notes |
|----------|--------|-------|
| Immediate | Sharpe > −5.0 | Meaningfully better than current −10.3 |
| Short-term | Sharpe > 0.0 | Break-even territory |
| Medium-term | Sharpe > 1.0 | Viable strategy |
| Goal | Sharpe > 1.5 | Competition-ready |

**Win rate targets by R:R:**
- R:R 1.0x (equal TP/SL): need >52% WR after fees
- R:R 1.44x (current 1.15/0.8): need >43.5% WR — current 43% is FAILING
- R:R 2.0x (e.g., 1.6/0.8): need >35% WR — much more achievable
- R:R 2.5x (e.g., 1.5/0.6): need >30% WR — easiest to achieve with tight SL

---

## Key Constraints

- MIN_TRADES: 250 (raised from 200 — strategies below this are statistically unreliable)
- Max stop loss: 2.0% (beyond this, 2x leverage creates liquidation cascade risk)
- Max hold time: 120 minutes (funding cost becomes significant beyond this)
- Leverage: fixed at 2x — do not propose leverage changes
- Fee rate: 0.0005 per side — always include in mental math

## Strategy Format

Propose ONE change per generation. State:
1. What you are changing and why
2. Which failure mode you are trying to fix (bad R:R, low win rate, wrong entry logic)
3. What result you expect (higher WR, better R:R, or more selective entries)

Do NOT make changes that:
- Adjust RSI thresholds by only 1-3 points without other changes
- Modify timeout by only 5-10 minutes without other changes
- Add a 4th condition that is highly correlated with existing conditions
- Reduce trade count below 250 (too few samples for reliable Sharpe)
```