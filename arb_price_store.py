#!/usr/bin/env python3
"""
arb_price_store.py - Compute z-score spread statistics for stat arb trading.

Reads existing hourly candle history from competition/swing/price_history/
(shared with the swing league — no duplicate fetching) and computes ratio
time series, rolling mean, rolling std, and current z-score for each pair.

Saves output to: competition/arb/pair_stats.json

Usage:
  python3 arb_price_store.py           # compute all configured pairs
  python3 arb_price_store.py --show    # print current z-scores
"""
import os
import sys
import json
import math
import argparse
from datetime import datetime, timezone

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
HISTORY_DIR  = os.path.join(WORKSPACE, "competition", "swing", "price_history")
OUTPUT_PATH  = os.path.join(WORKSPACE, "competition", "arb", "pair_stats.json")

# Spread pairs: (pair_a, pair_b) — trade ratio = price_a / price_b
SPREAD_PAIRS = [
    ("ETH/USD",  "BTC/USD"),   # fenrir, nidhogg, ratatoskr
    ("SOL/USD",  "ETH/USD"),   # jormungandr, hati, skoll
    ("AVAX/USD", "ETH/USD"),   # ymir
    ("LINK/USD", "ETH/USD"),   # surt
    ("SOL/USD",  "BTC/USD"),   # fafnir
    ("XRP/USD",  "BTC/USD"),   # garm, niflheim
    ("AVAX/USD", "SOL/USD"),   # muspell, bifrost
    ("LINK/USD", "BTC/USD"),   # utgard
    ("AAVE/USD", "ETH/USD"),   # asgard
]

LOOKBACK_WINDOWS = [240, 480, 720]  # short (10d) / medium (20d) / long (30d)
LOOKBACK_HOURS   = 480              # default — kept for backwards compat


# ---------------------------------------------------------------------------
# Price history loading
# ---------------------------------------------------------------------------

def load_closes(pair):
    """Return {timestamp_iso: close_price} dict for the pair."""
    safe = pair.replace("/", "-")
    path = os.path.join(HISTORY_DIR, f"{safe}.json")
    if not os.path.isfile(path):
        return {}
    with open(path) as f:
        candles = json.load(f)
    return {c["ts"]: float(c["close"]) for c in candles if c.get("close")}


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def _z_for_window(closes_a, closes_b, common_ts, lookback_hours):
    """Compute z-score for a specific lookback window. Returns (z, mean, std, n) or None."""
    recent_ts = common_ts[-lookback_hours:]
    ratios = [closes_a[ts] / closes_b[ts] for ts in recent_ts if closes_b.get(ts, 0) != 0]
    n = len(ratios)
    if n < 24:
        return None
    mean = sum(ratios) / n
    variance = sum((r - mean) ** 2 for r in ratios) / n
    std = math.sqrt(variance)
    if std == 0:
        return None
    z = (ratios[-1] - mean) / std
    return round(z, 4), round(mean, 8), round(std, 8), n


def compute_pair_stats(pair_a, pair_b):
    """
    Compute z-scores for the ratio price_a / price_b at all LOOKBACK_WINDOWS.

    Returns a dict with z_score_240/480/720, plus z_score (480, backwards compat),
    or None if there is insufficient data.
    """
    closes_a = load_closes(pair_a)
    closes_b = load_closes(pair_b)

    if not closes_a or not closes_b:
        return None

    common_ts = sorted(set(closes_a.keys()) & set(closes_b.keys()))
    if len(common_ts) < 48:
        return None

    # Compute z-score at each lookback window
    z_by_lb = {}
    for lb in LOOKBACK_WINDOWS:
        result = _z_for_window(closes_a, closes_b, common_ts, lb)
        if result:
            z_by_lb[lb] = result

    if not z_by_lb:
        return None

    # Use 480 as primary; fall back to closest available
    primary_lb   = 480 if 480 in z_by_lb else min(z_by_lb.keys(), key=lambda x: abs(x - 480))
    z_pri, mean_pri, std_pri, n_pri = z_by_lb[primary_lb]

    # Momentum from primary window
    recent_ts  = common_ts[-primary_lb:]
    ratios_pri = [closes_a[ts] / closes_b[ts] for ts in recent_ts if closes_b.get(ts, 0) != 0]
    z_series   = [(r - mean_pri) / std_pri for r in ratios_pri[-7:]] if len(ratios_pri) >= 7 else []
    z_momentum = round(z_series[-1] - z_series[0], 4) if len(z_series) >= 2 else 0.0

    current_ratio = ratios_pri[-1] if ratios_pri else 0.0
    price_a = closes_a.get(common_ts[-1])
    price_b = closes_b.get(common_ts[-1])

    stats = {
        "pair_a":        pair_a,
        "pair_b":        pair_b,
        "key":           f"{pair_a}/{pair_b}",
        "current_ratio": round(current_ratio, 8),
        "ratio_mean":    mean_pri,
        "ratio_std":     std_pri,
        "z_score":       z_pri,          # backwards compat — always the 480 window
        "z_momentum":    z_momentum,
        "n_samples":     n_pri,
        "price_a":       price_a,
        "price_b":       price_b,
        "computed_at":   datetime.now(timezone.utc).isoformat(),
    }
    # Per-window z-scores for bots with custom lookbacks
    for lb, (z, _, _, _) in z_by_lb.items():
        stats[f"z_score_{lb}"] = z

    return stats


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Arb spread statistics")
    parser.add_argument("--show", action="store_true", help="Print z-score table")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    stats = {}
    print("Computing arb spread statistics...")
    for pair_a, pair_b in SPREAD_PAIRS:
        key = f"{pair_a}/{pair_b}"
        result = compute_pair_stats(pair_a, pair_b)
        if result:
            stats[key] = result
            z_parts = "  ".join(
                f"z{lb}={result[f'z_score_{lb}']:+.3f}"
                for lb in LOOKBACK_WINDOWS if f"z_score_{lb}" in result
            )
            print(f"  {key:<22} {z_parts}  ratio={result['current_ratio']:.6f}")
        else:
            print(f"  {key:<22} insufficient data (need history in {HISTORY_DIR})")

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pairs": stats,
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved {len(stats)} pairs → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
