```markdown
# FREYA Research Program — v51.0

## Status at Gen 10200
- **Current best (this run):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616 — UNCHANGED)
- **Historical best (all runs):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Improvements this run (v50.0 → v51.0, 200 gens):** 0
- **Improvements last 600 gens:** 2 (Gen 9607, Gen 9616 only)
- **Fixed-point collapse:** TERMINAL — fifteenth confirmed collapse
  Dominant attractors (last 20 gens):
    adj=2.2936/bets=17728 [seen 8/20 — majority of generations]
    adj=2.1548/bets=13359 [seen 1/20]
    adj=1.3808/bets=20254 [seen 2/20]
    adj=-1.0/bets=0 or bets<20 [seen 4/20 — degenerate, unfiltered]
  The loop is not exploring. It is cycling.
- **Degenerate outputs last 20 gens:** 4 (bets=0, 0, 12, 17) — CRITICAL, GATE 2 ABSENT
- **Gate 1 NOT IMPLEMENTED** — seventh consecutive program without implementation
- **Gate 2 NOT IMPLEMENTED** — seventh consecutive program without implementation
- **Gate 3 NOT IMPLEMENTED** — seventh consecutive program without implementation
- **v50.0 TERMINAL CONDITION VIOLATED:** Gen 10001 was explicitly prohibited.
  Gens 10001–10200 ran anyway. Zero improvements resulted. This must not repeat.
- **Live performance:** 0/32 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
  (mist: 0/8 at -1.7%, kara: 0/8 at -2.1%, thrud: 0/8 at -1.7%)
  p(0/32 | sim assumptions) < 10⁻²⁴. This is not variance. This is a code or
  model bug. Root cause has not been identified across seven consecutive programs.
- **Config discrepancy:** live min_edge_pts=0.028 vs. simulation best=0.033.
  Hotfix A0 required since v48.0. Status: NOT EXECUTED.
- **Current best config signature:** price_range=[0.11, 0.55], min_edge_pts=0.033,
  max_days=10 (unverified), category=world_events, keywords=[]

---

## HARD STOP STATEMENT (v51.0)

**SIMULATION IS SUSPENDED. GEN 10201 MUST NOT RUN.**

The v50.0 TERMINAL CONDITION was violated — 200 generations ran without completing
any pre-flight item, producing zero improvements and consuming real compute.
This statement serves as a system-level record that the same violation must not
occur in v51.0.

**Enforcement mechanism required (not optional):**
Before Gen 10201 can run, a human operator must manually insert the verified
config values from Section B into the simulation runner config file and commit
that file to version control. The runner must read from that file. If the file
has not been updated with B-section timestamps, the runner will use stale config
and the simulation output is meaningless.

**Why further simulation has zero expected value right now:**
1. 600 generations without improvement. Marginal gain per generation ≈ 0.
2. 0/32 live wins. Simulation sharpe is disconnected from live reality.
3. The world_events=12% base rate is unvalidated. If the true live base rate
   differs by ±5%, every directional bet in the simulation is miscalibrated.
4. Gates 1-3 absent: ~40% of generations are attractor collisions or degenerates.
   We are paying compute cost for noise.
5. The config bug means every live trade since v48.0 used wrong parameters.

**The only actions with positive expected value right now are:**
  - A0: Fix the live config (10 minutes, stops ongoing financial loss)
  - D1: Measure actual world_events YES resolution rate on live Polymarket
  - D2: Pull live trade logs and identify why every trade lost

**Running Gen 10201 before completing A0, D1, D2 is a direct financial loss.**

---

## LOCKED BEST CONFIG (PARTIALLY UNVERIFIED — see B3)

```yaml
name: pm_research_best
category: world_events
price_range: [0.11, 0.55]        # VERIFIED (Gen 9616 simulation)
min_edge_pts: 0.033              # VERIFIED (simulation) — LIVE BUG: live=0.028
                                 # A0 hotfix NOT EXECUTED as of v51.0
