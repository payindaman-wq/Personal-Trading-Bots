```markdown
# ODIN Swing Optimizer | BTC/USD | Sharpe=1.3445 | trades=58
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
# FIXED VALUES — DO NOT CHANGE THESE (EVER)
# ══════════════════════════════════════════════
#   size_pct:        30         ← EXACT
#   max_open:        3
#   fee_rate:        0.001
#   take_profit_pct: 6.63
#   stop_loss_pct:   1.5
#   timeout_hours:   129        ← EXACT
#   pause_if_down:   8
#   stop_if_down:    18
#   pause_hours:     48
#   pairs:           [BTC/USD]  ← single pair unless applying E8a

# ══════════════════════════════════════════════
# RESULT CLASSIFICATION
# ══════════════════════════════════════════════
#   trades=58, Sharpe≈1.3445 → CLONE (no change made; apply next queue item)
#   trades=0,  Sharpe=0.00   → MALFORMED (changed >1 thing; revert)
#   trades<35                → TOO TIGHT (discard; next item)
#   trades>60                → TOO LOOSE (discard; next item)
#   trades 35–60, Sharpe>1.3445 → NEW BEST
#   trades 35–60, Sharpe≤1.3445 → VALID DISCARD (next item)

# ══════════════════════════════════════════════
# TEST QUEUE — apply the NEXT UNTESTED item
# ══════════════════════════════════════════════
#
# PRIORITY ORDER (apply next incomplete):
#
#   E7b: long price_change_pct value → -0.25         (was -0.5)  [loosen long entry]
#   E7c: long price_change_pct value → -0.75         (was -0.5)  [tighten long entry]
#   E5a: long bollinger period_hours → 24            (was 48)    [faster signal]
#   E5b: long bollinger period_hours → 72            (was 48)    [slower signal]
#   E4a: short macd_signal period_hours → 48         (was 24)    [align with long]
#   E4b: long macd_signal period_hours → 24          (was 48)    [faster macd]
#   E3a: short bollinger period_hours → 72           (was 168)   [tighten short]
#   E3b: short bollinger period_hours → 48           (was 168)   [match long period]
#   E6a: long momentum period_hours → 24             (was 48)    [faster momentum]
#   E6b: short momentum period_hours → 24            (was 48)    [faster momentum]
#   E9a: short price_change_pct value → 0.75         (was 0.5)   [tighten short]
#   E9b: short price_change_pct value → 0.25         (was 0.5)   [loosen short]
#   E10: timeout_hours → 96                          (was 129)   [earlier exit]
#   E11: timeout_hours → 168                         (was 129)   [longer hold]
#   E8a: pairs: [BTC/USD, ETH/USD, SOL/USD]          [expand — expect trades 50-75; reject if >60]
#
# ONE CHANGE ONLY. Do not modify exit or risk blocks (except E10/E11 above).
# Do not add/remove conditions. Do not change size_pct, max_open, fee_rate.
# NEVER change more than one parameter from the incumbent YAML above.
```