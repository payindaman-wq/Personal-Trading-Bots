#!/usr/bin/env python3
"""
HEIMDALL — Alpha Hunter Officer
Scans for emerging crypto opportunities every 30 minutes.

Sources:
  1. CoinGecko trending coins     (top 10 trending — no key)
  2. CoinGecko sector performance (top gaining / losing categories — no key)
  3. DexScreener boosted tokens   (projects actively promoted on-chain — no key)
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

WORKSPACE   = "/root/.openclaw/workspace"
STATE_PATH  = os.path.join(WORKSPACE, "research", "heimdall_state.json")
LOG_MAX     = 48   # 24 hours of 30-min snapshots

HEADERS = {"User-Agent": "OpenClaw/1.0"}

# ── Helpers ───────────────────────────────────────────────────────────────────
def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return None


def ts_now():
    return datetime.now(timezone.utc).isoformat()


# ── Signal 1: CoinGecko Trending Coins ───────────────────────────────────────
def fetch_trending_coins():
    data = fetch_json("https://api.coingecko.com/api/v3/search/trending")
    if not data:
        return {"ok": False, "error": "fetch failed", "coins": []}
    try:
        coins = []
        for item in (data.get("coins") or [])[:10]:
            c = item.get("item", {})
            coins.append({
                "rank":           c.get("market_cap_rank"),
                "name":           c.get("name"),
                "symbol":         c.get("symbol", "").upper(),
                "score":          round(c.get("score", 0), 2),
                "price_btc":      c.get("price_btc"),
                "data": {
                    "price_change_24h": (c.get("data") or {}).get("price_change_percentage_24h", {}).get("usd"),
                    "market_cap":       (c.get("data") or {}).get("market_cap"),
                    "volume_24h":       (c.get("data") or {}).get("total_volume"),
                }
            })
        return {"ok": True, "coins": coins}
    except Exception as e:
        return {"ok": False, "error": str(e), "coins": []}


# ── Signal 2: CoinGecko Sector Performance ────────────────────────────────────
def fetch_sectors():
    data = fetch_json("https://api.coingecko.com/api/v3/coins/categories")
    if not data or not isinstance(data, list):
        return {"ok": False, "error": "fetch failed", "top_gainers": [], "top_losers": []}
    try:
        valid = [c for c in data if c.get("market_cap_change_24h") is not None]
        valid.sort(key=lambda x: x["market_cap_change_24h"], reverse=True)
        def fmt(c):
            return {
                "name":          c.get("name"),
                "change_24h":    round(c["market_cap_change_24h"], 2),
                "volume_24h":    c.get("volume_24h"),
                "market_cap":    c.get("market_cap"),
                "num_coins":     c.get("coins_count"),
            }
        return {
            "ok":          True,
            "top_gainers": [fmt(c) for c in valid[:5]],
            "top_losers":  [fmt(c) for c in valid[-5:][::-1]],
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "top_gainers": [], "top_losers": []}


# ── Signal 3: DexScreener Boosted Tokens ──────────────────────────────────────
def fetch_dex_trending():
    data = fetch_json("https://api.dexscreener.com/token-boosts/latest/v1")
    if not data or not isinstance(data, list):
        return {"ok": False, "error": "fetch failed", "tokens": []}
    try:
        seen = set()
        tokens = []
        for item in data:
            addr = item.get("tokenAddress", "")
            if addr in seen:
                continue
            seen.add(addr)
            tokens.append({
                "chain":       item.get("chainId"),
                "name":        (item.get("description") or addr)[:60],
                "symbol":      item.get("symbol"),
                "url":         item.get("url"),
                "boosts":      item.get("totalAmount"),
            })
            if len(tokens) >= 10:
                break
        return {"ok": True, "tokens": tokens}
    except Exception as e:
        return {"ok": False, "error": str(e), "tokens": []}


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    prev_state = {}
    if os.path.exists(STATE_PATH):
        try:
            prev_state = json.load(open(STATE_PATH))
        except Exception:
            pass

    ts          = ts_now()
    trending    = fetch_trending_coins()
    sectors     = fetch_sectors()
    dex         = fetch_dex_trending()

    # Summarise top coins for quick log
    top_coins_str = ", ".join(
        f"{c['symbol']}({c['data']['price_change_24h']:+.1f}%)" if c['data']['price_change_24h'] is not None
        else c['symbol']
        for c in (trending.get("coins") or [])[:5]
    ) if trending["ok"] else "n/a"

    top_sector_str = ""
    if sectors["ok"] and sectors["top_gainers"]:
        g = sectors["top_gainers"][0]
        top_sector_str = f"{g['name']} +{g['change_24h']}%"

    log_entry = {
        "ts":          ts,
        "top_coins":   top_coins_str,
        "top_sector":  top_sector_str,
        "dex_count":   len(dex.get("tokens") or []),
    }

    log = [log_entry] + (prev_state.get("log") or [])
    log = log[:LOG_MAX]

    new_state = {
        "ts":              ts,
        "trending_coins":  trending,
        "sectors":         sectors,
        "dex_trending":    dex,
        "log":             log,
    }

    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(new_state, f, indent=2)

    ok_signals = sum([trending["ok"], sectors["ok"], dex["ok"]])
    print(f"[{ts}] HEIMDALL OK ({ok_signals}/3) | Trending: {top_coins_str} | Hot sector: {top_sector_str or 'n/a'}")


if __name__ == "__main__":
    main()
