```markdown
# ODIN Research Program — FUTURES DAY (v6)

## League: futures_day
Timeframe: 5-minute candles, 24h sprints
Leverage: 2x (multiplies both gains and losses)
Funding cost: ~0.01% per 8h on open positions (applied automatically in backtest)
Liquidation: positions force-closed if loss exceeds 45% of margin at 2x leverage

---

## ⚠️ LOKI CONSTANT — APPLY THIS IMMEDIATELY BEFORE ANY PROPOSAL

```
MIN_TRADES["futures_day"] = 450
```

The current constant is 400. It must be 450. Apply this change via LOKI now.
Every generation below 450 trades is automatically invalid. Do not propose configs
that produce fewer than 450 trades. If uncertain, loosen RSI thresholds first.

---

## ████████████████████████████████████████████████
## ⚠️ CRITICAL: WE HAVE BEEN STUCK SINCE GEN 702 ⚠️
## 577 GENERATIONS. ZERO REAL PROGRESS. READ THIS.
## ████████████████████████████████████████████████

The research has produced only 16 improvements in 1279 generations.
Since Gen 702, the best Sharpe has moved from −4.0842 to −4.0815.
That is not progress. That is a stall.

The last 20 generations show 12 of 19 runs rejected for low trade count.
The small LLM is broken in a loop. New instructions are mandatory.

**THE TWO THINGS THAT MATTER:**
1. Trade count ≥ 450 (ideally 580–700). Below this = garbage, always.
2. The 60-minute timeout is destroying returns. It must be fixed.

**THE ONE THING THAT IS CONFIRMED:**
The current champion uses `timeout_minutes: 60`. This is a known structural flaw.
It has not been fixed in 700+ generations. Every generation from here forward
must attempt to fix it. Not eventually. NOW. Every single proposal.

---

## ⚠️ CRITICAL SITUATION REPORT

**All-time champion: Gen 702/792/1279 — Sharpe −4.08, 618 trades, 44.3% WR**
**Previous: Gen 541 — Sharpe −4.29, 605 trades, 43.8% WR**
**Pattern: HIGH TRADE COUNT (580+) = BETTER SHARPE. This is non-negotiable.**

Trade count vs Sharpe evidence:
- 600+ trades → Sharpe range: −4.08 to −4.29 (best results)
- 400–599 trades → Sharpe range: −5.4 to −7.3 (mediocre)
- 200–399 trades → Sharpe range: −8 to −40 (garbage, always rejected)
- 0–199 trades → Sharpe = −999 (invalid)

**Every proposal must target 580+ trades. Accept nothing below 450.**

---

## CONFIRMED DEAD ENDS — NEVER REPEAT

### Entry Conditions
- RSI period > 14: reduces trades, no benefit. Use period 14 only.
- RSI long threshold < 42: reduces trades below 450. BANNED.
- RSI short threshold > 62: reduces trades below 450. BANNED.
- Adding any 3rd entry condition: ALWAYS kills trade count. BANNED.
- Removing pairs: ALWAYS hurts trade count. Use all 16 pairs always.
- Trend period > 20min: reduces signals too much. BANNED.

### Exit Conditions
- **timeout_minutes > 30: BANNED. Confirmed primary cause of negative Sharpe.**
- **timeout_minutes = 60: THE ENEMY. The current champion has this flaw.**
  Every proposal must use timeout ≤ 25 minutes.
- TP/SL changes without fixing timeout first: documented failure pattern.

### Position Sizing
- size_pct ≠ 13.64: DO NOT CHANGE. The champion uses 16.68 (inherited flaw).
  Normalize to 13.64 in all new proposals.
- max_open ≠ 2: DO NOT CHANGE.
- fee_rate ≠ 0.0005: DO NOT CHANGE.

### What The Small LLM Keeps Doing Wrong (do not repeat)
1. Tightening RSI to 38/40/42 for longs. STOP. Kills trade count.
2. Using RSI period 20. STOP. Use 14 only.
3. Setting timeout > 25 minutes. STOP. Hard limit is 25min.
4. Adding a 3rd entry condition. STOP. Never.
5. Using fewer than 16 pairs. STOP. All 16 always.
6. Changing size_pct from 13.64. STOP.
7. Making random TP/SL micro-changes while ignoring timeout. STOP.
8. Short RSI threshold < 55. STOP. RSI > 55 minimum for short signal.
9. Proposing configs with < 450 trades. STOP. Wasted generation.

---

## MANDATORY BASE CONFIGURATION

Non-negotiable. Every proposal must start from these parameters.

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

---

## CURRENT CHAMPION — CONFIRMED FLAWS

```yaml
# Current champion — Sharpe −4.08, 618 trades, 44.3% WR
# DO NOT clone this verbatim. Fix the flaws listed below.
entry:
  long:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: up
    - indicator: rsi
      period_minutes: 20   # FLAW: Use 14
      operator: lt
      value: 38            # FLAW: Too tight. Use 44 minimum.
  short:
    conditions:
    - indicator: trend
      period_minutes: 15
      operator: eq
      value: down
    - indicator: rsi
      period_minutes: 20   # FLAW: Use 14
      operator: gt
      value: 38            # FLAW: Not an overbought signal. Use 56 minimum.
