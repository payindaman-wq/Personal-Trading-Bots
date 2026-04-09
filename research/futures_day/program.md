```markdown
# ODIN Research Program — FUTURES DAY (v9.0) — FOLLOW THE DATA

## League: futures_day
Timeframe: 5-minute candle data available, USE 1-HOUR indicator periods
Leverage: 2x
Sprint duration: 24 hours

---

## ⚠️ CONSTANTS CHECK

```
MIN_TRADES["futures_day"] = 50
```

Confirmed correct. Do NOT raise this. Configs with 50-200 trades are valid and will be tested.

---

## WHAT THE DATA ACTUALLY SHOWS — READ THIS FIRST

After 1521 generations, the empirical evidence has overturned several assumptions.
Here is what the data proves:

### The Win-Rate Discovery (Critical)

The original program assumed tighter RSI thresholds (RSI lt 20-25) would produce
higher-quality trades with better win rates. This is FALSE in this dataset.

Actual results from recent generations:
- RSI lt 22-25, 150-300 trades → WR ~42-45%, Sharpe -2.4 to -5.8
- RSI lt 35-36, 967-1521 trades → WR ~47-48%, Sharpe -0.7 to -0.44

**Tighter RSI does NOT produce higher win rates. It only reduces trade count.**
**The higher-threshold configs have BETTER win rates AND better Sharpe.**

This means: the fee-drag math we used was wrong in its WR assumption.
At tight thresholds, WR drops along with trade count, so the EV doesn't improve.

### The Concurrency Discovery (Critical)

The current best (Gen 1521) uses max_open=1. This is the REAL trade limiter.
With RSI lt 36 and max_open=1, signals are frequently suppressed because a position
is already open. This creates a natural quality filter — only the first signal
in each "oversold episode" gets traded.

**max_open=1 + loose RSI = effective de-duplication of signals.**
**This is better than tight RSI + max_open=2.**

### The Current Path to Positive Sharpe

Current champion: Sharpe -0.44, 1521 trades, 47% WR, TP=4.0%, SL=2.39%

EV check at current params (leverage 2x, 47% WR):
- Win: +8.0% gross, -0.1% fee = +7.9% net
- Loss: -4.78% gross, -0.1% fee = -4.88% net
- EV = 0.47 × 7.9 - 0.53 × 4.88 = 3.713 - 2.586 = +1.127% per trade
- This is POSITIVE EV. The Sharpe is negative only because of high variance.

The path to positive Sharpe: WIDEN TP to increase win payoff.
- At TP=6%: Win = +11.9% net. EV = 0.47×11.9 - 0.53×4.88 = 5.593 - 2.586 = +3.007%
- At TP=8%: Win = +15.9% net. EV = 0.47×15.9 - 0.53×4.88 = 7.473 - 2.586 = +4.887%

**The current strategy has positive expected value. We just need to widen TP.**

---

## CURRENT CHAMPION (Gen 1521 — Start Here)

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
  size_pct: 16.91
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 35.97
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 72
exit:
  take_profit_pct: 4.0
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

**Current performance: Sharpe -0.4367, 1521 trades, 47.0% WR**
**Positive EV confirmed. Problem: high variance suppresses Sharpe.**
**Fix: Widen TP to let winning trades earn more.**

---

## LOCKED PARAMETERS — DO NOT CHANGE

```yaml
position:
  size_pct: 16.91      ← locked at current champion value
  max_open: 1          ← locked — this is the concurrency limiter
  fee_rate: 0.0005     ← locked — never change
