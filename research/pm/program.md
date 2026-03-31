```markdown
# FREYA Research Program — Prediction Markets (v9.0)

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

## 🚨 SYSTEM STATE — GEN 1400

- **Current best:** adj=1.7474, sharpe=0.2881, bets=8597 (Gen 1009, confirmed)
- **Generations since last improvement:** 391+ (Gen 1009 was last [new_best])
- **Status: FULLY DEADLOCKED — STRUCTURAL INTERVENTION REQUIRED**
- All 200 gens 1201–1400 show zero improvements
- Proposer is cycling between ~6 known attractor configurations
- Blacklist enforcement is NOT functioning (blacklisted configs reappear every 3–5 gens)
- Phase 1 keyword exploration was NEVER executed despite being mandatory since Gen 1201

---

## 🔴 CRITICAL: PROPOSER CONSTRAINT PROTOCOL (MANDATORY v9.0)

The proposer MUST maintain a `seen_configs.json` file containing the fingerprint of
every configuration ever simulated. A fingerprint is defined as:

```python
def fingerprint(config):
    return (
        config["category"],
        round(config["min_edge_pts"], 4),
        round(config["price_range"][0], 3),
        round(config["price_range"][1], 3),
        config["max_days_to_resolve"],
        tuple(sorted(config.get("include_keywords", []))),
        tuple(sorted(config.get("exclude_keywords", [])))
    )
```

**BEFORE ANY SIMULATION:**
1. Compute fingerprint of proposed config
2. Check against `seen_configs.json`
3. If fingerprint exists: LOG `[DUPLICATE — seen gen NNN]`, DO NOT SIMULATE, force new proposal
4. If fingerprint is new: add to `seen_configs.json`, proceed with simulation

**This is not optional. This is the primary fix for the attractor cycle.**

---

## 🔴 ADOPTION LOGIC (MANDATORY — unchanged from v8.0, must be verified working)

```python
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

---

## ✅ CANONICAL CONFIGS

| Gen  | adj    | sharpe | bets  | Notes                          |
|------|--------|--------|-------|--------------------------------|
| 1009 | 1.7474 | 0.2881 | 8597  | **CURRENT BEST** ✅             |
| 811  | 1.7424 | 0.2877 | 8523  | Attractor B (BLACKLISTED)      |
| 586–600 | 1.7349 | 0.2889 | 8088 | Attractor C (BLACKLISTED)   |
| ???  | 0.9578 | 0.1963 | 2607  | Mystery cluster — INVESTIGATE  |
| ???  | 0.7004 | 0.1663 | 1328  | Mystery cluster — INVESTIGATE  |
| 195  | 1.6167 | 0.2687 | 8189  | Old recorded best              |

**MYSTERY CLUSTER PRIORITY:** Configurations producing bets≈1328/adj≈0.7004 and
bets≈2607/adj≈0.9578 have appeared 5+ times each in gens 1201–1400 but have NEVER
been identified. These represent a specific keyword or filter combination. Phase 2
below is dedicated to identifying them, because their sharpe (~0.17–0.20) combined
with the world_events base rate may indicate a refinable sub-market.

---

## 🚨 BLACKLISTED CONFIGS — DO NOT SIMULATE

### BLACKLISTED ATTRACTOR 1 (CATASTROPHIC)
- Signature: bets≈12732–13038, sharpe≈-0.07 to -0.08, adj≈-0.49
- Cause: price_range_max > 0.90 OR min_edge_pts < 0.04
- HARD REJECT before simulation

### BLACKLISTED ATTRACTOR 2 (ZERO BETS)
- Signature: bets < 50, adj=-1.0
- Log as FAIL; trigger auto-recovery; widen filters

### BLACKLISTED ATTRACTOR 3 (OVER-FILTERED)
- Signature: bets≈156, adj≈0.47
- Cause: min_edge_pts > 0.15 OR price_range_min > 0.20
- REJECT if pre-simulation expected bets < 200

### BLACKLISTED ATTRACTOR 4 (FROZEN CYCLE)
- Signature A: adj=1.7474, bets=8597 — Gen 1009 config exactly
- Signature B: adj=1.7424, bets=8523 — Gen 811 config exactly
- Signature C: adj=1.7349, bets=8088 — Gen 586–600 config exactly
- Detection: fingerprint match via seen_configs.json (supersedes manual rule)
- These have been simulated 50+ combined times. Zero marginal value remains.

---

## ⚠️ GENERATION LOGGING REQUIREMENT (MANDATORY)

```
gen_id: NNNN
proposed_config: (full YAML)
fingerprint: (tuple output of fingerprint() function)
fingerprint_seen_before: [YES gen=NNN / NO]
proposed_adj: X.XXXX
proposed_sharpe: X.XXXX
proposed_bets: NNNN
disk_read_current_best_adj: X.XXXX
comparison_result: [new_best / no_improvement / DUPLICATE / FAIL / INVALID]
adoption_check: "proposed X.XXXX > disk X.XXXX → [YES/NO]"
disk_write_confirmed: [YES / NO / N/A]
reason_if_rejected: (explicit)
keyword_change_from_baseline: (describe diff from Gen 1009 config)
phase: (which research phase this gen belongs to)
```

