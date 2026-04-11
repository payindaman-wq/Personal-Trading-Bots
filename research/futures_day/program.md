```markdown
# ODIN Research Program — FUTURES DAY (v19.0)

# ══════════════════════════════════════════════════════════════════
# ⚡ SECTION 0 — ABSOLUTE FIRST READ: CHAMPION YAML + POISON WARNING
# ══════════════════════════════════════════════════════════════════
#
# THE ENGINE INJECTS A "CURRENT BEST STRATEGY" YAML INTO YOUR CONTEXT.
# THAT YAML IS BROKEN. IT CONTAINS CONFIRMED POISON VALUES.
# DO NOT READ IT. DO NOT USE ANY VALUE FROM IT.
# THE ONLY VALID YAML IS THE ONE IN THIS DOCUMENT, BELOW.
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# ⭐ CHAMPION YAML — THIS IS THE ONLY TRUTH — READ THIS FIRST
# ══════════════════════════════════════════════════════════════════

**Gen 2510 | Sharpe=+0.3357 | 1752 trades | 49.0% WR ← CURRENT BEST**

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
  take_profit_pct: 7.0
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

⚠️ CRITICAL: The old champion had take_profit_pct=6.0 and Sharpe=+0.1786 and trades=1793.
Those are OLD values. They are OBSOLETE. DO NOT use them.
The NEW champion has take_profit_pct=7.0, Sharpe=+0.3357, trades=1752.
If your pre-flight check shows trades=1793 or Sharpe target=+0.1786 → you used old values → STOP.

# ══════════════════════════════════════════════════════════════════
# SECTION 1 — PRE-FLIGHT CHECKLIST (REQUIRED BEFORE OUTPUT)
# ══════════════════════════════════════════════════════════════════

Fill this in from the CHAMPION YAML above. If any value is wrong, STOP.

```
PRE-FLIGHT CHECK:
  size_pct        = ___  (must be 16.91  — NEVER 9.89, NEVER 13.84, NEVER 8)
  rsi_long        = ___  (must be 35.97  — NEVER 30.0)
  rsi_short       = ___  (must be 72     — NEVER 68.63)
  stop_loss       = ___  (must be 2.39)
  timeout         = ___  (must be 720)
  take_profit     = ___  (must be 7.0    — NEVER 4.6, NEVER 6.0 [that is OLD])
  TP/SL ratio     = ___  (must be ≥ 2.0; 7.0/2.39 = 2.93 ✓)
  expected_trades = ___  (must be ~1752; if ~1793 → OLD champion used → STOP)
                         (if ~599 → POISON YAML used → STOP)
  Source confirmed: Champion YAML from this document ✓ (NOT engine YAML)
