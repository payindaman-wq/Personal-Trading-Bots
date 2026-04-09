```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-1200 Update | Updated by MIMIR

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
if they conflict with the YAML. Current authoritative values (GEN 1186 CHAMPION):

  - size_pct: 25                ← DO NOT CHANGE
  - stop_loss_pct: 1.91         ← Exactly 1.91. Not 1.9. Not 1.89. Not 1.93.
  - take_profit_pct: 4.65
  - timeout_hours: 166
  - rsi_long_threshold: 37.77   ← NEW CHAMPION VALUE. Not 37.82. Exactly 37.77.
  - rsi_short_threshold: 60     ← CONFIRMED 60 (trades = 1,265–1,266)
  - trend_period_hours: 48
  - max_open: 3

⚠️ RSI LONG DISAMBIGUATION:
  - 37.82 → Gen 1132 champion value (superseded)
  - 37.77 → CURRENT CHAMPION (use this as baseline)
  - Changes must be ±0.05 increments ONLY (e.g., 37.72, 37.82)
  - Never jump more than ±0.10 from 37.77 in a single generation
  - Values below 34.0 → Zombie C territory (causes low_trades, NEVER USE)
  - Gen 1194 failure (185 trades) was almost certainly caused by RSI long pushed too low

⚠️ STOP_LOSS DISAMBIGUATION:
  - 1.90  → Zombie D (NEVER USE — confirmed trap at exactly 1.90)
  - 1.91  → CURRENT CHAMPION (use this as baseline)
  - 1.89  → UNTESTED ADJACENT — HIGH PRIORITY to test
  - 1.93  → Previous champion stop loss (superseded, but not a zombie)
  - Below 1.88 → Zombie C/D territory (NEVER USE)
  - Above 1.97 → Zombie A/B territory (avoid)
  - The only valid test range is 1.88 to 1.97. Outside = zombie territory.

⚠️ NOTE: size_pct = 25. Do NOT change size_pct under any circumstances.
⚠️ NOTE: rsi_period_hours = 24. Do not change RSI period until RSI long/short axes
         are confirmed exhausted. When testing, use 22h or 26h only (±2h steps).

---

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer has declared DANGER regime (F&G=17, Extreme Fear, VIX elevated).
Directive: Reduce live position sizes to 25% of normal.
For LIVE DEPLOYMENT ONLY: effective size = 25% × 25% ≈ 6.25% per position.
This does NOT affect backtest research — continue optimizing against historical data normally.
Do NOT change size_pct in the research YAML based on macro regime.

---

## Current Champion Summary (Gen 1186 — NEW CHAMPION)
- Sharpe: 2.2475 | Win rate: 39.6% | Trades: 1,265
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.77
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.91% stop-loss, 166h timeout
- Sizing: 25% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)
- R:R ratio: 4.65/1.91 = 2.43:1 (healthy — maintain above 2.0)

✅ GEN 1186 INSIGHT: Improvement came from rsi_long_threshold = 37.77 (vs 37.82 previously).
   This is a fractional RSI tightening that reduced entry noise on longs.
   Trade count held steady at 1,265 (vs 1,266 prior) — minimal disruption.
   RSI long fine-tuning in ±0.05 increments is the CONFIRMED active axis.

Previous champions for reference:
  Gen 670:  Sharpe=2.1852 | Trades=1,266 | stop_loss=1.93 | rsi_long=37.82 | rsi_short=60
  Gen 939:  Sharpe=2.1972 | Trades=1,259 | stop_loss=1.93 | rsi_long≈37.82 | rsi_short≈61
  Gen 1132: Sharpe=2.2017 | Trades=1,266 | stop_loss=1.91 | rsi_long=37.82 | rsi_short=60
  Gen 1186: Sharpe=2.2475 | Trades=1,265 | stop_loss=1.91 | rsi_long=37.77 | rsi_short=60 ← CURRENT

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
  ⚠️ Gen 1194 (185 trades) is a confirmed new Zombie C instance — almost certainly caused
     by RSI long pushed too far below 37.77 (likely < 35) in a single large jump.
     NEVER change RSI long by more than ±0.10 per generation.

- Zombie D: ~1,228 trades, Sharpe ~1.5918, win rate ~38.4% — ⚠️ CRITICAL DANGER TRAP
  Seen 13+ times (gens 921, 928, 931, 932, 933, 938 and others)
  KNOWN CAUSE: stop_loss = 1.9 EXACTLY
               OR TP below 4.5%, OR stop below 1.88%
  FINGERPRINT: trades≈1228, sharpe≈1.5918, win_rate≈38.4%
  ⛔ If you land here: do NOT touch TP or stop loss further downward.
     Revert to stop_loss=1.91 immediately.
  ⚠️ NOTE: 1.89 has NOT been tested yet and is NOT confirmed as Zombie D.
     Only exactly 1.90 is Zombie D. Testing 1.89 is permitted and HIGH PRIORITY.

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
  KNOWN CAUSE: Loosening RSI long threshold (pushing above 39–40) increases trade count
               but destroys Sharpe by admitting lower-quality entries.
  ⛔ Do NOT push rsi_long_threshold above 38.5.

- Champion Echo — Gen 1132 (NOT a zombie — recognize and avoid):
  ~1,266 trades, Sharpe ~2.