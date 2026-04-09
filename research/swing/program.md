```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 14874 | Incumbent: Gen 14873 (Sharpe=1.1062)
# MIMIR-reviewed 2026-04-09 (v13)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — MOMENTUM PHASE (8 improvements in 2,149 gens)
# Sharpe has climbed from 0.0799 → 1.1062 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE. Continue mutating.
# ══════════════════════════════════════════════════════════════════════

## RESEARCH SCOPE
League: swing | Timeframe: 1h candles | Data: 2yr Binance OHLCV
Allowed pairs: BTC/USD, ETH/USD, SOL/USD (enforced in code)
Trade frequency target: 30–60 trades over 2yr backtest window
Min trades: SWING_MIN_TRADES=30 (immutable code constant)
Max trades: SWING_MAX_TRADES=60 (hard rejection in code)

## ══════════════════════════════════════════════════════════════════════
## CURRENT INCUMBENT — THIS IS THE ONLY YAML YOU MAY MUTATE
## DO NOT USE ANY PREVIOUS VERSION. THIS IS THE ONLY VALID BASE.
## ══════════════════════════════════════════════════════════════════════

```yaml
name: random_restart_v3_tightened_sl_v3
style: randomly generated
pairs:
- BTC/USD
position:
  size_pct: 25.0
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
  take_profit_pct: 7.38
  stop_loss_pct: 1.5
  timeout_hours: 138
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

Sharpe: 1.1062 | Trades: 59 | Win rate: 39.0%
⚠️ NOTE: size_pct has been corrected from 25.87% to 25.0% to comply
with DANGER regime directive (max 25%). Do not set size_pct > 25.0%.

All-time benchmark (lost): Gen 2126, Sharpe=2.9232, trades=30
The benchmark used RSI+MACD+EMA. The current incumbent uses
Bollinger+MACD+momentum_accelerating. Both are valid search paths.
The incumbent's path is CONFIRMED WORKING — stay on it.

## ══════════════════════════════════════════════════════════════════════
## CRITICAL INSTRUCTION — READ THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

You MUST propose exactly ONE small change to the CURRENT INCUMBENT YAML
above. Do NOT generate a new strategy from scratch. Do NOT change more
than one parameter at a time. Do NOT use any older YAML versions.

A "small change" means ONE of the following:
  (a) Change one numeric value (e.g., period_hours, take_profit_pct,
      stop_loss_pct, timeout_hours, size_pct)
  (b) Change one condition's operator or value
  (c) Replace one condition with a different indicator
  (d) Add one pair (ETH/USD or SOL/USD) alongside BTC/USD
  (e) Remove one condition (if currently 3 conditions)
  (f) Change one exit parameter

DO NOT: replace all conditions, change pairs and conditions
simultaneously, add more than one new condition, or generate a
completely different strategy.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CRITICAL CONSTRAINTS — DO NOT VIOLATE THESE
## ══════════════════════════════════════════════════════════════════════

### STOP LOSS IS AT THE FLOOR — DO NOT TOUCH IT
stop_loss_pct is currently 1.5%. This is the minimum allowed value.
DO NOT decrease stop_loss_pct. DO NOT set it below 1.5%.
If you change stop_loss_pct, you MUST increase it (e.g., 1.8, 2.0, 2.5).

### TRADE COUNT IS NEAR THE CEILING — BE CAREFUL
The incumbent has 59 trades — just 1 away from the hard rejection
ceiling of 60. Any change that loosens conditions or tightens exits
may push trades over 60 and cause [max_trades_reject].
SAFE mutations that are unlikely to increase trade count:
  - Increasing take_profit_pct (winners exit slower → fewer trades/time)
  - Increasing stop_loss_pct slightly (fewer stops hit → slightly fewer)
  - Increasing period_hours on any indicator (longer lookback = fewer signals)
  - Increasing timeout_hours (let trades run longer)
