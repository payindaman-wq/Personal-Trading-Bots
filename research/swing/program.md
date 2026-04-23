```markdown
# ODIN Swing Optimizer | BTC/USD | Sharpe=1.3550 | trades=58
# OUTPUT THE YAML BELOW WITH EXACTLY ONE CHANGE APPLIED — NOTHING ELSE.

```yaml
name: gen_NEXT
style: randomly generated
pairs:
- BTC/USD
position:
  size_pct: 21.41
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
  timeout_hours: 133
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

# ══════════════════════════════════════════════
# VERIFY YOUR OUTPUT — REQUIRED BEFORE SUBMITTING
# ══════════════════════════════════════════════
#
# Fixed values that MUST NOT change (ever):
#   size_pct:        21.41      ← EXACT, do not round or change
#   max_open:        3
#   fee_rate:        0.001
#   take_profit_pct: 6.63
#   stop_loss_pct:   1.5
#   timeout_hours:   133        ← EXACT
#   pause_if_down:   8
#   stop_if_down:    18
#   pause_hours:     48
#   pairs:           [BTC/USD]  ← unless applying E8a below
#
# Result classification:
#   trades=58, Sharpe≈1.355  → CLONE (you changed nothing; apply queue item)
#   trades=0,  Sharpe=0.00   → MALFORMED (changed >1 thing; revert)
#   trades<35                → TOO TIGHT (discard; move to next queue item)
#   trades 35–60, Sharpe>1.3550 → NEW BEST
#   trades 35–60, Sharpe≤1.3550 → VALID DISCARD (move to next queue item)

# ══════════════════════════════════════════════
# TEST QUEUE — apply the NEXT UNTESTED item
# ══════════════════════════════════════════════
#
# ACTIVE (apply whichever is next incomplete):
#   E8a: pairs: [BTC/USD, ETH/USD, SOL/USD]    ← PRIORITY: expand universe
#   E3c: short bollinger period_hours → 72      (was 168)
#   E4a: short macd_signal period_hours → 48    (was 24)
#   E4b: long macd_signal period_hours → 36     (was 48)
#   E5a: long bollinger period_hours → 24       (was 48)
#   E5b: long momentum period_hours → 24        (was 48)
#   E6a: long momentum period_hours → 72        (was 48)
#   E6b: short momentum period_hours → 24       (was 48)
#   E7a: long price_change_pct → -0.75          (was -0.5)
#   E7b: long price_change_pct → -0.25          (was -0.5)
#   E2b: long bollinger period_hours → 60       (was 48)
#
# ONE CHANGE ONLY. Do not modify exit or risk blocks.
# Do not add/remove conditions. Do not change size_pct, max_open, fee_rate.
# NEVER change more than one parameter from the incumbent YAML above.
#
# For E8a specifically: change pairs list ONLY. All other values unchanged.
# Result of E8a: expect trades to rise (50-70 range). If >60 trades → TOO MANY.
```