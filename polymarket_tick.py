#!/usr/bin/env python3
"""
polymarket_tick.py — 30-second copy-trading tick daemon for Polymarket.

For each bot, polls its assigned trader's recent activity. When a new TRADE
is detected, mirrors it in the bot's paper portfolio using fixed % position sizing.
Resolves positions when market settles (price hits 0 or 1).

Run as: python3 polymarket_tick.py
Or as a systemd service (see polymarket.service).
"""
import json, os, time, urllib.request, urllib.error, logging
from datetime import datetime, timezone, timedelta
from copy import deepcopy

STATE_FILE       = "/root/.openclaw/workspace/competition/polymarket/state.json"
DASH_OUTPUT      = "/var/www/dashboard/api/polymarket.json"
LOG_FILE         = "/root/.openclaw/workspace/competition/polymarket/tick.log"
SPRINT_RESULTS   = "/root/.openclaw/workspace/competition/polymarket/sprint_results"
POLL_SEC         = 30
MAX_RECENT       = 50  # recent_trades entries to keep
SPRINT_HOURS     = 168  # 7-day sprints, matches swing league

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger(__name__)


def api_get(url, timeout=10):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "polymarket-copy-bot/1.0", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def fetch_activity(wallet, since_ts=0, limit=20):
    """Returns new TRADE events after since_ts, oldest first."""
    url = f"https://data-api.polymarket.com/activity?user={wallet}&limit={limit}"
    try:
        data = api_get(url)
    except urllib.error.HTTPError as e:
        log.warning(f"Activity fetch {wallet[:10]}... HTTP {e.code}")
        return []
    except Exception as e:
        log.warning(f"Activity fetch {wallet[:10]}... error: {e}")
        return []

    trades = [
        t for t in data
        if t.get("type") == "TRADE"
        and t.get("timestamp", 0) > since_ts
        and t.get("side") in ("BUY", "SELL")
    ]
    return sorted(trades, key=lambda x: x["timestamp"])


def fetch_market_price(condition_id):
    """Get current best price for a condition (0-1)."""
    try:
        url = f"https://clob.polymarket.com/midpoints?conditionIds={condition_id}"
        data = api_get(url, timeout=5)
        # returns {"midpoints": {"conditionId": price}}
        midpoints = data.get("midpoints", {})
        val = midpoints.get(condition_id)
        return float(val) if val is not None else None
    except Exception:
        return None


