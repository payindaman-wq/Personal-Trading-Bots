```markdown
# ODIN Swing Trading Optimizer | Gen 21474 incumbent | Sharpe=1.3500 | trades=58
# YOUR JOB: Output the YAML below with EXACTLY ONE change applied.

# ══════════════════════════════════════════════
# OUTPUT THIS YAML — WITH THE CHANGE ALREADY APPLIED
# ══════════════════════════════════════════════

```yaml
name: gen21474_e2a
style: randomly generated
pairs:
- BTC/USD
position:
  size_pct: 30
  max_open: 3
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 36
      operator: eq
      value: below_lower
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bullish
    - indicator: price_change_pct
      period_hours: 24
      operator: lt
      value: -0.5
  short:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 168
      operator: eq
      value: above_upper
    - indicator: macd_signal
      period_hours: 24
      operator: eq
      value: bearish
    - indicator: price_change_pct
      period_hours: 24
      operator: gt
      value: 0.37
exit:
  take_profit_pct: 6.63
  stop_loss_pct: 1.5
  timeout_hours: 132
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

# THE ONE CHANGE APPLIED ABOVE: long bollinger period_hours = 36 (was 48)
# Everything else is IDENTICAL to the incumbent. Do not change anything else.

# ══════════════════════════════════════════════
# VERIFY YOUR OUTPUT — CHECK THESE EXACT VALUES
# ══════════════════════════════════════════════
#
#   name:                   gen21474_e2a
#   pairs:                  [BTC/USD]
#   size_pct:               30
#   max_open:               3
#   take_profit_pct:        6.63
#   stop_loss_pct:          1.5
#   timeout_hours:          132
#   long bollinger period:  36      ← THE CHANGE
#   long price_change:      -0.5
#   short price_change:     0.37
#   short bollinger period: 168
#
# IF YOUR OUTPUT HAS:
#   long bollinger period_hours: 48   → WRONG. You did not apply the change.
#   trades=58, Sharpe=1.35            → CLONE. long bollinger is still 48.
#   short price_change: 0.41          → WRONG. Must be 0.37.
#   size_pct: 17.89                   → WRONG. Must be 30.
#   max_open: 2                       → WRONG. Must be 3.
#   pairs includes ETH or SOL         → WRONG. BTC/USD only.

# ══════════════════════════════════════════════
# RESULT CLASSIFICATION
# ══════════════════════════════════════════════
#
#   trades=58, Sharpe≈1.35       [CLONE]         → bollinger still 48; fix it
#   trades=0,  Sharpe=0.00       [MALFORMED]     → you changed >1 thing; revert
#   trades<35                    [TOO TIGHT]     → E2a dead; move to E2b
#   trades 35–70, Sharpe>1.3500  [NEW BEST]      → advance to E2b
#   trades 35–70, Sharpe≤1.3500  [VALID DISCARD] → E2a tested; move to E2b

# ══════════════════════════════════════════════
# TEST QUEUE
# ══════════════════════════════════════════════
#
# ACTIVE:
#   E2a: long bollinger period_hours → 36        ← CURRENT GEN
#
# QUEUED (apply next if E2a is done):
#   E2b: long bollinger period_hours → 60
#   E3a: short price_change_pct → 0.5
#   E3b: short price_change_pct → 0.25
#   E3c: short bollinger period_hours → 72
#   E4a: short macd period_hours → 48
#   E4b: long macd period_hours → 36
#   E5a: add rsi lt 35.0 to long conditions
#   E5b: expand to ETH/USD, SOL/USD pairs
#
# RULES:
#   • ONE change per generation. Never more.
#   • Do NOT touch exit or risk parameters — confirmed no Sharpe gains.
#   • Do NOT add or remove conditions — only change existing values.
#   • Do NOT change pairs, size_pct, max_open, fee_rate.
#   • Advance through queue only after current test produces a classifiable result.
```

---