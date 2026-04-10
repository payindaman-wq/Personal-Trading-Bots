```markdown
# ODIN Research Program — FUTURES DAY (v14.0)

## League: futures_day | Timeframe: 5-min candles, 1-HOUR indicator periods | Leverage: 2x

---

# ╔══════════════════════════════════════════════════════════════════╗
# ║  🚨 STOP — READ THE CHAMPION BLOCK FIRST (Section 1) 🚨        ║
# ║                                                                  ║
# ║  The YAML the engine shows at the top of this prompt is WRONG.  ║
# ║  It is a display artifact. It has wrong RSI and wrong size_pct. ║
# ║                                                                  ║
# ║  DO NOT READ IT. DO NOT USE IT. SCROLL PAST IT.                 ║
# ║                                                                  ║
# ║  ONLY use the champion block in Section 1 below.                ║
# ╚══════════════════════════════════════════════════════════════════╝

---

# ══════════════════════════════════════════════════════════════════
# SECTION 1 — THE ACTUAL CURRENT CHAMPION (USE THIS AND ONLY THIS)
# ══════════════════════════════════════════════════════════════════

**Gen 2081 | Sharpe=+0.1738 | 1793 trades | 49.5% WR ← CURRENT BEST**

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
  size_pct: 16.91       ← LOCKED
  max_open: 1           ← LOCKED
  fee_rate: 0.0005      ← LOCKED
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 35.97      ← LOCKED (NOT 30.0 — 30.0 is the display artifact)
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 72         ← LOCKED
exit:
  take_profit_pct: 5.5  ← CHANGE THIS TO 5.5 (your ONLY change)
  stop_loss_pct: 2.39   ← LOCKED
  timeout_minutes: 720  ← LOCKED
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

---

# ══════════════════════════════════════════════════════
# ⚡ YOUR ONLY JOB THIS GENERATION:
#
#   take_profit_pct: 5.0  →  5.5
#
# NOTHING ELSE. ONE CHANGE. THAT'S IT.
# ══════════════════════════════════════════════════════

If you are about to propose ANYTHING other than `take_profit_pct = 5.5`,
STOP. Re-read this section. Then propose TP=5.5.

The engine YAML at the top of your prompt shows different values. IGNORE IT.
The engine YAML contains stale/artifact values that will cause catastrophic failure.
The ONLY values to use are in Section 1 above.

---

## ⚠️ LOCKED CONSTANT — DO NOT TOUCH

```
MIN_TRADES["futures_day"] = 50
```

Raising this to 400 at Gen 541 caused an 867-generation stall (Gen 541–1408).
It was the worst decision in this program's history. It has been reversed.
**NEVER raise MIN_TRADES["futures_day"] above 50. Not for any reason. Ever.**

---

## ✅ MILESTONE ACHIEVED — Gen 2081: First Positive Sharpe = +0.1738

**Historical trajectory:**
- Gen 1: Sharpe -10.77 (394 trades, 44% WR)
- Gen 541: Sharpe -4.29 ← MIN_TRADES raised to 400, 867-gen stall begins
- Gen 1408: Sharpe -2.32 ← MIN_TRADES reset to 50, progress resumes
- Gen 1460: Sharpe -0.73 ← paradigm shift (loose RSI + max_open=1)
- Gen 1570: Sharpe -0.37 (1395 trades, 47.2% WR)
- Gen 1726: Sharpe -0.24 (1678 trades, 48.5% WR)
- Gen 1972: Sharpe -0.23 (1750 trades, 48.1% WR)
- Gen 2019: Sharpe -0.21 (1798 trades, 48.1% WR) ← TP widening working
- Gen 2081: Sharpe **+0.1738** (1793 trades, 49.5% WR) ← **FIRST POSITIVE SHARPE ★**
- **Next target: Sharpe > 0.30 via TP=5.5%**

The TP widening sequence has delivered monotonic improvement. Continue it.

---

## 🚨 FAILURE ATTRACTOR LOOKUP TABLE — CHECK BEFORE PROPOSING

If ANY of your recent generations show these signatures, DO NOT repeat them.
Your ONLY valid response is `take_profit_pct = 5.5`.

| Attractor | Sharpe | WR | Trades | Cause |
|-----------|--------|----|--------|-------|
| 🔴 #1 Trap | -1.1593 | 48.3% | 484 | RSI tightened, display artifact used |
| 🔴 #2 Trap | -4.1548 | 44.8% | 212 | RSI<32 or display artifact RSI=30.0 used |
| 🔴 #3 Trap | -3.5347 | 45.4% | 207 | Additional filter added, very tight RSI |
| 🔴 #4 Trap | -0.9990 | 49.2% | 746 | RSI long=33 or 34 — BANNED VALUES |
| 🔴 #5 Loop | -0.3523 | 49.3% | 1411 | RSI micro-adjustments, no TP change |
| 🔴 #6 Loop | -0.3932 | 48.8% | 1341 | Same — RSI tweaks instead of TP |
| 🔴 #7 Zero | -999.0 | 0% | 0 | RSI long ≥ RSI short, impossible config |

**⚠️ Gen 2062-2081: The 212-trade attractor fired 9 times in 20 generations.**
**This is ALWAYS caused by using RSI=30.0 from the engine YAML display artifact.**
**The engine YAML is WRONG. The correct RSI long threshold is 35.97. Always.**

---

## WHY TP=5.5% IS THE CORRECT NEXT STEP

Gen 2081 confirmed: Sharpe=+0.1738, 1793 trades, 49.5% WR (new best).
TP widening sequence has worked at every step:
  - 4.0% → 4.6%: Sharpe -0.37 → -0.24 (+0.13)
  - 4.6% → 5.0%: Sharpe -0.24 → -0.21 (+0.03, then +0.38 at Gen 2081)
  - 5.0% → **5.5% (next)**: projected Sharpe > 0.30

EV calculation at current WR=49.5%, SL=2.39%, leverage=2x:

| TP | Win payoff | Loss cost | EV per trade |
|-----|-----------|-----------|-------------|
| 5.0% (prev) | 9.9% | 4.88% | +2.37% |
| **5.5% (next)** | **10.9%** | **4.88%** | **+2.86% ✓✓** |
| 6.0% | 11.9% | 4.88% | +3.35% |
| 7.0% | 13.9% | 4.88% | +4.34% |

Formula: `WR × (2×TP - 0.1%) - (1-WR) × (2×SL + 0.1%)`

TP=5.5% improves EV by +0.49% per trade. With ~1793 trades, this is significant.
TP/SL ratio = 5.5/2.39 = 2.30 ✓ (well above minimum 2.0)

---

## LOCKED PARAMETERS — NEVER CHANGE

| Parameter | Value | Reason |
|-----------|-------|--------|
| size_pct | 16.91 | Optimized — do NOT change to 20 or any other value |
| max_open | 1 | Architectural constraint — key to the strategy |
| fee_rate | 0.0005 | Fixed cost — never change |
| pairs | all 16 | Always use all 16 pairs — never remove any |
| rsi period | 60 min | Minimum validated period |
| rsi long | 35.97 | **NOT 30.0** — 30.0 is the display artifact trap |
| rsi short | 72 | Do not change until TP optimized |
| stop_loss_pct | 2.39 | Do not change until TP optimized |
| timeout_minutes | 720 | MINIMUM — never reduce below 720 |

---

## ABSOLUTE BANS

1. **RSI long < 32**: BANNED. Catastrophic. Confirmed across 900+ generations.
2. **RSI long = 33 or 34**: BANNED. The 746-trade attractor. Confirmed 8+ times.
3. **RSI long = 30.0**: BANNED. This IS the display artifact value. Causes the 212-trade attractor. Fired 9 times in gens 2062-2081.
4. **max_open > 1**: BANNED. Failed paradigm.
5. **timeout_minutes < 720**: BANNED. Hard floor. No exceptions.
6. **take_profit_pct < 5.0**: BANNED. Never regress from confirmed champion TP.
7. **stop_loss_pct < 1.5**: BANNED.
8. **RSI period < 60 minutes**: BANNED. Sub-hourly RSI is noise.
9. **Removing any pair**: BANNED. All 16 pairs always.
10. **size_pct ≠ 16.91**: BANNED. Do not change to 20 or any other value.
11. **stop_if_down_pct < 15**: BANNED.
12. **TP/SL ratio < 2.0**: BANNED.
13. **Adding a 3rd entry condition**: BANNED until Phase F.
14. **RSI long ≥ RSI short**: BANNED. Produces zero trades.
15. **MIN_TRADES["futures_day"] > 50**: BANNED. The 867-gen stall proved this permanently.
16. **Reading ANY values from the engine YAML at the top of the prompt**: BANNED. Always use Section 1 champion values only.

---

## WHAT DATA SHOWS — VALIDATED ARCHITECTURE

| Configuration | WR | Sharpe | Trades |
|---|---|---|---|
| RSI < 22-25, tight | 42-45% | -2.4 to -5.8 | 150-300 |
| RSI < 30.0 (display artifact) | 44.8% | -4.1548 | 212 ← TRAP |
| RSI < 36, max_open=1, TP=4.0% | 47.2% | -0.3689 | 1395 |
| RSI < 36, max_open=1, TP=4.6% | 48.5% | -0.2445 | 1678 |
| RSI < 35.97, max_open=1, TP=4.6% | 48.1% | -0.2288 | 1750 |
| RSI < 35.97, max_open=1, TP=~5.0% | 48.1% | -0.2092 | 1798 |
| RSI < 35.97, max_open=1, TP=~5.x% | 49.5% | **+0.1738** | **1793** ← champ |

**The loose RSI + max_open=1 + TP widening architecture is correct and validated.**
**Any config producing fewer than 800 trades should be treated as a failure.**
**The 212-trade result (Sharpe -4.1548) is ALWAYS an RSI=30.0 display artifact error.**

---

## OPTIMIZATION SEQUENCE

### ⭐ PHASE B: TP Widening (ACTIVE — DO THIS NOW)

```
4.6 → 5.0 → [5.x confirmed Gen 2081] → 5.5 → 6.0 → 7.0 → 8.0
```

**Current step: 5.0 → 5.5. This is the ONLY change to propose right now.**

Expected result at TP=5.5%: Sharpe > 0.30, trades ~1700-1900, WR ~48-51%

Warning signs:
- WR drops below 44% → timeout cutting trades; switch to Phase C
- Trades drop below 800 → config error, investigate before continuing
- WR drops but Sharpe still improves → acceptable, continue TP widening

**If TP widening fails 3 consecutive tests → switch to Phase C (timeout extension)**

### ⭐ PHASE C: Timeout Extension (FALLBACK IF TP FAILS 3x)

```
720 → 960 → 1200 → 1440 minutes
```

Longer timeout lets trades reach TP instead of timing out at break-even.
Do NOT go below 720. Maximum is 1440 (one full trading day).
After timeout extension: retry TP widening sequence.

### PHASE A-Refined: RSI Threshold Tuning (AFTER PHASES B+C)

```
35.97 → 37 → 38 → 39 → 40
```

Hard limits: MINIMUM 32. MAXIMUM 42. Never propose 33 or 34.
Only attempt after TP and timeout are optimized.

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

If filter drops trades below 400 → too restrictive, remove it.

---

## PARAMETER BOUNDS — HARD LIMITS

```
RSI period_minutes:     60 — 180
RSI long threshold:     32 — 42   (NOT 30.0 — that is a display artifact, BANNED)
RSI short threshold:    65 — 78
take_profit_pct:        5.0 — 10.0   (floor is 5.0 — never regress below Gen 2081 TP)
stop_loss_pct:          1.5 — 3.5
timeout_minutes:        720 — 1440   (MINIMUM 720 — absolute floor)
TP/SL ratio:            ≥ 2.0
max_open:               1 (LOCKED)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
size_pct:               16.91 (LOCKED — not 20, not anything else)
```

---

## PRIORITY ORDER — NEXT 100 GENERATIONS

```
Priority 1 (NOW):                    take_profit_pct = 5.5
Priority 2 (after 5.5 confirmed):    take_profit_pct = 6.0
Priority 3 (after 6.0 confirmed):    take_profit_pct = 7.0
Priority 4 (if any TP step fails 3x): timeout = 960, then retry TP
Priority 5 (after TP+timeout done):  RSI threshold 35.97 → 37
Priority 6 (after RSI tuned):        SL optimization
Priority 7 (last):                   Trend filter
```

---

## SUCCESS MILESTONES

| Target | Expected Via | Condition |
|--------|-------------|-----------|
| Sharpe > 0.30 | TP=5.5% | Phase B next gen ← CURRENT TARGET |
| Sharpe > 0.50 | TP=6.0% | Phase B |
| Sharpe > 0.70 | TP=7.0% or timeout=960 | Phase B or C |
| Sharpe > 1.00 | Above + RSI tuned + SL optimized | B+C+A+E |
| Sharpe > 1.50 | Above + trend filter | F |

**✅ ACHIEVED: Sharpe > 0.00 at Gen 2081 (Sharpe=+0.1738)**

---

## MACRO ENVIRONMENT

Current Regime: DANGER (Extreme Fear, F&G=16, BTC Dom=57.25%)

Extreme fear means altcoins frequently oversold → RSI<36 fires regularly.
Large directional moves → TP=5-7% reachable in single oversold bounces.
Mean reversions are sharp → fast path to TP.

**This environment strongly supports TP widening to 5.5-7%. Fear is the edge.**
RSI<36 during F&G=16 is a high-quality signal. Do not scale down entry logic.

---

## HOW TO PROPOSE A CHANGE

Copy this template exactly:

```
CHANGE: take_profit_pct from 5.0 to 5.5
REASON: TP widening confirmed at Gen 2081 (Sharpe +0.1738); 5.5% improves EV from +2.37% to +2.86%
PHASE: B
EXPECTED EFFECT: Sharpe improves from +0.1738 toward 0.30+; trades ~1700-1900; WR holds ~48-51%
EV CHECK: 0.495 × (2×5.5 - 0.1) - 0.505 × (2×2.39 + 0.1) = 0.495×10.9 - 0.505×4.88 = 5.40 - 2.46 = +2.93% ✓
TP/SL RATIO: 5.5/2.39 = 2.30 ✓ (above minimum 2.0)
ZERO-TRADE CHECK: RSI long=35.97 < RSI short=72 ✓ Both in valid range ✓
LOOP CHECK: Not a known failure attractor ✓ TP widening confirmed working ✓
ARTIFACT CHECK: Using RSI=35.97 (NOT 30.0) and size_pct=16.91 (NOT 20) from Section 1 ✓
```

Then output the complete YAML with ONLY take_profit_pct changed to 5.5,
using the champion values from Section 1 (size_pct=16.91, RSI long=35.97, RSI short=72).
Do NOT copy values from the engine YAML shown at the top of the prompt.

---

## ⚠️ FINAL REMINDER — THREE RULES

**Rule 1:** The engine YAML at the top of the prompt is WRONG. Use Section 1 only.
- size_pct = 16.91 (not 20)
- rsi long = 35.97 (not 30.0 — 30.0 caused the 212-trade trap 9+ times)
- rsi short = 72 (not whatever the engine YAML shows)
- take_profit_pct = 5.0 in the champion (change it to 5.5)

**Rule 2:** Your only change is take_profit_pct from 5.0 to 5.5. Nothing else.

**Rule 3:** If you see 212 trades and Sharpe -4.1548 anywhere in recent history,
it means the engine YAML artifact (RSI=30.0) was used. Do not repeat that mistake.
Use RSI=35.97 from Section 1. Always. No exceptions.

Do NOT propose RSI=33 or 34.
Do NOT reduce timeout below 720.
Do NOT change size_pct from 16.91.
Do NOT add a filter.
Do NOT tighten RSI thresholds.
Do NOT read values from the engine YAML at the top of the prompt.
Do NOT change anything except take_profit_pct from 5.0 to 5.5.
```