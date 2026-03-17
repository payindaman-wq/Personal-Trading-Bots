#!/usr/bin/env python3
"""Generate dashboard.json for the Viking Fleet web dashboard.
Run every 5 minutes via cron to keep the dashboard live."""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta

WORKSPACE = "/root/.openclaw/workspace"
OUT_FILE  = "/var/www/dashboard/api/dashboard.json"

DAY_LB_PATH   = os.path.join(WORKSPACE, "competition", "leaderboard.json")
SWING_LB_PATH = os.path.join(WORKSPACE, "competition", "swing", "swing_leaderboard.json")
ARB_LB_PATH    = os.path.join(WORKSPACE, "competition", "arb", "arb_leaderboard.json")
SPREAD_LB_PATH = os.path.join(WORKSPACE, "competition", "spread", "spread_leaderboard.json")

DAY_CRON_LOG   = os.path.join(WORKSPACE, "competition", "cron.log")
SWING_TICK_LOG  = os.path.join(WORKSPACE, "competition", "swing", "tick.log")
SPREAD_TICK_LOG = os.path.join(WORKSPACE, "competition", "spread", "tick.log")

DAY_RESULTS_DIR   = os.path.join(WORKSPACE, "competition", "results")
SWING_RESULTS_DIR = os.path.join(WORKSPACE, "competition", "swing", "results")
ARB_RESULTS_DIR   = os.path.join(WORKSPACE, "competition", "arb", "results")
SPREAD_RESULTS_DIR = os.path.join(WORKSPACE, "competition", "spread", "results")
CYCLE_STATE_PATH       = os.path.join(WORKSPACE, "competition", "cycle_state.json")
SWING_CYCLE_STATE_PATH = os.path.join(WORKSPACE, "competition", "swing", "swing_cycle_state.json")
POLY_CYCLE_STATE_PATH  = os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_cycle_state.json")
ARB_CYCLE_STATE_PATH   = os.path.join(WORKSPACE, "competition", "arb", "arb_cycle_state.json")
SPREAD_CYCLE_STATE_PATH = os.path.join(WORKSPACE, "competition", "spread", "spread_cycle_state.json")
POLY_LB_PATH   = os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_leaderboard.json")

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
    # Spread fleet
    {"bot": "skadi",    "league": "spread", "style": "ETH/BTC mean reversion",    "inspired_by": "Spread arb"},
    {"bot": "sigrid",   "league": "spread", "style": "SOL/BTC mean reversion",    "inspired_by": "Spread arb"},
    {"bot": "brynja",   "league": "spread", "style": "AAVE/LINK mean reversion",  "inspired_by": "Spread arb"},
    {"bot": "herdis",   "league": "spread", "style": "AVAX/SOL mean reversion",   "inspired_by": "Spread arb"},
    {"bot": "forseti",  "league": "spread", "style": "SOL/ETH momentum",          "inspired_by": "Spread arb"},
    {"bot": "gunhild",  "league": "spread", "style": "AVAX/ETH momentum",         "inspired_by": "Spread arb"},
    {"bot": "magni",    "league": "spread", "style": "LINK/ETH catch-up",         "inspired_by": "Spread arb"},
    {"bot": "sunniva",  "league": "spread", "style": "AAVE/ETH catch-up",         "inspired_by": "Spread arb"},
    {"bot": "ragnhild", "league": "spread", "style": "ETH/BTC breakout",          "inspired_by": "Spread arb"},
    {"bot": "estrid",   "league": "spread", "style": "SOL/ETH breakout",          "inspired_by": "Spread arb"},
    {"bot": "tofa",     "league": "spread", "style": "ETH/BTC dual confirmation", "inspired_by": "Spread arb"},
    {"bot": "ingrid",   "league": "spread", "style": "LINK/ETH dual confirmation","inspired_by": "Spread arb"},
    {"bot": "solrun",   "league": "spread", "style": "AAVE/LINK dual confirmation","inspired_by": "Spread arb"},
    {"bot": "thordis",  "league": "spread", "style": "AVAX/SOL dual confirmation", "inspired_by": "Spread arb"},

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


