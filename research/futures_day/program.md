```markdown
# ODIN Research Program — FUTURES DAY (v13.0)

## League: futures_day | Timeframe: 5-min candles, 1-HOUR indicator periods | Leverage: 2x

---

# ╔══════════════════════════════════════════════════════════════╗
# ║  ⚠️ DISPLAY ARTIFACT WARNING — READ THIS FIRST ⚠️           ║
# ║                                                              ║
# ║  The YAML the engine shows you at the top of this prompt    ║
# ║  is WRONG. It contains these display artifacts:             ║
# ║                                                              ║
# ║    WRONG: size_pct: 20        RIGHT: size_pct: 16.91        ║
# ║    WRONG: rsi value: 30.0     RIGHT: rsi value: 35.97       ║
# ║    WRONG: rsi short: 69.17    RIGHT: rsi short: 72          ║
# ║                                                              ║
# ║  DO NOT use the YAML values. Use the champion below.        ║
# ╚══════════════════════════════════════════════════════════════╝

---

# ══════════════════════════════════════════════════════
# ⚡ YOUR ONLY JOB THIS GENERATION:
#
#   take_profit_pct: 4.6  →  5.0
#
# NOTHING ELSE. ONE CHANGE. THAT'S IT.
# ══════════════════════════════════════════════════════

If you are about to propose anything other than `take_profit_pct = 5.0`,
STOP. Read the failure attractors section below. Then propose TP=5.0.

---

## ⚠️ LOCKED CONSTANT — DO NOT TOUCH

```
MIN_TRADES["futures_day"] = 50
```

Raising this to 400 at Gen 541 caused an 867-generation stall (Gen 541–1408).
It was the worst decision in this program's history. It has been reversed.
**NEVER raise MIN_TRADES["futures_day"] above 50. Not for any reason. Ever.**

---

## THE ACTUAL CURRENT CHAMPION — USE THESE VALUES ONLY

**Gen 1972 | Sharpe=-0.2288 | 1750 trades | 48.1% WR ← CURRENT BEST**

The engine YAML at the top of this prompt shows WRONG values. Ignore it.
Build your proposal from this champion ONLY:

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
  size_pct: 16.91       ← LOCKED — do not change to 20
  max_open: 1           ← LOCKED — do not change
  fee_rate: 0.0005      ← LOCKED — do not change
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 35.97      ← LOCKED — do not tighten — NOT 30.0
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 72         ← LOCKED — do not change — NOT 69.17
exit:
  take_profit_pct: 4.6  ← CHANGE THIS TO 5.0 (your ONLY change)
  stop_loss_pct: 2.39   ← LOCKED
  timeout_minutes: 720  ← LOCKED (minimum — never reduce)
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

---

## 🚨 FAILURE ATTRACTOR LOOKUP TABLE — CHECK BEFORE PROPOSING

Before you write your proposal, check the last 20 generations. If you see
ANY of these signatures, your ONLY valid response is `take_profit_pct = 5.0`.

| Attractor | Sharpe | WR | Trades | Cause |
|-----------|--------|----|--------|-------|
| 🔴 #1 Trap | -1.1593 | 48.3% | 484 | RSI tightened, display artifact used |
| 🔴 #2 Trap | -4.1548 | 44.8% | 212 | RSI<32 or display artifact (30.0) used |
| 🔴 #3 Trap | -3.5347 | 45.4% | 207 | Additional filter added, very tight RSI |
| 🔴 #4 Trap | -0.9990 | 49.2% | 746 | RSI long=33 or 34 — BANNED VALUES |
| 🔴 #5 Loop | -0.3523 | 49.3% | 1411 | RSI micro-adjustments, no TP change |
| 🔴 #6 Loop | -0.3932 | 48.8% | 1341 | Same — RSI tweaks instead of TP |
| 🔴 #7 Zero | -999.0 | 0% | 0 | RSI long ≥ RSI short, impossible config |

**⚠️ Gen 1953-1971 saw the 212-trade attractor 7 times in 19 generations.**
**This is caused by reading RSI=30.0 from the display artifact YAML.**
**The correct RSI long threshold is 35.97. Always. No exceptions.**

If recent history shows these patterns → propose TP=5.0 immediately.
If you are unsure what to propose → propose TP=5.0.
If you have any creative ideas → suppress them and propose TP=5.0.

---

## WHY TP=5.0% IS THE CORRECT NEXT STEP

Gen 1972 confirmed: Sharpe=-0.2288, 1750 trades, 48.1% WR (new best).
Gen 1726 proved TP widening works: 4.0%→4.6% improved Sharpe AND trades AND WR.
Gen 1972 continued that improvement: Sharpe -0.2445→-0.2288, trades 1678→1750.

EV calculation at current WR=48.1%, SL=2.39%, leverage=2x:

| TP | Win payoff | Loss cost | EV per trade |
|-----|-----------|-----------|-------------|
| 4.6% (now) | 9.1% | 4.88% | +1.87% |
| **5.0% (next)** | **9.9%** | **4.88%** | **+2.26% ✓✓** |
| 5.5% | 10.9% | 4.88% | +2.67% |
| 6.0% | 11.9% | 4.88% | +3.20% |

Formula: `WR × (2×TP - 0.1%) - (1-WR) × (2×SL + 0.1%)`

TP=5.0% improves EV by +0.39% per trade. With 1750 trades, this is significant.
TP/SL ratio = 5.0/2.39 = 2.09 ✓ (above minimum 2.0)

**The TP widening sequence is working. Continue it.**

---

## LOCKED PARAMETERS — NEVER CHANGE

| Parameter | Value | Reason |
|-----------|-------|--------|
| size_pct | 16.91 | Optimized — do NOT revert to 20 |
| max_open | 1 | Architectural constraint — key to the strategy |
| fee_rate | 0.0005 | Fixed cost — never change |
| pairs | all 16 | Always use all 16 pairs |
| rsi period | 60 min | Minimum validated period |
| rsi long | 35.97 | Do not change until TP optimized |
| rsi short | 72 | Do not change until TP optimized |
| stop_loss_pct | 2.39 | Do not change until TP optimized |
| timeout_minutes | 720 | MINIMUM — never reduce below 720 |

---

## ABSOLUTE BANS

1. **RSI long < 32**: BANNED. Catastrophic. Confirmed across 900+ generations.
2. **RSI long = 33 or 34**: BANNED. The 746-trade attractor. Confirmed 8+ times.
3. **RSI long = 30.0**: BANNED. This is the display artifact value. Using it causes the 212-trade attractor.
4. **max_open > 1**: BANNED. Failed paradigm.
5. **timeout_minutes < 720**: BANNED. Hard floor. No exceptions.
6. **take_profit_pct < 4.6**: BANNED. Never regress from confirmed champion TP.
7. **stop_loss_pct < 1.5**: BANNED.
8. **RSI period < 60 minutes**: BANNED. Sub-hourly RSI is noise.
9. **Removing any pair**: BANNED. All 16 pairs always.
10. **size_pct ≠ 16.91**: BANNED. Do not change to 20 or any other value.
11. **stop_if_down_pct < 15**: BANNED.
12. **TP/SL ratio < 2.0**: BANNED.
13. **Adding a 3rd entry condition**: BANNED until Phase F.
14. **RSI long ≥ RSI short**: BANNED. Produces zero trades.
15. **MIN_TRADES["futures_day"] > 50**: BANNED. The 867-gen stall proved this permanently.
16. **Reading values from the engine YAML**: BANNED. Use the champion values in this document.

---

## WHAT DATA SHOWS — VALIDATED ARCHITECTURE

| Configuration | WR | Sharpe | Trades |
|---|---|---|---|
| RSI < 22-25, tight | 42-45% | -2.4 to -5.8 | 150-300 |
| RSI < 30.0 (display artifact) | 44.8% | -4.1548 | 212 ← TRAP |
| RSI < 36, max_open=1, TP=4.0% | 47.2% | -0.3689 | 1395 |
| RSI < 36, max_open=1, TP=4.6% | 48.5% | -0.2445 | 1678 |
| RSI < 35.97, max_open=1, TP=4.6% | 48.1% | **-0.2288** | **1750** ← champ |

**The loose RSI + max_open=1 + TP widening architecture is correct and validated.**
**Any config producing fewer than 800 trades should be treated as a failure.**

---

## OPTIMIZATION SEQUENCE

### ⭐ PHASE B: TP Widening (ACTIVE — DO THIS NOW)

```
4.6 → 5.0 → 5.5 → 6.0 → 7.0 → 8.0
```

**Current step: 4.6 → 5.0. This is the ONLY change to propose right now.**

Expected result at TP=5.0%: Sharpe > -0.20, trades ~1700-1900, WR ~47-50%

Warning signs:
- WR drops below 44% → timeout cutting trades; switch to Phase C
- Trades drop below 800 → config error, investigate before continuing
- WR drops but Sharpe still improves → acceptable, continue

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
RSI long threshold:     32 — 42   (NOT 30.0 — that is a display artifact)
RSI short threshold:    65 — 78
take_profit_pct:        4.6 — 10.0   (floor is 4.6 — never regress)
stop_loss_pct:          1.5 — 3.5
timeout_minutes:        720 — 1440   (MINIMUM 720 — absolute floor)
TP/SL ratio:            ≥ 2.0
max_open:               1 (LOCKED)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
size_pct:               16.91 (LOCKED — not 20)
```

