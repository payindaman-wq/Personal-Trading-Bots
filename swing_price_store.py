#!/usr/bin/env python3
"""
swing_price_store.py - Fetch and persist hourly candles for swing trading.

Maintains a 30-day rolling window of hourly OHLCV data for each pair,
stored as JSON files in competition/swing/price_history/.

Usage:
  python3 swing_price_store.py              # update all pairs
  python3 swing_price_store.py --init       # force full 30-day fetch
  python3 swing_price_store.py --show PAIR  # print latest candles for pair
"""
import os
import sys
import json
import argparse
import urllib.request
from datetime import datetime, timezone, timedelta

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
HISTORY_DIR  = os.path.join(WORKSPACE, "competition", "swing", "price_history")
FLEET_DIR    = os.path.join(WORKSPACE, "fleet", "swing")
CANDLE_INTERVAL = "1h"
KEEP_DAYS    = 30
MAX_CANDLES  = KEEP_DAYS * 24  # 720 hourly candles

KRAKEN_TO_HL = {
    "BTC/USD": "BTC", "ETH/USD": "ETH", "SOL/USD": "SOL", "XRP/USD": "XRP",
    "DOGE/USD": "DOGE", "AVAX/USD": "AVAX", "LINK/USD": "LINK", "UNI/USD": "UNI",
    "AAVE/USD": "AAVE", "NEAR/USD": "NEAR", "APT/USD": "APT", "SUI/USD": "SUI",
    "ARB/USD": "ARB", "OP/USD": "OP", "WIF/USD": "WIF", "PEPE/USD": "PEPE",
}

ALL_PAIRS = list(KRAKEN_TO_HL.keys())


# ---------------------------------------------------------------------------
# Candle fetching
# ---------------------------------------------------------------------------

def fetch_hourly_candles(coin, days=30):
    """Fetch hourly candles from Hyperliquid for the last N days."""
    end   = int(datetime.now(timezone.utc).timestamp() * 1000)
    start = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp() * 1000)
    payload = {
        "type": "candleSnapshot",
        "req": {"coin": coin, "interval": CANDLE_INTERVAL,
                "startTime": start, "endTime": end}
    }
    req = urllib.request.Request(
        "https://api.hyperliquid.xyz/info",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = json.loads(r.read())
    candles = []
    for c in raw:
        ts_ms = c.get("t", c.get("T", 0))
        ts_iso = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()
        candles.append({
            "ts":     ts_iso,
            "open":   float(c.get("o", c.get("open", 0))),
            "high":   float(c.get("h", c.get("high", 0))),
            "low":    float(c.get("l", c.get("low", 0))),
            "close":  float(c.get("c", c.get("close", 0))),
            "volume": float(c.get("v", c.get("volume", 0))),
        })
    return sorted(candles, key=lambda x: x["ts"])


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def history_path(pair):
    safe = pair.replace("/", "-")
    return os.path.join(HISTORY_DIR, f"{safe}.json")


def load_history(pair):
    path = history_path(pair)
    if not os.path.isfile(path):
        return []
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        print(f"  WARNING: corrupt price history for {pair} — resetting")
        os.remove(path)
        return []


def save_history(pair, candles):
    # Keep only the most recent MAX_CANDLES
    candles = sorted(candles, key=lambda x: x["ts"])[-MAX_CANDLES:]
    # Atomic write: write to temp file then rename to avoid race condition with readers
    import tempfile
    path = history_path(pair)
    tmp = path + '.tmp'
    with open(tmp, "w") as f:
        json.dump(candles, f)
    os.replace(tmp, path)


def merge_candles(existing, new_candles):
    """Merge new candles into existing, dedup by timestamp."""
    by_ts = {c["ts"]: c for c in existing}
    for c in new_candles:
        by_ts[c["ts"]] = c
    return sorted(by_ts.values(), key=lambda x: x["ts"])


# ---------------------------------------------------------------------------
# Price store interface (used by swing indicators)
# ---------------------------------------------------------------------------

def get_current_price(pair):
    """Latest close price for pair."""
    history = load_history(pair)
    if not history:
        return None
    return history[-1]["close"]


def get_price_n_hours_ago(pair, hours):
    """Close price approximately N hours ago."""
    history = load_history(pair)
    if not history:
        return None
    target = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    past = [c for c in history if c["ts"] <= target]
    return past[-1]["close"] if past else None


def get_price_series(pair, n_points, interval_hours=1):
    """
    Returns list of n_points close prices sampled at interval_hours,
    ordered oldest-first. Returns None if insufficient history.
    """
    prices = []
    for i in range(n_points):
        if i == 0:
            price = get_current_price(pair)
        else:
            price = get_price_n_hours_ago(pair, i * interval_hours)
        if price is None:
            return None
        prices.append(price)
    return list(reversed(prices))


def get_vwap(pair, period_hours=24):
    """Volume-weighted average price over period_hours."""
    history = load_history(pair)
    if not history:
        return None
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=period_hours)).isoformat()
    recent = [c for c in history if c["ts"] >= cutoff]
    if not recent:
        return None
    total_vol = sum(c["volume"] for c in recent)
    if total_vol == 0:
        return None
    vwap = sum(c["close"] * c["volume"] for c in recent) / total_vol
    return round(vwap, 6)


