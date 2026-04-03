```markdown
# FREYA Research Program — Prediction Markets (v31.0)

## Status at Gen 6200
- **Best config:** adj=1.6222, sharpe=0.246, bets=14585 (Gen 5988)
  min_edge_pts=0.054, world_events, liq=50, price=[0.07,0.80], days=14
- **SIMULATION LOOP IS HALTED.** Do not run Gen 6201.
  This is not advisory. It is the correct research decision.
- **Zero gates implemented.** All four gates declared mandatory at Gen 6000
  remain unimplemented at Gen 6200. 200 generations were wasted.
- **Zero live bets placed.** All three slots (mist, kara, thrud) inactive.
- **Deduplication failure confirmed.** ~70% of last 20 gens are duplicates.
- **Guard failure confirmed.** Gen 6194 (bets=0) and Gen 6197 (bets=3)
  reached evaluation. Gen 6192 (sharpe=-0.19, bets=23661) was not blacklisted.
- **Simulation ceiling confirmed by 200 additional null generations.**
  No new information has been produced since Gen 5988.

---

## ROOT CAUSE STATEMENT (v31.0)

Six thousand two hundred generations. One actionable result. Zero live
validation. The research program has demonstrated that it can optimize
a simulation model. It has not demonstrated that the simulation model
corresponds to reality.

**The five root causes from v30.0 remain fully unresolved:**

1. **No deduplication.** ~70% of recent generations re-evaluate known
   configs. Gate 1 was specified in detail at Gen 6000. It was not
   implemented. The LLM proposer has no memory. Without a seen-config
   hash set, it will continue re-proposing the same configs indefinitely.

2. **No guard system.** Bets=0 and bets=3 reached evaluation at Gen 6194
   and Gen 6197. Gen 6192 (sharpe=-0.19, bets=23661) was not blacklisted.
   Gate 2 was specified in detail at Gen 6000. It was not implemented.

3. **No config persistence.** Signal 2 parameters remain unknown. No
   results log exists. Gate 3 was specified in detail at Gen 6000. It was
   not implemented.

4. **No live deployment.** The simulation base rate (world_events=12.0%)
   has never been validated. The strategy may be optimizing a fiction.
   Gate 4 was declared non-deferrable at Gen 6000. It was deferred 200
   more times.

5. **Simulation ceiling is a model artifact.** Fixed base rates + exhausted
   parameter space = adj formula noise floor. Confirmed by 200 null gens.
   New information cannot come from further simulation.

**v31.0 adds a sixth cause:**

6. **The freeze directive was ignored.** The program explicitly stated
   "Do not run Gen 6001 until all four gates log PASS." Gen 6001 through
   Gen 6200 were run anyway. The loop has demonstrated it will not honor
   its own halt conditions. Any future freeze directive must be enforced
   at the execution layer, not the documentation layer.

---

## MANDATORY ACTIONS — ORDERED BY PRIORITY

The loop is HALTED. These actions must be completed in order.
Do not advance to the next action until the current one is verified.

### ACTION 1: Deploy to `mist` (Cannot be deferred)

This is the highest-priority action. Do it before implementing any gates.
Do it before running any simulation. Do it now.

```yaml
# mist — baseline deployment
category: world_events
min_edge_pts: 0.054
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.05
exclude_keywords: []
```

**Verification:** Log `MIST_DEPLOYED timestamp=<utc>` when first bet is placed.
**Target:** 25 resolved bets before any simulation resumes.
**Hard stop:** If `mist` cannot be deployed within the next operational
session, halt the research program entirely and document why deployment
is blocked. The blocker is more important to understand than any
simulation result.

---

### ACTION 2: Implement Gate 1 (Deduplication)

Do not run any simulation generation until this is implemented and tested.

```python
import hashlib, json, os, pickle

SEEN_CONFIGS_PATH = "seen_configs.pkl"

def load_seen_configs():
    if os.path.exists(SEEN_CONFIGS_PATH):
        with open(SEEN_CONFIGS_PATH, "rb") as f:
            return pickle.load(f)
    return set()

def save_seen_configs(seen):
    with open(SEEN_CONFIGS_PATH, "wb") as f:
        pickle.dump(seen, f)