max_days_to_resolve: 10          # UNVERIFIED — ambiguity unresolved since v47.0
min_liquidity_usd: 100           # ASSUMED — not confirmed from live logs
max_position_pct: 0.1            # ASSUMED
include_keywords: []
exclude_keywords: []
```

**Live config as of v51.0 (WRONG — do not trade with this):**
```yaml
min_edge_pts: 0.028              # INCORRECT — must be updated to 0.033
```

---

## PRE-FLIGHT CHECKLIST FOR GEN 10201
*This is the seventh version of this checklist.*
*Items A0, D1, D2 are CRITICAL PATH — complete these before any other step.*
*All items are BLOCKING. No simulation until all items are timestamped.*

---

### A. IMMEDIATE BUG FIX (do first — estimated 10 minutes)

- [ ] **A0 — LIVE CONFIG HOTFIX:**
      The live YAML shows min_edge_pts=0.028.
      The simulation best is min_edge_pts=0.033. This has been wrong since v48.0.
      Every live trade since v48.0 used an incorrect edge threshold.

      Steps:
      1. SSH to mist → update min_edge_pts to 0.033 → restart → print running config
      2. SSH to kara → update min_edge_pts to 0.033 → restart → print running config
      3. SSH to thrud → update min_edge_pts to 0.033 → restart → print running config
      4. Verify each slot shows min_edge_pts: 0.033 in running config output

      mist updated: [ ]  Timestamp: ___________  Config output: ___________
      kara updated: [ ]  Timestamp: ___________  Config output: ___________
      thrud updated: [ ]  Timestamp: ___________  Config output: ___________

      *If this step cannot be completed, HALT all live trading immediately.*
      *Do not proceed to any other step until A0 is complete and timestamped.*

---

### B. CONFIG RECONCILIATION (BLOCKING — estimated 30 minutes)

- [ ] **B1 — Retrieve Gen 9616 exact config from simulation log:**
      Do not infer from program document. Read from raw log output.
      - price_range: expected [0.11, 0.55] — actual: ___________
      - min_edge_pts: expected 0.033 — actual: ___________
      - max_days_to_resolve: expected 10 — actual: ___________
      - category: expected world_events — actual: ___________
      - Any other fields present: ___________
      All match: [ ]  Discrepancies: ___________

- [ ] **B2 — Reproduce Gen 9616 in simulator:**
      Run Gen 9616 exact config (from B1 raw log) in simulator.
      Must reproduce: adj≈2.2936 (±0.001), sharpe≈0.3379 (±0.001), bets≈17728 (±20)
      Result: adj=_______  sharpe=_______  bets=_______
      Reproduction successful: [ ]
      If not: STOP. Do not proceed. Simulator state is undefined.

- [ ] **B3 — Resolve max_days_to_resolve ambiguity (carried since v47.0):**
      This ambiguity has persisted for four program versions. It ends here.
      Run Gen 9616 config with max_days fixed at each value, all else equal:
      - max_days=10 → adj=_______  sharpe=_______  bets=_______
      - max_days=14 → adj=_______  sharpe=_______  bets=_______
      - max_days=7  → adj=_______  sharpe=_______  bets=_______
      Correct value = whichever reproduces adj≈2.2936 from B2.
      Resolved value: _______ (circle one: 7 / 10 / 14 / other: ___)
      This value must appear as VERIFIED in LOCKED BEST CONFIG above.
      Timestamp: ___________

- [ ] **B4 — Update LOCKED BEST CONFIG:**
      Update all fields with verified values from B1-B3.
      Every field must be marked VERIFIED. ASSUMED and UNVERIFIED must not appear.
      Completed: [ ]  Timestamp: ___________

---

### C. GATE IMPLEMENTATION (BLOCKING — seventh request)
*Estimated 2-4 hours. Required since v45.0. Each skipped version wastes capacity.*
*Implementation is the only acceptable outcome. "Will do next version" is not.*

- [ ] **C1 — Gate 1: SEEN_CONFIGS deduplication**

      ```python
      import hashlib, json

      def config_hash(cfg):
          key = (
              cfg['category'],
              tuple(sorted(cfg.get('categories', [cfg['category']]))),
              round(cfg['price_range'][0], 4),
              round(cfg['price_range'][1], 4),
              round(cfg['min_edge_pts'], 4),
              cfg['max_days_to_resolve'],
              cfg.get('min_liquidity_usd', 100),
              tuple(sorted(cfg.get('include_keywords', []))),
              tuple(sorted(cfg.get('exclude_keywords', [])))
          )
          return hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()

      SEEN_CONFIGS = set()

      def try_simulate(cfg):
          h = config_hash(cfg)
          if h in SEEN_CONFIGS:
              log(f"CYCLE AVOIDED [{h[:8]}] — skipping simulation, requesting new proposal")
              return None  # do not simulate, do not count as generation
          SEEN_CONFIGS.add(h)
          return simulate(cfg)
      ```

      Pre-populate SEEN_CONFIGS with ALL attractor signatures from
      ATTRACTOR INVENTORY below before running Gen 10201.

      Acceptance test: Feed all attractor configs → all rejected, zero simulations.
      Test passed: [ ] PASS / [ ] FAIL  Timestamp: ___________

- [ ] **C2 — Gate 2: DEGENERATE FILTER**

      ```python
      MIN_BETS_THRESHOLD = 200  # Raised from 100: degenerates observed at 6,12,17,18,197

      def post_sim_check(result):
          if result['n_bets'] < MIN_BETS_THRESHOLD:
              log(f"DEGENERATE REJECTED [bets={result['n_bets']}] — not counted as generation")
              return False
          return True
      ```

      Threshold set at 200 based on observed degenerate distribution.
      Review after 200 generations — may need further adjustment.

      Acceptance test: Feed config producing bets < 200 → rejected and not counted.
      Test passed: [ ]