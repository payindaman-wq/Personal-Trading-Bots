```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-2785 | Revised by MIMIR (Gen 2785 review)
# STATUS: NEW CHAMPION at Gen 2785 (sharpe=2.2828). Previous stall BROKEN.
# URGENT: Identify Gen 2785 parameter diff before proceeding. See STEP 0.

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor — do not change)

---
## ██████████████████████████████████████████████████████████
## ODIN INJECTION NOTE (INTERNAL ONLY — NEVER SEND TO LLM)
##
## ─────────────────────────────────────────────────────────
## STEP 0 — CHAMPION IDENTIFICATION [DO FIRST, BEFORE ALL ELSE]:
##
##   Gen 2785 produced sharpe=2.2828, trades=1272, win_rate=40.0%.
##   This is the new champion. The Gen 1592 config is NO LONGER active.
##
##   ACTION REQUIRED:
##   a) Retrieve the YAML that was backtested in Gen 2785.
##   b) Diff it against Gen 1592 champion (stop_loss=1.91, rsi_short=60,
##      rsi_period=24, trend_period=48, tp=4.65, timeout=159).
##   c) Identify exactly ONE parameter that differs. Record it here:
##      IDENTIFIED CHANGE: [FILL IN — e.g., rsi_period_hours: 24→22]
##   d) Update the champion YAML below to reflect Gen 2785 values.
##   e) Set that parameter's P-item as RESOLVED in the priority queue.
##   f) Only then proceed to priority queue testing.
##
##   IF GEN 2785 YAML IS UNAVAILABLE:
##   Infer from fingerprint: trades=1272 (+5 vs 1267).
##   Most likely candidates:
##     P7 (rsi_period 24→22): faster RSI → more signals → +5 trades ✓ MOST LIKELY
##     P4 (rsi_short 60→59): more short entries → +5 trades possible ✓
##     P3 (tp 4.65→4.70): harder to hit → typically FEWER trades ✗ LESS LIKELY
##   Run confirmation backtests if needed:
##     Test A: rsi_period=22, all else Gen 1592 → expect ~1272 trades, ~2.2828
##     Test B: rsi_short=59, all else Gen 1592 → confirm or deny
##
## ─────────────────────────────────────────────────────────
## STEP 1 — DIRECT INJECTION (preferred, mandatory for all P-items):
##   Bypass the LLM entirely for all priority queue items.
##   Construct the YAML programmatically from champion + one parameter diff.
##   This eliminates clone/drift/zombie failure modes completely.
##   LLM clone rate confirmed at ~35% — direct injection is not optional.
##   If direct injection is available, skip STEP 2.
##
## STEP 2 — LLM FALLBACK (only if direct injection unavailable):
##   Send the LLM ONLY the section marked "LLM PROMPT" below.
##   Strip ALL other sections from LLM input.
##   Use temperature=0.0 (minimum).
##   If Attractor 1 or Attractor 3 appears: reject, do NOT count as valid gen,
##   retry up to 3 times, then skip to next priority item.
##   After 3 consecutive Attractor outputs on same Px item: auto-advance to Px+1.
##
## STEP 3 — GRID SCAN FALLBACK (if LLM fails repeatedly):
##   Run backtester directly on target parameter range with all other params frozen.
##   Accept best result as new champion if sharpe > 2.2828 (updated threshold).
##
## ─────────────────────────────────────────────────────────
## PRIORITY QUEUE (ODIN internal — NEVER send to LLM):
## All tests use Gen 2785 champion as baseline (sharpe=2.2828).
## Accept improvement only if sharpe > 2.2828 AND trades ≥ 400.
##
## P0 [IMMEDIATE — resolve before other P-items]:
##   ACTION: Identify Gen 2785 change (see STEP 0 above).
##   Once identified, mark the corresponding P-item RESOLVED.
##   Baseline champion YAML = Gen 2785 config (not Gen 1592).
##
## ── ASSUMING P7 RESOLVED (rsi_period 24→22) — most likely scenario ──
##
## P7-NEXT [if P7=RESOLVED, rsi_period went 24→22]:
##   rsi_period_hours: 22 → 20
##   All other params: Gen 2785 champion values.
##   Rationale: Continue directional search on RSI period.
##   Risk: May push toward high-frequency noise or Attractor 3 territory.
##   If trades increase significantly (>1350): caution, may be overfitting.
##   Stop direction if sharpe < 2.2828 or trades < 400.
##
## P4 [ACTIVE — test against Gen 2785 baseline]:
##   rsi_short_threshold: 60 → 59  (or keep at 59 if P4=RESOLVED)
##   All other params: Gen 2785 champion values.
##   Rationale: Slightly more selective short entries.
##   NOTE: If Gen 2785 change WAS rsi_short 60→59, mark P4 RESOLVED
##         and instead test rsi_short=58.
##
## P3 [ACTIVE — test against Gen 2785 baseline]:
##   take_profit_pct: 4.65 → 4.70
##   (Use Gen 2785 TP value if TP was the Gen 2785 change)
##   stop_loss_pct stays: Gen 2785 value (1.91 unless P2 resolved)
##   Rationale: Wider TP, R:R improvement.
##   If improves: test 4.75, then 4.80 (stop at first failure).
##   Expected: trades may decrease slightly (harder to hit TP).
##
## P2 [ACTIVE — retest against Gen 2785 baseline]:
##   stop_loss_pct: 1.91 → 1.89
##   All other params: Gen 2785 champion values.
##   Rationale: Tighter stop. Previously failed 800+ times vs Gen 1592 baseline.
##              Worth one clean test vs new Gen 2785 baseline.
##   KNOWN HAZARD: 1.90 = ZombieD (trades≈1228, sharpe≈1.59). SKIP 1.90.
##   Floor: 1.88 (below = ZombieC).
##   Use DIRECT INJECTION only — LLM cannot execute this change reliably.
##   If P2 improves: new champion. Test stop_loss=1.88 next.
##   If P2 fails: SL stays at 1.91. Record and move on. Do not retry.
##   If P2 Zombie (trades<400): SL floor confirmed at 1.91. Do not retry.
##   LIMIT: Maximum 3 clean attempts (direct injection). If all fail: CLOSE P2.
##
## P6 [ACTIVE]:
##   trend_period_hours: 48 → 50
##   All other params: Gen 2785 champion values.
##   Rationale: Slower trend filter may reduce false signals.
##   Expected: minor trade count change, unknown sharpe direction.
##
## P5 [SUSPENDED — do not test]:
##   rsi_long_threshold: 37.77 → 37.72
##   Reason: Infinitesimally small change, high contamination risk, low upside.
##
## ─────────────────────────────────────────────────────────
## COMPOUND TESTING (only after at least two Px items independently resolve):
##   Rule: Never combine two untested changes.
##   Rule: Each compound test = exactly TWO resolved improvements combined.
##   Rule: Compound tests require direct injection — no LLM.
##
##   Priority compound candidates (once individual results known):
##   C1: If P4 + P3 both improve independently → test P4+P3 combined.
##   C2: If P7-NEXT + P4 both improve independently → test combined.
##   C3: If P2 + any Px improve independently → test P2+Px combined.
##
## ─────────────────────────────────────────────────────────
## KNOWN FAILURE FINGERPRINTS (validator — auto-reject these):
##
## Attractor 1  [CLONE]:      trades=1267, sharpe=2.2657 → Gen 1592 clone (stale)
## Attractor 1b [NEW CLONE]:  trades=1272, sharpe=2.2828 → Gen 2785 clone (nothing changed)
## Attractor 3  [RSI DRIFT]:  trades=1272, sharpe=2.2015 → RSI or param contaminated
## Ghost Echo   [TIMEOUT]:    trades=1264, sharpe=2.1998 → timeout=166h used
## Zombie C     [EXTREME]:    trades<400                 → RSI extreme or stop<1.88
## Zombie D     [SL=1.90]:    trades≈1228, sharpe≈1.59  → stop_loss=1.90 (never use)
## Zombie G-adj [TIMEOUT]:    trades≈888,  sharpe≈2.00  → timeout=155h used
##
## NOTE: Attractor 1 (1267 trades, 2.2657) is now a STALE CLONE fingerprint.
##       Any result matching Gen 1592 values means the LLM used old champion YAML.
##       Reject and re-inject Gen 2785 champion YAML before retrying.
##
## ATTRACTOR 3 DIAGNOSTIC NOTE:
##   Attractor 3 (1272 trades, 2.2015) — note trade count now overlaps with Gen
##   2785 champion. Distinguish by sharpe: 2.2828 = new champion, 2.2015 = Attractor 3.
##   Trades=1272 alone is no longer diagnostic. Use BOTH trades AND sharpe.
##
## ─────────────────────────────────────────────────────────
## FROZEN PARAMETERS (hard-reject any YAML violating these):
##   size_pct       = 25       (FOREVER)
##   timeout_hours  = 159      (FOREVER — 155=ZombieG, 166=GhostEcho)
##   max_open       = 3        (FOREVER)
##   leverage       = 2        (FOREVER)
##   fee_rate       = 0.0005   (FOREVER)
##   stop_loss_pct  ≥ 1.88     (floor — below = ZombieC territory)
##   stop_loss_pct  ≠ 1.90     (FORBIDDEN — ZombieD)
##
## ─────────────────────────────────────────────────────────
## LLM FAILURE RATE SUMMARY (for operational awareness):
##   Clone rate (Attractor 1):  ~35% of LLM generations
##   Zombie rate (trades<400):  ~15% of LLM generations
##   Attractor 3 drift:         ~10% of LLM generations
##   Degraded/other:            ~35% of LLM generations
##   Valid novel result:        ~5% of LLM generations
##   → Direct injection is mandatory for all P-items.
##   → LLM should only be used for exploratory/creative proposals, not P-item execution.
##
## ─────────────────────────────────────────────────────────
## POST-P-ITEM RESOLUTION PATHS:
##   P7 RESOLVED (likely) → Test P7-NEXT (rsi_period=20). Test P4, P3, P6 independently.
##   P4 RESOLVED → Compound test C1 or C2 when second item resolves.
##   P3 RESOLVED → Test 4.75 next. Compound test C1 when second item resolves.
##   P2 RESOLVED → New champion with SL=1.89. Test SL=1.88 (absolute floor).
##   P2 FAILED/CLOSED → SL stays at Gen 2785 value. Focus P3/P4/P6/P7-NEXT.
##   P6 RESOLVED → Test trend_period=52 next.
##
## ─────────────────────────────────────────────────────────
## MACRO NOTE (does NOT affect research YAML):
##   TYR: DANGER regime (F&G=15, Extreme Fear). Stable for 10+ readings.
##   Live sizing: 25% × 25% = 6.25% effective. Research size_pct stays 25.
##   No completed live sprints yet. Out-of-sample validation CRITICAL.
##   FRAGILITY WARNING: Parameter sensitivity is extremely high (SL 1.90 vs 1.91
##   produces sharpe 1.59 vs 2.27). Treat live deployment with caution.
##   POSITIVE DEVELOPMENT: Gen 2785 broke 1,008-generation stall. Momentum
##   may indicate the parallel P3/P4/P6/P7 strategy is working.
## ██████████████████████████████████████████████████████████

---
## ══════════════════════════════════════════════════════════
## LLM PROMPT — SEND ONLY THIS SECTION TO THE LLM
## Strip everything above and below. No exceptions.
## Use temperature=0.0 (minimum). No system prompt needed.
## NOTE TO ODIN: Replace [TARGET_PARAM] and [TARGET_VALUE] with the
##   specific change before sending. Do not send placeholder text.
## ══════════════════════════════════════════════════════════

Make EXACTLY ONE change to the YAML below.

THE CHANGE: [TARGET_PARAM]: [CURRENT_VALUE]  →  [TARGET_PARAM]: [TARGET_VALUE]

Do not change any other line. Output only the complete modified YAML.

```yaml
name: crossover
style: swing_momentum
inspiration: "ODIN-injected champion — updated at each sprint reset"
league: futures_swing
leverage: 2
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
- XRP/USD
- DOGE/USD
- AVAX/USD
- LINK/USD
- UNI/USD
- AAVE/USD
- NEAR/USD
- APT/USD
- SUI/USD
- ARB/USD
- OP/USD
- ADA/USD
- POL/USD
position:
  size_pct: 25
  max_open: 3
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: up
    - indicator: rsi
      period_hours: [GEN_2785_RSI_PERIOD]
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: [GEN_2785_RSI_PERIOD]
      operator: gt
      value: [GEN_2785_RSI_SHORT]
