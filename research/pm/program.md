```markdown
# FREYA Research Program — Prediction Markets (v7.0)

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

## 🚨 PRIORITY ZERO — FIX ADOPTION LOGIC BEFORE GEN 1001 🚨

### The Adoption Bug Has Recurred (Gens 982–1000)

**CONFIRMED EVIDENCE:**
- Gen 811 correctly adopted adj=1.7424 as new best ✅
- Gens 982, 985, 988, 989, 990, 992, 993, 994, 995, 997, 999, 1000 ALL reproduce
  adj=1.7424 and are logged [no_improvement] — logical impossibility ❌
- This is the SAME failure mode as Gens 586–600 (v6.0 incident)

**REQUIRED FIXES before Gen 1001:**
1. Confirm `current_best_adj` is read from a live mutable variable, NOT a constant
2. Confirm the comparison is `proposed_adj > current_best_adj` (strict greater-than)
3. Check that Gen 811's adoption actually wrote adj=1.7424 to the tracked variable
   (it may have written to a local scope that was then discarded)
4. Run validation test: simulate Gen 811 config, confirm adoption fires with
   explicit log: "proposed 1.7424 > current_best 1.7424 → NO (equal, not greater)"
   OR "proposed 1.7425 > current_best 1.7424 → YES"
5. The proposer cycling between two attractors suggests it is ALSO reading a stale
   baseline — fix both reader and writer atomically

### Why This Recurs
The root cause is likely that `current_best_adj` is initialized at program start from
a hardcoded value and the write-on-adoption path either fails silently or writes to
a different variable name than the one read during comparison. Every program restart
resets to the hardcoded value. Solution: persist `current_best_adj` to disk and read
from disk at every comparison.

---

## ✅ TRUE CURRENT BEST — Gen 811 (CONFIRMED)

- adj_score=1.7424, sharpe=0.2877, roi=20.882%, win=79.23%, bets=8523
- Confirmed: appeared as new_best in Gen 811, reproduced 11+ times in Gens 982–1000
- Config: world_events, min_edge_pts perturbed from v6.0 baseline
  (exact YAML below — reconstruct from Gen 811 logs if needed)
- THIS IS THE CANONICAL BASELINE FOR ALL COMPARISONS FROM GEN 1001 ONWARD

```yaml
# GEN 811 BEST — CANONICAL BASELINE v7.0
category: world_events
exclude_keywords: []
include_keywords: []
max_days_to_resolve: 30
max_position_pct: 0.1
min_edge_pts: 0.066        # NOTE: confirm exact value from Gen 811 log
min_liquidity_usd: 100
name: pm_research_best
price_range:
- 0.05
- 0.77                     # NOTE: confirm exact value from Gen 811 log
```

**⚠️ If Gen 811 exact YAML is unavailable:** reconstruct by simulating a grid of
min_edge_pts ∈ {0.060, 0.062, 0.064, 0.066, 0.068, 0.070} × price_range_max ∈
{0.75, 0.77, 0.79, 0.81} and selecting the config that reproduces adj=1.7424
exactly. Log as [RECONSTRUCTION] not [new_best].

## ✅ REFERENCE CONFIGS

| Gen | adj    | sharpe | bets | Notes                        |
|-----|--------|--------|------|------------------------------|
| 811 | 1.7424 | 0.2877 | 8523 | **CURRENT BEST** ✅           |
| 586/591/600 | 1.7349 | 0.2889 | 8088 | Previous true best     |
| 195 | 1.6167 | 0.2687 | 8189 | Old recorded best             |
| 121 | 1.5244 | 0.2528 | 8288 | Reference floor               |

---

## 🚨 BLACKLISTED CONFIGS — DO NOT SIMULATE

### BLACKLISTED ATTRACTOR 1 (CATASTROPHIC)
- Signature: bets≈12732, sharpe≈-0.0745, adj≈-0.4813
- Cause: price_range_max > 0.90 OR min_edge_pts < 0.04
- HARD REJECT before simulation

### BLACKLISTED ATTRACTOR 2 (ZERO BETS)
- Signature: bets=0 or bets < 50
- Log as FAIL; trigger auto-recovery

### BLACKLISTED ATTRACTOR 3 (OVER-FILTERED)
- Signature: bets≈156, adj≈0.47
- Cause: min_edge_pts > 0.15 OR price_range_min > 0.20
- REJECT if pre-simulation expected bets < 200

### BLACKLISTED ATTRACTOR 4 (FROZEN CYCLE — NEW v7.0)
- Signature A: adj=1.7424, bets=8523 (Gen 811 / Attractor A)
- Signature B: adj=1.722, bets=8051 (Attractor B)
- These two configs have been simulated 15+ combined times with zero marginal value
- **DO NOT PROPOSE EITHER CONFIG AGAIN**
- If proposer outputs a config that would reproduce either signature:
  log as [DUPLICATE — frozen cycle], skip simulation, force keyword exploration

---

## ⚠️ GENERATION LOGGING REQUIREMENT (MANDATORY)

After EVERY generation, log ALL fields:
```
proposed_config: (full YAML)
proposed_adj: X.XXXX
proposed_sharpe: X.XXXX
proposed_bets: NNNN
current_best_adj: X.XXXX  ← MUST be dynamically read from persisted store
comparison_result: [new_best / no_improvement / DUPLICATE / FAIL / INVALID]
adoption_check: "proposed X.XXXX > current_best X.XXXX → [YES/NO]"
reason_if_rejected: (explicit)
```

**ADOPTION RULE (write literally each generation):**
```
IF proposed_adj > current_best_adj:
    → adopt; update persisted current_best_adj; log [new_best]
