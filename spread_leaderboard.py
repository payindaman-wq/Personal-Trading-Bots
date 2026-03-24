#!/usr/bin/env python3
"""
spread_leaderboard.py - Cumulative leaderboard for swing trading competition.

Usage:
  python3 spread_leaderboard.py              # print leaderboard
  python3 spread_leaderboard.py --json       # also dump spread_leaderboard.json
  python3 spread_leaderboard.py --sprint ID  # detail for one sprint
  python3 spread_leaderboard.py --no-live    # exclude active sprint
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESULTS_DIR  = os.path.join(WORKSPACE, "competition", "spread", "results")
ACTIVE_DIR   = os.path.join(WORKSPACE, "competition", "spread", "active")
LB_PATH      = os.path.join(WORKSPACE, "competition", "spread", "spread_leaderboard.json")
CYCLE_STATE  = os.path.join(WORKSPACE, "competition", "spread", "spread_cycle_state.json")
FLEET_DIR      = os.path.join(WORKSPACE, "fleet", "spread")
COINT_REPORT   = os.path.join(WORKSPACE, "competition", "spread", "cointegration_report.json")

POINTS_MAP = {1: 8, 2: 5, 3: 3}

DISPLAY_CAPITAL = 1000.0


def load_cycle_state():
    """Return swing cycle state dict, or defaults if file missing."""
    try:
        with open(CYCLE_STATE) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_pair_metadata():
    """Load each bot's assigned pair and current health verdict from cointegration report."""
    # Load bot → pair mapping from strategy.yaml files
    bot_pairs = {}
    if os.path.isdir(FLEET_DIR):
        try:
            import yaml
        except ImportError:
            yaml = None
        for bot in os.listdir(FLEET_DIR):
            strat_path = os.path.join(FLEET_DIR, bot, "strategy.yaml")
            if not os.path.isfile(strat_path):
                continue
            try:
                if yaml:
                    with open(strat_path) as f:
                        d = yaml.safe_load(f)
                else:
                    # fallback: parse just the spread block manually
                    d = {}
                sp = d.get("spread", {})
                base  = sp.get("base",  "").replace("/USD", "")
                quote = sp.get("quote", "").replace("/USD", "")
                bot_pairs[bot] = {
                    "pair":         f"{base}/{quote}" if base and quote else "?",
                    "analysis_pair": sp.get("analysis_pair", ""),
                    "health":       "?",
                    "half_life":    None,
                    "corr":         None,
                    "hurst":        None,
                }
            except Exception:
                pass

    # Overlay verdicts from cointegration report
    if os.path.isfile(COINT_REPORT):
        try:
            with open(COINT_REPORT) as f:
                report = json.load(f)
            active = report.get("active_pairs", {})
            for bot, meta in bot_pairs.items():
                ap = meta["analysis_pair"]
                if ap in active:
                    r = active[ap]
                    meta["health"]    = r.get("verdict", "?")
                    meta["half_life"] = r.get("half_life")
                    meta["corr"]      = r.get("corr")
                    meta["hurst"]     = r.get("hurst")
        except Exception:
            pass

    return bot_pairs


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
                "pair":                  "?",
                "pair_health":           "?",
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
            if not in_prog:
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

    # Attach current pair assignments and health verdicts
    pair_meta = load_pair_metadata()
    for name, b in bots.items():
        if name in pair_meta:
            b["pair"]        = pair_meta[name]["pair"]
            b["pair_health"] = pair_meta[name]["health"]
            b["pair_half_life"] = pair_meta[name].get("half_life")
            b["pair_corr"]      = pair_meta[name].get("corr")
            b["pair_hurst"]     = pair_meta[name].get("hurst")

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
    divider = "=" * 88

    cycle = load_cycle_state()
    cyc_num     = cycle.get("cycle", 1)
    sprint_n    = cycle.get("sprint_in_cycle", 0)
    sprints_per = cycle.get("sprints_per_cycle", 4)
    cyc_status  = cycle.get("status", "active")

    print()
    print(divider)
    print(f"  VIKING FLEET — SWING LEAGUE LEADERBOARD  --  {now}")
    if cyc_status == "awaiting_review":
        print(f"  Cycle {cyc_num} | COMPLETE ({sprint_n}/{sprints_per} sprints) -- awaiting strategy review")
    else:
        print(f"  Cycle {cyc_num} | Sprint {sprint_n} of {sprints_per}")
    if active_sprint:
        print(f"  Active sprint : {active_sprint['comp_id']}  (live data included)")
    print(divider)
    print(f"  {'#':<4} {'BOT':<12} {'PAIR':<10} {'PTS':>4} {'SPRINTS':>8} {'1ST':>4} {'TOP3':>5} "
          f"{'CUM PNL':>11} {'AVG/SPRINT':>11} {'WIN%':>6} {'TRADES':>7}")
    print("  " + "-" * 84)

    for i, b in enumerate(ranked, 1):
        icon    = RANK_ICONS.get(i, f"{i}.")
        pnl_str = fmt_pnl(b["cumulative_pnl_usd"], 11)
        avg_str = fmt_pct(b["avg_pnl_pct_per_sprint"], 11)
        health = b.get("pair_health", "?")
        pair   = b.get("pair", "?")
        flag   = " *" if health in ("WEAK", "RETIRE") else ""
        print(f"  {icon:<4} {b['bot']:<12} {pair+flag:<10} {b['points']:>4} "
              f"{b['sprints_entered']:>8} {b['sprint_wins']:>4} {b['podiums']:>5} "
              f"{pnl_str} {avg_str} {b['overall_win_rate']:>5.1f}% {b['total_trades']:>7}")

    print("  " + "-" * 84)
    print("  Ranked by cumulative P&L.  7-day sprints.  * = WEAK/RETIRE pair (see below)")
    print("  PTS: 1st=8 | 2nd=5 | 3rd=3 | 4th-8th=1")
    print()

    # Pair health context
    pair_meta = load_pair_metadata()
    if pair_meta:
        by_health = {}
        for bot, m in pair_meta.items():
            h = m.get("health", "?")
            by_health.setdefault(h, []).append(f"{bot}({m['pair']})")
        print("  PAIR HEALTH CONTEXT")
        print("  " + "-" * 84)
        for verdict in ("STRONG", "WATCH", "WEAK", "RETIRE"):
            bots_in = by_health.get(verdict)
            if bots_in:
                hl_notes = []
                for bot in sorted(pair_meta, key=lambda x: pair_meta[x]["pair"]):
                    if pair_meta[bot]["health"] == verdict:
                        hl = pair_meta[bot].get("half_life")
                        hl_str = f"hl={hl:.0f}h" if hl else ""
                        corr = pair_meta[bot].get("corr")
                        corr_str = f"corr={corr:.2f}" if corr else ""
                        hl_notes.append(f"{bot}({pair_meta[bot]['pair']} {hl_str} {corr_str}".strip() + ")")
                label = f"  {verdict:<8}"
                print(f"{label} {' | '.join(hl_notes)}")
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
    parser = argparse.ArgumentParser(description="Viking Fleet spread leaderboard")
    parser.add_argument("--json",    action="store_true", help="Save spread_leaderboard.json")
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
        cycle_st = load_cycle_state()
        out = {
            "generated_at":      datetime.now(timezone.utc).isoformat(),
            "league":            "swing",
            "total_sprints":     len(all_sprints),
            "archived":          len(archived),
            "active_sprint":     active["comp_id"] if active else None,
            "cycle":             cycle_st.get("cycle", 1),
            "sprint_in_cycle":   cycle_st.get("sprint_in_cycle", 0),
            "sprints_per_cycle": cycle_st.get("sprints_per_cycle", 4),
            "cycle_status":      cycle_st.get("status", "active"),
            "rankings":          ranked,
            "pair_health_summary": {
                bot: {
                    "pair":       ranked_bot.get("pair", "?"),
                    "health":     ranked_bot.get("pair_health", "?"),
                    "half_life":  ranked_bot.get("pair_half_life"),
                    "corr":       ranked_bot.get("pair_corr"),
                    "hurst":      ranked_bot.get("pair_hurst"),
                }
                for ranked_bot in ranked
                for bot in [ranked_bot["bot"]]
            },
        }
        with open(LB_PATH, "w") as f:
            json.dump(out, f, indent=2)
        print(f"  Saved to {LB_PATH}")


if __name__ == "__main__":
    main()
