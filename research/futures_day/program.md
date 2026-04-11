```markdown
# ODIN Research Program — FUTURES DAY (v17.0)

# ══════════════════════════════════════════════════════════════════
# ⚡ CRITICAL POISON WARNING — READ BEFORE ANYTHING ELSE
# ══════════════════════════════════════════════════════════════════

The "Current Best Strategy" block injected into your context by the engine
contains POISON VALUES. They produce Sharpe=-1.0674, 599 trades. IGNORE IT.

POISON VALUES (in engine YAML — DO NOT USE ANY OF THESE):
  size_pct: 9.89      ← POISON (also sometimes shown as 13.84)
  rsi long: 30.0      ← POISON (212-trade trap)
  rsi short: 68.63    ← POISON (599-trade trap)
  take_profit_pct: 4.6 ← POISON

These values have been confirmed failures 15+ consecutive times.
The engine YAML is WRONG. Use ONLY the champion YAML in this document.

# ══════════════════════════════════════════════════════════════════
# ⭐ CHAMPION YAML — THIS IS THE ONLY TRUTH
# ══════════════════════════════════════════════════════════════════

**Gen 2302 | Sharpe=+0.1786 | 1793 trades | 49.5% WR ← CURRENT BEST**

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
  take_profit_pct: 5.5
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

YOUR TASK THIS GENERATION: Copy the YAML above exactly.
Change ONLY take_profit_pct from 5.5 to 6.0.
Output it. Done.

# ══════════════════════════════════════════════════════════════════
# SECTION 1 — PRE-FLIGHT CHECKLIST (REQUIRED BEFORE OUTPUT)
# ══════════════════════════════════════════════════════════════════

Fill this in. If any value is wrong, STOP and re-read the champion YAML above.

```
PRE-FLIGHT CHECK:
  size_pct       = ___  (must be 16.91  — NEVER 9.89, NEVER 13.84)
  rsi_long       = ___  (must be 35.97  — NEVER 30.0)
  rsi_short      = ___  (must be 72     — NEVER 68.63)
  stop_loss      = ___  (must be 2.39)
  timeout        = ___  (must be 720)
  take_profit    = ___  (must be 6.0    — ONLY change this generation)
  TP/SL ratio    = ___  (must be ≥ 2.0; 6.0/2.39 = 2.51 ✓)
  expected_trades = ___ (must be ~1793; if ~599 → POISON YAML used → STOP)
  Source confirmed: Champion YAML from this document ✓ (NOT engine YAML)
