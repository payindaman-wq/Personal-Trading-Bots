```markdown
# FREYA Research Program — Prediction Markets (v15.0)

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

## 🏆 SYSTEM STATE — GEN 2800

- **Current best:** adj=2.6747, sharpe=1.6723, roi=44.3%, win=100%, bets=79
  (Gen 2410, world_events, include_kw=11 Middle East terms, max_days=14)
- **Generations since last improvement:** 390 (Gen 2410 was last [new_best])
- **Status: COMPLETE ATTRACTOR COLLAPSE — ARCHITECTURAL RESET REQUIRED**

### Dead Zone Summary (Gens 2411–2800)
- 0 improvements across 390 generations
- Only 3–4 distinct outcomes observed in last 20 gens:
  - adj=2.6747 (bets=79): Gen 2410 exact clone — FULLY EXHAUSTED
  - adj=2.6724 (bets=76): Near-twin universe — FULLY EXHAUSTED
  - adj=0.3647 (bets=105): Diluted-sharpe attractor — BLACKLISTED
  - adj=-1.0 (bets=2): Over-filter catastrophe — BLACKLISTED
- seen_configs.json fingerprinting has FAILED — proposer is replaying dead configs
- Bet-universe deduplication was never successfully implemented
- **ALL LIVE SLOTS DISABLED — no live validation of Gen 2410 signal**

---

## 🧠 CORE INSIGHT: THE GEN 2410 DISCOVERY

**Gen 2410 remains the most important result in this research program.**
- adj=2.6747, sharpe=1.6723, roi=44.3%, win=100%, bets=79
- Config: world_events, include_keywords=[iran, israel, palestine, syria, lebanon,
  iraq, turkey, saudi, yemen, afghanistan, armenia], max_days_to_resolve=14,
  min_edge_pts=0.065, price_range=[0.05, 0.77]

**Why it works (theoretical basis):**
Crowd availability heuristic + narrative salience bias causes systematic YES overpricing
on Middle East crisis/escalation markets. True YES resolution rate ≈ 5–8% in this
sub-niche vs. 12% world_events base rate. Crowds price these at 25–40%+.
Betting NO captures this structural miscalibration.

**Why it is stuck:**
- bets=79 is too small. log(79/20+1)=1.599 vs. log(500/20+1)=3.219.
  Maintaining sharpe≥1.0 with 500 bets → adj≈3.2. This is the primary target.
- 100% win rate on 79 bets likely contains survivorship bias. Live validation critical.
- The 11-keyword Middle East universe has been fully mined at max_days=14.
  Every adjacent config maps back to the same 79-bet pool or destroys sharpe.

**The key unlock:** MORE BETS at acceptable sharpe, not higher sharpe on 79 bets.
Target: bets ≥ 300, sharpe ≥ 0.9 → adj ≥ 2.7 (improvement territory).
Stretch target: bets ≥ 500, sharpe ≥ 1.0 → adj ≥ 3.2.

---

## 🔴 ARCHITECTURAL RESET — v15.0 MANDATORY PROTOCOL

**The proposer MUST implement all of the following before Gen 2801:**

### Step 1: Rebuild seen_configs.json
```python
def rebuild_seen_configs():
    """
    Scan ALL generation logs from gen 1 to gen 2800.
    Extract config fingerprint AND bet_universe_fingerprint for every gen.
    Rebuild seen_configs.json from scratch.
    Verify: should contain ~2800 entries (minus error gens).
    If < 2000 entries: fingerprinting was broken — log warning.
    """
    pass
```

### Step 2: Implement Bet-Universe Deduplication (MANDATORY — was never working)
```python
def bet_universe_fingerprint(config):
    """
    Run simulation, capture the EXACT SET of market IDs that receive bets.
    Return hash(frozenset(market_ids)).
    This is the ONLY reliable deduplication method.
    Config params that look different can produce identical bet universes.
    """
    market_ids = get_bet_market_ids(config)  # must be implemented
    return hash(frozenset(market_ids))

def pre_simulation_guard(config):
    cfg_fp = fingerprint(config)
    bet_fp = bet_universe_fingerprint(config)
    
    if cfg_fp in seen_config_fingerprints:
        raise HardReject(f"Config fingerprint seen before — DUPLICATE")
    if bet_fp in seen_bet_universe_fingerprints:
        raise HardReject(f"Bet universe fingerprint seen before — FUNCTIONALLY DUPLICATE")
    
    seen_config_fingerprints.add(cfg_fp)
    seen_bet_universe_fingerprints.add(bet_fp)
