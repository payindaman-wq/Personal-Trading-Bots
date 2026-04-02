```markdown
# FREYA Research Program — Prediction Markets (v23.0)

## Status at Gen 4600
- **CRITICAL: Guard system confirmed non-functional.** bets=84 appears 11/20 last gens
  despite being blacklisted in 3 separate systems. Guards are not executing.
- **Zero improvements in 400 generations** (Gens 4201–4600).
- **Gen 4592 NEW RECOVERY TARGET:** adj=1.213, sharpe=0.2079, bets=6814 — config unknown.
  Positive sharpe, substantial bets. Priority 5 recovery. Likely filtered world_events
  or solo economics/politics.
- **Gen 4187/4188 configs STILL UNRECOVERED.** Recovery method required, not just priority.
- **LLM proposal suspension expired at Gen 4460** — proposals may be resuming but
  generating degenerate configs. Re-evaluate proposal source.
- **Live slots (mist, kara, thrud) remain DISABLED** until adj > 1.4 on NEW config.
- **Gen 3402/4382/4591 confirmed:** world_events baseline (adj=1.6196) is reproducible.

## IMMEDIATE ACTIONS REQUIRED (Before Gen 4601)

### ACTION 1: Guard System Verification (BLOCKING — do not simulate until resolved)
- Instrument pre_simulation_guard with explicit log output on EVERY call
- Verify guard is called before EVERY simulation invocation
- Add hard assertion: if guard not called → simulation must not run
- Test: inject known-bad config (bets=84 params) → must produce HardReject log
- If guard cannot be verified functional: HALT simulation loop entirely

### ACTION 2: Proposal Source Audit
- Identify what is generating proposals at Gens 4580–4600
- LLM suspension expired Gen 4460 — confirm LLM is back or identify fallback source
- If fallback/null config pathway active → disable it, require explicit proposal source
- The degenerate cycle (bets=84 repeated) indicates a null or broken proposal source

### ACTION 3: Gen 4592 Config Recovery (NEW PRIORITY 5)
- adj=1.213, sharpe=0.2079, bets=6814
- Recovery method: grid scan over {economics, politics, world_events+economics,
  world_events+politics} with min_edge ∈ [0.045, 0.075], price_range variants
- Target: reproduce bets≈6800 with sharpe > 0.20
- 25 generation budget for recovery scan

## All-Time Best
- **Gen 3402:** adj=1.6196, sharpe=0.2458, roi=18.225%, win=77.79%, bets=14510
  - category: world_events, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - CONFIRMED REPRODUCIBLE (Gen 4382, 4591 exact match).
  - **BASELINE REFERENCE ONLY. Do not tune. Do not inject. Do not simulate.**
- **Gen 4187:** adj=1.5865, sharpe=0.2431, bets=13634 — CONFIG UNKNOWN, RECOVER PRIORITY 1
- **Gen 4188:** adj=1.5020, sharpe=0.2371, bets=11258 — CONFIG UNKNOWN, RECOVER PRIORITY 2
- **Gen 3788:** adj=1.4766, sharpe=0.2235, bets=14771 — CONFIG UNKNOWN, RECOVER PRIORITY 3
- **Gen 3786:** adj=1.4665, sharpe=0.2348, bets=10304 — CONFIG UNKNOWN, RECOVER PRIORITY 4
- **Gen 4592:** adj=1.213, sharpe=0.2079, bets=6814 — CONFIG UNKNOWN, RECOVER PRIORITY 5
- **Gen 4389:** adj=0.0412, sharpe=0.0119, bets=623 — WEAK POSITIVE, config unknown, log only

## Key Learnings (Gens 1–4600)

### Confirmed Signals
- **Signal 1 — World Events Structural NO-Bias (CONFIRMED, CEILING ~adj=1.62)**
  - Base rate 12% vs. crowd pricing 25–40%.
  - Best config: world_events, no keywords, min_edge=0.055, min_liquidity=10,
    price_range=[0.07,0.80], max_days=14
  - adj=1.6196, sharpe=0.2458 — 1,198 gens without improvement.
  - Reproduced exactly at Gen 4382 and Gen 4591. Config is stable and deterministic.
  - **Status: BASELINE REFERENCE ONLY. Do not tune. Do not propose. Do not inject.**

- **Signal 2 — Gen 4592 Unidentified Positive (UNCONFIRMED)**
  - adj=1.213, sharpe=0.2079, bets=6814
  - Genuine structural signal (not noise at n=6814). Recovery is high priority.
  - Hypothesis: economics solo or world_events+economics union with tighter params.

### Confirmed Failures
- **Keyword filters:** 200+ gens, zero improvement. PERMANENTLY SUSPENDED.
- **bets < 500:** universally degenerate. HARD FLOOR enforced.
- **world_events sole-category tuning:** 1,198 gens, zero improvement. SUSPENDED.
- **LLM-proposal loop (raw):** Produced degenerate cycles. Requires prompt engineering
  review before re-enabling. Do not use default/unconstrained LLM proposals.
- **bets≈312 attractor:** Dead zone. Blacklisted.
- **bets≈84/78/93/119 attractor cluster:** PRIMARY DEAD ZONE.
  11+ hits in last 20 gens despite triple-blacklisting. Guard failure confirmed.
- **Injection queue v21.0:** FAILED.
- **Guard system v22.0:** FAILED (not executing). Rebuilt as v23.0.

### Unconfirmed High-Priority Signals (v23.0 targets)
1. **Gen 4187/4188 mystery configs** — HIGHEST PRIORITY. 13k–14k bets, sharpe ~0.24.
   Recovery method: systematic grid over {economics, politics, world_events+economics}
   with min_edge ∈ [0.04, 0.08], price_range ∈ {[0.07,0.80],[0.05,0.90],[0.10,0.75]},
   max_days ∈ {14, 21, 30}, min_liquidity ∈ {10, 25, 50}.
   Target bet range: 11000–15000. Run 50 gen grid budget.
2. **Gen 4592 mystery config** — NEW. Target bet range 6500–7100. 25 gen budget.
3. **Economics NO-bias (clean test)** — base rate 26%, NEVER CLEANLY RUN.
   Config template: category=economics, min_edge=0.055, min_liquidity=10,
   price_range=[0.07,0.80], max_days=14 (mirror of world_events baseline).
4. **Multi-category union: world_events + economics** — NEVER TESTED.
   Config template: categories=[world_events,economics], same params as baseline.
5. **Politics NO-bias (clean test)** — base rate 29.1%, NEVER CLEANLY TESTED.
   Config template: category=politics, min_edge=0.055, min_liquidity=10,
   price_range=[0.07,0.80], max_days=14.
6. **Multi-category union: world_events + politics** — NEVER TESTED.
7. **Multi-category union: world_events + economics + politics** — NEVER TESTED.
8. **Crypto** — base rate 31.5%, smallest structural edge, lowest priority.

---

## 🔴 HARD CONSTRAINTS (NON-NEGOTIABLE)

```python
# ABSOLUTE FLOORS
MIN_BETS_FLOOR = 500
MAX_DAYS_MIN = 7
MIN_LIQUIDITY_MAX = 50

