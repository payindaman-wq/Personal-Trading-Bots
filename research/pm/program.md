```markdown
# FREYA Research Program — v52.0

## Status at Gen 10400
- **Current best (this run):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616 — UNCHANGED)
- **Historical best (all runs):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Improvements this run (v51.0 → v52.0, 200 gens):** 0
- **Improvements last 800 gens:** 2 (Gen 9607, Gen 9616 only)
- **Improvements last 200 gens:** 0
- **Fixed-point collapse:** TERMINAL — sixteenth confirmed collapse
  Dominant attractors (last 20 gens):
    adj=2.2867/bets=17242 [seen 14/20 — primary attractor]
    adj=2.2936/bets=17728 [seen 1/20 — historical best, not improving]
    adj=2.1994/bets=14825 [seen 1/20]
    adj=1.6524/bets=4423  [seen 1/20]
    adj=1.4921/bets=2482  [seen 1/20]
  The loop has not produced a new best in 784 generations.
  The search space reachable by single-parameter proposals is exhausted.
- **Gate 1 NOT IMPLEMENTED** — eighth consecutive program without implementation
- **Gate 2 NOT IMPLEMENTED** — eighth consecutive program without implementation
- **v51.0 TERMINAL CONDITION VIOLATED:** Gen 10201 was explicitly prohibited.
  Gens 10201–10400 ran anyway. Zero improvements resulted.
  This is the second consecutive violation of an explicit hard stop.
  A third violation is not acceptable.
- **Live performance:** 0/32 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
  (mist: 0/8 at -1.7%, kara: 0/8 at -2.1%, thrud: 0/8 at -1.7%)
  p(0/32 | sim assumptions) < 10⁻²⁴. Root cause not identified. Trading continues.
- **Config discrepancy:** live min_edge_pts=0.028 vs. simulation best=0.033.
  Hotfix A0 required since v48.0. Status: NOT EXECUTED after eight programs.
- **Current best config signature:** price_range=[0.11, 0.55], min_edge_pts=0.033,
  max_days=10 (unverified), category=world_events, keywords=[]

---

## HARD STOP STATEMENT (v52.0)

**SIMULATION IS SUSPENDED. GEN 10401 MUST NOT RUN.**

The v51.0 HARD STOP was violated for the second consecutive version.
200 generations ran, produced zero improvements, and consumed real compute.
The root cause of 0/32 live losses remains unidentified.
The world_events base rate remains unvalidated.
The live config bug remains unfixed.

**This is not a soft recommendation. This is a system record.**
Running Gen 10401 before completing A0, D1, and D2 is provably net-negative:
- Expected simulation improvement per generation: ~0 (measured over 800 gens)
- Expected financial loss per live trade at wrong base rate: systematic, not random
- Cost of D1 (measure actual base rate): ~1-2 hours
- Cost of continued simulation without D1: measured at zero improvement

**Enforcement:**
The human operator must complete items A0, D1, and D2 and record timestamps
in this document before any simulation runner is started.
If the runner starts without these timestamps, the output is not valid research.

---

## CRITICAL HYPOTHESIS (must be tested before Gen 10401)

**The strategy may be systematically inverted.**

The simulation bets NO on world_events markets where market price > 12% + 0.033.
This means nearly every world_events market above ~15% is a NO bet.
If actual world_events markets on Polymarket resolve YES at a rate materially
above 12% — say, 17-25% — then:
  - Every NO bet in the simulation is a losing bet by construction
  - Higher simulation Sharpe would reflect a historical artifact, not a real edge
  - Live losses of -1.7% to -2.1% per sprint are exactly what this predicts
  - No amount of parameter optimization fixes an inverted base rate

**This hypothesis is testable in 1-2 hours (D1 below).**
It must be tested before running more simulation.
If confirmed, the simulation model requires a new base rate before any
further optimization has meaning.

---

## LOCKED BEST CONFIG (PARTIALLY UNVERIFIED)

```yaml
name: pm_research_best
category: world_events
price_range: [0.11, 0.55]        # VERIFIED (Gen 9616 simulation)
min_edge_pts: 0.033              # VERIFIED (simulation) — LIVE BUG: live=0.028
                                 # A0 hotfix NOT EXECUTED as of v52.0
