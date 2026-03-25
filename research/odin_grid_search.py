#!/usr/bin/env python3
"""
odin_grid_search.py - Systematic grid search of exit parameters.

Finds globally optimal TP/SL/timeout for given entry conditions.
Uses multiprocessing for speed. Run once per league to establish baseline.

Usage:
  python3 odin_grid_search.py --league day
  python3 odin_grid_search.py --league swing
  python3 odin_grid_search.py --league day --workers 6
  python3 odin_grid_search.py --league day --strategy /path/to/custom.yaml
"""
import argparse
import copy
import json
import os
import sys
import time
import yaml
from multiprocessing import Pool

WORKSPACE = "/root/.openclaw/workspace"
RESEARCH  = os.path.join(WORKSPACE, "research")

CORE_PAIRS = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD"]

DAY_GRID = {
    "take_profit_pct": [0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0],
    "stop_loss_pct":   [0.5, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5],
    "timeout_minutes": [60, 120, 180, 240, 360, 480, 720],
}

SWING_GRID = {
    "take_profit_pct": [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0],
    "stop_loss_pct":   [2.0, 2.5, 3.0, 3.5, 4.0, 5.0],
    "timeout_hours":   [48, 72, 96, 120, 144, 168, 240],
}

MIN_TRADES = {"day": 30, "swing": 15}


def run_single(args):
    """Worker function for multiprocessing pool."""
    strategy, league, pairs, combo_id, total = args
    sys.path.insert(0, RESEARCH)
    from odin_backtest import run_backtest
    try:
        result = run_backtest(strategy, league, pairs)
        return combo_id, strategy["exit"], result
    except Exception as e:
        return combo_id, strategy["exit"], {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Grid search exit parameters")
    parser.add_argument("--league", choices=["day", "swing"], required=True)
    parser.add_argument("--strategy", default=None,
                        help="Base strategy YAML (default: best_strategy.yaml)")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--pairs", nargs="+", default=None)
    args = parser.parse_args()

    league = args.league
    strategy_path = args.strategy or os.path.join(RESEARCH, league, "best_strategy.yaml")
    pairs = args.pairs or CORE_PAIRS

    with open(strategy_path) as f:
        base = yaml.safe_load(f.read())

    grid = DAY_GRID if league == "day" else SWING_GRID
    min_t = MIN_TRADES[league]

    # Build all combinations
    combos = []
    if league == "day":
        for tp in grid["take_profit_pct"]:
            for sl in grid["stop_loss_pct"]:
                for to in grid["timeout_minutes"]:
                    s = copy.deepcopy(base)
                    s["exit"]["take_profit_pct"] = tp
                    s["exit"]["stop_loss_pct"] = sl
                    s["exit"]["timeout_minutes"] = to
                    s["exit"].pop("timeout_hours", None)
                    combos.append(s)
    else:
        for tp in grid["take_profit_pct"]:
            for sl in grid["stop_loss_pct"]:
                for to in grid["timeout_hours"]:
                    s = copy.deepcopy(base)
                    s["exit"]["take_profit_pct"] = tp
                    s["exit"]["stop_loss_pct"] = sl
                    s["exit"]["timeout_hours"] = to
                    s["exit"].pop("timeout_minutes", None)
                    combos.append(s)

    total = len(combos)
    print(f"[grid/{league}] {total} combinations, {args.workers} workers, pairs={pairs}")
    print(f"  Strategy: {strategy_path}")
    print()

    worker_args = [(s, league, pairs, i, total) for i, s in enumerate(combos)]
    results = []
    t0 = time.time()

    with Pool(args.workers) as pool:
        for done, (cid, exit_p, result) in enumerate(pool.imap_unordered(run_single, worker_args), 1):
            elapsed = time.time() - t0
            rate = done / elapsed if elapsed > 0 else 1
            eta = (total - done) / rate if rate > 0 else 0

            if done % 20 == 0 or done == total:
                if "error" not in result:
                    print(f"  [{done}/{total}] ETA {eta/60:.0f}m | "
                          f"sharpe={result['sharpe']:.4f} trades={result['total_trades']}")
                else:
                    print(f"  [{done}/{total}] ETA {eta/60:.0f}m | ERROR")

            if "error" not in result:
                results.append({
                    "exit": exit_p,
                    "sharpe": result["sharpe"],
                    "win_rate": result["win_rate_pct"],
                    "pnl_pct": result["total_pnl_pct"],
                    "trades": result["total_trades"],
                    "max_dd": result["max_drawdown_pct"],
                    "suspicious": result["suspicious"],
                })

    # Filter and sort
    valid = [r for r in results
             if not r["suspicious"] and r["trades"] >= min_t and r["sharpe"] > -10]
    valid.sort(key=lambda r: r["sharpe"], reverse=True)

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed/60:.1f} minutes. {len(valid)} valid / {len(results)} total.\n")

    # Print top 20
    to_key = "timeout_minutes" if league == "day" else "timeout_hours"
    to_unit = "m" if league == "day" else "h"
    print(f"{'#':>3} {'TP%':>5} {'SL%':>5} {'TO':>6} {'Sharpe':>8} {'Win%':>6} "
          f"{'PnL%':>8} {'Trades':>7} {'MaxDD%':>7}")
    print("-" * 68)
    for i, r in enumerate(valid[:20]):
        tp = r["exit"].get("take_profit_pct")
        sl = r["exit"].get("stop_loss_pct")
        to = r["exit"].get(to_key)
        print(f"{i+1:>3} {tp:>5.1f} {sl:>5.1f} {to:>5}{to_unit} "
              f"{r['sharpe']:>8.4f} {r['win_rate']:>5.1f}% {r['pnl_pct']:>7.2f}% "
              f"{r['trades']:>7} {r['max_dd']:>6.2f}%")

    # Save
    out_dir = os.path.join(RESEARCH, league)
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, "grid_results.json"), "w") as f:
        json.dump(valid[:50], f, indent=2)

    if valid:
        best = valid[0]
        best_s = copy.deepcopy(base)
        best_s["exit"].update(best["exit"])
        best_s["name"] = f"grid_best_{league}"
        best_s["style"] = (f"Grid-optimized: TP={best['exit'].get('take_profit_pct')}% "
                            f"SL={best['exit'].get('stop_loss_pct')}%")

        path = os.path.join(out_dir, "grid_best_strategy.yaml")
        with open(path, "w") as f:
            yaml.dump(best_s, f, default_flow_style=False, sort_keys=False)

        print(f"\nBest saved to {path}")
        print(f"Sharpe={best['sharpe']:.4f} Win={best['win_rate']:.1f}% "
              f"PnL={best['pnl_pct']:.2f}% Trades={best['trades']}")


if __name__ == "__main__":
    main()
