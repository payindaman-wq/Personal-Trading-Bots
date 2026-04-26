# Example Fleet — Reference Configuration

This documents the original fleet used in the crypto-trading-toolkit proof-of-concept.
All bot directories have been removed from the template — use `scripts/generate_fleet.py`
to create your own.

## Day League (24h sprints)

| Bot      | Style                        | Strategy Approach           |
|----------|------------------------------|-----------------------------|
| floki    | Multi-TF confluence scalper  | Trend + volume confluence   |
| bjorn    | EMA + MACD momentum          | Classic momentum            |
| lagertha | VWAP trend directional       | VWAP with trend filter      |
| ragnar   | VWAP reclaim                 | VWAP reclaim pattern        |
| leif     | BB squeeze breakout          | Bollinger squeeze           |
| gunnar   | Aggressive momentum scalper  | High-velocity momentum      |
| harald   | RSI + trend composite        | RSI composite               |
| freydis  | Contrarian extreme reversal  | Reversal at extremes        |
| sigurd   | Altcoin momentum rotation    | Sector rotation             |
| astrid   | RSI mean reversion           | RSI reversion               |
| ulf      | Breakout retest precision    | Breakout/retest pattern     |
| bjarne   | Trend pullback buyer         | Pullback to trend           |

## Swing League (7-day sprints)

| Bot      | Style                    | Strategy Approach         |
|----------|--------------------------|---------------------------|
| egil     | Weekly trend follower    | Higher-timeframe trend    |
| solveig  | Multi-day mean reversion | 3–5 day reversion         |
| orm      | Macro pullback buyer     | Macro-aligned pullbacks   |
| gudrid   | Macro sentiment          | Sentiment-driven swing    |
| halfdan  | Technical structure      | S/R structure             |
| thyra    | Altcoin cycles           | Cycle-aware altcoin swing |
| valdis   | Swing breakout           | Weekly breakout           |
| runa     | Bitcoin maximalist       | BTC-only trend            |
| ivar     | Broad mandate momentum   | Multi-asset momentum      |

## Futures Day League (24h sprints, Kraken Derivatives US)

| Bot           | Style              | Primary Pair |
|---------------|--------------------|--------------|
| asmund        | MACD crossover     | BTC/USD      |
| brandr        | RSI momentum       | ETH/USD      |
| haki          | Bollinger bands    | SOL/USD      |
| hakon         | EMA crossover      | BTC/USD      |
| helgi         | VWAP directional   | ETH/USD      |
| ketil         | Trend following    | SOL/USD      |
| kveldulf      | Contrarian         | BTC/USD      |
| orvar         | Scalp momentum     | ETH/USD      |
| starkad       | Breakout           | SOL/USD      |
| ulfhedinn     | Mean reversion     | BTC/USD      |
| vemund        | Multi-factor       | ETH/USD      |
| vikar         | Composite          | SOL/USD      |
| autobotdayfutures | Auto-generated  | BTC/USD     |

## Futures Swing League (7-day sprints, Kraken Derivatives US)

| Bot               | Style           |
|-------------------|-----------------|
| andvari           | Trend following |
| atli              | Momentum        |
| audun             | Mean reversion  |
| grimolf           | Breakout        |
| hogni             | Composite       |
| regin             | RSI swing       |
| sigmund           | MACD swing      |
| sinfjotli         | Volatility      |
| thorolf           | EMA swing       |
| autobotswingfutures | Auto-generated |

## Prediction Markets League (Polymarket)

| Bot          | Category | Type    |
|--------------|----------|---------|
| njal         | crypto   | opinion |
| var          | politics | opinion |
| tora         | sports   | opinion |
| eir          | crypto   | opinion |
| hermod       | macro    | opinion |
| skadi        | crypto   | opinion |
| autobotpred1 | crypto   | auto    |
| autobotpred2 | crypto   | auto    |
| autobotpred3 | crypto   | auto    |

## Generating Your Own Fleet

```bash
# Create day league bots
python3 scripts/generate_fleet.py --league day --names alice bob charlie dave

# Create swing league bots
python3 scripts/generate_fleet.py --league swing --names alpha beta gamma

# Create futures day bots
python3 scripts/generate_fleet.py --league futures_day --names striker hawk

# Create prediction market bots
python3 scripts/generate_fleet.py --league polymarket --names oracle sage

# List available leagues and options
python3 scripts/generate_fleet.py --help
```
