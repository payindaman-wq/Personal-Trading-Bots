```markdown
# ODIN Swing Optimizer | futures_swing | Champion Sharpe=1.3445 | trades=58

## CURRENT BEST STRATEGY — START FROM THIS EXACTLY
```yaml
name: crossover_tightened_momentum_short_v2
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

## LOCKED — NEVER CHANGE THESE
- size_pct: 30
- max_open: 3
- fee_rate: 0.001
- take_profit_pct: 6.63
- stop_loss_pct: 1.5
- timeout_hours: 129
- pause_if_down: 8, stop_if_down: 18, pause_hours: 48

## UNIVERSE — HARD CONSTRAINT
pairs must be a subset of [BTC/USD, ETH/USD, SOL/USD] ONLY. No other pairs exist.

## RESULT CLASSIFICATION
- trades=58, Sharpe≈1.3445 → CLONE — you changed nothing. Pick the NEXT untested item.
- trades=0, Sharpe=0.00 → MALFORMED — you changed >1 thing. Revert all.
- trades<35 → TOO TIGHT (discard)
- trades>60 → TOO LOOSE (discard)
- trades 35–60, Sharpe>1.3445 → NEW BEST ✓
- trades 35–60, Sharpe≤1.3445 → VALID DISCARD

## NEXT UNTESTED ITEM — APPLY EXACTLY ONE CHANGE

Apply the FIRST item not yet tested. Do NOT apply multiple changes.

**MANDATORY FIRST: C5**
```yaml
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
```
Change ONLY the pairs field. Everything else stays identical to the champion.

**IF C5 was already tested (produced trades=58 and Sharpe=1.3445), apply C1:**
- C1: Remove the long `momentum_accelerating` condition entirely (3 long conditions remain)

**IF C1 was already tested, apply C2:**
- C2: Remove the short `momentum_accelerating` condition entirely (3 short conditions remain)

**IF C1+C2 both tested, apply next from this list in order:**
- A1: long bollinger period_hours → 24 (was 48)
- A2: long bollinger period_hours → 72 (was 48)
- A3: long bollinger period_hours → 96 (was 48)
- A4: short bollinger period_hours → 72 (was 168)
- A5: short bollinger period_hours → 48 (was 168)
- A6: short bollinger period_hours → 96 (was 168)
- A7: long macd_signal period_hours → 24 (was 48)
- A8: long macd_signal period_hours → 72 (was 48)
- A9: short macd_signal period_hours → 48 (was 24)
- A10: long momentum period_hours → 24 (was 48)
- A11: long momentum period_hours → 72 (was 48)
- A12: short momentum period_hours → 24 (was 48)
- A13: short momentum period_hours → 72 (was 48)
- B1: long price_change_pct value → -0.25 (was -0.5) [loosen]
- B2: long price_change_pct value → -0.75 (was -0.5) [tighten]
- B3: long price_change_pct value → -1.0 (was -0.5) [tighter]
- B4: short price_change_pct value → 0.25 (was 0.5) [loosen]
- B5: short price_change_pct value → 0.75 (was 0.5) [tighten]
- B6: short price_change_pct value → 1.0 (was 0.5) [tighter]
- B7: long price_change_pct period_hours → 48 (was 24)
- B8: short price_change_pct period_hours → 48 (was 24)
- C3: long momentum_accelerating value → true (was false)
- C4: short momentum_accelerating value → true (was false)
- C6: long bollinger_position value → inside (was below_lower) [loosen]
- C7: short bollinger_position value → inside (was above_upper) [loosen]

## RULES — READ BEFORE GENERATING
1. Change EXACTLY ONE parameter from the champion YAML above.
2. Do NOT change any locked parameter.
3. Do NOT add conditions (C1/C2 remove one condition; C5 changes only pairs).
4. pairs must be a subset of [BTC/USD, ETH/USD, SOL/USD] only.
5. If your output has trades=58 and Sharpe≈1.3445, you made no effective change — pick the NEXT queue item.
6. Output the complete YAML only. No explanation. Wrap in ```yaml ... ```.
```

---