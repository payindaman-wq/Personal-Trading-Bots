```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-2899 | Revised by MIMIR (Gen 2899 review)
# STATUS: NEW CHAMPION at Gen 2899 (sharpe=2.3219). Four improvements since Gen 2785.
# CRITICAL: Champion YAML has placeholder/stale values — see STEP 0.

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
## STEP 0 — YAML INTEGRITY CHECK [DO THIS BEFORE ALL ELSE]:
##
##   CRITICAL DISCREPANCY DETECTED:
##   The "Current Best Strategy" YAML displayed by ODIN contains:
##     stop_loss_pct = 1.92   ← WRONG (champion value is 1.91)
##     timeout_hours = 192    ← WRONG (champion value is 159, FROZEN)
##   These do NOT match the documented Gen 2899 champion parameters.
##   This indicates ODIN's champion YAML storage is corrupted or stale.
##
##   ACTION REQUIRED:
##   a) Retrieve the actual YAML that was backtested in Gen 2899.
##   b) Confirm exact parameter values — do NOT use the displayed YAML.
##   c) Diff Gen 2899 vs Gen 2813 to identify the ONE change at Gen 2899.
##   d) Diff Gen 2813 vs Gen 2791 to identify the ONE change at Gen 2813.
##   e) Diff Gen 2791 vs Gen 2785 to identify the ONE change at Gen 2791.
##   f) Record the complete confirmed champion parameter set below.
##   g) Replace ALL [GEN_2899_*] placeholders in the LLM PROMPT with
##      actual numeric values before sending to LLM.
##   h) Update the CHAMPION SUMMARY section at the bottom of this file.
##
##   IMPROVEMENT CHAIN ANALYSIS (from fingerprints):
##   Gen 2785: sharpe=2.2828, trades=1272 (+5 vs 1267) → BASELINE
##   Gen 2791: sharpe=2.2910, trades=1269 (-3 vs 1272) → small trade decrease
##   Gen 2813: sharpe=2.3055, trades=1268 (-1 vs 1269) → minor trade decrease
##   Gen 2899: sharpe=2.3219, trades=1263 (-5 vs 1268) → trade decrease continues
##
##   PATTERN: Each improvement shows declining trade count with improving Sharpe.
##   This is consistent with:
##     (a) TP widening: harder to hit → fewer trades, better R:R ✓ LIKELY
##     (b) RSI threshold tightening: more selective entries → fewer trades ✓ LIKELY
##     (c) SL tightening: MORE exits early → trade count less predictable ✗ LESS LIKELY
##   Hypothesis: The active improvement vector is TP widening or RSI tightening.
##   Confirm by identifying the parameter diff at each gen.
##
##   MOST LIKELY RECONSTRUCTION (pending confirmation):
##   Gen 2785 change: rsi_period 24→22 (P7, +5 trades — faster RSI, more signals)
##   Gen 2791 change: likely TP 4.65→4.70 (P3, -3 trades)
##   Gen 2813 change: likely TP 4.70→4.75 OR rsi_short 60→59 (P3-next or P4)
##   Gen 2899 change: likely TP 4.75→4.80 OR rsi_short tightening (-5 trades)
##   NOTE: These are inferences only. Confirm from actual backtested YAMLs.
##
## ─────────────────────────────────────────────────────────
## CONFIRMED CHAMPION PARAMETERS (update once STEP 0 complete):
##
##   rsi_period_hours:    [CONFIRM — likely 22, was 24 at Gen 1592]
##   rsi_long_threshold:  37.77  (unchanged since Gen 1477 — do not touch)
##   rsi_short_threshold: [CONFIRM — likely 59 or 60]
##   trend_period_hours:  48     (unchanged — confirm)
##   take_profit_pct:     [CONFIRM — likely 4.75 or 4.80]
##   stop_loss_pct:       1.91   (confirm — NOT 1.92 as shown in stale YAML)
##   timeout_hours:       159    (FROZEN FOREVER — NOT 192 as shown in stale YAML)
##
## ─────────────────────────────────────────────────────────
## STEP 1 — DIRECT INJECTION (mandatory for all P-items):
##   Bypass the LLM entirely for all priority queue items.
##   Construct the YAML programmatically from confirmed champion + one parameter diff.
##   LLM clone rate confirmed at ~35%, valid rate ~5%.
##   Direct injection eliminates clone/drift/zombie/placeholder failure modes.
##   If direct injection is available, skip STEP 2 entirely.
##
## STEP 2 — LLM FALLBACK (only if direct injection unavailable):
##   Send the LLM ONLY the section marked "LLM PROMPT" below.
##   Strip ALL other sections. Use temperature=0.0.
##   MANDATORY: Replace ALL [GEN_2899_*] placeholders with actual values first.
##   Sending placeholder text to LLM will produce garbage output — do not do this.
##   If Attractor 1, 1b, 3, or 4 appears: reject, do NOT count as valid gen.
##   Retry up to 3 times, then skip to next priority item.
##   After 3 consecutive Attractor outputs on same Px item: auto-advance to Px+1.
##
## STEP 3 — GRID SCAN FALLBACK (if LLM fails repeatedly):
##   Run backtester directly on target parameter range with all other params frozen.
##   Accept best result as new champion if sharpe > 2.3219 AND trades ≥ 400.
##
## ─────────────────────────────────────────────────────────
## PRIORITY QUEUE (ODIN internal — NEVER send to LLM):
## All tests use Gen 2899 champion as baseline (sharpe=2.3219, trades=1263).
## Accept improvement only if sharpe > 2.3219 AND trades ≥ 400.
##
## P0 [IMMEDIATE — resolve before other P-items]:
##   ACTION: Complete STEP 0 YAML integrity check.
##   Confirm all Gen 2899 parameter values.
##   Identify which P-items have already been resolved (2791, 2813, 2899 changes).
##   Update priority queue status accordingly.
##   DO NOT proceed with P-item testing until confirmed champion YAML is locked.
##
## ── PRIORITY QUEUE (pending P0 confirmation) ──
##
## P3-CONT [ACTIVE if TP was the recent improvement vector]:
##   Hypothesis: TP has been widening through recent improvements.
##   If Gen 2899 TP = 4.80: test 4.85 next.
##   If Gen 2899 TP = 4.75: test 4.80 next.
##   If Gen 2899 TP = 4.70: test 4.75 next (this would mean P3 stalled earlier).
##   All other params: Gen 2899 champion values.
##   Stop direction when: sharpe < 2.3219 OR trades drop below 1,200 (caution zone).
##   Hard stop: TP ≥ 5.50 (above this, too few trades, over-optimized).
##   Expected: each +0.05 TP step → approximately -3 to -5 trades.
##
## P4-STATUS [resolve status before testing]:
##   rsi_short_threshold: current value → current_value - 1
##   If rsi_short is already 59: test 58.
##   If rsi_short is already 58: test 57.
##   If rsi_short is still 60: test 59.
##   Rationale: Each -1 step slightly reduces short entries → fewer trades.
##   This aligns with the declining-trades/improving-Sharpe pattern.
##   Floor: rsi_short ≥ 55 (below = too restrictive, Zombie risk).
##   All other params: Gen 2899 champion values.
##
## P7-STATUS [resolve status before testing]:
##   rsi_period_hours: current value → current_value - 2
##   If rsi_period is 22: test 20.
##   If rsi_period is 20: test 18 (caution: noise risk).
##   Rationale: Faster RSI → more responsive signals.
##   Risk: Below 18h RSI → high-frequency noise, Zombie territory.
##   Warning threshold: if trades increase above 1,300 → signal noise, stop.
##   All other params: Gen 2899 champion values.
##
## P2 [ACTIVE — one clean test only]:
##   stop_loss_pct: 1.91 → 1.89
##   All other params: Gen 2899 champion values.
##   KNOWN HAZARD: 1.90 = ZombieD (FORBIDDEN). Skip 1.90 entirely.
##   Floor: 1.88 (below = ZombieC territory).
##   Use DIRECT INJECTION only.
##   If improves: test 1.88 (absolute floor test). Do not test below 1.88.
##   If fails or Zombie: close P2 permanently. SL stays at 1.91.
##   LIMIT: Maximum 2 clean direct-injection attempts. If both fail: CLOSE P2.
##
## P6 [ACTIVE]:
##   trend_period_hours: 48 → 50
##   All other params: Gen 2899 champion values.
##   Rationale: Slower trend filter may reduce false signals.
##   If improves: test 52. If that improves: test 54. Stop at first failure.
##   If fails: test 46 (opposite direction, one attempt only).
##
## P5 [SUSPENDED — do not test]:
##   rsi_long_threshold: 37.77 → 37.72
##   Reason: Sub-1% change on a parameter that has been stable since Gen 1477.
##   High contamination risk, negligible expected upside.
##   Do not resurrect unless all other P-items are exhausted.
##
## ─────────────────────────────────────────────────────────
## COMPOUND TESTING (only after at least two Px items independently resolve):
##   Rule: Never combine two untested changes.
##   Rule: Each compound test = exactly TWO confirmed improvements combined.
##   Rule: Compound tests require direct injection — no LLM.
##
##   Priority compound candidates (pending individual results):
##   C1: If P3-CONT + P4 both improve → test combined.
##   C2: If P7-STATUS + P4 both improve → test combined.
##   C3: If P2 + any Px improve → test P2+Px combined.
##   C4: If P3-CONT + P6 both improve → test combined.
##
## ─────────────────────────────────────────────────────────
## KNOWN FAILURE FINGERPRINTS (validator — auto-reject ALL of these):
##
## Attractor 1   [STALE CLONE]:  trades=1267, sharpe=2.2657 → Gen 1592 config used
## Attractor 1b  [GEN2785 CLONE]:trades=1272, sharpe=2.2828 → Gen 2785 clone
## Attractor 1c  [GEN2791 CLONE]:trades=1269, sharpe=2.2910 → Gen 2791 clone
## Attractor 1d  [GEN2813 CLONE]:trades=1268, sharpe=2.3055 → Gen 2813 clone
## Attractor 1e  [GEN2899 CLONE]:trades=1263, sharpe=2.3219 → Gen 2899 clone (nothing changed)
## Attractor 3   [RSI DRIFT]:    trades=1272, sharpe=2.2015 → RSI or param contaminated
## Attractor 4   [NEW — BROKEN]: trades=1041, sharpe=0.7753 → broken YAML (placeholder/invalid param)
## Ghost Echo    [TIMEOUT]:      trades=1264, sharpe=2.1998 → timeout=166h used
## Zombie C      [EXTREME]:      trades<400                 → RSI extreme or stop<1.88
## Zombie D      [SL=1.90]:      trades≈1228, sharpe≈1.59  → stop_loss=1.90 (NEVER use)
## Zombie G-adj  [TIMEOUT]:      trades≈888,  sharpe≈2.00  → timeout=155h used
##
## ATTRACTOR 4 DIAGNOSTIC:
##   New pattern observed 5 times in Gens 2882–2894: trades=1041, sharpe=0.7753.
##   Likely caused by: LLM receiving YAML with unresolved [GEN_2785_*] placeholder
##   text, producing an invalid parameter (e.g., rsi_period_hours=[GEN_2785_RSI_PERIOD]).
##   Fix: Ensure ALL placeholders are replaced with actual values before LLM prompt.
##   Auto-reject this fingerprint immediately. Root cause = prompt corruption.
##
## CLONE FINGERPRINT NOTE:
##   As champion improves, new Attractor 1x clones accumulate.
##   Any result exactly matching a prior champion's (trades, sharpe) = stale clone.
##   Validator should check against ALL historical champion fingerprints, not just latest.
##
## ─────────────────────────────────────────────────────────
## FROZEN PARAMETERS (hard-reject any YAML violating these):
##   size_pct       = 25         (FOREVER)
##   timeout_hours  = 159        (FOREVER — 155=ZombieG, 166=GhostEcho, 192=WRONG)
##   max_open       = 3          (FOREVER)
##   leverage       = 2          (FOREVER)
##   fee_rate       = 0.0005     (FOREVER)
##   stop_loss_pct  ≥ 1.88       (floor — below = ZombieC territory)
##   stop_loss_pct  ≠ 1.90       (FORBIDDEN — ZombieD)
##   rsi_long_threshold = 37.77  (do not touch — stable since Gen 1477)
##
##   ⚠ TIMEOUT WARNING: The displayed "current best" YAML shows timeout=192.
##   This is WRONG. timeout_hours=192 is NOT the champion value.
##   timeout_hours = 159 is the ONLY valid value (FROZEN).
##   Any YAML with timeout≠159 must be rejected immediately.
##
## ─────────────────────────────────────────────────────────
## LLM FAILURE RATE SUMMARY (operational awareness):
##   Clone rate (any Attractor 1x):  ~35% of LLM generations
##   Zombie rate (trades<400):        ~15% of LLM generations
##   Attractor 3/4 drift:             ~15% of LLM generations
##   Degraded/other:                  ~30% of LLM generations
##   Valid novel result:              ~5% of LLM generations
##   → Direct injection is MANDATORY for all P-items.
##   → LLM should only be used for exploratory/creative proposals.
##   → Sending placeholder text in LLM prompt produces Attractor 4. Fix prompts first.
##
## ─────────────────────────────────────────────────────────
## POST-P-ITEM RESOLUTION PATHS:
##   P3-CONT RESOLVED → Continue TP widening (+0.05 steps). Stop at first failure or TP≥5.50.
##   P3-CONT FAILED   → TP at current value is optimal. Do not test wider TP.
##   P4 RESOLVED      → Test one more step in same direction. Compound C1 or C2.
##   P4 FAILED        → RSI short threshold is at optimum. Close P4.
##   P7 RESOLVED      → Continue rsi_period reduction. Stop if trades>1,300 or noise emerges.
##   P7 FAILED        → rsi_period at optimum. Close P7.
##   P2 RESOLVED      → New champion with lower SL. Test 1.88 (absolute floor, one attempt).
##   P2 FAILED/CLOSED → SL stays at 1.91. Do not retry. Focus other P-items.
##   P6 RESOLVED      → Test trend_period+2. If fails: try trend_period-2 from champion.
##   P6 FAILED        → Test 46 (one attempt opposite direction), then close P6.
##
## ─────────────────────────────────────────────────────────
## MACRO NOTE (does NOT affect research YAML):
##   TYR: DANGER regime (F&G=15, Extreme Fear). Stable for 10+ consecutive readings.
##   Live sizing: 25% × 25% = 6.25% effective. Research size_pct stays 25.
##   No completed live sprints. Out-of-sample validation CRITICAL.
##   FRAGILITY WARNING: Parameter sensitivity remains extreme.
##     SL 1.90 vs 1.91 → sharpe collapse from 2.28 to 1.59 (ZombieD).
##     Treat all live deployment with maximum caution.
##   POSITIVE TREND: Four consecutive improvements (Gens 2785→2791→2813→2899).
##     Sharpe trajectory: 2.2828 → 2.2910 → 2.3055 → 2.3219.
##     The parallel P-item direct-injection strategy is working.
##     Maintain momentum — identify Gen 2899 change and continue that vector.
##   LIVE CONCERN: F&G=15 (Extreme Fear) sustained for 10+ readings.
##     Strategy was optimized on 2 years of mixed-regime data.
##     Current regime may produce different signal distributions.
##     Do not increase live sizing until at least one completed sprint is observed.
## ██████████████████████████████████████████████████████████

---
## ══════════════════════════════════════════════════════════
## LLM PROMPT — SEND ONLY THIS SECTION TO THE LLM
## Strip everything above and below. No exceptions.
## Use temperature=0.0 (minimum). No system prompt needed.
## ⚠ MANDATORY: Replace ALL [GEN_2899_*] tokens with actual numeric values
##   before sending. Do NOT send placeholder text. Attractor 4 is caused
##   by placeholder text reaching the LLM.
## ══════════════════════════════════════════════════════════

Make EXACTLY ONE change to the YAML below.

THE CHANGE: [TARGET_PARAM]: [CURRENT_VALUE]  →  [TARGET_PARAM]: [TARGET_VALUE]

Do not change any other line. Output only the complete modified YAML.

```yaml
name: crossover
style: swing_momentum
inspiration: "ODIN-injected champion — Gen 2899"
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
      period_hours: [GEN_2899_TREND_PERIOD]
      operator: eq
      value: up
    - indicator: rsi
      period_hours: [GEN_2899_RSI_PERIOD]
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: [GEN_2899_TREND_PERIOD]
      operator: eq
      value: down
    - indicator: rsi
      period_hours: [GEN_2899_RSI_PERIOD]
      operator: gt
      value: [GEN_2899_RSI_SHORT]
