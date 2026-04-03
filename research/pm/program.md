```markdown
# FREYA Research Program — Prediction Markets (v29.0)

## Status at Gen 5800
- **2,800 generations without improvement** (Gens 3001–5800).
  Confirmed ceiling: adj=1.6196, sharpe=0.2458, bets=14510.
- **All three v28.0 pre-conditions remain unimplemented in code.**
  This is now the sixth version cycle of documentation without implementation.
  v29.0 treats implementation failure as the PRIMARY research finding.
- **Deterministic grid (v28.0, Gens 5601–5700) was NOT EXECUTED.**
  LLM loop continued running through all 200 gens (5601–5800).
  Evidence: adj=1.5117 appeared 9+ times in final 20 gens alone.
  Evidence: adj=-1.0/bets=0 appeared twice (Gens 5785, 5793) — guard not active.
- **Signal 2 is now fully characterized by repetition:**
  adj=1.5117, sharpe=0.229, bets=14707 — seen 15+ times total.
  Config is almost certainly world_events with one loosened parameter.
  Must be logged with full config on next occurrence.
- **Live slots (mist, kara, thrud): STILL DISABLED. Zero live bets ever placed.**
  This is no longer acceptable. See mandatory live deployment below.

---

## ROOT CAUSE STATEMENT

The loop has been running for 2,800 generations without improvement because:

1. **The LLM proposer has no memory.** It re-proposes configs it has already
   tried. Signal 2 has been rediscovered 15+ times. This is the dominant
   failure mode.
2. **The guard system is not implemented.** Degenerate configs (bets=0, bets=3)
   still reach evaluation. This wastes generation slots.
3. **Config persistence is not implemented.** When a config produces a
   notable result, its parameters are not recorded. Recovery attempts fail.
4. **The deterministic grid has never executed.** Five version cycles have
   specified it. Zero have implemented the suspension mechanism.
5. **No live deployment.** 5,800 generations of simulation with zero
   real-world validation.

v29.0 addresses these in strict priority order. Nothing else matters until
items 1–3 are fixed.

---

## MANDATORY ACTIONS BEFORE GEN 5801
### (Loop is FROZEN until all four pass)

These are not documented aspirations. They are gate conditions.
If your execution environment cannot enforce these gates, halt the loop
and report that fact explicitly rather than continuing to run LLM proposals.

---

### GATE 1: Implement Config Deduplication (HIGHEST PRIORITY)

This is the single most impactful change available. Without it, the LLM
will continue rediscovering Signal 2 indefinitely.

```python
# Persistent seen-configs registry (survives process restarts)
SEEN_CONFIGS = load_seen_configs_from_disk()  # set of config hashes

def get_next_config(gen_number):
    if SUSPENSION_ACTIVE and SUSPENSION_START <= gen_number <= SUSPENSION_END:
        return deterministic_grid.next()

    # LLM proposal with deduplication
    for attempt in range(10):
        candidate = llm_propose()
        h = hash_config(candidate)
        if h not in SEEN_CONFIGS:
            SEEN_CONFIGS.add(h)
            save_seen_configs_to_disk(SEEN_CONFIGS)
            return candidate
        log_duplicate_skip(gen_number, h, attempt)

    # If 10 attempts all duplicate, force a grid config
    log_dedup_exhaustion(gen_number)
    return fallback_grid.next()
```

**Test:** Propose the baseline config twice. Second proposal must be
rejected and logged as duplicate. Log "DEDUP_TEST_PASS" or halt.

---

### GATE 2: Implement Guard System (Same as v28.0 — must actually run)

```python
MIN_BETS_FLOOR = 501

def run_generation(config, gen_number):
    # STAGE 1: Pre-simulation estimate
    estimated = estimate_bets(config)
    if estimated <= 500:
        log_hard_reject(gen_number, config, "PRE_SIM_REJECT", estimated)
        return None

    # STAGE 2: Simulation
    result = simulate(config)

    # STAGE 3: Post-simulation check
    if result.bets <= 500:
        log_hard_reject(gen_number, config, "POST_SIM_REJECT", result.bets)
        return None

    # STAGE 4: Negative sharpe + high volume guard
    if result.sharpe < -0.01 and result.bets > 10000:
        log_hard_reject(gen_number, config, "NEG_SHARPE_HIGH_VOL", result)
        blacklist_config(config)
        return None

    # STAGE 5: Normal evaluation
    persist_result(gen_number, config, result)
    evaluate_and_update(result)
    return result
