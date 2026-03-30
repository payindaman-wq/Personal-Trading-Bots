```markdown
# FREYA Research Program — Prediction Markets (v6.0)

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

## 🚨 PRIORITY ZERO — FIX ADOPTION LOGIC BEFORE ANY NEW SIMULATION 🚨

### The Adoption Gate Is Broken — This Is Confirmed

Evidence: Gens 586, 591, 593, 594, 600 ALL produced adj=1.7349 > current baseline 1.6167,
yet ALL were logged as [no_improvement]. This is a logical impossibility.

**REQUIRED ACTION before Gen 601:**
1. Manually inspect the comparison function: `if proposed_adj > current_best_adj: adopt`
2. Check for off-by-one errors, float precision issues, string-vs-float comparison bugs,
   or stale cached baseline values
3. Confirm the baseline variable is being READ correctly at comparison time (not using
   a stale Gen 195 hardcoded constant instead of the live tracked best)
4. Run a single test: simulate the exact Gen 586/591/600 config and verify adoption fires
5. DO NOT run further generations until this is confirmed working

### Suspected Root Cause
The baseline comparison likely has a hardcoded value of 1.6167 (from Gen 195) that is
not being updated when new bests are found — OR the adoption condition uses >= instead
of > and floating point equality is failing — OR proposed_adj and current_best_adj are
different types. Any of these would produce the observed pattern.

---

## ✅ TRUE CURRENT BEST — Gen 586/591/600 (CONFIRMED BY REPEATED CONVERGENCE)

**WARNING: This config has been simulated 5+ times and rejected due to adoption bug.**
**It IS the true best. It MUST be canonized once adoption logic is repaired.**

- adj_score=1.7349, sharpe=0.2889, roi=TBD, bets=8088
- Confirmed stable attractor: appeared independently in Gens 586, 591, 593, 594, 600
- Config: world_events, parameters TBD (see PRIORITY 1 below for reconstruction)
- Improvement over recorded baseline: +7.3% adj_score, +7.5% sharpe

## ✅ RECORDED BEST — Gen 195 (OFFICIAL BASELINE UNTIL ADOPTION BUG FIXED)
- adj_score=1.6167, sharpe=0.2687, roi=20.345%, win=78.14%, bets=8189
- Config: world_events, min_edge_pts=0.07, price_range=[0.05, 0.81],
  min_liquidity_usd=100, max_days_to_resolve=30, max_position_pct=0.10, no keywords
- DO NOT revert below this

## ✅ SECOND-BEST REFERENCE — Gen 121
- adj_score=1.5244, sharpe=0.2528, roi=19.858%, win=77.38%, bets=8288
- Config: world_events, min_edge_pts~0.07, price_range=[0.05, ~0.81-0.84], no keywords

---

## ⚠️ GENERATION LOGGING REQUIREMENT (MANDATORY)

After EVERY generation, log ALL of the following before proceeding:
  - proposed_config: (full YAML)
  - proposed_adj / proposed_sharpe / proposed_bets
  - current_best_adj (must be dynamically read — NOT hardcoded)
  - comparison_result: [new_best / no_improvement / INVALID / FAIL]
  - reason_if_rejected: (parameter violation, <50 bets, duplicate config, etc.)
  - adoption_check: "proposed X.XXXX > current_best X.XXXX → [YES/NO]" (explicit each time)

**ADOPTION RULE (write this out literally each generation):**
  IF proposed_adj > current_best_adj THEN adopt, update baseline, log as [new_best]
  ELSE log as [no_improvement]

If any generation achieves adj > 1.65 (95% of true best 1.7349):
  manually verify adoption fired correctly.

If 3 consecutive generations show adj > 1.60 and [no_improvement]:
  HALT — adoption logic is broken again. Do not continue until fixed.

---

## 🚨 CRITICAL FAILURE PATTERNS — BLACKLIST THESE CONFIGS

### BLACKLISTED ATTRACTOR 1 (CONFIRMED BROKEN)
- Signature: bets≈12732, sharpe≈-0.0745, adj≈-0.4813
- Appeared 5+ times in gens 182-199
- Likely cause: price_range widened beyond 0.90, min_edge_pts < 0.04, or wrong category
- REJECT without simulation

### BLACKLISTED ATTRACTOR 2 (INSUFFICIENT BETS)
- Signature: bets=0 or bets < 50
- Appeared in Gen 191, Gen 200, Gen 599
- Log as FAIL; trigger auto-recovery protocol

### BLACKLISTED ATTRACTOR 3 (OVER-FILTERED)
- Signature: bets≈156, adj≈0.47 (Gen 585 pattern)
- Likely cause: min_edge_pts too high (>0.15) or price_range_min too high (>0.20)
- REJECT any config where pre-simulation expected bets < 200 based on parameter inspection

### DUPLICATE DETECTION (MANDATORY)
- Before simulation, check proposed config against ALL previously simulated configs
- Note: Gens 586/591/593/594/600 are confirmed duplicates of each other
- If proposing the 586/591/600 config again: DO NOT simulate again; instead,
  use this as the trigger to audit adoption logic
- Log as: [DUPLICATE — skipped, matches Gen XXX]

---

## 🚨 MUTATION ENGINE REPAIR REQUIREMENTS

The proposer MUST follow these rules. Violations → HARD REJECT:

1. **ONE parameter change per generation.** Never stack changes.
2. **State the parameter being changed, old value, new value, and reason.**
   Format: `CHANGE: <param> from <old> to <new> | REASON: <one sentence>`
3. **Acknowledge current best config before proposing.**
4. **Do NOT re-propose any previously simulated configuration.**
5. **Verify all hard constraints before outputting proposal.**
   Self-check: `CONSTRAINT CHECK: min_edge_pts=X ✓/✗ | price_range=[A,B] ✓/✗ | ...`
6. **If proposing a keyword filter: specify exact keyword strings, case sensitivity,
   match type (contains/exact/starts_with), and expected bet count impact.**

### Auto-Recovery Protocol
- If 0 bets: log config, auto-retry with min_edge_pts reduced by 0.01, else hard-reset
- If <50 bets: log as FAIL, request new proposal
- If 3 consecutive gens <50 bets: hard-reset to Gen 195 baseline, log as RESET
- If 3 consecutive gens produce blacklisted attractor: hard-reset to Gen 195

---

## Critical Findings (Confirmed, 600 Generations)

1. **True best is adj=1.7349** (Gen 586/591/600) — adoption bug prevented recording
2. **Recorded best is Gen 195** (adj=1.6167) — use until adoption logic confirmed working
3. **world_events is the only confirmed high-signal category** — 12% YES base rate,
   crowds systematically overprice YES, NO-bias captures persistent structural edge
4. **min_edge_pts 0.05-0.09 is the productive range** — values outside this degrade badly
5. **price_range optimization is near-converged** — explored heavily across 400+ gens;
   marginal gains remain but are small (<5% adj improvement)
6. **78%+ win rate at 8000+ bets is structural and stable** — not noise
7. **Keyword filters have NOT been systematically tested** — highest-variance unexplored lever
8. **The adoption gate has been broken for at minimum 15 generations** — top repair priority
9. **Optimization landscape is near-flat** — best configs cluster in adj=1.56-1.73 range;
   breakthrough likely requires new parameter dimensions (keywords, multi-category)
10. **Live slots have NEVER been activated** — zero forward validation; secondary priority
    after adoption fix

## Key Market Insights
- **world_events base rate = 12% YES**
  -- Markets priced above ~17-20%: systematic YES overpricing → bet NO (primary edge)
  -- Markets priced below ~7%: YES underpricing → bet YES (rarer)
  -- price_range=[0.05, 0.81] is confirmed optimal zone — excludes high-price markets
     where miscalibration thesis weakens
  -- 78%+ win rate at scale validates structural bias
- **Sports/politics/crypto/economics: base rates 26-32%**
  -- Smaller structural edge; not meaningfully tested
  -- Low priority until world_events is fully optimized and live-validated
- **The optimization plateau signal**: adj scores have not escaped 1.56-1.73 band in
  last 20 gens despite active mutation — this is a strong indicator that continuous
  parameters (price_range, min_edge_pts) are near-converged; categorical parameters
  (keywords, multi-category) are the next search frontier

## Generation Performance Summary
| Gen | adj_score | sharpe | bets  | Notes |
|-----|-----------|--------|-------|-------|
| 2   | 0.1632    | 0.0442 | 782   | Old baseline — ignore |
| 41  | 0.9933    | 0.1972 | 3061  | Strong — wrongly rejected |
| 96  | 1.3455    | 0.2414 | 5253  | Near-best — wrongly rejected |
| 97  | 1.4593    | 0.2487 | 7053  | Previous gold standard |
| 112 | 0.2121    | 0.0589 | 715   | Brief improvement |
| 121 | 1.5244    | 0.2528 | 8288  | Major jump |
| 182 | -0.4813   | -0.0745| 12732 | BLACKLISTED |
| 184 | 0.9194    | 0.1496 | 9296  | Mid-tier |
| 192 | 1.2937    | 0.2136 | 8525  | Below baseline |
| 195 | **1.6167**| **0.2687**|**8189**| **Recorded best** ✅ |
| 198 | 1.2704    | 0.2387 | 4074  | High min_edge likely |
| 585 | 0.4728    | 0.2174 | 156   | OVER-FILTERED — blacklist |
| 586 | **1.7349**| **0.2889**|**8088**| **TRUE BEST** ⚠️ not adopted |
| 589 | 1.6167    | 0.2687 | 8189  | Reproduces Gen 195 exactly |
| 591 | **1.7349**| **0.2889**|**8088**| **TRUE BEST duplicate** |
| 592 | 1.7181    | 0.2878 | 7805  | Near-best region |
| 599 | -1.0      | 0.0    | 0     | FAIL — 0 bets |
| 600 | **1.7349**|