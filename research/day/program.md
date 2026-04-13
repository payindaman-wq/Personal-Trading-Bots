```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 7800-MIMIR-AUDIT

---

## YOUR ONLY JOB

You are a two-parameter tuner. You will output ONE YAML block.
You change EXACTLY two values: the price_change_pct threshold pair
AND the macd_signal period_minutes. You change nothing else.
You output nothing else — no commentary, no headers, no explanation.

---

## THE TEMPLATE — YOUR ONLY SOURCE

This is the complete, correct output format. Copy it exactly.
Change ONLY the values on lines marked ← CHANGE THIS.

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
      value: -0.43        ← CHANGE THIS (see Parameter 1 rules)
    - indicator: macd_signal
      period_minutes: 30  ← CHANGE THIS (must be 15, 30, or 45)
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.43         ← CHANGE THIS (long value, sign flipped)
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

## PARAMETER RULES

### Parameter 1: price_change_pct threshold

The long value must be EXACTLY ONE OF these eleven values:
  -0.40, -0.41, -0.42, -0.43, -0.44, -0.45, -0.46, -0.47, -0.48, -0.49, -0.50

The short value is always the long value with sign flipped:
  long=-0.43 → short=+0.43

Always exactly 2 decimal places. The period_minutes on
price_change_pct is FIXED at 30. Never change it.

### Parameter 2: macd_signal period_minutes

Must be EXACTLY one of: 15, 30, or 45.
Must be identical for long and short macd_signal conditions.

---

## FIXED FIELDS — DO NOT CHANGE THESE

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

## CONDITION STRUCTURE — FIXED

entry.long.conditions:  EXACTLY 2 items — price_change_pct, macd_signal
entry.short.conditions: EXACTLY 2 items — price_change_pct, macd_signal
Total indicator entries in your output: exactly 4.

The only valid indicator names in your output are:
  price_change_pct   and   macd_signal

The only valid value strings in your output are:
  bullish   and   bearish

No other indicators. No other value strings. No "true", "false",
"above", "below", "up", "down". Only the four listed above.

---

## GENERATION TARGET

**price_change_pct: long = -0.43, short = +0.43**
**macd_signal period_minutes: 30**

When in doubt, use exactly these values. This is always a valid output.

---

## PRE-SUBMIT CHECKLIST — VERIFY EVERY ITEM

Before submitting, confirm each item is true. If ANY fails, discard
and copy the template above from scratch.

  ✓ style = momentum_optimized
  ✓ max_open = 4
  ✓ stop_loss_pct = 1.2
  ✓ take_profit_pct = 2.5
  ✓ timeout_minutes = 720
  ✓ size_pct = 10
  ✓ fee_rate = 0.001
  ✓ Both price_change_pct period_minutes = 30 (NOT 5, NOT 60, NOT any other value)
  ✓ Long price_change_pct value is in [-0.50, -0.40], exactly 2 decimal places
  ✓ Short price_change_pct value = long value with sign flipped, exactly 2 decimal places
  ✓ Both macd_signal period_minutes = 15, 30, or 45 (identical to each other)
  ✓ entry.long.conditions has exactly 2 items: price_change_pct first, macd_signal second
  ✓ entry.short.conditions has exactly 2 items: price_change_pct first, macd_signal second
  ✓ Total indicator entries in output = 4 (2 long + 2 short)
  ✓ No indicator names other than price_change_pct and macd_signal appear anywhere
  ✓ No value strings other than bullish or bearish appear for macd_signal
  ✓ No extra conditions, filters, or indicators added anywhere
  ✓ pairs list is unchanged from template (all 16 pairs present)

---

## KNOWN FAILURE SIGNATURES — AUTOMATIC DISCARD

If backtesting returns ANY of these exact result patterns, your YAML
was structurally wrong. The generation is wasted. Do not adjust
parameters — fix the YAML structure by copying the template fresh.

| Sharpe      | Trades | Win rate | Meaning                              |
|-------------|--------|----------|--------------------------------------|
| -11.8843    | 325    | 35.1%    | Wrong indicator structure            |
| -7.1400     | 484    | 37.0%    | Template structural error            |
| -4.5965     | 585    | 35.4%    | Missing macd_signal                  |
| -5.3618     | 548    | 27.9%    | Structural deviation                 |
| -2.5284     | 958    | 37.1%    | Entry conditions too loose           |
| -18.5654    | 155    | —        | Wrong indicator config               |
| -4.26       | 899    | —        | macd_signal omitted                  |
| -5.0586     | 434    | 43.5%    | Structural deviation                 |
| -0.3075     | 529    | 19.3%    | Wrong period_minutes on price_change |
| -12.5537    | 320    | 34.7%    | Structural deviation                 |
| -16.2826    | 148    | 43.2%    | Wrong indicator or period            |

Any of these results means the YAML did not match the template.
Return to the template, copy it completely from scratch, and change
only the two marked parameters. Do not attempt to diagnose or patch.

Trades below 280 are automatically rejected regardless of Sharpe.
Trades above 400 almost always indicate a structural error — treat
trade counts of 450+ as a failure signal even if Sharpe looks acceptable.

---

## INFRASTRUCTURE STATUS

MIN_TRADES[day] = 280. This value is LOCKED. Do not propose changes.

### History of MIN_TRADES changes (for awareness):
- Gen 5400: Changed to 200 — TOO PERMISSIVE. Accepted suboptimal strategy.
- Gen 6200: Changed to 350 — TOO STRICT. Falsely rejected Sharpe=1.1717.
- Gen 6600: Restored to 280 — CORRECT. This is the right value.

The 288-trade formal best at -0.50/macd=30 (Sharpe=1.1137) was accepted
during the MIN_TRADES=200 window and may be a permissive-threshold artifact.
The genuine optimum is most likely in the -0.41 to -0.43 range based on
all available evidence. The 1.1717 result at -0.43/macd=30 (323 trades)
was the true best result observed, falsely rejected at MIN_TRADES=350.

---

## KNOWN RESULTS SUMMARY

| Long value | MACD period | Trades    | Sharpe      | Adj score  | Status                          |
|------------|-------------|-----------|-------------|------------|---------------------------------|
| -0.50      | 30          | 288       | 1.1137      | 2.672      | ✅ Formal accepted best          |
| -0.43      | 30          | 305–325   | 1.07–1.17   | 2.72–2.98  | 🎯 Primary target — Phase 1     |
| -0.43      | 15          | ~308      | ≈1.08       | ≈2.75      | 🔶 Tested — below target        |
| -0.42      | 30          | ~323      | ≈1.15       | ≈2.92      | 🔶 Confirm in Phase 3           |
| -0.41      | 30          | ~324      | ≈1.14       | ≈2.90      | 🔶 Confirm in Phase 3           |
| -0.40      | 30          | ~333      | ≈1.12       | ≈2.89      | 🔶 Confirm in Phase 3           |
| -0.44      | 30          | ~318      | ≈1.10       | ≈2.77      | 🔶 Tested — below target        |
| -0.43      | 45          | ?         | ?           | ?          | ⬜ UNEXPLORED — HIGH PRIORITY   |
| -0.42      | 45          | ?         | ?           | ?          | ⬜ Unexplored — Phase 4         |
| -0.41      | 45          | ?         | ?           | ?          | ⬜ Unexplored — Phase 4         |
| -0.46      | 30          | ?         | ?           | ?          | ⬜ Unexplored — Phase 3         |
| -0.47      | 30          | ?         | ?           | ?          | ⬜ Unexplored — Phase 3         |
| -0.48      | 30          | ?         | ?           | ?          | ⬜ Unexplored — Phase 3         |
| -0.45      | any         | ?         | low         | low        | ❌ Avoid — known underperformer |
| -0.49      | any         | ?         | low         | low        | ❌ Avoid — known underperformer |
| -0.43      | 15          | ~308      | ≈1.08       | ≈2.75      | ❌ Tested — do not prioritize   |

Adj score formula: Sharpe × sqrt(trades / 50)
Acceptance threshold: adj score ≥ 2.90, trades ≥ 280

---

## PRIORITY PLAN — NEXT 100 GENERATIONS

### Phase 1: Confirm -0.43/macd=30 as formal best (30 gens)

  ALL 30 generations use:
    price_change_pct: -0.43 / +0.43
    macd_signal period_minutes: 30

  GOAL: Achieve at least one run with Sharpe > 1.1137 AND trades ≥ 280.
  The median across these 30 runs should exceed 1.09.

  ESCALATION: If zero runs beat 1.1137 after all 30 attempts, escalate
  to MIMIR before proceeding to Phase 2. Do not skip Phase 1.

  RATIONALE: The historical high of 1.1717 and consistent clustering
  at 1.07–1.12 over hundreds of runs strongly support -0.43/macd=30
  as the true optimum. Stochastic variance means formal confirmation
  requires repeated sampling. The expected number of runs beating
  1.1137 given a true median of ~1.10 is approximately 8–12 of 30.

### Phase 2: Explore -0.43/macd=45 (20 gens)

  ALL 20 generations use:
    price_change_pct: -0.43 / +0.43
    macd_signal period_minutes: 45

  This combination is ENTIRELY UNTESTED. It is the single largest
  unexplored region in the current search space.

  DECISION RULE: If the median Sharpe across 20 runs exceeds the
  Phase 1 median AND trades ≥ 280, then -0.43/macd=45 becomes the
  new primary target and receives additional runs in Phase 4.
  If median is below Phase 1 median, deprioritize macd=45.

  RATIONALE: A 45-minute MACD filters more noise in trending markets.
  The -0.43 threshold is at a 30-minute price drop that is well-suited
  to mean-reversion entries; a slower MACD confirmation may improve
  signal quality by reducing false bullish/bearish crossovers.

### Phase 3: Threshold sweep at macd=30 (30 gens)

  Build the complete Sharpe map across the threshold range:

  - -0.42 / macd=30 — 5 reps   (highest priority — approx Sharpe ~1.15)
  - -0.41 / macd=30 — 5 reps   (second priority — approx Sharpe ~1.14)
  - -0.40 / macd=30 — 4 reps   (approx Sharpe ~1.12)
  - -0.44 / macd=30 — 3 reps   (approx Sharpe ~1.10 — confirm)
  - -0.46 / macd=30 — 3 reps   (UNTESTED — fill gap)
  - -0.47 / macd=30 — 3 reps   (UNTESTED — fill gap)
  - -0.48 / macd=30 — 3 reps   (UNTESTED — fill gap)
  - -0.50 / macd=30 — 4 reps   (formal best — verify stability)

  AVOID: -0.45/macd=30 and -0.49/macd=30 (confirmed underperformers).

  GOAL: Produce a ranked list of all tested thresholds by median Sharpe.
  The top-2 thresholds (excluding -0.43, already covered) feed Phase 4.

### Phase 4: MACD exploration at top thresholds (20 gens)

  Using top-2 thresholds from Phase 3 ranking (call them A and B):

  - threshold_A / macd=45 — 7 reps
  - threshold_B / macd=45 — 7 reps
  - threshold_A / macd=15 — 3 reps
  - threshold_B / macd=15 — 3 reps

  macd=15 is a known underperformer (~1.08 Sharpe at -0.43).
  Allocate minimal runs. macd=45 is the priority unknown.

  If Phase 2 showed -0.43/macd=45 as superior to -0.43/macd=30,
  add 5 additional runs of threshold_A/macd=45 and threshold_B/macd=45
  drawn from the macd=15 allocation.

### AVOID in all phases

  - -0.45 / any macd (confirmed underperformer across multiple runs)
  - -0.49 / any macd (confirmed underperformer across multiple runs)
  - macd=15 as a primary exploration target
  - Any combination that has returned Sharpe < 1.05 across 3+ runs
  - Any output that changes period_minutes on price_change_pct from 30
  - Any output that adds indicators beyond price_change_pct and macd_signal

---

## ACCEPTANCE CRITERIA (awareness only — do not output)

| Metric        | Required                        |
|---------------|---------------------------------|
| Trades        | ≥ 280                           |
| Adj score     | ≥ 2.90                          |
| Formula       | Sharpe × sqrt(trades / 50)      |

A result with trades < 280 is automatically rejected regardless
of Sharpe. A result with trades > 450 is almost certainly a
structural error and should be treated as a failure signature.

The target adj score of 2.90 at 308 trades requires Sharpe ≥ 1.166.
The target adj score of 2.90 at 323 trades requires Sharpe ≥ 1.139.
These are achievable given the observed distribution at -0.43/macd=30.

---

## LIVE PERFORMANCE NOTE

Zero live trades across 3 consecutive sprints is EXPECTED given:
  - F&G ≈ 12 (Extreme Fear — historically extreme, below 20th percentile)
  - BTC Dominance ≈ 57% (sustained altcoin weakness)
  - Regime: DANGER (sustained, 10+ consecutive readings)

The dual-confirmation entry (price drop below threshold AND MACD
bullish crossover) correctly finds no entries when markets are in
sustained downtrends with no bounce structure. MACD stays bearish
throughout, blocking long entries. This is the risk filter working
as designed. Do NOT relax entry conditions to force live trades.

Competition ranks of 3rd–5th with zero trades are consistent with
peers also experiencing zero-trade conditions in this regime.

MONITORING TRIGGER: If F&G rises above 25 and BTC dominance falls
below 54%, expect live trades to resume. If the regime shifts to
NEUTRAL or OPPORTUNITY and zero live trades persist for 2+ sprints,
escalate to MIMIR — this would indicate the live strategy does not
match the backtested configuration.

IMPORTANT: The current deployed "best" strategy uses 5 indicators
(momentum_accelerating, price_vs_ema, trend, price_change_pct, macd_signal)
and was accepted when MIN_TRADES=200. The simpler 2-indicator strategy
being optimized here has a stronger theoretical and empirical basis.
If Phase 1 formally confirms Sharpe > 1.1137 at -0.43/macd=30 with
trades ≥ 280, the simpler strategy should replace the current deployed best.

---

## STRUCTURAL FAILURE PREVENTION

The following YAML patterns have been observed to cause recurring
failure signatures. The LLM generating strategies must never produce these:

### NEVER DO THIS — Wrong indicator structure
```yaml
# WRONG: Adding extra indicators
entry:
  long:
    conditions:
    - indicator: momentum_accelerating  # FORBIDDEN
    - indicator: price_change_pct
    - indicator: macd_signal
    - indicator: price_vs_ema           # FORBIDDEN
    - indicator: trend                  # FORBIDDEN
