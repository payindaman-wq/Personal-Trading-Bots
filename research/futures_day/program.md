```markdown
# ODIN Research Program — FUTURES DAY (v10.0) — EVIDENCE-FIRST

## League: futures_day
Timeframe: 5-minute candle data available, USE 1-HOUR indicator periods
Leverage: 2x
Sprint duration: 24 hours

---

## ⚠️ CONSTANTS — LOCKED

```
MIN_TRADES["futures_day"] = 50
```

**DO NOT CHANGE THIS.** The single most damaging event in this research program's history
was raising MIN_TRADES["futures_day"] to 400 at Gen 541, which stalled progress for
1,100+ generations. Configs with 50-200 trades are valid. Configs with 1500+ trades
are valid. The backtest engine decides quality; we do not pre-filter by count.

---

## WHAT THE DATA ACTUALLY SHOWS — READ THIS FIRST

### The Paradigm Shift (Gen 1460)

After 1,460 generations of optimization, the data reveals:

| Configuration | WR | Sharpe | Trades |
|---|---|---|---|
| RSI < 22-25, tight thresholds | 42-45% | -2.4 to -5.8 | 150-300 |
| RSI < 36, max_open=1 | 47-48% | -0.44 to -0.37 | 1395-1521 |

**Tighter RSI does NOT produce higher-quality trades. It produces worse WR AND worse Sharpe.**
**The loose RSI + max_open=1 architecture is the correct paradigm. Do not reverse it.**

### The Loop Problem (Gens 1580-1600)

The last 20 generations show a dangerous pattern: 8 of 20 generations produced
identical results (Sharpe=-0.9990, WR=49.2%, trades=746). This means the small LLM
is repeatedly proposing the same bad change — likely RSI tightening to ~33-34 or
a filter that cuts trades by 50%. **This exact config should be explicitly recognized
and rejected.**

If you find yourself proposing a change that would produce ~746 trades (vs current
~1400-1521), you are proposing RSI tightening or a filter that has already been
tested and failed. **Stop. Propose something different.**

### The TP Widening Question

The research program has theorized that widening TP from 4.0% to 5-6% should improve
Sharpe via higher win payoff. **This has NOT yet been confirmed by backtest results.**
The current best (Gen 1570) still uses TP=4.0%. This could mean:

1. The small LLM is not proposing TP widening (fixable with stronger instructions)
2. TP widening is failing in backtest (requires different approach)

The EV math is theoretically sound IF win rate is stable at 47% as TP widens.
But wider TP may reduce effective WR (fewer trades reach the target in time).
**We must test this empirically. TP widening is PRIORITY #1, but if it fails
3 consecutive tests, escalate to timeout extension instead.**

---

## CURRENT CHAMPION (Gen 1570)

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

**Performance: Sharpe -0.3689, 1395 trades, 47.2% WR**
**Positive EV confirmed: ~+1.1% per trade at current TP/SL.**
**Problem: high per-trade variance suppresses Sharpe below zero.**

---

## LOCKED PARAMETERS — NEVER CHANGE THESE

```yaml
position:
  size_pct: 16.91      ← locked
  max_open: 1          ← locked — the concurrency filter that makes this work
  fee_rate: 0.0005     ← locked — never change
