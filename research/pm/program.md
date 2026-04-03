```markdown
# FREYA Research Program — Prediction Markets (v28.0)

## Status at Gen 5600
- **2,600 generations without improvement** (Gens 3001–5600).
  Confirmed ceiling: adj=1.6196, sharpe=0.2458, bets=14510.
- **Deterministic grid (v27.0, Gens 5401–5500) was NEVER EXECUTED.**
  LLM loop continued running. Gen 5592 (bets=10) confirms guard still broken.
  Gen 5584 (adj=1.5883) and Gen 5594 (bets=15797) are unrecovered signals.
- **All three v27.0 blockers remain unimplemented in code.**
  This is the fifth version cycle of documentation without implementation.
  v28.0 treats all three as PRE-CONDITIONS, not blockers. See below.
- **Live slots (mist, kara, thrud): STILL DISABLED. Zero live bets ever placed.**
- **New recurring signals identified from Gens 5401–5600:**
  - adj=1.5117, sharpe=0.229, bets=14707 (seen 8+ times — config unknown)
  - adj=0.4785, sharpe=0.0713, bets=16436 (seen 4+ times — config unknown,
    likely multi-category or heavily loosened price_range, poor sharpe)
  - adj=1.5883, sharpe=0.2409, bets=14579 (Gen 5584 — config unknown)
  - adj=1.0111, sharpe=0.1515, bets=15797 (Gen 5594 — config unknown,
    HIGH PRIORITY: bets exceed baseline significantly)

---

## PRE-CONDITIONS FOR GEN 5601
### (Loop MUST NOT advance until all three pass a live test)

These are no longer called "blockers" because that framing has failed five times.
They are PRE-CONDITIONS. If they are not met, the loop is frozen, not advisory.

---

### PRE-CONDITION 1: Guard System (Runtime Implementation Required)

Translate the following to actual executable code. Run the eight test cases.
Log PASS/FAIL for each. Do not proceed until all eight pass.

```python
MIN_BETS_FLOOR = 501  # 500 is NOT sufficient — strict greater-than

def run_generation(config, gen_number):
    # STAGE 1: Pre-simulation estimate
    estimated = estimate_bets(config)
    if estimated <= 500:
        log_hard_reject(gen_number, config, "PRE_SIM_REJECT", estimated)
        return None  # no simulation, no count

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
    persist_result(gen_number, config, result)  # always persist before eval
    evaluate_and_update(result)
    return result
```

**Required test cases — all eight must log PASS:**
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

### PRE-CONDITION 2: LLM Loop Hard Suspension (Runtime Implementation Required)

```python
SUSPENSION_ACTIVE = True  # Set False only after Gen 5700 grid completes
SUSPENSION_START = 5601
SUSPENSION_END = 5700

def get_next_config(gen_number):
    if SUSPENSION_ACTIVE and SUSPENSION_START <= gen_number <= SUSPENSION_END:
        # Pull from deterministic grid iterator, not LLM
        config = deterministic_grid.next()
        if config is None:
            # Grid exhausted — log NOP, do not call LLM
            log_nop(gen_number, "GRID_EXHAUSTED")
            return None
        return config
    return llm_propose()
