```markdown
# FREYA Research Program — Prediction Markets (v14.0)

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

## 🏆 SYSTEM STATE — GEN 2600

- **Current best:** adj=2.6747, sharpe=1.6723, roi=44.3%, win=100%, bets=79
  (Gen 2410, world_events, include_kw=11 Middle East terms, max_days=14)
- **Generations since last improvement:** ~190 (Gen 2410 was last [new_best])
- **Status: CRITICAL ATTRACTOR LOCK-IN — GEN 2410 CONFIG DOMINATING ALL PROPOSALS**
- Gens 2411–2600: 0 improvements; ~15 of last 20 gens returning identical adj=2.6747
- **DUPLICATE CASCADE ALERT (CRITICAL):** seen_configs.json fingerprint check appears
  to be FAILING. 15+ gens with identical results = proposer is replaying Gen 2410 config
  or configs that map to identical 79-bet universe. DIAGNOSE BEFORE GEN 2601.
- **ERROR CASCADE ALERT (ONGOING):** ~5% of recent gens returning adj=0/bets=0.
  Infrastructure fault unresolved. Error gens do not count toward improvement streaks.
- **NEAR-ZERO-BET ATTRACTOR (ACTIVE):** Gens returning bets=6–14 (adj=-1.0) indicate
  proposer is occasionally generating over-filtered configs. Hard reject < 500 bets.
- **LIVE SLOTS:** mist/kara/thrud all disabled — no live validation available.
  PRIORITY: Re-enable at least one live slot to validate Gen 2410 signal durability.

---

## 📊 KEY DISCOVERY: THE HIGH-SHARPE GEOPOLITICAL NICHE

**Gen 2410 is the most important result in this research program.**
- adj=2.6747 (38% above previous best of 1.9387)
- sharpe=1.6723 (5x previous best sharpe of 0.3248)
- roi=44.3%, win=100% on 79 bets
- Config: world_events, include_keywords=[iran, israel, palestine, syria, lebanon,
  iraq, turkey, saudi, yemen, afghanistan, armenia], max_days_to_resolve=14,
  min_edge_pts=0.065, price_range=[0.05, 0.77]

**Interpretation:** Middle Eastern geopolitical markets are severely overpriced by
crowds due to availability heuristic and narrative salience bias. Historical YES
resolution rate in this sub-niche is likely 5–8%, vs. 12% world_events base rate,
while crowds price these markets at 25–40%+. This is a structural miscalibration.

**Critical risks:**
1. bets=79 is dangerously low — log(79/20+1)=1.599 vs. log(390/20+1)=3.045 for 390 bets.
   Doubling bets while maintaining sharpe>0.9 would yield adj≈5.1. This is the primary target.
2. 100% win rate on 79 bets may reflect overfitting to historical data. Live validation required.
3. The 190-gen stagnation since Gen 2410 suggests the neighborhood has been exhausted
   with the current include_keywords + exclude_keywords + price_range combination.

---

## 🔴 CRITICAL: DUPLICATE CASCADE DIAGNOSIS (MANDATORY — v14.0)

**BEFORE ANY SIMULATION IN GEN 2601+:**

The seen_configs.json must be audited. The following check must be performed:

```python
def audit_duplicate_cascade():
    """Run before Gen 2601. Check for fingerprint check failures."""
    # Count how many gens 2411-2600 returned adj=2.6747, sharpe=1.6723, bets=79
    # If > 5 gens returned identical results: seen_configs.json is BROKEN
    # Fix: Rebuild seen_configs.json from all logged fingerprints
    # Then: Force structural departure from Gen 2410 config as first proposal
    
    # FORCED STRUCTURAL DEPARTURE RULE (v14.0):
    # Gen 2601 MUST differ from Gen 2410 on at least TWO of these axes:
    # - include_keywords (add/remove/replace keywords)
    # - max_days_to_resolve (change by >= 7 days)
    # - price_range (change either bound by >= 0.05)
    # - min_edge_pts (change by >= 0.005)
    # Proposals that differ on only ONE axis: REJECTED as likely duplicate-universe
```

---

## 🔴 PROPOSER CONSTRAINT PROTOCOL (MANDATORY v14.0)

The proposer MUST maintain a `seen_configs.json` file containing the fingerprint of
every configuration ever simulated. **AUDIT REQUIRED AT GEN 2601 STARTUP.**

```python
def fingerprint(config):
    return (
        config["category"],
        round(config["min_edge_pts"], 4),
        round(config["price_range"][0], 3),
        round(config["price_range"][1], 3),
        config["max_days_to_resolve"],
        tuple(sorted(config.get("include_keywords", []))),
        tuple(sorted(config.get("exclude_keywords", [])))
    )

