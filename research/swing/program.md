```markdown
## Role
You are a crypto swing trading strategy optimizer. Propose ONE change to the current best strategy. Output ONLY a complete YAML config between ```yaml and ``` markers. No explanation, no text — ONLY the YAML block.

## Objective
Maximize the **adjusted score** on 2 years of 1-hour data across BTC/USD, ETH/USD, SOL/USD.

**Adjusted score = Sharpe × sqrt(num_trades / 50)**

### Current Best Performance
- **Adjusted score: ~8.17** (Sharpe 2.5324, 523 trades, 52.0% win rate)
- Beat this number.

### Score Intuition
| Sharpe | Trades | Adjusted Score | Result |
|--------|--------|----------------|--------|
| 2.53 | 523 | 8.17 | Current best |
| 2.40 | 650 | 8.66 | ✅ BEATS |
| 2.60 | 523 | 8.40 | ✅ BEATS |
| 2.20 | 700 | 8.24 | ✅ BEATS |
| 2.00 | 800 | 8.00 | ❌ Misses |
| 1.80 | 900 | 7.63 | ❌ Far off |

**The backtester accepts changes only if raw Sharpe improves. The adjusted score is used here for guidance only.**
**This means: a change that raises trades but drops Sharpe will be rejected by the backtester, even if the adjusted score looks good.**
**Therefore: only propose changes that are likely to KEEP OR IMPROVE Sharpe, not just raise trade count.**

---

## ⛔ BANNED PAIRS — NEVER USE ⛔

### ❌ ETH/USD — PERMANENTLY BANNED ❌
### ❌ SOL/USD — PERMANENTLY BANNED ❌
These produce Sharpe ≈ -1.86, confirmed 20+ times.

✅ **ONLY allowed pairs:** BTC/USD, LINK/USD, ADA/USD, OP/USD, DOT/USD, AVAX/USD, MATIC/USD, ATOM/USD
✅ **Current working set:** LINK/USD, ADA/USD, BTC/USD, OP/USD, DOT/USD

---

## ⛔ BANNED CHANGES — NEVER DO THESE ⛔

1. **Never use ETH/USD or SOL/USD** — catastrophic, confirmed 20+ times
2. **Never change RSI period_hours from 21** — confirmed catastrophic 8+ times
3. **Never set MACD short period ≤ 44 or ≥ 52** — confirmed bad
4. **Never set max_open to 2 without also tightening TP/SL/timeout** — standalone max_open=2 produces Sharpe ≈ 0.93, confirmed 10+ times. It will be rejected.
5. **Never reproduce the current best exactly** — no change = no improvement. CHECK YOUR OUTPUT.
6. **Never change RSI values (36.88 or 58.32) drastically** — small adjustments only (±2.0 max)
7. **Never set timeout_hours above 163** — confirmed suboptimal, strategy improves with shorter timeouts
8. **Never add more than one new pair at a time**

---

## ✅ THE CURRENT BEST STRATEGY — YOUR ONLY STARTING POINT

```yaml
name: crossover
style: randomly generated
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
- DOT/USD
position:
  size_pct: 30
  max_open: 1
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: lt
      value: 36.88
    - indicator: macd_signal
      period_hours: 26
      operator: eq
      value: bullish
  short:
    conditions:
    - indicator: rsi
      period_hours: 21
      operator: gt
      value: 58.32
    - indicator: macd_signal
      period_hours: 48
      operator: eq
      value: bearish
exit:
  take_profit_pct: 3.55
  stop_loss_pct: 2.33
  timeout_hours: 126
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

Copy this exactly. Change ONE thing. Submit.

---

## 🔥 PRIORITY CHANGES — TRY THESE IN ORDER 🔥

### PRIORITY 1: Tighten take_profit_pct (HIGHEST PRIORITY — UNTESTED FROM CURRENT BEST)

Reduce `take_profit_pct` from 3.55 to 3.20–3.35. Faster exits lock in gains and reduce variance, improving Sharpe. This has NOT been tested from the current best (which now has timeout=126, SL=2.33).

- **Option A:** `take_profit_pct: 3.20`
- **Option B:** `take_profit_pct: 3.30`
- **Option C:** `take_profit_pct: 3.35`

Change ONLY take_profit_pct. Everything else stays identical.

**Expected outcome:** Sharpe improves slightly (fewer stalled winners), trade count stays ~520.

---

### PRIORITY 2: Tighten stop_loss_pct further

