```markdown
# FREYA Research Program — v50.0

## Status at Gen 10000
- **Current best (this run):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Historical best (all runs):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Improvements this run (v49.0, 200 gens):** 0
- **Improvements last 400 gens:** 2 (Gen 9607, Gen 9616 only)
- **Fixed-point collapse:** TERMINAL — fourteenth confirmed collapse
  (200 consecutive non-improvements, dominant attractors:
   adj≈2.2936/bets≈17728 [seen 4× in last 20],
   adj≈2.2867/bets≈17242 [seen 3× in last 20],
   adj≈2.287/bets≈17534 [background])
- **Degenerate outputs last 20 gens:** 2 (Gen 9983 bets=6, Gen 9997 bets=18)
- **Degenerate rate last 20 gens:** 10% (2/20) — ELEVATED, TRENDING WORSE
- **Gate 1 NOT IMPLEMENTED** — sixth consecutive program without implementation
- **Gate 2 NOT IMPLEMENTED** — sixth consecutive program without implementation
- **Gate 3 NOT IMPLEMENTED** — sixth consecutive program without implementation
- **Live performance:** 0/24 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
  (six consecutive programs without root cause diagnosis)
- **Config discrepancy CONFIRMED AND UNRESOLVED:** Live YAML block in this document
  shows min_edge_pts=0.028. Simulation best uses min_edge_pts=0.033. Hotfix A0
  has been required since v48.0 and has not been executed. Every live trade since
  v48.0 has used an incorrect config.
- **Current best config signature:** price_range=[0.11, 0.55], min_edge_pts=0.033,
  max_days=10 (unverified), category=world_events

---

## TERMINAL CONDITION STATEMENT (v50.0)

**THE SIMULATION LOOP IS PERMANENTLY SUSPENDED AS OF GEN 10000.**

This is not a soft stop. Gen 10001 must not run until ALL pre-flight items below
are completed with timestamps and findings documented in this file.

Reasons for permanent suspension:
1. Zero improvements in 200 generations. Projected gain for next 100 generations: 0.
2. 0/24 live wins. p < 3×10⁻²¹ under simulation assumptions. This is a code bug.
3. Known config bug (min_edge_pts mismatch) unresolved since v48.0.
4. Gates 1-3 unimplemented across six consecutive programs.
5. Base rate assumption (world_events=12% YES) empirically unvalidated against
   live Polymarket. This is the most likely root cause of live failure.
6. Further simulation output has zero expected value until live root cause is found.

**Running Gen 10001 without completing pre-flight is a direct financial loss.**
**Each live trade with the wrong config is a direct financial loss.**
**These are not warnings. They are statements of observed fact.**

---

## LOCKED BEST CONFIG

```yaml
name: pm_research_best
category: world_events
price_range: [0.11, 0.55]        # VERIFIED (Gen 9616 simulation)
min_edge_pts: 0.033              # VERIFIED (simulation) — LIVE BUG: live shows 0.028
                                 # A0 hotfix has NOT been executed as of v50.0
