#!/usr/bin/env python3
"""
pm_collector.py — Collects resolved prediction market data for Odin research.
Runs every 4h via cron. Appends new resolved markets to resolved_markets.jsonl.
Sources: Polymarket (Gamma API), Kalshi, Manifold.

Also tracks active Polymarket markets with real pre-resolution prices so that
FREYA's validation gate has ground-truth realized PnL data.
  - active_tracking.jsonl: markets being monitored (runtime state, not committed)
  - competition/polymarket/resolved_markets.jsonl: markets from tracking that resolved
"""
import json, os, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

RESEARCH_DIR  = "/root/.openclaw/workspace/research/polymarket"
OUTPUT_FILE   = f"{RESEARCH_DIR}/resolved_markets.jsonl"
STATE_FILE    = f"{RESEARCH_DIR}/collector_state.json"
ACTIVE_TRACKING_FILE = f"{RESEARCH_DIR}/active_tracking.jsonl"
COMP_RESOLVED_FILE = "/root/.openclaw/workspace/competition/polymarket/resolved_markets.jsonl"
KALSHI_SECRET = "/root/.openclaw/secrets/kalshi.json"

os.makedirs(RESEARCH_DIR, exist_ok=True)
os.makedirs(os.path.dirname(COMP_RESOLVED_FILE), exist_ok=True)


# ── HTTP ───────────────────────────────────────────────────────────────────

def api_get(url, headers=None, timeout=20):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "odin-pm-collector/1.0",
                 "Accept": "application/json", **(headers or {})}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  WARN {url[:70]}: {e}")
        return None


# ── Categorize ─────────────────────────────────────────────────────────────

def categorize(question, source_category=""):
    q = (question + " " + source_category).lower()
    if any(w in q for w in ["bitcoin", "btc", "ethereum", "eth", "solana",
                             "crypto", "token", "defi", "nft", "blockchain",
                             "altcoin", "stablecoin", "memecoin"]):
        return "crypto"
    if any(w in q for w in ["election", "vote", "president", "senate",
                             "congress", "party", "democrat", "republican",
                             "prime minister", "chancellor", "parliament",
                             "referendum", "ballot", "mayor", "governor"]):
        return "politics"
    if any(w in q for w in ["nfl", "nba", "mlb", "nhl", "soccer", "football",
                             "basketball", "baseball", "hockey", "tennis",
                             "golf", "ufc", "mma", "olympic", "world cup",
                             "championship", "super bowl", "playoff",
                             "march madness", "ncaa"]):
        return "sports"
    if any(w in q for w in ["gdp", "inflation", "fed", "interest rate",
                             "recession", "unemployment", "cpi", "tariff",
                             "stock market", "s&p", "nasdaq", "dow",
                             "earnings", "ipo", "merger"]):
        return "economics"
    return "world_events"


# ── Dedup ──────────────────────────────────────────────────────────────────

