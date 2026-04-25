#!/usr/bin/env python3
import argparse, glob, json, os, statistics, subprocess
from datetime import datetime, timezone
import yaml

WORKSPACE = "/root/.openclaw/workspace"
RESEARCH  = os.path.join(WORKSPACE, "research")
COMP      = os.path.join(WORKSPACE, "competition")
LOG_DIR   = os.path.join(RESEARCH, "league_killswitch")
LOG_FILE  = os.path.join(LOG_DIR, "killswitch.log")
INBOX     = os.path.join(WORKSPACE, "syn_inbox.jsonl")
FLAG_DIR  = LOG_DIR
ALL_LEAGUES = ("day", "swing", "futures_day", "futures_swing")
F2_MEDIAN_PNL_FLOOR    = -0.5
F2_CHAMPION_SHARPE_CAP = 0.0
F2_MIN_SPRINT_SAMPLES  = 3
MC_GENS_FLOOR    = 1500
MC_UNIQUE_SHARPE = 1
SPRINT_WINDOW    = 5

def _ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _log(msg, dry_run=False):
    os.makedirs(LOG_DIR, exist_ok=True)
    prefix = "[DRY-RUN] " if dry_run else ""
    line = "[" + _ts() + "] " + prefix + msg
    print(line)
    if not dry_run:
        try:
            with open(LOG_FILE, "a") as f:
                f.write(line + "\n")
        except OSError:
            pass

def _inbox(severity, msg, league, reason, dry_run=False):
    if dry_run:
        print("  [DRY-RUN] syn_inbox: " + severity + " " + repr(msg[:80]))
        return
    rec = {"ts": _ts(), "source": "league_killswitch", "severity": severity,
           "league": league, "reason": reason, "msg": msg}
    try:
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError as e:
        _log("inbox write failed: " + str(e))

def league_pause_flag(league):
    return os.path.join(COMP, league, "league_paused.flag")

def is_paused(league):
    return os.path.exists(league_pause_flag(league))

def _load_drift(league):
    path = os.path.join(RESEARCH, league, "backtest_drift.json")
    if not os.path.exists(path): return None
    try:
        with open(path) as f: return json.load(f)
    except (json.JSONDecodeError, OSError): return None

def _champion_sharpe(league):
    path = os.path.join(RESEARCH, league, "best_strategy.meta.json")
    if not os.path.exists(path): return None
    try: return json.load(open(path)).get("sharpe")
    except (json.JSONDecodeError, OSError): return None

def _unique_sharpe(league):
    sharpes = set()
    for f in glob.glob(os.path.join(RESEARCH, league, "population", "elite_*.yaml")):
        try:
            d = yaml.safe_load(open(f))
            s = d.get("_sharpe")
            if s is not None: sharpes.add(round(float(s), 4))
        except Exception: pass
    return len(sharpes)

def _gens_since_best(league):
    path = os.path.join(RESEARCH, league, "gen_state.json")
    if not os.path.exists(path): return None
    try: return json.load(open(path)).get("gens_since_best")
    except (json.JSONDecodeError, OSError): return None

def evaluate(league):
    drift = _load_drift(league)
    champ_sharpe = _champion_sharpe(league)
    f2_stats = {}
    f2_fired = False
    f2_reason = ""
    if drift is not None and champ_sharpe is not None:
        per = drift.get("per_sprint") or []
        window = per[-SPRINT_WINDOW:]
        pnls = [r["live_pnl_pct"] for r in window if r.get("live_pnl_pct") is not None]
        median_pnl = statistics.median(pnls) if len(pnls) >= F2_MIN_SPRINT_SAMPLES else None
        f2_stats = {
            "champion_backtest_sharpe": champ_sharpe,
            "live_pnl_median_5sprint":  round(median_pnl, 4) if median_pnl is not None else None,
            "sprint_samples": len(pnls),
            "per_pnl": [round(p, 4) for p in pnls],
        }
        if (median_pnl is not None and median_pnl < F2_MEDIAN_PNL_FLOOR
                and champ_sharpe < F2_CHAMPION_SHARPE_CAP):
            f2_fired = True
            f2_reason = ("F2: live_pnl_median=" + format(median_pnl, ".4f")
                         + "%<" + str(F2_MEDIAN_PNL_FLOOR)
                         + "%, champion_sharpe=" + format(champ_sharpe, ".4f") + "<0")
    gsb = _gens_since_best(league)
    usharpe = _unique_sharpe(league)
    mc_stats = {"gens_since_best": gsb, "unique_sharpe": usharpe}
    mc_fired = False
    mc_reason = ""
    if gsb is not None and gsb > MC_GENS_FLOOR and usharpe == MC_UNIQUE_SHARPE:
        mc_fired = True
        mc_reason = ("mode-collapse: gens_since_best=" + str(gsb)
                     + ">" + str(MC_GENS_FLOOR)
                     + ", unique_sharpe=" + str(usharpe) + "==1")
    stats = {**f2_stats, **mc_stats}
    if f2_fired: return True, "F2", f2_reason, stats
    if mc_fired: return True, "mode-collapse", mc_reason, stats
    diag = []
    if drift is None: diag.append("F2_skip(no_drift)")
    elif champ_sharpe is None: diag.append("F2_skip(no_meta)")
    else:
        med = f2_stats.get("live_pnl_median_5sprint")
        n   = f2_stats.get("sprint_samples", 0)
        diag.append("F2_clear(median=" + str(med) + "%,n=" + str(n)
                    + ",sharpe=" + format(champ_sharpe, ".4f") + ")")
    diag.append("collapse_clear(gsb=" + str(gsb) + ",unique=" + str(usharpe) + ")")
    return False, "", "; ".join(diag), stats

