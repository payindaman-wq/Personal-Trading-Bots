#!/usr/bin/env python3
"""Generate dashboard.json for the Viking Fleet web dashboard.
Run every 5 minutes via cron to keep the dashboard live."""

import json
import os
import re
import time
from datetime import datetime, timezone, timedelta

WORKSPACE = "/root/.openclaw/workspace"
OUT_FILE  = "/var/www/dashboard/api/dashboard.json"

DAY_LB_PATH   = os.path.join(WORKSPACE, "competition", "leaderboard.json")
SWING_LB_PATH = os.path.join(WORKSPACE, "competition", "swing", "swing_leaderboard.json")

DAY_CRON_LOG   = os.path.join(WORKSPACE, "competition", "cron.log")
SWING_TICK_LOG = os.path.join(WORKSPACE, "competition", "swing", "tick.log")

DAY_RESULTS_DIR   = os.path.join(WORKSPACE, "competition", "results")
SWING_RESULTS_DIR = os.path.join(WORKSPACE, "competition", "swing", "results")

BOT_NAMES = [
    "floki", "bjorn", "lagertha", "ragnar", "leif", "gunnar",
    "harald", "freydis", "sigurd", "astrid", "ulf", "bjarne",
    "egil", "solveig", "orm", "gudrid", "halfdan", "thyra",
    "valdis", "runa", "ivar",
]

FLEET_ROSTER = [
    # Day league
    {"bot": "floki",    "league": "day",   "style": "Multi-TF confluence scalper",  "inspired_by": "Daan Crypto Trades"},
    {"bot": "bjorn",    "league": "day",   "style": "EMA + MACD momentum",          "inspired_by": "Crypto Tony"},
    {"bot": "lagertha", "league": "day",   "style": "VWAP trend directional",       "inspired_by": "TheWhiteWhaleHL"},
    {"bot": "ragnar",   "league": "day",   "style": "VWAP reclaim",                 "inspired_by": "VWAP reclaim"},
    {"bot": "leif",     "league": "day",   "style": "BB squeeze breakout",          "inspired_by": "Rekt Capital"},
    {"bot": "gunnar",   "league": "day",   "style": "Aggressive momentum scalper",  "inspired_by": "Gainzy"},
    {"bot": "harald",   "league": "day",   "style": "RSI + trend composite",        "inspired_by": "Scott Melker"},
    {"bot": "freydis",  "league": "day",   "style": "Contrarian extreme reversal",  "inspired_by": "GCRClassic"},
    {"bot": "sigurd",   "league": "day",   "style": "Altcoin momentum rotation",    "inspired_by": "van de Poppe"},
    {"bot": "astrid",   "league": "day",   "style": "RSI mean reversion",           "inspired_by": "Crypto Jebb"},
    {"bot": "ulf",      "league": "day",   "style": "Breakout retest precision",    "inspired_by": "The Trading Rush"},
    {"bot": "bjarne",   "league": "day",   "style": "Trend pullback buyer",         "inspired_by": "Credible Crypto"},
    # Swing league
    {"bot": "egil",     "league": "swing", "style": "Weekly trend follower",        "inspired_by": "Benjamin Cowen"},
    {"bot": "solveig",  "league": "swing", "style": "Multi-day mean reversion",     "inspired_by": "Crypto Jebb"},
    {"bot": "orm",      "league": "swing", "style": "Macro pullback buyer",         "inspired_by": "InvestAnswers"},
    {"bot": "gudrid",   "league": "swing", "style": "Macro sentiment",              "inspired_by": "Coin Bureau"},
    {"bot": "halfdan",  "league": "swing", "style": "Technical structure",          "inspired_by": "CryptoCred"},
    {"bot": "thyra",    "league": "swing", "style": "Altcoin cycles",               "inspired_by": "Altcoin Daily"},
    {"bot": "valdis",   "league": "swing", "style": "Swing breakout",               "inspired_by": "Rekt Capital"},
    {"bot": "runa",     "league": "swing", "style": "Bitcoin maximalist",           "inspired_by": "Tone Vays"},
    {"bot": "ivar",     "league": "swing", "style": "Narrative momentum swing",     "inspired_by": "chris-crypto"},
]


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def file_age_minutes(path):
    """Return age of file in minutes, or None if file does not exist."""
    try:
        mtime = os.path.getmtime(path)
        return (time.time() - mtime) / 60.0
    except Exception:
        return None