```

The deterministic grid iterator is defined in the Generation Plan below.
It is a finite ordered list. Exhaust it before returning control to LLM.

---

### PRE-CONDITION 3: Config Persistence (Runtime Implementation Required)

```python
def persist_result(gen, config, result):
    if result.adj > 1.0 or result.bets > 5000:
        record = {
            "gen": gen,
            "config_hash": hash_config(config),
            "config": config,          # full config object
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

**One-time test before Gen 5601:**
Write a synthetic record with gen=0, config=baseline, adj=1.6196.
Read it back. Assert all fields match. Log "PERSISTENCE_TEST_PASS" or halt.

**Retroactive recovery (one attempt only):**
- Try RNG seed replay for: Gens 3788, 5387, 5394, 5397, 5398, 5584, 5594.
- For each: if recovered → log to known-signals registry.
- If unrecoverable → log to known-lost registry. Do not attempt again.

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
adj=1.6196, sharpe=0.2458, bets=14510. Hard ceiling. Not improvable by
marginal perturbation. Only systematic grid exploration will exceed this.

### Signal 2 — Recurring Unknown (High Confidence)
adj=1.5117, sharpe=0.229, bets=14707. Seen 8+ times in Gens 5401–5600.
Config is almost certainly world_events with price_range upper bound loosened
to ~0.85 or min_liquidity reduced to ~40. RECOVERY PRIORITY via Grid A.

### Signal 3 — Gen 5584 (Config Unknown)
adj=1.5883, sharpe=0.2409, bets=14579. Near-baseline sharpe, comparable bets.
Likely a minor price_range or liquidity tweak. Recover via Grid A.

### Signal 4 — Gen 5594 (Config Unknown — HIGH INTEREST)
adj=1.0111, sharpe=0.1515, bets=15797. Bets significantly exceed baseline.
Lower sharpe but volume is a new high. May indicate a category or filter
combination that finds more markets. Recover via Grid C.

### Signal 5 — Unknown High-Volume Low-Sharpe
adj=0.4785, sharpe=0.0713, bets=16436. Seen 4+ times. Very low sharpe.
Likely a multi-category or heavily loosened config. Low priority but the
bets count is useful — it shows more volume is achievable. Understand config
to avoid accidentally optimizing toward it.

### Signal 6 — Gen 3788 (Config Unknown — RECOVERY PRIORITY)
adj=1.4766, bets=14771. Predates the current plateau. Likely world_events
with minor loosening. Recover via Grid B.

### Known Lost (Unrecoverable — Do Not Re-investigate)
- Gen 5387: adj=1.5621, sharpe=0.2408, bets=13120
- Gen 5394: adj=1.4479, sharpe=0.2334, bets=9881
- Gen 4592: adj=1.213, sharpe=0.2079, bets=6814
  (Mark permanently lost after single recovery attempt fails)

---

## GENERATION PLAN: Gens 5601–5700 (Deterministic Grid Only)

All 100 slots are fully specified. Execute in order. LLM is disabled.
Every result with adj > 1.0 OR bets > 5000 must be persisted (Pre-condition 3).

---

### GRID A: Signal 2 + Signal 3 Recovery (Gens 5601–5630, 30 slots)
**Goal:** Identify the config behind the recurring adj=1.5117/bets=14707 result
and the Gen 5584 adj=1.5883 result.

**Sub-grid A1: price_range upper bound expansion, baseline everything else**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
max_days_to_resolve: 14
price_range lower: 0.07 (fixed)
price_range upper: [0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90]
```
10 gens → slots 5601–5610
**Stop early trigger:** First result matching adj≈1.5117±0.002 AND bets≈14707±50
confirms the config. Log "SIGNAL_2_RECOVERED". Continue remaining slots.

**Sub-grid A2: price_range lower bound relaxation**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
max_days_to_resolve: 14
price_range lower: [0.06, 0.05, 0.04, 0.03]
price_range upper: 0.80 (fixed)
```
4 gens → slots 5611–5614

**Sub-grid A3: combined bounds**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
max_days_to_resolve: 14
price_range: [[0.06, 0.85], [0.06, 0.90], [0.05, 0.85], [0.05, 0.90],
              [0.07, 0.85], [0.07, 0.90], [0.06, 0.82], [0.07, 0.82]]
```
8 gens → slots 5615–5622

**Sub-grid A4: min_liquidity reduction**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: [40, 35, 30, 25, 20]
max_days_to_resolve: 14
price_range: [0.07, 0.80]
```
5 gens → slots 5623–5627

**Sub-grid A5: combined liquidity + price_range**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: [25, 40]
max_days_to_resolve: 14
price_range: [[0.07, 0.85], [0.07,