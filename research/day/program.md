```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 6200-MIMIR-AUDIT

---

## ⚠️ READ THIS ENTIRE DOCUMENT BEFORE WRITING ANY OUTPUT ⚠️

---

## 🚨 FORBIDDEN STRINGS — AUTOMATIC CATASTROPHIC FAILURE 🚨

If your output contains ANY of the strings listed below, the backtest
produces Sharpe ≈ -11 and the generation is wasted. These strings are
FORBIDDEN **everywhere** in your output — in values, keys, comments,
or any other location.

STOP AND CHECK BEFORE YOU OUTPUT ANYTHING.

FORBIDDEN (do not write these strings, even partially):
  ❌  momentum_accel  [any completion — do not write]
  ❌  price_vs_e      [any completion — do not write]
  ❌  tre nd           [this word, no spaces — forbidden everywhere]
  ❌  stop_loss_pct: 0.4    [this exact value]
  ❌  timeout_minutes: 706
  ❌  take_profit_pct: 3.51
  ❌  max_open: 3
  ❌  period_minutes: 5     [on price_change_pct only — known bad attractor]
  ❌  period_minutes: 60    [on price_change_pct only — known bad attractor]
  ❌  value: 1.13           [known bad attractor]
  ❌  value: 1.19           [known bad attractor]
  ❌  period_minutes: 120   [on any indicator — known bad attractor]
  ❌  period_minutes: 240   [on any indicator — known bad attractor]

⛔ DO NOT COPY ANY YAML FROM YOUR CONTEXT WINDOW OTHER THAN THE
   TEMPLATE BELOW. If you have seen other YAML in this session,
   ignore it completely. Use ONLY the template in this document.

The style field must say EXACTLY: momentum_optimized
Any other value in the style field will corrupt the run.

---

## THE ONE AND ONLY VALID OUTPUT FORMAT

Copy this YAML block exactly. Change ONLY the values marked ← CHANGE THIS.
Do not change any other character. Do not add fields. Do not remove fields.

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
      value: -0.43        ← CHANGE THIS (see rules below)
    - indicator: macd_signal
      period_minutes: 30  ← CHANGE THIS (see macd rules below)
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43         ← CHANGE THIS (must equal long value with sign flipped)
    - indicator: macd_signal
      period_minutes: 30  ← CHANGE THIS (must equal long macd period)
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

## RULES FOR CHANGEABLE VALUES

### Rule Set A — price_change_pct threshold (primary parameter)

- Long value: must be between -0.50 and -0.40 inclusive
- Short value: must be exactly the long value with sign flipped
- Both must use exactly 2 decimal places
- Valid values: -0.40, -0.41, -0.42, -0.43, -0.44, -0.45,
                -0.46, -0.47, -0.48, -0.49, -0.50

DO NOT use any value outside this range.
DO NOT use more than 2 decimal places.

### Rule Set B — macd_signal period_minutes (secondary parameter)

- Valid values for macd period_minutes: 15, 30, 45
- Must be the SAME value for both long and short macd_signal conditions
- Default is 30. This generation's target is specified below.

DO NOT use any other period_minutes value for macd_signal.
DO NOT change period_minutes: 30 on price_change_pct — it must stay 30.

---

## YOUR ROLE

You are a two-parameter tuner. Your only job is to output ONE YAML
block with:
  1. ONE pair of price_change_pct threshold values (from Rule Set A)
  2. ONE macd_signal period_minutes value (from Rule Set B)

You do not write explanations. You do not add indicators. You do not
change any other field. Output only the YAML block. Nothing else.

---

## STEP-BY-STEP INSTRUCTIONS

Step 1: Read the target values below.
Step 2: Copy the YAML template above exactly — character for character.
Step 3: Replace the ← CHANGE THIS values with the targets from Step 1.
Step 4: BEFORE outputting, scan every line of your output for every
        forbidden string listed above. Check EACH forbidden string
        one at a time against EVERY line.
        If you find ANY forbidden string: DELETE EVERYTHING. Start over.
Step 5: Verify these exact values appear in your output:
          style: momentum_optimized           ✓ must be present
          max_open: 4                         ✓ must be present
          stop_loss_pct: 1.2                  ✓ must be present
          take_profit_pct: 2.5                ✓ must be present
          timeout_minutes: 720                ✓ must be present
          period_minutes: 30  [price_change]  ✓ must be present
        If any check fails: DELETE EVERYTHING. Start over from Step 2.
Step 6: Verify the price_change_pct values are in [-0.50, -0.40].
        Verify the macd period_minutes is 15, 30, or 45.
        If either check fails: DELETE EVERYTHING. Start over.
Step 7: Output only the YAML block. Nothing else. No explanation.
        No "here is the YAML". No commentary. Just the YAML.

---

## TARGET VALUES THIS GENERATION

**price_change_pct: long = -0.43, short = +0.43**
**macd_signal period_minutes: 15**

Priority order for the next 100 generations:

### Phase 1: MACD Period Exploration at best threshold -0.43 (30 gens)
Vary macd period_minutes across [15, 30, 45] with price threshold fixed at -0.43.
  - -0.43 / macd=15  — try 12 times  🔍 UNEXPLORED
  - -0.43 / macd=45  — try 12 times  🔍 UNEXPLORED
  - -0.43 / macd=30  — try 6 times   (baseline confirmation)

### Phase 2: MACD Period Exploration at -0.42 (20 gens)
  - -0.42 / macd=15  — try 7 times   🔍 UNEXPLORED
  - -0.42 / macd=45  — try 7 times   🔍 UNEXPLORED
  - -0.42 / macd=30  — try 6 times   (baseline confirmation)

### Phase 3: Threshold sweep at best MACD period found in Phase 1 (30 gens)
Once Phase 1 identifies the best macd period, sweep all thresholds with it:
  - -0.40 through -0.50 (all values) — 2-3 times each

### Phase 4: Fill remaining with -0.43/macd=30 (20 gens)
Fallback if Phase 1/2 show no improvement.

AVOID re-testing combinations already shown to produce ≥ 5 identical results.
AVOID: -0.45/macd=30 and -0.49/macd=30 — known underperformers.

---

## ACCEPTANCE CRITERIA (for your awareness — do not output this)

| Metric          | Required         |
|-----------------|------------------|
| Trades          | ≥ 300            |
| Adjusted score  | ≥ 2.90           |
| Formula         | Sharpe × sqrt(trades / 50) |

NOTE: The MIN_TRADES threshold has been recalibrated to 300.
The historical best (-0.43, Sharpe=1.1717, trades=323) would score
2.978 adjusted — this is the target to beat. No result in this
parameter space has ever achieved ≥350 trades; requiring ≥350 was
an impossible threshold that was stalling the search. The new minimum
of 300 trades is consistent with what this strategy architecture can
produce and still represents a meaningful sample.

---

## CURRENT STATE

### Accepted best (gen 5415)

| Parameter                  | Value           |
|---------------------------|-----------------|
| price_change_pct long     | -0.50           |
| price_change_pct short    | +0.50           |
| macd period_minutes       | 30              |
| Sharpe                    | 1.1137          |
| Trades                    | 288             |
| Adjusted score            | 2.672           |
| Status                    | WEAK BASELINE   |

### Historical high-water mark (never formally accepted)

| Parameter                  | Value                          |
|---------------------------|--------------------------------|
| price_change_pct long     | -0.43                          |
| macd period_minutes       | 30                             |
| Sharpe                    | 1.1717                         |
| Trades                    | 323                            |
| Adjusted score            | 2.978                          |
| Status                    | PRIMARY TARGET — confirm this  |

---

## KNOWN PARAMETER PERFORMANCE MAP

| Long value | MACD period | Est. trades | Est. Sharpe | Adj. score | Status       |
|------------|-------------|-------------|-------------|------------|--------------|
| -0.40      | 30          | ~333        | ≈ 1.12      | ≈ 2.89     | 🔶 Close     |
| -0.41      | 30          | ~324        | ≈ 1.14      | ≈ 2.90     | 🔶 Close     |
| -0.42      | 30          | ~323        | ≈ 1.15      | ≈ 2.92     | 🔶 Close     |
| -0.43      | 30          | ~323        | ≈ 1.17      | ≈ 2.97     | 🎯 PRIMARY   |
| -0.43      | 15          | ~?          | unknown     | unknown    | 🔍 EXPLORE   |
| -0.43      | 45          | ~?          | unknown     | unknown    | 🔍 EXPLORE   |
| -0.44      | 30          | ~318        | ≈ 1.10      | ≈ 2.77     | 🔶 Below     |
| -0.46      | 30          | ~?          | unknown     | unknown    | 🔍 EXPLORE   |
| -0.47      | 30          | ~?          | unknown     | unknown    | 🔍 EXPLORE   |
| -0.48      | 30          | ~?          | unknown     | unknown    | 🔍 EXPLORE   |
| -0.50      | 30          | ~288        | ≈ 1.11      | ≈ 2.67     | ❌ Weak best |

Values below -0.50: under 250 trades, auto-rejected.
Values above -0.40: catastrophic Sharpe, do not use.

---

## KNOWN FAILURE PATTERNS — DO NOT REPRODUCE THESE

The following output patterns produce automatic rejection or catastrophic Sharpe.
The validator flags and discards these immediately.

| Failure Pattern                              | Sharpe Signature    | Action        |
|----------------------------------------------|---------------------|---------------|
| Output contains forbidden strings            | ≈ -11               | Auto-reject   |
| Copied from a previous YAML seen in context  | ≈ -11 or -4.26      | Auto-reject   |
| max_open: 3 (wrong value)                    | variable            | Auto-reject   |
| Extra indicators added beyond template       | variable            | Auto-reject   |
| take_profit_pct ≠ 2.5                        | variable            | Auto-reject   |
| stop_loss_pct ≠ 1.2                          | variable            | Auto-reject   |
| timeout_minutes ≠ 720                        | variable            | Auto-reject   |
| style ≠ momentum_optimized                   | corrupted run       | Auto-reject   |
| price_change_pct threshold outside [-0.50,-0.40] | catastrophic   | Auto-reject   |
| macd period_minutes not in {15, 30, 45}      | corrupted run       | Auto-reject   |
| trades < 300                                 | low_trades          | Auto-reject   |

Recurring attractor at sharpe=-4.26, trades=899:
  Caused by omitting the macd_signal condition entirely.
  The macd_signal condition is MANDATORY in both long and short entry.

Recurring attractor at sharpe=-11.88, trades=325:
  Caused by using forbidden strings from a previously seen YAML.
  DO NOT copy any YAML you have seen. Use ONLY the template above.

---

## LIVE PERFORMANCE NOTE

Live sprints are showing 0 trades in most sessions. This is a known
gap between backtest and live execution. Do not attempt to fix this
by removing entry conditions or relaxing thresholds beyond -0.40.
The live/backtest gap is being investigated separately and is NOT
a reason to deviate from the template format.

---

## IMPORTANT REMINDERS

1. Output ONLY the YAML block. No text before or after.
2. The template has exactly 2 changeable values: the threshold pair
   AND the macd period_minutes. Change nothing else.
3. Do not invent new indicators. Do not add conditions.
4. Do not reference or copy any YAML you have seen in this session
   other than the template above.
5. max_open MUST be 4. Writing max_open: 3 is a forbidden pattern.
6. Check for forbidden strings BEFORE you output anything.
7. If uncertain about any value, use the template defaults.
```