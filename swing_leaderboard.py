#!/usr/bin/env python3
"""
swing_leaderboard.py - Cumulative leaderboard for swing trading competition.

Usage:
  python3 swing_leaderboard.py              # print leaderboard
  python3 swing_leaderboard.py --json       # also dump swing_leaderboard.json
  python3 swing_leaderboard.py --sprint ID  # detail for one sprint
  python3 swing_leaderboard.py --no-live    # exclude active sprint
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESULTS_DIR  = os.path.join(WORKSPACE, "competition", "swing", "results")
ACTIVE_DIR   = os.path.join(WORKSPACE, "competition", "swing", "active")
LB_PATH      = os.path.join(WORKSPACE, "competition", "swing", "swing_leaderboard.json")

POINTS_MAP = {1: 8, 2: 5, 3: 3}

DISPLAY_CAPITAL = 1000.0


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_archived_sprints():
    sprints = []
    if not os.path.isdir(RESULTS_DIR):
        return sprints
    for entry in sorted(os.listdir(RESULTS_DIR)):
        score_path = os.path.join(RESULTS_DIR, entry, "final_score.json")
        meta_path  = os.path.join(RESULTS_DIR, entry, "meta.json")
        if not os.path.isfile(score_path):
            continue
        with open(score_path) as f:
            data = json.load(f)
        if os.path.isfile(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            data["starting_capital"] = meta.get("starting_capital", 10000.0)
        else:
            data["starting_capital"] = 10000.0
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

    starting_capital = meta.get("starting_capital", 10000.0)
    usd_scale = DISPLAY_CAPITAL / starting_capital

    rankings = []
    for bot in meta.get("bots", []):
        pfile = os.path.join(comp_dir, f"portfolio-{bot}.json")
        if not os.path.isfile(pfile):
            continue
        with open(pfile) as f:
            p = json.load(f)
        s = p["stats"]
        rankings.append({
            "bot":              bot,
            "final_equity":     round(p["equity"] * usd_scale, 2),
            "total_pnl_usd":    round(s["total_pnl_usd"] * usd_scale, 2),
            "total_pnl_pct":    round(s["total_pnl_pct"], 4),
            "total_trades":     s["total_trades"],
            "wins":             s["wins"],
            "losses":           s["losses"],
            "win_rate":         s["win_rate"],
            "max_drawdown_pct": s["max_drawdown_pct"],
            "total_fees":       round(s["total_fees"] * usd_scale, 4),
            "open_positions":   len(p.get("positions", [])),
            "rank":             None,
        })

    rankings.sort(key=lambda x: x["final_equity"], reverse=True)
    for i, r in enumerate(rankings, 1):
        r["rank"] = i

    return {
        "comp_id":        meta["comp_id"],
        "scored_at":      None,
        "duration_hours": meta["duration_hours"],
        "pairs":          meta["pairs"],
        "winner":         rankings[0]["bot"] if rankings else None,
        "rankings":       rankings,
        "in_progress":    True,
    }


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate(sprints):
    bots = {}

    def ensure(name):
        if name not in bots:
            bots[name] = {
                "bot":                   name,
                "sprints_entered":       0,
                "sprint_wins":           0,
                "podiums":               0,
                "points":                0,
                "cumulative_pnl_usd":    0.0,
                "cumulative_pnl_pct":    0.0,
                "total_trades":          0,
                "total_wins":            0,
                "total_losses":          0,
                "total_fees_usd":        0.0,
                "worst_drawdown_pct":    0.0,
                "best_sprint_pnl_pct":   None,
                "worst_sprint_pnl_pct":  None,
                "sprint_log":            [],
            }
        return bots[name]

    for sprint in sprints:
        in_prog   = sprint.get("in_progress", False)
        comp_id   = sprint["comp_id"]
        usd_scale = DISPLAY_CAPITAL / sprint.get("starting_capital", DISPLAY_CAPITAL)
        for r in sprint.get("rankings", []):
            name = r["bot"]
            b    = ensure(name)
            b["sprints_entered"] += 1
            rank = r.get("rank", 99)
            b["points"] += POINTS_MAP.get(rank, 1)
            if rank == 1: b["sprint_wins"] += 1
            if rank <= 3: b["podiums"]     += 1
            pnl_usd = round(r.get("total_pnl_usd", 0.0) * usd_scale, 2)
            pnl_pct = r.get("total_pnl_pct", 0.0)
            b["cumulative_pnl_usd"] = round(b["cumulative_pnl_usd"] + pnl_usd, 2)
            b["cumulative_pnl_pct"] = round(b["cumulative_pnl_pct"] + pnl_pct, 4)
            b["total_trades"]       += r.get("total_trades", 0)
            b["total_wins"]         += r.get("wins", 0)
            b["total_losses"]       += r.get("losses", 0)
            b["total_fees_usd"]      = round(b["total_fees_usd"] + r.get("total_fees", 0.0) * usd_scale, 4)
            dd = r.get("max_drawdown_pct", 0.0)
            if dd > b["worst_drawdown_pct"]:
                b["worst_drawdown_pct"] = dd
            if b["best_sprint_pnl_pct"] is None or pnl_pct > b["best_sprint_pnl_pct"]:
                b["best_sprint_pnl_pct"] = round(pnl_pct, 4)
            if b["worst_sprint_pnl_pct"] is None or pnl_pct < b["worst_sprint_pnl_pct"]:
                b["worst_sprint_pnl_pct"] = round(pnl_pct, 4)
            b["sprint_log"].append({
                "comp_id":     comp_id,
                "rank":        rank,
                "pnl_usd":     round(pnl_usd, 2),
                "pnl_pct":     round(pnl_pct, 4),
                "trades":      r.get("total_trades", 0),
                "win_rate":    r.get("win_rate", 0.0),
                "in_progress": in_prog,
            })

    for b in bots.values():
        t = b["total_trades"]
        b["overall_win_rate"]       = round(b["total_wins"] / t * 100, 1) if t > 0 else 0.0
        n = b["sprints_entered"]
        b["avg_pnl_pct_per_sprint"] = round(b["cumulative_pnl_pct"] / n, 4) if n > 0 else 0.0

    return bots


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

RANK_ICONS = {1: "1.", 2: "2.", 3: "3."}

def fmt_pnl(val, width=10):
    s = f"{'+'if val >= 0 else ''}${val:,.2f}"
    return s.rjust(width)

def fmt_pct(val, width=8):
    s = f"{'+'if val >= 0 else ''}{val:.2f}%"
    return s.rjust(width)


def print_leaderboard(bots_dict, active_sprint=None):
    ranked = sorted(bots_dict.values(),
                    key=lambda x: x["cumulative_pnl_usd"], reverse=True)
    now     = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    divider = "=" * 78

    print()
    print(divider)
    print(f"  VIKING FLEET — SWING LEAGUE LEADERBOARD  --  {now}")
    if active_sprint:
        print(f"  Active sprint : {active_sprint['comp_id']}  (live data included)")
    print(divider)
    print(f"  {'#':<4} {'BOT':<12} {'PTS':>4} {'SPRINTS':>8} {'1ST':>4} {'TOP3':>5} "
          f"{'CUM PNL':>11} {'AVG/SPRINT':>11} {'WIN%':>6} {'TRADES':>7}")
    print("  " + "-" * 74)

    for i, b in enumerate(ranked, 1):
        icon    = RANK_ICONS.get(i, f"{i}.")
        pnl_str = fmt_pnl(b["cumulative_pnl_usd"], 11)
        avg_str = fmt_pct(b["avg_pnl_pct_per_sprint"], 11)
        print(f"  {icon:<4} {b['bot']:<12} {b['points']:>4} "
              f"{b['sprints_entered']:>8} {b['sprint_wins']:>4} {b['podiums']:>5} "
              f"{pnl_str} {avg_str} {b['overall_win_rate']:>5.1f}% {b['total_trades']:>7}")

    print("  " + "-" * 74)
    print("  Ranked by cumulative P&L.  7-day sprints.")
    print("  PTS: 1st=8 | 2nd=5 | 3rd=3 | 4th-8th=1")
    print()

    if active_sprint and active_sprint.get("rankings"):
        print(f"  -- LIVE SPRINT: {active_sprint['comp_id']} --")
        print(f"  {'RANK':<6} {'BOT':<12} {'EQUITY':>10} {'PNL':>11} "
              f"{'TRADES':>7} {'WIN%':>6} {'OPEN':>5}")
        print("  " + "-" * 60)
        for r in active_sprint["rankings"]:
            pnl_str  = fmt_pnl(r["total_pnl_usd"], 11)
            open_pos = r.get("open_positions", 0)
            open_str = f"[{open_pos}]" if open_pos else "   -"
            print(f"  #{r['rank']:<5} {r['bot']:<12} ${r['final_equity']:>9,.2f} "
                  f"{pnl_str} {r['total_trades']:>7} {r['win_rate']:>5.1f}% {open_str:>5}")
        print()


def print_sprint_detail(sprint):
    comp_id = sprint["comp_id"]
    in_prog = sprint.get("in_progress", False)
    status  = "IN PROGRESS" if in_prog else f"FINAL  winner: {sprint.get('winner','?').upper()}"
    print()
    print(f"  Sprint: {comp_id}  [{status}]")
    print(f"  Duration: {sprint.get('duration_hours')}h  |  "
          f"Pairs: {', '.join(sprint.get('pairs', []))}")
    print(f"  {'RANK':<6} {'BOT':<12} {'EQUITY':>10} {'PNL':>11} "
          f"{'WIN%':>6} {'TRADES':>7} {'FEES':>8} {'MAX DD':>7}")
    print("  " + "-" * 70)
    for r in sprint.get("rankings", []):
        pnl_str = fmt_pnl(r["total_pnl_usd"], 11)
        icon    = RANK_ICONS.get(r["rank"], f"{r['rank']}.")
        print(f"  {icon:<6} {r['bot']:<12} ${r['final_equity']:>9,.2f} "
              f"{pnl_str} {r['win_rate']:>5.1f}% {r['total_trades']:>7} "
              f"${r['total_fees']:>6,.2f} {r['max_drawdown_pct']:>6.2f}%")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Viking Fleet swing leaderboard")
    parser.add_argument("--json",    action="store_true", help="Save swing_leaderboard.json")
    parser.add_argument("--sprint",  metavar="ID",        help="Detail for one sprint ID")
    parser.add_argument("--no-live", action="store_true", help="Exclude active sprint")
    args = parser.parse_args()

    archived = load_archived_sprints()
    active   = load_active_sprint()

    all_sprints = archived[:]
    if active and not args.no_live:
        all_sprints.append(active)

    if args.sprint:
        match = next((s for s in all_sprints if s["comp_id"] == args.sprint), None)
        if match:
            print_sprint_detail(match)
        else:
            ids = [s["comp_id"] for s in all_sprints]
            print(f"Sprint '{args.sprint}' not found. Available: {ids}")
        return

    bots = aggregate(all_sprints)
    print_leaderboard(bots, active_sprint=active if not args.no_live else None)

    if args.json:
        ranked = sorted(bots.values(),
                        key=lambda x: x["cumulative_pnl_usd"], reverse=True)
        out = {
            "generated_at":  datetime.now(timezone.utc).isoformat(),
            "league":        "swing",
            "total_sprints": len(all_sprints),
            "archived":      len(archived),
            "active_sprint": active["comp_id"] if active else None,
            "rankings":      ranked,
        }
        with open(LB_PATH, "w") as f:
            json.dump(out, f, indent=2)
        print(f"  Saved to {LB_PATH}")


if __name__ == "__main__":
    main()
