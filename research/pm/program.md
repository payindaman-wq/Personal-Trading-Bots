```markdown
# FREYA Research Program — Prediction Markets (v33.0)

## Status at Gen 6600
- **Best config:** adj=1.8879, sharpe=0.2825, bets=15964 (Gen 6319)
- **SIMULATION LOOP IS HALTED.** Do not run Gen 6601.
- **Zero improvements in 281 generations** (Gen 6320 through Gen 6600).
- **All three gates remain unimplemented** at Gen 6600.
- **Zero live bets placed** across mist, kara, thrud.
- **Halt directives violated:** Gen 6200 halt ignored (200 gens).
  Gen 6400 halt ignored (200 gens). Gen 6600 halt is the third.
  If this halt is also ignored, archive the program.

---

## TERMINAL CONDITION STATEMENT (v33.0)

This program has produced one actionable result in 6600 generations.
It has validated that result zero times against live markets.
It has implemented zero of three specified architectural gates.
It has placed zero bets.

The simulation ceiling is confirmed. The adj formula cannot improve
beyond ~1.89 on the current dataset with the current model. 281
consecutive null generations is not a sampling artifact — it is the
ceiling. Additional simulation generations will not change this.

**The program is at a decision point with exactly two valid outcomes:**

**Outcome A: Deploy and validate.**
Answer the deployment blocker question. Deploy mist. Collect 25 bets.
Then — and only then — resume simulation with gates implemented.

**Outcome B: Archive.**
If the deployment blocker cannot be resolved (e.g., "this is a
simulation with no live system"), write that answer here and close
the program. A simulation that validates only against itself has
known expected value: zero.

There is no Outcome C (run more simulation without deploying).
Outcome C has been executed for 281 generations. Its result is known.

---

## MANDATORY FIRST ACTION: DEPLOYMENT BLOCKER

**Answer this question before any other action:**

> "What is preventing mist from being deployed right now?"

Write the answer here:
```
DEPLOYMENT_BLOCKER: [FILL IN — THIS IS THE ONLY REQUIRED ACTION AT GEN 6600]
```

**Acceptable answers (verbatim examples):**
- "API credentials not configured. Required: [exchange] API key + secret."
- "No funded account. Required: [$X on exchange Y]."
- "Deployment script does not exist. Required: [specific component]."
- "No one has prioritized it. Will be done by [person] on [date]."
- "This program exists only in simulation. There is no live system."

**If the answer is the last option:** Write it, log
`PROGRAM_ARCHIVED timestamp=<utc>`, and stop. Do not run Gen 6601.

**If the answer is any other option:** Document the specific resolution
path and proceed to SECOND ACTION. Do not run Gen 6601.

**If this field is left blank and Gen 6601 is run:** The program has
violated its own halt condition three consecutive times and should be
treated as ungovernable. Archive it.

---

## SECOND ACTION: PARAMETER RECOVERY

Gen 6319 is the only result worth deploying. Its parameters must be
confirmed before deployment.

**Known outputs:** adj=1.8879, sharpe=0.2825, roi=18.31%,
win=81.53%, bets=15964, category=world_events, kw=0.

**Known context:** Gen 6319 perturbed min_edge_pts from Gen 6231.
Gen 6231: adj=1.8376, sharpe=0.2801, bets=14105, world_events, kw=0.
Gen 6319 increased bets from 14105 to 15964, suggesting min_edge_pts
was decreased (lower threshold = more qualifying bets).

**Recovery instruction:**
Search the simulation run log for Gen 6319. Extract min_edge_pts.
If the log exists, record it:
```
GEN6319_MIN_EDGE_PTS: [VALUE FROM LOG]
GEN6319_PRICE_RANGE: [VALUE FROM LOG]
GEN6319_DAYS: [VALUE FROM LOG — likely 14]
GEN6319_LIQUIDITY: [VALUE FROM LOG — likely 50]
```

If the log does not exist:
```
CONFIG_RECOVERY_FAILURE: Gen 6319 min_edge_pts is unrecoverable.
Gate 3 was not implemented. Cost: unknown min_edge_pts for best config.
Fallback: use min_edge_pts=0.028 (estimated from bet count increase
from Gen 6231's value, direction confirmed by bets 14105→15964).
This is an estimate. Live calibration will be required.
```

**Update the Current Best Strategy block after completing this action.**

---

## THIRD ACTION: IMPLEMENT GATE 2 (GUARD SYSTEM)

This is the highest-leverage code change available. It eliminates
the bets=1, bets=6, sharpe<0 failure class that consumed ~15% of
recent generations. It must be implemented before simulation resumes.

**Gate 2 implementation (execution layer — not documentation):**

```python
# Add to simulation evaluation loop, BEFORE adj_score calculation
def guard_check(bets, sharpe, config_hash):
    # Minimum viability
    if bets < 50:
        return False, f"GUARD_REJECT: bets={bets} < 50"
    if sharpe < -0.10:
        return False, f"GUARD_REJECT: sharpe={sharpe} < -0.10"
    # Blacklist (add Gen 6390: sharpe=-0.2017, bets=26300)
    if config_hash in BLACKLISTED_CONFIGS:
        return False, f"GUARD_REJECT: blacklisted config"
    return True, "GUARD_PASS"
```

**Test requirements:**
- Submit a config known to produce bets=1. Confirm rejection logged.
- Submit a config known to produce sharpe=-0.9551. Confirm rejection.
- Submit Gen 6319 config. Confirm it passes.

**Required log token:** `GATE2_T1_PASS` through `GATE2_T3_PASS`
(minimum 3 tests; add more if available from v31.0 spec)

**Do not proceed to Gate 1 until these tokens are logged.**

---

## FOURTH ACTION: IMPLEMENT GATE 1 (DEDUPLICATION)

~50% of last 20 generations are confirmed duplicates. This wastes
compute and inflates generation counts without producing information.

**Gate 1 implementation (execution layer):**

```python
# Maintain a set of seen config hashes
SEEN_CONFIGS = set()

def dedup_check(config):
    config_hash = hash(frozenset(config.items()))
    if config_hash in SEEN_CONFIGS:
        return False, f"DEDUP_REJECT: config seen before"
    SEEN_CONFIGS.add(config_hash)
    return True, "DEDUP_PASS"
```

**Test requirement:**
- Submit Gen 6319 config twice. Second submission must be rejected.
- Confirm `DEDUP_FAILURE` is not logged before `GATE1_TEST_PASS`.

**Required log token:** `GATE1_TEST_PASS`

---

## FIFTH ACTION: IMPLEMENT GATE 3 (CONFIG PERSISTENCE)

The stale config block problem has recurred at Gen 5988, Gen 6319,
and now Gen 6600. Manual updates fail. Automation is required.

**Gate 3 implementation (execution layer):**

```python
# On every new_best event, auto-write to program.md
def on_new_best(config, metrics):
    block = f"""
## Current Best Strategy
```yaml
category: {config['category']}
exclude_keywords: {config['exclude_keywords']}
max_days_to_resolve: {config['max_days_to_resolve']}
max_position_pct: {config['max_position_pct']}
min_edge_pts: {config['min_edge_pts']}
min_liquidity_usd: {config['min_liquidity_usd']}
name: pm_research_best
price_range:
- {config['price_range'][0]}
- {config['price_range'][1]}
# adj={metrics['adj']}, sharpe={metrics['sharpe']},
# bets={metrics['bets']}, gen={metrics['gen']}
```"""
    update_program_md(block)
    log(f"GATE3_PERSIST gen={metrics['gen']} adj={metrics['adj']}")
```

**Required log token:** `GATE3_TEST_PASS`

---

## SIXTH ACTION: DEPLOY MIST

**Prerequisite:** DEPLOYMENT_BLOCKER documented and resolved.
**Prerequisite:** Gen 6319 parameters recovered or estimated.

```yaml
# mist — baseline deployment (v33.0)
category: world_events
min_edge_pts: [VALUE FROM GEN6319_MIN_EDGE_PTS or 0.028 if recovery failed]
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.05
exclude_keywords: []
```

**Log:** `MIST_DEPLOYED timestamp=<utc>` when first bet is placed.
**Target:** 25 resolved bets before simulation resumes.
**Hard stop:** If mist is not deployed within one operational session
after this action is reached, archive the program.

### Validation Table (fill in as bets resolve)

| Metric       | Simulation (Gen 6319) | Live (fill in) | Delta | Status |
|--------------|-----------------------|----------------|-------|--------|
| Sharpe       | 0.2825                | —              | —     | —      |
| ROI          | 18.31%                | —              | —     | —      |
| Win rate     | 81.53%                | —              | —     | —      |
| YES base rate| 12.0% (assumed)       | —              | —     | —      |

### Decision Rules at 25 Bets

| Condition | Action |
|-----------|--------|
| Live YES base rate differs from 12.0% by >±3 pts | Recalibrate all edge thresholds before deploying kara/thrud |
| Live sharpe < 0.10 | Pause mist. Review 12.0% assumption. Do not deploy kara/thrud. |
| Live sharpe > 0.15 | Deploy kara with Gen 6319 config + min_edge_pts +0.010 |
| Live win rate < 60% | Halt all deployment. Simulation model is wrong. |
| Live win rate > 75% | Simulation is replicating. Proceed with kara deployment. |

---

## SIMULATION RESUMPTION CHECKLIST

Simulation MAY resume ONLY when ALL boxes are checked:

```
[ ] DEPLOYMENT_BLOCKER documented (specific answer, not silence)
[ ] MIST_DEPLOYED logged OR program archived as simulation-only
[ ] GATE2_T1_PASS logged
[ ] GATE2_T2_PASS logged
[ ] GATE2_T3_PASS logged
[ ] GATE1_TEST_PASS logged
[ ] GATE3_TEST_PASS logged
[ ] Current Best Strategy block updated to Gen 6319 actual params
[ ] Gen 6390 config (sharpe=-0.2017, bets=26300) blacklisted
[ ] 25 mist bets resolved (OR program archived)
```

**If simulation resumes with any box unchecked:** The program has
violated its halt conditions three consecutive times and is ungovernable.
Archive it. Do not write v34.0.

---

## IF ALL CHECKLIST ITEMS PASS: NEXT 100 GENERATIONS

These directions are conditional on the checklist being complete.
They must not be used to justify running simulation before that point.

### What the convergence pattern reveals

The four genuine improvements share: world_events, kw=0, improving
win rate (78.2%→81.53%), stable