exit:
  take_profit_pct: [GEN_2785_TP]
  stop_loss_pct: 1.91
  timeout_hours: 159
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

Verify before submitting:
1. Only [TARGET_PARAM] has changed ✅
2. timeout_hours = 159 ✅
3. stop_loss_pct ≠ 1.90 ✅
4. stop_loss_pct ≥ 1.88 ✅
5. size_pct = 25 ✅
6. All other params match Gen 2785 champion ✅

## ══════════════════════════════════════════════════════════
## END OF LLM PROMPT
## ══════════════════════════════════════════════════════════

---
## CHAMPION SUMMARY (Gen 2785) — ODIN REFERENCE
## ⚠ SUPERSEDES Gen 1592. Do not use Gen 1592 values as baseline.

- Sharpe: 2.2828 | Win rate: 40.0% | Trades: 1,272
- Entry: trend(48h) + RSI(period=TBD) mean-reversion
  - Long:  trend=up   AND RSI < 37.77
  - Short: trend=down AND RSI > 60 (or 59 if P4 was Gen 2785 change)
- Exit: TP=4.65% (or 4.70 if P3 was Gen 2785 change), SL=1.91%, timeout=159h
- Sizing: 25% per position, max_open=3, 2x leverage
- R:R: 4.65/1.91 = 2.43:1 (minimum — may be higher if TP changed)
- Risk guard: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR,
          APT, SUI, ARB, OP, ADA, POL)
- Live performance: no completed sprints (autobotswingfutures)
- Sensitivity: EXTREME — SL 1.90 collapses sharpe to 1.59 (ZombieD)
- ⚠ YAML PLACEHOLDER NOTE: Update [GEN_2785_*] fields in LLM PROMPT
  section once Gen 2785 parameter diff is confirmed (see STEP 0).

## STALL STATUS (MIMIR, Gen 2785 review):
- Previous stall: 1,008 generations (Gen 1592→2784) — NOW BROKEN
- Gen 2785 improvement: +0.0171 sharpe (2.2657→2.2828), +5 trades
- Probable cause: One of P3/P4/P6/P7 succeeded (most likely P7)
- Next steps: Identify change → update champion → continue P-item queue
- Live validation: Still zero completed sprints — deploy conservatively
- Direct injection: MANDATORY — LLM clone rate ~35%, valid rate ~5%

DO NOT use Gen 1592 config as baseline. Gen 2785 is the active champion.
DO NOT use stop_loss_pct = 1.90 under any circumstances (ZombieD).
DO NOT combine changes until individual improvements are confirmed.
```