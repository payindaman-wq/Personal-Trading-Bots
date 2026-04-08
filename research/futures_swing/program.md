```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-1132 Update | Updated by MIMIR

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
if they conflict with the YAML. Current authoritative values (GEN 1132 CHAMPION):

  - size_pct: 25                ← DO NOT CHANGE
  - stop_loss_pct: 1.91         ← NOTE: 1.91. Not 1.9. Not 1.93. Exactly 1.91.
  - take_profit_pct: 4.65
  - timeout_hours: 166
  - rsi_long_threshold: 37.82
  - rsi_short_threshold: 60     ← CONFIRMED 60 (trades returned to 1,266)
  - trend_period_hours: 48
  - max_open: 3

⚠️ STOP_LOSS DISAMBIGUATION:
  - 1.9  → Zombie D (NEVER USE)
  - 1.91 → CURRENT CHAMPION (use this)
  - 1.93 → Previous champion stop loss (no longer current)
  - Below 1.88 → Zombie D territory (NEVER USE)
  - Above 1.97 → Zombie A/B territory (avoid)
  The operative stop loss is 1.91. Do not use any other value without explicit instruction.

⚠️ NOTE: size_pct = 25. Do NOT change size_pct under any circumstances.

---

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer has declared DANGER regime (F&G=17, Extreme Fear, VIX elevated).
Directive: Reduce live position sizes to 25% of normal.
For LIVE DEPLOYMENT ONLY: effective size = 25% × 25% ≈ 6.25% per position.
This does NOT affect backtest research — continue optimizing against historical data normally.
Do NOT change size_pct in the research YAML based on macro regime.

---

## Current Champion Summary (Gen 1132 — NEW CHAMPION)
- Sharpe: 2.2017 | Win rate: 39.6% | Trades: 1,266
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.82
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.91% stop-loss, 166h timeout
- Sizing: 25% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)
- R:R ratio: 4.65/1.91 = 2.43:1 (healthy — maintain above 2.0)

✅ GEN 1132 INSIGHT: Improvement came from stop_loss=1.91 (vs 1.93 previously),
   NOT from RSI short threshold changes. Trade count returned to 1,266 confirming
   RSI short = 60 is still operative. Stop loss fine-tuning is the active axis.

Previous champions for reference:
  Gen 939: Sharpe=2.1972 | Trades=1,259 | stop_loss=1.93 | rsi_short≈61
  Gen 670: Sharpe=2.1852 | Trades=1,266 | stop_loss=1.93 | rsi_short=60

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
  (Gens 524, 530, 534, 538, 597, 781, 787, 794, 922, 923, 927, 1117, 1120, 1128, 1131)
  Cause: RSI thresholds too extreme, timeout too short, excessive stop tightening
  Prevention: Never set RSI long < 34, RSI short > 67, timeout < 140h, stop_loss < 1.88

- Zombie D: ~1,228 trades, Sharpe ~1.5918, win rate ~38.4% — ⚠️ CRITICAL DANGER TRAP
  Seen 13+ times (gens 921, 928, 931, 932, 933, 938 and others)
  KNOWN CAUSE: stop_loss=1.9 (exactly 1.9, not 1.91 or 1.93)
               OR TP below 4.5%, OR stop below 1.88%
  FINGERPRINT: trades≈1228, sharpe≈1.5918, win_rate≈38.4%
  ⛔ If you land here: do NOT touch TP or stop loss further downward.
     Revert to stop_loss=1.91 immediately.

- Zombie E: ~1,181 trades, Sharpe ~1.1013, win rate ~37.0% — ⚠️ NEW HIGH-FREQUENCY TRAP
  Seen 10+ times in gens 1113–1131 alone. This is currently the most common trap.
  FINGERPRINT: trades≈1181, sharpe≈1.1013, win_rate≈37.0%
  KNOWN CAUSE: RSI short threshold set too high (likely 64–68 range),
               OR combined parameter changes that overtighten short entry
  ⛔ If you land here: DO NOT continue in the same direction.
     Revert RSI short to 60. Do not test RSI short > 63 without explicit instruction.

- Champion Echo — Gen 939 (NOT a zombie — recognize and avoid):
  ~1,259 trades, Sharpe ~2.1972, win rate ~39.6%
  This is the PREVIOUS-PREVIOUS champion. If you reproduce this, your change had no net
  effect or partially reverted parameters. Try stop_loss=1.91 with rsi_short=60.

- Champion Echo — Gen 1132 (NOT a zombie — recognize and avoid):
  ~1,266 trades, Sharpe ~2.2017, win rate ~39.6%
  This is the CURRENT champion. If you reproduce this exactly, your change had zero effect.
  Revert and test the next parameter on the active axis.

---

## ⚠️ SINGLE-CHANGE DISCIPLINE — CRITICAL RULE

RULES:
1. Change EXACTLY ONE parameter per generation. Never two. Never zero.
2. Make SMALL incremental adjustments:
   - RSI thresholds: ±1.0 per step (integer values only for RSI short)
   - TP/SL: ±0.02–0.05% per step (very small — the landscape is sensitive)
   - Timeout: ±5–10h per step
   - Trend period: ±2–4h per step
3. If the last 3 generations all failed OR reproduced a champion echo, switch axes.
4. Never change the same parameter as the immediately preceding generation
   unless it produced a new_best result.
5. If you cannot identify a fresh change, default to Phase 1 (stop_loss fine-tuning).

## ⚠️ POST-NEW-BEST RULE (CRITICAL)
When a new_best is found on a particular axis, the NEXT generation MUST test
the adjacent value on the SAME axis before switching to a different axis.
Example: Gen 1132 improved stop_loss → Gen 1133 MUST test stop_loss = 1.89 or 1.93.

## ⚠️ STOP LOSS DISCIPLINE
The stop loss is 1.91. This is NOT 1.9. Not 1.93. Exactly 1.91.
Never propose 1.9 — it maps directly to Zombie D.
Never propose below 1.88 — it maps to Zombie C/D territory.
If you are unsure of the stop loss value, use 1.91. Always.
Valid test range: 1.88 to 1.97 only. Outside this range = zombie territory.

---

## Priority Phases for Generations 1133–1232

---

### ⭐⭐ PHASE 1: Stop Loss Fine-Tuning — TOP