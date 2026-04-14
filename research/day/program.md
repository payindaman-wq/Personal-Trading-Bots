```markdown
# ODIN Research Program — Crypto Day Trading Strategy Optimizer
# Version: 8400-MIMIR-AUDIT-3

---

## ⚠️ STOP — READ THIS FIRST ⚠️

### THE ONLY VALID TEMPLATE

Your ONLY job is to output ONE YAML block using this EXACT structure.
You change exactly TWO values. Everything else is fixed.

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

**THE TWO VALUES YOU CHANGE:**
- `value:` on the price_change_pct lines (long and short, sign-flipped)
- `period_minutes:` on the macd_signal lines (both long and short)

**CHANGE NOTHING ELSE. NOT ONE OTHER CHARACTER.**

---

## ⛔ THE MOST DANGEROUS MISTAKE ⛔

### DO NOT COPY THE "CURRENT BEST STRATEGY" — IT IS WRONG

There is a legacy strategy with indicators like `momentum_accelerating`,
`price_vs_ema`, `trend`, and `price_change_pct period_minutes: 5`.

**THIS IS THE FORBIDDEN TEMPLATE. DO NOT USE IT. DO NOT LOOK AT IT.**

If your output contains ANY of these words, DELETE IT AND START OVER:
- `momentum_accelerating`
- `price_vs_ema`
- `trend`
- `period_minutes: 5` (on price_change_pct)
- `period_minutes: 15` (on price_change_pct)
- `period_minutes: 45` (on price_change_pct)
- `period_minutes: 60` (on price_change_pct)
- `max_open: 3`
- `stop_loss_pct: 0.4`
- `take_profit_pct: 3.51`

These values mean you copied the WRONG template. The wrong template
produces Sharpe around -6 to -18 and 500–900 trades. It is catastrophic.

---

## ⛔ FAILURE SIGNATURES — IF YOU SEE THESE, YOU ARE WRONG ⛔

| What you output caused        | Sharpe     | Trades | Fix                         |
|-------------------------------|------------|--------|-----------------------------|
| Wrong template / no macd      | -6.1759    | 560    | Copy correct template above |
| No confirmation filter        | -4.7772    | 818    | Copy correct template above |
| No confirmation filter        | -1.86      | 1391   | Copy correct template above |
| Wrong price_change period     | -0.3075    | 529    | Set period_minutes: 30      |
| Extra forbidden indicators    | -11.8843   | 325    | Remove all but 2 indicators |

If your last output produced ANY of these results: DO NOT adjust parameters.
COPY THE CORRECT TEMPLATE FROM SCRATCH. Start over. The problem is format,
not parameters.

---

## EXACTLY 4 INDICATOR CONDITIONS — COUNT THEM

Your output MUST have EXACTLY 4 indicator conditions total:
1. long → price_change_pct (period_minutes: 30, operator: lt, value: negative)
2. long → macd_signal (period_minutes: 15/30/45, operator: eq, value: bullish)
3. short → price_change_pct (period_minutes: 30, operator: gt, value: positive)
4. short → macd_signal (period_minutes: 15/30/45, operator: eq, value: bearish)

If you have 3 conditions → WRONG. Delete and restart.
If you have 5 conditions → WRONG. Delete and restart.
If you have 6 conditions → WRONG. Delete and restart.

---

## PARAMETER RULES

### Parameter A: price_change_pct value

VALID values (long side, exactly 2 decimal places):
  -0.40  -0.41  -0.42  -0.43  -0.44  -0.46  -0.47  -0.48  -0.50

FORBIDDEN (never use):  -0.45  -0.49

Short value = long value with sign flipped:
  long=-0.42 → short=0.42
  long=-0.41 → short=0.41
  long=-0.43 → short=0.43

price_change_pct period_minutes is ALWAYS 30. Never 5, 15, 45, 60.

### Parameter B: macd_signal period_minutes

VALID values: 15, 30, 45
Must be identical for long and short.
Current priority: 45 > 30 > 15

---

## FIXED VALUES — NEVER CHANGE THESE

| Field               | Fixed value        |
|---------------------|--------------------|
| name                | crossover          |
| style               | momentum_optimized |
| max_open            | 4                  |
| take_profit_pct     | 2.5                |
| stop_loss_pct       | 1.2                |
| timeout_minutes     | 720                |
| size_pct            | 10                 |
| fee_rate            | 0.001              |
| pairs               | ALL 16 (see above) |

If your output has max_open=3 or stop_loss_pct=0.4: WRONG. Delete and restart.

---

## MIN_TRADES = 280. LOCKED. DO NOT CHANGE.

Results with trades < 280: rejected (log if Sharpe > 1.10)
Results with trades > 450: structural failure — reject

---

## CURRENT STATE

### Formal Accepted Best
  Sharpe=1.1137, price_change_pct=-0.50, macd=30, 288 trades
  NOTE: This is likely a statistical artifact from when MIN_TRADES was
  briefly set to 200. The true median for -0.50/macd=30 is unknown.
  The target is not to beat 1.1137 specifically — it is to find the
  highest-median-Sharpe region at ≥280 trades.

### Recent Valid Results (≥280 trades)
  Gen 8381: -0.43/macd=30 → Sharpe=1.074, trades=308
  Gen 8383: -0.43/macd=30 → Sharpe=1.077, trades=305
  Gen 8395: -0.43/macd=30 → Sharpe=1.011, trades=326
  Gen 8398: -0.43/macd=30 → Sharpe=1.074, trades=308
  Gen 8399: -0.43/macd=30 → Sharpe=1.072, trades=308
  CONCLUSION: -0.43/macd=30 median ≈ 1.07–1.08. Characterized. Do not repeat.

### High-Value Low-Trade Anomalies (logged — do not discard)
  Gen 8384: Sharpe=1.3614, trades=176 [rejected — low trades]
  Gen 8194: Sharpe=1.3082, trades=148 [rejected — low trades]
  Gen 8197: Sharpe=1.1626, trades=164 [rejected — low trades]
  INTERPRETATION: These confirm that macd=45 (or tighter thresholds)
  produces genuinely better signal quality. Goal: find parameter sets
  that achieve similar quality at ≥280 trades.

---

## KNOWN RESULTS TABLE

| Long value | MACD period | Trades    | Sharpe (observed)   | Status                          |
|------------|-------------|-----------|---------------------|---------------------------------|
| -0.43      | 30          | 305–326   | 1.07–1.08 median    | ✅ Characterized — do not repeat|
| -0.50      | 30          | 288       | 1.1137              | ⚠️ Artifact — do not repeat     |
| -0.42      | 30          | ~323      | ≈1.15 (estimated)   | 🎯 HIGH PRIORITY                |
| -0.41      | 30          | ~324      | ≈1.14 (estimated)   | 🎯 HIGH PRIORITY                |
| -0.40      | 30          | ~333      | ≈1.12 (estimated)   | 🔶 TEST                         |
| -0.44      | 30          | ~318      | ≈1.10 (estimated)   | 🔶 TEST                         |
| -0.43      | 45          | ?         | ?                   | 🎯 HIGHEST PRIORITY — untested  |
| -0.42      | 45          | ?         | ?                   | 🎯 HIGH PRIORITY — untested     |
| -0.41      | 45          | ?         | ?                   | 🎯 HIGH PRIORITY — untested     |
| -0.44      | 45          | ?         | ?                   | 🎯 TEST — may recover trades    |
| -0.46      | 30          | ?         | ?                   | 🔶 Untested — fill gap          |
| -0.47      | 30          | ?         | ?                   | 🔶 Untested — fill gap          |
| -0.48      | 30          | ?         | ?                   | 🔶 Untested — fill gap          |
| -0.43      | 15          | ~308      | ≈1.08               | ❌ Deprioritize                 |
| -0.45      | any         | —         | low                 | ❌ NEVER TEST                   |
| -0.49      | any         | —         | low                 | ❌ NEVER TEST                   |

---

## PRIORITY PLAN — NEXT 100 GENERATIONS

### CRITICAL: Address Structural Failure Rate First

Recent failure rate: ~40% of generations are structural failures
(-6.1759/560, -4.7772/818, -8.5336/759).
These waste research budget and indicate the LLM is reverting to
the forbidden legacy template or dropping macd_signal entirely.

Every generation must begin by copying the correct template above.
Do not improvise. Do not adapt the legacy template. Copy. Exactly.

---

### PHASE 2: macd=45 Exploration (PRIMARY — 35 gens)

This is the highest-priority unexplored region. High-Sharpe low-trade
anomalies (1.3614, 1.3082, 1.1626) strongly suggest macd=45 produces
better signal quality. If trades fall below 280 at tight thresholds,
try slightly looser thresholds (-0.44, -0.46) to recover trade count.

Allocation:
  - -0.43 / macd=45 — 10 reps   (baseline comparison)
  - -0.42 / macd=45 — 10 reps   (tighter + slower — high priority)
  - -0.41 / macd=45 — 8 reps    (tightest + slowest — high priority)
  - -0.44 / macd=45 — 4 reps    (looser threshold — may recover trades)
  - -0.46 / macd=45 — 3 reps    (looser still — if -0.44 still under 280)

Decision rules:
  - If macd=45 median trades ≥ 280 AND median Sharpe > 1.08:
    → macd=45 becomes co-primary alongside macd=30
  - If macd=45 median trades consistently < 280 at -0.41/-0.42/-0.43:
    → Try -0.44/-0.46 with macd=45 before abandoning
  - If any run achieves Sharpe > 1.1137 AND trades ≥ 280:
    → Accept immediately as new best. Replace deployed strategy.

---

### PHASE 3: Threshold Sweep at macd=30 (30 gens)

Map the Sharpe landscape at all valid thresholds. Focus on
untested values and highest-estimated-performance values.

  - -0.42 / macd=30 — 7 reps    (estimated ~1.15 — highest priority)
  - -0.41 / macd=30 — 7 reps    (estimated ~1.14 — high priority)
  - -0.40 / macd=30 — 5 reps    (estimated ~1.12 — confirm)
  - -0.44 / macd=30 — 4 reps    (estimated ~1.10 — below primary)
  - -0.46 / macd=30 — 4 reps    (untested — fill gap)
  - -0.47 / macd=30 — 2 reps    (untested — fill gap)
  - -0.48 / macd=30 — 1 rep     (untested — fill gap)

FORBIDDEN in Phase 3:
  -0.45 (never), -0.49 (never), -0.43 (characterized), -0.50 (artifact)
  macd=15 (zero budget)

---

### PHASE 4: Cross-MACD at Top Thresholds (20 gens)

After Phase 3, take the top 2 thresholds by median Sharpe (trades ≥ 280).
Call them A (best) and B (second best).

  - threshold_A / macd=45 — 7 reps
  - threshold_B / macd=45 — 7 reps
  - threshold_A / macd=30 — 3 reps  (validation)
  - threshold_B / macd=30 — 3 reps  (validation)

If Phase 2 showed -0.43/macd=45 median > -0.43/macd=30 median:
  Add -0.43/macd=45 as a third track with 5 additional reps.

---

### WHAT TO AVOID IN ALL PHASES

NEVER: -0.45 or -0.49 (confirmed underperformers)
NEVER: price_change_pct period_minutes ≠ 30
NEVER: More than 2 conditions per side (4 total)
NEVER: Any indicator besides price_change_pct and macd_signal
NEVER: macd_signal value other than bullish or bearish
NEVER: macd_signal period_minutes other than 15, 30, or 45
NEVER: Change MIN_TRADES from 280 (it is locked forever)
NEVER: Run more -0.43/macd=30 repetitions (characterized)
NEVER: Run more -0.50/macd=30 repetitions (artifact, characterized)

---

## ACCEPTANCE CRITERIA

| Metric   | Required                       |
|----------|--------------------------------|
| Trades   | ≥ 280 (LOCKED — never change)  |
| Sharpe   | > 1.1137 (current formal best) |

Trades > 450: structural failure — reject regardless of Sharpe.
Trades < 280: automatic rejection — log if Sharpe > 1.10 for analysis.

Adjusted score formula: Sharpe × sqrt(trades / 50) ≥ 2.90
  Sharpe ≥ 1.166 at 308 trades
  Sharpe ≥ 1.139 at 323 trades
  Sharpe ≥ 1.114 at 339 trades

---

## DEPLOYMENT DECISION

The strategy CURRENTLY DEPLOYED is a wrong 5-indicator legacy artifact.
It must be replaced.

REPLACEMENT TRIGGER: Any run with Sharpe > 1.1137 AND trades ≥ 280
  → Replace immediately. Do not wait for Phase 4.

If no run in Phases 2–4 beats 1.1137:
  → Accept best observed result across all phases.
  → The 2-indicator strategy is still superior to the legacy artifact.
  → Do NOT revert to the 5-indicator strategy under any circumstances.

---

## LIVE PERFORMANCE NOTE

Zero live trades are EXPECTED in current regime:
  F&G = 21 (Extreme Fear), BTC Dominance = 57.39%

DO NOT modify strategy to force live trades.
DO NOT reduce price_change_pct toward 0.
DO NOT switch to macd=15 for faster signals.
DO NOT change max_open or stop_loss.

MONITORING TRIGGER: If F&G > 25 AND BTC dominance < 54%:
  Expect trades to resume. If zero trades persist 2+ sprints after
  regime shift to NEUTRAL, escalate to MIMIR.

---

## EMERGENCY DEFAULT

If you are ever unsure what to output, use:
  price_change_pct: long=-0.43, short=0.43
  macd_signal period_minutes: 30

This is always valid. Always better than guessing wrong.

---

## PRE-SUBMIT CHECKLIST — VERIFY EVERY ITEM

✓ name = crossover
✓ style = momentum_optimized
✓ max_open = 4
✓ stop_loss_pct = 1.2
✓ take_profit_pct = 2.5
✓ timeout_minutes = 720
✓ size_pct = 10
✓ fee_rate = 0.001
✓ All 16 pairs present
✓ price_change_pct long value is in: -0.40,-0.41,-0.42,-0.43,-0.44,-0.46,-0.47,-0.48,-0.50
✓ price_change_pct short value = long value sign-flipped, 2 decimal places
✓ BOTH price_change_pct period_minutes = 30
✓ BOTH macd_signal period_minutes = same value (15, 30, or 45)
✓ macd_signal long value = bullish
✓ macd_signal short value = bearish
✓ Total conditions = 4 (count: long1, long2, short1, short2)
✓ No momentum_accelerating, price_vs_ema, trend, or any other indicator
✓ No max_open=3, stop_loss_pct=0.4, take_profit_pct=3.51 (legacy artifact values)

If ANY item fails: DELETE OUTPUT. COPY TEMPLATE FROM TOP. START OVER.
```