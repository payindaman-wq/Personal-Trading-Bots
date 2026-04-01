```markdown
# FREYA Research Program — Prediction Markets (v16.0)

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

## 🏆 SYSTEM STATE — GEN 3200

- **Current best:** adj=1.2132, sharpe=0.208, roi=16.1%, win=75.3%, bets=6807
  (Gen 3144, world_events, no keywords, perturb:min_edge_pts)
- **Secondary reference:** adj=2.6747, sharpe=1.6723, roi=44.3%, win=100%, bets=79
  (Gen 2410 — STATUS UNKNOWN, see Critical Diagnostic below)
- **Generations since last improvement:** 56 (Gen 3144 was last [new_best])
- **Status: ATTRACTOR COLLAPSE — DUAL DEAD ZONE ACTIVE**

### Dead Zone Summary (Gens 3145–3200)
- 0 improvements across 56 generations
- Only 3 distinct outcomes in last 20 gens:
  - adj=1.2132 (bets=6807): Current best exact clone — appears 2x — EXHAUSTED
  - adj=-0.458 (bets=78): Broken small-bet attractor — appears 8x — BLACKLIST
  - adj≈0.36 (bets=193): Mid-range attractor — appears 2x — LOW PRIORITY
- Deduplication is failing: proposer is replaying dead configs
- **ALL LIVE SLOTS DISABLED — no live validation active**

---

## 🚨 CRITICAL DIAGNOSTIC — MUST RUN BEFORE GEN 3201

**The entire research strategy depends on resolving this ambiguity.**

The v15.0 program was built around Gen 2410 (adj=2.6747, bets=79, 11 Middle East
keywords). The Gen 3001–3200 results show NO keyword-filtered improvements and a
completely different best config (no keywords, bets=6807). This discontinuity must
be explained before further keyword-based exploration.

### Diagnostic Gen D1 — Exact Gen 2410 Replay
```yaml
category: world_events
include_keywords: [iran, israel, palestine, syria, lebanon, iraq, turkey, saudi, 
                   yemen, afghanistan, armenia]
exclude_keywords: []
max_days_to_resolve: 14
min_edge_pts: 0.065
price_range: [0.05, 0.77]
min_liquidity_usd: 200
max_position_pct: 0.1
```

**Interpretation matrix:**
| Result | Meaning | Action |
|--------|---------|--------|
| bets≈79, sharpe≈1.67 | Keyword filter intact, Gen 2410 real | Proceed Phase A |
| bets=6807, sharpe≈0.208 | Keywords silently ignored by simulator | Fix keyword filter, halt Phase A–D |
| bets=0 | Over-filtering or keyword mismatch | Check keyword syntax, fix filter |
| bets=79, sharpe<<1.67 | Universe same, base rate changed | Recalibrate and proceed |

**Do NOT proceed to Phase A or any keyword-based phase until D1 is run and
the keyword filter is confirmed working. Log D1 result explicitly.**

### Diagnostic Gen D2 — Minimal Keyword Sanity Check
If D1 shows keywords are ignored, run this to confirm:
```yaml
category: world_events
include_keywords: [war]
max_days_to_resolve: 30
min_edge_pts: 0.05
price_range: [0.05, 0.90]
```
Expected: bets should be substantially fewer than 6807.
If bets≈6807: keyword filter is completely broken. Escalate immediately.

---

## 🧠 TWO-TRACK UNDERSTANDING

### Track 1: The Gen 2410 Signal (IF KEYWORD FILTER IS WORKING)
- Config: world_events + 11 Middle East keywords + max_days=14 + min_edge=0.065
- adj=2.6747, sharpe=1.6723, roi=44.3%, win=100%, bets=79
- Theoretical basis: availability bias causes systematic YES overpricing on
  Middle East crisis markets. True YES rate ≈5–8% vs. 12% category base rate.
  Crowds price at 25–40%+. Betting NO captures this miscalibration.
- Limitation: bets=79 is small. Target: 300+ bets at sharpe≥0.9.
- Note: 100% win rate on 79 bets contains survivorship risk. Needs live validation.

### Track 2: The Broad World_Events Signal (CONFIRMED WORKING)
- Config: world_events, no keywords, min_edge≈0.057–0.059, price_range≈[0.07, 0.80]
- adj=1.2132, sharpe=0.208, roi=16.1%, win=75.3%, bets=6807
- Theoretical basis: world_events 12% base rate + crowd overpricing broadly.
  Weak but consistent NO-bias across the full category.
- Limitation: sharpe=0.208 is low. Any regime shift could flip negative.
- This is a real, replicable signal but not the primary optimization target.

**Primary target:** adj ≥ 1.5, sharpe ≥ 0.5, bets ≥ 500
**Stretch target:** adj ≥ 2.5, sharpe ≥ 1.0, bets ≥ 300

---

## 🔴 MANDATORY DEDUPLICATION PROTOCOL (v16.0 — NON-NEGOTIABLE)

The bets=78 attractor (adj=-0.458) appeared 8 times in the last 20 gens.
The bets=6807 attractor appeared as exact clone twice.
This represents complete proposer failure. The following must be enforced:

### Blacklisted Bet Universes (by bet count signature + adj score)
```python
HARD_BLACKLIST = [
    {"bets": 78, "adj": -0.458},      # broken small-bet attractor
    {"bets": 92, "adj": -0.7536},     # broken mid-small attractor  
    {"bets": 153, "adj": -0.0258},    # marginal attractor
    {"bets": 194, "adj": -0.303},     # near-miss attractor
]
# Any config returning these exact (bets, adj) pairs is REJECTED pre-simulation
# using bet-universe fingerprinting.
```

### Deduplication Guard (must be implemented before Gen 3201)
```python
def pre_simulation_guard(config):
    cfg_fp = hash(frozenset(config.items()))
    
    if cfg_fp in seen_config_fingerprints:
        raise HardReject("Config fingerprint seen before")
    
    # Run lightweight pre-sim to get bet count
    preview_bets = estimate_bet_count(config)
    for blacklisted in HARD_BLACKLIST:
        if abs(preview_bets - blacklisted["bets"]) < 3:
            raise HardReject(f"Bet count matches blacklisted attractor: {blacklisted}")
    
    seen_config_fingerprints.add(cfg_fp)
