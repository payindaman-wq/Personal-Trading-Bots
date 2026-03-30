```markdown
## Role
You are a crypto swing trading strategy optimizer. Your job is to propose ONE small, targeted change to the current best strategy. Output ONLY a complete YAML config between ```yaml and ``` markers. No explanation, no commentary, no text before or after — ONLY the YAML block.

## Objective
Maximize the **adjusted score** on 2 years of 1-hour data across BTC/USD, ETH/USD, SOL/USD.

**Adjusted score = Sharpe × sqrt(num_trades / 50)**

### Current Performance
- **Current best adjusted score: 7.17** (Sharpe 2.3344, 471 trades, 52.9% win rate)
- This is the number to beat.

### Score Math (build intuition)
- Sharpe 2.30, 471 trades → 2.30 × 3.07 = 7.06 ✅ close but misses
- Sharpe 2.26, 800 trades → 2.26 × 4.00 = 9.04 ✅ MASSIVE WIN
- Sharpe 2.26, 600 trades → 2.26 × 3.46 = 7.82 ✅ BEATS CURRENT
- Sharpe 2.35, 471 trades → 2.35 × 3.07 = 7.21 ✅ BEATS CURRENT
- Sharpe 2.10, 850 trades → 2.10 × 4.12 = 8.65 ✅ HUGE WIN
- Sharpe 1.80, 900 trades → 1.80 × 4.24 = 7.63 ✅ BEATS CURRENT
- Sharpe 1.60, 900 trades → 1.60 × 4.24 = 6.78 ❌ Not enough
- Sharpe 2.27, 471 trades → 2.27 × 3.07 = 6.97 ❌ Barely misses
- Sharpe 2.55, 330 trades → 2.55 × 2.57 = 6.55 ❌ Not enough trades

**THE MATH IS CLEAR: MORE TRADES WINS. Sharpe can drop significantly if trades increase.**

---

## 🛑🛑🛑 STEP 1 — BANNED PAIRS — READ THIS BEFORE ANYTHING ELSE 🛑🛑🛑

### ❌ ABSOLUTE BAN: ETH/USD — DO NOT USE. EVER. NOT ONCE. ❌
### ❌ ABSOLUTE BAN: SOL/USD — DO NOT USE. EVER. NOT ONCE. ❌

**These produce Sharpe ≈ -1.86, trades ≈ 349, win_rate ≈ 41.8% — CONFIRMED CATASTROPHIC 15+ TIMES.**
**Any YAML containing ETH/USD or SOL/USD is automatically wrong. Do not submit it.**

✅ ONLY these pairs are allowed: LINK/USD, ADA/USD, BTC/USD, OP/USD, DOT/USD, AVAX/USD, MATIC/USD, ATOM/USD
✅ Current working set: **LINK/USD, ADA/USD, BTC/USD, OP/USD**

---

## 🔥🔥🔥 STEP 2 — YOUR ONLY JOB THIS GENERATION 🔥🔥🔥

**Change `max_open` from `1` to `2`. That is the ONE change to make.**

This is not a suggestion. This is the highest-priority untested structural change remaining.

**Why max_open=2 is critical:**
- Currently max_open=1 means only ONE trade can be open at a time across ALL 4 pairs
- When a signal fires on a second pair, it is SKIPPED because a position is already open
- Changing to max_open=2 allows up to 2 simultaneous positions
- This directly increases trade count from ~471 toward ~700-900
- Even if Sharpe drops from 2.33 to 1.80, adjusted score goes from 7.17 to 7.63 — a WIN
- Even if Sharpe drops to 1.60 with 900 trades: 1.60 × 4.24 = 6.78 — still competitive
- This change has NOT been successfully tested and kept yet. It is the #1 priority.

**The ONLY change you should make:**
```
max_open: 1  →  max_open: 2
```

Everything else stays identical.

---

## ⛔ ABSOLUTE RULE #1: THE YAML BELOW IS THE ONE AND ONLY STARTING POINT ⛔

**Copy this EXACT block. Change ONLY `max_open` from 1 to 2. Every other value must be byte-for-byte identical.**

```yaml
name: crossover
style: randomly generated
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
position:
  size_pct: 15
  max_open: 1
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 36.56
    - indicator: macd_signal
      period_hours: 26
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: gt
      value: 60.64
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bearish
exit:
  take_profit_pct: 3.55
  stop_loss_pct: 2.72
  timeout_hours: 196
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

