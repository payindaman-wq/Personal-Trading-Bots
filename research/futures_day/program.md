```markdown
# ODIN Research Program — FUTURES DAY (v16.0)

# ══════════════════════════════════════════════════════════════════
# ⚡ START HERE — CHAMPION YAML (COPY THIS EXACTLY, CHANGE ONLY TP)
# ══════════════════════════════════════════════════════════════════

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
  take_profit_pct: 5.5     ← CHANGE THIS LINE ONLY (was 5.0)
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

**YOUR ONLY TASK: Copy the YAML above. Set take_profit_pct: 5.5. Output it. Done.**

---

# ══════════════════════════════════════════════════════════════════
# ⚠️ ENGINE YAML ALERT — DO NOT USE THE YAML AT THE END OF THIS PROMPT
# ══════════════════════════════════════════════════════════════════

There is a second YAML block elsewhere in your context. It contains WRONG values:
- size_pct: 13.84        ← WRONG. Correct is 16.91
- rsi long value: 30.0  ← WRONG. Correct is 35.97
- rsi short value: 68.63 ← WRONG. Correct is 72
- take_profit_pct: 4.6  ← WRONG. Correct is 5.5

Using those values produces: 599 trades, Sharpe=-1.0674 (confirmed failure 12+ times).
If your output has size_pct=13.84 or rsi=30.0 or rsi_short=68.63 → STOP. Use champion above.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 1 — PRE-FLIGHT CHECKLIST (FILL THIS IN BEFORE OUTPUTTING)
# ══════════════════════════════════════════════════════════════════

```
PRE-FLIGHT CHECK:
  size_pct       = ___  (must be 16.91  — NOT 13.84)
  rsi_long       = ___  (must be 35.97  — NOT 30.0)
  rsi_short      = ___  (must be 72     — NOT 68.63)
  stop_loss      = ___  (must be 2.39)
  timeout        = ___  (must be 720)
  take_profit    = ___  (must be 5.5    — this is the ONLY change from champion)
  TP/SL ratio    = ___  (must be ≥ 2.0; 5.5/2.39 = 2.30 ✓)
  expected trades = ___ (expect ~1793; if ~599 → used wrong YAML → STOP)
  Source: Champion YAML at top of this prompt ✓
