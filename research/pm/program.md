```markdown
# FREYA Research Program — Prediction Markets (v13.0)

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

## 🏆 SYSTEM STATE — GEN 2200

- **Current best:** adj=1.9387, sharpe=0.3248, bets=7807 (Gen 2195, confirmed)
- **Generations since last improvement:** 5 (Gen 2195 was last [new_best])
- **Status: LOCAL OPTIMUM NEAR-EXHAUSTED — MULTI-AXIS EXPLORATION REQUIRED**
- Gens 2001–2200: 3 improvements total (Gens 2003, 2010, 2195); all world_events/kw=0
- **ERROR CASCADE ALERT (UNRESOLVED):** ~20% of recent gens returning adj=0/bets=0
  Infrastructure fault must be diagnosed. Error gens do not count toward improvement streaks.
- **ANOMALY SIGNAL (RECURRING):** Gen 2199 (sharpe=0.4191, bets=99) echoes Gen 1799
  (sharpe=0.3973, bets=107). HIGH PRIORITY: recover Gen 2199 config from logs.
- **SECONDARY BASIN SIGNAL:** Gen 2197 (adj=1.6873, sharpe=0.3169, bets=4084) — viable
  high-sharpe basin at larger bet count; distinct from mid-range attractor. Map this.
- **LIVE SLOTS:** mist/kara/thrud all disabled — no live validation available.

---

## 🔴 CRITICAL: PROPOSER CONSTRAINT PROTOCOL (MANDATORY v13.0)

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

**HARD REJECTION RULES (v13.0 — checked BEFORE fingerprint lookup):**
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
    # Rule 4: Mid-range attractor rejection
    if 1500 <= expected_bets(config) <= 2500 and config["category"] == "world_events":
        raise HardReject("mid-range world_events attractor — sharpe≈0.165 basin, BLACKLISTED")
    # Rule 5: Error cascade guard
    if consecutive_errors >= 3:
        raise HardReject("3+ consecutive errors — infrastructure fault, halt and diagnose")
    # Rule 6 (NEW v13.0): Local optimum echo prevention
    if expected_adj_delta(config, current_best_adj=1.9387) < 0.001:
        raise HardReject("insufficient differentiation from current best — force structural change")
```

**ADDITIONAL DIVERSITY ENFORCEMENT (v13.0):**
- If 3 consecutive proposals reproduce adj within 0.005 of 1.9387: FORCE structural
  change (different category OR add include_keywords OR change max_days_to_resolve)
- If 5 consecutive proposals have bets < 500: HALT, reset to Gen 2195 baseline and
  widen all filters by 20% before next proposal
- If 3 consecutive gens return error (adj=0, bets=0): HALT, diagnose infrastructure
  before continuing — do not count error gens toward improvement streaks
- Proposer must explicitly state research phase for every generation
- **NEW v13.0:** Proposer must log which exploration axis is being tested each gen
  (see Exploration Phases below)

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

| Gen  | adj    | sharpe | bets  | Notes                                                        |
|------|--------|--------|-------|--------------------------------------------------------------|
| 2195 | 1.9387 | 0.3248 | 7807  | **CURRENT BEST** ✅                                           |
| 2010 | 1.9371 | 0.3245 | 7808  | Superseded (BLACKLISTED)                                     |
| 2003 | 1.9356 | 0.3242 | 7813  | Superseded (BLACKLISTED)                                     |
| 1950 | 1.9324 | 0.3236 | 7815  | Superseded (BLACKLISTED)                                     |
| 1944 | 1.9300 | 0.3232 | 7818  | Superseded (BLACKLISTED)                                     |
| 1911 | 1.9299 | 0.3232 | 7822  | Superseded (BLACKLISTED)                                     |
| 1906 | 1.9131 | 0.3199 | 7892  | Superseded (BLACKLISTED)                                     |
| 1852 | 1.9129 | 0.3198 | 7905  | Superseded (BLACKLISTED)                                     |
| 2197 | 1.6873 | 0.3169 | 4084  | ⚠️ SECONDARY BASIN — high sharpe, distinct config; map this  |
| 1799 | 0.7344 | 0.3973 | 107   | ⚠️ ANOMALY — config lost; high-precision niche signal        |
| 2199 | 0.7475 | 0.4191 | 99    | ⚠️ ANOMALY — config must be recovered; highest sharpe seen   |
| 1009 | 1.7474 | 0.2881 | 8597  | Old best (BLACKLISTED)                                       |

**KEY INSIGHTS (updated v13.0):**
1. World_events base rate (12%) is the dominant edge engine — confirmed across 1000+
   gens. Politics/economics exploration produced zero improvements. Do not revisit.
2. Exclude_keywords optimization is near-exhausted. Marginal gains ~0.001–0.002 per
   keyword addition. The local optimum in this dimension is effectively reached.
3. The mid-range attractor (bets≈1500–2500, sharpe≈0.165) is a confirmed failure mode.
   BLACKLISTED. Do not explore loosened world_events filters in this bet range.
4. THREE NEW EXPLORATION AXES IDENTIFIED (v13.0, see Phases below):
   a. Temporal filtering (max_days_to_resolve: 7–90 days) — nearly unexplored
   b. Include_keywords approach — target specific high-miscalibration sub-niches
   c. Secondary basin mapping (bets ~3500–5000, sharpe ~0.30+) per Gen 2197 signal
5. RECURRING HIGH-SHARPE ANOMALY: Gens 1799 and 2199 both show sharpe >0.40 with
   ~100 bets. This is not noise — it is a reproducible signal of a very high-precision
   sub-niche. Likely a narrow include_keywords config. PRIORITY: recover Gen 2199 config.
6. Error cascade (~20% failure rate) is unresolved infrastructure fault. Each error
   gen wastes exploration budget. Diagnose before Gen 2201.
7. All three Gen 2001–2200 improvements were world_events/kw=0 — suggesting they
   came from min_edge_pts or price_range fine-tuning, not keyword changes.

---

## 🧭 EXPLORATION PHASES (v13.0 — MANDATORY ROTATION)

FREYA must cycle through these phases to prevent local optimum lock-in.
Each gen must declare its phase. After 10 gens in any one phase with no improvement,
rotate to the next phase.

### PHASE A: Temporal Filter Exploration (HIGHEST PRIORITY — unexplored axis)
- Vary max_days_to_resolve: test 7, 14, 21, 30, 45, 60, 90 days
- Hypothesis: Short-resolution markets (≤30 days) may have higher miscalibration
  due to recency bias and event proximity; long-resolution markets (>90 days) may
  allow reversion to base rate
- Combine with current best exclude_keywords set
- Expected bet range: unknown (must map) — reject if < 500
- Target: Find max_days_to_resolve sweet spot that improves sharpe

### PHASE B: Include_Keywords Niche Hunting (HIGH PRIORITY — anomaly recovery)
- Goal: Recover and extend the Gen 2199 high-sharpe signal (sharpe=0.4191)
- Strategy: Add include_keywords to world_events config targeting specific
  sub-ni