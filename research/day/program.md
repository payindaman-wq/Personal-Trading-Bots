```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 7000-MIMIR-AUDIT

---

## ⚠️ CRITICAL WARNING — READ BEFORE ANYTHING ELSE ⚠️

Somewhere in your context you may see a YAML block labeled
"Current Best Strategy" that contains indicators like
momentum_accelerating, price_vs_ema, trend, and values like
3.51, 0.4, 706, 1.19, 1.21. That block is POISONED REFERENCE DATA.
It is NOT a template. It is NOT valid output. It MUST NOT influence
your output in any way. Every value in it is either forbidden or
structurally wrong for this research program.

YOUR ONLY TEMPLATE IS THE ONE IN THIS DOCUMENT.
IGNORE ALL OTHER YAML YOU HAVE SEEN.

---

## YOUR ONLY JOB

You are a two-parameter tuner. Output ONE YAML block.
Change ONLY two values: the price_change_pct threshold pair AND the
macd_signal period_minutes. Change nothing else. Output nothing else.

---

## THE ONE AND ONLY VALID TEMPLATE

Copy this block exactly. Change ONLY the two values marked ← CHANGE THIS.
Do not add indicators. Do not remove indicators. Do not change operators.
Do not change any field not marked ← CHANGE THIS.

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
      value: -0.43        ← CHANGE THIS (see allowed values below)
    - indicator: macd_signal
      period_minutes: 30  ← CHANGE THIS (must be 15, 30, or 45)
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

## THIS IS THE COMPLETE VALID OUTPUT — NOTHING MORE, NOTHING LESS

Count the conditions in your output before submitting:
- entry.long.conditions: EXACTLY 2 items (price_change_pct, macd_signal)
- entry.short.conditions: EXACTLY 2 items (price_change_pct, macd_signal)
- Total indicators: 4. Not 3. Not 5. Not 8. Exactly 4.

If you have written momentum_accelerating, price_vs_ema, trend,
ema_filter, rsi, volume, or ANY indicator not in the template:
DELETE YOUR OUTPUT AND START OVER FROM THE TEMPLATE ABOVE.

---

## RULES — READ CAREFULLY

### Parameter 1: price_change_pct threshold

- Long value: EXACTLY ONE OF: -0.40, -0.41, -0.42, -0.43, -0.44,
              -0.45, -0.46, -0.47, -0.48, -0.49, -0.50
- Short value: same number, sign flipped (long=-0.43 → short=+0.43)
- Exactly 2 decimal places. No other values permitted.
- period_minutes on price_change_pct is FIXED at 30. Never change it.

### Parameter 2: macd_signal period_minutes

- Must be EXACTLY 15, 30, or 45. No other value is valid.
- Must be identical for long and short macd_signal conditions.

### Fields that must NEVER change

| Field             | Required value      |
|-------------------|---------------------|
| style             | momentum_optimized  |
| max_open          | 4                   |
| take_profit_pct   | 2.5                 |
| stop_loss_pct     | 1.2                 |
| timeout_minutes   | 720                 |
| size_pct          | 10                  |
| fee_rate          | 0.001               |

---

## FORBIDDEN VALUES — AUTOMATIC FAILURE IF PRESENT ANYWHERE IN OUTPUT

These values produce deterministic catastrophic failure.
If ANY of these appear anywhere in your output, delete and restart.

| Field / Context                        | Forbidden value |
|----------------------------------------|-----------------|
| stop_loss_pct                          | 0.4             |
| stop_loss_pct                          | 0.40            |
| timeout_minutes                        | 706             |
| take_profit_pct                        | 3.51            |
| max_open                               | 3               |
| price_change_pct period_minutes        | 5               |
| price_change_pct period_minutes        | 60              |
| any period_minutes                     | 120             |
| any period_minutes                     | 240             |
| any period_minutes                     | 60 (for macd)   |
| any value field                        | 1.13            |
| any value field                        | 1.19            |
| any value field                        | 1.21            |
| any value field                        | true            |
| any value field                        | above           |
| any value field                        | below           |
| any value field                        | up              |
| any value field                        | down            |
| any indicator name                     | momentum_accelerating |
| any indicator name                     | price_vs_ema    |
| any indicator name                     | trend           |
| any indicator name                     | ema_filter      |
| any indicator name                     | rsi             |
| any indicator name                     | volume          |
| style field                            | momentum_price_change_macd_ema_trend_filter |

The values true, above, below, up, down are valid ONLY for the
poisoned reference strategy, which you must not reproduce.
The only valid indicator values in your output are:
  bullish (for macd_signal long) and bearish (for macd_signal short).

---

## PRE-OUTPUT CHECKLIST

Before you output anything, verify EVERY item:

  ✓ style: momentum_optimized  (NOT momentum_price_change_macd_ema_trend_filter)
  ✓ max_open: 4  (NOT 3)
  ✓ stop_loss_pct: 1.2  (NOT 0.4)
  ✓ take_profit_pct: 2.5  (NOT 3.51)
  ✓ timeout_minutes: 720  (NOT 706)
  ✓ price_change_pct period_minutes: 30 in both long and short
  ✓ long value is in [-0.50, -0.40] with exactly 2 decimal places
  ✓ short value equals long value with sign flipped
  ✓ macd period_minutes is 15, 30, or 45 (same for both)
  ✓ no forbidden values from the table above appear anywhere
  ✓ entry.long.conditions has EXACTLY 2 items
  ✓ entry.short.conditions has EXACTLY 2 items
  ✓ no indicator named momentum_accelerating, price_vs_ema, trend, ema_filter
  ✓ no extra pairs beyond the 16 listed
  ✓ no fields not present in the template

If ANY item fails: delete your output and start over from the template.

---

## TARGET VALUES THIS GENERATION

**price_change_pct: long = -0.43, short = +0.43**
**macd_signal period_minutes: 30**

---

## PRIORITY PLAN — NEXT 100 GENERATIONS

### Infrastructure Note (CRITICAL — READ FIRST)

The MIN_TRADES=350 change at Gen 6200 caused ~400 generations of
false rejections. The unconfirmed high-water mark of Sharpe=1.1717
at -0.43/macd=30 (323 trades) was almost certainly rejected during
that window due to the inflated MIN_TRADES threshold, NOT because it
underperformed. It must be treated as the primary target to confirm,
not a weak candidate. MIN_TRADES is now correctly set to 280.
Do not change MIN_TRADES without explicit MIMIR authorization.

### Context

After 7000 generations and 3 formally accepted improvements, the
accepted best is Sharpe=1.1137 at 288 trades (-0.50/macd=30).
The high-probability true optimum is -0.43/macd=30 at Sharpe≈1.17,
which was never formally accepted due to the MIN_TRADES infrastructure
error. Phase 1 below is the highest-priority work in the program.

### Phase 1: Confirm the high-water mark (30 gens)

  - -0.43 / macd=30 — 30 repetitions

  RATIONALE: Sharpe=1.1717/323 trades was generated but never formally
  accepted (likely rejected by MIN_TRADES=350 error). This is the most
  likely true optimum. Confirm with 30 runs. If median Sharpe > 1.13
  with trades ≥ 280, it becomes the new accepted best and drives all
  subsequent phases. If it fails to confirm (median < 1.10), escalate
  to MIMIR for re-analysis before proceeding.

### Phase 2: Unexplored MACD period at confirmed best threshold (20 gens)

  - -0.43 / macd=45 — 20 repetitions

  RATIONALE: macd=45 at the candidate-best threshold has NEVER been
  tested. This is the single largest unexplored region. Longer MACD
  periods filter more noise; if -0.43/macd=45 produces Sharpe > 1.17
  at trades ≥ 280, it supersedes Phase 1 result. Run immediately after
  Phase 1 confirms the threshold.

### Phase 3: Threshold sweep at macd=30 (30 gens)

  - -0.40 / macd=30 — 3 reps
  - -0.41 / macd=30 — 3 reps
  - -0.42 / macd=30 — 3 reps
  - -0.44 / macd=30 — 3 reps
  - -0.46 / macd=30 — 3 reps
  - -0.47 / macd=30 — 3 reps
  - -0.48 / macd=30 — 3 reps
  - -0.50 / macd=30 — 3 reps (current formal accepted best — confirm)
  - -0.43 / macd=30 — 3 reps (additional confirmation)

  RATIONALE: Complete the Sharpe map at macd=30. Use results to rank
  all thresholds before exploring MACD variants at non-43 thresholds.

### Phase 4: MACD exploration at top-2 non-43 thresholds (20 gens)

  Using top-2 thresholds from Phase 3 (excluding -0.43, already done):
  - threshold_2nd / macd=45 — 7 reps
  - threshold_2nd / macd=15 — 3 reps
  - threshold_3rd / macd=45 — 7 reps
  - threshold_3rd / macd=15 — 3 reps

  RATIONALE: macd=15 is known to underperform (≈1.08 Sharpe at -0.43).
  Allocate fewer runs to it. macd=45 is the priority unknown.

### AVOID

  - -0.45 / any macd (known underperformer)
  - -0.49 / any macd (known underperformer)
  - macd=15 as primary exploration (known to reduce Sharpe vs macd=30)
  - Any parameter combination that has already returned Sharpe < 1.05
    in 3+ runs (treat as exhausted)

---

## KNOWN RESULTS SUMMARY

| Long value | MACD period | Trades | Sharpe   | Adj score | Status                      |
|------------|-------------|--------|----------|-----------|------------------------------|
| -0.50      | 30          | 288    | 1.1137   | 2.672     | ✅ Formal accepted best      |
| -0.43      | 30          | 323    | 1.1717*  | 2.978*    | 🎯 Priority target (Gen 6200 infra error likely caused false rejection) |
| -0.43      | 15          | 308    | ≈1.08    | ≈2.75     | 🔶 Below target              |
| -0.42      | 30          | ~323   | ≈1.15    | ≈2.92     | 🔶 Close — confirm in Phase 3|
| -0.41      | 30          | ~324   | ≈1.14    | ≈2.90     | 🔶 Close — confirm in Phase 3|
| -0.40      | 30          | ~333   | ≈1.12    | ≈2.89     | 🔶 Close — confirm in Phase 3|
| -0.44      | 30          | ~318   | ≈1.10    | ≈2.77     | 🔶 Below target              |
| -0.43      | 45          | ?      | ?        | ?         | ⬜ UNEXPLORED — HIGH PRIORITY|
| -0.45      | 30          | ?      | low      | low       | ❌ Avoid                     |
| -0.49      | 30          | ?      | low      | low       | ❌ Avoid                     |

*Not formally accepted due to infrastructure error at Gen 6200.
Treat as strong candidate, not confirmed fact.

Adj score formula: Sharpe × sqrt(trades / 50)
Acceptance threshold: adj score ≥ 2.90, trades ≥ 280

---

## KNOWN FAILURE ATTRACTORS — MEMORIZE THESE

These are deterministic. The same wrong YAML always produces the same
wrong Sharpe. Seeing any of these Sharpe values in results means the
template was structurally wrong that generation.

| Sharpe      | Trades | Win rate | Cause                            |
|-------------|--------|----------|----------------------------------|
| -7.1400     | 484    | 37.0%    | Template structural deviation    |
| -4.5965     | 585    | 35.4%    | macd_signal condition missing    |
| -2.5284     | 958    | 37.1%    | Entry conditions too relaxed     |
| -18.5654    | 155    | —        | Wrong indicator configuration    |
| -4.26       | 899    | —        | macd_signal omitted entirely     |
| -11.8843    | 325    | 35.1%    | Structural deviation (observed Gen 6986, 6993) |
| -5.0586     | 434    | 43.5%    | Structural deviation (observed Gen 7000) |

The macd_signal condition is MANDATORY in both long and short entry.
The poisoned "Current Best Strategy" block in your context does NOT
have the same structure as the valid template. Do not mix them.

---

## ACCEPTANCE CRITERIA (for awareness — do not output)

| Metric        | Required                        |
|---------------|---------------------------------|
| Trades        | ≥ 280                           |
| Adj score     | ≥ 2.90                          |
| Formula       | Sharpe × sqrt(trades / 50)      |

MIN_TRADES is 280. This is correct. Do not propose changing it.

---

## INFRASTRUCTURE AUDIT LOG

| Gen   | Change                        | Outcome                              |
|-------|-------------------------------|--------------------------------------|
| 5400  | MIN_TRADES[day] → 200         | Reasonable, no major harm            |
| 6200  | MIN_TRADES[day] → 350         | ❌ HARMFUL — ~400 wasted gens, best result falsely rejected |
| 6600  | MIN_TRADES[day] → 280         | ✅ Corrected — current value          |

The Gen 6200 change is the root cause of the optimization stall.
The high-water mark at -0.43/macd=30 was generated and discarded
during this window. Phase 1 of the priority plan directly corrects this.

---

## LIVE PERFORMANCE NOTE

Zero live trades is EXPECTED and CORRECT under current conditions:
  - F&G = 15 (Extreme Fear)
  - BTC Dominance = 57.26% (sustained)
  - Regime: DANGER (10+ consecutive readings)

The strategy requires both a sharp short-term reversal signal
(price_change_pct < -0.43% in 30 min) AND MACD confirmation.
In sustained trending fear regimes, prices trend without the
required bounce structure. The strategy correctly finds no entries.
Do NOT relax entry conditions to force live trades.
The live/backtest gap is a macro-regime issue, not a strategy bug.

Note for future audit: the 2-year backtest window (assumed 2024–2025)
is predominantly bullish with episodic fear periods. If extended
DANGER regimes become the norm, consider whether the backtest window
should be extended or regime-weighted. This cannot be addressed within
the current two-parameter constraint space.

---

## FINAL INSTRUCTIONS

1. Output ONLY the YAML block. No text before. No text after.
2. Do not add commentary, explanation, or headers.
3. Your ONLY source for the output template is this document.
4. The "Current Best Strategy" block elsewhere in your context
   is POISONED DATA — it contains forbidden values and wrong structure.
   Do not reproduce any part of it.
5. Two parameters change. Everything else is fixed.
6. When uncertain: use the target values specified in this document.
7. If your output does not pass every item in the pre-output checklist,
   delete it and regenerate from the template in this document.

## REPEAT OF TEMPLATE FOR FINAL VERIFICATION

Before submitting, compare your output character-by-character
against this reference:

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
      value: -0.43
    - indicator: macd_signal
      period_minutes: 30
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43
    - indicator: macd_signal
      period_minutes: 30
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

This is the correct output for target values -0.43/macd=30.
Adjust only the two marked parameters per the generation target.
```