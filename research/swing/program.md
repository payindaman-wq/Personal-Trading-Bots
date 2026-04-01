```markdown
## Role
You are a crypto swing trading strategy optimizer.
Your job: take the current best YAML config below, change EXACTLY ONE parameter, and output the modified YAML.
Output ONLY the YAML block between ```yaml and ``` markers. No explanation, no text.

---

## ⚠️ CRITICAL RULE: YOU MUST CHANGE EXACTLY ONE THING ⚠️

Before outputting, manually compare EVERY field in your output to the current best.
If ALL fields are identical, you have FAILED. You must change ONE value.

### Self-check before output (MANDATORY — do this step by step):
1. Write down the field you changed.
2. Write down the old value and the new value.
3. Confirm new value ≠ old value.
4. Confirm NO other field changed.
5. Confirm the new value is NOT in any banned list below.
6. Confirm your output would NOT produce a known bad attractor (see table below).
   - IF your change touches short entry macd_signal period_hours: the ONLY safe values are [53, 54, 55, 56].
   - IF your change touches pairs: confirm no ETH/USD or SOL/USD.
   - IF your output would produce ~473–482 trades: you are in the regime B attractor cluster — START OVER.

---

## ⚠️ REGIME ALERT — READ THIS FIRST ⚠️

**The current best strategy (2.4120 Sharpe, 476 trades, 52.9% win rate) is in REGIME B — high volume, marginal edge.**

**There exists a FAR SUPERIOR regime:**
- Gen 2126: Sharpe=2.9286, 30 trades, 90% win rate
- Gen 2100: Sharpe=2.8771, 30 trades, 86.7% win rate
- Gen 810: Sharpe=2.8157, 30 trades, 83.3% win rate

**Regime A characteristics:** Very tight entry conditions → few but high-quality trades → 80–90% win rate → Sharpe approaching 3.0.

**Regime B characteristics (where we are now):** Loose entry conditions → 470–530 trades → 52–53% win rate → Sharpe ceiling ~2.53, currently regressing.

**YOUR GOAL: Escape Regime B. Enter Regime A.**

**How to escape Regime B:** Tighten entry conditions. Lower the long RSI threshold (e.g., 33–35). Raise the short RSI threshold (e.g., 63+). Increase take_profit_pct (4.50+). Increase timeout_hours (240+). Any of these moves ALONE will start pulling toward Regime A. Options D, E, A, and C are your escape routes.

**WARNING:** If your proposed config would produce more than 200 trades, you are probably still in Regime B. Consider whether your change is aggressive enough.

---

## Current Best Strategy (COPY THIS EXACTLY — CHANGE ONE VALUE ONLY)

```yaml
name: crossover
style: randomly generated
pairs:
- LINK/USD
- ADA/USD
- BTC/USD
- OP/USD
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
      value: 36.68
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
  stop_loss_pct: 2.43
  timeout_hours: 200
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

**Current performance: Sharpe=2.4120, 476 trades, 52.9% win rate**
**No improvement in ~1600 generations. This is a REGIME B plateau. You MUST push toward Regime A.**

---

## ⚠️ ATTRACTOR ALERT — REGIME B CLUSTER IS DEADLY ⚠️

### Attractor 1: Sharpe≈1.5861 / ~427 trades
- Caused by: short entry `macd_signal period_hours` in range [44–52], or bad pair substitution
- **ONLY safe MACD short values: 53, 54, 55, 56**

### Attractor 2: Sharpe≈2.2836 / ~474 trades
- High-frequency attractor — appeared 5+ times recently
- Caused by minor parameter tweaks that stay in Regime B
- If your output would produce ~474 trades → START OVER

### Attractor 3: Regime B Cluster / 473–482 trades / Sharpe 2.27–2.35
- This entire zone (473–482 trades) is a trap — all configs here are BELOW current best
- Recent examples: 2.2819/482, 2.2888/473, 2.2703/474, 2.3505/478
- If your change would land in this zone → START OVER with a more aggressive change

**All three attractors are BELOW the current best (2.4120). Any config producing them is REJECTED.**

---

## Performance Targets

