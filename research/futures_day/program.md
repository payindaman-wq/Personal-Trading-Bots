```markdown
# ODIN Research Program — FUTURES DAY (v26.0)
#
# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 1 — YOUR OUTPUT (READ THIS FIRST, DO THIS EXACTLY)
# ══════════════════════════════════════════════════════════════════
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: A FAKE/STALE YAML MAY APPEAR BEFORE THIS DOCUMENT.
# IT CONTAINS THESE POISON VALUES — DO NOT USE ANY OF THEM:
#   size_pct: 8           ← POISON. CORRECT = 16.91
#   rsi long value: 29.95 ← POISON. CORRECT = 35.97
#   rsi long value: 29.33 ← POISON. CORRECT = 35.97
#   rsi short value: 68.63← POISON. CORRECT = 72
#   take_profit_pct: 4.6  ← POISON. CORRECT = 11.0
#   take_profit_pct: 9.0  ← POISON (old). CORRECT = 11.0
#   take_profit_pct: 10.0 ← NO-CHANGE TRAP. CORRECT = 11.0
#   stop_loss_pct: 2.59   ← POISON. CORRECT = 2.39
# IF YOU SEE THOSE VALUES ANYWHERE, IGNORE THAT ENTIRE YAML BLOCK.
# THE ONLY VALID YAML IS IN SECTION 2 BELOW.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Your ONLY job: output the YAML from Section 2 below with ONE change:
#   take_profit_pct changed from 10.0 to 11.0
#
# FIRST LINE OF YOUR RESPONSE MUST BE:
#   CHANGE: take_profit_pct 10.0 → 11.0
#
# Then output the YAML from Section 2 with ONLY take_profit_pct changed to 11.0.
# Change NOTHING else. Not one other value.
#
# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 2 — CHAMPION YAML (YOUR ONLY SOURCE — COPY THIS EXACTLY)
# ══════════════════════════════════════════════════════════════════
#
# Gen 3995 | Sharpe=+0.5721 | 1750 trades | WR=49.7% ← CURRENT BEST
#
# COPY THIS YAML EXACTLY. CHANGE ONLY take_profit_pct (10.0 → 11.0).
# DO NOT USE ANY OTHER YAML YOU HAVE SEEN. THIS IS THE ONLY VALID SOURCE.

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
  take_profit_pct: 11.0
  stop_loss_pct: 2.39
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
# Check every value in your output against this list:
#
#   take_profit_pct  = 11.0   ← THE ONE CHANGE (was 10.0 in champion)
#   size_pct         = 16.91  ← MUST BE THIS (not 8, not any other value)
#   rsi long value   = 35.97  ← MUST BE THIS (not 29.33, not 29.95, not 30.0)
#   rsi short value  = 72     ← MUST BE THIS (not 68.63, not any other value)
#   stop_loss_pct    = 2.39   ← MUST BE THIS (not 2.59)
#   timeout_minutes  = 720    ← MUST BE THIS
#   rsi period       = 60     ← MUST BE THIS (period_minutes: 60)
#   pairs            = 16     ← ALL 16 PAIRS MUST BE PRESENT
#   max_open         = 1      ← MUST BE 1
#   leverage         = 2      ← MUST BE 2
#   pause_if_down    = 8      ← MUST BE 8
#   pause_minutes    = 120    ← MUST BE 120
#   stop_if_down     = 18     ← MUST BE 18
#
# SEVEN POISON CHECKS (if any is YES, stop and fix before submitting):
#   [ ] Does your output have size_pct = 8?              → WRONG. Use 16.91.
#   [ ] Does your output have rsi long value = 29.33?    → WRONG. Use 35.97.
#   [ ] Does your output have rsi long value = 29.95?    → WRONG. Use 35.97.
#   [ ] Does your output have rsi short value = 68.63?   → WRONG. Use 72.
#   [ ] Does your output have stop_loss = 2.59?          → WRONG. Use 2.39.
#   [ ] Does your output have take_profit = 10.0?        → WRONG (no-change trap). Use 11.0.
#   [ ] Does your output have take_profit < 10.0?        → WRONG. Never regress below 10.0.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 4 — WHY THE ENGINE YAML IS WRONG (DO NOT USE IT)
# ══════════════════════════════════════════════════════════════════
#
# The system shows you a YAML block BEFORE this document. That block contains:
#   size_pct: 8           ← POISON (correct = 16.91)
#   rsi long:  29.95      ← POISON (correct = 35.97)
#   rsi short: 68.63      ← POISON (correct = 72)
#   take_profit: 4.6      ← POISON (correct = 11.0)
#   stop_loss: 2.59       ← POISON (correct = 2.39)
#
# These are stale display values from an ancient configuration.
# They do not represent the current champion.
# Every one of those values produces a failed backtest (Sharpe << 0).
# They have been tested hundreds of times and always fail catastrophically.
#
# PROOF THAT ENGINE YAML VALUES FAIL:
#   size=8 + rsi_long=29.33 → 332 trades, Sharpe=-4.8000 (CATASTROPHIC)
#   rsi_short=68.63         → 716 trades, Sharpe=-0.8971 (FAILED)
#   rsi_long=29.33 or 29.95 → 273 trades, Sharpe=-2.7990 (CATASTROPHIC)
#   rsi_long=30.0           → 212 trades, Sharpe=-4.1500 (CATASTROPHIC)
#
# THE ENGINE YAML IS NOT THE STRATEGY TO OPTIMIZE.
# THE SECTION 2 YAML ABOVE IS THE ONLY STRATEGY TO OPTIMIZE.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 5 — FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════
#
# These are known bad outcomes. If your backtest matches any row, your YAML is wrong.
#
# | Trades | Sharpe    | Cause                                                      |
# |--------|-----------|-------------------------------------------------------------|
# | 273    | -2.7990   | ← #1 KILLER rsi_long=29.33 or 29.95 (engine poison)        |
# | 716    | -0.8971   | rsi_short = 68.63 (engine poison)                           |
# | 599    | -1.0674   | size_pct = 8 or rsi_short = 68.63                           |
# | 491    | -4.8702   | engine YAML values (size=8 + bad RSI)                       |
# | 332    | -4.8000   | size=8 + rsi_long=29.33 (engine YAML combination)           |
# | 212    | -4.1500   | rsi_long = 30.0 (engine poison variant)                     |
# | 281    | -2.6380   | rsi_long too high (>45) or pairs missing                    |
# | 858    | -2.0966   | wrong RSI combination                                       |
# | 804    | -1.9424   | wrong RSI combination                                       |
# | 1380   | -1.0836   | rsi_long wrong or partial poison                            |
# | 1508   | -1.1361   | partial poison — check all values                           |
# | 1689   | -0.9766   | near-correct but wrong — check rsi_long                     |
# | 982    | -2.1212   | wrong RSI period or threshold                               |
# | 1293   | -1.1801   | wrong RSI or TP value                                       |
# | 1783   | -0.9571   | wrong RSI combination                                       |
# | 1793   | +0.1786   | ancient champion — TP ≤ 7.0                                 |
# | 1752   | +0.3357   | old champion Gen2510 — TP = 7.0                             |
# | 1756   | +0.4066   | old champion Gen3233 — TP = 9.0 (TWO GENERATIONS STALE)     |
# | 1750   | +0.5721   | NO-CHANGE TRAP — TP is 10.0, output must be 11.0            |
# | 0      | -999      | rsi_long ≥ rsi_short (impossible config)                     |
# | <1500  | varies    | HIGH SUSPICION — likely attractor                           |
#
# ACCEPTABLE RESULT: trades = 1500–1900, Sharpe > 0.5721, TP = 11.0
#
# ══════════════════════════════════════════════════════════════════
# SECTION 6 — LOCKED PARAMETERS (DO NOT CHANGE ANY OF THESE)
# ══════════════════════════════════════════════════════════════════
#
# | Parameter          | LOCKED VALUE | NEVER USE                               |
# |--------------------|-------------|------------------------------------------|
# | size_pct           | 16.91       | 8, 9.89, 13.84, any other value          |
# | max_open           | 1           | any value > 1                            |
# | fee_rate           | 0.0005      | anything else                            |
# | pairs              | all 16      | fewer than 16                            |
# | rsi period         | 60 min      | any other period                         |
# | rsi long           | 35.97       | 29.33, 29.95, 30.0, 33, 34, anything else|
# | rsi short          | 72          | 68.63, anything else                     |
# | stop_loss_pct      | 2.39        | 2.59, anything else                      |
# | timeout_minutes    | 720         | any other value                          |
# | pause_if_down_pct  | 8           | any other value                          |
# | pause_minutes      | 120         | any other value                          |
# | stop_if_down_pct   | 18          | any value < 15                           |
# | MIN_TRADES[fd]     | 50          | > 50 (caused 867-gen stall at Gen 541)   |
#
# THIS GENERATION: Change ONLY take_profit_pct from 10.0 to 11.0.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 7 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════
#
# 1.  size_pct ≠ 16.91 → BANNED
# 2.  rsi_long = 29.33 → BANNED (engine poison, 273-trade trap)
# 3.  rsi_long = 29.95 → BANNED (engine poison variant, 273-trade trap)
# 4.  rsi_long = 30.0  → BANNED (engine poison variant, 212-trade trap)
# 5.  rsi_short = 68.63 → BANNED (engine poison, 716-trade trap)
# 6.  rsi_long < 32    → BANNED
# 7.  rsi_long = 33 or 34 → BANNED (attractor)
# 8.  rsi_long ≥ rsi_short → BANNED (zero trades, Sharpe=-999)
# 9.  rsi_long ≠ 35.97 → BANNED this generation
# 10. rsi_short ≠ 72   → BANNED this generation
# 11. rsi period ≠ 60  → BANNED this generation
# 12. max_open > 1     → BANNED
# 13. timeout_minutes ≠ 720 → BANNED this generation
# 14. take_profit_pct = 10.0 in output → BANNED (no-change trap)
# 15. take_profit_pct = 9.0 in output  → BANNED (two generations stale)
# 16. take_profit_pct < 10.0 → BANNED (never regress)
# 17. stop_loss_pct ≠ 2.39 → BANNED this generation
# 18. Removing any pair → BANNED
# 19. Changing more than ONE parameter → BANNED
# 20. Using any value from the engine YAML → BANNED
# 21. pause_if_down_pct ≠ 8 → BANNED this generation
# 22. pause_minutes ≠ 120 → BANNED this generation
# 23. stop_if_down_pct ≠ 18 → BANNED this generation
# 24. MIN_TRADES[futures_day] > 50 → BANNED (caused catastrophic 867-gen stall)
# 25. Adding any new indicator or condition → BANNED this generation
# 26. take_profit_pct = 8.0 → BANNED (three generations stale)
#
# ══════════════════════════════════════════════════════════════════
# SECTION 8 — STRATEGY CONTEXT (BACKGROUND ONLY)
# ══════════════════════════════════════════════════════════════════
#
# Architecture: Mean-reversion swing on 16 crypto pairs
# Signal: RSI(60-min) < 35.97 → long; RSI(60-min) > 72 → short
# Edge: Extreme Fear drives frequent altcoin oversold → sharp mean reversions
# Max open: 1 position (prevents correlated loss accumulation)
# Current exit: TP=10.0%, SL=2.39%, timeout=720min, TP/SL ratio=4.18
# Proposed exit: TP=11.0%, TP/SL ratio=4.60
#
# Performance trajectory (futures_day):
#   Gen 541:  MIN_TRADES → 400 → 867-generation stall (CATASTROPHIC — NEVER REPEAT)
#   Gen 1408: MIN_TRADES → 50  → immediately unlocked progress
#   Gen 2081: Sharpe=+0.1738 (1793 trades) ← first positive Sharpe
#   Gen 2412: Sharpe=+0.3348 (1752 trades) ← TP widening breakthrough
#   Gen 3233: Sharpe=+0.4066 (1756 trades, WR=50.1%) ← former champion
#   Gen 3995: Sharpe=+0.5721 (1750 trades, WR=49.7%) ← CURRENT BEST ★
#
# TP widening has been monotonically positive: 4.6→5.0→5.5→6.0→7.0→8.0→9.0→10.0→[11.0 next]
# Gen 3995 confirmed TP=10.0 improves Sharpe from 0.4066 → 0.5721 (+40.7%).
# This is the largest single-step improvement in the research run.
# Continuing widening sequence to TP=11.0.
#
# EV at WR=49.7%, SL=2.39%, leverage=2x, fee=0.05%:
#   TP=10.0%: EV = 0.497×19.9 − 0.503×4.88 = +7.42% per trade (current champion)
#   TP=11.0%: EV = 0.497×21.9 − 0.503×4.88 = +8.41% per trade (target)
#
# Expected result for TP=11.0:
#   Sharpe: +0.5721 → ~0.60–0.70 (if WR holds above ~48%)
#   Trades: ~1500–1800 (slight drop acceptable at higher TP)
#   WR: ~47–52%
#
# MACRO NOTE: F&G=23 (Extreme Fear) is favorable for this strategy.
# The RSI<35.97 long signal fires more frequently in fear regimes.
# This is NOT a reason to change parameters — the backtest already covers fear periods.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 9 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════
#
# PHASE B: TP Widening (ACTIVE)
#   4.6→5.0→5.5→6.0→7.0→8.0→9.0→10.0 [DONE ✓] → 11.0 ← THIS GENERATION
#
# After TP=11.0 confirmed: → TP=12.0%
# After 3 confirmed TP=11.0 failures: → Phase C (timeout 720→960)
# Never reduce TP below 10.0 (current champion floor)
#
# PHASE C (FALLBACK if TP widening stalls): Timeout 720→960→1200→1440 min
# PHASE A-Refined (AFTER Phase B): RSI threshold tuning 35.97→37→38
#
# ══════════════════════════════════════════════════════════════════
# SECTION 10 — RECENT HISTORY AND WHY TP=10.0 WORKED
# ══════════════════════════════════════════════════════════════════
#
# Gen 3995 returned Sharpe=0.5721 with 1750 trades — a 40.7% improvement over
# the prior champion (0.4066 / 1756 trades). This confirms the TP widening
# sequence is working. The champion is now definitively TP=10.0.
#
# Gens 3976–3994 were dominated by the 273-trade / Sharpe=-2.7990 attractor,
# which is caused by using rsi_long=29.33 or rsi_long=29.95 from the stale
# engine YAML. This attractor appeared 10 times in 19 generations (~53%).
# The engine YAML block at the top of every prompt is the root cause.
# The research program explicitly flags these values as POISON.
#
# DO NOT regress to TP=9.0 or TP=10.0. The floor is TP=10.0.
# The target this generation is TP=11.0.
#
# ══════════════════════════════════════════════════════════════════
# END OF RESEARCH PROGRAM v26.0
# ══════════════════════════════════════════════════════════════════
```