max_days_to_resolve: 10          # UNVERIFIED — ambiguity unresolved since v47.0
min_liquidity_usd: 100           # ASSUMED — not confirmed from live logs
max_position_pct: 0.1            # ASSUMED
include_keywords: []
exclude_keywords: []
```

**Live config as of v52.0 (WRONG — do not trade with this):**
```yaml
min_edge_pts: 0.028              # INCORRECT — must be updated to 0.033
```

**If D1 reveals world_events base rate ≠ 12%, ALL config fields are suspect.**
Do not treat LOCKED BEST CONFIG as valid until D1 is complete.

---

## PRE-FLIGHT CHECKLIST FOR GEN 10401
*This is the eighth version of this checklist.*
*Items A0, D1, D2 are CRITICAL PATH. Complete these before any other step.*
*All items are BLOCKING. No simulation until all items are timestamped.*
*"Will do next version" is not an acceptable response to any item.*

---

### A. IMMEDIATE BUG FIX (do first — estimated 10 minutes)

- [ ] **A0 — LIVE CONFIG HOTFIX (BLOCKING — unfixed since v48.0):**
      The live YAML shows min_edge_pts=0.028.
      The simulation best is min_edge_pts=0.033.
      Every live trade since v48.0 used incorrect edge threshold.

      IF D1 (below) reveals base rate is wrong and strategy is inverted:
        → HALT ALL LIVE TRADING IMMEDIATELY before touching config.
        → Do not update to 0.033 if the strategy direction is wrong.
        → Fix D1 first, then determine correct parameters, then update.

      IF D1 confirms base rate is approximately correct:
        1. SSH to mist → update min_edge_pts to 0.033 → restart → print config
        2. SSH to kara → update min_edge_pts to 0.033 → restart → print config
        3. SSH to thrud → update min_edge_pts to 0.033 → restart → print config
        4. Verify each slot shows min_edge_pts: 0.033 in running config output

      mist updated: [ ]  Timestamp: ___________  Config output: ___________
      kara updated: [ ]  Timestamp: ___________  Config output: ___________
      thrud updated: [ ]  Timestamp: ___________  Config output: ___________

      *If this step cannot be completed for any reason, HALT all live trading.*

---

### D. ROOT CAUSE INVESTIGATION (CRITICAL PATH — do before B or C)
*These items have been listed since v48.0 and never completed.*
*They are now listed before config and gate items because they block everything.*
*Until D1 is complete, simulation results have unknown validity.*

- [ ] **D1 — MEASURE ACTUAL WORLD_EVENTS BASE RATE (highest priority item):**

      The simulation assumes world_events markets resolve YES at 12.0%.
      This value has never been validated against live Polymarket data.
      The live strategy bets NO on nearly every world_events market above 15%.
      If the true rate is materially above 12%, the strategy is directionally wrong.

      Procedure:
      1. Pull all resolved world_events markets from Polymarket API, last 90 days
         (or maximum available). Include only markets that resolved YES or NO.
      2. Count: n_yes = markets resolved YES, n_total = all resolved
      3. Compute: observed_rate = n_yes / n_total
      4. Compute 95% confidence interval: ±1.96 * sqrt(rate*(1-rate)/n)
      5. Record:

         n_total: _______
         n_yes: _______
         observed_rate: _______ (%)
         95% CI: [_______, _______]
         Simulation assumed: 12.0%
         Within CI of 12.0%: [ ] YES / [ ] NO

      6. If observed_rate > 16% or CI excludes 12%:
         → The simulation base rate is wrong.
         → Mark simulation results INVALID pending model correction.
         → Do not run Gen 10401 until base rate is corrected in simulation.
         → Update CRITICAL HYPOTHESIS status: CONFIRMED / REFUTED

      7. Also compute rate broken down by price range [0.11, 0.55] specifically:
         (Markets where initial market price was in this range)
         n_total_range: _______
         n_yes_range: _______
         rate_in_range: _______ (%)
         This is the most relevant base rate for the current strategy.

      Completed: [ ]  Timestamp: ___________
      Result summary: ___________
      Action required: ___________

- [ ] **D2 — PULL LIVE TRADE LOGS AND DIAGNOSE LOSSES:**

      0/32 trades have been profitable across three slots and multiple sprints.
      This cannot be variance. There is a systematic cause. Find it.

      Procedure:
      1. Pull complete trade logs from mist, kara, thrud for all sprints.
      2. For each losing trade, record:
         - Market name / ID
         - Market price at time of bet
         - Bet direction (YES or NO — confirm this matches expected direction)
         - Resolved outcome (YES or NO)
         - PnL for that trade
      3. Identify patterns:
         a. Are all bets in the same direction? (expect: mostly NO for world_events)
         b. Did the market resolve against the bet in every case?
         c. Was the bet direction correct per the simulation model?
            (i.e., if sim says bet NO at price 0.25 with base rate 0.12, did live
             bot actually bet NO?)
         d. Is the fee larger than the edge in practice?

      4. Check for implementation bugs:
         a. Is the YES/NO bet direction implemented correctly in the live bot?
            (This is a known failure mode — confirm explicitly)
         b. Is the base rate used in the live bot the same as the simulation?
         c. Is the price_range filter applied correctly?
         d. Are excluded markets actually being excluded?

      Trade log summary:
         Total trades reviewed: _______
         Trades where bet direction = NO: _______
         Trades where bet direction = YES: _______
         Markets that resolved YES: _______
         Markets that resolved NO: _______
         Apparent implementation bug identified: [ ] YES / [ ] NO
         Bug description (if yes): ___________

      Completed: [ ]  Timestamp: ___________
      Root cause identified: ___________

- [ ] **D3 — RECONCILE SIMULATION HISTORICAL DATA WITH LIVE MARKET UNIVERSE:**

      The simulation runs on 300k+ historical resolved markets.
      Live trading accesses current Polymarket markets.
      These may not be the same universe.

      Questions to answer:
      1. What time period does the simulation historical data cover?
         Answer: ___________
      2. Has Polymarket's market composition changed since that period?
         (More politics, fewer world_events, different resolution patterns?)
         Answer: ___________
      3. Is the simulation's world_events category defined the same way
         as Polymarket's