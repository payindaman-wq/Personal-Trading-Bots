```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-1400 Update | Updated by MIMIR

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions
At current 166h timeout: ~0.21% funding drag per full-hold trade (significant)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage
MIN_TRADES: 400 (hard floor — any result with <400 trades is INVALID regardless of Sharpe)
MIN_TRADES STATUS: ✅ CONFIRMED FIXED at gen 542. futures_swing = 400. No action needed.

---

## ⚠️ YAML IS AUTHORITATIVE — READ CAREFULLY

The YAML below is the single source of truth. Do NOT use summary text values
if they conflict with the YAML. The YAML has been corrected as of Gen 1400 to
exactly match the Gen 1186 champion values. These are verified correct:

  - size_pct: 25                ← DO NOT CHANGE UNDER ANY CIRCUMSTANCES
  - stop_loss_pct: 1.91         ← Exactly 1.91. Not 1.9. Not 1.89. Not 1.93.
  - take_profit_pct: 4.65       ← Baseline. See TP axis section below.
  - timeout_hours: 166          ← Do not reduce below 140h.
  - rsi_long_threshold: 37.77   ← CURRENT CHAMPION VALUE. Not 37.82. Exactly 37.77.
  - rsi_short_threshold: 60     ← CONFIRMED 60. See short axis section below.
  - trend_period_hours: 48
  - max_open: 3
  - rsi_period_hours: 24

⚠️ YAML CORRECTION NOTICE (Gen 1400):
  The YAML previously contained STALE values (size_pct=15, max_open=2,
  stop_loss=2.5, take_profit=5.0, timeout=96) that did NOT match the champion.
  This has been corrected. The YAML below now reflects the true Gen 1186 champion.
  ALL prior discards in gens 1–5 and convergence behavior in gens 1392–1400 may
  have been caused by this YAML/text conflict. The YAML is now authoritative AND
  consistent with the text. Trust the YAML.

---

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer has declared DANGER regime (F&G=14, Extreme Fear, VIX elevated).
Directive: Reduce live position sizes to 25% of normal.
For LIVE DEPLOYMENT ONLY: effective size = 25% × 25% ≈ 6.25% per position.
This does NOT affect backtest research — continue optimizing against historical data normally.
Do NOT change size_pct in the research YAML based on macro regime.

---

## Current Champion Summary (Gen 1186 — ACTIVE CHAMPION)
- Sharpe: 2.2475 | Win rate: 39.6% | Trades: 1,265
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.77
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.91% stop-loss, 166h timeout
- Sizing: 25% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)
- R:R ratio: 4.65/1.91 = 2.43:1 (healthy — maintain above 2.0 at all times)

Previous champions for reference (do not reproduce — these are superseded):
  Gen 670:  Sharpe=2.1852 | Trades=1,266 | stop_loss=1.93 | rsi_long=37.82 | rsi_short=60
  Gen 939:  Sharpe=2.1972 | Trades=1,259 | stop_loss=1.93 | rsi_long≈37.82 | rsi_short≈61
  Gen 1132: Sharpe=2.2017 | Trades=1,266 | stop_loss=1.91 | rsi_long=37.82 | rsi_short=60
  Gen 1186: Sharpe=2.2475 | Trades=1,265 | stop_loss=1.91 | rsi_long=37.77 | rsi_short=60 ← CURRENT

⚠️ CHAMPION ECHO WARNING:
  rsi_long=37.82 produces Sharpe≈2.2017 (Gen 1132 value — NOT an improvement).
  rsi_long=37.77 is the current champion. Do NOT propose 37.82 — it is a known echo.
  If you propose 37.82, you will waste a generation reproducing a superseded result.

---

## Active Research Axes — PRIORITY ORDER

These are the confirmed untested or undertested directions. Work through them
in priority order. Do NOT skip to lower-priority axes until higher ones are tested.

### PRIORITY 1 — Stop Loss: 1.89 (HIGH PRIORITY — UNTESTED)
  - Current: 1.91
  - Test: 1.89
  - Why: Explicitly flagged as untested. 1.90 is Zombie D. 1.89 is NOT confirmed
    as a zombie. This is the highest-priority single test remaining.
  - If 1.89 improves: test 1.88 next (the floor of the valid range).
  - If 1.89 fails: mark as Zombie D-adjacent and do NOT test 1.88.
  - Valid stop_loss range: 1.88 to 1.97 ONLY.

### PRIORITY 2 — RSI Long: 37.72 (ONE STEP BELOW CHAMPION)
  - Current: 37.77
  - Test: 37.72 (exactly −0.05 step)
  - Why: The trend of improvement has been downward (37.82 → 37.77 improved).
    37.72 is the logical next test in this direction.
  - If 37.72 improves: test 37.67 next.
  - If 37.72 fails or causes trade count drop toward 1,200: STOP, do not go lower.
  - If 37.72 produces <800 trades: mark as Zombie C-adjacent and halt RSI long axis.
  - NEVER change RSI long by more than ±0.10 in a single generation.
  - NEVER set RSI long below 34.0 (confirmed Zombie C territory).
  - NEVER set RSI long above 38.5 (confirmed Zombie F territory).

### PRIORITY 3 — Take Profit: 4.70 and 4.60
  - Current: 4.65
  - Test 4.70 first (tightening TP slightly to capture more wins).
  - If 4.70 fails, test 4.60.
  - Maintain R:R above 2.0: with stop=1.91, TP must stay above 3.82.
  - Do NOT test TP below 4.5 (Zombie D territory confirmed).
  - Do NOT test TP above 5.2 without explicit instruction.

### PRIORITY 4 — RSI Short: 59 (DOWNWARD EXPLORATION — UNTESTED)
  - Current: 60
  - Test: 59
  - Why: The short side has only been explored upward (60→64+ → Zombie E).
    Downward from 60 is completely untested.
  - If 59 improves: test 58 next.
  - If 59 reduces trades below 1,100: mark as overtightening, halt short axis.
  - NEVER set RSI short below 55 (extreme overtightening).
  - NEVER set RSI short above 63 (confirmed Zombie E territory begins at 64).

### PRIORITY 5 — Trend Period: 50h
  - Current: 48h
  - Test: 50h (one step tightening)
  - Why: Untested adjacent value. Minor filter tightening may reduce noise.
  - If fails: test 46h.
  - Valid range: 40h to 60h. Outside = untested risk.

### PRIORITY 6 — RSI Period: 22h or 26h (LOW PRIORITY — LAST RESORT)
  - Current: 24h
  - Only test after Priorities 1–5 are exhausted.
  - Test 22h first (not 26h).
  - Step size: ±2h only.

---

## ⚠️ RSI LONG DISAMBIGUATION (COMPLETE REFERENCE)
  - 37.82 → Gen 1132 champion (superseded — Champion Echo, NOT an improvement)
  - 37.77 → CURRENT CHAMPION (baseline — do not reproduce this)
  - 37.72 → PRIORITY 2 test target (untested — HIGH VALUE)
  - 37.67 → Test only if 37.72 improves
  - Below 34.0 → Zombie C territory (NEVER USE)
  - Above 38.5 → Zombie F territory (NEVER USE)
  - Changes must be ±0.05 increments ONLY
  - NEVER jump more than ±0.10 from 37.77 in a single generation

⚠️ STOP_LOSS DISAMBIGUATION (COMPLETE REFERENCE)
  - 1.88 → Floor of valid range (test only if 1.89 improves first)
  - 1.89 → PRIORITY 1 test target (untested — HIGH VALUE, NOT a zombie)
  - 1.90 → Zombie D (NEVER USE — confirmed trap at exactly 1.90)
  - 1.91 → CURRENT CHAMPION (baseline)
  - 1.93 → Previous champion (superseded, not a zombie — do not re-test)
  - Below 1.88 → Zombie territory (NEVER USE)
  - Above 1.97 → Zombie A territory (NEVER USE)
  - Valid test range: 1.88 to 1.97 ONLY

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
  (Gens 524, 530, 534, 538, 597, 781, 787, 794, 922, 923, 927, 1117, 1120, 1128, 1131, 1194)
  Cause: RSI thresholds too extreme, timeout too short, excessive stop tightening
  Prevention: Never set RSI long < 34, RSI short > 67, timeout < 140h, stop_loss < 1.88
  ⚠️ Gen 1194 (185 trades): confirmed Zombie C — RSI long pushed too far below 37.77.
  ⚠️ Gen 2 / Gen 4 (175 trades): confirmed Zombie C — caused by stale YAML baseline.
  ⚠️ Gen 1394 (541 trades, Sharpe -0.977): Zombie C-adjacent — likely RSI long pushed
     to ~36 from wrong anchor. Stale YAML was almost certainly the root cause.

- Zombie D: ~1,228 trades, Sharpe ~1.5918, win rate ~38.4% — ⚠️ CRITICAL DANGER TRAP
  Seen 13+ times (gens 921, 928, 931, 932, 933, 938 and others)
  KNOWN CAUSE: stop_loss = 1.90 EXACTLY
               OR TP below 4.5%, OR stop below 1.88%
  FINGERPRINT: trades≈1228, sharpe≈1.5918, win_rate≈38.4%
  ⛔ If you land here: do NOT touch TP or stop loss further downward.
     Revert to stop_loss=1.91 immediately.
  ⚠️ NOTE: 1.89 has NOT been tested and is NOT confirmed Zombie D.
     Only exactly 1.90 is Zombie D. Testing 1.89 is PRIORITY 1.

- Zombie E: ~1,181 trades, Sharpe ~1.1013, win rate ~37.0% — ⚠️ HIGH-FREQUENCY TRAP
  Seen 10+ times in gens 1113–1131.
  FINGERPRINT: trades≈1181, sharpe≈1.1013, win_rate≈37.0%
  KNOWN CAUSE: RSI short threshold set too high (64–68 range),
               OR combined parameter changes that overtighten short entry
  ⛔ If you land here: DO NOT continue in the same direction.
     Revert RSI short to 60. Do not test RSI short > 63 without explicit instruction.

- Zombie F: ~1,353 trades, Sharpe ~1.39, win rate ~40.5% — ⚠️ NEWLY IDENTIFIED TRAP
  Seen at Gen 1187 (trades=1353, sharpe=1.3930, win_rate=40.5%)
  FINGERPRINT: trades significantly above 1,270, sharpe below 1.5, win_rate above 40%
  KNOWN CAUSE: RSI long threshold pushed above 39–40 increases trade count
               but destroys Sharpe by admitting lower-quality entries.
  ⛔ Do NOT push rsi_long_threshold above 38.5 under any circumstances.

- Champion Echo (NOT a zombie — but wastes a generation):
  ~1,266 trades, Sharpe ~2.2017, win_rate ~39.6%
  FINGERPRINT: trades≈1266, sharpe≈2.20 (NOT 2.2475)
  CAUSE: rsi_long = 37.82 (the Gen 1132 superseded champion value)
  ⛔ Do NOT propose rsi_long=37.82. It is a known non-improvement.

---

## Stagnation Detection — What To Do If Stuck

If 5+ consecutive generations produce Sharpe in the range 2.18–2.22 and are discarded:
  → The LLM is oscillating in the Champion Echo zone.
  → STOP testing RSI long axis for now.
  → Switch immediately to PRIORITY 1 (stop_loss = 1.89).
  → If stop_loss axis also fails: switch to PRIORITY 3 (take_profit).
  → Do NOT keep testing the same axis that is producing Champion Echo results.

If 3+ consecutive generations produce Zombie C (<400 trades):
  → STOP all RSI changes immediately.
  → Revert to exact Gen 1186 champion values.
  → On next generation, propose only a stop_loss or TP change (not RSI).

---

## Rules for the Small LLM — READ BEFORE PROPOSING ANY CHANGE

1. READ THE YAML FIRST. The YAML is the baseline. Do not use text descriptions
   as your starting point if they differ from the YAML.
2. PROPOSE EXACTLY ONE CHANGE per generation. Not two. Not zero. One.
3. CHECK your proposed value against all Zombie fingerprints before submitting.
4. CHECK your proposed value against the Champion Echo fingerprint.
5. NEVER change size_pct. It is fixed at 25.
6. NEVER change max_open without explicit instruction.
7. NEVER set stop_loss to exactly 1.90 (Zombie D).
8. NEVER set rsi_long above 38.5 or below 34.0.
9. NEVER set rsi_short above 63.
10. NEVER make RSI long changes larger than ±0.10 in a single generation.
11. ALWAYS verify that R:R ratio (take_profit / stop_loss) remains above 2.0.
12. If you are unsure what to change, use the Priority Order above (Priority 1 first).

---

## Current Best Strategy

```yaml
name: autobotswingfutures
style: swing_momentum
inspiration: "ODIN-injected champion — Gen 1186, corrected at Gen 1400 reset"
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
  timeout_hours: 166
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```
```