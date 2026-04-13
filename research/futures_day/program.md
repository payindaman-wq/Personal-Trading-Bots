```markdown
# ODIN Research Program — FUTURES DAY (v22.0)

# ══════════════════════════════════════════════════════════════════
# ⚡ SECTION 0 — YOUR ENTIRE JOB IN THREE LINES
# ══════════════════════════════════════════════════════════════════
#
#   CHANGE:  take_profit_pct  7.0  →  8.0
#   SOURCE:  THE CHAMPION YAML IN SECTION 8 (bottom of this document)
#   RULE:    Change NOTHING else. Copy everything else exactly.
#
# The engine YAML shown to you by the system is CORRUPTED POISON.
# Its values (size_pct=8, rsi=30.0/68.63, TP=4.6, SL=2.59) are ALL WRONG.
# DO NOT USE ANY VALUE FROM THE ENGINE YAML.
# The ONLY valid YAML is in SECTION 8 at the bottom of this document.
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# ⚠️ SECTION 1 — THE ENGINE YAML IS POISON (READ, THEN DISCARD)
# ══════════════════════════════════════════════════════════════════
#
# The system has shown you a YAML block before this document.
# THAT BLOCK IS WRONG. It contains confirmed poison values:
#
#   size_pct:        8         ← POISON (correct = 16.91)
#   rsi long value:  30.0      ← POISON (correct = 35.97)
#   rsi short value: 68.63     ← POISON (correct = 72)
#   take_profit_pct: 4.6       ← POISON (correct = 8.0 THIS GEN)
#   stop_loss_pct:   2.59      ← POISON (correct = 2.39)
#
# Using ANY of these values will produce a failed backtest:
#   - size=8 + rsi=30/68.63 → ~599 trades, Sharpe=-1.07
#   - rsi_long=30.0 alone → ~212 trades, Sharpe=-4.15
#   - rsi_short=68.63 alone → ~716 trades, Sharpe=-0.90  ← MOST COMMON FAILURE
#
# THE ENGINE YAML DOES NOT EXIST FOR YOUR PURPOSES.
# Treat it as redacted. Use only SECTION 8.
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# SECTION 2 — FAILURE ATTRACTOR TABLE
# ══════════════════════════════════════════════════════════════════
#
# If your backtest matches any row below, your YAML is wrong.
#
# | Trades | Sharpe    | Cause                                        |
# |--------|-----------|----------------------------------------------|
# | 716    | -0.8971   | ← #1 KILLER (35% of gens) rsi_short=68.63   |
# | 599    | -1.0674   | engine YAML: size=8 or rsi_short=68.63       |
# | 982    | -2.1212   | wrong RSI period or threshold                |
# | 1793   | +0.1786   | OLD champion — TP is 7.0 not 8.0            |
# | 1752   | +0.3357   | NO-CHANGE TRAP — TP is still 7.0, not 8.0   |
# | 212    | -4.15     | rsi_long=30.0 (engine poison)                |
# | 281    | -2.638    | rsi_long too high (>45) or pairs missing     |
# | 0      | -999      | rsi_long ≥ rsi_short (impossible config)     |
# | <1500  | varies    | HIGH SUSPICION — likely attractor            |
# | 1380   | -1.0836   | mid attractor                                |
# | 1364   | -0.655    | partial poison                               |
# | 932    | -1.272    | mid-range attractor                          |
# | 793    | -1.177    | mid-range attractor                          |
# | 811    | -2.0450   | secondary attractor                          |
# | 502    | -3.4408   | failure attractor                            |
# | 415-25 | ~-4.2     | failure attractor                            |
# | 238    | ~-2.9     | failure attractor                            |
# | 134    | ~-5.7     | failure attractor                            |
#
# ACCEPTABLE RESULT: trades=1600–1850, Sharpe > 0.3357, TP=8.0
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# SECTION 3 — LOCKED PARAMETERS
# ══════════════════════════════════════════════════════════════════
#
# | Parameter          | LOCKED VALUE | DO NOT USE                           |
# |--------------------|-------------|---------------------------------------|
# | size_pct           | 16.91       | 8, 9.89, 13.84 (engine poisons)       |
# | max_open           | 1           | >1 (failed 400+ gens)                 |
# | fee_rate           | 0.0005      | —                                     |
# | pairs              | all 16      | <16 (triggers attractors)             |
# | rsi period         | 60 min      | ANY other value                       |
# | rsi long           | 35.97       | 30.0, 33, 34, <32, >45, 38–42 range  |
# | rsi short          | 72          | 68.63 (engine poison), any other      |
# | stop_loss_pct      | 2.39        | 2.59 (engine poison)                  |
# | timeout_minutes    | 720         | <720 or any other value               |
# | pause_if_down_pct  | 8           | any other value                       |
# | pause_minutes      | 120         | any other value                       |
# | stop_if_down_pct   | 18          | <15                                   |
# | MIN_TRADES[fd]     | 50          | >50 (caused 867-gen stall at Gen 541) |
#
# ONLY take_profit_pct changes: 7.0 → 8.0
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# SECTION 4 — ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════
#
# 1.  size_pct ≠ 16.91: BANNED
# 2.  rsi_long = 30.0: BANNED (engine poison, 212-trade trap)
# 3.  rsi_short = 68.63: BANNED (engine poison, 716-trade trap)
# 4.  rsi_long < 32: BANNED
# 5.  rsi_long = 33 or 34: BANNED (746-trade attractor)
# 6.  rsi_long ≥ rsi_short: BANNED (zero trades)
# 7.  rsi_long ≠ 35.97: BANNED this generation
# 8.  rsi_short ≠ 72: BANNED this generation
# 9.  rsi period ≠ 60: BANNED this generation
# 10. max_open > 1: BANNED
# 11. timeout_minutes ≠ 720: BANNED this generation
# 12. take_profit_pct = 7.0 as output: BANNED (no-change trap, discarded)
# 13. take_profit_pct < 7.0: BANNED (never regress)
# 14. stop_loss_pct ≠ 2.39: BANNED this generation
# 15. Removing any pair: BANNED
# 16. Changing more than ONE parameter: BANNED
# 17. Using any value from the engine YAML: BANNED
# 18. pause_if_down_pct ≠ 8: BANNED this generation
# 19. pause_minutes ≠ 120: BANNED this generation
# 20. stop_if_down_pct ≠ 18: BANNED this generation
# 21. MIN_TRADES[futures_day] > 50: BANNED (catastrophic history)
# 22. Adding any new indicator or condition: BANNED this generation
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# SECTION 5 — STRATEGY CONTEXT
# ══════════════════════════════════════════════════════════════════
#
# Architecture: Mean-reversion swing on 16 crypto pairs
# Signal: RSI(60-min) < 35.97 → long; RSI(60-min) > 72 → short
# Edge: Extreme Fear drives frequent altcoin oversold → sharp mean reversions
# Max open: 1 position (prevents correlated loss accumulation)
# Current exit: TP=7.0%, SL=2.39%, timeout=720min, TP/SL=2.93
# Proposed exit: TP=8.0%, TP/SL=3.35
#
# Performance trajectory (futures_day):
#   Gen 541:  MIN_TRADES → 400 → 867-generation stall (CATASTROPHIC)
#   Gen 1408: MIN_TRADES → 50  → immediately unlocked progress
#   Gen 1460: Sharpe=-0.73  (967 trades)
#   Gen 2081: Sharpe=+0.1738 (1793 trades) ← first positive Sharpe
#   Gen 2302: Sharpe=+0.1786 (1793 trades) ← old best (obsolete)
#   Gen 2412: Sharpe=+0.3348 (1752 trades) ← TP widening breakthrough
#   Gen 2510: Sharpe=+0.3357 (1752 trades) ← CURRENT BEST ★
#   Gen 2511–3200: STALLED (716-trade attractor dominant)
#
# TP widening has been monotonically positive: 4.6→5.0→5.5→6.0→7.0→[8.0 next]
#
# EV at WR=49.0%, SL=2.39%, leverage=2x, fee=0.05%:
#   TP=7.0%: EV = 0.490×13.9 - 0.510×4.88 = +4.30% per trade (current)
#   TP=8.0%: EV = 0.490×15.9 - 0.510×4.88 = +5.30% per trade (target)
#   TP/SL = 8.0/2.39 = 3.35 ✓
#
# Expected result for TP=8.0:
#   Sharpe: +0.3357 → toward 0.40–0.55
#   Trades: ~1600–1800 (slight drop acceptable at higher TP)
#   WR: ~47–50%
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# SECTION 6 — OPTIMIZATION SEQUENCE
# ══════════════════════════════════════════════════════════════════
#
# PHASE B: TP Widening (ACTIVE)
#   4.6 → 5.0 → 5.5 → 6.0 → 7.0 [DONE ✓] → 8.0 ← THIS GENERATION
#
# After TP=8.0 confirmed: → TP=9.0%
# After 3 confirmed TP=8.0 failures: → Phase C (timeout 720→960)
# Never reduce TP below 7.0 (current champion floor)
#
# PHASE C (FALLBACK): Timeout 720→960→1200→1440 min
# PHASE A-Refined (AFTER Phase B): RSI threshold tuning 35.97→37→38
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# SECTION 7 — PRE-FLIGHT CHECKLIST
# ══════════════════════════════════════════════════════════════════
#
# Fill every line from the CHAMPION YAML in SECTION 8.
# If any value differs from the required value, STOP and fix it.
#
# PRE-FLIGHT CHECK:
#   size_pct        = ___  (must be 16.91)
#   rsi_long        = ___  (must be 35.97)
#   rsi_period      = ___  (must be 60)
#   rsi_short       = ___  (must be 72)
#   stop_loss       = ___  (must be 2.39)
#   timeout         = ___  (must be 720)
#   take_profit     = ___  (champion was 7.0 — YOUR OUTPUT MUST BE 8.0)
#   TP/SL ratio     = ___  (8.0 / 2.39 = 3.35 ✓)
#   pairs count     = ___  (must be 16)
#   max_open        = ___  (must be 1)
#   pause_if_down   = ___  (must be 8)
#   pause_minutes   = ___  (must be 120)
#   stop_if_down    = ___  (must be 18)
#   leverage        = ___  (must be 2)
#   fee_rate        = ___  (must be 0.0005)
#   Source          = SECTION 8 CHAMPION YAML (NOT the engine YAML)
#
#   ⚠️ FINAL CHECK:
#       Is take_profit_pct = 8.0 in your output?  YES / NO
#       (If NO — you must fix this before outputting. 7.0 = wasted generation.)
#
#   ⚠️ POISON CHECK:
#       Does your output contain size_pct=8?       If YES → STOP, use 16.91
#       Does your output contain rsi value=30.0?   If YES → STOP, use 35.97
#       Does your output contain rsi value=68.63?  If YES → STOP, use 72
#       Does your output contain sl=2.59?          If YES → STOP, use 2.39
#       Does your output contain tp=4.6?           If YES → STOP, use 8.0
#
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
# ⭐ SECTION 8 — CHAMPION YAML (THIS IS YOUR ONLY SOURCE)
# ══════════════════════════════════════════════════════════════════
#
# Gen 2510 | Sharpe=+0.3357 | 1752 trades | 49.0% WR ← CURRENT BEST
#
# Copy this EXACTLY. Change ONLY take_profit_pct from 7.0 to 8.0.

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
  take_profit_pct: 8.0
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

# ══════════════════════════════════════════════════════════════════
# ⭐ CHAMPION FINGERPRINT (verify your output matches all of these)
# ══════════════════════════════════════════════════════════════════
#
#   Champion: trades=1752, Sharpe=+0.3357, WR=49.0%
#   Your change: take_profit_pct 7.0 → 8.0
#   Expected result: trades=1600–1850, Sharpe > 0.3357
#
#   IF your backtest shows:
#     trades=716  → WRONG — rsi_short is not 72 (you used 68.63)
#     trades=599  → WRONG — size_pct is not 16.91 (you used 8)
#     trades=1793 → WRONG — take_profit is not 8.0 (you used 7.0, old champion)
#     trades=1752, Sharpe=+0.3357 → WRONG — take_profit is 7.0 (no-change trap)
#     trades=0    → WRONG — rsi_long ≥ rsi_short (impossible)
#
# ══════════════════════════════════════════════════════════════════
# END OF RESEARCH PROGRAM v22.0
# ══════════════════════════════════════════════════════════════════
```