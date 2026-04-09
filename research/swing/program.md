```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 14739 | Incumbent: Gen 14738 (Sharpe=0.0799)
# MIMIR-reviewed 2026-04-09 (v12)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — NORMAL OPERATION
# ══════════════════════════════════════════════════════════════════════

## RESEARCH SCOPE
League: swing | Timeframe: 1h candles | Data: 2yr Binance OHLCV
Allowed pairs: BTC/USD, ETH/USD, SOL/USD (enforced in code)
Trade frequency target: 30–60 trades over 2yr backtest window
Min trades: SWING_MIN_TRADES=30 (immutable code constant)
Max trades: SWING_MAX_TRADES=60 (hard rejection in code)

## CURRENT INCUMBENT — DO NOT LOSE THIS

```yaml
name: random_restart
style: randomly generated
pairs:
- BTC/USD
position:
  size_pct: 20
  max_open: 2
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 48
      operator: eq
      value: below_lower
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 168
      operator: eq
      value: above_upper
    - indicator: macd_signal
      period_hours: 24
      operator: eq
      value: bearish
exit:
  take_profit_pct: 9.6
  stop_loss_pct: 3.2
  timeout_hours: 138
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

Sharpe: 0.0799 | Trades: 52 | Win rate: 44.2%
All-time benchmark (lost): Gen 2126, Sharpe=2.9232, trades=30
The benchmark used RSI+MACD+EMA. The incumbent uses
Bollinger+MACD+momentum_accelerating. Both are valid search paths.

## ══════════════════════════════════════════════════════════════════════
## CRITICAL INSTRUCTION — READ THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

You MUST propose exactly ONE small change to the CURRENT INCUMBENT YAML
above. Do NOT generate a new strategy from scratch. Do NOT change more
than one parameter at a time.

A "small change" means ONE of the following:
  (a) Change one numeric value (e.g., period_hours, take_profit_pct,
      stop_loss_pct, timeout_hours, size_pct)
  (b) Change one condition's operator or value (e.g., rsi threshold)
  (c) Replace one condition with a different indicator
  (d) Add one pair (ETH/USD or SOL/USD) alongside BTC/USD
  (e) Remove one condition (if currently 3 conditions)
  (f) Change one exit parameter

DO NOT: replace all conditions, change pairs and conditions simultaneously,
add more than one new condition, or generate a completely different strategy.

## WHY THIS MATTERS — TRADE COUNT CONSTRAINT

The 30–60 trade window is NARROW (~1.4–2.5 trades/month over 2 years).
- Too many conditions → 0 trades → [low_trades] rejection
- Too few conditions / loose thresholds → >60 trades → [max_trades_reject]
- The incumbent hits 52 trades with 3 conditions. This is the right zone.

The LLM has generated 2,014 strategies. Only 1 passed. The search space
is not the problem — the problem is generating wholesale new configs
instead of mutating the incumbent. STAY CLOSE TO THE INCUMBENT.

## RESEARCH DIRECTION (v12)

### PATH A — REFINE THE INCUMBENT (PRIMARY)
The incumbent (Bollinger+MACD+momentum_accelerating) is producing
Sharpe=0.0799 at 52 trades. The win rate (44.2%) is below 50%, which
means most gains come from asymmetric payoff (TP=9.6% vs SL=3.2%).
To improve Sharpe, try these mutations ONE AT A TIME:

1. TIGHTEN EXIT ASYMMETRY
   - Increase take_profit_pct: try 10.0–12.0% (let winners run more)
   - Decrease stop_loss_pct: try 2.0–2.8% (cut losers faster)
   - Caution: tighter SL may increase trades (stops hit more often)
   
2. REPLACE momentum_accelerating WITH RSI
   - Try replacing momentum_accelerating=false with:
     indicator: rsi, period_hours: 48, operator: lt, value: 35 (long)
     indicator: rsi, period_hours: 48, operator: gt, value: 65 (short)
   - RSI is well-understood and more predictable for trade frequency

3. ADJUST BOLLINGER PERIOD
   - Try period_hours: 72 or 96 (longer = fewer signals = fewer trades)
   - The current 48h Bollinger may be too responsive

4. ADJUST MACD PERIOD
   - Try macd_signal period_hours: 24 or 72 on the long side
   - Asymmetric MACD periods on long vs short may improve signal quality

