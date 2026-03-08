#!/usr/bin/env python3
"""Initialize a bot trading competition."""
import sys
import json
import os
from datetime import datetime, timezone

WORKSPACE        = "/root/.openclaw/workspace"
STARTING_CAPITAL = 10000.00
FEE_RATE         = 0.001

ALL_BOTS = [
    "floki", "bjorn", "lagertha", "ragnar",
    "leif",  "ivar",  "harald",   "freydis",
]

DEFAULT_PAIRS = [
    "BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD",
    "DOGE/USD", "AVAX/USD", "LINK/USD",
]


def main():
    if len(sys.argv) < 2:
        print("Usage: competition_start.py <duration_hours> [--bots b1 b2 ...] [--pairs p1 p2 ...]",
              file=sys.stderr)
        print(f"  Default bots : {ALL_BOTS}", file=sys.stderr)
        print(f"  Default pairs: {DEFAULT_PAIRS}", file=sys.stderr)
        sys.exit(1)

    try:
        duration_hours = float(sys.argv[1])
    except ValueError:
        print(f"Error: duration_hours must be a number, got: {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    # Parse optional --bots and --pairs flags
    args = sys.argv[2:]
    bots  = ALL_BOTS[:]
    pairs = DEFAULT_PAIRS[:]
    i = 0
    while i < len(args):
        if args[i] == "--bots":
            i += 1
            bots = []
            while i < len(args) and not args[i].startswith("--"):
                bots.append(args[i])
                i += 1
        elif args[i] == "--pairs":
            i += 1
            pairs = []
            while i < len(args) and not args[i].startswith("--"):
                pairs.append(args[i])
                i += 1
        else:
            i += 1

    # Validate bots have strategy files
    fleet_dir = os.path.join(WORKSPACE, "fleet")
    valid_bots = []
    for bot in bots:
        strat = os.path.join(fleet_dir, bot, "strategy.yaml")
        if not os.path.isfile(strat):
            print(f"  WARNING: {bot} has no strategy.yaml -- skipped", file=sys.stderr)
            continue
        import yaml
        with open(strat) as f:
            s = yaml.safe_load(f)
        has_conditions = any(
            s.get("entry", {}).get(d, {}).get("conditions", [])
            for d in ["long", "short"]
        )
        if not has_conditions:
            print(f"  WARNING: {bot} strategy has no conditions (placeholder) -- skipped",
                  file=sys.stderr)
            continue
        valid_bots.append(bot)

    if not valid_bots:
        print("Error: no valid bots with strategies found", file=sys.stderr)
        sys.exit(1)

    now     = datetime.now(timezone.utc)
    comp_id = f"comp-{now.strftime('%Y%m%d-%H%M')}"
    comp_dir = os.path.join(WORKSPACE, "competition", "active", comp_id)

    if os.path.exists(comp_dir):
        print(f"Error: competition {comp_id} already exists", file=sys.stderr)
        sys.exit(1)

    os.makedirs(comp_dir, exist_ok=True)

    for bot in valid_bots:
        portfolio = {
            "bot": bot,
            "competition_id": comp_id,
            "duration_hours": duration_hours,
            "started_at": now.isoformat(),
            "pairs": pairs,
            "starting_capital": STARTING_CAPITAL,
            "fee_rate": FEE_RATE,
            "cash": STARTING_CAPITAL,
            "positions": [],
            "closed_trades": [],
            "stats": {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "total_pnl_usd": 0.0,
                "total_pnl_pct": 0.0,
                "total_fees": 0.0,
                "max_drawdown_pct": 0.0,
                "largest_win_pct": 0.0,
                "largest_loss_pct": 0.0,
                "current_equity": STARTING_CAPITAL,
                "peak_equity": STARTING_CAPITAL,
            },
        }
        with open(os.path.join(comp_dir, f"portfolio-{bot}.json"), "w") as f:
            json.dump(portfolio, f, indent=2)

    meta = {
        "comp_id": comp_id,
        "duration_hours": duration_hours,
        "started_at": now.isoformat(),
        "pairs": pairs,
        "bots": valid_bots,
        "starting_capital": STARTING_CAPITAL,
        "fee_rate": FEE_RATE,
        "status": "active",
    }
    with open(os.path.join(comp_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    result = {
        "comp_id": comp_id,
        "comp_dir": comp_dir,
        "duration_hours": duration_hours,
        "started_at": now.isoformat(),
        "pairs": pairs,
        "bots": valid_bots,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
