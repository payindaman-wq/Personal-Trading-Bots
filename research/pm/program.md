```markdown
# FREYA Research Program — Prediction Markets (v17.0)

## Objective
Find prediction market filter strategies that maximize risk-adjusted ROI by identifying
market categories where crowd prices are systematically miscalibrated vs. historical
resolution rates. adj_score = sharpe × log(n_bets/20 + 1).

## Key Learnings (Gens 1–3400)
- **Keyword filters are non-functional or unreliable.** 200 gens of keyword-based
  exploration (Phase A/D, Gens 3201–3400) produced zero improvements. Gen 2410
  (bets=79, win=100%) is treated as a data artifact. ALL keyword-based phases
  are suspended indefinitely.
- **The real signal is structural:** world_events base rate ~12% vs. crowd pricing
  25–40%. Broad NO-bias across the full category. Consistent but low-sharpe.
- **adj_score improvement currently driven by bet-count scaling**, not sharpe gains.
  Gen 3269 improvement came from min_liquidity relaxation (bets: 6807→10386).
- **Current ceiling:** sharpe ~0.23, adj ~1.42 in world_events/no-keywords.
- **Primary targets:** adj ≥ 2.0, sharpe ≥ 0.5, bets ≥ 1000

## Simulator
- 300k+ resolved Polymarket/Kalshi/Manifold markets
- Category base rates: sports=30.6%, politics=29.1%, crypto=31.5%, economics=26.0%,
  world_events=12.0%
- Bet: if market_odds > base_rate + min_edge_pts → bet NO;
       if market_odds < base_rate - min_edge_pts → bet YES
- Fee: 2% per bet
- Fitness: adj_score = sharpe × log(n_bets/20 + 1)

---

## 🏆 SYSTEM STATE — GEN 3400

- **Current best:** adj=1.4155, sharpe=0.2263, roi=17.26%, win=76.38%, bets=10386
  (Gen 3269, world_events, no keywords, perturb:min_liquidity_usd)
- **Previous best:** adj=1.2132, sharpe=0.208, roi=16.1%, win=75.3%, bets=6807
  (Gen 3144)
- **Generations since last improvement:** 131 (Gen 3269 was last [new_best])
- **Status: NEAR-LOCAL-OPTIMUM — KEYWORD HYPOTHESIS RETIRED — STRUCTURAL PIVOT**

### Current Best Config
```yaml
category: world_events
include_keywords: []
exclude_keywords: []
max_days_to_resolve: 14
min_edge_pts: 0.059
min_liquidity_usd: [UNKNOWN — confirm from Gen 3269 exact params]
price_range: [0.07, 0.80]
max_position_pct: 0.1
```
**ACTION REQUIRED:** Log exact min_liquidity_usd from Gen 3269 before proceeding.
Assumption: likely reduced from 100 to ~25–50.

---

## 🔴 MANDATORY DEDUPLICATION PROTOCOL (v17.0 — NON-NEGOTIABLE)

### Hard Blacklist (reject pre-simulation if bet count within ±3)
```python
HARD_BLACKLIST = [
    {"bets": 78,   "adj": -0.458},    # recurring broken attractor
    {"bets": 83,   "adj": -0.5785},   # new recurring attractor (Gens 3391, 3394)
    {"bets": 92,   "adj": -0.7536},
    {"bets": 153,  "adj": -0.0258},
    {"bets": 194,  "adj": -0.303},
    {"bets": 270,  "adj": -0.3616},
]

# ABSOLUTE FLOOR: reject any config where estimated bets < 500
# These are statistically meaningless and waste generations
MIN_BETS_FLOOR = 500
```

### Deduplication Guard (enforce before every generation)
```python
def pre_simulation_guard(config):
    cfg_fp = hash(frozenset(flatten(config).items()))
    if cfg_fp in seen_config_fingerprints:
        raise HardReject("Exact config fingerprint already simulated")
    
    preview_bets = estimate_bet_count(config)
    
    if preview_bets < MIN_BETS_FLOOR:
        raise HardReject(f"Estimated bets={preview_bets} below floor={MIN_BETS_FLOOR}")
    
    for b in HARD_BLACKLIST:
        if abs(preview_bets - b["bets"]) < 3:
            raise HardReject(f"Matches blacklisted attractor: {b}")
    
    seen_config_fingerprints.add(cfg_fp)
    return True
