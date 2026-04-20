"""
Kraken Derivatives US leverage caps per symbol.

Fallback table reflects Kraken Derivatives US retail (CFTC-regulated, CME-style
contracts) where effective leverage = 1 / initial_margin. Values chosen to be
conservative relative to typical initial-margin requirements on the US product.

Live pull queries Kraken's public Futures instruments endpoint (non-US Pro) and
derives max leverage = floor(1 / retail_initialMargin). Since the US product is
strictly less permissive than Pro, we take MIN(api, fallback) as the effective
cap — API can only tighten, never loosen, relative to the hardcoded US table.

Cache: /root/.openclaw/workspace/competition/kraken_leverage_cache.json
Refresh: stale after 24h → re-pull; on API failure, return fallback.
"""
import json
import os
import math
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

WORKSPACE = "/root/.openclaw/workspace"
CACHE_PATH = f"{WORKSPACE}/competition/kraken_leverage_cache.json"
INSTRUMENTS_URL = "https://futures.kraken.com/derivatives/api/v3/instruments"
CACHE_TTL_HOURS = 24
HTTP_TIMEOUT = 10

# Kraken Derivatives US retail leverage caps (conservative fallback).
# Update if Kraken publishes a tighter ladder.
FALLBACK_CAPS = {
    "BTC/USD": 3.0,
    "ETH/USD": 3.0,
    "SOL/USD": 2.0,
}

# Map our symbol format to Kraken Futures Pro perpetual symbol.
SYMBOL_MAP = {
    "BTC/USD": "PF_XBTUSD",
    "ETH/USD": "PF_ETHUSD",
    "SOL/USD": "PF_SOLUSD",
}


def _load_cache():
    if not os.path.exists(CACHE_PATH):
        return None
    try:
        with open(CACHE_PATH) as f:
            data = json.load(f)
        fetched = datetime.fromisoformat(data["fetched_at"])
        if datetime.now(timezone.utc) - fetched > timedelta(hours=CACHE_TTL_HOURS):
            return None
        return data["caps"]
    except Exception:
        return None


def _save_cache(caps):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump({
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "caps": caps,
        }, f, indent=2)


def _pull_live():
    req = urllib.request.Request(
        INSTRUMENTS_URL,
        headers={"User-Agent": "kraken-leverage/1.0"},
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        payload = json.load(resp)
    if payload.get("result") != "success":
        raise RuntimeError(f"instruments endpoint returned {payload.get('result')}")
    by_symbol = {inst["symbol"]: inst for inst in payload.get("instruments", [])}
    caps = {}
    for our_sym, kraken_sym in SYMBOL_MAP.items():
        inst = by_symbol.get(kraken_sym)
        if not inst:
            continue
        # Prefer retailMarginLevels; fall back to marginLevels.
        levels = inst.get("retailMarginLevels") or inst.get("marginLevels") or []
        if not levels:
            continue
        base_im = min(float(lvl.get("initialMargin", 1.0)) for lvl in levels)
        if base_im <= 0:
            continue
        caps[our_sym] = math.floor(1.0 / base_im)
    return caps


def get_caps():
    """Return {symbol: max_leverage} for Kraken Derivatives US.

    Caches result for 24h. Always bounded by FALLBACK_CAPS — live API can only
    tighten, never loosen, the cap relative to the hardcoded US-retail table.
    """
    cached = _load_cache()
    if cached:
        return {s: float(cached.get(s, FALLBACK_CAPS[s])) for s in FALLBACK_CAPS}

    live = {}
    try:
        live = _pull_live()
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, TimeoutError):
        pass

    effective = {}
    for sym, fb in FALLBACK_CAPS.items():
        api_val = live.get(sym)
        effective[sym] = float(min(api_val, fb)) if api_val else float(fb)

    try:
        _save_cache(effective)
    except Exception:
        pass
    return effective


def cap_for(symbol):
    """Per-symbol cap. Unknown symbol → 1.0 (no leverage allowed)."""
    return get_caps().get(symbol, 1.0)


def cap_for_strategy(pairs):
    """Strategy-level cap = MIN across pairs. Strategy leverage is flat,
    so the tightest symbol governs. Empty/unknown pairs → 1.0."""
    caps = get_caps()
    vals = [caps.get(p, 1.0) for p in (pairs or [])]
    return min(vals) if vals else 1.0


if __name__ == "__main__":
    import sys
    caps = get_caps()
    print(json.dumps(caps, indent=2))
    if len(sys.argv) > 1 and sys.argv[1] == "--pairs":
        print(f"strategy cap for BTC/ETH/SOL: {cap_for_strategy(['BTC/USD','ETH/USD','SOL/USD'])}")
