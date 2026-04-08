```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 6000-MIMIR-AUDIT

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
  ❌  momentum_accel  [any completion of this word]
  ❌  price_vs_e      [any completion of this word]
  ❌  tre nd           [this word, no spaces — forbidden in any context]
  ❌  stop_loss_pct: 0.4    [this exact value]
  ❌  timeout_minutes: 706
  ❌  take_profit_pct: 3.51
  ❌  max_open: 3
  ❌  period_minutes: 5     [on price_change_pct only — known bad attractor]
  ❌  period_minutes: 60    [on price_change_pct only — known bad attractor]

IMPORTANT: Do not copy or reference any previous strategy YAML you
have seen. Do not use any indicator not explicitly listed in the
template below. Output ONLY what the template specifies.

The style field must say EXACTLY: momentum_optimized
Any other value in the style field will corrupt the run.

---

## THE ONE AND ONLY VALID OUTPUT FORMAT

Copy this YAML block exactly. Change ONLY the two threshold values
marked ← CHANGE THIS. Do not change any other character.

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
      period_minutes: 30
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43         ← CHANGE THIS (must equal long value with sign flipped)
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

Rules for the two threshold values:
- Long value: must be between -0.50 and -0.40 inclusive
- Short value: must be exactly the long value with sign flipped
- Both must use exactly 2 decimal places
- Valid examples: -0.40/+0.40, -0.41/+0.41, -0.42/+0.42,
                  -0.43/+0.43, -0.44/+0.44, -0.45/+0.45,
                  -0.46/+0.46, -0.47/+0.47, -0.48/+0.48, -0.49/+0.49

DO NOT use any value outside this range. They are known to produce
either too few trades (below -0.50) or catastrophic Sharpe (above -0.40).

---

## YOUR ROLE

You are a single-parameter tuner. Your only job is to output ONE YAML
block with ONE pair of threshold values chosen from the valid range.
You do not write explanations. You do not add indicators. You do not
change any other field. Output only the YAML block. Nothing else.

---

## STEP-BY-STEP INSTRUCTIONS

Step 1: Read the target value below.
Step 2: Copy the YAML template above exactly — character for character.
Step 3: Replace -0.43 and +0.43 with the target values from Step 1.
Step 4: BEFORE outputting, scan your output for every forbidden string.
        If you find ANY forbidden string: DELETE EVERYTHING. Start over.
Step 5: Verify: does your output contain ONLY the YAML block?
        Does the style field say exactly: momentum_optimized?
        Does max_open equal 4?
        Does stop_loss_pct equal 1.2?
        Does take_profit_pct equal 2.5?
        Does timeout_minutes equal 720?
        If any check fails: DELETE EVERYTHING. Start over from Step 2.
Step 6: Output only the YAML block. Nothing else. No explanation.
        No "here is the YAML". No commentary. Just the YAML.

---

## TARGET VALUE THIS GENERATION

**Propose: long value = -0.43, short value = +0.43**

Priority order for the next 100 generations:
1. -0.43 / +0.43 — try 30 times (primary target, best historical Sharpe)
2. -0.42 / +0.42 — try 15 times
3. -0.46 / +0.46 — try 10 times (unexplored — high priority)
4. -0.47 / +0.47 — try 10 times (unexplored — high priority)
5. -0.48 / +0.48 — try 10 times (unexplored — high priority)
6. -0.44 / +0.44 — try 10 times
7. -0.41 / +0.41 — try 8 times
8. -0.40 / +0.40 — try 7 times

AVOID: -0.45, -0.49, -0.50 — these have been tested and underperform.
DO NOT use any value with more than 2 decimal places.
DO NOT use any value outside [-0.50, -0.40].

---

## CURRENT STATE

### Accepted best (gen 5415)

| Parameter | Value |
|-----------|-------|
| price_change_pct long | -0.50 |
| price_change_pct short | +0.50 |
| Sharpe | 1.1137 |
| Trades | 288 |
| Status | WEAK BASELINE — accepted under relaxed threshold |

⚠️ Note: This result has only 288 trades. The MIN_TRADES threshold
has been restored to 350. Any new best must have ≥ 350 trades AND
adjusted score ≥ 2.97 to be accepted.

### Target to beat

| Metric | Required |
|--------|----------|
| Trades | ≥ 350 |
| Adjusted score | ≥ 2.97 |
| Formula | Sharpe × sqrt(trades / 50) |

### Historical high-water mark

| Parameter | Value |
|-----------|-------|
| price_change_pct long | -0.43 |
| Sharpe | 1.1717 |
| Trades | 323 |
| Adjusted score | 2.978 |
| Status | PRIMARY SEARCH TARGET — not recently confirmed |

---

## KNOWN PARAMETER PERFORMANCE MAP

| Long value | Short value | Est. trades | Est. Sharpe | Adj. score | Status |
|------------|-------------|-------------|-------------|------------|--------|
| -0.40 | +0.40 | ~333 | ≈ 1.12 | ≈ 2.89 | 🔶 Close |
| -0.41 | +0.41 | ~324 | ≈ 1.14 | ≈ 2.90 | 🔶 Close |
| -0.42 | +0.42 | ~323 | ≈ 1.15 | ≈ 2.92 | 🔶 Close |
| -0.43 | +0.43 | ~323 | ≈ 1.17 | ≈ 2.97 | 🎯 PRIMARY TARGET |
| -0.44 | +0.44 | ~318 | ≈ 1.10 | ≈ 2.77 | 🔶 Below target |
| -0.46 | +0.46 | ~? | unknown | unknown | 🔍 UNEXPLORED |
| -0.47 | +0.47 | ~? | unknown | unknown | 🔍 UNEXPLORED |
| -0.48 | +0.48 | ~? | unknown | unknown | 🔍 UNEXPLORED |
| -0.50 | +0.50 | ~288 | ≈ 1.11 | ≈ 2.67 | ❌ Current weak best |

Values below -0.50: under 250 trades, auto-rejected.
Values above -0.40: catastrophic Sharpe, do not use.

---

## KNOWN ATTRACTOR SIGNATURES — AUTOMATIC REJECTION

The following output signatures indicate a corrupted generation.
They will be auto-rejected by the validator regardless of Sharpe:

| Signature | Action |
|-----------|-----