#!/usr/bin/env python3
"""
odin_health_executor.py
"""
from __future__ import annotations
import argparse, json, os, sys
from datetime import datetime, timezone, timedelta

WORKSPACE    = "/root/.openclaw/workspace"
RESEARCH     = os.path.join(WORKSPACE, "research")
COMPETITION  = os.path.join(WORKSPACE, "competition")
STATE_FILE   = os.path.join(COMPETITION, "odin_health_executor_state.json")
SYN_INBOX    = os.path.join(WORKSPACE, "syn_inbox.jsonl")

STALL_GENS         = 1500
STALE_HRS          = 6.0
COOLDOWN_HRS       = 6.0
INJECT_WINDOW_DAYS = 7
INJECT_TIER2_COUNT = 3

ACTIVE_LEAGUES      = ["day", "swing", "futures_day", "futures_swing"]
SUCCESSFUL_STATUSES = {"new_best", "discarded", "rejected_lookahead"}

def _ts_iso(): return datetime.now(timezone.utc).isoformat()
def _now_utc(): return datetime.now(timezone.utc)

def _parse_ts(s):
    if not s: return None
    try:
        dt = datetime.fromisoformat(s.replace("Z","+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError): return None

def _atomic_write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp,"w") as f: json.dump(obj, f, indent=2); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)

def _append_jsonl(path, rec):
    d = os.path.dirname(path)
    if d: os.makedirs(d, exist_ok=True)
    with open(path,"a") as f: f.write(json.dumps(rec)+"\n")

def _load_state():
    if not os.path.exists(STATE_FILE): return {"version":1,"leagues":{}}
    try:
        with open(STATE_FILE) as f: d = json.load(f)
        d.setdefault("leagues",{}); return d
    except (json.JSONDecodeError, OSError): return {"version":1,"leagues":{}}

def _league_entry(state, league):
    if league not in state["leagues"]:
        state["leagues"][league] = {"last_action_ts":None,"last_action_reason":None,"injections_7d":[]}
    return state["leagues"][league]

def _best_sharpe_from_results(results_path):
    best = None
    try:
        with open(results_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("gen"): continue
                parts = line.split("\t")
                if len(parts) >= 2:
                    try:
                        s = float(parts[1])
                        if best is None or s > best: best = s
                    except ValueError: pass
    except OSError: pass
    return best

def _check_stall(league):
    league_dir   = os.path.join(RESEARCH, league)
    state_path   = os.path.join(league_dir, "gen_state.json")
    results_path = os.path.join(league_dir, "results.tsv")
    if not os.path.exists(state_path) or not os.path.exists(results_path):
        return False, None, 0, None
    try:
        with open(state_path) as f: gs = json.load(f)
    except (json.JSONDecodeError, OSError): return False, None, 0, None
    gens_since_best = gs.get("gens_since_best", 0)
    best_sharpe = _best_sharpe_from_results(results_path)
    if gens_since_best > STALL_GENS:
        return True, "gens_since_best={}".format(gens_since_best), gens_since_best, best_sharpe
    last_success_ts = None
    try:
        with open(results_path) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("gen")]
        for line in lines:
            parts = line.split("\t")
            if len(parts) >= 8 and parts[5] in SUCCESSFUL_STATUSES:
                last_success_ts = parts[7]
    except OSError: return False, None, gens_since_best, best_sharpe
    if last_success_ts:
        try:
            last_dt = datetime.fromisoformat(last_success_ts).replace(tzinfo=timezone.utc)
            age_h = (_now_utc() - last_dt).total_seconds() / 3600
            if age_h > STALE_HRS:
                return True, "no_successful_gen_{:.1f}h".format(age_h), gens_since_best, best_sharpe
        except ValueError: pass
    return False, None, gens_since_best, best_sharpe

def _trigger_diversity_injection(league, dry_run):
    league_dir  = os.path.join(RESEARCH, league)
    signal_path = os.path.join(league_dir, "diversity_inject_signal")
    state_path  = os.path.join(league_dir, "gen_state.json")
    if dry_run:
        print("  [dry-run] would write {}".format(signal_path)); return True
    try:
        with open(signal_path,"w") as f: f.write("written by odin_health_executor at {}\n".format(_ts_iso()))
    except OSError as e:
        print("  [odin_health_executor] signal write failed for {}: {}".format(league, e), file=sys.stderr)
        return False
    if os.path.exists(state_path):
        try:
            with open(state_path) as f: gs = json.load(f)
            gs["diversity_injected_this_stall"] = False
            _atomic_write_json(state_path, gs)
        except Exception as e:
            print("  [odin_health_executor] gen_state reset failed for {}: {}".format(league, e), file=sys.stderr)
    return True