def get_system_health(day_lb, swing_lb):
    """Compute tick freshness for both leagues."""
    now_iso = datetime.now(timezone.utc).isoformat()

    day_age   = file_age_minutes(DAY_LB_PATH)
    swing_age = file_age_minutes(SWING_LB_PATH)

    day_active   = bool(day_lb and day_lb.get("active_sprint"))
    swing_active = bool(swing_lb and swing_lb.get("active_sprint"))

    # Stalled only when a sprint is running and the tick file is too old
    day_stalled   = day_active   and day_age   is not None and day_age   > 15
    swing_stalled = swing_active and swing_age is not None and swing_age > 90

    return {
        "day_tick_age_min":   round(day_age,   2) if day_age   is not None else None,
        "day_tick_stalled":   day_stalled,
        "swing_tick_age_min": round(swing_age, 2) if swing_age is not None else None,
        "swing_tick_stalled": swing_stalled,
        "checked_at":         now_iso,
    }


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
        # Swing portfolios have an 'equity' field; day trading portfolios use
        # 'cash' + open position cost_basis to derive equity.
        if "equity" in p:
            equity = p["equity"]
        else:
            equity = p.get("cash", 0) + sum(
                pos.get("cost_basis", 0) for pos in p.get("positions", [])
            )
        s = p["stats"]
        bots.append({
            "bot":            p["bot"],
            "equity":         round(equity, 2),
            "pnl_usd":        round(s["total_pnl_usd"], 2),
            "pnl_pct":        round(s["total_pnl_pct"], 4),
            "trades":         s["total_trades"],
            "wins":           s["wins"],
            "losses":         s["losses"],
            "win_rate":       s["win_rate"],
            "max_drawdown":   round(s["max_drawdown_pct"], 4),
            "open_positions": len(p.get("positions", [])),
            "positions":      p.get("positions", []),
        })

    bots.sort(key=lambda x: x["equity"], reverse=True)
    for i, b in enumerate(bots):
        b["rank"] = i + 1

    started_at = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    ends_at    = started_at + timedelta(hours=meta["duration_hours"])
    now        = datetime.now(timezone.utc)
    secs_left  = max(0, int((ends_at - now).total_seconds()))

    return {
        "sprint_id":         active_sprint_id,
        "started_at":        meta["started_at"],
        "ends_at":           ends_at.isoformat(),
        "duration_hours":    meta["duration_hours"],
        "seconds_remaining": secs_left,
        "pairs":             meta.get("pairs", []),
        "bots":              bots,
    }


def get_fleet_roster(day_lb, swing_lb):
    """Build fleet roster merging static metadata with live cumulative stats."""
    # Index cumulative rankings by bot name
    day_stats   = {}
    swing_stats = {}

    if day_lb:
        for entry in day_lb.get("rankings", []):
            day_stats[entry["bot"].lower()] = entry

    if swing_lb:
        for entry in swing_lb.get("rankings", []):
            swing_stats[entry["bot"].lower()] = entry

    roster = []
    for member in FLEET_ROSTER:
        bot  = member["bot"]
        key  = bot.lower()
        src  = day_stats if member["league"] == "day" else swing_stats
        stats = src.get(key, {})

        roster.append({
            "bot":                    bot,
            "league":                 member["league"],
            "style":                  member["style"],
            "inspired_by":            member["inspired_by"],
            "sprints_entered":        stats.get("sprints_entered", 0),
            "sprint_wins":            stats.get("sprint_wins", 0),
            "podiums":                stats.get("podiums", 0),
            "points":                 stats.get("points", 0),
            "cumulative_pnl_usd":     round(stats.get("cumulative_pnl_usd", 0.0), 2),
            "avg_pnl_pct_per_sprint": round(stats.get("avg_pnl_pct_per_sprint", 0.0), 4),
            "overall_win_rate":       round(stats.get("overall_win_rate", 0.0), 2),
            "total_trades":           stats.get("total_trades", 0),
        })

    return roster


def get_activity_feed(day_active_id, swing_active_id):
    """Scan active portfolios and log files for recent activity events."""
    events = []

    # ── Open positions from active portfolio files ──
    for league, active_id in [("day", day_active_id), ("swing", swing_active_id)]:
        if not active_id:
            continue

        if league == "day":
            active_dir = os.path.join(WORKSPACE, "competition", "active", active_id)
        else:
            active_dir = os.path.join(WORKSPACE, "competition", "swing", "active", active_id)

        if not os.path.isdir(active_dir):
            continue

        for fname in sorted(os.listdir(active_dir)):
            if not fname.startswith("portfolio-"):
                continue
            p = load_json(os.path.join(active_dir, fname))
            if not p:
                continue
            bot = p.get("bot", fname.replace("portfolio-", "").replace(".json", ""))
            for pos in p.get("positions", []):
                events.append({
                    "type":        "position_open",
                    "league":      league,
                    "bot":         bot,
                    "pair":        pos.get("pair", "?"),
                    "direction":   pos.get("direction", "long"),
                    "entry_price": pos.get("entry_price", pos.get("cost_basis", 0)),
                    "timestamp":   pos.get("opened_at", None),
                })

    # ── Log file events ──
    bot_pattern = r"(?i)\b(" + "|".join(BOT_NAMES) + r")\b"
    action_pattern = r"(?i)\b(OPEN|CLOSE|BUY|SELL|EXECUTE)\b"

    for league, log_path in [("day", DAY_CRON_LOG), ("swing", SWING_TICK_LOG)]:
        try:
            with open(log_path, "r", errors="replace") as fh:
                lines = fh.readlines()
        except Exception:
            continue

        # Read last 200 lines to limit scan
        for line in lines[-200:]:
            line = line.rstrip()
            if re.search(bot_pattern, line) and re.search(action_pattern, line):
                m = re.search(bot_pattern, line)
                bot_found = m.group(1).lower() if m else "unknown"
                events.append({
                    "type":      "log",
                    "league":    league,
                    "bot":       bot_found,
                    "raw":       line[:200],
                    "timestamp": None,
                })

    # Return most recent 30 events (position_open first, then logs)
    position_events = [e for e in events if e["type"] == "position_open"]
    log_events      = [e for e in events if e["type"] == "log"]
    combined        = position_events + log_events[-max(0, 30 - len(position_events)):]
    return combined[:30]


