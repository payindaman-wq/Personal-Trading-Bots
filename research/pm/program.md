```markdown
# FREYA Research Program — Prediction Markets (v22.0)

## Status at Gen 4400
- **CRITICAL: System in bets=84 attractor collapse.** 9/20 last gens = exact attractor match.
- **Zero improvements in 200 generations** (Gens 4201–4400).
- **Injection queue v21.0 is DEAD.** Consumed, corrupted, or bypassed. Full rebuild required.
- **Pre-simulation guard BET ESTIMATION FAILING.** Configs with bets=78,84,93,119 passing guard.
- **Post-simulation guard NOT PREVENTING RE-SIMULATION** of known-bad configs.
- **Gen 4187/4188 configs STILL UNRECOVERED.** Highest-priority unresolved task.
- **LLM proposals remain SUSPENDED** until Phase H (Gen 4461+).
- **Live slots (mist, kara, thrud) remain DISABLED** until adj > 1.4 confirmed on new config.
- **Gen 4382 confirmed:** world_events baseline (adj=1.6196) is reproducible. Config stable.

## All-Time Best
- **Gen 3402:** adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510
  - category: world_events, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - CONFIRMED REPRODUCIBLE (Gen 4382 exact match).
- **Gen 4187:** adj=1.5865, sharpe=0.2431, bets=13634 — CONFIG UNKNOWN, RECOVER PRIORITY 1
- **Gen 4188:** adj=1.5020, sharpe=0.2371, bets=11258 — CONFIG UNKNOWN, RECOVER PRIORITY 2
- **Gen 3788:** adj=1.4766, sharpe=0.2235, bets=14771 — CONFIG UNKNOWN, RECOVER PRIORITY 3
- **Gen 3786:** adj=1.4665, sharpe=0.2348, bets=10304 — CONFIG UNKNOWN, RECOVER PRIORITY 4
- **Gen 4389:** adj=0.0412, sharpe=0.0119, bets=623 — WEAK POSITIVE, config unknown, log only

## Key Learnings (Gens 1–4400)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, CEILING ~adj=1.62)**
  - Base rate 12% vs. crowd pricing 25–40%.
  - Best config: world_events, no keywords, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458 — 998 gens without improvement.
  - Reproduced exactly at Gen 4382. Config is stable and deterministic.
  - **Status: BASELINE REFERENCE ONLY. Do not tune. Do not propose. Do not inject.**

### Confirmed Failures
- **Keyword filters:** 200+ gens, zero improvement. PERMANENTLY SUSPENDED.
- **bets < 500:** universally degenerate. HARD FLOOR enforced.
- **world_events sole-category tuning:** 998 gens, zero improvement. SUSPENDED.
- **LLM-proposal loop:** SUSPENDED through Gen 4460 minimum.
- **bets≈312 attractor:** Dead zone. Blacklisted.
- **bets≈84/78/93/119 attractor cluster:** NEW PRIMARY DEAD ZONE. 9+ hits in last 20 gens.
  All produce sharpe < -0.36. Expand blacklist to cover full neighborhood.
- **Injection queue v21.0:** FAILED. Did not execute Phase F/G cleanly. Rebuilt as v22.0.

### Unconfirmed High-Priority Signals (v22.0 targets)
1. **Gen 4187/4188 mystery configs** — HIGHEST PRIORITY. 13k–14k bets, sharpe ~0.24.
   Likely economics or multi-category with world_events-style params.
2. **Economics NO-bias (clean test)** — base rate 26%, Phase F contaminated. Never cleanly run.
3. **Multi-category union: world_events + economics** — both low base rates, NEVER TESTED.
4. **Politics NO-bias (clean test)** — base rate 29.1%, NEVER CLEANLY TESTED.
5. **Multi-category union: world_events + politics** — NEVER TESTED.
6. **Multi-category union: all categories** — NEVER TESTED.
7. **Crypto** — base rate 31.5%, smallest structural edge, lowest priority.

---

## 🔴 HARD CONSTRAINTS (NON-NEGOTIABLE)

```python
# ABSOLUTE FLOORS
MIN_BETS_FLOOR = 500
MAX_DAYS_MIN = 7
MIN_LIQUIDITY_MAX = 50

# *** EXPANDED BET COUNT BLACKLIST v22.0 ***
# Original bets=84 attractor neighborhood expanded to ±15 based on observed variants
# bets=78, 84, 93, 119 all confirmed attractor members — block full range 70–130
HARD_BLACKLIST_BET_RANGES = [
    (0, 10),      # Zero/near-zero class
    (30, 50),     # Near-zero class
    (70, 135),    # *** NEW: bets=84 attractor cluster (78, 84, 93, 119 all observed) ***
    (140, 160),   # Legacy attractor neighborhood
    (185, 200),   # Legacy attractor neighborhood
    (260, 325),   # bets=312 attractor neighborhood
]
# NOTE: Replace point-wise blacklist with range-based check. Any estimated bet count
# falling within ANY range above → HardReject.
# Retain legacy point list for backward compatibility during transition:
HARD_BLACKLIST_BETS_LEGACY = [0, 1, 2, 6, 12, 45, 78, 83, 84, 85, 92, 93,
                               119, 142, 153, 194, 270, 312]
