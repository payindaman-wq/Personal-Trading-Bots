#!/usr/bin/env python3
"""
polymarket_leaderboard.py — Unified cumulative leaderboard for all 38 Polymarket bots.

Merges copy-trader (state.json) and autonomous (auto_state.json) results across sprints.
Points: 1st=8, 2nd=5, 3rd=3, 4th+=1 (same as other leagues).

Usage:
  python3 polymarket_leaderboard.py         # print leaderboard to stdout
  python3 polymarket_leaderboard.py --json  # write polymarket_leaderboard.json
"""
import os, sys, json, argparse, re
from datetime import datetime, timezone

# Nevada TRO (2026-04-24): Kalshi blocks Sports, Elections, Entertainment for
# NV residents. We tag each trade by NV legality here so cumulative_pnl_usd
# (raw) and nv_legal_pnl_usd (NV-enforced) are both surfaced. Use nv_legal for
# funding decisions. Heuristic keyword classifier — biases toward over-blocking
# sports to avoid optimistic funding rankings. Mirrors nv_retro.py.
SPORTS_RE = re.compile("|".join([
    r"\bspread\b", r"\bmoneyline\b", r"\bover/under\b", r"\bo/u\b",
    r"\b\-?\d+\.5\)", r"\bhandicap\b", r"\b1h\b", r"\b2h\b", r"\bhalftime\b",
    r"\bfinal score\b", r"\bkick(-|\s)?off\b", r"\bpoints o/u\b",
    r"\bprop\b", r"\bprop bet\b", r"\brebounds o/u", r"\bassists o/u",
    r"\bstrikeouts?\b", r"\bwin by (ko|tko|submission|decision)\b",
    r"\bgoals?\b", r"\btouchdown", r"\bhomerun", r"\bhome run",
    r"\bwin on \d{4}-\d{2}-\d{2}\b", r"\bvs\.?\b", r"\bdefeat",
    r"\bnfl\b", r"\bnba\b", r"\bmlb\b", r"\bnhl\b", r"\bufc\b", r"\bmma\b",
    r"\bboxing\b", r"\bmls\b", r"\bepl\b", r"\bla liga\b", r"\bserie a\b",
    r"\bbundesliga\b", r"\bchampions league\b", r"\bworld cup\b",
    r"\beuro\s?20\d{2}\b", r"\bolympic", r"\bmasters\b",
    r"\bopen\b.{0,10}tennis", r"\bgrand slam\b", r"\bpga\b", r"\batp\b",
    r"\bwta\b", r"\bf1\b", r"\bformula 1\b", r"\bgrand prix\b",
    r"\bvalorant\b", r"\bcsgo\b", r"\bcs:go\b", r"\bdota\b",
    r"\bleague of legends\b", r"\bfc\b", r"\bunited\b.{0,10}fc",
    r"\bcity fc\b", r"\bcurrent fc\b",
    r"\blakers\b", r"\bceltics\b", r"\bwarriors\b", r"\bheat\b",
    r"\brockets\b", r"\bknicks\b", r"\bnets\b", r"\bbucks\b",
    r"\bthunder\b", r"\bnuggets\b", r"\byankees\b", r"\bdodgers\b",
    r"\bred sox\b", r"\bpatriots\b", r"\bchiefs\b", r"\beagles\b",
    r"\bcowboys\b", r"\b(red|blue) bulls\b",
    r"\bshai gilgeous", r"\bluka doncic", r"\blebron\b",
    r"\bkevin durant\b", r"\bstephen curry\b", r"\bgiannis\b",
    r"\bjokic\b", r"\bmahomes\b", r"\blamar jackson\b", r"\bjosh allen\b",
]), re.IGNORECASE)
ELECTIONS_RE = re.compile("|".join([
    r"\belection\b", r"\belectoral\b", r"\bpresidential\b", r"\bgovernor\b",
    r"\bsenator\b", r"\bsenate\b", r"\bhouse race\b", r"\bvote\b",
    r"\bcongress\b", r"\bmayor\b", r"\bnominee\b", r"\bprimary\b",
    r"\bdemocratic\b", r"\brepublican\b", r"\bapproval rating\b",
    r"\btrump\b", r"\bbiden\b", r"\bharris\b", r"\bvance\b",
    r"\bwhite house\b", r"\bimpeach", r"\bvice president\b",
    r"\bparliament\b", r"\bprime minister\b",
]), re.IGNORECASE)
ENTERTAINMENT_RE = re.compile("|".join([
    r"\boscar", r"\bgrammy", r"\bemmy", r"\btony award", r"\bgolden globe",
    r"\bbox office\b", r"\bopening weekend\b", r"\btaylor swift\b",
    r"\bkanye\b", r"\bkardashian\b", r"\bbeyonce\b", r"\bdrake\b",
    r"\bmovie\b", r"\bfilm\b", r"\balbum\b", r"\bbillboard\b",
    r"\bnetflix\b.{0,20}(show|series|movie)", r"\bhbo\b",
    r"\bsuperbowl halftime\b", r"\bmet gala\b",
]), re.IGNORECASE)


