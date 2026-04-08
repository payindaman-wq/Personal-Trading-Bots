```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-939 Update | Updated by MIMIR

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
if they conflict with the YAML. Current authoritative values (GEN 939 CHAMPION):

  - size_pct: 25
  - stop_loss_pct: 1.93        ← NOTE: 1.93, NOT 1.9. Do NOT use 1.9 anywhere.
  - take_profit_pct: 4.65
  - timeout_hours: 166
  - rsi_long_threshold: 37.82
  - rsi_short_threshold: ???   ← UNKNOWN: Gen 939 improved this but exact value
                                  not confirmed. Inferred ~61 based on trade count
                                  drop (1,266→1,259). BEGIN TESTING FROM 62.
  - trend_period_hours: 48
  - max_open: 3

⚠️ STOP_LOSS DISAMBIGUATION: The program previously stated 1.9 in the summary
but 1.93 in the YAML. The YAML is authoritative. The operative stop loss is 1.93.
Never propose 1.9 — it leads directly to Zombie D.

⚠️ NOTE: size_pct = 25. Do NOT change size_pct.

---

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer has declared DANGER regime (F&G=17, Extreme Fear, VIX elevated).
Directive: Reduce live position sizes to 25% of normal.
For LIVE DEPLOYMENT ONLY: effective size = 25% × 25% ≈ 6.25% per position.
This does NOT affect backtest research — continue optimizing against historical data normally.
Do NOT change size_pct in the research YAML based on macro regime.

---

## Current Champion Summary (Gen 939 — NEW CHAMPION after 269-generation stall)
- Sharpe: 2.1972 | Win rate: 39.6% | Trades: 1,259
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.82
  - Short: trend=down AND RSI > ~61 (inferred; exact value TBD — test 62 next)
- Exit: 4.65% take-profit, 1.93% stop-loss, 166h timeout
- Sizing: 25% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)
- R:R ratio: 4.65/1.93 = 2.41:1 (healthy — maintain above 2.0)

✅ BREAKTHROUGH: Gen 939 confirmed RSI short threshold axis IS productive.
   Trade count dropped 1,266→1,259 (fewer, better-quality shorts).
   Win rate rose 39.5%→39.6%. Sharpe rose 2.1852→2.1972.
   This validates the Phase 1 hypothesis. CONTINUE THIS AXIS IMMEDIATELY.

Previous champion for reference (Gen 670):
  Sharpe: 2.1852 | Win rate: 39.5% | Trades: 1,266
  RSI short threshold: 60

---

## Known Zombie Configurations — NEVER REPRODUCE THESE

The LLM repeatedly rediscovers these sub-optimal states. If your proposed change
leads to one of these, STOP immediately and choose a COMPLETELY DIFFERENT parameter.
Do NOT attempt incremental improvement from a zombie state.

- Zombie A: ~1,230 trades, Sharpe ~1.49, win rate ~38.0% (Gens 523, 528, 529, 539)

- Zombie B: ~1,190 trades, Sharpe ~1.02, win rate ~36.7% (Gens 535, 537, 540)

- Zombie C: <400 trades, Sharpe deeply negative
  (Gens 524, 530, 534, 538, 597, 781, 787, 794, 922, 923, 927)
  → Caused by: RSI thresholds too extreme, timeout too short, excessive stop tightening,
    or stop loss set to exactly 1.9 instead of 1.93
  → Prevention: Never set RSI long < 34, RSI short > 70, timeout < 140h,
    or stop_loss to exactly 1.9

- Zombie D: ~1,228 trades, Sharpe ~1.5918, win rate ~38.4% — ⚠️ CRITICAL DANGER TRAP
  Seen 13+ times total including gens 921, 928, 931, 932, 933, 938
  This is the most dangerous and frequent trap.
  Fingerprint: trades=1228, sharpe≈1.5918, win_rate≈38.4%
  KNOWN CAUSE: TP reduction (below 4.5%), stop tightening (below 1.8%),
               OR accidentally using stop_loss=1.9 instead of 1.93
  ESCAPE RULE: If you land here, the ONLY valid action is to continue testing
  RSI SHORT threshold. Do NOT touch TP or stop loss. Do NOT use stop_loss=1.9.

- Champion Echo (NOT a zombie — recognize and avoid):
  ~1,266 trades, Sharpe ~2.1852, win rate ~39.5%
  This is the PREVIOUS champion (gen 670). If you reproduce this, your proposed
  RSI short change had no effect (probably set it back to 60). Revert and test 62.
  Seen in gens 786, 791, 796, 798, 926, 930, 934, 935 — DO NOT REPRODUCE.

- New Champion Echo (NOT a zombie — recognize and avoid):
  ~1,259 trades, Sharpe ~2.1972, win rate ~39.6%
  This is the CURRENT champion (gen 939). If your change reproduces this exactly,
  your change had zero effect. Revert and test the next RSI short value.

---

## ⚠️ SINGLE-CHANGE DISCIPLINE — CRITICAL RULE

RULES:
1. Change EXACTLY ONE parameter per generation. Never two.
2. Make SMALL incremental adjustments:
   - RSI thresholds: ±0.5–1.0 per step (integers preferred for RSI short)
   - TP/SL: ±0.1–0.2% per step
   - Timeout: ±5–10h per step
3. If the last 3 generations all failed OR reproduced a champion echo, switch axes.
4. Never change the same parameter type as the immediately preceding generation
   unless it produced a new_best result.
5. If you cannot identify a fresh change, default to Phase 1 (RSI short threshold = 62).

## ⚠️ POST-NEW-BEST RULE (CRITICAL — NEW)
When a new_best is found on a particular axis, the NEXT generation MUST test
the adjacent value on the SAME axis before switching to a different axis.
This prevents abandoning a productive direction prematurely.
Example: Gen 939 improved RSI short → Gen 940 MUST test RSI short = 62.

## ⚠️ STOP LOSS DISCIPLINE
The stop loss is 1.93. This is NOT 1.9. Never propose 1.9.
The difference between 1.9 and 1.93 is small but maps directly to Zombie D.
If you are unsure of the stop loss value, use 1.93. Always.

---

## Priority Phases for Generations 940–1040

---

### ⭐⭐ PHASE 1: RSI Short Threshold — TOP PRIORITY (CONFIRMED PRODUCTIVE)
# GEN 939 PROVED THIS WORKS. CONTINUE IMMEDIATELY.

Current short entry: trend=down AND RSI > ~61 (gen 939 champion, inferred)
Gen 939 improved Sharpe from 2.1852 → 2.1972 by tightening RSI short threshold.
The next step is to continue climbing: test RSI short = 62, 63, 64, 65, 66.

WHY THIS MATTERS:
- Crypto is historically bull-biased. RSI > 60 in a downtrend is too permissive.
- Tightening requires stronger overbought confirmation before shorting.
- Gen 939 confirmed: fewer shorts → higher quality → better Sharpe.
- Expected: continued trade count reduction, win rate climbing toward 40%+.

TARGET VALUES — test STRICTLY in this order, ONE per generation:
  Gen 940: RSI short = 62   ← START HERE. Do not skip.
  Gen 941: RSI short = 63
  Gen 942: RSI short = 64
  Gen 943: RSI short = 65
  Gen 944: RSI short = 66
  Gen 945: RSI short = 67   (extend if trend continues improving)
  Gen 946: RSI short = 68   (extend if trend continues improving)

Expected trade count signatures (approximate):
  RSI short = 62: ~1,240–1,255 trades
  RSI short = 63: ~1,220–1,245 trades
  RSI short = 64: ~1,200