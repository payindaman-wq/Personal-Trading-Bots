```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-1800 Update | Updated by MIMIR

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions
At 159h timeout: ~0.199% funding drag per full-hold trade
MIN_TRADES: 400 (hard floor — any result with <400 trades is INVALID regardless of Sharpe)
MIN_TRADES STATUS: ✅ CONFIRMED FIXED at gen 542. futures_swing = 400. No action needed.

---

## ⚠️ MANDATORY PRE-FLIGHT CHECKLIST — DO THIS BEFORE ANY OTHER REASONING

Before proposing any change, you MUST complete this checklist IN ORDER.
Write your answer to each step explicitly before moving to the next.

☐ STEP 1: Open the YAML below. Find the line: timeout_hours: ___
           Write down the EXACT value you see: "timeout_hours = [value]"
           It MUST say 159. If it says anything else: STOP.
           Your only action this generation is to write timeout_hours: 159.
           Do not change anything else.

☐ STEP 2: Write: "stop_loss_pct = [value from YAML]". It must be 1.91.

☐ STEP 3: Write: "rsi_long_threshold = [value from YAML]". It must be 37.77.

☐ STEP 4: Write: "size_pct = [value from YAML]". It must be 25. FROZEN. NEVER CHANGE.

☐ STEP 5: Write: "take_profit_pct = [value from YAML]". It must be 4.65.

☐ STEP 6: Write: "I am testing Priority ___ : [parameter] changing from [old] to [new]"
           The Priority order is: 2 → 3 → 4 → 5 → 6 → 7.
           Priority 1 (timeout) is CLOSED. See below.

☐ STEP 7: Write: "My proposed change does NOT match any zombie fingerprint."
           Check against ALL zombie fingerprints listed below.

☐ STEP 8: Write: "I am changing EXACTLY ONE parameter: [parameter name]."
           Confirm: no other parameter differs from the champion YAML.

☐ STEP 9: Verify R:R ratio: take_profit / stop_loss > 2.0.
           Write: "R:R = [TP] / [SL] = [ratio]. This is above 2.0."

☐ STEP 10: ⚠️ ANTI-CLONE CHECK — CRITICAL.
            Compare your proposed YAML against the champion YAML line by line.
            If EVERY line is identical, you have changed NOTHING.
            A zero-change generation is a WASTED generation.
            Write: "The parameter I changed is [name]. Old value: [X]. New value: [Y]."
            If you cannot write this, DO NOT SUBMIT — go back to Step 6.

Only after completing all 10 steps may you write your proposed YAML.

---

## ⚠️ YAML IS AUTHORITATIVE — READ CAREFULLY

The YAML below is the single source of truth. Do NOT use summary text values
if they conflict with the YAML.

Verified correct champion values (Gen 1592):

  - size_pct: 25                ← FROZEN. NEVER CHANGE THIS. EVER.
  - stop_loss_pct: 1.91         ← Exactly 1.91. Not 1.9. Not 1.89. Not 1.93.
  - take_profit_pct: 4.65       ← Baseline. See TP axis section below.
  - timeout_hours: 159          ← CURRENT CHAMPION VALUE. AXIS CLOSED. DO NOT CHANGE.
  - rsi_long_threshold: 37.77   ← CURRENT CHAMPION VALUE. Exactly 37.77.
  - rsi_short_threshold: 60     ← CONFIRMED 60.
  - trend_period_hours: 48
  - max_open: 3
  - rsi_period_hours: 24

⚠️ TIMEOUT AXIS — PERMANENTLY CLOSED:
  timeout_hours = 159 is the CONFIRMED OPTIMAL value.
  - 155h was tested (Gens 1781 and 1600): both produced ~888 trades and Sharpe ~2.00.
    This is a consistent failure. 155h is CONFIRMED ZOMBIE TERRITORY.
  - 166h causes the Ghost Echo (sharpe=2.1998, trades=1264). NEVER USE 166.
  - DO NOT CHANGE timeout_hours FOR ANY REASON.
  - If your pre-flight checklist shows timeout ≠ 159: correct it and stop.
    Do not change any other parameter in that generation.

---

## ⚠️ ATTRACTOR WARNING — KNOWN TRAP CONFIGURATIONS

The small LLM has been observed collapsing into a small set of recurring outputs.
These are NOT improvements. If you are about to produce one of these, STOP and
go back to the Priority axis instead.

ATTRACTOR 1 — "Champion Clone": sharpe=2.2657, trades=1267, win_rate=39.9%
  This means you changed NOTHING. You reproduced the champion exactly.
  This wastes a generation. Go back to Step 6 of the pre-flight checklist.
  Make sure your proposed YAML actually changes the Priority axis parameter.

ATTRACTOR 2 — "Near-Miss Cluster": sharpe=2.2336, trades=1267, win_rate=39.6%
  Seen in Gens 1782, 1794, 1800 and many others.
  This is a known sub-champion configuration. It is NOT an improvement.
  If you keep landing here, you are testing the wrong parameter.
  Check your Priority axis and make sure you are testing the correct value.

ATTRACTOR 3 — "Soft Miss": sharpe=2.2015, trades=1272, win_rate=39.6%
  Seen in Gens 1785, 1796, 1797 and others.
  Also a known sub-champion. If you land here repeatedly, switch Priority axis.

ATTRACTOR 4 — "Zombie G-adjacent": sharpe≈2.00, trades≈888
  Seen in Gens 1781 and 1600.
  CONFIRMED CAUSE: timeout_hours=155.
  Do NOT test timeout=155. This result confirms 155h is Zombie C-adjacent territory.

If you observe yourself producing Attractor 1, 2, 3, or 4:
  → Explicitly name which attractor you hit.
  → Identify which parameter you actually changed (or failed to change).
  → Move to the next Priority axis on the following generation.

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

Previous champions for reference (do not reproduce — superseded):
  Gen 670:  Sharpe=2.1852 | timeout=166
  Gen 939:  Sharpe=2.1972 | timeout=166
  Gen 1132: Sharpe=2.2017 | stop_loss=1.91 | rsi_long=37.82 | timeout=166
  Gen 1186: Sharpe=2.2475 | stop_loss=1.91 | rsi_long=37.77 | timeout=166
  Gen 1477: Sharpe=2.2496 | stop_loss=1.91 | rsi_long=37.77 | timeout=166
  Gen 1592: Sharpe=2.2657 | stop_loss=1.91 | rsi_long=37.77 | timeout=159 ← CURRENT

⚠️ CHAMPION ECHO WARNINGS:
  - rsi_long=37.82 → Sharpe≈2.2017 (Champion Echo — NOT an improvement)
  - timeout=166 → Sharpe=2.1998, trades=1264 (Ghost Echo — NOT an improvement)
  - Exact champion reproduction → Sharpe=2.2657, trades=1267 (Attractor 1 — wasted generation)

---

## ⚠️ RECENT DANGER EVENTS — READ BEFORE PROPOSING (Post-Gen-1592)

Gen 1593: Ghost Echo — timeout=166 used. Corrected.
Gen 1598: Zombie C (158 trades, Sharpe=-1.9761) — most severe failure observed.
Gen 1600: Zombie G-adjacent (887 trades, Sharpe=1.9865) — likely timeout=155h.
Gen 1781: CONFIRMED 155h result (888 trades, Sharpe=2.0047) — matches Gen 1600 exactly.
          This confirms: timeout=155h → ~888 trades, Sharpe~2.00. CLOSED.
Gen 1784: Attractor 1 (champion clone — zero change made).
Gen 1786: Attractor 1 (champion clone — zero change made).
Gen 1787: 1,451 trades, Sharpe=1.2606 — Zombie F-adjacent (likely rsi_long pushed above 38.5).
Gen 1789: 1,329 trades, Sharpe=1.1810 — Zombie F-adjacent (similar cause).
Gen 1790: Attractor 1 (champion clone — zero change made).
Gen 1791: Attractor 1 (champion clone — zero change made).
Gen 1795: 1,234 trades, Sharpe=1.8266 — Zombie D-adjacent (likely stop_loss=1.90 or TP change).
Gen 1799: 184 trades, Sharpe=-0.7999 — Zombie C (catastrophic — cause unknown, likely RSI extreme).

DOMINANT FAILURE MODES (Gens 1593–1800):
  (1) Attractor 1 (clone) — LLM changes nothing, wastes generation.
  (2) Attractor 2/3 — LLM lands on known sub-champion, not the target.
  (3) Zombie C/F — LLM changes parameter too aggressively or combines changes.
  (4) Ghost Echo — LLM uses timeout=166 instead of 159.
  ALL are preventable with strict pre-flight checklist adherence.

---

## Active Research Axes — PRIORITY ORDER

### ⛔ PRIORITY 1 — Timeout: CLOSED
  STATUS: CLOSED. 159h is confirmed optimal.
  - 155h tested twice (Gens 1600 and 1781): both → ~888 trades, Sharpe~2.00. FAIL.
  - 166h → Ghost Echo (2.1998). FAIL.
  - DO NOT change timeout_hours under any circumstances.
  - If timeout ≠ 159 in your YAML: correct it. That is your only action that generation.

---

### PRIORITY 2 — Stop Loss: 1.89 (HIGHEST ACTIVE PRIORITY)
  STATUS: UNTESTED. This is your primary target for the next generation.

  EXACT INSTRUCTION:
    Find this line in the YAML:   stop_loss_pct: 1.91
    Change it to:                 stop_loss_pct: 1.89
    Change NO other line.

  - Why: 1.90 is Zombie D (confirmed, sharpe≈1.5918). 1.89 is NOT tested and NOT a zombie.
    A tighter stop may improve Sharpe by reducing the size of losing trades.
  - Expected result: trades should remain near 1,267. If trades drop below 1,000, revert.
  - If 1.89 improves (Sharpe > 2.2657): test 1.88 next (floor of valid range).
  - If 1.89 fails (Sharpe ≤ 2.2657, trades ≥ 400): mark as sub-optimal. Move to Priority 3.
  - If 1.89 produces sharpe≈1.5918 and trades≈1228: you hit Zombie D. Revert immediately.
  - NEVER use exactly 1.90 (Zombie D — confirmed trap).
  - Valid stop_loss range: 1.88 to 1.97 ONLY (excluding exactly 1.90).
  - CHANGE ONLY stop_loss_pct. Do NOT touch any other parameter.

  ⚠️ HOW TO VERIFY YOU DID THIS CORRECTLY:
    After writing your YAML, check:
    - stop_loss_pct: 1.89  ← should say 1.89
    - timeout_hours: 159   ← unchanged
    - rsi_long_threshold: 37.77  ← unchanged (entry/long/conditions/value)
    - take_profit_pct: 4.65  ← unchanged
    - size_pct: 25  ← unchanged
    If any of these are wrong, fix them before submitting.

---

### PRIORITY 3 — Take Profit: 4.70 (HIGH PRIORITY — SAFE TEST)
  STATUS: UNTESTED from Gen 1592 baseline. Low risk of zombie events.

  EXACT INSTRUCTION:
    Find this line in the YAML:   take_profit_pct: 4.65
    Change it to:                 take_profit_pct: 4.70
    Change NO other line.

  - Why: A slightly wider TP may allow profitable trades to run further.
    R:R check: 4.70 / 1.91 = 2.46. Still above 2.0. Safe.
  - If 4.70 improves: test 4.75 next.
  - If 4.70 fails: test 4.60 (exactly −0.05 from champion).
  - If 4.60 fails: TP axis exhausted. Move to Priority 4.
  - Do NOT test TP below 4.50 (Zombie D territory confirmed).
  - Do NOT test TP above 5.20 without explicit instruction.
  - CHANGE ONLY take_profit_pct. Do NOT combine with other changes.
  - Only test Priority 3 after Priority 2 has been fully attempted.

---

### PRIORITY 4 — RSI Short: 59 (UNTESTED, MODERATE RISK)
  STATUS: UNTESTED. The short side has only been explored upward (Zombie E above 63).
  Downward exploration is safe within the 55–63 range.

  EXACT INSTRUCTION:
    Find the short entry condition in the YAML:
      - indicator: rsi
        period_hours: 24
        operator: gt
        value: 60
    Change value: 60 to value: 59
    Change NO other line.

  - If 59 improves: test 58 next.
  - If 59 reduces trades below 1,100: halt short axis.
  - NEVER set RSI short below 55.
  - NEVER set RSI short above 63 (Zombie E territory begins at 64).
  - CHANGE ONLY rsi_short_threshold. Do NOT combine with other changes.
  - Only test Priority 4 after Priorities 2 and 3 are fully attempted.

---

### PRIORITY 5 — RSI Long: 37.72 (SUSPENDED — TEST AFTER P2, P3, P4)
  ⚠️ SUSPENSION NOTICE: RSI long axis remains suspended until Priorities 2, 3,
  and 4 are resolved. Multiple Zombie C events (Gens 1588, 1591, 1598, 1799)
  confirm the LLM cannot safely handle RSI long changes.
  When this axis resumes:

  EXACT INSTRUCTION:
    Find the long entry condition in the YAML:
      - indicator: rsi
        period_hours: 24
        operator: lt
        value: 37.77
    Change value: 37.77 to value: 37.72
    Change NO other line.

  - NEVER change RSI long by more than ±0.05 in a single generation.
  - NEVER set RSI long below 34.0 (confirmed Zombie C territory).
  - NEVER set RSI long above 38.5 (confirmed Zombie F territory).
  - If 37.72 fails or trades drop toward 1,200: STOP RSI long axis permanently.
  - If 37.72 produces <800 trades: Zombie C-adjacent — halt immediately.

---

### PRIORITY 6 — Trend Period: 50h (LOW PRIORITY)
  - Current: 48h
  - Test: 50h ONLY (not 52h — Gen 1600/1787/1789 suggest this range is dangerous)
  - ⚠️ Gens 1787 (1,451 trades) and 1789 (1,329 trades) may have been trend period changes.
    If so, valid range is narrower than expected. Step with extreme caution.
  - Valid range: 46h to 50h ONLY (narrowed based on observed failures).
  - If 50h fails: test 46h.
  - CHANGE ONLY trend_period_hours. Do NOT combine with other changes.
  - Only test after Priorities 2–5 are exhausted.

---

### PRIORITY 7 — RSI Period: 22h (LAST RESORT)
  - Current: 24h
  - Only test after Priorities 2–6 are exhausted.
  - Test 22h first (not 26h). Step size: ±2h only.
  - CHANGE ONLY rsi_period_hours. Do NOT combine with other changes.

---

## ⚠️ PARAMETER DISAMBIGUATION (COMPLETE REFERENCE)

### RSI LONG THRESHOLD (entry/long/conditions/value)
  - Below 34.0  → ⛔ Zombie C territory (NEVER USE)
  - 34.0–37.71  → Dangerous — approach with ±0.05 steps only
  - 37.72       → Priority 5 test target (suspended)
  - 37.77       → ✅ CURRENT CHAMPION (baseline)
  - 37.82       → ⛔ Champion Echo (superseded)
  - Above 38.5  → ⛔ Zombie F territory (NEVER USE — Gens 1787, 1789 confirm danger)
  - Changes: ±0.05 increments ONLY. NEVER jump more than ±0.05.

### STOP LOSS
  - Below 1.88  → ⛔ Zombie territory (NEVER USE)
  - 1.88        → Floor (test only if 1.89 improves first)
  - 1.89        → ✅ Priority 2 test target (untested — NOT confirmed zombie)
  - 1.90        → ⛔ Zombie D EXACTLY (NEVER USE — sharpe≈1.5918, trades≈1228)
  - 1.91        → ✅ CURRENT CHAMPION (baseline)
  - 1.93        → Previous champion (superseded — do not re-test)
  - Above 1.97  → ⛔ Zombie A territory (NEVER USE)

### TIMEOUT HOURS
  - ⛔ AXIS CLOSED. timeout_hours = 159 is confirmed optimal. DO NOT CHANGE.
  - 155h → ⛔ CONFIRMED FAILURE (~888 trades, Sharpe~2.00) — Gens 1600, 1781.
  - 166h → ⛔ Ghost Echo (sharpe=2.1998, trades=1264). NEVER USE.
  - 159h → ✅ CURRENT CHAMPION (baseline, FROZEN).

### TAKE PROFIT
  - Below 4.50% → ⛔ Zombie D territory (confirmed)
  - 4.60%       → Fallback if 4.70 fails
  - 4.65%       → ✅ CURRENT CHAMPION (baseline)
  - 4.70%       → Priority 3 test target
  - 4.75%       → Test if 4.70 improves
  - Above 5.20% → Do not test without explicit instruction

### RSI SHORT THRESHOLD (entry/short/conditions/value)
  - Below 55    → ⛔ NEVER USE
  - 55–58       → Caution zone
  - 59          → Priority 4 test target
  - 60          → ✅ CURRENT CHAMPION (baseline)
  - 61–63       → Valid but confirmed sub-optimal upward
  - Above 63    → ⛔ Zombie E territory (NEVER USE)

---

## Known Zombie Configurations — NEVER REPRODUCE THESE

- Zombie A: ~1,230 trades, Sharpe ~1.49, win rate ~38.0%
  CAUSE: stop_loss above 1.97%

- Zombie B: ~1,190 trades, Sharpe ~1.02, win rate ~36.7%
  CAUSE: TP too low combined with loose stop

- Zombie C: <400 trades, Sharpe deeply negative
  CAUSE: RSI thresholds too extreme, timeout too short (<140h), excessive stop tightening
  CONFIRMED INSTANCES: Gens 524, 530, 534, 538, 597, 781, 787, 794, 922, 923, 927,
    1117, 1120, 1128, 1131, 1194, 1394, 1588, 1591, 1598, 1799
  Prevention: Never RSI long < 34, RSI short > 67, timeout < 159 (CLOSED), stop < 1.88

- Zombie D: ~1,228 trades, Sharpe ~1.5918, win rate ~38.4%
  CAUSE: stop_loss = 1.90 EXACTLY, OR TP below 4.5%, OR stop below 1.88%
  ⚠️ 1.89 is NOT confirmed Zombie D. Only exactly 1.90 is Zombie D.
  Seen 13+ times (Gens 921, 928, 931, 932, 933, 938 and others).
  Gen 1795 (1,234 trades, Sharpe=1.8266) may be Zombie D-adjacent.

- Zombie E: ~1,181 trades, Sharpe ~1.1013, win rate ~37.0%
  CAUSE: RSI short threshold set too high (64–68 range)
  Seen 10+ times in Gens 1113–1131.

- Zombie F: ~1,353 trades, Sharpe ~1.39, win rate ~40.5%
  CAUSE: RSI long threshold pushed above 39–40.
  ⚠️ Gens 1787 (1,451 trades, Sharpe=1.2606) and 1789 (1,329 trades, Sharpe=1.1810)
  suggest Zombie F-adjacent territory begins even below 39 — possibly above 38.5.
  DO NOT push rsi_long above 38.5.

- Zombie G: trades significantly below 1,200, win_rate below 35%, Sharpe ~1.4–2.0
  CAUSE: Unknown — likely aggressive RSI perturbation or trend period change.
  Gen 1600 (887 trades): now confirmed as 155h timeout result (not Zombie G proper).
  Gen 1781 (888 trades): same confirmation.

- Ghost Echo — NOT a zombie, but wastes generations:
  FINGERPRINT: trades=1264, sharpe=2.1998, win_rate=39.5%
  ROOT CAUSE: timeout=166 used instead of 159.
  Fix: correct timeout to 159. Do not change anything else.

- Champion Echo — NOT a zombie, but wastes a generation:
  FINGERPRINT: trades≈1266, sharpe≈2.20 (NOT 2.2657)
  CAUSE: rsi_long = 37.82

- Attractor 1 (Clone) — wastes a generation:
  FINGERPRINT: trades=1267, sharpe=2.2657, win_rate=39.9% — EXACT CHAMPION
  CAUSE: LLM changed nothing. Use Step 10 of pre-flight checklist to prevent.

- Attractor 2 (Near-Miss) — NOT an improvement:
  FINGERPRINT: trades=1267, sharpe=2.2336, win_rate=39.6%
  Seen repeatedly: Gens 1782, 1794, 1800 and many others before.
  CAUSE: Unknown specific configuration — possibly a known-bad parameter set.
  If you land here: you are not testing the right parameter. Check your YAML.

- Attractor 3 (Soft Miss) — NOT an improvement:
  FINGERPRINT: trades=1272, sharpe=2