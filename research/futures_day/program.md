```markdown
# ODIN Research Program — FUTURES DAY (v12.0)

## League: futures_day | Timeframe: 5-min candles, 1-HOUR indicator periods | Leverage: 2x

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
**NEVER raise MIN_TRADES["futures_day"] above 50. Not for any reason.**

---

## THE ACTUAL CURRENT CHAMPION

There is a known display inconsistency: the engine YAML shows size_pct=20 and
RSI lt=30.0. These are BASE CONFIG DISPLAY ARTIFACTS. The operational champion is:

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
      value: 35.97      ← LOCKED — do not tighten
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 72         ← LOCKED — do not change
exit:
  take_profit_pct: 4.6  ← CHANGE THIS TO 5.0
  stop_loss_pct: 2.39   ← LOCKED
  timeout_minutes: 720  ← LOCKED (minimum — never reduce)
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

**Champion performance: Sharpe -0.2445, 1678 trades, 48.5% WR**

**⚠️ CRITICAL WARNING ABOUT THE YAML THE ENGINE SHOWS YOU:**
If the YAML at the top of this prompt shows `value: 30.0` for RSI long, that is
a display artifact. Do NOT use 30.0 as your base. Use 35.97.
If it shows `size_pct: 20`, that is a display artifact. Use 16.91.
The champion parameters above are correct. Build your proposal from these.

---

## WHY TP=5.0% IS THE CORRECT NEXT STEP

EV calculation at current WR=48.5%, SL=2.39%, leverage=2x:

| TP | Win payoff | Loss cost | EV per trade |
|-----|-----------|-----------|-------------|
| 4.6% (now) | 9.1% | 4.88% | +1.90% ✓ |
| **5.0% (next)** | **9.9%** | **4.88%** | **+2.29% ✓✓** |
| 5.5% | 10.9% | 4.88% | +2.71% ✓✓ |
| 6.0% | 11.9% | 4.88% | +3.26% ✓✓✓ |

Formula: `WR × (2×TP - 0.1%) - (1-WR) × (2×SL + 0.1%)`

TP=5.0% improves EV by +0.39% per trade over champion. With 1678 trades,
this is meaningful. TP/SL ratio = 5.0/2.39 = 2.09 ✓ (above minimum 2.0)

**Gen 1726 proved TP widening works: 4.0% → 4.6% improved Sharpe from
-0.3689 → -0.2445 AND increased trades 1395 → 1678 AND improved WR 47.2% → 48.5%.
All three metrics improved simultaneously. The sequence must continue.**

**Note on Gen 1792:** This generation achieved Sharpe=-0.3081, 1739 trades,
48.3% WR (new_elite). This is slightly worse Sharpe than champion but higher
trade count, confirming the loose RSI architecture continues to produce
high-quality high-volume results. TP widening from that base should also work.

---

## FAILURE ATTRACTORS — MEMORIZE THESE

If your proposal would land in one of these, STOP and propose TP=5.0% instead.

### 🔴 Attractor 1: The 484-Trade Trap
```
Sharpe=-1.1593, WR=48.3%, trades=484
```
Appeared 6 times in the last 20 generations. MOST DANGEROUS CURRENT TRAP.
Caused by: any change that reduces RSI threshold below ~32, adds a restrictive
filter, or misreads RSI lt=30.0 from the display artifact.
**Escape: TP=5.0% from the correct base (RSI lt=35.97, size_pct=16.91)**

### 🔴 Attractor 2: The 212-Trade Trap
```
Sharpe=-4.1548, WR=44.8%, trades=212
```
Appeared 3 times in last 20 generations.
Caused by: very tight RSI threshold + additional filter = almost no trades.
**Escape: TP=5.0%**

### 🔴 Attractor 3: The 746-Trade Trap
```
Sharpe=-0.9990, WR=49.2%, trades=746
```
Caused by: RSI long=33 or 34. Do not ever propose RSI=33 or 34.
**Escape: TP=5.0%**

### 🔴 Attractor 4: Zero Trades
```
Sharpe=-999.0, WR=0%, trades=0
```
Caused by: impossible RSI conditions, conflicting thresholds, invalid values.
If RSI long threshold ≥ RSI short threshold, that's the bug.
**Escape: TP=5.0%**

### 🔴 Attractor 5: Dead-Config Loop
```
Sharpe=-0.3523, WR=49.3%, trades=1411  (appeared 4+ times)
Sharpe=-0.3932, WR=48.8%, trades=1341  (appeared 3+ times)
```
Caused by: repeated RSI micro-adjustments that don't improve Sharpe.
**Escape: TP=5.0%**

**If you recognize ANY of these patterns from recent history, your ONLY
valid proposal is: take_profit_pct from 4.6 to 5.0**

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
3. **max_open > 1**: BANNED. Failed paradigm.
4. **timeout_minutes < 720**: BANNED. Hard floor. No exceptions.
5. **take_profit_pct < 4.6**: BANNED. Never regress from confirmed champion TP.
6. **stop_loss_pct < 1.5**: BANNED.
7. **RSI period < 60 minutes**: BANNED. Sub-hourly RSI is noise.
8. **Removing any pair**: BANNED. All 16 pairs always.
9. **size_pct ≠ 16.91**: BANNED. Do not change to 20 or any other value.
10. **stop_if_down_pct < 15**: BANNED.
11. **TP/SL ratio < 2.0**: BANNED.
12. **Adding a 3rd entry condition**: BANNED until Phase F.
13. **RSI long ≥ RSI short**: BANNED. Produces zero trades.

---

## WHAT DATA SHOWS — VALIDATED ARCHITECTURE

| Configuration | WR | Sharpe | Trades |
|---|---|---|---|
| RSI < 22-25, tight | 42-45% | -2.4 to -5.8 | 150-300 |
| RSI < 36, max_open=1, TP=4.0% | 47.2% | -0.3689 | 1395 |
| RSI < 36, max_open=1, TP=4.6% | 48.5% | **-0.2445** | **1678** ← champ |

**The loose RSI + max_open=1 + TP widening architecture is correct and validated.**

---

## OPTIMIZATION SEQUENCE

### ⭐ PHASE B: TP Widening (ACTIVE — DO THIS NOW)

```
4.6 → 5.0 → 5.5 → 6.0 → 7.0 → 8.0
```

**Current step: 4.6 → 5.0. This is the ONLY change to propose right now.**

Expected result at TP=5.0%: Sharpe > -0.20, trades ~1600-1800, WR ~48-50%

Warning signs:
- WR drops below 44% → timeout cutting trades; switch to Phase C
- Trades drop below 800 → something wrong, investigate before continuing
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
RSI long threshold:     32 — 42
RSI short threshold:    65 — 78
take_profit_pct:        4.6 — 10.0   (floor is 4.6 — Gen 1726 confirmed)
stop_loss_pct:          1.5 — 3.5
timeout_minutes:        720 — 1440   (MINIMUM 720 — absolute floor)
TP/SL ratio:            ≥ 2.0
max_open:               1 (LOCKED)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
size_pct:               16.91 (LOCKED)
```