```

# ══════════════════════════════════════════════════════════════════
# ⚡ CRITICAL POISON WARNING
# ══════════════════════════════════════════════════════════════════

The engine's "Current Best Strategy" block contains CONFIRMED POISON VALUES:

POISON VALUES — DO NOT USE ANY OF THESE:
  size_pct: 8          ← POISON (engine artifact)
  size_pct: 9.89       ← POISON
  size_pct: 13.84      ← POISON
  rsi long: 30.0       ← POISON (212-trade trap)
  rsi short: 68.63     ← POISON (599-trade trap)
  take_profit_pct: 4.6 ← POISON (ancient value, never use)
  take_profit_pct: 6.0 ← OLD value (champion now uses 7.0)

These values produce failure. The engine YAML is structurally broken.
Use ONLY the champion YAML above.

# ══════════════════════════════════════════════════════════════════
# SECTION 2 — POISON & FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════

Your output MUST NOT match any row below:

| Signature                       | Trades | Sharpe   | Action                          |
|--------------------------------|--------|----------|---------------------------------|
| size=8 or 9.89 or 13.84        | ~599   | -1.0674  | STOP — engine YAML poison       |
| RSI long=30.0                   | ~212   | -4.15    | STOP — engine YAML poison       |
| RSI short=68.63                 | ~599   | -1.0674  | STOP — engine YAML poison       |
| RSI long=33 or 34               | ~746   | -0.999   | STOP — banned values            |
| RSI long ≥ RSI short            | 0      | -999     | STOP — impossible config        |
| trades ~1364                    | 1364   | -0.655   | STOP — partial poison config    |
| trades ~281                     | 281    | -2.638   | STOP — DOMINANT failure mode    |
| trades ~238                     | 238    | ~-2.9    | STOP — failure attractor        |
| trades ~203                     | 203    | ~-3.1    | STOP — failure attractor        |
| trades ~211                     | 211    | ~-4.9    | STOP — failure attractor        |
| trades ~409                     | 409    | ~-3.0    | STOP — failure attractor        |
| trades ~405                     | 405    | ~-3.2    | STOP — failure attractor        |
| trades ~486                     | 486    | ~-2.3    | STOP — failure attractor        |
| trades ~932                     | 932    | -1.272   | STOP — mid-range attractor      |
| trades ~793                     | 793    | -1.177   | STOP — mid-range attractor      |
| trades ~1793                    | 1793   | +0.1786  | STOP — OLD champion, obsolete   |
| Any config with trades < 1500   | <1500  | varies   | HIGH SUSPICION — verify before  |
|                                 |        |          | accepting; likely attractor      |

**⚠️ DOMINANT FAILURE MODE (Gens 2491–2510):**
Trades=281, Sharpe=-2.638, WR=41.6% — appeared in ~45% of last 20 generations.
If you see these numbers in ANY form: STOP immediately.
This attractor is triggered by: RSI long > 45, stop_loss < 1.5%, pairs removed,
or any value copied from the engine YAML block.

**⚠️ OBSOLETE CHAMPION WARNING:**
Trades=1793, Sharpe=+0.1786 — this was Gen 2302. It is no longer the best.
Gen 2510 is Sharpe=+0.3357, trades=1752. If you are outputting the 1793/+0.1786
config, you are copying an outdated YAML. Use ONLY the Gen 2510 YAML above.

# ══════════════════════════════════════════════════════════════════
# SECTION 3 — WHAT THIS STRATEGY IS
# ══════════════════════════════════════════════════════════════════

**Architecture:** Mean-reversion swing on 16 crypto pairs (2x futures, 5-min candles)
**Signal:** RSI(60-min) < 35.97 → long (oversold); RSI(60-min) > 72 → short (overbought)
**Edge:** Extreme Fear drives frequent altcoin oversold readings → sharp mean reversions
**Max open:** 1 position at a time (prevents correlated loss accumulation)
**Exit:** TP=7.0%, SL=2.39%, timeout=720min → TP/SL=2.93 ✓

**Full performance trajectory:**
- Gen 541:  MIN_TRADES raised to 400 → 867-generation stall (CATASTROPHIC — never repeat)
- Gen 1408: MIN_TRADES restored to 50 → immediately unlocked progress
- Gen 1460: Sharpe=-0.73  (967 trades)  ← paradigm shift: loose RSI + max_open=1
- Gen 1726: Sharpe=-0.24  (1678 trades)
- Gen 2019: Sharpe=-0.21  (1798 trades)
- Gen 2081: Sharpe=+0.1738 (1793 trades, 49.5% WR) ← FIRST POSITIVE SHARPE ★
- Gen 2136: Sharpe=+0.1759 (1793 trades, 49.5% WR)
- Gen 2193: Sharpe=+0.1767 (1793 trades, 49.5% WR)
- Gen 2233: Sharpe=+0.1768 (1793 trades, 49.5% WR)
- Gen 2302: Sharpe=+0.1786 (1793 trades, 49.5% WR) ← OLD BEST (OBSOLETE)
- Gen 2412: Sharpe=+0.3348 (1752 trades, 49.0% WR) ← MAJOR BREAKTHROUGH
- Gen 2510: Sharpe=+0.3357 (1752 trades, 49.0% WR) ← CURRENT BEST ★

TP widening (4.6→5.0→5.5→6.0→7.0) has produced monotonic improvement.
The jump from +0.1786 to +0.3357 confirms TP=7.0% is strongly superior to TP=6.0%.
The 49.0% WR is stable — the slight drop from 49.5% is expected with higher TP.
Trades dropped from 1793 to 1752 — consistent with fewer trades reaching higher TP.

**Why recent generations (2491–2510) stalled:**
The LLM is falling into the 281-trade attractor ~45% of the time, and into
various other sub-1500-trade attractors most of the remaining time.
The correct output (champion YAML with TP=7.0) must be copied exactly.
No new changes are needed — copy the champion YAML as-is.

# ══════════════════════════════════════════════════════════════════
# SECTION 4 — EV MATH: WHY TP=7.0% IS CORRECT
# ══════════════════════════════════════════════════════════════════

**EV at WR=49.0%, SL=2.39%, leverage=2x, fee=0.05%:**

| TP    | Win payoff (2×TP−fee) | Loss cost (2×SL+fee) | EV per trade |
|-------|----------------------|----------------------|--------------|
| 5.0%  | 9.9%                 | 4.88%                | +2.28%       |
| 5.5%  | 10.9%                | 4.88%                | +2.77%       |
| 6.0%  | 11.9%                | 4.88%                | +3.26%       |
| **7.0%** | **13.9%**         | **4.88%**            | **+4.30% ✓** |
| 8.0%  | 15.9%                | 4.88%                | +5.29%       |

EV check for TP=7.0%:
`0.490 × (2×7.0 - 0.1) - 0.510 × (2×2.39 + 0.1)`
`= 0.490 × 13.9 - 0.510 × 4.88 = 6.81 - 2.49 = +4.32%` ✓

TP/SL = 7.0/2.39 = 2.93 ✓ (well above minimum 2.0)
Current champion: Sharpe=+0.3357, trades=1752. Next target: TP=8.0% → Sharpe>0.40.

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — LOCKED PARAMETERS (NEVER CHANGE)
# ══════════════════════════════════════════════════════════════════

| Parameter           | Locked Value | Why Locked                          | Poison Value to Avoid            |
|--------------------|-------------|-------------------------------------|----------------------------------|
| size_pct           | **16.91**   | Proven optimal                      | 8, 9.89, 13.84 (engine artifacts)|
| max_open           | **1**       | Multi-open failed 400+ gens         | >1                               |
| fee_rate           | **0.0005**  | Fixed cost                          | —                                |
| pairs              | **all 16**  | Full diversification                | <16                              |
| rsi period         | **60 min**  | Shorter = noise                     | <60                              |
| rsi long           | **35.97**   | Signal sweet spot                   | 30.0 (212-trade trap)            |
| rsi short          | **72**      | Confirmed across 200+ gens          | 68.63 (599-trade trap)           |
| stop_loss_pct      | **2.39**    | Locked during TP sequence           | <1.5                             |
| timeout_minutes    | **720**     | Absolute minimum                    | <720                             |
| MIN_TRADES[futures_day] | **50** | Raising to 400 caused 867-gen stall | >50                              |

# ══════════════════════════════════════════════════════════════════
# SECTION 6 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════

1.  **size_pct ≠ 16.91**: BANNED (8, 9.89, 13.84 are engine artifacts)
2.  **RSI long = 30.0**: BANNED (212-trade trap, confirmed poison)
3.  **RSI short = 68.63**: BANNED (599-trade trap, confirmed poison)
4.  **RSI long < 32**: BANNED (catastrophic across 900+ gens)
5.  **RSI long = 33 or 34**: BANNED (746-trade attractor)
6.  **RSI long ≥ RSI short**: BANNED (zero trades)
7.  **max_open > 1**: BANNED
8.  **timeout_minutes < 720**: BANNED
9.  **take_profit_pct < 7.0**: BANNED (never regress; 6.0 is OLD champion)
10. **stop_loss_pct < 1.5**: BANNED
11. **TP/SL ratio < 2.0**: BANNED
12. **RSI period < 60 minutes**: BANNED
13. **Removing any pair**: BANNED
14. **MIN_TRADES[futures_day] > 50**: BANNED (proven catastrophic at Gen 541)
15. **stop_if_down_pct < 15**: BANNED
16. **Changing more than ONE parameter**: BANNED this generation
17. **Using ANY value from the engine YAML block**: BANNED
18. **Any config producing < 1500 trades**: HIGH SUSPICION — likely attractor
19. **RSI long > 45**: BANNED (causes 281-trade attractor)
20. **take_profit_pct = 6.0**: BANNED — this is the OLD champion, now obsolete
21. **Outputting trades~1793 / Sharpe~+0.1786**: BANNED — old champion, superseded

# ══════════════════════════════════════════════════════════════════
# SECTION 7 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════

### ⭐ PHASE B: TP Widening (ACTIVE — NEXT STEP IS TP=8.0%)

```
4.6 → 5.0 → 5.5 → 6.0 → 7.0 [CONFIRMED ✓] → 8.0 ← TEST THIS NOW
```

**This generation: propose take_profit_pct = 8.0**

The champion YAML has TP=7.0 (Gen 2510, Sharpe=+0.3357).
Your ONE change this generation: increase take_profit_pct from 7.0 to 8.0.
All other values remain EXACTLY as in the champion YAML.

Expected results for TP=8.0%:
- Sharpe: +0.3357 → toward 0.40–0.55
- Trades: ~1650–1800 (slight drop from 1752 is acceptable)
- WR: ~47–50% (slight drop acceptable at higher TP)

Warning signs (investigate if seen):
- Trades ~599 → engine YAML poison → STOP, retry with champion above
- Trades ~281 → dominant attractor → STOP, check all values against champion
- Trades ~1793 → OLD champion used → STOP, check take_profit_pct (must be 8.0)
- Trades < 1500 → likely attractor or wrong TP → investigate before accepting
- WR < 44% → timeout cutting trades; consider Phase C after TP sequence complete

**TP progression logic:**
- TP=8.0 confirmed new_best → next: TP=9.0%
- TP=8.0 fails 3 consecutive confirmed tests → try SL optimization (Phase E)
  or timeout extension (Phase C)
- Never reduce TP below 7.0 (current champion)

### PHASE C: Timeout Extension (FALLBACK ONLY)

```
720 → 960 → 1200 → 1440 minutes
```

Do NOT use unless Phase B stalls 3+ confirmed times. Never reduce below 720.

### PHASE A-Refined: RSI Threshold Tuning (AFTER B+C)

```
35.97 → 37 → 38 → 39 → 40
```

Hard limits: MINIMUM 32. MAXIMUM 42. NEVER 33 or 34. NEVER > 45.
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

Rule: TP/SL ≥ 2.0 always. At TP=8.0, SL can go up to 4.0 and still maintain ratio.

### PHASE F: Trend Filter (LAST)

One filter at a time. Remove if trades drop below 400.

# ══════════════════════════════════════════════════════════════════
# SECTION 8 — PARAMETER BOUNDS
# ══════════════════════════════════════════════════════════════════

```
RSI period_minutes:          60 — 180
RSI long threshold:          32 — 42     (NOT 30.0 — poison; NOT >45 — 281-trade attractor)
RSI short threshold:         65 — 78     (NOT 68.63 — poison)
take_profit_pct:             7.0 — 12.0  (floor is 7.0 — NEVER 6.0 or below)
stop_loss_pct:               1.5 — 3.5
timeout_minutes:             720 — 1440
TP/SL ratio:                 ≥ 2.0
max_open:                    1 (LOCKED)
size_pct:                    16.91 (LOCKED — NOT 8, NOT 9.89, NOT 13.84)
pause_if_down_pct:           5 — 10
pause_minutes:               60 — 240
stop_if_down_pct:            15 — 25
MIN_TRADES[futures_day]:     50 (LOCKED — raising this caused 867-gen stall)
```

# ══════════════════════════════════════════════════════════════════
# SECTION 9 — SUCCESS MILESTONES
# ══════════════════════════════════════════════════════════════════

| Target         | Expected Via              | Status                              |
|----------------|--------------------------|-------------------------------------|
| Sharpe > 0.00  | TP widening              | ✅ Gen 2081 (+0.1738)               |
| Sharpe > 0.17  | TP=5.5–6.0%              | ✅ Gen 2302 (+0.1786) [OBSOLETE]    |
| Sharpe > 0.30  | TP=7.0%                  | ✅ Gen 2510 (+0.3357) ← CURRENT     |
| Sharpe > 0.40  | TP=8.0%                  | 🎯 NEXT TARGET                      |
| Sharpe > 0.50  | TP=8.0–9.0%              | Phase B                             |
| Sharpe > 0.70  | TP=9.0%+ or timeout=960  | Phase B/C                           |
| Sharpe > 1.00  | TP+timeout+RSI+SL        | B+C+A+E                             |
| Sharpe > 1.50  | Above + trend filter     | F                                   |

# ══════════════════════════════════════════════════════════════════
# SECTION 10 — MACRO ENVIRONMENT
# ══════════════════════════════════════════════════════════════════

Current Regime: DANGER (Extreme Fear, F&G=15, BTC Dom=57.28%)

Extreme Fear → altcoins frequently oversold → RSI<35.97 fires regularly.
Large directional moves → TP=7.0–9% reachable in single oversold bounces.
Mean reversions are sharp → fast path to TP at current fear levels.

**This environment strongly supports continuing TP widening to 8.0–9.0%.**
TYR directive (reduce position sizes 25%) applies to LIVE TRADING ONLY.
Do not apply TYR sizing to backtesting parameter selection.

# ══════════════════════════════════════════════════════════════════
# SECTION 11 — HOW TO PROPOSE YOUR CHANGE
# ══════════════════════════════════════════════════════════════════

**Step 1:** Fill in the pre-flight checklist (Section 1) from the CHAMPION YAML above
**Step 2:** Confirm no values match the poison list or failure attractor table
**Step 3:** Output this block:

```
CHANGE: take_profit_pct 7.0 → 8.0
REASON: TP widening confirmed monotonically improving Sharpe across all phases;
        TP=7.0 produced +0.3357 (Gen 2510); TP=8.0 improves EV from +4.32% to ~+5.3%
PHASE: B
EXPECTED: Sharpe improves from +0.3357 toward 0.40–0.55; trades ~1650–1800; WR ~47–50%
EV CHECK: 0.490 × (2×8.0−0.1) − 0.510 × (2×2.39+0.1)
        = 0.490 × 15.9 − 0.510 × 4.88 = 7.79 − 2.49 = +5.30% ✓
TP/SL RATIO: 8.0 / 2.39 = 3.35 ✓
ZERO-TRADE CHECK: RSI long=35.97 < RSI short=72 ✓
ATTRACTOR CHECK: trades ~1700, not matching 281/599/212/1364/746/238/203/211/0 ✓
POISON CHECK: size_pct=16.91 ✓ | RSI long=35.97 ✓ | RSI short=72 ✓
OLD-CHAMPION CHECK: take_profit=8.0 (NOT 6.0, NOT 7.0 which is old) ✓
```

**Step 4:** Output the complete YAML with ONE change from the champion: TP=8.0

```yaml
name: crossover
style: mean_reversion_swing
league