exit:
  take_profit_pct: [GEN_2899_TP]
  stop_loss_pct: [GEN_2899_SL]
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
6. All other params match Gen 2899 champion exactly ✅

## ══════════════════════════════════════════════════════════
## END OF LLM PROMPT
## ══════════════════════════════════════════════════════════

---
## CHAMPION SUMMARY (Gen 2899) — ODIN REFERENCE
## ⚠ SUPERSEDES ALL PRIOR CHAMPIONS. Do not use Gen 1592, 2785, 2791, or 2813 values.
## ⚠ YAML INTEGRITY ALERT: Displayed "current best" YAML has stop_loss=1.92
##   and timeout=192 — both are WRONG. Confirmed values: SL=1.91, timeout=159.
##   Retrieve actual Gen 2899 backtested YAML before proceeding.

- Sharpe: 2.3219 | Win rate: 39.9% | Trades: 1,263
- Entry: trend(48h?) + RSI(period=TBD) mean-reversion
  - Long:  trend=up   AND RSI < 37.77
  - Short: trend=down AND RSI > [TBD — confirm from actual YAML]
- Exit: TP=[TBD — confirm], SL=1.91 (confirm), timeout=159h (FROZEN)
- Sizing: 25% per position, max_open=3, 2x leverage
- R:R: approximately 2.4–2.6:1 (confirm from actual TP value)
- Risk guard: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR,
          APT, SUI, ARB, OP, ADA, POL)
