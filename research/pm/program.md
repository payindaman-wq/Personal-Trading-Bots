```markdown
# FREYA Research Program — Prediction Markets (v18.0)

## Objective
Find prediction market filter strategies that maximize risk-adjusted ROI by identifying
market categories where crowd prices are systematically miscalibrated vs. historical
resolution rates. adj_score = sharpe × log(n_bets/20 + 1).

## Key Learnings (Gens 1–3600)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, EXPLOITED TO CEILING)**
  - Base rate 12% vs. crowd pricing 25–40%. Broad NO-bias across full category.
  - Best config: world_events, no keywords, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510 (Gen 3402)
  - **CEILING CONFIRMED: 198 gens of no improvement post-Gen 3402**
  - Sharpe has not exceeded 0.246 despite hundreds of parameter perturbations
  - Further world_events tuning is SUSPENDED except as a baseline reference
  - Do NOT return to world_events configs — the local optimum is fully exploited

### Retired Hypotheses
- **Keyword filters: NON-FUNCTIONAL.** 200+ gens of keyword exploration yielded
  zero improvement. All keyword phases permanently suspended.
- **Gen 2410 (bets=79, win=100%):** confirmed data artifact, blacklisted.
- **Bet-count scaling via liquidity relaxation:** diminishing returns confirmed.
  Gen 3402 liquidity reduction from 50→10 added bets but future reduction toward
  zero adds noise markets with poor price discovery. Floor at min_liquidity=10.

### Current Frontier
- **Sharpe ceiling ~0.245 in world_events.** adj improvement requires either:
  (a) Higher sharpe from a different category with stronger structural mispricing
  (b) More bets from a validated new category
  (c) Multi-category union if simulator supports it
- **Primary blocker:** FREYA anchors on world_events. Forced rotation is mandatory.

---

## 🏆 SYSTEM STATE — GEN 3600

- **Current best:** adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510
  (Gen 3402, world_events, no keywords)
- **Generations since last improvement:** 198
- **Status: WORLD_EVENTS LOCAL OPTIMUM CONFIRMED — MANDATORY CROSS-CATEGORY PIVOT**

### Current Best Config (LOCKED — use as baseline only)
```yaml
category: world_events
include_keywords: []
exclude_keywords: []
max_days_to_resolve: 14
min_edge_pts: 0.055
min_liquidity_usd: 10
price_range: [0.07, 0.80]
max_position_pct: 0.1
```

---

## 🔴 MANDATORY DEDUPLICATION PROTOCOL (v18.0 — NON-NEGOTIABLE)

### Hard Blacklist (reject pre-simulation if bet count within ±3)
```python
HARD_BLACKLIST = [
    {"bets": 45,   "adj": -0.3936},   # Gen 3592 degenerate attractor
    {"bets": 78,   "adj": -0.610},    # Gen 3600 recurring attractor — ADD NOW
    {"bets": 83,   "adj": -0.637},    # Gens 3587/3591/3597 recurring — ADD NOW
    {"bets": 92,   "adj": -0.7536},
    {"bets": 142,  "adj": -0.112},    # Gen 3586
    {"bets": 153,  "adj": -0.0258},
    {"bets": 194,  "adj": -0.303},
    {"bets": 270,  "adj": -0.3616},
]

# ABSOLUTE FLOOR: reject any config where estimated bets < 500
# Enforce STRICTLY — recent gens show bets=45,78,83,142 slipping through
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

### Category Rotation Enforcement (CRITICAL — was failing in Gens 3401–3600)
```python
WORLD_EVENTS_RETURN_LIMIT = 5  # max world_events configs in any 10-gen window

def category_rotation_guard(config, recent_10_gens):
    we_count = sum(1 for g in recent_10_gens if g.category == "world_events")
    if config.category == "world_events" and we_count >= WORLD_EVENTS_RETURN_LIMIT:
        raise HardReject(
            f"World_events appeared {we_count}/10 recent gens. "
            f"Force rotate to economics/sports/politics."
        )
```

### Anti-Cycling Rule (strengthened)
- If the same (category, kw_count, bets_bucket) triple appears 2+ times in the
  last 10 gens without improvement → force category rotation on next gen.
- bets_bucket = round(bets, -2)  # nearest 100
- world_events is considered a single "used slot" — any return to world_events
  counts against the rotation budget regardless of parameter changes.

---

## 🧠 SIGNAL INVENTORY

### Signal 1: World Events Structural NO-Bias ✅ CONFIRMED, CEILING REACHED
- adj=1.6196, sharpe=0.2458 — local optimum confirmed after 198 no-improvement gens
- **Status: SUSPENDED. Use Gen 3402 config as fixed baseline only.**

### Signal 2: Economics Structural NO-Bias 🔴 UNTESTED — TOP PRIORITY
- Base rate 26.0% vs. hypothesized crowd pricing 35–45%
- Hypothesis: economic forecasts (recession, rate cuts, GDP, inflation) overpriced
  YES due to optimism/recency/media salience bias
