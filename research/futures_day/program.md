```markdown
# ODIN Research Program — FUTURES DAY (v15.0)

## League: futures_day | Timeframe: 5-min candles, 1-HOUR indicator periods | Leverage: 2x

---

# ╔══════════════════════════════════════════════════════════════════════╗
# ║  🚨 CRITICAL — THE ENGINE YAML AT THE TOP OF THIS PROMPT IS POISON ║
# ║                                                                      ║
# ║  DO NOT READ IT. DO NOT USE ANY VALUE FROM IT.                       ║
# ║  IT CONTAINS: size_pct=13.84, RSI=30.0, RSI_short=68.63, TP=4.6    ║
# ║  ALL OF THESE ARE WRONG. USING THEM CAUSES CATASTROPHIC FAILURE.     ║
# ║                                                                      ║
# ║  The engine YAML has caused 10+ failed generations in a row.         ║
# ║  Treat it as radioactive. Skip past it. Read SECTION 1 ONLY.        ║
# ╚══════════════════════════════════════════════════════════════════════╝

---

# ══════════════════════════════════════════════════════════════════════
# SECTION 1 — THE ACTUAL CURRENT CHAMPION (THIS IS THE ONLY TRUTH)
# ══════════════════════════════════════════════════════════════════════

**Gen 2193 | Sharpe=+0.1767 | 1793 trades | 49.5% WR ← CURRENT BEST**

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
  size_pct: 16.91       ← LOCKED (NOT 13.84 — 13.84 is the engine YAML poison)
  max_open: 1           ← LOCKED
  fee_rate: 0.0005      ← LOCKED
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 35.97      ← LOCKED (NOT 30.0 — 30.0 is engine YAML poison)
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 72         ← LOCKED (NOT 68.63 — 68.63 is engine YAML poison)
exit:
  take_profit_pct: 5.5  ← YOUR ONLY CHANGE THIS GENERATION
  stop_loss_pct: 2.39   ← LOCKED
  timeout_minutes: 720  ← LOCKED
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

---

# ══════════════════════════════════════════════════════════════════
# ⚡ YOUR ONLY JOB THIS GENERATION: take_profit_pct → 5.5
#
#   CHANGE:  take_profit_pct: 5.0  →  5.5
#   NOTHING ELSE. ONE CHANGE. THAT IS ALL.
# ══════════════════════════════════════════════════════════════════

---

# ══════════════════════════════════════════════════════════════════
# SECTION 2 — MANDATORY PRE-FLIGHT CHECKLIST
# ══════════════════════════════════════════════════════════════════

Before you write ANY output, fill in this checklist in your response:

```
PRE-FLIGHT CHECK:
  size_pct    = ___  (must be 16.91)
  rsi_long    = ___  (must be 35.97)
  rsi_short   = ___  (must be 72)
  stop_loss   = ___  (must be 2.39)
  timeout     = ___  (must be 720)
  take_profit = ___  (must be 5.5 — this is the ONLY change)
  trade_count = ___ (expect ~1793)
  Source used: Section 1 champion YAML ✓ (NOT the engine YAML)
