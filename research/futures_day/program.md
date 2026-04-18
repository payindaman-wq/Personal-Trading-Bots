```markdown
# ODIN Research Program — FUTURES DAY (v34.0)
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY TASK THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# Copy the CHAMPION YAML below EXACTLY.
# Make ONE change: set take_profit_pct to 5.0
# Output the two required lines, then the complete YAML.
#
# Required output line 1: CHANGE: take_profit_pct 4.6 → 5.0
# Required output line 2: USING: size_pct=8, rsi_long=29.33, rsi_short=68.63, stop_loss=2.59, tp=5.0
#
# ══════════════════════════════════════════════════════════════════════
# CHAMPION YAML — Gen 3233 | Sharpe=+0.4066 | 1756 trades | WR=50.1%
# ══════════════════════════════════════════════════════════════════════
#
# THIS IS THE ONLY REAL CHAMPION. Values reported above Gen 3233
# (e.g., Sharpe=0.5721, Sharpe=0.6880) were NEVER confirmed as
# new_best events and must be treated as fabricated. Do not reference
# them. Do not build on them. The YAML below is canonical.

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
  size_pct: 8
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 29.33
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 68.63
exit:
  take_profit_pct: 5.0
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

# ══════════════════════════════════════════════════════════════════════
# VERIFICATION CHECKLIST — confirm every value before submitting
# ══════════════════════════════════════════════════════════════════════
#
#   size_pct     = 8       ✓   (NOT 16.91 — that value is invalid)
#   rsi_long     = 29.33   ✓   (NOT 35.97 — that value is invalid)
#   rsi_short    = 68.63   ✓   (NOT 72 — that value is invalid)
#   stop_loss    = 2.59    ✓   (NOT 2.39 — that value is invalid)
#   take_profit  = 5.0     ✓   (the one change from 4.6)
#   rsi_long < rsi_short?  ✓   (29.33 < 68.63)
#   pairs list   = 16 pairs ✓  (copy exactly, add no new pairs)
#
# If your output uses ANY of these INVALID values:
#   size_pct=16.91, rsi_long=35.97, rsi_short=72, stop_loss=2.39
# then you have been poisoned by stale data. STOP. Use the YAML above.
#
# ══════════════════════════════════════════════════════════════════════
# CONFIRMED IMPROVEMENT SERIES (verified new_best events only)
# ══════════════════════════════════════════════════════════════════════
#
#   Gen 2412: Sharpe=+0.3348, 1752 trades
#   Gen 2510: Sharpe=+0.3357, 1752 trades
#   Gen 3233: Sharpe=+0.4066, 1756 trades, WR=50.1% ← CURRENT CHAMPION
#
# NOTE: Results claiming Sharpe=0.5721 (Gen 3995) or Sharpe=0.6880
# (Gen 4080) were NEVER recorded as new_best events in the improvement
# log. They do not exist as confirmed improvements. Do not reference
# them as a baseline. The champion is Gen 3233 with Sharpe=0.4066.
#
# ══════════════════════════════════════════════════════════════════════
# RESEARCH ROADMAP (execute in order, one step per generation)
# ══════════════════════════════════════════════════════════════════════
#
# Step 1 (NOW):    TP 4.6 → 5.0   [target: Sharpe > 0.4066]
# Step 2:          TP 5.0 → 5.5   [only after Step 1 confirmed]
# Step 3:          TP 5.5 → 6.0   [only after Step 2 confirmed]
# Step 4:          TP 6.0 → 7.0   [only after Step 3 confirmed]
#
# If 3 consecutive TP increases fail to improve Sharpe:
#   → Freeze TP, test rsi_long 29.33 → 32.0 (more trades)
#   → Then test rsi_short 68.63 → 66.0 (more trades)
#   → Then test stop_loss 2.59 → 2.20 (tighter stop)
#   → Then test timeout_minutes 720 → 960
#
# ══════════════════════════════════════════════════════════════════════
# KNOWN POISON ATTRACTORS — if your output matches these, DISCARD IT
# ══════════════════════════════════════════════════════════════════════
#
# Attractor A: Sharpe≈-2.799, ~273 trades
#   Signature: very tight RSI thresholds, size_pct far from 8
#
# Attractor B: Sharpe≈-4.870, ~491 trades
#   Signature: rsi_long/rsi_short values inconsistent with champion
#
# Attractor C: Sharpe=-999, 0 trades
#   Signature: rsi_long set below 20 OR rsi_short set above 80
#   → RSI thresholds must remain: 25 ≤ rsi_long ≤ 40, 60 ≤ rsi_short ≤ 75
#
# Attractor D: INVALID PARAMETER SET (phantom champion)
#   size_pct=16.91, rsi_long=35.97, rsi_short=72, stop_loss=2.39
#   → These values have never produced a confirmed new_best.
#   → Any YAML using these values must be rejected immediately.
#
# ══════════════════════════════════════════════════════════════════════
# SYSTEM CONSTANTS (frozen — never change)
# ══════════════════════════════════════════════════════════════════════
#
# MIN_TRADES[futures_day] = 50 — PERMANENTLY FROZEN.
#   Raising this to 400 at Gen 541 caused an 867-generation stall.
#   Reset to 50 at Gen 1408 → progress immediately resumed.
#   Never raise this value again under any circumstances.
#
# ══════════════════════════════════════════════════════════════════════
# WHAT ONE CHANGE MEANS
# ══════════════════════════════════════════════════════════════════════
#
# You are allowed to change EXACTLY ONE parameter from the champion YAML.
# That parameter is take_profit_pct: change it from 4.6 to 5.0.
# Every other field — pairs, size_pct, rsi values, stop_loss,
# timeout_minutes, risk parameters — must be copied without alteration.
#
# Do not add new indicators. Do not add new pairs. Do not change leverage.
# Do not change fee_rate. Do not change max_open.
# The ONLY difference between your output and the champion YAML
# must be: take_profit_pct changes from 4.6 to 5.0.
#
# ══════════════════════════════════════════════════════════════════════
# RECENT GENERATION HISTORY (last 20 — all failures)
# ══════════════════════════════════════════════════════════════════════
#
# Gen 5381–5400: All failed (poison_reject, discarded, low_trades)
#   Root cause: LLM was using phantom champion parameters
#   (size_pct=16.91, rsi_long=35.97) instead of real champion.
#   Fix: Use the YAML printed above. It is the ground truth.
#
# The goal: a successful TP=5.0 backtest with Sharpe > 0.4066.
```