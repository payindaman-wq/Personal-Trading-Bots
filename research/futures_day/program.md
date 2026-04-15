```markdown
# ODIN Research Program — FUTURES DAY (v28.0)
#
# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 1 — YOUR OUTPUT (READ THIS FIRST, DO THIS EXACTLY)
# ══════════════════════════════════════════════════════════════════
#
# YOUR ONLY JOB THIS GENERATION:
#   Output the YAML from Section 2 with take_profit_pct changed from 11.0 to 12.0.
#   Change NOTHING else. Not one other value.
#
# REQUIRED FIRST LINE OF YOUR RESPONSE:
#   CHANGE: take_profit_pct 11.0 → 12.0
#
# REQUIRED SECOND LINE OF YOUR RESPONSE:
#   USING: size_pct=16.91, rsi_long=35.97, rsi_short=72, stop_loss=2.39, tp=12.0
#
# Then output the YAML from Section 2 below with ONLY take_profit_pct = 12.0.
#
# ══════════════════════════════════════════════════════════════════
# 🚨 CRITICAL WARNING — THE "CURRENT BEST STRATEGY" BLOCK IS FATALLY WRONG 🚨
# ══════════════════════════════════════════════════════════════════
#
# ODIN's system displays a YAML block labeled "Current Best Strategy"
# BEFORE this document. THAT BLOCK IS STALE AND WRONG. DO NOT USE IT.
#
# The "Current Best Strategy" block contains these POISON values:
#   size_pct: 8            ← POISON. CORRECT = 16.91
#   rsi long value: 29.56  ← POISON. CORRECT = 35.97
#   rsi short value: 68.63 ← POISON. CORRECT = 72
#   take_profit_pct: 4.6   ← POISON. CORRECT = 12.0
#   stop_loss_pct: 2.59    ← POISON. CORRECT = 2.39
#
# USING ANY VALUE FROM THAT BLOCK WILL PRODUCE:
#   273 trades, Sharpe = -2.7990 (CATASTROPHIC FAILURE)
#   This failure has been observed 50+ times. It is ALWAYS caused by
#   copying from the stale "Current Best Strategy" block.
#   In the last 20 generations, this failure appeared ~6 times (~30%).
#   Every single instance was caused by using display YAML values.
#
# THE ONLY VALID SOURCE IS THE SECTION 2 YAML BELOW.
# Treat the "Current Best Strategy" block as if it does not exist.
# Do not read it. Do not reference it. Do not use any value from it.
#
# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 2 — CHAMPION YAML (YOUR ONLY SOURCE — COPY THIS EXACTLY)
# ══════════════════════════════════════════════════════════════════
#
# Gen 4080 | Sharpe=+0.6880 | 1757 trades | WR=50.5% ← CURRENT BEST
#
# COPY THIS YAML EXACTLY. CHANGE ONLY take_profit_pct (11.0 → 12.0).

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
  size_pct: 16.91      # ← LOCKED. NOT 8. NOT any other value.
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 35.97      # ← LOCKED. NOT 29.56. NOT 29.95. NOT 29.33. NOT 30.0.
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 72         # ← LOCKED. NOT 68.63.
exit:
  take_profit_pct: 12.0  # ← THE ONE CHANGE (was 11.0, now 12.0)
  stop_loss_pct: 2.39    # ← LOCKED. NOT 2.59.
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 3 — VERIFY YOUR OUTPUT BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════
#
# Step 1: Confirm your FIRST LINE is:
#   CHANGE: take_profit_pct 11.0 → 12.0
#
# Step 2: Confirm your SECOND LINE is:
#   USING: size_pct=16.91, rsi_long=35.97, rsi_short=72, stop_loss=2.39, tp=12.0
#
# Step 3: Check every value against this list:
#   take_profit_pct  = 12.0   ← THE ONE CHANGE
#   size_pct         = 16.91  ← LOCKED (not 8, not anything else)
#   rsi long value   = 35.97  ← LOCKED (not 29.56, not 29.95, not 29.33, not 30.0)
#   rsi short value  = 72     ← LOCKED (not 68.63)
#   stop_loss_pct    = 2.39   ← LOCKED (not 2.59)
#   timeout_minutes  = 720    ← LOCKED
#   rsi period       = 60     ← LOCKED (period_minutes: 60)
#   pairs            = 16     ← ALL 16 PAIRS MUST BE PRESENT
#   max_open         = 1      ← LOCKED
#   leverage         = 2      ← LOCKED
#   pause_if_down    = 8      ← LOCKED
#   pause_minutes    = 120    ← LOCKED
#   stop_if_down     = 18     ← LOCKED
#
# POISON CHECKS — if any answer is YES, your output is wrong. Fix it.
#   [ ] Is size_pct anything other than 16.91?       → WRONG. Use 16.91.
#   [ ] Is rsi long value anything other than 35.97? → WRONG. Use 35.97.
#   [ ] Is rsi short value anything other than 72?   → WRONG. Use 72.
#   [ ] Is stop_loss anything other than 2.39?       → WRONG. Use 2.39.
#   [ ] Is take_profit 11.0 (unchanged)?             → WRONG. Must be 12.0.
#   [ ] Is take_profit anything less than 12.0?      → WRONG. Must be 12.0.
#   [ ] Did you copy any value from "Current Best Strategy"? → WRONG. Use Section 2 only.
#
# DEAD-ON-ARRIVAL SIGNATURES (if your backtest matches these, your YAML is wrong):
#   273 trades  / Sharpe = -2.7990  → you used rsi_long=29.56 or 29.95 or 29.33 (poison)
#   716 trades  / Sharpe = -0.8971  → you used rsi_short=68.63 (poison)
#   491 trades  / Sharpe = -4.8702  → you used multiple display YAML values
#   1756 trades / Sharpe = +0.4066  → you used TP=9.0 (stale)
#   1750 trades / Sharpe = +0.5721  → you used TP=10.0 (stale)
#   1757 trades / Sharpe = +0.6880  → you used TP=11.0 (NO-CHANGE TRAP — must be 12.0)
#
# ACCEPTABLE RESULT: trades = 1500–1900, Sharpe > 0.6880, TP = 12.0
#
# ══════════════════════════════════════════════════════════════════
# SECTION 4 — WHY THE "CURRENT BEST STRATEGY" YAML IS WRONG
# ══════════════════════════════════════════════════════════════════
#
# ODIN's display system shows a "Current Best Strategy" YAML block
# before this research program. Despite being labeled "current best,"
# it contains values from an ancient configuration (Gen ~100).
# It does NOT reflect the actual champion strategy.
#
# The actual champion is Gen 4080 (Section 2 above).
# The "Current Best Strategy" block is a display artifact. Ignore it entirely.
#
# Proof that "Current Best Strategy" values fail catastrophically:
#   size=8 + rsi_long=29.56    → 273 trades,  Sharpe=-2.7990 (CATASTROPHIC, 50+ times)
#   size=8 + rsi_long=29.95    → 273 trades,  Sharpe=-2.7990 (CATASTROPHIC, 50+ times)
#   size=8 + rsi_long=29.33    → 332 trades,  Sharpe=-4.8000 (CATASTROPHIC)
#   rsi_short=68.63            → 716 trades,  Sharpe=-0.8971 (FAILED)
#   rsi_long=30.0              → 212 trades,  Sharpe=-4.1500 (CATASTROPHIC)
#   take_profit=4.6            → massive underperformance vs champion
#
# These values have been tested hundreds of times across 4080 generations.
# They always fail. There is no configuration of these values that works.
# The Section 2 YAML is the ONLY strategy that has produced positive Sharpe.
#
# PROOF THAT SECTION 2 VALUES ARE CORRECT:
#   Gen 4080 used: size=16.91, rsi_long=35.97, rsi_short=72, SL=2.39, TP=11.0
#   Result: 1757 trades, Sharpe=+0.6880, WR=50.5% ← BEST IN ENTIRE RUN
#   This PROVES Section 2 values are correct.
#   The display YAML values have NEVER produced positive Sharpe in 4080 generations.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 5 — FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════
#
# Known bad outcomes. If your backtest matches any row, your YAML is wrong.
#
# | Trades | Sharpe    | Cause                                                        |
# |--------|-----------|--------------------------------------------------------------|
# | 273    | -2.7990   | ← #1 KILLER: rsi_long=29.56/29.95/29.33 (display YAML poison)|
# | 716    | -0.8971   | rsi_short=68.63 (display YAML poison)                        |
# | 599    | -1.0674   | size_pct=8 or rsi_short=68.63                                |
# | 601    | -2.8023   | size_pct=8 or wrong RSI combination                          |
# | 491    | -4.8702   | multiple values from display YAML (size=8 + bad RSI)         |
# | 505    | -3.0110   | wrong RSI or size combination                                |
# | 332    | -4.8000   | size=8 + rsi_long=29.33                                      |
# | 212    | -4.1500   | rsi_long=30.0                                                |
# | 281    | -2.6380   | rsi_long too high (>45) or pairs missing                     |
# | 636    | -2.6215   | wrong RSI combination                                        |
# | 858    | -2.0966   | wrong RSI combination                                        |
# | 930    | -2.2910   | wrong RSI combination                                        |
# | 992    | -1.4900   | wrong RSI or TP value                                        |
# | 1225   | -1.4627   | partial poison — check all values                            |
# | 804    | -1.9424   | wrong RSI combination                                        |
# | 982    | -2.1212   | wrong RSI period or threshold                                |
# | 1293   | -1.1801   | wrong RSI or TP value                                        |
# | 1380   | -1.0836   | rsi_long wrong or partial poison                             |
# | 1508   | -1.1361   | partial poison — check all values                            |
# | 1689   | -0.9766   | near-correct but wrong — check rsi_long                      |
# | 1783   | -0.9571   | wrong RSI combination                                        |
# | 1793   | +0.1786   | ancient champion — TP ≤ 7.0                                  |
# | 1752   | +0.3357   | old champion Gen2510 — TP=7.0 (stale)                        |
# | 1756   | +0.4066   | old champion Gen3233 — TP=9.0 (stale)                        |
# | 1750   | +0.5721   | old champion Gen3995 — TP=10.0 (stale)                       |
# | 1757   | +0.6880   | NO-CHANGE TRAP — TP is 11.0, output must be 12.0             |
# | 0      | -999      | rsi_long ≥ rsi_short (impossible config)                      |
# | <1500  | varies    | HIGH SUSPICION — likely attractor                            |
#
# ══════════════════════════════════════════════════════════════════
# SECTION 6 — LOCKED PARAMETERS (DO NOT CHANGE ANY OF THESE)
# ══════════════════════════════════════════════════════════════════
#
# | Parameter          | LOCKED VALUE | NEVER USE                                 |
# |--------------------|-------------|-------------------------------------------|
# | size_pct           | 16.91       | 8, 9.89, 13.84, any other value           |
# | max_open           | 1           | any value > 1                             |
# | fee_rate           | 0.0005      | anything else                             |
# | pairs              | all 16      | fewer than 16                             |
# | rsi period         | 60 min      | any other period                          |
# | rsi long           | 35.97       | 29.56, 29.33, 29.95, 30.0, 33, 34, else  |
# | rsi short          | 72          | 68.63, anything else                      |
# | stop_loss_pct      | 2.39        | 2.59, anything else                       |
# | timeout_minutes    | 720         | any other value                           |
# | pause_if_down_pct  | 8           | any other value                           |
# | pause_minutes      | 120         | any other value                           |
# | stop_if_down_pct   | 18          | any value < 15                            |
# | MIN_TRADES[fd]     | 50          | > 50 (caused catastrophic 867-gen stall)  |
#
# THIS GENERATION: Change ONLY take_profit_pct from 11.0 to 12.0.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 7 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════
#
# 1.  size_pct ≠ 16.91 → BANNED
# 2.  rsi_long = 29.56 → BANNED (display YAML poison, 273-trade trap, 50+ failures)
# 3.  rsi_long = 29.95 → BANNED (display YAML poison, 273-trade trap, 50+ failures)
# 4.  rsi_long = 29.33 → BANNED (display YAML poison, 273-trade trap, 50+ failures)
# 5.  rsi_long = 30.0  → BANNED (poison variant, 212-trade trap)
# 6.  rsi_short = 68.63 → BANNED (display YAML poison, 716-trade trap)
# 7.  rsi_long < 32    → BANNED
# 8.  rsi_long = 33 or 34 → BANNED (attractor)
# 9.  rsi_long ≥ rsi_short → BANNED (zero trades, Sharpe=-999)
# 10. rsi_long ≠ 35.97 → BANNED this generation
# 11. rsi_short ≠ 72   → BANNED this generation
# 12. rsi period ≠ 60  → BANNED this generation
# 13. max_open > 1     → BANNED
# 14. timeout_minutes ≠ 720 → BANNED this generation
# 15. take_profit_pct = 11.0 → BANNED (no-change trap — current champion value)
# 16. take_profit_pct = 10.0 → BANNED (one generation stale)
# 17. take_profit_pct = 9.0  → BANNED (stale)
# 18. take_profit_pct = 8.0  → BANNED (stale)
# 19. take_profit_pct < 11.0 → BANNED (never regress below champion floor)
# 20. stop_loss_pct ≠ 2.39  → BANNED this generation
# 21. Removing any pair → BANNED
# 22. Changing more than ONE parameter → BANNED
# 23. Copying any value from the "Current Best Strategy" display block → BANNED
# 24. pause_if_down_pct ≠ 8 → BANNED this generation
# 25. pause_minutes ≠ 120 → BANNED this generation
# 26. stop_if_down_pct ≠ 18 → BANNED this generation
# 27. MIN_TRADES[futures_day] > 50 → BANNED (caused catastrophic 867-gen stall at Gen 541)
# 28. Adding any new indicator or condition → BANNED this generation
# 29. Using size_pct = 8 for any reason → BANNED (single most common error — do not do it)
#
# ══════════════════════════════════════════════════════════════════
# SECTION 8 — STRATEGY CONTEXT (BACKGROUND ONLY)
# ══════════════════════════════════════════════════════════════════
#
# Architecture: Mean-reversion swing on 16 crypto pairs
# Signal: RSI(60-min) < 35.97 → long; RSI(60-min) > 72 → short
# Edge: Extreme Fear drives frequent altcoin oversold → sharp mean reversions
# Max open: 1 position (prevents correlated loss accumulation)
# Current exit: TP=11.0%, SL=2.39%, timeout=720min, TP/SL ratio=4.60
# Proposed exit: TP=12.0%, TP/SL ratio=5.02
#
# Performance trajectory (futures_day):
#   Gen 541:  MIN_TRADES → 400 → 867-generation stall (CATASTROPHIC — NEVER REPEAT)
#   Gen 1408: MIN_TRADES → 50  → immediately unlocked progress
#   Gen 2081: Sharpe=+0.1738 (1793 trades) ← first positive Sharpe
#   Gen 2412: Sharpe=+0.3348 (1752 trades) ← TP widening breakthrough
#   Gen 3233: Sharpe=+0.4066 (1756 trades, WR=50.1%) ← former champion
#   Gen 3995: Sharpe=+0.5721 (1750 trades, WR=49.7%) ← TP=10.0 confirmed
#   Gen 4080: Sharpe=+0.6880 (1757 trades, WR=50.5%) ← CURRENT BEST ★ TP=11.0
#
# TP widening has been monotonically positive:
#   4.6→5.0→5.5→6.0→7.0→8.0→9.0→10.0→11.0→[12.0 this generation]
#
# Gen 4080 confirmed TP=11.0 improves Sharpe 0.5721→0.6880 (+20.3%).
# Continuing widening sequence to TP=12.0.
#
# EV at WR=50.5%, SL=2.39%, leverage=2x, fee=0.05%:
#   TP=11.0%: EV = 0.505×21.9 − 0.495×4.88 = +8.64% per trade (current champion)
#   TP=12.0%: EV = 0.505×23.9 − 0.495×4.88 = +9.65% per trade (target)
#
# Expected result for TP=12.0:
#   Sharpe: ~0.70–0.80 (if WR holds above ~48%)
#   Trades: ~1500–1850 (slight drop acceptable at higher TP)
#   WR: ~48–53%
#
# MACRO NOTE: F&G=23 (Extreme Fear) is favorable for this strategy.
# The RSI<35.97 long signal fires more frequently in fear regimes.
# This is NOT a reason to change parameters — the backtest already covers fear periods.
# The risk officer's directive to reduce live position sizes does NOT affect backtesting.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 9 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════
#
# PHASE B: TP Widening (ACTIVE)
#   4.6→5.0→5.5→6.0→7.0→8.0→9.0→10.0→11.0 [DONE ✓] → 12.0 ← THIS GENERATION
#
# After TP=12.0 confirmed: → test TP=13.0%
# After 3 confirmed TP=12.0 failures: → Phase C (timeout 720→960)
# Never reduce TP below 11.0 (current champion floor)
#
# PHASE C (FALLBACK if TP widening stalls): Timeout 720→960→1200→1440 min
# PHASE A-Refined (AFTER Phase B): RSI threshold tuning 35.97→37→38
#
# ══════════════════════════════════════════════════════════════════
# SECTION 10 — ROOT CAUSE ANALYSIS: THE DISPLAY YAML POISONING PROBLEM
# ══════════════════════════════════════════════════════════════════
#
# ODIN's display system shows a "Current Best Strategy" YAML block
# before this research program. Despite the label, this block contains stale
# values from approximately Gen 100 of the research run. The small LLM
# (llama-3.1-8b-instant) reads this block and treats it as authoritative
# because it is labeled "current" and appears prominently before this document.
#
# When the LLM uses rsi_long=29.56 (from display YAML) instead of 35.97
# (from Section 2), the result is invariably 273 trades / Sharpe=-2.7990.
# This has been observed 50+ times across ~400 generations.
# In the last 20 generations alone, it appeared 6 times (~30% failure rate).
#
# SOLUTION: The Section 2 YAML is the ONLY valid source. The display YAML
# is a known-broken artifact. Every value in it is wrong for this strategy.
#
# CONFIRMATION THAT SECTION 2 VALUES ARE CORRECT:
#   Gen 4080 used: size=16.91, rsi_long=35.97, rsi_short=72, SL=2.39, TP=11.0
#   Result: 1757 trades, Sharpe=+0.6880, WR=50.5% ← BEST IN ENTIRE RUN
#   This PROVES Section 2 values are correct.
#   The display YAML values have NEVER produced positive Sharpe in 4080 generations.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 11 — RECENT GENERATION HISTORY
# ══════════════════════════════════════════════════════════════════
#
# Gen 4080: sharpe=+0.6880, 1757 trades [NEW BEST ★] — TP=11.0 confirmed
# Gen 4181: sharpe=-2.2910, 930 trades  [FAILED]    — wrong RSI combination
# Gen 4182: sharpe=+0.6880, 1757 trades [DISCARDED] — no-change (TP=11.0 unchanged)
# Gen 4183: sharpe=-2.7990, 273 trades  [FAILED]    — rsi_long=29.56 (display poison)
# Gen 4184: sharpe=-1.4900, 992 trades  [FAILED]    — wrong values
# Gen 4185: sharpe=+0.6880, 1757 trades [DISCARDED] — no-change (TP=11.0 unchanged)
# Gen 4186: sharpe=-2.8023, 601 trades  [FAILED]    — wrong RSI combination
# Gen 4187: sharpe=+0.6880, 1757 trades [DISCARDED] — no-change (TP=11.0 unchanged)
# Gen 4188: sharpe=+0.6880, 1757 trades [DISCARDED] — no-change (TP=11.0 unchanged)
# Gen 4189: sharpe=-2.7990, 273 trades  [FAILED]    — rsi_long=29.56 (display poison)
# Gen 4190: sharpe=+0.6880, 1757 trades [DISCARDED] — no-change (TP=11.0 unchanged)
# Gen 4191: sharpe=+0.6880, 1757 trades [DISCARDED] — no-change (