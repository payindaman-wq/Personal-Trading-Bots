```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6284 | Revised by MIMIR (Gen 6284 review)
# ══════════════════════════════════════════════════════════════════
# SHARPE=2.3513 | TRADES=1265 | WIN=40.1% | Source: elite_0.yaml
# ══════════════════════════════════════════════════════════════════

# ── STEP 1: COPY THIS YAML EXACTLY, THEN CHANGE EXACTLY ONE VALUE ─

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
# STEP 2 — PICK EXACTLY ONE CHANGE FROM THE TABLE BELOW
# ══════════════════════════════════════════════════════════════════
# RULES (violation = instant reject, do not submit):
#   stop_loss_pct MUST be ≥ 1.70
#   rsi long (lt) MUST be 30–45
#   rsi_period_hours MUST be 18–30
#   timeout_hours MUST be ≤ 210
#   Do NOT add/remove pairs. Do NOT change fee_rate.
#   Do NOT submit the champion unchanged.
#   Output must produce 400–3000 trades.
#
# ── PRIORITY 1 — try these first, in order shown ─────────────────
#
# PARAMETER         CURRENT   CANDIDATES (try left-to-right, skip if tried)
# take_profit_pct   4.65      4.70, 4.75, 4.80, 4.85, 4.90, 4.95,
#                             5.00, 5.10, 5.20, 5.30, 5.40, 5.50,
#                             4.60, 4.55, 4.50
#
# stop_loss_pct     1.92      1.95, 2.00, 2.05, 2.10, 2.15, 2.20,
#                             2.25, 2.30, 1.90, 1.85, 1.80, 1.75
#                             ← FLOOR IS 1.70; DO NOT GO BELOW 1.70
#
# timeout_hours     166       160, 168, 172, 164, 156, 176, 180,
#                             152, 184, 144, 192, 136, 200
#
# rsi long (lt)     37.77     38.0, 37.5, 38.5, 37.0, 39.0, 36.5,
#                             39.5, 36.0, 40.0, 40.5, 35.5, 35.0
#                             ← FLOOR IS 35.0; CEILING IS 45.0
#
# ── PRIORITY 2 — only if ALL Priority 1 values are exhausted ─────
#
# rsi_period_hours  24        22, 23, 25, 26, 20, 21, 18, 19, 27, 28
#                             (do NOT use 24 — that is the champion value)
#
# rsi short (gt)    60        59, 61, 58, 62, 57, 63
#
# ── PRIORITY 3 — last resort only ────────────────────────────────
#
# trend_period_hrs  48        36, 42, 54, 60, 72
# pause_if_down_pct 8         6, 7, 9, 10
# stop_if_down_pct  18        15, 16, 17, 20, 22
#
# DO NOT CHANGE: size_pct, max_open, pairs, fee_rate, leverage
#
# ══════════════════════════════════════════════════════════════════
# STEP 3 — VERIFY BEFORE SUBMITTING (check every box)
# ══════════════════════════════════════════════════════════════════
# □ Copied YAML exactly — only ONE value changed
# □ New value is NOT the current champion value
# □ stop_loss_pct ≥ 1.70
# □ rsi long (lt) is between 30 and 45
# □ timeout_hours ≤ 210
# □ Estimated trade count: 400–3000
# □ This exact config has NOT been submitted before
#
# KNOWN-BAD — do not reproduce any of these:
# (trades≈190, sharpe<0), (trades≈185, sharpe<0), (trades≈174, sharpe<0)
# (trades≈224, sharpe<0), (trades≈178, sharpe<0), (trades≈158, sharpe<0)
# (trades≈239, sharpe<0), (trades≈397, sharpe<0.6), (trades≈461, sharpe<0.6)
# stop_loss_pct < 1.70 → always bad, always reject
# rsi long (lt) > 45   → bad Sharpe, reject
# rsi long (lt) < 30   → bad Sharpe, reject
# timeout_hours > 210  → reject
#
# ══════════════════════════════════════════════════════════════════
# OPERATOR NOTES (do not send to LLM)
# ══════════════════════════════════════════════════════════════════
# [STATUS] Stalled since gen 3340. Dedup rate ~65% in last 20 gens.
#          Random single-param walk is structurally exhausted.
# [Z8]  ACTION REQUIRED: Run full 2D grid sweep of take_profit_pct
#       × stop_loss_pct (~150 backtests). This is now critical path.
#       Random LLM sampling cannot find improvement without this.
# [Z4]  Confirm APT/SUI/ARB/OP have ≥17,520 candles before live deploy.
# [Z9]  Live deployment blocked until Z4+Z8 complete.
#       Macro = CAUTION. Live sizing = 50% of normal only.
#       Do NOT change size_pct in YAML (keep 25 for comparability).
# [Z10] Gen gap 5031→5944 (913 gens missing). Investigate log writes.
# [BUG-2] elite_0.yaml may lag in-memory champion. Fix: write on every accept.
# [BUG-4] Clone detection is post-backtest. Fix: pre-backtest SHA-256 gate.
# [BUG-5] Poison attractor (~190t) still appearing sporadically.
#         MIN_TRADES=400 is correct; verify gate is applied pre-backtest.
# [NOTE] Last improvement: gen 3340 (2946 gens ago). Z8 grid sweep
#        must be actioned by human operator — prompt changes alone
#        cannot overcome combinatorial exhaustion at this stage.
# ══════════════════════════════════════════════════════════════════
```