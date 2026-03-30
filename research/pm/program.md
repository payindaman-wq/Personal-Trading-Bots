```markdown
# FREYA Research Program — Prediction Markets (v5.0)

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

---

## ✅ CURRENT BASELINE — Gen 195 (CONFIRMED BEST)
- adj_score=1.6167, sharpe=0.2687, roi=20.345%, win=78.14%, bets=8189
- Achieved by: perturb:price_range_max on world_events, no keywords
- Config (inferred): world_events, min_edge_pts=0.07, price_range=[0.05, 0.81],
  no keywords, min_liquidity_usd=100, max_days_to_resolve=30
- DO NOT revert to any prior baseline under any circumstances
- All future generations compare against adj=1.6167

## ✅ SECOND-BEST REFERENCE — Gen 121
- adj_score=1.5244, sharpe=0.2528, roi=19.858%, win=77.38%, bets=8288
- Config: world_events, min_edge_pts~0.07, price_range=[0.05, ~0.81-0.84], no keywords
- Use as fallback reference if Gen 195 config cannot be exactly reproduced

## ⚠️ GENERATION LOGGING REQUIREMENT (MANDATORY)
After EVERY generation, log ALL of the following before proceeding:
  - proposed_config: (full YAML)
  - proposed_adj / proposed_sharpe / proposed_bets
  - current_best_adj (must be 1.6167 unless a new_best was just recorded)
  - comparison_result: [new_best / no_improvement / INVALID / FAIL]
  - reason_if_rejected: (parameter violation, <50 bets, duplicate config, etc.)

If any generation achieves adj > 1.53 (95% of current best), manually verify adoption.
If 5 consecutive generations show adj > 0.5 but [no_improvement], HALT and audit comparison logic.

---

## 🚨 CRITICAL FAILURE PATTERNS — BLACKLIST THESE CONFIGS

The following configurations have been identified as attractor states that waste simulation
slots. If the proposer generates ANY of these, HARD REJECT without simulation:

### BLACKLISTED ATTRACTOR 1 (CONFIRMED BROKEN)
- Signature: bets≈12732, sharpe≈-0.0745, adj≈-0.4813
- Appeared 5+ times in gens 182-199
- Likely cause: price_range widened beyond 0.90, or min_edge_pts < 0.04, or wrong category
- REJECT any config that produced this signature previously

### BLACKLISTED ATTRACTOR 2 (INSUFFICIENT BETS)
- Signature: bets=19 or bets=0, adj=-1.0 or adj=0.0
- Appeared in Gen 191, Gen 200
- REJECT any config with n_bets < 50 pre-simulation if detectable; post-simulation log as FAIL

### DUPLICATE DETECTION (MANDATORY)
- Before simulation, check proposed config against ALL previously simulated configs
- If the proposed config is identical to any prior config (same parameter values), SKIP and
  request a new proposal — do not waste a simulation slot on a known result
- Log as: [DUPLICATE — skipped, matches Gen XXX]

---

## 🚨 MUTATION ENGINE REPAIR REQUIREMENTS

The proposer (Gemini Flash Lite) MUST follow these rules. Violations → HARD REJECT:

1. **ONE parameter change per generation.** Never stack changes.
2. **State the parameter being changed, the old value, the new value, and the reason.**
   Format: `CHANGE: <param> from <old> to <new> | REASON: <one sentence>`
3. **The proposer must acknowledge the current best config before proposing a change.**
   If it cannot reproduce the current best config, it must say so explicitly.
4. **The proposer must NOT re-propose a configuration that has already been simulated.**
   It must check the generation log before proposing.
5. **All hard constraints (see Parameter Constraints table) must be verified by the proposer
   before outputting a proposal.** Self-check format:
   `CONSTRAINT CHECK: min_edge_pts=X ✓/✗ | price_range=[A,B] ✓/✗ | ...`

### Auto-Recovery Protocol (if mutation engine produces bad outputs)
- If 0 bets: log config, auto-retry with min_edge_pts reduced by 0.01, else hard-reset to Gen 195
- If <50 bets: log as FAIL, do not evaluate score, request new proposal
- If 3 consecutive gens produce <50 bets: hard-reset to Gen 195 baseline, log as RESET
- If 3 consecutive gens produce the blacklisted -0.4813 attractor: hard-reset to Gen 195 baseline

---

## Critical Findings (Confirmed by Data, 200 Generations)

1. **Gen 195 is the gold standard**: adj=1.6167, 78.14% win rate, 8189 bets, 20.3% ROI
2. **world_events is the only confirmed high-signal category** — 12% YES base rate,
   crowds systematically overprice YES, NO-bias captures persistent structural edge
3. **min_edge_pts 0.05-0.09 is the productive range** — values >0.12 catastrophically
   reduce bets; values <0.04 invert the signal
4. **price_range_max near 0.81 appears optimal** — Gen 195 and Gen 121 both cluster here
5. **78.14% win rate at 8189 bets is structural, not noise** — confirmed across multiple gens
6. **Keyword filters have NOT been seriously tested** — remain potential upside lever
7. **The broken -0.4813 attractor is the primary waste vector** — 5+ wasted slots in last 20 gens
8. **Live slots have NEVER been activated** — zero forward validation exists

## Key Market Insights
- world_events base rate = 12% YES
  -- Markets priced above ~17-20%: systematic YES overpricing → bet NO (primary edge)
  -- Markets priced below ~7%: YES underpricing → bet YES (rarer opportunity)
  -- price_range=[0.05, 0.81] appears to be the sweet spot — excludes very high-priced
     markets where the miscalibration thesis may weaken or reverse
  -- 78.14% win rate at scale validates the structural bias
- Sports/politics/crypto/economics: base rates 26-32%
  -- Smaller structural edge; have not been meaningfully tested
  -- Secondary priority — only after world_events is fully optimized AND live-validated
- price_range_max is a high-leverage parameter — Gen 195 improved over Gen 121 by
  adjusting this value; further fine-tuning is the top simulation priority

## Generation Performance Summary
| Gen | adj_score | sharpe | bets  | Notes |
|-----|-----------|--------|-------|-------|
| 2   | 0.1632    | 0.0442 | 782   | OLD baseline — min_edge=0.219, ignore |
| 41  | 0.9933    | 0.1972 | 3061  | Strong — wrongly rejected by adoption bug |
| 96  | 1.3455    | 0.2414 | 5253  | Near-best — wrongly rejected by adoption bug |
| 97  | 1.4593    | 0.2487 | 7053  | Previous gold standard |
| 112 | 0.2121    | 0.0589 | 715   | Brief improvement over Gen 2 only |
| 121 | 1.5244    | 0.2528 | 8288  | LLM proposal — major jump |
| 182 | -0.4813   | -0.0745| 12732 | BLACKLISTED attractor — do not re-simulate |
| 184 | 0.9194    | 0.1496 | 9296  | Mid-tier attractor |
| 192 | 1.2937    | 0.2136 | 8525  | Good but below baseline |
| 195 | **1.6167**| **0.2687**|**8189**| **TRUE BEST — current baseline** ✅ |
| 198 | 1.2704    | 0.2387 | 4074  | Lower bets — likely higher min_edge or liquidity |

---

## Priority Mutation Targets (Next 100 Generations)

### PRIORITY 0 (BLOCKING): Document and Freeze Gen 195 Config
- The exact Gen 195 config MUST be precisely documented before further mutation
- Inferred config: world_events, min_edge_pts=0.07, price_range=[0.05, 0.81],
  min_liquidity_usd=100, max_days_to_resolve=30, max_position_pct=0.10, no keywords
- If uncertain, run a single confirmatory simulation with the above exact config
- Target: reproduce adj_score ≥ 1.58 (within 2% of Gen 195)
- Freeze this as the v5.0 baseline before any further mutation
- **DO THIS FIRST. DO NOT SKIP.**

### PRIORITY 1: Fine-Tune price_range Around Gen 195 (Highest Leverage Parameter)
Change EXACTLY ONE parameter per generation. Never stack changes.
Gen 195 improved Gen 121 by adjusting price_range_max — this is confirmed high-leverage.

**1a. price_range_max sweep (primary focus):**
- Test: 0.75, 0.77, 0.79, 0.81 (current), 0.83, 0.85, 0.87
- Do NOT test 0.90 or above — the blacklisted attractor likely involves wide price ranges
- Expected: there is a peak near 0.81; confirm it, then stop sweeping this parameter
- Stop immediately if any value produces the -0.4813 signature; blacklist that value

**1b. price_range_min sweep:**
- Test: 0.05 (current), 0.07, 0.09, 0.10, 0.12, 0.15
- Goal: exclude very-low-probability markets that may be noise or near-zero liquidity
- Watch: higher minimums will reduce bets; acceptable if sharpe improves proportionally

**1c. Combined price_range (only after 1a and 1b individually converge):**
- Test the combination of best 1a result + best 1b result as a single generation
- This is the ONE exception to the single-parameter rule — document explicitly

### PRIORITY 2: min_edge_pts Fine-Tune
**2a. min_edge_pts sweep:**
- Test: 0.05, 0.06, 0.07 (current), 0.08, 0.09
- Do NOT test below 0.04 or above 0.12 (hard limits)
- Note: Gen 198 (bets=4074) may have resulted from higher min_edge_pts — confirms the
  bet-count sensitivity; prefer values that keep bets > 6000

### PRIORITY 3: Liquidity and Resolution Window
**3a. min_liquidity_usd sweep:**
- Test: