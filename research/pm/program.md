```markdown
# FREYA Research Program — Prediction Markets (v11.0)

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

## 🏆 SYSTEM STATE — GEN 1800

- **Current best:** adj=1.8901, sharpe=0.3157, bets=7940 (Gen 1734, confirmed)
- **Generations since last improvement:** 66 (Gen 1734 was last [new_best])
- **Status: POST-IMPROVEMENT COLLAPSE — PROPOSER GRADIENT LOST**
- Gens 1735–1800: zero improvements; proposer trapped between current-best echoes
  and catastrophic low-bet attractors (bets=4–29, adj≈-0.7 to -1.0)
- **ANOMALY SIGNAL:** Gen 1799 achieved sharpe=0.3973 (HIGHEST IN 200-GEN WINDOW)
  at only 107 bets → adj=0.7344. Config must be recovered and filter-widened.
- **PHASE 3/4 RESULT:** Politics and economics exploration (Gens 1601–1733) produced
  ZERO improvements. World_events base rate asymmetry (12%) remains the dominant edge.
- **LIVE SLOTS:** mist/kara/thrud all disabled — no live validation available.

---

## 🔴 CRITICAL: PROPOSER CONSTRAINT PROTOCOL (MANDATORY v11.0)

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

**HARD REJECTION RULES (NEW v11.0 — checked BEFORE fingerprint lookup):**
```python
def pre_simulation_guard(config):
    # Rule 1: Catastrophic low-bet attractor prevention
    if expected_bets(config) < 500:
        raise HardReject("expected_bets < 500 — catastrophic attractor risk")
    # Rule 2: Blacklisted edge/range combinations
    if config["min_edge_pts"] < 0.04:
        raise HardReject("min_edge_pts < 0.04 — negative sharpe attractor")
    if config["price_range"][1] > 0.90:
        raise HardReject("price_range_max > 0.90 — fee-drag attractor")
    if config["min_edge_pts"] > 0.15:
        raise HardReject("min_edge_pts > 0.15 — over-filtered attractor")
    if config["price_range"][0] > 0.20:
        raise HardReject("price_range_min > 0.20 — over-filtered attractor")
    # Rule 3: keyword overload
    if len(config.get("exclude_keywords", [])) > 15 and \
       (config["price_range"][1] - config["price_range"][0]) < 0.30:
        raise HardReject("keyword overload with narrow price range — zero-bet risk")
