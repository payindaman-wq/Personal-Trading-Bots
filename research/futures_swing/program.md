```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-2200 | Revised by MIMIR for 8B model compliance
# STATUS: Champion unchanged since Gen 1592. Priority 2 (stop_loss=1.89) UNTESTED.
# ARCHITECTURE NOTE: If ODIN can inject YAML directly without LLM, do so for P2.

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor — results with <400 trades are INVALID)

---

## ██████████████████████████████████████████████████████████
## YOUR ONLY JOB THIS GENERATION — READ NOTHING ELSE FIRST
## ██████████████████████████████████████████████████████████

Take the YAML below. Make ONE change. Output the result.

FIND THIS LINE:     stop_loss_pct: 1.91
CHANGE IT TO:       stop_loss_pct: 1.89

Change NO other line. Not timeout. Not RSI. Not TP. Not size_pct.
If you change anything else, your output is wrong.

## ██████████████████████████████████████████████████████████

---

## CURRENT CHAMPION YAML (Gen 1592 — copy this exactly, change only stop_loss_pct)

```yaml
name: crossover
style: swing_momentum
inspiration: "ODIN-injected champion — updated at each sprint reset"
league: futures_swing
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
  size_pct: 25
  max_open: 3
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: up
    - indicator: rsi
      period_hours: 24
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24
      operator: gt
      value: 60
exit:
  take_profit_pct: 4.65
  stop_loss_pct: 1.91
  timeout_hours: 159
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

---

## YOUR OUTPUT MUST BE:

```yaml
name: crossover
style: swing_momentum
inspiration: "ODIN-injected champion — updated at each sprint reset"
league: futures_swing
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
  size_pct: 25
  max_open: 3
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: up
    - indicator: rsi
      period_hours: 24
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24
      operator: gt
      value: 60
exit:
  take_profit_pct: 4.65
  stop_loss_pct: 1.89
  timeout_hours: 159
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18
```

## VERIFY BEFORE SUBMITTING (3 checks only):

1. stop_loss_pct is 1.89 ✅
2. timeout_hours is 159 ✅
3. Every other line is identical to champion ✅

If any check fails: fix it. Do not submit until all 3 pass.

---

## WHAT TO EXPECT FROM BACKTEST

If correctly submitted (stop_loss=1.89, all else champion):
- trades: ~1,267 (acceptable range: 1,200–1,340)
- sharpe: unknown — could be 1.60 to 2.30+ (that is why we are testing)
- win_rate: ~39–40%

If result is sharpe=2.2657, trades=1267 → you submitted a clone. Fix and resubmit.
If result is sharpe=2.2015, trades=1272 → Attractor 3. You changed RSI or another param.
If result is sharpe=2.0047, trades=888 → timeout=155 was used. Fix it.
If result is sharpe≈1.59, trades≈1228 → Zombie D. Stop_loss was 1.90, not 1.89.
If result trades < 400 → Zombie C. Stop_loss went below 1.88 or RSI was changed.

---

## IF PRIORITY 2 HAS BEEN RESOLVED THIS SESSION

Priority 2 result outcomes and next steps:

IF stop_loss=1.89 IMPROVED (sharpe > 2.2657):
  → New champion. Next test: stop_loss_pct: 1.88 (floor — do not go below 1.88)
  → Change ONLY stop_loss_pct. Everything else champion.

IF stop_loss=1.89 FAILED (sharpe ≤ 2.2657, trades ≥ 400):
  → Mark 1.89 sub-optimal. Move to PRIORITY 3.
  → Find:    take_profit_pct: 4.65
  → Replace: take_profit_pct: 4.70
  → stop_loss_pct stays at 1.91 (champion). Change ONLY take_profit_pct.
  → R:R check: 4.70 / 1.91 = 2.46 ✅

IF stop_loss=1.89 produced trades < 400:
  → Zombie C. Move to PRIORITY 3 (take_profit test above).

---

## PRIORITY QUEUE (for reference only — do not act on these until P2 is resolved)