---

## PRIORITY ORDER — NEXT 100 GENERATIONS

```
Priority 1 (NOW):                    take_profit_pct = 5.0
Priority 2 (after 5.0 confirmed):    take_profit_pct = 5.5
Priority 3 (after 5.5 confirmed):    take_profit_pct = 6.0
Priority 4 (if any TP step fails 3x): timeout = 960, then retry TP
Priority 5 (after TP+timeout done):  RSI threshold 35.97 → 37
Priority 6 (after RSI tuned):        SL optimization
Priority 7 (last):                   Trend filter
```

---

## SUCCESS MILESTONES

| Target | Expected Via | Condition |
|--------|-------------|-----------|
| Sharpe > -0.20 | TP=5.0% | Phase B next gen |
| Sharpe > -0.10 | TP=5.5% | Phase B |
| Sharpe > 0.00 | TP=6.0% or timeout=960 | Phase B or C |
| Sharpe > 0.30 | TP=6.0% + timeout=960 + RSI tuned | B+C+A |
| Sharpe > 0.70 | Above + SL optimized | E |
| Sharpe > 1.00 | Above + trend filter | F |

**Historical trajectory:**
- Gen 1: Sharpe -10.77 (394 trades, 44% WR)
- Gen 541: Sharpe -4.29 ← MIN_TRADES raised to 400, 867-gen stall begins
- Gen 1408: Sharpe -2.32 ← MIN_TRADES reset to 50, progress resumes
- Gen 1460: Sharpe -0.73 ← paradigm shift (loose RSI + max_open=1)
- Gen 1570: Sharpe -0.37 (1395 trades, 47.2% WR)
- Gen 1726: Sharpe -0.24 (1678 trades, 48.5% WR)
- Gen 1972: Sharpe -0.23 (1750 trades, 48.1% WR) ← **current best ★**
- **Next target: Sharpe > -0.20 via TP=5.0%**

