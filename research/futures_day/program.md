```markdown
# ODIN Research Program — FUTURES DAY (v5)

## League: futures_day
Timeframe: 5-minute candles, 24h sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (applied automatically in backtest)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage

---

## ⚠️ CRITICAL SITUATION REPORT — READ EVERY WORD BEFORE PROPOSING ANY CHANGE

**Gen 541 just achieved Sharpe −4.29 with 605 trades — the best result in 541
generations. The pattern is now proven beyond doubt:**

**HIGH TRADE COUNT (500+) = BETTER SHARPE. This is the single most important
variable in this entire research program. Do not forget it.**

**All-time champion: Gen 541 — Sharpe −4.29, 605 trades, 43.8% WR**
**Previous best: Gen 140 — Sharpe −6.15, 623 trades, 41.7% WR**
**Both champions share one trait: 600+ trades. Every strategy below 400 trades
has Sharpe worse than −7. Every strategy below 300 trades has Sharpe worse than −12.**

**YOUR SOLE OBJECTIVE: Produce 500+ trades while fixing the structural flaws
identified in the Gen 541 champion. The fixes are listed below. Apply them
one at a time, in order. Do not skip ahead.**

---

## ⚠️ MANDATORY CONSTANT CHANGE (APPLY IMMEDIATELY VIA LOKI)

```
MIN_TRADES["futures_day"] = 450
```

**Rationale:** The current floor of 200 allows the LLM to pollute the generation
history with statistically meaningless 200–300 trade runs. Every result below 400
trades has been garbage. Raising the floor to 450 forces valid proposals only.
Any generation below 450 trades must be automatically rejected as low_trades.

---

## CONFIRMED DEAD ENDS — DO NOT REPEAT ANY OF THESE — EVER

### Entry Conditions
- RSI period > 14 (period 20 tested extensively, reduces trade count, no benefit)
- RSI thresholds < 42 for long entry (38, 40, 42 — ALL EXHAUSTED, reduce trades)
- Adding volume, pivot, or any 3rd entry condition: ALWAYS reduces trades below 500
- Removing pairs: ALWAYS hurts trade count and Sharpe
- Tightening stop_loss by ±0.1–0.2% in isolation: NEVER improved Sharpe

### Exit Conditions
- **timeout_minutes > 30: PERMANENTLY BANNED. The 60-minute timeout is the
  confirmed primary cause of negative Sharpe. It allows losers to bleed past
  the stop-loss. Never propose timeout > 30 under any circumstances.**
- TP 1.39% / SL 0.85% / timeout 60min: the Gen 541 champion config — has structural
  flaws (wrong timeout, wrong RSI period) — do not clone it, fix it

### What The Small LLM Keeps Doing Wrong (do not repeat these mistakes)
1. **Tightening RSI thresholds** (going to 38, 40, 42). STOP. Reduces trade count.
2. **Using RSI period 20**. STOP. Use period 14 only.
3. **Setting timeout > 30 minutes**. STOP. Max timeout is 25 minutes.
4. **Adding a 3rd entry condition when stuck**. STOP. Always kills trade count.
5. **Reducing pairs below 16**. STOP. Use all 16 pairs always.
6. **Changing size_pct away from 13.64**. STOP. Do not touch position sizing.
7. **Making ±0.1% TP/SL changes while keeping timeout at 60min**. STOP. The timeout
   is the problem, not the TP/SL when timeout is 60min.
8. **Short entry RSI threshold matching long entry (e.g., rsi gt 38)**. STOP.
   Short entry requires RSI > 55 minimum to mean anything as an overbought filter.

---

## MANDATORY BASE CONFIGURATION

**Non-negotiable. Every proposal must use exactly these parameters as the base.**

```yaml
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
  size_pct: 13.64      # DO NOT CHANGE
  max_open: 2          # DO NOT CHANGE
  fee_rate: 0.0005     # DO NOT CHANGE
```

**TRADE COUNT REQUIREMENT: Any strategy producing fewer than 450 trades is
automatically rejected. If your proposed change reduces trades below 450, the
proposal is invalid. Loosen conditions until trades ≥ 450.**

---

## CURRENT CHAMPION — STRUCTURAL FLAW ANALYSIS

Gen 541's winning config has confirmed flaws. The next block of generations (542–570)
must fix these flaws one at a time to extract the true potential of this config:

```yaml
# Gen 541 champion — DO NOT USE THIS VERBATIM, FIX IT AS DIRECTED BELOW
entry:
  long:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: up
    - indicator: rsi
      period_minutes: 20   # FLAW 1: Should be 14
      operator: lt
      value: 38            # FLAW 2: Too restrictive, reduces trades
  short:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: down
    - indicator: rsi
      period_minutes: 20   # FLAW 1: Should be 14
      operator: gt
      value: 38            # FLAW 3: RSI > 38 is not an overbought signal