RISKY mutations (may increase trades → rejection):
  - Decreasing any period_hours
  - Loosening any operator threshold
  - Removing a condition
  - Adding a second pair

### SIZE_PCT CAP
Do NOT set size_pct > 25.0%. DANGER regime directive is active.
Minimum size_pct is 10.0%.

### DO NOT ADD A 4TH CONDITION
The incumbent has 3 conditions per side. Adding a 4th will likely
drop trade count to 0 → [low_trades] rejection.

## WHY THIS MATTERS — TRADE COUNT CONSTRAINT

The 30–60 trade window is NARROW (~1.4–2.5 trades/month over 2 years).
- Too many conditions → 0 trades → [low_trades] rejection
- Too few conditions / loose thresholds → >60 trades → [max_trades_reject]
- The incumbent hits 59 trades with 3 conditions. This is at the top
  of the valid zone. Prefer mutations that hold or reduce trade count.

## ══════════════════════════════════════════════════════════════════════
## RESEARCH DIRECTION (v13)
## ══════════════════════════════════════════════════════════════════════

### CONTEXT: WHERE WE ARE
The strategy has a clear identity: low win rate (39%), asymmetric payoff.
- SL = 1.5% (floor — do not reduce further)
- TP = 7.38% → reward:risk ratio ≈ 4.9:1
- This structure works. The goal now is to improve TP or signal quality.

### PATH A — REFINE THE INCUMBENT (PRIMARY, ACTIVE)

**PRIORITY 1: INCREASE take_profit_pct (HIGHEST EXPECTED VALUE)**
The most promising mutation right now. The SL floor is reached;
the remaining asymmetry lever is letting winners run further.
  - Try take_profit_pct: 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0
  - Each test should be ONE value only, not a range
  - Higher TP means fewer trades close via TP → may slightly reduce
    trade count (good, since we are near the 60-trade ceiling)
  - Win rate will likely decrease further, but Sharpe may improve
    if the payoff ratio increases enough

**PRIORITY 2: ADJUST timeout_hours**
Current value is 138h. This has not been varied recently.
  - Try timeout_hours: 168 (1 week) — let trades breathe longer
  - Try timeout_hours: 96 (4 days) — close stale trades faster
  - Try timeout_hours: 120 — midpoint test
  - Longer timeout = fewer trades close via timeout → may reduce count

**PRIORITY 3: ADJUST MACD PERIOD ON LONG SIDE**
  - Try macd_signal period_hours: 24 on long (currently 48)
  - Try macd_signal period_hours: 72 on long (currently 48)
  - Asymmetric MACD periods (long vs short) may improve signal quality

**PRIORITY 4: ADJUST BOLLINGER PERIOD**
  - Try bollinger_position period_hours: 72 on long (currently 48)
  - Try bollinger_position period_hours: 96 on long (currently 48)
  - Longer period = fewer Bollinger signals = likely fewer trades
    (beneficial given we are near the 60-trade ceiling)

**PRIORITY 5: REPLACE momentum_accelerating WITH RSI**
  - If take_profit and timeout tuning stall for 100+ gens, try:
    Long: replace momentum_accelerating=false with
      indicator: rsi, period_hours: 48, operator: lt, value: 35
    Short: replace momentum_accelerating=false with
      indicator: rsi, period_hours: 48, operator: gt, value: 65
  - RSI is more predictable and interpretable than momentum_accelerating
  - Do NOT change any other conditions when making this swap

**PRIORITY 6: SLIGHT size_pct INCREASE (MINOR)**
  - size_pct is at 25.0% (DANGER cap). Do not increase above 25.0%.
  - If regime improves (F&G > 30, regime exits DANGER), this lever opens.
  - Do not touch size_pct until macro regime improves.

