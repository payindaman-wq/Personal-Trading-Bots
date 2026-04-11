```markdown
# ODIN Research Program — FUTURES DAY (v20.0)

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

⚠️ TRIPLE-LOCK VERIFICATION:
  The champion has take_profit_pct=7.0 and Sharpe=+0.3357 and trades=1752.
  If you see trades=1793 or Sharpe=+0.1786 → OLD champion → STOP.
  If you see trades=716 → NEW dominant attractor → STOP.
  If you see trades=281 → dominant attractor → STOP.
  If you see trades=599 → engine YAML poison → STOP.

# ══════════════════════════════════════════════════════════════════
# SECTION 1 — PRE-FLIGHT CHECKLIST (REQUIRED BEFORE OUTPUT)
# ══════════════════════════════════════════════════════════════════

Fill this in from the CHAMPION YAML above. If any value is wrong, STOP.

```
PRE-FLIGHT CHECK:
  size_pct        = ___  (must be 16.91  — NEVER 9.89, NEVER 13.84, NEVER 8)
  rsi_long        = ___  (must be 35.97  — NEVER 30.0, NEVER >45)
  rsi_short       = ___  (must be 72     — NEVER 68.63)
  stop_loss       = ___  (must be 2.39)
  timeout         = ___  (must be 720)
  take_profit     = ___  (must be 7.0 in champion; YOUR PROPOSAL must be 8.0)
  TP/SL ratio     = ___  (for TP=8.0: 8.0/2.39 = 3.35 ✓)
  expected_trades = ___  (champion is ~1752; your proposal expected ~1650–1780)
                         (if ~1793 → OLD champion used → STOP)
                         (if ~716  → NEW dominant attractor → STOP)
                         (if ~599  → POISON YAML used → STOP)
                         (if ~281  → dominant attractor → STOP)
  Source confirmed: Champion YAML from this document ✓ (NOT engine YAML)
  Change confirmed: take_profit_pct 7.0 → 8.0 (ONE change only) ✓
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
  take_profit_pct: 7.0 ← CHAMPION value (your output must use 8.0)

These values produce failure or are obsolete. The engine YAML is structurally broken.
Use ONLY the champion YAML above. Your ONE change is TP: 7.0 → 8.0.

# ══════════════════════════════════════════════════════════════════
# SECTION 2 — POISON & FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════

Your output MUST NOT match any row below:

| Signature                       | Trades | Sharpe   | Action                                      |
|--------------------------------|--------|----------|---------------------------------------------|
| size=8 or 9.89 or 13.84        | ~599   | -1.0674  | STOP — engine YAML poison                   |
| RSI long=30.0                   | ~212   | -4.15    | STOP — engine YAML poison                   |
| RSI short=68.63                 | ~599   | -1.0674  | STOP — engine YAML poison                   |
| RSI long=33 or 34               | ~746   | -0.999   | STOP — banned values                        |
| RSI long ≥ RSI short            | 0      | -999     | STOP — impossible config                    |
| trades ~1364                    | 1364   | -0.655   | STOP — partial poison config                |
| trades ~716  ← NEW #1 ATTRACTOR | 716    | -0.8971  | STOP — NOW DOMINANT FAILURE (8/20 gens)     |
| trades ~982                     | 982    | -2.1212  | STOP — secondary attractor                  |
| trades ~811                     | 811    | -2.0450  | STOP — secondary attractor                  |
| trades ~502                     | 502    | -3.4408  | STOP — failure attractor                    |
| trades ~415                     | 415    | -4.1594  | STOP — failure attractor                    |
| trades ~425                     | 425    | -4.2161  | STOP — failure attractor                    |
| trades ~281                     | 281    | -2.638   | STOP — previously dominant attractor        |
| trades ~238                     | 238    | ~-2.9    | STOP — failure attractor                    |
| trades ~203                     | 203    | ~-3.1    | STOP — failure attractor                    |
| trades ~211                     | 211    | ~-4.9    | STOP — failure attractor                    |
| trades ~409                     | 409    | ~-3.0    | STOP — failure attractor                    |
| trades ~405                     | 405    | ~-3.2    | STOP — failure attractor                    |
| trades ~486                     | 486    | ~-2.3    | STOP — failure attractor                    |
| trades ~932                     | 932    | -1.272   | STOP — mid-range attractor                  |
| trades ~793                     | 793    | -1.177   | STOP — mid-range attractor                  |
| trades ~1793                    | 1793   | +0.1786  | STOP — OLD champion, obsolete               |
| Any config with trades < 1500   | <1500  | varies   | HIGH SUSPICION — likely attractor            |