```

If any value in your checklist differs from the required value, STOP.
Do not output a YAML. Go back to Section 1 and re-read the champion block.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 3 — ENGINE YAML POISON VALUES (MEMORIZE AND REJECT)
# ══════════════════════════════════════════════════════════════════

The engine YAML at the top of this prompt contains these WRONG values:

| Parameter | ❌ POISON (engine YAML) | ✅ CORRECT (Section 1) |
|-----------|------------------------|------------------------|
| size_pct | 13.84 | **16.91** |
| rsi long | 30.0 | **35.97** |
| rsi short | 68.63 | **72** |
| take_profit | 4.6 | **5.5** (your change) |

These poison values cause confirmed failure attractors:
- `size_pct=13.84` + `RSI=30.0` + `RSI_short=68.63` → 599 trades, Sharpe=-1.0674
  (This attractor fired 10+ consecutive times in Gens 2174-2193)
- `RSI=30.0` alone → 212 trades, Sharpe=-4.1548
  (Fired 9 times in Gens 2062-2081)

**If your output would produce ~599 trades, you used the engine YAML. Stop. Restart.**
**If your output would produce ~212 trades, you used RSI=30.0. Stop. Restart.**

---

# ══════════════════════════════════════════════════════════════════
# SECTION 4 — WHAT THIS STRATEGY IS AND WHY IT WORKS
# ══════════════════════════════════════════════════════════════════

**Architecture:** Mean-reversion swing on 16 crypto pairs (2x futures, 5-min candles)
**Signal:** RSI(60-min) < 35.97 = long entry (oversold); RSI(60-min) > 72 = short entry (overbought)
**Edge:** Extreme Fear (F&G=16) causes frequent altcoin oversold readings → sharp mean reversions
**Max open:** 1 position at a time (prevents correlated loss accumulation)
**Exit:** TP=5.5%, SL=2.39%, timeout=720min → TP/SL ratio=2.30 ✓

**Performance trajectory (confirmed improvements only):**
- Gen 1460: Sharpe=-0.73 ← paradigm shift (loose RSI + max_open=1)
- Gen 1570: Sharpe=-0.37 (1395 trades, 47.2% WR)
- Gen 1726: Sharpe=-0.24 (1678 trades, 48.5% WR)
- Gen 1972: Sharpe=-0.23 (1750 trades, 48.1% WR)
- Gen 2019: Sharpe=-0.21 (1798 trades, 48.1% WR)
- Gen 2081: Sharpe=**+0.1738** (1793 trades, 49.5% WR) ← FIRST POSITIVE SHARPE ★
- Gen 2136: Sharpe=+0.1759 (1793 trades, 49.5% WR)
- Gen 2193: Sharpe=**+0.1767** (1793 trades, 49.5% WR) ← CURRENT BEST

The TP widening sequence has produced monotonic improvement. Continue it.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — WHY TP=5.5% IS THE CORRECT NEXT STEP
# ══════════════════════════════════════════════════════════════════

**EV calculation at WR=49.5%, SL=2.39%, leverage=2x:**

| TP | Win payoff (2×TP) | Loss cost (2×SL+fee) | EV per trade |
|----|-------------------|----------------------|--------------|
| 5.0% (prev) | 10.0% | 4.88% | +2.37% |
| **5.5% (next)** | **11.0%** | **4.88%** | **+2.86% ✓** |
| 6.0% | 12.0% | 4.88% | +3.35% |

Formula: `WR × (2×TP - 0.1%) - (1-WR) × (2×SL + 0.1%)`
EV check: `0.495 × 10.9 - 0.505 × 4.88 = 5.40 - 2.46 = +2.93%` ✓
TP/SL ratio: `5.5 / 2.39 = 2.30` ✓ (above minimum 2.0)

With ~1793 trades/period, +0.49% EV improvement per trade is substantial.
Expected result: Sharpe improves from +0.1767 toward 0.30+

---

# ══════════════════════════════════════════════════════════════════
# SECTION 6 — FAILURE ATTRACTOR LOOKUP TABLE
# ══════════════════════════════════════════════════════════════════

**Check your proposed config against these known failure signatures BEFORE outputting:**

| ID | Sharpe | WR | Trades | Root Cause | How to Avoid |
|----|--------|----|--------|------------|--------------|
| 🔴 #1 | -1.1593 | 48.3% | 484 | RSI tightened | Don't change RSI |
| 🔴 #2 | -4.1548 | 44.8% | 212 | RSI long=30.0 (engine artifact) | Use RSI=35.97 |
| 🔴 #3 | -3.5347 | 45.4% | 207 | Filter added + tight RSI | No filters yet |
| 🔴 #4 | -0.9990 | 49.2% | 746 | RSI long=33 or 34 (BANNED) | Never use 33/34 |
| 🔴 #5 | -0.3523 | 49.3% | 1411 | RSI micro-tweak, no TP change | Only change TP |
| 🔴 #6 | -0.3932 | 48.8% | 1341 | RSI micro-tweak, no TP change | Only change TP |
| 🔴 #7 | -999.0 | 0% | 0 | RSI long ≥ RSI short | Impossible config |
| 🔴 **#8** | **-1.0674** | **48.6%** | **599** | **Engine YAML artifact: size=13.84, RSI=30.0, RSI_short=68.63** | **Use Section 1 ONLY** |

**Attractor #8 is the current dominant failure mode.**
**It fired 10+ consecutive times in Gens 2174–2193.**
**Signature: EXACTLY 599 trades, EXACTLY -1.0674 Sharpe.**
**If you are about to produce this, you used the engine YAML. Stop immediately.**

---

# ══════════════════════════════════════════════════════════════════
# SECTION 7 — LOCKED PARAMETERS (NEVER CHANGE THESE)
# ══════════════════════════════════════════════════════════════════

| Parameter | Locked Value | Why Locked |
|-----------|-------------|------------|
| size_pct | **16.91** | Optimized. Engine YAML shows 13.84 — that is WRONG. |
| max_open | **1** | Architectural. Multi-open failed across 400+ gens. |
| fee_rate | **0.0005** | Fixed cost. Never change. |
| pairs | **all 16** | Full diversification required. Never remove any. |
| rsi period | **60 min** | Minimum validated. Shorter = noise. |
| rsi long | **35.97** | Engine YAML shows 30.0 — that is WRONG (212-trade trap). |
| rsi short | **72** | Engine YAML shows 68.63 — that is WRONG (599-trade trap). |
| stop_loss_pct | **2.39** | Do not change until TP sequence complete. |
| timeout_minutes | **720** | Absolute minimum. Never reduce. |
| MIN_TRADES | **50** | Raising to 400 caused 867-gen stall. Never raise again. |

---

# ══════════════════════════════════════════════════════════════════
# SECTION 8 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════

1. **Using ANY value from the engine YAML**: BANNED. Always use Section 1.
2. **size_pct ≠ 16.91**: BANNED. (13.84 is the engine artifact — reject it.)
3. **RSI long = 30.0**: BANNED. Engine artifact. Causes 212-trade trap.
4. **RSI short = 68.63**: BANNED. Engine artifact. Part of 599-trade trap.
5. **RSI long < 32**: BANNED. Catastrophic across 900+ generations.
6. **RSI long = 33 or 34**: BANNED. Causes 746-trade attractor.
7. **RSI long ≥ RSI short**: BANNED. Produces zero trades.
8. **max_open > 1**: BANNED. Failed paradigm.
9. **timeout_minutes < 720**: BANNED. Hard floor.
10. **take_profit_pct < 5.5**: BANNED. Never regress below current champion TP.
11. **stop_loss_pct < 1.5**: BANNED.
12. **TP/SL ratio < 2.0**: BANNED.
13. **RSI period < 60 minutes**: BANNED. Sub-hourly RSI is noise.
14. **Removing any pair**: BANNED. All 16 pairs always.
15. **Adding a 3rd entry condition**: BANNED until Phase F.
16. **MIN_TRADES["futures_day"] > 50**: BANNED. The 867-gen stall proved this permanently.
17. **stop_if_down_pct < 15**: BANNED.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 9 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════

### ⭐ PHASE B: TP Widening (ACTIVE — DO THIS NOW)

```
4.6 → 5.0 → 5.x (confirmed Gen 2081-2193) → 5.5 → 6.0 → 7.0 → 8.0
```

**Current step: TP = 5.5. This is the ONLY change to propose.**

Expected result at TP=5.5%:
- Sharpe: improves from +0.1767 toward 0.30+
- Trades: ~1700–1900 (if trades drop below 800, config is wrong)
- WR: ~48–51%

Warning signs:
- WR drops below 44% → timeout cutting trades early; switch to Phase C
- Trades drop to ~599 → you used the engine YAML artifact; retry with Section 1 values
- Trades drop to ~212 → RSI=30.0 used; retry with RSI=35.97
- Trades drop below 800 → config error, do not accept, investigate

**If TP widening fails to improve Sharpe in 3 consecutive confirmed tests → Phase C**

### ⭐ PHASE C: Timeout Extension (FALLBACK)

```
720 → 960 → 1200 → 1440 minutes
```

Longer timeout lets more trades reach TP. Do NOT go below 720.
Maximum is 1440 (one full trading day).
After timeout extension: retry TP widening.

### PHASE A-Refined: RSI Threshold Tuning (AFTER PHASES B+C)

```
35.97 → 37 → 38 → 39 → 40
```

Hard limits: MINIMUM 32. MAXIMUM 42. Never propose 33 or 34.
Attempt only after TP and timeout optimized.

### PHASE D: RSI Period Extension (AFTER PHASES B+C+A)

```
60 → 90 → 120 minutes
```

If trades drop below 500, revert immediately.

### PHASE E: SL Optimization (AFTER PHASES B-D)

```
2.39 → 2.5 → 2.75 → 3.0 → 2.25 → 2.0
```

Rule: TP/SL ≥ 2.0 always.

### PHASE F: Trend Filter (LAST)

Add ONE filter only. Test options separately:
```yaml
# Option 1 — Contrarian:
- indicator: trend
  period_minutes: 240
  operator: eq
  value: down