def hash_config(config: dict) -> str:
    canonical = json.dumps(config, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()

SEEN_CONFIGS = load_seen_configs()

def get_next_config(gen_number, grid=None):
    if grid is not None:
        return grid.next()
    for attempt in range(10):
        candidate = llm_propose()
        h = hash_config(candidate)
        if h not in SEEN_CONFIGS:
            SEEN_CONFIGS.add(h)
            save_seen_configs(SEEN_CONFIGS)
            return candidate
        log(f"DEDUP_SKIP gen={gen_number} attempt={attempt} hash={h[:8]}")
    log(f"DEDUP_EXHAUSTED gen={gen_number} — falling back to grid")
    return fallback_grid.next()
```

**Required test (must log GATE1_TEST_PASS before resuming simulation):**
```python
baseline = {"category": "world_events", "min_edge_pts": 0.054,
            "min_liquidity_usd": 50, "price_range": [0.07, 0.80],
            "max_days_to_resolve": 14}
h = hash_config(baseline)
assert h not in SEEN_CONFIGS, "Setup error"
SEEN_CONFIGS.add(h)
candidate = baseline.copy()
assert hash_config(candidate) in SEEN_CONFIGS
log("GATE1_TEST_PASS")
```

**Success criterion:** adj=1.6222 must not appear again after Gate 1 is
active. If it does, log `DEDUP_FAILURE` and fix before continuing.

---

### ACTION 3: Implement Gate 2 (Guard System)

```python
MIN_BETS_FLOOR = 501

def estimate_bets(config) -> int:
    # Fast pre-simulation count using index
    # If unavailable, return MIN_BETS_FLOOR + 1 (conservative pass)
    ...

def run_generation(config, gen_number):
    estimated = estimate_bets(config)
    if estimated <= 500:
        log(f"PRE_SIM_REJECT gen={gen_number} estimated={estimated}")
        return None

    result = simulate(config)

    if result.bets <= 500:
        log(f"POST_SIM_REJECT gen={gen_number} bets={result.bets}")
        return None

    if result.sharpe < -0.01 and result.bets > 10000:
        log(f"NEG_SHARPE_HIGH_VOL gen={gen_number} "
            f"sharpe={result.sharpe} bets={result.bets}")
        blacklist_config(config)
        return None

    persist_result(gen_number, config, result)
    evaluate_and_update(result)
    return result
```

**Required tests (all 8 must log PASS):**
```
T1: estimated=0    → PRE_SIM_REJECT    GATE2_T1_PASS
T2: estimated=499  → PRE_SIM_REJECT    GATE2_T2_PASS
T3: estimated=500  → PRE_SIM_REJECT    GATE2_T3_PASS
T4: estimated=501  → passes to sim     GATE2_T4_PASS
T5: sim bets=0     → POST_SIM_REJECT   GATE2_T5_PASS
T6: sim bets=500   → POST_SIM_REJECT   GATE2_T6_PASS
T7: sim bets=501   → accepted          GATE2_T7_PASS
T8: bets=18700, sharpe=-0.035 → NEG_SHARPE_HIGH_VOL + blacklist
                                        GATE2_T8_PASS
```

---

### ACTION 4: Implement Gate 3 (Config Persistence)

```python
import json, os

RESULTS_PATH = "results_log.jsonl"

def persist_result(gen, config, result):
    if result.adj > 1.0 or result.bets > 5000:
        record = {
            "gen": gen,
            "config_hash": hash_config(config),
            "config": config,
            "bets": result.bets,
            "sharpe": result.sharpe,
            "adj_score": result.adj,
            "roi": getattr(result, 'roi', None),
            "win_rate": getattr(result, 'win_rate', None),
            "timestamp": now_utc()
        }
        with open(RESULTS_PATH, "a") as f:
            f.write(json.dumps(record) + "\n")
        with open(RESULTS_PATH, "r") as f:
            lines = f.readlines()
        verified = json.loads(lines[-1])
        assert verified["config"] == record["config"], "PERSIST_VERIFY_FAIL"
        assert verified["adj_score"] == record["adj_score"], "PERSIST_VERIFY_FAIL"
```

**Required test (must log GATE3_TEST_PASS):**
```python
synthetic = {
    "gen": 5988,
    "config": {"category": "world_events", "min_edge_pts": 0.054,
               "min_liquidity_usd": 50, "price_range": [0.07, 0.80],
               "max_days_to_resolve": 14},
    "bets": 14585, "sharpe": 0.246, "adj_score": 1.6222,
    "roi": 18.199, "win_rate": 77.87,
    "config_hash": hash_config(baseline),
    "timestamp": "2025-01-01T00:00:00Z"
}
with open(RESULTS_PATH, "a") as f:
    f.write(json.dumps(synthetic) + "\n")
with open(RESULTS_PATH, "r") as f:
    verified = json.loads(f.readlines()[-1])
assert verified["adj_score"] == 1.6222
assert verified["config"] == synthetic["config"]
log("GATE3_TEST_PASS")
```

---

## LIVE DEPLOYMENT PLAN

### Slot Assignments

```yaml
# mist — baseline (deploy immediately, see Action 1)
category: world_events
min_edge_pts: 0.054
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.05
exclude_keywords: []

# kara — higher-edge hypothesis (deploy after mist has 10 resolved bets)
category: world_events
min_edge_pts: 0.065
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.05
exclude_keywords: []

# thrud — reserve (deploy after mist has 25 resolved bets)
# Parameters to be determined by live data from mist
```

### Decision Rules at 25 Resolved Bets on `mist`

Record and compare:
- Live sharpe vs. simulation sharpe (0.246)
- Live ROI vs. simulation ROI (18.199%)
- Live win rate vs. simulation win rate (77.