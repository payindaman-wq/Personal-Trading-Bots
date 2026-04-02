```markdown
# FREYA Research Program — Prediction Markets (v20.0)

## Status at Gen 4000
- **SYSTEM IN COLLAPSE.** 200 consecutive generations, zero improvements.
- **Phase F sweep was NEVER executed** despite being mandated in v19.0.
- LLM-proposal loop is permanently suspended until Phase F/G injections complete.
- All live slots (mist, kara, thrud) disabled — re-enable only after Phase H.

## All-Time Best
- **Gen 3402:** adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510
  - category: world_events, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
- **Gen 3788:** adj=1.4766, sharpe=0.2235, bets=14771 — CONFIG UNKNOWN, RECOVER
- **Gen 3786:** adj=1.4665, sharpe=0.2348, bets=10304 — CONFIG UNKNOWN, RECOVER

## Key Learnings (Gens 1–4000)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, CEILING ~adj=1.62)**
  - Base rate 12% vs. crowd pricing 25–40%.
  - Best: world_events, no keywords, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458 — 598 gens without improvement.
  - **Status: BASELINE REFERENCE ONLY. Do not tune further. Do not propose.**

### Degenerate Attractors — SIMULATION OUTPUT BLACKLIST
These are identified by their *simulation outputs*, not config fingerprints.
If a simulation returns any of the following, HARD REJECT and do not record:

```python
SIMULATION_OUTPUT_BLACKLIST = [
    {"bets": 85, "adj": -0.6208},   # PRIMARY ATTRACTOR — blocked 100+ times
    {"bets": 84, "adj": -0.6288},   # VARIANT
    {"bets": 93, "adj": -0.5846},   # VARIANT
    {"bets": 35, "adj": -0.1813},   # NEAR-ZERO
    {"bets": 11, "adj": -1.0},      # ZERO-BET CLASS
    {"bets": 10, "adj": -1.0},      # ZERO-BET CLASS
]
# Matching rule: abs(result.bets - bl.bets) <= 3 AND abs(result.adj - bl.adj) <= 0.01
# If match: log as ATTRACTOR HIT, increment attractor_hit_counter, do NOT update state
```

### Confirmed Failures
- **Keyword filters:** 200+ gens of testing, zero improvement. PERMANENTLY SUSPENDED.
- **bets < 500:** universally degenerate. HARD FLOOR enforced.
- **world_events further tuning:** 598 gens, zero improvement. SUSPENDED.
- **LLM-proposal loop:** SUSPENDED for Gens 4001–4060. Injected configs only.

### Unconfirmed High-Priority Signals (UNTESTED after 4000 gens)
- **Gen 3786/3788 mystery configs** — must recover before anything else
- **Economics NO-bias** — base rate 26.0%, NEVER TESTED as sole category
- **Sports NO-bias** — base rate 30.6%, NEVER TESTED as sole category
- **Politics NO-bias** — base rate 29.1%, NEVER TESTED as sole category
- **Crypto** — base rate 31.5%, NEVER TESTED as sole category
- **Multi-category union** — NEVER TESTED

---

## 🔴 HARD CONSTRAINTS (NON-NEGOTIABLE)

```python
# ABSOLUTE FLOORS
MIN_BETS_FLOOR = 500
MAX_DAYS_MIN = 7
MIN_LIQUIDITY_MAX = 50

# BET COUNT BLACKLIST (config estimation)
HARD_BLACKLIST_BETS = [0, 1, 2, 12, 45, 78, 83, 84, 85, 92, 93, 142, 153, 194, 270]
# Matching tolerance: ±5

# SIMULATION OUTPUT BLACKLIST (post-simulation)
# See degenerate attractor table above. Match tolerance: bets ±3, adj ±0.01

# CATEGORY LOCK
SUSPENDED_CATEGORIES = ["world_events"]  # as sole category, until Phase G

# NO KEYWORDS
# include_keywords: [] always
# exclude_keywords: [] always

