#!/usr/bin/env python3
"""
polymarket_data.py — Generate /var/www/dashboard/api/polymarket.json

Reads competition/polymarket/state.json (the live Polymarket copy-trader
competition state, written by polymarket_tick.py / polymarket.service) and
emits the dashboard feed.

If state.json is missing, falls back to a roster view built from
research/pm_leaders_seed.json so the 10 copy bots are still visible by name
+ Polymarket trader. The competition runs in paper mode regardless of
real-money funding (Phase 7 is independent).
"""
import json
import os
from datetime import datetime, timezone

STATE_FILE   = "/root/.openclaw/workspace/competition/polymarket/state.json"
LEADERS_SEED = "/root/.openclaw/workspace/research/pm_leaders_seed.json"
OUTPUT_FILE  = "/var/www/dashboard/api/polymarket.json"


def fallback_from_seed():
    """Roster-only view when state.json is missing — 10 bots, zero stats."""
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode":   "paper",
        "status": "active",
        "stats":  {"total_pnl_usd": 0.0, "overall_win_rate": 0.0,
                   "active_positions": 0, "total_trades": 0, "total_wins": 0},
        "bots": [], "tracked_traders": [],
        "open_positions": [], "closed_positions": [], "recent_trades": [],
    }
    if not os.path.isfile(LEADERS_SEED):
        return out
    try:
        seed = json.load(open(LEADERS_SEED))
    except Exception:
        return out
    for L in seed.get("leaders", []):
        out["bots"].append({
            "bot":              L.get("bot_alias", ""),
            "assigned_trader":  L.get("pm_trader", ""),
            "pnl_usd":          0.0,
            "win_rate":         0.0,
            "trades":           0,
            "active_positions": 0,
            "status":           "active",
            "sprint_pnl_usd":   0.0,
            "sprint_win_rate":  0.0,
            "sprint_trades":    0,
        })
        out["tracked_traders"].append({
            "name":   L.get("pm_trader", ""),
            "bot":    L.get("bot_alias", ""),
            "wallet": L.get("pm_wallet", ""),
        })
    return out


def normalize_from_state(state):
    """Convert competition state.json into the dashboard feed shape."""
    raw_bots = state.get("bots", [])
    sprint_started = state.get("sprint_started_at", "")
    status = state.get("status", "active")

    bots_out, open_positions, closed_positions = [], [], []
    for b in raw_bots:
        wins  = b.get("wins", 0)
        total = b.get("total_trades", 0)
        st    = b.get("sprint_trades", 0)
        sw    = b.get("sprint_wins", 0)
        bots_out.append({
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
        for cid, pos in b.get("positions", {}).items():
            open_positions.append({
                "bot":            b.get("name", ""),
                "trader":         b.get("trader", ""),
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
                "bot":          b.get("name", ""),
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

    return {
        "generated_at":      datetime.now(timezone.utc).isoformat(),
        "mode":              state.get("mode", "paper"),
        "status":            status,
        "started_at":        state.get("started_at", ""),
        "sprint_id":         state.get("sprint_id", ""),
        "sprint_started_at": sprint_started,
        "sprint_ends_at":    state.get("sprint_ends_at", ""),
        "stats": {
            "total_pnl_usd":    round(total_pnl, 2),
            "overall_win_rate": win_rate,
            "active_positions": active_pos,
            "total_trades":     all_trades,
            "total_wins":       int(all_wins),
        },
        "bots":             bots_out,
        "tracked_traders":  state.get("tracked_traders", []),
        "open_positions":   open_positions,
        "closed_positions": closed_positions,
        "recent_trades":    state.get("recent_trades", []),
    }


def main():
    if os.path.isfile(STATE_FILE):
        try:
            state = json.load(open(STATE_FILE))
            data  = normalize_from_state(state)
        except Exception as e:
            print(f"[polymarket_data] state.json read failed: {e} — using seed fallback")
            data = fallback_from_seed()
    else:
        data = fallback_from_seed()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[polymarket_data] Wrote {OUTPUT_FILE} (bots={len(data.get('bots',[]))} status={data.get('status')})")


if __name__ == "__main__":
    main()
