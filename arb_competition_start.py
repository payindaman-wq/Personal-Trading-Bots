#!/usr/bin/env python3
"""
arb_competition_start.py - Start a statistical arbitrage competition sprint.

Usage:
  python3 arb_competition_start.py              # 7-day sprint (default)
  python3 arb_competition_start.py 168          # explicit hours
"""
import sys
import json
import os
import yaml
from datetime import datetime, timezone

WORKSPACE        = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
STARTING_CAPITAL = 1000.00
FEE_RATE         = 0.001
DEFAULT_DURATION = 168  # 7 days


def discover_bots():
    """Find arb bots with valid strategy.yaml in fleet/arb/."""
    fleet_dir = os.path.join(WORKSPACE, "fleet", "arb")
    if not os.path.isdir(fleet_dir):
        print(f"Error: {fleet_dir} not found", file=sys.stderr)
        return []
    bots = []
    for name in sorted(os.listdir(fleet_dir)):
        strat = os.path.join(fleet_dir, name, "strategy.yaml")
        if not os.path.isfile(strat):
            continue
        with open(strat) as f:
            s = yaml.safe_load(f)
        if s.get("pair_a") and s.get("pair_b"):
            bots.append((name, s["pair_a"], s["pair_b"]))
        else:
            print(f"  WARNING: {name} missing pair_a/pair_b — skipped", file=sys.stderr)
    return bots


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Start an arb competition sprint")
    parser.add_argument("duration_hours", nargs="?", type=float, default=DEFAULT_DURATION)
    args = parser.parse_args()

    bot_list = discover_bots()
    if not bot_list:
        print("Error: no arb bots found", file=sys.stderr)
        sys.exit(1)

    now     = datetime.now(timezone.utc)
    comp_id = f"arb-{now.strftime('%Y%m%d-%H%M')}"
    comp_dir = os.path.join(WORKSPACE, "competition", "arb", "active", comp_id)

    if os.path.exists(comp_dir):
        print(f"Error: competition {comp_id} already exists", file=sys.stderr)
        sys.exit(1)

    os.makedirs(comp_dir, exist_ok=True)

    spread_names = []
    bots = []
    for (bot, pair_a, pair_b) in bot_list:
        bots.append(bot)
        # Clean spread name for display (e.g. "ETH/BTC")
        a = pair_a.replace("/USD", "")
        b = pair_b.replace("/USD", "")
        spread_name = f"{a}/{b}"
        if spread_name not in spread_names:
            spread_names.append(spread_name)

        portfolio = {
            "bot":             bot,
            "competition_id":  comp_id,
            "league":          "arb",
            "duration_hours":  args.duration_hours,
            "started_at":      now.isoformat(),
            "pair_a":          pair_a,
            "pair_b":          pair_b,
            "spread_name":     spread_name,
            "starting_capital": STARTING_CAPITAL,
            "fee_rate":        FEE_RATE,
            "equity":          STARTING_CAPITAL,
            "peak_equity":     STARTING_CAPITAL,
            "positions":       [],
            "stats": {
                "total_trades":     0,
                "wins":             0,
                "losses":           0,
                "win_rate":         0.0,
                "total_pnl_usd":    0.0,
                "total_pnl_pct":    0.0,
                "total_fees":       0.0,
                "max_drawdown_pct": 0.0,
                "current_equity":   STARTING_CAPITAL,
            },
        }
        with open(os.path.join(comp_dir, f"portfolio-{bot}.json"), "w") as f:
            json.dump(portfolio, f, indent=2)

    meta = {
        "comp_id":          comp_id,
        "league":           "arb",
        "duration_hours":   args.duration_hours,
        "started_at":       now.isoformat(),
        "pairs":            spread_names,   # shown in sprint bar as traded spreads
        "bots":             bots,
        "starting_capital": STARTING_CAPITAL,
        "fee_rate":         FEE_RATE,
        "status":           "active",
    }
    with open(os.path.join(comp_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    result = {
        "comp_id":        comp_id,
        "comp_dir":       comp_dir,
        "duration_hours": args.duration_hours,
        "started_at":     now.isoformat(),
        "spreads":        spread_names,
        "bots":           bots,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