exit:
  take_profit_pct: 1.37
  stop_loss_pct: 0.85
  timeout_minutes: 60      # ████ PRIMARY FLAW. MUST BE ≤ 25. ████
risk:
  pause_if_down_pct: 5
  pause_minutes: 30
  stop_if_down_pct: 12
```

**Why timeout=60 is the enemy:**
- A 60-minute timeout allows losing trades to bleed for up to 60 minutes.
- At 5-minute candles, that is 12 more candles of potential drawdown.
- The stop_loss_pct=0.85% is nominal but timeout overrides it in trending moves.
- Result: actual realized losses far exceed 0.85%, destroying Sharpe.
- Fix: timeout=20 cuts losing trades at 4 candles, protecting capital.

**Why the math still works at timeout=20:**
- TP=1.37%, SL=0.85% → R:R = 1.61x
- Breakeven WR at 1.61x R:R = 38.3% (before fees), ~39.5% after fees
- Current WR = 44.3% → 4.8 percentage points ABOVE breakeven
- Even if timeout=20 reduces trade count to 500, Sharpe should improve
  because losing trades are cut faster.

---

## GENERATION ASSIGNMENTS — STRICT SEQUENCE

### ████ IMMEDIATE PRIORITY: ONE CHANGE ONLY ████

**The next generation MUST be this exact config. No other changes.**

```yaml
# PROPOSAL FOR NEXT GENERATION — CHANGE ONLY timeout_minutes
name: crossover_timeout_fix
style: momentum_scalper
league: futures_day
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
  size_pct: 13.64
  max_open: 2
  fee_rate: 0.0005
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
  take_profit_pct: 1.37
  stop_loss_pct: 0.85
  timeout_minutes: 20
risk:
  pause_if_down_pct: 5
  pause_minutes: 30
  stop_if_down_pct: 12
```

**This config simultaneously fixes:**
- timeout 60 → 20 (primary fix)
- RSI period 20 → 14 (secondary fix, more trades)
- RSI long 38 → 44 (more long signals, more trades)
- RSI short 38 → 56 (meaningful overbought filter)
- size_pct 16.68 → 13.64 (normalized)

**Expected outcome:** 550–700 trades, WR ~42–45%, Sharpe should exceed −4.08
if the timeout fix works as theorized. If trade count falls below 450, widen
RSI thresholds: long to lt 46, short to gt 54.

---

### BLOCK 1: Timeout Fix Verification (Next 20 Generations)

**Goal:** Confirm the timeout fix improves Sharpe. Test variants around the
base fix config. Change ONE parameter per generation. Always keep timeout ≤ 25.

**Ordered test sequence — one per generation:**

1. RSI 44/56 + TP 1.37% / SL 0.85% / timeout 20min  ← PRIMARY FIX (above