def _write_pending_review(league, evidence, injections_7d, dry_run):
    flag_path = os.path.join(COMPETITION, league, "odin_pending_review.flag")
    if dry_run: print("  [dry-run] would write {}".format(flag_path)); return
    os.makedirs(os.path.dirname(flag_path), exist_ok=True)
    deadline = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    _atomic_write_json(flag_path, {
        "source": "odin_health_executor", "league": league,
        "detected_ts": _ts_iso(), "deadline_ts": deadline,
        "finding": "{} diversity injections in {}d with no Sharpe improvement".format(INJECT_TIER2_COUNT, INJECT_WINDOW_DAYS),
        "evidence": evidence,
        "proposed_action": "Full population reset for {}: delete elite_0..elite_N and reseed. Review research/{}/program.md for paradigm-level issues first.".format(league, league),
        "revert_note": "Population reset is Tier 2 (capital-adjacent). Human ack required.",
        "injections_7d": injections_7d,
    })

def _is_tier2_triggered(injections_7d, current_best_sharpe):
    now = _now_utc(); cutoff = now - timedelta(days=INJECT_WINDOW_DAYS)
    recent = [e for e in injections_7d if _parse_ts(e.get("ts")) and _parse_ts(e.get("ts")) > cutoff]
    if len(recent) < INJECT_TIER2_COUNT: return False, ""
    first_sharpe = recent[0].get("best_sharpe")
    if first_sharpe is not None and current_best_sharpe is not None and current_best_sharpe <= first_sharpe:
        return True, "{} injections in 7d; first_sharpe={:.4f} current={:.4f} (no improvement)".format(len(recent), first_sharpe, current_best_sharpe)
    return False, ""

def process_leagues(dry_run=False):
    state = _load_state(); now = _now_utc()
    summary = {"checked":0,"injected":0,"tier2_flagged":0,"skipped_cooldown":0,"no_stall":0}
    for league in ACTIVE_LEAGUES:
        summary["checked"] += 1
        stall, reason, gens_since_best, best_sharpe = _check_stall(league)
        if not stall:
            summary["no_stall"] += 1
            print("  [{}] ok (gens_since_best={})".format(league, gens_since_best)); continue
        entry = _league_entry(state, league)
        last_action = _parse_ts(entry.get("last_action_ts"))
        if last_action and (now - last_action).total_seconds() / 3600 < COOLDOWN_HRS:
            summary["skipped_cooldown"] += 1
            print("  [{}] stall ({}) cooldown {:.1f}h".format(league, reason, (now-last_action).total_seconds()/3600)); continue
        print("  [{}] stall: {} -- triggering diversity re-injection".format(league, reason))
        ok = _trigger_diversity_injection(league, dry_run)
        if not ok: continue
        summary["injected"] += 1
        if not dry_run:
            entry["last_action_ts"] = _ts_iso(); entry["last_action_reason"] = reason
            entry["injections_7d"].append({"ts": _ts_iso(), "best_sharpe": best_sharpe})
            cutoff_str = (now - timedelta(days=INJECT_WINDOW_DAYS)).isoformat()
            entry["injections_7d"] = [e for e in entry["injections_7d"] if (e.get("ts") or "") >= cutoff_str]
        tier2, evidence = _is_tier2_triggered(entry.get("injections_7d",[]), best_sharpe)
        if tier2:
            print("  [{}] Tier 2: {}".format(league, evidence))
            _write_pending_review(league, evidence, entry.get("injections_7d",[]), dry_run)
            if not dry_run:
                _append_jsonl(SYN_INBOX, {"ts":_ts_iso(),"source":"odin_health_executor","severity":"info","league":league,
                    "msg":"[OPS/odin_health_executor] {}: Tier 2 -- {}. Pending review flag written.".format(league, evidence)})
            summary["tier2_flagged"] += 1
    if not dry_run: _atomic_write_json(STATE_FILE, state)
    return summary

def main():
    p = argparse.ArgumentParser(); p.add_argument("--dry-run", action="store_true"); args = p.parse_args()
    print("[odin_health_executor] {}  dry_run={}".format(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M UTC"), args.dry_run))
    summary = process_leagues(dry_run=args.dry_run)
    print("[odin_health_executor] done. {}".format(json.dumps(summary)))

if __name__ == "__main__": main()
