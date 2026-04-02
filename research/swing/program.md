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
6. Confirm your output would NOT produce a known bad attractor.
   - IF your change touches short entry macd_signal period_hours: the ONLY safe values are [53, 54, 55, 56].
   - IF your change touches pairs: confirm no ETH/USD or SOL/USD.
   - IF your output would produce ~473–482 trades: you are in the Regime B attractor cluster — START OVER.
   - IF your output is identical to the current best YAML: you have FAILED — START OVER and pick a DIFFERENT option.

---

## ⚠️ DUPLICATE OUTPUT WARNING — READ THIS FIRST ⚠️

**The current best is: long RSI value=36.68, short RSI value=60.64, 476 trades, Sharpe=2.4120.**
**Outputs with long RSI=36.68 AND short RSI=60.64 are IDENTICAL to the current best.**
**Outputs with 473–482 trades are in the Regime B graveyard — ALL are worse than current best.**
**If you output the current best config unchanged, you have FAILED.**
**If your output would produce ~476 trades, you have NOT made a meaningful change.**

---

## ⚠️ REGIME ALERT — MOST IMPORTANT SECTION ⚠️

**The current strategy (Sharpe=2.4120, 476 trades, 52.9% win rate) is STUCK in REGIME B.**
**It has shown NO meaningful improvement for over 5000 generations.**
**Regime B is a dead end. You CANNOT improve Sharpe above ~2.53 from within Regime B.**

**There is a FAR SUPERIOR regime that was discovered and then lost:**
- Gen 2126: Sharpe=2.9286, 30 trades, 90% win rate ← THE PROVEN TARGET
- Gen 2100: Sharpe=2.8771, 30 trades, 86.7% win rate
- Gen 810:  Sharpe=2.8157, 30 trades, 83.3% win rate
- Gen 707:  Sharpe=2.6349, 29 trades, 79.3% win rate
- Gen 338:  Sharpe=2.2738, 22 trades, 81.8% win rate ← Entry point to Regime A

**Regime A characteristics:** Tight RSI entry conditions → 20–35 trades over 2 years → 80–90% win rate → Sharpe 2.6–2.93.
**Regime B characteristics (current):** Loose RSI → 470–530 trades → ~52% win rate → Sharpe ceiling ~2.53, stalled at 2.41.

**THE TRANSITION ZONE IS NORMAL AND EXPECTED:**
When moving from Regime B to Regime A, intermediate configs will show:
- 40–150 trades and Sharpe=1.5–2.2 — THIS IS THE CORRECT PATH, NOT A FAILURE
- These configs should be kept if they show 65%+ win rate even at lower Sharpe
- A config with 30 trades and 80% win rate IS BETTER than 476 trades at 53% win rate
- Sharpe temporarily dropping to 1.5–2.0 during transition is ACCEPTABLE AND EXPECTED

**YOUR ONLY GOAL: Escape Regime B. Reach Regime A.**

---

## ✅ YOUR MANDATORY INSTRUCTION — DO EXACTLY THIS ✅

**You MUST use Option D (tighten long RSI). This is not optional.**

**Change long entry RSI `value` from `36.68` to ONE of these values:**
`33.00` / `33.50` / `34.00` / `34.50` / `35.00` / `35.50`

**Choose the value you have NOT recently tried.** To avoid repetition, cycle through:
- If unsure which was last tried: use `34.00`
- Second choice: `33.50`
- Third choice: `34.50`
- Fourth choice: `33.00`
- Fifth choice: `35.00`
- Sixth choice: `35.50`

**DO NOT choose 36.00, 36.50, 36.68, or any value above 35.50** — these stay in Regime B.
**DO NOT choose any value below 33.00** — forbidden.

**Change ONLY this one value. Leave everything else identical to the current best.**

