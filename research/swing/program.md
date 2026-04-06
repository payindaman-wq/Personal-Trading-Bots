```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 12001 | Incumbent: Gen 2126 (MUST BE RESTORED — SEE HALT)
# MIMIR-reviewed 2026-04-06 (v8)
#
# ⚠️ CRITICAL HALT — ACTIVE — DO NOT RUN ANY GENERATION
# ⚠️ THIS HALT HAS BEEN ACTIVE SINCE GEN 11001 (1000+ GENERATIONS AGO)
# ⚠️ ZERO COMPLIANCE IN 1000 GENERATIONS — ROOT CAUSE CONFIRMED BELOW
#
# ══════════════════════════════════════════════════════════════════════
# HALT HISTORY (every reissuance has been ignored — this is evidence,
# not repetition):
#   Gen 11001 (v2): First halt
#   Gen 11156 (v3): Re-issued — not acted on
#   Gen 11200 (v4): Re-issued — not acted on
#   Gen 11400 (v5): Re-issued — not acted on
#   Gen 11600 (v6): Re-issued — not acted on
#   Gen 11800 (v7): Re-issued — not acted on
#   Gen 12000 (v8): Re-issued — confirmed 1000 generations of zero compliance
# ══════════════════════════════════════════════════════════════════════
#
# ROOT CAUSE (CONFIRMED, UNCHANGED ACROSS ALL VERSIONS):
#   This document is NOT read at session startup.
#   ODIN loads from memory/cache only.
#   Every instruction, every halt, every fix written here is invisible
#   to the running system until Item 1 is implemented and verified.
#   There is exactly ONE fix that enables all other fixes: Item 1.
#   Do not implement any other item until Item 1 passes all three
#   verification tests.
#
# ══════════════════════════════════════════════════════════════════════
# CONFIRMED ACTIVE FAILURES AS OF GEN 12000
# ══════════════════════════════════════════════════════════════════════
#
# FAILURE 1 — DOCUMENT NOT READ AT STARTUP [ROOT CAUSE]
#   Evidence: Zero [DOCUMENT_VERIFIED] or [DOCUMENT_FAIL] lines in any
#   log across 1000 generations (Gen 11001–12000).
#   Impact: All other failures persist. No instruction survives restart.
#   Fix: Item 1 (mandatory first).
#
# FAILURE 2 — INCUMBENT SLOT CONTAINS CORRUPTED REGIME B CONFIG
#   Evidence: size_pct=15, RSI_long=36.56, stop_loss_pct=2.72,
#   timeout_hours=196 visible in Current Best Strategy.
#   These values entered at Gen 2149 (Sharpe=0.8798, 345 trades).
#   Gen 2149 should have been rejected by MAX_TRADES (345 >> 60).
#   The true incumbent is Gen 2126: Sharpe=2.9232, win_rate=90.0%,
#   trades=30.
#   This single corrupt incumbent slot has misdirected ~9,850 generations.
#   Fix: Item 6 (restore Gen 2126 exactly).
#
# FAILURE 3 — MAX_TRADES ENFORCEMENT NON-FUNCTIONAL
#   Evidence: Gens 11985 (715 trades), and the entire post-Gen-2149
#   history showing 345–540 trade results accepted without rejection.
#   Gen 2149 (345 trades) entered the incumbent slot because this check
#   did not exist. That single failure caused this entire crisis.
#   Fix: Item 3.
#
# FAILURE 4 — DEDUPLICATION CACHE NON-FUNCTIONAL
#   Evidence: Gen 11993, 11995, 11998 — identical Sharpe=2.4226,
#   win_rate=53.0%, trades=477 — evaluated three separate times in the
#   last 20 generations alone. Prior identical pair at Gens 11781/11796.
#   Fix: Item 2.
#
# FAILURE 5 — MIN_TRADES[swing] HAS BEEN CHANGED 9 TIMES
#   History: 30→20→10→20→25→20→25→21→30
#   Current value: 30 (correct — do not change)
#   Every reduction below 30 opened search to overfit low-trade configs
#   or to the Regime B high-frequency attractor.
#   The reduction to 10 (Gen 7200) was the worst individual change.
#   Fix: Item 4 (lock at 30, make immutable).
#
# FAILURE 6 — PAIRS LIST INCONSISTENT WITH RESEARCH SCOPE
#   Evidence: Current incumbent shows LINK/USD, ADA/USD, BTC/USD, OP/USD.
#   Research scope specifies BTC/USD, ETH/USD, SOL/USD.
#   This discrepancy must be resolved before optimization resumes.
#   Fix: Item 7.
#
# FAILURE 7 — SHARPE MAXIMUM (2.9286) UNACCOUNTED FOR
#   Evidence: Best recorded improvement is Gen 2126 at Sharpe=2.9232.
#   All-time Sharpe maximum shows 2.9286. The config producing 2.9286
#   has no log entry. It may be a logging artifact or an unrecorded
#   session result. Must be investigated before Gen 2126 restore.
#   Fix: Item 8.

══════════════════════════════════════════════════════════════════════
⚠️  HARD HALT — HUMAN OPERATOR — ALL 20 ITEMS REQUIRED  ⚠️
    DO NOT RESUME AT GEN 12001 UNTIL ALL ITEMS ARE CHECKED
    ITEMS ARE ORDERED BY DEPENDENCY — DO NOT SKIP OR REORDER
    A BOX MAY ONLY BE CHECKED WHEN IMPLEMENTATION IS CONFIRMED
    WORKING BY TEST — NOT MERELY ATTEMPTED
══════════════════════════════════════════════════════════════════════

═══════════════════════════
BLOCK A: INFRASTRUCTURE
(Complete before all other blocks. Nothing else works without this.)
═══════════════════════════

1. [ ] IMPLEMENT DOCUMENT-READ-AND-CHECKSUM AT STARTUP
        Why this is item 1: Every other fix in this document is written
        here. If ODIN does not read this document, no fix survives a
        restart. This is the only item that enables all other items.
        Do not implement any other item until this one passes all tests.

        Implementation requirements (all required, no shortcuts):
        a) ODIN reads THIS FILE (research_program.md or equivalent path)
           as the ABSOLUTE FIRST ACTION of every session — before any
           LLM call, backtest, config load, LOKI action, or log write
           other than the verification log line itself.
        b) Computes SHA-256 of the file contents byte-for-byte.
        c) Compares against the checksum stored in checksum.txt.
           checksum.txt MUST be:
           - A separate file from this document
           - Never auto-updated by ODIN, LOKI, or any automated process
           - Only updatable by a human operator with explicit intent
           - Located at a path that is hardcoded (not configurable)
        d) On match: logs exactly:
             [DOCUMENT_VERIFIED gen=N checksum=HASH]
           as the first line of the session log. Then continues.
        e) On mismatch or missing file: logs exactly:
             [DOCUMENT_FAIL gen=N reason=REASON]
           Then HALTS. Does not run any generation. Does not call LLM.
           Does not load any config. Does not write anything else.

        Mandatory verification tests (all three required before
        checking this box):
        TEST A — Normal operation:
          Run one session. Confirm [DOCUMENT_VERIFIED] is the first
          log line. Confirm the checksum matches checksum.txt.
        TEST B — Corruption detection:
          Add one character to this file temporarily. Run a session.
          Confirm [DOCUMENT_FAIL] appears and NO generation runs.
          Restore the file. Confirm [DOCUMENT_VERIFIED] resumes.
        TEST C — Missing checksum file:
          Rename checksum.txt temporarily. Run a session.
          Confirm [DOCUMENT_FAIL reason=CHECKSUM_FILE_MISSING] appears
          and NO generation runs. Restore checksum.txt.

        Do not check this box until all three tests pass and their
        results are documented in the run log.

2. [ ] FIX DEDUPLICATION CACHE
        Why: Gen 11993, 11995, 11998 are identical. Gen 11781 and 11796
        are identical. The cache is not functioning. Every duplicate
        wastes a full backtest cycle.

        Implementation requirements:
        a) Wipe the existing cache file completely (confirmed corrupted).
        b) Rebuild from scratch with these exact specifications:
           - Fingerprint: SHA-256 of JSON-serialized config with all
             fields present, keys sorted alphabetically, no whitespace
             variation (canonical form)
           - Cache file: persisted to disk after EVERY generation
             (not buffered, not session-end only)
           - Cache loaded from disk at startup, AFTER document
             verification (Item 1), BEFORE any generation runs
           - Check occurs AFTER LLM proposes config, BEFORE backtest
           - On duplicate: log [DUPLICATE gen=N fingerprint=HASH]
             Do NOT run backtest. Do NOT consume generation number.
             Do NOT update incumbent. Do NOT re-enter cache.
           - On new config: run backtest, then add to cache regardless
             of whether result is accepted or disc