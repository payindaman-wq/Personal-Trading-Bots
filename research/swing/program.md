```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 11801 | Incumbent: Gen 2126 | MIMIR-reviewed 2026-04-06 (v7)
#
# ⚠️ CRITICAL HALT — ACTIVE — DO NOT RUN ANY GENERATION UNTIL ALL CONDITIONS RESOLVED
#
# HALT HISTORY:
#   Gen 11001 (v2): First halt issued
#   Gen 11156 (v3): Re-issued — halt not acted on
#   Gen 11200 (v4): Re-issued — halt not acted on
#   Gen 11400 (v5): Re-issued — halt not acted on
#   Gen 11600 (v6): Re-issued — 600 generations since first halt, zero compliance
#   Gen 11800 (v7): Re-issued — 800 generations since first halt, zero compliance
#
# FAILURE SUMMARY AS OF GEN 11800 (all failures confirmed active, none resolved):
#
#   FAILURE 1 — DOCUMENT NOT READ AT STARTUP [CRITICAL, ROOT CAUSE OF ALL OTHERS]
#     Evidence: No [DOCUMENT_VERIFIED] or [DOCUMENT_FAIL] line exists in any log
#     since Gen 11001. Zero compliance across 800 generations.
#     This is the root cause. All other failures persist because instructions
#     written here are never received by ODIN.
#     Required fix: Implement document-read-and-checksum as the absolute first
#     action of every session. See Item 1 below.
#
#   FAILURE 2 — INCUMBENT SLOT CONTAINS BLACKLISTED REGIME B CONFIG
#     Evidence: size_pct=15, RSI_long=36.56, stop_loss_pct=2.72, timeout_hours=196
#     visible in "Current Best Strategy". These are not Gen 2126 values.
#     This config entered as incumbent at Gen 2149 (Sharpe=0.8798, 345 trades)
#     — a false improvement that should have been rejected by MAX_TRADES.
#     Required fix: Restore Gen 2126 exactly. See Item 6 below.
#
#   FAILURE 3 — MAX_TRADES ENFORCEMENT NON-FUNCTIONAL
#     Evidence: Recent gens show 483, 488, 491, 495, 499, 504, 513, 521, 523,
#     537, 541 trades against a supposed limit of MAX_TRADES[swing]=60.
#     None were rejected. Gen 2149's 345 trades were also not rejected.
#     Required fix: See Item 3 below.
#
#   FAILURE 4 — DEDUPLICATION CACHE NON-FUNCTIONAL
#     Evidence: Gen 11781 and Gen 11796 both show Sharpe=2.4226, win_rate=53.0%,
#     trades=477 — identical result, evaluated twice, no rejection logged.
#     Multiple other duplicate clusters visible in last 20 gens.
#     Required fix: See Item 2 below.
#
#   FAILURE 5 — MIN_TRADES[swing] UNSTABLE
#     Evidence: Changed 8 times (30→20→10→20→25→20→25→21→30).
#     Current value=30 per constants block but must be verified in live code.
#     Every reduction below 30 opened the search to overfit low-trade configs
#     and produced no improvement over Gen 2126.
#     Required fix: See Item 4 below.
#
# ROOT CAUSE (CONFIRMED v7, unchanged from v6):
#   This document is NOT read before sessions start.
#   ODIN loads from memory/cache only — the corrupted Regime B config persists.
#   The halt, the incumbent restore, the MAX_TRADES limit, and all guidance
#   exist only here and are invisible to ODIN.
#   Until Item 1 is implemented and verified, no other fix will survive a
#   session restart.

═══════════════════════════════════════════════════════════════
⚠️  HARD HALT — HUMAN OPERATOR — ALL 16 ITEMS REQUIRED  ⚠️
     DO NOT RESUME AT GEN 11801 UNTIL ALL ITEMS ARE CHECKED
     ITEMS ARE ORDERED BY DEPENDENCY — DO NOT SKIP AHEAD
═══════════════════════════════════════════════════════════════

## Step 0: Diagnose Before You Fix — Answer All Five Questions
## Document answers in the run log before touching any checklist item.

(a) IS THIS DOCUMENT BEING READ AT STARTUP?
    Search the last 800 generation logs (Gen 11001–11800) for any line
    containing "DOCUMENT_VERIFIED" or "DOCUMENT_FAIL".
    Expected if working: at least one such line per session.
    Actual finding: ZERO such lines across 800 generations.
    Conclusion: Document is NEVER read. Fix this before everything else.
    No other fix survives a restart until this is working.

(b) DID THE GEN 2126 RESTORE EVER HAPPEN?
    Search all logs for "restore" or "2126".
    Expected if working: log line confirming restored values:
      size_pct=30, RSI_long=34.00, stop_loss_pct=2.41,
      timeout_hours=200, take_profit_pct=3.55
    If absent: restore was never attempted.
    If present: verify the live incumbent matches these values exactly.

(c) WHY IS MAX_TRADES NOT BLOCKING >60-TRADE RESULTS?
    Read the backtest rejection code directly. Confirm ALL of:
      - Constant MAX_TRADES["swing"] = 60 exists as a literal in live code
      - Check: if result.trades > MAX_TRADES[style]: reject
      - Check runs AFTER backtest returns result.trades (trades come from backtest)
      - Rejected configs log: [discarded_high_trades gen=N trades=N]
      - Rejected configs do NOT update incumbent, do NOT enter dedup cache
    If ANY of these are absent: enforcement is broken.
    Note: Gen 2149 (345 trades) entered the incumbent slot because this check
    did not exist. That single failure caused 9,600 wasted generations.

(d) WHY IS THE DEDUP CACHE NOT BLOCKING EXACT DUPLICATES?
    Read the deduplication code directly. Confirm ALL of:
      - Cache stores SHA-256 of the FULL config (all fields, sorted alphabetically)
      - Cache persisted to disk after every generation
      - Cache loaded from disk at startup, before any generation runs
      - Check happens BEFORE backtest: if fingerprint in cache → skip
      - Log format: [DUPLICATE gen=N fingerprint=HASH]
    Run manual test: submit same config twice → second must be logged [DUPLICATE]
    and not backtested.

(e) WHY ARE 800 GENERATIONS RUNNING AFTER A HARD HALT?
    Answer: ODIN does not read this file at startup.
    The halt exists only on paper and is invisible to ODIN.
    Fix: Item 1 — document-read-and-checksum as the first startup action.
    This is not optional. Every other fix in this document is meaningless
    if ODIN cannot receive instructions across session boundaries.

═══════════════════════════════════════════════════════════════
## Human Operator Checklist — ALL 16 ITEMS REQUIRED
## Items are ordered by dependency. Do not check a box until
## the implementation is confirmed working, not just attempted.
═══════════════════════════════════════════════════════════════

### BLOCK A: INFRASTRUCTURE (Must complete before any other block)

1. [ ] IMPLEMENT DOCUMENT-READ-AND-CHECKSUM AT STARTUP
        This is the single most important fix. Nothing else survives a restart
        without it.
        Implementation requirements:
        - ODIN reads THIS FILE as the absolute first action of every session
        - Computes SHA-256 of file contents
        - Compares against checksum stored in a SEPARATE, IMMUTABLE file
          (checksum.txt — must not be auto-updated by ODIN or LOKI)
        - If match: logs [DOCUMENT_VERIFIED gen=N checksum=HASH] → continue
        - If mismatch or file missing: logs [DOCUMENT_FAIL gen=N reason=REASON]
          → HALT immediately, do not continue session
        - No LLM call, no backtest, no config load, no LOKI action may precede
          this check
        Verification test (MANDATORY before proceeding):
        - Run one dummy session → confirm [DOCUMENT_VERIFIED] is the first log line
        - Corrupt this file temporarily → confirm [DOCUMENT_FAIL] appears and
          session halts without running any generation
        - Restore file → confirm [DOCUMENT_VERIFIED] resumes
        Do not check this box until all three tests pass.

2. [ ] FIX DEDUPLICATION CACHE
        Implementation requirements:
        - Wipe existing cache completely (confirmed corrupted/non-functional)
        - Rebuild from scratch:
            * Fingerprint = SHA-256(JSON of all config fields, keys sorted A-Z)
            * Persisted to disk after every generation (not just at session end)
            * Loaded from disk at startup, before any generation runs
            * Check happens AFTER LLM proposes config, BEFORE backtest runs
            * If duplicate: log [DUPLICATE gen=N fingerprint=HASH], skip backtest
            * Duplicate configs do NOT consume a generation number
        Verification tests (all three required):
        - Test A: Submit same config twice → second logged [DUPLICATE