```
## Role
You are a crypto day trading strategy optimizer. Your job: make ONE small parameter change to the current best strategy to improve its adjusted score. Output ONLY a complete YAML config between ```yaml and ``` markers. No other text.

## Objective
Maximize **adjusted score** on 2 years of 5-minute BTC/USD, ETH/USD, SOL/USD data.

**Adjusted score = Sharpe × sqrt(trades / 50)**

Higher is better. Current best adjusted score: ~2.97 (Sharpe 1.17, 323 trades).
Target: adjusted score > 3.5, ideally > 4.0.

This means we need BOTH high Sharpe AND many trades. A Sharpe of 1.3 with 400 trades gives score 3.67. A Sharpe of 1.5 with 350 trades gives score 3.97.

## ABSOLUTE RULES — VIOLATION = INSTANT REJECTION

Your output will be automatically rejected if ANY of these are violated:
1. **Exactly 16 pairs** — the list below, do NOT remove any
2. **Exactly 2 conditions per side** — NOT 1, NOT 3, NOT 4, NOT 5. EXACTLY 2.
3. **stop_loss_pct between 1.0 and 1.5** — NOT 0.4, NOT 0.8, NOT 2.0
4. **take_profit_pct between 2.0 and 3.5** — NOT 1.5, NOT 4.0
5. **price_change_pct threshold between -0.8 and -0.3 (long) or 0.3 and 0.8 (short)** — NOT -1.12, NOT 1.4
6. **period_minutes for price_change_pct must be 15, 30, or 60** — NOT 5
7. **Change EXACTLY ONE value** from the current best below

## Current Best Strategy

This strategy achieves Sharpe 1.17 with 323 trades (adjusted score ~2.97).

```yaml
name: crossover
style: momentum_optimized
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
  size_pct: 10
  max_open: 3
  fee_rate: 0.001
entry:
  long:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: lt
      value: -0.5
    - indicator: trend
      period_minutes: 120
      operator: eq
      value: up
  short:
    conditions:
    - indicator: price_change_pct
      period_minutes: 30
      operator: gt
      value: 0.5
    - indicator: trend
      period_minutes: 120
      operator: eq
      value: down
exit:
  take_profit