ELSE:
    → log [no_improvement]
```

**HALT CONDITIONS:**
- If any gen achieves adj > 1.70: verify adoption fired correctly before continuing
- If 3 consecutive gens show adj > 1.65 and [no_improvement]: HALT, fix adoption
- If 5 consecutive gens reproduce adj=1.7424 or adj=1.722: HALT, adoption frozen

---

## 🔬 RESEARCH AGENDA — NEXT 100 GENERATIONS (1001–1100)

### PHASE 1: Adoption Validation (Gens 1001–1005)
**DO NOT explore new configs yet.**
- Gen 1001: Simulate Gen 811 config exactly. Log result. Verify current_best_adj=1.7424.
- Gen 1002: Simulate a config known to be slightly below best (e.g., Gen 195 config).
  Verify adoption does NOT fire. Confirm current_best_adj still reads 1.7424.
- Gen 1003: Simulate a config with artificially high expected adj (e.g., min_edge_pts
  slightly adjusted to target ~1.75). Verify adoption fires if result > 1.7424.
- If all three pass: adoption logic confirmed. Proceed to Phase 2.
- If any fail: stop, fix, retest.

### PHASE 2: Keyword Filter Exploration (Gens 1006–1060)
**This is the highest-priority unexplored dimension.**

After 1000 generations, include_keywords and exclude_keywords have NEVER been tested
(kw=0 in all configs). Given world_events is the confirmed signal category, keyword
segmentation is the highest-variance remaining lever.

#### 2A: Exclusion Filters (Expected: reduce noise, improve sharpe)
Test these exclude_keywords lists ONE AT A TIME, one per generation:
- `["sport", "football", "soccer", "basketball", "tennis"]`
  — removes sports-adjacent markets miscategorized as world_events
- `["stock", "price", "bitcoin", "crypto", "ethereum"]`
  — removes finance-adjacent world_events
- `["poll", "approval", "rating", "survey"]`
  — removes opinion-polling markets (may have different calibration)
- `["will.*win", "championship", "tournament", "league"]`
  — regex-style: competitive outcome markets
- `["earthquake", "hurricane", "flood", "disaster"]`
  — tests whether natural disaster markets have different YES rate

For each: log keyword list, expected bet count change, observed bets, adj delta.

#### 2B: Inclusion Filters (Expected: isolate highest-signal subcategories)
Test these include_keywords lists ONE AT A TIME:
- `["war", "conflict", "military", "attack"]`
  — geopolitical conflict subcategory
- `["election", "vote", "referendum", "ballot"]`
  — electoral world_events (may overlap with politics)
- `["death", "resign", "arrest", "sanction"]`
  — leadership/legal event subcategory
- `["nuclear", "missile", "invasion", "ceasefire"]`
  — high-stakes geopolitical
- `["UN", "treaty", "agreement", "summit"]`
  — diplomatic events

For each: expect bets to DROP significantly. If bets < 200: log [OVER-FILTERED], skip.
Target: find subcategory with adj > 1.7424 at bets > 500.

#### 2C: Combined Keyword Strategy (Gens 1051–1060)
- Take best exclusion filter from 2A + best inclusion filter from 2B
- Test combined config
- If bets < 200: relax one filter; retry

### PHASE 3: Multi-Category Exploration (Gens 1061–1080)
**Only if Phase 2 fails to beat adj=1.7424.**

Test adding a second category alongside world_events:
- `[world_events, politics]`: combined