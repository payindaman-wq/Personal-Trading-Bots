#!/usr/bin/env python3
"""
kalshi_copy_tick.py — Live Kalshi copy trader mirroring top Polymarket traders.

Monitors 3 Polymarket copy-trade winners. When they enter a position, finds the
equivalent Kalshi market and executes a REAL order. Closes when they exit.

Capital: $333/bot × 3 bots = ~$999 live on Kalshi
Position size: 10% of bot capital per bet (~$33 per trade)
Match threshold: 0.55 (Jaccard title similarity)

Run:     python3 /root/.openclaw/workspace/kalshi_copy_tick.py
Service: kalshi_copy.service
"""

import json
import logging
import math
import os
import re
import time
import urllib.error
import urllib.request
import uuid
from copy import deepcopy
from datetime import datetime, timezone, timedelta

# ── Paths ──────────────────────────────────────────────────────────────────
WORKSPACE       = "/root/.openclaw/workspace"
STATE_FILE      = f"{WORKSPACE}/competition/polymarket/kalshi_copy_state.json"
LOG_FILE        = f"{WORKSPACE}/competition/polymarket/kalshi_copy_tick.log"
DASH_OUTPUT     = "/var/www/dashboard/api/kalshi_copy.json"
SPRINT_RESULTS  = f"{WORKSPACE}/competition/polymarket/sprint_results"
KALSHI_SECRET   = "/root/.openclaw/secrets/kalshi.json"

# ── Tuning ─────────────────────────────────────────────────────────────────
POLL_SEC          = 30          # seconds between ticks
MATCH_THRESHOLD   = 0.55        # minimum Jaccard similarity to trust a Kalshi match
POSITION_PCT      = 0.10        # 10% of bot capital per trade
SPRINT_HOURS      = 168         # 7-day sprints
KALSHI_TRADE_URL  = "https://trading-api.kalshi.com/trade-api/v2"
KALSHI_DATA_URL   = "https://api.elections.kalshi.com/trade-api/v2"  # public endpoint, no auth needed for reads
PM_ACTIVITY_URL   = "https://data-api.polymarket.com/activity"
PM_MARKET_URL     = "https://gamma-api.polymarket.com/markets"

# ── Bots: top 3 Polymarket copy-trade winners ──────────────────────────────
BOT_CONFIG = [
    {
        "name":             "sol_k",
        "pm_trader":        "SecondWindCapital",
        "pm_wallet":        "0x8c80d213c0cbad777d06ee3f58f6ca4bc03102c3",
        "starting_capital": 333.33,
    },
    {
        "name":             "freyr_k",
        "pm_trader":        "beachboy4",
        "pm_wallet":        "0x",   # wallet filled in at init from PM profile
        "starting_capital": 333.33,
    },
    {
        "name":             "baldur_k",
        "pm_trader":        "UAEVALORANTFAN",
        "pm_wallet":        "0x",
        "starting_capital": 333.33,
    },
]

STOP_WORDS = {
    "will", "the", "a", "an", "of", "in", "on", "at", "to", "for",
    "is", "are", "be", "has", "have", "by", "or", "and", "vs", "vs.",
    "who", "what", "when", "how", "does", "do", "can", "could",
    "would", "should", "may", "might",
}

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


# ── HTTP helpers ───────────────────────────────────────────────────────────

