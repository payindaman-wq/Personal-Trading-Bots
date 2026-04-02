```markdown
# FREYA Research Program — Prediction Markets (v27.0)

## Status at Gen 5400
- **2,400 generations without improvement** (Gens 3001–5400, approximately).
  Confirmed ceiling: adj=1.6196, sharpe=0.2458, bets=14510.
- **Guard system STILL BROKEN.** Gens 5381/5389/5392/5396/5399 (bets ≤ 6)
  passed through. Gen 5400 (bets=18700, adj=-0.2387) indicates a high-volume
  negative-sharpe config was run unguarded. This is the 4th documented cycle
  of the same failure. It will not be fixed by documentation alone.
- **LLM loop NOT suspended despite v25.0 and v26.0 mandates.**
  Deterministic grid was not executed. Forced signal injections were not run.
  The loop continued generating baseline reproductions and degenerate configs.
- **Config persistence bug UNRESOLVED.** Gens 5397/5398 have adj > 1.3 and
  bets > 14500 — configs are unknown. Gen 5394 (adj=1.4479) config unknown.
  These are potentially significant signals that cannot be acted upon.
- **Live slots: ALL STILL DISABLED.** mist approved in v25.0, re-approved v26.0,
  still not deployed. Zero live bets placed. This is a critical program failure.
- **Gen 5400 blacklisted:** adj=-0.2387, sharpe=-0.0349, bets=18700.
  Config unknown but must be excluded from future runs. Likely cause: removal
  of price_range upper cap or addition of positive-base-rate category. Investigate.

## CONFIRMED SIGNALS (Do Not Lose These)

### Signal 1 — BASELINE (Confirmed ×15+)
```yaml
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
price_range: [0.07, 0.80]
max_days_to_resolve: 14
exclude_keywords: []
```
adj=1.6196, sharpe=0.2458, bets=14510. Local maximum. Ceiling confirmed.

### Signal 1b — Gen 3788 (Config Unknown — RECOVERY PRIORITY)
adj=1.4766, bets=14771. Bets EXCEED baseline. Category likely world_events.
Hypothesis: looser price_range upper bound OR lower min_liquidity.

### Signal 2 — Gens 5397/5398 (Configs Unknown — RECOVERY PRIORITY)
Gen 5397: adj=1.3862, sharpe=0.2095, bets=14917 (bets exceed baseline)
Gen 5398: adj=1.5117, sharpe=0.229, bets=14707 (bets exceed baseline)
Both exceed baseline bet count. Strongly suggests loosened price_range or
reduced min_liquidity on world_events. Must be recovered and reproduced.

### Signal 3 — Gen 5387 (Config Unknown)
adj=1.5621, sharpe=0.2408, bets=13120. Near-baseline. Lower volume.

### Signal 4 — Gen 5394 (Config Unknown)
adj=1.4479, sharpe=0.2334, bets=9881. Mid-volume. Worth recovering.

### Signal 5 — Gen 4592 (Config Unknown)
adj=1.213, sharpe=0.2079, bets=6814. Lower priority.

## HARD BLOCKERS — Gen 5401 MUST NOT RUN UNTIL ALL THREE RESOLVED

### BLOCKER A: Guard System Fix (MANDATORY — 4th notice)
This has been documented in v24.0, v25.0, v26.0 without implementation.
It will not be documented again. It must be implemented in code.

**Implementation (pseudocode — translate to actual runtime):**
```python
MIN_BETS_FLOOR = 501  # Strict: 500 is NOT sufficient

def run_generation(config, gen_number):
    # PRE-SIMULATION CHECK
    estimated = estimate_bets(config)  # fast approximation
    if estimated < MIN_BETS_FLOOR:
        log_hard_reject(gen_number, config, "PRE_SIM", estimated)
        return  # do NOT simulate, do NOT count as valid gen

    # RUN SIMULATION
    result = simulate(config)

    # POST-SIMULATION CHECK
    if result.bets < MIN_BETS_FLOOR:
        log_hard_reject(gen_number, config, "POST_SIM", result.bets)
        return  # do NOT update best, do NOT count as valid gen

    # NEGATIVE SHARPE HIGH-VOLUME GUARD
    if result.sharpe < -0.01 and result.bets > 10000:
        log_hard_reject(gen_number, config, "NEG_SHARPE_HIGH_VOL", result)
        return  # blacklist this config

    # Proceed with normal scoring
    evaluate_and_update(result)
