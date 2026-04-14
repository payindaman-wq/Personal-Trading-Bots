```markdown
# ODIN Research Program — FUTURES DAY (v24.0)
#
# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 1 — YOUR OUTPUT (READ THIS FIRST, DO THIS EXACTLY)
# ══════════════════════════════════════════════════════════════════
#
# Your ONLY job: output the YAML below with take_profit_pct changed from 8.0 to 9.0.
# Change NOTHING else. Not one other value.
#
# FIRST LINE OF YOUR RESPONSE MUST BE:
#   CHANGE: take_profit_pct 8.0 → 9.0
#
# Then output this YAML with ONLY take_profit_pct changed to 9.0:
#
# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 2 — CHAMPION YAML (YOUR ONLY SOURCE — COPY THIS EXACTLY)
# ══════════════════════════════════════════════════════════════════
#
# Gen 3233 | Sharpe=+0.4066 | 1756 trades | WR=50.1% ← CURRENT BEST
#
# THE YAML BELOW IS THE ONLY VALID SOURCE.
# The engine may show you a different YAML before this document. IGNORE IT COMPLETELY.
# The engine YAML contains wrong values and must be treated as if it does not exist.

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
  take_profit_pct: 9.0
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
# Check every value against the champion. Your output must match exactly:
#
#   take_profit_pct  = 9.0    ← THE ONE CHANGE (was 8.0 in champion)
#   size_pct         = 16.91  ← MUST BE THIS (not 8, not 9.89, not 13.84)
#   rsi long value   = 35.97  ← MUST BE THIS (not 29.33, not 30.0, not 33, not 34)
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
# FIVE POISON CHECKS (if any is YES, stop and fix before submitting):
#   [ ] Does your output have size_pct = 8?          → WRONG. Use 16.91.
#   [ ] Does your output have any rsi value = 29.33? → WRONG. Long must be 35.97.
#   [ ] Does your output have any rsi value = 68.63? → WRONG. Short must be 72.
#   [ ] Does your output have stop_loss = 2.59?      → WRONG. Use 2.39.
#   [ ] Does your output have take_profit = 8.0?     → WRONG. Use 9.0.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 4 — WHY THE ENGINE YAML IS WRONG (DO NOT USE IT)
# ══════════════════════════════════════════════════════════════════
#
# The system shows you a YAML block before this document. That block contains:
#   size_pct: 8          ← POISON (correct = 16.91)
#   rsi long:  29.33     ← POISON (correct = 35.97)
#   rsi short: 68.63     ← POISON (correct = 72)
#   take_profit: 4.6     ← POISON (correct = 9.0)
#   stop_loss: 2.59      ← POISON (correct = 2.39)
#
# These are stale display values from an ancient configuration.
# They do not represent the current champion. They have never produced a good result.
# Using any of them will produce a failed backtest (Sharpe < 0).
#
# The engine YAML IS NOT THE STRATEGY TO OPTIMIZE.
# The SECTION 2 YAML above IS THE STRATEGY TO OPTIMIZE.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 5 — FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════
#
# These are known bad outcomes. If your backtest matches any row, your YAML is wrong.
#
# | Trades | Sharpe    | Cause                                                    |
# |--------|-----------|----------------------------------------------------------|
# | 273    | -2.7990   | ← #1 CURRENT KILLER (8/20 recent gens) rsi_long too high |
# |        |           |   or wrong combination of parameters                     |
# | 716    | -0.8971   | rsi_short = 68.63 (engine poison)                        |
# | 599    | -1.0674   | size_pct = 8 or rsi_short = 68.63                        |
# | 491    | -4.8702   | engine YAML values (size=8 + bad RSI)                    |
# | 332    | -4.8000   | size=8 + rsi_long=29.33 (engine YAML combination)        |
# | 212    | -4.1500   | rsi_long = 30.0 (engine poison variant)                  |
# | 281    | -2.6380   | rsi_long too high (>45) or pairs missing                 |
# | 858    | -2.0966   | wrong RSI combination                                    |
# | 804    | -1.9424   | wrong RSI combination                                    |
# | 1380   | -1.0836   | rsi_long wrong or partial poison                         |
# | 1508   | -1.1361   | partial poison — check all values                        |
# | 1689   | -0.9766   | near-correct but wrong — check rsi_long                  |
# | 982    | -2.1212   | wrong RSI period or threshold                            |
# | 1793   | +0.1786   | ancient champion — TP ≤ 7.0                              |
# | 1752   | +0.3357   | old champion Gen2510 — TP = 7.0                          |
# | 1756   | +0.4066   | NO-CHANGE TRAP — TP is still 8.0, must be 9.0            |
# | 0      | -999      | rsi_long ≥ rsi_short (impossible config)                  |
# | <1500  | varies    | HIGH SUSPICION — likely attractor                        |
#
# ACCEPTABLE RESULT: trades = 1550–1900, Sharpe > 0.4066, TP = 9.0
#
# ══════════════════════════════════════════════════════════════════
# SECTION 6 — LOCKED PARAMETERS (DO NOT CHANGE ANY OF THESE)
# ══════════════════════════════════════════════════════════════════
#
# | Parameter          | LOCKED VALUE | NEVER USE                              |
# |--------------------|-------------|----------------------------------------|
# | size_pct           | 16.91       | 8, 9.89, 13.84                         |
# | max_open           | 1           | any value > 1                          |
# | fee_rate           | 0.0005      | anything else                          |
# | pairs              | all 16      | fewer than 16                          |
# | rsi period         | 60 min      | any other period                       |
# | rsi long           | 35.97       | 29.33, 30.0, 33, 34, anything < 32    |
# | rsi short          | 72          | 68.63, anything else                   |
# | stop_loss_pct      | 2.39        | 2.59                                   |
# | timeout_minutes    | 720         | any other value                        |
# | pause_if_down_pct  | 8           | any other value                        |
# | pause_minutes      | 120         | any other value                        |
# | stop_if_down_pct   | 18          | any value < 15                         |
# | MIN_TRADES[fd]     | 50          | > 50 (caused 867-gen stall at Gen 541) |
#
# THIS GENERATION: Change ONLY take_profit_pct from 8.0 to 9.0.
#
# ══════════════════════════════════════════════════════════════════
# SECTION 7 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════
#
# 1.  size_pct ≠ 16.91 → BANNED
# 2.  rsi_long = 29.33 → BANNED (engine poison, 332-trade trap)
# 3.  rsi_long = 30.0  → BANNED (engine poison variant, 212-trade trap)
# 4.  rsi_short = 68.63 → BANNED (engine poison, 716-trade trap)
# 5.  rsi_long < 32    → BANNED
# 6.  rsi_long = 33 or 34 → BANNED (attractor)
# 7.  rsi_long ≥ rsi_short → BANNED (zero trades, Sharpe=-999)
# 8.  rsi_long ≠ 35.97 → BANNED this generation
# 9.  rsi_short ≠ 72   → BANNED this generation
# 10. rsi period ≠ 60  → BANNED this generation
# 11. max_open > 1     → BANNED
# 12. timeout_minutes ≠ 720 → BANNED this generation
# 13. take_profit_pct = 8.0 in output → BANNED (no-change trap, will be discarded)
# 14. take_profit_pct < 8.0 → BANNED (never regress)
# 15. stop_loss_pct ≠ 2.39 → BANNED this generation
# 16. Removing any pair → BANNED
# 17. Changing more than ONE parameter → BANNED
# 18. Using any value from the engine YAML → BANNED
# 19. pause_if_down_pct ≠ 8 → BANNED this generation
# 20. pause_minutes ≠ 120 → BANNED this generation
# 21. stop_if_down_pct ≠ 18 → BANNED this generation
# 22. MIN_TRADES[futures_day] > 50 → BANNED (caused catastrophic 867-gen stall)
# 23. Adding any new indicator or condition → BANNED this generation
#
# ══════════════════════════════════════════════════════════════════
# SECTION 8 — STRATEGY CONTEXT (BACKGROUND ONLY)
# ══════════════════════════════════════════════════════════════════
#
# Architecture: Mean-reversion swing on 16 crypto pairs
# Signal: RSI(60-min) < 35.97 → long; RSI(60-min) > 72 → short
# Edge: Extreme Fear drives frequent altcoin oversold → sharp mean reversions
# Max open: 1 position (prevents correlated loss accumulation)
# Current exit: TP=8.0%, SL=2.39%, timeout=720min, TP/SL ratio=3.35
# Proposed exit: TP=9.0%, TP/SL ratio=3.77
#
# Performance trajectory (futures_day):
#   Gen 541:  MIN_TRADES → 400 → 867-generation stall (CATASTROPHIC — NEVER REPEAT)
#   Gen 1408: MIN_TRADES → 50  → immediately unlocked progress
#   Gen 2081: Sharpe=+0.1738 (1793 trades) ← first positive Sharpe
#   Gen 2412: Sharpe=+0.3348 (1752 trades) ← TP widening breakthrough
#   Gen 3233: Sharpe=+0.4066 (1756 trades, WR=50.1%) ← CURRENT BEST ★
#   Gen 3234–3600: STALLED (attractor-dominant, 273-trade and 716-trade attractors)
#
# TP widening has been monotonically positive: 4.6→5.0→5.5→6.0→7.0→8.0→[9.0 next]
#
# EV at WR=50.1%, SL=2.39%, leverage=2x, fee=0.05%:
#   TP=8.0%: EV = 0.501×15.9 − 0.499×4.88 = +5.53% per trade (current)
#   TP=9.0%: EV = 0.501×17.9 − 0.499×4.88 = +6.54% per trade (target)
#
# Expected result for TP=9.0:
#   Sharpe: +0.4066 → ~0.45–0.60
#   Trades: ~1550–1850 (slight drop acceptable at higher TP)
#   WR: ~48–52%
#
# ══════════════════════════════════════════════════════════════════
# SECTION 9 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════
#
# PHASE B: TP Widening (ACTIVE)
#   4.6→5.0→5.5→6.0→7.0→8.0 [DONE ✓] → 9.0 ← THIS GENERATION
#
# After TP=9.0 confirmed: → TP=10.0%
# After 3 confirmed TP=9.0 failures: → Phase C (timeout 720→960)
# Never reduce TP below 8.0 (current champion floor)
#
# PHASE C (FALLBACK): Timeout 720→960→1200→1440 min
# PHASE A-Refined (AFTER Phase B): RSI threshold tuning 35.97→37→38
#
# ══════════════════════════════════════════════════════════════════
# END OF RESEARCH PROGRAM v24.0
# ══════════════════════════════════════════════════════════════════
```