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
    ("ETH/USD", "BTC/USD"),   # fenrir
    ("SOL/USD", "ETH/USD"),   # jormungandr
    ("AVAX/USD", "ETH/USD"),  # ymir
    ("LINK/USD", "ETH/USD"),  # surt
    ("SOL/USD", "BTC/USD"),   # fafnir
]

LOOKBACK_HOURS = 480  # 20-day rolling window


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

def compute_pair_stats(pair_a, pair_b, lookback_hours=LOOKBACK_HOURS):
    """
    Compute rolling z-score for the ratio price_a / price_b.

    Returns a dict with current z-score, mean, std, and metadata,
    or None if there is insufficient data.
    """
    closes_a = load_closes(pair_a)
    closes_b = load_closes(pair_b)

    if not closes_a or not closes_b:
        return None

    # Align on common timestamps
    common_ts = sorted(set(closes_a.keys()) & set(closes_b.keys()))
    if len(common_ts) < 48:  # need at least 2 days of data
        return None

    # Use most recent lookback_hours data points
    recent_ts = common_ts[-lookback_hours:]
    ratios = []
    for ts in recent_ts:
        b = closes_b[ts]
        if b == 0:
            continue
        ratios.append(closes_a[ts] / b)

    n = len(ratios)
    if n < 24:
        return None

    # Full-window mean and std
    mean = sum(ratios) / n
    variance = sum((r - mean) ** 2 for r in ratios) / n
    std = math.sqrt(variance)
    if std == 0:
        return None

    current_ratio = ratios[-1]
    z_score = (current_ratio - mean) / std

    # Short-term z-score momentum (change over last 6 candles)
    z_recent = [(r - mean) / std for r in ratios[-7:]]
    z_momentum = round(z_recent[-1] - z_recent[0], 4)

    # Latest raw prices
    price_a = closes_a.get(recent_ts[-1])
    price_b = closes_b.get(recent_ts[-1])

    return {
        "pair_a":        pair_a,
        "pair_b":        pair_b,
        "key":           f"{pair_a}/{pair_b}",
        "current_ratio": round(current_ratio, 8),
        "ratio_mean":    round(mean, 8),
        "ratio_std":     round(std, 8),
        "z_score":       round(z_score, 4),
        "z_momentum":    z_momentum,   # positive = spreading away from mean
        "n_samples":     n,
        "lookback_hours": lookback_hours,
        "price_a":       price_a,
        "price_b":       price_b,
        "computed_at":   datetime.now(timezone.utc).isoformat(),
    }


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
            direction = "SHORT spread" if result["z_score"] > 0 else "LONG spread "
            signal = (
                f"  *** ENTRY SIGNAL [{direction}]" if abs(result["z_score"]) >= 2.0
                else ""
            )
            print(f"  {key:<22} z={result['z_score']:+6.3f}  "
                  f"ratio={result['current_ratio']:.6f}  "
                  f"mean={result['ratio_mean']:.6f}  "
                  f"n={result['n_samples']}{signal}")
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