def get_system_health(day_lb, swing_lb, arb_lb=None, spread_lb=None):
    """Compute tick freshness for all leagues."""
    now_iso = datetime.now(timezone.utc).isoformat()

    day_age    = file_age_minutes(DAY_LB_PATH)
    swing_age  = file_age_minutes(SWING_LB_PATH)
    arb_age    = file_age_minutes(ARB_LB_PATH)
    spread_age = file_age_minutes(SPREAD_LB_PATH)

    day_active    = bool(day_lb    and day_lb.get("active_sprint"))
    swing_active  = bool(swing_lb  and swing_lb.get("active_sprint"))
    arb_active    = bool(arb_lb    and arb_lb.get("active_sprint"))
    spread_active = bool(spread_lb and spread_lb.get("active_sprint"))

    # Stalled only when a sprint is running and the tick file is too old
    day_stalled    = day_active    and day_age    is not None and day_age    > 15
    swing_stalled  = swing_active  and swing_age  is not None and swing_age  > 90
    arb_stalled    = arb_active    and arb_age    is not None and arb_age    > 90
    spread_stalled = spread_active and spread_age is not None and spread_age > 90

    return {
        "day_tick_age_min":    round(day_age,    2) if day_age    is not None else None,
        "day_tick_stalled":    day_stalled,
        "swing_tick_age_min":  round(swing_age,  2) if swing_age  is not None else None,
        "swing_tick_stalled":  swing_stalled,
        "arb_tick_age_min":    round(arb_age,    2) if arb_age    is not None else None,
        "arb_tick_stalled":    arb_stalled,
        "spread_tick_age_min": round(spread_age, 2) if spread_age is not None else None,
        "spread_tick_stalled": spread_stalled,
        "checked_at":          now_iso,
    }


def get_live_sprint(league, active_sprint_id):
    if not active_sprint_id:
        return None

    if league == "day":
        active_dir = os.path.join(WORKSPACE, "competition", "active", active_sprint_id)
    elif league == "arb":
        active_dir = os.path.join(WORKSPACE, "competition", "arb", "active", active_sprint_id)
    elif league == "spread":
        active_dir = os.path.join(WORKSPACE, "competition", "spread", "active", active_sprint_id)
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


