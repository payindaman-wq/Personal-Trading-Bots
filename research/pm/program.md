```markdown
# FREYA Research Program — v54.0

## Status at Gen 10800
- **Current best (this run):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616 — UNCHANGED)
- **Historical best (all runs):** adj=2.2936, sharpe=0.3379, bets=17728 (Gen 9616)
- **Improvements this run (v53.0 → v54.0, 200 gens):** 0
- **Improvements last 1000 gens:** 2 (Gen 9607, Gen 9616 only)
- **Improvements last 200 gens:** 0
- **Fixed-point collapse:** TERMINAL — eighteenth confirmed collapse
  Dominant attractors (last 20 gens):
    adj=2.2867/bets=17242 [seen 8/20 — primary attractor]
    adj=2.2936/bets=17728 [seen 3/20 — historical best, not improving]
    adj=-1.0/bets=0       [seen 1/20 — degenerate]
    adj=2.0466-2.2455     [seen 3/20 — sub-optimal basin]
    adj=0.6549-1.8854     [seen 4/20 — low-bet basin]
  The loop has not produced a new best in 984 generations.
  The search space reachable by single-parameter proposals is exhausted.
  Measured improvement probability over last 784 gens: ~0.

- **Gate 1 NOT IMPLEMENTED** — tenth consecutive program without implementation
- **Gate 2 NOT IMPLEMENTED** — tenth consecutive program without implementation

- **HARD STOP VIOLATIONS:** v50.0, v51.0, v52.0, and v53.0 hard stops all violated.
  This is the FOURTH consecutive violation of an explicit hard stop.
  800 total generations have run across four violations, producing zero improvements.
  A fifth violation represents complete breakdown of the research governance process.

- **Live performance:** 0/32 wins across mist/kara/thrud — CRITICAL STRUCTURAL FAILURE
  (mist: 0/8 at -1.7%, kara: 0/8 at -2.1%, thrud: 0/8 at -1.7%)
  p(0/32 | sim assumptions valid) < 10⁻²⁴
  Loss profile: ~2% per trade = fee-magnitude loss = consistent with every bet
  resolving against the predicted direction = consistent with inverted base rate.
  Root cause: NOT YET IDENTIFIED (D1 and D2 incomplete after ten program versions).
  **TRADING MUST REMAIN HALTED. NO NEW SPRINT MAY START UNDER ANY CIRCUMSTANCES.**

- **Config discrepancy:** live min_edge_pts=0.028 vs. simulation best=0.033.
  Hotfix A0 required since v48.0. Status: BLOCKED pending D1.
  Do not apply A0 until D1 is complete. If base rate is wrong, A0 is irrelevant.

- **Current best config signature:** price_range=[0.11, 0.55], min_edge_pts=0.033,
  max_days=10, category=world_events, keywords=[]
  **STATUS: CONDITIONALLY INVALID pending D1 result.**
  **DO NOT USE THIS CONFIG FOR LIVE TRADING UNTIL D1 IS COMPLETE.**

---

## ABSOLUTE HARD STOP — v54.0

### GEN 10801 MUST NOT RUN.
### LIVE TRADING MUST NOT RESUME.
### NO NEW SPRINT MAY START.

This is not a recommendation. These are inviolable conditions.

Four consecutive hard stops have been violated. Zero improvements have resulted
from any generation after Gen 9616. The live strategy has lost every single trade
across 32 attempts. The simulation model's base rate has never been validated.

The cost of violating this hard stop a fifth time:
- Simulation: 0 expected improvements, 100% certainty of compute waste
- Live trading: systematic negative EV until root cause is identified and fixed
- Information: zero new information gained from either activity

The cost of completing D1 and D2:
- Time: ~4 hours total
- Information: whether the entire simulation and live framework is valid
- Financial: prevents ongoing systematic losses

**There is no argument, under any decision framework, for running Gen 10801
before D1 is complete. None. This has been true for nine program versions.**

**REQUIRED ACTIONS BEFORE ANYTHING ELSE (in order):**

1. [ ] CONFIRM live trading is halted on mist, kara, and thrud.
       No new sprints. No manual trades. Nothing.
       Timestamp confirmed: ___________

2. [ ] COMPLETE D1 (measure actual world_events base rate).
       Hard deadline: within 48 hours of this document being read.
       Timestamp started: ___________
       Timestamp completed: ___________

3. [ ] COMPLETE D2 (diagnose live trade losses).
       Hard deadline: within 48 hours of D1 completion.
       Timestamp started: ___________
       Timestamp completed: ___________

4. [ ] APPLY DECISION TREE based on D1+D2 findings (see below).
       Timestamp: ___________

5. [ ] Only after steps 1-4 are timestamped and complete may Gen 10801 run
       or live trading resume.

---

## CRITICAL HYPOTHESIS (UNRESOLVED — tenth consecutive program)

**The strategy is almost certainly inverted due to an incorrect base rate.**

Evidence supporting this hypothesis:
- Simulation bets NO on world_events where market price > 12% + 0.033 ≈ 15.3%
- Nearly every world_events market in the price range [0.11, 0.55] receives a NO bet
- If actual world_events YES resolution rate is 17-25% (plausible for current Polymarket):
  → Every NO bet in the 15-25% price zone is a losing bet by construction
  → Losses of ~2% per trade = fee-magnitude = consistent with directional losing
  → 0/32 live wins is the expected outcome
  → Simulation Sharpe of 0.3379 reflects historical artifact, not real edge
- This hypothesis is testable in ~2 hours (D1 below)
- It has not been tested in ten program versions

**If this hypothesis is correct:**
- No parameter change fixes it
- No additional simulation generations fix it
- The only fix is: measure the true base rate, correct the simulation, restart from Gen 1
- All 10,800 simulation generations are invalid as a basis for live trading

**If this hypothesis is incorrect (D1 shows ~12% base rate):**
- The simulation findings are conditionally valid
- The root cause of 0/32 live losses is an implementation bug
- D2 will identify the bug
- Fixing the bug may restore positive EV

---

## DECISION TREE (execute after D1)

### Branch A: D1 shows observed_rate > 16% OR 95% CI excludes 12.0%
→ Base rate is wrong. Strategy is inverted. This confirms the critical hypothesis.
→ HALT all live trading (should already be halted — confirm).
→ Update simulation: base_rates['world_events'] = observed_rate from D1.
→ RESTART optimization from Gen 1 with corrected base rate.
   Do NOT continue from Gen 10800. Do NOT use current config as starting point.
   The current config is derived from an invalid base rate and is meaningless.
→ Before any live trading: validate new simulation on holdout data (last 30 days).
→ Before any live trading: verify live bot uses corrected base rate (not 12%).
→ Before any live trading: paper trade for minimum 1 sprint (8 trades) with new config.
→ Record: new base rate used, Gen 1 restart timestamp, holdout validation result.

### Branch B: D1 shows observed_rate ≈ 12% (within 95% CI)
→ Base rate is approximately correct. Simulation validity is conditionally confirmed.
→ Root cause of 0/32 live losses is an implementation bug in the live bot.
→ Complete D2 immediately (if not already complete).
→ Identify the specific bug (direction logic, base rate value, price filter, etc.).
→ Fix the bug. Do NOT resume live trading until bug is fixed and verified.
→ Paper trade for minimum 1 sprint (8 trades) after bug fix.
→ Apply A0 hotfix (min_edge_pts: 0.028 → 0.033) after bug is confirmed fixed.
→ Simulation may resume with architecture change (see below — not single-param hill climb).
→ Record: bug identified, fix applied, paper trade results, A0 applied timestamp.

### Branch C: D1 is inconclusive (insufficient data, API errors, etc.)
→ Do NOT assume base rate is correct.
→ Treat as Branch A: halt trading, do not run simulation.
→ Find alternative data source (manual market review, different API, scraping).
→ Do not resume until base rate is established with statistical confidence.
→ Record: reason for inconclusive result, alternative data source being tried.

---

## ROOT CAUSE INVESTIGATION PROCEDURES

### D1 — MEASURE ACTUAL WORLD_EVENTS BASE RATE (HIGHEST PRIORITY)

The simulation assumes world_events markets resolve YES at 12.0%.
This value has NEVER been validated. It is the single most important unknown.

Procedure:
1. Pull all resolved world_events markets from Polymarket, last 90 days minimum.
   Include only binary markets resolved YES or NO (exclude N/A, cancelled).
   Use Polymarket API or Gamma Markets API. Adjust endpoint to actual API structure.
   Suggested: GET /markets?tag=world_events&closed=true (or equivalent)

2. Count:
   n_total: _______ (all resolved YES or NO)
   n_yes: _______ (resolved YES)

3. Compute:
   observed_rate = n_yes / n_total = _______ (%)
   95% CI = observed_rate ± 1.96 × sqrt(rate × (1-rate) / n_total)
   95% CI: [_______, _______]
   Simulation assumed: 12.0%
   12.0% within CI: [ ] YES → Branch B    [ ] NO → Branch A

4. Repeat for price range [0.11, 0.55] only (operationally relevant subset):
   n_total_in_range: _______
   n_yes_in_range: _______
   rate_in_range: _______ (%)
   95% CI_in_range: [_______, _______]

5. Repeat for markets where price > 0.153 (above betting threshold):
   n_total_above_threshold: _______
   n_yes_above_threshold: _______
   rate_above_threshold: _______ (%)
   (If this rate >> 12%, NO bets in this zone are systematically losing)

6. Apply Decision Tree above.

Completed: [ ]  Timestamp: ___________
n_total: _______  n_yes: _______  observed_rate: _______ %
95% CI: [_______, _______]
12.0% within CI: [ ] YES  [ ] NO
Decision Tree branch selected: [ ] A  [ ] B  [ ] C

---

### D2 — DIAGNOSE LIVE TRADE LOSSES

0/32 wins is not variance. There is a systematic cause. Find it.

Procedure:
1. Pull complete trade logs from mist, kara, thrud for all 4 sprints.
   For each trade collect:
   - Market ID
   - Market price at entry
   - Bet direction (YES or NO)
   - Resolution outcome (YES or NO)
   - PnL

2. Compute aggregate statistics:
   Total trades: _______
   Bet direction = NO: _______  Bet direction = YES: _______
   Markets resolved YES: _______  Markets resolved NO: _______
   Average entry price: _______
   Average PnL per trade: _______
   Loss type:
   [ ] Fee drag only (~2% per bet, consistent with random resolution)
   [ ] Directional — markets resolving AGAINST bet direction consistently
   [ ] Mixed
   [ ] Unknown

3. Check implementation:
   a. Live bot bet direction logic:
      Expected: IF price > base_rate + edge → bet NO
                IF price < base_rate - edge → bet YES
      Actual (describe): ___________
      Correct: [ ] YES  [ ] NO

   b. Base rate used in live bot: _______
      (Expected: 12.0% for world_