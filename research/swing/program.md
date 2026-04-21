```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 21280 | Incumbent (STORED): Sharpe=1.3498, trades=58
# MIMIR-reviewed 2026-04-20 (v50)

# ════════════════════════════════════════════════════════
# YOUR ONLY JOB: OUTPUT THE YAML BELOW WITH EXACTLY ONE CHANGE
# ════════════════════════════════════════════════════════

# ████████████████████████████████████████████████
# STEP 1 — COPY THIS YAML EXACTLY (this is the TRUE champion)
# ████████████████████████████████████████████████

# ```yaml
# name: gen21279_e1a
# style: randomly generated
# pairs:
# - BTC/USD
# position:
#   size_pct: 30
#   max_open: 3
#   fee_rate: 0.001
# entry:
#   long:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 48
#       operator: eq
#       value: below_lower
#     - indicator: macd_signal
#       period_hours: 48
#       operator: eq
#       value: bullish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: lt
#       value: -0.38
#   short:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 168
#       operator: eq
#       value: above_upper
#     - indicator: macd_signal
#       period_hours: 24
#       operator: eq
#       value: bearish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: gt
#       value: 0.37
# exit:
#   take_profit_pct: 6.63
#   stop_loss_pct: 1.5
#   timeout_hours: 132
# risk:
#   pause_if_down_pct: 8
#   stop_if_down_pct: 18
#   pause_hours: 48
# ```

# ████████████████████████████████████████████████
# STEP 2 — APPLY EXACTLY ONE CHANGE FROM THE TEST QUEUE
# ████████████████████████████████████████████████
#
# ACTIVE TEST: E1a
#   Change: long price_change_pct value: -0.38 → -0.75
#
# AFTER YOUR CHANGE, the long price_change_pct block must read:
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: lt
#       value: -0.75

# ════════════════════════════════════════════════
# POISON CHECK — verify before submitting
# ════════════════════════════════════════════════
#
# Required values in your output:
#   pairs: [BTC/USD]  (1 pair only)
#   size_pct: 30
#   max_open: 3
#   take_profit_pct: 6.63
#   stop_loss_pct: 1.5
#   timeout_hours: 132
#   long price_change_pct value: -0.75   ← THE ONE CHANGE
#   short price_change_pct value: 0.37
#
# POISON SIGNATURES (your YAML is wrong if you see these):
#   trades=58, Sharpe≈1.34  →  CLONE. price_change_pct is still -0.38. Fix it.
#   trades=0,  Sharpe=0.00  →  You changed more than one thing. Revert extra changes.
#   pairs includes ETH or SOL  →  WRONG BASE. Use BTC/USD only.
#   take_profit_pct=9.5  →  WRONG BASE. Must be 6.63.
#   timeout_hours=129  →  WRONG BASE. Must be 132.
#   short price_change_pct=0.5  →  WRONG BASE. Must be 0.37.
#
# VALID: trades 35–70, Sharpe computed (any value), price_change_pct=-0.75

# ════════════════════════════════════════════════
# RESULT CLASSIFICATION
# ════════════════════════════════════════════════
#
# trades=58, Sharpe≈1.35        [CLONE]         → price_change_pct still -0.38
# trades=0,  Sharpe=0.00        [MALFORMED]     → revert; one change only
# trades<35                     [TOO TIGHT]     → E1a dead; move to E1b
# trades 35–70, Sharpe>1.3498   [NEW BEST]      → success; advance to E1b
# trades 35–70, Sharpe≤1.3498   [VALID DISCARD] → E1a tested; move to E1b

# ════════════════════════════════════════════════
# STORED CHAMPION (do not change these)
# ════════════════════════════════════════════════
#
# Sharpe=1.3498, trades=58, WR=41.4%
#
#   pairs:               BTC/USD  (1 pair)
#   size_pct:            30
#   max_open:            3
#   long price_change:   -0.38, lt, period=24   ← E1a changes to -0.75
#   long bollinger:      below_lower, period=48
#   long macd:           bullish, period=48
#   long momentum:       false, period=48
#   short bollinger:     above_upper, period=168
#   short macd:          bearish, period=24
#   short price_change:  0.37, gt, period=24
#   short momentum:      false, period=48
#   take_profit_pct:     6.63
#   stop_loss_pct:       1.5
#   timeout_hours:       132

# ════════════════════════════════════════════════
# TEST QUEUE
# ════════════════════════════════════════════════
#
# ACTIVE:
#   E1a: long price_change_pct → -0.75       ← CURRENT
#
# QUEUED:
#   E1b: long price_change_pct → -0.5        (if E1a too tight)
#   E1c: long price_change_pct → -0.25       (if E1b too tight; loosens entry)
#   E2a: long bollinger period_hours → 36
#   E2b: long bollinger period_hours → 60
#   E3a: short price_change_pct → 0.5
#   E3b: short price_change_pct → 0.25
#   E3c: short bollinger period_hours → 72
#   E4a: short macd period_hours → 48
#   E4b: long macd period_hours → 36
#   E5a: add rsi lt 35.0 to long conditions
#   E5b: expand to ETH/USD, SOL/USD pairs
#
# NOTE: Historical best Sharpe≈1.63 was achieved around gen 23765–23932.
# Target is recovering and exceeding that level. Entry condition changes
# are the ONLY proven source of Sharpe gains.
#
# SUSPENDED (confirmed no Sharpe gains):
#   take_profit, stop_loss, timeout, pause, stop_if_down

# ════════════════════════════════════════════════
# KEY RULES
# ════════════════════════════════════════════════
#
# • ONE change only. Never touch more than one value.
# • Exit/risk parameters never improve Sharpe. Do not touch them.
# • Entry condition changes are the only proven source of gains.
# • Do NOT add or remove conditions — only change existing values.
# • Do NOT change pairs, size_pct, max_open, fee_rate.
```

---