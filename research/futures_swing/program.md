```markdown
# ODIN Research Program — FUTURES SWING
# Champion: Sharpe=2.3513 | Trades=1265 | Win=40.1%

# ══════════════════════════════════════════════════════════════════
# STEP 1 — COPY THIS YAML EXACTLY, THEN CHANGE EXACTLY ONE VALUE
# ══════════════════════════════════════════════════════════════════

name: crossover
style: swing_momentum
league: futures_swing
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
  size_pct: 25
  max_open: 3
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: up
    - indicator: rsi
      period_hours: 24
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24
      operator: gt
      value: 60
exit:
  take_profit_pct: 4.65
  stop_loss_pct: 1.92
  timeout_hours: 166
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18

# ══════════════════════════════════════════════════════════════════
# STEP 2 — HARD REJECT (check ALL before submitting)
# ══════════════════════════════════════════════════════════════════
# REJECT if ANY of these are true:
#   stop_loss_pct < 1.70
#   rsi long (lt) value > 45 or < 30
#   rsi_period_hours < 18 or > 30
#   timeout_hours > 210
#   trades outside 400–3000
#   fee_rate changed
#   pairs added or removed
#   more than ONE value changed
#   identical to champion above

# ══════════════════════════════════════════════════════════════════
# STEP 3 — PICK ONE VALUE FROM THIS LIST (priority order)
# ══════════════════════════════════════════════════════════════════

# TIER 1 — LEAST EXPLORED (try these first)
#
# rsi_period_hours (currently 24):
#   → TRY: 22, 23, 25, 26, 21, 27, 20, 28, 19, 18
#
# rsi short gt (currently 60):
#   → TRY: 59, 61, 58, 62, 57, 63
#
# trend_period_hours (currently 48):
#   → TRY: 42, 54, 60, 36, 72

# TIER 2 — MODERATELY EXPLORED
#
# take_profit_pct (currently 4.65):
#   → TRY: 4.80, 4.85, 4.90, 4.95, 5.00, 5.10, 5.20, 5.30, 5.40, 5.50
#   → TRY: 4.55, 4.50, 4.45, 4.40
#   → FINE: 4.62, 4.63, 4.64, 4.66, 4.67, 4.68, 4.69, 4.71, 4.72, 4.73
#
# stop_loss_pct (currently 1.92):
#   → TRY: 2.10, 2.15, 2.20, 2.25, 2.30, 2.35, 2.40
#   → TRY: 1.85, 1.80, 1.75, 1.70  ← 1.70 is hard floor
#   → FINE: 1.88, 1.89, 1.90, 1.91, 1.93, 1.94, 1.96, 1.97, 1.98, 1.99
#
# timeout_hours (currently 166):
#   → TRY: 158, 162, 163, 164, 165, 167, 168, 169, 170, 172, 174, 176, 178, 180

# TIER 3 — LAST RESORT
#
# rsi long lt (currently 37.77):
#   → TRY: 38.0, 38.2, 38.4, 38.6, 38.8, 39.0, 37.5, 37.3, 37.0, 36.5
#   (most adjacent values already tested — prefer larger steps)
#
# pause_if_down_pct (currently 8):  → TRY: 7, 9, 6, 10
# stop_if_down_pct (currently 18):  → TRY: 16, 17, 20, 22

# ══════════════════════════════════════════════════════════════════
# STEP 4 — VERIFY BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════
# □ Copied YAML exactly from champion above
# □ Changed EXACTLY ONE parameter
# □ Value is NOT the current champion value
# □ All HARD REJECT rules pass
# □ This exact config not submitted before

# ══════════════════════════════════════════════════════════════════
# DO NOT CHANGE (fixed):
# size_pct=25 | max_open=3 | fee_rate=0.0005 | leverage=2
#
# KNOWN CATASTROPHIC — do not reproduce:
# stop_loss_pct < 1.70 → catastrophic loss
# max_open=2 → kills trade count
# trend_period=24 → kills trade count
# ~190 trades → poison attractor (sharpe ~ -1.6)
# ~500 trades → weak attractor (sharpe ~ 0.84–0.94), already tested many times
#
# KNOWN-BAD SIGNATURES (do not reproduce):
# (503t, 0.81), (521t, 0.94), (506t, 0.94), (447t, 1.10), (345t, 0.89)
# (188t, −1.65), (190t, −1.05), (190t, −1.63), (185t, −0.79)
# (502t, +0.87), (501t, +1.00), (505t, +0.84), (457t, +1.04)
# ══════════════════════════════════════════════════════════════════

# INFRASTRUCTURE NOTES (human operator — do not send to LLM):
# [BUG-4] CRITICAL: Pre-backtest SHA-256 dedup gate still missing.
#         ~60% of recent gens are dedup rejects = wasted compute.
#         Implement immediately.
# [Z4]  Confirm APT/SUI/ARB/OP/POL have ≥17,520 candles before live deploy.
# [Z8]  Run systematic 2D grid: take_profit (4.40–5.50, step 0.10)
#       × stop_loss (1.70–2.50, step 0.08) = ~150 backtests.
#       LLM random search is exhausted. Grid is required.
# [Z9]  Live deployment blocked until Z4+Z8 complete.
#       Macro = CAUTION. Live sizing = 50% only.
# [Z10] Gen gap 5031→5944 (913 gens missing). Champion 2.3513 may reflect
#       unlogged improvement. TSV audit required.
# [Z11] Dedup rate ~60% — BUG-4 is now top infrastructure priority.
# [Z12] Non-monotonic gen numbers (gen 5257 after gen 9000) = log corruption.
#       Audit log integrity before trusting improvement counts.
```

---