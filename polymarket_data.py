#!/usr/bin/env python3
"""
polymarket_data.py — Generate /var/www/dashboard/api/polymarket.json

Emits the 10 PM copy-trader bots (with their Polymarket trader usernames from
pm_leaders_seed.json) for Live Action display. Autonomous fleet data lives in
polymarket_auto.json (written by polymarket_syn_tick.py); the dashboard merges
both feeds.

Updated 2026-04-25 during Phase 7 Kalshi retirement: Kalshi copy fleet is
paused (no destination exchange until offshore Polymarket goes live) but the
10 leader-wallet identities remain visible in Live Action with their PM
usernames so the roster is preserved.
"""
import json
import os
from datetime import datetime, timezone

AUTO_STATE_FILE = "/root/.openclaw/workspace/competition/polymarket/auto_state.json"
LEADERS_SEED    = "/root/.openclaw/workspace/research/pm_leaders_seed.json"
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


def load_copy_bots():
    """Build the 10 copy-trader bot rows from pm_leaders_seed.json.
    Each row carries the Polymarket trader username so Live Action shows it."""
    if not os.path.isfile(LEADERS_SEED):
        return []
    try:
        with open(LEADERS_SEED) as f:
            seed = json.load(f)
    except Exception:
        return []
    leaders = seed.get("leaders") or []
    bots = []
    for L in leaders:
        bots.append({
            "bot":              L.get("bot_alias", ""),
            "assigned_trader":  L.get("pm_trader", ""),
            "pm_wallet":        L.get("pm_wallet", ""),
            "pnl_usd":          0.0,
            "win_rate":         0.0,
            "trades":           0,
            "active_positions": 0,
            "status":           "paused",
            "sprint_pnl_usd":   0.0,
            "sprint_win_rate":  0.0,
            "sprint_trades":    0,
        })
    return bots


def main():
    sprint_meta = {}
    if os.path.exists(AUTO_STATE_FILE):
        try:
            with open(AUTO_STATE_FILE) as f:
                raw = json.load(f)
            sprint_meta = {
                "mode":              raw.get("mode", "paper"),
                "status":            raw.get("status", "active"),
                "sprint_id":         raw.get("sprint_id", ""),
                "sprint_started_at": raw.get("sprint_started_at", ""),
                "sprint_ends_at":    raw.get("sprint_ends_at", ""),
            }
        except Exception:
            sprint_meta = {}

    copy_bots = load_copy_bots()

    if not copy_bots and not sprint_meta:
        data = pending_setup()
    else:
        total_pnl  = sum(b["pnl_usd"] for b in copy_bots)
        all_trades = sum(b["trades"] for b in copy_bots)
        active_pos = sum(b["active_positions"] for b in copy_bots)
        data = {
            "generated_at":      datetime.now(timezone.utc).isoformat(),
            "mode":              sprint_meta.get("mode", "paper"),
            "status":            sprint_meta.get("status", "active"),
            "sprint_id":         sprint_meta.get("sprint_id", ""),
            "sprint_started_at": sprint_meta.get("sprint_started_at", ""),
            "sprint_ends_at":    sprint_meta.get("sprint_ends_at", ""),
            "stats": {
                "total_pnl_usd":    round(total_pnl, 2),
                "overall_win_rate": 0.0,
                "active_positions": active_pos,
                "total_trades":     all_trades,
                "total_wins":       0,
            },
            "bots":             copy_bots,
            "tracked_traders":  [{"alias": b["bot"], "username": b["assigned_trader"], "wallet": b["pm_wallet"]} for b in copy_bots],
            "open_positions":   [],
            "closed_positions": [],
            "recent_trades":    [],
        }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[polymarket_data] Wrote {OUTPUT_FILE} (copy_bots={len(data.get('bots',[]))})")


if __name__ == "__main__":
    main()