pairs: [all 16]        ← locked — never remove any pair
```

**size_pct was 20 in the base config but was optimized to 16.91 in the champion.**
**Do not change it back to 20. Do not change it at all.**

---

## OPTIMIZATION SEQUENCE

### ⭐ PHASE B: Widen Take-Profit (IMMEDIATE PRIORITY)

**Why:** At TP=4.0%, positive EV = +1.13%/trade but high variance → negative Sharpe.
At TP=6.0%, EV = +3.0%/trade. Same variance, better mean → Sharpe improves.

**Sequence:**
```
4.0 → 4.5 → 5.0 → 5.5 → 6.0 → 7.0 → 8.0
```

Test ONE step per generation. Do not skip steps — each step tells us if WR holds.

**EV check for each step:**
| TP | Win (2x lev) | EV (at 47% WR) |
|---|---|---|
| 4.0% | 7.9% net | +1.13% ✓ |
| 4.5% | 8.9% net | +1.60% ✓ |
| 5.0% | 9.9% net | +2.07% ✓✓ |
| 5.5% | 10.9% net | +2.54% ✓✓ |
| 6.0% | 11.9% net | +3.01% ✓✓✓ |

Keep SL at 2.39% unless TP/SL < 2.0. All values above maintain TP/SL ≥ 1.88.
At TP=5.0%: TP/SL = 5.0/2.39 = 2.09 ✓

**If TP widening fails 3 consecutive tests (Sharpe does not improve):**
This means effective WR is dropping as TP widens (fewer trades reach target).
→ Switch immediately to Phase C (timeout extension) to let more trades reach TP.
→ Then retest TP widening with the longer timeout.

**Warning sign:** If a TP widening test produces WR below 44%, the wider TP is
causing early timeout exits before TP is reached. Fix: extend timeout first.

### ⭐ PHASE C: Extend Timeout (CO-EQUAL PRIORITY WITH PHASE B)

Current timeout=720 minutes (12 hours). With TP=4-6%, many trades may be timing
out before reaching TP. Extending timeout allows more trades to complete.

**Sequence:**
```
720 → 960 → 1200 → 1440 minutes
```

**Why this improves Sharpe:**
- More TP hits → effective WR increases
- Timeout exits are typically partial losses or small gains → removing them helps
- Expected: each 240-minute extension adds 1-3% to effective WR

**If TP widening is failing:** Start Phase C immediately, then retry Phase B.
**If TP widening is succeeding:** Run Phase C in parallel (alternate proposals).

Do NOT go below 720 minutes. Do NOT try 480 or 360 — this was the failure mode.

### Phase A-Refined: RSI Threshold Fine-Tuning (SECONDARY — ONLY AFTER B/C)

Current RSI long=35.97 is near-optimal. Very small adjustments only:
```
35.97 → 37 → 38 → 36 (retest) → 39 → 40
```

**Hard limits:**
- Do NOT go below 32. Confirmed catastrophic (WR drops to 42-44%).
- Do NOT go above 42. Too many false signals.
- The 746-trade / 49.2% WR / Sharpe=-0.9990 attractor is around RSI~33-34.
  **If your proposed RSI is 33 or 34, stop. This has been tested. It fails.**

For RSI short: current 72 is fine. Test 70 or 74 only after TP and timeout are optimized.

### Phase D: RSI Period Extension (TERTIARY)

Test RSI period: 60 → 90 → 120 minutes
Longer period = smoother RSI = marginally better signal quality.
**Only test this after TP and timeout are optimized.**
If trade count drops below 300, revert.

### Phase E: SL Optimization (AFTER PHASES B-D)

With optimal TP from above, test SL values:
```
2.39 → 2.5 → 2.75 → 3.0 → 2.25 → 2.0
```

**Rule:** TP/SL ≥ 2.0 always.
- Looser SL: tests whether market often recovers from temporary drawdowns
- Tighter SL: only if WR is already ≥ 50%

### Phase F: Trend Filter (ONLY AFTER ALL ABOVE)

Add ONE confirming or contrarian filter. Test both options separately:

**Option 1 — Contrarian (deep mean reversion):**
```yaml
- indicator: trend
  period_minutes: 240
  operator: eq
  value: down
```

**Option 2 — Confirming (momentum recovery):**
```yaml
- indicator: trend
  period_minutes: 240
  operator: eq
  value: up
```

If adding a filter drops trades below 300, it is too restrictive — remove it.
**Do NOT add a filter before TP and timeout are optimized. It wastes generations.**

---

## PARAMETER BOUNDS — HARD LIMITS

```
RSI period_minutes:     60 — 180
RSI long threshold:     32 — 42     (MINIMUM 32 — confirmed catastrophic below this)
RSI short threshold:    65 — 78
take_profit_pct:        4.0 — 10.0
stop_loss_pct:          1.5 — 3.5
timeout_minutes:        720 — 1440  (MINIMUM 720 — do not reduce)
R:R ratio (TP/SL):      ≥ 2.0
max_open:               1           (LOCKED)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
```

---

## ABSOLUTE BANS — VIOLATIONS WASTE A GENERATION

1. **RSI long threshold < 32**: BANNED. 900+ generations confirm this is harmful.
2. **RSI long threshold 33-34**: STRONGLY DISCOURAGED. This produces the
   746-trade / 49.2% WR / Sharpe=-0.9990 attractor. It has appeared 8+ times.
   If you are about to propose RSI=33 or RSI=34, stop and propose TP widening instead.
3. **max_open > 1**: BANNED. This was the failed paradigm before Gen 1460.
4. **timeout_minutes < 720**: BANNED. Minimum 12 hours.
5. **take_profit_pct < 4.0**: BANNED. Fee cost makes this unprofitable.
6. **stop_loss_pct < 1.5**: BANNED. Too tight for hourly volatility.
7. **RSI period_minutes < 60**: BANNED. Sub-60-minute RSI is noise.
8. **Removing any pair**: BANNED. Always use all 16.
9. **Changing size_pct (16.91), max_open (1), fee_rate (0.0005)**: BANNED.
10. **stop_if_down_pct < 15**: BANNED.
11. **R:R ratio (TP/SL) < 2.0**: BANNED.
12. **Adding 3rd entry condition before Phase F**: BANNED.
13. **Reverting RSI long below 32**: BANNED.

---

## THE 746-TRADE TRAP — RECOGNIZE AND ESCAPE IT

In the last 20 generations, 8 proposals produced this exact result:
```
Sharpe=-0.9990, WR=49.2%, trades=746
```

This is a known failure configuration. It is worse than the current best despite
having higher WR (49.2% vs 47.2%), because fewer trades mean more variance.

**If you are about to propose any of the following, STOP:**
- RSI long threshold: 33, 34
- timeout_minutes: 360, 480
- Adding a trend filter without testing TP/timeout first
- Any change that would approximately halve the trade count from ~1400 to ~700

**The escape from this trap:** Propose TP widening.
```
take_profit_pct from 4.0 to 4.5
```
This is the single highest-probability improvement available.

---

## HOW TO PROPOSE A CHANGE

Propose exactly ONE change. Format:

```
CHANGE: [parameter_name] from [old_value] to [new_value]
REASON: [one sentence explaining why this should improve Sharpe]
PHASE: [which phase letter]
EXPECTED EFFECT: [specific prediction, e.g., "Win payoff increases from +7.9% to +8.9% net"]
EV CHECK: [0.47 × (2×new_TP - 0.1) - 0.53 × (2×SL + 0.1) = X%. Must be > +1.13%]
LOOP CHECK: [confirm this is NOT the 746-trade / RSI=33-34 attractor]
```

Then output the complete YAML config with exactly that one change applied.

---

## EV CALCULATOR — USE BEFORE EVERY PROPOSAL

At leverage=2x, fee=0.1% round-trip, current WR=47.2%:

```
Win payoff  = 2 × TP_pct - 0.1%
Loss cost   = 2 × SL_pct + 0.1%
EV per trade = 0.472 × win_payoff - 0.528 × loss_cost
```

**Current baseline (TP=4.0, SL=2.39):**
- Win = 7.9%, Loss = 4.88%
- EV = 0.472×7.9 - 0.528×4.88 = 3.73 - 2.58 = +1.15% ✓

**Target (TP=4.5, SL=2.39):**
- Win = 8.9%, Loss = 4.88%
- EV = 0.472×8.9 - 0.528×4.88 = 4.20 - 2.58 = +1.62% ✓✓

**Target (TP=6.0, SL=2.39):**
- Win = 11.9%, Loss = 4.88%
- EV = 0.472×11.9 - 0.528×4.88 = 5.62 - 2.58 = +3.04% ✓✓✓

**Any change that increases EV per trade without dramatically reducing trade count
is worth testing.**

---

## PRIORITY ORDER FOR NEXT 100 GENERATIONS

```
Priority 1 (Gens 1601-1630): TP widening
  → Propose: 4.0 → 4.5 → 5.0 → 5.5 → 6.0
  → If 3 consecutive TP proposals fail → switch to timeout extension

