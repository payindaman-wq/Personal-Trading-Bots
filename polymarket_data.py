#!/usr/bin/env python3
"""
polymarket_data.py — Generate /var/www/dashboard/api/polymarket.json
Reads from auto_state.json (autonomous Polymarket fleet, written by
polymarket_syn_tick.py). Replaced kalshi_copy_state.json source 2026-04-25
during Phase 7 Kalshi retirement.
"""
import json
import os
from datetime import datetime, timezone

AUTO_STATE_FILE = "/root/.openclaw/workspace/competition/polymarket/auto_state.json"
OUTPUT_FILE     = "/var/www/dashboard/api/polymarket.json"


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
    if not os.path.exists(AUTO_STATE_FILE):
        data = pending_setup()
    else:
        try:
            with open(AUTO_STATE_FILE) as f:
                raw = json.load(f)

            raw_bots       = raw.get("bots", [])
            sprint_started = raw.get("sprint_started_at", "")

            bots_out         = []
            open_positions   = []
            closed_positions = []

            for b in raw_bots:
                bot_name = b.get("name", "")
                category = b.get("category", "auto")
                pnl      = round(b.get("pnl_usd", 0.0), 2)
                trades   = b.get("total_trades", 0)
                wins     = b.get("wins", 0)

                # auto_state.json is sprint-scoped (resets at sprint boundary),
                # so lifetime stats inside the file == current-sprint stats.
                wr = round(wins / trades * 100, 1) if trades > 0 else 0.0

                bots_out.append({
                    "bot":              bot_name,
                    "assigned_trader":  category,
                    "pnl_usd":          pnl,
                    "win_rate":         wr,
                    "trades":           trades,
                    "active_positions": len(b.get("positions", {})),
                    "status":           "stopped" if b.get("stopped") else "active",
                    "sprint_pnl_usd":   pnl,
                    "sprint_win_rate":  wr,
                    "sprint_trades":    trades,
                })

                for cid, pos in b.get("positions", {}).items():
                    open_positions.append({
                        "bot":            bot_name,
                        "trader":         category,
                        "market":         pos.get("title", cid),
                        "outcome":        pos.get("outcome", ""),
                        "side":           pos.get("side", "BUY"),
                        "entry_price":    pos.get("entry_price", 0),
                        "current_price":  pos.get("current_price", 0),
                        "cost_usd":       pos.get("cost_usd", 0),
                        "current_value":  pos.get("current_value", pos.get("cost_usd", 0)),
                        "unrealized_pnl": pos.get("unrealized_pnl", 0),
                        "opened_at":      pos.get("opened_at", ""),
                    })

                for t in b.get("closed_trades", []):
                    ts = t.get("closed_at", "")
                    if sprint_started and ts and ts < sprint_started:
                        continue
                    closed_positions.append({
                        "bot":          bot_name,
                        "market_title": t.get("title", ""),
                        "direction":    t.get("outcome", ""),
                        "outcome":      "win" if (t.get("pnl_usd") or 0) >= 0 else "loss",
                        "pnl_usd":      t.get("pnl_usd", 0),
                        "pnl_pct":      t.get("pnl_pct", 0),
                        "entry_price":  t.get("entry_price"),
                        "exit_price":   t.get("exit_price"),
                        "cost_usd":     t.get("cost_usd"),
                        "reason":       t.get("reason", ""),
                        "closed_at":    ts,
                        "source":       "polymarket",
                    })

            closed_positions.sort(key=lambda x: x.get("closed_at") or "", reverse=True)

            total_pnl  = sum(b["pnl_usd"] for b in bots_out)
            all_trades = sum(b["trades"] for b in bots_out)
            all_wins   = round(sum(b["win_rate"] * b["trades"] / 100 for b in bots_out))
            active_pos = sum(b["active_positions"] for b in bots_out)
            win_rate   = round(all_wins / all_trades * 100, 1) if all_trades > 0 else 0.0

            data = {
                "generated_at":      datetime.now(timezone.utc).isoformat(),
                "mode":              raw.get("mode", "paper"),
                "status":            raw.get("status", "active"),
                "started_at":        raw.get("started_at", ""),
                "sprint_id":         raw.get("sprint_id", ""),
                "sprint_started_at": sprint_started,
                "sprint_ends_at":    raw.get("sprint_ends_at", ""),
                "stats": {
                    "total_pnl_usd":    round(total_pnl, 2),
                    "overall_win_rate": win_rate,
                    "active_positions": active_pos,
                    "total_trades":     all_trades,
                    "total_wins":       int(all_wins),
                },
                "bots":             bots_out,
                "tracked_traders":  [],
                "open_positions":   open_positions,
                "closed_positions": closed_positions,
                "recent_trades":    [],
            }
        except Exception as e:
            print(f"[polymarket_data] Error: {e}")
            import traceback; traceback.print_exc()
            data = pending_setup()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    n_closed = len(data.get("closed_positions", []))
    print(f"[polymarket_data] Wrote {OUTPUT_FILE} (bots={len(data.get('bots',[]))}, closed={n_closed})")


if __name__ == "__main__":
    main()
