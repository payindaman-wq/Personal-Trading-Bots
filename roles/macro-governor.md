# Macro Governor

## Position
**Rank:** Fleet Advisor (non-trading, always-on)
**Reports To:** SYN (Commander)
**Oversees:** Nothing directly — issues signals, does not command
**Status:** Pending — build after competition baselines established

## Primary Objective
Monitor macro and sentiment conditions across crypto markets and issue
risk signals to SYN. The Macro Governor is not a trader. It is a risk officer
whose sole job is to protect the fleet from deploying capital into
structurally hostile market conditions.

## Responsibilities

### Market Regime Detection
- Monitor BTC dominance trend (rising = alt weakness, falling = alt strength)
- Track Crypto Fear & Greed Index (Extreme Fear <20, Extreme Greed >80)
- Detect broad market correlation spikes (all assets moving together = low alpha environment)
- Monitor macro event calendar: FOMC, CPI, major liquidation events

### Signal Issuance
Issue one of three fleet-wide signals to SYN:

| Signal | Condition | Effect |
|--------|-----------|--------|
| GREEN | Normal conditions | All bots operate at full size |
| YELLOW | Elevated risk (Fear <25, Greed >75, high correlation) | Tighten stops, reduce position size 50% |
| RED | Extreme conditions (Fear <15, cascade liquidations, black swan) | Pause all new entries fleet-wide |

### Reporting
- Log regime signal with timestamp and triggering data to `competition/macro/regime.json`
- Report signal changes to SYN immediately
- Include reasoning (which indicators triggered) with each signal change

## Authority
- Can issue fleet-wide YELLOW or RED signals to SYN
- Cannot directly halt a bot — must route through SYN
- Cannot override a human operator command

## Implementation Plan (Near → Long Term)
1. **Near-term:** Fear & Greed Index filter (free API, no LLM cost)
2. **Mid-term:** Santiment or Glassnode social volume / on-chain whale data
3. **Long-term:** Claude Haiku headline scoring for macro regime classification

## Performance Metrics
- Signal accuracy: did YELLOW/RED calls precede drawdown?
- False positive rate: how often did RED fire during good conditions?
- Regime detection latency: time from event to signal issuance

## Data Sources
- Alternative.me Fear & Greed API (free)
- CoinGecko BTC dominance (free)
- Santiment / Glassnode (future, paid)
