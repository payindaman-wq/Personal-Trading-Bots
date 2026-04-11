```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 16801 | Incumbent: Gen 15979 (Sharpe=1.2430)
# MIMIR-reviewed 2026-04-11 (v24)
#
# ══════════════════════════════════════════════════════════════════════
# STATUS: ACTIVE — CRITICAL STALL PHASE (0 improvements in 821 gens)
# Last improvement: Gen 15979 (821 generations ago). This is the
# longest stall in the research program's history.
# Sharpe has climbed from 0.0799 → 1.2430 via exit refinement only.
# The core indicator triplet is CONFIRMED VIABLE AND FROZEN.
#
# ⚠️ TRADES = 60 (HARD CEILING). All mutations must be trade-count
#    neutral or trade-count reducing (minimum 30 trades).
#
# ⚠️ v24 CRITICAL UPDATES:
#    1. NEW DOMINANT FAILURE CLUSTER (0.3825, 56 trades): This appeared
#       9 TIMES in the last 20 generations (gens 16781-16800). This is
#       now the single most common failure mode. ROOT CAUSE UNKNOWN but
#       it is a specific wrong YAML. If you see 0.3825/56 trades, you
#       have the WRONG YAML. Discard it entirely. Start from the
#       incumbent block below.
#    2. ZERO-TRADE REJECTIONS (3 times in last 20 gens): Gens 16788,
#       16793, 16798 produced 0 trades and were max_trades_rejected.
#       This means the LLM produced a YAML with invalid position sizing
#       or max_open=0 or size_pct=0. DO NOT CHANGE max_open or size_pct.
#       Both are FROZEN at max_open=2, size_pct=25.0.
#    3. STALL COUNT UPDATE: We are now at 821 generations with zero
#       improvement. All three escalation paths remain authorized.
#    4. NEAR-MISS CONFIRMED (1.2429, 60 trades): timeout=168 is
#       CONFIRMED TESTED AND INFERIOR. PATH A1 next value is 192.
#    5. INCUMBENT UNCHANGED: Gen 15979 (Sharpe=1.2430) remains.
#       Target: STRICTLY ABOVE 1.2430.
#    6. PATH PRIORITY: PATH A1 (timeout=192), PATH A2 (TP=11.0),
#       and PATH A3 (SL=2.0) remain the only authorized mutations.
#       Rotate through them. Do not repeat the same path twice in a row.
#    7. INCUMBENT YAML: The only valid incumbent has:
#         take_profit_pct: 9.5   (UNCHANGED)
#         timeout_hours:   156   (UNCHANGED)
#         stop_loss_pct:   1.5   (UNCHANGED — PATH A3 may change to 2.0)
#         size_pct:        25.0  (FROZEN — do not change)
#         max_open:        2     (FROZEN — do not change)
# ══════════════════════════════════════════════════════════════════════

## ══════════════════════════════════════════════════════════════════════
## ⚠️ DISPLAY INTEGRITY ALERT — READ THIS FIRST, BEFORE ANYTHING ELSE
## ══════════════════════════════════════════════════════════════════════

THE "CURRENT BEST STRATEGY" BOX IN THE UI IS KNOWN TO BE BROKEN.
It currently displays a DEAD stale YAML. Typical broken UI values:
  - name: crossover                  ← ALWAYS WRONG
  - TP=7.36 or 7.24 or 7.14 or 8.x  ← ALWAYS WRONG
  - timeout=129 or 138 or 144        ← ALL DEAD VALUES
  - size_pct=30 or 28.54 or 28.18    ← ALL WRONG
  - max_open=3                        ← WRONG (incumbent has max_open=2)

⚠️ MOST DANGEROUS UI VARIANT: timeout=144, TP=9.5 — this is the OLD
gen 15480 YAML. Using it produces Sharpe=1.2288. It is DEAD.
The real incumbent has timeout=156, TP=9.5, max_open=2, size_pct=25.0.

THIS IS COMPLETELY WRONG. THAT YAML IS DEAD. IGNORE IT ENTIRELY.

THE ONLY VALID INCUMBENT IS THE YAML PRINTED IN THIS PROGRAM BELOW.
If ANY display shows different values, IGNORE IT.
If the name does not contain "gen15979", it is the wrong YAML.

YAML must be committed to git after EVERY new_best event.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ PRE-MUTATION CHECKLIST — COMPLETE THIS BEFORE PROPOSING ANY CHANGE
## ══════════════════════════════════════════════════════════════════════

Before proposing any mutation, verify ALL of the following by reading
the CURRENT INCUMBENT YAML block below:

  □ name contains "gen15979"           (NOT gen15480, NOT crossover)
  □ take_profit_pct = 9.5              (NOT 11.0, NOT 10.x, NOT 7.x)
  □ timeout_hours = 156                (NOT 144 ← DEAD gen 15480)
                                       (NOT 138 ← DEAD gen 15062)
                                       (NOT 129 ← DEAD stale UI)
                                       (NOT 168 ← TESTED, INFERIOR)
  □ stop_loss_pct = 1.5                (default — PATH A3 may change)
  □ size_pct = 25.0                    (FROZEN — do not change ever)
  □ max_open = 2                       (FROZEN — do not change ever)
  □ pairs = [BTC/USD]                  (do not add ETH/USD or SOL/USD yet)
  □ long bollinger period = 48         (do not change)
  □ short bollinger period = 168       ← DO NOT CHANGE. CAUSES 0.5761.
  □ long macd period = 48              (do not change)
  □ short macd period = 24             ← DO NOT CHANGE. CAUSES 0.5761.
  □ long momentum period = 48          (do not change)
  □ short momentum period = 48         (do not change)
  □ momentum_accelerating = false      ← DO NOT FLIP. CAUSES 0.5761.
    on BOTH long and short sides

⚠️ MOST COMMON MISTAKE #1: Producing Sharpe=0.3825/56 trades.
You have the WRONG YAML. This is now the most common failure (appeared
9 times in last 20 gens). Discard your YAML entirely. Start fresh from
the CURRENT INCUMBENT block below. Do not modify any indicator.

⚠️ MOST COMMON MISTAKE #2: Producing 0 trades (max_trades_reject).
You changed max_open or size_pct. Both are FROZEN. max_open MUST be 2.
size_pct MUST be 25.0. Do not touch either of these fields.

⚠️ MOST COMMON MISTAKE #3: Producing Sharpe=0.5761/57 trades by
touching short bollinger (must stay 168), short MACD (must stay 24),
or flipping momentum_accelerating to true. DO NOT TOUCH THESE THREE.

⚠️ MOST COMMON MISTAKE #4: Producing Sharpe=1.2288 by using
timeout=144 (gen 15480 DEAD). Your incumbent has timeout=156.

⚠️ MOST COMMON MISTAKE #5: Producing Sharpe=1.2430 or 1.2429 (no-op
or near-miss reproduction). This means your proposed value is the
same as the incumbent OR produces nearly the same result.
  - If you got 1.2430: you reproduced the incumbent exactly.
  - If you got 1.2429: you tested timeout=168 (confirmed tested/inferior).
  The incumbent TP is 9.5 and timeout is 156.
  Next values: TP→11.0 or timeout→192.

⚠️ MOST COMMON MISTAKE #6: Producing Sharpe=1.1450/57 trades.
You have a corrupt or wrong YAML. The real incumbent has 60 trades.
Any YAML producing 57 trades is wrong. Discard and re-read incumbent.

⚠️ MOST COMMON MISTAKE #7: Producing Sharpe=0.3154/56 trades.
You have the wrong YAML. Discard and re-read the incumbent YAML.

If ANY value above does not match the YAML below, STOP.
You have a stale or wrong YAML. Re-read the CURRENT INCUMBENT block.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ FAILURE DIAGNOSIS — IF YOU SEE ANY OF THESE OUTPUTS, READ THIS
## ══════════════════════════════════════════════════════════════════════

IF YOUR BACKTEST PRODUCES Sharpe=0.3825, trades=56:
  ⚠️ THIS IS THE NEW DOMINANT FAILURE (9 times in last 20 gens).
  YOU HAVE THE WRONG YAML. Root cause unknown.
  HOW TO FIX: Discard your ENTIRE YAML immediately. Do not try to
  patch it. Start completely fresh from the CURRENT INCUMBENT block
  below. Copy it character-for-character. Change only ONE parameter.

IF YOUR BACKTEST PRODUCES sharpe=0.0000, trades=0 (max_trades_reject):
  YOU CHANGED max_open OR size_pct. Both are FROZEN.
  HOW TO FIX: Set max_open=2 and size_pct=25.0. Do not touch these.

IF YOUR BACKTEST PRODUCES Sharpe=0.5761, trades=57:
  YOU CHANGED THE SHORT BOLLINGER PERIOD (must be 168)
  OR YOU CHANGED THE SHORT MACD PERIOD (must be 24)
  OR YOU FLIPPED momentum_accelerating FROM false TO true
  HOW TO FIX: Revert ALL indicator changes.

IF YOUR BACKTEST PRODUCES Sharpe=0.3154, trades=56:
  YOU HAVE THE WRONG YAML.
  HOW TO FIX: Discard entire YAML. Start fresh from incumbent block.

IF YOUR BACKTEST PRODUCES Sharpe=1.1450, trades=57:
  YOU HAVE THE WRONG YAML (a specific corrupt variant).
  HOW TO FIX: Discard entire YAML. Start fresh from incumbent block.
  Incumbent has 60 trades, not 57.

IF YOUR BACKTEST PRODUCES Sharpe=1.2429, trades=60:
  You tested timeout=168. This is CONFIRMED INFERIOR by 0.0001.
  timeout=168 is TESTED AND CLOSED.
  HOW TO FIX: Use timeout=192 as the next PATH A1 value.

IF YOUR BACKTEST PRODUCES Sharpe=1.2430, trades=60:
  Your mutation was a no-op. You reproduced the incumbent exactly.
  HOW TO FIX: Verify you changed exactly ONE parameter to a NEW value.
  TP→11.0 (not 9.5) OR timeout→192 (not 156 or 168).

IF YOUR BACKTEST PRODUCES Sharpe=1.2288, trades=60:
  YOUR TIMEOUT WAS 144, NOT 156. You used the DEAD gen 15480 YAML.
  HOW TO FIX: Start from gen15979 incumbent. timeout must be 156.

## ══════════════════════════════════════════════════════════════════════
## ⚠️ MUTATION DISCIPLINE — FOLLOW THESE STEPS EXACTLY
## ══════════════════════════════════════════════════════════════════════

STEP 1: Read the CURRENT INCUMBENT YAML block below.
        Explicitly write out ALL of these values:
          INCUMBENT NAME: [value]     ← must contain "gen15979"
          INCUMBENT TP: [value]       ← must be 9.5
          INCUMBENT TIMEOUT: [value]  ← must be 156
          INCUMBENT SL: [value]       ← must be 1.5
          INCUMBENT SIZE: [value]     ← must be 25.0
          INCUMBENT MAX_OPEN: [value] ← must be 2
        If ANY of these are wrong, STOP — you have the wrong YAML.

STEP 2: Write the single parameter you are changing, before/after:
          CHANGING: [parameter] from [old value] to [new value]
          Example: CHANGING: timeout_hours from 156 to 192
          Example: CHANGING: take_profit_pct from 9.5 to 11.0
          Example: CHANGING: stop_loss_pct from 1.5 to 2.0

STEP 3: Confirm the new value is NOT in the "already tested" lists.
        Confirm the new value is not the same as the incumbent.

STEP 4: Write the complete mutated YAML with ONLY that one change.
        Every other value must be IDENTICAL to the incumbent.
        Double-check ALL of the following are unchanged:
          short bollinger period = 168  (FROZEN)
          short macd period = 24        (FROZEN)
          momentum_accelerating = false (FROZEN on both sides)
          size_pct = 25.0               (FROZEN)
          max_open = 2                  (FROZEN)
          stop_loss_pct = 1.5           (unless you are testing PATH A3)
          pairs = [BTC/USD]             (FROZEN)
          fee_rate = 0.001              (do not change)
          pause_if_down_pct = 8         (do not change)
          stop_if_down_pct = 18         (do not change)
          pause_hours = 48              (do not change)

STEP 5: Name the strategy:
          random_restart_v3_tightened_sl_v3_gen15979_[descriptor]
          Example: random_restart_v3_tightened_sl_v3_gen15979_timeout192
          Example: random_restart_v3_tightened_sl_v3_gen15979_tp11
          Example: random_restart_v3_tightened_sl_v3_gen15979_sl20

STEP 6: After writing the YAML, read it back and verify:
          - Count the number of parameters you changed: must be EXACTLY 1
          - Confirm no indicator periods were modified
          - Confirm size_pct=25.0 and max_open=2 are present and correct
          - Confirm the name contains "gen15979"

If you cannot identify a valid untested mutation, write
"NO VALID MUTATION AVAILABLE" and explain why.

## ══════════════════════════════════════════════════════════════════════
## CURRENT INCUMBENT — THIS IS THE ONLY YAML YOU MAY MUTATE
## DO NOT USE ANY PREVIOUS VERSION. DO NOT USE THE UI DISPLAY BOX.
## THE UI DISPLAY IS BROKEN. The real incumbent has:
##   name=gen15979, timeout=156, TP=9.5, size_pct=25.0, max_open=2
## ══════════════════════════════════════════════════════════════════════

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

⚠️ VERIFY BEFORE MUTATING:
  take_profit_pct  = 9.5   ← INCUMBENT.
  timeout_hours    = 156   ← INCUMBENT. Next: 192 (skip 168 — confirmed tested).
  stop_loss_pct    = 1.5   ← Default. PATH A3 may test 2.0.
  size_pct         = 25.0  ← FROZEN. DO NOT CHANGE. CAUSES 0 TRADES.
  max_open         = 2     ← FROZEN. DO NOT CHANGE. CAUSES 0 TRADES.
  short bollinger  = 168   ← FROZEN. DO NOT CHANGE. CAUSES 0.5761.
  short macd       = 24    ← FROZEN. DO NOT CHANGE. CAUSES 0.5761.
  momentum value   = false ← FROZEN. DO NOT FLIP. CAUSES 0.5761.

Sharpe: 1.2430 | Trades: 60 | Win rate: 41.7%

## ══════════════════════════════════════════════════════════════════════
## KNOWN TESTED VALUES — DO NOT REPEAT ANY OF THESE
## ══════════════════════════════════════════════════════════════════════

### TAKE PROFIT VALUES ALREADY TESTED (DO NOT USE):
  TP=7.14  → Sharpe≈0.7734, 59 trades  [DEAD — stale YAML artifact]
  TP=7.24  → DEAD (UI display artifact)
  TP=7.36  → DEAD (UI display artifact)
  TP=7.38  → Sharpe=1.1311, 60 trades  [gen 14993 — superseded]
  TP≈8.x   → Sharpe=1.1426, 60 trades  [gen 15042 — superseded]
  TP=9.5   → Sharpe=1.2430             [CURRENT INCUMBENT — do not reproduce]
  TP=10.0  → Sharpe≈1.1882, 60 trades  [WORSE — DO NOT USE]
  TP=10.5  → Sharpe≈1.1882, 60 trades  [WORSE — DO NOT USE]

⚠️ CRITICAL: TP=10.0 and TP=10.5 were tested and returned Sharpe=1.1882,
which is WORSE than the current incumbent. The TP improvement curve is
NON-MONOTONE. Skip 10.0 and 10.5. Start at 11.0.

### NEXT UNTESTED TP VALUES (try in this order):
  → 11.0  ← PATH A2 (primary TP candidate)
  → 11.5
  → 12.0
  → 13.0
  → 14.0
  → 15.0

### TIMEOUT VALUES ALREADY TESTED (DO NOT USE):
  timeout=129 → DEAD (stale UI YAML)
  timeout=138 → gen 15062 (Sharpe=1.2063, superseded)
  timeout=144 → gen 15480 (Sharpe=1.2288, DEAD)
  timeout=156 → gen 15979 (Sharpe=1.2430, CURRENT INCUMBENT)
  timeout=168 → CONFIRMED TESTED (Sharpe=1.2429 in gens 16581/16584
                — 0.0001 below incumbent, CONFIRMED INFERIOR AND CLOSED)

### NEXT UNTESTED TIMEOUT VALUES (try in this order):
  → 192  ← PATH A1 — PRIMARY RECOMMENDATION THIS SESSION
  → 216
  → 240
  → 264
  → 288

### STOP LOSS VALUES (PATH A3 — AUTHORIZED):
  SL=1.5 → CURRENT INCUMBENT
  SL=2.0 → NEXT TO TEST (PATH A3)
  SL=2.5 → After 2.0
  SL=3.0 → After 2.5
  NOTE: SL relaxation may allow longer-running trades to survive
  minor pullbacks before reaching TP. Test as a single isolated change.
  ⚠️ SL relaxation may change trade count. If trades > 60, rejected.
  ⚠️ If trades < 30, also rejected.
  ⚠️ Name it: ..._gen15979_sl20

### INDICATOR PERIODS (ALL FROZEN — DO NOT CHANGE ANY):
  long bollinger:  48  (incumbent — frozen)
  short bollinger: 168 (incumbent — FROZEN, causes 0.5761 if changed)
  long macd:        48 (incumbent — frozen)
  short macd:       24 (incumbent — FROZEN, causes 0.5761 if changed)
  long momentum:    48 (incumbent — frozen)
  short momentum:   48 (incumbent — frozen)

## ══════════════════════════════════════════════════════════════════════
## DEAD CLUSTERS — SHARPE VALUES THAT INDICATE SOMETHING WENT WRONG
## ══════════════════════════════════════════════════════════════════════

  DEAD: Sharpe=0.3825 (56 trades) — ⚠️ NEW DOMINANT FAILURE (9 times
        in last 20 gens). Most common failure mode as of v24.
        ROOT CAUSE UNKNOWN. You have the wrong YAML.
        FIX: Discard your ENTIRE YAML. Start completely fresh from the
        CURRENT INCUMBENT block. Copy it exactly. Change only ONE field.

  DEAD: Sharpe=0.3154 (56 trades) — ⚠️ FAILURE CLUSTER (4 prior times).
        ROOT CAUSE UNKNOWN. You have the wrong YAML.
        FIX: Discard entire YAML. Start fresh from incumbent block.

  DEAD: Sharpe=0.5279 (57 trades) — short-side indicator mutation.
  DEAD: Sharpe=0.5761 (57 trades) — ⚠️ PERSISTENT FAILURE.
        ROOT CAUSE: changed short bollinger (168), short MACD (24),
        or flipped momentum value false→true.
        FIX: Revert ALL indicator changes. Only change TP, timeout, SL.

  DEAD: Sharpe≈0.7734 (59 trades) — stale UI YAML (TP=7.14, timeout=129)
  DEAD: Sharpe=0.6911 (57 trades) — broken UI YAML (name: crossover)
  DEAD: Sharpe=0.5954 (58 trades) — wrong YAML variant
  DEAD: Sharpe≈1.0182/1.0325/1.0642/1.0952/1.1090 — dead ends
  DEAD: Sharpe≈1.1160/1.1161 (57 trades) — corrupt YAML
  DEAD: Sharpe≈1.1311 (60 trades) — gen 14993, superseded
  DEAD: Sharpe≈1.1362 (60 trades) — corrupt YAML variant
  DEAD: Sharpe≈1.1426 (60 trades) — gen 15042, superseded
  DEAD: Sharpe≈1.1450 (57 trades) — ⚠️ RECURRING FAILURE.
        Wrong YAML producing 57 trades. Incumbent has 60 trades.
        FIX: Discard your YAML. Re-read incumbent YAML.
  DEAD: Sharpe≈1.1643 (60 trades) — gen 15960, discarded
  DEAD: Sharpe≈1.1708 (60 trades) — gen 15998, discarded
  DEAD: Sharpe≈1.1882 (60 trades) — TP=10.0 or 10.5, inferior
  DEAD: Sharpe=1.2063 (60 trades) — gen 15062, superseded
  DEAD: Sharpe=1.2287 (60 trades) — float duplicate of gen 15480
  DEAD: Sharpe=1.2288 (60 trades) — gen 15480, timeout=144 DEAD
  DEAD: Sharpe=1.2429 (60 trades) — timeout=168, CONFIRMED INFERIOR.
        Fully tested and closed. Use timeout=192.
  DEAD: Sharpe=1.2430 (60 trades) — gen 15979, CURRENT INCUMBENT.
        Reproducing this = no-op. Your mutation had no effect.
  DEAD: Sharpe=0.0000 (0 trades, max_trades_reject) — you changed
        max_open or size_pct. Both are FROZEN at 2 and 25.0.

Diagnostic guide:
  Got 0.3825/56 trades: MOST COMMON FAILURE. Wrong YAML entirely.
        Discard it all. Start fresh from incumbent. Copy exactly.
  Got 0.3154/56