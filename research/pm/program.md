```markdown
# FREYA Research Program — Prediction Markets (v4.0)

## Objective
Find prediction market filter strategies that maximize risk-adjusted ROI by identifying
market categories and keyword buckets where crowd prices are systematically miscalibrated
vs. historical resolution rates.

## Simulator
- 300k+ resolved Polymarket/Kalshi/Manifold markets
- Category base rates: sports=30.6%, politics=29.1%, crypto=31.5%, economics=26.0%, world_events=12.0%
- Bet: if market_odds > base_rate + min_edge_pts -> bet NO; if market_odds < base_rate - min_edge_pts -> bet YES
- Fee: 2% per bet
- Fitness: adj_score = sharpe x log(n_bets/20 + 1)

## ✅ CURRENT BASELINE — Gen 97 (CONFIRMED BEST)
- adj_score=1.4593, sharpe=0.2487, roi=20.817%, win=74.88%, bets=7053
- This IS the current best. All future generations compare against this.
- Estimated config: world_events, min_edge_pts~0.05-0.08, price_range [0.05, 0.84],
  no keywords, min_liquidity_usd~100, max_days_to_resolve~30
- DO NOT revert to Gen 2 config (min_edge_pts=0.219) under any circumstances

## ⚠️ ADOPTION BUG — PARTIALLY RESOLVED, STILL MONITOR
- Gen 41 (adj=0.9933) was marked [no_improvement] despite being 6x better than baseline
- Gen 96 (adj=1.3455) was also marked [no_improvement] before Gen 97 finally registered
- Root cause: comparison logic appears to fail intermittently when baseline is stale
- Gen 97 was correctly adopted — system is now properly anchored
- **ACTION**: After every generation, log: current_best_adj, proposed_adj, and comparison result
- **ACTION**: If any generation achieves adj > current_best * 0.95, manually verify adoption
- **ACTION**: If 5 consecutive generations show adj > 0.5 but [no_improvement], halt and audit

## ⚠️ MUTATION ENGINE STILL BROKEN
- 14+ of last 20 generations produced ≤6 bets — hard clamps are NOT being enforced
- Gen 100 (sharpe=-0.2187, bets=29) signals the engine is again probing bad territory
- Every 0-bet or <50-bet generation wastes a simulation slot
- The guardrails below are MANDATORY — violations must be caught PRE-SIMULATION

## Critical Findings (Confirmed by Data)
1. **Gen 97 is the gold standard**: adj=1.4593, 74.88% win rate, 7053 bets, 20.8% ROI
2. **min_edge_pts > 0.15 is catastrophically destructive** — confirmed across 14+ generations
3. **min_edge_pts 0.05-0.10 is the productive range** — all high-performing gens are here
4. **world_events is the highest-signal category** — 12% YES rate, crowds systematically
   overprice YES, NO-bias strategy captures persistent edge at scale
5. **74.88% win rate confirms structural miscalibration, not noise** — the edge is real
6. **Keyword filters mostly hurt performance** — reduce n_bets without proportional sharpe gain
7. **All three live slots have never been activated** — this is an operational failure

## Key Market Insights
- world_events base rate = 12% YES
  -- Markets priced above ~17-20%: systematic YES overpricing → bet NO
  -- Markets priced below ~7%: YES underpricing → bet YES (rarer opportunity)
  -- The vast majority of edge is in NO bets on markets priced 15-40%
  -- Gen 97's 74.88% win rate validates this structural bias at scale
- Sports/politics/crypto/economics: base rates 26-32%
  -- Smaller structural edge; require precise keyword filters
  -- Secondary priority — only after world_events is fully optimized
- Higher min_liquidity_usd filters to better-quality markets but reduces n_bets
  -- Gen 97 appears to use min_liquidity_usd=100; test whether raising improves sharpe
  -- Sweet spot likely 100-1000 given Gen 97's high bet count

## Generation Performance Summary
| Gen | adj_score | sharpe | bets  | Notes |
|-----|-----------|--------|-------|-------|
| 2   | 0.1632    | 0.0442 | 782   | OLD "best" — min_edge=0.219, TOO HIGH, ignore |
| 35  | 0.4479    | 0.1177 | 878   | Moderate edge, world_events |
| 36  | 0.5541    | 0.1272 | 1539  | Moderate edge, world_events |
| 41  | 0.9933    | 0.1972 | 3061  | Strong — wrongly rejected by adoption bug |
| 47  | 0.9933    | 0.1972 | 3061  | Duplicate of Gen 41 config |
| 48  | 0.8924    | 0.1822 | 2657  | Slight variant of Gen 41 |
| 96  | 1.3455    | 0.2414 | 5253  | Near-best — wrongly rejected by adoption bug |
| 97  | **1.4593**| **0.2487**|**7053**| **TRUE BEST — current baseline** ✅ |

## Priority Mutation Targets (Next 100 Generations)

### PRIORITY 0 (BLOCKING): Reconstruct Exact Gen 97 Configuration
- Gen 97 config must be precisely documented before further mutation
- If not logged, run targeted grid search to reconstruct:
  * min_edge_pts: [0.04, 0.05, 0.06, 0.07, 0.08]
  * category: world_events
  * price_range: [0.05, 0.84] (as shown in current best yaml)
  * no keywords
  * min_liquidity_usd: [100, 200, 500]
  * max_days_to_resolve: [30, 45, 60]
- Target: reproduce adj_score ≥ 1.40 (within 2% of Gen 97)
- Document the exact config and freeze it as the v4.0 baseline
- This takes priority over ALL other mutations

### PRIORITY 1: Fine-Tune Around Gen 97 Baseline
Change EXACTLY ONE parameter per generation. Never stack changes.

**1a. min_edge_pts sweep (highest leverage parameter):**
- Test: 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10
- Expected: lower values increase bets but may reduce sharpe; find the optimum
- Stop if any value produces <100 bets (likely means min_edge_pts is too high)

**1b. Price range narrowing (improve signal quality):**
- Test upper bound: [0.05, 0.70], [0.05, 0.75], [0.05, 0.80], [0.05, 0.84], [0.05, 0.90]
- Test lower bound: [0.07, 0.84], [0.10, 0.84], [0.12, 0.84], [0.15, 0.84]
- Test both: [0.10, 0.75], [0.12, 0.70], [0.15, 0.65]
- Goal: exclude very-low-probability markets (potential noise) and very-high (floor effects)

**1c. Liquidity threshold sweep:**
- Test: 100, 250, 500, 750, 1000, 2000
- Higher liquidity = fewer but better-calibrated markets
- Watch for the crossover where sharpe improves enough to offset bet count reduction

**1d. Resolution time window:**
- Test max_days_to_resolve: 7, 14, 21, 30, 45, 60, 90
- Shorter windows may have more predictable outcomes
- Longer windows increase n_bets; test whether they degrade sharpe

**1e. Position sizing:**
- Test max_position_pct: 0.03, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20
- Higher position sizing amplifies both gains and variance

### PRIORITY 2: Keyword Refinement on world_events
Only begin after Priority 1 has stabilized (best adj_score unchanged for 10+ gens).

Test ONE keyword at a time as include_keyword. Minimum 100 bets required.

**High-priority include keywords (isolate overpriced YES markets):**
- Military/conflict: "war", "attack", "invade", "bomb", "conflict", "strike"
- Personal events: "resign", "die", "death", "arrest", "impeach", "assassin"
- Policy actions: "ban", "sanction", "veto", "restrict"
- Diplomatic: "agreement", "deal", "treaty", "ceasefire"
- Electoral: "win", "lose", "election", "vote", "defeat"

**Evaluation criteria for keywords:**
- Keep if: adj_score > 1.0 AND bets ≥ 100
- Keep conditionally if: adj_score > 0.8 AND bets ≥ 200 AND sharpe > Gen 97 sharpe
- Reject if: bets < 100 OR adj_score < current best
- Only test keyword PAIRS if single keyword achieves adj > 1.2

### PRIORITY 3: Exclude-Keyword Strategies
Remove noise that may be polluting world_events signal quality:
- Exclude sports leakage: "score", "points", "game", "match", "goal", "season"
- Exclude crypto leakage: "price", "token", "coin", "bitcoin", "ethereum", "btc"
- Exclude financial: "market cap", "trading", "ath"
- Test each exclusion separately; combine only if both individually improve adj_score

### PRIORITY 4: Category Diversification
Only pursue if world_events optimization plateaus (adj_score unchanged for 20+ gens).
- Politics (base=29.1%): keywords "impeach", "indict", "resign", "lose", "convict"
- Economics (base=26.0%): keywords "recession", "default", "crash", "collapse"
- min_edge_pts for these: 0.08-0.12 (tighter calibration needed vs world_events)
- Never mix categories in a single strategy config

## Parameter Constraints (HARD ENFORCED — REJECT VIOLATIONS PRE-SIMULATION)
These checks must run BEFORE simulation, not after. A violation means the generation
is discarded without simulation and logged as INVALID.

| Parameter | Minimum | Maximum | Default (Gen 97) |
|-----------|---------|---------|-----------------|
| min_edge_pts | 0.04 | 0.12 | ~0.05-0.08 |
| min_liquidity_usd | 100 | 5000 | 100 |
| max_days_to_resolve | 7 | 90 | 30 |
| max_position_pct | 0.03 | 0.20 | 0.10 |
| price_range lower | 0.05 | 0.30 | 0.05 |
| price_range upper | 0.50 | 0.95 | 0.84 |
| include_keywords | 0 | 3 | 0 |
| exclude_keywords | 0 | 3 | 0 |

- **ANY proposed min_edge_pts > 0.12 → HARD REJECT, do not simulate**
- **ANY proposed min_edge_pts < 0.04 → HARD REJECT, do not simulate**
- **n_bets < 50 → automatic failure, log as FAIL, do not evaluate score**
- **Changing more than ONE parameter per generation → HARD REJECT**

## Mutation Engine Guardrails (MANDATORY)
1. The proposer must output EXACT parameter values being changed and REASON before simulation
2. If a generation produces 0 bets:
   - Log the proposed config for debugging
   - Auto-retry with min_edge_pts reduced by 0.02
   - If still 0 bets, auto-retry with all keywords removed
   - If still 0 bets, hard-reset to Gen 97 baseline config
3. If 3 consecutive generations produce <50 b