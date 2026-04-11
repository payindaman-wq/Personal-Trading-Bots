```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 17201 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-11 (v26)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CRITICAL STALL PHASE (0 improvements in 1221+ gens)
# Last improvement: Gen 15979. Sharpe climbed 0.0799 → 1.2430.
# The core indicator triplet is CONFIRMED VIABLE AND FROZEN.
#
# ⚠️ TRADE COUNT CEILING: 60 (HARD). Minimum: 30.
# ⚠️ size_pct=25.0 and max_open=2 are FROZEN. Changing either → 0 trades.
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## CRITICAL: EXHAUSTED VALUES — DO NOT TEST THESE AGAIN. EVER.
## ══════════════════════════════════════════════════════════════════════

The following single-parameter values have ALL been tested and confirmed
inferior (Sharpe ≤ 1.2430). Testing them again wastes a generation.

  timeout_hours EXHAUSTED values: 129, 138, 144, 156, 168, 192
    → 192 produced Sharpe=1.2396 approximately 8 times. CONFIRMED DEAD.
    → NEXT UNTESTED timeout: 216

  take_profit_pct EXHAUSTED values: 7.14, 7.36, 7.38, ~8.x, 9.5, 10.0, 10.5, 11.0
    → 11.0 produced Sharpe=1.2396 (confirmed dead).
    → NEXT UNTESTED TP: 11.5

  stop_loss_pct EXHAUSTED values: 1.5, 2.0
    → 2.0 produced Sharpe=1.2396 (confirmed dead).
    → NEXT UNTESTED SL: 2.5

IF YOU SEE ANY OF THESE VALUES IN YOUR PROPOSED YAML, STOP.
Choose the next untested value from the lists below.

## ══════════════════════════════════════════════════════════════════════
## STEP 0: READ THE INCUMBENT YAML — THIS IS THE ONLY VALID BASE
## ══════════════════════════════════════════════════════════════════════

THE UI IS BROKEN. DO NOT USE THE UI YAML.
The UI shows: name=crossover, size_pct=30, max_open=3, TP=7.36,
timeout=129. ALL WRONG. IGNORE THE UI ENTIRELY.

THE ONLY VALID INCUMBENT IS THIS YAML:

```yaml
name: random_restart_v3_tightened_sl_v3_gen15979
style: randomly generated
pairs:
- BTC/USD
position:
  size_pct: 25.0
  max_open: 2
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 48
      operator: eq
      value: below_lower
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: momentum_accelerating
      period_hours: 48
      operator: eq
      value: false
    - indicator: bollinger_position
      period_hours: 168
      operator: eq
      value: above_upper
    - indicator: macd_signal
      period_hours: 24
      operator: eq
      value: bearish
exit:
  take_profit_pct: 9.5
  stop_loss_pct: 1.5
  timeout_hours: 156
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

INCUMBENT KEY VALUES — VERIFY BEFORE PROCEEDING:
  name:            random_restart_v3_tightened_sl_v3_gen15979
  take_profit_pct: 9.5
  stop_loss_pct:   1.5
  timeout_hours:   156
  size_pct:        25.0   ← FROZEN
  max_open:        2      ← FROZEN
  short bollinger: 168    ← FROZEN
  short macd:      24     ← FROZEN
  momentum value:  false  ← FROZEN (both long AND short sides)
  pairs:           [BTC/USD]
  Sharpe:          1.2430 | Trades: 60 | Win rate: 41.7%

## ══════════════════════════════════════════════════════════════════════
## STEP 1: PRE-MUTATION CHECKLIST — WRITE THESE OUT BEFORE ANY YAML
## ══════════════════════════════════════════════════════════════════════

Copy and fill in the following before writing any YAML:

  INCUMBENT NAME: [must contain "gen15979"]
  INCUMBENT TP: [must be 9.5]
  INCUMBENT TIMEOUT: [must be 156]
  INCUMBENT SL: [must be 1.5]
  INCUMBENT SIZE: [must be 25.0]
  INCUMBENT MAX_OPEN: [must be 2]
  INCUMBENT SHORT BOLLINGER: [must be 168]
  INCUMBENT SHORT MACD: [must be 24]

