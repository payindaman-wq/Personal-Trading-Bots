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
import yaml
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


# Sharpe field names in best_strategy.yaml for spot leagues.
SPOT_SHARPE_FIELD = {
    "day":   "_sharpe_24h_median",
    "swing": "_sharpe",
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
    """Return (sharpe, backfilled) from deployed_strategy.meta.json, or (None, False)."""
    meta = os.path.join(sprint_dir, "deployed_strategy.meta.json")
    if not os.path.exists(meta):
        return None, False
    try:
        with open(meta) as f:
            d = json.load(f)
        sharpe = d.get("sharpe")
        backfilled = bool(d.get("_backfilled", False))
        return (float(sharpe) if sharpe is not None else None), backfilled
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return None, False


def _annualise_sharpe(returns, periods_per_year):
    if len(returns) < MIN_SPRINTS_FOR_SHARPE:
        return None
    mean_r = sum(returns) / len(returns)
    var_r = sum((r - mean_r) ** 2 for r in returns) / len(returns)
    std_r = math.sqrt(var_r)
    if std_r == 0:
        return None
    return round(mean_r / std_r * math.sqrt(periods_per_year), 4)


def _read_best_strategy_sharpe(league):
    """Read backtest Sharpe for spot leagues.

    Primary: SPOT_SHARPE_FIELD from best_strategy.yaml.
    Fallback: best_strategy.meta.json.sharpe (same source futures leagues use).
    Returns None only when no champion file exists at all.
    """
    field = SPOT_SHARPE_FIELD.get(league)
    if field is None:
        return None
    yaml_path = os.path.join(RESEARCH, league, "best_strategy.yaml")
    meta_path = os.path.join(RESEARCH, league, "best_strategy.meta.json")
    # Try yaml field first
    if os.path.exists(yaml_path):
        try:
            with open(yaml_path) as f:
                d = yaml.safe_load(f)
            val = d.get(field)
            if val is not None:
                return float(val)
        except Exception:
            pass
    # Fallback to meta.json (present for all spot leagues after ODIN first runs)
    if os.path.exists(meta_path):
        try:
            with open(meta_path) as f:
                val = json.load(f).get("sharpe")
            return float(val) if val is not None else None
        except Exception:
            pass
    return None


def _write_deployed_meta(sprint_dir, sharpe, backfilled=False):
    """Write deployed_strategy.meta.json into sprint_dir. Returns True on success."""
    meta = {"sharpe": sharpe}
    if backfilled:
        meta["_backfilled"] = True
    try:
        with open(os.path.join(sprint_dir, "deployed_strategy.meta.json"), "w") as f:
            json.dump(meta, f, indent=2)
        return True
    except Exception:
        return False


def backfill_spot_leagues():
    """Write deployed_strategy.meta.json into last 10 archived sprint dirs for day + swing.

    Uses current best_strategy.yaml Sharpe as best-effort. Marks files with
    _backfilled: true. Skips dirs that already have the file. Idempotent.
    """
    for league in ("day", "swing"):
        cfg = LEAGUE_CONFIG[league]
        sharpe = _read_best_strategy_sharpe(league)
        if sharpe is None:
            print(f"[backfill][{league}] no sharpe in best_strategy.yaml -- skipping")
            continue
        dirs = _sprint_dirs(cfg)
        candidates = [
            d for d in dirs
            if _sprint_pnl_pct(d, cfg["bot"]) is not None
            and not os.path.exists(os.path.join(d, "deployed_strategy.meta.json"))
        ]
        to_fill = candidates[-10:]
        written = 0
        for d in to_fill:
            if _write_deployed_meta(d, sharpe, backfilled=True):
                written += 1
                print(f"[backfill][{league}] wrote sharpe={sharpe} -> {os.path.basename(d)}")
        print(f"[backfill][{league}] done: {written}/{len(to_fill)} dirs updated")


def update(league):
    cfg = LEAGUE_CONFIG.get(league)
    if cfg is None:
        return None

    per_sprint = []
    for d in _sprint_dirs(cfg):
        comp_id = os.path.basename(d)
        pnl = _sprint_pnl_pct(d, cfg["bot"])
        bt, bt_backfilled = _sprint_backtest_sharpe(d)
        if pnl is None:
            continue
        row = {
            "comp_id": comp_id,
            "live_pnl_pct": round(pnl, 4),
            "backtest_sharpe": bt,
        }
        if bt_backfilled:
            row["_backfilled"] = True
        per_sprint.append(row)

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
    args = sys.argv[1:]
    if "--backfill" in args:
        backfill_spot_leagues()
        args = [a for a in args if a != "--backfill"]
    for L in (args or list(LEAGUE_CONFIG.keys())):
        r = update(L)
        if r:
            print(f"[{L}] sprints={r['sprints_seen']} "
                  f"live_sharpe={r['live_sharpe_ann']} "
                  f"backtest_sharpe={r['mean_backtest_sharpe']} "
                  f"delta={r['delta']} gate_bonus={r['gate_bonus']}")
        else:
            print(f"[{L}] unknown league")