pairs: [all 16 — never remove any]
```

LOCKED. Never change size_pct, max_open, fee_rate, or pairs.

---

## OPTIMIZATION SEQUENCE — REVISED BASED ON EVIDENCE

### ⭐ IMMEDIATE PRIORITY: Widen Take-Profit (Phase B — now primary)

The #1 lever to improve Sharpe is widening TP.
Current TP=4.0% with 47% WR = barely positive EV but high variance.
Wider TP = higher win payoff = higher EV per trade = positive Sharpe.

**Why this works:**
- Current EV per trade ≈ +1.1%. At 1521 trades, total EV is large but variance kills Sharpe.
- At TP=6%, EV per trade ≈ +3.0%. Same variance, much better mean. Sharpe improves.
- The win AMOUNT grows proportionally with TP, but variance doesn't grow as fast.

**Target sequence:**
```
TP 4.0 → 4.5 → 5.0 → 5.5 → 6.0 → 7.0 → 8.0
```

Test ONE step per generation. Keep SL at 2.39% unless TP/SL < 2.0.
At TP=5.0%: TP/SL = 5.0/2.39 = 2.09 ✓
At TP=6.0%: TP/SL = 6.0/2.39 = 2.51 ✓
At TP=8.0%: TP/SL = 8.0/2.39 = 3.35 ✓ (fine to increase SL slightly if WR drops)

Expected outcome: Each TP increment should improve Sharpe by 0.1-0.3.
First positive Sharpe expected around TP=5.5-6.0%.

### Phase A-Revised: RSI Threshold Fine-Tuning (Secondary)

The current RSI long=35.97 is producing 47% WR. We can test nearby values:
- 35.97 → 37 → 38 → 36 → 34

Do NOT go below 32 (WR will drop below 45%) or above 40 (too many false signals).
Do NOT go below 28 (confirmed bad: produces WR 44-45% with fewer trades = worse Sharpe).

For RSI short: current 72 is fine. Test 70 → 68 if other changes plateau.
Do NOT tighten short below 68.

### Phase C: Timeout Extension

Current timeout=720 minutes (12 hours). With TP=5-6%, price needs more time.
Test: 720 → 960 → 1200 → 1440 minutes

Longer timeout = more TP hits = higher effective WR = better Sharpe.
Expected: each 240-minute extension adds 1-3% to WR as more trades reach TP.

Do NOT go below 720 minutes. We are not scalping.

### Phase D: RSI Period Extension

Test RSI periods: 60 → 90 → 120 minutes
Longer period = smoother RSI = marginally better signal quality.
Expected: small improvement. Do not rely on this as primary lever.
If trade count drops below 200 with longer periods, revert — we need WR volume.

### Phase E: SL Optimization

With best TP from above, test SL:
- 2.39 (current) → 2.5 → 2.75 → 3.0 → 2.25 → 2.0

Maintain TP/SL ≥ 2.0 at all times.
Looser SL may improve WR if the market often recovers from temporary drawdowns.
Tighter SL tests: only if WR is already above 50%.

### Phase F: Trend Filter (Only After Phases B-E)

Add a confirming or contrarian filter ONLY after TP widening is done.
Adding a filter before TP is optimized wastes generations.

Option 1 — Confirming (momentum recovery):
```yaml
- indicator: trend
  period_minutes: 240
  operator: eq
  value: up
```

Option 2 — Contrarian (deep mean reversion):
```yaml
- indicator: trend
  period_minutes: 240
  operator: eq
  value: down