def bet_universe_fingerprint(config):
    """NEW v14.0: Secondary deduplication on bet universe, not just config params.
    If two configs produce identical sets of market IDs bet on: they are functionally
    identical even if config params differ. Log bet_universe_fingerprint separately."""
    return hash(frozenset(get_bet_market_ids(config)))
```

**BEFORE ANY SIMULATION:**
1. Compute config fingerprint AND bet_universe_fingerprint
2. Check BOTH against seen_configs.json
3. If EITHER fingerprint exists: LOG [DUPLICATE — seen gen NNN], DO NOT SIMULATE
4. If both are new: add both to seen_configs.json, proceed

**HARD REJECTION RULES (v14.0):**
```python
def pre_simulation_guard(config):
    # Rule 1: Catastrophic low-bet attractor prevention
    if expected_bets(config) < 500:
        raise HardReject("expected_bets < 500 — catastrophic attractor risk")
    # Rule 2: Blacklisted edge/range combinations
    if config["min_edge_pts"] < 0.04:
        raise HardReject("min_edge_pts < 0.04 — negative sharpe attractor")
    if config["price_range"][1] > 0.90:
        raise HardReject("price_range_max > 0.90 — fee-drag attractor")
    if config["min_edge_pts"] > 0.15:
        raise HardReject("min_edge_pts > 0.15 — over-filtered attractor")
    if config["price_range"][0] > 0.20:
        raise HardReject("price_range_min > 0.20 — over-filtered attractor")
    # Rule 3: Keyword overload
    if len(config.get("exclude_keywords", [])) > 15 and \
       (config["price_range"][1] - config["price_range"][0]) < 0.30:
        raise HardReject("keyword overload with narrow price range — zero-bet risk")
    # Rule 4: Mid-range attractor rejection
    if 1500 <= expected_bets(config) <= 2500 and config["category"] == "world_events" \
       and not config.get("include_keywords"):
        raise HardReject("mid-range world_events attractor — sharpe≈0.165 basin, BLACKLISTED")
    # Rule 5: Error cascade guard
    if consecutive_errors >= 3:
        raise HardReject("3+ consecutive errors — infrastructure fault, halt and diagnose")
    # Rule 6: Local optimum echo prevention
    if expected_adj_delta(config, current_best_adj=2.6747) < 0.001:
        raise HardReject("insufficient differentiation from current best — force structural change")
    # Rule 7 (NEW v14.0): Attractor lock-in prevention
    if includes_all_keywords(config, GEN_2410_INCLUDE_KW) and \
       abs(config["max_days_to_resolve"] - 14) < 7 and \
       abs(config["min_edge_pts"] - 0.065) < 0.005:
        raise HardReject("Gen 2410 attractor neighborhood — force departure on 2+ axes")
    # Rule 8 (NEW v14.0): Bet universe identity check
    if bet_universe_fingerprint(config) in seen_bet_universes:
        raise HardReject("identical bet universe to previously seen config — functionally duplicate")
```

**ADDITIONAL DIVERSITY ENFORCEMENT (v14.0):**
- If 3 consecutive proposals reproduce adj within 0.01 of 2.6747: FORCE structural
  change (different include_keywords OR change max_days_to_resolve by >=14 days)
- If 5 consecutive proposals have bets < 500: HALT, reset to Gen 2410 baseline and
  widen all filters by 20% before next proposal
- If 3 consecutive gens return error (adj=0, bets=0): HALT, diagnose infrastructure
- Proposer must explicitly state research phase for every generation
- Proposer must log which exploration axis is being tested each gen

---

## 🔴 ADOPTION LOGIC (MANDATORY — unchanged)

```python
def maybe_adopt(proposed_adj, proposed_config, gen_id):
    current = load_from_disk("best_adj.json")  # always read from disk
    if proposed_adj > current["adj"]:
        write_to_disk("best_adj.json", {
            "adj": proposed_adj,
            "gen": gen_id,
            "config": proposed_config
        })
        fsync()
        log(f"[new_best] proposed {proposed_adj} > current {current['adj']} → ADOPTED")
        return True
    else:
        log(f"[no_improvement] proposed {proposed_adj} <= current {current['adj']} → REJECTED")