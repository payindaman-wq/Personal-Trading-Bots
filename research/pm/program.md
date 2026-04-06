```markdown
# FREYA Research Program — v53.0

## Status at Gen 10600
- **Current best (this run):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616 — UNCHANGED)
- **Historical best (all runs):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Improvements this run (v52.0 → v53.0, 200 gens):** 0
- **Improvements last 800 gens:** 2 (Gen 9607, Gen 9616 only)
- **Improvements last 200 gens:** 0
- **Fixed-point collapse:** TERMINAL — seventeenth confirmed collapse
  Dominant attractors (last 20 gens):
    adj=2.2867/bets=17242 [seen 8/20 — primary attractor]
    adj=2.2936/bets=17728 [seen 3/20 — historical best, not improving]
    adj=-1.0/bets≤17       [seen 3/20 — degenerate]
    adj=2.2075-2.2455      [seen 3/20 — sub-optimal basin]
    adj=1.8854/bets=7627   [seen 1/20]
    adj=1.0817/bets=19067  [seen 1/20]
    adj=0.6549/bets=258    [seen 1/20]
  The loop has not produced a new best in 784 generations.
  The search space reachable by single-parameter proposals is exhausted.
- **Gate 1 NOT IMPLEMENTED** — ninth consecutive program without implementation
- **Gate 2 NOT IMPLEMENTED** — ninth consecutive program without implementation
- **HARD STOP VIOLATIONS:** v50.0, v51.0, and v52.0 hard stops all violated.
  This is the third consecutive violation of an explicit hard stop.
  200 generations ran in v52.0, produced zero improvements, consumed real compute.
  A fourth violation is not acceptable under any circumstance.
- **Live performance:** 0/32 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
  (mist: 0/8 at -1.7%, kara: 0/8 at -2.1%, thrud: 0/8 at -1.7%)
  p(0/32 | sim assumptions) < 10⁻²⁴. Root cause not identified.
  **TRADING MUST BE HALTED until D1 and D2 are complete.**
  Continued trading at current configuration is provably net-negative.
- **Config discrepancy:** live min_edge_pts=0.028 vs. simulation best=0.033.
  Hotfix A0 required since v48.0. Status: NOT EXECUTED after nine programs.
  NOTE: Do not execute A0 until D1 is complete — if base rate is wrong,
  changing edge threshold does not fix the underlying problem.
- **Current best config signature:** price_range=[0.11, 0.55], min_edge_pts=0.033,
  max_days=10 (unverified), category=world_events, keywords=[]
  **STATUS: CONDITIONALLY INVALID pending D1 result.**

---

## HARD STOP STATEMENT (v53.0)

**SIMULATION IS SUSPENDED. GEN 10601 MUST NOT RUN.**
**LIVE TRADING IS SUSPENDED. NO NEW SPRINT MAY START.**

Three consecutive hard stops have been violated.
Zero improvements have resulted from any generation after Gen 9616.
The live strategy has lost every single trade across 32 attempts.
The simulation model's foundational base rate has never been validated.

**The following actions are required before anything else:**

1. HALT live trading on mist, kara, and thrud immediately.
2. Complete D1 (measure actual world_events base rate) — ~2 hours.
3. Complete D2 (diagnose live trade losses) — ~2 hours.
4. Based on D1+D2 findings, either:
   a. Correct the simulation base rate and restart optimization from scratch, OR
   b. Identify and fix the live implementation bug and validate before resuming.
5. Record timestamps for all completed items in this document.
6. Only then may Gen 10601 run or live trading resume.

**Expected value of running Gen 10601 without completing D1:**
- Simulation improvement probability: ~0 (measured over 784 generations)
- Additional information gained: 0 (exhausted search space)
- Financial loss from continued live trading at wrong base rate: systematic

**Expected value of completing D1:**
- Cost: ~2 hours
- Information gained: whether the entire simulation framework is valid
- If base rate is wrong: prevents all future simulation waste
- If base rate is correct: narrows root cause to implementation bug

**There is no rational argument for running Gen 10601 before completing D1.**

---

## CRITICAL HYPOTHESIS (status: UNRESOLVED — must be tested before Gen 10601)

**The strategy may be systematically inverted due to incorrect base rate.**

The simulation bets NO on world_events markets where market price > 12% + 0.033.
This means nearly every world_events market above ~15% receives a NO bet.
If actual world_events markets on Polymarket resolve YES at a rate materially
above 12% — say, 17-25% — then:
  - Every NO bet is a losing bet by construction
  - The simulation's high Sharpe reflects a historical artifact, not real edge
  - Live losses of -1.7% to -2.1% per sprint are exactly what this predicts
  - No amount of parameter optimization fixes an inverted base rate
  - 0/32 live wins is the expected outcome of a structurally inverted strategy

**This hypothesis is testable in 1-2 hours (D1 below).**
**Status: UNRESOLVED after nine program versions.**
**If not tested before Gen 10601, all simulation results remain meaningless.**

Hypothesis resolution requires D1. Until D1 is complete:
- All simulation adj_scores are of unknown validity
- All config parameters derived from simulation are suspect
- Live trading with any configuration derived from this simulation is high-risk

---

## DECISION TREE (complete D1 first, then follow appropriate branch)

### Branch A: D1 shows observed_rate > 16% OR CI excludes 12%
→ Base rate is wrong. Strategy is inverted.
→ HALT all live trading immediately (if not already halted).
→ Update simulation base_rates['world_events'] to observed_rate from D1.
→ Re-run optimization from scratch (Gen 1, not Gen 10601).
→ Do not use any config parameter from the current best as a starting point.
→ Before resuming live trading, validate new simulation on holdout data.
→ Before resuming live trading, verify live bot uses corrected base rate.

### Branch B: D1 shows observed_rate ≈ 12% (within CI)
→ Base rate is approximately correct. Simulation findings are conditionally valid.
→ Root cause of 0/32 live losses must be an implementation bug.
→ Complete D2 immediately to identify the bug.
→ Fix the bug and validate on paper trading before resuming live trading.
→ A0 hotfix (min_edge_pts=0.033) may then be applied.
→ Simulation can resume with minor parameter search if D2 bug is unrelated
   to simulation validity.

### Branch C: D1 is inconclusive (insufficient data, API error, etc.)
→ Do not assume base rate is correct.
→ Treat situation as Branch A (halt trading, do not run simulation).
→ Find alternative data source for world_events resolution rates.
→ Do not resume until base rate is established with statistical confidence.

---

## PRE-FLIGHT CHECKLIST FOR GEN 10601
*This is the ninth version of this checklist.*
*Items D1 and D2 are CRITICAL PATH. A0 depends on D1 result.*
*ALL items are BLOCKING. No simulation and no live trading until timestamped.*
*"Will do next version" has been the response nine times. It is not acceptable.*

---

### D. ROOT CAUSE INVESTIGATION (COMPLETE THESE FIRST — EVERYTHING ELSE IS BLOCKED)

- [ ] **D1 — MEASURE ACTUAL WORLD_EVENTS BASE RATE (HIGHEST PRIORITY):**

      The simulation assumes world_events markets resolve YES at 12.0%.
      This value has never been validated against live Polymarket data.
      Until this is measured, no simulation result has known validity.

      Procedure:
      1. Pull all resolved world_events markets from Polymarket API, last 90 days
         (or maximum available). Include only markets resolved YES or NO.
         API endpoint: GET /markets?category=world_events&resolved=true
         (adjust to actual Polymarket API structure as needed)
      2. Count: n_yes = markets resolved YES, n_total = all resolved
      3. Compute: observed_rate = n_yes / n_total
      4. Compute 95% CI: ±1.96 × sqrt(rate × (1-rate) / n)
      5. Record:

         n_total: _______
         n_yes: _______
         observed_rate: _______ (%)
         95% CI: [_______, _______]
         Simulation assumed: 12.0%
         Within CI of 12.0%: [ ] YES  [ ] NO

      6. Also compute for price range [0.11, 0.55] specifically:
         n_total_in_range: _______
         n_yes_in_range: _______
         rate_in_range: _______ (%)
         This is the operationally relevant base rate for the current strategy.

      7. Also compute rate by resolution direction for NO bets specifically:
         (Markets where market price was above 12% + 0.033 = above ~15%)
         n_total_above_threshold: _______
         n_yes_above_threshold: _______
         rate_above_threshold: _______ (%)
         (If this rate >> 12%, NO bets in this zone are systematically losing)

      8. Apply Decision Tree above based on result.

      Completed: [ ]  Timestamp: ___________
      Result summary: ___________
      Decision Tree branch selected: [ ] A  [ ] B  [ ] C
      Action required: ___________

- [ ] **D2 — PULL LIVE TRADE LOGS AND DIAGNOSE LOSSES:**

      0/32 trades profitable. This is not variance. Find the systematic cause.

      Procedure:
      1. Pull complete trade logs from mist, kara, thrud for all sprints.
         Collect: market ID, market price at entry, bet direction, resolved outcome, PnL.
      2. For each trade, answer:
         a. Was bet direction NO or YES?
            (Expected: mostly NO, since nearly all world_events above 15% → NO)
         b. Did the market resolve against the bet?
         c. Is the loss consistent with fee drag alone, or is it directional loss?
            (Fee drag = ~2% per bet. Directional loss = market moves against position.)
      3. Check implementation correctness:
         a. Confirm live bot bet direction logic:
            IF market_price > base_rate + min_edge → bet NO
            IF market_price < base_rate - min_edge → bet YES
            Is this implemented correctly? [ ] YES  [ ] NO
            If NO, describe actual implementation: ___________
         b. Confirm base rate used in live bot: _______
            (Should be 12.0% for world_events — confirm this is what the bot uses)
         c. Confirm price_range filter: [_______, _______]
            (Should be [0.11, 0.55])
         d. Confirm min_edge_pts in live bot: _______
            (Is 0.028, should be 0.033 — but do not fix until D1 complete)
      4. Summarize findings:

         Total trades reviewed: _______
         Trades where bet direction = NO: _______
         Trades where bet direction = YES: _______
         Markets that resolved YES: _______
         Markets that resolved NO: _______
         Average market price at entry: _______
         Average PnL per trade: _______
         Loss type: [ ] Fee drag only  [ ] Directional (markets resolving against bets)
                    [ ] Mixed  [ ] Unknown
         Implementation bug identified: [ ] YES  [ ] NO
         Bug description: ___________

      Completed: [ ]  Timestamp: ___________
      Root cause identified: ___________

- [ ] **D3 — RECONCILE SIMULATION DATA WITH LIVE MARKET UNIVERSE:**

      The simulation uses 300k+ historical resolved markets.
      Live trading uses current Polymarket markets.
      These may not be the same universe.

      Procedure:
      1. What time period does the simulation historical data cover