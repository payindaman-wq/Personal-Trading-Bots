```markdown
# FREYA Research Program — Prediction Markets (v10.0)

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

## 🏆 SYSTEM STATE — GEN 1600

- **Current best:** adj=1.8802, sharpe=0.3158, bets=7686 (Gen 1440, confirmed)
- **Generations since last improvement:** 160 (Gen 1440 was last [new_best])
- **Status: LOCAL BASIN DEADLOCK — STRUCTURAL CATEGORY EXPLORATION REQUIRED**
- Gens 1441–1600: zero improvements, cycling between three near-identical configs
- Attractor A: adj≈1.8802, bets≈7686 (Gen 1440 config exactly)
- Attractor B: adj≈1.8797, bets≈7685 (1-bet difference from A)
- Attractor C: adj≈1.8641, bets≈7487
- Root cause: proposer is making micro-perturbations only; proposal diversity has collapsed
- Fix: MANDATORY category diversification — world_events exploration is SUSPENDED
  for Gens 1601–1650

---

## 🔴 CRITICAL: PROPOSER CONSTRAINT PROTOCOL (MANDATORY v10.0)

The proposer MUST maintain a `seen_configs.json` file containing the fingerprint of
every configuration ever simulated.

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

**ADDITIONAL DIVERSITY ENFORCEMENT (NEW v10.0):**
- If proposed config has same `category` as current best AND same exclude_keywords
  set (regardless of minor numeric differences): REJECT, force category change
- If 3 consecutive proposals have adj within 0.01 of current best: FORCE a config
  with category != world_events on the 4th proposal
- Proposer must explicitly state which research phase the proposal belongs to

---

## 🔴 ADOPTION LOGIC (MANDATORY — unchanged)

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

| Gen  | adj    | sharpe | bets  | Notes                                    |
|------|--------|--------|-------|------------------------------------------|
| 1440 | 1.8802 | 0.3158 | 7686  | **CURRENT BEST** ✅                       |
| 1438 | 1.8797 | 0.3155 | 7709  | Attractor B (BLACKLISTED)                |
| 1409 | 1.8781 | 0.3153 | 7710  | Attractor C (BLACKLISTED)                |
| 1009 | 1.7474 | 0.2881 | 8597  | Superseded best (BLACKLISTED)            |
| 811  | 1.7424 | 0.2877 | 8523  | Old attractor (BLACKLISTED)              |
| 195  | 1.6167 | 0.2687 | 8189  | Old recorded best (BLACKLISTED)          |

**KEY INSIGHT FROM GEN 1401–1440:**
- Sharpe improved from 0.2881 → 0.3158 by REDUCING bets (8597→7686)
- Mechanism: excluding well-calibrated sub-topics raises per-bet edge quality
- The world_events base rate (12%) is the engine; keyword exclusion is the tuning
- This methodology should now be applied to politics and economics categories

---

## 🚨 BLACKLISTED CONFIGS — DO NOT SIMULATE

### BLACKLISTED ATTRACTOR 1 (CATASTROPHIC)
- Signature: bets≈12732–13038, sharpe≈-0.07 to -0.08, adj≈-0.49
- Cause: price_range_max > 0.90 OR min_edge_pts < 0.04
- HARD REJECT before simulation

### BLACKLISTED ATTRACTOR 2 (ZERO BETS)
- Signature: bets < 50, adj=-1.0 (confirmed reappearance Gen 1597)
- Log as FAIL; trigger auto-recovery; widen filters
- Note: Gen 1597 confirmed this attractor is still reachable — add guard:
  if expected_bets < 100 based on keyword count > 15 AND price_range < 0.3 wide: REJECT

### BLACKLISTED ATTRACTOR 3 (OVER-FILTERED)
- Signature: bets≈156, adj≈0.47
- Cause: min_edge_pts > 0.15 OR price_range_min > 0.20
- REJECT if pre-simulation expected bets < 200

### BLACKLISTED ATTRACTOR 4 (CURRENT BASIN — MICRO-PERTURBATIONS)
- Signature A: adj=1.8802, bets=7686 — Gen 1440 config exactly
- Signature B: adj=1.8797, bets=7685 — 1-bet variant
- Signature C: adj=1.8641, bets=7487 — price_range variant
- Detection: fingerprint match OR (category=world_events AND adj within 0.005 of 1.8802)
- These represent the exhausted world_events local optimum.
- SUSPENDED: no world_events proposals in Gens 1601–1650

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
keyword_change_from_baseline: (describe diff from Gen 1440 config)
category_change_from_baseline: [YES / NO] (new v10.0)
phase: (which research phase this gen belongs to)
```