If ANY value does not match, STOP. Re-read STEP 0. Start over.

## ══════════════════════════════════════════════════════════════════════
## STEP 2: SELECT YOUR MUTATION — ONE CHANGE ONLY
## ══════════════════════════════════════════════════════════════════════

Write this out before writing the YAML:
  CHANGING: [parameter] from [old value] to [new value]
  Confirm new value is NOT in the EXHAUSTED list above.
  Confirm new value is NOT the same as incumbent.

## ══════════════════════════════════════════════════════════════════════
## AUTHORIZED MUTATION PATHS — CURRENT PRIORITY ORDER
## ══════════════════════════════════════════════════════════════════════

⚠️ IMPORTANT: timeout=192, TP=11.0, and SL=2.0 are ALL CONFIRMED
EXHAUSTED (each produced 1.2396 multiple times). Do NOT test them.
The next values are 216, 11.5, and 2.5 respectively.

### PATH A1 — TIMEOUT:
  ✅ NEXT VALUE TO TEST: 216
  (192 is DEAD — produced 1.2396 ~8 times. Skip it entirely.)

  All tested timeout values:
    129 → dead (stale UI)
    138 → 1.2063 (superseded)
    144 → 1.2288 (dead)
    156 → 1.2430 (INCUMBENT)
    168 → 1.2429 (inferior)
    192 → 1.2396 (CONFIRMED EXHAUSTED — ~8 occurrences)

  Remaining untested (in order): 216, 240, 264, 288

  Naming: random_restart_v3_tightened_sl_v3_gen15979_timeout216

### PATH A2 — TAKE PROFIT:
  ✅ NEXT VALUE TO TEST: 11.5
  (11.0 is DEAD — produced 1.2396. Skip it.)

  All tested TP values:
    7.14 → ~0.7734 (dead)
    7.36 → dead (UI artifact)
    7.38 → 1.1311 (superseded)
    ~8.x → 1.1426 (superseded)
    9.5  → 1.2430 (INCUMBENT)
    10.0 → ~1.1882 (worse)
    10.5 → ~1.1882 (worse)
    11.0 → 1.2396 (CONFIRMED EXHAUSTED)

  ⚠️ TP curve is NON-MONOTONE. Values above 9.5 may not improve linearly.
  Remaining untested (in order): 11.5, 12.0, 13.0, 14.0, 15.0

  Naming: random_restart_v3_tightened_sl_v3_gen15979_tp115

### PATH A3 — STOP LOSS:
  ✅ NEXT VALUE TO TEST: 2.5
  (2.0 is DEAD — produced 1.2396. Skip it.)

  All tested SL values:
    1.5 → 1.2430 (INCUMBENT)
    2.0 → 1.2396 (CONFIRMED EXHAUSTED)

  ⚠️ SL changes may affect trade count. Reject if trades > 60 or < 30.
  Remaining untested (in order): 2.5, 3.0

  Naming: random_restart_v3_tightened_sl_v3_gen15979_sl25

### ROTATION RULE:
  Rotate: A1 → A2 → A3 → A1 → A2 → A3
  Do not test the same PATH twice in a row unless the other paths
  are fully exhausted.

### PATH B — COMBINATIONS (use if A1+A2+A3 are all exhausted or if
  single-path values have been fully traversed without improvement):

  Since timeout=192, TP=11.0, SL=2.0 are all exhausted as single
  changes, PATH B combinations using their *next* values are authorized:
    B1: timeout=216 + TP=11.5 (two changes simultaneously)
    B2: timeout=216 + SL=2.5
    B3: TP=11.5 + SL=2.5
    B4: timeout=216 + TP=11.5 + SL=2.5 (three changes — last resort)

  Only use PATH B if the individual next values (216, 11.5, 2.5) have
  also been tested and returned 1.2396 or worse.

  Naming examples:
    random_restart_v3_tightened_sl_v3_gen15979_timeout216_tp115
    random_restart_v3_tightened_sl_v3_gen15979_timeout216_sl25