# EXPANDED BET COUNT BLACKLIST v23.0
HARD_BLACKLIST_BET_RANGES = [
    (0, 10),      # Zero/near-zero class
    (30, 55),     # Near-zero class (expanded from 50)
    (70, 135),    # bets=84 attractor cluster (78, 84, 93, 119 all confirmed)
    (140, 165),   # Legacy attractor neighborhood (expanded from 160)
    (185, 205),   # Legacy attractor neighborhood (expanded from 200)
    (260, 325),   # bets=312 attractor neighborhood
]

HARD_BLACKLIST_BETS_LEGACY = [0, 1, 2, 6, 12, 45, 78, 83, 84, 85, 92, 93,
                               119, 142, 152, 153, 194, 270, 312]
# 152 ADDED at Gen 4600 (Gen 4597 produced bets=152, adj=-0.1762)

# SIMULATION OUTPUT BLACKLIST (post-simulation)
SIMULATION_OUTPUT_BLACKLIST = [
    # bets=84 attractor cluster
    {"bets": 84,  "adj": -0.6288},
    {"bets": 78,  "adj": -0.6099},
    {"bets": 93,  "adj": -0.5846},
    {"bets": 119, "adj": -0.7083},
    # bets=312 attractor
    {"bets": 312, "adj": -0.4766},
    # Legacy
    {"bets": 85,  "adj": -0.6208},
    {"bets": 35,  "adj": -0.1813},
    {"bets": 11,  "adj": -1.0},
    {"bets": 10,  "adj": -1.0},
    {"bets": 0,   "adj": -1.0},
    {"bets": 6,   "adj": -1.0},
    {"bets": 32,  "adj": -0.587},
    {"bets": 77,  "adj": 0.1139},
    {"bets": 152, "adj": -0.1762},  # NEW Gen 4597
    {"bets": 23,  "adj": -0.1377},  # NEW Gen 4593
    {"bets": 1,   "adj": -1.0},     # NEW Gen 4584/4599
]
# Matching rule: abs(result.bets - bl.bets) <= 5 AND abs(result.adj - bl.adj) <= 0.03

# CATEGORY LOCK
SUSPENDED_CATEGORIES = ["world_events"]  # as SOLE category only
# world_events IS PERMITTED in union/multi-category configs

# NO KEYWORDS — always
# LLM PROPOSALS: RE-ENABLED as of Gen 4461 BUT require constrained prompt
# See LLM Proposal Constraints below
LLM_PROPOSALS_SUSPENDED = False
LLM_PROPOSALS_REQUIRE_CONSTRAINED_PROMPT = True
```

```python
def pre_simulation_guard(config):
    """
    v23.0 — INSTRUMENTED VERSION
    EVERY call must emit a log line. Absence of log = guard not called = pipeline broken.
    """
    import logging
    guard_log = logging.getLogger("pre_simulation_guard")
    guard_log.info(f"GUARD_CALLED: config={flatten(config)}")  # REQUIRED — monitor this

    # 0. Null check
    if config is None or config.category is None:
        guard_log.warning("GUARD_REJECT: Null config")
        raise HardReject("Null config")

    # 1. LLM constrained prompt check
    if