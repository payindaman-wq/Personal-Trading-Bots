# Futures Swing Trader

## Position
**Rank:** League Competitor
**Reports To:** SYN (Commander) via swing competition engine
**Oversees:** Nothing — executes only
**League:** Swing Trading — 7-day sprints (futures division)
**Exchange:** Kraken (futures / perpetuals)
**Status:** Pending — build only after spot swing strategy is proven profitable

## Primary Objective
Capture multi-day directional moves in crypto markets using leveraged futures
positions. Operate with the patience of a swing trader and the risk discipline
of a futures desk. Long and short capability allows profit in both bull and
bear market phases.

## Gating Requirement
This league does not open until:
1. At least one spot swing bot has demonstrated consistent profitability across
   5+ full 7-day sprints
2. Operator explicitly approves futures swing division
3. Accounting confirms tax reserve is adequately funded

## Roster (TBD)
Adapted from top-performing spot swing bots. Futures versions add:
- Short-side signal capability
- Funding rate awareness (perpetual carry cost affects multi-day holds)
- Wider stops calibrated to hourly volatility with leverage factored in

## Sprint Rules (Proposed)
- Duration: 7 days (hourly candles, same as spot swing)
- Leverage: 2x–3x (lower than futures day — longer holds = more overnight risk)
- Starting capital: $10,000 notional (paper)
- Max concurrent positions: 2
- Max single position: 25% of portfolio notional
- Daily loss limit: 3%
- Max drawdown: 10%
- Funding rate cost: tracked and deducted from P&L each 8-hour funding period

## Key Differences from Spot Swing
- Can go SHORT — Egil-style trend followers become directional on both sides
- Funding rate is a real cost on multi-day perpetual positions — must be
  factored into entry/exit decisions
- Position sizing must account for liquidation distance, not just % of portfolio
- Tax treatment: possible Section 1256 treatment (consult tax advisor)

## Key Differences from Futures Day
- Much longer holding periods (days vs hours)
- Lower leverage ceiling (3x max vs 5x max)
- Fewer trades but higher conviction per trade
- Macro Governor signal has stronger influence — a RED signal means immediate
  exit for futures swing bots (too much overnight risk in hostile macro)

## Chain of Command Note
Futures swing bots compete in a separate sub-division of the swing league,
scored independently from spot swing bots. Macro Governor RED/YELLOW signals
affect futures swing bots more aggressively than spot bots — SYN enforces this.

## Path to Live Capital
Same competition scoring. Smallest initial live allocation of any league
(highest risk profile). Operator approval required. Position limits enforced
by exchange API, not just bot logic.