exit:
  take_profit_pct: 1.39
  stop_loss_pct: 0.85
  timeout_minutes: 60      # FLAW 4: BANNED. Must be ≤ 25.
```

**Identified flaws in priority order:**
1. `timeout_minutes: 60` — HIGHEST PRIORITY FIX. Replace with 20.
2. `rsi period_minutes: 20` — Replace with 14 (more signals, more trades).
3. `short rsi gt 38` — Replace with `gt 58` (meaningful overbought filter).
4. `long rsi lt 38` — Replace with `lt 44` (more long signals, more trades).
5. `size_pct: 17.0` — Must be normalized to 13.64 per base config.

---

## GENERATION ASSIGNMENTS — MANDATORY SEQUENCE

### BLOCK 1: Fix the Gen 541 Champion (Generations 542–570)

**Goal:** Apply the four structural fixes to Gen 541 one at a time. Keep TP 1.39%
and SL 0.85% while fixing entry and timeout first, then explore TP/SL adjustments.
Keep trade count above 500 at all times.

**Start here — Generation 542 (highest priority fix):**
```yaml
entry:
  long:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: up
    - indicator: rsi
      period_minutes: 14
      operator: lt
      value: 44
  short:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: down
    - indicator: rsi
      period_minutes: 14
      operator: gt
      value: 56
exit:
  take_profit_pct: 1.39
  stop_loss_pct: 0.85
  timeout_minutes: 20    # THE KEY FIX
risk:
  pause_if_down_pct: 5
  pause_minutes: 30
  stop_if_down_pct: 12
```

**Variants to test in order (one per generation, 542–570):**

*Phase 1: Fix timeout only, vary entry thresholds*
1. RSI 44/56 + TP 1.39% / SL 0.85% / timeout 20min  ← start here
2. RSI 44/56 + TP 1.39% / SL 0.85% / timeout 15min
3. RSI 44/56 + TP 1.39% / SL 0.85% / timeout 25min
4. RSI 46/54 + TP 1.39% / SL 0.85% / timeout 20min  (looser → more trades)
5. RSI 42/58 + TP 1.39% / SL 0.85% / timeout 20min

*Phase 2: Best timeout from Phase 1 + adjust TP/SL for scalp R:R*
6. RSI 44/56 + TP 0.9% / SL 0.5% / timeout 20min   (scalp R:R 1.8x)
7. RSI 44/56 + TP 0.8% / SL 0.5% / timeout 20min   (scalp R:R 1.6x)
8. RSI 44/56 + TP 1.0% / SL 0.55% / timeout 20min  (moderate scalp)
9. RSI 44/56 + TP 1.1% / SL 0.6% / timeout 20min
10. RSI 44/56 + TP 0.8% / SL 0.45% / timeout 15min  (tightest scalp)

*Phase 3: Best TP/SL/timeout from Phase 2 + fine-tune*
11. Best config ± 0.05% TP, same SL and timeout
12. Best config, same TP, ± 0.05% SL
13. Best config ± 3min timeout
14. Best config with RSI 45/55 (symmetric, slightly looser)
15. Best config with RSI 43/57

*Phase 4: Trend period variation*
16. Best config with trend period 10min (shorter → more signals)
17. Best config with trend period 20min (longer → fewer but cleaner signals)
18. Best config with trend period 30min

**If any variant exceeds −4.29 Sharpe:** immediately mine ±0.05% around its
TP/SL and ±2min around its timeout before moving to Block 2.

---

### BLOCK 2: Scalp Mode — Short Timeout Focus (Generations 571–600)

**Mathematical basis:**
- At TP 0.8% / SL 0.5%, R:R = 1.6x → breakeven WR = 38.5% (after fees ≈ 39.5%)
- Current WR is consistently 41–44% → ABOVE breakeven
- With timeout 15–20min, most trades resolve at TP or SL before timeout bleed
- Expected trade count: 500–700

**Primary target:**
```yaml