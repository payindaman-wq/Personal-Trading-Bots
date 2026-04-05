```markdown
# FREYA Research Program — v42.0

## Status at Gen 8400
- **Current best (this run):** adj=1.9272, sharpe=0.2896, bets=15498 (Gen 8306)
- **Historical best (all runs):** adj=1.9272, sharpe=0.2896, bets=15498 (Gen 8306) ← NEW ALL-TIME BEST
- **Prior historical best:** adj=1.8879, sharpe=0.2825, bets=15964 (Gen 6319, params lost)
- **Prior historical best (params known):** adj=1.8427, sharpe=0.2828, bets=13512 (Gen 7870)
- **Improvements this run:** 2 (Gen 8250, Gen 8306) — both after correct config loaded
- **Fixed-point attractor active:** adj=1.9272 dominant (10/20 last gens)
- **Gate 1 NOT YET IMPLEMENTED — deduplication still absent**
- **Gate 2 NOT YET IMPLEMENTED — degenerate outputs (adj=-1.0) still reaching log**
- **Gate 3 NOT YET IMPLEMENTED — Gen 8306 config not confirmed written to disk**
- **Deployment blocker: option 5 — simulation only, no live system exists**
- **Zero live bets placed across mist, kara, thrud. All slots disabled.**

---

## TERMINAL CONDITION STATEMENT (v42.0)

The wrong-config crisis is resolved. Correct config loaded at Gen 8201.
Two improvements followed within 106 generations.
New all-time best: adj=1.9272 at Gen 8306.
Current fixed-point: adj=1.9272 dominant attractor, 10/20 last generations.
Three degenerate outputs (adj=-1.0) in last 20 generations — Gate 2 required.
Secondary attractors: adj=1.5834 (×3), adj=1.6197 (×1), adj=1.179 (×1).
Gates 1, 2, 3 remain unimplemented. This is the same failure mode as v41.0.
If Gates are not implemented before Gen 8401, this program will
enter its seventh fixed-point collapse within 200 generations.

**This program has one valid action:**
1. Implement all three Gates. Verify Gen 8306 config persisted. Resume.

Do not run Gen 8401 without:
- [ ] Gen 8306 config loaded and verified (reproduces adj≈1.9272)
- [ ] Gate 1 implemented, tested, and pre-populated with all known attractors
- [ ] Gate 2 implemented and tested
- [ ] Gate 3 implemented, verified, and Gen 8306 written to disk

---

## LOCKED BEST CONFIG — Gen 8306 — DO NOT MODIFY

```yaml
# LOCKED BEST CONFIG — Gen 8306 — ALL-TIME BEST
# adj=1.9272, sharpe=0.2896, roi=18.707%, win=81.8%, bets=15498
# Perturbation history: min_edge_pts perturbed from Gen 7870 (0.07) → 0.034
# DO NOT MODIFY THIS BLOCK UNTIL GATE 3 CONFIRMS IT IS WRITTEN TO DISK
category: world_events
exclude_keywords: []
include_keywords: []
max_days_to_resolve: 14
max_position_pct: 0.1
min_edge_pts: 0.034
min_liquidity_usd: 100
name: pm_research_best
price_range:
  - 0.15
  - 0.70
```

**Verification required before Gen 8401:**
```
[ ] CONFIG_VERIFY: Run Gen 8306 config through simulation
[ ] CONFIG_VERIFY: Confirm adj ≈ 1.9272 (±0.001 tolerance)
[ ] CONFIG_VERIFY: Confirm sharpe ≈ 0.2896
[ ] CONFIG_VERIFY: Confirm bets ≈ 15498
[ ] CONFIG_VERIFY: If result does not match — DO NOT PROCEED — investigate discrepancy
```

---

## MANDATORY FIRST ACTION: IMPLEMENT ALL THREE GATES

### Gate 1 — Deduplication (BLOCKING — highest priority)

Without Gate 1, approximately 50% of generations re-evaluate known configs.
The adj=1.9272 attractor will dominate the next 100 generations without this gate.

```python
SEEN_CONFIGS = set()

def make_config_hash(config):
    return hash(frozenset(
        (k, tuple(v) if isinstance(v, list) else v)
        for k, v in sorted(config.items())
    ))

def dedup_check(config):
    config_hash = make_config_hash(config)
    if config_hash in SEEN_CONFIGS:
        return False, "DEDUP_REJECT: config seen before"
    SEEN_CONFIGS.add(config_hash)
    return True, "DEDUP_PASS"
