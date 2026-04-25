"""Live-vs-backtest Sharpe drift tracker.

For each league in {futures_day, futures_swing}, compare the research backtest
Sharpe claimed for the deployed strategy (snapshotted from best_strategy.meta.json
at sprint start) against the live realised Sharpe computed from the autobot's
completed sprints.

Writes research/{league}/backtest_drift.json for consumption by:
  - odin_researcher_v2 (drift-aware new_best gating)
  - dashboard_data (Research Lab observability)

Live Sharpe construction:
  - Each completed sprint yields one per-sprint return r_i = live_pnl_pct / 100.
  - Over last N=10 sprints (where N >= 3), compute
        live_sharpe = mean(r) / std(r) * sqrt(periods_per_year)
    where periods_per_year = 365 / (duration_hours/24).
  - If N < 3, live_sharpe is None and no penalty is applied.

Drift penalty multiplier (applied to new_best gating):
  delta = backtest_sharpe - live_sharpe
  if delta <= 0:    gate_bonus = 0          (backtest isn't overstating)
  elif delta >= 1.5: gate_bonus = delta     (full penalty, clipped at delta)
  else:             gate_bonus = delta * (delta / 1.5)
  --> ODIN requires raw_sharpe > best_sharpe + gate_bonus for a new_best claim.

This does NOT alter adj_score or elite ranking — only hardens the "is this
actually better" gate so inflated backtest claims can't keep resetting the
champion.
"""
from __future__ import annotations

import glob
import json
import math
import os
from datetime import datetime, timezone

WORKSPACE   = "/root/.openclaw/workspace"
RESEARCH    = os.path.join(WORKSPACE, "research")
COMPETITION = os.path.join(WORKSPACE, "competition")

# F5 (meta_audit 2026-04-25): day + swing leagues use archived cycle dirs,
# not a single results_dir. results_glob is a list of glob patterns whose
# matches are unioned (for spot leagues that flatten into archive/cycle-N/).
LEAGUE_CONFIG = {
    "day": {
        "bot": "autobotday",
        "results_dir": os.path.join(COMPETITION, "archive"),
        "sprint_glob": "cycle-*/comp-*",
        "duration_hours": 24,
    },
    "swing": {
        "bot": "autobotswing",
        "results_dir": os.path.join(COMPETITION, "swing", "archive"),
        "sprint_glob": "cycle-*/swing-*",
        "duration_hours": 168,
    },
    "futures_day": {
        "bot": "autobotdayfutures",
        "results_dir": os.path.join(COMPETITION, "futures_day", "results"),
        "sprint_glob": "fut-day-*",
        "duration_hours": 24,
    },
    "futures_swing": {
        "bot": "autobotswingfutures",
        "results_dir": os.path.join(COMPETITION, "futures_swing", "results"),
        "sprint_glob": "fut-swing-*",
        "duration_hours": 168,
    },
}

WINDOW_SPRINTS = 10
MIN_SPRINTS_FOR_SHARPE = 3
MAX_DELTA_FOR_FULL_PENALTY = 1.5
# F1 (meta_audit 2026-04-25): rolling veto + live_pnl_z blend.
VETO_WINDOW_SPRINTS = 5
MIN_SPRINTS_FOR_VETO = 5
Z_WINDOW_SPRINTS = 10


def _sprint_dirs(cfg):
    return sorted(d for d in glob.glob(os.path.join(cfg["results_dir"], cfg["sprint_glob"]))
                  if os.path.isdir(d))


def _sprint_pnl_pct(sprint_dir, bot):
    """Return the autobot's live_pnl_pct for a completed sprint, or None."""
    pf = os.path.join(sprint_dir, f"portfolio-{bot}.json")
    if not os.path.exists(pf):
        return None
    try:
        with open(pf) as f:
            p = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    stats = p.get("stats") or {}
    # Prefer realised PnL (closed trades) over mark-to-market — the backtest
    # scores realised PnL, so this keeps live and backtest measured the same
    # way. Falls back to MTM only if realised is unavailable.
    if "total_pnl_pct" in stats:
        return float(stats["total_pnl_pct"])
    if "live_pnl_pct" in stats:
        return float(stats["live_pnl_pct"])
    return None


def _sprint_backtest_sharpe(sprint_dir):
    """Return the backtest Sharpe claimed at deploy time, or None."""
    meta = os.path.join(sprint_dir, "deployed_strategy.meta.json")
    if not os.path.exists(meta):
        return None
    try:
        with open(meta) as f:
            return float(json.load(f).get("sharpe"))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return None


def _annualise_sharpe(returns, periods_per_year):
    if len(returns) < MIN_SPRINTS_FOR_SHARPE:
        return None
    mean_r = sum(returns) / len(returns)
    var_r = sum((r - mean_r) ** 2 for r in returns) / len(returns)
    std_r = math.sqrt(var_r)
    if std_r == 0:
        return None
    return round(mean_r / std_r * math.sqrt(periods_per_year), 4)


