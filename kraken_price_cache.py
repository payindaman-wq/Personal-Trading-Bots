#!/usr/bin/env python3
"""
kraken_price_cache.py - Shared Kraken price fetcher with /tmp cache.

Both futures_day_competition_tick.py and competition_tick.py import this
so only one Kraken API call is made per 5-minute window regardless of how
many ticks read prices.

Usage:
    from kraken_price_cache import get_prices
    prices = get_prices(['BTC/USD', 'ETH/USD', ...])
    # returns {'BTC/USD': {'last': 68000.0, 'bid': ..., 'ask': ...}, ...}
"""
import json, os, time, urllib.request
from datetime import datetime, timezone

CACHE_FILE = '/tmp/kraken_price_cache.json'
CACHE_TTL  = 270  # 4.5 minutes — safe within a 5-min tick window

KRAKEN_PAIR_MAP = {
    'BTC/USD':  'XBTUSD',  'ETH/USD':  'ETHUSD',  'SOL/USD':  'SOLUSD',
    'XRP/USD':  'XRPUSD',  'DOGE/USD': 'XDGUSD',  'AVAX/USD': 'AVAXUSD',
    'LINK/USD': 'LINKUSD', 'UNI/USD':  'UNIUSD',  'AAVE/USD': 'AAVEUSD',
    'NEAR/USD': 'NEARUSD', 'APT/USD':  'APTUSD',  'SUI/USD':  'SUIUSD',
    'ARB/USD':  'ARBUSD',  'OP/USD':   'OPUSD',   'ADA/USD':  'ADAUSD',
    'POL/USD':  'POLUSD',  'PEPE/USD': 'PEPEUSD', 'WIF/USD':  'WIFUSD',
}

KRAKEN_KEY_MAP = {v: k for k, v in KRAKEN_PAIR_MAP.items()}
# Kraken sometimes returns with X/Z prefixes
KRAKEN_KEY_MAP.update({
    'XXBTZUSD': 'BTC/USD', 'XETHZUSD': 'ETH/USD', 'XXRPZUSD': 'XRP/USD',
    'XXDGZUSD': 'DOGE/USD',
})


def _fetch_from_kraken(pairs):
    kraken_pairs = [KRAKEN_PAIR_MAP.get(p, p.replace('/', '')) for p in pairs]
    url = f"https://api.kraken.com/0/public/Ticker?pair={','.join(kraken_pairs)}"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())
    if data.get('error'):
        raise RuntimeError(str(data['error']))
    result = {}
    for k, v in data['result'].items():
        label = KRAKEN_KEY_MAP.get(k, k)
        result[label] = {
            'last': float(v['c'][0]),
            'bid':  float(v['b'][0]),
            'ask':  float(v['a'][0]),
            'vwap': float(v['p'][0]) if 'p' in v else None,
        }
    return result


def get_prices(pairs):
    """Return prices for the requested pairs.
    Reads from /tmp cache if fresh; otherwise fetches from Kraken and updates cache.
    """
    pairs_needed = set(pairs)

    # Try cache
    try:
        if os.path.exists(CACHE_FILE):
            age = time.time() - os.path.getmtime(CACHE_FILE)
            if age < CACHE_TTL:
                cached = json.load(open(CACHE_FILE))
                if pairs_needed.issubset(set(cached.get('prices', {}).keys())):
                    return {p: cached['prices'][p] for p in pairs}
    except Exception:
        pass

    # Fetch all pairs in one call (union of what's in cache + what we need)
    try:
        existing_pairs = set()
        if os.path.exists(CACHE_FILE):
            try:
                existing_pairs = set(json.load(open(CACHE_FILE)).get('prices', {}).keys())
            except Exception:
                pass
        all_pairs = list(pairs_needed | existing_pairs)
        fresh = _fetch_from_kraken(all_pairs)
    except Exception:
        # Fall back to fetching only what we need
        fresh = _fetch_from_kraken(list(pairs_needed))

    # Merge with any existing cache entries and write back
    try:
        existing = {}
        if os.path.exists(CACHE_FILE):
            try:
                existing = json.load(open(CACHE_FILE)).get('prices', {})
            except Exception:
                pass
        existing.update(fresh)
        with open(CACHE_FILE, 'w') as f:
            json.dump({'ts': datetime.now(timezone.utc).isoformat(), 'prices': existing}, f)
    except Exception:
        pass

    return {p: fresh[p] for p in pairs if p in fresh}
