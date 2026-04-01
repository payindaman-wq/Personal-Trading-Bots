```markdown
# FREYA Research Program — Prediction Markets (v19.0)

## Objective
Find prediction market filter strategies that maximize risk-adjusted ROI by identifying
market categories where crowd prices are systematically miscalibrated vs. historical
resolution rates. adj_score = sharpe × log(n_bets/20 + 1).

## All-Time Best
- **Gen 3402:** adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510
  - category: world_events, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
- **Gen 3788:** adj=1.4766, sharpe=0.2235, bets=14771 — REVERSE-ENGINEER PRIORITY
- **Gen 3786:** adj=1.4665, sharpe=0.2348, bets=10304 — REVERSE-ENGINEER PRIORITY

## Key Learnings (Gens 1–3800)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, CEILING ~adj=1.62)**
  - Base rate 12% vs. crowd pricing 25–40%.
  - Best: world_events, no keywords, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458 — 398 gens without improvement.
  - **Status: BASELINE REFERENCE ONLY. Do not tune further.**

### Critical Failure Pattern (Gens 3601–3800)
- **bets=85, adj=-0.6208, sharpe=-0.3744 DEGENERATE ATTRACTOR**
  - Appeared in ~70% of Gens 3781–3800. System is trapped.
  - Root cause: LLM proposing configs that pass fingerprint check but
    map to same 85-bet losing universe.
  - This configuration LOSES money — negative sharpe means directional error,
    not just noise. The crowd is better calibrated than our base rates in
    whatever market slice this represents.
  - **ADD TO HARD BLACKLIST: bets=85, adj=-0.6208**
  - **ADD TO HARD BLACKLIST: bets=0, bets=1, bets=2, bets=12 (zero/near-zero)**

### Confirmed Failures
- **Keyword filters:** 200+ gens of testing, zero improvement. PERMANENTLY SUSPENDED.
- **bets < 500:** universally degenerate. HARD FLOOR enforced.
- **world_events further tuning:** 398 gens, zero improvement. SUSPENDED.
- **Phase F (economics/sports/politics):** NEVER EXECUTED despite being mandated
  at Gen 3601. Must execute immediately in v19.0.

### Unconfirmed High-Priority Signals
- **Gen 3786/3788 configs (UNKNOWN — reverse-engineer immediately)**
  - Both achieved adj > 1.45 with bets > 10,000. These are the second and third
    best results ever recorded. Their configs are unknown but must be recovered
    and refined.
- **Economics NO-bias (UNTESTED)**
- **Sports NO-bias (UNTESTED)**
- **Politics NO-bias (UNTESTED)**
- **Multi-category union (UNTESTED)**

---

## 🔴 HARD CONSTRAINTS (NON-NEGOTIABLE — ENFORCE BEFORE EVERY GEN)

```python
# ABSOLUTE FLOORS
MIN_BETS_FLOOR = 500          # reject any config with estimated bets < 500
MAX_DAYS_MIN = 7              # never set max_days_to_resolve < 7
MIN_LIQUIDITY_MAX = 50        # never set min_liquidity_usd > 50

# HARD BLACKLIST — reject if estimated bets within ±5 of any entry
HARD_BLACKLIST_BETS = [0, 1, 2, 12, 45, 78, 83, 85, 92, 142, 153, 194, 270]

# CATEGORY LOCK — world_events is SUSPENDED
# Only allowed categories: economics, sports, politics, crypto
# world_events may only appear as part of a multi-category union in Phase G
SUSPENDED_CATEGORIES = ["world_events"]  # as sole category

# NO KEYWORDS — permanently suspended
# include_keywords must always be []
# exclude_keywords must always be []
```

```python
def pre_simulation_guard(config):
    # 1. Fingerprint check
    cfg_fp = hash(frozenset(flatten(config).items()))
    if cfg_fp in seen_config_fingerprints:
        raise HardReject("Duplicate fingerprint")

    # 2. Keyword check
    if config.include_keywords or config.exclude_keywords:
        raise HardReject("Keywords permanently suspended")

    # 3. Category check
    if config.category in SUSPENDED_CATEGORIES:
        raise HardReject("world_events suspended as sole category")

    # 4. Bet floor
    preview = estimate_bet_count(config)
    if preview < MIN_BETS_FLOOR:
        raise HardReject(f"Estimated bets={preview} < floor=500")

    # 5. Blacklist check
    for bl in HARD_BLACKLIST_BETS:
        if abs(preview - bl) <= 5:
            raise HardReject(f"Matches blacklisted bet count ~{bl}")

    # 6. Parameter sanity
    if config.max_days_to_resolve < 7:
        raise HardReject("max_days < 7")
    if config.min_liquidity_usd > 50:
        raise HardReject("min_liquidity > 50")

    seen_config_fingerprints.add(cfg_fp)
    return True
