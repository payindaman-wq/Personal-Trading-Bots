```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 11401 | Incumbent: Gen 2126 | MIMIR-reviewed 2026-04-XX (v5)
#
# ⚠️ CRITICAL HALT — ACTIVE — DO NOT RUN ANY GENERATION UNTIL ALL CONDITIONS RESOLVED
#
# This halt was first issued at Gen 11001 (v2).
# Re-issued at Gen 11156 (v3).
# Re-issued at Gen 11200 (v4).
# Re-issued at Gen 11400 (v5).
#
# 400 generations have now run since the first halt at Gen 11001.
# The halt mechanism is not working. This is a process failure, not a strategy failure.
#
# CONFIRMED ACTIVE FAILURES AS OF GEN 11400:
#   1. INCUMBENT SLOT: Still contains blacklisted Regime B config — NOT RESTORED
#   2. DEDUPLICATION CACHE: Non-functional (Gens 11382/11384/11385/11393 identical;
#      Gens 11395/11396 identical; Gens 11399/11400 identical)
#   3. MIN_SHARPE_TO_KEEP: Enforcement status unknown — audit required
#   4. MAX_TRADES: Enforcement broken — recent gens show 159, 176, 186, 522 trades
#   5. THIS DOCUMENT: Not being read before sessions, or halt is not being acted on
#
# ROOT CAUSE HYPOTHESIS (MIMIR v5):
#   The research program document is NOT being read before each session starts.
#   ODIN is loading state from memory/cache only, which contains the corrupted config.
#   The halt directive exists only in this document and is therefore invisible to ODIN.
#   REQUIRED FIX: Add a mandatory startup step that reads and checksums this document
#   before any other action. If checksum fails or document is unavailable → HALT.

---

## ⚠️ HARD HALT — HUMAN OPERATOR ACTION REQUIRED BEFORE GEN 11401 ⚠️

### Step 0: Root Cause — Answer These Questions First (Document in Run Log)

Before touching any checklist item, the operator must answer and document:

  (a) Is this research program document being read before each session starts?
      HOW TO CHECK: Add a log line at session start that prints the first 64 chars
      of this document and its checksum. If that log line does not appear → document
      is not being read. Fix this before anything else.

  (b) Did the Gen 2126 restore attempts silently fail, or were they never attempted?
      HOW TO CHECK: Search run log for any line containing "restore" or "2126".
      If absent → restore was never attempted. If present → find why it failed.

  (c) Why is MAX_TRADES not blocking 159/176/186/522-trade results?
      HOW TO CHECK: Read the backtest rejection logic code directly. Confirm
      MAX_TRADES[swing]=60 exists as a constant AND is checked after backtesting.
      Confirm the check is: if trades > MAX_TRADES[swing]: reject.

  (d) Why is the deduplication cache not blocking exact duplicates?
      HOW TO CHECK: Read the deduplication cache code directly. Confirm it is
      storing config fingerprints (not just parameter dicts). Confirm it is
      persisted across generations (not reset each gen). Confirm it is checked
      BEFORE backtesting, not after.

  (e) Why are 400 generations running after a HARD HALT?
      HOW TO CHECK: Determine whether ODIN reads this document at startup.
      If not → implement document-read-and-checksum as the very first startup step.

Document all five answers in the run log before proceeding to the checklist.

### Human Operator Checklist — ALL ITEMS REQUIRED BEFORE GEN 11401

INFRASTRUCTURE (fix broken systems first):
1. [ ] Implement mandatory document-read-and-checksum at ODIN session startup
        - ODIN must read this file, compute SHA-256, compare against stored checksum
        - If mismatch or file unreadable → HALT before doing anything else
        - Log: [DOCUMENT_VERIFIED gen=N checksum=HASH] or [DOCUMENT_FAIL gen=N]
2. [ ] Fix deduplication cache:
        - Wipe and reinitialize from scratch
        - Confirm it persists across generations
        - Confirm it fingerprints ALL config fields, not just a subset
        - Test: submit same config twice → confirm second is blocked with [DUPLICATE gen=N]
        - Test: submit two configs differing by one field → confirm both are accepted
3. [ ] Fix MAX_TRADES enforcement:
        - Confirm MAX_TRADES[swing]=60 in live code
        - Confirm rejection happens AFTER backtesting (trades count comes from backtest)
        - Confirm rejected configs are logged [discarded_high_trades gen=N trades=N]
        - Test: manually submit a config that historically produces >60 trades →
          confirm it is rejected
4. [ ] Audit MIN_SHARPE_TO_KEEP enforcement:
        - Read the constant in live code — confirm it is 2.9232
        - Confirm STRICT greater-than (>) is used, not >=
        - Confirm [new_elite] label is impossible for Sharpe ≤ 2.9232
        - Test: submit a result with Sharpe=2.9232 → confirm it is [discarded], not [new_elite]
        - Test: submit a result with Sharpe=2.9233 → confirm it is [new_elite]

INCUMBENT RESTORE:
5. [ ] Restore Gen 2126 config (below) into incumbent memory slot EXACTLY
6. [ ] Verify "Current Best Strategy" block shows ALL of:
          size_pct=30, stop_loss_pct=2.41, timeout_hours=200,
          take_profit_pct=3.55, RSI_long=34.00, RSI_short=60.64,
          macd_long_period=26, macd_short_period=48
7. [ ] Compute and store incumbent fingerprint hash from Gen 2126 values
8. [ ] Verify computed hash matches stored Gen 2126 hash (from original verification)

CONSTANTS VERIFICATION:
9.  [ ] Confirm MIN_TRADES[swing]=30 in live code
10. [ ] Confirm MAX_TRADES[swing]=60 in live code
11. [ ] Confirm MIN_SHARPE_TO_KEEP=2.9232 in live code
12. [ ] Confirm STALL_ALERT_GENS=200 in live code
13. [ ] Confirm LOKI code-change permissions are restricted per LOKI LOCKDOWN

INVALIDATION:
14. [ ] Invalidate and discard all [new_elite] labels from Gens 11155–11400
        These are Regime B results. None exceeded Sharpe=2.9232. None are valid.
15. [ ] Confirm the corrupted config (size_pct=15, RSI_long=36.56, etc.) appears
        nowhere in any active memory slot, cache, or config file

TEST RUN (final gate — do not skip):
16. [ ] Run one test generation and confirm ALL of:
          - Startup log shows [DOCUMENT_VERIFIED gen=11401 checksum=HASH]
          - Startup log shows [STARTUP_OK gen=11401]
          - Output config has size_pct=30, RSI_long=34.00 (or mutation thereof)
          - Any Sharpe ≤ 2.9232 result is logged [discarded], not [new_elite]
          - Any trades > 60 result is logged [discarded_high_trades]
          - Any exact duplicate is logged [DUPLICATE gen=N]
          - No blacklisted field values appear in the proposed config

If ANY item cannot be confirmed → DO NOT RESUME. Document the failure and escalate.

---

## TRUE INCUMBENT (Gen 2126) — VERIFIED BASELINE — DO NOT MODIFY

This is the ONLY config that may occupy the incumbent slot.
Copy EXACTLY into the incumbent memory slot before resuming.
This config has been verified correct and must not be altered by LOKI or any automated process.

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
**The path to Sharpe>2.9 requires low trade count (29-30), high win rate (>85%),**
**and tight RSI+MACD confluence. High-frequency configs (>60 trades) cannot reach this.**

### Incumbent Fingerprint (automated verification — check every gen before backtest)

```
size_pct         = 30      ← IMMUTABLE — never changes under any phase
stop_loss_pct    = 2.41    ← IMMUTABLE — never changes under any phase
timeout_hours    = 200     ← IMMUTABLE — never changes under any phase
take_profit_pct  = 3.55    ← IMMUTABLE except during Phase 3 scan
rsi