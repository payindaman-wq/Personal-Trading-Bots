```markdown
# FREYA Research Program — Prediction Markets (v12.0)

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

## 🏆 SYSTEM STATE — GEN 2000

- **Current best:** adj=1.9324, sharpe=0.3236, bets=7815 (Gen 1950, confirmed)
- **Generations since last improvement:** 50 (Gen 1950 was last [new_best])
- **Status: APPROACHING LOCAL OPTIMUM EXHAUSTION — STRUCTURAL CHANGE REQUIRED**
- Gens 1951–2000: zero improvements; proposer cycling between current-best echoes,
  error states, and new mid-range attractor (bets≈1700–2200, sharpe≈0.165)
- **ERROR CASCADE ALERT:** 8 of last 20 gens returned adj=0/bets=0 — infrastructure
  fault suspected. Mandatory error diagnosis before Gen 2001 proceeds.
- **NEW ATTRACTOR IDENTIFIED (v12.0):** Mid-range cluster (bets≈1710–2208,
  sharpe≈0.16–0.17, adj≈0.72–0.80) — BLACKLISTED (see below)
- **LIVE SLOTS:** mist/kara/thrud all disabled — no live validation available.

---

## 🔴 CRITICAL: PROPOSER CONSTRAINT PROTOCOL (MANDATORY v12.0)

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

**HARD REJECTION RULES (v12.0 — checked BEFORE fingerprint lookup):**
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
    # Rule 4 (NEW v12.0): Mid-range attractor rejection
    if 1500 <= expected_bets(config) <= 2500 and config["category"] == "world_events":
        raise HardReject("mid-range world_events attractor — sharpe≈0.165 basin, BLACKLISTED")
    # Rule 5 (NEW v12.0): Error cascade guard
    if consecutive_errors >= 3:
        raise HardReject("3+ consecutive errors — infrastructure fault, halt and diagnose")
```

**ADDITIONAL DIVERSITY ENFORCEMENT (v12.0):**
- If 3 consecutive proposals reproduce adj within 0.005 of 1.9324: FORCE structural
  change (different category OR add include_keywords OR change max_days_to_resolve)
- If 5 consecutive proposals have bets < 500: HALT, reset to Gen 1950 baseline and
  widen all filters by 20% before next proposal
- If 3 consecutive gens return error (adj=0, bets=0): HALT, diagnose infrastructure
  before continuing — do not count error gens toward improvement streaks
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

| Gen  | adj    | sharpe | bets  | Notes                                                |
|------|--------|--------|-------|------------------------------------------------------|
| 1950 | 1.9324 | 0.3236 | 7815  | **CURRENT BEST** ✅                                   |
| 1944 | 1.9300 | 0.3232 | 7818  | Superseded (BLACKLISTED)                             |
| 1911 | 1.9299 | 0.3232 | 7822  | Superseded (BLACKLISTED)                             |
| 1906 | 1.9131 | 0.3199 | 7892  | Superseded (BLACKLISTED)                             |
| 1852 | 1.9129 | 0.3198 | 7905  | Superseded (BLACKLISTED)                             |
| 1822 | 1.9097 | 0.3192 | 7907  | Superseded (BLACKLISTED)                             |
| 1734 | 1.8901 | 0.3157 | 7940  | Prior best (BLACKLISTED)                             |
| 1799 | 0.7344 | 0.3973 | 107   | ⚠️ ANOMALY — highest sharpe; config lost; deprioritize|
| 1009 | 1.7474 | 0.2881 | 8597  | Old best (BLACKLISTED)                               |

**KEY INSIGHTS (updated v12.0):**
1. World_events base rate (12%) is the dominant edge engine — politics/economics
   exploration (200 gens) produced zero improvements. This is structurally confirmed.
2. Excluding well-calibrated sub-topics improves sharpe (mechanism confirmed across
   Gens 1401–1950). Marginal gains are now ~0.001–0.002 per keyword addition,
   indicating the local optimum is near-exhausted.
3. The mid-range attractor (bets≈1700–2200, sharpe≈0.165) is a NEW failure mode
   identified in Gens 1986–1999. It likely represents a loosened world_events config
   that captures broader but less miscalibrated markets. BLACKLISTED.
4. Error cascade (8/20 gens failing) in Gens 1981–2000 indicates infrastructure
   fault, not strategy failure. Must be diagnosed.
5. Gen 1799 anomaly (sharpe=0.3973, bets=107) config is lost. Deprioritize unless
   reconstructable from logs. Do not chase this signal with new low-bet configs.
6. The improvement trajectory (adj: 1.8901 → 1.9324 over 216 gens) shows
   diminishing returns. Structural change — new category, temporal filter, or
   include_keywords approach — is required for the next breakthrough.

---

## 🚨 BLACKLISTED CONFIGS — DO NOT SIMULATE

### BLACKLISTED ATTRACTOR 1 (CATASTROPHIC NEGATIVE SHARPE)
- Signature: bets≈12732–13038, sharpe≈-0.07 to -0.08, adj≈-0.49
- Cause: price_range_max > 0.90 OR min_edge_pts < 0.04
- HARD REJECT before simulation

### BLACKLISTED ATTRACTOR 2 (ZERO/NEAR-ZERO BETS)
- Signature: bets < 50, adj=-1.0 or adj≈-0.7 to -0.9
- HARD REJECT: if expected_bets < 500 based on filter analysis
- Auto-recovery trigger: if 3 consecutive gens hit this attractor, reset to
  Gen 1950 baseline config

### BLACKLISTED ATTRACTOR 3 (OVER-FILTERED)
- Signature: bets≈100–499, adj≈0.4–0.8
- Cause: min_edge_pts > 0.15 OR price_range_min > 0.20
- REJECT all proposals targeting this range

### BLACKLISTED ATTRACTOR 4 (EXHAUSTED WORLD_EVENTS MICRO-PERTURBATION BASIN)
- Signature: adj≈1.9097 to 1.9324, bets≈7815–7907, world_events category,
  same or near-identical exclude_keywords set as Gen 1950
- Detection: fingerprint match OR reproduces current best within 0.005
- These represent the exhausted local optimum

### BLACKLISTED ATTRACTOR 5 (NEW v12.0 — MID-RANGE WORLD_EVENTS)
- Signature: bets≈1500–2500, sharpe≈0.14–0.18, adj≈0.70–0.85,
  world_events category
- First observed: Gens 1986–1999 (5 instances in 14 non-error gens)
- Cause: Loosened price_range or reduced edge threshold capturing broader
  but less miscalibrated world_events markets
- HARD REJECT: expected_bets 1500–2500 in world_events category

---

## ⚠️ GENERATION LOGGING