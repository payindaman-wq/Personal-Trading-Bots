#!/usr/bin/env python3
"""
regression_watch.py — Detect live-vs-backtest regression for fleet bots.

Compares trailing live performance (leaderboard sprint_log pnl_pct) against
pinned backtest expectations, alerts via Telegram when a bot is meaningfully
underperforming its baseline.

Modes:
  (default)          Hourly check. Alerts on regression, per-bot cooldown.
  --report           Print current live vs baseline table; no alerts sent.
  --refresh-baseline Run backtest.py for each bot in --league and pin
                     daily_expected_pnl_pct into regression_baselines.json.
                     Intended to be invoked by LOKI on cycle advance.
  --dry-run          Compute alerts but don't send. Works with default mode.

Alert rule (both conditions must hold):
  - under_pct > UNDER_PCT_THRESHOLD  (live trails expected by > 40%)
  - z_score  < Z_SCORE_THRESHOLD     (mean-of-means z-score < -2)
Requires at least MIN_SPRINTS completed live sprints to avoid low-n noise.
"""
import argparse
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
COMP_DIR = f"{WORKSPACE}/competition"
BASELINE_FILE = f"{COMP_DIR}/regression_baselines.json"
STATE_FILE = f"{COMP_DIR}/regression_watch_state.json"
BACKTEST_RESULTS = f"{COMP_DIR}/backtest_results.json"
BACKTEST_SCRIPT = f"{WORKSPACE}/backtest.py"
LOG_FILE = f"{COMP_DIR}/regression_watch.log"

BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID = "8154505910"

MIN_SPRINTS = 5
TRAILING_WINDOW = 7
UNDER_PCT_THRESHOLD = 0.40
Z_SCORE_THRESHOLD = -2.0
COOLDOWN_HOURS = 6
BASELINE_STALE_DAYS = 21
BACKTEST_DAYS = 30

LEAGUES = {
    "day":           {"leaderboard": "leaderboard.json",                             "sprint_days": 1, "label": "Spot Day"},
    "futures_day":   {"leaderboard": "futures_day/futures_day_leaderboard.json",     "sprint_days": 1, "label": "Futures Day"},
    "swing":         {"leaderboard": "swing/swing_leaderboard.json",                 "sprint_days": 7, "label": "Spot Swing"},
    "futures_swing": {"leaderboard": "futures_swing/futures_swing_leaderboard.json", "sprint_days": 7, "label": "Futures Swing"},
}


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M PST")


def log(msg):
    line = f"[{pst_now()}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_json(path, default):
    if not os.path.isfile(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        log(f"load_json({path}) failed: {e}")
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def tg_send(msg):
    import urllib.request
    try:
        payload = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10).read()
    except Exception as e:
        log(f"tg_send failed: {e}")


def trailing_live_sprints(bot_entry, window=TRAILING_WINDOW):
    """Return list of completed sprint pnl_pct values, newest-last, capped at window."""
    sprints = [s for s in bot_entry.get("sprint_log", []) if not s.get("in_progress")]
    sprints = sprints[-window:]
    return [s.get("pnl_pct", 0.0) for s in sprints]


def zscore(values, expected):
    n = len(values)
    if n == 0:
        return 0.0
    mean = sum(values) / n
    if n < 2:
        return 0.0 if mean == expected else (-math.inf if mean < expected else math.inf)
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    sd = math.sqrt(var)
    if sd == 0:
        return 0.0 if mean == expected else (-math.inf if mean < expected else math.inf)
    return (mean - expected) / (sd / math.sqrt(n))


def under_pct(live_mean, expected):
    """Fraction that live trails expected, regardless of sign.
    expected=+1.0, live=+0.3 -> 0.7 (70% short of a gain).
    expected=-0.5, live=-1.0 -> 1.0 (lost twice as much as baseline predicted)."""
    if expected == 0:
        return 0.0 if live_mean >= 0 else abs(live_mean)
    return max(0.0, (expected - live_mean) / abs(expected))


