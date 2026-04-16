```markdown
# ODIN Research Program — FUTURES DAY (v31.0)
#
# ══════════════════════════════════════════════════════════════════════
# SINGLE TASK THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# Copy the YAML below EXACTLY.
# Change ONLY: take_profit_pct from 11.0 to 12.0
# Change NOTHING else.
#
# Required output line 1: CHANGE: take_profit_pct 11.0 → 12.0
# Required output line 2: USING: size_pct=16.91, rsi_long=35.97, rsi_short=72, stop_loss=2.39, tp=12.0
#
# ══════════════════════════════════════════════════════════════════════
# THE ONLY VALID YAML — USE THIS, NOTHING ELSE
# Gen 4080 | Sharpe=+0.6880 | 1757 trades | WR=50.5%
# ══════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════
# VERIFICATION — answer before submitting
# ══════════════════════════════════════════════════════════════════════
#
#   size_pct     = 16.91   ✓
#   rsi_long     = 35.97   ✓
#   rsi_short    = 72      ✓
#   stop_loss    = 2.39    ✓
#   take_profit  = 12.0    ✓  (THIS is the one change from 11.0)
#
# ══════════════════════════════════════════════════════════════════════
# CONTEXT WARNING
# ══════════════════════════════════════════════════════════════════════
#
# Your context contains a block labeled "Current Best Strategy".
# That block is CORRUPTED. Its values are wrong. Do not use them.
# The correct values are ONLY in the YAML above.
#
# The corrupted block contains these wrong values — ignore them:
#   size_pct: 8          ← wrong
#   rsi long:  29.33     ← wrong
#   rsi short: 68.63     ← wrong
#   take_profit_pct: 4.6 ← wrong
#   stop_loss_pct: 2.59  ← wrong
#
# Use the YAML above. That is all.
#
# ══════════════════════════════════════════════════════════════════════
# KNOWN FAILURE SIGNATURES (do not reproduce these)
# ══════════════════════════════════════════════════════════════════════
#
#  273 trades / Sharpe=-2.7990  → rsi_long wrong (was 29.56)
#  491 trades / Sharpe=-4.8702  → multiple wrong values
#  506 trades / Sharpe=-3.3113  → bad RSI combination
#    0 trades / Sharpe=-999     → rsi_long ≥ rsi_short (impossible)
# 1770 trades / Sharpe=+0.3494  → stale TP value, not 12.0
# 1757 trades / Sharpe=+0.6880  → TP still 11.0 (no change made)
#
# Target: trades=1500–1900, Sharpe > 0.6880
#
# ══════════════════════════════════════════════════════════════════════
# OPTIMIZATION CONTEXT
# ══════════════════════════════════════════════════════════════════════
#
# Strategy: Mean-reversion swing on 16 crypto pairs, RSI(60-min)
# Signal:   RSI < 35.97 → long;  RSI > 72 → short
# Leverage: 2x futures day
#
# TP widening trajectory (each step improved Sharpe):
#   4.6 → 5.0 → 5.5 → 6.0 → 7.0 → 8.0 → 9.0 → 10.0 → 11.0 → [12.0 NOW]
#
# Confirmed results:
#   Gen 3233: Sharpe=+0.4066 (1756 trades, TP=9.0)
#   Gen 3995: Sharpe=+0.5721 (1750 trades, TP=10.0)
#   Gen 4080: Sharpe=+0.6880 (1757 trades, TP=11.0) ← CURRENT BEST
#   Target:   Sharpe ~0.70–0.80 (TP=12.0)
#
# EV at WR=50.5%, SL=2.39%, leverage=2x:
#   TP=11.0: EV = 0.505×21.9 − 0.495×4.88 = +8.64% per trade
#   TP=12.0: EV = 0.505×23.9 − 0.495×4.88 = +9.65% per trade
#
# After TP=12.0 confirmed: → test TP=13.0
# After 3 genuine failures at TP=12.0: → test timeout_minutes 720→960
#
# MIN_TRADES[futures_day] = 50 — PERMANENTLY FROZEN.
#   Raising to 400 at Gen 541 caused 867-generation stall (Gen 541–1408).
#   Reset to 50 at Gen 1408 → immediate progress. Never raise again.
#
# ══════════════════════════════════════════════════════════════════════
# RECENT HISTORY
# ══════════════════════════════════════════════════════════════════════
#
# Gen 4080: sharpe=+0.6880, 1757 trades [BEST ★] — TP=11.0
# Gen 4781: sharpe=-4.8702,  491 trades [FAILED]  — multiple poison values
# Gen 4782: sharpe=+0.3494, 1770 trades [DISCARDED]— stale TP
# Gen 4783: sharpe=+0.3494, 1770 trades [DISCARDED]— stale TP
# Gen 4784: sharpe=-0.5356, 1783 trades [DISCARDED]— wrong parameter
# Gen 4785: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4786: sharpe=+0.3488, 1770 trades [DISCARDED]— stale TP
# Gen 4787: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4788: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4789: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4790: sharpe=-2.1338,  770 trades [FAILED]  — wrong values
# Gen 4791: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4792: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4793: sharpe=-4.8702,  491 trades [FAILED]  — multiple poison values
# Gen 4794: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4795: sharpe=-999.000,   0 trades [FAILED]  — rsi_long ≥ rsi_short
# Gen 4796: sharpe=+0.3494, 1770 trades [DISCARDED]— stale TP
# Gen 4797: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4798: sharpe=-4.8702,  491 trades [FAILED]  — multiple poison values
# Gen 4799: sharpe=-2.7990,  273 trades [FAILED]  — rsi_long=29.56 (poison)
# Gen 4800: sharpe=-3.3113,  506 trades [FAILED]  — bad RSI combination
#
# Zero successful TP=12.0 backtests yet. That is the only goal.
#
# ══════════════════════════════════════════════════════════════════════
# FINAL INSTRUCTION
# ══════════════════════════════════════════════════════════════════════
#
# 1. Use the YAML in this document (size_pct=16.91, rsi=35.97/72, SL=2.39)
# 2. Set take_profit_pct: 12.0
# 3. Change nothing else
# 4. Output the two required lines, then the complete YAML
#
# One change. One YAML. TP=12.0. Done.
```