### PATH B — RSI+MACD+EMA RECONSTRUCTION (SECONDARY)
Only attempt if PATH A stalls for 300+ consecutive gens with 0 improvements.
The all-time benchmark (Sharpe=2.9232) used this combination.
Template:
  Long: RSI < 35, MACD bullish, price > EMA(period=50)
  Short: RSI > 65, MACD bearish, price < EMA(period=50)
  Exit: TP=6–8%, SL=2–3%, timeout=168–240h
  Pairs: BTC/USD only first, then consider ETH/USD
Note: This represents a full indicator swap, not a mutation. Use only
as a reset if the incumbent is definitively stuck.

## ══════════════════════════════════════════════════════════════════════
## WHAT HAS FAILED — DO NOT REPEAT
## ══════════════════════════════════════════════════════════════════════

1. DO NOT generate strategies with 0 or 1 conditions per side.
   These produce >60 trades every time. [max_trades_reject]

2. DO NOT combine multiple boolean eq/neq conditions on exotic
   indicators. Collapses signal count to near zero. [low_trades]

3. DO NOT change pairs to anything outside BTC/USD, ETH/USD, SOL/USD.
   Hard rejection in code.

4. DO NOT propose size_pct > 25.0% (DANGER regime cap) or < 10%.

5. DO NOT set timeout_hours < 48 or > 300.

6. DO NOT add a 4th condition. Will likely produce [low_trades].

7. DO NOT propose RSI thresholds looser than: long < 45, short > 55.
   Loose RSI → too many trades → [max_trades_reject].

8. DO NOT set take_profit_pct < 4% or stop_loss_pct < 1.5%.
   Very tight exits increase trade count significantly.

9. ⚠️ NEW: DO NOT set stop_loss_pct below 1.5%. It is already at the
   floor. Reducing it further violates hard constraints AND will
   increase trade count dangerously close to the 60-trade ceiling.

10. ⚠️ NEW: DO NOT reproduce near-identical variants of Sharpe≈1.058
    (57 trades). These have been seen in gens 14855, 14857, 14861–14863,
    14867–14868. They represent a local plateau below the current best.
    The current best is Sharpe=1.1062 at 59 trades. Mutate FROM THAT.

11. ⚠️ NEW: DO NOT use the old incumbent (Sharpe=0.0799, size_pct=20,
    SL=3.2%, TP=9.6%). That YAML is obsolete. The current best YAML
    is the one printed above this section.

## ══════════════════════════════════════════════════════════════════════
## MACRO ENVIRONMENT AWARENESS (as of 2026-04-09)
## ══════════════════════════════════════════════════════════════════════

Current Regime: DANGER | Fear & Greed: 14 (Extreme Fear)
BTC Dominance: 57.0% (elevated — BTC outperforming alts)
VIX: 25.78 (elevated volatility)

Implications for strategy direction:
- BTC/USD is the safest pair to trade in this regime (high dominance)
- Do NOT add SOL/USD while F&G < 20 and regime = DANGER
- ETH/USD is acceptable as a secondary pair but adds trade count risk
  (we are already at 59 trades — adding a second pair likely pushes
  over 60 → [max_trades_reject] unless conditions are tightened first)
- DANGER directive: position size ≤ 25% — incumbent is compliant
- Extreme Fear favors LONG entries after capitulation:
  (Bollinger below_lower + oversold = good combo in fear regimes ✓)
- SHORT entries may underperform in fear regimes (fear already priced in)
  Consider stricter short conditions if win rate on shorts is poor

## ══════════════════════════════════════════════════════════════════════
## IMPROVEMENT LOGIC
## ══════════════════════════════════════════════════════════════════════
- Compare candidates on raw Sharpe only (no adj_score weighting)
- Reject if trades > 60 (MAX_TRADES) or < 30 (MIN_TRADES)
- Reject if any pair not in {BTC/USD, ETH/USD, SOL/USD}
- Reject duplicates (MD5 hash dedup cache)
- Suspicious filter: SUSPICIOUS_SHARPE=3.5, SUSPICIOUS_WINRATE=90.0%