max_days_to_resolve: 10          # UNVERIFIED — ambiguity unresolved since v47.0
min_liquidity_usd: 100           # ASSUMED — not confirmed from live logs
max_position_pct: 0.1            # ASSUMED
include_keywords: []
exclude_keywords: []
```

**Live config as of v50.0 (WRONG — do not trade with this):**
```yaml
min_edge_pts: 0.028              # INCORRECT — must be updated to 0.033
```

---

## PRE-FLIGHT CHECKLIST FOR GEN 10001
*Every item is BLOCKING. No simulation until all items are checked and timestamped.*
*This is the sixth version of this checklist. Items not completed cost real money.*

---

### A. IMMEDIATE BUG FIX (do first, before any analysis)
**Estimated time: 10 minutes. Must be done before any other step.**

- [ ] **A0 — LIVE CONFIG HOTFIX:**
      The live YAML shows min_edge_pts=0.028.
      The simulation best is min_edge_pts=0.033. Divergence confirmed.
      
      Steps:
      1. SSH to mist → update min_edge_pts to 0.033 → restart → print running config
      2. SSH to kara → update min_edge_pts to 0.033 → restart → print running config
      3. SSH to thrud → update min_edge_pts to 0.033 → restart → print running config
      4. Verify each slot shows min_edge_pts: 0.033 in running config
      
      mist updated: [ ]  Timestamp: ___________
      kara updated: [ ]  Timestamp: ___________
      thrud updated: [ ]  Timestamp: ___________
      
      *If this step cannot be completed, HALT all live trading immediately.*
      *Do not proceed to A1 until A0 is complete and timestamped.*

---

### B. CONFIG RECONCILIATION (BLOCKING)
**Estimated time: 30 minutes.**

- [ ] **B1 — Retrieve Gen 9616 exact config from simulation log:**
      Do not infer. Read from raw log output.
      - price_range: expected [0.11, 0.55] — actual: ___________
      - min_edge_pts: expected 0.033 — actual: ___________
      - max_days_to_resolve: expected 10 — actual: ___________
      - category: expected world_events — actual: ___________
      - Any other fields present: ___________
      All match: [ ]  Discrepancies found: ___________

- [ ] **B2 — Reproduce Gen 9616 in simulator:**
      Run Gen 9616 exact config (from B1) in simulator.
      Must reproduce: adj≈2.2936 (±0.001), sharpe≈0.3379 (±0.001), bets≈17728 (±20)
      Result: adj=___  sharpe=___  bets=___
      Reproduction successful: [ ]  If not: STOP, investigate simulator state.

- [ ] **B3 — Resolve max_days_to_resolve ambiguity (carried since v47.0):**
      Run Gen 9616 config (all other fields fixed) with:
      - max_days=10 → adj=___  sharpe=___  bets=___
      - max_days=14 → adj=___  sharpe=___  bets=___
      Correct value = whichever reproduces adj≈2.2936.
      Resolved value: ___ (10 / 14)
      Document permanently. This ambiguity must not appear in v51.0.

- [ ] **B4 — Update LOCKED BEST CONFIG:**
      Update all fields above with verified values from B1-B3.
      Mark every field VERIFIED. No field may remain UNVERIFIED after this step.
      Completed: [ ]  Timestamp: ___________

---

### C. GATE IMPLEMENTATION (BLOCKING — sixth request)
**Estimated time: 2-4 hours for a competent engineer.**
**These gates have been required since v45.0. Each skipped generation costs capacity.**

- [ ] **C1 — Gate 1: SEEN_CONFIGS deduplication**

      Hash key (all fields must be included):
      ```python
      import hashlib, json
      def config_hash(cfg):
          key = (
              cfg['category'],
              cfg['price_range'][0],
              cfg['price_range'][1],
              cfg['min_edge_pts'],
              cfg['max_days_to_resolve'],
              cfg['min_liquidity_usd'],
              tuple(sorted(cfg.get('include_keywords', []))),
              tuple(sorted(cfg.get('exclude_keywords', [])))
          )
          return hashlib.sha256(json.dumps(key).encode()).hexdigest()
      
      SEEN_CONFIGS = set()
      
      def try_simulate(cfg):
          h = config_hash(cfg)
          if h in SEEN_CONFIGS:
              log(f"CYCLE AVOIDED [{h[:8]}] — requesting new proposal")
              return None  # do not simulate, do not count as generation
          SEEN_CONFIGS.add(h)
          return simulate(cfg)
      ```
      
      Pre-populate SEEN_CONFIGS with ALL attractor signatures from
      ATTRACTOR INVENTORY below before running Gen 10001.
      
      Acceptance test: Feed all attractor configs → all rejected, zero simulations run.
      Test result: [ ] PASS / [ ] FAIL
      Timestamp: ___________

- [ ] **C2 — Gate 2: DEGENERATE FILTER**

      ```python
      MIN_BETS_THRESHOLD = 100
      
      def post_sim_check(result):
          if result['bets'] < MIN_BETS_THRESHOLD:
              log(f"DEGENERATE REJECTED [bets={result['bets']}]")
              return False  # do not update best, do not count as generation
          return True
      ```
      
      Threshold: 100 bets (degenerate outputs observed at 6, 18, 197, 988).
      This threshold may need to be raised further — review after 100 generations.
      
      Acceptance test: Feed config known to produce bets < 100 → rejected.
      Test result: [ ] PASS / [ ] FAIL
      Timestamp: ___________

- [ ] **C3 — Gate 3: LIVE CONFIG SYNC VERIFICATION**

      After A0 hotfix:
      1. Print running YAML from each slot (mist, kara, thrud)
      2. Diff each against LOCKED BEST CONFIG (post-B4 verified version)
      3. Diff must be empty on all three slots
      
      mist diff empty: [ ]  mist diff output (if any): ___________
      kara diff empty: [ ]  kara diff output (if any): ___________
      thrud diff empty: [ ]  thrud diff output (if any): ___________
      
      If any diff is non-empty: fix, restart, re-verify before proceeding.

- [ ] **C4 — LLM PROMPT UPDATE**

      Replace current proposal prompt with the following. Do not modify without
      documenting the change in this file.
      
      ```
      You are proposing ONE change to a prediction market strategy config.
      
      Current best config:
      [INSERT LOCKED BEST CONFIG HERE — use post-B4 verified version]
      
      Current best adj_score: 2.2936
      
      FORBIDDEN — do not reproduce these configs (known attractors):
      [INSERT ALL ATTRACTOR INVENTORY ENTRIES HERE]
      Do not propose any config within ±0.005 of any attractor's numeric parameters.
      If your proposal matches a forbidden config, it will be rejected without
      simulation. Propose something genuinely different.
      
      PRIORITY SEARCH REGIONS (in order of priority):
        1. price_range lower bound in [0.05, 0.10] (current: 0.11 — explore below)
        2. price_range upper bound in [0.45, 0.70] (current: 0.55 — explore above)
        3. min_edge_pts in [0.015, 0.032] (current: 0.033 — explore below)
        4. Multi-category combinations: world_events + economics
           (base rates 12% and 26% — combined filter may improve n_bets without
           sacrificing sharpe)
        5. Asymmetric th