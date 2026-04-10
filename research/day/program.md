```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 6800-MIMIR-AUDIT

---

## ⚠️ READ THIS ENTIRE DOCUMENT BEFORE WRITING ANY OUTPUT ⚠️

---

## YOUR ONLY JOB

You are a two-parameter tuner. Output ONE YAML block.
Change ONLY two values: the price_change_pct threshold pair AND the
macd_signal period_minutes. Change nothing else. Output nothing else.

---

## THE ONE AND ONLY VALID TEMPLATE

Copy this block exactly. Change ONLY the two values marked ← CHANGE THIS.

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
      operator: lt
      value: -0.43        ← CHANGE THIS
    - indicator: macd_signal
      period_minutes: 30  ← CHANGE THIS
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43         ← CHANGE THIS (sign-flipped long value)
    - indicator: macd_signal
      period_minutes: 30  ← CHANGE THIS (same as long macd period)
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

---

## RULES — READ CAREFULLY

### Parameter 1: price_change_pct threshold

- Long value: one of exactly: -0.40, -0.41, -0.42, -0.43, -0.44,
              -0.45, -0.46, -0.47, -0.48, -0.49, -0.50
- Short value: same number, sign flipped (e.g., long=-0.43 → short=+0.43)
- Exactly 2 decimal places. No other values permitted.
- period_minutes: 30 on price_change_pct is FIXED. Never change it.

### Parameter 2: macd_signal period_minutes

- Must be exactly 15, 30, or 45
- Must be identical for long and short macd_signal conditions
- No other values permitted

### Fields that must never change

| Field             | Required value      |
|-------------------|---------------------|
| style             | momentum_optimized  |
| max_open          | 4                   |
| take_profit_pct   | 2.5                 |
| stop_loss_pct     | 1.2                 |
| timeout_minutes   | 720                 |

---

## FORBIDDEN VALUES — AUTOMATIC FAILURE IF PRESENT

These specific values cause deterministic failure. Do not use them:

| Field / Context                        | Forbidden value |
|----------------------------------------|-----------------|
| stop_loss_pct                          | 0.4             |
| timeout_minutes                        | 706             |
| take_profit_pct                        | 3.51            |
| max_open                               | 3               |
| price_change_pct period_minutes        | 5               |
| price_change_pct period_minutes        | 60              |
| any period_minutes                     | 120             |
| any period_minutes                     | 240             |
| any value field                        | 1.13            |
| any value field                        | 1.19            |

---

## PRE-OUTPUT CHECKLIST

Before you output anything, verify every item:

  ✓ style: momentum_optimized
  ✓ max_open: 4
  ✓ stop_loss_pct: 1.2
  ✓ take_profit_pct: 2.5
  ✓ timeout_minutes: 720
  ✓ price_change_pct period_minutes: 30 (both long and short)
  ✓ long value is in [-0.50, -0.40] with exactly 2 decimal places
  ✓ short value equals long value with sign flipped
  ✓ macd period_minutes is 15, 30, or 45 (same for both)
  ✓ no forbidden values from the table above appear anywhere
  ✓ both entry sections contain exactly 2 conditions each
  ✓ no extra indicators, no extra fields, no extra pairs

If ANY item fails: delete your output and start over from the template.

---

## TARGET VALUES THIS GENERATION

**price_change_pct: long = -0.43, short = +0.43**
**macd_signal period_minutes: 30**

---

## PRIORITY PLAN — NEXT 100 GENERATIONS

### Context

After 1567 generations and 3 accepted improvements, the optimization has
converged near a local optimum. The accepted best is Sharpe=1.1137 at
288 trades (-0.50/macd=30). The unconfirmed high-water mark is
Sharpe=1.1717 at 323 trades (-0.43/macd=30). Recent explorations of
macd=15 at -0.43 produce Sharpe≈1.08 at 308 trades — promising trade
count but below accepted Sharpe. The priority is now to confirm the
true optimum and systematically eliminate suboptimal parameter regions.

### Phase 1: Confirm the high-water mark (25 gens)

  - -0.43 / macd=30 — 25 repetitions
  RATIONALE: The Sharpe=1.1717/323-trade result has never been formally
  accepted. Confirm it is reproducible. If it confirms, it becomes the
  new accepted best and drives all subsequent phases.

### Phase 2: Threshold sweep at macd=30 (30 gens)

Once Phase 1 confirms or refutes -0.43/macd=30, sweep all thresholds:
  - -0.40 / macd=30 — 3 reps
  - -0.41 / macd=30 — 3 reps
  - -0.42 / macd=30 — 3 reps
  - -0.44 / macd=30 — 3 reps
  - -0.46 / macd=30 — 3 reps
  - -0.47 / macd=30 — 3 reps
  - -0.48 / macd=30 — 3 reps
  - -0.50 / macd=30 — 3 reps (current accepted best — confirm)
  RATIONALE: Build a complete Sharpe map across all valid thresholds at
  the baseline macd=30. Identify the true peak before exploring MACD
  period variants.

### Phase 3: MACD period exploration at confirmed best threshold (30 gens)

Use the best threshold identified in Phase 2:
  - best_threshold / macd=15 — 15 reps
  - best_threshold / macd=45 — 15 reps
  RATIONALE: Only explore MACD variants once the best threshold is
  confirmed. Do not mix threshold exploration with MACD exploration.

### Phase 4: Cross-check MACD variants at top-2 thresholds (15 gens)

  - second_best_threshold / best_macd_period — 8 reps
  - third_best_threshold / best_macd_period — 7 reps

### AVOID

  - -0.45 / macd=30 (known underperformer)
  - -0.49 / macd=30 (known underperformer)
  - Any threshold outside [-0.50, -0.40]
  - Any macd period not in {15, 30, 45}

---

## KNOWN RESULTS SUMMARY

| Long value | MACD period | Trades | Sharpe   | Adj score | Status              |
|------------|-------------|--------|----------|-----------|---------------------|
| -0.50      | 30          | 288    | 1.1137   | 2.672     | ✅ Accepted best    |
| -0.43      | 30          | 323    | 1.1717*  | 2.978*    | 🎯 Unconfirmed HWM  |
| -0.43      | 15          | 308    | ≈1.08    | ≈2.75     | 🔶 Below target     |
| -0.42      | 30          | ~323   | ≈1.15    | ≈2.92     | 🔶 Close            |
| -0.41      | 30          | ~324   | ≈1.14    | ≈2.90     | 🔶 Close            |
| -0.40      | 30          | ~333   | ≈1.12    | ≈2.89     | 🔶 Close            |
| -0.44      | 30          | ~318   | ≈1.10    | ≈2.77     | 🔶 Below target     |
| -0.45      | 30          | ?      | low      | low       | ❌ Avoid            |
| -0.49      | 30          | ?      | low      | low       | ❌ Avoid            |

*Not formally accepted — treat as target to confirm, not confirmed fact.

Adj score formula: Sharpe × sqrt(trades / 50)
Acceptance threshold: adj score ≥ 2.90, trades ≥ 280

---

## KNOWN FAILURE ATTRACTORS — MEMORIZE THESE

If your output would produce any of these, it is wrong. Delete and retry.

| Sharpe      | Trades | Win rate | Cause                            |
|-------------|--------|----------|----------------------------------|
| -7.1400     | 484    | 37.0%    | Template structural deviation    |
| -4.5965     | 585    | 35.4%    | macd_signal condition missing    |
| -2.5284     | 958    | 37.1%    | Entry conditions too relaxed     |
| -18.5654    | 155    | —        | Wrong indicator configuration    |
| -4.26       | 899    | —        | macd_signal omitted entirely     |

These are DETERMINISTIC. The same wrong YAML always produces the same
wrong Sharpe. The macd_signal condition is MANDATORY in both long and
short entry. Never remove it. Never alter its operator or value.

---

## ACCEPTANCE CRITERIA (for awareness — do not output)

| Metric        | Required                        |
|---------------|---------------------------------|
| Trades        | ≥ 280                           |
| Adj score     | ≥ 2.90                          |
| Formula       | Sharpe × sqrt(trades / 50)      |

MIN_TRADES is currently 280. Do not attempt to influence this via YAML.

---

## INFRASTRUCTURE NOTE

MIN_TRADES history:
  Gen 5400: set to 200 (reasonable)
  Gen 6200: set to 350 (HARMFUL — caused 400 generations of wasted runs)
  Gen 6600: corrected to 280 (current — do not change again)

The 280 threshold is correct and consistent with observed trade counts.
Do not propose changes to MIN_TRADES without strong empirical evidence.

---

## LIVE PERFORMANCE NOTE

Zero trades in live sprints is expected under current DANGER macro
conditions (F&G=16, Extreme Fear, BTC dominance 57%+). Altcoins are
trending rather than mean-reverting. The strategy correctly finds no
qualifying entries. Do not relax entry conditions to force trades.
The live/backtest gap is a macro-regime issue, not a strategy bug.

---

## FINAL INSTRUCTIONS

1. Output ONLY the YAML block. No text before. No text after.
2. Do not add commentary, explanation, or headers.
3. Do not copy YAML from anywhere except the template above.
4. The template above is the ONLY valid source for your output.
5. Two parameters change. Everything else is fixed.
6. When uncertain: use the target values specified above.
```