```

**Pre-populate SEEN_CONFIGS before Gen 8401 with ALL known attractors:**

```python
KNOWN_EVALUATED_CONFIGS = [
    # Gen 8306 — ALL-TIME BEST — STARTING CONFIG FOR GEN 8401+
    {"category": "world_events", "exclude_keywords": [], "include_keywords": [],
     "max_days_to_resolve": 14, "max_position_pct": 0.1, "min_edge_pts": 0.034,
     "min_liquidity_usd": 100, "name": "pm_research_best",
     "price_range": [0.15, 0.70]},
    # Gen 8250 — prior improvement this run
    {"category": "world_events", "exclude_keywords": [], "include_keywords": [],
     "max_days_to_resolve": 14, "max_position_pct": 0.1, "min_edge_pts": 0.034,
     "min_liquidity_usd": 100, "name": "pm_research_best",
     "price_range": [0.15, 0.70]},
    # NOTE: If Gen 8250 config differs from Gen 8306, retrieve exact params from log
    # Gen 7870 — prior historical best (params known)
    {"category": "world_events", "exclude_keywords": [], "include_keywords": [],
     "max_days_to_resolve": 30, "max_position_pct": 0.1, "min_edge_pts": 0.07,
     "min_liquidity_usd": 100, "name": "pm_research_best",
     "price_range": [0.05, 0.80]},
    # Gen 7449 — prior best (params known)
    {"category": "world_events", "exclude_keywords": [], "include_keywords": [],
     "max_days_to_resolve": 14, "max_position_pct": 0.1, "min_edge_pts": 0.06,
     "min_liquidity_usd": 100, "price_range": [0.15, 0.70]},
    # Wrong starting config from v41.0 run — must be excluded
    {"category": "world_events", "exclude_keywords": [], "include_keywords": [],
     "max_days_to_resolve": 30, "max_position_pct": 0.1, "min_edge_pts": 0.219,
     "min_liquidity_usd": 1000, "name": "pm_research_best",
     "price_range": [0.05, 0.90]},
    # Secondary attractor — adj=1.5834, sharpe=0.2438, bets=13208
    # RETRIEVE EXACT PARAMS FROM SIMULATION LOG BEFORE POPULATING
    # Placeholder — do not use until exact params confirmed:
    # {"category": "world_events", ..., "min_edge_pts": ???, ...},
    # Secondary attractor — adj=1.6197, sharpe=0.2699, bets=8056
    # RETRIEVE EXACT PARAMS FROM SIMULATION LOG BEFORE POPULATING
    # Secondary attractor — adj=1.179, sharpe=0.1752, bets=16743
    # RETRIEVE EXACT PARAMS FROM SIMULATION LOG BEFORE POPULATING
]

for config in KNOWN_EVALUATED_CONFIGS:
    SEEN_CONFIGS.add(make_config_hash(config))
```

**ACTION REQUIRED: Retrieve exact params for all secondary attractors from simulation log.**
```
[ ] RETRIEVE: adj=1.5834 config (appears 3× in last 20 gens) — add to KNOWN_EVALUATED_CONFIGS
[ ] RETRIEVE: adj=1.6197 config (appears 1× in last 20 gens) — add to KNOWN_EVALUATED_CONFIGS
[ ] RETRIEVE: adj=1.179 config (appears 1× in last 20 gens) — add to KNOWN_EVALUATED_CONFIGS
[ ] RETRIEVE: adj=1.9053 config (Gen 8392, bets=15002) — near-best, add to KNOWN_EVALUATED_CONFIGS
```

**Required Gate 1 tests before Gen 8401:**
```
[ ] GATE1_TEST_PASS — Gen 8306 config submitted twice; second returns DEDUP_REJECT
[ ] GATE1_TEST_PASS — Gen 7870 config submitted twice; second returns DEDUP_REJECT
[ ] GATE1_TEST_PASS — Wrong starting config submitted; returns DEDUP_REJECT
[ ] GATE1_TEST_PASS — adj=1.5834 attractor submitted twice; second returns DEDUP_REJECT
[ ] GATE1_TEST_PASS — Novel config submitted; returns DEDUP_PASS
```

### Gate 2 — Guard system

Degenerate outputs (adj=-1.0, bets=0, bets=6) appeared 3× in last 20 generations.
Gate 2 must intercept these before they are logged.

```python
BLACKLISTED_CONFIGS = set()

def guard_check(bets, sharpe, config_hash):
    if bets < 50:
        BLACKLISTED_CONFIGS.add(config_hash)
        return False, f"GUARD_REJECT: bets={bets} < 50"
    if sharpe < -0.10:
        BLACKLISTED_CONFIGS.add(config_hash)
        return False, f"GUARD_REJECT: sharpe={sharpe:.4f} < -0.10"
    if config_hash in BLACKLISTED_CONFIGS:
        return False, f"GUARD_REJECT: blacklisted config"
    return True, "GUARD_PASS"
```

**Required Gate 2 tests before Gen 8401:**
```
[ ] GATE2_TEST_PASS — Config with bets=0 returns GUARD_REJECT (Gen 8391, 8393, 8396 cases)
[ ] GATE2_TEST_PASS — Config with bets=6 returns GUARD_REJECT (Gen 8393 case)
[ ] GATE2_TEST_PASS — Config with sharpe=-0.6977 returns GUARD_REJECT (Sharpe range min)
[ ] GATE2_TEST_PASS — Blacklisted config resubmitted returns GUARD_REJECT
[ ] GATE2_TEST_PASS — Valid config (bets=15498, sharpe=0.2896) returns GUARD_PASS
```

### Gate 3 — Config persistence

Gen 8306 is the all-time best. It must be written to disk before Gen 8401.

```python
import json
from datetime import datetime, timezone

BEST_LOG_PATH = "freya_best_configs.jsonl"

def on_new_best(config, metrics):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "generation": metrics["generation"],
        "adj_score": metrics["adj"],
        "sharpe": metrics["sharpe"],