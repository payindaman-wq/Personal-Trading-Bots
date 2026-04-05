```markdown
# FREYA Research Program — v47.0

## Status at Gen 9400
- **Current best (this run):** adj=2.1573, sharpe=0.3273, bets=14553 (Gen 9218)
- **Historical best (all runs):** adj=2.1573, sharpe=0.3273, bets=14553 (Gen 9218)
- **Improvements this run (v46.0, 200 gens):** 2 (Gen 9214, Gen 9218)
- **Improvements last 400 gens:** 4 (Gen 8802, Gen 9018, Gen 9214, Gen 9218)
- **Fixed-point collapse:** ACTIVE — eleventh confirmed collapse (post-9218, 182 consecutive
  non-improvements)
- **Degenerate outputs last 20 gens:** 2 (Gen 9385 bets=20, Gen 9387 bets=11)
- **Degenerate rate last 20 gens:** 10% (2/20)
- **Gate 1 NOT IMPLEMENTED** — attractor cycling confirmed, 4 known attractors dominant
- **Gate 2 NOT IMPLEMENTED** — degenerate outputs still consuming log capacity
- **Gate 3 NOT IMPLEMENTED** — live configs unverified
- **Live performance:** 0/24 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
- **Config discrepancy:** max_days_to_resolve appears as 10 in Gen 9018 locked config;
  Gen 8802 used 14. Which parameter produced the adj=2.1252 improvement? UNRESOLVED.
- **Current best config signature:** price_range [0.15, 0.56], min_edge_pts=0.033,
  max_days=10 (unverified), category=world_events

---

## TERMINAL CONDITION STATEMENT (v47.0)

Gen 9218 produced adj=2.1573 via price_range upper bound tightening (0.58 → ~0.56).
The system then collapsed into 182 non-improving generations — identical to v45.0 and v46.0.
The three Gates remain unimplemented after three consecutive research programs.
Live performance is structurally broken (0/24 wins, -1.7% to -2.1% PnL = pure fee drag).

The LLM single-parameter perturbation approach has exhausted its productive range in the
current parameter neighborhood. Unmodified continuation of this approach is projected to
produce adj gain ≈ 0.000 per 100 generations.

**HARD STOP: Do not run Gen 9401 without completing ALL pre-flight items below.**

The Gates are not optional. The directed sweep is not optional. Live diagnosis is not optional.
Every generation without Gates 1+2 wastes capacity. Live failure means zero real-world value.

---

## PRE-FLIGHT CHECKLIST FOR GEN 9401
*All items must be checked before resuming. Log completion timestamp for each.*

### A. CONFIG RECONCILIATION (BLOCKING)
- [ ] **A1:** Retrieve Gen 9018 config from disk/log. Confirm price_range upper bound and
      max_days_to_resolve exact value.
- [ ] **A2:** Retrieve Gen 8802 config from disk/log. Confirm max_days_to_resolve=14.
- [ ] **A3:** Re-run Gen 9018 config in simulator → must reproduce adj≈2.1252 (±0.001).
      If not → stop, investigate data or simulator change before proceeding.
- [ ] **A4:** Re-run Gen 8802 config in simulator → must reproduce adj≈2.0877 (±0.001).
- [ ] **A5:** Run Gen 9018 config with max_days=14 (everything else identical) → log adj.
      This resolves whether the 9018 improvement came from price_range or max_days.
- [ ] **A6:** Run Gen 9218 config in simulator → confirm adj≈2.1573, sharpe≈0.3273,
      bets≈14553. Log exact price_range upper bound (expected 0.56 — confirm).
- [ ] **A7:** Document resolved configs in LOCKED BEST CONFIG section below.

### B. GATE IMPLEMENTATION (BLOCKING)
- [ ] **B1 — Gate 1:** Implement SEEN_CONFIGS hash set. Pre-populate with ALL known
      attractor signatures (see ATTRACTOR INVENTORY below). Before evaluating any config,
      hash its parameters and check SEEN_CONFIGS. If found: skip evaluation, log "CYCLE
      AVOIDED", propose new config immediately. Do NOT count skipped configs as generations.
- [ ] **B2 — Gate 2:** Implement pre-evaluation filter. If proposed config produces
      bets < 20 in simulation: log "DEGENERATE REJECTED", do not record to improvement log,
      do not update current best, propose new config immediately. Do NOT count as generation.
- [ ] **B3 — Gate 3:** Write Gen 9218 config to disk on ALL live slots (mist, kara, thrud).
      SSH to each slot and print running config. Compare line-by-line to Gen 9218 locked
      config. Log diff output (must be empty). Do not proceed with live trading until
      confirmed on all three slots.
- [ ] **B4:** Update LLM proposal prompt to include current attractor list and instruct
      model to avoid known-attractor neighborhoods.

### C. LIVE DIAGNOSIS (BLOCKING — complete before any new sprint)
*0/24 wins is p < 0.000003 under simulation assumptions. This is not variance.*

**Investigate in strict order — do not skip:**

1. [ ] **C1 — Config audit:** SSH to mist, kara, thrud. Print exact running YAML config.
       Compare field-by-field to Gen 9218 locked config. Check specifically:
       - category: must be world_events (not sports, crypto, etc.)
       - price_range: must be [0.15, 0.56]
       - min_edge_pts: must be 0.033
       - max_days_to_resolve: must match verified value from A6
       - min_liquidity_usd: must be 100
       If ANY field differs → Gate 3 failure confirmed → fix immediately → log what was wrong.

2. [ ] **C2 — Market log audit:** Retrieve all 24 traded markets (8 per slot). For each record:
       - Market title
       - Category assigned by system
       - market_odds at time of bet
       - Direction bet (YES or NO)
       - Resolved price
       - Whether bet was within price_range [0.15, 0.56]
       Compute: fraction that were world_events; YES resolution rate; fraction where
       direction prediction was correct before fees.

3. [ ] **C3 — Base rate audit:** If YES resolution rate in the 24-market sample >> 12%
       (world_events historical base rate), the live market universe has different
       composition than simulation training data. Document gap. Determine whether
       Polymarket's "world_events" category maps cleanly to simulation's category definition.

4. [ ] **C4 — API/odds audit:** Confirm that market_odds value retrieved from Polymarket
       API is the quantity the simulation assumes (probability in [0,1], last trade price,
       or order book mid). If definition differs from simulation assumption, edge calculation
       is wrong by construction.

5. [ ] **C5 — Fee audit:** Confirm actual fee structure matches simulation's 2% per bet.
       If Polymarket charges spread + platform fee, effective fee may exceed 2%, eliminating
       thin-edge bets.

6. [ ] **C6:** Document root cause and remediation plan before starting next sprint.

---

## LOCKED BEST CONFIG — Gen 9218 — ALL-TIME BEST

```yaml
# LOCKED BEST CONFIG — Gen 9218 — ALL-TIME BEST
# adj=2.1573, sharpe=0.3273, roi=18.489%, win=84.38%, bets=14553
# Improvement over Gen 9018: +0.0321 adj (+1.5%), +0.0055 sharpe, -194 bets
# Key change from Gen 9018: price_range upper bound 0.58 → 0.56 (CONFIRM VIA A6)
# max_days_to_resolve: VERIFY — may be 10 or 14, resolve via A5/A6 before using
# DO NOT MODIFY UNTIL GATE 3 CONFIRMS DISK WRITE ON ALL LIVE SLOTS
category: world_events
exclude_keywords: []
include_keywords: []
max_days_to_resolve: 10  # UNVERIFIED — reconcile via checklist item A5/A6
max_position_pct: 0.1
min_edge_pts: 0.033
min_liquidity_usd: 100
name: pm_research_best
price_range:
  - 0.15
  - 0.56  # CONFIRM — expected from Gen 9214→9218 progression