```

---

## 🔴 EXPLICIT NEXT-GEN OVERRIDE (Gens 3801–3820)

**DO NOT USE LLM PROPOSAL FOR THESE GENS. INJECT THESE CONFIGS DIRECTLY.**

FREYA has demonstrated it cannot self-navigate out of the bets=85 attractor.
The following configs are pre-specified and must be simulated in order.
Each is designed to test a different category/parameter combination that
has NEVER been simulated.

### Batch 1: Economics Sweep (Gens 3801–3807)
All use: category=economics, keywords=[], max_position_pct=0.1, min_liquidity=10

```yaml
# Gen 3801 — F1a BASELINE
category: economics
min_edge_pts: 0.05
price_range: [0.07, 0.80]
max_days_to_resolve: 30

# Gen 3802 — F1b TIGHTER EDGE
category: economics
min_edge_pts: 0.07
price_range: [0.07, 0.80]
max_days_to_resolve: 30

# Gen 3803 — F1c WIDER RANGE
category: economics
min_edge_pts: 0.05
price_range: [0.05, 0.90]
max_days_to_resolve: 30

# Gen 3804 — F1d LONGER HORIZON
category: economics
min_edge_pts: 0.05
price_range: [0.07, 0.80]
max_days_to_resolve: 60

# Gen 3805 — F1e LOW EDGE HIGH VOLUME
category: economics
min_edge_pts: 0.03
price_range: [0.07, 0.80]
max_days_to_resolve: 60

# Gen 3806 — F1f TIGHT EDGE LONG HORIZON
category: economics
min_edge_pts: 0.08
price_range: [0.07, 0.80]
max_days_to_resolve: 90

# Gen 3807 — F1g MATCH WORLD_EVENTS PARAMS EXACTLY (category swap test)
category: economics
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
```

### Batch 2: Sports Sweep (Gens 3808–3813)
All use: category=sports, keywords=[], max_position_pct=0.1, min_liquidity=10

```yaml
# Gen 3808 — F2a BASELINE
category: sports
min_edge_pts: 0.06
price_range: [0.07, 0.80]
max_days_to_resolve: 14

# Gen 3809 — F2b TIGHTER EDGE
category: sports
min_edge_pts: 0.09
price_range: [0.07, 0.80]
max_days_to_resolve: 14

# Gen 3810 — F2c SHORT HORIZON
category: sports
min_edge_pts: 0.06
price_range: [0.07, 0.80]
max_days_to_resolve: 7

# Gen 3811 — F2d HIGH EDGE
category: sports
min_edge_pts: 0.12
price_range: [0.07, 0.80]
max_days_to_resolve: 14

# Gen 3812 — F2e WIDER RANGE
category: sports
min_edge_pts: 0.06
price_range: [0.05, 0.90]
max_days_to_resolve: 14

# Gen 3813 — F2f MATCH WORLD_EVENTS PARAMS EXACTLY
category: sports
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
```

### Batch 3: Politics Sweep (Gens 3814–3818)
All use: category=politics, keywords=[], max_position_pct=0.1, min_liquidity=10

```yaml
# Gen 3814 — F3a BASELINE
category: politics
min_edge_pts: 0.05
price_range: [0.07, 0.80]
max_days_to_resolve: 30

# Gen 3815 — F3b TIGHTER EDGE
category: politics
min_edge_pts: 0.07
price_range: [0.07, 0.80]
max_days_to_resolve: 30

# Gen 3816 — F3c LONGER HORIZON
category: politics
min_edge_pts: 0.05
price_range: [0.07, 0.80]
max_days_to_resolve: 60

# Gen 3817 — F3d SHORT CYCLE
category: politics
min_edge_pts: 0.06
price_range: [0.07, 0.80]
max_days_to_resolve: 14

# Gen 3818 — F3e MATCH WORLD_EVENTS PARAMS EXACTLY
category: politics
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
```

### Batch 4: Crypto + Multi-Category (Gens 3819–3820)
```yaml
# Gen 3819 — Crypto baseline
category: crypto
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10

# Gen 3820 — Multi-category union attempt (if simulator supports)
# Use category: "world_events|economics" or ["world_events","economics"]
# If union not supported, use economics with max_days=90 as fallback
category: