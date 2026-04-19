```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-5257 | Revised by MIMIR (Gen 5257 review)
#
# ══════════════════════════════════════════════════════════════════
# STOP — READ THIS FIRST
# ══════════════════════════════════════════════════════════════════
#
# LOOP STATUS: RUNNING (Gen 5257 context — loop is active)
# CHAMPION:    sharpe=2.3513 | trades=1265 | win_rate=~40%
#              Source: elite_0.yaml (canonical). Do NOT use log estimates.
# BUG-2:       YAML persistence may be broken. In-memory champion may be
#              higher than 2.3513. Inspect elite_0.yaml before trusting
#              [new_best] / [discarded] labels.
# PAIR AUDIT:  APT, SUI, ARB, OP may lack full 2yr data → Sharpe may be
#              inflated. Do not deploy live until Z4 is complete.
# LIVE DATA:   Zero live sprint results. Backtest overfitting risk unknown.
#
# ══════════════════════════════════════════════════════════════════
# PROPOSE EXACTLY ONE YAML CHANGE PER GENERATION — TEMPLATE BELOW
# ══════════════════════════════════════════════════════════════════
#
# Copy this YAML, change EXACTLY ONE parameter, submit.
# Do NOT change two parameters. Do NOT reproduce this unchanged.

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
      period_hours: 22        # CONFIRMED champion value — do NOT change to 24
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 22        # CONFIRMED champion value — do NOT change to 24
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
# RULES — CHECK ALL BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════
#
# RULE 1: Change EXACTLY ONE parameter. One. Not two. Not zero.
# RULE 2: Result must produce 400–3000 trades. If your change is likely
#         to drop below 400 trades, pick a different parameter.
# RULE 3: Do NOT reproduce the champion YAML unchanged → [discarded].
# RULE 4: Do NOT propose a configuration you have proposed before → [dedup_reject].
# RULE 5: Do NOT propose any of these known-bad signatures (trades, sharpe):
#           (190t, -1.0517), (185t, -0.7900), (28t, -9.018),
#           (174t, -1.9619), (224t, -1.7297), (178t, -0.8033),
#           (182t, -1.8625), (158t, -2.0796), (239t, -2.4141),
#           (397t, -0.5405), (461t, -0.4605), (18t, -14.3473),
#           (190t, -1.0406).
#         If your change would recreate one of these, pick a different parameter.
# RULE 6: Prioritize the HIGH-VALUE parameters listed below.
#
# ══════════════════════════════════════════════════════════════════
# HIGH-VALUE PARAMETERS — CHANGE THESE FIRST
# ══════════════════════════════════════════════════════════════════
#
# These parameters have the strongest improvement history.
# Try them in grid order. Do not skip ranges.
#
# take_profit_pct:    try 4.50, 4.60, 4.70, 4.80, 4.90, 5.00,
#                         5.10, 5.20, 5.30, 5.40, 5.50
#                     (current: 4.65 — try adjacent values first)
#
# stop_loss_pct:      try 1.70, 1.75, 1.80, 1.85, 1.90, 1.95,
#                         2.00, 2.05, 2.10, 2.15, 2.20
#                     (current: 1.92 — try adjacent values first)
#
# timeout_hours:      try 120, 128, 136, 144, 152, 160, 168,
#                         176, 184, 192, 200
#                     (current: 166 — try 160, 168, 152, 176 first)
#
# rsi_long_threshold: try 34.0, 34.5, 35.0, 35.5, 36.0, 36.5,
#                         37.0, 37.5, 38.0, 38.5, 39.0, 39.5,
#                         40.0, 40.5, 41.0, 41.5, 42.0
#                     (current: 37.77 — try 37.0, 38.0, 36.5 first)
#
# rsi_period_hours:   try 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
#                     (current: 22 — confirmed champion value)
#
# LOW-PRIORITY (change only if all high-value ranges exhausted):
#   trend_period_hours: 36, 42, 48, 54, 60
#   rsi_short_threshold: 58, 59, 60, 61, 62, 63, 64
#   size_pct: 20, 22, 25, 28, 30
#   max_open: 2, 3, 4
#
# ══════════════════════════════════════════════════════════════════
# KNOWN FAILURES — DO NOT REPEAT
# ══════════════════════════════════════════════════════════════════
#
# These consistently produce bad results. Do not propose them:
#   - Very large timeout_hours (>210) → low trades, rejected
#   - Very small stop_loss_pct (<1.50) → low trades or degenerate Sharpe
#   - rsi_long_threshold > 45 or < 30 → degenerate attractor zone
#   - rsi_period_hours < 18 or > 30 → low trades or attractor
#   - Removing pairs → changes trade count unpredictably, avoid
#   - Adding new pairs → may lack 2yr data, invalid backtest
#
# ══════════════════════════════════════════════════════════════════
# INFRASTRUCTURE STATUS (human operator — action required)
# ══════════════════════════════════════════════════════════════════
#
# [BUG-2] YAML persistence broken. In-memory champion may be ~2.3680
#   (Gen 9000 evidence from prior run context). elite_0.yaml shows 2.3513.
#   Fix: ensure persistence call writes elite_0.yaml on every acceptance.
#   Test: submit above-champion YAML, confirm file timestamp updates.
#
# [BUG-4] Clone detection is post-backtest (35% dedup_reject rate).
#   Fix: pre-backtest SHA-256 hash of proposed YAML vs all prior accepted.
#
# [BUG-5] Poison_reject blocklist incomplete — (190t, -1.0406) still appearing.
#   Fix: add all RULE 5 signatures to blocklist with hash-based matching.
#
# [Z4] Pair audit overdue. Confirm APT/SUI/ARB/OP have ≥17,520 candles.
#   Remove any pair with incomplete data before live deployment.
#
# [Z8] Grid scan overdue (~5,000 gens without systematic sweep).
#   Run 1D sweep of all HIGH-VALUE ranges above (~61 backtests).
#   Sort by Sharpe. If any result > 2.3513, run 2D grid around that point.
#
# [Z9] Live deployment: zero sprint data. Deploy after Z4+Z8 complete.
#   Minimum 3 completed sprints before further parameter optimization.
#   Note: Current macro = CAUTION (F&G=27, Fear). Apply 50% position sizing.
#
# ══════════════════════════════════════════════════════════════════
# END OF RESEARCH PROGRAM
# ══════════════════════════════════════════════════════════════════
```

---