```

**Verification checksums (complete after A6):**
```
[ ] adj = 2.1573 ± 0.001
[ ] sharpe = 0.3273 ± 0.001
[ ] bets = 14553 ± 10
[ ] price_range upper = 0.56 (CONFIRMED / NOT CONFIRMED — circle one)
[ ] max_days_to_resolve = __ (fill in after A5)
```

**Prior confirmed configs (for reference and Gate 1):**
```yaml
# Gen 9018: adj=2.1252, sharpe=0.3218, roi=18.557%, win=83.98%, bets=14747
price_range: [0.15, 0.58]
min_edge_pts: 0.033
max_days_to_resolve: 10  # unverified
---
# Gen 8802: adj=2.0877, sharpe=0.3155, roi=18.571%, win=83.58%, bets=14924
price_range: [0.15, 0.60]
min_edge_pts: 0.033
max_days_to_resolve: 14
---
# Gen 8801: adj=2.027, sharpe=0.3052, roi=18.855%, win=82.75%, bets=15295
price_range: [0.15, ~0.62–0.63]  # RETRIEVE EXACT VALUE
min_edge_pts: 0.033
max_days_to_resolve: 14
```

---

## ATTRACTOR INVENTORY (Gate 1 SEEN_CONFIGS — pre-populate ALL)

| adj    | sharpe | bets  | Config signature