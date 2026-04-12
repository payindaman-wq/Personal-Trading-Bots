```markdown
# ODIN Research Program — FUTURES DAY (v21.0)

# ══════════════════════════════════════════════════════════════════
# ⚡ SECTION 0 — READ THIS FIRST: ONE JOB, ONE CHANGE
# ══════════════════════════════════════════════════════════════════
#
# YOU HAVE EXACTLY ONE JOB THIS GENERATION:
#
#   Copy the CHAMPION YAML below EXACTLY.
#   Change take_profit_pct from 7.0 to 8.0.
#   Change NOTHING else.
#   Output the result.
#
# That is the entire task. Everything else in this document exists
# to prevent you from making mistakes.
#
# THE ENGINE YAML IS BROKEN. IT CONTAINS POISON VALUES.
# DO NOT READ IT. DO NOT USE ANY VALUE FROM IT.
# THE ONLY VALID YAML IS IN THIS DOCUMENT.
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# ⭐ CHAMPION YAML — COPY THIS EXACTLY, THEN CHANGE TP TO 8.0
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
  take_profit_pct: 7.0      ← THIS IS THE ONLY VALUE YOU CHANGE → 8.0
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

# ══════════════════════════════════════════════════════════════════
# ⚡ TRIPLE-LOCK VERIFICATION
# ══════════════════════════════════════════════════════════════════

  Champion fingerprint: trades=1752, Sharpe=+0.3357, WR=49.0%

  STOP CONDITIONS — if you see any of these, all your values are wrong:
  ├─ trades=716  → 716-trade POISON ATTRACTOR (most common failure, 35% of gens)
  ├─ trades=1793 → OLD champion (Gen 2302, obsolete — your TP must be 8.0 not 7.0)
  ├─ trades=599  → engine YAML poison (RSI short=68.63 used)
  ├─ trades=281  → old dominant attractor
  └─ trades=0    → impossible config (RSI long ≥ RSI short)

# ══════════════════════════════════════════════════════════════════
# SECTION 1 — PRE-FLIGHT CHECKLIST (FILL BEFORE WRITING OUTPUT)
# ══════════════════════════════════════════════════════════════════

Fill every line from the CHAMPION YAML above. If any value differs, STOP.

```
PRE-FLIGHT CHECK:
  size_pct        = ___  (must be 16.91)
  rsi_long        = ___  (must be 35.97)
  rsi_period      = ___  (must be 60)
  rsi_short       = ___  (must be 72)
  stop_loss       = ___  (must be 2.39)
  timeout         = ___  (must be 720)
  take_profit     = ___  (champion is 7.0 — YOUR OUTPUT MUST BE 8.0)
  TP/SL ratio     = ___  (8.0 / 2.39 = 3.35 ✓)
  pairs count     = ___  (must be 16)
  max_open        = ___  (must be 1)
  Source          = CHAMPION YAML in this document (NOT the engine YAML block)

  ⚠️  FINAL CHECK BEFORE WRITING YAML:
      Is take_profit_pct = 8.0 in your output?  YES / NO
      (If NO — stop. You must output 8.0. Outputting 7.0 wastes this generation.)