```

### Anti-Cycling Rule
- If the same (category, kw_count, bets_bucket) triple appears 3+ times in the
  last 15 gens without improvement → force category rotation on next gen.
- bets_bucket = round(bets, -2)  # nearest 100

---

## 🧠 SIGNAL INVENTORY

### Signal 1: World Events Structural NO-Bias (CONFIRMED, ACTIVE)
- Base rate: 12.0% vs. crowd pricing 25–40%
- Best config: world_events, no keywords, min_edge≈0.059, bets~10k
- adj=1.4155, sharpe=0.2263, roi=17.26%, win=76.38%
- Headroom: sharpe improvement unlikely without new insight; bet-count scaling
  may yield incremental adj gains
- **Status: EXPLOITATION MODE — minor parameter tuning only**

### Signal 2: Cross-Category Structural Signals (UNTESTED, PRIORITY)
- Hypothesis: economics (base 26%) and sports (base 30.6%) may show similar
  crowd overpricing in YES direction
- economics: low base rate + macro uncertainty → potential NO-bias
- sports: high-salience events → availability bias → YES overpricing likely
- **Status: PRIMARY EXPLORATION TARGET Gens 3401–3450**

### Signal 3: Bet-Count Scaling via Liquidity Relaxation (PARTIALLY EXPLOITED)
- Gen 3269 showed relaxing min_liquidity_usd boosted adj via n_bets multiplier
- Further relaxation (min_liquidity → 10–20) may push bets toward 15k–20k
- Risk: very low liquidity markets may have worse calibration (noisier signal)
- **Status: SECONDARY EXPLORATION TARGET — test carefully**

### Signal 4: Price Range Expansion (UNTESTED)
- Current: [0.07, 0.80]. Expanding to [0.05, 0.90] or [0.03, 0.95] adds markets
  at the extremes where crowd mispricing may be strongest (tails)
- Risk: very low-priced markets (0.03–0.07) may be legitimately low-probability
- **Status: SECONDARY EXPLORATION TARGET**

### Signal 5: Category Union / Multi-Category (UNTESTED)
- Hypothesis: combining world_events + economics (both low base rates, both
  susceptible to crowd overpricing) doubles bet universe while preserving signal
- If simulator supports category arrays, test [world_events, economics]
- **Status: TEST IN PHASE C if category union is supported**

---

## 🗺️ RESEARCH PHASES — GEN 3401–3500

**Label every generation: Phase, Axis, bets, adj. No keywords unless explicitly
authorized by a future program revision.**

**Rotation rule: max 10 consecutive gens on same Phase before forced rotation.**

---

### PHASE E: WORLD_EVENTS LOCAL EXPLOITATION (Gens 3401–3415)
*Squeeze remaining value from confirmed signal*

Axis E1 — Liquidity floor reduction:
```yaml
category: world_events
include_keywords: []
min_liquidity_usd: [25, 15, 10, 5]  # test each
min_edge_pts: 0.059
price_range: [0.07, 0.80]
max_days_to_resolve: 14
```
Target: bets ≥ 12000, sharpe ≥ 0.22

Axis E2 — Price range expansion:
```yaml
category: world_events
include_keywords: []
min_liquidity_usd: [best from E1]
min_edge_pts: 0.059
price_range: [0.05, 0.85]  # then [0.05, 0.90], [0.03, 0.90]
max_days_to_resolve: 14
```
Target: incremental adj improvement

Axis E3 — Edge threshold micro-tuning:
```yaml
min_edge_pts: [0.055, 0.057, 0.060, 0.062]  # test each
# all other params: best from E1/E2
```
Target: find sharpe-maximizing edge threshold

Axis E4 — Time window expansion:
```yaml
max_days_to_resolve: [21, 30, 60, null]  # null = no filter
# all other params: best from E1–E3
```
Target: more bets, check if sharpe degrades

**Stop criteria:** if E1–E4 yield < 0.05 adj improvement over 1.4155 → move to Phase F

---

### PHASE F: CROSS-CATEGORY STRUCTURAL SIGNALS (Gens 3416–3450)
*Test whether availability-bias NO-overpricing exists in other categories*

**F1 — Economics structural signal:**
```yaml
category: economics
include_keywords: []
exclude_keywords: []
min_edge_pts: [0.05, 0.06, 0.07, 0.08]  # economics base=26%, need higher edge
price_range: [0.07, 0.80]
max_days_to_resolve: 30
min_liquidity_usd: 25
```
Hypothesis: economic forecasts (recession, rate hikes, GDP) are systematically
overpriced YES by optimism/recency bias. True rate 26% vs. crowd 35–45%.
Target: sharpe ≥ 0.3, bets ≥ 1000

**F2 — Sports structural signal:**
```yaml
category: sports
include_keywords: []
exclude_keywords: []
min_edge_pts: [0.06, 0.08, 0.10]  # sports base=30.6%
price_range: [0.07, 0.80]
max_days_to_resolve: 14
min_liquidity_usd: 25
```
Hypothesis: high-salience sports outcomes (upsets, championships) overpriced YES.
Base rate 30.6% but crowd may price 40–50% on favorites.
Target: sharpe ≥ 0.3, bets ≥ 500

**F3 — Politics structural signal:**
```yaml
category: politics
include_keywords: []
exclude_keywords: []
min_edge_pts: [0.05, 0.07, 0.09]  # politics base=29.1%
price_range: [0.07, 0.80]
max_days_to_resolve: 30
min_liquidity_usd: 25
```
Hypothesis: political event markets overpriced YES on dramatic/controversial events.
Note: politics may have stronger informed trader presence — lower signal expected.
Target: sharpe ≥ 0.25, bets ≥ 500

**F4 — Best cross-category × best world_events params:**
Take the best-performing non-world_events category from F1–F3 and test its
optimal parameters alongside best world_events params for comparison.

**F5 — Combined category