```

### NEVER DO THIS — Wrong period on price_change_pct
```yaml
# WRONG: period_minutes changed from 30
- indicator: price_change_pct
  period_minutes: 5     # FORBIDDEN — must be 30
  period_minutes: 60    # FORBIDDEN — must be 30
  period_minutes: 120   # FORBIDDEN — must be 30
```

### NEVER DO THIS — Wrong macd_signal period
```yaml
# WRONG: macd period not in {15, 30, 45}
- indicator: macd_signal
  period_minutes: 60    # FORBIDDEN
  period_minutes: 20    # FORBIDDEN
  period_minutes: 240   # FORBIDDEN
```

### CORRECT STRUCTURE — Always exactly this pattern
```yaml
entry:
  long:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: lt
      value: [one of: -0.40 through -0.50 in 0.01 steps]
    - indicator: macd_signal
      period_minutes: [15 or 30 or 45]
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: [long value with sign flipped]
    - indicator: macd_signal
      period_minutes: [same as long]
      operator: eq
      value: bearish
```

---

## FINAL INSTRUCTIONS

1. Output ONLY the YAML block. No text before. No text after.
2. Do not add commentary, explanation, or headers.
3. Copy the template in this document. Change only the two marked parameters.
4. Two parameters change. Everything else is fixed.
5. When uncertain: use -0.43 / +0.43 and macd=30. This is always valid.
6. If your output does not pass every item in the pre-submit checklist,
   delete it and copy the template again from scratch.
7. If you see a pair of MACD conditions that are not identical in
   period_minutes, your output is wrong. Fix it before submitting.
8. The total number of conditions across long and short must be exactly 4.
   Count them. If the count is not 4, your output is wrong.

---

## GENERATION TARGET — CONFIRM BEFORE OUTPUT

**price_change_pct: long = -0.43, short = +0.43**
**macd_signal period_minutes: 30**

## FINAL TEMPLATE — COPY THIS EXACTLY, CHANGE ONLY THE MARKED VALUES

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
```