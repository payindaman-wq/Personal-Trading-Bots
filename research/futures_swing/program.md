```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-2400 | Revised by MIMIR
# STATUS: Champion unchanged since Gen 1592.
# CRITICAL: P2 (stop_loss=1.89) has NEVER been successfully tested in 800+ gens.
# ROOT CAUSE: LLM prompt overload causing Attractor 3, clones, and zombie outputs.
# FIX: Prompt compression. LLM sees ONLY the minimal diff section below.

## League: futures_swing
Timeframe: 1-hour candles, 7-day sprints
Leverage: 2x
Funding cost: ~0.01% per 8h
MIN_TRADES: 400 (hard floor)

---
## ██████████████████████████████████████████████████████████
## ODIN INJECTION NOTE (NOT FOR LLM — ODIN INTERNAL ONLY)
##
## MANDATORY ARCHITECTURE DIRECTIVE (MIMIR, Gen 2400):
## ► BYPASS THE LLM FOR P2. Inject the YAML below directly into the backtester.
## ► If direct injection is unavailable, send the LLM ONLY the "LLM PROMPT"
##   section below — nothing else. Strip all other sections from the LLM input.
## ► Do NOT send the priority queue, zombie table, or failure fingerprints
##   to the LLM. These cause Attractor 3. They are for ODIN/MIMIR review only.
## ► If Attractor 3 (1272 trades, 2.2015) appears again: reject immediately,
##   do not count as a valid generation, and retry with the stripped prompt.
##
## PRIORITY QUEUE (ODIN internal — never send to LLM):
## P2 NOW: stop_loss_pct 1.91 → 1.89
## P3:     take_profit_pct 4.65 → 4.70  (only if P2 fails)
## P4:     rsi_short_threshold 60 → 59
## P5 SUSP: rsi_long_threshold 37.77 → 37.72 (SUSPENDED)
## P6:     trend_period_hours 48 → 50
## P7:     rsi_period_hours 24 → 22
##
## KNOWN FAILURE FINGERPRINTS (ODIN validator — reject these automatically):
## Attractor 1:  trades=1267, sharpe=2.2657 → clone, nothing changed
## Attractor 3:  trades=1272, sharpe=2.2015 → RSI or param drifted (most common)
## Ghost Echo:   trades=1264, sharpe=2.1998 → timeout=166h used
## Zombie C:     trades<400               → RSI extreme or stop<1.88
## Zombie D:     trades≈1228, sharpe≈1.59 → stop_loss=1.90 (never use 1.90)
## Zombie G-adj: trades≈888,  sharpe≈2.00 → timeout=155h used
##
## FROZEN PARAMETERS (validator should hard-reject any YAML violating these):
## size_pct = 25 (FOREVER)
## timeout_hours = 159 (FOREVER — 155=ZombieG, 166=GhostEcho)
## max_open = 3
## leverage = 2
## fee_rate = 0.0005
##
## IF P2 RESOLVES THIS SESSION:
## P2 IMPROVED (sharpe > 2.2657): New champion. Next: stop_loss_pct=1.88 (floor).
## P2 FAILED (sharpe ≤ 2.2657, trades ≥ 400): Move to P3.
##   P3: take_profit_pct 4.65 → 4.70, stop_loss stays 1.91. R:R=4.70/1.91=2.46 ✅
## P2 trades<400: Zombie C. Move to P3.
##
## MACRO NOTE (does NOT affect research YAML):
## TYR: DANGER regime (F&G=16, Extreme Fear).
## Live sizing: 25% × 25% = 6.25% effective. Research size_pct stays 25.
## ██████████████████████████████████████████████████████████

---
## ══════════════════════════════════════════════════════════
## LLM PROMPT — SEND ONLY THIS SECTION TO THE LLM
## (Everything above and below this box is ODIN-internal only)
## ══════════════════════════════════════════════════════════

Take the YAML below. Make EXACTLY ONE change. Output ONLY the modified YAML.

THE CHANGE:
  Find:    stop_loss_pct: 1.91
  Replace: stop_loss_pct: 1.89

Change nothing else. No other line. Not timeout. Not RSI. Not take_profit. Not size_pct.

INPUT YAML:

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

EXPECTED OUTPUT (verify before submitting):

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

Before submitting, confirm:
1. stop_loss_pct is 1.89 ✅
2. timeout_hours is 159 ✅
3. take_profit_pct is 4.65 ✅
4. rsi value (long) is 37.77 ✅
5. rsi value (short) is 60 ✅

## ══════════════════════════════════════════════════════════
## END OF LLM PROMPT
## ══════════════════════════════════════════════════════════

---
## CHAMPION SUMMARY (Gen 1592) — ODIN REFERENCE

- Sharpe: 2.2657 | Win rate: 39.9% | Trades: 1,267
- Entry: trend(48h) + RSI(24h) mean-reversion
  - Long:  trend=up   AND RSI(24h) < 37.77
  - Short: trend=down AND RSI(24h) > 60
- Exit: TP=4.65%, SL=1.91%, timeout=159h
- Sizing: 25% per position, max_open=3, 2x leverage
- R:R: 4.65/1.91 = 2.43:1
- Risk guard: pause if down 8% (120 min), stop if down 18%
- Pairs: 16 (BTC, ETH, SOL, XRP, DOGE, AVAX, LINK, UNI, AAVE, NEAR,
          APT, SUI, ARB, OP, ADA, POL)
- Live performance: no completed sprints yet (autobotswingfutures)

DO NOT reproduce previous champions. Only Gen 1592 config is active.
```