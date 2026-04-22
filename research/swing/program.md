```markdown
# ODIN Swing Optimizer | BTC/USD only | Sharpe=1.3445 | trades=58
# OUTPUT THE YAML BELOW WITH EXACTLY ONE CHANGE APPLIED — NOTHING ELSE.

```yaml
name: gen_NEXT
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
      period_hours: 48
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
      value: 0.5
exit:
  take_profit_pct: 6.63
  stop_loss_pct: 1.5
  timeout_hours: 129
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

# ══════════════════════════════════════════════
# TEST QUEUE — apply the NEXT UNTESTED item
# ══════════════════════════════════════════════
#
# ACTIVE (apply whichever is next incomplete):
#   E2b: long bollinger period_hours → 60        (was 48)
#   E3a: short price_change_pct → 0.5            (was 0.37 in prior run; anchor is 0.5)
#   E3b: short price_change_pct → 0.25
#   E3c: short bollinger period_hours → 72       (was 168)
#   E4a: short macd_signal period_hours → 48     (was 24)
#   E4b: long macd_signal period_hours → 36      (was 48)
#   E5a: long bollinger period_hours → 24
#   E5b: long momentum period_hours → 24         (was 48)
#   E6a: long momentum period_hours → 72
#   E6b: short momentum period_hours → 24        (was 48)
#   E7a: long price_change_pct → -0.75
#   E7b: long price_change_pct → -0.25
#   E8a: pairs: [BTC/USD, ETH/USD, SOL/USD]     (expand universe)
#
# ONE CHANGE ONLY. Do not modify exit or risk blocks.
# Do not add/remove conditions. Do not change size_pct, max_open, fee_rate.
# NEVER change more than one parameter from the incumbent YAML above.

# ══════════════════════════════════════════════
# VERIFY YOUR OUTPUT — REQUIRED BEFORE SUBMITTING
# ══════════════════════════════════════════════
#
# Fixed values that MUST NOT change (ever):
#   pairs:           [BTC/USD]          ← unless applying E8a
#   size_pct:        30
#   max_open:        3
#   fee_rate:        0.001
#   take_profit_pct: 6.63
#   stop_loss_pct:   1.5
#   timeout_hours:   129
#   pause_if_down:   8
#   stop_if_down:    18
#   pause_hours:     48
#
# Result classification:
#   trades=58, Sharpe≈1.34   → CLONE (you changed nothing; apply the queue item)
#   trades=0,  Sharpe=0.00   → MALFORMED (you changed >1 thing; revert extras)
#   trades<35                → TOO TIGHT (discard; move to next queue item)
#   trades 35–70, Sharpe>1.3445 → NEW BEST
#   trades 35–70, Sharpe≤1.3445 → VALID DISCARD (move to next queue item)
```