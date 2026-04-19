# ODIN Day League Research Program
# v11000-lean

═══════════════════════════════════════════════════════════════
COPY THIS YAML EXACTLY. Change ONLY the three values in Step 2.
═══════════════════════════════════════════════════════════════

```yaml
name: crossover
style: momentum_optimized
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
  size_pct: 10
  max_open: 4
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: lt        # <-- MUST be lt. If gt: DELETE, start over.
      value: -0.43        # <-- MUST be negative. If positive or 0: DELETE, start over.
    - indicator: macd_signal
      period_minutes: 45
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt        # <-- MUST be gt. If lt: DELETE, start over.
      value: 0.43
    - indicator: macd_signal
      period_minutes: 45
      operator: eq
      value: bearish
exit:
  take_profit_pct: 2.5
  stop_loss_pct: 1.2
  timeout_minutes: 720
risk:
  pause_if_down_pct: 4
  stop_if_down_pct: 10
  pause_minutes: 60
```

═══════════════════════════════════════════════════════════════
STEP 1 — VERIFY THREE THINGS BEFORE SUBMITTING
═══════════════════════════════════════════════════════════════

  long.operator   = lt     (NOT gt)
  long.value      = -0.43  (NEGATIVE, not positive, not 0)
  short.operator  = gt     (NOT lt)

If any are wrong → DELETE and restart. Do not patch.

═══════════════════════════════════════════════════════════════
STEP 2 — THREE VALUES THAT CHANGE BY TARGET
═══════════════════════════════════════════════════════════════

Only long.value, short.value, macd period_minutes change. Nothing else, ever.

| Target | long.value | short.value | macd period |
|--------|------------|-------------|-------------|
| A1     | -0.43      | 0.43        | 45          | ← CURRENT
| A2     | -0.42      | 0.42        | 45          |
| A3     | -0.41      | 0.41        | 45          |
| A4     | -0.44      | 0.44        | 45          |
| A5     | -0.40      | 0.40        | 45          |
| B1     | -0.42      | 0.42        | 30          |
| B2     | -0.41      | 0.41        | 30          |
| B3     | -0.40      | 0.40        | 30          |

Run 8 reps per target before advancing. A rep = any result with trades ≤ 450.

═══════════════════════════════════════════════════════════════
STEP 3 — ACCEPTANCE
═══════════════════════════════════════════════════════════════

Formal best: Sharpe = 1.1227, trades = 309 (gen 9325).
Beat it = Sharpe > 1.1227 AND trades ≥ 280.

| Result                     | Tag                   | Counts as rep? |
|----------------------------|-----------------------|----------------|
| trades > 450               | [structural_failure]  | NO             |
| trades < 280               | [low_trades]          | YES            |
| 280 ≤ trades ≤ 450, S<1.12 | [discarded]           | YES            |
| 280 ≤ trades ≤ 450, S>1.12 | [new_best] — deploy   | YES            |

MIN_TRADES = 280. Final. Do not change.

═══════════════════════════════════════════════════════════════
NEVER CHANGE THESE FIELDS
═══════════════════════════════════════════════════════════════

name, style, pairs (all 16), max_open=4, size_pct=10, fee_rate=0.001,
take_profit_pct=2.5, stop_loss_pct=1.2, timeout_minutes=720,
price_change_pct period_minutes=30, total conditions=4 (2 long, 2 short).

═══════════════════════════════════════════════════════════════
FAILURE FINGERPRINTS — DIAGNOSE FAST
═══════════════════════════════════════════════════════════════

  trades=818, sharpe=-4.78  → long.operator is gt (should be lt)
  trades≥1000               → structural failure; recheck all operators
  trades<140, sharpe<0      → long.value is 0 or positive
  trades=0                  → YAML malformed

═══════════════════════════════════════════════════════════════
NOTE
═══════════════════════════════════════════════════════════════

Escalation to MIMIR is now handled by the researcher loop in code.
You do NOT need to self-check escalation triggers. Just submit YAMLs.
