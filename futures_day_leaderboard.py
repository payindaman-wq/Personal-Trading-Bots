#!/usr/bin/env python3
"""
futures_day_leaderboard.py - Cumulative leaderboard for Futures Day league.
"""
import os, sys, json, argparse
from datetime import datetime, timezone

WORKSPACE   = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESULTS_DIR = os.path.join(WORKSPACE, "competition", "futures_day", "results")
ACTIVE_DIR  = os.path.join(WORKSPACE, "competition", "futures_day", "active")
LB_PATH     = os.path.join(WORKSPACE, "competition", "futures_day", "futures_day_leaderboard.json")
CYCLE_STATE = os.path.join(WORKSPACE, "competition", "futures_day", "cycle_state.json")

POINTS_MAP      = {1: 8, 2: 5, 3: 3}
DISPLAY_CAPITAL = 1000.0


def load_cycle_state():
    try:
        with open(CYCLE_STATE) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 7, "status": "active"}


def _portfolio_equity(p):
    return p.get("cash", 0) + sum(pos.get("cost_basis", 0) for pos in p.get("positions", []))


def _rankings_from_dir(comp_dir):
    rankings = []
    if not os.path.isdir(comp_dir):
        return rankings
    for fname in sorted(os.listdir(comp_dir)):
        if not fname.startswith("portfolio-"):
            continue
        try:
            with open(os.path.join(comp_dir, fname)) as f:
                p = json.load(f)
        except Exception:
            continue
        eq    = _portfolio_equity(p)
        s     = p.get("stats", {})
        start = p.get("starting_capital", DISPLAY_CAPITAL)
        scale = DISPLAY_CAPITAL / start if start else 1.0
        rankings.append({
            "bot":              p.get("bot", fname.replace("portfolio-", "").replace(".json", "")),
            "final_equity":     round(eq * scale, 2),
            "total_pnl_usd":    round(s.get("total_pnl_usd", 0) * scale, 2),
            "total_pnl_pct":    round(s.get("total_pnl_pct", 0), 4),
            "total_trades":     s.get("total_trades", 0),
            "wins":             s.get("wins", 0),
            "losses":           s.get("losses", 0),
            "win_rate":         s.get("win_rate", 0),
            "max_drawdown_pct": s.get("max_drawdown_pct", 0),
            "open_positions":   len(p.get("positions", [])),
            "rank":             None,
        })
    rankings.sort(key=lambda x: x["final_equity"], reverse=True)
    for i, r in enumerate(rankings, 1):
        r["rank"] = i
    return rankings


