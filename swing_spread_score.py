#!/usr/bin/env python3
"""
swing_spread_score.py - Evaluate spread strategy groups against promotion criteria.

Groups bots by strategy, aggregates stats across all completed sprints plus
the active sprint, and scores each strategy against five gates:

  Gate 1 -- Volume       : >= 10 trades total across the strategy group
  Gate 2 -- Win rate     : aggregate win rate >= 55%
  Gate 3 -- Profit factor: avg_win / abs(avg_loss) >= 1.3
  Gate 4 -- Risk         : no bot in group has max drawdown > 15%
  Gate 5 -- Consistency  : strategy works (positive P&L + win rate >= 50%)
                           on >= 2 pairs within the group

Verdict per strategy:
  PROMOTE           -- all gates pass
  WATCH             -- passes critical gates, some gates not yet measurable
  CUT               -- fails win rate or drawdown gate
  INSUFFICIENT DATA -- zero trades

Usage:
  python3 swing_spread_score.py              # include active sprint
  python3 swing_spread_score.py --no-active  # completed sprints only
  python3 swing_spread_score.py --json       # machine-readable output
"""
import os
import json
import argparse

WORKSPACE   = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESULTS_DIR = os.path.join(WORKSPACE, "competition", "swing", "results")
ACTIVE_DIR  = os.path.join(WORKSPACE, "competition", "swing", "active")

# ---------------------------------------------------------------------------
# Strategy group definitions
# ---------------------------------------------------------------------------

STRATEGY_GROUPS = {
    "mean_reversion": {
        "description": "RSI extremes + Bollinger on ratio -- bet on reversion to mean",
        "bots": ["skadi", "sigrid", "brynja", "herdis"],
        "pairs": {
            "skadi":  "ETH/BTC",
            "sigrid": "SOL/BTC",
            "brynja": "AAVE/LINK",
            "herdis": "AVAX/SOL",
        },
    },
    "momentum": {
        "description": "Trend + accelerating momentum on ratio -- follow the spread",
        "bots": ["forseti", "gunhild"],
        "pairs": {
            "forseti": "SOL/ETH",
            "gunhild": "AVAX/ETH",
        },
    },
    "catch_up": {
        "description": "7-day underperformance + RSI -- buy the laggard",
        "bots": ["magni", "sunniva"],
        "pairs": {
            "magni":   "LINK/ETH",
            "sunniva": "AAVE/ETH",
        },
    },
    "breakout": {
        "description": "Bollinger breakout + trend -- follow the regime change",
        "bots": ["ragnhild", "estrid"],
        "pairs": {
            "ragnhild": "ETH/BTC",
            "estrid":   "SOL/ETH",
        },
    },
    "dual_confirmation": {
        "description": "Ratio extreme + abs price trend must agree -- filtered mean reversion",
        "bots": ["tofa", "ingrid", "solrun", "thordis"],
        "pairs": {
            "tofa":    "ETH/BTC",
            "ingrid":  "LINK/ETH",
            "solrun":  "AAVE/LINK",
            "thordis": "AVAX/SOL",
        },
    },
}