# ---------------------------------------------------------------------------
# Update logic
# ---------------------------------------------------------------------------

def update_pair(pair, full=False):
    coin = KRAKEN_TO_HL.get(pair)
    if not coin:
        print(f"  {pair}: no mapping, skip")
        return

    existing = load_history(pair)
    days_to_fetch = KEEP_DAYS if full or not existing else 2

    try:
        new_candles = fetch_hourly_candles(coin, days=days_to_fetch)
    except Exception as e:
        print(f"  {pair}: fetch error -- {e}")
        return

    merged = merge_candles(existing, new_candles)
    save_history(pair, merged)
    print(f"  {pair}: {len(merged)} candles  (latest: {merged[-1]['ts'][:16]}  close: {merged[-1]['close']})")


def show_pair(pair, n=10):
    history = load_history(pair)
    if not history:
        print(f"  No history for {pair}")
        return
    print(f"\n  {pair} -- last {n} hourly candles:")
    print(f"  {'TIMESTAMP':<22} {'OPEN':>10} {'HIGH':>10} {'LOW':>10} {'CLOSE':>10} {'VOL':>12}")
    print("  " + "-" * 78)
    for c in history[-n:]:
        print(f"  {c['ts'][:19]:<22} {c['open']:>10.4f} {c['high']:>10.4f} "
              f"{c['low']:>10.4f} {c['close']:>10.4f} {c['volume']:>12.2f}")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    os.makedirs(HISTORY_DIR, exist_ok=True)
    parser = argparse.ArgumentParser(description="Swing price store — hourly candles")
    parser.add_argument("--init", action="store_true", help="Force full 30-day fetch for all pairs")
    parser.add_argument("--show", metavar="PAIR",    help="Show latest candles for a pair (e.g. BTC/USD)")
    parser.add_argument("--pairs", nargs="+", default=ALL_PAIRS, help="Pairs to update")
    args = parser.parse_args()

    if args.show:
        show_pair(args.show)
        return

    print(f"Updating swing price history ({'full' if args.init else 'incremental'})...")
    for pair in args.pairs:
        update_pair(pair, full=args.init)
    update_spread_ratios()
    print("Done.")




# ---------------------------------------------------------------------------
# Spread ratio pairs
# ---------------------------------------------------------------------------

SPREAD_PAIRS = {
    "ETH_BTC_RATIO":  ("ETH/USD",  "BTC/USD"),
    "SOL_ETH_RATIO":  ("SOL/USD",  "ETH/USD"),
    "SOL_BTC_RATIO":  ("SOL/USD",  "BTC/USD"),
    "AVAX_ETH_RATIO": ("AVAX/USD", "ETH/USD"),
    "AVAX_SOL_RATIO": ("AVAX/USD", "SOL/USD"),
    "LINK_ETH_RATIO": ("LINK/USD", "ETH/USD"),
    "AAVE_ETH_RATIO": ("AAVE/USD", "ETH/USD"),
    "AAVE_LINK_RATIO": ("AAVE/USD", "LINK/USD"),
}


def update_spread_ratios():
    """
    Compute and store ratio candles for spread pairs.
    Must be called after regular pairs are updated.
    Ratio candle: base_close / quote_close per matching timestamp.
    """
    os.makedirs(HISTORY_DIR, exist_ok=True)
    for ratio_name, (base_pair, quote_pair) in SPREAD_PAIRS.items():
        base_hist  = load_history(base_pair)
        quote_hist = load_history(quote_pair)
        if not base_hist or not quote_hist:
            print(f"  {ratio_name}: insufficient history, skip")
            continue

        quote_by_ts = {c["ts"]: c for c in quote_hist}
        ratio_candles = []
        for bc in base_hist:
            qc = quote_by_ts.get(bc["ts"])
            if not qc:
                continue
            if qc["close"] <= 0 or qc["open"] <= 0 or qc["high"] <= 0 or qc["low"] <= 0:
                continue
            ratio_candles.append({
                "ts":     bc["ts"],
                "open":   bc["open"]  / qc["open"],
                "high":   bc["high"]  / qc["low"],
                "low":    bc["low"]   / qc["high"],
                "close":  bc["close"] / qc["close"],
                "volume": (bc["volume"] + qc["volume"]) / 2,
            })

        save_history(ratio_name, ratio_candles)
        latest = ratio_candles[-1]["close"] if ratio_candles else 0
        print(f"  {ratio_name}: {len(ratio_candles)} ratio candles  (latest: {latest:.6f})")


if __name__ == "__main__":
    main()