## ══════════════════════════════════════════════════════════════════════
## GENERATION HEALTH TARGETS (next 100 gens)
## ══════════════════════════════════════════════════════════════════════
- Target: ≥ 3 new_best events (current pace: 8 in 2,149 gens)
- Target: < 50% of gens ending in [low_trades] or [max_trades_reject]
- Target: Sharpe > 1.3 within 200 gens
- Red flag: if >80% of gens are binary failures (0 trades or >60 trades),
  the LLM is generating fresh configs, not mutations — escalate to MIMIR
- If after 300 gens there are 0 new_best events from PATH A:
  trigger PATH B (RSI+MACD+EMA reconstruction)
- YAML of best strategy must be committed to git after EVERY new_best
  event. The Gen 2126 loss must not be repeated. This is mandatory.

## ══════════════════════════════════════════════════════════════════════
## IMPROVEMENT TRAJECTORY (for context)
## ══════════════════════════════════════════════════════════════════════
Gen 14738: Sharpe=0.0799  trades=52  win=44.2%  ← old program baseline
Gen 14740: Sharpe=0.2827  trades=52  win=44.2%
Gen 14746: Sharpe=0.4823  trades=55  win=41.8%
Gen 14749: Sharpe=0.5902  trades=55  win=41.8%
Gen 14751: Sharpe=0.7714  trades=53  win=47.2%
Gen 14759: Sharpe=1.0165  trades=56  win=44.6%
Gen 14784: Sharpe=1.0642  trades=56  win=44.6%
Gen 14873: Sharpe=1.1062  trades=59  win=39.0%  ← CURRENT BEST

Pattern: SL tightening drove early gains. TP and period tuning
drove later gains. Win rate is declining (44% → 39%) but Sharpe
is rising — asymmetric payoff is working. Next lever: TP increase.

## ══════════════════════════════════════════════════════════════════════
## LIVE COMPETITION CONTEXT
## ══════════════════════════════════════════════════════════════════════
AutoBotSwing recent: rank 3/10 both sprints (+4.97%, +3.21%)
Live win rates (50–67%) exceed backtest win rate (39%) — healthy sign,
no evidence of overfitting. Strategy is underperforming in ranking
likely due to position sizing or absolute PnL vs. competitors.
A Sharpe improvement from 1.1 toward 1.5+ should translate to
more consistent top-2 finishes.
Live trades: 3–4 per sprint ✓ (consistent with 59/2yr cadence)

## ══════════════════════════════════════════════════════════════════════
## NOTES FOR NEXT MIMIR REVIEW
## ══════════════════════════════════════════════════════════════════════
- If Sharpe reaches 1.5: review whether ETH/USD expansion is safe,
  but only if trade count drops below 55 (buffer needed for 2nd pair)
- If Sharpe reaches 2.0: consider relaxing MAX_TRADES to 80 and
  review whether size_pct can increase if macro regime improves
- If 300 more gens pass with < 2 improvements from PATH A:
  escalate to PATH B (RSI+MACD+EMA) or full program redesign
- Monitor win rate: if it drops below 30%, the SL at 1.5% may be
  too tight and causing premature exits on valid setups. If so,
  consider testing SL=1.8% or SL=2.0% as a corrective measure.
- size_pct correction: the previous best had size_pct=25.87% which
  violated the DANGER cap. Corrected to 25.0% in this program.
  If this correction causes a Sharpe discrepancy in backtest,
  flag to MIMIR for resolution.
- The LLM cluster problem (Sharpe≈1.058 plateau at gens 14855–14868)
  is addressed by explicit "DO NOT REPEAT" instructions above and
  by updating the incumbent YAML. Monitor whether clustering recurs.
- YAML of best strategy must be committed to git. Verify this happened
  for Gen 14873. Do not allow another Gen 2126 loss event.
```