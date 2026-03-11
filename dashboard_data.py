#!/usr/bin/env python3
"""Generate dashboard.json for the Viking Fleet web dashboard.
Run every 5 minutes via cron to keep the dashboard live."""

import json
import os
from datetime import datetime, timezone, timedelta

WORKSPACE = "/root/.openclaw/workspace"
OUT_FILE  = "/var/www/dashboard/api/dashboard.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def get_live_sprint(league, active_sprint_id):
    if not active_sprint_id:
        return None

    if league == "day":
        active_dir = os.path.join(WORKSPACE, "competition", "active", active_sprint_id)
    else:
        active_dir = os.path.join(WORKSPACE, "competition", "swing", "active", active_sprint_id)

    if not os.path.isdir(active_dir):
        return None

    meta = load_json(os.path.join(active_dir, "meta.json"))
    if not meta:
        return None

    bots = []
    for fname in sorted(os.listdir(active_dir)):
        if not fname.startswith("portfolio-"):
            continue
        p = load_json(os.path.join(active_dir, fname))
        if not p:
            continue
        bots.append({
            "bot":           p["bot"],
            "equity":        round(p["equity"], 2),
            "pnl_usd":       round(p["stats"]["total_pnl_usd"], 2),
            "pnl_pct":       round(p["stats"]["total_pnl_pct"], 4),
            "trades":        p["stats"]["total_trades"],
            "wins":          p["stats"]["wins"],
            "losses":        p["stats"]["losses"],
            "win_rate":      p["stats"]["win_rate"],
            "max_drawdown":  round(p["stats"]["max_drawdown_pct"], 4),
            "open_positions": len(p.get("positions", [])),
            "positions":     p.get("positions", []),
        })

    bots.sort(key=lambda x: x["equity"], reverse=True)
    for i, b in enumerate(bots):
        b["rank"] = i + 1

    started_at = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    ends_at    = started_at + timedelta(hours=meta["duration_hours"])
    now        = datetime.now(timezone.utc)
    secs_left  = max(0, int((ends_at - now).total_seconds()))

    return {
        "sprint_id":        active_sprint_id,
        "started_at":       meta["started_at"],
        "ends_at":          ends_at.isoformat(),
        "duration_hours":   meta["duration_hours"],
        "seconds_remaining": secs_left,
        "pairs":            meta.get("pairs", []),
        "bots":             bots,
    }


def build():
    day_lb   = load_json(os.path.join(WORKSPACE, "competition", "leaderboard.json"))
    swing_lb = load_json(os.path.join(WORKSPACE, "competition", "swing", "swing_leaderboard.json"))
    funded   = load_json("/var/www/dashboard/api/funded.json") or []

    dashboard = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "leagues":      {},
        "funded_bots":  funded,
    }

    if day_lb:
        active = day_lb.get("active_sprint")
        dashboard["leagues"]["day"] = {
            "label":                "Day Trading League",
            "sprint_duration_hours": 24,
            "active_sprint":        active,
            "total_sprints":        day_lb.get("total_sprints", 0),
            "cumulative_rankings":  day_lb.get("rankings", []),
            "live_sprint":          get_live_sprint("day", active),
        }

    if swing_lb:
        active = swing_lb.get("active_sprint")
        dashboard["leagues"]["swing"] = {
            "label":                "Swing Trading League",
            "sprint_duration_hours": 168,
            "active_sprint":        active,
            "total_sprints":        swing_lb.get("total_sprints", 0),
            "cumulative_rankings":  swing_lb.get("rankings", []),
            "live_sprint":          get_live_sprint("swing", active),
        }

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}] dashboard.json written")


if __name__ == "__main__":
    build()
