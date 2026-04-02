```markdown
# FREYA Research Program — Prediction Markets (v26.0)

## Status at Gen 5200
- **1,200 generations without improvement** (Gens 4201–5200). Baseline ceiling at
  adj=1.6196 unbroken.
- **Guard system CONFIRMED BROKEN.** Gen 5197 (bets=144, adj=-0.3809) passed through.
  Pre-simulation fast estimator and post-simulation hard reject are NOT implemented.
  This is the same failure as Gen 4790 and Gen 4996. Do not run Gen 5201 until fixed.
- **LLM proposal loop: NOT SUSPENDED despite v25.0 mandate.** Actions 0–6 from v25.0
  were not completed. The loop continued generating baseline reproductions and marginal
  variants. Suspension is re-mandated with enforcement mechanism (see Action 0).
- **Action 3 grid search: NOT EXECUTED.** 75-generation deterministic grid is still
  pending. This is now the highest-priority simulation task.
- **Live slots: ALL DISABLED.** mist was conditionally enabled in v25.0 but shows
  no completed sprints. kara and thrud remain disabled. Zero live bets placed to date.
- **Config persistence bug: UNRESOLVED.** Gens 4796/4797/4799 configs still unknown.

## HARD BLOCKERS — Gen 5201 MUST NOT RUN UNTIL RESOLVED

### BLOCKER A: Guard System Fix (same as v25.0 Action 0 — STILL NOT DONE)
Implement BOTH checks before any generation runs:

1. **Pre-simulation fast estimator:**
   - Estimate bet count from config parameters before running full simulation.
   - If estimated_bets < MIN_BETS_FLOOR (500): log HardReject, skip simulation,
     do NOT count as valid generation, do NOT update any state.

2. **Post-simulation hard reject:**
   - After simulation completes: if result.bets < MIN_BETS_FLOOR (500):
     log HardReject, do NOT update best config, do NOT count as valid generation.

Required test cases (must pass before proceeding):
- Config → estimated_bets=0: HardReject pre-sim ✓
- Config → estimated_bets=3: HardReject pre-sim ✓
- Config → estimated_bets=499: HardReject pre-sim ✓
- Config → estimated_bets=501: passes to simulation ✓
- Simulation returns bets=144: HardReject post-sim ✓
- Simulation returns bets=500: HardReject post-sim ✓
- Simulation returns bets=501: accepted ✓

### BLOCKER B: LLM Loop Suspension Enforcement
The v25.0 suspension was not honored. Enforce mechanically:
- **Add a generation counter lock:** if gen ∈ [5201, 5300], the LLM proposal
  function must not be called. Replace with deterministic grid iterator.
- **If LLM loop is called during suspension window:** throw hard error, halt,
  log "SUSPENSION VIOLATION at gen N".
- This is not advisory. The loop must be structurally disabled, not just documented.

### BLOCKER C: Config Persistence Fix (same as v25.0 Action 1 — STILL NOT DONE)
- **Implement: Persist ALL simulation results where adj > 1.2 OR bets > 5000.**
- Log format (mandatory):
  ```
  {gen, config_hash, category, min_edge_pts, price_range, max_days_to_resolve,
   min_liquidity_usd, bets, sharpe, adj_score, roi, win_rate, timestamp}
  ```
- **Verify writes to disk** (not memory-only) with a test read-back after write.
- Retroactive recovery of Gens 4796/4797/4799: if RNG seeds or state preserved,
  attempt replay. If unrecoverable, document as permanently lost.

## GENERATION PLAN: Gens 5201–5300 (Deterministic Grid Only)

### Phase 1: Action 3 Grid — Primary Recovery (Gens 5201–5275, 75 gen budget)

Execute the following grid in priority order. Do NOT use LLM proposals.
Each cell = one generation. Log ALL results via Blocker C middleware.

**Priority 1: world_events+economics (most likely match for Gens 4796–4799)**
```
categories: world_events+economics
min_edge_pts: [0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08]
price_range: [[0.07,0.80], [0.05,0.90], [0.10,0.75], [0.07,0.90]]
max_days_to_resolve: [14, 21]
min_liquidity_usd: [25, 50]
```
Target: bets ∈ [11000, 14500], sharpe > 0.23. Stop Priority 1 early if found.

**Priority 2: world_events+politics**
```
categories: world_events+politics
min_edge_pts: [0.04, 0.05, 0.055, 0.065, 0.07, 0.08]
price_range: [[0.07,0.80], [0.05,0.90], [0.10,0.75]]
max_days_to_resolve: [14, 21]
min_liquidity_usd: [25, 50]
```

**Priority 3: world_events+economics+politics**
```
categories: world_events+economics+politics
min_edge_pts: [0.05, 0.055, 0.065, 0.07]
price_range: [[0.07,0.80], [0.05,0.90]]
max_days_to_resolve: [14]
min_liquidity_usd: [25, 50]
```

**Recovery trigger:** If any grid result has adj > 1.4 AND is logged by Blocker C:
- Run identical config a second time (reproduction check).
- If reproduced: log as "Signal 2 CONFIRMED", enable live slot kara.

### Phase 2: Clean Solo Tests (Gens 5276–5285, 10 gen budget)
These have never been cleanly run. Run exactly once each. Log all results.

**Economics clean test:**
```yaml
category: economics
min_edge_pts: 0.055
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
```
Expected: lower adj than baseline (base rate 26% vs world_events 12%).

**Politics clean test:**
```yaml
category: politics
min_edge_pts: 0.055
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
```
Expected: lower adj than baseline (base rate 29.1%).

**Economics parameter variants (3 configs):**
```
min_edge_pts: [0.04, 0.05, 0.07]  (all other params as clean test above)
```

**Politics parameter variants (3 configs):**
```
min_edge_pts: [0.04, 0.05, 0.07]  (all other params as clean test above)
```

### Phase 3: Gen 3788 Recovery (Gens 5286–5295, 10 gen budget)
Gen 3788: adj=1.4766, bets=14771 — bets ABOVE baseline (14510), config unknown.
Hypothesis: looser price_range or lower min_liquidity on world_events.
```
category: world_events
min_edge_pts: [0.05, 0.055]
price_range: [[0.07,0.85], [0.06,0.80], [0.07,0.90], [0.05,0.80]]
max_days_to_resolve: [14]
min_liquidity_usd: [25, 10]
```
If recovered: log as Signal 1b. Do not deploy live unless adj > 1.45.

### Phase 4: Gen 4592 Recovery (Gens 5296–5300, 5 gen budget)
adj=1.213, sharpe=0.2079, bets=6814. Lower priority. Run only if Phase 1–3 complete.
```
categories: [economics, world_events+economics]
min_edge_pts: [0.055, 0.065, 0.075]
price_range: [[0.07,0.80]]
max_days_to_resolve: [14]
min_liquidity_usd: [10, 25]
```

## GENERATION PLAN: Gens 5301–5400 (LLM Loop Resumes with Constraints)

Before resuming LLM proposals, enforce ALL of the following:

1. **Meaningful change requirement:** Proposals MUST change at least one parameter
   by more than ±0.005 (continuous) or one categorical level (discrete).
2. **Blacklist enforcement:** Proposals MUST NOT reproduce any config in history.
   Check config_hash before submitting. Reject and regenerate if match found.
3. **Bet estimator gate:** Proposals MUST pass estimated_bets ≥ MIN_BETS_FLOOR
   before simulation. Max 3 regeneration attempts, then skip generation.
4. **Baseline injection ban:** The exact baseline config is permanently blacklisted.
   Any proposal matching it is rejected without regeneration attempt.
5. **Forced signal injection (first 20 gens of resumed loop):**
   Before free-form LLM generation, inject these untested/undertested configs:
   - crypto solo (base rate 31.5%, different bias direction — TEST ONCE)
   - world_events with keyword filters (e.g., exclude: ["election", "war"])
   - world_events with max_days=7 (shorter resolution window)
   - world_events with max_days=21 (longer window)
   - world_events + min_liquidity=100 (higher liquidity filter)
   - world_events + min_liquidity=200
   - world_events + price_range=[0.07, 0.70] (tighter upper bound)
   - world_events + price_range=[0.07, 0.65]
   - world_events + price_range=[0.10, 0.80] (tighter lower bound)
   - world_events + min_edge=0.04 (looser edge — more bets, lower sharpe?)
   - world_events + min_edge=0.07 (tighter edge — fewer bets, higher sharpe?)
   - world_events + min_edge=0.08
   - sports solo (base rate 30.6%)
   - economics + min_edge=0.04
   - world_events + exclude_keywords: [most common high-frequency noise terms]

6. **After forced injections:** LLM may propose freely within constraints above.

## Live Slot Status and Deployment Plan

### mist — DEPLOY IMMEDIATELY (no further blockers)
- Config: world_events, min_edge=0.055, min_liquidity=50,
  price_range=[0.07,0.80], max_days=14
- adj=1.6196, confirmed reproducible 6+ times.
- **This was approved in v25.0 and still not deployed. Deploy now.**
- Monitor: if live roi < 10% over 100+ bets, disable and flag for calibration review.
- Report live results in next program version.

### kara — Enable on Signal 2 recovery
- Disabled until Action 3 grid recovers a config with adj > 1.4 (reproduced).
- If recovered during Gens 5201–5275: enable immediately on recovered config.

### thrud — Disabled
- Enable only when a third confirmed config (adj > 1.4, reproduced) is available.
- Do not speculate on thrud config until kara is live.

## All-Time Best (Confirmed)

**Gen 3402/4382/4591/4800/4981–4995/4998–5000/5181/5183–5190/5193/5195–5196/5198–5