Priority 2 (Gens 1601-1630, if TP fails): Timeout extension
  → Propose: 720 → 960 → 1200 → 1440
  → Then retry TP widening with longer timeout

Priority 3 (Gens 1631-1660): RSI threshold micro-tuning
  → Try: 35.97 → 37 → 38

Priority 4 (Gens 1661-1680): RSI period extension
  → Try: 60 → 90

Priority 5 (Gens 1681-1720): SL optimization
  → Try: 2.39 → 2.5 → 2.75

Priority 6 (Gens 1721+): Trend filter
  → Try contrarian filter (trend=down, period=240)
```

---

## SUCCESS MILESTONES

| Milestone | Target | Expected Via |
|---|---|---|
| Sharpe > -0.30 | TP=4.5-5.0% OR timeout=960 | Phase B or C |
| Sharpe > 0.00 | TP=5.5-6.0% + timeout=960 | Phase B+C |
| Sharpe > 0.30 | TP=6.0% + timeout=1200 + RSI tuned | Phase B+C+A |
| Sharpe > 0.70 | Above + SL optimized | Phase E |
| Sharpe > 1.00 | Above + trend filter | Phase F |

**Historical context:**
- Gen 1: Sharpe -10.77 (394 trades, 44% WR)
- Gen 1460: Sharpe -0.73 (967 trades, 48% WR) ← paradigm shift
- Gen 1570: Sharpe -0.37 (1395 trades, 47% WR) ← current best ★
- Next target: Sharpe > -0.25 (TP widening or timeout extension)

---

## MACRO ENVIRONMENT NOTE

Current Regime: DANGER (Extreme Fear, F&G=14, BTC Dom=56.95%)
VIX elevated (~25+).

High fear + elevated volatility means:
- Altcoins getting deeply oversold → RSI < 36 signals are frequent and real
- Larger price swings → TP=5-6% is MORE reachable than in calm markets
- Mean reversions can be sharp and fast → shorter holding time to TP

This environment **supports TP widening**: price can move 5-6% in a single
oversold bounce during high-volatility fear episodes.

---

## REMINDER TO THE SMALL LLM

You are close to positive Sharpe. The current strategy has:
✓ 47% win rate
✓ Positive EV per trade (+1.15%)
✓ max_open=1 as natural signal filter
✓ 1395 trades (statistically significant)

The ONLY problem: TP=4.0% leaves money on the table. Winners close too early.

**Your ONLY job right now: WIDEN THE TAKE PROFIT.**

```
take_profit_pct from 4.0 to 4.5
```

Do NOT propose RSI=33 or RSI=34. That is the 746-trade trap. It fails every time.
Do NOT reduce timeout below 720. Do NOT tighten RSI. Do NOT change max_open.

Propose exactly one change: take_profit_pct from 4.0 to 4.5.
```