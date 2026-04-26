#!/usr/bin/env python3
"""Initialize a swing trading competition (7-day sprints, hourly candles)."""
import sys
import json
import os
import yaml
from datetime import datetime, timezone
import cycle_ledger

WORKSPACE        = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
ODIN_BEST_SWING  = os.path.join(WORKSPACE, "research", "swing", "best_strategy.yaml")
STARTING_CAPITAL = 1000.00
FEE_RATE         = 0.001
DEFAULT_DURATION = 168  # 7 days in hours

ALL_BOTS = []  # populated from fleet/swing/ directory

DEFAULT_PAIRS = [
    "BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD",
    "DOGE/USD", "AVAX/USD", "LINK/USD", "UNI/USD",
    "AAVE/USD", "NEAR/USD", "APT/USD", "SUI/USD",
    "ARB/USD", "OP/USD", "ADA/USD", "POL/USD",
]


def discover_bots():
    """Find all bots with valid strategy.yaml in fleet/swing/."""
    fleet_dir = os.path.join(WORKSPACE, "fleet", "swing")
    if not os.path.isdir(fleet_dir):
        return []
    bots = []
    for name in sorted(os.listdir(fleet_dir)):
        strat = os.path.join(fleet_dir, name, "strategy.yaml")
        if not os.path.isfile(strat):
            continue
        with open(strat) as f:
            s = yaml.safe_load(f)
        has_conditions = any(
            s.get("entry", {}).get(d, {}).get("conditions", [])
            for d in ["long", "short"]
        )
        if has_conditions:
            bots.append(name)
        else:
            print(f"  WARNING: {name} has no conditions (placeholder) -- skipped",
                  file=sys.stderr)
    return bots



def _write_sprint_backtest_meta(comp_dir):
    """Snapshot backtest Sharpe into the new sprint dir for drift tracking.

    Primary: _sharpe from best_strategy.yaml.
    Fallback: best_strategy.meta.json.sharpe (present after first ODIN run).
    """
    sharpe = None
    try:
        if os.path.exists(ODIN_BEST_SWING):
            with open(ODIN_BEST_SWING) as f:
                d = yaml.safe_load(f)
            sharpe = d.get("_sharpe")
    except Exception:
        pass
    if sharpe is None:
        meta_path = os.path.join(WORKSPACE, "research", "swing", "best_strategy.meta.json")
        try:
            if os.path.exists(meta_path):
                with open(meta_path) as f:
                    sharpe = json.load(f).get("sharpe")
        except Exception:
            pass
    if sharpe is None:
        return
    try:
        with open(os.path.join(comp_dir, "deployed_strategy.meta.json"), "w") as f:
            json.dump({"sharpe": float(sharpe)}, f)
        print(f"  [drift] deployed_strategy.meta.json sharpe={sharpe}", file=sys.stderr)
    except Exception as e:
        print(f"  [drift] meta write failed: {e}", file=sys.stderr)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Start a swing trading competition")
    parser.add_argument("duration_hours", nargs="?", type=float, default=DEFAULT_DURATION,
                        help=f"Sprint duration in hours (default: {DEFAULT_DURATION} = 7 days)")
    parser.add_argument("--bots",  nargs="+", help="Override bot list")
    parser.add_argument("--pairs", nargs="+", help="Override pair list",
                        default=DEFAULT_PAIRS)
    parser.add_argument("--cycle",           type=int, default=None, help="Cycle number")
    parser.add_argument("--sprint-in-cycle", type=int, default=None, dest="sprint_in_cycle",
                        help="Sprint number within the cycle")
    args = parser.parse_args()

    bots = args.bots if args.bots else discover_bots()
    if not bots:
        print("Error: no swing bots found in fleet/swing/", file=sys.stderr)
        sys.exit(1)

    pairs = args.pairs

    now      = datetime.now(timezone.utc)
    comp_id  = f"swing-{now.strftime('%Y%m%d-%H%M')}"
    comp_dir = os.path.join(WORKSPACE, "competition", "swing", "active", comp_id)

    if os.path.exists(comp_dir):
        print(f"Error: competition {comp_id} already exists", file=sys.stderr)
        sys.exit(1)

    os.makedirs(comp_dir, exist_ok=True)
    _write_sprint_backtest_meta(comp_dir)

    for bot in bots:
        portfolio = {
            "bot":              bot,
            "competition_id":  comp_id,
            "league":          "swing",
            "duration_hours":  args.duration_hours,
            "started_at":      now.isoformat(),
            "pairs":           pairs,
            "starting_capital": STARTING_CAPITAL,
            "fee_rate":        FEE_RATE,
            "fixed_sizing":    True,  # phase-1: no profit reinvestment
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
        "comp_id":        comp_id,
        "league":         "swing",
        "duration_hours": args.duration_hours,
        "started_at":     now.isoformat(),
        "pairs":          pairs,
        "bots":           bots,
        "starting_capital": STARTING_CAPITAL,
        "fee_rate":       FEE_RATE,
        "fixed_sizing":   True,  # phase-1: no profit reinvestment
        "status":         "active",
    }
    if args.cycle is not None:
        meta["cycle"] = args.cycle
    if args.sprint_in_cycle is not None:
        meta["sprint_in_cycle"] = args.sprint_in_cycle
    with open(os.path.join(comp_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    try:
        cycle_ledger.emit("swing", "sprint_started",
                          comp_id=comp_id,
                          cycle=args.cycle,
                          sprint_in_cycle=args.sprint_in_cycle)
    except Exception as _e:
        print(f"  [ledger] emit failed (sprint_started swing): {_e}")

    result = {
        "comp_id":        comp_id,
        "comp_dir":       comp_dir,
        "duration_hours": args.duration_hours,
        "started_at":     now.isoformat(),
        "pairs":          pairs,
        "bots":           bots,
        "cycle":          args.cycle,
        "sprint_in_cycle": args.sprint_in_cycle,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