def load_archived_sprints():
    sprints = []
    if not os.path.isdir(RESULTS_DIR):
        return sprints
    for entry in sorted(os.listdir(RESULTS_DIR)):
        entry_path = os.path.join(RESULTS_DIR, entry)
        if not os.path.isdir(entry_path):
            continue
        score_path = os.path.join(RESULTS_DIR, f"{entry}_score.json")
        meta_path  = os.path.join(entry_path, "meta.json")
        meta = {}
        if os.path.isfile(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
        start_cap = meta.get("starting_capital", DISPLAY_CAPITAL)

        if os.path.isfile(score_path):
            with open(score_path) as f:
                sd = json.load(f)
            scale = DISPLAY_CAPITAL / start_cap if start_cap else 1.0
            rankings = []
            for i, sc in enumerate(sd.get("scores", []), 1):
                eq = sc.get("final_equity", start_cap)
                rankings.append({
                    "bot":              sc["bot"],
                    "rank":             i,
                    "final_equity":     round(eq * scale, 2),
                    "total_pnl_usd":    round((eq - start_cap) * scale, 2),
                    "total_pnl_pct":    round(sc.get("total_pnl_pct", 0), 4),
                    "total_trades":     sc.get("total_trades", 0),
                    "wins":             0,
                    "losses":           0,
                    "win_rate":         sc.get("win_rate", 0),
                    "max_drawdown_pct": 0,
                    "open_positions":   0,
                })
            sprints.append({
                "comp_id": entry, "scored_at": sd.get("ended_at", ""),
                "duration_hours": sd.get("duration_hours", 24),
                "pairs": meta.get("pairs", []), "winner": sd.get("winner"),
                "rankings": rankings, "starting_capital": start_cap, "in_progress": False,
            })
        else:
            if meta.get("status") == "active":
                continue
            rankings = _rankings_from_dir(entry_path)
            if not rankings:
                continue
            sprints.append({
                "comp_id": entry, "scored_at": meta.get("ended_at", meta.get("started_at", "")),
                "duration_hours": meta.get("duration_hours", 24),
                "pairs": meta.get("pairs", []),
                "winner": rankings[0]["bot"] if rankings else None,
                "rankings": rankings, "starting_capital": start_cap, "in_progress": False,
            })
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
    rankings = _rankings_from_dir(comp_dir)
    return {
        "comp_id": meta["comp_id"], "scored_at": None,
        "duration_hours": meta["duration_hours"], "pairs": meta.get("pairs", []),
        "winner": rankings[0]["bot"] if rankings else None,
        "rankings": rankings, "starting_capital": meta.get("starting_capital", DISPLAY_CAPITAL),
        "in_progress": True,
    }


def aggregate(sprints):
    bots = {}
    def ensure(name):
        if name not in bots:
            bots[name] = {
                "bot": name, "sprints_entered": 0, "sprint_wins": 0, "podiums": 0,
                "points": 0, "cumulative_pnl_usd": 0.0, "cumulative_pnl_pct": 0.0,
                "total_trades": 0, "total_wins": 0, "total_losses": 0,
                "best_sprint_pnl_pct": None, "worst_sprint_pnl_pct": None,
                "sprint_log": [],
            }
        return bots[name]
    for sprint in sprints:
        in_prog = sprint.get("in_progress", False)
        comp_id = sprint["comp_id"]
        for r in sprint.get("rankings", []):
            b = ensure(r["bot"])
            b["sprints_entered"] += 1
            rank = r.get("rank", 99)
            if not in_prog:
                b["points"] += POINTS_MAP.get(rank, 1)
                if rank == 1: b["sprint_wins"] += 1
                if rank <= 3: b["podiums"]     += 1
            pnl_usd = r.get("total_pnl_usd", 0.0)
            pnl_pct = r.get("total_pnl_pct", 0.0)
            b["cumulative_pnl_usd"]  = round(b["cumulative_pnl_usd"] + pnl_usd, 2)
            b["cumulative_pnl_pct"]  = round(b["cumulative_pnl_pct"] + pnl_pct, 4)
            b["total_trades"]        += r.get("total_trades", 0)
            b["total_wins"]          += r.get("wins", 0)
            b["total_losses"]        += r.get("losses", 0)
            if b["best_sprint_pnl_pct"] is None or pnl_pct > b["best_sprint_pnl_pct"]:
                b["best_sprint_pnl_pct"] = round(pnl_pct, 4)
            if b["worst_sprint_pnl_pct"] is None or pnl_pct < b["worst_sprint_pnl_pct"]:
                b["worst_sprint_pnl_pct"] = round(pnl_pct, 4)
            b["sprint_log"].append({
                "comp_id": comp_id, "rank": rank, "pnl_usd": round(pnl_usd, 2),
                "pnl_pct": round(pnl_pct, 4), "trades": r.get("total_trades", 0),
                "win_rate": r.get("win_rate", 0), "in_progress": in_prog,
            })
    for b in bots.values():
        t = b["total_trades"]
        b["overall_win_rate"]       = round(b["total_wins"] / t * 100, 1) if t > 0 else 0.0
        n = b["sprints_entered"]
        b["avg_pnl_pct_per_sprint"] = round(b["cumulative_pnl_pct"] / n, 4) if n > 0 else 0.0
    return bots


def main():
    parser = argparse.ArgumentParser(description="Futures Day leaderboard")
    parser.add_argument("--json",    action="store_true")
    parser.add_argument("--no-live", action="store_true")
    args = parser.parse_args()

    archived = load_archived_sprints()
    active   = load_active_sprint()
    all_sprints = archived[:]
    if active and not args.no_live:
        all_sprints.append(active)

    bots   = aggregate(all_sprints)
    ranked = sorted(bots.values(), key=lambda x: x["cumulative_pnl_usd"], reverse=True)
    cycle  = load_cycle_state()
    now    = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"\n{'='*72}")
    print(f"  FUTURES DAY LEAGUE LEADERBOARD  --  {now}")
    print(f"  Cycle {cycle.get('cycle',1)} | Sprint {cycle.get('sprint_in_cycle',0)}/{cycle.get('sprints_per_cycle',7)}")
    if active:
        print(f"  Active: {active['comp_id']}  (live included)")
    print(f"{'='*72}")
    print(f"  {'#':<4} {'BOT':<22} {'PTS':>4} {'SPRINTS':>7} {'1ST':>4} {'CUM PNL':>11} {'WIN%':>6} {'TRADES':>7}")
    print("  " + "-" * 68)
    for i, b in enumerate(ranked, 1):
        sgn = "+" if b["cumulative_pnl_usd"] >= 0 else ""
        print(f"  {i:<4} {b['bot']:<22} {b['points']:>4} {b['sprints_entered']:>7} "
              f"{b['sprint_wins']:>4} {sgn}${b['cumulative_pnl_usd']:>9,.2f} "
              f"{b['overall_win_rate']:>5.1f}% {b['total_trades']:>7}")

    if active and active.get("rankings"):
        print(f"\n  -- LIVE SPRINT: {active['comp_id']} --")
        for r in active["rankings"]:
            sgn = "+" if r["total_pnl_usd"] >= 0 else ""
            print(f"  #{r['rank']:<3} {r['bot']:<22} ${r['final_equity']:>8,.2f}  "
                  f"{sgn}${r['total_pnl_usd']:>8,.2f}  trades:{r['total_trades']}")
    print()

    if args.json:
        out = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "league": "futures_day",
            "total_sprints": len(all_sprints),
            "archived": len(archived),
            "active_sprint": active["comp_id"] if active else None,
            "cycle": cycle.get("cycle", 1),
            "sprint_in_cycle": cycle.get("sprint_in_cycle", 0),
            "sprints_per_cycle": cycle.get("sprints_per_cycle", 7),
            "cycle_status": cycle.get("status", "active"),
            "rankings": ranked,
        }
        os.makedirs(os.path.dirname(LB_PATH), exist_ok=True)
        with open(LB_PATH, "w") as f:
            json.dump(out, f, indent=2)
        print(f"  Saved to {LB_PATH}")


if __name__ == "__main__":
    main()
