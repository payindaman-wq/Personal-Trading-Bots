```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 11601 | Incumbent: Gen 2126 | MIMIR-reviewed 2026-04-XX (v6)
#
# ⚠️ CRITICAL HALT — ACTIVE — DO NOT RUN ANY GENERATION UNTIL ALL CONDITIONS RESOLVED
#
# HALT HISTORY:
#   Gen 11001 (v2): First halt issued
#   Gen 11156 (v3): Re-issued — halt not acted on
#   Gen 11200 (v4): Re-issued — halt not acted on
#   Gen 11400 (v5): Re-issued — halt not acted on
#   Gen 11600 (v6): Re-issued — 600 generations since first halt, zero compliance
#
# CONFIRMED ACTIVE FAILURES AS OF GEN 11600 (unchanged from v5):
#   1. INCUMBENT SLOT: Contains blacklisted Regime B config — NOT RESTORED
#      Evidence: size_pct=15, RSI_long=36.56 visible in "Current Best Strategy"
#   2. DEDUPLICATION CACHE: Non-functional
#      Evidence: Gens 11586/11589/11596/11598/11600 all show identical
#      Sharpe=2.4226, win_rate=53.0%, trades=477
#   3. MAX_TRADES ENFORCEMENT: Non-functional
#      Evidence: Recent gens show 483, 495, 517, 522, 537 trades
#      against supposed limit of MAX_TRADES[swing]=60
#   4. DOCUMENT NOT BEING READ: Root cause of all above
#      Evidence: 600 generations have run after a HARD HALT in this document
#   5. MIN_TRADES[swing]: History of instability (30→20→10→20→25→20→25→21→30)
#      Current value=30 per constants block but must be verified in live code
#
# ROOT CAUSE (CONFIRMED v6):
#   This document is NOT read before sessions start.
#   ODIN loads from memory/cache only — the corrupted Regime B config.
#   The halt, the incumbent restore, the MAX_TRADES limit, and all guidance
#   exist only here and are invisible to ODIN.
#
# REQUIRED FIX (mandatory, non-negotiable):
#   Implement document-read-and-checksum as the VERY FIRST action at session startup.
#   No backtest, no LLM call, no config load may occur before this check passes.
#   Format: [DOCUMENT_VERIFIED gen=N checksum=SHA256_HASH]
#   On failure: [DOCUMENT_FAIL gen=N reason=REASON] → HALT, do not continue.

═══════════════════════════════════════════════════════════════
⚠️  HARD HALT — HUMAN OPERATOR — ALL ITEMS BELOW REQUIRED  ⚠️
     DO NOT RESUME AT GEN 11601 UNTIL ALL ITEMS ARE CHECKED
═══════════════════════════════════════════════════════════════

## Step 0: Diagnose Before You Fix — Answer All Five Questions

Document answers in the run log before touching any checklist item.

(a) IS THIS DOCUMENT BEING READ AT STARTUP?
    HOW TO CHECK: Search the last 600 generation logs for any line containing
    "DOCUMENT_VERIFIED" or "DOCUMENT_FAIL". If absent for every generation
    since Gen 11001 → the document is never read. Fix this first, before
    everything else. No other fix matters if ODIN cannot receive instructions.

(b) DID THE GEN 2126 RESTORE EVER HAPPEN?
    HOW TO CHECK: Search all logs for "restore" or "2126". If absent → restore
    was never attempted. If present → find the log line and confirm the restored
    values match: size_pct=30, RSI_long=34.00, stop_loss_pct=2.41,
    timeout_hours=200, take_profit_pct=3.55.

(c) WHY IS MAX_TRADES NOT BLOCKING >60-TRADE RESULTS?
    HOW TO CHECK: Read the backtest rejection code directly. Confirm:
      - The constant MAX_TRADES["swing"] = 60 exists as a literal in code
      - The check reads: if result.trades > MAX_TRADES[style]: reject
      - This check runs AFTER backtest returns (not before — trades come from backtest)
      - Rejected configs log: [discarded_high_trades gen=N trades=N]
    If ANY of these are absent → the enforcement is broken regardless of what
    constants say.

(d) WHY IS THE DEDUP CACHE NOT BLOCKING EXACT DUPLICATES?
    HOW TO CHECK: Read the deduplication code directly. Confirm:
      - Cache stores a fingerprint (SHA-256 or equivalent) of the FULL config
      - Cache is loaded from disk at startup, saved to disk after each gen
      - Cache is checked BEFORE the backtest is run, not after
      - Fingerprint covers ALL config fields (not just a subset)
    Run a manual test: submit the same config twice → second must be
    logged [DUPLICATE gen=N] and not backtested.

(e) WHY ARE 600 GENERATIONS RUNNING AFTER A HARD HALT?
    HOW TO CHECK: Confirm whether ODIN reads this file at startup.
    If not → the halt only exists on paper and is meaningless.
    FIX: Make document-read-and-checksum the FIRST startup step, before
    anything else. Store this document's SHA-256 checksum in a separate
    immutable file (checksum.txt). Compare on every startup.

═══════════════════════════════════════════════════════════════
## Human Operator Checklist — ALL 16 ITEMS REQUIRED
## Check each box only after confirming, not just attempting
═══════════════════════════════════════════════════════════════

### INFRASTRUCTURE (Fix These First — Nothing Else Works Without Them)

1. [ ] IMPLEMENT DOCUMENT-READ-AND-CHECKSUM AT STARTUP
        Implementation requirements:
        - ODIN reads this file as the very first action of every session
        - Computes SHA-256 of the file contents
        - Compares against checksum stored in a separate file (checksum.txt)
        - If match: logs [DOCUMENT_VERIFIED gen=N checksum=HASH] → continue
        - If mismatch or file missing: logs [DOCUMENT_FAIL gen=N] → HALT
        - No LLM call, no backtest, no config load may precede this check
        Verification: Run one dummy session. Confirm [DOCUMENT_VERIFIED] appears
        as the first log line. Then corrupt this file temporarily → confirm
        [DOCUMENT_FAIL] appears and session halts.

2. [ ] FIX DEDUPLICATION CACHE
        Implementation requirements:
        - Wipe existing cache (it is corrupted/non-functional)
        - Rebuild from scratch with the following properties:
            * Fingerprint = SHA-256 of ALL config fields, sorted alphabetically
            * Persisted to disk after every generation
            * Loaded from disk at startup, before any generation runs
            * Check happens BEFORE backtest: if fingerprint in cache → skip, log [DUPLICATE gen=N]
            * Check happens AFTER LLM proposes config, BEFORE backtest runs
        - Test A: Submit same config twice → second logged [DUPLICATE gen=N], not backtested
        - Test B: Submit configs differing by one field → both accepted
        - Test C: Restart session mid-run → cache survives, still blocks duplicates

3. [ ] FIX MAX_TRADES ENFORCEMENT
        Implementation requirements:
        - Constant in live code: MAX_TRADES = {"swing": 60, "day": 999}
        - Check runs AFTER backtest returns result.trades
        - Check: if result.trades > MAX_TRADES[style]: log [discarded_high_trades gen=N trades=N]; skip
        - Rejected configs do NOT update the incumbent, do NOT enter dedup cache
          (they should enter a separate "high_trades_seen" log only)
        - Test: Submit a config known to produce >60 swing trades → confirm rejection log
        - Test: Submit a config producing exactly 60 trades → confirm it is NOT rejected
        Note: Based on all improvement history, Sharpe>2.5 is only achievable with
        trades=20-30. The 60-trade limit is conservative — we could use 40 and still
        protect the Regime A search space.

4. [ ] AUDIT AND CONFIRM MIN_TRADES[swing]
        - Read the constant in live code: confirm MIN_TRADES["swing"] = 30
        - LOKI change history shows this bounced between 10 and 30 eight times
        - The correct value is 30 — this matches Gen 2126's trade count exactly
        - If current value is not 30 → fix it to 30
        - Confirm check: if result.trades < MIN_TRADES[style]: log [discarded_low_trades gen=N trades=N]; skip
        Note: Lowering MIN_TRADES below 30 was the single most damaging parameter
        change in the research history. It opened the door to overfitted low-trade
        configs. Do not lower it below 30 for any reason.

5. [ ] AUDIT MIN_SHARPE_TO_KEEP ENFORCEMENT
        - Read the constant in live code: confirm MIN_SHARPE_TO_KEEP = 2.9232
        - Check uses strict greater-than (>), not >=
        - Sharpe=2.9232 → [discarded], not [new_elite]
        - Sharpe=2.9233 → [new_elite]
        - Test both cases and confirm log output

### INCUMBENT RESTORE

6. [ ] RESTORE GEN 2126 CONFIG INTO INCUMBENT SLOT EXACTLY
        Copy the YAML from the "TRUE INCUMBENT (Gen 2126)" block below.
        Do not modify any field. Do not let LOKI modify it during restore.
        The corrupted config (size_pct=15, RSI_long=36.56, stop_loss_pct=2.72,
        timeout_hours=196) must be completely removed from all memory slots.

7. [ ] VERIFY INCUMBENT SLOT CONTAINS ALL OF:
          size_pct          = 30
          stop_loss_pct     = 2.41
          timeout_hours     = 200
          take_profit_pct   = 3.55
          RSI_