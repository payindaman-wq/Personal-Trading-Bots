#!/usr/bin/env python3
"""
polymarket_data.py — Generate /var/www/dashboard/api/polymarket.json
Reads from kalshi_copy_state.json (_k bots, live Kalshi activity) and
kalshi_copy_pm_backfill.json (historical PM activity for the current sprint).
"""
import json
import os
from datetime import datetime, timezone

KALSHI_STATE_FILE = "/root/.openclaw/workspace/competition/polymarket/kalshi_copy_state.json"
PM_BACKFILL_FILE  = "/root/.openclaw/workspace/competition/polymarket/kalshi_copy_pm_backfill.json"
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


def load_backfill():
    """Load PM backfill data; returns dict keyed by bot name."""
    if not os.path.exists(PM_BACKFILL_FILE):
        return {}
    try:
        with open(PM_BACKFILL_FILE) as f:
            bf = json.load(f)
        return bf.get("bots", {})
    except Exception:
        return {}


def main():
    if not os.path.exists(KALSHI_STATE_FILE):
        data = pending_setup()
    else:
        try:
            with open(KALSHI_STATE_FILE) as f:
                raw = json.load(f)

            raw_bots = raw.get("bots", [])
            backfill = load_backfill()

            bots_out         = []
            open_positions   = []
            closed_positions = []
            sprint_started   = raw.get("sprint_started_at", "")

            for b in raw_bots:
                bot_name = b.get("name", b.get("bot", ""))
                bf = backfill.get(bot_name, {})

                # Merge Kalshi live + PM backfill stats
                kalshi_pnl     = b.get("pnl_usd", 0.0)
                kalshi_trades  = b.get("total_trades", 0)
                kalshi_wins    = b.get("wins", 0)
                kalshi_losses  = b.get("losses", 0)
                kalshi_sp_pnl  = b.get("sprint_pnl_usd", 0.0)
                kalshi_sp_tr   = b.get("sprint_trades", 0)
                kalshi_sp_wins = b.get("sprint_wins", 0)

                pm_pnl     = bf.get("pnl_usd", 0.0)
                pm_trades  = bf.get("total_trades", 0)
                pm_wins    = bf.get("wins", 0)
                pm_losses  = bf.get("losses", 0)
                pm_sp_pnl  = bf.get("sprint_pnl_usd", 0.0)
                pm_sp_tr   = bf.get("sprint_trades", 0)
                pm_sp_wins = bf.get("sprint_wins", 0)

                merged_pnl     = round(kalshi_pnl + pm_pnl, 2)
                merged_trades  = kalshi_trades + pm_trades
                merged_wins    = kalshi_wins + pm_wins
                merged_losses  = kalshi_losses + pm_losses
                merged_sp_pnl  = round(kalshi_sp_pnl + pm_sp_pnl, 2)
                merged_sp_tr   = kalshi_sp_tr + pm_sp_tr
                merged_sp_wins = kalshi_sp_wins + pm_sp_wins

                win_rate    = round(merged_wins / merged_trades * 100, 1) if merged_trades > 0 else 0.0
                sp_win_rate = round(merged_sp_wins / merged_sp_tr * 100, 1) if merged_sp_tr > 0 else 0.0
                active_pos  = len(b.get("positions", {}))

                bots_out.append({
                    "bot":              bot_name,
                    "assigned_trader":  b.get("pm_trader", b.get("trader", "?")),
                    "pnl_usd":          merged_pnl,
                    "win_rate":         win_rate,
                    "trades":           merged_trades,
                    "active_positions": active_pos,
                    "status":           "active",
                    "sprint_pnl_usd":   merged_sp_pnl,
                    "sprint_win_rate":  sp_win_rate,
                    "sprint_trades":    merged_sp_tr,
                })

                # Open positions (Kalshi live only)
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

                # Closed trades: Kalshi live
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
                        "source":       t.get("source", "kalshi"),
                    })

                # Closed trades: PM backfill
                for t in bf.get("closed_trades", []):
                    ts = t.get("closed_at", "")
                    closed_positions.append({
                        "bot":          bot_name,
                        "market_title": t.get("title", ""),
                        "direction":    t.get("outcome", ""),
                        "outcome":      "win" if (t.get("pnl_usd") or 0) >= 0 else "loss",
                        "pnl_usd":      t.get("pnl_usd", 0),
                        "closed_at":    ts,
                        "source":       "polymarket",
                    })

            closed_positions.sort(key=lambda x: x.get("closed_at") or "", reverse=True)

            # Fleet-level stats
            total_pnl  = sum(b["pnl_usd"] for b in bots_out)
            all_trades = sum(b["trades"] for b in bots_out)
            all_wins   = round(sum(b["win_rate"] * b["trades"] / 100 for b in bots_out))
            active_pos = sum(b["active_positions"] for b in bots_out)
            win_rate   = round(all_wins / all_trades * 100, 1) if all_trades > 0 else 0.0

            data = {
                "generated_at":      datetime.now(timezone.utc).isoformat(),
                "mode":              raw.get("mode", "simulation"),
                "status":            "active",
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