5. ADJUST TIMEOUT
   - Try timeout_hours: 168 (1 week) or 96 (4 days)
   - Current 138h is between these — test boundaries

6. ADD ETH/USD AS SECOND PAIR
   - Current strategy is BTC-only. Adding ETH/USD doubles opportunity
   - Risk: may push trades above 60 — test carefully
   - If ETH/USD pushes trades > 60, try SOL/USD instead

### PATH B — RSI+MACD+EMA RECONSTRUCTION (SECONDARY)
The all-time benchmark (Sharpe=2.9232) used this combination.
Only attempt this if incumbent mutations stall for 200+ gens.
Template:
  Long: RSI < 35, MACD bullish, price > EMA(period=50)
  Short: RSI > 65, MACD bearish, price < EMA(period=50)
  Exit: TP=6–8%, SL=2–3%, timeout=168–240h
  Pairs: BTC/USD only first, then add ETH/USD

## WHAT HAS FAILED — DO NOT REPEAT

1. DO NOT generate strategies with 0 conditions or 1 condition only.
   These produce >60 trades every time. [max_trades_reject]

2. DO NOT use highly exotic indicators with boolean outputs together.
   Combining multiple boolean eq/neq conditions collapses signal count
   to near zero. [low_trades]

3. DO NOT change pairs to anything outside BTC/USD, ETH/USD, SOL/USD.
   Hard rejection in code.

4. DO NOT propose size_pct > 25% or < 10%.

5. DO NOT set timeout_hours < 48 or > 300.

6. DO NOT add a 4th condition. Current 3 conditions already produce
   only 52 trades. A 4th condition will likely drop to 0. [low_trades]

7. DO NOT propose RSI thresholds looser than: long < 45, short > 55.
   Loose RSI is not selective enough → too many trades.

8. DO NOT set take_profit_pct < 4% or stop_loss_pct < 1.5%.
   Very tight exits increase trade count significantly.

## MACRO ENVIRONMENT AWARENESS (as of 2026-04-09)

Current Regime: DANGER | Fear & Greed: 14 (Extreme Fear)
BTC Dominance: 57.0% (elevated — BTC outperforming alts)

Implications for strategy direction:
- BTC/USD is the safest pair to trade in this regime (high dominance)
- Avoid adding SOL/USD as primary pair while F&G < 20
- ETH/USD is acceptable as a secondary pair
- The DANGER directive calls for position size ≤ 25% (already compliant
  at size_pct=20)
- Extreme Fear environments favor LONG entries after capitulation
  (Bollinger below_lower + RSI oversold = good combo in fear regimes)
- SHORT entries may underperform as fear-driven selling is already
  priced in; consider stricter short conditions

## IMPROVEMENT LOGIC
- Compare candidates on raw Sharpe only (no adj_score weighting)
- Reject if trades > 60 (MAX_TRADES) or < 30 (MIN_TRADES)
- Reject if any pair not in {BTC/USD, ETH/USD, SOL/USD}
- Reject duplicates (MD5 hash dedup cache)
- Suspicious filter: SUSPICIOUS_SHARPE=3.5, SUSPICIOUS_WINRATE=90.0%

## GENERATION HEALTH TARGETS (next 100 gens)
- Target: ≥ 5 new_best events (vs. 1 in last 2,014)
- Target: < 50% of gens ending in [low_trades] or [max_trades_reject]
- If after 200 gens there are 0 new_best events: trigger random restart
  using PATH B template above
- Red flag: if >80% of gens are binary failures (0 trades or >60 trades),
  the LLM is generating fresh configs, not mutations — escalate to MIMIR

## LIVE COMPETITION CONTEXT
AutoBotSwing recent: rank 3/10 both sprints (+4.97%, +3.21%)
This is acceptable but not top-tier. A Sharpe improvement from 0.0799
toward 0.5+ should translate to more consistent top-2 finishes.
Live trades: 3–4 per sprint (consistent with 30–60/2yr cadence ✓)

## NOTES FOR NEXT MIMIR REVIEW
- If Sharpe reaches 0.5: review whether multi-pair expansion is safe
- If Sharpe reaches 1.0: consider relaxing MAX_TRADES to 80
- If 500 more gens pass with <3 improvements: escalate to full program
  redesign — the current indicator set may not be backtest-profitable
  on BTC/ETH/SOL 1h data at this trade frequency
- YAML of best strategy must be committed to git after EVERY new_best
  event. The Gen 2126 loss must not be repeated.
```