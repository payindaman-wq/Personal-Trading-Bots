```markdown
# FREYA Research Program — Prediction Markets (v24.0)

## Status at Gen 4800
- **CRITICAL: Improvement detection is functional but config logging is broken.**
  Gen 4799 (adj=1.5865, sharpe=0.2431, bets=13634) and Gen 4796 (adj=1.5129,
  bets=11895) are above live deployment threshold but configs were NOT captured.
  Config persistence must log ALL results with adj > 1.2, not just new_best events.
- **Guard system: PARTIALLY FUNCTIONAL.** bets=84 cluster: 3/20 gens (down from 11/20).
  Gen 4790 (bets=3) slipped through — null-check branch still has gaps.
  Guard is not confirmed fully functional. Do not declare resolved.
- **Gen 4799 = Gen 4187 RECOVERED (tentative).** adj=1.5865, sharpe=0.2431, bets=13634.
  Config unknown — MUST extract before declaring recovered. Priority 1.
- **Gen 4796/4797 configs unknown.** adj=1.5129/1.5008, bets=11895/11588.
  Likely Gen 4188 and Gen 3786 neighborhood. Config extraction Priority 2.
- **Zero new_best improvements in 600 generations** (Gens 4201–4800).
  Baseline ceiling at adj=1.6196 remains unbroken.
- **Live slots (mist, kara, thrud) remain DISABLED.**
  Unlock condition: adj > 1.4 on NEW confirmed+logged config.
  Gen 4799 may qualify — pending config extraction.

## IMMEDIATE ACTIONS REQUIRED (Before Gen 4801)

### ACTION 1: Config Persistence Fix (BLOCKING — HIGHEST PRIORITY)
- Current system only persists configs on new_best events.
- **CHANGE: Persist ALL simulation results where adj > 1.2.**
- Specifically: retroactively attempt to reconstruct configs for Gens 4796, 4797, 4799.
- If reconstruction is impossible, add persistence middleware NOW before Gen 4801.
- Without this fix, every high-value config discovered will be lost again.
- Log format: `{gen, config_hash, category, min_edge, price_range, max_days,
  min_liquidity, bets, sharpe, adj, roi, win_rate}`

### ACTION 2: Guard System — Null-Check Branch Fix
- Gen 4790 (bets=3, adj=-1.0) passed guard and reached simulation.
- Null-check in pre_simulation_guard v23.0 has a gap — category may be set but
  params may produce near-zero bets.
- **ADD: Post-config-generation pre-simulation bet count estimation.**
  If estimated_bets < MIN_BETS_FLOOR (500): reject before simulation runs.
- This requires a fast approximate bet counter (can use category + price_range
  + min_edge to estimate from historical distribution without full simulation).
- Until this is implemented: add explicit check — if result.bets < 500 after
  simulation, log HardReject and do not update any state.

### ACTION 3: Gen 4799/4796/4797 Config Recovery (URGENT)
- Gen 4799: adj=1.5865, sharpe=0.2431, bets=13634 → matches Gen 4187 target exactly.
- Gen 4796: adj=1.5129, sharpe=0.2368, bets=11895 → matches Gen 4188 neighborhood.
- Gen 4797: adj=1.5008, sharpe=0.2358, bets=11588 → matches Gen 3786 neighborhood.
- Recovery method: grid scan targeting bets ∈ [11000,14500] with sharpe > 0.23.
  Grid: {economics, politics, world_events+economics, world_events+politics,
  world_events+economics+politics} × min_edge ∈ [0.04,0.08,step=0.005]
  × price_range ∈ {[0.07,0.80],[0.05,0.90],[0.10,0.75],[0.07,0.90]}
  × max_days ∈ {14,21,30} × min_liquidity ∈ {10,25,50}
- Budget: 75 generation grid (covers ~288 combinations, sample strategically).
- If Gen 4799 config recovered and adj confirmed > 1.4: ENABLE live slot mist.

### ACTION 4: Gen 4592 Config Recovery (Priority 5, lower urgency)
- adj=1.213, sharpe=0.2079, bets=6814
- Hypothesis: economics solo or world_events+economics with tighter params.
- Budget: 25 generations, run after Action 3 grid completes.
- Grid: {economics, world_events+economics} × min_edge ∈ [0.045,0.075,step=0.005]
  × price_range ∈ {[0.07,0.80],[0.05,0.85]} × max_days=14 × min_liquidity ∈ {10,25}

## All-Time Best (Confirmed)
- **Gen 3402/4382/4591/4800:** adj=1.6196, sharpe=0.2458, roi=18.225%,
  win=77.79%, bets=14510
  - category: world_events, min_edge=0.055, min_liquidity=50,
    price_range=[0.07,0.80], max_days=14
  - CONFIRMED REPRODUCIBLE (4 independent reproductions).
  - **BASELINE REFERENCE ONLY. Do not tune. Do not inject. Do not simulate.**
  - Note: v23.0 baseline listed min_liquidity=10; confirmed config uses 50.
    If mismatch found, flag for resolution.

## High-Value Unconfirmed Configs (adj > 1.4, config unknown)
- **Gen 4799:** adj=1.5865, sharpe=0.2431, bets=13634 — **NEW. Likely Gen 4187 match.**
  Config unknown. RECOVER PRIORITY 1. May unlock live deployment.
- **Gen 4796:** adj=1.5129, sharpe=0.2368, bets=11895 — **NEW.**
  Config unknown. RECOVER PRIORITY 2.
- **Gen 4797:** adj=1.5008, sharpe=0.2358, bets=11588 — **NEW.**
  Config unknown. RECOVER PRIORITY 3.
- **Gen 4187:** adj=1.5865, sharpe=0.2431, bets=13634 — likely = Gen 4799. Priority 1.
- **Gen 4188:** adj=1.5020, sharpe=0.2371, bets=11258 — likely ≈ Gen 4797. Priority 3.
- **Gen 3788:** adj=1.4766, sharpe=0.2235, bets=14771 — CONFIG UNKNOWN. Priority 4.
- **Gen 3786:** adj=1.4665, sharpe=0.2348, bets=10304 — likely ≈ Gen 4796. Priority 2.
- **Gen 4592:** adj=1.213, sharpe=0.2079, bets=6814 — CONFIG UNKNOWN. Priority 5.
- **Gen 4389:** adj=0.0412, sharpe=0.0119, bets=623 — WEAK POSITIVE, log only.

## Key Learnings (Gens 1–4800)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, CEILING ~adj=1.62)**
  - Base rate 12% vs. crowd pricing 25–40%.
  - Best config: world_events, no keywords, min_edge=0.055, min_liquidity=50,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458 — reproduced 4 times across 1,400+ gens.
  - **Status: BASELINE REFERENCE ONLY. Do not tune. Do not propose. Do not inject.**

- **Signal 2 — High-Bet Secondary Configs (EMERGING, UNCONFIRMED)**
  - Gens 4796/4797/4799 all produced adj 1.50–1.59, sharpe 0.23–0.24,
    bets 11k–14k. Not world_events baseline (different bets/adj profile).
  - Structural pattern: likely multi-category union with economics or politics,
    or parameter variant producing different market coverage.
  - Config extraction (Action 3) is required to confirm.
  - If confirmed: these represent an independent deployable signal.

- **Signal 3 — Gen 4592 Unidentified Positive (UNCONFIRMED)**
  - adj=1.213, sharpe=0.2079, bets=6814
  - Genuine structural signal at n=6814. Recovery is secondary priority.
  - Hypothesis: economics solo or world_events+economics union, tighter params.

### Confirmed Failures
- **Keyword filters:** 200+ gens, zero improvement. PERMANENTLY SUSPENDED.
- **bets < 500:** universally degenerate. HARD FLOOR enforced.
- **world_events sole-category tuning:** 1,398 gens, zero improvement. SUSPENDED.
- **LLM-proposal loop (unconstrained):** Produces degenerate cycles (bets=84 attractor).
  Constrained prompt required. Do not use default/unconstrained LLM proposals.
- **bets attractor clusters (84, 312, etc.):** Dead zones. Blacklisted.
  Guard partially functional — not fully eliminated.
- **Config persistence on new_best only:** FAILURE MODE CONFIRMED Gen 4796–4799.
  Must persist all adj > 1.2 results.

### Unconfirmed High-Priority Signals (v24.0 targets)
1. **Gen 4799 config extraction** — HIGHEST PRIORITY. adj=1.5865 likely reproducible.
   Target: confirm config, verify reproduction, enable live slot mist if adj > 1.4.
2. **Gen 4796/4797 config extraction** — Priority 2/3. adj 1.50–1.51 range.
3. **Gen 4592 mystery config** — Priority 5. Target bet range 6500–7100. 25 gen budget.
4. **Economics NO-bias (clean test)** — base rate 26%, NEVER CLEANLY RUN.
   Config: category=economics, min_edge=0.055, min_liquidity=50,
   price_range=[0.07,0.80], max_days=14. Run once if grid budget allows.
5. **Multi-category unions** — world_events+economics, world_events+politics,
   world_events+economics+politics — NEVER CLEANLY TESTED.
   Likely candidates for gens 4796/4797/4799 configs.
6. **Politics NO-bias (clean test)** — base rate 29.1%, NEVER CLEANLY TESTED.
   Config: category=politics, min_edge=0.055, min_liquidity=50,
   price_range=[0.07,0.80], max_days=14. Low priority until grid completes.
7. **Crypto** — base rate 31.5%, smallest structural edge, lowest priority.

---

## 🔴 HARD CONSTRAINTS (NON-NEGOTIABLE)

```python
# ABSOLUTE FLOORS
MIN_BETS_FLOOR = 500
MAX_DAYS_MIN = 7
MIN_LIQUIDITY_MAX = 50

# EXPANDED BET COUNT BLACKLIST v24.0
HARD_BLACKLIST_BET_RANGES = [
    (0, 10),       # Zero/near-zero class
    (11, 55),      # Near-zero class (expanded: Gen 4790 bets=3 slipped through)
    (70, 135),     # bets=84 attractor cluster
    (140, 165),    # Legacy attractor neighborhood
    (185, 205),    # Legacy attractor neighborhood
    (260, 325