```markdown
# FREYA Research Program — Prediction Markets (v25.0)

## Status at Gen 5000
- **800 generations without improvement** (Gens 4201–5000). Baseline ceiling at
  adj=1.6196 unbroken. LLM proposal loop is confirmed exhausted on current baseline.
- **Config persistence bug UNRESOLVED.** Gens 4796/4797/4799 configs still unknown.
  This is the highest-value unresolved issue in the program. Every generation run
  before fixing persistence risks losing another high-value config permanently.
- **Guard system PARTIALLY BROKEN.** Gen 4996 (bets=0, adj=-1.0) passed through.
  Null-check and post-simulation bets < MIN_BETS_FLOOR reject are NOT implemented.
  Do not declare guard functional until both checks are verified in code.
- **LLM proposal loop: SUSPENDED for next 100 generations.**
  Switching to deterministic grid search for config recovery (Actions 3 and 4).
- **Live slots (mist, kara, thrud): mist CONDITIONALLY ENABLED (see below).**
  kara and thrud remain disabled pending new confirmed config.

## IMMEDIATE ACTIONS REQUIRED (Before Gen 5001)

### ACTION 0: Guard System Fix — BLOCKING, MUST COMPLETE BEFORE ANY GENERATION RUNS
- Gen 4996 (bets=0) passed through to simulation. This is the same gap as Gen 4790.
- The pre_simulation_guard null-check branch is not catching zero-bet configs.
- **IMPLEMENT NOW — two checks required:**
  1. Pre-simulation fast bet estimator: if estimated_bets < MIN_BETS_FLOOR (500),
     reject config before simulation runs. Log as HardReject with reason.
  2. Post-simulation hard reject: if result.bets < MIN_BETS_FLOOR after simulation,
     log HardReject, do NOT update any state, do NOT count as valid generation.
- **Do not run Gen 5001 until both checks are confirmed in code with test cases.**
- Test cases required:
  - Config with expected bets=0 → HardReject pre-simulation
  - Config with expected bets=3 → HardReject pre-simulation
  - Config with expected bets=499 → HardReject pre-simulation
  - Config with expected bets=501 → Pass to simulation

### ACTION 1: Config Persistence Fix — BLOCKING, MUST COMPLETE BEFORE GEN 5001
- Current system only persists configs on new_best events.
- **IMPLEMENT: Persist ALL simulation results where adj > 1.2 OR bets > 5000.**
- Log format (mandatory fields):
  ```
  {gen, config_hash, category, min_edge_pts, price_range, max_days_to_resolve,
   min_liquidity_usd, bets, sharpe, adj_score, roi, win_rate, timestamp}
  ```
- **Retroactive recovery attempt for Gens 4796/4797/4799:**
  - If any generation state or RNG seed is preserved, attempt replay.
  - If not recoverable, document as permanently lost and proceed to grid recovery.
- **Verify persistence is writing to disk** (not memory-only) before proceeding.
- Test: run one simulation, confirm log entry appears in persistent store.

### ACTION 2: Live Slot mist — CONDITIONALLY ENABLE (Baseline Config)
- Baseline config (world_events, min_edge=0.055, min_liquidity=50,
  price_range=[0.07,0.80], max_days=14) is confirmed reproducible 4 times.
- adj=1.6196 > 1.4 unlock threshold. Config is fully logged and verified.
- **DECISION: Enable mist on baseline config immediately.**
  Rationale: 800 generations of stagnation with no live data is worse than
  deploying a confirmed strategy while recovery work continues in simulation.
- kara and thrud remain disabled until a second confirmed config (adj > 1.4)
  is recovered and logged.
- If mist performance diverges significantly from simulation (roi < 10% over
  100+ live bets), disable and flag for calibration review.

### ACTION 3: Gen 4799/4796/4797 Config Recovery — HIGHEST SIM PRIORITY
- **Gens 4796–4799 produced adj 1.50–1.59 with bets 11,500–13,700.**
  This is a different profile from the baseline (14,510 bets) suggesting a
  multi-category union or parameter variant with different market coverage.
- **Recovery grid (deterministic, 75 generation budget):**
  ```
  categories: [
    "world_events+economics",
    "world_events+politics",
    "world_events+economics+politics",
    "economics",
    "politics"
  ]
  min_edge_pts: [0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08]
  price_range: [[0.07,0.80], [0.05,0.90], [0.10,0.75], [0.07,0.90]]
  max_days_to_resolve: [14, 21, 30]
  min_liquidity_usd: [10, 25, 50]
  ```
  Target: configs producing bets ∈ [11000, 14500] with sharpe > 0.23.
  Priority order: world_events+economics first (most likely), then
  world_events+politics, then world_events+economics+politics.
- **If any grid result has adj > 1.4 AND is logged by Action 1 middleware:**
  - Confirm by running identical config a second time (reproduction check).
  - If reproduced: enable live slot kara on that config.
- **If Gen 4799 config recovered with adj confirmed > 1.4:**
  - This is a second independent deployable signal.
  - Enable kara. Document as Signal 2.

### ACTION 4: Clean Solo Tests — Economics and Politics NO-Bias
- **These have never been cleanly run. This is a 5,000-generation gap.**
- Run as part of Action 3 grid but flag results explicitly.
- Economics clean test config:
  ```yaml
  category: economics
  min_edge_pts: 0.055
  min_liquidity_usd: 50
  price_range: [0.07, 0.80]
  max_days_to_resolve: 14
  ```
- Politics clean test config:
  ```yaml
  category: politics
  min_edge_pts: 0.055
  min_liquidity_usd: 50
  price_range: [0.07, 0.80]
  max_days_to_resolve: 14
  ```
- Expected: economics base rate 26% → smaller structural edge than world_events (12%).
  Politics base rate 29.1% → smaller still. Expect lower adj than baseline.
  These are still worth running once to quantify the ceiling for each category.
- Log all results regardless of adj score. These are calibration data points.

### ACTION 5: Gen 4592 Config Recovery — Lower Priority (Post Action 3)
- adj=1.213, sharpe=0.2079, bets=6814
- Hypothesis: economics solo or world_events+economics with tighter params.
- **Budget: 25 generations, run only after Action 3 grid completes.**
- Grid:
  ```
  categories: ["economics", "world_events+economics"]
  min_edge_pts: [0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075]
  price_range: [[0.07,0.80], [0.05,0.85]]
  max_days_to_resolve: [14]
  min_liquidity_usd: [10, 25]
  ```

### ACTION 6: LLM Proposal Loop — Suspension and Redesign
- **LLM proposal loop is SUSPENDED for Gens 5001–5100.**
  800 generations of no improvement confirms the unconstrained loop is
  not generating useful variation from the current baseline.
- **When loop resumes (Gen 5101+), enforce these constraints:**
  1. Proposals MUST change at least one parameter meaningfully
     (not within ±0.005 of current best for continuous params).
  2. Proposals MUST NOT reproduce any config in the blacklist history.
  3. Proposals MUST estimate expected bets before submitting.
     If estimated_bets < MIN_BETS_FLOOR: regenerate (max 3 attempts, then skip).
  4. Proposals that reproduce the baseline config exactly are rejected.
  5. Inject remaining high-priority untested signals as forced proposals
     before allowing free-form LLM generation (see Signal Targets below).

## All-Time Best (Confirmed)
- **Gen 3402/4382/4591/4800/4981–4995/4998–5000:**
  adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510
  ```yaml
  category: world_events
  min_edge_pts: 0.055
  min_liquidity_usd: 50
  price_range: [0.07, 0.80]
  max_days_to_resolve: 14
  exclude_keywords: []
  include_keywords: []
  ```
  CONFIRMED REPRODUCIBLE (multiple independent reproductions).
  **STATUS: BASELINE REFERENCE + LIVE DEPLOYMENT (mist, pending Action 2).**
  Do not tune. Do not inject as a proposal. Do not simulate again unless
  reproducing a specific recovery target.

## High-Value Unconfirmed Configs (adj > 1.4, config unknown)
- **Gen 4799:** adj=1.5865, sharpe=0.2431, bets=13634 — RECOVER PRIORITY 1.
  Likely Gen 4187 match. Config unknown. Recovery via Action 3 grid.
- **Gen 4796:** adj=1.5129, sharpe=0.2368, bets=11895 — RECOVER PRIORITY 2.
  Config unknown. Recovery via Action 3 grid.
- **Gen 4797:** adj=1.5008, sharpe=0.2358, bets=11588 — RECOVER PRIORITY 3.
  Config unknown. Recovery via Action 3 grid.
- **Gen 4187:** adj=1.5865, sharpe=0.2431, bets=13634 — likely = Gen 4799.
- **Gen 4188:** adj=1.5020, sharpe=0.2371, bets=11258 — likely ≈ Gen 4797.
- **Gen 3788:** adj=1.4766, sharpe=0.2235, bets=14771 — CONFIG UNKNOWN. Priority 4.
  Note: bets=14771 is ABOVE baseline bets=14510 — may be a looser price_range
  or lower min_liquidity variant. Include in Action 3 grid sweep.
- **Gen 3786:** adj=1.4665, sharpe=0.2348, bets=10304 — likely ≈ Gen 4796. Priority 2.
- **Gen 4592:** adj=1.213, sharpe=0.2079, bets=6814 — CONFIG UNKNOWN. Priority 5.
- **Gen 4389:** adj=0.0412, sharpe=0.0119, bets=623 — WEAK POSITIVE, log only.

## Key Learnings (Gens 1–5000)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, CEILING adj≈1.62)**
  - Base rate 12% vs. crowd pricing 25–40%.
  - Best config: world_events, no keywords, min_edge=0.055, min_liquidity=50,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458 — repro