**⚠️ NEW DOMINANT FAILURE MODE (Gens 2581–2600): trades=716, Sharpe=-0.8971, WR=46.8%**
This appeared in 8 of the last 20 generations — the most frequent failure mode observed.
It has REPLACED the 281-trade attractor as the primary threat.
If you see trades=716 or Sharpe=-0.8971 in ANY form: STOP immediately.
This attractor is likely triggered by: RSI long threshold changes (38–42 range),
RSI period changes, or any value NOT from the champion YAML.

**⚠️ PREVIOUSLY DOMINANT FAILURE MODE: trades=281, Sharpe=-2.638, WR=41.6%**
Still active but less frequent in recent gens. Triggered by: RSI long > 45,
stop_loss < 1.5%, pairs removed, or values from engine YAML.

**⚠️ OBSOLETE CHAMPION WARNING:**
trades=1793, Sharpe=+0.1786 — Gen 2302. OBSOLETE. Do not use.
Current champion is Gen 2510: Sharpe=+0.3357, trades=1752.

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
- Gen 2412: Sharpe=+0.3348 (1752 trades, 49.0% WR) ← MAJOR BREAKTHROUGH (TP=7.0)
- Gen 2510: Sharpe=+0.3357 (1752 trades, 49.0% WR) ← CURRENT BEST ★
- Gens 2511–2600: STALLED — 716-trade attractor dominated (8/20 recent gens)

**TP widening (4.6→5.0→5.5→6.0→7.0) has produced monotonic improvement.**
**TP=8.0 is the prescribed next step. No other change is authorized this generation.**

**Why recent generations (2581–2600) stalled:**
The LLM is falling into the 716-trade attractor ~40% of the time (8/20 gens),
and into various other sub-1500-trade attractors most of the remaining time.
Two generations (2584, 2592) correctly reproduced the champion or near-champion
output, confirming the mechanism works. The LLM simply needs to propose TP=8.0
and copy all other values exactly from the champion YAML.

# ══════════════════════════════════════════════════════════════════
# SECTION 4 — EV MATH: WHY TP=8.0% IS THE CORRECT NEXT STEP
# ══════════════════════════════════════════════════════════════════

**EV at WR=49.0%, SL=2.39%, leverage=2x, fee=0.05%:**

| TP    | Win payoff (2×TP−fee) | Loss cost (2×SL+fee) | EV per trade |
|-------|----------------------|----------------------|--------------|
| 5.0%  | 9.9%                 | 4.88%                | +2.28%       |
| 5.5%  | 10.9%                | 4.88%                | +2.77%       |
| 6.0%  | 11.9%                | 4.88%                | +3.26%       |
| 7.0%  | 13.9%                | 4.88%                | +4.30% ✓ current |
| **8.0%** | **15.9%**         | **4.88%**            | **+5.30% ✓ TARGET** |
| 9.0%  | 17.9%                | 4.88%                | +6.29%       |

EV check for TP=8.0%:
`0.490 × (2×8.0 - 0.1) - 0.510 × (2×2.39 + 0.1)`
`= 0.490 × 15.9 - 0.510 × 4.88 = 7.79 - 2.49 = +5.30%` ✓

