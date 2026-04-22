#!/usr/bin/env python3
"""
league_killswitch.py — per-league circuit breaker for futures leagues.

Meta_audit F7 (2026-04-22): account-wide 15% drawdown in kraken_killswitch is
too coarse. A losing league (futures_day at live_sharpe_ann=-18.55) can bleed
1-3% per sprint indefinitely without tripping the account kill, while burning
Gemini spend and blocking capital concentration in winners.

Trigger conditions (all must hold) over the last N=5 sprints:
  - >=3 of 5 sprints have live_pnl_pct < 0 (majority losing)
  - cumulative live_pnl_pct across the 5 sprints < -3% (non-trivial bleed)
  - live_sharpe_ann over those sprints < 0 (not just one spike)

Effect when triggered:
  - Writes /root/.openclaw/workspace/research/league_killswitch/{league}.flag
  - Appends syn_inbox.jsonl entry at severity=critical (Chris action required)
  - futures_{day,swing}_restart.py skips start_new if flag present.

Reactivation (manual Chris step):
  - Delete the .flag file. VIDAR deep_dive + positive drift delta expected
    before manual reactivation, but not enforced here.

Runs every 30 minutes via cron. Read-only wrt ODIN state — does not touch
elite files, gen_state, or fleet/.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

WORKSPACE   = "/root/.openclaw/workspace"
RESEARCH    = os.path.join(WORKSPACE, "research")
FLAG_DIR    = os.path.join(RESEARCH, "league_killswitch")
LOG_FILE    = os.path.join(FLAG_DIR, "killswitch.log")
INBOX       = os.path.join(WORKSPACE, "syn_inbox.jsonl")

FUTURES_LEAGUES = ("futures_day", "futures_swing")

# Trigger thresholds (conservative so we don't false-positive on volatility).
WINDOW_SPRINTS          = 5
MIN_LOSING_IN_WINDOW    = 3       # >= 3 of 5 sprints losing
CUMULATIVE_PCT_FLOOR    = -3.0    # sum of last 5 live_pnl_pct < -3%
LIVE_SHARPE_FLOOR       = 0.0     # live_sharpe_ann over window < 0


def _ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(msg):
    os.makedirs(FLAG_DIR, exist_ok=True)
    line = f"[{_ts()}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def _inbox(severity, msg, league, reason):
    rec = {
        "ts":       _ts(),
        "source":   "league_killswitch",
        "severity": severity,
        "league":   league,
        "reason":   reason,
        "msg":      msg,
    }
    try:
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError as e:
        _log(f"inbox write failed: {e}")


def _load_drift(league):
    path = os.path.join(RESEARCH, league, "backtest_drift.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def evaluate(league):
    """Return (should_kill, reason_str, stats_dict)."""
    drift = _load_drift(league)
    if drift is None:
        return False, "no drift file (cold start)", {}

    per = drift.get("per_sprint") or []
    if len(per) < WINDOW_SPRINTS:
        return False, f"only {len(per)} sprints available (<{WINDOW_SPRINTS})", {}

    window = per[-WINDOW_SPRINTS:]
    pnls = [row.get("live_pnl_pct", 0.0) for row in window]
    losing = sum(1 for p in pnls if p < 0)
    cumulative = sum(pnls)
    live_sharpe = drift.get("live_sharpe_ann")

    stats = {
        "window":       WINDOW_SPRINTS,
        "losing_count": losing,
        "cumulative":   round(cumulative, 4),
        "live_sharpe":  live_sharpe,
        "per_pnl":      [round(p, 4) for p in pnls],
    }

    if losing < MIN_LOSING_IN_WINDOW:
        return False, f"only {losing}/{WINDOW_SPRINTS} losing (<{MIN_LOSING_IN_WINDOW})", stats
    if cumulative >= CUMULATIVE_PCT_FLOOR:
        return False, f"cumulative {cumulative:.2f}% >= {CUMULATIVE_PCT_FLOOR}%", stats
    if live_sharpe is None or live_sharpe >= LIVE_SHARPE_FLOOR:
        return False, f"live_sharpe_ann={live_sharpe} >= {LIVE_SHARPE_FLOOR}", stats

    reason = (
        f"{losing}/{WINDOW_SPRINTS} losing sprints, cumulative={cumulative:.2f}%, "
        f"live_sharpe_ann={live_sharpe:.2f} (all below floor)"
    )
    return True, reason, stats


def is_paused(league):
    """Public helper used by restart scripts to check the pause flag."""
    return os.path.exists(os.path.join(FLAG_DIR, f"{league}.flag"))


def apply(league):
    should_kill, reason, stats = evaluate(league)
    flag_path = os.path.join(FLAG_DIR, f"{league}.flag")
    already_paused = os.path.exists(flag_path)

    if should_kill and not already_paused:
        os.makedirs(FLAG_DIR, exist_ok=True)
        payload = {
            "paused_at":    _ts(),
            "league":       league,
            "reason":       reason,
            "stats":        stats,
            "reactivation": "manual (delete this file) after VIDAR deep_dive + positive drift delta",
        }
        with open(flag_path, "w") as f:
            json.dump(payload, f, indent=2)
        _log(f"{league}: PAUSED — {reason}")
        _inbox(
            "critical",
            f"[SYN/league_killswitch] {league} paused — {reason}. "
            f"Sprint restart will skip until {flag_path} is removed.",
            league,
            reason,
        )
    elif should_kill and already_paused:
        _log(f"{league}: already paused — {reason}")
    elif (not should_kill) and already_paused:
        # Pause remains active — reactivation is manual only. Log a status ping
        # occasionally; do not re-alert Chris.
        _log(f"{league}: pause flag present but criteria no longer met ({reason}); awaiting manual clear")
    else:
        _log(f"{league}: healthy — {reason}")


def main():
    for league in FUTURES_LEAGUES:
        apply(league)


if __name__ == "__main__":
    main()
