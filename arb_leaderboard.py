#!/usr/bin/env python3
"""
arb_leaderboard.py - Cumulative leaderboard for the stat arb competition.

Usage:
  python3 arb_leaderboard.py           # print leaderboard table
  python3 arb_leaderboard.py --json    # also write arb_leaderboard.json
  python3 arb_leaderboard.py --no-live # exclude active sprint from rankings
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESULTS_DIR  = os.path.join(WORKSPACE, "competition", "arb", "results")
ACTIVE_DIR   = os.path.join(WORKSPACE, "competition", "arb", "active")
LB_PATH      = os.path.join(WORKSPACE, "competition", "arb", "arb_leaderboard.json")
CYCLE_STATE  = os.path.join(WORKSPACE, "competition", "arb", "arb_cycle_state.json")
STATS_PATH   = os.path.join(WORKSPACE, "competition", "arb", "pair_stats.json")
FLEET_DIR    = os.path.join(WORKSPACE, "fleet", "arb")

POINTS_MAP       = {1: 8, 2: 5, 3: 3}
DISPLAY_CAPITAL  = 1000.0


def load_cycle_state():
    try:
        with open(CYCLE_STATE) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


def load_pair_stats():
    try:
        with open(STATS_PATH) as f:
            return json.load(f).get("pairs", {})
    except Exception:
        return {}


def load_strategy(bot_name):
    import yaml
    path = os.path.join(FLEET_DIR, bot_name, "strategy.yaml")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_archived_sprints():
    sprints = []
    if not os.path.isdir(RESULTS_DIR):
        return sprints
    for entry in sorted(os.listdir(RESULTS_DIR)):
        score_path = os.path.join(RESULTS_DIR, entry, "final_score.json")
        if not os.path.isfile(score_path):
            continue
        with open(score_path) as f:
            data = json.load(f)
        sprints.append(data)
    return sprints


def load_active_sprint():
    if not os.path.isdir(ACTIVE_DIR):
        return None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None
    comp_dir  = os.path.join(ACTIVE_DIR, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None
    with open(meta_path) as f:
        meta = json.load(f)
    if meta.get("status") != "active":
        return None

    starting_capital = meta.get("starting_capital", DISPLAY_CAPITAL)
    usd_scale = DISPLAY_CAPITAL / starting_capital
    pair_stats = load_pair_stats()

    rankings = []
    for fname in sorted(os.listdir(comp_dir)):
        if not fname.startswith("portfolio-"):
            continue
        with open(os.path.join(comp_dir, fname)) as f:
            p = json.load(f)

        # Mark open positions to market
        equity = p["equity"]
        bot    = p["bot"]
        s_yaml = load_strategy(bot)
        if s_yaml and pair_stats:
            key = f"{s_yaml['pair_a']}/{s_yaml['pair_b']}"
            stats = pair_stats.get(key, {})
            current_ratio = stats.get("current_ratio")
            for pos in p.get("positions", []):
                if current_ratio:
                    entry_ratio = pos["entry_ratio"]
                    dm = 1.0 if pos["direction"] == "long" else -1.0
                    ratio_change = (current_ratio - entry_ratio) / entry_ratio if entry_ratio else 0
                    unrealized = (pos["size_usd"] / 2) * dm * ratio_change
                    equity = round(equity + unrealized, 2)

        s = p["stats"]
        rankings.append({
            "bot":           bot,
            "final_equity":  round(equity * usd_scale, 2),
            "total_pnl_usd": round(s["total_pnl_usd"] * usd_scale, 2),
            "total_pnl_pct": round(s.get("total_pnl_pct", 0.0), 4),
            "total_trades":  s["total_trades"],
            "wins":          s["wins"],
            "losses":        s["losses"],
            "win_rate":      s["win_rate"],
            "open_positions": len(p.get("positions", [])),
        })

    rankings.sort(key=lambda x: x["final_equity"], reverse=True)
    for i, r in enumerate(rankings, 1):
        r["rank"] = i

    started_at = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    ends_at    = started_at + timedelta(hours=meta["duration_hours"])
    now        = datetime.now(timezone.utc)

    return {
        "comp_id":           entries[-1],
        "league":            "arb",
        "duration_hours":    meta["duration_hours"],
        "started_at":        meta["started_at"],
        "starting_capital":  starting_capital,
        "pairs":             meta.get("pairs", []),
        "rankings":          rankings,
        "seconds_remaining": max(0, int((ends_at - now).total_seconds())),
    }


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate(sprints):
    bots = {}
    for sprint in sprints:
        ranked = sorted(sprint["rankings"], key=lambda x: x["final_equity"], reverse=True)
        sc = DISPLAY_CAPITAL / sprint.get("starting_capital", DISPLAY_CAPITAL)
        for i, r in enumerate(ranked):
            b = r["bot"]
            pts = POINTS_MAP.get(i + 1, 1)
            if b not in bots:
                bots[b] = {
                    "bot":                  b,
                    "points":               0,
                    "sprints_entered":      0,
                    "sprint_wins":          0,
                    "podiums":              0,
                    "cumulative_pnl_usd":   0.0,
                    "total_trades":         0,
                    "total_wins":           0,
                    "overall_win_rate":     0.0,
                    "avg_pnl_pct_per_sprint": 0.0,
                    "style":                "stat arb",
                }
            e = bots[b]
            e["points"]            += pts
            e["sprints_entered"]   += 1
            e["cumulative_pnl_usd"] = round(e["cumulative_pnl_usd"] + r["total_pnl_usd"] * sc, 2)
            e["total_trades"]      += r["total_trades"]
            e["total_wins"]        += r["wins"]
            if i == 0:
                e["sprint_wins"] += 1
            if i < 3:
                e["podiums"] += 1

    for b in bots.values():
        t = b["total_trades"]
        b["overall_win_rate"] = round(b["total_wins"] / t * 100, 1) if t > 0 else 0.0
        n = b["sprints_entered"]
        b["avg_pnl_pct_per_sprint"] = round(
            b["cumulative_pnl_usd"] / DISPLAY_CAPITAL / n * 100, 4) if n > 0 else 0.0

    return bots


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_leaderboard(bots, active_sprint=None):
    ranked = sorted(bots.values(), key=lambda x: x["cumulative_pnl_usd"], reverse=True)
    print(f"\n{'BOT':<14} {'PTS':>4} {'SPRINTS':>7} {'CUM P&L':>10} {'AVG%':>8} {'WIN%':>6} {'TRADES':>6}")
    print("-" * 62)
    for b in ranked:
        print(f"{b['bot']:<14} {b['points']:>4}  {b['sprints_entered']:>6}  "
              f"{b['cumulative_pnl_usd']:>+9.2f}  {b['avg_pnl_pct_per_sprint']:>+7.2f}%  "
              f"{b['overall_win_rate']:>5.1f}%  {b['total_trades']:>5}")
    if active_sprint:
        print(f"\nLive: {active_sprint['comp_id']}  "
              f"{active_sprint['seconds_remaining']//3600}h left")


def main():
    parser = argparse.ArgumentParser(description="Arb leaderboard")
    parser.add_argument("--json",    action="store_true")
    parser.add_argument("--no-live", action="store_true", dest="no_live")
    args = parser.parse_args()

    archived = load_archived_sprints()
    active   = load_active_sprint()

    all_sprints = archived[:]
    if active and not args.no_live:
        all_sprints.append(active)

    bots = aggregate(all_sprints)
    print_leaderboard(bots, active_sprint=active if not args.no_live else None)

    if args.json:
        ranked = sorted(bots.values(), key=lambda x: x["cumulative_pnl_usd"], reverse=True)
        cycle_st = load_cycle_state()
        out = {
            "generated_at":      datetime.now(timezone.utc).isoformat(),
            "league":            "arb",
            "total_sprints":     len(all_sprints),
            "archived":          len(archived),
            "active_sprint":     active["comp_id"] if active else None,
            "cycle":             cycle_st.get("cycle", 1),
            "sprint_in_cycle":   cycle_st.get("sprint_in_cycle", 0),
            "sprints_per_cycle": cycle_st.get("sprints_per_cycle", 4),
            "cycle_status":      cycle_st.get("status", "active"),
            "rankings":          ranked,
        }
        with open(LB_PATH, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\n  Saved → {LB_PATH}")


if __name__ == "__main__":
    main()