# *** 119 ADDED at Gen 4400. ***

# SIMULATION OUTPUT BLACKLIST (post-simulation)
SIMULATION_OUTPUT_BLACKLIST = [
    # bets=84 attractor cluster (NEW PRIMARY — 9+ hits last 20 gens)
    {"bets": 84,  "adj": -0.6288},
    {"bets": 78,  "adj": -0.6099},
    {"bets": 93,  "adj": -0.5846},
    {"bets": 119, "adj": -0.7083},  # *** NEW — 3 hits in last 20 gens ***
    # bets=312 attractor (previous primary)
    {"bets": 312, "adj": -0.4766},
    # Legacy
    {"bets": 85,  "adj": -0.6208},
    {"bets": 35,  "adj": -0.1813},
    {"bets": 11,  "adj": -1.0},
    {"bets": 10,  "adj": -1.0},
    {"bets": 0,   "adj": -1.0},
    {"bets": 6,   "adj": -1.0},
    {"bets": 32,  "adj": -0.587},
    {"bets": 77,  "adj": 0.1139},
]
# Matching rule: abs(result.bets - bl.bets) <= 5 AND abs(result.adj - bl.adj) <= 0.03
# *** TOLERANCE EXPANDED from ±3/±0.02 to ±5/±0.03 to catch near-variants ***

# CATEGORY LOCK
SUSPENDED_CATEGORIES = ["world_events"]  # as SOLE category only
# world_events IS PERMITTED in union configs (multi-category)

# NO KEYWORDS — always
# LLM PROPOSALS SUSPENDED until Gen 4461
LLM_PROPOSALS_SUSPENDED = True
```

```python
def pre_simulation_guard(config):
    """v22.0 — range-based blacklist, stricter estimation requirement"""

    # 0. Null check
    if config is None or config.category is None:
        raise HardReject("Null config")

    # 1. LLM lock
    if not config.is_injected:
        raise HardReject("LLM proposals suspended until Gen 4461")

    # 2. Fingerprint check (prevents re-simulation of known configs)
    cfg_fp = hash(frozenset(flatten(config).items()))
    if cfg_fp in seen_config_fingerprints:
        raise HardReject("Duplicate fingerprint")

    # 3. Keyword check
    if config.include_keywords or config.exclude_keywords:
        raise HardReject("Keywords permanently suspended")

    # 4. Category check
    categories = config.categories if hasattr(config, 'categories') else [config.category]
    if categories == ["world_events"]:
        raise HardReject("world_events suspended as sole category")

    # 5. Parameter sanity
    if config.max_days_to_resolve < MAX_DAYS_MIN:
        raise HardReject(f"max_days < {MAX_DAYS_MIN}")
    if config.min_liquidity_usd > MIN_LIQUIDITY_MAX:
        raise HardReject(f"min_liquidity > {MIN_LIQUIDITY_MAX}")

    # 6. Bet count estimation — REQUIRE ACCURATE ESTIMATE (not approximation)
    # estimate_bet_count must use full historical data slice, not heuristic
    preview = estimate_bet_count(config)  # MUST be deterministic and accurate
    if preview is None:
        raise HardReject("Bet count estimation failed — do not simulate")

    # 7. Absolute floor
    if preview < MIN_BETS_FLOOR:
        raise HardReject(f"Estimated bets={preview} < floor={MIN_BETS_FLOOR}")

    # 8. Range-based blacklist check (v22.0)
    for (lo, hi) in HARD_BLACKLIST_BET_RANGES:
        if lo <= preview <= hi:
            raise HardReject(f"Estimated bets={preview} in blacklisted range [{lo},{hi}]")

    # 9. Legacy point blacklist (belt-and-suspenders)
    for bl in HARD_BLACKLIST_BETS_LEGACY:
        if abs(preview - bl) <= 5:
            raise HardReject(f"Estimated bets={preview} matches legacy blacklist point {bl}")

    seen_config_fingerprints.add(cfg_fp)
    return True

def post_simulation_guard(result):
    """v22.0 — expanded tolerance, range check, hard floor"""

    # 1. Absolute bet floor (catches estimation misses)
    if result.bets < MIN_BETS_FLOOR:
        log(f"POST-GUARD BET FLOOR: bets={result.bets} — discarded")
        attractor_hit_counter += 1
        return False

    # 2. Range-based blacklist check