```

### Step 3: Blacklist the Three Known Attractors
```python
BLACKLISTED_BET_UNIVERSES = {
    # Add frozenset of market IDs for bets=79 universe (Gen 2410)
    # Add frozenset of market IDs for bets=76 universe (Gen 2410 near-twin)
    # Add frozenset of market IDs for bets=105 universe (adj=0.3647 attractor)
    # These must be logged at startup and never re-simulated
}
```

---

## 🗺️ RESEARCH PHASES — GEN 2801–2900

**The proposer MUST explicitly label each generation with its Phase and Axis.**
**No more than 10 consecutive gens on the same Phase without rotation.**

---

### PHASE A: GEOGRAPHIC EXPANSION (Gens 2801–2820)
**Hypothesis:** The availability-bias overpricing phenomenon extends beyond the 11
Middle East keywords to other high-salience geopolitical conflict zones.
Adding actors/regions should increase bet count while preserving sharpe.

**Exploration axes:**
- A1: Add South/Central Asia actors: `pakistan, kashmir, india, myanmar, bangladesh`
- A2: Add East Asia actors: `korea, taiwan, china, philippines, japan`  
  (note: china was in exclude_kw — remove that exclusion, test include_kw only)
- A3: Add Africa conflict zones: `ethiopia, sudan, somalia, mali, sahel, nigeria, congo`
- A4: Add Latin America instability: `venezuela, colombia, haiti, nicaragua, cuba`
- A5: Add non-Middle-East nuclear/WMD terms: `nuclear, missile, warhead, proliferation`
  (exclude Middle East terms to test if signal is geographic or topic-based)
- A6: UNION test — combine ALL geographic expansions, measure bets and sharpe
- A7: Test max_days=21 with original 11 keywords (time expansion, not geographic)
- A8: Test max_days=7 with original 11 keywords (tighter time = sharper signal?)
- A9: Test max_days=30 with original 11 keywords (more bets, likely sharpe dilution)
- A10: Test max_days=60 with original 11 keywords (maximum bet count test)

**Accept criteria for Phase A:** bets ≥ 150, sharpe ≥ 0.9 → continue Phase A
**Reject criteria:** if best Phase A result has bets < 150 OR sharpe < 0.7 → move to Phase B

---

### PHASE B: CROSS-CATEGORY AVAILABILITY BIAS (Gens 2821–2840)
**Hypothesis:** Availability bias overpricing may exist in politics and economics
categories for specific high-salience event types.

**Exploration axes:**
- B1: politics + include_kw=[impeach, resign, removal, coup, overthrow, recall]
  min_edge_pts=0.06, max_days=30
- B2: politics + include_kw=[sanction, embargo, expel, ban, veto, override]
  min_edge_pts=0.06, max_days=21
- B3: politics + include_kw=[referendum, secession, independence, separatist]
  min_edge_pts=0.065, max_days=60
- B4: economics + include_kw=[default, bankruptcy, collapse, recession, crash]
  min_edge_pts=0.07, max_days=30
- B5: economics + include_kw=[sanction, tariff, embargo, trade war, freeze]
  min_edge_pts=0.065, max_days=21
- B6: Test politics category with Gen 2410's exact 11 Middle East keywords
  (does the signal exist in politics-categorized Middle East markets too?)
- B7: world_events + include_kw focused on NATURAL DISASTER overpricing:
  [earthquake, tsunami, hurricane, typhoon, volcano, flood, wildfire]
  Hypothesis: disaster escalation also overpriced
- B8: world_events + include_kw focused on TERRORISM overpricing:
  [terror, attack, bombing, assassination, hostage, kidnap]
- B9: world_events + include_kw focused on HEALTH CRISIS overpricing:
  [outbreak, epidemic, virus, pathogen, quarantine, lockdown]
- B10: Cross-category test — run same keywords across ALL categories, compare sharpe

---

### PHASE C: PRICE RANGE SURGERY (Gens 2841–2855)
**Hypothesis:** The current [0.05, 0.77] range may include high-priced markets
(0.50–0.77) that dilute sharpe. Tightening the upper bound may improve sharpe
while the lower bound expansion may capture more NO bets.

**Exploration axes:**
- C1: price_range=[0.05, 0.60] — exclude expensive YES markets
- C2: price_range=[0.05, 0.50] — only bet when crowd prices ≤ 50%
- C3: price_range=[0.05, 0.70] — minor tighten from 0.77
- C4: price_range=[0.03, 0.77] — expand lower bound (more aggressive NO bets)
- C5: price_range=[0.10, 0.77] — exclude very cheap markets (possible noise)
- C6: price_range=[0.05, 0.55], min_edge_pts=0.055 — combined adjustment
- C7: price_range=[0.05, 0.85] — test whether 0.77 cap is overly conservative
  (note: 0.90 is blacklisted; 0.85 is within bounds)
- C8: Split testing — run C1 and C4 simultaneously, compare bet universes
- C9: Test whether price_range surgery on bets=105 attractor reveals what's
  destroying sharpe (diagnostic, not improvement-seeking)

---

### PHASE D: EDGE THRESHOLD CALIBRATION (Gens 2856–2870)
**Hypothesis:** min_edge_pts=0.065 was optimal for