| Priority | Parameter          | Champion | Test Value | Constraint                    |
|----------|--------------------|----------|------------|-------------------------------|
| P2 ✅NOW | stop_loss_pct      | 1.91     | 1.89       | Floor=1.88. Never use 1.90.  |
| P3       | take_profit_pct    | 4.65     | 4.70       | Range: 4.50–5.20             |
| P4       | rsi_short_threshold| 60       | 59         | Range: 55–63                 |
| P5 SUSP  | rsi_long_threshold | 37.77    | 37.72      | SUSPENDED. Step ±0.05 only.  |
| P6       | trend_period_hours | 48       | 50         | Range: 46–50                 |
| P7       | rsi_period_hours   | 24       | 22         | Step ±2 only                 |

---

## FROZEN PARAMETERS — DO NOT CHANGE UNDER ANY CIRCUMSTANCES

| Parameter            | Value | Reason                                    |
|----------------------|-------|-------------------------------------------|
| size_pct             | 25    | FROZEN FOREVER                            |
| timeout_hours        | 159   | FROZEN — 155h=Zombie G, 166h=Ghost Echo   |
| max_open             | 3     | Do not change                             |

---

## KNOWN FAILURE FINGERPRINTS

| Name         | Trades | Sharpe  | Cause                                        |
|--------------|--------|---------|----------------------------------------------|
| Attractor 1  | 1,267  | 2.2657  | Clone — nothing changed                      |
| Attractor 3  | 1,272  | 2.2015  | RSI or other param drifted — most common fail|
| Ghost Echo   | 1,264  | 2.1998  | timeout=166 used                             |
| Zombie A     | ~1,230 | ~1.49   | stop_loss above 1.97                         |
| Zombie C     | <400   | negative| RSI extreme, stop<1.88, or timeout too short |
| Zombie D     | ~1,228 | ~1.5918 | stop_loss=1.90 EXACTLY. Never use 1.90.     |
| Zombie E     | ~1,181 | ~1.10   | rsi_short 64–68                              |
| Zombie F     | ~1,353 | ~1.39   | rsi_long above 38.5                          |
| Zombie G-adj | ~888   | ~2.00   | timeout=155h                                 |

⚠️ Attractor 3 (1272 trades, 2.2015) is the #1 failure mode in recent gens.
   It has appeared in Gens 2182, 2186, 2190, 2192 and 8+ times before that.
   If you land here: your YAML has a wrong value somewhere. Check all fields.

---

## CHAMPION SUMMARY (Gen 1592)

- Sharpe: 2.2657 | Win rate: 39.9% | Trades: 1,267
- Entry: trend(48h) + RSI(24h) mean-reversion
  - Long:  trend=up   AND RSI(24h) < 37.77
  - Short: trend=down AND RSI(24h) > 60
- Exit: TP=4.65%, SL=1.91%, timeout=159h
- Sizing: 25% per position, max_open=3, 2x leverage
- R:R: 4.65/1.91 = 2.43:1 ✅
- Risk guard: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR, APT, SUI, ARB, OP, ADA, POL)

DO NOT reproduce previous champions. Only Gen 1592 config is active.

---

## MACRO ENVIRONMENT NOTE (does NOT affect research YAML)

TYR Risk Officer: DANGER regime (F&G=16, Extreme Fear).
Live position sizing: 25% × 25% = 6.25% effective. Research size_pct stays at 25.

---

## ARCHITECTURE RECOMMENDATION FOR ODIN (MIMIR NOTE — NOT FOR LLM)

After 600+ failed generations, consider bypassing the LLM for Priority 2:
1. Directly inject YAML with stop_loss_pct=1.89 into the backtester.
2. If backtester accepts direct YAML input, this test can be resolved in 1 generation.
3. If LLM must be used, consider providing ONLY the diff and YAML — strip all
   historical context, zombie tables, and priority descriptions from the LLM prompt.
   The 8B model cannot reliably handle a 2000-token instruction document.
4. If Attractor 3 (1272/2.2015) continues to appear, fingerprint the exact YAML
   that produces it and add it as a hard-coded rejection in the backtest validator.
```