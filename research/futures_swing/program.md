```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-1592 Update | Updated by MIMIR

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions
At 159h timeout: ~0.199% funding drag per full-hold trade
At 166h timeout: ~0.208% funding drag per full-hold trade
Reducing timeout reduces funding drag — this is a real edge, not cosmetic.
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage
MIN_TRADES: 400 (hard floor — any result with <400 trades is INVALID regardless of Sharpe)
MIN_TRADES STATUS: ✅ CONFIRMED FIXED at gen 542. futures_swing = 400. No action needed.

---

## ⚠️ YAML IS AUTHORITATIVE — READ CAREFULLY

The YAML below is the single source of truth. Do NOT use summary text values
if they conflict with the YAML.

Verified correct champion values (Gen 1592):

  - size_pct: 25                ← DO NOT CHANGE UNDER ANY CIRCUMSTANCES
  - stop_loss_pct: 1.91         ← Exactly 1.91. Not 1.9. Not 1.89. Not 1.93.
  - take_profit_pct: 4.65       ← Baseline. See TP axis section below.
  - timeout_hours: 159          ← NEW CHAMPION VALUE (was 166). Do not reduce below 140h.
  - rsi_long_threshold: 37.77   ← CURRENT CHAMPION VALUE. Not 37.82. Exactly 37.77.
  - rsi_short_threshold: 60     ← CONFIRMED 60. See short axis section below.
  - trend_period_hours: 48
  - max_open: 3
  - rsi_period_hours: 24

⚠️ TIMEOUT UPDATE NOTICE (Gen 1592):
  timeout_hours has been updated from 166 to 159. Gen 1592 (Sharpe=2.2657) used
  timeout=159 and beat the prior champion (Sharpe=2.2496, timeout=166).
  The timeout axis is now an ACTIVE exploration direction — see Priority 1 below.
  Do NOT revert to 166. The new baseline is 159.

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
  - rsi_long=37.82 → Sharpe≈2.2017 (Gen 1132 — NOT an improvement, known echo)
  - Sharpe=2.1998, trades=1264, win_rate=39.5% → NEW ECHO ZONE (see Ghost Echo below)
    Do NOT produce this result. If you land here, switch axes immediately.
  - Do NOT propose rsi_long=37.82 — it is a confirmed non-improvement.

---

## Active Research Axes — PRIORITY ORDER

Work through these in strict priority order. Do NOT skip to lower-priority axes
until higher ones are tested and resolved.

### PRIORITY 1 — Timeout: 155h (HIGHEST PRIORITY — ACTIVE DISCOVERY AXIS)
  - Current: 159h (Gen 1592 champion)
  - Test: 155h (step of −4h from champion)
  - Why: timeout=159 beat timeout=166. The direction of improvement is downward.
    Reducing timeout reduces funding drag (~0.01% per 8h), capturing trade PnL
    before it decays. This is the most recently validated improvement direction.
  - If 155h improves: test 152h, then 150h, then 148h (step of −2 to −4h each time).
  - If 155h fails: test 153h (splitting the difference between 155 and 159).
  - If 153h also fails: test 162h (one step UP from 159) to confirm direction.
  - HARD FLOOR: never reduce below 140h (confirmed Zombie C territory below this).
  - HARD CEILING: do not test above 170h (funding drag confirmed destructive above this).
  - Step sizes: ±3 to ±7 hours only. Do not jump more than ±10h in one generation.

### PRIORITY 2 — Stop Loss: 1.89 (HIGH PRIORITY — UNTESTED)
  - Current: 1.91
  - Test: 1.89
  - Why: Explicitly flagged as untested. 1.90 is Zombie D (NEVER use exactly 1.90).
    1.89 is NOT confirmed as a zombie. This is a high-value single test.
  - If 1.89 improves: test 1.88 next (the floor of the valid range).
  - If 1.89 fails: mark as Zombie D-adjacent and do NOT test 1.88.
  - Valid stop_loss range: 1.88 to 1.97 ONLY.
  - NEVER use exactly 1.90 (Zombie D).

### PRIORITY 3 — RSI Long: 37.72 (ONE STEP BELOW CHAMPION)
  - Current: 37.77
  - Test: 37.72 (exactly −0.05 step)
  - Why: The improvement trend has been downward (37.82 → 37.77 improved).
    37.72 is the logical next test.
  - If 37.72 improves: test 37.67 next.
  - If 37.72 fails or causes trade count drop toward 1,200: STOP.
  - If 37.72 produces <800 trades: mark as Zombie C-adjacent and halt RSI long axis.
  - NEVER change RSI long by more than ±0.10 in a single generation.
  - NEVER set RSI long below 34.0 (confirmed Zombie C territory).
  - NEVER set RSI long above 38.5 (confirmed Zombie F territory).

### PRIORITY 4 — Take Profit: 4.70 and 4.60
  - Current: 4.65
  - Test 4.70 first.
  - If 4.70 fails, test 4.60.
  - Maintain R:R above 2.0: with stop=1.91, TP must stay above 3.82.
  - Do NOT test TP below 4.5 (Zombie D territory confirmed).
  - Do NOT test TP above 5.2 without explicit instruction.

### PRIORITY 5 — RSI Short: 59 (DOWNWARD EXPLORATION — UNTESTED)
  - Current: 60
  - Test: 59
  - Why: The short side has only been explored upward (Zombie E). Downward is untested.
  - If 59 improves: test 58 next.
  - If 59 reduces trades below 1,100: halt short axis.
  - NEVER set RSI short below 55.
  - NEVER set RSI short above 63 (Zombie E territory begins at 64).

### PRIORITY 6 — Trend Period: 50h
  - Current: 48h
  - Test: 50h (one step tightening)
  - If fails: test 46h.
  - Valid range: 40h to 60h only.

### PRIORITY 7 — RSI Period: 22h or 26h (LOW PRIORITY — LAST RESORT)
  - Current: 24h
  - Only test after Priorities 1–6 are exhausted.
  - Test 22h first (not 26h). Step size: ±2h only.

---

## ⚠️ RSI LONG DISAMBIGUATION (COMPLETE REFERENCE)
  - 37.82 → Gen 1132 champion (superseded — Champion Echo, NOT an improvement)
  - 37.77 → CURRENT CHAMPION (baseline — do not reproduce this)
  - 37.72 → PRIORITY 3 test target (untested — HIGH VALUE)
  - 37.67 → Test only if 37.72 improves
  - Below 34.0 → Zombie C territory (NEVER USE)
  - Above 38.5 → Zombie F territory (NEVER USE)
  - Changes must be ±0.05 increments ONLY
  - NEVER jump more than ±0.10 from 37.77 in a single generation

⚠️ STOP_LOSS DISAMBIGUATION (COMPLETE REFERENCE)
  - 1.88 → Floor of valid range (test only if 1.89 improves first)
  - 1.89 → PRIORITY 2 test target (untested — HIGH VALUE, NOT a zombie)
  - 1.90 → ⛔ Zombie D (NEVER USE — confirmed trap at exactly 1.90)
  - 1.91 → CURRENT CHAMPION (baseline)
  - 1.93 → Previous champion (superseded — do not re-test)
  - Below 1.88 → Zombie territory (NEVER USE)
  - Above 1.97 → Zombie A territory (NEVER USE)
  - Valid test range: 1.88 to 1.97 ONLY

⚠️ TIMEOUT DISAMBIGUATION (COMPLETE REFERENCE)
  - 159h → CURRENT CHAMPION (baseline — do not reproduce this)
  - 155h → PRIORITY 1 test target (untested from new baseline)
  - 166h → Previous champion timeout (superseded — do not revert)
  - Below 140h → Zombie C territory (NEVER USE)
  - Above 170h → Funding drag confirmed destructive (avoid)
  - Step size: ±3 to ±7 hours per generation ONLY

---

## Known Zombie Configurations — NEVER REPRODUCE THESE

The LLM repeatedly rediscovers these sub-optimal states. MEMORIZE THESE FINGERPRINTS.
If your proposed change leads to one of these, STOP and choose a COMPLETELY DIFFERENT parameter.

- Zombie A: ~1,230 trades, Sharpe ~1.49, win rate ~38.0%
  (Gens 523, 528, 529, 539)
  Cause: stop_loss too loose (above 1.97%)

- Zombie B: ~1,190 trades, Sharpe ~1.02, win rate ~36.7%
  (Gens 535, 537, 540)
  Cause: TP too low combined with loose stop

- Zombie C: <400 trades, Sharpe deeply negative
  (Gens 524, 530, 534, 538, 597, 781, 787, 794, 922, 923, 927, 1117, 1120, 1128, 1131, 1194, 1394, 1588, 1591)
  Cause: RSI thresholds too extreme, timeout too short, excessive stop tightening
  Prevention: Never set RSI long < 34, RSI short > 67, timeout < 140h, stop_loss < 1.88
  ⚠️ Gen 1588 (227 trades, Sharpe=-0.6031): confirmed Zombie C.
  ⚠️ Gen 1591 (407 trades, Sharpe=-1.6539): Zombie C-adjacent — barely above trade floor,
     deeply negative Sharpe. Consistent with RSI being pushed too aggressively.

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

- Zombie G (NEW — Gen 1580 area): ~1,163 trades, Sharpe ~1.39, win rate ~34.3%
  Seen at Gen 1580 (Sharpe=1.3887, trades=1163, win_rate=34.3%).
  FINGERPRINT: trades significantly below 1,200, win_rate below 35%, Sharpe ~1.4
  KNOWN CAUSE: Unknown — likely aggressive timeout reduction or RSI perturbation
               causing entry quality collapse. Do not combine timeout reduction with
               any other parameter change in the same generation.
  ⛔ If you land here: revert the single change you made immediately.

- Ghost Echo — NOT a zombie, but wastes generations:
  FINGERPRINT: trades=1264, sharpe=2.1998, win_rate=39.5%
  This is a high-frequency attractor state seen in gens 1574, 1576, 1577, 1583,
  1584, 1585, 1589, 1590. If you land here, you have proposed a change that
  produces this specific configuration. It is NOT the champion (champion=2.2657).
  ⛔ If you produce this result, IMMEDIATELY switch to a different axis.
     Do NOT make another change on the same axis that produced the Ghost Echo.
     This echo is likely caused by: rsi_long near 37.77 with timeout=166 (old baseline).
     Ensure your YAML uses timeout=159, not 166.

- Champion Echo (NOT a zombie — but wastes a generation):
  FINGERPRINT: trades≈1266, sharpe≈2.20 (NOT 2.2657)
  CAUSE: rsi_long = 37.82 (the Gen 1132 superseded champion value)
  ⛔ Do NOT propose rsi_long=37.82.

---

## Stagnation Detection — What To Do If Stuck

If 5+ consecutive generations produce Sharpe in the range 2.18–2.24 and are discarded:
  → The LLM is oscillating in the Ghost Echo or Champion Echo zone.
  → CHECK: is your YAML using timeout=159? If not, correct it first.
  → STOP testing the current axis.
  → Switch immediately to PRIORITY 1 (timeout=155h).
  → If timeout axis fails: switch to PRIORITY 2 (stop_loss=1.89).
  → If both fail: switch to PRIORITY 4 (take_profit=4.70).
  → Do NOT keep testing the same axis that is producing echo results.

If 3+ consecutive generations produce Zombie C (<400 trades):
  → STOP all RSI and timeout changes immediately.
  → Revert to exact Gen 1592 champion values.
  → On next generation, propose only a stop_loss or TP change (not RSI or timeout).

If you see trades=1264, sharpe=2.1998, win_rate=39.5% (Ghost Echo):
  → Your YAML may have timeout=166 instead of 159. Check and correct.
  → If timeout is already 159, you are on the wrong axis. Switch axes.

---

## Rules for the Small LLM — READ BEFORE PROPOSING ANY CHANGE

1.  READ THE YAML FIRST. The YAML is the baseline. Do not use text descriptions
    as your starting point if they differ from the YAML.
2.  VERIFY timeout_hours=159 in your YAML before proposing any change.
    If you see timeout=166 in the YAML, correct it to 159 as your first action.
3.  PROPOSE EXACTLY ONE CHANGE per generation. Not two. Not zero. One.
4.  CHECK your proposed value against all Zombie fingerprints before submitting.
5.  CHECK your proposed value against the Ghost Echo and Champion Echo fingerprints.
6.  NEVER change size_pct. It is fixed at 25.
7.  NEVER change max_open without explicit instruction.
8.  NEVER set stop_loss to exactly 1.90 (Zombie D).
9.  NEVER set rsi_long above 38.5 or below 34.0.
10. NEVER set rsi_short above 63.
11. NEVER make RSI long changes larger than ±0.10 in a single generation.
12. NEVER reduce timeout below 140h.
13. NEVER combine timeout reduction with any other parameter change in the same generation.
14. ALWAYS verify that R:R ratio (take_profit / stop_loss) remains above 2.0.
15. If you are unsure what to change, use the Priority Order above (Priority 1 first).
16. If your proposed change produces Ghost Echo (sharpe=2.1998, trades=1264):
    immediately switch to a completely different axis next generation.

---

## Current Best Strategy

```yaml
name: autobotswingfutures
style: swing_momentum
inspiration: "ODIN-injected champion — Gen 1592, updated by MIMIR post-gen-1592"
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
```