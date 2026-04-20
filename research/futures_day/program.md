```markdown
# ODIN — FUTURES DAY v38.0

## YOUR ONLY JOB
Output EXACTLY: a CHANGE line, a USING line, then the YAML below with ONE value changed from the champion. Nothing else. No explanation.

## CHAMPION YAML (copy this exactly, change ONE value only)

```yaml
name: crossover
style: mean_reversion_swing
league: futures_day
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
  size_pct: 8
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: lt
      value: 29.33
  short:
    conditions:
    - indicator: rsi
      period_minutes: 60
      operator: gt
      value: 68.63
exit:
  take_profit_pct: 4.6
  stop_loss_pct: 2.59
  timeout_minutes: 720
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

## BANNED VALUES — DO NOT USE THESE (instant reject)
- entry.short.conditions[0].value: 68.63 (champion — must change it)
- entry.long.conditions[0].value: 32.0, 35.97
- position.size_pct: 16.91
- exit.stop_loss_pct: 2.39
- exit.take_profit_pct: 5.0

## NEXT STEP TO TRY (pick the first untested one)
1. entry.short.conditions[0].value → 66.0  ← TRY THIS FIRST
2. entry.short.conditions[0].value → 64.0  (if 66.0 already tested)
3. entry.short.conditions[0].value → 62.0  (if 64.0 already tested)
4. exit.stop_loss_pct → 2.3               (if short ladder exhausted)
5. position.size_pct → 10                 (if stop_loss tested)
6. exit.take_profit_pct → 4.2             (if size_pct tested)
7. entry.long.conditions[0].value → 27.0  (if tp tested)

## PREFLIGHT CHECKLIST (verify before outputting)
- [ ] Exactly ONE value differs from champion YAML above
- [ ] Changed value is NOT in the BANNED VALUES list
- [ ] Changed value has NOT been tested before (check TESTED list)
- [ ] YAML structure is identical to champion (same keys, same order)
- [ ] fee_rate is 0.0005 (do not change)
- [ ] leverage is 2 (do not change)
- [ ] All 16 pairs present (do not add or remove)

## TESTED AND FAILED (do not resubmit these)
- rsi_short=68.63 (champion)
- rsi_short=66.0 (Gen ~Step3 — if this appears in results, skip to 64.0)
- rsi_long=32.0 (Gen 3903/3916: Sharpe=0.296)
- rsi_long=35.97 (BANNED)
- size_pct=16.91 (BANNED)
- stop_loss=2.39 (BANNED)
- tp=5.0 (Gen 3770: Sharpe=0.0213)

## CHAMPION CONTEXT
- Champion: Gen 3233, Sharpe=0.4066, 1756 trades, WR=50.1%
- Goal: Sharpe > 0.4066
- MIN_TRADES[futures_day] = 50 — FROZEN

## OUTPUT FORMAT (exactly this, nothing else)
CHANGE: [field] [old_value] → [new_value]
USING: size_pct=8, rsi_long=29.33, rsi_short=[value], stop_loss=2.59, tp=4.6
[YAML]
```