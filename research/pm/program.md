```markdown
# FREYA Research Program — Prediction Markets (v21.0)

## Status at Gen 4200
- **SYSTEM IN ATTRACTOR LOOP.** bets=312, adj=-0.4766 appearing 10+ times in last 20 gens.
- **NEW ATTRACTOR CONFIRMED:** {bets≈312, adj≈-0.4766} — added to BLACKLIST.
- **Zero-bet guard FAILING:** bets=0 and bets=6 passing pre-simulation guard. Fix required.
- **Phase F sweep INCOMPLETE** after 200 injected generations. Queue rebuilt below.
- **Gen 4187/4188 promising results** — configs must be recovered (see Recovery Queue).
- LLM proposals remain SUSPENDED until Phase H (Gen 4261+) or Phase G completes.
- Live slots (mist, kara, thrud) remain DISABLED until Phase H.

## All-Time Best
- **Gen 3402:** adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510
  - category: world_events, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
- **Gen 4187:** adj=1.5865, sharpe=0.2431, bets=13634 — CONFIG UNKNOWN, RECOVER PRIORITY 1
- **Gen 4188:** adj=1.5020, sharpe=0.2371, bets=11258 — CONFIG UNKNOWN, RECOVER PRIORITY 2
- **Gen 3788:** adj=1.4766, sharpe=0.2235, bets=14771 — CONFIG UNKNOWN, RECOVER PRIORITY 3
- **Gen 3786:** adj=1.4665, sharpe=0.2348, bets=10304 — CONFIG UNKNOWN, RECOVER PRIORITY 4

## Key Learnings (Gens 1–4200)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, CEILING ~adj=1.62)**
  - Base rate 12% vs. crowd pricing 25–40%.
  - Best: world_events, no keywords, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458 — 798 gens without improvement.
  - **Status: BASELINE REFERENCE ONLY. Do not tune further. Do not propose.**
  - NOTE: world_events configs are leaking through injection queue (Gen 4195 = exact match
    to all-time best). Suspension enforcement must be verified.

- **Signal 2 — High-Bet Moderate-Sharpe Regime (EMERGING, UNCONFIRMED)**
  - Gen 4187 (adj=1.5865, bets=13634) and Gen 4188 (adj=1.5020, bets=11258) suggest
    a second category or multi-category config in 10k–15k bet range with sharpe ~0.23–0.24.
  - This is the most important unexplored cluster. Must recover configs before Phase G.

### Confirmed Failures
- **Keyword filters:** 200+ gens, zero improvement. PERMANENTLY SUSPENDED.
- **bets < 500:** universally degenerate. HARD FLOOR enforced.
- **world_events sole-category tuning:** 798 gens, zero improvement. SUSPENDED.
- **LLM-proposal loop:** SUSPENDED through Gen 4260 minimum.
- **bets≈312 attractor:** New confirmed dead zone. Added to output blacklist.

### Unconfirmed High-Priority Signals (Phase F/G targets)
- **Gen 4187/4188 mystery configs** — HIGHEST PRIORITY, recover before anything else
- **Multi-category union: world_events + economics** — both low base rates, NEVER TESTED
- **Multi-category union: world_events + politics** — NEVER TESTED
- **Economics NO-bias** — base rate 26.0%, Phase F results contaminated by attractor loop
- **Sports NO-bias** — base rate 30.6%, Phase F results contaminated
- **Politics NO-bias** — base rate 29.1%, NEVER CLEANLY TESTED
- **Crypto** — base rate 31.5%, NEVER CLEANLY TESTED
- **Multi-category union (all low-bias)** — NEVER TESTED

---

## 🔴 HARD CONSTRAINTS (NON-NEGOTIABLE)

```python
# ABSOLUTE FLOORS
MIN_BETS_FLOOR = 500
MAX_DAYS_MIN = 7
MIN_LIQUIDITY_MAX = 50

# BET COUNT BLACKLIST (config estimation, pre-simulation)
HARD_BLACKLIST_BETS = [0, 1, 2, 6, 12, 45, 78, 83, 84, 85, 92, 93,
                       142, 153, 194, 270, 312]
# Matching tolerance: ±5
# NOTE: 312 added at Gen 4200. Zero-floor must also catch bets=0,1,2,6.

