#!/usr/bin/env python3
"""
polymarket_leaderboard.py — Unified cumulative leaderboard for all 38 Polymarket bots.

Merges copy-trader (state.json) and autonomous (auto_state.json) results across sprints.
Points: 1st=8, 2nd=5, 3rd=3, 4th+=1 (same as other leagues).

Usage:
  python3 polymarket_leaderboard.py         # print leaderboard to stdout
  python3 polymarket_leaderboard.py --json  # write polymarket_leaderboard.json
"""
import os, sys, json, argparse
from datetime import datetime, timezone

WORKSPACE   = "/root/.openclaw/workspace"
POLY_DIR    = os.path.join(WORKSPACE, "competition", "polymarket")
STATE_FILE  = os.path.join(POLY_DIR, "state.json")
AUTO_STATE  = os.path.join(POLY_DIR, "auto_state.json")
SPRINT_DIR  = os.path.join(POLY_DIR, "sprint_results")
LB_PATH     = os.path.join(POLY_DIR, "polymarket_leaderboard.json")
CYCLE_FILE  = os.path.join(POLY_DIR, "polymarket_cycle_state.json")

POINTS_MAP     = {1: 8, 2: 5, 3: 3}
DEFAULT_POINTS = 1
STARTING_CAPITAL = 1000.0


