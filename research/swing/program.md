```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 14993 | Incumbent: Gen 14993 (Sharpe=1.1311)
# MIMIR-reviewed 2026-04-09 (v14)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CEILING PHASE (10 improvements in 2,269 gens)
# Sharpe has climbed from 0.0799 → 1.1311 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ BOTH RECENT NEW_BESTS HIT EXACTLY 60 TRADES (THE HARD CEILING).
# The strategy is now operating at maximum trade density.
# ALL mutations must be trade-count neutral or trade-count reducing.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DATA INTEGRITY ALERT — READ BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

A YAML discrepancy was detected between the "Current Best Strategy"
display (which showed the old pre-gen-14873 YAML with TP=5.95,
timeout=129, size_pct=25.87) and the research program incumbent.

THE ONLY VALID INCUMBENT IS THE YAML PRINTED BELOW IN THIS PROGRAM.
Gen 14993 produced a new_best. That YAML MUST be committed to git.
Verify the committed YAML matches what is printed in this program.
If there is any doubt, re-run gen 14993 and re-commit.
The Gen 2126 loss must not be repeated.

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
name: random_restart_v3_tightened_sl_v3_gen14993
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

Sharpe: 1.1311 | Trades: 60 | Win rate: 41.7%
⚠️ NOTE: size_pct is 25.0% — at the DANGER regime cap. Do not exceed.
⚠️ NOTE: Trades = 60, which is the HARD CEILING. Any mutation that
increases signal frequency WILL be rejected [max_trades_reject].
Every mutation must be trade-count neutral or trade-count reducing.

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
## ⚠️ THE MOST IMPORTANT CONSTRAINT RIGHT NOW
## ══════════════════════════════════════════════════════════════════════

THE CURRENT STRATEGY HITS EXACTLY 60 TRADES — THE HARD CEILING.

This means:
  - ANY mutation that loosens entry conditions → [max_trades_reject]
  - ANY mutation that tightens exits (lower TP, lower SL, lower timeout)
    → more trades close sooner → more re-entries → [max_trades_reject]
  - ONLY mutations that reduce or maintain trade count are viable

SAFE mutations (trade-count neutral or reducing):
  ✓ Increasing take_profit_pct (winners hold longer → fewer closed)
  ✓ Increasing timeout_hours (trades hold longer → fewer re-entries)
  ✓ Increasing period_hours on any indicator (fewer signals generated)
  ✓ Slightly increasing stop_loss_pct (fewer stops triggered)
  ✓ Replacing momentum_accelerating with RSI (may reduce signal count)

DANGEROUS mutations (will likely cause [max_trades_reject]):
  ✗ Decreasing any period_hours
  ✗ Decreasing take_profit_pct
  ✗ Decreasing timeout_hours
  ✗ Removing any condition
  ✗ Adding a second pair
  ✗ Loosening any operator threshold

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CRITICAL CONSTRAINTS — DO NOT VIOLATE THESE
## ══════════════════════════════════════════════════════════════════════

### STOP LOSS IS AT THE FLOOR — DO NOT TOUCH IT (unless increasing)
stop_loss_pct is currently 1.5%. This is the minimum allowed value.
DO NOT decrease stop_loss_pct. DO NOT set it below 1.5%.
If you change stop_loss_pct, you MUST increase it (e.g., 1.8, 2.0, 2.5).

### TRADE COUNT IS AT THE CEILING — THIS IS THE PRIMARY CONSTRAINT
The incumbent has 60 trades — AT the hard rejection ceiling.
This is NOT "near" the ceiling. It IS the ceiling.
Any mutation that could increase trade count WILL be rejected.
Prefer mutations with high confidence of reducing trade count.

### SIZE_PCT CAP
Do NOT set size_pct > 25.0%. DANGER regime directive is active.
Minimum size_pct is 10.0%.

### DO NOT ADD A 4TH CONDITION
The incumbent has 3 conditions per side. Adding a 4th will likely
drop trade count to 0 → [low_trades] rejection.

### DO NOT DECREASE TAKE_PROFIT_PCT
Current TP = 7.38%. Decreasing it causes faster exits → more
re-entries → more trades → [max_trades_reject].
ONLY increase take_profit_pct.

### DO NOT DECREASE TIMEOUT_HOURS
Current timeout = 138h. Decreasing causes faster timeout exits →
more re-entries → more trades → [max_trades_reject].
ONLY increase timeout_hours (within the 48–300h allowed range).

## ══════════════════════════════════════════════════════════════════════
## RESEARCH DIRECTION (v14)
## ══════════════════════════════════════════════════════════════════════

### CONTEXT: WHERE WE ARE
The strategy has a clear identity: low win rate (41.7%), asymmetric payoff.
- SL = 1.5% (floor — do not reduce further)
- TP = 7.38% → reward:risk ratio ≈ 4.9:1
- Trades = 60 (AT THE HARD CEILING — this is the binding constraint)
- The goal is to let winners run further while reducing trade frequency

### PATH A — REFINE THE INCUMBENT (PRIMARY, ACTIVE)

**PRIORITY 1: INCREASE take_profit_pct (HIGHEST EXPECTED VALUE)**
The most promising mutation. Increasing TP does two things:
  1. Lets winners run to larger gains → higher Sharpe if captured
  2. Slows the rate at which trades close → may reduce trade count
     below 60, opening up further mutations

Specific values to test (one at a time):
  - take_profit_pct: 8.0   ← try this first
  - take_profit_pct: 8.5
  - take_profit_pct: 9.0
  - take_profit_pct: 9.5
  - take_profit_pct: 10.0
  - take_profit_pct: 11.0
  - take_profit_pct: 12.0

Each test should be ONE value only. Higher TP reduces trade count
(beneficial) and may improve Sharpe if the market delivers extended
trends. Win rate will likely decrease but payoff ratio increases.

**PRIORITY 2: INCREASE timeout_hours**
Current value is 138h. Increasing lets trades breathe longer and
may reduce the rate of timeout-based re-entries.
  - timeout_hours: 144  ← smallest increment, try first
  - timeout_hours: 156
  - timeout_hours: 168 (1 week) — natural swing trading boundary
  - timeout_hours: 192
  - timeout_hours: 216
  - timeout_hours: 240

DO NOT go below 138h (current value). That will increase trade count.
DO NOT go above 300h (program hard limit).

**PRIORITY 3: INCREASE BOLLINGER PERIOD ON LONG SIDE**
Longer lookback → fewer Bollinger signals → fewer long entries →
trade count may drop below 60 (creating room for further mutations).
  - bollinger_position period_hours: 72 (long side, currently 48)
  - bollinger_position period_hours: 96 (long side, currently 48)
  - bollinger_position period_hours: 120 (long side)

Do NOT change the short-side Bollinger (period_hours: 168 — already long).

**PRIORITY 4: INCREASE MOMENTUM_ACCELERATING PERIOD ON LONG SIDE**
  - momentum_accelerating period_hours: 72 (long side, currently 48)
  - momentum_accelerating period_hours: 96 (long side)
Longer period = fewer momentum signals = fewer entries = trade count
may drop below 60.

**PRIORITY 5: REPLACE momentum_accelerating WITH RSI**
If TP and timeout tuning stall for 100+ gens with no improvements:
  Long: replace momentum_accelerating=false with
    indicator: rsi, period_hours: 48, operator: lt, value: 35
  Short: replace momentum_accelerating=false with
    indicator: rsi, period_hours: 48, operator: gt, value: 65

RSI is more predictable. Tighter RSI thresholds (35/65) should
maintain or reduce trade count vs. the current setup.
DO NOT use looser thresholds (e.g., RSI < 45 or > 55) — too many trades.
DO NOT change any other conditions when making this swap.

**PRIORITY 6: SLIGHT stop_loss_pct INCREASE (MINOR)**
SL is at the floor (1.5%). A small increase may:
  - Reduce the number of stops triggered → slightly fewer trades
  - Improve win rate by giving trades more room
  Test: stop_loss_pct: 1.8, 2.0
  Risk: wider SL reduces per-trade risk-adjusted return.
  Only test if PRIORITY 1–5 all fail to produce improvements.

**PRIORITY 7: size_pct (DO NOT TOUCH IN DANGER REGIME)**
  size_pct is at 25.0% (DANGER cap). Do not increase above 25.0%.
  Do not touch until macro regime improves (F&G > 30).

### PATH B — RSI+MACD+EMA RECONSTRUCTION (SECONDARY)
Only attempt if PATH A stalls for 300+ consecutive gens with 0 improvements.
The all-time benchmark (Sharpe=2.9232) used this combination.
Template:
  Long: RSI < 35, MACD bullish, price > EMA(period=50)
  Short: RSI > 65, MACD bearish, price < EMA(period=50)
  Exit: TP=7–9%, SL=1.5–2.0%, timeout=168–240h
  Pairs: BTC/USD only first
  Start with TP=7.38% and timeout=138h to match current exit structure

Note: This represents a full indicator swap, not a mutation. Use only
as a reset if the incumbent is definitively stuck for 300+ gens.

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

5. DO NOT set timeout_hours < 138 (current value — decreasing will
   increase trade count and cause [max_trades_reject]).
   DO NOT set timeout_hours > 300 (program hard limit).

6. DO NOT add a 4th condition. Will likely produce [low_trades].

7. DO NOT propose RSI thresholds looser than: long < 40, short > 60.
   Loose RSI → too many trades → [max_trades_reject].
   Recommended thresholds: long < 35, short > 65.

8. DO NOT set take_profit_pct < 7.38% (current value — decreasing
   will increase trade count and cause [max_trades_reject]).
   Minimum TP: 7.38%. Only increase TP.

9. DO NOT set stop_loss_pct below 1.5%. It is at the floor.
   If changing SL, only increase it.

10. DO NOT reproduce near-identical variants of known plateau values:
    - Sharpe≈1.058 (57 trades) — seen gens 14855–14868, local plateau
    - Sharpe≈1.0325 (57 trades) — seen gens 14982, 14985
    - Sharpe≈0.7734 (59 trades) — seen gens 14976, 14984, 14986, 14988, 14989
    - Sharpe≈1.1090 (60 trades) — seen gens 14907, 14978, 14980, 14983
    The current best is Sharpe=1.1311 at 60 trades. Mutate FROM THAT.

11. DO NOT use any old incumbent YAML. The only valid base is the YAML
    printed in this program (gen 14993 incumbent).

12. DO NOT decrease any period_hours. At 60 trades (ceiling), shorter
    periods generate more signals → [max_trades_reject].

13. DO NOT add a second pair (ETH/USD or SOL/USD) while at 60 trades.
    Adding a second pair roughly doubles trade opportunities →
    guaranteed [max_trades_reject] unless conditions are dramatically
    tightened (which risks [low_trades]).

## ══════════════════════════════════════════════════════════════════════
## MACRO ENVIRONMENT AWARENESS (as of 2026-04-09)
## ══════════════════════════════════════════════════════════════════════

Current Regime: DANGER | Fear & Greed: 14 (Extreme Fear)
BTC Dominance: 57.0% (elevated — BTC outperforming alts)
VIX: 25.78 (elevated volatility)

Implications for strategy direction:
- BTC/USD is the safest pair. Stay BTC-only until regime improves.
- Do NOT add SOL/USD while F&G < 20 and regime = DANGER
- Do NOT add ETH/USD while trades = 60 (would push far over ceiling)
- DANGER directive: position size ≤ 25% — incumbent is compliant
- Extreme Fear favors LONG entries after capitulation:
  (Bollinger below_lower + oversold = good combo in fear regimes ✓)
- SHORT entries may underperform in fear regimes (fear already priced in)
  The asymmetric Bollinger period (short uses 168h vs long's 48h) may
  already be compensating for this — short signals are already rarer.
- Elevated VIX means wider price swings → TP=7.38% may be reachable
  more often than in calm markets. Higher TP targets (8–10%) may be
  viable in this environment.

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
- Target: ≥ 3 new_best events
- Target: < 40% of gens ending in [max_trades_reject]
  (currently too high — at 60 trades, almost any loosening is rejected)
- Target: Sharpe > 1.3 within 200 gens
- Target: Sharpe > 1.5 within 400 gens
- Red flag: if >60% of gens are [max_trades_reject], the LLM is
  proposing signal-loosening mutations despite explicit warnings.
  Escalate to MIMIR for prompt revision if this occurs.
- Red flag: if the same Sharpe values recur >3 times in 20 gens
  (clustering behavior), the LLM is not exploring — escalate to MIMIR.
- If after 300 gens there are 0 new_best events from PATH A:
  trigger PATH B (RSI+MACD+EMA reconstruction)
- YAML of best strategy must be committed to git after EVERY new_best
  event. The Gen 2126 loss must not be repeated. This is mandatory.
- VERIFY the committed YAML matches the program incumbent before
  each MIMIR review. A discrepancy was detected this cycle.

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
Gen 14873: Sharpe=1.1062  trades=59  win=39.0%
Gen 14907: Sharpe=1.1090  trades=60  win=40.0%
Gen 14993: Sharpe=1.1311  trades=60  win=41.7%  ← CURRENT BEST

Pattern: SL tightening drove early gains. TP and period tuning drove
later gains. Win rate declined (44% → 41.7%) but Sharpe rose —
asymmetric payoff is working. Trade count is now AT the ceiling (60).
The next lever is: let winners run further (higher TP) or let trades
breathe longer (higher timeout) to create room for further exploration.

## ══════════════════════════════════════════════════════════════════════
## LIVE COMPETITION CONTEXT
## ══════════════════════════════════════════════════════════════════════
AutoBotSwing recent: rank 3/10 both sprints (+4.97%, +3.21%)
Live win rates (50–67%) substantially exceed backtest win rate (41.7%)
— healthy sign, no evidence of overfitting.
Live trades: 3–4 per sprint ✓ (consistent with 60/2yr cadence)

Strategy underperforming in ranking likely due to absolute PnL vs.
competitors with higher-volatility pairs or larger position sizing.
A Sharpe improvement from 1.13 toward 1.5+ should translate to
more consistent top-2 finishes.

## ══════════════════════════════════════════════════════════════════════
## DATA REQUEST FOR NEXT MIMIR REVIEW
## ══════════════════════════════════════════════════════════════════════
To improve mutation guidance, ODIN should log the following for
each new_best event:
  - Exit type breakdown: % closed via TP vs. SL vs. timeout
  - Long vs. short trade split and separate win rates
  - Average holding time per trade

This data would reveal:
  - If timeout exits dominate → increasing TP won't help, need
    to increase timeout or accept the timeout exit as the primary exit
  - If SL exits dominate → SL at 1.5% may be too tight for current
    volatility; testing SL=1.8–2.0% may improve win rate
  - If long win rate >> short win rate → consider stricter short
    conditions to eliminate poor short trades

Without this data, mutations are partially blind. Escalate request
to LOKI/ODIN development if not currently logged.

## ══════════════════════════════════════════════════════════════════════
## NOTES FOR NEXT MIMIR REVIEW
## ══════════════════════════════════════════════════════════════════════
- YAML INTEGRITY: Verify gen 14993 YAML is correctly committed to git.
  The "Current Best Strategy" display showed an old pre-14873 YAML.
  This must be resolved before the next review.
- If Sharpe reaches 1.5 AND trade count drops below 55:
  review whether ETH/USD expansion is safe (need ≥5 trade buffer)
- If Sharpe reaches 2.0: consider relaxing MAX_TRADES to 80 and
  reviewing whether size_pct can increase if macro regime improves
- If 300 more gens pass with < 2 improvements from PATH A:
  escalate to PATH B (RSI+MACD+EMA reconstruction)
- Monitor win rate: if it drops below 30%, SL at 1.5% may be causing
  premature exits. Consider testing SL=1.8% or 2.0% as corrective.
- Monitor [max_trades_reject] rate: if >60% of gens are rejected for
  max trades, the LLM is not respecting the ceiling constraint.
  Consider adding explicit examples of REJECTED vs. ACCEPTED mutations
  in the next program revision.
- Clustering recurrence: gens 14974–14993 showed repeated identical
  Sharpe values (0.7734, 1.0325, 1.1090). The explicit DO NOT REPEAT
  list above should reduce this. Monitor carefully.
- size_pct: corrected from 25.87% to 25