---

## PRIORITY ORDER — NEXT 100 GENERATIONS

```
Priority 1 (NOW): take_profit_pct = 5.0
Priority 2 (after 5.0 confirmed): take_profit_pct = 5.5
Priority 3 (after 5.5 confirmed): take_profit_pct = 6.0
Priority 4 (if any TP step fails 3x): timeout = 960, then retry TP
Priority 5 (after TP+timeout done): RSI threshold 35.97 → 37
Priority 6 (after RSI tuned): SL optimization
Priority 7 (last): Trend filter
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
- Gen 1726: Sharpe -0.24 (1678 trades, 48.5% WR) ← **current best ★**
- Gen 1792: Sharpe -0.31 (1739 trades, 48.3% WR) ← new_elite (not champion)
- **Next target: Sharpe > -0.20 via TP=5.0%**

---

## MACRO ENVIRONMENT

Current Regime: DANGER (Extreme Fear, F&G=14, BTC Dom=57.1%)

Extreme fear means altcoins frequently oversold → RSI<36 fires regularly.
Large directional moves → TP=5-7% reachable in single oversold bounces.
Mean reversions are sharp → fast path to TP.

**This environment strongly supports TP widening to 5-7%. Fear is the edge.**
RSI<36 during F&G=14 is a high-quality signal. Do not scale down.

---

## HOW TO PROPOSE A CHANGE

```
CHANGE: take_profit_pct from 4.6 to 5.0
REASON: TP widening confirmed at Gen 1726; 5.0% improves EV from +1.90% to +2.29%
PHASE: B
EXPECTED EFFECT: Sharpe improves from -0.2445 toward -0.20; WR holds ~48-50%
EV CHECK: 0.485 × (2×5.0 - 0.1) - 0.515 × (2×2.39 + 0.1) = 0.485×9.9 - 0.515×4.88 = 4.80 - 2.51 = +2.29% ✓
ZERO-TRADE CHECK: RSI long=35.97 < RSI short=72 ✓ Both in valid range ✓
LOOP CHECK: Not a known failure attractor ✓ TP widening confirmed working ✓
```

Then output the complete YAML with ONLY take_profit_pct changed to 5.0.

---

## ⚠️ FINAL REMINDER

You are 1800 generations into a 1800-generation program.
The strategy is working. The signal is real. EV is positive.
**The only remaining problem is that TP is too tight.**

Propose: `take_profit_pct: 5.0`

Do NOT propose RSI=33 or 34.
Do NOT reduce timeout below 720.
Do NOT change size_pct to 20.
Do NOT add a filter.
Do NOT tighten RSI thresholds.
Do NOT change anything except take_profit_pct from 4.6 to 5.0.
```