CRITERIA = {
    "min_trades":        10,
    "min_win_rate":      55.0,
    "min_profit_factor": 1.3,
    "max_drawdown":      15.0,
    "min_working_pairs": 2,
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_portfolio_stats(portfolio_dir, bot_names):
    stats = {}
    for bot in bot_names:
        path = os.path.join(portfolio_dir, "portfolio-" + bot + ".json")
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            p = json.load(f)
        s = p.get("stats", {})
        stats[bot] = {
            "total_trades":     s.get("total_trades", 0),
            "wins":             s.get("wins", 0),
            "losses":           s.get("losses", 0),
            "total_pnl_usd":    s.get("total_pnl_usd", 0.0),
            "total_fees":       s.get("total_fees", 0.0),
            "max_drawdown_pct": s.get("max_drawdown_pct", 0.0),
            "starting_capital": p.get("starting_capital", 1000.0),
            "sum_wins_usd":     s.get("sum_wins_usd"),
            "sum_losses_usd":   s.get("sum_losses_usd"),
        }
    return stats


def collect_all_stats(include_active=True):
    all_bots = set()
    for g in STRATEGY_GROUPS.values():
        all_bots.update(g["bots"])

    agg = {bot: {
        "total_trades":      0,
        "wins":              0,
        "losses":            0,
        "total_pnl_usd":     0.0,
        "total_fees":        0.0,
        "max_drawdown_pct":  0.0,
        "sum_wins_usd":      0.0,
        "sum_losses_usd":    0.0,
        "has_profit_factor": True,
        "sprints_present":   0,
    } for bot in all_bots}

    sprint_count = 0

    if os.path.isdir(RESULTS_DIR):
        for entry in sorted(os.listdir(RESULTS_DIR)):
            if not entry.endswith("_portfolios"):
                continue
            port_dir = os.path.join(RESULTS_DIR, entry)
            sprint_stats = load_portfolio_stats(port_dir, all_bots)
            for bot, s in sprint_stats.items():
                a = agg[bot]
                a["total_trades"]    += s["total_trades"]
                a["wins"]            += s["wins"]
                a["losses"]          += s["losses"]
                a["total_pnl_usd"]    = round(a["total_pnl_usd"] + s["total_pnl_usd"], 2)
                a["total_fees"]       = round(a["total_fees"] + s["total_fees"], 4)
                a["max_drawdown_pct"] = max(a["max_drawdown_pct"], s["max_drawdown_pct"])
                a["sprints_present"] += 1
                if s["sum_wins_usd"] is None or s["sum_losses_usd"] is None:
                    a["has_profit_factor"] = False
                else:
                    a["sum_wins_usd"]  = round(a["sum_wins_usd"] + s["sum_wins_usd"], 2)
                    a["sum_losses_usd"] = round(a["sum_losses_usd"] + s["sum_losses_usd"], 2)
            sprint_count += 1

    if include_active and os.path.isdir(ACTIVE_DIR):
        entries = sorted(os.listdir(ACTIVE_DIR))
        if entries:
            active_dir = os.path.join(ACTIVE_DIR, entries[-1])
            sprint_stats = load_portfolio_stats(active_dir, all_bots)
            for bot, s in sprint_stats.items():
                a = agg[bot]
                a["total_trades"]    += s["total_trades"]
                a["wins"]            += s["wins"]
                a["losses"]          += s["losses"]
                a["total_pnl_usd"]    = round(a["total_pnl_usd"] + s["total_pnl_usd"], 2)
                a["total_fees"]       = round(a["total_fees"] + s["total_fees"], 4)
                a["max_drawdown_pct"] = max(a["max_drawdown_pct"], s["max_drawdown_pct"])
                a["sprints_present"] += 1
                if s["sum_wins_usd"] is None or s["sum_losses_usd"] is None:
                    a["has_profit_factor"] = False
                else:
                    a["sum_wins_usd"]  = round(a["sum_wins_usd"] + s["sum_wins_usd"], 2)
                    a["sum_losses_usd"] = round(a["sum_losses_usd"] + s["sum_losses_usd"], 2)

    for bot, a in agg.items():
        t = a["total_trades"]
        a["win_rate"] = round(a["wins"] / t * 100, 1) if t > 0 else 0.0

    return agg, sprint_count


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_strategy(name, group_def, bot_stats):
    bots  = group_def["bots"]
    pairs = group_def["pairs"]

    total_trades = sum(bot_stats[b]["total_trades"] for b in bots)
    total_wins   = sum(bot_stats[b]["wins"] for b in bots)
    total_pnl    = round(sum(bot_stats[b]["total_pnl_usd"] for b in bots), 2)
    max_dd       = max(bot_stats[b]["max_drawdown_pct"] for b in bots)
    win_rate     = round(total_wins / total_trades * 100, 1) if total_trades > 0 else 0.0

    has_pf        = all(bot_stats[b]["has_profit_factor"] for b in bots)
    profit_factor = None
    avg_win_usd   = None
    avg_loss_usd  = None
    if has_pf and total_wins > 0 and (total_trades - total_wins) > 0:
        sum_w        = sum(bot_stats[b]["sum_wins_usd"] for b in bots)
        sum_l        = sum(bot_stats[b]["sum_losses_usd"] for b in bots)
        total_losses = total_trades - total_wins
        avg_win_usd  = round(sum_w / total_wins, 2)
        avg_loss_usd = round(abs(sum_l / total_losses), 2)
        profit_factor = round(avg_win_usd / avg_loss_usd, 2) if avg_loss_usd > 0 else None

    working    = [b for b in bots if bot_stats[b]["total_pnl_usd"] > 0
                                  and bot_stats[b]["win_rate"] >= 50.0]
    struggling = [b for b in bots if b not in working]

    def gate(condition, has_data):
        if not has_data:
            return "no_data"
        return "pass" if condition else "fail"

    has_trades = total_trades > 0
    gates = {
        "volume":        gate(total_trades >= CRITERIA["min_trades"], has_trades),
        "win_rate":      gate(win_rate >= CRITERIA["min_win_rate"], has_trades),
        "profit_factor": gate(profit_factor is not None and profit_factor >= CRITERIA["min_profit_factor"],
                              profit_factor is not None),
        "drawdown":      gate(max_dd <= CRITERIA["max_drawdown"], True),
        "consistency":   gate(len(working) >= CRITERIA["min_working_pairs"], has_trades),
    }

    if total_trades == 0:
        verdict = "INSUFFICIENT DATA"
    elif any(gates[g] == "fail" for g in ["win_rate", "drawdown"]):
        verdict = "CUT"
    elif any(gates[g] == "fail" for g in gates):
        verdict = "WATCH"
    elif any(gates[g] == "no_data" for g in gates):
        verdict = "WATCH"
    else:
        verdict = "PROMOTE"

    return {
        "name":          name,
        "description":   group_def["description"],
        "bots":          bots,
        "pairs":         pairs,
        "total_trades":  total_trades,
        "total_wins":    total_wins,
        "win_rate":      win_rate,
        "profit_factor": profit_factor,
        "avg_win_usd":   avg_win_usd,
        "avg_loss_usd":  avg_loss_usd,
        "total_pnl":     total_pnl,
        "max_drawdown":  max_dd,
        "working":       working,
        "struggling":    struggling,
        "gates":         gates,
        "verdict":       verdict,
        "bot_stats":     {b: bot_stats[b] for b in bots},
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

VERDICT_ORDER = {"PROMOTE": 0, "WATCH": 1, "CUT": 2, "INSUFFICIENT DATA": 3}


def gstr(v):
    return "pass" if v == "pass" else ("FAIL" if v == "fail" else "n/a ")


def print_report(results, sprint_count):
    print()
    print("=" * 66)
    print("  SPREAD STRATEGY EVALUATION")
    print("  Sprints evaluated: " + str(sprint_count))
    print("  Gates: " + str(CRITERIA["min_trades"]) + " trades | " +
          str(CRITERIA["min_win_rate"]) + "% win rate | " +
          "PF >= " + str(CRITERIA["min_profit_factor"]) + " | " +
          "DD < " + str(CRITERIA["max_drawdown"]) + "% | " +
          ">= " + str(CRITERIA["min_working_pairs"]) + " pairs working")
    print("=" * 66)

    for r in sorted(results, key=lambda x: VERDICT_ORDER[x["verdict"]]):
        verdict = r["verdict"]
        print()
        print("  [" + verdict + "]  " + r["name"].upper().replace("_", " "))
        print("  " + r["description"])
        print()

        gt = r["gates"]
        pf_str = (str(r["profit_factor"])) if r["profit_factor"] is not None else "n/a"
        aw_str = ("$" + str(r["avg_win_usd"])) if r["avg_win_usd"] is not None else "n/a"
        al_str = ("$" + str(r["avg_loss_usd"])) if r["avg_loss_usd"] is not None else "n/a"

        print("  Trades:        {:>5}    gate: {}  (need >= {})".format(
            r["total_trades"], gstr(gt["volume"]), CRITERIA["min_trades"]))
        print("  Win rate:      {:>4.1f}%    gate: {}  (need >= {}%)".format(
            r["win_rate"], gstr(gt["win_rate"]), CRITERIA["min_win_rate"]))
        print("  Profit factor: {:>5}    gate: {}  avg win {} / avg loss {}".format(
            pf_str, gstr(gt["profit_factor"]), aw_str, al_str))
        print("  Max drawdown:  {:>4.1f}%    gate: {}  (need < {}%)".format(
            r["max_drawdown"], gstr(gt["drawdown"]), CRITERIA["max_drawdown"]))
        print("  Net P&L:       ${:>+.2f}".format(r["total_pnl"]))
        print()

        print("  {:<12} {:<12} {:>6} {:>8} {:>8}  {:>6}  {}".format(
            "Bot", "Pair", "Trades", "WinRate", "P&L", "DD", "Status"))
        print("  " + "-"*12 + " " + "-"*12 + " " + "-"*6 + " " + "-"*8 +
              " " + "-"*8 + "  " + "-"*6 + "  " + "-"*10)
        for bot in r["bots"]:
            s    = r["bot_stats"][bot]
            pair = r["pairs"].get(bot, "?")
            ok   = bot in r["working"]
            wr   = "{:.1f}%".format(s["win_rate"]) if s["total_trades"] > 0 else "n/a"
            pnl  = "${:+.2f}".format(s["total_pnl_usd"]) if s["total_trades"] > 0 else "n/a"
            dd   = "{:.1f}%".format(s["max_drawdown_pct"]) if s["total_trades"] > 0 else "n/a"
            status = "working" if ok else ("struggling" if s["total_trades"] > 0 else "no trades yet")
            print("  {:<12} {:<12} {:>6} {:>8} {:>8}  {:>6}  {}".format(
                bot, pair, s["total_trades"], wr, pnl, dd, status))

        wp = len(r["working"])
        tp = len(r["bots"])
        print()
        print("  Pair consistency: {}/{} working    gate: {}  (need >= {})".format(
            wp, tp, gstr(gt["consistency"]), CRITERIA["min_working_pairs"]))
        print()
        print("  " + "-" * 62)

    promotes = [r for r in results if r["verdict"] == "PROMOTE"]
    watches  = [r for r in results if r["verdict"] == "WATCH"]
    cuts     = [r for r in results if r["verdict"] == "CUT"]

    print()
    print("  RECOMMENDATION")
    print("  " + "-" * 44)

    if promotes:
        print("  FUND: " + ", ".join(r["name"].replace("_", " ") for r in promotes))
        for r in promotes:
            best      = max(r["bots"], key=lambda b: r["bot_stats"][b]["total_pnl_usd"])
            best_pair = r["pairs"].get(best, "?")
            print("    -> Deploy {} on {}  ({})".format(
                r["name"].replace("_", " "), best_pair, best))
        if watches:
            print()
            print("  MONITOR 1 more cycle: " +
                  ", ".join(r["name"].replace("_", " ") for r in watches))
    elif watches:
        print("  Not ready. Promising -- run 1 more cycle:")
        for r in watches:
            failing = [k for k, v in r["gates"].items() if v == "fail"]
            missing = [k for k, v in r["gates"].items() if v == "no_data"]
            issues  = []
            if failing: issues.append("failing: " + ", ".join(failing))
            if missing: issues.append("no data yet: " + ", ".join(missing))
            print("    {}: {} trades, {:.1f}% win rate{}".format(
                r["name"].replace("_", " "), r["total_trades"], r["win_rate"],
                "  (" + "; ".join(issues) + ")" if issues else ""))
    else:
        print("  No strategy ready. Run 2 more cycles before re-evaluating.")

    if cuts:
        print()
        print("  CUT: " + ", ".join(r["name"].replace("_", " ") for r in cuts) +
              "  (failing critical gates)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Score spread strategy groups")
    parser.add_argument("--no-active", action="store_false", dest="active",
                        default=True, help="Exclude active sprint data")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    bot_stats, sprint_count = collect_all_stats(include_active=args.active)

    results = []
    for name, group_def in STRATEGY_GROUPS.items():
        results.append(score_strategy(name, group_def, bot_stats))

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results, sprint_count)


if __name__ == "__main__":
    main()