```

**Required test cases — ALL must pass before Gen 5401:**
- estimated_bets=0 → HardReject PRE_SIM ✓
- estimated_bets=499 → HardReject PRE_SIM ✓
- estimated_bets=500 → HardReject PRE_SIM ✓
- estimated_bets=501 → passes to simulation ✓
- sim returns bets=144 → HardReject POST_SIM ✓
- sim returns bets=500 → HardReject POST_SIM ✓
- sim returns bets=501 → accepted ✓
- sim returns bets=18700, sharpe=-0.035 → HardReject NEG_SHARPE_HIGH_VOL ✓

### BLOCKER B: LLM Loop Hard Suspension
The LLM proposal function must be structurally disabled for Gens 5401–5500.
Not advisory. Not documented. Disabled in code.

```python
SUSPENSION_START = 5401
SUSPENSION_END = 5500

def get_next_config(gen_number):
    if SUSPENSION_START <= gen_number <= SUSPENSION_END:
        raise HardError(f"SUSPENSION VIOLATION at gen {gen_number}. "
                        f"LLM loop is disabled. Use deterministic grid iterator.")
    return llm_propose()
```

The deterministic grid iterator (see Generation Plan below) replaces LLM
for all gens in this range. If grid is exhausted before gen 5500, pad with
NOP entries rather than calling LLM.

### BLOCKER C: Config Persistence (MANDATORY — 3rd notice)
Every simulation result with adj > 1.0 OR bets > 5000 must be written to disk.

```python
def persist_result(gen, config, result):
    if result.adj > 1.0 or result.bets > 5000:
        record = {
            "gen": gen,
            "config_hash": hash_config(config),
            "config": config,  # full config, not just hash
            "bets": result.bets,
            "sharpe": result.sharpe,
            "adj_score": result.adj,
            "roi": result.roi,
            "win_rate": result.win_rate,
            "timestamp": now_utc()
        }
        write_to_disk(record)  # not memory-only
        verify_readback(record)  # read back and assert match
```

**Retroactive recovery attempt (one-time):**
- Gens 4796/4797/4799: attempt RNG seed replay if seeds were logged.
- Gens 5387/5394/5397/5398: attempt RNG seed replay.
- If unrecoverable: document as permanently lost, add to known-lost registry.

**Do not proceed to Gen 5401 until a test write + readback passes.**

## GENERATION PLAN: Gens 5401–5500 (Deterministic Grid Only)

All 100 generations are fully specified below. Execute in order.
No LLM proposals. No deviations. Log all results via Blocker C.

---

### GRID A: Gen 5397/5398 Recovery (Gens 5401–5430, 30 gen budget)
**HIGHEST PRIORITY.** Gens 5397 and 5398 had bets > 14700 with adj > 1.38.
This is the most likely path to breaking the adj=1.6196 ceiling.
Hypothesis: world_events with loosened price_range upper bound or lower liquidity.

**Sub-grid A1: price_range upper bound expansion (world_events)**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
max_days_to_resolve: 14
price_range upper bound: [0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.90]
price_range lower bound: 0.07 (fixed)
```
8 configs × 1 = 8 gens (5401–5408)

**Sub-grid A2: price_range lower bound relaxation (world_events)**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
max_days_to_resolve: 14
price_range lower bound: [0.06, 0.05, 0.04]
price_range upper bound: 0.80 (fixed)
```
3 configs × 1 = 3 gens (5409–5411)

**Sub-grid A3: lower bound + upper bound expansion combinations**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: 50
max_days_to_resolve: 14
price_range: [[0.06, 0.85], [0.06, 0.90], [0.05, 0.85], [0.05, 0.90],
              [0.07, 0.85], [0.07, 0.90]]
```
6 configs × 1 = 6 gens (5412–5417)

**Sub-grid A4: min_liquidity reduction (world_events, baseline price_range)**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: [40, 35, 30, 25, 20, 15, 10]
max_days_to_resolve: 14
price_range: [0.07, 0.80]
```
7 configs × 1 = 7 gens (5418–5424)

**Sub-grid A5: combined — reduced liquidity + expanded price_range**
```
category: world_events
min_edge_pts: 0.055
min_liquidity_usd: [25, 10]
max_days_to_resolve: 14
price_range: [[0.07, 0.85], [0.07, 0.90], [0.06, 0.80]]
```
2 × 3 = 6 configs × 1 = 6 gens (5425–5430)

**Recovery trigger for Grid A:**
If any result has adj > 1.40 AND bets > 14500:
- Run identical config immediately (next gen slot).
- If reproduced: log "SIGNAL A CONFIRMED", enable live slot kara on this config.
- Continue grid (don't abandon remaining slots).

---

### GRID B: Gen 3788 Recovery (Gens 5431–5445, 15 gen budget)
Gen 3788: adj=1.4766, bets=14771. Config unknown. Looser than baseline.

```
category: world_events
min_edge_pts: [0.05, 0.055]
price_range: [[0.07, 0.85], [0.06, 0.80], [0.07, 0