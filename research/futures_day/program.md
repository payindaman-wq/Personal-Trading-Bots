```markdown
# ODIN Research Program — FUTURES DAY (v33.0)
#
# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY TASK THIS GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# Copy the CHAMPION YAML below EXACTLY.
# Make ONE change: set take_profit_pct to 12.0
# Output the two required lines, then the complete YAML.
#
# Required output line 1: CHANGE: take_profit_pct 11.0 → 12.0
# Required output line 2: USING: size_pct=16.91, rsi_long=35.97, rsi_short=72, stop_loss=2.39, tp=12.0
#
# ══════════════════════════════════════════════════════════════════════
# CHAMPION YAML — Gen 4080 | Sharpe=+0.6880 | 1757 trades | WR=50.5%
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
# VERIFICATION CHECKLIST — confirm before submitting
# ══════════════════════════════════════════════════════════════════════
#
#   size_pct     = 16.91   ✓
#   rsi_long     = 35.97   ✓
#   rsi_short    = 72      ✓
#   stop_loss    = 2.39    ✓
#   take_profit  = 12.0    ✓  (the one change from 11.0)
#   rsi_long < rsi_short?  ✓  (35.97 < 72)
#
# ══════════════════════════════════════════════════════════════════════
# CONFIRMED IMPROVEMENT SERIES (do not deviate from this path)
# ══════════════════════════════════════════════════════════════════════
#
#   TP= 9.0 → Sharpe=+0.4066 (Gen 3233, 1756 trades)
#   TP=10.0 → Sharpe=+0.5721 (Gen 3995, 1750 trades)
#   TP=11.0 → Sharpe=+0.6880 (Gen 4080, 1757 trades) ← current champion
#   TP=12.0 → target Sharpe ~0.70–0.80              ← YOUR TASK
#
# Each +1.0 TP step has reliably added ~+0.14 Sharpe.
# Trade count remains stable (~1750) because most exits are SL or timeout.
#
# ══════════════════════════════════════════════════════════════════════
# ROADMAP (context only — do NOT implement now)
# ══════════════════════════════════════════════════════════════════════
#
# After TP=12.0 confirmed: → test TP=13.0
# After TP=13.0 confirmed: → test TP=14.0
# After 3 TP failures:     → test timeout_minutes 720→960
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
# RECENT GENERATION HISTORY
# ══════════════════════════════════════════════════════════════════════
#
# Gen 4080: Sharpe=+0.6880, 1757 trades [BEST ★] — TP=11.0
# Gen 5181–5200: All failed or discarded — stale parameter values
#
# The only goal: a successful TP=12.0 backtest with Sharpe > 0.6880.
```

---