def get_sprint_archive():
    """Load completed sprint results from both leagues, normalized to $1k base."""
    archive = []

    sources = [
        ("day",   DAY_RESULTS_DIR),
        ("swing", SWING_RESULTS_DIR),
    ]

    for league, results_dir in sources:
        if not os.path.isdir(results_dir):
            continue

        for entry_name in os.listdir(results_dir):
            entry_path = os.path.join(results_dir, entry_name)
            if not os.path.isdir(entry_path):
                continue

            final_score = load_json(os.path.join(entry_path, "final_score.json"))
            meta        = load_json(os.path.join(entry_path, "meta.json"))

            if not final_score or not meta:
                continue

            raw_rankings = final_score.get("rankings", [])
            if len(raw_rankings) < 3:
                continue

            starting_capital = meta.get("starting_capital", 1000.0)
            usd_scale        = 1000.0 / starting_capital if starting_capital else 1.0

            rankings = []
            for r in raw_rankings:
                raw_pnl = r.get("total_pnl_usd", 0.0)
                norm_pnl = raw_pnl * usd_scale
                final_eq = 1000.0 + norm_pnl
                rankings.append({
                    "rank":          r.get("rank", 0),
                    "bot":           r.get("bot", ""),
                    "final_equity":  round(final_eq, 2),
                    "total_pnl_usd": round(norm_pnl, 2),
                    "total_pnl_pct": round(r.get("total_pnl_pct", 0.0), 4),
                    "total_trades":  r.get("total_trades", 0),
                    "win_rate":      round(r.get("win_rate", 0.0), 2),
                })

            winner = rankings[0]["bot"] if rankings else ""

            # Parse started_at from meta and compute duration
            started_at_raw = meta.get("started_at", "")
            scored_at_raw  = final_score.get("scored_at", meta.get("ended_at", ""))
            duration_hours = meta.get("duration_hours", 0)

            archive.append({
                "comp_id":        entry_name,
                "league":         league,
                "winner":         winner,
                "duration_hours": duration_hours,
                "started_at":     started_at_raw,
                "scored_at":      scored_at_raw,
                "pairs":          meta.get("pairs", []),
                "rankings":       rankings,
            })

    # Sort newest first by comp_id (lexicographic on timestamp-based IDs)
    archive.sort(key=lambda x: x["comp_id"], reverse=True)
    return archive


def build():
    day_lb   = load_json(DAY_LB_PATH)
    swing_lb = load_json(SWING_LB_PATH)
    funded   = load_json("/var/www/dashboard/api/funded.json") or []

    day_active_id   = day_lb.get("active_sprint")   if day_lb   else None
    swing_active_id = swing_lb.get("active_sprint") if swing_lb else None

    dashboard = {
        "generated_at":  datetime.now(timezone.utc).isoformat(),
        "leagues":       {},
        "funded_bots":   funded,
        "system_health": get_system_health(day_lb, swing_lb),
        "fleet_roster":  get_fleet_roster(day_lb, swing_lb),
        "activity_feed": get_activity_feed(day_active_id, swing_active_id),
        "sprint_archive": get_sprint_archive(),
    }

    if day_lb:
        dashboard["leagues"]["day"] = {
            "label":                 "Day Trading League",
            "sprint_duration_hours": 24,
            "active_sprint":         day_active_id,
            "total_sprints":         day_lb.get("total_sprints", 0),
            "cumulative_rankings":   day_lb.get("rankings", []),
            "live_sprint":           get_live_sprint("day", day_active_id),
        }

    if swing_lb:
        dashboard["leagues"]["swing"] = {
            "label":                 "Swing Trading League",
            "sprint_duration_hours": 168,
            "active_sprint":         swing_active_id,
            "total_sprints":         swing_lb.get("total_sprints", 0),
            "cumulative_rankings":   swing_lb.get("rankings", []),
            "live_sprint":           get_live_sprint("swing", swing_active_id),
        }

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}] dashboard.json written")


if __name__ == "__main__":
    build()