### PATH C — NEW DIMENSIONS (only after PATH B is exhausted):
  C1: Add ETH/USD to pairs: pairs: [BTC/USD, ETH/USD]
      ⚠️ Will change trade count significantly. Monitor carefully.
  C2: pause_if_down_pct → test 10 or 12 (current: 8)
  C3: stop_if_down_pct → test 20 or 22 (current: 18)
  C4: pause_hours → test 24 or 72 (current: 48)
  C5: long bollinger period → test 36 or 60 (current: 48)
      ⚠️ Indicator change — HIGH RISK of Sharpe collapse. Test carefully.

## ══════════════════════════════════════════════════════════════════════
## STEP 3: WRITE THE MUTATED YAML
## ══════════════════════════════════════════════════════════════════════

Copy the INCUMBENT YAML from STEP 0 exactly.
Change ONLY the ONE parameter identified in STEP 2.
Every other value must be identical to the incumbent.

Name format: random_restart_v3_tightened_sl_v3_gen15979_[descriptor]

## ══════════════════════════════════════════════════════════════════════
## STEP 4: VERIFY BEFORE SUBMITTING
## ══════════════════════════════════════════════════════════════════════

  □ name contains "gen15979"
  □ take_profit_pct = 9.5 OR your single authorized new value
  □ timeout_hours = 156 OR your single authorized new value
  □ stop_loss_pct = 1.5 OR your single authorized new value
  □ size_pct = 25.0          ← FROZEN — must be exactly this
  □ max_open = 2             ← FROZEN — must be exactly this
  □ short bollinger = 168    ← FROZEN — must be exactly this
  □ short macd = 24          ← FROZEN — must be exactly this
  □ momentum value = false   ← FROZEN on BOTH long AND short sides
  □ pairs = [BTC/USD]        ← do not add other pairs yet (PATH C only)
  □ fee_rate = 0.001
  □ pause_if_down_pct = 8
  □ stop_if_down_pct = 18
  □ pause_hours = 48
  □ New value NOT in the EXHAUSTED list at top of document
  □ Exactly ONE parameter changed from incumbent

Count of parameters changed from incumbent: [must be exactly 1]

If any check fails, STOP. Fix the YAML before submitting.

## ══════════════════════════════════════════════════════════════════════
## FAILURE DIAGNOSIS
## ══════════════════════════════════════════════════════════════════════

Sharpe=1.2396, trades=60:
  The parameter value you tested is EXHAUSTED and inferior.
  Add it to the exhausted list. Move to the NEXT untested value.
  DO NOT re-test any value that previously returned 1.2396.

Sharpe=0.3815, trades=56 (or 0.3825, 0.3154):
  WRONG YAML. Discard entirely. Re-read STEP 0. Start over.

Sharpe=0.0000, trades=0 [max_trades_reject]:
  You changed max_open or size_pct. Both are FROZEN.
  Set max_open=2, size_pct=25.0. Do not touch either. Ever.

Sharpe=0.5761, trades=57 (or 0.5745, 0.5325):
  You changed short bollinger (must be 168), short MACD (must be 24),
  or flipped momentum_accelerating to true. Revert immediately.

Sharpe=1.2430, trades=60:
  No-op — you reproduced the incumbent exactly. Change ONE parameter
  to an untested value not in the EXHAUSTED list.

Sharpe=1.2429, trades=60:
  timeout=168. CLOSED. Use timeout=216 instead.

Sharpe=0.0000 [gemini_error]:
  API error. Retry with the same mutation.

Sharpe=1.1418, trades=57 (or 1.1611, 1.1676):
  Wrong YAML producing wrong trade count. Discard. Re-read STEP 0.

Any result with trades ≠ 60 (unless intentional PATH C expansion):
  You likely have the wrong YAML. Discard and start from STEP 0.