def load_cycle_state():
    try:
        with open(CYCLE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


def load_completed_sprints():
    """
    Read completed sprint results from sprint_results/.
    Each sprint has a _copy.json and/or _auto.json file.
    Returns list of merged sprint dicts with 'bots' list.
    """
    if not os.path.isdir(SPRINT_DIR):
        return []

    # Group files by base sprint_id (strip _copy / _auto suffix)
    groups = {}
    for fname in sorted(os.listdir(SPRINT_DIR)):
        if not fname.endswith(".json"):
            continue
        base = fname.replace("_copy.json", "").replace("_auto.json", "").replace(".json", "")
        groups.setdefault(base, []).append(os.path.join(SPRINT_DIR, fname))

    sprints = []
    for sprint_id in sorted(groups.keys()):
        bots = []
        started_at = None
        ended_at = None
        for fpath in groups[sprint_id]:
            try:
                with open(fpath) as f:
                    data = json.load(f)
            except Exception:
                continue
            if not started_at:
                started_at = data.get("started_at")
            if not ended_at:
                ended_at = data.get("ended_at")
            bots.extend(data.get("bots", []))
        if bots:
            sprints.append({
                "sprint_id":  sprint_id,
                "started_at": started_at,
                "ended_at":   ended_at,
                "bots":       bots,
            })
    return sprints


def get_live_bots():
    """Read current sprint P&L directly from both state files."""
    bots = []

    # Copy-trader bots
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
        sprint_id = state.get("sprint_id", "")
        for b in state.get("bots", []):
            sp_pnl = b.get("sprint_pnl_usd", b.get("pnl_usd", 0.0))
            sp_trades = b.get("sprint_trades", 0)
            sp_wins = b.get("sprint_wins", 0)
            bots.append({
                "bot":             b["name"],
                "type":            "copy",
                "username":        b.get("trader", ""),
                "sprint_id":       sprint_id,
                "sprint_pnl_usd":  round(sp_pnl, 4),
                "sprint_pnl_pct":  round((sp_pnl / STARTING_CAPITAL) * 100, 2),
                "sprint_trades":   sp_trades,
                "sprint_wins":     sp_wins,
                "win_rate":        round(sp_wins / sp_trades * 100, 1) if sp_trades > 0 else 0.0,
                "active_positions": len(b.get("positions", {})),
            })
    except Exception:
        pass

    # Autonomous bots
    try:
        with open(AUTO_STATE) as f:
            state = json.load(f)
        sprint_id = state.get("sprint_id", "")
        for b in state.get("bots", []):
            pnl = b.get("pnl_usd", 0.0)
            trades = b.get("total_trades", 0)
            wins = b.get("wins", 0)
            bots.append({
                "bot":             b["name"],
                "type":            b.get("category", "auto"),
                "username":        "",
                "sprint_id":       sprint_id,
                "sprint_pnl_usd":  round(pnl, 4),
                "sprint_pnl_pct":  round(b.get("pnl_pct", 0.0), 2),
                "sprint_trades":   trades,
                "sprint_wins":     wins,
                "win_rate":        round(wins / trades * 100, 1) if trades > 0 else 0.0,
                "active_positions": len(b.get("positions", {})),
            })
    except Exception:
        pass

    return bots


def score_sprint(bots_list):
    """Rank bots by sprint_pnl_usd, assign points. Returns new list."""
    ranked = sorted(bots_list, key=lambda x: x.get("sprint_pnl_usd", 0.0), reverse=True)
    for i, b in enumerate(ranked):
        b["rank"]   = i + 1
        b["points"] = POINTS_MAP.get(i + 1, DEFAULT_POINTS)
    return ranked


def aggregate(completed_sprints, live_bots):
    """
    Build cumulative standings across completed sprints.
    Live sprint data is included as 0 pts (in-progress), just for showing current pnl.
    """
    tally = {}

    def ensure(name, type_, username):
        if name not in tally:
            tally[name] = {
                "bot":               name,
                "type":              type_,
                "username":          username,
                "sprints_entered":   0,
                "sprint_wins":       0,
                "podiums":           0,
                "points":            0,
                "cumulative_pnl_usd": 0.0,
                "total_trades":      0,
                "total_wins":        0,
            }
        # Update type/username if we have better info
        if type_ and type_ != "auto":
            tally[name]["type"] = type_
        if username:
            tally[name]["username"] = username
        return tally[name]

    for sprint in completed_sprints:
        # Skip dead sprints (unrecoverable or aborted) — zero activity = no points awarded
        if sum(b.get("sprint_trades", 0) for b in sprint["bots"]) == 0:
            continue
        ranked = score_sprint(sprint["bots"])
        for b in ranked:
            name = b.get("bot", "")
            t = ensure(name, b.get("type", "auto"), b.get("username", ""))
            t["sprints_entered"]   += 1
            t["points"]            += b["points"]
            t["cumulative_pnl_usd"] = round(t["cumulative_pnl_usd"] + b.get("sprint_pnl_usd", 0.0), 2)
            t["total_trades"]      += b.get("sprint_trades", 0)
            t["total_wins"]        += b.get("sprint_wins", 0)
            rank = b["rank"]
            if rank == 1:
                t["sprint_wins"] += 1
            if rank <= 3:
                t["podiums"] += 1

    # Include live sprint P&L in cumulative totals (no points until sprint ends)
    for b in live_bots:
        t = ensure(b["bot"], b.get("type", "auto"), b.get("username", ""))
        t["cumulative_pnl_usd"] = round(t["cumulative_pnl_usd"] + b.get("sprint_pnl_usd", 0.0), 2)
        t["total_trades"] += b.get("sprint_trades", 0)
        t["total_wins"]   += b.get("sprint_wins", 0)

    # Compute derived fields
    result = []
    for t in tally.values():
        tr = t["total_trades"]
        t["overall_win_rate"] = round(t["total_wins"] / tr * 100, 1) if tr > 0 else 0.0
        result.append(t)

    # Sort by cumulative_pnl_usd desc, then points as tiebreaker
    result.sort(key=lambda x: (x["cumulative_pnl_usd"], x["points"]), reverse=True)
    for i, r in enumerate(result):
        r["rank"] = i + 1

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Write leaderboard.json")
    args = parser.parse_args()

    cs        = load_cycle_state()
    completed = load_completed_sprints()
    live      = get_live_bots()
    rankings  = aggregate(completed, live)
    live_ranked = score_sprint(list(live)) if live else []

    # Determine active sprint id (prefer copy state, fall back to auto)
    active_id = None
    if live:
        ids = [b["sprint_id"] for b in live if b["sprint_id"]]
        if ids:
            active_id = ids[0]

    output = {
        "generated_at":       datetime.now(timezone.utc).isoformat(),
        "total_sprints":      len(completed) + (1 if active_id else 0),
        "cycle":              cs.get("cycle", 1),
        "sprint_in_cycle":    cs.get("sprint_in_cycle", 0),
        "sprints_per_cycle":  cs.get("sprints_per_cycle", 4),
        "active_sprint":      active_id,
        "rankings":           rankings,
        "live_sprint_rankings": live_ranked,
    }

    if args.json:
        os.makedirs(os.path.dirname(LB_PATH), exist_ok=True)
        tmp = LB_PATH + ".tmp"
        with open(tmp, "w") as f:
            json.dump(output, f, indent=2)
        os.replace(tmp, LB_PATH)
        print(f"Written {len(rankings)} bots to {LB_PATH}")
    else:
        cycle = cs.get("cycle", 1)
        print(f"\nPolymarket Leaderboard — Cycle #{cycle} — {len(completed)} completed sprint(s)\n")
        print(f"  {'#':>3}  {'Bot':<12}  {'Type':<12}  {'Pts':>4}  {'Sp':>3}  {'1st':>3}  {'Pod':>3}  {'Cum P&L':>9}  {'Win%':>5}  {'Trades':>6}")
        print("  " + "-" * 72)
        for r in rankings:
            wr = f"{r['overall_win_rate']:.0f}%" if r['total_trades'] > 0 else "—"
            print(f"  #{r['rank']:>2}  {r['bot']:<12}  {r['type']:<12}  {r['points']:>4}  "
                  f"{r['sprints_entered']:>3}  {r['sprint_wins']:>3}  {r['podiums']:>3}  "
                  f"${r['cumulative_pnl_usd']:>+8.2f}  {wr:>5}  {r['total_trades']:>6}")


if __name__ == "__main__":
    main()