def is_nv_legal(title):
    t = title or ""
    if SPORTS_RE.search(t):       return False
    if ELECTIONS_RE.search(t):    return False
    if ENTERTAINMENT_RE.search(t): return False
    return True


WORKSPACE   = "/root/.openclaw/workspace"
POLY_DIR    = os.path.join(WORKSPACE, "competition", "polymarket")
STATE_FILE   = os.path.join(POLY_DIR, "kalshi_copy_state.json")
BACKFILL_FILE = os.path.join(POLY_DIR, "kalshi_copy_pm_backfill.json")
AUTO_STATE   = os.path.join(POLY_DIR, "auto_state.json")
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

    # Copy-trader bots (_k fleet) — merge live Kalshi state + historical PM backfill
    # for current sprint. Mirrors polymarket_data.py merge logic.
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
        backfill = {}
        try:
            with open(BACKFILL_FILE) as bf:
                backfill = json.load(bf).get("bots", {})
        except Exception:
            backfill = {}
        sprint_id = state.get("sprint_id", "")
        for b in state.get("bots", []):
            name  = b.get("name", "")
            bf_b  = backfill.get(name, {})
            pnl     = round(b.get("sprint_pnl_usd", 0.0) + bf_b.get("sprint_pnl_usd", 0.0), 4)
            # NV-legal split: walk closed_trades + backfill trades and sum only
            # the trades whose title passes is_nv_legal. Copy bots store titles
            # on each trade record (same shape as autonomous bots).
            closed_live   = b.get("closed_trades", []) or []
            closed_bf     = bf_b.get("closed_trades", []) or []
            nv_pnl = round(
                sum(t.get("pnl_usd", 0.0) for t in closed_live if isinstance(t, dict) and is_nv_legal(t.get("title", "")))
                + sum(t.get("pnl_usd", 0.0) for t in closed_bf if isinstance(t, dict) and is_nv_legal(t.get("title", ""))),
                4,
            )
            nv_trades = (
                sum(1 for t in closed_live if isinstance(t, dict) and is_nv_legal(t.get("title", "")))
                + sum(1 for t in closed_bf if isinstance(t, dict) and is_nv_legal(t.get("title", "")))
            )
            pnl_pct = round((pnl / STARTING_CAPITAL) * 100, 2)
            trades  = b.get("sprint_trades", 0) + bf_b.get("sprint_trades", 0)
            wins    = b.get("sprint_wins", 0)   + bf_b.get("sprint_wins", 0)
            bots.append({
                "bot":             name,
                "type":            "copy",
                "username":        b.get("pm_trader", b.get("trader", "")),
                "sprint_id":       sprint_id,
                "sprint_pnl_usd":  pnl,
                "sprint_pnl_pct":  pnl_pct,
                "sprint_trades":   trades,
                "sprint_wins":     wins,
                "win_rate":        round(wins / trades * 100, 1) if trades > 0 else 0.0,
                "active_positions": len(b.get("positions", {})),
                "sprint_nv_legal_pnl_usd": nv_pnl,
                "sprint_nv_legal_trades":  nv_trades,
            })
    except Exception:
        pass

    # Autonomous bots — closed P&L only (open positions excluded)
    try:
        with open(AUTO_STATE) as f:
            state = json.load(f)
        sprint_id    = state.get("sprint_id", "")
        sprint_start = state.get("sprint_started_at", "")
        for b in state.get("bots", []):
            closed  = [t for t in b.get("closed_trades", [])
                       if not sprint_start or t.get("closed_at", "") >= sprint_start]
            pnl     = round(sum(t.get("pnl_usd", 0.0) for t in closed), 4)
            nv_pnl  = round(sum(t.get("pnl_usd", 0.0) for t in closed
                                if is_nv_legal(t.get("title", ""))), 4)
            nv_trades = sum(1 for t in closed if is_nv_legal(t.get("title", "")))
            pnl_pct = round((pnl / STARTING_CAPITAL) * 100, 2)
            trades  = len(closed)
            wins    = sum(1 for t in closed if t.get("pnl_usd", 0.0) > 0)
            bots.append({
                "bot":             b["name"],
                "type":            b.get("category", "auto"),
                "username":        "",
                "sprint_id":       sprint_id,
                "sprint_pnl_usd":  pnl,
                "sprint_pnl_pct":  pnl_pct,
                "sprint_trades":   trades,
                "sprint_wins":     wins,
                "win_rate":        round(wins / trades * 100, 1) if trades > 0 else 0.0,
                "active_positions": len(b.get("positions", {})),
                "sprint_nv_legal_pnl_usd": nv_pnl,
                "sprint_nv_legal_trades":  nv_trades,
            })
    except Exception:
        pass

    # Copy-trader bots can also be classified — autonomous closed_trades have
    # 'title', copy-trader bots don't store per-trade titles in the same shape,
    # so nv_legal_pnl for copy fleet is tracked separately via the per-sprint
    # _copy.json files below.
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
                "cumulative_pnl_usd":          0.0,
                "cumulative_nv_legal_pnl_usd": 0.0,
                "total_trades":      0,
                "total_wins":        0,
                "total_nv_legal_trades": 0,
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
            t["cumulative_nv_legal_pnl_usd"] = round(
                t["cumulative_nv_legal_pnl_usd"] + b.get("sprint_nv_legal_pnl_usd", 0.0), 2)
            t["total_trades"]      += b.get("sprint_trades", 0)
            t["total_wins"]        += b.get("sprint_wins", 0)
            t["total_nv_legal_trades"] += b.get("sprint_nv_legal_trades", 0)
            rank = b["rank"]
            if rank == 1:
                t["sprint_wins"] += 1
            if rank <= 3:
                t["podiums"] += 1

    # Include live sprint P&L in cumulative totals (no points until sprint ends)
    for b in live_bots:
        t = ensure(b["bot"], b.get("type", "auto"), b.get("username", ""))
        t["cumulative_pnl_usd"] = round(t["cumulative_pnl_usd"] + b.get("sprint_pnl_usd", 0.0), 2)
        t["cumulative_nv_legal_pnl_usd"] = round(
            t["cumulative_nv_legal_pnl_usd"] + b.get("sprint_nv_legal_pnl_usd", 0.0), 2)
        t["total_trades"] += b.get("sprint_trades", 0)
        t["total_wins"]   += b.get("sprint_wins", 0)
        t["total_nv_legal_trades"] += b.get("sprint_nv_legal_trades", 0)

    # Compute derived fields
    result = []
    for t in tally.values():
        tr = t["total_trades"]
        t["overall_win_rate"] = round(t["total_wins"] / tr * 100, 1) if tr > 0 else 0.0
        result.append(t)

    # Exclude ghost bots — retired bots with no trades AND not in current live fleet
    live_names = {b["bot"] for b in live_bots}
    result = [t for t in result if t["total_trades"] > 0 or t["bot"] in live_names]

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