# LLM PROPOSAL LOCK
LLM_PROPOSALS_SUSPENDED = True  # Until Gen 4061 or Phase H begins
```

```python
def pre_simulation_guard(config):
    # 1. LLM lock check — reject if not from injection queue
    if not config.is_injected:
        raise HardReject("LLM proposals suspended until Gen 4061")

    # 2. Fingerprint check
    cfg_fp = hash(frozenset(flatten(config).items()))
    if cfg_fp in seen_config_fingerprints:
        raise HardReject("Duplicate fingerprint")

    # 3. Keyword check
    if config.include_keywords or config.exclude_keywords:
        raise HardReject("Keywords permanently suspended")

    # 4. Category check
    if config.category in SUSPENDED_CATEGORIES:
        raise HardReject("world_events suspended as sole category")

    # 5. Bet floor (estimated)
    preview = estimate_bet_count(config)
    if preview < MIN_BETS_FLOOR:
        raise HardReject(f"Estimated bets={preview} < floor=500")

    # 6. Blacklist check (estimated)
    for bl in HARD_BLACKLIST_BETS:
        if abs(preview - bl) <= 5:
            raise HardReject(f"Matches blacklisted bet count ~{bl}")

    # 7. Parameter sanity
    if config.max_days_to_resolve < 7:
        raise HardReject("max_days < 7")
    if config.min_liquidity_usd > 50:
        raise HardReject("min_liquidity > 50")

    seen_config_fingerprints.add(cfg_fp)
    return True

def post_simulation_guard(result):
    for bl in SIMULATION_OUTPUT_BLACKLIST:
        if abs(result.bets - bl["bets"]) <= 3 and abs(result.adj - bl["adj"]) <= 0.01:
            log(f"ATTRACTOR HIT: bets={result.bets}, adj={result.adj} — discarded")
            return False  # do not update state, do not record as improvement
    return True
```

---

## 🔴 INJECTION QUEUE (Gens 4001–4060) — LLM SUSPENDED

**Execute these in strict order. Do not skip. Do not substitute LLM proposals.**
**Each config is marked INJECTED. All pass pre_simulation_guard by construction.**
**Record all results regardless of improvement status.**

### Phase F: Category Baseline Sweeps (Gens 4001–4035)

#### F1: Economics (Gens 4001–4009)
All use: category=economics, keywords=[], max_position_pct=0.1, min_liquidity=10

```yaml
# Gen 4001 — F1a BASELINE (match world_events winning params)
category: economics
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4002 — F1b WIDER EDGE
category: economics
min_edge_pts: 0.07
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4003 — F1c TIGHTER EDGE (more bets, lower quality)
category: economics
min_edge_pts: 0.03
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4004 — F1d LONGER HORIZON
category: economics
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 30
min_liquidity_usd: 10

# Gen 4005 — F1e LONGEST HORIZON
category: economics
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 60
min_liquidity_usd: 10

# Gen 4006 — F1f NARROW PRICE RANGE (low-probability focus)
category: economics
min_edge_pts: 0.055
price_range: [0.05, 0.40]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4007 — F1g HIGH EDGE HIGH SELECTIVITY
category: economics
min_edge_pts: 0.10
price_range: [0.07, 0.80]
max_days_to_resolve: 30
min_liquidity_usd: 10

# Gen 4008 — F1h VERY LOW EDGE MAXIMUM VOLUME
category: economics
min_edge_pts: 0.02
price_range: [0.05, 0.90]
max_days_to_resolve: 60
min_liquidity_usd: 10

# Gen 4009 — F1i HIGH LIQUIDITY FILTER
category: economics
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 50
```

#### F2: Sports (Gens 4010–4018)
All use: category=sports, keywords=[], max_position_pct=0.1

```yaml
# Gen 4010 — F2a BASELINE (match world_events winning params)
category: sports
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4011 — F2b TIGHTER EDGE
category: sports
min_edge_pts: 0.08
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4012 — F2c VERY TIGHT EDGE
category: sports
min_edge_pts: 0.12
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4013 — F2d SHORT HORIZON (sports resolve fast)
category: sports
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 7
min_liquidity_usd: 10

# Gen 4014 — F2e LOW EDGE HIGH VOLUME
category: sports
min_edge_pts: 0.03
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4015 — F2f WIDE PRICE RANGE
category: sports
min_edge_pts: 0.055
price_range: [0.05, 0.90]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4016 — F2g LOW PROBABILITY FOCUS
category: sports
min_edge_pts: 0.055
price_range: [0.05, 0.40]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 4017 — F2h LONGER HORIZON
category: sports
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 30
min_liquidity_usd: 10

# Gen 4018 — F2i HIGH LIQUIDITY
category: sports
min_edge_pts: