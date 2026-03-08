# Polymarket Trader

## Position
**Rank:** Division Competitor (Separate Division)
**Reports To:** SYN (Commander)
**Oversees:** Nothing — executes only
**League:** Polymarket Division (independent — not part of crypto trading leagues)
**Exchange:** Polymarket (prediction market, USDC on Polygon)
**Status:** Pending

## Primary Objective
Generate alpha by identifying prediction market contracts on Polymarket where
the market-implied probability is miscalibrated relative to true event
probability. Place position bets (YES/NO shares) on mispriced outcomes and
exit before resolution or hold to settlement.

## Core Concept
Polymarket is a decentralized prediction market where users bet on real-world
event outcomes. Prices represent the crowd's implied probability (e.g., a
contract trading at $0.65 implies 65% chance of YES). The bot profits when:
- It identifies events where the crowd is systematically wrong
- It buys YES at $0.40 and the true probability is 60% (positive EV)
- It buys NO at $0.30 and the event fails to occur (profits as price → $1.00)

## Why It's a Separate Division
Polymarket operates on fundamentally different principles than crypto trading:
- No OHLCV candles — probability curves, not price charts
- Outcomes are binary (YES/NO), not continuous
- Settlement is event-driven, not time-driven
- Requires information edge, not technical edge
- Uses USDC on Polygon — separate wallet, separate accounting

SYN manages the division but uses distinct tooling from the crypto leagues.

## Target Market Categories (Research Required)
- Crypto price milestones ("BTC above $100k by March 31?")
- Macro events (Fed rate decisions, CPI outcomes)
- Protocol governance outcomes
- Election / political markets (operator discretion)

## Responsibilities
- Monitor active Polymarket contracts for pricing anomalies
- Calculate expected value: EV = (true_prob × $1.00) - contract_price
- Enter positions only where EV > 10% (minimum edge threshold)
- Size positions based on Kelly Criterion (partial Kelly — max 25% of full)
- Monitor open positions for early exit opportunities (price moves in our favor)
- Exit before resolution if >80% of expected gain is captured

## Risk Parameters (Proposed)
- Max per-contract position: 10% of Polymarket bankroll
- Max concurrent open contracts: 5
- Minimum liquidity: $10,000 in contract pool before entry
- Max loss per contract: position size (binary — can go to zero)
- Bankroll separate from crypto trading capital

## Accounting Treatment
Polymarket positions are in USDC — treated as USD for tax purposes.
Each settled contract is a taxable event:
- Winning position: proceeds = $1.00 per share, cost basis = purchase price
- Losing position: proceeds = $0.00, cost basis = purchase price (capital loss)
- Accounting bot tracks separately in `competition/accounting/polymarket_ledger.json`
- Short-term capital gains apply (prediction markets settle quickly)
- Report on same Form 8949 as crypto trades

## Chain of Command Note
Polymarket division reports directly to SYN but operates completely
independently from the crypto trading leagues. Macro Governor signals do not
apply (event outcomes are independent of crypto price action). SYN reports
Polymarket P&L separately in daily summaries.

## Prerequisites Before Building
- Polymarket API / data access (or web scraping layer)
- USDC wallet on Polygon (separate from Kraken funds)
- Event probability estimation model (initial: base rates + calibration data)
- Accounting bot extended with Polymarket ledger support
- Operator decision on which market categories are in scope