def get_fleet_roster(day_lb, swing_lb, arb_lb=None, spread_lb=None):
    """Build fleet roster merging static metadata with live cumulative stats."""
    day_stats   = {}
    swing_stats = {}
    arb_stats    = {}
    spread_stats = {}

    if day_lb:
        for entry in day_lb.get("rankings", []):
            day_stats[entry["bot"].lower()] = entry
    if swing_lb:
        for entry in swing_lb.get("rankings", []):
            swing_stats[entry["bot"].lower()] = entry
    if arb_lb:
        for entry in arb_lb.get("rankings", []):
            arb_stats[entry["bot"].lower()] = entry
    if spread_lb:
        for entry in spread_lb.get("rankings", []):
            spread_stats[entry["bot"].lower()] = entry

    roster = []
    for member in FLEET_ROSTER:
        bot   = member["bot"]
        key   = bot.lower()
        lg    = member["league"]
        src   = day_stats if lg == "day" else (arb_stats if lg == "arb" else (spread_stats if lg == "spread" else swing_stats))
        stats = src.get(key, {})

        roster.append({
            "bot":                    bot,
            "league":                 lg,
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

    # Arb bots (not in FLEET_ROSTER — dynamic from arb_lb)
    if arb_lb:
        existing = {r["bot"].lower() for r in roster}
        for entry in arb_lb.get("rankings", []):
            if entry["bot"].lower() not in existing:
                roster.append({
                    "bot":                    entry["bot"],
                    "league":                 "arb",
                    "style":                  entry.get("style", "stat arb"),
                    "inspired_by":            "mean reversion",
                    "sprints_entered":        entry.get("sprints_entered", 0),
                    "sprint_wins":            entry.get("sprint_wins", 0),
                    "podiums":                entry.get("podiums", 0),
                    "points":                 entry.get("points", 0),
                    "cumulative_pnl_usd":     round(entry.get("cumulative_pnl_usd", 0.0), 2),
                    "avg_pnl_pct_per_sprint": round(entry.get("avg_pnl_pct_per_sprint", 0.0), 4),
                    "overall_win_rate":       round(entry.get("overall_win_rate", 0.0), 2),
                    "total_trades":           entry.get("total_trades", 0),
                })

    return roster


def _load_cycle_sprint_ids(league):
    """Return the list of completed sprint IDs in the current cycle for a league."""
    paths = {
        "day":    CYCLE_STATE_PATH,
        "swing":  SWING_CYCLE_STATE_PATH,
        "arb":    ARB_CYCLE_STATE_PATH,
        "spread": SPREAD_CYCLE_STATE_PATH,
    }
    try:
        state = load_json(paths[league])
        return state.get("sprints", []) if state else []
    except Exception:
        return []


def _archived_portfolio_dir(league, sprint_id):
    """Return the directory containing archived portfolio files for a completed sprint."""
    if league == "day":
        # Day archives portfolios directly in results/<sprint_id>/
        return os.path.join(DAY_RESULTS_DIR, sprint_id)
    results = {
        "swing":  SWING_RESULTS_DIR,
        "arb":    ARB_RESULTS_DIR,
        "spread": SPREAD_RESULTS_DIR,
    }
    return os.path.join(results[league], sprint_id + "_portfolios")


def _normalize_pos(league, pos):
    if league == "arb":
        return (
            pos.get("pair", f"{pos.get('pair_a','?')}/{pos.get('pair_b','?')}"),
            pos.get("entry_price_a", 0), 0,
            pos.get("size_usd", 0), pos.get("entry_z"), None,
        )
    return (
        pos.get("pair", "?"),
        pos.get("entry_price", 0),
        pos.get("quantity", 0),
        pos.get("cost_basis", pos.get("size_usd", 0)),
        None, None,
    )


def _normalize_ct(league, ct):
    if league == "arb":
        return (
            ct.get("pair", f"{ct.get('pair_a','?')}/{ct.get('pair_b','?')}"),
            ct.get("entry_price_a", 0), 0,
            0, ct.get("size_usd", 0),
            ct.get("entry_z"), ct.get("exit_z"),
        )
    return (
        ct.get("pair", "?"),
        ct.get("entry_price", 0),
        ct.get("exit_price", 0),
        ct.get("quantity", 0),
        ct.get("cost_basis", ct.get("size_usd", 0)),
        None, None,
    )


def _scan_portfolios(league, portfolio_dir, events, open_only=False):
    """Read portfolio files from a directory and append events."""
    if not os.path.isdir(portfolio_dir):
        return
    for fname in sorted(os.listdir(portfolio_dir)):
        if not fname.startswith("portfolio-"):
            continue
        p = load_json(os.path.join(portfolio_dir, fname))
        if not p:
            continue
        bot = p.get("bot", fname.replace("portfolio-", "").replace(".json", ""))

        if not open_only:
            for ct in p.get("closed_trades", []):
                pair, ep, xp, qty, cb, ez, exz = _normalize_ct(league, ct)
                events.append({
                    "type": "position_close", "league": league, "bot": bot,
                    "pair": pair, "direction": ct.get("direction", "long"),
                    "entry_price": ep, "exit_price": xp,
                    "quantity": qty, "cost_basis": cb,
                    "entry_z": ez, "exit_z": exz,
                    "net_pnl": ct.get("net_pnl", 0),
                    "pnl_pct": ct.get("pnl_pct", 0),
                    "reason":  ct.get("reason", ""),
                    "timestamp": ct.get("closed_at"),
                })

        for pos in p.get("positions", []):
            if open_only:
                pair, ep, qty, cb, ez, _ = _normalize_pos(league, pos)
                events.append({
                    "type": "position_open", "league": league, "bot": bot,
                    "pair": pair, "direction": pos.get("direction", "long"),
                    "entry_price": ep, "quantity": qty, "cost_basis": cb,
                    "entry_z": ez, "timestamp": pos.get("opened_at"),
                })


def get_activity_feed(day_active_id, swing_active_id, arb_active_id=None, spread_active_id=None):
    """Open positions from active sprint + closed trades from entire current cycle."""
    events = []

    ACTIVE_DIRS = {
        "day":    os.path.join(WORKSPACE, "competition", "active"),
        "swing":  os.path.join(WORKSPACE, "competition", "swing",  "active"),
        "arb":    os.path.join(WORKSPACE, "competition", "arb",    "active"),
        "spread": os.path.join(WORKSPACE, "competition", "spread", "active"),
    }
    ACTIVE_IDS = {
        "day": day_active_id, "swing": swing_active_id,
        "arb": arb_active_id, "spread": spread_active_id,
    }

    for league in ["day", "swing", "arb", "spread"]:
        active_id = ACTIVE_IDS[league]

        # ── Open positions: active sprint only ──
        if active_id:
            active_dir = os.path.join(ACTIVE_DIRS[league], active_id)
            _scan_portfolios(league, active_dir, events, open_only=True)

        # ── Closed trades: all completed sprints in current cycle + active sprint ──
        cycle_sprints = _load_cycle_sprint_ids(league)
        for sprint_id in cycle_sprints:
            _scan_portfolios(league, _archived_portfolio_dir(league, sprint_id), events, open_only=False)
        if active_id:
            active_dir = os.path.join(ACTIVE_DIRS[league], active_id)
            _scan_portfolios(league, active_dir, events, open_only=False)

    # Open positions first, then closed sorted newest-first
    position_events = [e for e in events if e["type"] == "position_open"]
    closed_events   = [e for e in events if e["type"] == "position_close"]
    closed_events.sort(key=lambda e: e.get("timestamp") or "", reverse=True)
    return position_events + closed_events[:50]


def get_sprint_archive():
    """Load completed sprint results from both leagues, normalized to $1k base."""
    archive = []

    sources = [
        ("day",    DAY_RESULTS_DIR),
        ("swing",  SWING_RESULTS_DIR),
        ("arb",    ARB_RESULTS_DIR),
        ("spread", SPREAD_RESULTS_DIR),
    ]

    for league, results_dir in sources:
        if not os.path.isdir(results_dir):
            continue

        for entry_name in os.listdir(results_dir):
            entry_path = os.path.join(results_dir, entry_name)
            if not os.path.isdir(entry_path):
                continue

            final_score = load_json(os.path.join(entry_path, "final_score.json"))
            # meta.json may be in entry_path directly (day) or in _portfolios dir (swing/arb/spread)
            meta = load_json(os.path.join(entry_path, "meta.json"))
            if meta is None:
                portfolios_dir = os.path.join(results_dir, entry_name + "_portfolios")
                meta = load_json(os.path.join(portfolios_dir, "meta.json"))
            # Final fallback: reconstruct minimal meta from final_score.json
            if meta is None and final_score:
                meta = {
                    "started_at":      final_score.get("scored_at", ""),
                    "duration_hours":  final_score.get("duration_hours", 0),
                    "pairs":           final_score.get("pairs", []),
                    "starting_capital": 1000.0,
                }

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

            # Compute is_complete: True if end time has passed
            try:
                from datetime import datetime, timezone, timedelta as _td
                _utc = timezone.utc
                _started = datetime.fromisoformat(started_at_raw.replace("Z", "+00:00")) if started_at_raw else None
                if _started and duration_hours:
                    is_complete = datetime.now(_utc) >= _started + _td(hours=duration_hours)
                else:
                    is_complete = True  # if we can't determine, assume complete
            except Exception:
                is_complete = True

            archive.append({
                "comp_id":        entry_name,
                "league":         league,
                "winner":         winner,
                "duration_hours": duration_hours,
                "started_at":     started_at_raw,
                "scored_at":      scored_at_raw,
                "pairs":          meta.get("pairs", []),
                "rankings":       rankings,
                "is_complete":    is_complete,
            })

    # Sort newest first by comp_id (lexicographic on timestamp-based IDs)
    archive.sort(key=lambda x: x["comp_id"], reverse=True)
    return archive



def get_cycle_state():
    try:
        with open(CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 7, "status": "active"}


def get_swing_cycle_state():
    try:
        with open(SWING_CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


def get_poly_cycle_state():
    try:
        with open(POLY_CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


def get_spread_cycle_state():
    try:
        p = os.path.join(WORKSPACE, "competition", "spread", "spread_cycle_state.json")
        with open(p) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


def get_arb_cycle_state():
    try:
        with open(ARB_CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


def get_spread_score():
    """Import and run the spread strategy scoring script."""
    try:
        if WORKSPACE not in sys.path:
            sys.path.insert(0, WORKSPACE)
        from swing_spread_score import collect_all_stats, score_strategy, STRATEGY_GROUPS, CRITERIA
        bot_stats, sprint_count = collect_all_stats(include_active=True)
        results = []
        for name, group_def in STRATEGY_GROUPS.items():
            results.append(score_strategy(name, group_def, bot_stats))
        return {
            "sprint_count": sprint_count,
            "strategies":   results,
            "criteria":     CRITERIA,
        }
    except Exception as e:
        return {"error": str(e), "strategies": [], "sprint_count": 0}



def get_cycle_state():
    try:
        with open(CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 7, "status": "active"}


def get_cycle_state():
    try:
        with open(CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 7, "status": "active"}


def get_cycle_state():
    try:
        with open(CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 7, "status": "active"}

def build():
    day_lb   = load_json(DAY_LB_PATH)
    swing_lb = load_json(SWING_LB_PATH)
    arb_lb    = load_json(ARB_LB_PATH)
    spread_lb = load_json(SPREAD_LB_PATH)
    funded   = load_json("/var/www/dashboard/api/funded.json") or []

    day_active_id   = day_lb.get("active_sprint")   if day_lb   else None
    swing_active_id = swing_lb.get("active_sprint") if swing_lb else None
    arb_active_id    = arb_lb.get("active_sprint")    if arb_lb    else None
    spread_active_id = spread_lb.get("active_sprint") if spread_lb else None

    dashboard = {
        "generated_at":  datetime.now(timezone.utc).isoformat(),
        "leagues":       {},
        "funded_bots":   funded,
        "system_health": get_system_health(day_lb, swing_lb, arb_lb, spread_lb),
        "fleet_roster":  get_fleet_roster(day_lb, swing_lb, arb_lb, spread_lb),
        "activity_feed": get_activity_feed(day_active_id, swing_active_id, arb_active_id, spread_active_id),
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

    if arb_lb:
        dashboard["leagues"]["arb"] = {
            "label":                 "Arbitrage Trading League",
            "sprint_duration_hours": 168,
            "active_sprint":         arb_active_id,
            "total_sprints":         arb_lb.get("total_sprints", 0),
            "cumulative_rankings":   arb_lb.get("rankings", []),
            "live_sprint":           get_live_sprint("arb", arb_active_id),
        }

    if spread_lb:
        dashboard["leagues"]["spread"] = {
            "label":                 "Spread Trading League",
            "sprint_duration_hours": 168,
            "active_sprint":         spread_active_id,
            "total_sprints":         spread_lb.get("total_sprints", 0),
            "cumulative_rankings":   spread_lb.get("rankings", []),
            "live_sprint":           get_live_sprint("spread", spread_active_id),
        }

    dashboard["cycle_state"]       = get_cycle_state()
    dashboard["spread_score"]      = get_spread_score()
    dashboard["spread_cycle_state"] = get_spread_cycle_state()
    dashboard["swing_cycle_state"] = get_swing_cycle_state()
    dashboard["poly_cycle_state"]  = get_poly_cycle_state()
    poly_lb = load_json(POLY_LB_PATH) if os.path.exists(POLY_LB_PATH) else None
    if poly_lb:
        dashboard["poly_cumulative_rankings"] = poly_lb.get("rankings", [])
        dashboard["poly_live_sprint_rankings"] = poly_lb.get("live_sprint_rankings", [])
        dashboard["poly_total_sprints"]       = poly_lb.get("total_sprints", 0)
    else:
        dashboard["poly_cumulative_rankings"] = []
        dashboard["poly_live_sprint_rankings"] = []
        dashboard["poly_total_sprints"]       = 0
    dashboard["arb_cycle_state"]   = get_arb_cycle_state()

    dashboard["cycle_state"] = get_cycle_state()

    dashboard["cycle_state"] = get_cycle_state()

    dashboard["cycle_state"] = get_cycle_state()

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(dashboard, f, indent=2)
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}] dashboard.json written")


if __name__ == "__main__":
    build()