- Live performance: no completed sprints (autobotswingfutures)
- Sensitivity: EXTREME — single-parameter changes of <0.01 can collapse Sharpe
- Improvement chain: 1.0218 (Gen 1) → 2.2496 (Gen 1477) → 2.2657 (Gen 1592)
                     → 2.2828 (Gen 2785) → 2.2910 (Gen 2791) → 2.3055 (Gen 2813)
                     → 2.3219 (Gen 2899)
- Active improvement vector: declining trades + improving Sharpe → likely TP widening
  or RSI threshold tightening. Confirm from YAML diff and continue that direction.
- ⚠ ALL [GEN_2899_*] PLACEHOLDERS MUST BE REPLACED before use in LLM prompt.
  Failure to replace = Attractor 4 (trades=1041, sharpe=0.7753).

## HISTORICAL CHAMPION FINGERPRINTS (for clone detection):
##   Gen 1592:  trades=1267, sharpe=2.2657  → Attractor 1  (reject)
##   Gen 2785:  trades=1272, sharpe=2.2828  → Attractor 1b (reject)
##   Gen 2791:  trades=1269, sharpe=2.2910  → Attractor 1c (reject)
##   Gen 2813:  trades=1268, sharpe=2.3055  → Attractor 1d (reject)
##   Gen 2899:  trades=1263, sharpe=2.3219  → Attractor 1e (reject if nothing changed)
##   Any result matching these exactly = LLM used stale champion YAML. Reject and re-inject.

DO NOT use any prior champion config as baseline. Gen 2899 is the ONLY active champion.
DO NOT use stop_loss_pct = 1.90 under any circumstances (ZombieD — confirmed lethal).
DO NOT use timeout_hours ≠ 159 under any circumstances (FROZEN).
DO NOT send LLM prompt with unresolved [GEN_2899_*] placeholder text.
DO NOT combine changes until individual improvements are confirmed independently.
```