```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-2000 Update | Updated by MIMIR
# CRITICAL STATUS: Research stalled. Last improvement: Gen 1592. 400+ wasted generations.
# ROOT CAUSE: LLM failing to execute Priority 2 (stop_loss 1.91→1.89). Fix this first.

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions
MIN_TRADES: 400 (hard floor — any result with <400 trades is INVALID)
MIN_TRADES STATUS: ✅ CONFIRMED FIXED at gen 542. No action needed.

---

## ══════════════════════════════════════════════════════
## 🚨 GENERATION 2001+ DIRECTIVE — READ THIS FIRST 🚨
## ══════════════════════════════════════════════════════
##
## THIS IS YOUR ONLY JOB THIS GENERATION:
##
##   Find this line in the YAML:    stop_loss_pct: 1.91
##   Change it to:                  stop_loss_pct: 1.89
##   Change NO other line. Not one. Not timeout. Not RSI. Not TP.
##
## THIS IS PRIORITY 2. IT HAS NOT BEEN CLEANLY TESTED IN 400+ GENERATIONS.
## DO NOT PROCEED TO THE CHECKLIST UNTIL YOU HAVE UNDERSTOOD THIS.
##
## The ONLY valid output this generation (if champion YAML is unchanged):
##   stop_loss_pct: 1.89   ← changed
##   everything else       ← identical to champion
##
## If you are tempted to change anything else: DO NOT. STOP. Submit 1.89 only.
## ══════════════════════════════════════════════════════

---

## ⚠️ MANDATORY PRE-FLIGHT CHECKLIST — COMPLETE IN ORDER

Before writing your YAML, complete every step. Write your answer explicitly.

☐ STEP 1: Open the YAML. Find: timeout_hours: ___
           Write: "timeout_hours = [value]"
           It MUST be 159. If not: correct it to 159. That is your ONLY action.
           Do not change anything else.

☐ STEP 2: Write: "stop_loss_pct = [value from YAML]" — must be 1.91 in champion.

☐ STEP 3: Write: "rsi_long_threshold = [value from YAML]" — must be 37.77.

☐ STEP 4: Write: "size_pct = [value from YAML]" — must be 25. FROZEN. NEVER CHANGE.

☐ STEP 5: Write: "take_profit_pct = [value from YAML]" — must be 4.65.

☐ STEP 6: Write: "I am testing Priority 2: stop_loss_pct changing from 1.91 to 1.89"
           (If Priority 2 has already been tested this session and confirmed
           sub-optimal, write which priority you are on and what the change is.)

☐ STEP 7: Write: "My proposed change does NOT match any zombie fingerprint."
           Check ALL fingerprints in the zombie table below.

☐ STEP 8: Write: "I am changing EXACTLY ONE parameter: stop_loss_pct."
           Confirm: no other parameter differs from the champion YAML.

☐ STEP 9: Verify R:R: take_profit / stop_loss > 2.0
           Write: "R:R = 4.65 / 1.89 = 2.46. This is above 2.0. ✅"

☐ STEP 10: ANTI-CLONE CHECK.
            Write: "The parameter I changed is stop_loss_pct. Old: 1.91. New: 1.89."
            If you cannot write this honestly, DO NOT SUBMIT. Go back to Step 6.

Only after completing all 10 steps may you write your proposed YAML.

---

## ⚠️ YAML IS AUTHORITATIVE — DO NOT USE SUMMARY VALUES IF THEY CONFLICT

Champion values (Gen 1592 — CONFIRMED):
  - size_pct: 25                ← FROZEN. NEVER CHANGE. EVER.
  - stop_loss_pct: 1.91         ← Exactly 1.91. Your Priority 2 target: 1.89.
  - take_profit_pct: 4.65       ← Unchanged until Priority 3.
  - timeout_hours: 159          ← FROZEN. AXIS CLOSED. NEVER CHANGE.
  - rsi_long_threshold: 37.77   ← Exactly 37.77. Unchanged until Priority 5.
  - rsi_short_threshold: 60     ← Confirmed 60. Unchanged until Priority 4.
  - trend_period_hours: 48      ← Unchanged until Priority 6.
  - max_open: 3                 ← Do not change.
  - rsi_period_hours: 24        ← Unchanged until Priority 7.

---

## ⚠️ FROZEN PARAMETERS — DO NOT TOUCH THESE UNDER ANY CIRCUMSTANCES

| Parameter       | Value | Status                          |
|-----------------|-------|---------------------------------|
| size_pct        | 25    | FROZEN FOREVER                  |
| timeout_hours   | 159   | FROZEN — AXIS CLOSED            |
| rsi_long        | 37.77 | Frozen until Priority 5 opens   |
| rsi_short       | 60    | Frozen until Priority 4 opens   |
| trend_period    | 48    | Frozen until Priority 6 opens   |
| rsi_period      | 24    | Frozen until Priority 7 opens   |
| max_open        | 3     | Do not change                   |

These parameters produced the champion. Leave them alone until their
Priority axis is explicitly opened.

---

## ⚠️ TIMEOUT AXIS — PERMANENTLY CLOSED
timeout_hours = 159 is confirmed optimal. DO NOT CHANGE FOR ANY REASON.
- 155h → ~888 trades, Sharpe ~2.00 (CONFIRMED FAIL — Gens 1600, 1781)
- 166h → Ghost Echo (Sharpe=2.1998, trades=1264) — NEVER USE
- 159h → ✅ CHAMPION (FROZEN)

---

## Active Research Axes — PRIORITY ORDER

### 🔴 PRIORITY 2 — Stop Loss: 1.91 → 1.89 (YOUR CURRENT TARGET)
  STATUS: UNTESTED (400+ generations wasted without clean test)

  EXACT INSTRUCTION:
    Find:    stop_loss_pct: 1.91
    Replace: stop_loss_pct: 1.89
    Change NO other line.

  Expected profile if working correctly:
    - trades: near 1,267 (if trades drop below 1,000, revert)
    - sharpe: anywhere from 1.60 to 2.30+ (unknown — that's why we're testing)
    - win_rate: near 39–40%

  If 1.89 IMPROVES (Sharpe > 2.2657):
    → Next test: stop_loss_pct: 1.88 (floor — do not go below)
  If 1.89 FAILS (Sharpe ≤ 2.2657, trades ≥ 400):
    → Mark sub-optimal. Move to Priority 3.
  If 1.89 produces sharpe≈1.5918, trades≈1228:
    → You hit Zombie D-adjacent. Revert. Move to Priority 3.
  If 1.89 produces trades < 400:
    → Zombie C. Revert immediately. Move to Priority 3.

  ⚠️ NEVER USE 1.90 (Zombie D — confirmed, sharpe≈1.5918)
  ⚠️ NEVER USE below 1.88 (Zombie territory)
  ⚠️ NEVER USE above 1.97 (Zombie A territory)
  ⚠️ 1.89 is NOT a confirmed zombie. It is simply untested. Test it.

  SELF-VERIFY after writing YAML:
    stop_loss_pct: 1.89  ✅
    timeout_hours: 159   ✅ (unchanged)
    rsi_long: 37.77      ✅ (unchanged)
    take_profit_pct: 4.65 ✅ (unchanged)
    size_pct: 25         ✅ (unchanged)

---

### PRIORITY 3 — Take Profit: 4.65 → 4.70 (test after Priority 2 resolved)
  STATUS: UNTESTED from Gen 1592 baseline.

  EXACT INSTRUCTION:
    Find:    take_profit_pct: 4.65
    Replace: take_profit_pct: 4.70
    Change NO other line.

  R:R check: 4.70 / 1.91 = 2.46. ✅ Above 2.0.

  If 4.70 improves → test 4.75 next.
  If 4.70 fails → test 4.60 (exactly −0.05 from champion).
  If 4.60 fails → TP axis exhausted. Move to Priority 4.
  NEVER test TP below 4.50 (Zombie D territory).
  NEVER test TP above 5.20 without explicit instruction.
  CHANGE ONLY take_profit_pct.

---

### PRIORITY 4 — RSI Short: 60 → 59 (test after Priorities 2–3 resolved)
  STATUS: UNTESTED downward. Valid range: 55–63.

  EXACT INSTRUCTION:
    Find the short condition value: 60
    Change to: 59
    Change NO other line.

  If 59 improves → test 58 next.
  If 59 reduces trades below 1,100 → halt short axis.
  NEVER set RSI short below 55.
  NEVER set RSI short above 63 (Zombie E begins at 64).
  CHANGE ONLY rsi_short_threshold.

---

### PRIORITY 5 — RSI Long: 37.77 → 37.72 (SUSPENDED — test after P2, P3, P4)
  ⚠️ SUSPENSION ACTIVE: Multiple Zombie C events confirm LLM cannot safely
  handle RSI long changes without prior axes being resolved.

  When resumed:
    Find the long condition value: 37.77
    Change to: 37.72
    Change NO other line.

  Step size: ±0.05 ONLY. NEVER jump more than ±0.05.
  NEVER set RSI long below 34.0 (Zombie C territory).
  NEVER set RSI long above 38.5 (Zombie F territory — Gens 1787, 1789).

---

### PRIORITY 6 — Trend Period: 48 → 50 (LOW PRIORITY — after P2–P5)
  Current: 48h. Test: 50h ONLY.
  Valid range: 46h to 50h ONLY (narrowed — Gens 1787/1789 suggest danger above 50).
  If 50h fails → test 46h.
  CHANGE ONLY trend_period_hours.

---

### PRIORITY 7 — RSI Period: 24 → 22 (LAST RESORT — after P2–P6)
  Current: 24h. Test: 22h first. Step size: ±2h only.
  CHANGE ONLY rsi_period_hours.

---

## ⚠️ KNOWN ZOMBIE FINGERPRINTS — NEVER REPRODUCE

If your backtest result matches any fingerprint below, you hit a known failure.
Name it, identify the cause, and correct it next generation.

| Name            | Trades  | Sharpe  | Win Rate | Cause                                      |
|-----------------|---------|---------|----------|--------------------------------------------|
| Attractor 1     | 1,267   | 2.2657  | 39.9%    | Changed NOTHING. Clone of champion.        |
| Attractor 2     | 1,267   | 2.2336  | 39.6%    | Known sub-champion config. Wrong param.    |
| Attractor 3     | 1,272   | 2.2015  | 39.6%    | Known sub-champion. Seen 8+ times recent.  |
| Ghost Echo      | 1,264   | 2.1998  | 39.5%    | timeout=166 used instead of 159.           |
| Champion Echo   | ~1,266  | ~2.20   | ~39.5%   | rsi_long=37.82 used instead of 37.77.     |
| Zombie A        | ~1,230  | ~1.49   | ~38.0%   | stop_loss above 1.97%                      |
| Zombie B        | ~1,190  | ~1.02   | ~36.7%   | TP too low + loose stop                    |
| Zombie C        | <400    | deeply negative | any | RSI extreme, timeout too short, stop<1.88 |
| Zombie D        | ~1,228  | ~1.5918 | ~38.4%   | stop_loss=1.90 EXACTLY, or TP<4.5%        |
| Zombie E        | ~1,181  | ~1.10   | ~37.0%   | RSI short threshold 64–68                  |
| Zombie F        | ~1,353  | ~1.39   | ~40.5%   | RSI long above 38.5                        |
| Zombie G-adj    | ~888    | ~2.00   | any      | timeout=155h (confirmed Gens 1600, 1781)   |

⚠️ Attractor 3 (1272 trades, 2.2015 sharpe) is the most frequent recent failure.
   It has appeared in Gens 1983, 1984, 1987, 1990, 1995, 1996, 1998 and others.
   If you land here: you are NOT testing stop_loss=1.89. Check your YAML.

---

## ⚠️ PARAMETER DISAMBIGUATION (COMPLETE REFERENCE)

### STOP LOSS — Priority 2 axis
  Below 1.88  → ⛔ Zombie territory (NEVER USE)
  1.88        → Floor (only if 1.89 first improves)
  1.89        → ✅ Priority 2 target (UNTESTED — test now)
  1.90        → ⛔ Zombie D EXACTLY (NEVER USE)
  1.91        → ✅ Champion baseline
  1.93        → Previous champion (superseded)
  Above 1.97  → ⛔ Zombie A territory (NEVER USE)

### TAKE PROFIT — Priority 3 axis (locked until P2 resolved)
  Below 4.50  → ⛔ Zombie D territory
  4.60        → Fallback if 4.70 fails
  4.65        → ✅ Champion baseline
  4.70        → Priority 3 target
  4.75        → Test if 4.70 improves
  Above 5.20  → Do not test without instruction

### RSI LONG — Priority 5 axis (SUSPENDED)
  Below 34.0  → ⛔ Zombie C (NEVER USE)
  34.0–37.71  → Dangerous — ±0.05 steps only
  37.72       → Priority 5 target (suspended)
  37.77       → ✅ Champion baseline
  37.82       → ⛔ Champion Echo (superseded)
  Above 38.5  → ⛔ Zombie F territory (NEVER USE)

### RSI SHORT — Priority 4 axis (locked until P2–P3 resolved)
  Below 55    → ⛔ NEVER USE
  55–58       → Caution zone
  59          → Priority 4 target
  60          → ✅ Champion baseline
  61–63       → Valid but confirmed sub-optimal
  Above 63    → ⛔ Zombie E territory

### TIMEOUT HOURS — AXIS CLOSED
  155h → ⛔ FAIL (~888 trades, ~2.00 Sharpe)
  159h → ✅ CHAMPION (FROZEN — DO NOT CHANGE)
  166h → ⛔ Ghost Echo

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
- R:R ratio: 4.65/1.91 = 2.43:1 ✅

Previous champions (do not reproduce — superseded):
  Gen 670:  Sharpe=2.1852 | timeout=166
  Gen 939:  Sharpe=2.1972 | timeout=166
  Gen 1132: Sharpe=2.2017 | stop_loss=1.91 | rsi_long=37.82 | timeout=166
  Gen 1186: Sharpe=2.2475 | stop_loss=1.91 | rsi_long=37.77 | timeout=166
  Gen 1477: Sharpe=2.2496 | stop_loss=1.91 | rsi_long=37.77 | timeout=166
  Gen 1592: Sharpe=2.2657 | stop_loss=1.91 | rsi_long=37.77 | timeout=159 ← CURRENT

---

## ⚠️ RECENT DANGER EVENTS (Post-Gen-1592 through Gen-2000)

Gen 1593: Ghost Echo — timeout=166. Corrected.
Gen 1598: Zombie C (158 trades, Sharpe=-1.9761) — most severe failure.
Gen 1600: Zombie G-adj (887 trades, Sharpe=1.9865) — timeout=155h confirmed.
Gen 1781: Zombie G-adj (888 trades, Sharpe=2.0047) — timeout=155h confirmed.
Gen 1784: Attractor 1 (clone — nothing changed).
Gen 1786: Attractor 1 (clone — nothing changed).
Gen 1787: 1,451 trades, Sharpe=1.2606 — Zombie F-adjacent.
Gen 1789: 1,329 trades, Sharpe=1.1810 — Zombie F-adjacent.
Gen 1790: Attractor 1 (clone — nothing changed).
Gen 1791: Attractor 1 (clone — nothing changed).
Gen 1795: 1,234 trades, Sharpe=1.8266 — Zombie D-adjacent.
Gen 1799: 184 trades, Sharpe=-0.7999 — Zombie C.
Gen 1981: 940 trades, Sharpe=1.1462 — unknown cause (Zombie G-adj or trend change).
Gen 1982: 1,337 trades, Sharpe=1.5180 — Zombie D or TP-adjacent.
Gen 1983: Attractor 3 (1272 trades, Sharpe=2.2015).
Gen 1984: Attractor 3 (1272 trades, Sharpe=2.2015).
Gen 1985: 1,409 trades, Sharpe=1.3393 — Zombie F or RSI long pushed too high.
Gen 1986: Attractor 1 (clone — nothing changed).
Gen 1987: Attractor 3 (1272 trades, Sharpe=2.2015).
Gen 1988: Attractor 1 (clone — nothing changed).
Gen 1989: 1,339 trades, Sharpe=1.6526 — Zombie D-adjacent.
Gen 1990: Attractor 3 (1272 trades, Sharpe=2.2015).
Gen 1991: 55 trades, Sharpe=-5.0687 — Zombie C (catastrophic).
Gen 1992: 403 trades, Sharpe=-0.5880 — Zombie C-adjacent (barely above MIN_TRADES).
Gen 1993: 1,268 trades, Sharpe=2.1982 — Ghost Echo-adjacent or Champion Echo.
Gen 1994: 314 trades, Sharpe=-1.9477 — Zombie C (low trades).
Gen 1995: Attractor 3 (1272 trades, Sharpe=2.2015).
Gen 1996: Attractor 3 (1272 trades, Sharpe=2.2015).
Gen 1997: 1,268 trades, Sharpe=2.1708 — sub-champion (cause unknown).
Gen 1998: Attractor 3 (1272 trades, Sharpe=2.2015).
Gen 1999: 1,112 trades, Sharpe=1.3154 — Zombie G-adjacent or RSI shift.
Gen 2000: 1,340 trades, Sharpe=1.6627 — Zombie D or TP-adjacent.

SUMMARY: 400+ generations since last improvement. Priority 2 (stop_loss=1.89)
has NOT been cleanly tested. This is the #1 research gap. Fix it now.

---

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer: DANGER regime (F&G=16, Extreme Fear, VIX elevated).
Directive: Reduce LIVE position sizes to 25% of normal.
Effective live size: 25% × 25% ≈ 6.25% per position.
This does NOT affect backtest research. Do NOT change size_pct in research YAML.

---

## Current Best Strategy (YAML — AUTHORITATIVE)

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

## YOUR PROPOSED YAML FOR THIS GENERATION
Change ONLY stop_loss_pct from 1.91 to 1.89. Everything else identical.

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
  stop_loss_pct: 1.89
  timeout_hours: 159
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```