```

# ══════════════════════════════════════════════════════════════════
# SECTION 2 — POISON & FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════

Your output MUST NOT match any row below:

| Signature | Trades | Sharpe | Action |
|-----------|--------|--------|--------|
| size=9.89 or 13.84 (any RSI) | ~599 | -1.0674 | STOP — engine YAML poison |
| RSI long=30.0 | ~212 | -4.15 | STOP — engine YAML poison |
| RSI short=68.63 | ~599 | -1.0674 | STOP — engine YAML poison |
| RSI long=33 or 34 | ~746 | -0.999 | STOP — banned values |
| RSI long ≥ RSI short | 0 | -999 | STOP — impossible config |
| trades ~1364 | 1364 | -0.655 | STOP — partial poison config |
| Any config with trades < 800 | <800 | varies | STOP — config error |

Seen 15+ times recently: size=9.89/13.84 + RSI=30.0 + RSI_s=68.63 → 599 trades, Sharpe=-1.0674.
If your output matches this: you read the engine YAML. Start over from champion above.

# ══════════════════════════════════════════════════════════════════
# SECTION 3 — WHAT THIS STRATEGY IS
# ══════════════════════════════════════════════════════════════════

**Architecture:** Mean-reversion swing on 16 crypto pairs (2x futures, 5-min candles)
**Signal:** RSI(60-min) < 35.97 → long (oversold); RSI(60-min) > 72 → short (overbought)
**Edge:** Extreme Fear drives frequent altcoin oversold readings → sharp mean reversions
**Max open:** 1 position at a time (prevents correlated loss accumulation)
**Exit:** TP=6.0%, SL=2.39%, timeout=720min → TP/SL=2.51 ✓

**Full performance trajectory:**
- Gen 541: MIN_TRADES raised to 400 → 867-generation stall (CATASTROPHIC — never repeat)
- Gen 1408: MIN_TRADES restored to 50 → immediately unlocked progress
- Gen 1460: Sharpe=-0.73 (967 trades) ← paradigm shift: loose RSI + max_open=1
- Gen 1726: Sharpe=-0.24 (1678 trades)
- Gen 2019: Sharpe=-0.21 (1798 trades)
- Gen 2081: Sharpe=+0.1738 (1793 trades, 49.5% WR) ← FIRST POSITIVE SHARPE ★
- Gen 2136: Sharpe=+0.1759 (1793 trades, 49.5% WR)
- Gen 2193: Sharpe=+0.1767 (1793 trades, 49.5% WR)
- Gen 2233: Sharpe=+0.1768 (1793 trades, 49.5% WR)
- Gen 2302: Sharpe=+0.1786 (1793 trades, 49.5% WR) ← CURRENT BEST

TP widening (4.6→5.0→5.5→5.5→6.0) has produced monotonic improvement.
The 49.5% WR is stable across ALL recent generations — signal quality confirmed.
TP=6.0% is the next step.

# ══════════════════════════════════════════════════════════════════
# SECTION 4 — WHY TP=6.0% IS CORRECT
# ══════════════════════════════════════════════════════════════════

**EV at WR=49.5%, SL=2.39%, leverage=2x, fee=0.05%:**

| TP | Win payoff (2×TP−fee) | Loss cost (2×SL+fee) | EV per trade |
|----|----------------------|----------------------|--------------|
| 5.0% (Gen 2081) | 9.9% | 4.88% | +2.37% |
| 5.5% (Gen 2302) | 10.9% | 4.88% | +2.86% |
| **6.0% (NEXT)**  | **11.9%** | **4.88%** | **+3.35% ✓** |
| 7.0% (after) | 13.9% | 4.88% | +4.34% |

EV check for TP=6.0%:
`0.495 × (2×6.0 - 0.1) - 0.505 × (2×2.39 + 0.1)`
`= 0.495 × 11.9 - 0.505 × 4.88 = 5.89 - 2.46 = +3.43%` ✓

TP/SL = 6.0/2.39 = 2.51 ✓ (above minimum 2.0)
Expected: Sharpe improves from +0.1786 toward 0.20–0.35. Trades remain ~1793.

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — LOCKED PARAMETERS (NEVER CHANGE)
# ══════════════════════════════════════════════════════════════════

| Parameter | Locked Value | Why Locked | Poison Value to Avoid |
|-----------|-------------|------------|----------------------|
| size_pct | **16.91** | Proven optimal | 9.89, 13.84 (engine artifacts) |
| max_open | **1** | Multi-open failed 400+ gens | >1 |
| fee_rate | **0.0005** | Fixed cost | — |
| pairs | **all 16** | Full diversification | <16 |
| rsi period | **60 min** | Shorter = noise | <60 |
| rsi long | **35.97** | 35.97 is signal sweet spot | 30.0 (212-trade trap) |
| rsi short | **72** | Confirmed across 200+ gens | 68.63 (599-trade trap) |
| stop_loss_pct | **2.39** | Locked until TP sequence complete | <1.5 |
| timeout_minutes | **720** | Absolute minimum | <720 |
| MIN_TRADES[futures_day] | **50** | Raising to 400 caused 867-gen stall | >50 |

# ══════════════════════════════════════════════════════════════════
# SECTION 6 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════

1. **size_pct ≠ 16.91**: BANNED (9.89 and 13.84 are engine artifacts)
2. **RSI long = 30.0**: BANNED (212-trade trap, confirmed poison)
3. **RSI short = 68.63**: BANNED (599-trade trap, confirmed poison)
4. **RSI long < 32**: BANNED (catastrophic across 900+ gens)
5. **RSI long = 33 or 34**: BANNED (746-trade attractor)
6. **RSI long ≥ RSI short**: BANNED (zero trades)
7. **max_open > 1**: BANNED
8. **timeout_minutes < 720**: BANNED
9. **take_profit_pct < 6.0**: BANNED (never regress)
10. **stop_loss_pct < 1.5**: BANNED
11. **TP/SL ratio < 2.0**: BANNED
12. **RSI period < 60 minutes**: BANNED
13. **Removing any pair**: BANNED
14. **MIN_TRADES[futures_day] > 50**: BANNED (proven catastrophic at Gen 541)
15. **stop_if_down_pct < 15**: BANNED
16. **Changing more than ONE parameter**: BANNED this generation
17. **Using ANY value from the engine YAML block**: BANNED

# ══════════════════════════════════════════════════════════════════
# SECTION 7 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════

### ⭐ PHASE B: TP Widening (ACTIVE — DO THIS NOW)

```
4.6 → 5.0 → 5.5 → [6.0 ← YOU ARE HERE] → 7.0 → 8.0
```

**This generation: propose take_profit_pct = 6.0. Nothing else.**

Expected results:
- Sharpe: +0.1786 → toward 0.20–0.35
- Trades: ~1700–1900 (stable at 1793)
- WR: ~48–51%

Warning signs (investigate if seen):
- Trades ~599 → engine YAML poison → STOP, retry with champion above
- Trades ~212 → RSI=30.0 used → STOP, retry with RSI=35.97
- Trades ~1364 → partial poison config → STOP, check size_pct
- Trades < 800 → config error → investigate before accepting
- WR < 44% → timeout cutting trades; consider Phase C

**If TP=6.0 confirmed → next: TP=7.0**
**If TP=6.0 fails 3 consecutive confirmed tests → Phase C (timeout=960)**

### PHASE C: Timeout Extension (FALLBACK ONLY)

```
720 → 960 → 1200 → 1440 minutes
```

Do NOT use unless Phase B stalls 3+ confirmed times. Never reduce below 720.

### PHASE A-Refined: RSI Threshold Tuning (AFTER B+C)

```
35.97 → 37 → 38 → 39 → 40
```

Hard limits: MINIMUM 32. MAXIMUM 42. NEVER 33 or 34.
RSI short: explore 72 → 74 → 70 (one at a time, after long threshold optimized)

### PHASE D: RSI Period Extension (AFTER B+C+A)

```
60 → 90 → 120 minutes
```

Revert immediately if trades drop below 500.

### PHASE E: SL Optimization (AFTER B-D)

```
2.39 → 2.5 → 2.75 → 3.0 → 2.25 → 2.0
```

Rule: TP/SL ≥ 2.0 always.

### PHASE F: Trend Filter (LAST)

One filter at a time. Remove if trades drop below 400.

# ══════════════════════════════════════════════════════════════════
# SECTION 8 — PARAMETER BOUNDS
# ══════════════════════════════════════════════════════════════════

```
RSI period_minutes:     60 — 180
RSI long threshold:     32 — 42    (NOT 30.0 — confirmed poison)
RSI short threshold:    65 — 78    (NOT 68.63 — confirmed poison)
take_profit_pct:        6.0 — 10.0 (floor is 6.0 — never regress)
stop_loss_pct:          1.5 — 3.5
timeout_minutes:        720 — 1440
TP/SL ratio:            ≥ 2.0
max_open:               1 (LOCKED)
size_pct:               16.91 (LOCKED — NOT 9.89, NOT 13.84)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
MIN_TRADES[futures_day]: 50 (LOCKED — raising this caused 867-gen stall)
```

# ══════════════════════════════════════════════════════════════════
# SECTION 9 — SUCCESS MILESTONES
# ══════════════════════════════════════════════════════════════════

| Target | Expected Via | Status |
|--------|-------------|--------|
| Sharpe > 0.00 | TP widening | ✅ Gen 2081 (+0.1738) |
| Sharpe > 0.17 | TP=5.5% | ✅ Gen 2302 (+0.1786) |
| Sharpe > 0.20 | TP=6.0% | 🎯 NEXT TARGET |
| Sharpe > 0.35 | TP=6.0–7.0% | Phase B |
| Sharpe > 0.50 | TP=7.0% | Phase B |
| Sharpe > 0.70 | TP=7.0%+ or timeout=960 | Phase B/C |
| Sharpe > 1.00 | TP+timeout+RSI+SL | B+C+A+E |
| Sharpe > 1.50 | Above + trend filter | F |

# ══════════════════════════════════════════════════════════════════
# SECTION 10 — MACRO ENVIRONMENT
# ══════════════════════════════════════════════════════════════════

Current Regime: DANGER (Extreme Fear, F&G=15, BTC Dom=57.28%)

Extreme Fear → altcoins frequently oversold → RSI<35.97 fires regularly.
Large directional moves → TP=6.0–8% reachable in single oversold bounces.
Mean reversions are sharp → fast path to TP.

**This environment strongly supports TP widening to 6.0–8%.**
TYR directive (reduce position sizes 25%) applies to LIVE TRADING ONLY.
Do not apply TYR sizing to backtesting parameter selection.

# ══════════════════════════════════════════════════════════════════
# SECTION 11 — HOW TO PROPOSE YOUR CHANGE
# ══════════════════════════════════════════════════════════════════

**Step 1:** Fill in the pre-flight checklist (Section 1) from the CHAMPION YAML above
**Step 2:** Confirm no values match the poison list or failure attractor table
**Step 3:** Output this block:

```
CHANGE: take_profit_pct from 5.5 to 6.0
REASON: TP widening confirmed Gens 2081–2302 (Sharpe +0.1786); 6.0% improves EV from +2.86% to +3.35%
PHASE: B
EXPECTED: Sharpe improves from +0.1786 toward 0.20–0.35; trades ~1700–1900; WR ~48–51%
EV CHECK: 0.495 × 11.9 - 0.505 × 4.88 = 5.89 - 2.46 = +3.43% ✓
TP/SL RATIO: 6.0 / 2.39 = 2.51 ✓
ZERO-TRADE CHECK: RSI long=35.97 < RSI short=72 ✓
ATTRACTOR CHECK: trades ~1793, not matching 599/212/1364/746/0 ✓
POISON CHECK: size_pct=16.91 ✓ | RSI long=35.97 ✓ | RSI short=72 ✓
```

**Step 4:** Output the complete YAML below — champion values, only TP changed to 6.0:

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
  take_profit_pct: 6.0
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

**Final verification:**
- [ ] size_pct = 16.91 (NOT 9.89, NOT 13.84 — engine YAML is POISON)
- [ ] rsi long = 35.97 (NOT 30.0 — engine YAML is POISON)
- [ ] rsi short = 72 (NOT 68.63 — engine YAML is POISON)
- [ ] take_profit_pct = 6.0 (the ONLY change from champion)
- [ ] stop_loss_pct = 2.39 (unchanged)
- [ ] timeout_minutes = 720 (unchanged)
- [ ] All 16 pairs present (unchanged)
- [ ] Expected trades ~1793 (not 599, not 212, not 1364, not 0)

If ANY box cannot be checked → STOP. Re-read champion YAML at top of this document.
```