**HALT CONDITIONS:**
- If 5 consecutive gens are DUPLICATE: HALT, seen_configs.json is not loading correctly
- If 3 consecutive gens show adj > 1.85 and [no_improvement]: HALT, fix adoption logic
- If keyword exploration produces 0 bets in 3 consecutive gens: widen filters
- If ANY gen achieves adj > 1.90: verify disk write fired before continuing
- If 10 consecutive gens propose world_events during Gens 1601–1650: HALT, proposer
  is ignoring phase constraints

---

## 🔬 RESEARCH AGENDA — GENS 1601–1700

### PHASE 3: Politics Category Exploration (Gens 1601–1620)
**Goal: Apply the keyword-exclusion methodology to politics (base rate 29.1%)**

Hypothesis: Politics markets have analogous miscalibration to world_events, but in
different sub-topics. Election markets may be well-calibrated (sophisticated bettors),
while obscure legislative/appointment markets may be overpriced.

**Baseline politics config:**
```yaml
category: politics
min_edge_pts: 0.07
price_range: [0.05, 0.77]
max_days_to_resolve: 30
min_liquidity_usd: 100
max_position_pct: 0.1
exclude_keywords: []
```

**Gen 1601–1605: Politics baseline and single-keyword exclusions**
- Gen 1601: Politics baseline (no keyword filters). Record bets, sharpe, adj.
  This is the politics zero-point.
- Gen 1602: exclude_keywords: ["election"]
- Gen 1603: exclude_keywords: ["poll"]
- Gen 1604: exclude_keywords: ["president"]
- Gen 1605: exclude_keywords: ["congress"]

**Gen 1606–1610: Politics multi-keyword exclusions**
- Gen 1606: exclude_keywords: ["election", "poll"]
- Gen 1607: exclude_keywords: ["election", "poll", "president"]
- Gen 1608: exclude_keywords: ["election", "poll", "president", "congress"]
- Gen 1609: exclude_keywords: ["vote", "ballot", "referendum"]
- Gen 1610: exclude_keywords: ["election", "poll", "vote", "ballot", "approval"]

**Gen 1611–1615: Politics edge threshold sweep**
Use the best keyword config from 1601–1610. Sweep min_edge_pts:
- Gen 1611: min_edge_pts=0.05
- Gen 1612: min_edge_pts=0.06
- Gen 1613: min_edge_pts=0.07 (baseline repeat — expect DUPLICATE, confirm dedup)
- Gen 1614: min_edge_pts=0.08
- Gen 1615: min_edge_pts=0.09

**Gen 1616–1620: Politics price_range sweep**
Use best config from 1601–1615:
- Gen 1616: price_range: [0.05, 0.70]
- Gen 1617: price_range: [0.05, 0.65]
- Gen 1618: price_range: [0.08, 0.77]
- Gen 1619: price_range: [0.10, 0.77]
- Gen 1620: price_range: [0.08, 0.70]
- Log: "POLITICS EXPLORATION CHECKPOINT — best adj found: X.XXXX"

---

### PHASE 4: Economics Category Exploration (Gens 1621–1640)
**Goal: Apply keyword-exclusion methodology to economics (base rate 26.0%)**