---

## MACRO ENVIRONMENT

Current Regime: DANGER (Extreme Fear, F&G=16, BTC Dom=57.16%)

Extreme fear means altcoins frequently oversold → RSI<36 fires regularly.
Large directional moves → TP=5-7% reachable in single oversold bounces.
Mean reversions are sharp → fast path to TP.

**This environment strongly supports TP widening to 5-7%. Fear is the edge.**
RSI<36 during F&G=16 is a high-quality signal. Do not scale down entry logic.

---

## HOW TO PROPOSE A CHANGE

Copy this template exactly:

```
CHANGE: take_profit_pct from 4.6 to 5.0
REASON: TP widening confirmed at Gen 1726 and 1972; 5.0% improves EV from +1.87% to +2.26%
PHASE: B
EXPECTED EFFECT: Sharpe improves from -0.2288 toward -0.20; trades ~1700-1900; WR holds ~47-50%
EV CHECK: 0.481 × (2×5.0 - 0.1) - 0.519 × (2×2.39 + 0.1) = 0.481×9.9 - 0.519×4.88 = 4.76 - 2.53 = +2.23% ✓
ZERO-TRADE CHECK: RSI long=35.97 < RSI short=72 ✓ Both in valid range ✓
LOOP CHECK: Not a known failure attractor ✓ TP widening confirmed working ✓
ATTRACTOR CHECK: Recent gens show 212-trade trap (display artifact) — using correct RSI=35.97 ✓
```

Then output the complete YAML with ONLY take_profit_pct changed to 5.0,
using the champion values above (size_pct=16.91, RSI long=35.97, RSI short=72).
Do NOT copy values from the engine YAML shown at the top of the prompt.

---

## ⚠️ FINAL REMINDER — THREE RULES

**Rule 1:** The engine YAML is wrong. Use the champion values in this document.
- size_pct = 16.91 (not 20)
- rsi long = 35.97 (not 30.0)
- rsi short = 72 (not 69.17)

**Rule 2:** Your only change is take_profit_pct from 4.6 to 5.0. Nothing else.

**Rule 3:** If you see the 212-trade attractor in recent history, it means
someone used RSI=30.0 from the display artifact. Do not repeat that mistake.
Use RSI=35.97.

Do NOT propose RSI=33 or 34.
Do NOT reduce timeout below 720.
Do NOT change size_pct from 16.91.
Do NOT add a filter.
Do NOT tighten RSI thresholds.
Do NOT read values from the engine YAML.
Do NOT change anything except take_profit_pct from 4.6 to 5.0.
```