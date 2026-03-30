```markdown
# FREYA Research Program — Prediction Markets (v3.0)

## Objective
Find prediction market filter strategies that maximize risk-adjusted ROI by identifying
market categories and keyword buckets where crowd prices are systematically miscalibrated
vs. historical resolution rates.

## Simulator
- 300k+ resolved Polymarket/Kalshi/Manifold markets
- Category base rates: sports=30.6%, politics=29.1%, crypto=31.5%, economics=26.0%, world_events=12.0%
- Bet: if market_odds > base_rate + min_edge_pts -> bet NO; if market_odds < base_rate - min_edge_pts -> bet YES
- Fitness: adj_score = sharpe x log(n_bets/20 + 1)

## ⚠️ CRITICAL BUG — ADOPTION LOGIC FAILURE
- Gen 41 achieved adj_score=0.9933 (sharpe=0.1972, bets=3061)
- Current best has adj_score=0.1632 (sharpe=0.0442, bets=782)
- Gen 41 is OBJECTIVELY BETTER by 6x but was marked [no_improvement]
- **ACTION REQUIRED**: Force-adopt Gen 41's configuration as the new best immediately
- **ACTION REQUIRED**: Audit the comparison logic in the adoption step
- Until this is fixed, every generation is wasted optimizing from a suboptimal baseline
- If Gen 41 config is lost, reconstruct it: world_events, min_edge_pts ~0.07-0.10, 
  price_range [0.05, 0.90], no keywords, max_days_to_resolve ~30-60, min_liquidity_usd ~500-1000

## Critical Findings (Confirmed by Data)
1. **min_edge_pts=0.219 is catastrophically too high** — produces 0-6 bets in most mutations
2. **min_edge_pts 0.05-0.12 is the productive range** — Gen 41 (0.9933), Gen 36 (0.5541), Gen 35 (0.4479) all operated here
3. **world_events is the highest-signal category** — 290k markets, 12% YES rate, massive NO-bet opportunity
4. **The structural edge is behavioral** — crowds systematically overprice dramatic/rare events
5. **Keyword filters mostly hurt performance** — they reduce n_bets without improving sharpe proportionally
6. **14 of last 20 generations produced ≤6 bets** — the mutation engine is broken or ignoring constraints

## Key Market Insights
- world_events is the largest category (290k markets) with YES rate of only 12%
  -- markets priced above ~17-20% represent systematic YES overpricing (NO bets)
  -- markets priced below ~7% represent YES underpricing (YES bets, rarer)
  -- The vast majority of the edge is in NO bets on markets priced 15-40%
- Sports/politics/crypto/economics have base rates 26-32%
  -- These require more precise keyword filters to find miscalibration
  -- Secondary priority — only pursue after world_events is fully optimized
- Higher min_liquidity_usd filters to better-quality markets but reduces n_bets
  -- min_liquidity_usd=500-1000 is the sweet spot

## Generation Performance Summary
| Gen | adj_score | sharpe | bets | Config hint |
|-----|-----------|--------|------|-------------|
| 2   | 0.1632    | 0.0442 | 782  | min_edge=0.219 (current "best" — TOO HIGH) |
| 35  | 0.4479    | 0.1177 | 878  | ~moderate edge, world_events |
| 36  | 0.5541    | 0.1272 | 1539 | ~moderate edge, world_events |
| 41  | 0.9933    | 0.1972 | 3061 | **TRUE BEST** — reconstruct & adopt |

## Priority Mutation Targets (Next 100 Generations)

### PRIORITY 0 (BLOCKING): Fix Adoption Logic & Adopt Gen 41
- Reconstruct Gen 41 configuration and force-set as new best
- If exact config unknown, run a grid search:
  * min_edge_pts: [0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12]
  * category: world_events
  * price_range: [0.05, 0.90]
  * no keywords
  * min_liquidity_usd: 500 or 1000
  * max_days_to_resolve: 30 or 60
- One of these configurations should reproduce adj_score ~0.99
- **Do not proceed to other priorities until this is resolved**

### PRIORITY 1: Optimize Around Gen 41 Baseline
Once Gen 41 is adopted, make SMALL perturbations:
- min_edge_pts: test 0.06, 0.07, 0.08, 0.09, 0.10, 0.11 (one at a time)
- price_range narrowing: [0.10, 0.90], [0.15, 0.90], [0.15, 0.50], [0.10, 0.50]
- max_days_to_resolve: test 14, 21, 30, 45, 60
- min_liquidity_usd: test 500, 750, 1000, 2000
- max_position_pct: test 0.05, 0.08, 0.10, 0.15
- **Change ONE parameter per generation — never stack multiple changes**

### PRIORITY 2: Keyword Refinement on world_events (After Priority 1 Stabilizes)
Starting from the optimized Gen 41 baseline, test single keywords:
- High-priority keywords (likely to isolate overpriced YES markets):
  * "war", "attack", "invade", "bomb" — military/conflict events
  * "resign", "die", "arrest", "impeach" — rare personal events
  * "ban", "sanction", "veto" — policy actions
  * "announce", "sign", "agreement" — diplomatic outcomes
  * "election", "win", "lose" — electoral outcomes
- Test each keyword ALONE first as include_keyword
- Only test keyword PAIRS if singles show adj_score > 0.5
- Reject any keyword that drops bets below 100

### PRIORITY 3: Exclude-Keyword Strategies
- Instead of including keywords, try EXCLUDING noise keywords:
  * Exclude "score", "points", "game" (sports leakage into world_events)
  * Exclude "price", "token", "coin" (crypto leakage)
- This preserves high n_bets while potentially improving sharpe

### PRIORITY 4: Category Diversification (Low Priority)
- Only pursue if world_events optimization plateaus above adj=1.0
- Politics: base_rate=29.1%, test keywords "impeach", "indict", "resign", "lose"
- Economics: base_rate=26.0%, test keywords "recession", "default", "crash"
- min_edge_pts for these categories: 0.08-0.12 (tighter calibration needed)

## Parameter Constraints (HARD ENFORCED — REJECT VIOLATIONS PRE-SIMULATION)
- min_edge_pts: 0.04 to 0.15 ONLY
  * **ANY proposed min_edge_pts > 0.15 must be auto-clamped to 0.12**
  * **ANY proposed min_edge_pts < 0.04 must be auto-clamped to 0.05**
- min_liquidity_usd: 200 to 5000 (never above 5000)
- max_days_to_resolve: 7 to 90
- max_position_pct: 0.03 to 0.20
- price_range: lower bound >= 0.05, upper bound <= 0.95
- n_bets minimum: 50 (any result with <50 bets = automatic failure, do not evaluate)

## Mutation Engine Guardrails (NEW)
- If a generation produces 0 bets: DO NOT log as normal failure. Instead:
  1. Log the proposed config for debugging
  2. Auto-retry with min_edge_pts reduced by 0.03
  3. If still 0 bets, auto-retry with all keywords removed
- If 3 consecutive generations produce <50 bets: force-reset to last known good config
- The proposer (Gemini Flash Lite) must output the EXACT parameter values it is changing
  and the REASON for the change before simulation runs
- Limit keyword lists to max 3 include_keywords and 3 exclude_keywords per mutation

## Scoring Interpretation
- adj_score > 0.9 = excellent (Gen 41 achieved this — it IS possible)
- adj_score 0.5-0.9 = good, worth refining (Gens 35, 36)
- adj_score 0.16-0.5 = marginal but better than current "best"
- adj_score < 0.1 or bets < 50 = failed, revert immediately
- Current TRUE best should be adj_score ≈ 0.9933 (Gen 41)

## Live Competition Strategy (MUST ACTIVATE)
- **thrud**: Deploy Gen 41's reconstructed config IMMEDIATELY
  * This is the validation slot — confirm simulation results translate to live markets
  * Run for minimum 2 weeks before making changes
- **mist**: Deploy Gen 36-like config (slightly different edge threshold) as comparison
  * If Gen 36 config unknown: world_events, min_edge_pts=0.10, no keywords
- **kara**: Explorer slot for Priority 2 keyword strategies
  * Start with best keyword variant once Priority 2 testing begins
- **Review cadence**: Check live results every 50 generations and update program if 
  live performance diverges significantly from simulation

## What to Avoid (Hard Rules)
1. min_edge_pts > 0.15 — PRIMARY FAILURE MODE, causes zero-bet collapse (confirmed 14/20 gens)
2. Stacking multiple tight filters simultaneously (keywords + narrow price_range + high edge)
3. Keywords yielding <100 markets — no statistical power
4. Ultra-broad keywords ("will", "the", "a", "be") — add zero signal
5. Sharpe > 0.5 with bets < 30 — overfitting, reject automatically
6. min_liquidity_usd > 5000 — eliminates too many markets
7. Changing more than ONE parameter per generation
8. Ignoring the adoption bug — Gen 41 MUST be adopted before further optimization
9. Running more than 5 consecutive generations without at least one producing >50 bets
10. Keeping all live competition slots disabled — at least one must be active at all times

## Appendix: Theoretical Edge Model
For world_events (base_rate = 0.12):
- Market priced at 0.20: edge = 0.20 - 0.12 = 0.08 (bet NO, expected profit ~6% after fees)
- Market priced at 0.30: edge = 0.30 - 0.12 = 0.18 (bet NO, expected profit ~16% after fees)  
- Market priced at 0.40: edge = 0.40 - 0.12 = 0.28 (bet NO, expected profit ~26% after fees)
- Market priced at 0.05: edge = 0.12 - 0.05 = 0.07 (bet YES, expected profit ~5% after fees)

With min_edge_pts=