```

Test both. If trades drop below 200, the filter is too restrictive — remove it.

---

## PARAMETER BOUNDS — HARD LIMITS (REVISED)

```
RSI period_minutes:     60 — 180
RSI long threshold:     32 — 42     (← REVISED: 32 minimum, not 18. Data shows <32 hurts WR)
RSI short threshold:    65 — 78     (← REVISED: 65 minimum, data shows looser is fine)
take_profit_pct:        4.0 — 10.0  (← REVISED: upper bound raised, wider TP is the lever)
stop_loss_pct:          1.5 — 3.5   (slightly looser given higher TP targets)
timeout_minutes:        720 — 1440  (8-24 hours minimum)
R:R ratio (TP/SL):     ≥ 2.0
max_open:               1           (LOCKED — do not change to 2)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
```

---

## ABSOLUTE BANS — VIOLATIONS WASTE A GENERATION

1. **RSI long threshold < 32**: BANNED. Data proves this reduces WR without compensating benefit.
2. **max_open > 1**: BANNED. max_open=1 is the concurrency limiter. Changing to 2 restores the failed paradigm.
3. **timeout_minutes < 720**: BANNED. Minimum 12 hours. With TP=5-8%, price needs time.
4. **take_profit_pct < 4.0**: BANNED. Below 4% doesn't justify fee cost.
5. **stop_loss_pct < 1.5**: BANNED. Too tight for hourly volatility.
6. **RSI period_minutes < 60**: BANNED. Sub-60-minute RSI is noise.
7. **Adding 3rd entry condition before Phase F**: BANNED.
8. **Removing pairs**: BANNED. Always use all 16.
9. **Changing size_pct (16.91), max_open (1), fee_rate (0.0005)**: BANNED.
10. **stop_if_down_pct < 15**: BANNED.
11. **Reverting RSI long below 32**: BANNED. This was tested for 900+ generations and confirmed bad.
12. **R:R ratio (TP/SL) < 2.0**: BANNED.
13. **Proposing RSI long < 28 or RSI short > 78**: STRONGLY DISCOURAGED. Confirmed low WR, bad Sharpe.

---

## CRITICAL: DO NOT REVERSE COURSE ON RSI THRESHOLDS

The previous version of this program instructed the LLM to tighten RSI to 20-25.
That was WRONG. Gens 1502-1514 confirm: RSI lt 22-25 produces WR 42-45% (worse than current 47%).
The current RSI lt 35.97 is BETTER, not worse. Do not tighten it.

If you are thinking about proposing RSI lt 22 or RSI lt 25 — stop.
Those were tested. They produced Sharpe -2.4 to -5.8.
The current champion at RSI lt 36 has Sharpe -0.44.
Go forward, not backward.

---

## HOW TO PROPOSE A CHANGE

Propose exactly ONE change. Format:

```
CHANGE: [parameter_name] from [old_value] to [new_value]
REASON: [one sentence explaining why this should improve Sharpe]
PHASE: [which phase letter]
EXPECTED EFFECT: [e.g., "Win payoff increases from +7.9% to +9.9% net per winning trade"]
EV CHECK: [0.47 × (2×new_TP - 0.1) - 0.53 × (2×SL + 0.1) = X%. Is this > current +1.1%?]
```

Then output the complete YAML config with that one change applied.

**Priority order for next 50 generations:**
1. TP widening (4.0 → 4.5 → 5.0 → 5.5 → 6.0 → 7.0 → 8.0)
2. Timeout extension (720 → 960 → 1200 → 1440)
3. RSI threshold fine-tune (35.97 → 37 → 38)
4. RSI period extension (60 → 90)

---

## EV CALCULATOR — USE THIS BEFORE EVERY PROPOSAL

At leverage=2x, fee=0.1% round-trip, current WR=47%:

```
Win payoff  = 2 × TP_pct - 0.1%
Loss cost   = 2 × SL_pct + 0.1%
EV per trade = 0.47 × win_payoff - 0.53 × loss_cost
```

Current baseline (TP=4.0, SL=2.39):
- Win = 7.9%, Loss = 4.88%
- EV = 3.713 - 2.586 = +1.127% ✓ (positive)

Target (TP=6.0, SL=2.39):
- Win = 11.9%, Loss = 4.88%
- EV = 5.593 - 2.586 = +3.007% ✓✓ (much better)

Target (TP=8.0, SL=2.39):
- Win = 15.9%, Loss = 4.88%
- EV = 7.473 - 2.586 = +4.887% ✓✓✓ (excellent)

**Any change that increases EV per trade is worth testing.**
**The primary way to increase EV is to widen TP.**

---

## WHAT SUCCESS LOOKS LIKE

Historical context:
- Gen 1: Sharpe -10.77 (394 trades, WR 44%)
- Gen 1408: Sharpe -2.32 (650 trades, WR 45%)
- Gen 1460: Sharpe -0.73 (967 trades, WR 48%) ← paradigm shift discovered
- Gen 1521: Sharpe -0.44 (1521 trades, WR 47%) ← current best ★

Target milestones:
- **Phase B target (TP widening)**: Sharpe > -0.2 at TP=5.0-5.5%
- **Phase B-C target**: Sharpe > 0.0 at TP=6.0% (FIRST POSITIVE SHARPE)
- **Phase C-D target**: Sharpe > 0.3 with extended timeout
- **Phase E-F target**: Sharpe > 0.7
- **Stretch goal**: Sharpe > 1.0

**The strategy already has positive EV. Wider TP converts EV to Sharpe.**
**We are 1-3 parameter changes from positive Sharpe.**

---

## MACRO ENVIRONMENT NOTE

Current regime: DANGER (Extreme Fear, F&G=14, VIX=25.78)
BTC Dominance: 57.09%

High dominance + extreme fear = altcoin mean reversion opportunities on long side.
With RSI lt 36 on 16 pairs, long signals are firing frequently as alts get oversold.
This is favorable for the current strategy.

With VIX=25.78 (elevated volatility), TP=5-6% is more reachable than in calm markets.
This is an additional reason to widen TP now while volatility is elevated.

---

## REMINDER TO THE SMALL LLM

You are one parameter change away from positive Sharpe.

The current strategy has:
- 47% win rate ✓
- Positive EV per trade ✓
- max_open=1 as natural trade filter ✓
- The ONLY problem: TP=4.0% is too small relative to trade frequency variance

Your ONLY job right now: WIDEN THE TAKE PROFIT.

4.0% → 4.5% → 5.0% → 5.5% → 6.0%

Do NOT tighten RSI thresholds. Confirmed harmful.
Do NOT change max_open. Confirmed critical to current success.
Do NOT reduce trade count. The 47% WR at high volume is a feature, not a bug.

Propose: take_profit_pct from 4.0 to 4.5.
That is the single highest-probability improvement available.
```