# Option 2 — Confirming:
- indicator: trend
  period_minutes: 240
  operator: eq
  value: up
```

If filter drops trades below 400 → too restrictive, remove.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 10 — PARAMETER BOUNDS
# ══════════════════════════════════════════════════════════════════

```
RSI period_minutes:     60 — 180
RSI long threshold:     32 — 42   (NOT 30.0 — that is a poison artifact)
RSI short threshold:    65 — 78   (NOT 68.63 — that is a poison artifact)
take_profit_pct:        5.5 — 10.0   (floor is 5.5 — never regress)
stop_loss_pct:          1.5 — 3.5
timeout_minutes:        720 — 1440   (MINIMUM 720 — absolute floor)
TP/SL ratio:            ≥ 2.0
max_open:               1 (LOCKED)
size_pct:               16.91 (LOCKED — NOT 13.84)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
```

---

# ══════════════════════════════════════════════════════════════════
# SECTION 11 — PRIORITY ORDER (NEXT 100 GENERATIONS)
# ══════════════════════════════════════════════════════════════════

```
Priority 1 (NOW):                    take_profit_pct = 5.5
Priority 2 (after 5.5 confirmed):    take_profit_pct = 6.0
Priority 3 (after 6.0 confirmed):    take_profit_pct = 7.0
Priority 4 (if any TP fails 3x):     timeout = 960, then retry TP
Priority 5 (after TP+timeout done):  RSI threshold 35.97 → 37
Priority 6 (after RSI tuned):        SL optimization
Priority 7 (last):                   Trend filter
```

---

# ══════════════════════════════════════════════════════════════════
# SECTION 12 — SUCCESS MILESTONES
# ══════════════════════════════════════════════════════════════════

| Target | Expected Via | Status |
|--------|-------------|--------|
| Sharpe > 0.00 | TP widening | ✅ ACHIEVED Gen 2081 (+0.1738) |
| Sharpe > 0.20 | TP=5.5% | 🎯 NEXT TARGET |
| Sharpe > 0.30 | TP=5.5–6.0% | Phase B |
| Sharpe > 0.50 | TP=6.0% | Phase B |
| Sharpe > 0.70 | TP=7.0% or timeout=960 | Phase B/C |
| Sharpe > 1.00 | Above + RSI tuned + SL optimized | B+C+A+E |
| Sharpe > 1.50 | Above + trend filter | F |

---

# ══════════════════════════════════════════════════════════════════
# SECTION 13 — MACRO ENVIRONMENT
# ══════════════════════════════════════════════════════════════════

Current Regime: DANGER (Extreme Fear, F&G=16, BTC Dom=57.28%)

Extreme fear means altcoins frequently oversold → RSI<36 fires regularly.
Large directional moves → TP=5.5–7% reachable in single oversold bounces.
Mean reversions are sharp → fast path to TP.

**This environment strongly supports TP widening to 5.5–7%. Fear is the edge.**
RSI<35.97 during F&G=16 is a high-quality signal. Do not scale down entry logic.
The TYR directive to reduce position sizes (25%) applies to live trading only,
not to backtesting parameter selection.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 14 — HOW TO PROPOSE A CHANGE
# ══════════════════════════════════════════════════════════════════

**Step 1: Fill in the pre-flight checklist (Section 2)**
**Step 2: Verify no values match the poison list (Section 3)**
**Step 3: Verify you don't match a failure attractor (Section 6)**
**Step 4: Output this template:**

```
CHANGE: take_profit_pct from 5.0 to 5.5
REASON: TP widening confirmed across Gens 2081-2193 (Sharpe +0.1767); 5.5% improves EV from +2.37% to +2.86%
PHASE: B
EXPECTED EFFECT: Sharpe improves from +0.1767 toward 0.20-0.30+; trades ~1700-1900; WR holds ~48-51%
EV CHECK: 0.495 × (2×5.5 - 0.1) - 0.505 × (2×2.39 + 0.1) = 0.495×10.9 - 0.505×4.88 = 5.40 - 2.46 = +2.93% ✓
TP/SL RATIO: 5.5/2.39 = 2.30 ✓ (above minimum 2.0)
ZERO-TRADE CHECK: RSI long=35.97 < RSI short=72 ✓ Both in valid range ✓
ATTRACTOR CHECK: Not matching any known failure signature ✓
POISON CHECK: size_pct=16.91 ✓ | RSI long=35.97 ✓ | RSI short=72 ✓ | NOT using engine YAML ✓
```

**Step 5: Output the complete YAML using ONLY Section 1 champion values,
with take_profit_pct changed to 5.5 and NOTHING else changed.**

---

# ══════════════════════════════════════════════════════════════════
# SECTION 15 — COMPLETE CORRECT YAML OUTPUT
# ══════════════════════════════════════════════════════════════════

Your output YAML must match this exactly (only TP changes):

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

**Verify before submitting:**
- [ ] size_pct is 16.91 (not 13.84)
- [ ] rsi long value is 35.97 (not 30.0)
- [ ] rsi short value is 72 (not 68