# SIMULATION OUTPUT BLACKLIST (post-simulation)
SIMULATION_OUTPUT_BLACKLIST = [
    {"bets": 312, "adj": -0.4766},  # *** NEW PRIMARY ATTRACTOR — 10+ hits in gens 4181-4200
    {"bets": 85,  "adj": -0.6208},  # Legacy primary attractor
    {"bets": 84,  "adj": -0.6288},  # Legacy variant
    {"bets": 93,  "adj": -0.5846},  # Legacy variant
    {"bets": 35,  "adj": -0.1813},  # Near-zero
    {"bets": 11,  "adj": -1.0},     # Zero-bet class
    {"bets": 10,  "adj": -1.0},     # Zero-bet class
    {"bets": 0,   "adj": -1.0},     # Zero-bet class (explicit)
    {"bets": 6,   "adj": -1.0},     # Zero-bet class (Gen 4194 observed)
    {"bets": 32,  "adj": -0.587},   # Gen 4185 observed
    {"bets": 77,  "adj": 0.1139},   # Gen 4184 low-bet degenerate
]
# Matching rule: abs(result.bets - bl.bets) <= 3 AND abs(result.adj - bl.adj) <= 0.02
# If match: log ATTRACTOR HIT, increment attractor_hit_counter, do NOT update state

# CATEGORY LOCK
SUSPENDED_CATEGORIES = ["world_events"]  # as SOLE category — Phase G may lift for union tests

# NO KEYWORDS
# include_keywords: [] always
# exclude_keywords: [] always

# LLM PROPOSAL LOCK
LLM_PROPOSALS_SUSPENDED = True  # Until Gen 4261 minimum or Phase H begins
```

```python
def pre_simulation_guard(config):
    # 0. Zero-bet absolute floor (catches before estimation)
    if config is None or config.category is None:
        raise HardReject("Null config")

    # 1. LLM lock check
    if not config.is_injected:
        raise HardReject("LLM proposals suspended until Gen 4261")

    # 2. Fingerprint check
    cfg_fp = hash(frozenset(flatten(config).items()))
    if cfg_fp in seen_config_fingerprints:
        raise HardReject("Duplicate fingerprint")

    # 3. Keyword check
    if config.include_keywords or config.exclude_keywords:
        raise HardReject("Keywords permanently suspended")

    # 4. Category check
    if config.category == "world_events" and not config.is_union:
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
        if abs(result.bets - bl["bets"]) <= 3 and abs(result.adj - bl["adj"]) <= 0.02:
            log(f"ATTRACTOR HIT: bets={result.bets}, adj={result.adj} — discarded")
            attractor_hit_counter += 1
            return False
    # Additional sanity: reject any result with bets < 500 that passed pre-guard
    if result.bets < 500:
        log(f"POST-GUARD BET FLOOR: bets={result.bets} — discarded")
        return False
    return True
```

---

## 🔴 INJECTION QUEUE (Gens 4201–4260) — LLM SUSPENDED

**QUEUE REBUILT at Gen 4200 due to attractor contamination of Phase F.**
**Execute in strict order. Do not skip. Do not substitute LLM proposals.**
**All configs pre-validated against updated blacklists.**
**Record ALL results regardless of improvement status.**

### PRIORITY 0: Config Recovery (Gens 4201–4204)
Recover Gen 4187/4188 configs. These produced adj=1.5865 and adj=1.5020 respectively.
Likely candidates based on injection queue position and bet count (13k–14k bets suggests
a broad multi-category or single high-volume category sweep).

```yaml
# Gen 4201 — R0a: RECOVERY PROBE — economics baseline wide
# Hypothesis: Gen 4187 was economics with loose params (13634 bets ~ economics wide)
category: economics
min_edge_pts: 0.04
price_range: [0.05, 0.90]
max_days_to_resolve: 30
min_liquidity_usd: 10

# Gen 4202 — R0b: RECOVERY PROBE — sports baseline wide
# Hypothesis: Gen 4188 was sports broad (11258 bets)
category: sports
min_edge_pts: 0.04
price_range: [0.05, 0.90]
max_days_to_resolve: 30
min_liquidity_usd: 10

# Gen 4203 — R0c: RECOVERY PROBE — politics baseline wide
category: politics
min_edge_pts: 0.04
price_range: [0.05, 0.90]
max_days_to_resolve: 30
min_liquidity_usd: 10

# Gen 4204 — R0d: RECOVERY PROBE — multi-category economics+world_events
# First multi-category union test
categories: [economics, world_events]
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 10
```

### Phase F (REBUILT): Category Baseline Sweeps (Gens 4205–4235)
**Clean re-execution of F1–F4 with attractor-resistant param choices.**
All use: keywords=[], max_position_pct=0.1

#### F1-CLEAN: Economics (Gens 4205–4210)

```yaml
# Gen 4205 — F1-CLEAN-a: ECONOMICS BASELINE
category: economics
min_edge_pts: 0.055
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min