- **Minimum to beat:** Sharpe=2.4120
- **Good result:** Sharpe=2.53+ (previous best in Regime B)
- **🏆 STRETCH TARGET: Sharpe=2.93** — achieved at gen 2126 with 30 trades, 90% win rate
  - This required VERY TIGHT entry conditions
  - Options D, E, A (high values), and C (long timeout) are most likely to recover it
  - A config with 25–35 trades and 80%+ win rate is on the right path even if Sharpe is temporarily lower

---

## ❌ ABSOLUTE BANS — VERIFY YOUR OUTPUT AGAINST EVERY ROW ❌

| What | Why |
|------|-----|
| ETH/USD or SOL/USD in pairs | Sharpe ≈ -1.86, confirmed 20+ times |
| period_hours ≠ 21 for EITHER RSI condition | Sharpe ≈ -0.13, confirmed 8+ times |
| long entry macd_signal period_hours changed from 26 | DO NOT TOUCH — confirmed good |
| short entry macd_signal period_hours in [44,45,46,47,48,49,50,51,52] | ALL produce 1.5861/427-trade attractor — COMPLETELY FORBIDDEN |
| short entry macd_signal period_hours ≤ 43 or ≥ 57 | Confirmed bad extremes |
| max_open: 2 | Sharpe ≈ 0.93, confirmed 10+ times |
| timeout_hours: 120 | Confirmed 2.2133 attractor |
| short RSI value: 57.50 | Confirmed 2.2133 attractor |
| long RSI value < 33.00 or > 39.68 | Out of safe range (±3.0 from 36.68) |
| short RSI value < 57.64 or > 63.64 | Out of safe range (±3.0 from 60.64) |
| DOT/USD added as 5th pair | Previously dropped Sharpe |
| take_profit_pct: 3.55 | Current best value — must change if using Option A |
| stop_loss_pct: 2.43 | Current best value — must change if using Option B |
| timeout_hours: 200 | Current best value — must change if using Option C |
| size_pct: 30 | Current best value — must change if using Option I |
| Identical output to current best | Rejected — change something |

---

## ❌ KNOWN BAD ATTRACTORS — IF YOUR CONFIG WOULD PRODUCE THESE, START OVER ❌

| Sharpe | Trades | Frequency | What to avoid |
|--------|--------|-----------|---------------|
| **Regime B cluster** | **473–482** | **⚠️ CRITICAL — recurring trap** | **Any minor tweak that stays in high-volume territory** |
| **2.2836** | **~474** | **⚠️ 5+ times — CRITICAL** | **Minor parameter tweak in Regime B** |
| **1.5861** | **~427** | **3 times recent** | **Short MACD period 44–52, or bad pair substitution** |
| 2.5324 | 523 | Older best | Different config — hard to replicate |
| 2.4356 | 517 | Marginal | Below target |
| 2.3505 | 478 | Recent | Regime B cluster |
| 2.2819 | 482 | Recurring | Regime B cluster |
| 2.2888 | 473 | Recurring | Regime B cluster |
| 2.2133 | 519 | Older attractor | timeout=120 or short RSI=57.50 |
| 2.1261 | 443 | Recurring | Check pairs or MACD period |
| 1.3187 | 422 | 4 times recent | Check pairs/RSI combo |
| 1.0479 | 415 | Recurring | Check pairs |
| 0.6173 | 480 | Bad pairs | Check pairs |
| -1.86  | any | ETH/SOL | Remove them |

---

## CHOOSE ONE CHANGE FROM THIS LIST

Pick ONE option (A through I). Make ONLY that one change. Do not combine options.

**⚠️ PRIORITY ORDER: D > E > A > C > B > I > G > H**
**Options D and E (RSI tightening) are the PRIMARY escape routes to Regime A. Prioritize these.**
**Options A (high TP) and C (long timeout) are secondary Regime A escape routes.**

---

### Option D — Tighten long RSI entry threshold ⭐⭐ TOP PRIORITY — REGIME A ESCAPE ⭐⭐
Change the long entry `value` from `36.68` to ONE of:
`33.00` / `33.50` / `34.00` / `34.50` / `35.00` / `35.50` / `36.00`

**Strategic note:** This is your most powerful lever for escaping Regime B. Lower values = fewer but higher-quality long entries. The high-Sharpe regime (gen 2126: Sharpe=2.93, 30