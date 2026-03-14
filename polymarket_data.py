#!/usr/bin/env python3
"""
polymarket_data.py — Generate /var/www/dashboard/api/polymarket.json
Reads from /root/.openclaw/workspace/competition/polymarket/state.json
"""
import json
import os
from datetime import datetime, timezone

STATE_FILE  = "/root/.openclaw/workspace/competition/polymarket/state.json"
OUTPUT_FILE = "/var/www/dashboard/api/polymarket.json"


def pending_setup():
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "paper",
        "status": "pending_setup",
        "stats": {"total_pnl_usd": 0.0, "overall_win_rate": 0.0,
                  "active_positions": 0, "total_trades": 0},
        "bots": [], "tracked_traders": [],
        "open_positions": [], "recent_trades": [],
    }


def build_stats(raw_bots):
    total_pnl  = sum(b.get("pnl_usd", 0) for b in raw_bots)
    all_wins   = sum(b.get("wins", 0) for b in raw_bots)
    all_trades = sum(b.get("total_trades", 0) for b in raw_bots)
    active_pos = sum(len(b.get("positions", {})) for b in raw_bots)
    win_rate   = round(all_wins / all_trades * 100, 1) if all_trades > 0 else 0.0
    return {
        "total_pnl_usd":    round(total_pnl, 2),
        "overall_win_rate": win_rate,
        "active_positions": active_pos,
        "total_trades":     all_trades,
    }


def build_open_positions(raw_bots):
    positions = []
    for bot in raw_bots:
        for cid, pos in bot.get("positions", {}).items():
            positions.append({
                "bot":            bot.get("name", ""),
                "trader":         bot.get("trader", ""),
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
    return positions


def normalize_bots(raw_bots, status):
    out = []
    for b in raw_bots:
        wins  = b.get("wins", 0)
        total = b.get("total_trades", 0)
        out.append({
            "bot":              b.get("name", ""),
            "assigned_trader":  b.get("trader", ""),
            "pnl_usd":          round(b.get("pnl_usd", 0.0), 2),
            "win_rate":         round(wins / total * 100, 1) if total > 0 else 0.0,
            "trades":           total,
            "active_positions": len(b.get("positions", {})),
            "status":           status,
        })
    return out


def build_recent_trades(raw):
    trades = []
    for entry in raw.get("trade_log", []):
        trades.append({
            "bot":          entry.get("bot", ""),
            "market_title": entry.get("market", ""),
            "direction":    entry.get("outcome", "YES"),
            "outcome":      "open",
            "pnl_usd":      None,
        })
    return list(reversed(trades[-20:]))


def main():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                raw = json.load(f)
            raw_bots = raw.get("bots", [])
            status   = raw.get("status", "active")

            tracked = []
            for t in raw.get("tracked_traders", []):
                tracked.append({
                    "name":    t.get("trader", ""),
                    "bot":     t.get("bot", ""),
                    "roi_pct": t.get("roi_pct", 0),
                })

            data = {
                "generated_at":    datetime.now(timezone.utc).isoformat(),
                "mode":            raw.get("mode", "paper"),
                "status":          status,
                "started_at":      raw.get("started_at", ""),
                "stats":           build_stats(raw_bots),
                "bots":            normalize_bots(raw_bots, status),
                "tracked_traders": tracked,
                "open_positions":  build_open_positions(raw_bots),
                "recent_trades":   build_recent_trades(raw),
            }
        except Exception as e:
            print(f"[polymarket_data] Error: {e}")
            data = pending_setup()
    else:
        data = pending_setup()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    n_pos = len(data.get("open_positions", []))
    print(f"[polymarket_data] Wrote {OUTPUT_FILE} (status={data.get('status')}, positions={n_pos})")


if __name__ == "__main__":
    main()