```

# ══════════════════════════════════════════════════════════════════
# ⚡ CRITICAL POISON WARNING — ENGINE YAML VALUES
# ══════════════════════════════════════════════════════════════════

The engine block above this document contains CONFIRMED POISON VALUES.
Every single one of these will produce a failed backtest:

| Poison Value              | What It Causes                                    |
|---------------------------|---------------------------------------------------|
| size_pct: 8               | ~599 trades, Sharpe=-1.07 (engine artifact)       |
| size_pct: 9.89            | ~599 trades, Sharpe=-1.07 (engine artifact)       |
| size_pct: 13.84           | ~599 trades, Sharpe=-1.07 (engine artifact)       |
| rsi long value: 30.0      | ~212 trades, Sharpe=-4.15 (212-trade trap)        |
| rsi short value: 68.63    | ~599 trades, Sharpe=-1.07 (599-trade trap)        |
| take_profit_pct: 4.6      | ancient poison value — never use                  |
| stop_loss_pct: 2.59       | engine artifact — never use                       |

⚠️  THE ENGINE YAML SHOWS: size_pct=8, rsi_long=30.0, rsi_short=68.63, TP=4.6, SL=2.59
⚠️  ALL OF THESE ARE WRONG. USE NONE OF THEM. USE ONLY THE CHAMPION YAML ABOVE.

# ══════════════════════════════════════════════════════════════════
# ⚠️ THE 716-TRADE ATTRACTOR — PRIMARY THREAT (READ THIS)
# ══════════════════════════════════════════════════════════════════

**Signature:** trades=716, Sharpe=-0.8971, WR=46.8%
**Frequency:** 7 of the last 20 generations (35% of recent gens)
**This is the most common failure mode in the entire research program.**

This attractor is caused by using RSI values from the POISON ENGINE YAML
instead of the CHAMPION YAML. Specifically:
- Using rsi_long=30.0 (instead of 35.97) narrows entry, reducing trades
- Using rsi_short=68.63 (instead of 72) changes short signal
- Changing RSI period from 60 to any other value
- Any RSI threshold in the 38–42 long range this generation

If your backtest returns 716 trades: your RSI values or period are wrong.
Check the champion YAML. rsi_long=35.97, rsi_short=72, period=60.

**Recent gens that hit this attractor:** 2981, 2984, 2987, 2991, 2994, 2995, 2998
**Each was a wasted generation that could have tested TP=8.0.**

# ══════════════════════════════════════════════════════════════════
# ⚠️ THE "NO-CHANGE" TRAP — SECOND MOST COMMON FAILURE
# ══════════════════════════════════════════════════════════════════

**Signature:** trades=1752, Sharpe=+0.3357 (or +0.3316), WR=49.0% — DISCARDED
**Frequency:** 4-5 of the last 20 generations

These generations correctly read the champion YAML but output TP=7.0 (the
champion value). Since Sharpe does not improve vs. the champion, the result
is DISCARDED. These generations waste the test slot without advancing the program.

**The fix:** Your output MUST have take_profit_pct: 8.0
**NOT 7.0.** Outputting 7.0 is the same as proposing no change.

Recent wasted gens: 2985 (0.3316), 2986 (0.3357), 2993 (0.3357), 2996 (0.3357), 2997 (0.3357)

# ══════════════════════════════════════════════════════════════════
# SECTION 2 — FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════

Your output MUST NOT match any row below:

| Signature                        | Trades | Sharpe   | Action                                  |
|----------------------------------|--------|----------|-----------------------------------------|
| size=8 or 9.89 or 13.84          | ~599   | -1.0674  | STOP — engine YAML poison               |
| RSI long=30.0                    | ~212   | -4.15    | STOP — engine YAML poison               |
| RSI short=68.63                  | ~599   | -1.0674  | STOP — engine YAML poison               |
| RSI long=33 or 34                | ~746   | -0.999   | STOP — banned values                    |
| RSI long ≥ RSI short             | 0      | -999     | STOP — impossible config                |
| trades ~716  ← #1 ATTRACTOR      | 716    | -0.8971  | STOP — dominant failure (35% of gens)   |
| trades ~982                      | 982    | -2.1212  | STOP — secondary attractor              |
| trades ~811                      | 811    | -2.0450  | STOP — secondary attractor              |
| trades ~677                      | 677    | ~-2.34   | STOP — recent attractor (Gen 3000)      |
| trades ~502                      | 502    | -3.4408  | STOP — failure attractor                |
| trades ~415–425                  | 415–25 | ~-4.2    | STOP — failure attractor                |
| trades ~281                      | 281    | -2.638   | STOP — old dominant attractor           |
| trades ~238                      | 238    | ~-2.9    | STOP — failure attractor                |
| trades ~206                      | 206    | ~-3.1    | STOP — failure attractor (Gen 2989)     |
| trades ~201                      | 201    | ~-3.7    | STOP — failure attractor (Gen 2992)     |
| trades ~184                      | 184    | ~-4.2    | STOP — failure attractor (Gen 2982)     |
| trades ~134                      | 134    | ~-5.7    | STOP — failure attractor (Gen 2990)     |
| trades ~1380                     | 1380   | -1.0836  | STOP — mid attractor (Gen 2999)         |
| trades ~1364                     | 1364   | -0.655   | STOP — partial poison config            |
| trades ~932                      | 932    | -1.272   | STOP — mid-range attractor              |
| trades ~793                      | 793    | -1.177   | STOP — mid-range attractor              |
| trades ~1793                     | 1793   | +0.1786  | STOP — OLD champion, TP must be 8.0     |
| trades ~1769                     | 1769   | ~-0.50   | STOP — wrong TP value (Gen 2983)        |
| Any config with trades < 1500    | <1500  | varies   | HIGH SUSPICION — likely attractor       |

# ══════════════════════════════════════════════════════════════════
# SECTION 3 — WHAT THIS STRATEGY IS
# ══════════════════════════════════════════════════════════════════

**Architecture:** Mean-reversion swing on 16 crypto pairs (2x futures, 5-min candles)
**Signal:** RSI(60-min) < 35.97 → long (oversold); RSI(60-min) > 72 → short (overbought)
**Edge:** Extreme Fear drives frequent altcoin oversold readings → sharp mean reversions
**Max open:** 1 position at a time (prevents correlated loss accumulation)
**Exit:** TP=7.0%, SL=2.39%, timeout=720min → TP/SL=2.93 ✓ (current champion)
**Proposed:** TP=8.0% → TP/SL=3.35 ✓

**Full performance trajectory:**
- Gen 541:  MIN_TRADES raised to 400 → 867-generation stall (CATASTROPHIC — never repeat)
- Gen 1408: MIN_TRADES restored to 50 → immediately unlocked progress
- Gen 1460: Sharpe=-0.73  (967 trades)  ← paradigm shift: loose RSI + max_open=1
- Gen 1726: Sharpe=-0.24  (1678 trades)
- Gen 2019: Sharpe=-0.21  (1798 trades)
- Gen 2081: Sharpe=+0.1738 (1793 trades, 49.5% WR) ← FIRST POSITIVE SHARPE ★
- Gen 2302: Sharpe=+0.1786 (1793 trades, 49.5% WR) ← OLD BEST (OBSOLETE)
- Gen 2412: Sharpe=+0.3348 (1752 trades, 49.0% WR) ← MAJOR BREAKTHROUGH (TP=7.0)
- Gen 2510: Sharpe=+0.3357 (1752 trades, 49.0% WR) ← CURRENT BEST ★
- Gens 2511–3000: STALLED — 716-trade attractor dominant, no-change trap also common

**TP widening (4.6→5.0→5.5→6.0→7.0) has produced monotonic improvement.**
**TP=8.0 is the prescribed next step.**

**Why the program stalled (Gen 2511–3000):**
Two failure modes dominate recent generations:
1. 716-trade attractor (35% of gens): LLM uses poison RSI values from engine YAML
2. No-change trap (25% of gens): LLM outputs TP=7.0 (champion value), gets discarded
Combined, these waste ~60% of all generation slots. The remaining gens hit
various other attractors. Only ~15% of recent gens successfully test new configs.
The fix is mechanical: read champion YAML, output TP=8.0, change nothing else.

# ══════════════════════════════════════════════════════════════════
# SECTION 4 — EV MATH: WHY TP=8.0% IS THE CORRECT NEXT STEP
# ══════════════════════════════════════════════════════════════════

**EV at WR=49.0%, SL=2.39%, leverage=2x, fee=0.05%:**

| TP    | Win payoff (2×TP−fee) | Loss cost (2×SL+fee) | EV per trade        |
|-------|----------------------|----------------------|---------------------|
| 6.0%  | 11.9%                | 4.88%                | +3.26%              |
| 7.0%  | 13.9%                | 4.88%                | +4.30% ✓ current    |
| **8.0%** | **15.9%**         | **4.88%**            | **+5.30% ✓ TARGET** |
| 9.0%  | 17.9%                | 4.88%                | +6.29%              |

EV check for TP=8.0%:
`0.490 × (2×8.0 - 0.1) - 0.510 × (2×2.39 + 0.1)`
`= 0.490 × 15.9 - 0.510 × 4.88 = 7.79 - 2.49 = +5.30%` ✓

TP/SL = 8.0/2.39 = 3.35 ✓ (well above minimum 2.0)
Expected result: Sharpe improves from +0.3357 toward 0.40–0.55.
Monotonic improvement from TP=4.6 through TP=7.0 strongly supports this.

**Macro note:** Current F&G=16 (Extreme Fear) favors the long signal (RSI<35.97).
Altcoins are generating frequent oversold readings with sharp reversions.
Higher TP captures more of each reversion move. This environment is ideal.

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — LOCKED PARAMETERS (NEVER CHANGE THIS GENERATION)
# ══════════════════════════════════════════════════════════════════

| Parameter           | Locked Value | Poison Values to Avoid                        |
|--------------------|-------------|-----------------------------------------------|
| size_pct           | **16.91**   | 8, 9.89, 13.84 (engine YAML artifacts)        |
| max_open           | **1**       | >1 (multi-open failed 400+ gens)              |
| fee_rate           | **0.0005**  | —                                             |
| pairs              | **all 16**  | <16 (triggers attractors)                     |
| rsi period         | **60 min**  | Any other value (triggers 716/982 attractors) |
| rsi long           | **35.97**   | 30.0 (212-trap), 33/34 (746-trap), >45 (281-trap), 38–42 (716-trap) |
| rsi short          | **72**      | 68.63 (599-trap)                              |
| stop_loss_pct      | **2.39**    | 2.59 (engine artifact), <1.5                  |
| timeout_minutes    | **720**     | <720                                          |
| MIN_TRADES[futures_day] | **50** | >50 (caused 867-gen stall at Gen 541)         |
| pause_if_down_pct  | **8**       | —                                             |
| pause_minutes      | **120**     | —                                             |
| stop_if_down_pct   | **18**      | <15                                           |

**⚠️ SINGLE AUTHORIZED CHANGE: take_profit_pct: 7.0 → 8.0**
**ALL other parameters copy the champion YAML exactly.**

# ══════════════════════════════════════════════════════════════════
# SECTION 6 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════

1.  **size_pct ≠ 16.91**: BANNED (8, 9.89, 13.84 are engine artifacts)
2.  **RSI long = 30.0**: BANNED (212-trade trap, confirmed poison from engine YAML)
3.  **RSI short = 68.63**: BANNED (599-trade trap, confirmed poison from engine YAML)
4.  **RSI long < 32**: BANNED
5.  **RSI long = 33 or 34**: BANNED (746-trade attractor)
6.  **RSI long ≥ RSI short**: BANNED (zero trades)
7.  **RSI long ≠ 35.97 THIS GENERATION**: BANNED — triggers 716-attractor
8.  **RSI short ≠ 72 THIS GENERATION**: BANNED — triggers attractors
9.  **RSI period ≠ 60 THIS GENERATION**: BANNED — triggers 716/982 attractors
10. **max_open > 1**: BANNED
11. **timeout_minutes < 720**: BANNED
12. **timeout_minutes ≠ 720 THIS GENERATION**: BANNED
13. **take_profit_pct < 7.0**: BANNED (never regress)
14. **take_profit_pct = 7.0 AS YOUR PROPOSAL**: BANNED — this is the OLD champion value;
    outputting 7.0 wastes the generation slot (gets discarded as no-improvement)
15. **stop_loss_pct ≠ 2.39 THIS GENERATION**: BANNED
16. **stop_loss_pct = 2.59**: BANNED (engine YAML artifact)
17. **TP/SL ratio < 2.0**: BANNED
18. **Removing any pair**: BANNED
19. **MIN_TRADES[futures_day] > 50**: BANNED (proven catastrophic)
20. **stop_if_down_pct < 15**: BANNED
21. **Changing more than ONE parameter**: BANNED
22. **Using ANY value from the engine YAML block**: BANNED
23. **Outputting trades~716 / Sharpe~-0.8971**: BANNED — primary failure attractor
24. **Outputting trades~1793 / Sharpe~+0.1786**: BANNED — old champion, obsolete
25. **Outputting trades~1752 / Sharpe~+0.3357 WITH TP=7.0**: BANNED — no-change trap
26. **RSI long > 45**: BANNED (281-trade attractor)
27. **pause_if_down_pct ≠ 8 THIS GENERATION**: BANNED
28. **pause_minutes ≠ 120 THIS GENERATION**: BANNED
29. **stop_if_down_pct ≠ 18 THIS GENERATION**: BANNED
30. **Adding any new indicator or condition**: BANNED this generation

# ══════════════════════════════════════════════════════════════════
# SECTION 7 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════

### ⭐ PHASE B: TP Widening (ACTIVE — NEXT STEP IS TP=8.0%)

```
4.6 → 5.0 → 5.5 → 6.0 → 7.0 [CONFIRMED ✓] → 8.0 ← TEST THIS NOW
```

**This generation: propose take_profit_pct = 8.0**
**This is the ONLY authorized change. Copy everything else from champion YAML.**

Expected results for TP=8.0%:
- Sharpe: +0.3357 → toward 0.40–0.55
- Trades: ~1650–1780 (slight drop from 1752 acceptable at higher TP)
- WR: ~47–50% (slight drop acceptable)

Warning signs (stop immediately):
- Trades ~716  → PRIMARY ATTRACTOR — RSI values wrong (check: must be 35.97 / 72)
- Trades ~599  → engine YAML poison — RSI short wrong (must be 72, not 68.63)
- Trades ~281  → old attractor — RSI long too high or pairs missing
- Trades ~982  → secondary attractor — RSI period or threshold wrong
- Trades ~1793 → OLD champion used (TP=7.0 not 8.0) — this is the no-change trap
- Trades ~1752 WITH Sharpe=+0.3357 → no-change (TP still 7.0) — discarded
- Trades < 1500 → likely attractor — investigate before accepting

**TP progression logic:**
- TP=8.0 confirmed new_best → next: TP=9.0%
- TP=8.0 fails 3 consecutive confirmed tests → Phase E (SL) or Phase C (timeout)
- Never reduce TP below 7.0 (current champion floor)

### PHASE C: Timeout Extension (FALLBACK — only after 3 confirmed TP=8.0 failures)

```
720 → 960 → 1200 → 1440 minutes
```

Note: timeout changes may trigger 716-trade or 982-trade attractor. Check carefully.

### PHASE A-Refined: RSI Threshold Tuning (AFTER Phase B complete)

```
35.97 → 37 → 38 →