def _stop_service(league, dry_run):
    svc = "odin_" + league + ".service"
    for cmd in [["systemctl", "stop", svc], ["systemctl", "disable", svc]]:
        if dry_run:
            print("  [DRY-RUN] would run: " + " ".join(cmd))
        else:
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if r.returncode != 0:
                    _log(" ".join(cmd) + " rc=" + str(r.returncode) + ": " + r.stderr.strip())
            except (subprocess.TimeoutExpired, OSError) as e:
                _log(" ".join(cmd) + " failed: " + str(e))

def apply(league, dry_run=False):
    if is_paused(league):
        _log(league + ": already paused (flag exists) -- skip", dry_run=dry_run)
        return
    should_kill, criteria, reason, stats = evaluate(league)
    if not should_kill:
        _log(league + ": healthy -- " + reason, dry_run=dry_run)
        return
    _log(league + ": KILL TRIGGERED (" + criteria + ") -- " + reason, dry_run=dry_run)
    _stop_service(league, dry_run)
    flag_path = league_pause_flag(league)
    if dry_run:
        print("  [DRY-RUN] would write " + flag_path)
    else:
        payload = {
            "paused_at":        _ts(),
            "league":           league,
            "criteria_matched": criteria,
            "reason":           reason,
            "stats":            stats,
            "resume_command":   ("rm " + flag_path + " && "
                                  "systemctl enable odin_" + league + ".service && "
                                  "systemctl start odin_" + league + ".service"),
        }
        os.makedirs(os.path.dirname(flag_path), exist_ok=True)
        with open(flag_path, "w") as f:
            json.dump(payload, f, indent=2)
        _log(league + ": wrote " + flag_path)
    _inbox(
        "critical",
        "[SYN/league_killswitch] " + league + " paused (" + criteria + "): " + reason
        + ". Resume: rm " + flag_path + " then systemctl enable+start odin_" + league + ".service",
        league, reason, dry_run=dry_run,
    )

def replay_f2(league):
    drift = _load_drift(league)
    champ_sharpe = _champion_sharpe(league)
    if drift is None:
        print("  " + league + ": no backtest_drift.json -- skip"); return
    if champ_sharpe is None:
        print("  " + league + ": no best_strategy.meta.json -- skip"); return
    per = drift.get("per_sprint") or []
    if len(per) < SPRINT_WINDOW:
        print("  " + league + ": only " + str(len(per)) + " sprints, need " + str(SPRINT_WINDOW) + " -- skip"); return
    print("  " + league + ": champion_sharpe=" + format(champ_sharpe, ".4f") + ", " + str(len(per)) + " total sprints")
    first_fire = None
    for i in range(SPRINT_WINDOW - 1, len(per)):
        window = per[i - SPRINT_WINDOW + 1 : i + 1]
        pnls = [r["live_pnl_pct"] for r in window if r.get("live_pnl_pct") is not None]
        if len(pnls) < F2_MIN_SPRINT_SAMPLES: continue
        median_pnl = statistics.median(pnls)
        comp_id = per[i].get("comp_id", "sprint_" + str(i))
        fire = median_pnl < F2_MEDIAN_PNL_FLOOR and champ_sharpe < F2_CHAMPION_SHARPE_CAP
        marker = "  *** WOULD FIRE ***" if fire else ""
        print("    [" + comp_id + "] median=" + format(median_pnl, ".4f") + "% sharpe=" + format(champ_sharpe, ".4f") + marker)
        if fire and first_fire is None: first_fire = comp_id
    if first_fire: print("  " + league + ": F2 first fires at sprint " + first_fire)
    else: print("  " + league + ": F2 never fires in replay window")

def main():
    parser = argparse.ArgumentParser(description="League killswitch -- all 4 leagues")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    if args.replay:
        print("=== F10 Historical F2 Replay [" + _ts() + "] ===")
        for league in ALL_LEAGUES:
            print("\n--- " + league + " ---")
            replay_f2(league)
        return
    if args.dry_run:
        print("=== DRY-RUN [" + _ts() + "] ===")
    for league in ALL_LEAGUES:
        apply(league, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
