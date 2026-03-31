```markdown
# FREYA Research Program — Prediction Markets (v8.0)

## Objective
Find prediction market filter strategies that maximize risk-adjusted ROI by identifying
market categories and keyword buckets where crowd prices are systematically miscalibrated
vs. historical resolution rates.

## Simulator
- 300k+ resolved Polymarket/Kalshi/Manifold markets
- Category base rates: sports=30.6%, politics=29.1%, crypto=31.5%, economics=26.0%,
  world_events=12.0%
- Bet: if market_odds > base_rate + min_edge_pts -> bet NO;
       if market_odds < base_rate - min_edge_pts -> bet YES
- Fee: 2% per bet
- Fitness: adj_score = sharpe x log(n_bets/20 + 1)

---

## 🚨 PRIORITY ZERO — ADOPTION LOGIC BROKEN AGAIN (AS OF GEN 1009) 🚨

### What Happened (Third Recurrence)
- Gen 1009 correctly logged adj=1.7474 as [new_best] ✅
- Gens 1184–1198 show both adj=1.7474 AND adj=1.7424 logged as [no_improvement] ❌
- This proves Gen 1009's adoption wrote to a local variable, not the persisted store
- current_best_adj in the persisted store was NEVER updated from 1.7424
- The proposer is reading the stale persisted value (1.7424) and cycling between
  the two known attractors

### MANDATORY FIXES — DO NOT PROCEED TO GEN 1201 WITHOUT COMPLETING ALL

**Fix 1: Persistent Store**
- current_best_adj MUST be stored in a file (e.g., `best_adj.json`)
- Format: `{"adj": 1.7474, "gen": 1009, "config": {...full YAML...}}`
- Every read of current_best_adj MUST load from this file
- Every write (adoption) MUST write to this file AND fsync before continuing
- NEVER cache current_best_adj in memory between generations

**Fix 2: Atomic Adoption**
```python
# REQUIRED ADOPTION PSEUDOCODE (implement exactly)
def maybe_adopt(proposed_adj, proposed_config, gen_id):
    current = load_from_disk("best_adj.json")  # always read from disk
    if proposed_adj > current["adj"]:
        write_to_disk("best_adj.json", {
            "adj": proposed_adj,
            "gen": gen_id,
            "config": proposed_config
        })
        fsync()
        log(f"[new_best] proposed {proposed_adj} > current {current['adj']} → ADOPTED")
        return True
    else:
        log(f"[no_improvement] proposed {proposed_adj} <= current {current['adj']} → REJECTED")
        return False
```

**Fix 3: Attractor Blacklist Enforcement**
- Before ANY simulation, check if proposed config would reproduce a blacklisted
  signature (see BLACKLISTED CONFIGS below)
- If yes: log [DUPLICATE — frozen cycle], do NOT simulate, force new proposal
- The proposer MUST be capable of detecting its own attractor convergence

**Fix 4: Validation Test (run BEFORE Gen 1201)**
```
Test A: Load best_adj.json. Confirm it reads 1.7474 (or 1.7424 if Gen 1009
        adoption truly failed). Log: "DISK READ: current_best_adj = X.XXXX"
Test B: Simulate Gen 1009 config. Confirm adj=1.7474.
Test C: Simulate a config with expected adj=1.7480 (minor perturbation).
        If adj > 1.7474: confirm adoption fires and disk is updated.
        If adj <= 1.7474: confirm [no_improvement] is logged.
