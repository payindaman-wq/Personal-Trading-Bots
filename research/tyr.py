#!/usr/bin/env python3
"""
TYR — Risk Officer
Composite macro watchdog. Aggregates 5 signals every 30 minutes and issues
a fleet-wide risk regime directive.

Signals:
  1. Fear & Greed Index     (alternative.me)
  2. BTC Dominance          (CoinGecko)
  3. VIX                    (Yahoo Finance)
  4. DXY 1-day change       (Yahoo Finance)
  5. Perpetual funding rate (Binance futures, no auth)
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

WORKSPACE       = "/root/.openclaw/workspace"
STATE_PATH      = os.path.join(WORKSPACE, "research", "tyr_state.json")
FINNHUB_SECRET  = "/root/.openclaw/secrets/finnhub.json"
LOG_MAX    = 96  # 48 hours of 30-min readings

# ── Thresholds ────────────────────────────────────────────────────────────────
FG_EXTREME_FEAR  = 20
FG_FEAR          = 35
FG_GREED         = 65
FG_EXTREME_GREED = 80

BTC_DOM_CAUTION  = 58.0
BTC_DOM_DANGER   = 65.0

STABLE_DOM_CAUTION = 12.0
STABLE_DOM_DANGER  = 15.0

OI_CHANGE_CAUTION  = 5.0
OI_CHANGE_DANGER   = 10.0

LS_LONG_CAUTION    = 1.8
LS_LONG_DANGER     = 2.5
LS_SHORT_CAUTION   = 0.6

VIX_CAUTION      = 25.0   # elevated volatility
VIX_DANGER       = 35.0   # market panic

DXY_CHANGE_CAUTION = 0.75  # % gain in 1 day → dollar surging
DXY_CHANGE_DANGER  = 1.50

FUNDING_HIGH_CAUTION = 0.08   # % per 8h → overleveraged longs
FUNDING_HIGH_DANGER  = 0.15
FUNDING_LOW_CAUTION  = -0.05  # % per 8h → crowded shorts


NEWS_BEARISH_CAUTION = -10   # net score < -10 → CAUTION
NEWS_BEARISH_DANGER  = -25   # net score < -25 → DANGER


FUNDING_PAIRS = [
    "BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT","DOGEUSDT",
    "AVAXUSDT","LINKUSDT","UNIUSDT","AAVEUSDT","NEARUSDT",
    "APTUSDT","SUIUSDT","ARBUSDT","OPUSDT","ADAUSDT","POLUSDT",
]


# ── Fetchers ──────────────────────────────────────────────────────────────────

def fetch_fear_greed():
    try:
        with urllib.request.urlopen("https://api.alternative.me/fng/?limit=1", timeout=10) as r:
            e = json.loads(r.read())["data"][0]
        return {"value": int(e["value"]), "label": e["value_classification"], "ok": True}
    except Exception as ex:
        return {"ok": False, "error": str(ex)}


def fetch_coingecko_global():
    try:
        req = urllib.request.Request(
            "https://api.coingecko.com/api/v3/global",
            headers={"User-Agent": "tyr-watchdog/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            pcts = json.loads(r.read())["data"]["market_cap_percentage"]
        btc_dom    = round(float(pcts.get("btc", 0)), 2)
        stable_dom = round(
            pcts.get("usdt", 0) + pcts.get("usdc", 0) +
            pcts.get("dai",  0) + pcts.get("busd", 0), 2
        )
        return {"btc_dom": btc_dom, "stable_dom": stable_dom, "ok": True}
    except Exception as ex:
        return {"ok": False, "error": str(ex)}

def fetch_btc_dominance():
    result = fetch_coingecko_global()
    if result["ok"]:
        return {"value": result["btc_dom"], "ok": True}
    return result


def _yahoo_chart(symbol, range_="5d"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range={range_}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def fetch_vix():
    try:
        data   = _yahoo_chart("%5EVIX")
        closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        closes = [c for c in closes if c is not None]
        value  = round(closes[-1], 2)
        label  = ("Extreme" if value > VIX_DANGER else
                  "Elevated" if value > VIX_CAUTION else "Normal")
        return {"value": value, "label": label, "ok": True}
    except Exception as ex:
        return {"ok": False, "error": str(ex)}


def fetch_dxy():
    try:
        data   = _yahoo_chart("DX-Y.NYB")
        closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        closes = [c for c in closes if c is not None]
        current  = round(closes[-1], 3)
        previous = round(closes[-2], 3) if len(closes) >= 2 else current
        change_pct = round((current - previous) / previous * 100, 3)
        label = ("Surging" if change_pct > DXY_CHANGE_DANGER else
                 "Rising"  if change_pct > DXY_CHANGE_CAUTION else
                 "Falling" if change_pct < -DXY_CHANGE_CAUTION else "Stable")
        return {"value": current, "change_1d_pct": change_pct, "label": label, "ok": True}
    except Exception as ex:
        return {"ok": False, "error": str(ex)}


def fetch_funding_rates():
    try:
        url = "https://fapi.binance.com/fapi/v1/premiumIndex"
        req = urllib.request.Request(url, headers={"User-Agent": "tyr-watchdog/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        rates = {}
        for entry in data:
            if entry["symbol"] in FUNDING_PAIRS:
                rates[entry["symbol"]] = float(entry["lastFundingRate"]) * 100  # → %
        if not rates:
            return {"ok": False, "error": "no matching pairs"}
        avg = round(sum(rates.values()) / len(rates), 5)
        label = ("Extreme Greed" if avg > FUNDING_HIGH_DANGER else
                 "Overleveraged" if avg > FUNDING_HIGH_CAUTION else
                 "Crowded Short" if avg < FUNDING_LOW_CAUTION else "Neutral")
        return {"avg_pct": avg, "label": label, "pair_count": len(rates), "ok": True}
    except Exception as ex:
        return {"ok": False, "error": str(ex)}


def fetch_open_interest(prev_oi=None):
    try:
        req = urllib.request.Request(
            "https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT",
            headers={"User-Agent": "tyr-watchdog/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            oi = float(json.loads(r.read())["openInterest"])
        change_pct = None
        if prev_oi and prev_oi > 0:
            change_pct = round((oi - prev_oi) / prev_oi * 100, 3)
        return {"value": round(oi, 2), "change_pct": change_pct, "ok": True}
    except Exception as ex:
        return {"ok": False, "error": str(ex)}


def fetch_long_short_ratio():
    try:
        req = urllib.request.Request(
            "https://fapi.binance.com/futures/data/globalLongShortAccountRatio"
            "?symbol=BTCUSDT&period=1h&limit=1",
            headers={"User-Agent": "tyr-watchdog/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        ratio     = round(float(data[0]["longShortRatio"]), 4)
        long_pct  = round(float(data[0]["longAccount"])  * 100, 1)
        short_pct = round(float(data[0]["shortAccount"]) * 100, 1)
        label = ("Crowded Long"  if ratio > LS_LONG_DANGER  else
                 "Long-Heavy"    if ratio > LS_LONG_CAUTION  else
                 "Crowded Short" if ratio < LS_SHORT_CAUTION else "Balanced")
        return {"ratio": ratio, "long_pct": long_pct, "short_pct": short_pct,
                "label": label, "ok": True}
    except Exception as ex:
        return {"ok": False, "error": str(ex)}


NEWS_FEEDS = [
    ('CoinDesk',      'https://www.coindesk.com/arc/outboundfeeds/rss/'),
    ('Cointelegraph', 'https://cointelegraph.com/rss'),
    ('Decrypt',       'https://decrypt.co/feed'),
]

BEARISH_TERMS = [
    'crash', 'dump', 'bear', 'sell-off', 'selloff', 'collapse', 'hack', 'exploit',
    'ban', 'banned', 'crackdown', 'lawsuit', 'sec charges', 'regulation', 'restrict',
    'liquidat', 'panic', 'fear', 'plunge', 'plummet', 'tumble', 'drop', 'decline',
    'warning', 'fraud', 'scam', 'rug', 'insolvent', 'bankrupt', 'loss', 'recession',
    'inflation', 'tariff', 'sanctions',
]
BULLISH_TERMS = [
    'bull', 'rally', 'surge', 'pump', 'ath', 'all-time high', 'adoption', 'approval',
    'etf', 'institutional', 'breakout', 'buy', 'accumulate', 'moon', 'soar', 'spike',
    'gain', 'rise', 'rise', 'upgrade', 'launch', 'partnership', 'integration',
    'record', 'milestone', 'growth', 'recover', 'rebound', 'support',
]

def fetch_news_sentiment():
    import xml.etree.ElementTree as ET
    headlines = []
    sources   = []
    for name, url in NEWS_FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                root = ET.fromstring(r.read())
            titles = [item.findtext("title") or "" for item in root.iter("item")][:15]
            headlines.extend(titles)
            sources.append(name)
        except Exception:
            pass
    # Finnhub crypto news (headline + summary for richer scoring)
    try:
        fh_key = json.load(open(FINNHUB_SECRET)).get("finnhub_api_key", "")
        if fh_key:
            fh_url = f"https://finnhub.io/api/v1/news?category=crypto&token={fh_key}"
            req = urllib.request.Request(fh_url, headers={"User-Agent": "tyr-watchdog/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                articles = json.loads(r.read())[:25]
            for a in articles:
                h = (a.get("headline") or "").strip()
                s = (a.get("summary") or "").strip()
                if h:
                    headlines.append(h + (" " + s if s else ""))
            sources.append("Finnhub")
    except Exception:
        pass

    if not headlines:
        return {"ok": False, "error": "all feeds failed"}

    bearish = 0
    bullish = 0
    for h in headlines:
        hl = h.lower()
        if any(t in hl for t in BEARISH_TERMS):
            bearish += 1
        if any(t in hl for t in BULLISH_TERMS):
            bullish += 1

    total     = len(headlines)
    net_score = round((bullish - bearish) / total * 100, 1)  # -100 to +100
    label     = ("Very Bearish" if net_score < -20 else
                 "Bearish"      if net_score < -5  else
                 "Very Bullish" if net_score > 20  else
                 "Bullish"      if net_score > 5   else "Neutral")
    # Sample top bearish headlines for MIMIR context
    bearish_headlines = [h for h in headlines if any(t in h.lower() for t in BEARISH_TERMS)][:3]
    return {
        "ok":               True,
        "net_score":        net_score,
        "label":            label,
        "bullish_count":    bullish,
        "bearish_count":    bearish,
        "total_headlines":  total,
        "sources":          sources,
        "bearish_headlines": bearish_headlines,
    }


# ── Regime evaluation ─────────────────────────────────────────────────────────

def evaluate_regime(fg, cg_global, vix, dxy, funding, news, oi, ls):
    signals = []
    level   = "normal"

    def escalate(to):
        nonlocal level
        if to == "danger" or (to == "caution" and level == "normal"):
            level = to

    # Fear & Greed
    if fg["ok"]:
        v = fg["value"]
        if v < FG_EXTREME_FEAR:
            signals.append(f"F&G {v} (Extreme Fear)")
            escalate("danger")
        elif v < FG_FEAR:
            signals.append(f"F&G {v} (Fear)")
            escalate("caution")
        elif v > FG_EXTREME_GREED:
            signals.append(f"F&G {v} (Extreme Greed)")
            escalate("danger")
        elif v > FG_GREED:
            signals.append(f"F&G {v} (Greed)")
            escalate("caution")

    # BTC Dominance + Stablecoin Dominance
    if cg_global["ok"]:
        d = cg_global["btc_dom"]
        if d > BTC_DOM_DANGER:
            signals.append(f"BTC dom {d}% (extreme alt risk)")
            escalate("danger")
        elif d > BTC_DOM_CAUTION:
            signals.append(f"BTC dom {d}% (elevated alt risk)")
            escalate("caution")
        s = cg_global["stable_dom"]
        if s > STABLE_DOM_DANGER:
            signals.append(f"Stablecoin dom {s}% (capital fleeing to safety)")
            escalate("danger")
        elif s > STABLE_DOM_CAUTION:
            signals.append(f"Stablecoin dom {s}% (elevated safe haven demand)")
            escalate("caution")

    # VIX
    if vix["ok"]:
        v = vix["value"]
        if v > VIX_DANGER:
            signals.append(f"VIX {v} (market panic)")
            escalate("danger")
        elif v > VIX_CAUTION:
            signals.append(f"VIX {v} (elevated volatility)")
            escalate("caution")

    # DXY
    if dxy["ok"]:
        c = dxy["change_1d_pct"]
        if c > DXY_CHANGE_DANGER:
            signals.append(f"DXY +{c}% today (dollar surging)")
            escalate("danger")
        elif c > DXY_CHANGE_CAUTION:
            signals.append(f"DXY +{c}% today (dollar rising)")
            escalate("caution")

    # Funding rates
    if funding["ok"]:
        f = funding["avg_pct"]
        if f > FUNDING_HIGH_DANGER:
            signals.append(f"Funding {f:.4f}% (extreme long leverage)")
            escalate("danger")
        elif f > FUNDING_HIGH_CAUTION:
            signals.append(f"Funding {f:.4f}% (overleveraged longs)")
            escalate("caution")
        elif f < FUNDING_LOW_CAUTION:
            signals.append(f"Funding {f:.4f}% (crowded shorts)")
            escalate("caution")

    # News sentiment
    if news["ok"]:
        s = news["net_score"]
        if s < NEWS_BEARISH_DANGER:
            signals.append(f"News sentiment {s} (very bearish headlines)")
            escalate("danger")
        elif s < NEWS_BEARISH_CAUTION:
            signals.append(f"News sentiment {s} (bearish headlines)")
            escalate("caution")

    # Open Interest change
    if oi["ok"] and oi["change_pct"] is not None:
        c = oi["change_pct"]
        if c > OI_CHANGE_DANGER:
            signals.append(f"OI +{c}% in 30 min (extreme leverage buildup)")
            escalate("danger")
        elif c > OI_CHANGE_CAUTION:
            signals.append(f"OI +{c}% in 30 min (leverage buildup)")
            escalate("caution")

    # Long/Short ratio
    if ls["ok"]:
        r = ls["ratio"]
        if r > LS_LONG_DANGER:
            signals.append(f"L/S ratio {r} (dangerously crowded longs)")
            escalate("danger")
        elif r > LS_LONG_CAUTION:
            signals.append(f"L/S ratio {r} (crowded longs)")
            escalate("caution")
        elif r < LS_SHORT_CAUTION:
            signals.append(f"L/S ratio {r} (crowded shorts)")
            escalate("caution")

    modifiers = {"normal": 1.00, "caution": 0.50, "danger": 0.25}
    actions   = {
        "normal":  "Normal position sizing.",
        "caution": "Reduce position sizes to 50%.",
        "danger":  "Reduce position sizes to 25%.",
    }
    regimes = {"normal": "NORMAL", "caution": "CAUTION", "danger": "DANGER"}

    signal_str = " | ".join(signals) if signals else "Macro conditions nominal."
    message    = f"{signal_str} {actions[level]}"

    return regimes[level], level, modifiers[level], message


# ── State I/O ─────────────────────────────────────────────────────────────────

def load_state():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH))
        except Exception:
            pass
    return {"log": []}


def main():
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[tyr] {ts} — fetching signals...")

    fg        = fetch_fear_greed()
    cg_global = fetch_coingecko_global()
    vix       = fetch_vix()
    dxy       = fetch_dxy()
    funding   = fetch_funding_rates()
    news      = fetch_news_sentiment()
    prev_state = load_state()
    prev_oi    = (prev_state.get("open_interest") or {}).get("value")
    oi         = fetch_open_interest(prev_oi)
    ls         = fetch_long_short_ratio()

    for name, val in [("F&G", fg), ("CG_GLOBAL", cg_global), ("VIX", vix),
                      ("DXY", dxy), ("FUNDING", funding), ("OI", oi),
                      ("L/S", ls), ("NEWS", news)]:
        print(f"[tyr]   {name}: {val}")

    regime, level, modifier, message = evaluate_regime(fg, cg_global, vix, dxy, funding, news, oi, ls)
    print(f"[tyr] Regime={regime} | {message}")

    state = prev_state
    log   = state.get("log", [])
    log.insert(0, {
        "ts":               ts,
        "regime":           regime,
        "level":            level,
        "message":          message,
        "position_modifier": modifier,
        "fear_greed":       fg.get("value") if fg["ok"] else None,
        "fear_greed_label": fg.get("label") if fg["ok"] else None,
        "btc_dominance":    cg_global.get("btc_dom") if cg_global["ok"] else None,
        "vix":              vix.get("value") if vix["ok"] else None,
        "dxy":              dxy.get("value") if dxy["ok"] else None,
        "dxy_change_1d":    dxy.get("change_1d_pct") if dxy["ok"] else None,
        "funding_avg_pct":  funding.get("avg_pct") if funding["ok"] else None,
        "news_score":       news.get("net_score") if news["ok"] else None,
        "news_label":       news.get("label") if news["ok"] else None,
        "stable_dom":       cg_global.get("stable_dom") if cg_global["ok"] else None,
        "oi_value":         oi.get("value") if oi["ok"] else None,
        "oi_change_pct":    oi.get("change_pct") if oi["ok"] else None,
        "ls_ratio":         ls.get("ratio") if ls["ok"] else None,
    })
    log = log[:LOG_MAX]

    new_state = {
        "ts":      ts,
        "regime":  regime,
        "level":   level,
        "message": message,
        "directive": {
            "level":                  level,
            "message":                message,
            "position_size_modifier": modifier,
            "suspend_trading":        False,
        },
        "fear_greed":   {"value": fg.get("value") if fg["ok"] else None,
                         "label": fg.get("label") if fg["ok"] else None,
                         "ok": fg["ok"], "error": fg.get("error")},
        "btc_dominance": {"value": cg_global.get("btc_dom") if cg_global["ok"] else None,
                          "ok": cg_global["ok"], "error": cg_global.get("error")},
        "stable_dom":    {"value": cg_global.get("stable_dom") if cg_global["ok"] else None,
                          "ok": cg_global["ok"]},
        "open_interest": {"value": oi.get("value") if oi["ok"] else None,
                          "change_pct": oi.get("change_pct") if oi["ok"] else None,
                          "ok": oi["ok"], "error": oi.get("error")},
        "long_short":    {"ratio": ls.get("ratio") if ls["ok"] else None,
                          "long_pct": ls.get("long_pct") if ls["ok"] else None,
                          "short_pct": ls.get("short_pct") if ls["ok"] else None,
                          "label": ls.get("label") if ls["ok"] else None,
                          "ok": ls["ok"], "error": ls.get("error")},
        "vix":          {"value": vix.get("value") if vix["ok"] else None,
                         "label": vix.get("label") if vix["ok"] else None,
                         "ok": vix["ok"], "error": vix.get("error")},
        "dxy":          {"value": dxy.get("value") if dxy["ok"] else None,
                         "change_1d_pct": dxy.get("change_1d_pct") if dxy["ok"] else None,
                         "label": dxy.get("label") if dxy["ok"] else None,
                         "ok": dxy["ok"], "error": dxy.get("error")},
        "funding":      {"avg_pct": funding.get("avg_pct") if funding["ok"] else None,
                         "label": funding.get("label") if funding["ok"] else None,
                         "pair_count": funding.get("pair_count") if funding["ok"] else None,
                         "ok": funding["ok"], "error": funding.get("error")},
        "news":         {"net_score": news.get("net_score") if news["ok"] else None,
                         "label": news.get("label") if news["ok"] else None,
                         "bullish_count": news.get("bullish_count") if news["ok"] else None,
                         "bearish_count": news.get("bearish_count") if news["ok"] else None,
                         "total_headlines": news.get("total_headlines") if news["ok"] else None,
                         "sources": news.get("sources") if news["ok"] else None,
                         "bearish_headlines": news.get("bearish_headlines", []) if news["ok"] else [],
                         "ok": news["ok"], "error": news.get("error")},
        "thresholds": {
            "fear_greed":    {"extreme_fear": FG_EXTREME_FEAR, "fear": FG_FEAR,
                              "greed": FG_GREED, "extreme_greed": FG_EXTREME_GREED},
            "btc_dominance": {"caution": BTC_DOM_CAUTION, "danger": BTC_DOM_DANGER},
            "vix":           {"caution": VIX_CAUTION, "danger": VIX_DANGER},
            "dxy_change":    {"caution": DXY_CHANGE_CAUTION, "danger": DXY_CHANGE_DANGER},
            "funding":       {"high_caution": FUNDING_HIGH_CAUTION,
                              "high_danger":  FUNDING_HIGH_DANGER,
                              "low_caution":  FUNDING_LOW_CAUTION},
            "news":          {"bearish_caution": NEWS_BEARISH_CAUTION,
                              "bearish_danger":  NEWS_BEARISH_DANGER},
            "stable_dom":    {"caution": STABLE_DOM_CAUTION, "danger": STABLE_DOM_DANGER},
            "oi_change":     {"caution": OI_CHANGE_CAUTION,  "danger": OI_CHANGE_DANGER},
            "long_short":    {"long_caution": LS_LONG_CAUTION, "long_danger": LS_LONG_DANGER,
                              "short_caution": LS_SHORT_CAUTION},
        },
        "log": log,
    }

    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(new_state, f, indent=2)
    print(f"[tyr] Saved → {STATE_PATH}")


if __name__ == "__main__":
    main()
