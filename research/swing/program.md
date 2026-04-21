```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 21474 | Incumbent (STORED): Sharpe=1.3500, trades=58
# MIMIR-reviewed 2026-04-20 (v51)

# ════════════════════════════════════════════════════════
# YOUR ONLY JOB: OUTPUT THE YAML BELOW WITH EXACTLY ONE CHANGE
# ════════════════════════════════════════════════════════

# ████████████████████████████████████████████████
# STEP 1 — OUTPUT THIS YAML EXACTLY, THEN APPLY THE ONE CHANGE BELOW
# ████████████████████████████████████████████████

# ```yaml
# name: gen21474_e1b
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
#       value: -0.5
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
# STEP 2 — APPLY EXACTLY ONE CHANGE
# ████████████████████████████████████████████████
#
# ACTIVE TEST: E1b
#   Change: long price_change_pct value: -0.5 → -0.5
#   (E1b IS the base — this is the incumbent long price_change_pct value)
#
# NEXT QUEUED: E2a — long bollinger period_hours: 48 → 36
#
# FOR THIS GENERATION: Apply E2a.
# Change long bollinger period_hours from 48 to 36.
#
# AFTER YOUR CHANGE, the long bollinger block must read:
#     - indicator: bollinger_position
#       period_hours: 36
#       operator: eq
#       value: below_lower

# ════════════════════════════════════════════════
# POISON CHECK — verify before submitting
# ════════════════════════════════════════════════
#
# Required values in your output:
#   pairs: [BTC/USD]               ← 1 pair only
#   size_pct: 30
#   max_open: 3
#   take_profit_pct: 6.63
#   stop_loss_pct: 1.5
#   timeout_hours: 132
#   long price_change_pct value: -0.5    ← unchanged
#   short price_change_pct value: 0.37   ← unchanged
#   long bollinger period_hours: 36      ← THE ONE CHANGE
#
# POISON SIGNATURES — your YAML is WRONG if you see these:
#   trades=58, Sharpe≈1.35  →  CLONE. bollinger period_hours is still 48. Fix it.
#   trades=0,  Sharpe=0.00  →  You changed more than one thing. Revert extra changes.
#   pairs includes ETH or SOL  →  WRONG. Use BTC/USD only.
#   take_profit_pct ≠ 6.63  →  WRONG BASE. Must be 6.63.
#   timeout_hours ≠ 132  →  WRONG BASE. Must be 132.
#   size_pct ≠ 30  →  WRONG BASE. Must be 30.
#   short price_change_pct ≠ 0.37  →  WRONG BASE. Must be 0.37.
#   long bollinger period_hours=48  →  CLONE. Change it to 36.
#
# VALID: trades 35–70, Sharpe computed (any value), long bollinger period_hours=36

# ════════════════════════════════════════════════
# RESULT CLASSIFICATION
# ════════════════════════════════════════════════
#
# trades=58, Sharpe≈1.35        [CLONE]         → bollinger still 48; fix it
# trades=0,  Sharpe=0.00        [MALFORMED]     → revert; one change only
# trades<35                     [TOO TIGHT]     → E2a dead; move to E2b
# trades 35–70, Sharpe>1.3500   [NEW BEST]      → success; advance to E2b
# trades 35–70, Sharpe≤1.3500   [VALID DISCARD] → E2a tested; move to E2b

# ════════════════════════════════════════════════
# STORED CHAMPION (do not change these values)
# ════════════════════════════════════════════════
#
# Sharpe=1.3500, trades=58, WR=41.4%
#
#   pairs:               BTC/USD  (1 pair)
#   size_pct:            30
#   max_open:            3
#   long price_change:   -0.5, lt, period=24
#   long bollinger:      below_lower, period=48   ← E2a changes to 36
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
# COMPLETED:
#   E1a: long price_change_pct → -0.75   [too tight or valid discard]
#   E1b: long price_change_pct → -0.5    [this IS the incumbent value; base confirmed]
#   E1c: long price_change_pct → -0.25   [skipped; incumbent already at -0.5]
#
# ACTIVE:
#   E2a: long bollinger period_hours → 36        ← CURRENT
#
# QUEUED:
#   E2b: long bollinger period_hours → 60
#   E3a: short price_change_pct → 0.5
#   E3b: short price_change_pct → 0.25
#   E3c: short bollinger period_hours → 72
#   E4a: short macd period_hours → 48
#   E4b: long macd period_hours → 36
#   E5a: add rsi lt 35.0 to long conditions
#   E5b: expand to ETH/USD, SOL/USD pairs
#
# NOTE: Historical best Sharpe≈1.63 (gens 23765–23932) was lost during population
# reordering. Target is recovering and exceeding that level. Entry condition changes
# are the ONLY proven source of Sharpe gains.
#
# SUSPENDED (confirmed no Sharpe gains):
#   take_profit, stop_loss, timeout, pause_if_down, stop_if_down

# ════════════════════════════════════════════════
# KEY RULES
# ════════════════════════════════════════════════
#
# • ONE change only. Never touch more than one value.
# • Exit/risk parameters never improve Sharpe. Do not touch them.
# • Entry condition changes are the only proven source of gains.
# • Do NOT add or remove conditions — only change existing values.
# • Do NOT change pairs, size_pct, max_open, fee_rate.
# • The name field must reflect the current gen/test (e.g., gen21474_e2a).
```

---

**Program Notes for MIMIR (not sent to LLM):**

- The "Current Best Strategy" YAML displayed in the UI shows `size_pct=17.89, max_open=2, long price_change_pct=-0.5, short price_change_pct=0.41` — this diverges from the stored champion in elite_0.yaml (`size_pct=30, max_open=3, price_change_pct=-0.38/-0.37`). The research program correctly anchors to elite_0.yaml values. The displayed YAML likely reflects a different population slot or a stale display cache. Monitor for convergence.
- E1a result is ambiguous from the log — gen 21474 (Sharpe=1.3500, trades=58) is labeled new_best but the margin over 1.3498 is trivial. The research program should treat the long price_change_pct as effectively at -0.5 (the current best YAML value) rather than -0.38 (the research program anchor). I've updated the incumbent to reflect -0.5 in the program, advancing to E2a.
- Live sprint (0 trades, rank 5/10) is a concern. If this persists for 2+ sprints, escalate to check live signal generation — the backtest strategy may not be deployed correctly.