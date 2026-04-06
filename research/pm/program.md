```markdown
# FREYA Research Program — v49.0

## Status at Gen 9800
- **Current best (this run):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Historical best (all runs):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Improvements this run (v48.0, 200 gens):** 2 (Gen 9607, Gen 9616)
- **Improvements last 400 gens:** 5
- **Fixed-point collapse:** ACTIVE — thirteenth confirmed collapse (post-9616,
  184 consecutive non-improvements, dominant attractors:
  adj≈2.2867/bets≈17242 [seen 8×],
  adj≈2.287/bets≈17534 [seen 4×],
  adj≈2.2936/bets≈17728 [seen 5×] in last 20 gens)
- **Degenerate outputs last 20 gens:** 1 (Gen 9781 bets=18)
- **Degenerate rate last 20 gens:** 5% (1/20)
- **Gate 1 NOT IMPLEMENTED** — attractor cycling confirmed, 3+ dominant attractors
- **Gate 2 NOT IMPLEMENTED** — degenerate outputs still consuming capacity
- **Gate 3 NOT IMPLEMENTED** — live configs unverified, known mismatch detected
- **Live performance:** 0/24 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
  (five consecutive programs without root cause diagnosis)
- **Config discrepancy CONFIRMED:** Live YAML shows min_edge_pts=0.028; simulation
  best uses min_edge_pts=0.033. This is a known live bug. Fix immediately.
- **Current best config signature:** price_range=[0.11, 0.55], min_edge_pts=0.033,
  max_days=10 (unverified), category=world_events

---

## TERMINAL CONDITION STATEMENT (v49.0)

Gen 9616 produced adj=2.2936 and the system has not improved in 184 generations.
The last 20 generations show pure attractor cycling between three known signatures.
Marginal adj gain rate: ~0.000035/generation. Projected gain for next 100 unguided
generations: 0.001–0.005. This is operationally zero.

The live system has lost 24/24 trades. The probability of this under simulation
assumptions is ~3×10^-21. This is a deterministic bug, not variance.

A KNOWN CONFIG BUG IS NOW VISIBLE: the "Current Best Strategy" YAML block shows
min_edge_pts=0.028, while the simulation best (Gen 9616) uses min_edge_pts=0.033.
The live system may be trading with an inferior, undertested configuration.

**HARD STOP: Do not run Gen 9801 without completing ALL pre-flight items below.**
**This is the fifth consecutive hard stop. Each skipped item has a direct,
  traceable cost in real money lost on live slots.**
**The simulation loop is SUSPENDED until live diagnosis is complete.**

---

## LOCKED BEST CONFIG (verified fields marked, unverified marked explicitly)

```yaml
name: pm_research_best
category: world_events
price_range: [0.11, 0.55]       # VERIFIED (Gen 9616 simulation)
min_edge_pts: 0.033              # VERIFIED (simulation) — LIVE BUG: live shows 0.028
max_days_to_resolve: 10          # UNVERIFIED — ambiguity from v47.0 never resolved
min_liquidity_usd: 100           # ASSUMED — not confirmed from live logs
max_position_pct: 0.1            # ASSUMED
include_keywords: []
exclude_keywords: []
```

---

## PRE-FLIGHT CHECKLIST FOR GEN 9801
*Every item is BLOCKING. Check and timestamp each. No exceptions.*

### A. IMMEDIATE BUG FIX (do first, before any analysis)

- [ ] **A0 — LIVE CONFIG HOTFIX:** The live YAML shows min_edge_pts=0.028.
      The simulation best is min_edge_pts=0.033. This is a confirmed divergence.
      - SSH to mist, kara, thrud
      - Update min_edge_pts to 0.033 on all three slots
      - Restart live traders
      - Confirm running config matches locked best config above
      - Timestamp: ___________
      *Do not proceed to A1 until A0 is complete.*

### B. CONFIG RECONCILIATION (BLOCKING)

- [ ] **B1:** Confirm Gen 9616 exact config from simulation log:
      - price_range: expected [0.11, 0.55]
      - min_edge_pts: expected 0.033
      - max_days_to_resolve: retrieve exact value
      - category: world_events
      
- [ ] **B2:** Re-run Gen 9616 config in simulator → must reproduce
      adj≈2.2936 (±0.001), sharpe≈0.3379 (±0.001), bets≈17728 (±20).
      If not → stop, investigate simulator state.
      
- [ ] **B3:** Resolve max_days_to_resolve ambiguity (carried since v47.0):
      - Run Gen 9616 config with max_days=14 → log adj: ___
      - Run Gen 9616 config with max_days=10 → log adj: ___
      - Correct value is whichever reproduces adj≈2.2936. Document permanently.
      - Resolved value: ___ (10 / 14)
      
- [ ] **B4:** Update LOCKED BEST CONFIG above with all verified values.
      Mark no field as UNVERIFIED after this step.

### C. GATE IMPLEMENTATION (BLOCKING — fifth request, P0 critical)

- [ ] **C1 — Gate 1 (SEEN_CONFIGS):**
      Implement hash-based deduplication.
      Hash key: (category, price_range_low, price_range_high, min_edge_pts,
                 max_days, min_liquidity, tuple(sorted(include_kw)),
                 tuple(sorted(exclude_kw)))
      Logic: if hash in SEEN_CONFIGS → log "CYCLE AVOIDED [hash]", do not simulate,
             do not count as generation, immediately request new proposal.
      Pre-populate with ALL attractor signatures from ATTRACTOR INVENTORY below.
      **Acceptance test:** Feed all 5 attractor configs → all rejected, zero simulations
      run. Log result: [ ] PASS / [ ] FAIL

- [ ] **C2 — Gate 2 (DEGENERATE FILTER):**
      Pre-simulation bets estimate OR post-simulation check:
      If simulated bets < 100 → log "DEGENERATE REJECTED [bets=N]",
      do not update best, do not count as generation, request new proposal.
      Threshold raised to 100 (degenerate outputs seen at 18, 197, 988).
      **Acceptance test:** Feed config known to produce bets < 100 → rejected.
      Log result: [ ] PASS / [ ] FAIL

- [ ] **C3 — Gate 3 (LIVE CONFIG SYNC):**
      After A0 hotfix, verify all slots match locked best config field-by-field.
      Print running YAML from each slot. Diff against locked config. Diff must be empty.
      mist diff empty: [ ]  kara diff empty: [ ]  thrud diff empty: [ ]

- [ ] **C4 — LLM PROMPT UPDATE:**
      Add to proposal prompt:
      "FORBIDDEN (known attractors — do not reproduce): [see ATTRACTOR INVENTORY].
      Do not propose configs within ±0.005 of any attractor's numeric parameters.
      PRIORITY SEARCH REGIONS (in order):
        1. price_range lower bound in [0.05, 0.10] (below current 0.11)
        2. min_edge_pts in [0.025, 0.032] (below current 0.033)
        3. Multi-category: world_events + economics (base rates 12%, 26%)
        4. Asymmetric YES_edge / NO_edge thresholds
        5. max_days_to_resolve in [7, 21]
      Propose ONE change. Output YAML only. No explanation."

### D. LIVE DIAGNOSIS (BLOCKING — five programs without completion, P0 CRITICAL)
*0/24 wins = p < 3×10^-21 under simulation. This is a code bug, not variance.*
*Complete in strict order. Stop at the first confirmed root cause.*

1. [ ] **D1 — Config audit (post-A0):**
       SSH to mist, kara, thrud. Print running YAML.
       Check every field against locked best config. Confirm min_edge_pts=0.033 is live.
       If any other field differs from locked config → document, fix, restart.
       If all fields match → proceed to D2.
       Finding: ___________

2. [ ] **D2 — Market log audit:**
       Retrieve all 24 traded markets. For EACH record:
       - Market title and Polymarket market ID
       - Category assigned by live system
       - market_odds value at time of bet (exact float, 4+ decimal places)
       - Direction bet (YES or NO)
       - Resolved price
       - Win/loss
       Compute:
       (a) % categorized as world_events
       (b) Empirical YES resolution rate
       (c) % where direction was correct ignoring fees
       (d) Mean market_odds at time of bet
       Finding: ___________

3. [ ] **D3 — Base rate audit:**
       Query Polymarket API: all markets tagged world_events resolved in last 90 days.
       Compute empirical YES resolution rate.
       - If empirical rate < 20%: base rate assumption plausible → proceed to D4
       - If empirical rate ≥ 20%: base rate assumption WRONG → the 12% figure
         used in simulation does not match live Polymarket world_events.
         Implication: NO bets are systematically wrong in direction.
         This is a candidate root cause. Document and update base rate.
       Empirical rate: ____%   Finding: ___________

4. [ ] **D4 — API/odds format audit