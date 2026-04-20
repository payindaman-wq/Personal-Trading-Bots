```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-5949 | Revised by MIMIR (Gen 5949 review)

# ══════════════════════════════════════════════════════════════════
# STEP 1 — COPY THIS YAML EXACTLY, CHANGE EXACTLY ONE VALUE
# ══════════════════════════════════════════════════════════════════
# Sharpe=2.3513 | Trades=1265 | Win=40.1% | Source: elite_0.yaml

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
# STEP 2 — CHANGE EXACTLY ONE PARAMETER (read table carefully)
# ══════════════════════════════════════════════════════════════════
# HARD RULES — violation = automatic reject, do not submit:
#   stop_loss_pct < 1.70        → ~190 trades → REJECT
#   rsi long value > 45 or < 30 → bad Sharpe  → REJECT
#   rsi_period_hours < 18 or > 30              → REJECT
#   timeout_hours > 210                        → REJECT
#   Do NOT add/remove pairs. Do NOT change fee_rate.
#   Do NOT submit champion unchanged.
#   Output must produce 400–3000 trades.

# ── PRIORITY 1 (try these first — highest improvement history) ───
#
# PARAMETER          CURRENT   TRY NEXT (prefer earlier values)
# take_profit_pct    4.65      4.70, 4.80, 4.90, 5.00, 5.10, 5.20,
#                              5.30, 5.40, 5.50, 4.60, 4.55, 4.50,
#                              4.75, 4.85, 4.95
#
# stop_loss_pct      1.92      1.95, 2.00, 2.05, 2.10, 2.15, 2.20,
#                              2.25, 2.30, 1.90, 1.85, 1.80, 1.75,
#                              1.70  ← absolute floor, do not go lower
#
# timeout_hours      166       160, 168, 172, 164, 156, 176, 180,
#                              152, 184, 144, 192, 136, 200
#
# rsi long (lt)      37.77     38.0, 37.5, 38.5, 37.0, 39.0, 36.5,
#                              39.5, 36.0, 40.0, 40.5, 41.0, 35.5,
#                              35.0  ← floor

# ── PRIORITY 2 (only after Priority 1 values are exhausted) ─────
#
# rsi_period_hours   24        18, 19, 20, 21, 22, 23, 25, 26, 27, 28
#                              (do NOT use 24 = champion value)
#
# rsi short (gt)     60        59, 61, 58, 62, 57, 63, 65

# ── PRIORITY 3 (last resort only) ───────────────────────────────
#
# trend_period_hours 48        36, 42, 54, 60, 72
# size_pct           25        20, 22, 28, 30
# max_open           3         2, 4
# pause_if_down_pct  8         6, 7, 9, 10
# stop_if_down_pct   18        15, 16, 17, 20, 22

# ══════════════════════════════════════════════════════════════════
# STEP 3 — VERIFY BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════
# □ Copied YAML exactly, changed ONE value only
# □ New value is NOT in the KNOWN-BAD list below
# □ Estimated trade count: 400–3000
# □ This exact config has not been submitted before

# KNOWN-BAD SIGNATURES (do not reproduce):
# (190t, −1.05), (190t, −1.63), (185t, −0.79), (174t, −1.96),
# (224t, −1.73), (178t, −0.80), (182t, −1.86), (158t, −2.08),
# (239t, −2.41), (397t, −0.54), (461t, −0.46)
# stop_loss_pct values confirmed bad: any < 1.70

# ══════════════════════════════════════════════════════════════════
# INFRASTRUCTURE NOTES (human operator — do not send to LLM)
# ══════════════════════════════════════════════════════════════════
# [BUG-2] elite_0.yaml may lag in-memory champion. Fix: write on every accept.
# [BUG-4] Clone detection is post-backtest. Fix: pre-backtest SHA-256 gate.
# [BUG-5] Poison attractor (~190t) still appearing. Fix: pre-backtest trade gate.
# [Z4]  Confirm APT/SUI/ARB/OP have ≥17,520 candles before live deployment.
# [Z8]  CRITICAL: Run full 2D grid sweep of take_profit_pct × stop_loss_pct
#       (~150 backtests). 2,600+ gens with zero improvement — random LLM
#       sampling is exhausted. Systematic sweep is the required next action.
# [Z9]  Live deployment blocked until Z4+Z8 complete.
#       Macro = CAUTION. Live position sizing = 50% only.
#       Do NOT change size_pct in backtest YAML (keep 25 for comparability).
# [Z10] Gen gap 5031→5944 unexplained (913 gens missing from log). Investigate
#       whether results were written and whether champion tracking held.
# ══════════════════════════════════════════════════════════════════
```

---