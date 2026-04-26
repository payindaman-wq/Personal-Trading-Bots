#!/usr/bin/env python3
"""
generate_fleet.py — Create bot fleet directories for any league.

Usage:
    python3 scripts/generate_fleet.py --league day --names alice bob charlie
    python3 scripts/generate_fleet.py --league swing --names alpha beta gamma
    python3 scripts/generate_fleet.py --league futures_day --names striker hawk
    python3 scripts/generate_fleet.py --league futures_swing --names titan wolf
    python3 scripts/generate_fleet.py --league polymarket --names oracle sage

Each bot gets a strategy.yaml template suited to its league type.
Edit the template to tune parameters before the first sprint.
"""
import argparse
import os
import sys

WORKSPACE = os.environ.get("WORKSPACE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LEAGUE_DIRS = {
    "day":          os.path.join(WORKSPACE, "fleet", "day"),
    "swing":        os.path.join(WORKSPACE, "fleet", "swing"),
    "futures_day":  os.path.join(WORKSPACE, "fleet", "futures_day"),
    "futures_swing":os.path.join(WORKSPACE, "fleet", "futures_swing"),
    "polymarket":   os.path.join(WORKSPACE, "fleet", "polymarket"),
}

TEMPLATES = {
    "day": """\
name: {name}
style: ema_macd_momentum
league: day
pairs:
  - BTC/USD
  - ETH/USD
  - SOL/USD
position:
  size_pct: 10
  max_open: 2
  fee_rate: 0.001
entry:
  long:
    conditions:
      - indicator: macd_signal
        period_hours: 1
        operator: eq
        value: bullish
      - indicator: rsi
        period_hours: 14
        operator: lt
        value: 60
  short:
    conditions:
      - indicator: macd_signal
        period_hours: 1
        operator: eq
        value: bearish
      - indicator: rsi
        period_hours: 14
        operator: gt
        value: 40
exit:
  take_profit_pct: 3.0
  stop_loss_pct: 1.5
  timeout_hours: 24
risk:
  pause_if_down_pct: 6
  pause_hours: 4
  stop_if_down_pct: 15
""",

    "swing": """\
name: {name}
style: trend_pullback
league: swing
pairs:
  - BTC/USD
  - ETH/USD
  - SOL/USD
position:
  size_pct: 12
  max_open: 2
  fee_rate: 0.001
entry:
  long:
    conditions:
      - indicator: trend
        period_hours: 72
        operator: eq
        value: up
      - indicator: price_vs_ema
        period_hours: 50
        operator: eq
        value: above
      - indicator: rsi
        period_hours: 14
        operator: lt
        value: 62
  short:
    conditions:
      - indicator: trend
        period_hours: 72
        operator: eq
        value: down
      - indicator: price_vs_ema
        period_hours: 50
        operator: eq
        value: below
      - indicator: rsi
        period_hours: 14
        operator: gt
        value: 38
exit:
  take_profit_pct: 8.0
  stop_loss_pct: 3.0
  timeout_hours: 168
risk:
  pause_if_down_pct: 8
  pause_hours: 48
  stop_if_down_pct: 18
""",

    "futures_day": """\
name: {name}
style: macd_crossover
league: futures_day
leverage: 2
pairs:
  - BTC/USD
  - ETH/USD
  - SOL/USD
position:
  size_pct: 8
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
      - indicator: macd_signal
        period_minutes: 15
        operator: eq
        value: bullish
      - indicator: rsi
        period_minutes: 21
        operator: lt
        value: 50
  short:
    conditions:
      - indicator: macd_signal
        period_minutes: 15
        operator: eq
        value: bearish
      - indicator: rsi
        period_minutes: 21
        operator: gt
        value: 50
exit:
  take_profit_pct: 1.2
  stop_loss_pct: 0.7
  timeout_minutes: 60
risk:
  pause_if_down_pct: 4
  pause_minutes: 20
  stop_if_down_pct: 10
""",

    "futures_swing": """\
name: {name}
style: ema_trend_swing
league: futures_swing
leverage: 2
pairs:
  - BTC/USD
  - ETH/USD
  - SOL/USD
position:
  size_pct: 10
  max_open: 1
  fee_rate: 0.0005
entry:
  long:
    conditions:
      - indicator: trend
        period_hours: 24
        operator: eq
        value: up
      - indicator: rsi
        period_hours: 4
        operator: lt
        value: 55
  short:
    conditions:
      - indicator: trend
        period_hours: 24
        operator: eq
        value: down
      - indicator: rsi
        period_hours: 4
        operator: gt
        value: 45
exit:
  take_profit_pct: 3.0
  stop_loss_pct: 1.5
  timeout_hours: 168
risk:
  pause_if_down_pct: 6
  pause_hours: 24
  stop_if_down_pct: 15
""",

    "polymarket": """\
name: {name}
category: crypto
type: opinion
description: Crypto price probability analyst
prompt_persona: >
  You are a cryptocurrency analyst who uses technical analysis, on-chain metrics,
  market cycle theory, and macro conditions to assess the probability of specific
  price targets being hit within a given timeframe.
market_filter:
  include_keywords: ["bitcoin", "ethereum", "btc", "eth", "crypto", "price", "above", "below", "reach"]
  exclude_keywords: ["election", "vote", "president", "sports", "weather"]
  price_range:
    - 0.1
    - 0.9
  min_liquidity_usd: 1000
  max_days_to_resolve: 14
edge:
  min_edge_pts: 0.08
  min_confidence: medium
  max_positions: 8
  max_position_pct: 0.1
risk:
  stop_if_down_pct: 20
  starting_capital: 1000.0
""",
}


def create_bot(league: str, name: str, dry_run: bool = False) -> str:
    league_dir = LEAGUE_DIRS[league]
    bot_dir = os.path.join(league_dir, name)
    strategy_path = os.path.join(bot_dir, "strategy.yaml")

    if os.path.exists(strategy_path):
        return f"  SKIP  {league}/{name} — already exists"

    template = TEMPLATES[league].format(name=name)

    if not dry_run:
        os.makedirs(bot_dir, exist_ok=True)
        with open(strategy_path, "w") as f:
            f.write(template)

    return f"  {'DRY   ' if dry_run else 'CREATE'} {league}/{name}/strategy.yaml"


def main():
    parser = argparse.ArgumentParser(
        description="Generate bot fleet directories for crypto-trading-toolkit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--league",
        required=True,
        choices=list(LEAGUE_DIRS.keys()),
        help="League type to generate bots for",
    )
    parser.add_argument(
        "--names",
        nargs="+",
        required=True,
        metavar="NAME",
        help="One or more bot names (lowercase, no spaces)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without writing files",
    )
    args = parser.parse_args()

    bad = [n for n in args.names if not n.replace("-", "").replace("_", "").isalnum()]
    if bad:
        print(f"ERROR: invalid bot names (alphanumeric + hyphens/underscores only): {bad}", file=sys.stderr)
        sys.exit(1)

    print(f"Generating {len(args.names)} bot(s) for league '{args.league}':")
    for name in args.names:
        result = create_bot(args.league, name.lower(), dry_run=args.dry_run)
        print(result)

    if not args.dry_run:
        print(f"\nDone. Edit fleet/{args.league}/<name>/strategy.yaml to tune parameters.")
        print("Then restart the league or wait for the next sprint cycle.")


if __name__ == "__main__":
    main()