```

If ANY value differs from required: STOP. Do not output YAML. Re-read champion block above.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 2 — FAILURE ATTRACTOR CHECKLIST (VERIFY BEFORE OUTPUTTING)
# ══════════════════════════════════════════════════════════════════

Your output must NOT match any of these:

| Signature | Trades | Sharpe | Cause |
|-----------|--------|--------|-------|
| 🔴 size=13.84 + RSI=30.0 + RSI_s=68.63 | ~599 | -1.0674 | Engine YAML artifact |
| 🔴 RSI long = 30.0 only | ~212 | -4.1548 | Engine YAML artifact |
| 🔴 RSI long = 33 or 34 | ~746 | -0.999 | Banned values |
| 🔴 RSI long ≥ RSI short | 0 | -999 | Impossible config |
| 🔴 Any config with trades < 800 | <800 | varies | Config error |

**If your expected trade count is ~599 → you used the engine YAML. Start over.**
**If your expected trade count is ~212 → you used RSI=30.0. Start over.**
**If your expected trade count is 0 → RSI long ≥ RSI short. Start over.**

---

# ══════════════════════════════════════════════════════════════════
# SECTION 3 — WHAT THIS STRATEGY IS
# ══════════════════════════════════════════════════════════════════

**Architecture:** Mean-reversion swing on 16 crypto pairs (2x futures, 5-min candles)
**Signal:** RSI(60-min) < 35.97 → long (oversold); RSI(60-min) > 72 → short (overbought)
**Edge:** Extreme Fear drives frequent altcoin oversold readings → sharp mean reversions
**Max open:** 1 position at a time (prevents correlated loss accumulation)
**Exit:** TP=5.5%, SL=2.39%, timeout=720min → TP/SL=2.30 ✓

**Performance trajectory (confirmed improvements only):**
- Gen 1460: Sharpe=-0.73 (967 trades)  ← paradigm shift: loose RSI + max_open=1
- Gen 1726: Sharpe=-0.24 (1678 trades)
- Gen 2019: Sharpe=-0.21 (1798 trades)
- Gen 2081: Sharpe=+0.1738 (1793 trades, 49.5% WR) ← FIRST POSITIVE SHARPE ★
- Gen 2136: Sharpe=+0.1759 (1793 trades, 49.5% WR)
- Gen 2193: Sharpe=+0.1767 (1793 trades, 49.5% WR) ← CURRENT BEST

TP widening (4.6→5.0→5.5) has produced monotonic improvement. TP=5.5 is next.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 4 — WHY TP=5.5% IS CORRECT
# ══════════════════════════════════════════════════════════════════

**EV at WR=49.5%, SL=2.39%, leverage=2x:**

| TP | Win payoff (2×TP) | Loss cost (2×SL+fee) | EV per trade |
|----|-------------------|----------------------|--------------|
| 5.0% (champion) | 10.0% | 4.88% | +2.37% |
| **5.5% (next)** | **11.0%** | **4.88%** | **+2.86% ✓** |
| 6.0% (after) | 12.0% | 4.88% | +3.35% |

EV check: `0.495 × (2×5.5 - 0.1) - 0.505 × (2×2.39 + 0.1)`
`= 0.495 × 10.9 - 0.505 × 4.88 = 5.40 - 2.46 = +2.93%` ✓

TP/SL = 5.5/2.39 = 2.30 ✓ (above minimum 2.0)
Expected: Sharpe improves from +0.1767 toward 0.20-0.30+. Trades remain ~1793.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — LOCKED PARAMETERS (NEVER CHANGE)
# ══════════════════════════════════════════════════════════════════

| Parameter | Locked Value | Note |
|-----------|-------------|------|
| size_pct | **16.91** | Engine YAML shows 13.84 — WRONG |
| max_open | **1** | Multi-open failed 400+ gens |
| fee_rate | **0.0005** | Fixed cost |
| pairs | **all 16** | Full diversification required |
| rsi period | **60 min** | Shorter = noise |
| rsi long | **35.97** | Engine YAML shows 30.0 — WRONG (212-trade trap) |
| rsi short | **72** | Engine YAML shows 68.63 — WRONG (599-trade trap) |
| stop_loss_pct | **2.39** | Locked until TP sequence complete |
| timeout_minutes | **720** | Absolute minimum |
| MIN_TRADES[futures_day] | **50** | NEVER raise — caused 867-gen stall at 400 |

---

# ══════════════════════════════════════════════════════════════════
# SECTION 6 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════

1. **Using ANY value from the engine YAML at the bottom of your context**: BANNED
2. **size_pct ≠ 16.91**: BANNED (13.84 is engine artifact)
3. **RSI long = 30.0**: BANNED (212-trade trap)
4. **RSI short = 68.63**: BANNED (599-trade trap)
5. **RSI long < 32**: BANNED (catastrophic across 900+ gens)
6. **RSI long = 33 or 34**: BANNED (746-trade attractor)
7. **RSI long ≥ RSI short**: BANNED (zero trades)
8. **max_open > 1**: BANNED
9. **timeout_minutes < 720**: BANNED
10. **take_profit_pct < 5.5**: BANNED (never regress)
11. **stop_loss_pct < 1.5**: BANNED
12. **TP/SL ratio < 2.0**: BANNED
13. **RSI period < 60 minutes**: BANNED
14. **Removing any pair**: BANNED
15. **MIN_TRADES[futures_day] > 50**: BANNED (proven catastrophic)
16. **stop_if_down_pct < 15**: BANNED
17. **Changing more than ONE parameter**: BANNED this generation

---

# ══════════════════════════════════════════════════════════════════
# SECTION 7 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════

### ⭐ PHASE B: TP Widening (ACTIVE — DO THIS NOW)

```
4.6 → 5.0 → [5.5 ← YOU ARE HERE] → 6.0 → 7.0 → 8.0
```

**This generation: propose take_profit_pct = 5.5. Nothing else.**

Expected results:
- Sharpe: +0.1767 → toward 0.20-0.30+
- Trades: ~1700–1900
- WR: ~48–51%

Warning signs (investigate if seen):
- Trades ~599 → used engine YAML → retry with Section 1 champion
- Trades ~212 → used RSI=30.0 → retry with RSI=35.97
- Trades < 800 → config error → investigate before accepting
- WR < 44% → timeout cutting trades; escalate to Phase C

**If TP=5.5 confirmed → next: TP=6.0**
**If TP=5.5 fails 3 consecutive confirmed tests → Phase C (timeout=960)**

### PHASE C: Timeout Extension (FALLBACK ONLY)

```
720 → 960 → 1200 → 1440 minutes
```

Do NOT use unless Phase B stalls 3+ times. Never reduce below 720.

### PHASE A-Refined: RSI Threshold Tuning (AFTER B+C)

```
35.97 → 37 → 38 → 39 → 40
```

Hard limits: MINIMUM 32. MAXIMUM 42. NEVER 33 or 34.

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

---

# ══════════════════════════════════════════════════════════════════
# SECTION 8 — PARAMETER BOUNDS
# ══════════════════════════════════════════════════════════════════

```
RSI period_minutes:     60 — 180
RSI long threshold:     32 — 42    (NOT 30.0 — poison artifact)
RSI short threshold:    65 — 78    (NOT 68.63 — poison artifact)
take_profit_pct:        5.5 — 10.0 (floor is 5.5 — never regress)
stop_loss_pct:          1.5 — 3.5
timeout_minutes:        720 — 1440
TP/SL ratio:            ≥ 2.0
max_open:               1 (LOCKED)
size_pct:               16.91 (LOCKED — NOT 13.84)
pause_if_down_pct:      5 — 10
pause_minutes:          60 — 240
stop_if_down_pct:       15 — 25
```

---

# ══════════════════════════════════════════════════════════════════
# SECTION 9 — SUCCESS MILESTONES
# ══════════════════════════════════════════════════════════════════

| Target | Expected Via | Status |
|--------|-------------|--------|
| Sharpe > 0.00 | TP widening | ✅ Gen 2081 (+0.1738) |
| Sharpe > 0.20 | TP=5.5% | 🎯 NEXT TARGET |
| Sharpe > 0.30 | TP=5.5–6.0% | Phase B |
| Sharpe > 0.50 | TP=6.0% | Phase B |
| Sharpe > 0.70 | TP=7.0% or timeout=960 | Phase B/C |
| Sharpe > 1.00 | TP+timeout+RSI+SL | B+C+A+E |
| Sharpe > 1.50 | Above + trend filter | F |

---

# ══════════════════════════════════════════════════════════════════
# SECTION 10 — MACRO ENVIRONMENT
# ══════════════════════════════════════════════════════════════════

Current Regime: DANGER (Extreme Fear, F&G=16, BTC Dom=57.28%)

Extreme Fear → altcoins frequently oversold → RSI<35.97 fires regularly.
Large directional moves → TP=5.5–7% reachable in single oversold bounces.
Mean reversions are sharp → fast path to TP.

**This environment strongly supports TP widening to 5.5–7%.**
The TYR directive to reduce position sizes (25%) applies to live trading only,
not to backtesting parameter selection.

---

# ══════════════════════════════════════════════════════════════════
# SECTION 11 — HOW TO PROPOSE YOUR CHANGE
# ══════════════════════════════════════════════════════════════════

**Step 1:** Fill in the pre-flight checklist (Section 1)
**Step 2:** Confirm no values match the poison list
**Step 3:** Confirm no failure attractor match (Section 2)
**Step 4:** Output this block:

```
CHANGE: take_profit_pct from 5.0 to 5.5
REASON: TP widening confirmed Gens 2081–2193 (Sharpe +0.1767); 5.5% improves EV from +2.37% to +2.86%
PHASE: B
EXPECTED: Sharpe improves from +0.1767 toward 0.20–0.30+; trades ~1700–1900; WR ~48–51%
EV CHECK: 0.495 × 10.9 - 0.505 × 4.88 = 5.40 - 2.46 = +2.93% ✓
TP/SL RATIO: 5.5 / 2.39 = 2.30 ✓
ZERO-TRADE CHECK: RSI long=35.97 < RSI short=72 ✓
ATTRACTOR CHECK: trades ~1793, not matching 599/212/746/0 ✓
POISON CHECK: size_pct=16.91 ✓ | RSI long=35.97 ✓ | RSI short=72 ✓
```

**Step 5:** Output the complete YAML below — champion values, only TP changed:

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

**Final verification:**
- [ ] size_pct = 16.91 (NOT 13.84)
- [ ] rsi long = 35.97 (NOT 30.0)
- [ ] rsi short = 72 (NOT 68.63)
- [ ] take_profit_pct = 5.5 (the ONLY change)
- [ ] stop_loss_pct = 2.39 (unchanged)
- [ ] timeout_minutes = 720 (unchanged)
- [ ] All 16 pairs present (unchanged)
- [ ] Expected trades ~1793 (not 599, not 212, not 0)
```