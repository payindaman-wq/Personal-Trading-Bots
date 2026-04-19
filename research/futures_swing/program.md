```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-5515 | Revised by MIMIR (Gen 5515 review)
#
# ══════════════════════════════════════════════════════════════════
# CHAMPION YAML — COPY THIS, CHANGE EXACTLY ONE VALUE, SUBMIT
# ══════════════════════════════════════════════════════════════════
#
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
      period_hours: 24        # CANONICAL value from elite_0.yaml — do NOT change to 22
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24        # CANONICAL value from elite_0.yaml — do NOT change to 22
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
# RULES — VERIFY BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════
#
# RULE 1: Change EXACTLY ONE parameter. One. Not two. Not zero.
# RULE 2: Your result MUST produce 400–3000 trades. If uncertain, pick
#         a different parameter. Small RSI or stop_loss changes are risky.
# RULE 3: Do NOT submit the champion YAML unchanged → [discarded].
# RULE 4: Do NOT repeat a previously proposed configuration → [dedup_reject].
# RULE 5: Do NOT recreate these known-bad signatures (trades, sharpe):
#           (190t, -1.0517), (185t, -0.7900), (28t, -9.018),
#           (174t, -1.9619), (224t, -1.7297), (178t, -0.8033),
#           (182t, -1.8625), (158t, -2.0796), (239t, -2.4141),
#           (397t, -0.5405), (461t, -0.4605), (18t, -14.3473),
#           (190t, -1.0406), (190t, -1.6316).
#         If your change would produce ~190 trades, do NOT submit it.
# RULE 6: Use the HIGH-VALUE parameter grid below. Try untested values.
#
# ══════════════════════════════════════════════════════════════════
# HIGH-VALUE PARAMETERS — PRIORITY ORDER
# ══════════════════════════════════════════════════════════════════
#
# PRIORITY 1 — try these first (strongest improvement history):
#
# take_profit_pct:   [4.50, 4.55, 4.60, 4.70, 4.75, 4.80, 4.85,
#                     4.90, 4.95, 5.00, 5.10, 5.20, 5.30, 5.40, 5.50]
#                    (current=4.65; try 4.70, 4.60, 4.80, 4.55 first)
#
# stop_loss_pct:     [1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00,
#                     2.05, 2.10, 2.15, 2.20, 2.25, 2.30]
#                    (current=1.92; try 1.95, 1.90, 2.00, 1.85 first)
#                    WARNING: values < 1.70 → ~190 trades → [low_trades]
#
# timeout_hours:     [120, 128, 136, 144, 152, 156, 160, 164, 168,
#                     172, 176, 180, 184, 192, 200]
#                    (current=166; try 160, 168, 172, 164 first)
#
# rsi_long_threshold (value under "lt"): 
#                    [34.0, 34.5, 35.0, 35.5, 36.0, 36.5, 37.0,
#                     37.5, 38.0, 38.5, 39.0, 39.5, 40.0, 40.5,
#                     41.0, 41.5, 42.0]
#                    (current=37.77; try 38.0, 37.5, 38.5, 37.0 first)
#                    WARNING: values > 45 or < 30 → degenerate attractor
#
# PRIORITY 2 — try after Priority 1 exhausted:
#
# rsi_period_hours:  [18, 19, 20, 21, 22, 23, 25, 26, 27, 28]
#                    (current=24; do NOT try 24 — that is the champion)
#                    WARNING: values < 18 or > 30 → low trades
#
# rsi_short_threshold (value under "gt"):
#                    [57, 58, 59, 61, 62, 63, 64, 65]
#                    (current=60; try 59, 61, 58, 62 first)
#
# PRIORITY 3 — low priority, try last:
#
# trend_period_hours: [36, 42, 54, 60, 72]  (current=48)
# size_pct:          [20, 22, 28, 30]        (current=25)
# max_open:          [2, 4]                  (current=3)
# pause_if_down_pct: [6, 7, 9, 10]          (current=8)
# stop_if_down_pct:  [15, 16, 17, 20, 22]   (current=18)
#
# ══════════════════════════════════════════════════════════════════
# KNOWN FAILURES — DO NOT PROPOSE
# ══════════════════════════════════════════════════════════════════
#
# - stop_loss_pct < 1.70 → ~190 trades → automatic reject
# - rsi_long_threshold > 45 or < 30 → degenerate Sharpe
# - rsi_period_hours < 18 or > 30 → low trades
# - timeout_hours > 210 → low trades
# - Adding or removing pairs → invalid (data gaps / unpredictable trade count)
# - rsi_period_hours = 22 → was a previous tested value, avoid
#
# ══════════════════════════════════════════════════════════════════
# INFRASTRUCTURE STATUS (human operator — action required)
# ══════════════════════════════════════════════════════════════════
#
# [CRITICAL] rsi_period_hours corrected to 24 (was erroneously listed as 22
#   in previous program versions). The elite_0.yaml canonical value is 24.
#   Prior program misdirected the LLM. All generation output from programs
#   specifying 22 may have been mutating from wrong base.
#
# [BUG-2] YAML persistence broken. elite_0.yaml may lag in-memory champion.
#   Fix: ensure persistence call writes elite_0.yaml on every acceptance.
#
# [BUG-4] Clone detection is post-backtest (35% dedup_reject rate).
#   Fix: pre-backtest SHA-256 hash of proposed YAML vs all prior accepted.
#
# [BUG-5] Poison attractor (~190 trades, negative Sharpe) still appearing.
#   Fix: pre-backtest trade-count estimation gate; block known-bad signatures.
#
# [Z4] REQUIRED before live: confirm APT/SUI/ARB/OP have ≥17,520 candles.
#   Remove pairs with incomplete data before any live deployment.
#
# [Z8] REQUIRED: systematic grid scan overdue (>2,000 gens since last improvement).
#   Run full 1D sweep of all PRIORITY 1 ranges (~50 backtests).
#   Sort results by Sharpe. If any > 2.3513, run 2D grid around that point.
#   This is more efficient than random LLM sampling at this plateau depth.
#
# [Z9] Live deployment: zero sprint data. Do NOT deploy until Z4+Z8 complete.
#   Macro = CAUTION (F&G=27, Fear). Apply 50% position sizing in live only
#   (do NOT change size_pct in backtest YAML — keep at 25 for comparability).
#
# ══════════════════════════════════════════════════════════════════
# END OF RESEARCH PROGRAM
# ══════════════════════════════════════════════════════════════════
```

---