#!/usr/bin/env python3
"""
prepare.py - Fetch 2 years of OHLCV data for Volva research.

Source : Binance public API (no key needed, best free historical coverage)
Pairs  : BTC/USD, ETH/USD, SOL/USD
Output : /root/.openclaw/workspace/research/data/
         BTC_USD_5m.csv, ETH_USD_5m.csv, SOL_USD_5m.csv  (day league)
         BTC_USD_1h.csv, ETH_USD_1h.csv, SOL_USD_1h.csv  (swing league)

CSV columns: timestamp(ms), open, high, low, close, volume

Usage:
  python3 prepare.py               # full 2yr fetch, all leagues
  python3 prepare.py --league day  # 5-min only
  python3 prepare.py --league swing# 1h only
  python3 prepare.py --refresh     # append only new candles since last stored
"""
import argparse
import csv
import json
import os
import time
import urllib.request
from datetime import datetime, timezone, timedelta

DATA_DIR = "/root/.openclaw/workspace/research/data"
YEARS    = 2

PAIRS = {
    "BTC/USD": "BTCUSDT",
    "ETH/USD": "ETHUSDT",
    "SOL/USD": "SOLUSDT",
}

LEAGUES = {
    "day":   {"interval": "5m",  "minutes": 5,  "limit": 1000},
    "swing": {"interval": "1h",  "minutes": 60, "limit": 1000},
}


def binance_klines(symbol, interval, start_ms, end_ms, limit=1000):
    url = (
        "https://api.binance.com/api/v3/klines"
        "?symbol=" + symbol +
        "&interval=" + interval +
        "&startTime=" + str(start_ms) +
        "&endTime=" + str(end_ms) +
        "&limit=" + str(limit)
    )
    req = urllib.request.Request(url, headers={"User-Agent": "volva-research/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def fetch_pair(symbol, interval, minutes_per_candle, limit, start_ms):
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    all_candles = []
    page = 0
    cur = start_ms
    while cur < now_ms - minutes_per_candle * 60 * 1000:
        end_ms = min(cur + limit * minutes_per_candle * 60 * 1000, now_ms)
        candles = binance_klines(symbol, interval, cur, end_ms, limit)
        if not candles:
            break
        all_candles.extend(candles)
        page += 1
        newest = datetime.fromtimestamp(candles[-1][0] / 1000, tz=timezone.utc)
        print(f"    page {page}: {len(candles)} candles -> {newest.strftime('%Y-%m-%d %H:%M')}")
        cur = candles[-1][0] + minutes_per_candle * 60 * 1000
        time.sleep(0.15)
    return all_candles


def last_timestamp(path):
    if not os.path.exists(path):
        return None
    last = None
    with open(path) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row:
                last = int(row[0])
    return last


def save_csv(candles, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for c in candles:
            # Binance: [open_time, open, high, low, close, volume, ...]
            w.writerow([c[0], c[1], c[2], c[3], c[4], c[5]])
    print(f"    Saved {len(candles):,} rows -> {path}")


def append_csv(candles, path):
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        for c in candles:
            w.writerow([c[0], c[1], c[2], c[3], c[4], c[5]])
    print(f"    Appended {len(candles):,} new rows -> {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league", choices=["day", "swing"])
    parser.add_argument("--refresh", action="store_true",
                        help="Only fetch candles newer than last stored timestamp")
    args = parser.parse_args()

    leagues = [args.league] if args.league else list(LEAGUES.keys())
    now_ts = datetime.now(timezone.utc)

    for league in leagues:
        cfg = LEAGUES[league]
        print(f"\n[{league.upper()}] interval={cfg['interval']}  years={YEARS}")
        for display_pair, symbol in PAIRS.items():
            fname = display_pair.replace("/", "_") + "_" + cfg["interval"] + ".csv"
            path  = os.path.join(DATA_DIR, fname)
            print(f"  {display_pair}...")

            if args.refresh:
                last_ts = last_timestamp(path)
                if last_ts is None:
                    print("    No existing data -- doing full fetch.")
                    start_ms = int((now_ts - timedelta(days=365 * YEARS)).timestamp() * 1000)
                else:
                    start_ms = last_ts + cfg["minutes"] * 60 * 1000
                    dt = datetime.fromtimestamp(last_ts/1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
                    print(f"    Refreshing from {dt}")
            else:
                start_ms = int((now_ts - timedelta(days=365 * YEARS)).timestamp() * 1000)

            try:
                candles = fetch_pair(symbol, cfg["interval"], cfg["minutes"],
                                     cfg["limit"], start_ms)
                if not candles:
                    print("    No new candles.")
                    continue
                if args.refresh and os.path.exists(path):
                    append_csv(candles, path)
                else:
                    save_csv(candles, path)
            except Exception as e:
                print(f"    ERROR: {e}")
            time.sleep(1)

    print("\nDone.")
    print("Weekly refresh cron: 0 6 * * 1 python3 /root/.openclaw/workspace/research/prepare.py --refresh")


if __name__ == "__main__":
    main()