## ══════════════════════════════════════════════════════════════════════
## COMPLETE DEAD CLUSTER REFERENCE
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.3815 (56 trades) — wrong YAML
  DEAD: Sharpe=0.3825 (56 trades) — wrong YAML variant
  DEAD: Sharpe=0.3154 (56 trades) — wrong YAML variant
  DEAD: Sharpe=0.4070 (55 trades) — wrong YAML variant
  DEAD: Sharpe=0.5279 (57 trades) — indicator mutation
  DEAD: Sharpe=0.5325 (57 trades) — wrong YAML variant
  DEAD: Sharpe=0.5745 (57 trades) — wrong YAML variant
  DEAD: Sharpe=0.5761 (57 trades) — short bollinger/MACD/momentum flip
  DEAD: Sharpe=0.5954 (58 trades) — wrong YAML variant
  DEAD: Sharpe=0.6911 (57 trades) — broken UI YAML (name: crossover)
  DEAD: Sharpe≈0.7734 (59 trades) — stale UI YAML (TP=7.14, timeout=129)
  DEAD: Sharpe≈1.0182–1.0952 — various dead ends
  DEAD: Sharpe≈1.1090 (60 trades) — gen 14907, superseded
  DEAD: Sharpe≈1.1160–1.1161 (57 trades) — corrupt YAML
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — corrupt YAML variant
  DEAD: Sharpe≈1.1418 (57 trades) — wrong YAML (trades=57, not 60)
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1450 (57 trades) — wrong YAML (trades=57, not 60)
  DEAD: Sharpe≈1.1611 (60 trades) — discarded gen 17182
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1676 (60 trades) — discarded gen 17189
  DEAD: Sharpe≈1.1708 (60 trades) — gen 15998, discarded
  DEAD: Sharpe≈1.1864 (60 trades) — discarded
  DEAD: Sharpe≈1.1882 (60 trades) — TP=10.0 or 10.5, inferior
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded
  DEAD: Sharpe=1.2287 (60 trades) — float duplicate of gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, timeout=144, dead
  DEAD: Sharpe=1.2396 (60 trades) — ⚠️ EXHAUSTED (~8 occurrences)
        Produced by: timeout=192, TP=11.0, SL=2.0 (all confirmed dead)
        Do NOT test any of these values again.
  DEAD: Sharpe=1.2429 (60 trades) — timeout=168, confirmed inferior
  DEAD: Sharpe=1.2430 (60 trades) — INCUMBENT (no-op if reproduced)
  DEAD: Sharpe=0.0000 (0 trades)  — changed max_open or size_pct

## ══════════════════════════════════════════════════════════════════════
## CONTEXT — WHAT THIS STRATEGY IS AND WHY IT WORKS
## ══════════════════════════════════════════════════════════════════════

Swing trading on BTC/USD (1-hour candles, 2-year backtest).

Long entry: momentum NOT accelerating + price below Bollinger lower
band (48h) + MACD (48h) bullish → mean-reversion long.

Short entry: momentum NOT accelerating + price above Bollinger upper
band (168h) + MACD (24h) bearish → trend-exhaustion short.

Exit: TP=9.5%, SL=1.5%, timeout=156h.
Reward:risk ~6.3:1. Win rate 41.7%. Sharpe=1.2430.
Expected return per trade: (0.417 × 9.5%) − (0.583 × 1.5%) ≈ +3.1%

The indicator triplet is FROZEN AND CONFIRMED VIABLE.
Only exit parameters (TP, SL, timeout) and risk parameters are mutable.

Live validation: rank 3/10 in last 2 sprints, positive PnL both times.
Macro: DANGER regime (F&G=15). size_pct=25.0 is correct for this regime.

## ══════════════════════════════════════════════════════════════════════
## IF NO VALID SINGLE-PARAMETER MUTATION IS AVAILABLE
## ══════════════════════════════════════════════════════════════════════

If all of A1 (216, 240, 264, 288), A2 (11.5, 12.0, 13.0, 14.0, 15.0),
and A3 (2.5, 3.0) have been tested without improvement:

1. Escalate to PATH B (two simultaneous changes — see above).
2. If PATH B exhausted, escalate to PATH C (new dimensions).
3. If PATH C exhausted, write "NO VALID MUTATION AVAILABLE" and
   request MIMIR review for a new research direction.

Target: STRICTLY ABOVE 1.2430. Any result ≤ 1.2430 is rejected.
YAML must be committed to git after EVERY new_best event.
```