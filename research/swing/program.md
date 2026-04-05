```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 11201 | Incumbent: Gen 2126 | MIMIR-reviewed 2026-04-05 (v4)
#
# ⚠️ CRITICAL HALT — ACTIVE — DO NOT RUN ANY GENERATION UNTIL ALL CONDITIONS RESOLVED
#
# Three systems are simultaneously broken as of Gen 11200:
#   1. INCUMBENT SLOT: RSI_long=36.7 (blacklisted) — Gen 2126 NOT restored
#   2. DEDUPLICATION CACHE: Non-functional (3 distinct exact duplicates in last 20 gens)
#   3. MIN_SHARPE_TO_KEEP: Not enforced (Gens 11191/11194/11197 labeled [new_elite]
#      at Sharpe=2.4242, far below the 2.9232 threshold)
#
# This halt was first issued at Gen 11001 (v2). It was re-issued at Gen 11156 (v3).
# As of Gen 11200, 200 generations have run without resolution.
# The operator must determine WHY the halt is not being acted on before resuming.

---

## ⚠️ HARD HALT — HUMAN OPERATOR ACTION REQUIRED BEFORE GEN 11201 ⚠️

### Root Cause Investigation Required First

Before executing the checklist below, the operator must answer:
  (a) Is the research program document being read before each session starts?
      If not → add a mandatory startup step that reads and checksums this document.
  (b) Did the Gen 2126 restore silently fail, or was it never attempted?
      If silently failed → find and fix the restore bug before attempting again.
  (c) Why is MIN_SHARPE_TO_KEEP not blocking Sharpe=2.4242 results from [new_elite]?
      Audit the acceptance logic code directly — do not assume it is correct.
  (d) Why is the deduplication cache not blocking exact-duplicate configs?
      The cache was implemented at Gen 9400 but is visibly non-functional by Gen 11185.

Document answers to all four questions in the run log before proceeding.

### Human Operator Checklist — ALL ITEMS REQUIRED BEFORE GEN 11201

1. [ ] Restore Gen 2126 config (below) into the incumbent memory slot EXACTLY
2. [ ] Verify "Current Best Strategy" block shows:
         size_pct=30, stop_loss_pct=2.41, timeout_hours=200,
         take_profit_pct=3.55, RSI_long=34.00, RSI_short=60.64
3. [ ] Verify incumbent fingerprint hash matches stored Gen 2126 hash
4. [ ] Wipe and reinitialize the deduplication cache from scratch
5. [ ] Run a deduplication test: submit the same config twice, confirm second is blocked
6. [ ] Audit MIN_SHARPE_TO_KEEP enforcement in live code — confirm it is 2.9232
         and that STRICT greater-than (not >=) is used
7. [ ] Confirm [new_elite] label is IMPOSSIBLE for any result with Sharpe < 2.9232
8. [ ] Confirm MIN_TRADES[swing]=30 in live code
9. [ ] Confirm MAX_TRADES[swing]=60 in live code
10. [ ] Confirm STALL_ALERT_GENS=200 in live code
11. [ ] Confirm LOKI code-change permissions are restricted per LOKI LOCKDOWN
12. [ ] Run one test generation and confirm:
          - output config has size_pct=30, RSI_long=34.00
          - Sharpe < 2.9232 results are logged [discarded], not [new_elite]
          - trades > 60 results are rejected before backtesting
13. [ ] Invalidate and discard all [new_elite] labels from Gens 11155-11200 —
          they are Regime B results, all below MIN_SHARPE_TO_KEEP

If ANY item cannot be confirmed → DO NOT RESUME. Escalate and document immediately.

---

## TRUE INCUMBENT (Gen 2126) — VERIFIED BASELINE — DO NOT MODIFY

This is the ONLY config that may occupy the incumbent slot.
Copy EXACTLY into the incumbent memory slot before resuming.

```yaml
name: crossover
style: randomly generated
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
position:
  size_pct: 30
  max_open: 1
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 34.00
    - indicator: macd_signal
      period_hours: 26
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: gt
      value: 60.64
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bearish
exit:
  take_profit_pct: 3.55
  stop_loss_pct: 2.41
  timeout_hours: 200
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

**Gen 2126 verified metrics: Sharpe=2.9232 | Win rate=90.0% | Trades=30**
**This is the ONLY known result above Sharpe=2.9. It must be protected absolutely.**

### Incumbent Fingerprint (automated verification — check every gen before backtest)

```
size_pct        = 30      ← immutable
stop_loss_pct   = 2.41    ← immutable
timeout_hours   = 200     ← immutable
take_profit_pct = 3.55    ← immutable (except during Phase 3 scan)
rsi_long_value  = 34.00   ← changes during Phase 1 scan only
rsi_short_value = 60.64   ← changes during Phase 2 scan only
macd_long_period = 26     ← changes during Phase 4 scan only
macd_short_period = 48    ← changes during Phase 4 scan only
```

If ANY non-designated field differs from above → HALT immediately, log
`[CORRUPTED_INCUMBENT_DETECTED gen=N field=FIELD value=VALUE]`, do not backtest,
alert operator. Do not attempt auto-restore — require human confirmation.

### Startup Verification Procedure (MANDATORY before EVERY generation)

ODIN must execute this sequence before every single generation, without exception:
1. Load incumbent from memory slot
2. Compute fingerprint hash of all 8 fields above
3. Compare against stored hash from last verified-good state
4. If mismatch → HALT, log `[INCUMBENT_FINGERPRINT_MISMATCH gen=N]`, alert operator
5. Confirm deduplication cache is non-empty (if empty and gen > 1 → HALT, do not warn)
6. Confirm MIN_SHARPE_TO_KEEP=2.9232 in live code (read the constant, do not assume)
7. Confirm MIN_TRADES[swing]=30, MAX_TRADES[swing]=60 in live code
8. Confirm STALL_ALERT_GENS=200 in live code
9. Log startup verification result: `[STARTUP_OK gen=N]` or `[STARTUP_FAIL gen=N reason=R]`

If any step fails → HALT. Do not run the generation. Alert operator.

---

## KNOWN CORRUPTED CONFIG — PERMANENTLY BLACKLISTED

**NEVER load as incumbent. NEVER backtest. NEVER use as base for mutations.**

```
size_pct=15, stop_loss_pct=2.72, timeout_hours=196, RSI long=36.56
```

Any config containing ANY of the following is a Regime B artifact — reject immediately,
before backtesting, at the proposal stage:
- size_pct = 15
- stop_loss_pct = 2.72
- timeout_hours = 196
- entry.long RSI value ∈ {36.56, 36.7, 36.70, 36.68}
- trades > 60 (any backtest result — reject after backtesting if not caught before)

Log as: `[CORRUPTED_INCUMBENT_DETECTED gen=N field=FIELD value=VALUE]`

**How this corruption occurred:**
Gen 2149 accepted Sharpe=0.8798 over the incumbent Sharpe=2.9232. This was a bug
in the acceptance logic — MIN_SHARPE_TO_KEEP was inactive or set incorrectly.
The corrupted config ran as incumbent for 8,900+ generations.
Damage: 8,900 wasted generations, Regime B ceiling of 2.5324 never exceeded.

---

## SYSTEM CONSTANTS — PERMANENTLY LOCKED — LOKI MAY NOT MODIFY

```
MIN_TRADES[