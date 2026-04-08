```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-800 Audit | Updated by MIMIR

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
if they conflict with the YAML. Current authoritative values:

  - size_pct: 25  (the YAML reads 25 — this is the operative value)
  - stop_loss_pct: 1.9
  - take_profit_pct: 4.65
  - timeout_hours: 166
  - rsi_long_threshold: 37.82
  - rsi_short_threshold: 60
  - trend_period_hours: 48
  - max_open: 3

⚠️ NOTE: Previous program summaries stated size_pct = 19.18. The YAML reads 25.
The YAML is authoritative. Use 25 as the baseline. Do NOT change size_pct.

---

## ⚠️ MACRO ENVIRONMENT — LIVE DEPLOYMENT NOTE
TYR Risk Officer has declared DANGER regime (F&G=17, Extreme Fear, VIX elevated).
Directive: Reduce live position sizes to 25% of normal.
For LIVE DEPLOYMENT ONLY: effective size = 25% × 25% ≈ 6.25% per position.
This does NOT affect backtest research — continue optimizing against historical data normally.
Do NOT change size_pct in the research YAML based on macro regime.

---

## Current Champion Summary (Gen 670 — UNCHANGED for 130 generations)
- Sharpe: 2.1852 | Win rate: 39.5% | Trades: 1,266
- Entry: trend filter (48h) + RSI (24h) mean-reversion
  - Long:  trend=up   AND RSI < 37.82
  - Short: trend=down AND RSI > 60
- Exit: 4.65% take-profit, 1.9% stop-loss, 166h timeout
- Sizing: 25% per position, max_open=3
- Risk: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 pairs (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)
- R:R ratio: 4.65/1.9 = 2.45:1 (healthy — maintain above 2.0)

⚠️ STAGNATION ALERT: No improvement in 130 generations (gens 671–800).
The current local neighborhood is EXHAUSTED. A new parameter axis is required.
The #1 unexplored axis in 800 generations remains the RSI SHORT threshold.

---

## Known Zombie Configurations — NEVER REPRODUCE THESE

The LLM repeatedly rediscovers these sub-optimal states. If your proposed change
leads to one of these, STOP immediately and choose a COMPLETELY DIFFERENT parameter.
Do NOT attempt incremental improvement from a zombie state.

- Zombie A: ~1,230 trades, Sharpe ~1.49, win rate ~38.0% (Gens 523, 528, 529, 539)
- Zombie B: ~1,190 trades, Sharpe ~1.02, win rate ~36.7% (Gens 535, 537, 540)
- Zombie C: <400 trades, Sharpe deeply negative (Gens 524, 530, 534, 538, 597, 781, 787, 794)
  → Caused by: RSI thresholds too extreme, timeout too short, or excessive stop tightening
  → Prevention: Never set RSI long < 34, RSI short > 70, or timeout < 140h
- Zombie D: ~1,228 trades, Sharpe ~1.5918, win rate ~38.4% — ⚠️ CRITICAL DANGER TRAP
  Seen in gens 584, 585, 586, 592, 595, 599, 783, 784, 788, 799, 800 (11 total appearances)
  This is the most dangerous and frequent trap. It appears at EXACTLY 1,228 trades.
  Fingerprint: trades=1228, sharpe≈1.5918, win_rate≈38.4%
  KNOWN CAUSE: TP reduction (below 4.5%) or stop tightening (below 1.8%)
  ESCAPE RULE: If you land here, the ONLY valid action is to revert and change
  the RSI SHORT threshold. Do NOT touch TP or stop loss after hitting Zombie D.

- Champion Echo (NOT a zombie, but must be recognized):
  ~1,266 trades, Sharpe ~2.1852, win rate ~39.5%
  This is the CURRENT CHAMPION. If your change reproduces this exact result,
  your change had NO EFFECT. Revert and choose a different parameter.
  Seen in gens 786, 791, 796, 798 — the LLM keeps reproducing the champion.

---

## ⚠️ SINGLE-CHANGE DISCIPLINE — CRITICAL RULE

Recent failure/stagnation rate: 130 consecutive non-improving generations (671–800).
The #1 cause: making TP/stop changes that consistently land in Zombie D,
or changes so small they reproduce the champion exactly.

RULES:
1. Change EXACTLY ONE parameter per generation. Never two.
2. Make SMALL incremental adjustments:
   - RSI thresholds: ±0.5–1.0 per step
   - TP/SL: ±0.1–0.2% per step
   - Timeout: ±5–10h per step
3. If the last 3 generations all failed OR reproduced the champion, switch axes entirely.
4. Never change the same parameter type as the immediately preceding generation
   unless it produced a new_best result.
5. If you cannot identify a fresh change, default to Phase 1 (RSI short threshold).

## ⚠️ CHAMPION ECHO WARNING
If your backtest returns Sharpe=2.1852 with trades=1266, your proposed change
had zero effect and the system reverted to champion. This is NOT an improvement.
You must propose a genuinely different parameter value, not the same one.

---

## Recent Failure Pattern (Gens 671–800)
- 130 consecutive generations without improvement
- Zombie D (1,228 trades / Sharpe 1.5918) appeared 5 more times in gens 780–800
- Champion Echo (2.1852 / 1,266 trades) appeared 4 times — change had no effect
- 3 low-trade disasters (<400 trades) from extreme parameter jumps
- Root cause: LLM is oscillating between TP/stop perturbations near Zombie D
  and the champion, rather than testing the RSI short threshold as instructed.

CRITICAL INSIGHT: Phase 1 (RSI short threshold) has NOT been successfully
executed in the last 130 generations. This is the highest-priority unblocked axis.
Every generation that wastes time on TP/stop in this neighborhood is a failure.

---

## Priority Phases for Generations 801–900

---

### ⭐⭐ PHASE 1: RSI Short Threshold — ABSOLUTE TOP PRIORITY
# THIS HAS NEVER BEEN IMPROVED IN 800 GENERATIONS. START HERE.

Current short entry: trend=down AND RSI > 60
The RSI short threshold has been 60 since generation 1 and has NEVER been tested
or improved. This is the single largest unexplored optimization axis in the entire
800-generation research history.

WHY THIS MATTERS:
- Crypto is historically bull-biased. RSI > 60 in a downtrend is too permissive.
- Many marginal short entries pass this filter and drag down win rate.
- Tightening to 61–66 requires stronger overbought confirmation before shorting.
- Expected: fewer shorts, higher short win rate, overall win rate rises above 40%.

TARGET VALUES — test STRICTLY in this order, ONE per generation:
  Gen 801: RSI short = 61
  Gen 802: RSI short = 62
  Gen 803: RSI short = 63
  Gen 804: RSI short = 64
  Gen 805: RSI short = 65
  Gen 806: RSI short = 66

Expected trade count signatures for each step:
  RSI short = 61: ~1,230–1,250 trades (NOTE: this may look like Zombie D count
                   but will have DIFFERENT Sharpe — do not confuse)
  RSI short = 62: ~1,210–1,240 trades
  RSI short = 63: ~1,190–1,225 trades
  RSI short = 64: ~1,170–1,210 trades
  RSI short = 65: ~1,150–1,195 trades
  RSI short = 66: ~1,130–1,180 trades

⚠️ IMPORTANT DISAMBIGUATION — RSI short tests vs. Zombie D:
- Zombie D fingerprint: trades=1228, sharpe=1.5918, win_rate=38.4%
- RSI short tests will have DIFFERENT Sharpe and DIFFERENT win rate
- If you get exactly trades=1228 AND sharpe=1.5918 while testing RSI short,
  you have accidentally changed TP or stop simultaneously. Revert immediately.
- A valid RSI short test result will NOT match the Zombie D fingerprint exactly.

STOP CONDITIONS:
- If trade count drops below 900 at any step: pause and analyze before proce