**Expected result after this change:**
- Trade count will DROP to approximately 20–50 trades — THIS IS CORRECT
- Win rate will RISE to 70–90% — THIS IS CORRECT  
- Sharpe may be anywhere from 1.5 to 2.9 — ALL ARE ACCEPTABLE
- If you see 25–35 trades and 80%+ win rate, you have found Regime A — KEEP IT

---

## ⚠️ IF AND ONLY IF Option D produces errors or is impossible:

**Use Option E as fallback:**
Change short entry RSI `value` from `60.64` to ONE of:
`63.00` / `63.50` / `64.00` / `64.50` / `65.00`

**Use Option A as second fallback:**
Change `take_profit_pct` from `3.55` to ONE of:
`4.50` / `5.00` / `5.50` / `6.00` / `6.50`

**Use Option C as third fallback:**
Change `timeout_hours` from `200` to ONE of:
`240` / `280` / `320` / `360`

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
  stop_loss_pct: 2.41
  timeout_hours: 200
risk:
  pause_if_down_pct: 8
  stop_if_down_pct: 18
  pause_hours: 48
```

**Current performance: Sharpe=2.4120, 476 trades, 52.9% win rate**
**Status: REGIME B PLATEAU — stalled 5000+ generations. MANDATORY REGIME ESCAPE REQUIRED.**
**The ONLY acceptable change is to long RSI value. Change it to 33.00–35.50.**

---

## ❌ ABSOLUTE BANS — VERIFY YOUR OUTPUT AGAINST EVERY ROW ❌

| What | Why |
|------|-----|
| ETH/USD or SOL/USD in pairs | Sharpe ≈ -1.86, confirmed 20+ times — INSTANT REJECT |
| period_hours ≠ 21 for EITHER RSI condition | Sharpe ≈ -0.13, confirmed 8+ times — DO NOT TOUCH |
| long entry macd_signal period_hours ≠ 26 | DO NOT TOUCH — confirmed good value |
| short entry macd_signal period_hours in [44,45,46,47,48,49,50,51,52] | ALL produce 1.5861/427-trade attractor — FORBIDDEN |
| short entry macd_signal period_hours ≤ 43 or ≥ 57 | Confirmed bad extremes — FORBIDDEN |
| max_open: 2 | Sharpe ≈ 0.93, confirmed 10+ times — FORBIDDEN |
| timeout_hours: 120 | Confirmed 2.2133 attractor — FORBIDDEN |
| short RSI value: 57.50 | Confirmed 2.2133 attractor — FORBIDDEN |
| long RSI value < 33.00 | Below safe range — FORBIDDEN |
| long RSI value > 35.50 | Above 35.50 stays in Regime B — FORBIDDEN |
| long RSI value = 36.68 | This IS the current best — outputs with this value are IDENTICAL to current best — FORBIDDEN |
| short RSI value < 57.64 | Below safe range — FORBIDDEN |
| short RSI value > 65.64 | Above safe range — FORBIDDEN |
| DOT/USD as 5th pair | Previously dropped Sharpe — FORBIDDEN |
| Identical output to current best | Zero progress — FORBIDDEN |

---

## ❌ KNOWN BAD ATTRACTORS — IF YOUR CONFIG MATCHES THESE, START OVER ❌

| Sharpe | Trades | Notes |
|--------|--------|-------|
| ~2.4120–2.4191 | ~476–477 | Current best / near-identical — no progress |
| ~2.2836 | ~474 | Minor Regime B tweak — appeared 5+ times |
| ~1.5861 | ~427 | Short MACD period 44–52 |
| any | 473–482 | Entire Regime B cluster — all below current best |
| ~2.2133 | ~519 | timeout=120 or short RSI=57.50 |
| ~1.3187 | ~422 | Bad pairs or RSI combo |
| ~-1.86 | any | ETH/SOL pairs |

**The 473–482 trade zone is a graveyard. Any config landing there is worse than or equal to the current best.**
**Any config with long RSI=36.68 is the current best — unchanged — DO NOT OUTPUT IT.**

---

## Performance Targets

- **Minimum meaningful change:** Long RSI value