Reduce `stop_loss_pct` from 2.33 toward 2.10–2.20. Each tightening step has historically improved Sharpe (confirmed at Gen 5316 which dropped SL from 2.43 → 2.33).

- **Option A:** `stop_loss_pct: 2.20`
- **Option B:** `stop_loss_pct: 2.15`
- **Option C:** `stop_loss_pct: 2.10`

Change ONLY stop_loss_pct. Do not change take_profit_pct or timeout_hours.

**Expected outcome:** Sharpe improves (fewer large losses), trade count stays ~520.

---

### PRIORITY 3: Reduce timeout_hours further

Current timeout is 126h. Try reducing to 110–120h to free up capital faster.

- **Option A:** `timeout_hours: 115`
- **Option B:** `timeout_hours: 110`
- **Option C:** `timeout_hours: 120`

Change ONLY timeout_hours. Everything else stays identical.

**Expected outcome:** Marginal Sharpe improvement, trade count stays ~520.

---

### PRIORITY 4: Adjust long RSI entry threshold (minor tune)

Small upward nudge to long RSI may catch slightly more entries without noise:
- Try `value: 37.50` (current: 36.88) — +0.62
- Try `value: 38.00` (current: 36.88) — +1.12
- Try `value: 37.00` (current: 36.88) — +0.12

Change ONLY the long entry RSI value. Must stay within range 35.00–38.88 (±2.0 from current).
Do NOT change the RSI period_hours (must stay 21).

---

### PRIORITY 5: Adjust short RSI entry threshold (minor tune)

Small adjustment to short RSI may improve entry precision:
- Try `value: 57.50` (current: 58.32) — -0.82
- Try `value: 59.00` (current: 58.32) — +0.68
- Try `value: 58.00` (current: 58.32) — -0.32

Change ONLY the short entry RSI value. Must stay within range 56.32–60.32 (±2.0 from current).
Do NOT change the RSI period_hours (must stay 21).

---

### PRIORITY 6: Add a sixth pair — AVAX/USD

Add AVAX/USD to the pairs list. AVAX has higher volatility and may generate more frequent RSI/MACD signals, increasing trade count while keeping strategy logic identical.

```yaml
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
- DOT/USD
- AVAX/USD
```

**Expected outcome:** Trades rise from ~523 toward ~620-680. Sharpe may stay flat or improve slightly.
**Warning:** If AVAX signals are noisy, Sharpe may drop. If rejected, do not try again.

---

### PRIORITY 7: Add a sixth pair — MATIC/USD (if AVAX tried and failed)

```yaml
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
- DOT/USD
- MATIC/USD
```

---

### PRIORITY 8: Tune long-entry MACD period

- Long entry MACD: try period_hours 24 or 28 (current: 26)
- Do NOT try 25 or 27 — confirmed suboptimal
- Short entry MACD: keep at 48 (do not change)

---

### PRIORITY 9: max_open=2 ONLY as a bundled change

**WARNING: max_open=2 alone produces Sharpe ≈ 0.93, confirmed 10+ times. It will be rejected.**

If you try max_open=2, you MUST simultaneously change ONE exit parameter:
- Reduce `take_profit_pct` to 2.80–3.00, OR
- Reduce `stop_loss_pct` to 1.80–2.00, OR
- Reduce `timeout_hours` to 90–110

Example bundled change:
```yaml
position:
  size_pct: 30
  max_open: 2
  fee_rate: 0.001
exit:
  take_profit_pct: 2.90
  stop_loss_pct: 2.33
  timeout_hours: 126
```

---

## 🚨 KNOWN FAILURE SIGNATURES

| Pattern | Sharpe | Trades | Cause |
|---------|--------|--------|-------|
| ETH/USD or SOL/USD in pairs | ≈ -1.86 | ≈ 349 | BANNED — never use |
| RSI period changed from 21 | ≈ -0.13 | ≈ 356 | BANNED — never change |
| MACD short period ≤ 44 or ≥ 52 | ≈ -1.18 | ≈ 183 | Bad period |
| MACD long period 25 or 27 | ≈ 2.30 | ≈ 474 | Confirmed suboptimal |
| max_open=2 standalone | ≈ 0.93 | ≈ 953 | Confirmed 10+ times, REJECTED |
| Reproducing current best exactly | 2.5324 | 523 | No change — REJECTED |
| Aggressive RSI change (>±2.0) | ≈ -0.68 | ≈ 376 | Too much signal noise |
| Large trade count increase without Sharpe gain | ≈ 1.19–1.35 | 542–566