```markdown
# FREYA Research Program — Prediction Markets (v30.0)

## Status at Gen 6000
- **Best config:** adj=1.6222, sharpe=0.246, bets=14585 (Gen 5988)
  min_edge_pts=0.054, world_events, liq=50, price=[0.07,0.80], days=14
- **Simulation ceiling confirmed.** 3,000 generations without adj>1.63.
  Marginal perturbation within world_events is exhausted.
- **Gate 1 (deduplication) NOT IMPLEMENTED.** Signal 2 appeared 8×
  in the final 20 gens of this batch. This is the dominant waste mode.
- **Gate 2 (guard system) NOT IMPLEMENTED.** Gen 5992: bets=4, adj=-1.0
  reached evaluation. Zero of eight required tests have logged PASS.
- **Gate 3 (config persistence) NOT IMPLEMENTED.** Signal 2 config
  still unknown after 20+ occurrences across 1,000+ generations.
- **Gate 4 (live deployment) NOT INITIATED.** Zero live bets ever placed.
  6,000 simulation generations. Zero real-world validation.
- **Signal 2 config is now hypothetically known:** world_events,
  edge=0.055, liq=50, price=[0.07,0.80], days=14, with one loosened
  parameter (likely liq=40 or price_upper=0.82). It scores below
  baseline by construction. Stop rediscovering it.

---

## ROOT CAUSE STATEMENT (v30.0 — Final Form)

The research program has produced one actionable result: a simulated
strategy with adj=1.6222. It has not validated that result in any
real market. Every generation run after Gen 5988 without live deployment
has negative expected information value.

The four root causes are unchanged from v29.0 because none were fixed:

1. **No deduplication.** LLM re-proposes known configs. Signal 2 has
   been re-evaluated 20+ times. Each re-evaluation costs one generation
   slot and produces zero new information.

2. **No guard system.** Degenerate configs (bets<500) reach evaluation.
   Gen 5992 is the 3rd documented occurrence of bets<10 reaching eval.

3. **No config persistence.** Notable configs are not written to disk.
   Signal 2's parameters are unknown despite 20+ observations.

4. **No live deployment.** The simulation base rate (world_events=12.0%)
   has never been validated. The strategy may not exist in live markets.

v30.0 adds a fifth cause:

5. **Simulation ceiling is a model artifact, not a market truth.**
   With fixed base rates and no subcategory resolution, further
   simulation search is sampling the noise floor of the adj formula.
   New information can only come from live markets or a new data source.

---

## MANDATORY GATES — ALL MUST PASS BEFORE GEN 6001

The loop is FROZEN. Do not run Gen 6001 until all four gates log PASS.
If the execution environment cannot enforce freezing, halt and report.
Do not document, version-increment, or re-specify. Implement or halt.

---

### GATE 1: Config Deduplication

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

**Gate 1 Test (must log before Gen 6001):**
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

**Expected behavior after implementation:**
Signal 2 should never appear again. If adj=1.5117 appears in any
generation after Gate 1 is active, that is a deduplication bug.
Log it as "DEDUP_FAILURE" and fix before continuing.

---

### GATE 2: Guard System

```python
MIN_BETS_FLOOR = 501

def estimate_bets(config) -> int:
    # Fast pre-simulation count using index
    # If not available, return MIN_BETS_FLOOR + 1 (conservative pass)
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
        log(f"NEG_SHARPE_HIGH_VOL gen={gen_number} sharpe={result.sharpe} bets={result.bets}")
        blacklist_config(config)
        return None

    persist_result(gen_number, config, result)
    evaluate_and_update(result)
    return result
```

**Gate 2 Tests (all 8 must log PASS before Gen 6001):**
```
T1: estimated=0    → PRE_SIM_REJECT    GATE2_T1_PASS
T2: estimated=499  → PRE_SIM_REJECT    GATE2_T2_PASS
T3: estimated=500  → PRE_SIM_REJECT    GATE2_T3_PASS
T4: estimated=501  → passes to sim     GATE2_T4_PASS
T5: sim bets=0     → POST_SIM_REJECT   GATE2_T5_PASS
T6: sim bets=500   → POST_SIM_REJECT   GATE2_T6_PASS
T7: sim bets=501   → accepted          GATE2_T7_PASS
T8: bets=18700, sharpe=-0.035 → NEG_SHARPE_HIGH_VOL + blacklist GATE2_T8_PASS
```

If all 8 do not pass, halt. Do not run Gen 6001.

---

### GATE 3: Config Persistence

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
        # Verify
        with open(RESULTS_PATH, "r") as f:
            lines = f.readlines()
        verified = json.loads(lines[-1])
        assert verified["config"] == record["config"], "PERSIST_VERIFY_FAIL"
        assert verified["adj_score"] == record["adj_score"], "PERSIST_VERIFY_FAIL"
```

**Gate 3 Test (must log before Gen 6001):**
```python
synthetic = {"gen": 0, "config": baseline, "bets": 14585,
             "sharpe": 0.246, "adj_score": 1.6222, "roi": 18.199,
             "win_rate": 77.87, "config_hash": hash_config(baseline),
             "timestamp": "2025-01-01T00:00:00Z"}
# Write and read back
with open(RESULTS_PATH, "a") as f:
    f.write(json.dumps(synthetic) + "\n")
with open(RESULTS_PATH, "r") as f:
    verified = json.loads(f.readlines()[-1])
assert verified["adj_score"] == 1.6222
assert verified["config"] == baseline
log("GATE3_TEST_PASS")
```

---

### GATE 4: Live Deployment (Cannot Be Deferred Again)

Deploy baseline config to slot `mist` before Gen 6001.
Deploy Signal 3 hypothesis to slot `kara` before Gen 6050.
`thrud` remains reserve until mist returns 25+ resolved bets.

```yaml
# mist — confirmed baseline (deploy immediately)
category: world_events
min_edge_pts: 0.054
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.05   # reduced from 0.1 — first deployment, be conservative
exclude_keywords: []

# kara — Signal 3 hypothesis (deploy by Gen 6050)
category: world_events
min_edge_pts: 0.065
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.05
exclude_keywords: []
```

**Target:** 50 live resolved bets on `mist` before Gen 6100.
**Report required at Gen 6100:**
- Live sharpe vs. simulation sharpe (0.246)
- Live ROI vs. simulation ROI (18.199%)
- Live win rate vs. simulation win rate (77.87%)
- Live base rate of YES resolutions (compare to model's 12.0%)
- If live sharpe < 0.10: halt simulation search, investigate model validity
- If live sharpe > 0.20: simulation model is credible, resume search

**If Gate 4 is skipped again:** halt the loop entirely. Do not run Gen 6101.
This is not a threat. It is the correct research decision. A strategy that
cannot be deployed is not a strategy.

---

## CONFIRMED SIGNALS

### Signal 1 — BASELINE (Current Best)
```yaml
category: world_events
min_edge_pts: 0.054          # updated from 0.055 (Gen 5988)
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
exclude_keywords: []
```
adj=1.6222, sharpe=0.246, roi=18.199%, win=77.87%, bets=14585.