```

**Required test cases — all eight must log PASS before Gen 5801:**
```
Test 1: estimated=0      → PRE_SIM_REJECT    ✓
Test 2: estimated=499    → PRE_SIM_REJECT    ✓
Test 3: estimated=500    → PRE_SIM_REJECT    ✓
Test 4: estimated=501    → passes to sim     ✓
Test 5: sim bets=0       → POST_SIM_REJECT   ✓
Test 6: sim bets=500     → POST_SIM_REJECT   ✓
Test 7: sim bets=501     → accepted          ✓
Test 8: sim bets=18700, sharpe=-0.035 → NEG_SHARPE_HIGH_VOL + blacklist ✓
```

---

### GATE 3: Implement Config Persistence (Same as v28.0 — must actually run)

```python
def persist_result(gen, config, result):
    if result.adj > 1.0 or result.bets > 5000:
        record = {
            "gen": gen,
            "config_hash": hash_config(config),
            "config": config,
            "bets": result.bets,
            "sharpe": result.sharpe,
            "adj_score": result.adj,
            "roi": result.roi,
            "win_rate": result.win_rate,
            "timestamp": now_utc()
        }
        write_to_disk(record)
        verified = read_from_disk(gen)
        assert verified["config"] == record["config"], "PERSISTENCE VERIFY FAILED"
        assert verified["adj_score"] == record["adj_score"], "PERSISTENCE VERIFY FAILED"
```

**One-time test before Gen 5801:**
Write synthetic record: gen=0, config=baseline, adj=1.6196.
Read it back. Assert all fields match. Log "PERSISTENCE_TEST_PASS" or halt.

**Immediate action:** On the next occurrence of adj=1.5117/bets=14707,
log and persist the full config. This signal has been seen 15+ times and
its config is still unknown. This is unacceptable.

---

### GATE 4: Deploy Live Slot (Cannot Wait Longer)

Deploy the confirmed baseline config to slot `mist` immediately.

```yaml
# mist deployment — v29.0 baseline
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
max_position_pct: 0.1
exclude_keywords: []
```

Target: 50 live resolved bets before Gen 5900.
Report: live sharpe, live ROI, and comparison to simulation sharpe=0.2458.
This is not optional. Simulation-only research is invalid after 5,800 gens.

---

## CONFIRMED SIGNALS

### Signal 1 — BASELINE (Confirmed ×20+)
```yaml
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
exclude_keywords: []
```
adj=1.6196, sharpe=0.2458, bets=14510.
Hard ceiling for marginal perturbation within this parameter space.

### Signal 2 — Recurring (Confirmed ×15+, Config Still Unknown — CRITICAL)
adj=1.5117, sharpe=0.229, bets=14707.
**Config must be captured on next occurrence via Gate 3 persistence.**
Hypothesis: world_events, price_range upper=0.85, everything else baseline.
Hash this hypothesis config and run it as Gen 5801 slot 1.

### Signal 3 — Gen 5787 (New, Partially Characterized)
adj=1.4563, sharpe=0.2337, bets=10154.
Sharpe close to baseline but only 10154 bets. Tighter filter than baseline.
Hypothesis: min_edge_pts=0.065 or min_liquidity_usd=75 or price_range tighter.
Run tighter-filter grid in Gens 5831–5850.

### Signal 4 — Gen 5786/5782 Pattern (Volume-Gain/Sharpe-Loss)
adj≈1.24, sharpe≈0.19, bets≈15100.
Loosened filters gain volume but lose sharpe faster than log(volume) compensates.
This is a confirmed dead end for adj improvement via volume alone.
Do not explore further unless a new formula weighting is proposed.

### Signal 5 — Gen 5594 (High Volume, Config Unknown)
adj=1.0111, sharpe=0.1515, bets=15797. Bets significantly exceed baseline.
Recovery still pending. Include in Grid C if deterministic grid executes.

### Known Lost (Do Not Re-investigate)
- Gen 5387: adj=1.5621, sharpe=0.2408, bets=13120
- Gen 5394: adj=1.4479, sharpe=0.2334, bets=9881
- Gen 4592: adj=1.213, sharpe=0.2079, bets=6814
- Gen 5584: adj=1.5883, sharpe=0.2409, bets=14579
  (Added v29.0 — unrecovered after 200 gens, mark lost)

---

## GENERATION PLAN: Gens 5801–5900

**Gates 1–3 must be confirmed PASS before any gen runs.**
**Gate 4 (live deployment) must be initiated before Gen 5850.**

Generation slots execute in strict order. LLM is suspended for Gens 5801–5870.
Gens 5871–5900 return to LLM with deduplication active.

---

### GRID A: Signal 2 Config Recovery (Gens 5801–5810, 10 slots)
**Goal:** Identify the config behind adj=1.5117/bets=14707 once and for all.

```
Gen 5801: world_events, edge=0.055, liq=50, price=[0.07,0.85], days=14
Gen 5802: world_events, edge=0.055, liq=40, price=[0.07,0.80], days=14
Gen 5803: world_events, edge=0.055, liq=50, price=[0.07,0.82], days=14
Gen 5804: world_events, edge=0.055, liq=45, price=[0.07,0.80], days=14
Gen 5805: world_events, edge=0.055, liq=50, price=[0.07,0.84], days=14
Gen 5806: world_events, edge=0.055, liq=50, price=[0.07,0.83], days=14
Gen 5807