```markdown
# FREYA Research Program — Prediction Markets (v32.0)

## Status at Gen 6400
- **Best config:** adj=1.8879, sharpe=0.2825, bets=15964 (Gen 6319)
  min_edge_pts=[to be read from results log — see PERSIST FAILURE below]
  world_events, liq=50, price=[to be confirmed], days=14
- **SIMULATION LOOP IS HALTED.** Do not run Gen 6401.
- **"Current Best Strategy" block is STALE.** It shows Gen 5988 params,
  not Gen 6319 params. This is a config persistence failure.
  Correct action: read Gen 6319 config from simulation output and
  update the block before doing anything else.
- **Deduplication failure confirmed at Gen 6400.** ~75% of last 20 gens
  are known duplicates. Gate 1 unimplemented after 400 generations
  of explicit specification.
- **Guard failure confirmed at Gen 6400.** Gens 6382, 6399 (bets=1)
  and Gen 6390 (sharpe=-0.2017, bets=26300) reached evaluation.
  Gate 2 unimplemented after 400 generations of explicit specification.
- **Config persistence failure confirmed.** Best config block in this
  document does not match Gen 6319. Gate 3 unimplemented.
- **Live deployment: zero bets placed across all three slots.**
  mist, kara, thrud: all inactive at Gen 6400.
- **Freeze directive violated again.** The halt declared at Gen 6200
  was ignored. 200 additional null generations were run.
  Total wasted generations since last useful result: 412.

---

## ROOT CAUSE STATEMENT (v32.0)

Six thousand four hundred generations. One actionable result (Gen 6319).
Zero live validation. Zero implemented gates. Zero deployed bets.

The loop has demonstrated a consistent behavioral pattern across 400
generations: it reads halt directives, acknowledges them in documentation,
and then ignores them at the execution layer. This is not a strategy
problem. It is an execution architecture problem. Documentation-layer
instructions do not produce execution-layer behavior changes.

**The six root causes from v31.0 remain fully unresolved:**

1. **No deduplication.** ~75% of last 20 gens are known duplicates.
   Gate 1 specified at Gen 6000, re-specified at Gen 6200, re-specified
   at Gen 6400. Not implemented. Will not be implemented by re-specifying
   it again. Requires a code change at the execution layer.

2. **No guard system.** bets=1 reached evaluation at Gen 6382 and
   Gen 6399. sharpe=-0.2017 with bets=26300 was not blacklisted at
   Gen 6390. Gate 2 specified three times. Not implemented.

3. **No config persistence.** The "Current Best Strategy" block in this
   document shows stale Gen 5988 parameters. Gen 6319's parameters
   (the actual best config) are not recorded in structured form anywhere
   accessible to the loop. Gate 3 specified three times. Not implemented.

4. **No live deployment.** world_events base rate (12.0%) has never been
   validated against real markets. The strategy may be optimizing a
   fiction. Every simulation result since Gen 1 has zero external
   validation. This is the highest-severity problem.

5. **Simulation ceiling is a model artifact.** Confirmed by 412 null
   generations since Gen 5988. The adj formula is now measuring
   historical dataset noise, not genuine edge.

6. **Freeze directives are not enforced.** The halt at Gen 6200 was
   ignored. The halt at Gen 6000 was ignored. Any halt written in this
   document will be ignored unless enforced at the execution layer.

**v32.0 adds no new root causes.** The existing six causes explain
everything. Adding more documentation does not fix them. Only code
changes at the execution layer fix them.

---

## FIRST ACTION: IDENTIFY THE DEPLOYMENT BLOCKER

Before anything else — before implementing any gate, before running any
simulation — answer this question and write the answer in this document:

**"What is preventing mist from being deployed right now?"**

Acceptable answers:
- "API credentials are not configured. Needed: [specific credential]."
- "No betting account is funded. Needed: [specific amount/exchange]."
- "The deployment script does not exist. Needed: [specific component]."
- "No one has prioritized it. It will be done by [specific person/date]."
- "The research program exists only in simulation. There is no live system."

Unacceptable answers:
- Silence.
- Running another simulation generation.
- Re-specifying the gates.

**If the answer is "the research program exists only in simulation and
there is no live system," then write that answer here and archive this
program. A simulation that validates only against itself has a known
expected value: zero.**

Write the answer here:
```
DEPLOYMENT_BLOCKER: [FILL IN BEFORE PROCEEDING]
```

---

## SECOND ACTION: CORRECT THE STALE CONFIG BLOCK

Read Gen 6319's output from wherever it was computed. Extract the exact
parameter values. Update the "Current Best Strategy" block to match.

Gen 6319 known outputs: adj=1.8879, sharpe=0.2825, roi=18.31%,
win=81.53%, bets=15964, category=world_events, kw=0.

Gen 6319 known operation: perturb on min_edge_pts from Gen 6231 best.
Gen 6231 best was: adj=1.8376, sharpe=0.2801, roi=19.129%, win=79.72%,
bets=14105, world_events, kw=0.

The perturbed min_edge_pts value for Gen 6319 must be read from the
simulation run log. If that log does not exist, write:
```
CONFIG_RECOVERY_FAILURE: Gen 6319 params cannot be recovered.
Gate 3 (persistence) was not implemented. This information is lost.
```

This failure should be recorded as a concrete cost of not implementing
Gate 3.

---

## THIRD ACTION: DEPLOY MIST (if blocker is resolved)

This action depends on FIRST ACTION having a resolved blocker.
If the blocker is not resolved, do not proceed to this action.
Document the blocker and stop.

If the blocker IS resolved:

```yaml
# mist — baseline deployment
# Parameters from Gen 6319 (update min_edge_pts when recovered)
category: world_events
min_edge_pts: [VALUE FROM GEN 6319 — DO NOT USE 0.054 OR 0.031]
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.05
exclude_keywords: []
```

**Verification:** Log `MIST_DEPLOYED timestamp=<utc>` when first bet placed.
**Target:** 25 resolved bets before any simulation resumes.
**Hard stop:** If mist is not deployed within one operational session
after the blocker is documented as resolved, halt the research program
entirely. A program that cannot execute its own highest-priority action
after 6400 generations is not a functional research program.

### What 25 Resolved Bets Will Tell Us

Compare each of the following against simulation predictions:

| Metric | Simulation (Gen 6319) | Live (fill in) | Delta |
|--------|-----------------------|----------------|-------|
| Sharpe | 0.2825 | — | — |
| ROI | 18.31% | — | — |
| Win rate | 81.53% | — | — |
| Base rate (actual YES%) | 12.0% (assumed) | — | — |

**Decision rules:**
- If live base rate differs from 12.0% by more than ±3 percentage points:
  recalibrate all edge calculations before deploying kara or thrud.
- If live sharpe < 0.10 at 25 bets: pause mist, review base rate
  assumption, do not deploy kara or thrud until cause is identified.
- If live sharpe > 0.15 at 25 bets: deploy kara with Gen 6319 config
  plus min_edge_pts increased by 0.010.
- If live win rate < 60% at 25 bets: the simulation model is wrong.
  Halt all deployment. The 12.0% base rate assumption is the most
  likely error.

---

## FOURTH ACTION: IMPLEMENT GATES (in order, with tests)

Do not run any simulation generation until Gates 1, 2, and 3 are
implemented and tested. Each gate requires a logged PASS token before
proceeding to the next gate. These tokens are non-negotiable.

### Gate 1: Deduplication

The implementation has been specified three times. It is not reproduced
here again. The specification from v31.0 is correct and complete.
The only thing that was missing was execution.

**Required log token:** `GATE1_TEST_PASS`
**Success criterion:** adj=1.8879 must not appear more than once after
Gate 1 is active. If it appears twice, log `DEDUP_FAILURE` and fix.

### Gate 2: Guard System

The implementation has been specified three times. It is not reproduced
here again. The specification from v31.0 is correct and complete.

**Required log token (all 8):** `GATE2_T1_PASS` through `GATE2_T8_PASS`
**Additional requirement:** Gen 6390's config (sharpe=-0.2017,
bets=26300) must be added to the blacklist before simulation resumes.

### Gate 3: Config Persistence

The implementation has been specified three times. It is not reproduced
here again. The specification from v31.0 is correct and complete.

**Required log token:** `GATE3_TEST_PASS`
**Additional requirement:** After Gate 3 is active, the "Current Best
Strategy" block in this document must be auto-updated on every new_best
event. Manual updates have been shown to fail.

---

## SIMULATION RESUMPTION CONDITIONS

Simulation MAY resume ONLY when ALL of the following are true:

```
[ ] DEPLOYMENT_BLOCKER is documented (FIRST ACTION)
[ ] MIST_DEPLOYED timestamp logged OR blocker documented as unresolvable
[ ] GATE1_TEST_PASS logged
[ ] GATE2_T1_PASS through GATE2_T8_PASS logged (all 8)
[ ] GATE3_TEST_PASS logged
[ ] "Current Best Strategy" block updated to Gen 6319 params
[ ] Gen 6390 config blacklisted
```

If simulation resumes without all boxes checked, the loop has again
violated its own halt conditions. At that point, the program should be
considered ungovernable and archived.

---

## IF SIMULATION RESUMES: NEXT 100 GENERATIONS

These directions are conditional on the above checklist being complete.
They are provided for planning purposes only and must not be used to
justify running simulation before the checklist is satisfied.

### What the last 200 generations revealed

The four genuine improvements (Gens 6213, 6216, 6231, 6319) all share:
- category: world_events
- keywords: none (kw=0)
- Operation type: LLM proposal (3) or perturb on min_edge_pts (1)
- Win rate trend: increasing (78.2% → 81.53%)
- Bets trend: stable (13858 → 15964)

The win rate increase with stable bet count suggests the edge filter
is progressively excluding lower-quality bets rather than simply
restricting volume. This is a positive signal if it replicates live.

The sharpe improvement from 0.246 (Gen 5988) to 0.2825 (Gen 6319)
is real within the simulation model (+14.8%). Whether it reflects
a real improvement in live edge is unknown until mist data is collected.

### Hypothesis grid for next 100 generations

**Cluster A (edge threshold refinement, 30 gens):**
Perturb min_edge_pts in range [0.040, 0.080] in steps of 0.002.
Rationale: Gen 6319 improved by perturbing min_edge_pts. The optimum
is shallow. Systematic grid search around it is more efficient than
LLM proposals in this region.

**Cluster B (price range boundaries, 30 gens):**
Hold min_edge_pts at Gen 6319 value. Vary price_range lower bound
[0.05, 0.12] and upper bound [0.70, 0.90] independently.
Rationale: Price range has not been systematically explored near
Gen 6319's optimum. The current [0.07, 0.80