def open_position(bot, trade):
    """Open a paper position mirroring the trader's buy."""
    cid = trade.get("conditionId", "")
    title = trade.get("title", "Unknown")
    outcome = trade.get("outcome", "")
    price = float(trade.get("price", 0.5))
    side = trade.get("side")

    if price <= 0 or price >= 1:
        return  # degenerate price, skip

    # Position size: fixed % of available cash
    state = load_state()
    trade_size_pct = state.get("trade_size_pct", 0.10)
    size_usd = round(bot["cash"] * trade_size_pct, 4)
    if size_usd < 0.10:
        log.info(f"  [{bot['name']}] Insufficient cash (${bot['cash']:.2f}), skipping")
        return

    # Don't stack positions on same market
    if cid in bot["positions"]:
        log.info(f"  [{bot['name']}] Already in {title[:40]}, skipping duplicate")
        return

    bot["cash"] = round(bot["cash"] - size_usd, 4)
    shares = round(size_usd / price, 4)

    position = {
        "condition_id": cid,
        "title": title,
        "outcome": outcome,
        "side": side,
        "entry_price": price,
        "shares": shares,
        "cost_usd": size_usd,
        "current_price": price,
        "current_value": size_usd,
        "unrealized_pnl": 0.0,
        "opened_at": datetime.now(timezone.utc).isoformat(),
        "trader_tx": trade.get("transactionHash", ""),
    }

    bot["positions"][cid] = position
    bot["total_trades"] += 1
    log.info(f"  [{bot['name']}] OPEN {side} {outcome} @ {price:.3f} | ${size_usd:.2f} | {title[:40]}")

    return {
        "bot": bot["name"],
        "trader": bot["trader"],
        "action": "OPEN",
        "market": title,
        "outcome": outcome,
        "side": side,
        "price": price,
        "size_usd": size_usd,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def close_position(bot, cid, reason="resolved", final_price=None):
    """Close a paper position and record P&L."""
    pos = bot["positions"].get(cid)
    if not pos:
        return

    if final_price is None:
        final_price = pos.get("current_price", pos["entry_price"])

    proceeds = round(pos["shares"] * final_price, 4)
    pnl = round(proceeds - pos["cost_usd"], 4)
    pnl_pct = round((pnl / pos["cost_usd"]) * 100, 2) if pos["cost_usd"] else 0

    bot["cash"] = round(bot["cash"] + proceeds, 4)
    if pnl >= 0:
        bot["wins"] += 1
        bot["sprint_wins"] = bot.get("sprint_wins", 0) + 1
    else:
        bot["losses"] += 1
    bot["sprint_trades"] = bot.get("sprint_trades", 0) + 1

    closed = {**pos, "closed_at": datetime.now(timezone.utc).isoformat(),
              "exit_price": final_price, "proceeds_usd": proceeds,
              "pnl_usd": pnl, "pnl_pct": pnl_pct, "reason": reason}
    bot["closed_trades"].append(closed)
    del bot["positions"][cid]

    log.info(f"  [{bot['name']}] CLOSE {reason} @ {final_price:.3f} | PNL ${pnl:+.2f} ({pnl_pct:+.1f}%) | {pos['title'][:35]}")

    return {
        "bot": bot["name"],
        "trader": bot["trader"],
        "action": "CLOSE",
        "market": pos["title"],
        "outcome": pos["outcome"],
        "exit_price": final_price,
        "pnl_usd": pnl,
        "pnl_pct": pnl_pct,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def update_bot_equity(bot):
    """Refresh current prices on open positions and recompute equity."""
    total_position_value = 0.0
    for cid, pos in list(bot["positions"].items()):
        price = fetch_market_price(cid)
        if price is not None:
            pos["current_price"] = price
            pos["current_value"] = round(pos["shares"] * price, 4)
            pos["unrealized_pnl"] = round(pos["current_value"] - pos["cost_usd"], 4)

            # Auto-close if market resolved (price = 0 or 1)
            if price >= 0.99:
                close_position(bot, cid, reason="resolved_win", final_price=1.0)
                continue
            elif price <= 0.01:
                close_position(bot, cid, reason="resolved_loss", final_price=0.0)
                continue

        total_position_value += pos.get("current_value", pos["cost_usd"])

    bot["equity"] = round(bot["cash"] + total_position_value, 4)
    bot["pnl_usd"] = round(bot["equity"] - bot["starting_capital"], 4)
    bot["pnl_pct"] = round((bot["pnl_usd"] / bot["starting_capital"]) * 100, 2)
    sprint_base = bot.get("sprint_start_equity", bot["starting_capital"])
    bot["sprint_pnl_usd"] = round(bot["equity"] - sprint_base, 4)


def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    state["generated_at"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def write_dashboard(state):
    raw_bots = state.get("bots", [])
    status   = state.get("status", "active")

    normalized_bots = []
    for b in raw_bots:
        wins  = b.get("wins", 0)
        total = b.get("total_trades", 0)
        st = b.get("sprint_trades", 0)
        sw = b.get("sprint_wins", 0)
        normalized_bots.append({
            "bot":              b.get("name", ""),
            "assigned_trader":  b.get("trader", ""),
            "pnl_usd":          round(b.get("pnl_usd", 0.0), 2),
            "win_rate":         round(wins / total * 100, 1) if total > 0 else 0.0,
            "trades":           total,
            "active_positions": len(b.get("positions", {})),
            "status":           status,
            "sprint_pnl_usd":   round(b.get("sprint_pnl_usd", 0.0), 2),
            "sprint_win_rate":  round(sw / st * 100, 1) if st > 0 else 0.0,
            "sprint_trades":    st,
        })

    open_positions = []
    for b in raw_bots:
        for cid, pos in b.get("positions", {}).items():
            open_positions.append({
                "bot":            b.get("name", ""),
                "trader":         b.get("trader", ""),
                "market":         pos.get("title", ""),
                "outcome":        pos.get("outcome", ""),
                "side":           pos.get("side", "BUY"),
                "entry_price":    pos.get("entry_price", 0),
                "current_price":  pos.get("current_price", 0),
                "cost_usd":       pos.get("cost_usd", 0),
                "current_value":  pos.get("current_value", 0),
                "unrealized_pnl": pos.get("unrealized_pnl", 0),
                "opened_at":      pos.get("opened_at", ""),
            })

    tracked = []
    for t in state.get("tracked_traders", []):
        tracked.append({
            "name":    t.get("trader", ""),
            "bot":     t.get("bot", ""),
            "roi_pct": t.get("roi_pct", 0),
        })

    sprint_started_at = state.get("sprint_started_at")
    recent_trades = []
    for entry in state.get("recent_trades", []):
        if entry.get("action") == "OPEN":
            continue
        ts = entry.get("timestamp", "")
        if sprint_started_at and ts and ts < sprint_started_at:
            continue
        recent_trades.append({
            "bot":          entry.get("bot", ""),
            "market_title": entry.get("market", entry.get("title", "")),
            "direction":    entry.get("outcome", "YES"),
            "outcome":      "win" if (entry.get("pnl_usd") or 0) >= 0 else "loss",
            "pnl_usd":      entry.get("pnl_usd"),
            "pnl_pct":      entry.get("pnl_pct"),
            "closed_at":    entry.get("timestamp", ""),
            "reason":       entry.get("reason", ""),
        })

    dashboard = {
        "generated_at":      datetime.now(timezone.utc).isoformat(),
        "mode":              state.get("mode", "paper"),
        "status":            status,
        "started_at":        state.get("started_at", ""),
        "sprint_id":         state.get("sprint_id"),
        "sprint_started_at": state.get("sprint_started_at"),
        "sprint_ends_at":    state.get("sprint_ends_at"),
        "stats":             state.get("stats", {}),
        "bots":              normalized_bots,
        "tracked_traders":   tracked,
        "open_positions":    open_positions,
        "recent_trades":     recent_trades,
    }

    os.makedirs(os.path.dirname(DASH_OUTPUT), exist_ok=True)
    with open(DASH_OUTPUT, "w") as f:
        json.dump(dashboard, f, indent=2)


def recompute_stats(state):
    bots = state["bots"]
    total_pnl = sum(b["pnl_usd"] for b in bots)
    total_trades = sum(b["total_trades"] for b in bots)
    total_wins = sum(b["wins"] for b in bots)
    total_losses = sum(b["losses"] for b in bots)
    active_pos = sum(len(b["positions"]) for b in bots)
    win_rate = round((total_wins / (total_wins + total_losses)) * 100, 1) if (total_wins + total_losses) else 0.0

    state["stats"] = {
        "total_pnl_usd": round(total_pnl, 2),
        "overall_win_rate": win_rate,
        "active_positions": active_pos,
        "total_trades": total_trades,
        "total_wins": total_wins,
        "total_losses": total_losses,
    }


def advance_sprint(state):
    now = datetime.now(timezone.utc)
    sprint_id = state.get("sprint_id", f"copy-{now.strftime('%Y%m%d-%H%M')}")
    os.makedirs(SPRINT_RESULTS, exist_ok=True)
    results = {
        "sprint_id": sprint_id,
        "started_at": state.get("sprint_started_at"),
        "ended_at": now.isoformat(),
        "bots": [
            {
                "bot":             b["name"],
                "trader":          b["trader"],
                "sprint_pnl_usd":  round(b.get("sprint_pnl_usd", 0), 2),
                "sprint_wins":     b.get("sprint_wins", 0),
                "sprint_trades":   b.get("sprint_trades", 0),
                "sprint_win_rate": round(b.get("sprint_wins", 0) / b["sprint_trades"] * 100, 1)
                                   if b.get("sprint_trades", 0) > 0 else 0.0,
            }
            for b in state["bots"]
        ],
    }
    with open(os.path.join(SPRINT_RESULTS, f"{sprint_id}.json"), "w") as f:
        json.dump(results, f, indent=2)

    new_id   = f"copy-{now.strftime('%Y%m%d-%H%M')}"
    ends_at  = now + timedelta(hours=SPRINT_HOURS)
    state["sprint_id"]         = new_id
    state["sprint_started_at"] = now.isoformat()
    state["sprint_ends_at"]    = ends_at.isoformat()
    for bot in state["bots"]:
        bot["sprint_pnl_usd"]      = 0.0
        bot["sprint_wins"]         = 0
        bot["sprint_trades"]       = 0
        bot["sprint_start_equity"] = bot["equity"]
    log.info(f"Sprint advanced: {sprint_id} → {new_id} (ends {ends_at.isoformat()})")


def tick():
    state = load_state()

    # Advance sprint if window has elapsed
    sprint_ends = state.get("sprint_ends_at")
    if sprint_ends:
        ends_dt = datetime.fromisoformat(sprint_ends)
        if datetime.now(timezone.utc) >= ends_dt:
            advance_sprint(state)

    new_events = []

    for bot in state["bots"]:
        wallet = bot["wallet"]
        since_ts = bot.get("last_seen_ts", 0)

        # Fetch new trades from this trader
        new_trades = fetch_activity(wallet, since_ts=since_ts)

        for trade in new_trades:
            ts = trade.get("timestamp", 0)
            tx = trade.get("transactionHash", "")
            side = trade.get("side")

            if side == "BUY":
                event = open_position(bot, trade)
                if event:
                    new_events.append(event)
            elif side == "SELL":
                cid = trade.get("conditionId", "")
                if cid in bot["positions"]:
                    price = float(trade.get("price", 0))
                    event = close_position(bot, cid, reason="trader_sold", final_price=price)
                    if event:
                        new_events.append(event)

            if ts > bot.get("last_seen_ts", 0):
                bot["last_seen_ts"] = ts
                bot["last_seen_tx"] = tx

        # Update prices + equity for all open positions
        update_bot_equity(bot)

    # Prepend new events to recent_trades
    state["recent_trades"] = (new_events + state.get("recent_trades", []))[:MAX_RECENT]

    recompute_stats(state)
    save_state(state)
    write_dashboard(state)

    n_pos = state["stats"]["active_positions"]
    n_trades = state["stats"]["total_trades"]
    pnl = state["stats"]["total_pnl_usd"]
    log.info(f"Tick done | positions={n_pos} trades={n_trades} total_pnl=${pnl:+.2f}")


def main():
    if not os.path.exists(STATE_FILE):
        log.error(f"State file not found: {STATE_FILE}")
        log.error("Run polymarket_init.py first.")
        return

    log.info(f"polymarket_tick starting — polling every {POLL_SEC}s")
    while True:
        try:
            tick()
        except Exception as e:
            log.error(f"Tick error: {e}", exc_info=True)
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
