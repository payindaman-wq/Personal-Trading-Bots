#!/usr/bin/env python3
"""Score a bot trading competition."""
import sys
import json
import os
import shutil
import urllib.request
import urllib.error
from datetime import datetime, timezone

WORKSPACE = "/root/.openclaw/workspace"
BOTS = ["floki", "bjorn", "lagertha"]
FEE_RATE = 0.001

KRAKEN_PAIR_MAP = {
    "BTC/USD": "XBTUSD",
    "ETH/USD": "ETHUSD",
    "SOL/USD": "SOLUSD",
    "XRP/USD": "XRPUSD",
}
KRAKEN_KEY_LABELS = {
    "XBT": "BTC/USD",
    "ETH": "ETH/USD",
    "SOL": "SOL/USD",
    "XRP": "XRP/USD",
}


def fetch_current_prices(pairs):
    kraken_pairs = [KRAKEN_PAIR_MAP.get(p, p.replace("/", "")) for p in pairs]
    url = f"https://api.kraken.com/0/public/Ticker?pair={','.join(kraken_pairs)}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        prices = {}
        for kraken_key, info in data.get("result", {}).items():
            label = next(
                (lbl for frag, lbl in KRAKEN_KEY_LABELS.items() if frag in kraken_key),
                kraken_key,
            )
            prices[label] = {"last": float(info["c"][0])}
        return prices
    except Exception as e:
        print(f"Warning: could not fetch prices ({e}), using entry prices for open positions", file=sys.stderr)
        return {}


def score_portfolio(portfolio, current_prices):
    cash = portfolio["cash"]
    fee_rate = portfolio.get("fee_rate", FEE_RATE)
    total_fees = portfolio["stats"]["total_fees"]
    force_closed = 0

    for pos in portfolio.get("positions", []):
        pair = pos["pair"]
        entry = pos["entry_price"]
        current = current_prices.get(pair, {}).get("last", entry)
        quantity = pos["quantity"]
        cost_basis = pos["cost_basis"]

        if pos["direction"] == "long":
            gross_pnl = (current - entry) * quantity
        else:
            gross_pnl = (entry - current) * quantity

        close_fee = cost_basis * fee_rate
        net_pnl = gross_pnl - close_fee
        total_fees += close_fee
        cash += cost_basis + net_pnl
        force_closed += 1

    total_pnl_usd = cash - portfolio["starting_capital"]
    total_pnl_pct = (total_pnl_usd / portfolio["starting_capital"]) * 100

    trades = portfolio["stats"]["total_trades"]
    wins = portfolio["stats"]["wins"]
    win_rate = (wins / trades * 100) if trades > 0 else 0.0

    return {
        "bot": portfolio["bot"],
        "final_equity": round(cash, 2),
        "total_pnl_usd": round(total_pnl_usd, 2),
        "total_pnl_pct": round(total_pnl_pct, 4),
        "total_trades": trades,
        "wins": wins,
        "losses": portfolio["stats"]["losses"],
        "win_rate": round(win_rate, 1),
        "max_drawdown_pct": portfolio["stats"]["max_drawdown_pct"],
        "total_fees": round(total_fees, 2),
        "open_positions_force_closed": force_closed,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: competition_score.py <comp_id> [--archive]", file=sys.stderr)
        sys.exit(1)

    comp_id = sys.argv[1]
    archive = "--archive" in sys.argv

    comp_dir = os.path.join(WORKSPACE, "competition", "active", comp_id)
    if not os.path.exists(comp_dir):
        print(f"Error: competition {comp_id} not found at {comp_dir}", file=sys.stderr)
        sys.exit(1)

    meta_path = os.path.join(comp_dir, "meta.json")
    with open(meta_path) as f:
        meta = json.load(f)

    current_prices = fetch_current_prices(meta["pairs"])

    results = []
    for bot in BOTS:
        path = os.path.join(comp_dir, f"portfolio-{bot}.json")
        if not os.path.exists(path):
            print(f"Warning: portfolio for {bot} not found, skipping", file=sys.stderr)
            continue
        with open(path) as f:
            portfolio = json.load(f)
        results.append(score_portfolio(portfolio, current_prices))

    results.sort(key=lambda x: x["total_pnl_pct"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    now = datetime.now(timezone.utc)
    output = {
        "comp_id": comp_id,
        "scored_at": now.isoformat(),
        "duration_hours": meta["duration_hours"],
        "pairs": meta["pairs"],
        "winner": results[0]["bot"] if results else None,
        "rankings": results,
    }

    if archive:
        results_base = os.path.join(WORKSPACE, "competition", "results")
        results_dir = os.path.join(results_base, comp_id)
        os.makedirs(results_base, exist_ok=True)
        shutil.copytree(comp_dir, results_dir, dirs_exist_ok=True)
        with open(os.path.join(results_dir, "final_score.json"), "w") as f:
            json.dump(output, f, indent=2)
        shutil.rmtree(comp_dir)
        output["archived_to"] = results_dir

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