def api_get(url, headers=None, timeout=15):
    hdrs = {"User-Agent": "kalshi-copy/1.0", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def api_post(url, payload, headers=None, timeout=20):
    hdrs = {"Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "kalshi-copy/1.0"}
    if headers:
        hdrs.update(headers)
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        return None, f"HTTP {e.code}: {body[:200]}"


# ── Polymarket helpers ─────────────────────────────────────────────────────

def fetch_pm_activity(wallet, since_ts=0, limit=20):
    """Return new TRADE events for a Polymarket wallet, oldest first."""
    url = f"{PM_ACTIVITY_URL}?user={wallet}&limit={limit}"
    try:
        data = api_get(url)
    except Exception as e:
        log.warning(f"PM activity fetch {wallet[:10]}... error: {e}")
        return []
    trades = [
        t for t in data
        if t.get("type") == "TRADE"
        and t.get("timestamp", 0) > since_ts
        and t.get("side") in ("BUY", "SELL")
    ]
    return sorted(trades, key=lambda x: x["timestamp"])


def fetch_pm_market_price(condition_id, outcome):
    """Get current Polymarket price for a specific outcome."""
    try:
        url   = f"{PM_MARKET_URL}?condition_ids={condition_id}"
        data  = api_get(url, timeout=10)
        if not data:
            return None
        market    = data[0] if isinstance(data, list) else data
        outcomes  = market.get("outcomes", [])
        prices    = market.get("outcomePrices", [])
        if isinstance(outcomes, str):
            outcomes = json.loads(outcomes)
        if isinstance(prices, str):
            prices   = json.loads(prices)
        if outcome in outcomes:
            idx = outcomes.index(outcome)
            if idx < len(prices):
                return float(prices[idx])
    except Exception:
        pass
    return None


# ── Kalshi helpers ─────────────────────────────────────────────────────────

def auth_headers(api_key):
    return {"Authorization": f"Bearer {api_key}"}


def fetch_kalshi_markets(api_key=None):
    """Fetch all active Kalshi markets. Public endpoint — no auth required for reads."""
    markets, cursor = [], None
    for _ in range(10):
        try:
            url = f"{KALSHI_DATA_URL}/events?limit=200&with_nested_markets=true"
            if cursor:
                url += f"&cursor={cursor}"
            page = api_get(url, timeout=20)
        except Exception as e:
            log.warning(f"Kalshi market fetch error: {e}")
            break
        for event in page.get("events", []):
            for m in event.get("markets", []):
                yes_bid = m.get("yes_bid_dollars") or m.get("yes_bid")
                yes_ask = m.get("yes_ask_dollars") or m.get("yes_ask")
                if yes_bid is None or yes_ask is None:
                    continue
                try:
                    bid, ask = float(yes_bid), float(yes_ask)
                except (ValueError, TypeError):
                    continue
                if bid <= 0 or ask <= 0 or bid >= 1 or ask >= 1:
                    continue
                title = m.get("title", "") or event.get("title", "")
                if not title:
                    continue
                markets.append({
                    "ticker": m.get("ticker", ""),
                    "title":  title,
                    "yes_bid": bid,
                    "yes_ask": ask,
                    "prob":   (bid + ask) / 2,
                    "close_time": m.get("close_time", ""),
                })
        cursor = page.get("cursor")
        if not cursor or not page.get("events"):
            break
    log.info(f"Fetched {len(markets)} Kalshi markets")
    return markets


def place_kalshi_order(api_key, ticker, side, count, price_cents, dry_run=False):
    """
    Place a limit order on Kalshi.
    side: 'yes' or 'no'
    price_cents: 1-99 (price in cents per contract)
    count: number of contracts
    Returns (order_id, error_msg)
    """
    if count < 1:
        return None, "count < 1, skipping"
    if dry_run:
        fake_id = f"dry_{uuid.uuid4().hex[:8]}"
        log.info(f"DRY RUN order: ticker={ticker} side={side} count={count} price={price_cents}c → {fake_id}")
        return fake_id, None

    payload = {
        "ticker":           ticker,
        "client_order_id":  uuid.uuid4().hex,
        "type":             "limit",
        "action":           "buy",
        "side":             side,
        "count":            count,
        f"{side}_price":    price_cents,
    }
    url  = f"{KALSHI_TRADE_URL}/portfolio/orders"
    resp, err = api_post(url, payload, headers=auth_headers(api_key))
    if err:
        return None, err
    order_id = resp.get("order", {}).get("order_id") or resp.get("order_id")
    return order_id, None


def sell_kalshi_position(api_key, ticker, side, count, price_cents, dry_run=False):
    """
    Sell (exit) a Kalshi position by placing a sell order.
    price_cents: the current bid for our side (what we'll receive per contract)
    """
    if count < 1:
        return None, "count < 1"
    if dry_run:
        fake_id = f"dry_sell_{uuid.uuid4().hex[:8]}"
        log.info(f"DRY RUN sell: ticker={ticker} side={side} count={count} price={price_cents}c → {fake_id}")
        return fake_id, None

    # To sell YES contracts: sell action, side=yes
    payload = {
        "ticker":           ticker,
        "client_order_id":  uuid.uuid4().hex,
        "type":             "limit",
        "action":           "sell",
        "side":             side,
        "count":            count,
        f"{side}_price":    price_cents,
    }
    url  = f"{KALSHI_TRADE_URL}/portfolio/orders"
    resp, err = api_post(url, payload, headers=auth_headers(api_key))
    if err:
        return None, err
    order_id = resp.get("order", {}).get("order_id") or resp.get("order_id")
    return order_id, None


def get_kalshi_market_price(api_key, ticker):
    """Fetch current yes_bid and yes_ask for a Kalshi ticker."""
    try:
        url  = f"{KALSHI_DATA_URL}/markets/{ticker}"
        data = api_get(url, headers=auth_headers(api_key), timeout=10)
        m    = data.get("market", data)
        yes_bid = m.get("yes_bid_dollars") or m.get("yes_bid")
        yes_ask = m.get("yes_ask_dollars") or m.get("yes_ask")
        if yes_bid is not None and yes_ask is not None:
            return float(yes_bid), float(yes_ask)
    except Exception as e:
        log.debug(f"Price fetch {ticker}: {e}")
    return None, None


# ── Title matching (from SYN) ──────────────────────────────────────────────

def _tokens(text):
    words = re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
    return set(w for w in words if w not in STOP_WORDS and len(w) > 2)


def title_similarity(a, b):
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def build_title_index(markets):
    index = {}
    for i, m in enumerate(markets):
        for tok in _tokens(m["title"]):
            index.setdefault(tok, []).append(i)
    return index


def find_kalshi_match(pm_title, kalshi_markets, index, threshold=MATCH_THRESHOLD):
    """Find best Kalshi market matching a Polymarket title."""
    pm_toks      = _tokens(pm_title)
    cand_indices = set()
    for tok in pm_toks:
        cand_indices.update(index.get(tok, []))

    best, best_score = None, threshold
    for i in cand_indices:
        score = title_similarity(pm_title, kalshi_markets[i]["title"])
        if score > best_score:
            best, best_score = kalshi_markets[i], score
    if best:
        log.info(f"Match: '{pm_title[:45]}' → '{best['title'][:45]}' (score={best_score:.2f})")
    return best, best_score


# ── Position helpers ───────────────────────────────────────────────────────

def calc_contracts(usd_amount, price_prob):
    """
    Calculate Kalshi contract count for a dollar amount at a probability price.
    price_prob: 0-1 (e.g. 0.55)
    Returns (count, price_cents, actual_cost_usd)
    """
    if price_prob <= 0 or price_prob >= 1:
        return 0, 0, 0
    price_cents = max(1, min(99, round(price_prob * 100)))
    count       = math.floor(usd_amount * 100 / price_cents)
    actual_cost = round(count * price_cents / 100, 4)
    return count, price_cents, actual_cost


# ── State management ───────────────────────────────────────────────────────

def init_state():
    """Build initial state from BOT_CONFIG."""
    now      = datetime.now(timezone.utc)
    sprint_id = f"kalshi-copy-{now.strftime('%Y%m%d-%H%M')}"
    bots = []
    for cfg in BOT_CONFIG:
        bots.append({
            "name":              cfg["name"],
            "pm_trader":         cfg["pm_trader"],
            "pm_wallet":         cfg["pm_wallet"],
            "starting_capital":  cfg["starting_capital"],
            "cash":              cfg["starting_capital"],
            "equity":            cfg["starting_capital"],
            "pnl_usd":           0.0,
            "pnl_pct":           0.0,
            "total_trades":      0,
            "wins":              0,
            "losses":            0,
            "last_seen_ts":      0,
            "last_seen_tx":      "",
            "sprint_pnl_usd":    0.0,
            "sprint_wins":       0,
            "sprint_trades":     0,
            "sprint_start_equity": cfg["starting_capital"],
            "positions":         {},   # pm_condition_id → kalshi position
            "closed_trades":     [],
        })
    return {
        "mode":              "live",
        "dry_run":           False,
        "started_at":        now.isoformat(),
        "sprint_id":         sprint_id,
        "sprint_started_at": now.isoformat(),
        "sprint_ends_at":    (now + timedelta(hours=SPRINT_HOURS)).isoformat(),
        "bots":              bots,
        "recent_trades":     [],
        "stats":             {},
    }


def load_state():
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    state["generated_at"] = datetime.now(timezone.utc).isoformat()
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)


# ── Core trade logic ───────────────────────────────────────────────────────

def open_position(bot, trade, kalshi_match, api_key, dry_run):
    """Mirror a Polymarket buy into a Kalshi position."""
    pm_cid   = trade.get("conditionId", "")
    pm_title = trade.get("title", "")
    outcome  = trade.get("outcome", "Yes")
    side     = "yes" if outcome.lower() == "yes" else "no"

    # Use Kalshi ask price (what we pay to buy)
    if side == "yes":
        price_prob = kalshi_match["yes_ask"]
    else:
        # no price = 1 - yes_ask
        price_prob = 1.0 - kalshi_match["yes_bid"]

    size_usd = round(bot["cash"] * POSITION_PCT, 2)
    if size_usd < 1.00:
        log.info(f"[{bot['name']}] Insufficient cash (${bot['cash']:.2f}), skipping")
        return None

    if pm_cid in bot["positions"]:
        log.info(f"[{bot['name']}] Already in market {pm_cid[:12]}, skipping duplicate")
        return None

    count, price_cents, actual_cost = calc_contracts(size_usd, price_prob)
    if count < 1:
        log.info(f"[{bot['name']}] Price too extreme ({price_prob:.2f}), skipping")
        return None

    ticker   = kalshi_match["ticker"]
    order_id, err = place_kalshi_order(api_key, ticker, side, count, price_cents, dry_run)
    if err:
        log.warning(f"[{bot['name']}] Order failed for {ticker}: {err}")
        return None

    bot["cash"] = round(bot["cash"] - actual_cost, 4)
    position = {
        "pm_condition_id":  pm_cid,
        "pm_title":         pm_title,
        "kalshi_ticker":    ticker,
        "kalshi_title":     kalshi_match["title"],
        "side":             side,
        "count":            count,
        "entry_price":      price_prob,
        "entry_cents":      price_cents,
        "cost_usd":         actual_cost,
        "current_value":    actual_cost,
        "unrealized_pnl":   0.0,
        "order_id":         order_id,
        "opened_at":        datetime.now(timezone.utc).isoformat(),
    }
    bot["positions"][pm_cid] = position
    bot["total_trades"] += 1

    log.info(
        f"[{bot['name']}] OPEN {side.upper()} {ticker} | "
        f"{count} contracts @ {price_cents}c = ${actual_cost:.2f} | "
        f"PM: {pm_title[:40]}"
    )
    return {
        "bot": bot["name"], "trader": bot["pm_trader"], "action": "OPEN",
        "pm_title": pm_title, "kalshi_ticker": ticker, "side": side,
        "count": count, "price_cents": price_cents, "cost_usd": actual_cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def close_position(bot, pm_cid, reason, api_key, dry_run, final_price=None):
    """Close a Kalshi position and record P&L."""
    pos = bot["positions"].get(pm_cid)
    if not pos:
        return None

    ticker = pos["kalshi_ticker"]
    side   = pos["side"]
    count  = pos["count"]

    # Get current exit price
    if final_price is not None:
        exit_prob = final_price
    else:
        # Fetch current bid (what we receive when selling)
        yes_bid, yes_ask = get_kalshi_market_price(api_key, ticker)
        if side == "yes":
            exit_prob = yes_bid if yes_bid else pos["entry_price"]
        else:
            exit_prob = (1.0 - yes_ask) if yes_ask else pos["entry_price"]

    exit_cents = max(1, min(99, round(exit_prob * 100)))

    # Place sell order
    sell_id, err = sell_kalshi_position(api_key, ticker, side, count, exit_cents, dry_run)
    if err:
        log.warning(f"[{bot['name']}] Sell failed {ticker}: {err} — marking closed anyway")

    proceeds = round(count * exit_cents / 100, 4)
    pnl      = round(proceeds - pos["cost_usd"], 4)
    pnl_pct  = round((pnl / pos["cost_usd"]) * 100, 2) if pos["cost_usd"] else 0

    bot["cash"] = round(bot["cash"] + proceeds, 4)
    if pnl >= 0:
        bot["wins"] += 1
        bot["sprint_wins"] = bot.get("sprint_wins", 0) + 1
    else:
        bot["losses"] += 1
    bot["sprint_trades"] = bot.get("sprint_trades", 0) + 1

    closed = {
        **pos,
        "closed_at":   datetime.now(timezone.utc).isoformat(),
        "exit_price":  exit_prob,
        "exit_cents":  exit_cents,
        "proceeds_usd": proceeds,
        "pnl_usd":     pnl,
        "pnl_pct":     pnl_pct,
        "reason":      reason,
        "sell_order_id": sell_id,
    }
    bot["closed_trades"].append(closed)
    del bot["positions"][pm_cid]

    log.info(
        f"[{bot['name']}] CLOSE {reason} {ticker} @ {exit_cents}c | "
        f"PNL ${pnl:+.2f} ({pnl_pct:+.1f}%) | {pos['pm_title'][:35]}"
    )
    return {
        "bot": bot["name"], "trader": bot["pm_trader"], "action": "CLOSE",
        "kalshi_ticker": ticker, "pm_title": pos["pm_title"],
        "exit_price": exit_prob, "pnl_usd": pnl, "pnl_pct": pnl_pct,
        "reason": reason, "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def update_bot_equity(bot, api_key):
    """Refresh current values on open positions and recompute equity."""
    total_position_value = 0.0
    for pm_cid, pos in list(bot["positions"].items()):
        ticker = pos["kalshi_ticker"]
        side   = pos["side"]
        yes_bid, yes_ask = get_kalshi_market_price(api_key, ticker)

        if side == "yes":
            current_price = yes_bid
        else:
            current_price = (1.0 - yes_ask) if yes_ask else None

        if current_price is not None:
            pos["current_price"] = current_price
            pos["current_value"] = round(pos["count"] * current_price, 4)
            pos["unrealized_pnl"] = round(pos["current_value"] - pos["cost_usd"], 4)

            # Auto-close if resolved
            if current_price >= 0.99:
                close_position(bot, pm_cid, "resolved_win", api_key, bot.get("_dry_run", False), final_price=1.0)
                continue
            elif current_price <= 0.01:
                close_position(bot, pm_cid, "resolved_loss", api_key, bot.get("_dry_run", False), final_price=0.0)
                continue

        total_position_value += pos.get("current_value", pos["cost_usd"])

    bot["equity"]       = round(bot["cash"] + total_position_value, 4)
    bot["pnl_usd"]      = round(bot["equity"] - bot["starting_capital"], 4)
    bot["pnl_pct"]      = round(bot["pnl_usd"] / bot["starting_capital"] * 100, 2)
    sprint_base         = bot.get("sprint_start_equity", bot["starting_capital"])
    bot["sprint_pnl_usd"] = round(bot["equity"] - sprint_base, 4)


def advance_sprint(state):
    now       = datetime.now(timezone.utc)
    sprint_id = state["sprint_id"]
    os.makedirs(SPRINT_RESULTS, exist_ok=True)

    bots_data = []
    for b in state["bots"]:
        sp_trades = b.get("sprint_trades", 0)
        sp_wins   = b.get("sprint_wins", 0)
        sp_pnl    = round(b.get("sprint_pnl_usd", 0), 2)
        bots_data.append({
            "bot":            b["name"],
            "type":           "kalshi_copy",
            "pm_trader":      b.get("pm_trader", ""),
            "sprint_pnl_usd": sp_pnl,
            "sprint_pnl_pct": round(sp_pnl / b.get("starting_capital", 333.33) * 100, 2),
            "sprint_trades":  sp_trades,
            "sprint_wins":    sp_wins,
            "win_rate":       round(sp_wins / sp_trades * 100, 1) if sp_trades > 0 else 0.0,
        })

    results = {
        "sprint_id":  sprint_id,
        "started_at": state.get("sprint_started_at"),
        "ended_at":   now.isoformat(),
        "bots":       bots_data,
    }
    out_path = os.path.join(SPRINT_RESULTS, f"{sprint_id}_kalshi_copy.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    log.info(f"Sprint archived: {out_path}")

    new_id  = f"kalshi-copy-{now.strftime('%Y%m%d-%H%M')}"
    ends_at = now + timedelta(hours=SPRINT_HOURS)
    state["sprint_id"]         = new_id
    state["sprint_started_at"] = now.isoformat()
    state["sprint_ends_at"]    = ends_at.isoformat()
    for bot in state["bots"]:
        bot["sprint_pnl_usd"]       = 0.0
        bot["sprint_wins"]          = 0
        bot["sprint_trades"]        = 0
        bot["sprint_start_equity"]  = bot["equity"]
    log.info(f"Sprint: {sprint_id} → {new_id}")


def recompute_stats(state):
    bots        = state["bots"]
    total_pnl   = sum(b["pnl_usd"] for b in bots)
    total_capital = sum(b["starting_capital"] for b in bots)
    total_trades  = sum(b["total_trades"] for b in bots)
    total_wins    = sum(b["wins"] for b in bots)
    total_losses  = sum(b["losses"] for b in bots)
    active_pos    = sum(len(b["positions"]) for b in bots)
    win_rate = round(total_wins / (total_wins + total_losses) * 100, 1) if (total_wins + total_losses) else 0.0
    state["stats"] = {
        "total_capital_usd":  total_capital,
        "total_pnl_usd":      round(total_pnl, 2),
        "total_pnl_pct":      round(total_pnl / total_capital * 100, 2) if total_capital else 0,
        "overall_win_rate":   win_rate,
        "active_positions":   active_pos,
        "total_trades":       total_trades,
    }


def write_dashboard(state):
    bot_rows = []
    for b in state["bots"]:
        wins  = b.get("wins", 0)
        total = b.get("total_trades", 0)
        st    = b.get("sprint_trades", 0)
        sw    = b.get("sprint_wins", 0)
        bot_rows.append({
            "bot":             b["name"],
            "pm_trader":       b["pm_trader"],
            "capital_usd":     b["starting_capital"],
            "equity_usd":      round(b["equity"], 2),
            "pnl_usd":         round(b["pnl_usd"], 2),
            "pnl_pct":         round(b["pnl_pct"], 2),
            "sprint_pnl_usd":  round(b.get("sprint_pnl_usd", 0), 2),
            "win_rate":        round(wins / total * 100, 1) if total else 0,
            "sprint_win_rate": round(sw / st * 100, 1) if st else 0,
            "trades":          total,
            "sprint_trades":   st,
            "open_positions":  len(b["positions"]),
        })

    open_pos = []
    for b in state["bots"]:
        for cid, pos in b["positions"].items():
            open_pos.append({
                "bot":          b["name"],
                "pm_trader":    b["pm_trader"],
                "kalshi_ticker":pos["kalshi_ticker"],
                "pm_title":     pos["pm_title"],
                "kalshi_title": pos["kalshi_title"],
                "side":         pos["side"],
                "count":        pos["count"],
                "entry_price":  pos["entry_price"],
                "current_price":pos.get("current_price", pos["entry_price"]),
                "cost_usd":     pos["cost_usd"],
                "current_value":pos.get("current_value", pos["cost_usd"]),
                "unrealized_pnl":pos.get("unrealized_pnl", 0),
                "opened_at":    pos["opened_at"],
            })

    dashboard = {
        "generated_at":      datetime.now(timezone.utc).isoformat(),
        "mode":              state.get("mode", "live"),
        "dry_run":           state.get("dry_run", True),
        "sprint_id":         state.get("sprint_id"),
        "sprint_started_at": state.get("sprint_started_at"),
        "sprint_ends_at":    state.get("sprint_ends_at"),
        "stats":             state.get("stats", {}),
        "bots":              bot_rows,
        "open_positions":    open_pos,
        "recent_trades":     state.get("recent_trades", [])[-20:],
    }
    os.makedirs(os.path.dirname(DASH_OUTPUT), exist_ok=True)
    with open(DASH_OUTPUT, "w") as f:
        json.dump(dashboard, f, indent=2)


# ── Main tick ──────────────────────────────────────────────────────────────

def tick(state, api_key, kalshi_markets, kalshi_index):
    dry_run    = state.get("dry_run", True)
    new_events = []

    for bot in state["bots"]:
        wallet   = bot["pm_wallet"]
        since_ts = bot.get("last_seen_ts", 0)

        new_trades = fetch_pm_activity(wallet, since_ts=since_ts)
        for trade in new_trades:
            ts   = trade.get("timestamp", 0)
            side = trade.get("side")
            pm_cid = trade.get("conditionId", "")
            title  = trade.get("title", "")

            if side == "BUY":
                match, score = find_kalshi_match(title, kalshi_markets, kalshi_index)
                if match:
                    event = open_position(bot, trade, match, api_key, dry_run)
                    if event:
                        new_events.append(event)
                else:
                    log.info(f"[{bot['name']}] No Kalshi match for: {title[:50]}")

            elif side == "SELL":
                if pm_cid in bot["positions"]:
                    pm_exit_price = float(trade.get("price", 0)) or None
                    event = close_position(bot, pm_cid, "pm_trader_sold", api_key, dry_run, pm_exit_price)
                    if event:
                        new_events.append(event)

            if ts > bot.get("last_seen_ts", 0):
                bot["last_seen_ts"] = ts
                bot["last_seen_tx"] = trade.get("transactionHash", "")

        update_bot_equity(bot, api_key)

    state["recent_trades"] = (new_events + state.get("recent_trades", []))[:50]
    recompute_stats(state)

    s = state["stats"]
    log.info(
        f"Tick | positions={s['active_positions']} trades={s['total_trades']} "
        f"pnl=${s['total_pnl_usd']:+.2f} ({s['total_pnl_pct']:+.2f}%)"
        + (" [DRY RUN]" if dry_run else "")
    )


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--init",    action="store_true", help="Initialize state file and exit")
    parser.add_argument("--dry-run", action="store_true", help="Override to dry-run mode (no real orders)")
    parser.add_argument("--wallets", action="store_true", help="Print bot wallets and exit")
    args = parser.parse_args()

    # Load Kalshi API key
    with open(KALSHI_SECRET) as f:
        api_key = json.load(f).get("kalshi_api_key", "")
    if not api_key:
        log.error("No kalshi_api_key in secrets. Exiting.")
        return 1

    if args.init:
        if os.path.exists(STATE_FILE):
            log.warning(f"State file already exists: {STATE_FILE}")
            log.warning("Delete it first if you want a fresh start.")
            return 1
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        state = init_state()
        save_state(state)
        log.info(f"Initialized: {STATE_FILE}")
        log.info("IMPORTANT: Set pm_wallet for freyr_k and baldur_k bots before running.")
        log.info("Run with --wallets to see which wallets need updating.")
        return 0

    if not os.path.exists(STATE_FILE):
        log.error(f"State file not found: {STATE_FILE}")
        log.error("Run with --init first.")
        return 1

    state = load_state()

    if args.dry_run:
        state["dry_run"] = True
        log.info("Dry-run mode FORCED by --dry-run flag")

    if args.wallets:
        for b in state["bots"]:
            print(f"{b['name']:12s} | {b['pm_trader']:25s} | wallet: {b['pm_wallet']}")
        return 0

    dry_run = state.get("dry_run", True)
    log.info(
        f"kalshi_copy_tick starting | mode={'DRY RUN' if dry_run else 'LIVE'} | "
        f"poll={POLL_SEC}s | match_threshold={MATCH_THRESHOLD}"
    )

    # Pre-fetch Kalshi markets (refresh every 30 min)
    kalshi_markets = fetch_kalshi_markets(api_key)
    kalshi_index   = build_title_index(kalshi_markets)
    last_market_refresh = time.time()
    MARKET_REFRESH_SEC  = 1800

    while True:
        try:
            # Advance sprint if window elapsed
            sprint_ends = state.get("sprint_ends_at")
            if sprint_ends:
                if datetime.now(timezone.utc) >= datetime.fromisoformat(sprint_ends):
                    advance_sprint(state)

            # Refresh Kalshi markets periodically
            if time.time() - last_market_refresh > MARKET_REFRESH_SEC:
                kalshi_markets     = fetch_kalshi_markets(api_key)
                kalshi_index       = build_title_index(kalshi_markets)
                last_market_refresh = time.time()

            tick(state, api_key, kalshi_markets, kalshi_index)
            save_state(state)
            write_dashboard(state)

        except Exception as e:
            log.error(f"Tick error: {e}", exc_info=True)

        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
