```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 20133 | Incumbent (STORED): Sharpe=1.4796, trades=55
# MIMIR-reviewed 2026-04-19 (v48)

# ══════════════════════════════════════════════════════════════════════
# YOUR ONLY JOB: OUTPUT THE YAML BELOW WITH EXACTLY ONE CHANGE (Step 2).
# ══════════════════════════════════════════════════════════════════════

# ████████████████████████████████████████████████████████████████████
# STEP 1 — COPY THIS YAML EXACTLY, THEN APPLY THE ONE CHANGE IN STEP 2
# ████████████████████████████████████████████████████████████████████

# ```yaml
# name: gen20133_e1a
# style: randomly generated
# pairs:
# - BTC/USD
# - ETH/USD
# - SOL/USD
# position:
#   size_pct: 25.0
#   max_open: 2
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
#       value: -0.5
#     - indicator: rsi
#       period_hours: 14
#       operator: lt
#       value: 35.0
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
#       value: 0.54
# exit:
#   take_profit_pct: 9.5
#   stop_loss_pct: 1.5
#   timeout_hours: 156
# risk:
#   pause_if_down_pct: 8
#   stop_if_down_pct: 18
#   pause_hours: 48
# ```

# ████████████████████████████████████████████████████████████████████
# STEP 2 — THE ONE CHANGE (apply to Step 1 YAML, nothing else)
# ████████████████████████████████████████████████████████████████████
#
# ACTIVE TEST: E1a
#   Change: long price_change_pct value: -0.5 → -1.0
#   (Requires a larger dip before entering long)
#   This is the ONLY change. All other values are identical to Step 1.
#
# AFTER YOUR CHANGE, the long price_change_pct block must read:
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: lt
#       value: -1.0

# ══════════════════════════════════════════════════════════════════════
# POISON CHECK — verify your output before submitting
# ══════════════════════════════════════════════════════════════════════
#
# ✗ pairs must be [BTC/USD, ETH/USD, SOL/USD]     (3 pairs)
# ✗ size_pct = 25.0
# ✗ max_open = 2
# ✗ take_profit_pct = 9.5
# ✗ stop_loss_pct = 1.5
# ✗ timeout_hours = 156
# ✗ rsi value = 35.0
# ✗ long price_change_pct value = -1.0             ← THE ONE CHANGE
# ✗ short price_change_pct value = 0.54
#
# POISON SIGNATURES (your YAML is wrong if you see these):
#   trades=55, Sharpe≈1.4796  →  CLONE. price_change_pct is still -0.5.
#   trades=0,  Sharpe=0.00    →  You added/removed a condition. Revert.
#   trades=58, Sharpe≈1.34    →  Wrong base. pairs must include ETH and SOL.
#
# VALID: trades 35–65, Sharpe computed (any value)

# ══════════════════════════════════════════════════════════════════════
# RESULT CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════
#
# trades=55, Sharpe≈1.4796     [CLONE]         → price_change_pct still -0.5
# trades=0,  Sharpe=0.00       [MALFORMED]     → revert to Step 1 + one change only
# trades<35                    [TOO TIGHT]     → E1a dead; move to E1b (-0.75)
# trades 35–65, Sharpe>1.4796  [NEW BEST]      → success; advance to E1b
# trades 35–65, Sharpe≤1.4796  [VALID DISCARD] → E1a tested; move to E1b (-0.75)

# ══════════════════════════════════════════════════════════════════════
# STORED CHAMPION VALUES (do not change these)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.4796, trades=55, WR=43.6% (Gen 20132 — elite_0.yaml GROUND TRUTH)
#
#   pairs:               BTC/USD, ETH/USD, SOL/USD
#   size_pct:            25.0
#   max_open:            2
#   long rsi:            35.0, lt, period=14
#   long price_change:   -0.5, lt, period=24   ← E1a changes this to -1.0
#   long bollinger:      below_lower, period=48
#   long macd:           bullish, period=48
#   long momentum:       false, period=48
#   short bollinger:     above_upper, period=168
#   short macd:          bearish, period=24
#   short price_change:  0.54, gt, period=24
#   short momentum:      false, period=48
#   take_profit_pct:     9.5
#   stop_loss_pct:       1.5
#   timeout_hours:       156
#   pause_if_down_pct:   8
#   stop_if_down_pct:    18
#   pause_hours:         48

# ══════════════════════════════════════════════════════════════════════
# TEST QUEUE
# ══════════════════════════════════════════════════════════════════════
#
# ACTIVE:
#   E1a: long price_change_pct → -1.0   ← CURRENT
#
# QUEUED (entry conditions only — exit/risk changes do not improve Sharpe):
#   E1b: long price_change_pct → -0.75  (if E1a dead or too restrictive)
#   E1c: long price_change_pct → -0.3   (if E1b dead; loosens entry)
#   E2a: long bollinger period_hours → 36
#   E2b: long bollinger period_hours → 60
#   E3a: short price_change_pct → 1.0
#   E3b: short bollinger period_hours → 72
#   E4a: rsi → 33.5
#   E4b: rsi → 36.5
#
# SUSPENDED (confirmed no Sharpe gains ever):
#   Exit/risk parameters: take_profit, stop_loss, timeout, pause, stop_if_down
#
# ══════════════════════════════════════════════════════════════════════
# CONFIRMED IMPROVEMENT TRAJECTORY
# ══════════════════════════════════════════════════════════════════════
#
#   Gen 19808: Sharpe=1.3483, trades=58, WR=41.4%
#   Gen 20475: Sharpe=1.4877, trades=55, WR=43.6%  (+0.139) entry change
#   Gen 20492: Sharpe=1.4898, trades=52, WR=50.0%  (+0.002) entry change
#   Gen 20502: Sharpe=1.6060, trades=54, WR=44.4%  (+0.116) multi-pair + RSI
#   Gen 20132: Sharpe=1.4796, trades=55, WR=43.6%  CURRENT STORED CHAMPION
#
# NOTE: Gen 22157–23932 entries in earlier program were phantom/corrupted.
# The stored file (elite_0.yaml) is the ground truth: Sharpe=1.4796.
#
# KEY INSIGHTS:
#   • Every gain came from entry condition changes
#   • Trade count ~54–55 is the natural signal count for this filter set
#   • WR ~43–50% with 9.5/1.5 TP/SL = 6.3:1 reward/risk is the edge
#   • Fewer, better-filtered trades = better Sharpe
#   • Do NOT change exit or risk parameters

# ══════════════════════════════════════════════════════════════════════
# COMMON LLM MISTAKES — READ BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# 1. CLONE: No change made. price_change_pct is still -0.5.
#    Fix: value must be -1.0 in your output.
#
# 2. ZERO TRADES: You added a condition or changed multiple values.
#    Fix: ONE change only. Do not touch momentum, bollinger, macd, rsi, or exit.
#
# 3. WRONG BASE: pairs=[BTC/USD] only, or size_pct=30, or take_profit=6.63.
#    Fix: Use the Step 1 YAML exactly. 3 pairs. size_pct=25.0. take_profit=9.5.
```

---