**HALT CONDITIONS:**
- If 5 consecutive gens are DUPLICATE: HALT, seen_configs.json is not loading correctly
- If 3 consecutive gens show adj > 1.65 and [no_improvement]: HALT, fix adoption
- If keyword exploration produces 0 bets in 3 consecutive gens: widen filters
- If ANY gen achieves adj > 1.75: verify disk write fired before continuing

---

## 🔬 RESEARCH AGENDA — GENS 1401–1500

### PHASE 0: System Integrity Check (Gens 1401–1403) — 3 GENS ONLY
Verify adoption and deduplication are working before any exploration.

- **Gen 1401:** Simulate Gen 1009 config. Expect adj=1.7474, [no_improvement] (or DUPLICATE).
  Confirm fingerprint logged. Confirm disk still reads 1.7474.
  Log: "DISK READ: current_best_adj = X.XXXX"
- **Gen 1402:** Simulate any config not in seen_configs.json with expected adj < 1.7474.
  Confirm [no_improvement]. Confirm disk unchanged. Confirm fingerprint added to seen_configs.
- **Gen 1403:** Attempt to re-simulate Gen 1402's config. Confirm [DUPLICATE — seen gen 1402].
  Confirm simulation was skipped. **If this fails: HALT. seen_configs.json is broken.**
- **If 1401–1403 all pass: log [PHASE 0 COMPLETE v9.0] and proceed.**

---

### PHASE 1: Mystery Cluster Identification (Gens 1404–1420)
**Goal: Identify the configuration(s) producing bets≈1328/adj≈0.7004 and bets≈2607/adj≈0.9578**

These configs appeared 5+ times in gens 1201–1400 as accidental proposals. We now
deliberately hunt for them. A config with sharpe~0.20 and clean bets~2600 may be a
refinable sub-market with untapped adj potential.

Strategy: Systematic include_keywords grid on world_events baseline.

**Gen 1404–1408: Single geographic keyword includes**
Test one keyword per gen. Baseline: Gen 1009 config + include_keywords=[KEYWORD].
Target keywords (regions frequently in world_events markets):
- Gen 1404: include_keywords: ["africa"]
- Gen 1405: include_keywords: ["middle east"]
- Gen 1406: include_keywords: ["asia"]
- Gen 1407: include_keywords: ["europe"]
- Gen 1408: include_keywords: ["latin america"]

**Gen 1409–1413: Single topic keyword includes**
- Gen 1409: include_keywords: ["war"]
- Gen 1410: include_keywords: ["election"]  ← note: may shift to politics base rate
- Gen 1411: include_keywords: ["climate"]
- Gen 1412: include_keywords: ["earthquake"]
- Gen 1413: include_keywords: ["sanctions"]

**Gen 1414–1418: Single topic keyword EXCLUDES (reduce noise)**
Baseline: Gen 1009 config + exclude_keywords=[KEYWORD]
- Gen 1414: exclude_keywords: ["election"]
- Gen 1415: exclude_keywords: ["crypto"]
- Gen 1416: exclude_keywords: ["sports"]
- Gen 1417: exclude_keywords: ["will there be"]
- Gen 1418: exclude_keywords: ["price"]

**Gen 1419–1420: Analysis checkpoint**
- Gen 1419: Simulate the include_keywords config with highest adj from 1404–1418.
  Vary min_edge_pts ±0.005 to test sensitivity.
- Gen 1420: Simulate the exclude_keywords config with highest adj from 1404–1418.
  Vary min_edge_pts ±0.005 to test sensitivity.
- Log: "MYSTERY CLUSTER STATUS: [IDENTIFIED / UNIDENTIFIED]"
- If identified: document the fingerprint and add to CANONICAL CONFIGS table.

---

### PHASE 2: Sharpe Improvement via Keyword Exclusion Stacking (Gens 1421–1445)
**Goal: Improve sharpe above 0.2881 by excluding systematically miscalibrated-low subsets**

Hypothesis: Some world_events sub-topics have WORSE miscalibration than average
(crowds are better calibrated there), dragging down sharpe. Excluding them improves
sharpe even if bets decrease, because adj_score is sharpe-dominated at high bet counts.

**Gen 1421–1430: Two-keyword exclude combinations**
Build from best single-excludes found in Phase 1. Test pairs:
- Each gen: exclude_keywords: [best_single_1, candidate_2]
- Vary candidate_2 across: "sports", "crypto", "price", "will", "odds", "bitcoin",
  "nba", "nfl", "ufc", "weather"
- Target: find combo where sharpe > 0.29 with bets > 5000

**Gen 1431–1