- Potential edge: ~9–19 percentage points if signal exists
- If sharpe matches world_events (~0.245) with more bets → higher adj
- **Status: MUST TEST IN PHASE F1 — NO FURTHER DELAYS**

### Signal 3: Sports Structural NO-Bias 🔴 UNTESTED — HIGH PRIORITY
- Base rate 30.6% vs. hypothesized crowd pricing 40–55% on favorites/upsets
- Hypothesis: availability bias inflates YES pricing on high-salience outcomes
- Risk: sports markets may have more sophisticated bettors (sharper pricing)
- **Status: MUST TEST IN PHASE F2**

### Signal 4: Politics Structural NO-Bias 🔴 UNTESTED — MEDIUM PRIORITY
- Base rate 29.1% vs. hypothesized crowd pricing 35–45%
- Risk: politics has strong informed-trader presence, may be efficiently priced
- **Status: TEST IN PHASE F3 after F1/F2**

### Signal 5: Crypto Structural Bias 🟡 DEPRIORITIZED
- Base rate 31.5% — close to 50/50 structure, lower expected edge
- Crowd pricing for crypto events may be more sophisticated
- **Status: LOW PRIORITY — test only if F1–F3 fail**

### Signal 6: Multi-Category Union 🟡 UNTESTED — PHASE G
- Hypothesis: combining world_events + economics or world_events + sports
  doubles bet universe while preserving structural NO-bias signal
- Requires simulator to support category arrays or OR logic
- **Status: TEST IN PHASE G if simulator supports it**

### Signal 7: Asymmetric Edge Thresholds (YES vs NO) 🟡 NOVEL
- Current model uses same min_edge_pts for both YES and NO bets
- Hypothesis: NO-bias signal may benefit from a lower threshold for NO bets
  and a higher threshold for YES bets (or disabling YES bets entirely)
- **Status: TEST IN PHASE H if F/G phases underperform**

---

## 🗺️ RESEARCH PHASES — GEN 3601–3700

**MANDATORY: Label every generation with Phase, Axis, category, bets, adj.**
**NO KEYWORDS under any circumstances.**
**NO WORLD_EVENTS configs except as forced by deduplication rollback.**
**Max 10 consecutive gens on same Phase before forced rotation.**

---

### PHASE F: CROSS-CATEGORY STRUCTURAL SIGNALS (Gens 3601–3650)
*This phase was planned for Gen 3416 but never executed. Execute now.*

#### F1 — Economics Structural Signal (Gens 3601–3615)
```yaml
category: economics
include_keywords: []
exclude_keywords: []
min_liquidity_usd: 10       # match best world_events liquidity
max_days_to_resolve: 30     # economics resolves slower
max_position_pct: 0.1
```
Test matrix (simulate each independently):
```
Run F1a: min_edge_pts=0.05, price_range=[0.07, 0.80]
Run F1b: min_edge_pts=0.06, price_range=[0.07, 0.80]
Run F1c: min_edge_pts=0.07, price_range=[0.07, 0.80]
Run F1d: min_edge_pts=0.08, price_range=[0.07, 0.80]
Run F1e: min_edge_pts=0.05, price_range=[0.05, 0.90]  # wider range
Run F1f: min_edge_pts=0.05, price_range=[0.07, 0.80], max_days=60
Run F1g: min_edge_pts=0.04, price_range=[0.07, 0.80]  # lower edge, more bets
```
Targets: sharpe ≥ 0.20, bets ≥ 500
Decision gate: if best F1 adj ≥ 1.0, continue F1 refinement for 5 more gens
Decision gate: if best F1 adj < 0.5 across all runs, classify economics as low-signal

#### F2 — Sports Structural Signal (Gens 3616–3628)
```yaml
category: sports
include_keywords: []
exclude_keywords: []
min_liquidity_usd: 10
max_days_to_resolve: 14
max_position_pct: 0.1
```
Test matrix:
```
Run F2a: min_edge_pts=0.06, price_range=[0.07, 0.80]
Run F2b: min_edge_pts=0.08, price_range=[0.07, 0.80]
Run F2c: min_edge_pts=0.10, price_range=[0.07, 0.80]
Run F2d: min_edge_pts=0.06, price_range=[0.07, 0.80], max_days=7
Run F2e: min_edge_pts=0.12, price_range=[0.07, 0.80]
Run F2f: min_edge_pts=0.06, price_range=[0.05, 0.90]
```
Hypothesis check: sports may show LOWER edge (informed bettors)
Decision gate: if best F2 sharpe < 0.10, classify sports as efficiently-priced,
  do not pursue further

#### F3 — Politics Structural Signal (Gens 3629–3638)
```yaml
category: politics
include_keywords: []
exclude_keywords: []
min_liquidity_usd: