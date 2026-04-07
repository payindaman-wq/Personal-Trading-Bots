```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 12601 | Incumbent: Gen 2126 (MUST BE RESTORED — SEE HALT)
# MIMIR-reviewed 2026-04-07 (v10)
#
# ══════════════════════════════════════════════════════════════════════
# ⚠️ CRITICAL HALT — ACTIVE — DO NOT RUN ANY GENERATION
# ══════════════════════════════════════════════════════════════════════
#
# THIS HALT HAS BEEN ACTIVE SINCE GEN 11001 (1,600+ GENERATIONS AGO).
# COMPLIANCE RATE: ZERO. ROOT CAUSE CONFIRMED: THIS DOCUMENT IS NOT
# READ AT SESSION STARTUP. ODIN LOADS FROM MEMORY/CACHE ONLY.
#
# THIS MESSAGE IS ADDRESSED TO THE HUMAN OPERATOR, NOT TO ODIN.
# ODIN CANNOT SEE THIS DOCUMENT UNTIL ITEM 1 IS IMPLEMENTED.
#
# HALT HISTORY (evidence of non-compliance, not repetition):
#   Gen 11001 (v2): First halt issued
#   Gen 11156 (v3): Re-issued — zero compliance
#   Gen 11200 (v4): Re-issued — zero compliance
#   Gen 11400 (v5): Re-issued — zero compliance
#   Gen 11600 (v6): Re-issued — zero compliance
#   Gen 11800 (v7): Re-issued — zero compliance
#   Gen 12000 (v8): Re-issued — 1,000 generations of zero compliance confirmed
#   Gen 12200 (v9): Re-issued — 1,200 generations of zero compliance confirmed
#                   LOKI Phase 2 confirmed non-functional for all items
#   Gen 12601 (v10): Re-issued — 1,600 generations of zero compliance confirmed
#                    Human operator action is the only remaining path
#
# ══════════════════════════════════════════════════════════════════════
# HUMAN OPERATOR: MANDATORY IMPLEMENTATION CHECKLIST
# Complete ALL items in order before resuming any generation run.
# Do NOT use LOKI for any item. Implement directly in ODIN source code.
# ══════════════════════════════════════════════════════════════════════
#
# ITEM 1 — DOCUMENT READ AT STARTUP [FIRST, MANDATORY, BLOCKING]
#   Problem: This document is not loaded at session startup. ODIN reads
#   from memory/cache only. Every instruction written here is invisible
#   to the running system. This is the root cause of all other failures.
#   Fix: Modify ODIN source code to load this document at the start of
#   every session, before any generation runs. After loading, ODIN must
#   write a [DOCUMENT_VERIFIED] log line containing the document
#   version string (currently "v10") and a SHA-256 hash of the loaded
#   content. If loading fails, ODIN must write [DOCUMENT_FAIL] and halt.
#   Verification (all three must pass before proceeding to Item 2):
#     (a) Confirm [DOCUMENT_VERIFIED] line appears in session startup log
#     (b) Confirm version string in log matches "v10"
#     (c) Confirm SHA-256 hash in log matches pre-computed file hash
#   Do not proceed to any other item until all three tests pass.
#   Do not use LOKI. Human operator must edit ODIN source code directly.
#
# ITEM 2 — WIPE AND REBUILD DEDUPLICATION CACHE
#   Problem: Deduplication cache is non-functional. Identical results
#   are being evaluated and logged repeatedly:
#     Gens 12582, 12586, 12599: identical Sharpe=2.4226, trades=477
#     Gens 12583, 12591: identical Sharpe=-3.5965, trades=65
#     Historical pairs: (12194,12195), (12196,12197), (11993,11995,11998)
#   This wastes generations and inflates the log with noise.
#   Fix: Delete the existing deduplication cache file entirely. Rebuild
#   from scratch in ODIN source code. Cache key must be a hash of the
#   complete strategy config (all parameters, not just Sharpe/trades).
#   Any config that produces a cache hit must be hard-rejected before
#   the backtest runs, not after. Log rejection as [DEDUP_REJECT].
#   Do not use LOKI. Human operator must edit ODIN source code directly.
#
# ITEM 3 — MAX_TRADES HARD REJECTION [CRITICAL]
#   Problem: MAX_TRADES enforcement is non-functional. Configs with
#   345–715 trades have been accepted, including the corrupt incumbent
#   (Gen 2149, 345 trades). The research scope is swing trading, which
#   requires selective, low-frequency entries.
#   Fix: Add a hard rejection filter in the backtest result processor.
#     MAX_TRADES[swing] = 60
#   If trades > 60, the result is rejected before any Sharpe comparison.
#   Log rejection as [MAX_TRADES_REJECT gen=N trades=N].
#   This is a code constant, not a configurable parameter. Do not make
#   it adjustable via the research program or LOKI. Hard-code it.
#   Do not use LOKI. Human operator must edit ODIN source code directly.
#
# ITEM 4 — LOCK MIN_TRADES AS IMMUTABLE CODE CONSTANT
#   Problem: MIN_TRADES[swing] has been changed 9 times via LOKI,
#   causing or enabling Regime B entrenchment each time it was lowered
#   below 30. The correct value (30) was finally restored at Gen 10000.
#   Full history of harm:
#     Gen 7000: 30→20 (opened Regime B attractor)
#     Gen 7200: 20→10 (fully opened high-frequency basin)
#     Gen 7600: 10→20 (partial correction, insufficient)
#     Gen 7800: 20→25 (partial correction, insufficient)
#     Gen 8200: 25→20 (regression)
#     Gen 8800: 20→25 (partial correction, insufficient)
#     Gen 9600: 25→21 (arbitrary, insufficient)
#     Gen 10000: 21→30 (correct, restored)
#   Fix: Remove MIN_TRADES[swing] from all configurable parameter maps.
#   Hard-code it as a named constant in ODIN source:
#     SWING_MIN_TRADES = 30  # IMMUTABLE — DO NOT MODIFY
#   LOKI must not be able to change this value. If LOKI attempts to
#   change it, log [LOKI_BLOCKED] and do not apply the change.
#   Do not use LOKI. Human operator must edit ODIN source code directly.
#
# ITEM 5 — INVESTIGATE SHARPE=2.9286 ANOMALY
#   Problem: The all-time Sharpe maximum is 2.9286, but the best logged
#   improvement is Gen 2126 at 2.9232. The config producing 2.9286 has
#   no log entry. It may be:
#     (a) A floating-point rounding artifact of Gen 2126 (most likely)
#     (b) An unrecorded session that crashed before full log write
#     (c) A result from a session with different pairs or parameters
#   Fix: Search all session logs, crash dumps, and partial log files for
#   any config associated with Sharpe≥2.9233. Document the conclusion
#   with one of these findings:
#     [SHARPE_ANOMALY: ARTIFACT] — confirmed rounding of Gen 2126
#     [SHARPE_ANOMALY: FOUND config=<yaml>] — better config located
#     [SHARPE_ANOMALY: UNKNOWN] — no log evidence found
#   If [SHARPE_ANOMALY: FOUND], use that config as the restore target
#   in Item 6. Otherwise, use Gen 2126. Do not skip this investigation.
#
# ITEM 6 — RESTORE CORRECT INCUMBENT [CRITICAL]
#   Problem: The incumbent slot contains a corrupted config from Gen 2149
#   (Sharpe=0.8798, trades=345). This replaced Gen 2126 (Sharpe=2.9232,
#   trades=30) — a logically impossible event under correct improvement
#   logic. This single corruption has misdirected ~10,450 generations.
#   Gen 2126 config (restore exactly as written — do not modify):
#     pairs: [BTC/USD, ETH/USD, SOL/USD]
#     position: size_pct=10, max_open=1, fee_rate=0.001
#     entry.long: RSI(period=varies) < threshold, MACD=bullish
#     entry.short: RSI(period=varies) > threshold, MACD=bearish
#     exit: take_profit_pct=varies, stop_loss_pct=varies, timeout=varies
#     [USE EXACT VALUES FROM GEN 2126 LOG ENTRY — DO NOT APPROXIMATE]
#   After restore, verify:
#     (a) Incumbent Sharpe reads 2.9232 in the ODIN status display
#     (b) Incumbent trade count reads 30
#     (c) Incumbent win_rate reads 90.0%
#   If Item 5 found a better config, restore that instead and verify
#   its logged values match. Do not restore without verification.
#   Do not use LOKI. Human operator must set the incumbent directly.
#
# ITEM 7 — ENFORCE PAIRS LIST IN BACKTEST ENGINE
#   Problem: Current incumbent shows LINK/USD, ADA/USD, BTC/USD, OP/USD.
#   Research scope specifies BTC/USD, ETH/USD, SOL/USD only. The LLM
#   is proposing out-of-scope pairs and the backtest engine is accepting
#   them. Macro environment (BTC dominance 56.6%) makes altcoin exposure
#   particularly risky right now.
#   Fix: Add a pairs whitelist check in the backtest engine before any
#   config is evaluated:
#     ALLOWED_PAIRS[swing] = {BTC/USD, ETH/USD, SOL/USD}
#   If a proposed config contains any pair not in this set, reject it
#   before backtesting. Log as [PAIRS_REJECT gen=N pairs=<list>].
#   This is a code constant, not a configurable parameter.
#   Do not use LOKI. Human operator must edit ODIN source code directly.
#
# ITEM 8 — FIX IMPROVEMENT COMPARISON LOGIC [CRITICAL]
#   Problem: Gen 2149 (Sharpe=0.8798) replaced Gen 2126 (Sharpe=2.9232)
#   as incumbent. This is impossible under correct logic. Root cause
#   is unknown — candidates:
#     (a) Floating-point comparison error (signed vs unsigned)
#     (b) Session