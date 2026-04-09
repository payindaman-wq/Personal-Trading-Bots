```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-1600 Update | Updated by MIMIR

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions
At 159h timeout: ~0.199% funding drag per full-hold trade
At 155h timeout: ~0.194% funding drag per full-hold trade
Reducing timeout reduces funding drag — this is a real edge, not cosmetic.
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage
MIN_TRADES: 400 (hard floor — any result with <400 trades is INVALID regardless of Sharpe)
MIN_TRADES STATUS: ✅ CONFIRMED FIXED at gen 542. futures_swing = 400. No action needed.

---

## ⚠️ MANDATORY PRE-FLIGHT CHECKLIST — DO THIS BEFORE ANY OTHER REASONING

Before proposing any change, you MUST complete this checklist IN ORDER:

☐ STEP 1: Open the YAML below. Find the line: timeout_hours: ___
           Write down the value you see. It MUST say 159.
           If it says 166 or any other value: STOP. Your first and only action
           this generation is to correct it to 159. Do not change anything else.

☐ STEP 2: Confirm stop_loss_pct = 1.91 in the YAML.

☐ STEP 3: Confirm rsi_long_threshold = 37.77 in the YAML (entry/long/conditions/value).

☐ STEP 4: Confirm size_pct = 25 in the YAML. This value is FROZEN — never change it.

☐ STEP 5: Identify which Priority axis you are testing (see Priority Order below).
           Write it down: "I am testing Priority ___ : [parameter] = [value]"

☐ STEP 6: Check your proposed value against ALL zombie fingerprints.
           Write: "My proposed change does NOT match any zombie fingerprint."

☐ STEP 7: Verify R:R ratio: take_profit / stop_loss > 2.0.
           Current: 4.65 / 1.91 = 2.43. Do not let this fall below 2.0.

☐ STEP 8: Confirm you are changing EXACTLY ONE parameter. Not two. Not zero.

Only after completing all 8 steps may you write your proposed YAML.

---

## ⚠️ YAML IS AUTHORITATIVE — READ CAREFULLY

The YAML below is the single source of truth. Do NOT use summary text values
if they conflict with the YAML.

Verified correct champion values (Gen 1592):

  - size_pct: 25                ← FROZEN. NEVER CHANGE THIS. EVER.
  - stop_loss_pct: 1.91         ← Exactly 1.91. Not 1.9. Not 1.89. Not 1.93.
  - take_profit_pct: 4.65       ← Baseline. See TP axis section below.
  - timeout_hours: 159          ← CURRENT CHAMPION VALUE. MUST BE 159. NOT 166.
  - rsi_long_threshold: 37.77   ← CURRENT CHAMPION VALUE. Not 37.82. Exactly 37.77.
  - rsi_short_threshold: 60     ← CONFIRMED 60. See short axis section below.
  - trend_period_hours: 48
  - max_open: 3
  - rsi_period_hours: 24

⚠️ TIMEOUT CRITICAL REMINDER:
  timeout_hours = 159 is the CURRENT CHAMPION. NOT 166.
  The Ghost Echo (sharpe=2.1998, trades=1264) is caused by using timeout=166.
  If your YAML says 166, you will produce the Ghost Echo. Correct to 159 first.
  The timeout axis direction is DOWNWARD from 159 (toward 155h).
  Do NOT revert to 166. Do NOT use 166 for any reason.

---

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer has declared DANGER regime (F&G=14, Extreme Fear, VIX elevated).
Directive: Reduce live position sizes to 25% of normal.
For LIVE DEPLOYMENT ONLY: effective size = 25% × 25% ≈ 6.25% per position.
This does NOT affect backtest research — continue optimizing against historical data normally.
Do NOT change size_pct in the research YAML based on macro regime.

---

## Current Champion Summary (Gen 1592 — ACTIVE CHAMPION)
- Sharpe: 2.2657 | Win rate: 39.9% | Trades: 1,267
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.77
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.91% stop-loss, 159h timeout
- Sizing: 25% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)
- R:R ratio: 4.65/1.91 = 2.43:1 (healthy — maintain above 2.0 at all times)

Previous champions for reference (do not reproduce — these are superseded):
  Gen 670:  Sharpe=2.1852 | Trades=1,266 | stop_loss=1.93 | rsi_long=37.82 | rsi_short=60 | timeout=166
  Gen 939:  Sharpe=2.1972 | Trades=1,259 | stop_loss=1.93 | rsi_long≈37.82 | rsi_short≈61 | timeout=166
  Gen 1132: Sharpe=2.2017 | Trades=1,266 | stop_loss=1.91 | rsi_long=37.82 | rsi_short=60 | timeout=166
  Gen 1186: Sharpe=2.2475 | Trades=1,265 | stop_loss=1.91 | rsi_long=37.77 | rsi_short=60 | timeout=166
  Gen 1477: Sharpe=2.2496 | Trades=1,267 | stop_loss=1.91 | rsi_long=37.77 | rsi_short=60 | timeout=166
  Gen 1592: Sharpe=2.2657 | Trades=1,267 | stop_loss=1.91 | rsi_long=37.77 | rsi_short=60 | timeout=159 ← CURRENT

⚠️ CHAMPION ECHO WARNINGS (read all before proposing):
  - rsi_long=37.82 → Sharpe≈2.2017 (Gen 1132 — NOT an improvement, Champion Echo)
  - Sharpe=2.1998, trades=1264, win_rate=39.5% → GHOST ECHO (see below)
    CAUSE: Using timeout=166 instead of 159. Fix the timeout. Do not test further.
  - Do NOT propose rsi_long=37.82 — confirmed non-improvement.

---

## ⚠️ RECENT DANGER EVENTS — READ BEFORE PROPOSING (Post-Gen-1592)

The following severe failures occurred AFTER the Gen 1592 champion. Learn from them.

Gen 1593: Ghost Echo (sharpe=2.1998, trades=1264) — timeout reverted to 166.
Gen 1594: sharpe=2.2336 — discarded. Unknown cause, slightly below champion.
Gen 1595: sharpe=2.1914 — discarded.
Gen 1596: sharpe=2.2496 — new_elite but NOT new_best (Gen 1477 level, not champion).
Gen 1597: sharpe=2.2336 — discarded.
Gen 1598: sharpe=-1.9761, trades=158 — ⚠️ CATASTROPHIC ZOMBIE C EVENT.
          158 trades is the lowest non-error count observed. This is extreme.
          CAUSE: Almost certainly timeout dropped below 140h OR two parameters
          were changed simultaneously. Do NOT combine parameter changes.
          Do NOT reduce timeout below 140h. 155h is the next valid test.
Gen 1599: sharpe=2.2015, trades=1272 — discarded. Trades slightly above champion,
          Sharpe below. Possible trend_period change. Do not replicate.
Gen 1600: sharpe=1.9865, trades=887 — ⚠️ SEVERE TRADE COUNT COLLAPSE.
          887 trades is a Zombie G event. Single-parameter change caused this.
          If you land here: immediately revert the change you made.
          CAUSE: Unknown — likely RSI or trend_period change. Do not push RSI
          long below 37.72 or trend_period outside 46-52h range.

PATTERN OBSERVED (Gens 1593–1600):
  The small LLM is repeatedly failing in two ways:
  (1) Ghost Echo → using old timeout=166 (fix: confirm timeout=159 first)
  (2) Zombie C/G events → violating the one-change rule or ignoring hard floors
  Both failures are preventable with the Pre-Flight Checklist above.

---

## Active Research Axes — PRIORITY ORDER

Work through these in strict priority order. Do NOT skip to lower-priority axes
until higher ones are tested and resolved.

### PRIORITY 1 — Timeout: 155h (HIGHEST PRIORITY — UNTESTED FROM NEW BASELINE)
  ⚠️ STATUS: This has NOT been cleanly tested from the Gen 1592 baseline (timeout=159).
  Gen 1598 (158 trades, Sharpe=-1.9761) suggests a timeout test went catastrophically
  wrong — possibly combined with another change, or timeout was reduced below 140h.
  155h has NOT been confirmed as Zombie C territory. It remains the primary test target.

  - Current: 159h (Gen 1592 champion)
  - Test: 155h ONLY — change timeout_hours from 159 to 155. Nothing else.
  - Why: timeout=159 beat timeout=166. The improvement direction is downward.
    Reducing timeout by 4h saves ~0.005% in funding drag per trade.
  - CHANGE ONLY timeout_hours. Do NOT touch any other parameter in the same generation.
  - If 155h improves (Sharpe > 2.2657): test 152h next.
  - If 155h fails (Sharpe ≤ 2.2657 but trades ≥ 400): test 157h (splitting difference).
  - If 155h produces <400 trades: it is Zombie C territory. HALT timeout axis.
    Immediately move to Priority 2 on the next generation.
  - HARD FLOOR: NEVER reduce below 140h. Gen 1598 proves this territory is fatal.
  - HARD CEILING: Do NOT test above 162h (funding drag confirmed destructive).
  - Step sizes: ±2 to ±6 hours only. Never jump more than ±8h in one generation.
  - ⚠️ ONE CHANGE ONLY: Do NOT combine timeout change with RSI, stop_loss, or TP change.

### PRIORITY 2 — Stop Loss: 1.89 (HIGH PRIORITY — UNTESTED, HIGH VALUE)
  - Current: 1.91
  - Test: 1.89 (exactly — not 1.88, not 1.90)
  - Why: Explicitly flagged as untested. 1.90 is Zombie D (NEVER use exactly 1.90).
    1.89 is NOT confirmed as a zombie. This is a high-value single test.
  - If 1.89 improves (Sharpe > 2.2657): test 1.88 next (floor of valid range).
  - If 1.89 fails: mark as Zombie D-adjacent. Do NOT test 1.88.
  - Valid stop_loss range: 1.88 to 1.97 ONLY.
  - NEVER use exactly 1.90 (Zombie D — confirmed trap, sharpe≈1.5918).
  - CHANGE ONLY stop_loss_pct. Do NOT touch any other parameter.

### PRIORITY 3 — RSI Long: 37.72 (SUSPENDED PENDING PRIORITY 1 AND 2 RESOLUTION)
  ⚠️ SUSPENSION NOTICE: The RSI long axis is temporarily suspended due to the
  Zombie C cluster (Gens 1588, 1591, 1598, 1600) — multiple catastrophic trade
  count collapses strongly suggest the LLM is mishandling RSI changes.
  Do NOT test RSI long until Priority 1 AND Priority 2 are resolved.
  When this axis resumes:

  - Current: 37.77
  - Test: 37.72 (exactly −0.05 step — not 37.70, not 37.75)
  - If 37.72 improves: test 37.67 next.
  - If 37.72 fails or trades drop toward 1,200: STOP RSI long axis permanently.
  - If 37.72 produces <800 trades: Zombie C-adjacent — halt immediately.
  - NEVER change RSI long by more than ±0.05 in a single generation.
  - NEVER set RSI long below 34.0 (confirmed Zombie C territory).
  - NEVER set RSI long above 38.5 (confirmed Zombie F territory).
  - CHANGE ONLY rsi_long_threshold. Do NOT touch timeout or stop_loss simultaneously.

### PRIORITY 4 — Take Profit: 4.70 and 4.60
  - Current: 4.65
  - Test 4.70 first (exactly +0.05).
  - If 4.70 fails, test 4.60 (exactly −0.05).
  - Maintain R:R above 2.0: with stop=1.91, TP must stay above 3.82.
  - Do NOT test TP below 4.5 (Zombie D territory confirmed).
  - Do NOT test TP above 5.2 without explicit instruction.
  - CHANGE ONLY take_profit_pct. Do NOT combine with other changes.

### PRIORITY 5 — RSI Short: 59 (UNTESTED, DOWNWARD EXPLORATION)
  - Current: 60
  - Test: 59 (exactly −1)
  - Why: The short side has only been explored upward (Zombie E). Downward is untested.
  - If 59 improves: test 58 next.
  - If 59 reduces trades below 1,100: halt short axis.
  - NEVER set RSI short below 55.
  - NEVER set RSI short above 63 (Zombie E territory begins at 64).
  - CHANGE ONLY rsi_short_threshold. Do NOT combine with other changes.

### PRIORITY 6 — Trend Period: 50h
  - Current: 48h
  - Test: 50h ONLY (one step tightening — not 52h, not 54h)
  - ⚠️ Gen 1600 (trades=887) may have been caused by a trend period change.
    If so, the valid range is narrower than expected. Step carefully.
  - If 50h fails: test 46h.
  - Valid range: 44h to 52h (narrowed from 40-60h based on Gen 1600 failure).
  - CHANGE ONLY trend_period_hours. Do NOT combine with other changes.

### PRIORITY 7 — RSI Period: 22h (LAST RESORT)
  - Current: 24h
  - Only test after Priorities 1–6 are exhausted.
  - Test 22h first (not 26h). Step size: ±2h only.
  - CHANGE ONLY rsi_period_hours. Do NOT combine with other changes.

---

## ⚠️ PARAMETER DISAMBIGUATION (COMPLETE REFERENCE — READ ALL BEFORE PROPOSING)

### RSI LONG THRESHOLD
  - Below 34.0  → ⛔ Zombie C territory (NEVER USE)
  - 34.0–37.71  → Untested and potentially dangerous — approach with ±0.05 steps only
  - 37.72       → PRIORITY 3 test target (suspended — do not test until P1/P2 resolve)
  - 37.77       → ✅ CURRENT CHAMPION (do not reproduce — this is the baseline)
  - 37.82       → ⛔ Champion Echo (superseded — NOT an improvement)
  - 38.5–40.0   → ⛔ Zombie F territory (NEVER USE)
  - Changes: ±0.05 increments ONLY. NEVER jump more than ±0.05 in a single generation.

### STOP LOSS
  - Below 1.88  → ⛔ Zombie territory (NEVER USE)
  - 1.88        → Floor of valid range (test only if 1.89 improves first)
  - 1.89        → PRIORITY 2 test target (untested — NOT confirmed zombie)
  - 1.90        → ⛔ Zombie D EXACTLY (NEVER USE — confirmed trap, sharpe≈1.5918)
  - 1.91        → ✅ CURRENT CHAMPION (do not reproduce — this is the baseline)
  - 1.93        → Previous champion (superseded — do not re-test)
  - Above 1.97  → ⛔ Zombie A territory (NEVER USE)
  - Valid test range: 1.88 to 1.97 ONLY (excluding exactly 1.90)

### TIMEOUT HOURS
  - Below 140h  → ⛔ Zombie C territory (NEVER USE — Gen 1598 confirms this is fatal)
  - 140–154h    → Uncharted but approaching danger — step carefully, ±4h maximum
  - 155h        → PRIORITY 1 test target (cleanly untested from Gen 1592 baseline)
  - 157h        → Fallback if 155h fails (test before moving to Priority 2)
  - 159h        → ✅ CURRENT CHAMPION (do not reproduce — this is the baseline)
  - 162h        → Fallback if 155h AND 157h both fail (confirm direction)
  - 166h        → ⛔ Previous champion timeout (SUPERSEDED — causes Ghost Echo)
  - Above 170h  → ⛔ Funding drag confirmed destructive (avoid)
  - Step size: ±2 to ±6 hours per generation ONLY. NEVER jump more than ±8h.

### TAKE PROFIT
  - Below 4.5%  → ⛔ Zombie D territory (confirmed)
  - 4.5–4.64%   → Untested below champion — approach carefully
  - 4.65%       → ✅ CURRENT CHAMPION (do not reproduce — this is the baseline)
  - 4.70%       → PRIORITY 4 test target
  - Above 5.2%  → Do not test without explicit instruction

---

## Known Zombie Configurations — NEVER REPRODUCE THESE

Memorize ALL fingerprints. Check your proposed change against each one.

- Zombie A: ~1,230 trades, Sharpe ~1.49, win rate ~38.0%
  (Gens 523, 528, 529, 539)
  Cause: stop_loss too loose (above 1.97%)

- Zombie B: ~1,190 trades, Sharpe ~1.02, win rate ~36.7%
  (Gens 535, 537, 540)
  Cause: TP too low combined with loose stop

- Zombie C: <400 trades, Sharpe deeply negative
  (Gens 524, 530, 534, 538, 597, 781, 787, 794, 922, 923, 927, 1117, 1120,
   1128, 1131, 1194, 1394, 1588, 1591, 1598)
  Cause: RSI thresholds too extreme, timeout too short (<140h), excessive stop tightening
  Prevention: Never set RSI long < 34, RSI short > 67, timeout < 140h, stop_loss < 1.88
  ⚠️ Gen 1588 (227 trades): confirmed Zombie C.
  ⚠️ Gen 1591 (407 trades): Zombie C-adjacent.
  ⚠️ Gen 1598 (158 trades, Sharpe=-1.9761): MOST SEVERE Zombie C observed.
     Cause likely: timeout below 140h OR two parameters changed simultaneously.

- Zombie D: ~1,228 trades, Sharpe ~1.5918, win rate ~38.4% — ⚠️ CRITICAL DANGER TRAP
  Seen 13+ times (gens 921, 928, 931, 932, 933, 938 and others)
  KNOWN CAUSE: stop_loss = 1.90 EXACTLY
               OR TP below 4.5%, OR stop below 1.88%
  FINGERPRINT: trades≈1228, sharpe≈1.5918, win_rate≈38.4%
  ⛔ If you land here: revert to stop_loss=1.91 immediately.
  ⚠️ NOTE: 1.89 has NOT been tested and is NOT confirmed Zombie D.
     Only exactly 1.90 is Zombie D. Testing 1.89 is PRIORITY 2.

- Zombie E: ~1,181 trades, Sharpe ~1.1013, win rate ~37.0% — ⚠️ HIGH-FREQUENCY TRAP
  Seen 10+ times in gens 1113–1131.
  FINGERPRINT: trades≈1181, sharpe≈1.1013, win_rate≈37.0%
  KNOWN CAUSE: RSI short threshold set too high (64–68 range)
  ⛔ If you land here: revert RSI short to 60. Do not test RSI short > 63.

- Zombie F: ~1,353 trades, Sharpe ~1.39, win rate ~40.5%
  Seen at Gen 1187.
  FINGERPRINT: trades significantly above 1,270, sharpe below 1.5, win_rate above 40%
  KNOWN CAUSE: RSI long threshold pushed above 39–40.
  ⛔ Do NOT push rsi_long_threshold above 38.5.

- Zombie G: ~1,163 trades, Sharpe ~1.39, win rate ~34.3%
  Seen at Gen 1580 and possibly Gen 1600 (trades=887, sharpe=1.9865).
  FINGERPRINT: trades significantly below 1,200, win_rate below 35%, Sharpe ~1.4–2.0
  KNOWN CAUSE: Unknown — likely aggressive RSI perturbation or trend period change
               causing entry quality collapse.
  Gen 1600 (trades=887): more severe variant. Possible trend_period or large RSI jump.
  ⛔ If you land here: immediately revert the single change you made. Do not persist.

- Ghost Echo — NOT a zombie, but wastes generations:
  FINGERPRINT: trades=1264, sharpe=2.1998, win_rate=39.5%
  Seen in gens 1574, 1576, 1577, 1583, 1584, 1585, 1589, 1590, 1593.
  ROOT CAUSE CONFIRMED: The small LLM is using timeout=166 instead of timeout=159.
  ⛔ If you produce this result: your YAML has timeout=166. Correct to 159 immediately.
     This is not a parameter tuning problem. It is a YAML reading error.
     Fix the timeout. Do not change any other parameter.

- Champion Echo — NOT a zombie, but wastes a generation:
  FINGERPRINT: trades≈1266, sharpe≈2.20 (NOT 2.2657)
  CAUSE: rsi_long = 37.82 (the Gen 1132 superseded champion value)
  ⛔ Do NOT propose rsi_long=37.82.

---

## Stagnation Detection — Emergency Protocols

### Protocol A: Ghost Echo Loop (Sharpe=2.1998, trades=1264)
If you produce this result:
  → STEP 1: Check your YAML. Find timeout_hours. Is it 159 or 166?
  → If timeout=166: correct to 159. This IS the fix. Nothing else needed.
  → If timeout=159 and you still get Ghost Echo: switch to Priority 2 axis (stop_loss=1.89).
  → Do NOT keep testing the same parameter that produced the Ghost Echo.

### Protocol B: Zombie C Cluster (<400 trades, 3+ consecutive generations)
If 3+ consecutive generations produce Zombie C:
  → STOP ALL CHANGES IMMEDIATELY.
  → On the very next generation: reproduce the EXACT Gen 1592 champion YAML.
     (Confirm: timeout=159, stop_loss=1.91, rsi_long=37.77, rsi_short=60, tp=4.65)
  → This generation will produce sharpe≈2.2657 — this confirms the baseline is restored.
  → On the generation AFTER that: test ONLY stop_loss=1.89 (Priority 2). Nothing else.
  → Do NOT touch RSI or timeout after a Zombie C cluster.

### Protocol C: Sharpe Oscillation (2.18–2.24 for 5+ consecutive generations)
If 5+ consecutive gens produce Sharpe in 2.18–2.24 and are all discarded:
  → CHECK: Is your YAML using timeout=159? If not: fix it.
  → If timeout is already 159: you are on the wrong axis. Switch to Priority 1 (155h).
  → If Priority 1 has been tried and failed: move to Priority 2 (stop_loss=1.89).
  → If both fail: move to Priority 4 (take_profit=4.70).

### Protocol D: Severe Trade Count Collapse (trades < 500, non-error)
If any single generation produces trades < 500:
  → This is a catastrophic failure. Do NOT continue on the same axis.
  → Revert to the exact Gen 1592 champion values in the next generation