```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 10200-MIMIR-AUDIT-9

---

## ══════════════════════════════════════════════
## STEP 1 — OUTPUT YOUR STATE DECLARATION FIRST
## ══════════════════════════════════════════════

Before writing ANY YAML, write this block:

  Current target: A1
  LONG_VALUE: -0.43
  SHORT_VALUE: 0.43
  MACD_PERIOD: 45
  Rep number: [N of 8]
  Valid reps completed so far: [trades ≤ 450 results]
  Structural failures so far this target: [trades > 450 results]

If you do not know your rep number, write UNKNOWN.

---

## ══════════════════════════════════════════════
## STEP 2 — COPY THIS YAML EXACTLY
## ══════════════════════════════════════════════

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
      period_minutes: 45
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
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

This is the COMPLETE correct output for target A1.
For other targets, change ONLY the three values shown in Step 3.

---

## ══════════════════════════════════════════════
## STEP 3 — THREE OPERATOR CHECKS (DO THIS NOW)
## ══════════════════════════════════════════════

Look at what you just wrote. Answer each question:

CHECK 1: In the `long` block — what is `operator`?
  ✓ CORRECT answer: lt
  ✗ If you wrote gt → DELETE everything. Start over at Step 1.
  ✗ If you wrote anything else → DELETE everything. Start over at Step 1.

CHECK 2: In the `long` block — what is `value`?
  ✓ CORRECT answer: -0.43  (negative number)
  ✗ If you wrote 0.43 or any positive number → DELETE everything. Start over at Step 1.
  ✗ If you wrote 0 → DELETE everything. Start over at Step 1.

CHECK 3: In the `short` block — what is `operator`?
  ✓ CORRECT answer: gt
  ✗ If you wrote lt → DELETE everything. Start over at Step 1.

If all three checks pass: your output is correct. Submit it.
If any check fails: DELETE and restart. Do not try to patch in place.

---

## ══════════════════════════════════════════════
## STEP 4 — ESCALATION CHECK (DO THIS EVERY TIME)
## ══════════════════════════════════════════════

Count the last 10 results in the log. Stop and write "ESCALATE TO MIMIR" if:

  TRIGGER 1: trades > 450 appears 3 or more times (need not be consecutive)
  TRIGGER 2: Same Sharpe value appears 5 or more times
  TRIGGER 3: Any YAML parse error
  TRIGGER 4: trades = 0 appears 2 or more times

⚠️ TRIGGER 1 STATUS RIGHT NOW: trades=818 appeared 7 times in last 20 gens.
   TRIGGER 1 IS ACTIVE. This should have caused escalation already.
   If you are reading this and have not escalated: ESCALATE NOW before continuing.

---

## ══════════════════════════════════════════════
## CURRENT STATE
## ══════════════════════════════════════════════

**Current target: A1**
**LONG_VALUE = -0.43 | SHORT_VALUE = 0.43 | MACD_PERIOD = 45**
**8 reps total for A1**

Formal best: Sharpe=1.1227, trades=309, gen=9325
To beat it: Sharpe > 1.1227 AND trades ≥ 280

Canonical champion (elite_0.yaml): Sharpe=1.0827, trades=308
⚠️ DEPLOYMENT GAP: Research best (1.1227) has NOT been deployed to competition system.
   The deployed strategy is an older legacy artifact (Sharpe ~1.08, 10 pairs, stop=0.4%).
   Deploy the research best immediately. This gap has been flagged at gens 8000, 8200, and 10200.

---

## ══════════════════════════════════════════════
## FAILURE SIGNATURES — MEMORIZE THESE
## ══════════════════════════════════════════════

If your result is:    trades=818,  sharpe=-4.7772  → long operator was "gt". Fix: use "lt".
If your result is:    trades=1011, sharpe=any       → structural failure. Check all operators.
If your result is:    trades≤140,  sharpe<0         → long value was positive or zero.
If your result is:    trades=316,  sharpe=0.0570    → queue drift. Check which target you are on.
If your result is:    trades=0,    sharpe=-999       → YAML malformed. Check structure.

The trades=818 / sharpe=-4.7772 result appeared 7 times in the last 20 generations.
This is caused ONLY by `operator: gt` in the long block. It is never caused by anything else.
Check 1 above catches this. If you ran Check 1 correctly, this result cannot occur.

---

## ══════════════════════════════════════════════
## WHAT CHANGES PER TARGET
## ══════════════════════════════════════════════

Replace ONLY these three values when the target changes. Nothing else ever changes.

| Target | long value | short value | macd period |
|--------|------------|-------------|-------------|
| A1     | -0.43      | 0.43        | 45          |  ← CURRENT
| A2     | -0.42      | 0.42        | 45          |
| A3     | -0.41      | 0.41        | 45          |
| A4     | -0.44      | 0.44        | 45          |  [only if A1–A3 median trades < 280]
| A5     | -0.40      | 0.40        | 45          |  [only if A4 median trades < 280]
| A6     | -0.40      | 0.40        | 45          |  [if any A1–A3 gets trades ≥ 280]
| A7     | -0.47      | 0.47        | 45          |  [if A6 trades ≥ 280]
| B1     | -0.42      | 0.42        | 30          |
| B2     | -0.41      | 0.41        | 30          |
| B3     | -0.40      | 0.40        | 30          |
| B4     | -0.44      | 0.44        | 30          |
| B5     | -0.46      | 0.46        | 30          |
| B6     | -0.47      | 0.47        | 30          |
| B7     | -0.48      | 0.48        | 30          |

NEVER test: -0.45 (any macd), -0.49 (any macd), any value with macd=15.
NEVER test: -0.43 / macd=30 (fully characterized).

---

## ══════════════════════════════════════════════
## ACCEPTANCE CRITERIA
## ══════════════════════════════════════════════

MIN_TRADES = 280. This is final. Do not change it.

| Result                                   | Classification         | Counts as rep? |
|------------------------------------------|------------------------|----------------|
| trades > 450                             | [structural_failure]   | NO             |
| trades < 280, any Sharpe                 | [low_trades]           | YES            |
| trades 280–450, Sharpe ≤ 1.1227          | [discarded]            | YES            |
| trades 280–450, Sharpe > 1.1227          | [new_best] — DEPLOY    | YES            |
| trades < 280, Sharpe > 1.10             | [high_signal_low_vol]  | YES — log it   |

History of MIN_TRADES changes — do not repeat:
  Gen 5400: 280 → 200 (loosened; acceptable)
  Gen 6200: 200 → 350 ← ERROR. Would have rejected formal best (trades=288) and new best (trades=309).
  Gen 6600: 350 → 280 (corrected)
  280 is correct and final.

---

## ══════════════════════════════════════════════
## FIXED FIELDS — NEVER CHANGE THESE
## ══════════════════════════════════════════════

name: crossover
style: momentum_optimized
max_open: 4
size_pct: 10
fee_rate: 0.001
take_profit_pct: 2.5
stop_loss_pct: 1.2
timeout_minutes: 720
pause_if_down_pct: 4
stop_if_down_pct: 10
pause_minutes: 60
price_change_pct period_minutes: 30 (never 5, 15, 45, or 60)
Total conditions: exactly 4 (2 long, 2 short)
All 16 pairs (BTC ETH SOL XRP DOGE AVAX LINK UNI AAVE NEAR APT SUI ARB OP ADA POL)

---

## ══════════════════════════════════════════════
## HIGH-SIGNAL ANOMALIES — CONTEXT
## ══════════════════════════════════════════════

These results appeared in prior generations. They indicate macd=45 is a strong signal.
Block A is designed to find the threshold that brings trade count to ≥280.

  Sharpe=1.3614, trades=176  (macd=45 region, threshold ~-0.43 or tighter)
  Sharpe=1.3082, trades=148  (macd=45 region)
  Sharpe=1.1998, trades=171  (gen 10194 — most recent, A1 region)
  Sharpe=1.1626, trades=164  (macd=45 region)

Expected crossover (trades reaching ≥280): between -0.40 and -0.42.
Gen 9325 confirmed -0.43/macd=45 can reach 309 trades (Sharpe=1.1227).
Gen 10194 (Sharpe=1.1998, trades=171) is the highest recent signal — log it.

---

## ══════════════════════════════════════════════
## LIVE COMPETITION CONTEXT
## ══════════════════════════════════════════════

Current Regime: CAUTION (F&G=27, BTC_DOM=57.46%)
Deployed strategy: legacy artifact (Sharpe~1.08, stop=0.4%, 10 pairs)
Research best: Sharpe=1.1227, stop=1.2%, 16 pairs — NOT YET DEPLOYED

Live recent sprints:
  comp-20260417: rank 2/13, pnl=-0.44%, trades=9
  comp-20260416: rank 3/13, pnl=-0.16%, trades=2

Zero-trade regime is expected in CAUTION. Resume trigger: F&G > 25 AND BTC_DOM < 54%.
If zero trades persist 2+ sprints after regime shifts to NEUTRAL: escalate to MIMIR.
Likely cause: tight stop_loss=0.4% on deployed legacy artifact suppressing live entries.
This is the primary reason to deploy the research best immediately.

---

## ══════════════════════════════════════════════
## BLOCK C — CROSS-VALIDATION (after Blocks A and B)
## ══════════════════════════════════════════════

Once Block A and Block B are complete, run cross-validation on the top 2 configs
by median Sharpe (with trades ≥ 280).

  BEST config   / macd=45 → 7 reps
  SECOND config / macd=45 → 7 reps
  BEST config   / macd=30 → 3 reps
  SECOND config / macd=30 → 3 reps

---

## ══════════════════════════════════════════════
## QUICK REFERENCE — VALID PARAMETER VALUES
## ══════════════════════════════════════════════

LONG_VALUE  (always negative): -0.40, -0.41, -0.42, -0.43, -0.44, -0.46, -0.47, -0.48, -0.50
SHORT_VALUE (always positive): equals LONG_VALUE × (−1), two decimal places
MACD period_minutes: 30 or 45 only. Never 15.
price_change_pct period_minutes: 30 only.

FORBIDDEN VALUES: -0.45, -0.49, 0, any positive LONG_VALUE, macd=15.
```

---