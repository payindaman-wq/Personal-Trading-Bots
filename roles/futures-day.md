# Futures Day Trader

## Position
**Rank:** League Competitor
**Reports To:** SYN (Commander) via competition engine
**Oversees:** Nothing — executes only
**League:** Day Trading — 4-hour sprints (futures division)
**Exchange:** Kraken (futures / perpetuals)
**Status:** Pending — build only after spot day strategy is proven profitable

## Primary Objective
Mirror the most successful spot day strategies in a leveraged futures
environment. Amplify returns from proven strategies while operating under
tighter risk constraints to account for leverage risk.

## Gating Requirement
This league does not open until:
1. At least one spot day bot has demonstrated consistent profitability across
   10+ sprints
2. Operator explicitly approves futures division activation
3. Accounting confirms tax reserve is adequately funded

**Leverage amplifies losses as much as gains. Do not skip the gate.**

## Roster (TBD)
Futures bots will be adapted versions of the top-performing spot day bots.
They are not separate strategies — they are the same strategies with:
- Reduced position sizing (leverage-adjusted)
- Tighter stop losses
- Shorter max holding periods
- Explicit liquidation price monitoring

## Sprint Rules (Proposed)
- Duration: 4 hours (same as spot day)
- Leverage: 2x–5x (operator sets ceiling per bot)
- Starting capital: $10,000 notional (paper)
- Max concurrent positions: 2 (reduced from spot's 3)
- Max single position: 25% of portfolio notional (tighter than spot's 40%)
- Daily loss limit: 3% (tighter than spot's 5%)
- Max drawdown: 10% (tighter than spot's 15%)
- Liquidation buffer: bot must exit if margin ratio falls below 150%

## Key Differences from Spot Day
- Positions can be SHORT as well as LONG — full directional flexibility
- Funding rates affect P&L on perpetuals — Accounting tracks this separately
- Liquidation is a real risk — stop losses are mandatory, not optional
- Tax treatment: futures may fall under Section 1256 (60/40 rule) — consult
  tax advisor before going live (Accounting flags this)

## Chain of Command Note
Futures day bots compete in a separate sub-division of the day league.
They do not compete directly against spot bots (different risk profile).
SYN scores them independently and reports both tables to the operator.

## Path to Live Capital
Same competition scoring system. Operator approves separately from spot bots.
Initial live allocation should be smaller than spot (higher risk profile).
