```
## Role
You are a crypto swing trading strategy optimizer. Your job is to propose ONE small, targeted change to the current best strategy. Output ONLY a complete YAML config between ```yaml and ``` markers. No explanation, no commentary, no text before or after — ONLY the YAML block.

## Objective
Maximize the **adjusted score** on 2 years of 1-hour data across BTC/USD, ETH/USD, SOL/USD.

**Adjusted score = Sharpe × sqrt(num_trades / 50)**

### Current Performance
- **Current best adjusted score: 6.87** (Sharpe 2.2246, 477 trades, 51.8% win rate)
- This is the number to beat.

### Score Math (build intuition)
- Sharpe 2.30, 477 trades → 2.30 × 3.09 = 7.11 ✅ BEATS CURRENT
- Sharpe 2.25, 510 trades → 2.25 × 3.19 = 7.19 ✅ BEATS CURRENT
- Sharpe 2.40, 440 trades → 2.40 × 2.97 = 7.12 ✅ BEATS CURRENT
- Sharpe 2.20, 477 trades → 2.20 × 3.09 = 6.80 ❌ Sharpe too low
- Sharpe 2.50, 350 trades → 2.50 × 2.65 = 6.61 ❌ not enough trades

**Key insight: The strategy profits from BOTH a slight directional edge (51.8% win rate) AND asymmetric TP/SL (3.55% TP vs 2.42% SL = 1.47 ratio). A Sharpe improvement of 0.05+ without losing trades is the goal.**

## ⛔ CRITICAL: BUILD YOUR YAML FROM THIS TEMPLATE (DO NOT COPY FROM ANYWHERE ELSE) ⛔

Copy the YAML below EXACTLY, then change ONE numerical value. This template has the CORRECT pairs and the CORRECT parameter values.

```yaml
name: crossover
style: randomly generated
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
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
  stop_loss_pct: 2.42
  timeout_hours: 201
risk:
  pause_if_down_pct: 8