def update(league):
    cfg = LEAGUE_CONFIG.get(league)
    if cfg is None:
        return None

    per_sprint = []
    for d in _sprint_dirs(cfg):
        comp_id = os.path.basename(d)
        pnl = _sprint_pnl_pct(d, cfg["bot"])
        bt  = _sprint_backtest_sharpe(d)
        if pnl is None:
            continue
        per_sprint.append({
            "comp_id": comp_id,
            "live_pnl_pct": round(pnl, 4),
            "backtest_sharpe": bt,
        })

    recent = per_sprint[-WINDOW_SPRINTS:]
    returns = [row["live_pnl_pct"] / 100.0 for row in recent]
    periods_per_year = 365.0 / (cfg["duration_hours"] / 24.0)
    live_sharpe = _annualise_sharpe(returns, periods_per_year)

    bt_samples = [row["backtest_sharpe"] for row in recent if row["backtest_sharpe"] is not None]
    mean_backtest_sharpe = round(sum(bt_samples) / len(bt_samples), 4) if bt_samples else None

    if live_sharpe is not None and mean_backtest_sharpe is not None:
        delta = round(mean_backtest_sharpe - live_sharpe, 4)
    else:
        delta = None

    if delta is None or delta <= 0:
        gate_bonus = 0.0
    elif delta >= MAX_DELTA_FOR_FULL_PENALTY:
        gate_bonus = round(delta, 4)
    else:
        gate_bonus = round(delta * (delta / MAX_DELTA_FOR_FULL_PENALTY), 4)

    # F1: rolling 5-sprint median of live pnl (veto signal) + live_pnl_z.
    veto_window = per_sprint[-VETO_WINDOW_SPRINTS:]
    veto_pnls = [row['live_pnl_pct'] for row in veto_window]
    if len(veto_pnls) >= MIN_SPRINTS_FOR_VETO:
        _sorted = sorted(veto_pnls)
        _n = len(_sorted)
        _mid = _n // 2
        live_pnl_5sprint_median = round(_sorted[_mid] if _n % 2 else (_sorted[_mid-1] + _sorted[_mid]) / 2, 4)
    else:
        live_pnl_5sprint_median = None
    z_window = per_sprint[-Z_WINDOW_SPRINTS:]
    z_pnls = [row['live_pnl_pct'] for row in z_window]
    if len(z_pnls) >= MIN_SPRINTS_FOR_SHARPE:
        _zmean = sum(z_pnls) / len(z_pnls)
        _zvar = sum((p - _zmean) ** 2 for p in z_pnls) / len(z_pnls)
        _zstd = math.sqrt(_zvar)
        if _zstd < 1e-9:
            live_pnl_z = 0.0
        else:
            live_pnl_z = round(_zmean / _zstd, 4)
    else:
        live_pnl_z = 0.0

    out = {
        "league": league,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sprints_seen": len(per_sprint),
        "window_used": len(recent),
        "min_sprints_for_sharpe": MIN_SPRINTS_FOR_SHARPE,
        "live_sharpe_ann": live_sharpe,
        "mean_backtest_sharpe": mean_backtest_sharpe,
        "delta": delta,
        "gate_bonus": gate_bonus,
        "live_pnl_5sprint_median": live_pnl_5sprint_median,
        "live_pnl_z": live_pnl_z,
        "per_sprint": recent,
    }

    out_path = os.path.join(RESEARCH, league, "backtest_drift.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    return out


# F1 (meta_audit 2026-04-25)
def get_live_pnl_z(league):
    """Z-score of recent live PnL distribution. 0.0 if no drift file or insufficient data."""
    path = os.path.join(RESEARCH, league, "backtest_drift.json")
    if not os.path.exists(path):
        return 0.0
    try:
        with open(path) as f:
            return float(json.load(f).get("live_pnl_z") or 0.0)
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return 0.0


def get_veto_signal(league):
    """F1: True if rolling 5-sprint median live_pnl_pct < 0 with >=5 sprints.

    Brand-new champion (<5 sprints history) returns False — blend only, no veto.
    """
    path = os.path.join(RESEARCH, league, "backtest_drift.json")
    if not os.path.exists(path):
        return False
    try:
        with open(path) as f:
            d = json.load(f)
        med = d.get("live_pnl_5sprint_median")
        if med is None:
            return False
        return float(med) < 0.0
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return False


def get_gate_bonus(league):
    """ODIN reads this before declaring a new_best.

    Returns a non-negative Sharpe bonus that a mutation's raw_sharpe must
    exceed on top of the population's current best_sharpe. Defaults to 0.0
    if no drift file exists yet (cold-start)."""
    path = os.path.join(RESEARCH, league, "backtest_drift.json")
    if not os.path.exists(path):
        return 0.0
    try:
        with open(path) as f:
            return float(json.load(f).get("gate_bonus") or 0.0)
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return 0.0


if __name__ == "__main__":
    import sys
    for L in (sys.argv[1:] or list(LEAGUE_CONFIG.keys())):
        r = update(L)
        if r:
            print(f"[{L}] sprints={r['sprints_seen']} "
                  f"live_sharpe={r['live_sharpe_ann']} "
                  f"backtest_sharpe={r['mean_backtest_sharpe']} "
                  f"delta={r['delta']} gate_bonus={r['gate_bonus']}")
        else:
            print(f"[{L}] unknown league")