def evaluate_bot(league, sprint_days, bot_entry, baseline):
    live_vals = trailing_live_sprints(bot_entry)
    n = len(live_vals)
    daily_expected = baseline.get("daily_expected_pnl_pct")
    if daily_expected is None:
        return None
    expected_per_sprint = daily_expected * sprint_days
    live_mean = sum(live_vals) / n if n else 0.0
    z = zscore(live_vals, expected_per_sprint)
    up = under_pct(live_mean, expected_per_sprint)
    return {
        "league": league,
        "bot": bot_entry["bot"],
        "n": n,
        "live_mean_per_sprint": live_mean,
        "expected_per_sprint": expected_per_sprint,
        "daily_expected": daily_expected,
        "under_pct": up,
        "z_score": z,
        "baseline_pinned_at": baseline.get("pinned_at"),
        "baseline_cycle": baseline.get("cycle"),
        "is_regression": (n >= MIN_SPRINTS and up > UNDER_PCT_THRESHOLD and z < Z_SCORE_THRESHOLD),
    }


def baseline_is_stale(baseline):
    pinned = baseline.get("pinned_at")
    if not pinned:
        return True
    try:
        dt = datetime.fromisoformat(pinned)
    except Exception:
        return True
    return datetime.now(timezone.utc) - dt > timedelta(days=BASELINE_STALE_DAYS)


def should_alert(state, key):
    last = state.get("last_alerted", {}).get(key)
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return True
    return datetime.now(timezone.utc) - last_dt > timedelta(hours=COOLDOWN_HOURS)


def mark_alerted(state, key):
    state.setdefault("last_alerted", {})[key] = datetime.now(timezone.utc).isoformat()


def format_alert(r):
    pinned = r["baseline_pinned_at"] or "?"
    try:
        pinned = datetime.fromisoformat(pinned).astimezone(PST).strftime("%Y-%m-%d %H:%M PST")
    except Exception:
        pass
    return (
        f"<b>SYN: Regression detected</b>\n"
        f"Bot: <b>{r['bot']}</b> ({r['league']})\n"
        f"Live mean: {r['live_mean_per_sprint']:+.3f}%/sprint (n={r['n']})\n"
        f"Expected: {r['expected_per_sprint']:+.3f}%/sprint "
        f"({r['daily_expected']:+.3f}%/day backtest)\n"
        f"Underperform: {r['under_pct']*100:.0f}%, z={r['z_score']:+.2f}\n"
        f"Baseline: cycle {r['baseline_cycle']} pinned {pinned}\n"
        f"Time: {pst_now()}"
    )


def run_default(dry_run=False):
    baselines = load_json(BASELINE_FILE, {})
    state = load_json(STATE_FILE, {"last_alerted": {}})
    findings = []
    stale_warnings = []

    for league, cfg in LEAGUES.items():
        lb_path = os.path.join(COMP_DIR, cfg["leaderboard"])
        lb = load_json(lb_path, None)
        if not lb:
            continue
        league_baselines = baselines.get(league, {})
        for bot_entry in lb.get("rankings", []):
            bot = bot_entry["bot"]
            bl = league_baselines.get(bot)
            if not bl:
                continue
            if baseline_is_stale(bl):
                stale_warnings.append(f"{league}:{bot}")
                continue
            r = evaluate_bot(league, cfg["sprint_days"], bot_entry, bl)
            if r:
                findings.append(r)

    regressions = [r for r in findings if r["is_regression"]]
    log(f"checked {len(findings)} bot/baseline pairs; {len(regressions)} regressions; {len(stale_warnings)} stale baselines")

    for r in regressions:
        key = f"regression:{r['league']}:{r['bot']}"
        if not should_alert(state, key):
            log(f"skip (cooldown): {key}")
            continue
        msg = format_alert(r)
        log(f"ALERT: {r['league']}/{r['bot']} under={r['under_pct']:.2f} z={r['z_score']:.2f} n={r['n']}")
        if dry_run:
            print("--- dry-run alert ---"); print(msg); print()
        else:
            tg_send(msg)
            mark_alerted(state, key)

    if stale_warnings and not dry_run:
        key = "stale_baselines"
        if should_alert(state, key):
            tg_send(
                "<b>SYN: Regression baselines stale</b>\n"
                f"Stale (>{BASELINE_STALE_DAYS}d): {len(stale_warnings)} entries\n"
                f"Sample: {', '.join(stale_warnings[:6])}\n"
                f"Run: regression_watch.py --refresh-baseline --league &lt;name&gt;\n"
                f"Time: {pst_now()}"
            )
            mark_alerted(state, key)

    save_json(STATE_FILE, state)
    return findings, regressions


