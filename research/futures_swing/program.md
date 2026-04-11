```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-2600 | Revised by MIMIR (Gen 2600 review)
# STATUS: Champion FROZEN since Gen 1592. No improvement in 1,008 generations.
# CRISIS: P2 (stop_loss=1.89) unresolved after 800+ attempts. Moving to parallel
#         exploration. P2 retry continues but P3/P6/P7 now unlocked concurrently.

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
## MANDATORY EXECUTION PROTOCOL (MIMIR, Gen 2600):
##
## STEP 1 — DIRECT INJECTION (preferred):
##   Bypass the LLM entirely for all priority queue items.
##   Construct the YAML programmatically from champion + one parameter diff.
##   This eliminates clone/drift/zombie failure modes completely.
##   If direct injection is available, skip STEP 2.
##
## STEP 2 — LLM FALLBACK (only if direct injection unavailable):
##   Send the LLM ONLY the section marked "LLM PROMPT" below.
##   Strip ALL other sections from LLM input.
##   Use temperature=0.0 or minimum available for this task.
##   If Attractor 1 or Attractor 3 appears: reject, do NOT count as valid gen,
##   retry up to 3 times, then skip to next priority item.
##   After 3 consecutive Attractor outputs on same Px item: auto-advance to Px+1.
##
## STEP 3 — GRID SCAN FALLBACK (if LLM fails P2 repeatedly):
##   Run backtester directly on:
##     stop_loss_pct ∈ {1.88, 1.89, 1.90, 1.91} × all other params frozen
##   Accept best result as new champion if sharpe > 2.2657.
##   Note: 1.90 is ZombieD territory — expect ~1228 trades, ~1.59 sharpe.
##
## ─────────────────────────────────────────────────────────
## PRIORITY QUEUE (ODIN internal — NEVER send to LLM):
##
## P2 [ACTIVE, 800+ failed attempts]:
##   stop_loss_pct: 1.91 → 1.89
##   Rationale: Tighter stop, same R:R direction. Floor is 1.88 (below = ZombieC).
##   Expected: trades ~1267±20, sharpe unknown (never cleanly tested).
##   KNOWN HAZARD: 1.90 = ZombieD (trades≈1228, sharpe≈1.59). Skip 1.90.
##   If P2 improves (sharpe > 2.2657): new champion. Next test: stop_loss=1.88.
##   If P2 fails (sharpe ≤ 2.2657, trades ≥ 400): record result, move to P3.
##   If P2 Zombie (trades < 400): ZombieC confirmed. Move to P3.
##
## P3 [UNLOCKED — test in parallel with P2 retries]:
##   take_profit_pct: 4.65 → 4.70
##   stop_loss_pct stays: 1.91 (champion value, not 1.89)
##   Rationale: Wider TP, R:R = 4.70/1.91 = 2.46 ✅ (improves on 2.43)
##   Expected: trades may decrease slightly (harder to hit TP).
##   If improves: also test 4.75, 4.80 (stop at first failure).
##
## P4 [UNLOCKED]:
##   rsi_short_threshold: 60 → 59
##   All other params: champion values.
##   Rationale: Slightly more selective short entries.
##   Expected: trade count decrease ~30–50 trades, possible quality improvement.
##
## P6 [UNLOCKED]:
##   trend_period_hours: 48 → 50
##   All other params: champion values.
##   Rationale: Slower trend filter may reduce false signals.
##
## P7 [UNLOCKED]:
##   rsi_period_hours: 24 → 22
##   All other params: champion values.
##   Rationale: Faster RSI may increase trade frequency with fresher signals.
##   Risk: May push toward Attractor 3 territory — monitor trade count carefully.
##
## P5 [SUSPENDED — do not test]:
##   rsi_long_threshold: 37.77 → 37.72
##   Reason: Infinitesimally small change, high contamination risk, low upside.
##
## ─────────────────────────────────────────────────────────
## KNOWN FAILURE FINGERPRINTS (validator — auto-reject these):
##
## Attractor 1  [CLONE]:      trades=1267, sharpe=2.2657 → nothing changed
## Attractor 3  [RSI DRIFT]:  trades=1272, sharpe=2.2015 → RSI or param contaminated
## Ghost Echo   [TIMEOUT]:    trades=1264, sharpe=2.1998 → timeout=166h used
## Zombie C     [EXTREME]:    trades<400                 → RSI extreme or stop<1.88
## Zombie D     [SL=1.90]:    trades≈1228, sharpe≈1.59  → stop_loss=1.90 (never use)
## Zombie G-adj [TIMEOUT]:    trades≈888,  sharpe≈2.00  → timeout=155h used
##
## ATTRACTOR 3 DIAGNOSTIC NOTE:
##   Attractor 3 (1272 trades, 2.2015) appeared at Gen 2596–2597 despite
##   compressed prompt. This confirms the LLM is modifying RSI thresholds
##   even when instructed not to. The stop_loss change may be present in
##   these runs but contamination makes results invalid. Do not count as P2 test.
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
## POST-P2 RESOLUTION PATHS:
##   P2 IMPROVED → New champion. Test stop_loss=1.88 next (absolute floor).
##   P2 FAILED   → Champion SL stays 1.91. Pursue P3, P4, P6, P7 independently.
##   P2 ZOMBIE   → SL floor confirmed at 1.91. Pursue P3, P4, P6, P7.
##
## COMPOUND TESTING (only after at least one Px resolves):
##   If P3 improves AND P4 improves independently:
##     Test P3+P4 combined (take_profit=4.70, rsi_short=59).
##   Do not combine untested changes.
##
## ─────────────────────────────────────────────────────────
## MACRO NOTE (does NOT affect research YAML):
##   TYR: DANGER regime (F&G=16, Extreme Fear). Stable for 10+ readings.
##   Live sizing: 25% × 25% = 6.25% effective. Research size_pct stays 25.
##   No completed live sprints yet. Out-of-sample validation pending.
##   FRAGILITY WARNING: Parameter sensitivity is extremely high (SL 1.90 vs 1.91
##   produces sharpe 1.59 vs 2.27). Treat live deployment with caution until
##   at least one sprint completes.
## ██████████████████████████████████████████████████████████

---
## ══════════════════════════════════════════════════════════
## LLM PROMPT — SEND ONLY THIS SECTION TO THE LLM
## Strip everything above and below. No exceptions.
## Use temperature=0.0 (minimum). No system prompt needed.
## ══════════════════════════════════════════════════════════

Make EXACTLY ONE change to the YAML below.

THE CHANGE: stop_loss_pct: 1.91  →  stop_loss_pct: 1.89

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
      period_hours: 24
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24
      operator: gt
      value: 60
exit:
  take_profit_pct: 4.65
  stop_loss_pct: 1.91
  timeout_hours: 159
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

Verify before submitting:
1. stop_loss_pct = 1.89 ✅
2. timeout_hours = 159 ✅
3. take_profit_pct = 4.65 ✅
4. rsi long value = 37.77 ✅
5. rsi short value = 60 ✅
6. period_hours (trend) = 48 ✅
7. period_hours (rsi) = 24 ✅

## ══════════════════════════════════════════════════════════
## END OF LLM PROMPT
## ══════════════════════════════════════════════════════════

---
## CHAMPION SUMMARY (Gen 1592) — ODIN REFERENCE

- Sharpe: 2.2657 | Win rate: 39.9% | Trades: 1,267
- Entry: trend(48h) + RSI(24h) mean-reversion
  - Long:  trend=up   AND RSI(24h) < 37.77
  - Short: trend=down AND RSI(24h) > 60
- Exit: TP=4.65%, SL=1.91%, timeout=159h
- Sizing: 25% per position, max_open=3, 2x leverage
- R:R: 4.65/1.91 = 2.43:1
- Risk guard: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR,
          APT, SUI, ARB, OP, ADA, POL)
- Live performance: no completed sprints (autobotswingfutures)
- Sensitivity: EXTREME — SL 1.90 collapses sharpe to 1.59 (ZombieD)

## STALL DIAGNOSIS (MIMIR, Gen 2600):
- 1,008 generations without improvement (since Gen 1592)
- P2 failure rate: ~100% over 800+ attempts (clone, drift, or zombie)
- Root cause: LLM cannot reliably make surgical single-parameter edits
- Resolution path: Direct backtester injection (bypass LLM for P2)
- Fallback: Grid scan SL ∈ {1.88, 1.89} with all other params frozen
- Parallel tracks P3/P4/P6/P7 now active to break optimization stall

DO NOT reproduce previous champions. Only Gen 1592 config is active.
DO NOT use stop_loss_pct = 1.90 under any circumstances (ZombieD).
```