Test D: Restart the process. Re-read disk. Confirm current_best_adj persisted.
```

### Root Cause History (Three Recurrences — Pattern Analysis)
| Event | Gens | Symptom | Root Cause |
|-------|------|---------|------------|
| First | 586–600 | adj=1.7349 cycling | Write to local var |
| Second | 982–1000 | adj=1.7424 cycling | Same; v7.0 reinit |
| Third | 1185–1200 | 1.7424+1.7474 cycling | Same; adoption at Gen 1009 |

All three have the same root cause. The fix must be structural, not procedural.

---

## ✅ TRUE CURRENT BEST — Gen 1009 (CONFIRMED, PENDING DISK VALIDATION)

- adj_score=1.7474, sharpe=0.2881, roi=20.831%, win=79.38%, bets=8597
- Confirmed: appeared as [new_best] in Gen 1009
- Config: world_events, min_edge_pts slightly below Gen 811's 0.066

```yaml
# GEN 1009 BEST — CANONICAL BASELINE v8.0
category: world_events
exclude_keywords: []
include_keywords: []
max_days_to_resolve: 30
max_position_pct: 0.1
min_edge_pts: 0.064        # NOTE: confirm exact value from Gen 1009 log
min_liquidity_usd: 100
name: pm_research_best
price_range:
- 0.05
- 0.77
```

**⚠️ If Gen 1009 exact YAML is unavailable:** reconstruct by simulating grid
min_edge_pts ∈ {0.062, 0.063, 0.064, 0.065, 0.066} × price_range_max ∈ {0.75, 0.77}
and selecting config that reproduces adj=1.7474 exactly. Log as [RECONSTRUCTION].

## ✅ REFERENCE CONFIGS

| Gen  | adj    | sharpe | bets | Notes                          |
|------|--------|--------|------|--------------------------------|
| 1009 | 1.7474 | 0.2881 | 8597 | **CURRENT BEST** ✅             |
| 811  | 1.7424 | 0.2877 | 8523 | Previous best (attractor A)    |
| 586–600 | 1.7349 | 0.2889 | 8088 | Pre-v7.0 best               |
| 195  | 1.6167 | 0.2687 | 8189 | Old recorded best              |
| 121  | 1.5244 | 0.2528 | 8288 | Reference floor                |

---

## 🚨 BLACKLISTED CONFIGS — DO NOT SIMULATE

### BLACKLISTED ATTRACTOR 1 (CATASTROPHIC)
- Signature: bets≈12732, sharpe≈-0.0745, adj≈-0.4813
- Cause: price_range_max > 0.90 OR min_edge_pts < 0.04
- HARD REJECT before simulation

### BLACKLISTED ATTRACTOR 2 (ZERO BETS)
- Signature: bets=0 or bets < 50
- Log as FAIL; trigger auto-recovery

### BLACKLISTED ATTRACTOR 3 (OVER-FILTERED)
- Signature: bets≈156, adj≈0.47
- Cause: min_edge_pts > 0.15 OR price_range_min > 0.20
- REJECT if pre-simulation expected bets < 200

### BLACKLISTED ATTRACTOR 4 (FROZEN CYCLE — v7.0/v8.0)
- Signature A: adj=1.7474, bets=8597 (Gen 1009 / Attractor A)
- Signature B: adj=1.7424, bets=8523 (Gen 811 / Attractor B)
- Signature C: adj=1.7349, bets=8088 (Gen 586–600 / Attractor C)
- These configs have been simulated 30+ combined times with zero marginal value
- **DO NOT PROPOSE ANY OF THESE CONFIGS AGAIN**
- Detection rule: if proposed config has kw=0 AND category=world_events AND
  min_edge_pts ∈ [0.060, 0.070] AND price_range_max ∈ [0.75, 0.79]:
  → flag as likely attractor, require keyword diff OR category diff to proceed

---

## ⚠️ GENERATION LOGGING REQUIREMENT (MANDATORY)

After EVERY generation, log ALL fields:
```
gen_id: NNNN
proposed_config: (full YAML including all keyword lists)
proposed_adj: X.XXXX
proposed_sharpe: X.XXXX
proposed_bets: NNNN
disk_read_current_best_adj: X.XXXX  ← MUST show disk read, not cached value
comparison_result: [new_best / no_improvement / DUPLICATE / FAIL / INVALID]
adoption_check: "proposed X.XXXX > disk_best X.XXXX → [YES/NO]"
disk_write_confirmed: [YES / NO / N/A]
reason_if_rejected: (explicit)
keyword_change_from_baseline: (describe any include/exclude diff from Gen 1009)
```

**ADOPTION RULE (write literally each generation):**
```
READ current_best_adj FROM DISK
IF proposed_adj > current_best_adj (disk value):
    WRITE proposed_adj TO DISK (fsync)
    LOG [new_best] "proposed X.XXXX > disk X.XXXX → ADOPTED, disk updated"
ELSE:
    LOG [no_improvement] "proposed X.XXXX <= disk X.XXXX → REJECTED"
```

**HALT CONDITIONS:**
- If ANY gen achieves adj > 1.70: verify disk write fired before continuing
- If 3 consecutive gens show adj > 1.65 and [no_improvement]: HALT, fix adoption
- If 5 consecutive gens reproduce adj=1.7474 or adj=1.7424 or adj=1.7349: HALT
- If keyword exploration produces 0 bets in 3 consecutive gens: widen filters

---

## 🔬 RESEARCH AGENDA — NEXT 100 GENERATIONS (1201–1300)

### PHASE 0: Adoption Re-Validation (Gens 1201–1205)
**MANDATORY before any new exploration.**

- Gen 1201: Read disk. Log "DISK READ: current_best_adj = X.XXXX". Should be 1.7474.
  If disk shows 1.7424: Gen 1009 adoption failed. Manually write 1.7474 to disk.
  Simulate Gen 1009 config. Confirm adj=1.7474. Log [RECONSTRUCTION if needed].
- Gen 1202: Simulate Gen 811 config (adj expected=1.7424). Confirm [no_improvement].
  Log: "proposed 1.7424 <= disk 1.7474 → REJECTED". Confirm disk still shows 1.7474.
- Gen 1203: Simulate a minor perturbation targeting adj~1.75 (e.g., min_edge_pts=0.063,
  price_range_max=0.78). If adj > 1.7474: confirm adoption fires and disk updates.
  If adj <= 1.7474: log [no_improvement], confirm disk unchanged.
- Gen 1204: Restart process cold. Re-read disk. Confirm value persisted from Gen 1203.
- Gen 1205: Simulate any non-attractor config. Confirm logging format complete.
- **If any of 1201–1205 fail: HALT, fix, rerun from Gen 1201.**
- **If all pass: log [PHASE 0 COMPLETE] and proceed to Phase 1.**

### PHASE 1: Keyword Exclusion Filters (Gens 1206–1230)
**Highest-priority unexplored dimension. Never tested in 1200 generations.**

Baseline for all Phase 1 tests: Gen 1009 config with ONLY the keyword field changed.
Test ONE exclude_keywords list per