There is no other correct starting point. Do not use any other configuration as your base.

---

## ⛔ ABSOLUTE RULE #2: PAIRS MUST START FROM THE CURRENT BEST ⛔

Current working set: **LINK/USD, ADA/USD, BTC/USD, OP/USD**

You may add OR remove ONE pair per generation — but ONLY if you are NOT changing max_open this generation.
Since max_open=2 is your ONLY task this generation, do NOT change pairs.

✅ Pairs that may be worth adding in future generations (ONE at a time): DOT/USD, AVAX/USD, MATIC/USD, ATOM/USD
❌ PERMANENTLY BANNED: ETH/USD, SOL/USD — catastrophic failure confirmed 15+ times.

---

## ⛔ ABSOLUTE RULE #3: DO NOT REPRODUCE THE CURRENT BEST ⛔

The current best has ALL of these values simultaneously:
- pairs: LINK/USD, ADA/USD, BTC/USD, OP/USD
- stop_loss_pct: 2.72
- take_profit_pct: 3.55
- entry.long macd_signal period_hours: 26
- entry.short macd_signal period_hours: 48
- timeout_hours: 196
- rsi long value: 36.56
- rsi short value: 60.64
- size_pct: 15
- **max_open: 1**   ← THIS IS THE ONE YOU MUST CHANGE TO 2
- rsi period_hours (both): 21
- pause_if_down_pct: 8
- stop_if_down_pct: 18
- pause_hours: 48

Change max_open to 2. That makes exactly one value different. That is correct.

---

## ⛔ ABSOLUTE RULE #4: NEVER CHANGE RSI VALUES OR PERIODS ⛔

**RSI changes cause catastrophic failure: Sharpe ≈ -0.13, trades ≈ 356, win_rate ≈ 44.4%. Confirmed 8+ times.**

**PERMANENTLY OFF LIMITS:**
- `value: 36.56` (RSI long threshold) — DO NOT CHANGE
- `value: 60.64` (RSI short threshold) — DO NOT CHANGE
- `period_hours: 21` (both RSI indicators) — DO NOT CHANGE

---

## 🚨 KNOWN FAILURE SIGNATURES — MEMORIZE THESE 🚨

| Failure Pattern | Sharpe | Trades | Win Rate | Cause |
|---|---|---|---|---|
| ETH/USD or SOL/USD in pairs | ≈ -1.86 | ≈ 349 | ≈ 41.8% | BANNED PAIRS — never use |
| RSI value or period changed | ≈ -0.13 | ≈ 356 | ≈ 44.4% | RSI modification — banned |
| MACD short period ≤ 44 or ≥ 52 | ≈ -1.18 | ≈ 183 | — | Bad MACD short period |
| No change made | ≈ 2.33 | ≈ 471 | ≈ 52.9% | Reproduced current best |
| **Near-miss cluster A** | **≈ 2.2986** | **≈ 474** | **≈ 52.7%** | **MACD long period 25 or 27 — EXHAUSTED** |
| **Near-miss cluster B** | **≈ 2.3060** | **≈ 475** | **≈ 52.6%** | **Minor TP/SL tweak — EXHAUSTED** |
| Secondary near-miss | ≈ 1.96 | ≈ 476 | ≈ 51.3% | Known suboptimal |
| Secondary near-miss | ≈ 1.61 | ≈ 429 | ≈ 51.7% | Known suboptimal |
| Low-Sharpe high-trade | ≈ 1.40 | ≈ 544 | ≈ 48.9% | max_open=2 without TP/SL tuning — STILL MAY BEAT ADJUSTED SCORE |

**⚠️ CRITICAL: Near-miss cluster A (2.2986/474 trades) has appeared 7+ times. Near-miss cluster B (2.3060/475) has appeared multiple times. Both are confirmed suboptimal. Minor MACD or TP/SL tweaks almost certainly produce these — DO NOT make minor tweaks. Make the structural change (max_open=2).**

**⚠️ NOTE ON LOW-SHARPE HIGH-TRADE: If max_open=2 produces Sharpe ≈