def run_report():
    findings, regressions = run_default(dry_run=True)
    if not findings:
        print("No bot/baseline pairs evaluated. Pin baselines first with --refresh-baseline.")
        return
    print(f"{'LEAGUE':<14} {'BOT':<14} {'N':>3}  {'LIVE/SPRT':>10}  {'EXP/SPRT':>9}  {'UNDER%':>7}  {'Z':>6}  {'REGR':>4}")
    for r in sorted(findings, key=lambda x: (x["league"], -x["under_pct"])):
        flag = "YES" if r["is_regression"] else ""
        print(f"{r['league']:<14} {r['bot']:<14} {r['n']:>3}  "
              f"{r['live_mean_per_sprint']:>+9.3f}%  {r['expected_per_sprint']:>+8.3f}%  "
              f"{r['under_pct']*100:>6.0f}%  {r['z_score']:>+6.2f}  {flag:>4}")
    print(f"\n{len(regressions)} regression(s) flagged.")


def run_refresh_baseline(league, bots_filter=None, days=BACKTEST_DAYS):
    if league not in LEAGUES:
        print(f"Unknown league: {league}. Options: {list(LEAGUES.keys())}")
        sys.exit(1)
    cfg = LEAGUES[league]
    lb_path = os.path.join(COMP_DIR, cfg["leaderboard"])
    lb = load_json(lb_path, None)
    if not lb:
        log(f"refresh-baseline: leaderboard missing for {league} at {lb_path}")
        sys.exit(1)
    cycle = lb.get("cycle")
    bots = [r["bot"] for r in lb.get("rankings", [])]
    if bots_filter:
        bots = [b for b in bots if b in bots_filter]
    if not bots:
        log(f"refresh-baseline: no bots to process for {league}")
        return

    baselines = load_json(BASELINE_FILE, {})
    league_map = baselines.setdefault(league, {})
    ok = skipped = 0
    for bot in bots:
        log(f"refresh-baseline: backtesting {league}/{bot} over {days}d")
        proc = subprocess.run(
            ["python3", BACKTEST_SCRIPT, "--bot", bot, "--days", str(days)],
            capture_output=True, text=True, timeout=600,
        )
        if proc.returncode != 0:
            log(f"  backtest failed rc={proc.returncode}: {proc.stderr[:200]}")
            skipped += 1
            continue
        results = load_json(BACKTEST_RESULTS, [])
        result = next((x for x in results if x.get("bot") == bot and "error" not in x), None)
        if not result:
            log(f"  no usable result for {bot}")
            skipped += 1
            continue
        total_pnl_pct = result.get("total_pnl_pct", 0.0)
        daily_expected = total_pnl_pct / days if days > 0 else 0.0
        league_map[bot] = {
            "daily_expected_pnl_pct": daily_expected,
            "total_pnl_pct": total_pnl_pct,
            "backtest_days": days,
            "backtest_trades": result.get("total_trades"),
            "backtest_win_rate_pct": result.get("win_rate_pct"),
            "cycle": cycle,
            "pinned_at": datetime.now(timezone.utc).isoformat(),
        }
        ok += 1
        log(f"  pinned: daily_expected={daily_expected:+.4f}% (total={total_pnl_pct:+.2f}% over {days}d)")

    save_json(BASELINE_FILE, baselines)
    log(f"refresh-baseline {league}: pinned {ok}, skipped {skipped}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--refresh-baseline", action="store_true", help="Run backtest.py per bot and pin baseline")
    p.add_argument("--league", help="League key (day, futures_day, swing, futures_swing). Required for --refresh-baseline.")
    p.add_argument("--bot", action="append", help="Limit baseline refresh to this bot (repeatable)")
    p.add_argument("--days", type=int, default=BACKTEST_DAYS, help=f"Backtest lookback days (default {BACKTEST_DAYS})")
    p.add_argument("--report", action="store_true", help="Print live vs baseline table")
    p.add_argument("--dry-run", action="store_true", help="Compute alerts but don't send")
    args = p.parse_args()

    if args.refresh_baseline:
        if not args.league:
            print("--refresh-baseline requires --league")
            sys.exit(1)
        run_refresh_baseline(args.league, bots_filter=args.bot, days=args.days)
        return
    if args.report:
        run_report()
        return
    run_default(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
