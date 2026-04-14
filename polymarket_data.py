#!/usr/bin/env python3
"""
polymarket_data.py — Generate /var/www/dashboard/api/polymarket.json
Reads from kalshi_copy_state.json (_k bots mirroring Polymarket traders onto Kalshi).
"""
import json
import os
from datetime import datetime, timezone

KALSHI_STATE_FILE = "/root/.openclaw/workspace/competition/polymarket/kalshi_copy_state.json"
OUTPUT_FILE       = "/var/www/dashboard/api/polymarket.json"


def pending_setup():
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode":   "paper",
        "status": "pending_setup",
        "stats":  {"total_pnl_usd": 0.0, "overall_win_rate": 0.0,
                   "active_positions": 0, "total_trades": 0},
        "bots": [], "tracked_traders": [],
        "open_positions": [], "closed_positions": [], "recent_trades": [],
    }


def main():
    if not os.path.exists(KALSHI_STATE_FILE):
        data = pending_setup()
    else:
        try:
            with open(KALSHI_STATE_FILE) as f:
                raw = json.load(f)

            raw_bots = raw.get("bots", [])

            # Aggregate stats
            total_pnl  = sum(b.get("pnl_usd", 0) for b in raw_bots)
            all_wins   = sum(b.get("wins", 0) for b in raw_bots)
            all_losses = sum(b.get("losses", 0) for b in raw_bots)
            all_trades = sum(b.get("total_trades", 0) for b in raw_bots)
            active_pos = sum(len(b.get("positions", {})) for b in raw_bots)
            win_rate   = round(all_wins / all_trades * 100, 1) if all_trades > 0 else 0.0

            # Normalize bots: map kalshi_copy fields to dashboard-expected fields
            bots_out = []
            for b in raw_bots:
                trades       = b.get("total_trades", 0)
                wins         = b.get("wins", 0)
                sp_trades    = b.get("sprint_trades", 0)
                sp_wins      = b.get("sprint_wins", 0)
                bots_out.append({
                    "bot":              b.get("name", b.get("bot", "")),
                    "assigned_trader":  b.get("pm_trader", b.get("trader", "—")),
                    "pnl_usd":          round(b.get("pnl_usd", 0.0), 2),
                    "win_rate":         round(wins / trades * 100, 1) if trades > 0 else 0.0,
                    "trades":           trades,
                    "active_positions": len(b.get("positions", {})),
                    "status":           "active",
                    "sprint_pnl_usd":   round(b.get("sprint_pnl_usd", 0.0), 2),
                    "sprint_win_rate":  round(sp_wins / sp_trades * 100, 1) if sp_trades > 0 else 0.0,
                    "sprint_trades":    sp_trades,
                })

            # Open positions across all bots
            open_positions = []
            for b in raw_bots:
                bot_name = b.get("name", b.get("bot", ""))
                for cid, pos in b.get("positions", {}).items():
                    open_positions.append({
                        "bot":            bot_name,
                        "trader":         b.get("pm_trader", ""),
                        "market":         pos.get("title", cid),
                        "outcome":        pos.get("outcome", ""),
                        "side":           pos.get("side", "YES"),
                        "entry_price":    pos.get("entry_price", 0),
                        "current_price":  pos.get("current_price", 0),
                        "cost_usd":       pos.get("cost_usd", 0),
                        "current_value":  pos.get("current_value", pos.get("cost_usd", 0)),
                        "unrealized_pnl": pos.get("unrealized_pnl", 0),
                        "opened_at":      pos.get("opened_at", ""),
                    })

            # Closed trades across all bots (current sprint only)
            sprint_started = raw.get("sprint_started_at", "")
            closed_positions = []
            for b in raw_bots:
                bot_name = b.get("name", b.get("bot", ""))
                for t in b.get("closed_trades", []):
                    ts = t.get("closed_at", "")
                    if sprint_started and ts and ts < sprint_started:
                        continue
                    closed_positions.append({
                        "bot":          bot_name,
                        "market_title": t.get("title", t.get("market", "")),
                        "direction":    t.get("outcome", ""),
                        "outcome":      "win" if (t.get("pnl_usd") or 0) >= 0 else "loss",
                        "pnl_usd":      t.get("pnl_usd", 0),
                        "closed_at":    ts,
                    })
            closed_positions.sort(key=lambda x: x.get("closed_at") or "", reverse=True)

            data = {
                "generated_at":    datetime.now(timezone.utc).isoformat(),
                "mode":            raw.get("mode", "simulation"),
                "status":          "active",
                "started_at":      raw.get("started_at", ""),
                "sprint_id":       raw.get("sprint_id", ""),
                "sprint_started_at": raw.get("sprint_started_at", ""),
                "sprint_ends_at":  raw.get("sprint_ends_at", ""),
                "stats": {
                    "total_pnl_usd":    round(total_pnl, 2),
                    "overall_win_rate": win_rate,
                    "active_positions": active_pos,
                    "total_trades":     all_trades,
                    "total_wins":       all_wins,
                    "total_losses":     all_losses,
                },
                "bots":             bots_out,
                "tracked_traders":  [],
                "open_positions":   open_positions,
                "closed_positions": closed_positions,
                "recent_trades":    [],
            }
        except Exception as e:
            print(f"[polymarket_data] Error reading kalshi state: {e}")
            data = pending_setup()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    n_pos = len(data.get("open_positions", []))
    print(f"[polymarket_data] Wrote {OUTPUT_FILE} (bots={len(data.get('bots',[]))}, positions={n_pos})")


if __name__ == "__main__":
    main()