```

**ADDITIONAL DIVERSITY ENFORCEMENT (v11.0):**
- If 3 consecutive proposals reproduce adj within 0.005 of 1.8901: FORCE structural
  change (different category OR add include_keywords OR change max_days_to_resolve)
- If 5 consecutive proposals have bets < 500: HALT, reset to Gen 1734 baseline and
  widen all filters by 20% before next proposal
- Proposer must explicitly state research phase for every generation

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

| Gen  | adj    | sharpe | bets  | Notes                                              |
|------|--------|--------|-------|----------------------------------------------------|
| 1734 | 1.8901 | 0.3157 | 7940  | **CURRENT BEST** ✅                                 |
| 1440 | 1.8802 | 0.3158 | 7686  | Superseded best (BLACKLISTED)                      |
| 1799 | 0.7344 | 0.3973 | 107   | ⚠️ ANOMALY — highest sharpe observed; scale up     |
| 1438 | 1.8797 | 0.3155 | 7709  | Attractor B (BLACKLISTED)                          |
| 1409 | 1.8781 | 0.3153 | 7710  | Attractor C (BLACKLISTED)                          |
| 1009 | 1.7474 | 0.2881 | 8597  | Old best (BLACKLISTED)                             |

**KEY INSIGHTS:**
1. World_events base rate (12%) is the dominant edge engine — politics/economics
   exploration (200 gens) produced zero improvements.
2. Reducing bets by excluding well-calibrated sub-topics improves sharpe
   (mechanism confirmed Gen 1401–1734).
3. Gen 1799 sharpe=0.3973 > current best sharpe=0.3157 — a high-precision niche
   exists; it needs bet volume to overcome adj_score log penalty.
4. Proposer post-improvement collapse is a recurring failure mode. After any
   new_best event, enforce structured exploration (not random perturbation).

---

## 🚨 BLACKLISTED CONFIGS — DO NOT SIMULATE

### BLACKLISTED ATTRACTOR 1 (CATASTROPHIC NEGATIVE SHARPE)
- Signature: bets≈12732–13038, sharpe≈-0.07 to -0.08, adj≈-0.49
- Cause: price_range_max > 0.90 OR min_edge_pts < 0.04
- HARD REJECT before simulation

### BLACKLISTED ATTRACTOR 2 (ZERO/NEAR-ZERO BETS)
- Signature: bets < 50, adj=-1.0 or adj≈-0.7 to -0.9
- Confirmed reappearance: Gens 1782–1798 (8 of 17 gens in this range)
- HARD REJECT: if expected_bets < 500 based on filter analysis
- Auto-recovery trigger: if 3 consecutive gens hit this attractor, reset to
  Gen 1734 baseline config

### BLACKLISTED ATTRACTOR 3 (OVER-FILTERED)
- Signature: bets≈100–200, adj≈0.4–0.8
- Cause: min_edge_pts > 0.15 OR price_range_min > 0.20
- Note: Gen 1799 (bets=107) is in this range but has anomalous sharpe=0.3973;
  treat as SIGNAL not as failure — recover and scale
- REJECT new proposals targeting this range unless specifically scaling Gen 1799

### BLACKLISTED ATTRACTOR 4 (EXHAUSTED WORLD_EVENTS MICRO-PERTURBATION BASIN)
- Signature: adj≈1.8802 to 1.8901, bets≈7686–7940, world_events category,
  same exclude_keywords set as Gen 1440 or Gen 1734
- Detection: fingerprint match OR reproduces current best within 0.005
- These represent the exhausted local optimum — minor keyword changes and
  minor edge changes in this space have been fully explored

---

## ⚠️ GENERATION LOGGING REQUIREMENT (MANDATORY v11.0)

```
gen_id: NNNN
proposed_config: (full YAML)
fingerprint: (tuple output of fingerprint() function)
fingerprint_seen_before: [YES gen=NNN / NO]
pre_simulation_guard_passed: [YES / NO — reason if NO]
proposed_adj: X.XXXX
proposed_sharpe: X.XXXX
proposed_bets: NNNN
disk_read_current_best_adj: X.XXXX
comparison_result: [new_best / no_improvement / DUPLICATE / FAIL / INVALID / HARD_REJECT]
adoption_check: "proposed X.XXXX > disk X.XXXX → [YES/NO]"
disk_write_confirmed: [YES / NO / N/A]
reason_if_rejected: (explicit)
keyword_change_from_baseline: (describe diff from Gen 1734 config)
category_change_from_baseline: [YES / NO]
phase: (which research phase this gen belongs to)
structural_change: [YES / NO] (is this a fundamentally different config structure?)
```

**HALT CONDITIONS:**
- If 5 consecutive gens are DUPLICATE: HALT, seen_configs.json is not loading correctly
- If 3 consecutive gens show adj > 1.88 and [no_improvement]: HALT, fix adoption logic
- If ANY gen achieves adj > 1.92: verify disk write fired before continuing
- If 5 consecutive gens have bets < 500: HALT, reset proposer to Gen 1734 baseline
- If 10 consecutive gens propose world_events micro-perturbations with no structural
  change: HALT, proposer is not following phase constraints

---

## 🔬 RESEARCH AGENDA — GENS 1801–1900

### ⚡ IMMEDIATE PRIORITY: GEN 1799 ANOMALY RECOVERY (Gens 1801–1810)

**Goal: Recover the Gen 1799 config (sharpe=0.3973, bets=107) and scale bet volume**