TP/SL = 8.0/2.39 = 3.35 ✓ (well above minimum 2.0)
Expected result: Sharpe improves from +0.3357 toward 0.40–0.55.
Monotonic improvement from TP=4.6 through TP=7.0 strongly supports this projection.

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — LOCKED PARAMETERS (NEVER CHANGE)
# ══════════════════════════════════════════════════════════════════

| Parameter           | Locked Value | Why Locked                                  | Poison Value to Avoid                 |
|--------------------|-------------|---------------------------------------------|---------------------------------------|
| size_pct           | **16.91**   | Proven optimal                              | 8, 9.89, 13.84 (engine artifacts)     |
| max_open           | **1**       | Multi-open failed 400+ gens                 | >1                                    |
| fee_rate           | **0.0005**  | Fixed cost                                  | —                                     |
| pairs              | **all 16**  | Full diversification                        | <16 (causes attractor)                |
| rsi period         | **60 min**  | Shorter = noise; changes cause 716-attractor| <60                                   |
| rsi long           | **35.97**   | Signal sweet spot; changes cause 716-attractor | 30.0 (212-trap), >45 (281-trap)    |
| rsi short          | **72**      | Confirmed across 200+ gens                  | 68.63 (599-trap)                      |
| stop_loss_pct      | **2.39**    | Locked during TP sequence                   | <1.5                                  |
| timeout_minutes    | **720**     | Absolute minimum                            | <720                                  |
| MIN_TRADES[futures_day] | **50** | Raising to 400 caused 867-gen stall         | >50 (CATASTROPHIC — proven)           |

**⚠️ IMPORTANT: ANY change to RSI thresholds, RSI period, or pairs this generation**
**is likely to trigger the 716-trade attractor. DO NOT change these. TP only.**

# ══════════════════════════════════════════════════════════════════
# SECTION 6 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════

1.  **size_pct ≠ 16.91**: BANNED (8, 9.89, 13.84 are engine artifacts)
2.  **RSI long = 30.0**: BANNED (212-trade trap, confirmed poison)
3.  **RSI short = 68.63**: BANNED (599-trade trap, confirmed poison)
4.  **RSI long < 32**: BANNED (catastrophic across 900+ gens)
5.  **RSI long = 33 or 34**: BANNED (746-trade attractor)
6.  **RSI long ≥ RSI short**: BANNED (zero trades)
7.  **RSI long ≠ 35.97 THIS GENERATION**: BANNED — changes to RSI long trigger 716-attractor
8.  **RSI short ≠ 72 THIS GENERATION**: BANNED — changes to RSI short trigger attractors
9.  **RSI period ≠ 60 THIS GENERATION**: BANNED — changes trigger 716/982 attractors
10. **max_open > 1**: BANNED
11. **timeout_minutes < 720**: BANNED
12. **timeout_minutes ≠ 720 THIS GENERATION**: BANNED — only TP change authorized
13. **take_profit_pct < 7.0**: BANNED (never regress; 7.0 is current champion)
14. **take_profit_pct = 7.0 AS YOUR PROPOSAL**: This is the OLD champion. Propose 8.0.
15. **stop_loss_pct < 1.5**: BANNED
16. **stop_loss_pct ≠ 2.39 THIS GENERATION**: BANNED — only TP change authorized
17. **TP/SL ratio < 2.0**: BANNED
18. **Removing any pair**: BANNED (triggers attractors)
19. **MIN_TRADES[futures_day] > 50**: BANNED (proven catastrophic at Gen 541)
20. **stop_if_down_pct < 15**: BANNED
21. **Changing more than ONE parameter**: BANNED this generation
22. **Using ANY value from the engine YAML block**: BANNED
23. **Any config producing < 1500 trades**: HIGH SUSPICION — likely attractor
24. **RSI long > 45**: BANNED (causes 281-trade attractor)
25. **Outputting trades~1793 / Sharpe~+0.1786**: BANNED — old champion, superseded
26. **Outputting trades~716 / Sharpe~-0.8971**: BANNED — new dominant attractor
27. **Outputting trades~982 / Sharpe~-2.1212**: BANNED — secondary attractor
28. **pause_if_down_pct ≠ 8 THIS GENERATION**: BANNED — only TP change authorized
29. **pause_minutes ≠ 120 THIS GENERATION**: BANNED — only TP change authorized
30. **stop_if_down_pct ≠ 18 THIS GENERATION**: BANNED — only TP change authorized

