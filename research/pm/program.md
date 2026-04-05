```markdown
# FREYA Research Program — v48.0

## Status at Gen 9600
- **Current best (this run):** adj=2.2867, sharpe=0.3382, bets=17242 (Gen 9591)
- **Historical best (all runs):** adj=2.2867, sharpe=0.3382, bets=17242 (Gen 9591)
- **Improvements this run (v48.0, 200 gens):** 2 (Gen 8413, Gen 9591)
- **Improvements last 400 gens:** 3 (Gen 9018, Gen 9218, Gen 9591)
- **Fixed-point collapse:** ACTIVE — twelfth confirmed collapse (post-9591, 9 consecutive
  non-improvements, dominant attractor adj≈2.2695/bets≈17100 seen 7× in last 20 gens)
- **Degenerate outputs last 20 gens:** 2 (Gen 9590 bets=988, Gen 9593 bets=197)
- **Degenerate rate last 20 gens:** 10% (2/20)
- **Gate 1 NOT IMPLEMENTED** — attractor cycling confirmed, 5+ known attractors dominant
- **Gate 2 NOT IMPLEMENTED** — degenerate outputs still consuming generation capacity
- **Gate 3 NOT IMPLEMENTED** — live configs unverified
- **Live performance:** 0/24 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
  (unchanged from v47.0 — live diagnosis checklist C1–C6 never completed)
- **Config discrepancy v47.0:** max_days_to_resolve 10 vs 14 — STILL UNRESOLVED
- **Current best config signature:** price_range [0.11, 0.55], min_edge_pts=0.033,
  max_days=10 (unverified), category=world_events

---

## TERMINAL CONDITION STATEMENT (v48.0)

Gen 9591 produced adj=2.2867 via price_range lower bound reduction (0.15 → 0.11),
capturing the 0.11–0.15 price zone and increasing bet count by ~2,700 without sharpe
degradation. The system immediately collapsed into its twelfth fixed-point cycle.

The three Gates remain unimplemented after FOUR consecutive research programs (v45–v48).
Live performance is structurally broken (0/24 wins, pure fee drag) with root cause
undiagnosed despite explicit blocking instructions in v45.0, v46.0, and v47.0.

The simulation has reached near-ceiling performance for single-parameter perturbation
in the current neighborhood. The adj gain per 100 generations from unmodified LLM
perturbation is projected at ≈0.000–0.005. The live-simulation gap is total: simulation
shows all-time best while live shows all-time worst. These two facts together indicate
the research program is producing zero real-world value in its current form.

**HARD STOP: Do not run Gen 9601 without completing ALL pre-flight items below.**
**This is the fourth consecutive hard stop. Non-compliance is the root cause of
  accumulated technical debt. Treat every unchecked item as a bug, not a suggestion.**

---

## PRE-FLIGHT CHECKLIST FOR GEN 9601
*All items must be checked and timestamped before resuming simulation.*

### A. CONFIG RECONCILIATION (BLOCKING)
- [ ] **A1:** Confirm Gen 9591 exact config parameters from simulation log:
      - price_range: expected [0.11, 0.55] — confirm exact values
      - min_edge_pts: expected 0.033
      - max_days_to_resolve: retrieve exact value (10 or 14 — still unresolved from v47.0)
      - category: world_events
- [ ] **A2:** Re-run Gen 9591 config in simulator → must reproduce adj≈2.2867 (±0.001),
      sharpe≈0.3382 (±0.001), bets≈17242 (±20). If not → stop, investigate simulator
      state before proceeding.
- [ ] **A3:** Resolve max_days_to_resolve ambiguity (carried from v47.0):
      Run Gen 9591 config with max_days=14 (all else identical) → log adj.
      Run Gen 9591 config with max_days=10 (all else identical) → log adj.
      Whichever reproduces adj≈2.2867 is the correct value. Document permanently.
- [ ] **A4:** Document resolved config in LOCKED BEST CONFIG section below with all
      verified parameter values. Mark unverified fields explicitly.

### B. GATE IMPLEMENTATION (BLOCKING — fourth request, treat as P0 bug)
- [ ] **B1 — Gate 1 (SEEN_CONFIGS):** Implement hash-based deduplication.
      Pre-populate with ALL attractor signatures from ATTRACTOR INVENTORY below.
      Logic: hash(category, price_range, min_edge_pts, max_days, min_liquidity,
      include_keywords, exclude_keywords) → if in SEEN_CONFIGS: skip, log "CYCLE AVOIDED",
      propose new config. Do NOT count skipped configs as generations.
      **Acceptance test:** Feed the 5 known attractor configs → all must be rejected
      before any simulation runs. Log test result here: [ ]
- [ ] **B2 — Gate 2 (DEGENERATE FILTER):** Implement pre-evaluation bets threshold.
      If simulated bets < 50 (raised from 20 — degenerate outputs at 197, 988 indicate
      20 was too low): log "DEGENERATE REJECTED", do not update best, do not count as
      generation, propose new config immediately.
      **Acceptance test:** Feed a config known to produce bets < 50 → must be rejected.
      Log test result here: [ ]
- [ ] **B3 — Gate 3 (LIVE CONFIG SYNC):** Write Gen 9591 config to disk on ALL live
      slots (mist, kara, thrud). SSH to each slot, print running YAML, compare
      field-by-field to Gen 9591 locked config. Log diff output (must be empty).
      Do not resume live trading until confirmed identical on all three slots.
      mist confirmed: [ ]  kara confirmed: [ ]  thrud confirmed: [ ]
- [ ] **B4 — LLM PROMPT UPDATE:** Add to proposal prompt:
      "Known attractors to avoid: [list from ATTRACTOR INVENTORY]. Do not propose
      configs within ±0.01 of any attractor's price_range bounds. Prioritize:
      (1) price_range lower bound in [0.08, 0.11), (2) min_edge_pts in [0.025, 0.033),
      (3) multi-category combinations, (4) asymmetric YES/NO edge thresholds."

### C. LIVE DIAGNOSIS (BLOCKING — never completed, now P0 critical)
*0/24 wins is p < 0.000003 under simulation assumptions. Four programs have passed
without resolving this. The live system is trading real money with a broken strategy.*

**Complete in strict order. Do not skip any step.**

1. [ ] **C1 — Config audit:** SSH to mist, kara, thrud. Print exact running YAML.
       Compare field-by-field to Gen 9591 locked config. Check:
       - category: must be world_events
       - price_range: must be [0.11, 0.55]
       - min_edge_pts: must be 0.033
       - max_days_to_resolve: must match A3 verified value
       - min_liquidity_usd: must be 100
       If ANY field differs → this is the root cause → fix and document what was wrong.
       If all fields match → proceed to C2.

2. [ ] **C2 — Market log audit:** Retrieve all 24 traded markets. For each record:
       - Market title and Polymarket market ID
       - Category assigned by system (live) vs. category on Polymarket UI
       - market_odds value at time of bet (exact float)
       - Direction bet (YES or NO)
       - Resolved price (final)
       - Win/loss
       Compute: (a) fraction categorized as world_events, (b) YES resolution rate,
       (c) fraction where direction was correct ignoring fees.

3. [ ] **C3 — Base rate audit:** If YES resolution rate >> 12%, the live world_events
       universe differs from simulation training data. Specifically:
       - Query Polymarket API for all world_events markets resolved in last 90 days.
       - Compute empirical YES resolution rate.
       - If empirical rate > 20%: the 12% base rate assumption is wrong for live markets.
         This would mean NO bets are systematically wrong — the strategy bets against
         the correct direction on every trade. Document and update base rate.

4. [ ] **C4 — API/odds definition audit:** Confirm the market_odds value the live system
       reads from Polymarket API is:
       - A probability in [0,1] (e.g., 0.15 = 15% chance YES)
       - NOT a decimal odds multiplier (e.g., 6.67 for 15% probability)
       - NOT an order book ask/bid that differs from last trade price
       If definition differs from simulation assumption, edge calculation is inverted
       or scaled incorrectly. Document exact API field name and value format.

5. [ ] **C5 — Fee audit:** Confirm actual Polymarket fee structure.
       - Does Polymarket charge 2% per trade, or a different rate?
       - Is there additional spread cost (bid-ask) beyond the platform fee?
       - For thin-edge bets (edge ≈ 0.033), effective fee may eliminate all edge.
       If total cost > min_edge_pts: every bet is negative EV by construction.

6. [ ] **C6 — Root cause documentation:** Write one sentence stating the confirmed root
       cause of 0/24 wins. Write a remediation plan with specific config or code changes.
       Do not start next live sprint until this is written and reviewed.

### D. DIRECTED PARAMETER SWEEP (complete after A–C, before resuming LLM perturbation)
*Purpose: systematically map the adj surface around Gen 9591 best, replacing blind
 LLM perturbation for the next 50 generations.*

- [ ] **D1 — Lower bound sweep:** Test price_range lower bounds [0.05, 0.07, 0.08,
      0.09, 0.10, 0.11, 0.12, 0.13] with upper bound fixed at 0.55, all else at
      Gen 9591 values. Log adj for each. Identify optimal lower bound.
- [ ] **D2 — Upper bound sweep:** Test price_range upper bounds [0.50, 0.52, 0.53,
      0.54, 0.55, 0.56, 0.57, 0.58] with lower bound fixed at 0.11, all else at
      Gen 9591 values. Log adj for each. Identify optimal upper bound.
- [ ] **D3 — Edge threshold sweep:** Test min_edge_pts [0.020, 0.025, 0.028, 0.030,
      0.033, 0.035, 0.038, 0.040] with price_range fixed at Gen 9591 optimal from D1/D2.
      Log adj for each.
- [ ] **D4 — Asymmetric edge test:** Test separate YES_edge and NO_edge thresholds:
      (YES_edge=0.025, NO_edge=0.033), (YES_edge=0.033, NO_