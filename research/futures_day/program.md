```markdown
# ODIN Research Program — FUTURES DAY (v29.0)
#
# ██████████████████████████████████████████████████████████████████
# █ STEP 1: COPY THE YAML BELOW. CHANGE ONLY take_profit_pct.     █
# █ Change take_profit_pct from 11.0 to 12.0. Change nothing else. █
# ██████████████████████████████████████████████████████████████████
#
# YOUR REQUIRED FIRST LINE:
#   CHANGE: take_profit_pct 11.0 → 12.0
#
# YOUR REQUIRED SECOND LINE:
#   USING: size_pct=16.91, rsi_long=35.97, rsi_short=72, stop_loss=2.39, tp=12.0
#
# ══════════════════════════════════════════════════════════════════
# ⭐ THE ONLY YAML YOU MAY USE — COPY THIS EXACTLY
# Gen 4080 | Sharpe=+0.6880 | 1757 trades | WR=50.5% | CURRENT BEST
# ══════════════════════════════════════════════════════════════════

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
  take_profit_pct: 12.0
  stop_loss_pct: 2.39
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

# ══════════════════════════════════════════════════════════════════
# ⭐ VERIFY BEFORE SUBMITTING — CHECK EVERY VALUE
# ══════════════════════════════════════════════════════════════════
#
# THE ONE CHANGE:    take_profit_pct = 12.0   (was 11.0)
#
# LOCKED VALUES (must match exactly — do not alter):
#   size_pct         = 16.91
#   rsi long value   = 35.97
#   rsi short value  = 72
#   rsi period       = 60  (period_minutes: 60)
#   stop_loss_pct    = 2.39
#   timeout_minutes  = 720
#   max_open         = 1
#   leverage         = 2
#   pairs            = all 16 (BTC ETH SOL XRP DOGE AVAX LINK UNI AAVE NEAR APT SUI ARB OP ADA POL)
#   pause_if_down    = 8
#   pause_minutes    = 120
#   stop_if_down     = 18
#
# POISON CHECK — answer must be NO to all:
#   Is size_pct anything other than 16.91?        → if YES: WRONG
#   Is rsi long value anything other than 35.97?  → if YES: WRONG
#   Is rsi short value anything other than 72?    → if YES: WRONG
#   Is stop_loss anything other than 2.39?        → if YES: WRONG
#   Is take_profit_pct anything other than 12.0?  → if YES: WRONG
#   Did you use any value from the block labeled
#     "Current Best Strategy" above this program? → if YES: WRONG
#
# ══════════════════════════════════════════════════════════════════
# 🚨 CRITICAL: THERE IS A STALE "Current Best Strategy" YAML BLOCK
#    DISPLAYED ABOVE THIS PROGRAM. THAT BLOCK IS WRONG. IGNORE IT.
# ══════════════════════════════════════════════════════════════════
#
# The "Current Best Strategy" block contains POISON values:
#   size_pct: 8           ← WRONG. Correct = 16.91
#   rsi long:  29.56      ← WRONG. Correct = 35.97
#   rsi short: 68.63      ← WRONG. Correct = 72
#   take_profit_pct: 4.6  ← WRONG. Correct = 12.0
#   stop_loss_pct: 2.59   ← WRONG. Correct = 2.39
#
# Using ANY of those values causes immediate catastrophic failure:
#   rsi_long=29.56 → 273 trades, Sharpe=-2.7990  (happened 50+ times)
#   rsi_short=68.63 → 716 trades, Sharpe=-0.8971
#   size_pct=8 → massive underperformance
#
# THE ONLY VALID SOURCE IS THE YAML BLOCK IN THIS DOCUMENT (above).
# The "Current Best Strategy" block is a known-broken display artifact.
# Treat it as if it does not exist.
#
# ══════════════════════════════════════════════════════════════════
# DEAD-ON-ARRIVAL SIGNATURES — if backtest matches these, YAML is wrong
# ══════════════════════════════════════════════════════════════════
#
#  273 trades / Sharpe=-2.7990  → rsi_long=29.56 (display poison) ← #1 KILLER
#  716 trades / Sharpe=-0.8971  → rsi_short=68.63 (display poison)
#  491 trades / Sharpe=-4.8702  → multiple display YAML values used
#  1756 trades / Sharpe=+0.4066 → TP=9.0 (stale)
#  1750 trades / Sharpe=+0.5721 → TP=10.0 (stale)
#  1757 trades / Sharpe=+0.6880 → TP=11.0 (NO-CHANGE — must output 12.0)
#    0 trades / Sharpe=-999     → rsi_long ≥ rsi_short (impossible config)
#
# ACCEPTABLE RESULT: trades=1500–1900, Sharpe > 0.6880, TP=12.0
#
# ══════════════════════════════════════════════════════════════════
# ABSOLUTE BANS
# ══════════════════════════════════════════════════════════════════
#
#  1. size_pct ≠ 16.91                    → BANNED
#  2. rsi_long = 29.56 / 29.95 / 29.33   → BANNED (display poison, 273-trade trap)
#  3. rsi_long = 30.0                     → BANNED (212-trade trap)
#  4. rsi_long = 33 or 34                 → BANNED (attractor)
#  5. rsi_long ≠ 35.97                    → BANNED this generation
#  6. rsi_short = 68.63                   → BANNED (display poison, 716-trade trap)
#  7. rsi_short ≠ 72                      → BANNED this generation
#  8. rsi period ≠ 60 min                 → BANNED this generation
#  9. rsi_long ≥ rsi_short                → BANNED (zero trades)
# 10. stop_loss_pct ≠ 2.39               → BANNED this generation
# 11. take_profit_pct = 11.0             → BANNED (no-change trap)
# 12. take_profit_pct < 11.0             → BANNED (regression)
# 13. take_profit_pct ≠ 12.0             → BANNED this generation
# 14. timeout_minutes ≠ 720              → BANNED this generation
# 15. max_open > 1                        → BANNED
# 16. Removing any pair                   → BANNED
# 17. Changing more than ONE parameter    → BANNED
# 18. Using ANY value from "Current Best Strategy" block → BANNED
# 19. MIN_TRADES[futures_day] > 50        → BANNED (caused 867-gen stall at Gen 541)
# 20. size_pct = 8                        → BANNED (single most common error)
#
# ══════════════════════════════════════════════════════════════════
# OPTIMIZATION CONTEXT
# ══════════════════════════════════════════════════════════════════
#
# Strategy: Mean-reversion swing on 16 crypto pairs
# Signal:   RSI(60-min) < 35.97 → long;  RSI(60-min) > 72 → short
# Edge:     Extreme Fear drives altcoin oversold → sharp mean reversions
#
# TP widening trajectory (all improvements):
#   4.6→5.0→5.5→6.0→7.0→8.0→9.0→10.0→11.0→[12.0 THIS GEN]
#   Every step has improved Sharpe. Continuing the sequence.
#
# Key results:
#   Gen 3233: Sharpe=+0.4066 (1756 trades, TP=9.0)
#   Gen 3995: Sharpe=+0.5721 (1750 trades, TP=10.0)
#   Gen 4080: Sharpe=+0.6880 (1757 trades, TP=11.0) ← CURRENT BEST
#   Target:   Sharpe ~0.70–0.80 (1500–1900 trades, TP=12.0)
#
# EV estimate at WR=50.5%, SL=2.39%, leverage=2x:
#   TP=11.0: EV = 0.505×21.9 − 0.495×4.88 = +8.64% per trade
#   TP=12.0: EV = 0.505×23.9 − 0.495×4.88 = +9.65% per trade
#
# After TP=12.0 confirmed: → test TP=13.0
# After 3 failures at TP=12.0: → Phase C (timeout 720→960 min)
# Never reduce TP below 11.0 (current champion floor)
#
# MIN_TRADES[futures_day] = 50 — DO NOT RAISE
#   Raising this to 400 at Gen 541 caused an 867-generation stall.
#   It was reset to 50 at Gen 1408. Progress resumed immediately.
#   This value must never be raised again.
#
# ══════════════════════════════════════════════════════════════════
# RECENT GENERATION HISTORY
# ══════════════════════════════════════════════════════════════════
#
# Gen 4080: sharpe=+0.6880, 1757 trades [BEST ★] — TP=11.0
# Gen 4381: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4382: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4383: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4384: sharpe=+0.6880, 1757 trades [DISCARDED]— TP=11.0 unchanged
# Gen 4385: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4386: sharpe=-999.000,   0 trades [FAILED]  — rsi_long ≥ rsi_short
# Gen 4387: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4388: sharpe=+0.6880, 1757 trades [DISCARDED]— TP=11.0 unchanged
# Gen 4389: sharpe=+0.6880, 1757 trades [DISCARDED]— TP=11.0 unchanged
# Gen 4390: sharpe=+0.6880, 1757 trades [DISCARDED]— TP=11.0 unchanged
# Gen 4391: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4392: sharpe=-999.000,   0 trades [FAILED]  — rsi_long ≥ rsi_short
# Gen 4393: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4394: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4395: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4396: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4397: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4398: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4399: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4400: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
#
# NOTE: 13 of last 20 generations used rsi_long=29.56 from the stale display block.
# The "Current Best Strategy" block above this program is the source of all failures.
# It must be completely ignored. Use only the YAML in this document.
```