# ══════════════════════════════════════════════════════════════════
# SECTION 7 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════

### ⭐ PHASE B: TP Widening (ACTIVE — NEXT STEP IS TP=8.0%)

```
4.6 → 5.0 → 5.5 → 6.0 → 7.0 [CONFIRMED ✓] → 8.0 ← TEST THIS NOW
```

**This generation: propose take_profit_pct = 8.0**
**This is the ONLY authorized change. Everything else copies the champion YAML exactly.**

Expected results for TP=8.0%:
- Sharpe: +0.3357 → toward 0.40–0.55
- Trades: ~1650–1780 (slight drop from 1752 is acceptable)
- WR: ~47–50% (slight drop acceptable at higher TP)

Warning signs (stop and investigate immediately):
- Trades ~716 → NEW dominant attractor (8/20 recent gens) → STOP, all values wrong
- Trades ~599 → engine YAML poison → STOP, retry with champion above
- Trades ~281 → old dominant attractor → STOP, check all values
- Trades ~982 → secondary attractor → STOP
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
Note: timeout changes may trigger the 716-trade or 982-trade attractor — proceed carefully.

### PHASE A-Refined: RSI Threshold Tuning (AFTER B+C)

```
35.97 → 37 → 38 → 39 → 40
```

Hard limits: MINIMUM 32. MAXIMUM 42. NEVER 33 or 34. NEVER > 45.
⚠️ RSI changes have been triggering the 716-trade attractor. Proceed ONLY after
TP sequence is complete, and add explicit attractor checks before accepting.
RSI short: explore 72 → 74 → 70 (one at a time, after long threshold optimized)

### PHASE D: RSI Period Extension (AFTER B+C+A)

```
60 → 90 → 120 minutes
```

Revert immediately if trades drop below 500. Likely to trigger 716/982 attractors.

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
RSI period_minutes:          60 — 180   (60 LOCKED this generation)
RSI long threshold:          32 — 42    (35.97 LOCKED this generation)
                             (NOT 30.0 — poison; NOT >45 — 281-trade attractor)
                             (NOT 38–42 range this gen — triggers 716-attractor)
RSI short threshold:         65 — 78    (72 LOCKED this generation)
                             (NOT 68.63 — poison)
take_profit_pct:             7.0 — 12.0 (YOUR PROPOSAL: 8.0)
                             (floor is 7.0 — NEVER 6.0 or below)
stop_loss_pct:               1.5 — 3.5  (2.39 LOCKED this generation)
timeout_minutes:             720 — 1440 (720 LOCKED this generation)
TP/SL ratio:                 ≥ 2.0
max_open:                    1 (LOCKED)
size_pct:                    16.91 (LOCKED — NOT 8, NOT 9.89, NOT 13.84)
pause_if_down_pct:           5 — 10     (8 LOCKED this generation)
pause_minutes:               60 — 240   (120 LOCKED this generation)
stop_if_down_pct:            15 — 25    (18 LOCKED this generation)
MIN_TRADES[futures_day]:     50 (LOCKED — raising this caused 867-gen stall)
```

# ══════════════════════════════════════════════════════════════════
# SECTION 9 — SUCCESS MILESTONES
# ══════════════════════════════════════════════════════════════════

| Target         | Expected Via              | Status                              |
|----------------|--------------------------|-------------------------------------|
| Sharpe > 0.00  | TP widening              | ✅ Gen 2081 (+0.1738)               |
| Sharpe > 0.17  | TP=5.5–6.0%              | ✅ Gen 2302 (+0.1786) [OBSOLETE]    |
| Sharpe > 0.30  | TP=7.0%                  | ✅ Gen 2510 (+0.