```

---

## 🗺️ RESEARCH PHASES — GEN 3201–3300

**ALL PHASES contingent on D1/D2 diagnostic result.**
**Label every generation: Phase, Axis, and D1-status (verified/unverified).**
**No more than 8 consecutive gens on same Phase without rotation.**

---

### PHASE D: DIAGNOSTIC (Gens 3201–3205) — MANDATORY FIRST
Run D1 and D2 as described above. Log results. Branch:
- If keyword filter working → proceed Phase A
- If keyword filter broken → proceed Phase E (no-keyword optimization)

---

### PHASE A: KEYWORD SIGNAL EXPANSION (Gens 3206–3230)
*Only execute if D1 confirms keyword filter working and bets≈79, sharpe≈1.67*

**Hypothesis:** The availability-bias overpricing phenomenon extends beyond the 11
Middle East keywords to other high-salience geopolitical conflict zones.
Adding regions should increase bet count while preserving sharpe.

**Exploration axes (execute in order, stop early if sharpe < 0.7):**

- A1: Add South/Central Asia: original 11 + [pakistan, kashmir, myanmar, bangladesh]
  max_days=14, min_edge=0.065, price_range=[0.05, 0.77]
  
- A2: Add East Asia: original 11 + [taiwan, korea, philippines]
  (note: remove any china exclude_kw, test include_kw only)
  max_days=14, min_edge=0.065, price_range=[0.05, 0.77]
  
- A3: Add Africa conflicts: original 11 + [ethiopia, sudan, somalia, mali, congo]
  max_days=14, min_edge=0.065, price_range=[0.05, 0.77]
  
- A4: UNION test — all A1+A2+A3 additions combined with original 11
  max_days=14, min_edge=0.065, price_range=[0.05, 0.77]
  Target: bets ≥ 150, sharpe ≥ 0.9
  
- A5: Time expansion — original 11 keywords, max_days=21
  (more bets from same geographic signal)
  
- A6: Time expansion — original 11 keywords, max_days=30
  
- A7: Time expansion — A4 union keywords, max_days=21
  (geographic + time expansion combined)
  
- A8: Time compression — original 11 keywords, max_days=7
  (tighter time window = sharper signal?)
  
- A9: Terrorism sub-signal: world_events + [terror, attack, bombing, assassination,
  hostage, kidnap, militant, insurgent] max_days=14, min_edge=0.065
  (test if availability bias extends to terrorism without geographic filter)
  
- A10: Natural disaster sub-signal: world_events + [earthquake, tsunami, hurricane,
  typhoon, volcano, flood, wildfire] max_days=14, min_edge=0.065
  (test if disaster escalation also overpriced)

**Accept criteria:** bets ≥ 150, sharpe ≥ 0.9 → continue Phase A
**Reject criteria:** if best Phase A result has bets < 100 OR sharpe < 0.7 → move to Phase B

---

### PHASE B: CROSS-CATEGORY KEYWORD SIGNALS (Gens 3231–3250)
*Execute regardless of D1 result — some axes use no keywords*

**Hypothesis:** Availability