def load_seen():
    seen = set()
    if not os.path.exists(OUTPUT_FILE):
        return seen
    with open(OUTPUT_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    d = json.loads(line)
                    seen.add(d["source"] + "::" + d["market_id"])
                except Exception:
                    pass
    return seen


def append_market(record):
    with open(OUTPUT_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


# ── Polymarket research (resolved, for ODIN/FREYA historical simulation) ──

def fetch_polymarket(seen):
    new = 0
    offset = 0
    limit = 500
    for page in range(40):   # up to 20k markets
        url = (f"https://gamma-api.polymarket.com/markets"
               f"?closed=true&limit={limit}&offset={offset}")
        data = api_get(url)
        if not data or not isinstance(data, list) or len(data) == 0:
            break
        for m in data:
            mid = str(m.get("id", "") or m.get("conditionId", ""))
            if not mid:
                continue
            key = "polymarket::" + mid
            if key in seen:
                continue

            try:
                outcomes = json.loads(m.get("outcomes", "[]"))
                prices   = json.loads(m.get("outcomePrices", "[]"))
                prices_f = [float(p) for p in prices]
            except Exception:
                continue

            if len(prices_f) < 2 or len(outcomes) < 2:
                continue

            if outcomes[0] not in ("Yes", "YES") or outcomes[1] not in ("No", "NO"):
                continue

            yes_price = prices_f[0]
            no_price  = prices_f[1]

            if yes_price > 0.99 and no_price < 0.01:
                resolution = "yes"
            elif no_price > 0.99 and yes_price < 0.01:
                resolution = "no"
            else:
                continue

            question   = m.get("question", "") or m.get("title", "")
            pm_cat     = m.get("category", "")
            volume     = float(m.get("volume", 0) or 0)

            record = {
                "source":           "polymarket",
                "market_id":        mid,
                "question":         question,
                "category":         categorize(question, pm_cat),
                "resolution":       resolution,
                "resolution_value": 1.0 if resolution == "yes" else 0.0,
                "odds_close":       round(yes_price, 4),
                "volume_usd":       round(volume, 2),
                "resolved_at":      m.get("endDate") or m.get("closedTime", ""),
                "collected_at":     datetime.now(timezone.utc).isoformat(),
            }
            seen.add(key)
            append_market(record)
            new += 1

        offset += limit
        if len(data) < limit:
            break
        time.sleep(0.3)

    return new


# ── Polymarket active tracking (for FREYA validation gate) ─────────────────

def load_active_tracking():
    """Returns {market_id: record} of markets being monitored."""
    if not os.path.exists(ACTIVE_TRACKING_FILE):
        return {}
    tracking = {}
    with open(ACTIVE_TRACKING_FILE) as f:
        for line in f:
            try:
                d = json.loads(line.strip())
                if d and d.get("market_id"):
                    tracking[str(d["market_id"])] = d
            except Exception:
                pass
    return tracking


def save_active_tracking(tracking):
    with open(ACTIVE_TRACKING_FILE, "w") as f:
        for record in tracking.values():
            f.write(json.dumps(record) + "\n")


def load_comp_resolved_ids():
    """Returns set of market_ids already in competition resolved file."""
    seen = set()
    if not os.path.exists(COMP_RESOLVED_FILE):
        return seen
    with open(COMP_RESOLVED_FILE) as f:
        for line in f:
            try:
                d = json.loads(line.strip())
                if d.get("market_id"):
                    seen.add(str(d["market_id"]))
            except Exception:
                pass
    return seen


def append_comp_resolved(record):
    with open(COMP_RESOLVED_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


def fetch_polymarket_active_track():
    """
    1. Fetch currently-active Polymarket markets; add new binary YES/NO markets
       to active_tracking with their real pre-resolution entry prices.
    2. For tracked markets whose endDate has passed, query to check if resolved.
    3. Write newly-resolved ones to competition/polymarket/resolved_markets.jsonl.
    Returns (n_new_tracked, n_newly_resolved).
    """
    tracking = load_active_tracking()
    comp_resolved_ids = load_comp_resolved_ids()
    now    = datetime.now(timezone.utc)
    now_ts = now.isoformat()

    # Step 1: Fetch all active markets and record new binary YES/NO markets
    n_new  = 0
    offset = 0
    limit  = 500
    for _page in range(25):   # up to 12.5k active markets
        url = (f"https://gamma-api.polymarket.com/markets"
               f"?active=true&closed=false&limit={limit}&offset={offset}")
        data = api_get(url)
        if not data or not isinstance(data, list) or len(data) == 0:
            break

        for m in data:
            mid = str(m.get("id", "") or m.get("conditionId", ""))
            if not mid or mid in tracking or mid in comp_resolved_ids:
                continue

            try:
                outcomes = json.loads(m.get("outcomes", "[]"))
                prices   = json.loads(m.get("outcomePrices", "[]"))
                prices_f = [float(p) for p in prices]
            except Exception:
                continue

            if len(prices_f) < 2 or len(outcomes) < 2:
                continue
            if outcomes[0] not in ("Yes", "YES") or outcomes[1] not in ("No", "NO"):
                continue

            yes_price = prices_f[0]
            if not (0.05 <= yes_price <= 0.95):
                continue  # too close to settlement; skip as entry price

            question = m.get("question", "") or m.get("title", "")
            pm_cat   = m.get("category", "")

            tracking[mid] = {
                "market_id":       mid,
                "question":        question,
                "category":        categorize(question, pm_cat),
                "entry_yes_price": round(yes_price, 4),
                "first_seen":      now_ts,
                "end_date":        m.get("endDate", ""),
            }
            n_new += 1

        offset += limit
        if len(data) < limit:
            break
        time.sleep(0.3)

    # Step 2: Check tracked markets whose endDate has passed
    n_newly_resolved = 0
    to_remove = []

    for mid, rec in list(tracking.items()):
        if mid in comp_resolved_ids:
            to_remove.append(mid)
            continue

        end_date_str = rec.get("end_date", "")
        if not end_date_str:
            continue

        try:
            end_dt = datetime.fromisoformat(
                end_date_str.replace("Z", "+00:00")
            ).replace(tzinfo=timezone.utc)
            if end_dt > now:
                continue   # still active
        except Exception:
            continue

        # Past scheduled end date — query current market status
        url         = f"https://gamma-api.polymarket.com/markets?id={mid}"
        m_data_list = api_get(url)
        if not m_data_list or not isinstance(m_data_list, list) or len(m_data_list) == 0:
            continue

        m_data = m_data_list[0]
        if not m_data.get("closed", False):
            continue   # Polymarket has not closed it yet

        try:
            prices   = json.loads(m_data.get("outcomePrices", "[]"))
            prices_f = [float(p) for p in prices]
        except Exception:
            continue

        if len(prices_f) < 2:
            continue

        yes_price = prices_f[0]
        no_price  = prices_f[1]

        if yes_price > 0.99 and no_price < 0.01:
            resolution_outcome = "YES"
        elif no_price > 0.99 and yes_price < 0.01:
            resolution_outcome = "NO"
        else:
            resolution_outcome = "INVALID"

        comp_rec = {
            "market_id":          mid,
            "question":           rec.get("question", ""),
            "category":           rec.get("category", ""),
            "fetched_at":         now_ts,
            "first_seen":         rec.get("first_seen"),
            "entry_yes_price":    rec.get("entry_yes_price"),
            "resolved_at":        m_data.get("endDate") or m_data.get("closedTime", now_ts),
            "resolution_outcome": resolution_outcome,
            "final_yes_price":    round(yes_price, 4),
        }
        append_comp_resolved(comp_rec)
        comp_resolved_ids.add(mid)
        to_remove.append(mid)
        n_newly_resolved += 1
        time.sleep(0.1)

    for mid in to_remove:
        tracking.pop(mid, None)

    save_active_tracking(tracking)
    return n_new, n_newly_resolved


# ── Kalshi ─────────────────────────────────────────────────────────────────

def fetch_kalshi(seen):
    new = 0
    headers = {}
    try:
        with open(KALSHI_SECRET) as f:
            key = json.load(f).get("kalshi_api_key", "")
        if key:
            headers["Authorization"] = f"Token {key}"
    except Exception:
        pass

    cursor = None
    for _ in range(50):    # up to 10k markets
        url = ("https://api.elections.kalshi.com/trade-api/v2/markets"
               "?status=settled&limit=200")
        if cursor:
            url += f"&cursor={cursor}"
        data = api_get(url, headers=headers)
        if not data:
            break

        for m in data.get("markets", []):
            result = m.get("result", "")
            if result not in ("yes", "no"):
                continue
            ticker = m.get("ticker", "")
            if not ticker:
                continue
            key = "kalshi::" + ticker
            if key in seen:
                continue

            question = m.get("title", "") or m.get("subtitle", "")
            if len(question) > 200:
                continue

            last_price = m.get("last_price_dollars")
            try:
                odds_close = float(last_price) if last_price is not None else None
                if odds_close is not None and odds_close > 1:
                    odds_close = odds_close / 100
            except Exception:
                odds_close = None

            volume = 0.0
            try:
                volume = float(m.get("volume_fp") or m.get("volume_24h_fp") or 0)
            except Exception:
                pass

            record = {
                "source":           "kalshi",
                "market_id":        ticker,
                "question":         question,
                "category":         categorize(question),
                "resolution":       result,
                "resolution_value": 1.0 if result == "yes" else 0.0,
                "odds_close":       round(odds_close, 4) if odds_close is not None else None,
                "volume_usd":       round(volume, 2),
                "resolved_at":      m.get("close_time", ""),
                "collected_at":     datetime.now(timezone.utc).isoformat(),
            }
            seen.add(key)
            append_market(record)
            new += 1

        cursor = data.get("cursor")
        if not cursor or len(data.get("markets", [])) < 200:
            break
        time.sleep(0.3)

    return new


# ── Manifold ───────────────────────────────────────────────────────────────

def fetch_manifold(seen):
    new = 0
    before = None
    for _ in range(20):    # up to 20k markets
        url = "https://api.manifold.markets/v0/markets?limit=1000"
        if before:
            url += f"&before={before}"
        data = api_get(url)
        if not data or not isinstance(data, list) or len(data) == 0:
            break

        for m in data:
            if m.get("outcomeType") != "BINARY":
                continue
            if not m.get("isResolved"):
                continue
            resolution = (m.get("resolution") or "").lower()
            if resolution not in ("yes", "no"):
                continue

            mid = m.get("id", "")
            if not mid:
                continue
            key = "manifold::" + mid
            if key in seen:
                continue

            question = m.get("question", "")
            prob = m.get("probability")
            try:
                odds_close = float(prob) if prob is not None else None
            except Exception:
                odds_close = None

            volume = 0.0
            try:
                volume = float(m.get("volume", 0) or 0)
            except Exception:
                pass

            record = {
                "source":           "manifold",
                "market_id":        mid,
                "question":         question,
                "category":         categorize(question),
                "resolution":       resolution,
                "resolution_value": 1.0 if resolution == "yes" else 0.0,
                "odds_close":       round(odds_close, 4) if odds_close is not None else None,
                "volume_usd":       round(volume, 2),
                "resolved_at":      str(m.get("resolutionTime", "")),
                "collected_at":     datetime.now(timezone.utc).isoformat(),
            }
            seen.add(key)
            append_market(record)
            new += 1

        if len(data) < 1000:
            break
        before = data[-1].get("id")
        time.sleep(0.3)

    return new


# ── Main ───────────────────────────────────────────────────────────────────

def count_by_source():
    counts = {"polymarket": 0, "kalshi": 0, "manifold": 0}
    if not os.path.exists(OUTPUT_FILE):
        return counts
    with open(OUTPUT_FILE) as f:
        for line in f:
            try:
                d = json.loads(line.strip())
                s = d.get("source", "")
                if s in counts:
                    counts[s] += 1
            except Exception:
                pass
    return counts


def main():
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] pm_collector starting")
    seen = load_seen()
    print(f"  already collected: {len(seen)} markets")

    total_new = 0
    for fn, name in [
        (fetch_polymarket, "Polymarket"),
        (fetch_kalshi,     "Kalshi"),
        (fetch_manifold,   "Manifold"),
    ]:
        print(f"  fetching {name}...", end=" ", flush=True)
        try:
            n = fn(seen)
            print(f"{n} new")
            total_new += n
        except Exception as e:
            print(f"ERROR: {e}")

    # Active tracking for FREYA validation gate
    print(f"  Polymarket active tracking...", end=" ", flush=True)
    try:
        n_new_tracked, n_resolved = fetch_polymarket_active_track()
        print(f"{n_new_tracked} new tracked, {n_resolved} newly resolved")
    except Exception as e:
        print(f"ERROR: {e}")

    counts = count_by_source()
    total  = sum(counts.values())
    print(f"  totals — PM:{counts['polymarket']}  Kalshi:{counts['kalshi']}"
          f"  Manifold:{counts['manifold']}  grand:{total}  new_this_run:{total_new}")

    state = {
        "total":          total,
        "by_source":      counts,
        "last_run":       ts,
        "new_this_run":   total_new,
        "researcher_ready": total >= 500,
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print("done")


if __name__ == "__main__":
    main()
