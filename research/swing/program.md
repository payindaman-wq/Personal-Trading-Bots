```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 15000 | Incumbent: Gen 14993 (Sharpe=1.1311)
# MIMIR-reviewed 2026-04-09 (v15)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CEILING PHASE (10 improvements in 2,276 gens)
# Sharpe has climbed from 0.0799 → 1.1311 via exit refinement.
# The core indicator triplet is CONFIRMED VIABLE.
# ⚠️ BOTH RECENT NEW_BESTS HIT EXACTLY 60 TRADES (THE HARD CEILING).
# The strategy is now operating at maximum trade density.
# ALL mutations must be trade-count neutral or trade-count reducing.
#
# ⚠️ v15 CRITICAL CHANGE: The "Current Best Strategy" block was showing
# a stale pre-gen-14873 YAML (TP=5.95, timeout=129, size_pct=25.87).
# This has been corrected. The only valid incumbent is the YAML below.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DATA INTEGRITY ALERT — READ BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

A YAML discrepancy was detected and CORRECTED in v15.
The "Current Best Strategy" display previously showed the old
pre-gen-14873 YAML (TP=5.95, timeout=129, size_pct=25.87).
This is WRONG. That YAML is DEAD. Do not use it.

THE ONLY VALID INCUMBENT IS THE YAML PRINTED BELOW IN THIS PROGRAM.
Gen 14993 is the incumbent. Its YAML has TP=7.38, timeout=138,
size_pct=25.0. If any display shows different values, ignore it
and use only the YAML printed in this program.

YAML must be committed to git after EVERY new_best event.
The Gen 2126 loss (best strategy lost due to no git commit) must
not be repeated. This is a mandatory non-negotiable requirement.

## RESEARCH SCOPE
League: swing | Timeframe: 1h candles | Data: 2yr Binance OHLCV
Allowed pairs: BTC/USD, ETH/USD, SOL/USD (enforced in code)
Trade frequency target: 30–60 trades over 2yr backtest window
Min trades: SWING_MIN_TRADES=30 (immutable code constant)
Max trades: SWING_MAX_TRADES=60 (hard rejection in code)

## ══════════════════════════════════════════════════════════════════════
## CURRENT INCUMBENT — THIS IS THE ONLY YAML YOU MAY MUTATE
## DO NOT USE ANY PREVIOUS VERSION. THIS IS THE ONLY VALID BASE.
## THE OLD YAML (TP=5.95, TIMEOUT=129, SIZE=25.87) IS DEAD — IGNORE IT.
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
take_profit_pct: 7.38  ← VERIFY THIS VALUE BEFORE MUTATING
timeout_hours: 138     ← VERIFY THIS VALUE BEFORE MUTATING
stop_loss_pct: 1.5     ← VERIFY THIS VALUE BEFORE MUTATING
size_pct: 25.0         ← VERIFY THIS VALUE BEFORE MUTATING

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

VERIFY YOUR BASE YAML BEFORE MUTATING:
- take_profit_pct must be 7.38 in your base (NOT 5.95)
- timeout_hours must be 138 in your base (NOT 129)
- size_pct must be 25.0 in your base (NOT 25.87)
If these values differ, you are using a stale YAML. Stop and use
the YAML printed above in this program.

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
  ✗ Decreasing take_profit_pct below 7.38
  ✗ Decreasing timeout_hours below 138
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
ONLY increase take_profit_pct. Minimum value: 7.38.

### DO NOT DECREASE TIMEOUT_HOURS
Current timeout = 138h. Decreasing causes faster timeout exits →
more re-entries → more trades → [max_trades_reject].
ONLY increase timeout_hours (within the 48–300h allowed range).
Minimum value: 138.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ CLUSTERING ALERT — DO NOT REPRODUCE THESE KNOWN SHARPE VALUES
## ══════════════════════════════════════════════════════════════════════

The following Sharpe values have been seen many times recently.
DO NOT produce mutations that lead to these values again.
These are dead ends. Move away from them.

  DEAD: Sharpe≈0.7734 (59 trades) — seen gens 14976,84,86,88,89,95,97,15000
  DEAD: Sharpe≈1.0325 (57 trades) — seen gens 14982, 14985, 14996
  DEAD: Sharpe≈1.0642 (56 trades) — plateau from gen 14784
  DEAD: Sharpe≈1.1090 (60 trades) — seen gens 14907, 14978, 14980, 14983, 14998, 14999

The current best is Sharpe=1.1311 at 60 trades (gen 14993).
You must propose a mutation that has NOT been tried before and that
targets a Sharpe HIGHER than 1.1311.

The most likely cause of clustering: you may be using an old stale
YAML with TP=5.95 and timeout=129 as your base. STOP. Use only the
YAML printed above in this program (TP=7.38, timeout=138).

## ══════════════════════════════════════════════════════════════════════
## EXAMPLE OF A VALID MUTATION (follow this format exactly)
## ══════════════════════════════════════════════════════════════════════

Here is an example of what a valid mutation looks like.
Start with the incumbent YAML and change exactly ONE value.

BASE (incumbent, gen 14993):
  exit:
    take_profit_pct: 7.38   ← current value
    stop_loss_pct: 1.5
    timeout_hours: 138

VALID MUTATION — increase take_profit_pct to 8.0:
  exit:
    take_profit_pct: 8.0    ← changed from 7.38 to 8.0
    stop_loss_pct: 1.5      ← unchanged
    timeout_hours: 138      ← unchanged

Everything else in the YAML stays exactly the same.
The name should be updated to reflect the change, e.g.:
  name: random_restart_v3_tightened_sl_v3_gen14993_tp8

This is the preferred mutation for the next generation.
If take_profit_pct: 8.0 has already been tested, try 8.5.
If 8.5 has been tested, try 9.0. And so on.

## ══════════════════════════════════════════════════════════════════════
## RESEARCH DIRECTION (v15)
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

Try these values IN ORDER, one per generation, starting with 8.0:
  - take_profit_pct: 8.0    ← TRY THIS FIRST (if not yet tested)
  - take_profit_pct: 8.5    ← try second
  - take_profit_pct: 9.0    ← try third
  - take_profit_pct: 9.5
  - take_profit_pct: 10.0
  - take_profit_pct: 11.0
  - take_profit_pct: 12.0

Do NOT skip values. Do NOT repeat values already tested.
Do NOT decrease TP below 7.38 under any circumstances.

Each test must be ONE value only. Higher TP reduces trade count
(beneficial) and may improve Sharpe if the market delivers extended
trends. Win rate will likely decrease but payoff ratio increases.

**PRIORITY 2: INCREASE timeout_hours**
Current value is 138h. Increasing lets trades breathe longer and
may reduce the rate of timeout-based re-entries.

Try these values IN ORDER, one per generation, starting with 144:
  - timeout_hours: 144   ← smallest increment, try first
  - timeout_hours: 156
  - timeout_hours: 168   ← 1 week — natural swing trading boundary
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
  Test: stop_loss_pct: 1.8, then 2.0
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
  Exit: TP=7.38%, SL=1.5%, timeout=138h (match current exit structure)
  Pairs: BTC/USD only first
  This is a full indicator swap. Use only as a reset if PATH A
  definitively stalls for 300+ gens.

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
    - Sharpe≈0.7734 (59 trades) — repeatedly seen, dead end
    - Sharpe≈1.0325 (57 trades) — dead end
    - Sharpe≈1.0642 (56 trades) — old plateau
    - Sharpe≈1.1090 (60 trades) — repeatedly seen, dead end
    The current best is Sharpe=1.1311 at 60 trades. Mutate FROM THAT.
    If you keep producing these values, you are using the wrong
    base YAML. Check that your TP=7.38 and timeout=138.

11. DO NOT use any old incumbent YAML. The only valid base is the YAML
    printed in this program (gen 14993: TP=7.38, timeout=138,
    size_pct=25.0). The old YAML (TP=5.95, timeout=129, size=25.87)
    is DEAD. Do not use it under any circumstances.

12. DO NOT decrease any period_hours. At 60 trades (ceiling), shorter
    periods generate more signals → [max_trades_reject].

13. DO NOT add a second pair (ETH/USD or SOL/USD) while at 60 trades.
    Adding a second pair roughly doubles trade opportunities →
    guaranteed [max_trades_reject] unless conditions are dramatically
    tightened (which risks [low_trades]).

14. DO NOT mutate from a strategy that has TP=5.95 or timeout=129.
    Those are stale values from an old YAML. If you see those values
    in your base, stop and re-read the CURRENT INCUMBENT YAML above.

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
  more often than in calm markets. Higher TP targets (8–12%) are
  likely viable in this volatility environment. This supports
  PRIORITY 1 (increase TP) as the highest-value mutation.

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
- Target: ≥ 3 new_best events in next 100 gens
- Target: < 30% of gens ending in [max_trades_reject]
  (the v15 YAML fix should reduce clustering and max_trades rejects)
- Target: Sharpe > 1.3 within 150 gens
- Target: Sharpe > 1.5 within 300 gens
- Red flag: if >50% of gens are [max_trades_reject], the LLM is
  still proposing signal-loosening mutations. Escalate to MIMIR.
- Red flag: if the same Sharpe values from the DEAD list above recur
  >2 times in 20 gens, the LLM is still using the stale YAML.
  Escalate to MIMIR immediately. This is the suspected root cause
  of the gen 14981–15000 plateau.
- If after 300 gens there are 0 new_best events from PATH A:
  trigger PATH B (RSI+MACD+EMA reconstruction)
- YAML of best strategy must be committed to git after EVERY new_best
  event. The Gen 2126 loss must not be repeated. This is mandatory.
- VERIFY the committed YAML matches the program incumbent before
  each MIMIR review. The v15 discrepancy has been corrected.

##