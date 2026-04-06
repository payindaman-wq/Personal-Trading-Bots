```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 12201 | Incumbent: Gen 2126 (MUST BE RESTORED — SEE HALT)
# MIMIR-reviewed 2026-04-06 (v9)
#
# ⚠️ CRITICAL HALT — ACTIVE — DO NOT RUN ANY GENERATION
# ⚠️ THIS HALT HAS BEEN ACTIVE SINCE GEN 11001 (1200+ GENERATIONS AGO)
# ⚠️ ZERO COMPLIANCE IN 1200 GENERATIONS — ROOT CAUSE CONFIRMED BELOW
# ⚠️ ESCALATION VIA LOKI PHASE 2 IS NOT WORKING — HUMAN OPERATOR REQUIRED
#
# ══════════════════════════════════════════════════════════════════════
# HALT HISTORY (every reissuance has been ignored — this is evidence,
# not repetition — DO NOT treat this as informational only):
#   Gen 11001 (v2): First halt
#   Gen 11156 (v3): Re-issued — not acted on
#   Gen 11200 (v4): Re-issued — not acted on
#   Gen 11400 (v5): Re-issued — not acted on
#   Gen 11600 (v6): Re-issued — not acted on
#   Gen 11800 (v7): Re-issued — not acted on
#   Gen 12000 (v8): Re-issued — confirmed 1000 generations of zero compliance
#   Gen 12200 (v9): Re-issued — confirmed 1200 generations of zero compliance
#                   LOKI Phase 2 escalations confirmed non-functional
#                   Human operator code changes required — no automation path
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
#   SECONDARY CONFIRMED FAILURE: LOKI Phase 2 escalations are being
#   logged but not implemented. Nine escalations between Gen 9000 and
#   Gen 11800 produced zero confirmed code changes. Do not use LOKI
#   for any item in the checklist below. Human operator must implement
#   all items directly in ODIN source code.
#
# ══════════════════════════════════════════════════════════════════════
# CONFIRMED ACTIVE FAILURES AS OF GEN 12200
# ══════════════════════════════════════════════════════════════════════
#
# FAILURE 1 — DOCUMENT NOT READ AT STARTUP [ROOT CAUSE]
#   Evidence: Zero [DOCUMENT_VERIFIED] or [DOCUMENT_FAIL] lines in any
#   log across 1200 generations (Gen 11001–12200).
#   Impact: All other failures persist. No instruction survives restart.
#   Fix: Item 1 (mandatory first). Must be implemented by human operator
#   directly in ODIN source code. LOKI escalation has been confirmed
#   non-functional for this class of change.
#
# FAILURE 2 — INCUMBENT SLOT CONTAINS CORRUPTED REGIME B CONFIG
#   Evidence: size_pct=15, RSI_long=36.56, stop_loss_pct=2.72,
#   timeout_hours=196 visible in Current Best Strategy.
#   These values entered at Gen 2149 (Sharpe=0.8798, 345 trades).
#   Gen 2149 had LOWER Sharpe than Gen 2126 (0.8798 vs 2.9232) —
#   it should never have replaced the incumbent under any rule.
#   Additionally, Gen 2149 should have been rejected by MAX_TRADES
#   (345 >> 60). The true incumbent is Gen 2126: Sharpe=2.9232,
#   win_rate=90.0%, trades=30.
#   This single corrupt incumbent slot has misdirected ~10,050
#   generations. Regime B optimization ceiling is ~2.55 Sharpe.
#   Regime A peak is 2.9232+. The gap is unbridgeable without restore.
#   Fix: Item 8 (investigate Sharpe anomaly first), then Item 6
#   (restore Gen 2126 exactly).
#
# FAILURE 3 — MAX_TRADES ENFORCEMENT NON-FUNCTIONAL
#   Evidence: Gens 11985 (715 trades), Gen 2149 (345 trades accepted
#   into incumbent slot), entire post-Gen-2149 history showing 345–540
#   trade results accepted without rejection.
#   Fix: Item 3. MAX_TRADES[swing] = 60. Hard reject, no exceptions.
#
# FAILURE 4 — DEDUPLICATION CACHE NON-FUNCTIONAL
#   Evidence (Gen 11001–12200):
#     Gens 12194, 12195: identical Sharpe=2.4226, trades=477
#     Gens 12196, 12197: identical Sharpe=-1.6652, trades=164
#     Gens 11993, 11995, 11998: identical Sharpe=2.4226, trades=477
#     Gens 11781, 11796: identical pair
#   Fix: Item 2. Wipe existing cache. Rebuild from scratch.
#
# FAILURE 5 — MIN_TRADES[swing] HAS BEEN CHANGED 9 TIMES
#   Complete history:
#     Initial: 30 (correct)
#     Gen 6400: 30 (STALL_ALERT change, MIN_TRADES unchanged — OK)
#     Gen 6600: 30 (confirmed correct)
#     Gen 7000: 20 (MISTAKE — opened Regime B attractor)
#     Gen 7200: 10 (WORST CHANGE — fully opened high-frequency basin)
#     Gen 7600: 20 (partial correction — insufficient)
#     Gen 7800: 25 (partial correction — insufficient)
#     Gen 8200: 20 (MISTAKE — regression)
#     Gen 8800: 25 (partial correction — insufficient)
#     Gen 9600: 21 (MISTAKE — arbitrary, insufficient)
#     Gen 10000: 30 (CORRECT — restored)
#   Current value: 30 (correct — do not change under any circumstances)
#   Note: Every value below 30 either caused or failed to prevent
#   entrenchment of the Regime B high-frequency attractor.
#   Fix: Item 4 (lock at 30, make immutable via code constant, not
#   configurable parameter).
#
# FAILURE 6 — PAIRS LIST INCONSISTENT WITH RESEARCH SCOPE
#   Evidence: Current incumbent shows LINK/USD, ADA/USD, BTC/USD,
#   OP/USD. Research scope specifies BTC/USD, ETH/USD, SOL/USD.
#   The LLM is either not receiving the pairs constraint or ignoring it.
#   Fix: Item 7 (enforce pairs list in backtest engine, not just prompt).
#
# FAILURE 7 — SHARPE MAXIMUM (2.9286) UNACCOUNTED FOR
#   Evidence: Best recorded improvement is Gen 2126 at Sharpe=2.9232.
#   All-time Sharpe maximum shows 2.9286. The config producing 2.9286
#   has no log entry. It may be a logging artifact (rounding, float
#   precision), an unrecorded session, or a result from a session that
#   crashed before full log write. Must be investigated before Gen 2126
#   restore — if a better config exists it should be the restore target.
#   Fix: Item 8 (investigate, document conclusion, then proceed to
#   Item 6 regardless of outcome — Gen 2126 restore is the fallback).
#
# FAILURE 8 — IMPROVEMENT LOGIC ACCEPTED LOWER SHARPE AS NEW BEST
#   Evidence: Gen 2149 (Sharpe=0.8798) replaced Gen 2126 (Sharpe=2.9232)
#   as incumbent. This is logically impossible under correct improvement
#   logic (new_best requires strictly higher Sharpe than current best).
#   Root cause unknown — may be floating point comparison error, sign
#   error, or session restart resetting the incumbent tracking variable.
#   Fix: Item 9 (audit and fix improvement comparison logic).
#
# FAILURE 9 — LOKI PHASE 2 ESCALATION IS NON-FUNCTIONAL
#   Evidence: 9 escalations between Gen 9000 and Gen 11800, zero
#   confirmed implementations. This has been the primary attempted
#   remediation pathway and it has failed completely.
#   Fix: Item 10 (disable automatic LOKI escalation for infrastructure
#   changes; route all infrastructure changes to human operator queue
#   with blocking confirmation before next generation runs).
#
# ══════════════════════════════════════════════════════════════════════
# CONFIRMED BEHAVIORAL FACTS ABOUT THE SMALL LLM (llama-3.1-8b-instant)
# ══════════════════════════════════════════════════════════════════════
#
# These are not speculations — they are patterns confirmed across
# thousands of generations:
#
# LLM PATTERN 1 — MICRO-ADJUSTMENT ADDICTION
#   The LLM proposes RSI threshold, stop_loss_pct, and timeout_hours
#   micro-adjustments that move Sharpe by <0.01 while keeping trade
#   counts pinned at 470–530. This is gradient descent in a flat basin.
#   Mitigation: Item 5 (forced exploration directive) and MAX_TRADES
#   enforcement (Item 3) which structurally prevents Regime B