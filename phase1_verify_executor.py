#!/usr/bin/env python3
"""phase1_verify_executor.py — auto-fix Phase-1 fixed-sizing cutover problems.

Polls syn_inbox.jsonl for source==phase1_verify entries with severity==error.

Tier 1 (auto):   fixed_sizing flag missing -> set fixed_sizing=True with backups.
Tier 2 (flag):   sprint timing or unknown problems -> pending_review.flag.

State: competition/phase1_verify_executor_state.json
"""
from __future__ import annotations
import argparse, glob as _glob, json, os, re, shutil, sys
from datetime import datetime, timezone, timedelta

WORKSPACE      = "/root/.openclaw/workspace"
COMPETITION    = os.path.join(WORKSPACE, "competition")
SYN_INBOX      = os.path.join(WORKSPACE, "syn_inbox.jsonl")
STATE_FILE     = os.path.join(COMPETITION, "phase1_verify_executor_state.json")
PENDING_REVIEW = os.path.join(COMPETITION, "phase1_verify_pending_review.flag")
TIER2_REVIEW_HRS = 24

LEAGUE_ACTIVE_DIRS = {
    "day":           os.path.join(COMPETITION, "active"),
    "swing":         os.path.join(COMPETITION, "swing", "active"),
    "futures_day":   os.path.join(COMPETITION, "futures_day", "active"),
    "futures_swing": os.path.join(COMPETITION, "futures_swing", "active"),
}

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

def _load_state():
    if not os.path.exists(STATE_FILE): return {"version":1,"processed":{}}
    try:
        with open(STATE_FILE) as f: d = json.load(f)
        d.setdefault("processed",{}); return d
    except (json.JSONDecodeError, OSError): return {"version":1,"processed":{}}

def _read_phase1_errors():
    if not os.path.exists(SYN_INBOX): return []
    rows = []
    try:
        with open(SYN_INBOX) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try: rec = json.loads(line)
                except json.JSONDecodeError: continue
                if rec.get("source")=="phase1_verify" and rec.get("severity")=="error":
                    rows.append(rec)
    except OSError: return []
    rows.sort(key=lambda r: r.get("ts",""))
    return rows

def _alert_id(rec):
    return "phase1_verify:{}".format((rec.get("ts") or "")[:16])

def _parse_missing_flag_leagues(msg):
    leagues = []
    for league in ("day","swing","futures_day","futures_swing","polymarket"):
        if re.search(r"{}[^;]*fixed_sizing missing".format(re.escape(league)), msg):
            leagues.append(league)
    return leagues

def _is_sprint_timing_problem(msg):
    return any(k in msg for k in ("pre-cutover, still running","sprint timing","league reset","backfill"))

def _set_fixed_sizing_meta(league, dry_run):
    active_dir = LEAGUE_ACTIVE_DIRS.get(league)
    if not active_dir or not os.path.isdir(active_dir): return False, "active_dir missing"
    sprints = sorted([d for d in os.listdir(active_dir) if not d.startswith(".")], reverse=True)
    if not sprints: return False, "no sprint dirs"
    meta_path = os.path.join(active_dir, sprints[0], "meta.json")
    if not os.path.exists(meta_path): return False, "meta.json missing"
    try:
        with open(meta_path) as f: meta = json.load(f)
    except Exception as e: return False, "meta.json unreadable: {}".format(e)
    if meta.get("fixed_sizing") is True: return True, "already set"
    if dry_run: return True, "[dry-run] would set"
    bak = meta_path + ".bak_{}".format(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"))
    shutil.copy2(meta_path, bak); meta["fixed_sizing"] = True; _atomic_write_json(meta_path, meta)
    return True, "set in {}/meta.json".format(sprints[0])

def _set_fixed_sizing_portfolios(league, dry_run):
    active_dir = LEAGUE_ACTIVE_DIRS.get(league)
    if not active_dir or not os.path.isdir(active_dir): return 0, "active_dir missing"
    sprints = sorted([d for d in os.listdir(active_dir) if not d.startswith(".")], reverse=True)
    if not sprints: return 0, "no sprint dirs"
    port_files = _glob.glob(os.path.join(active_dir, sprints[0], "portfolio-*.json"))
    fixed_count = 0
    for pf in port_files:
        try:
            with open(pf) as f: p = json.load(f)
            if p.get("fixed_sizing") is True: continue
            if dry_run: fixed_count += 1; continue
            bak = pf + ".bak_{}".format(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"))
            shutil.copy2(pf, bak); p["fixed_sizing"] = True; _atomic_write_json(pf, p); fixed_count += 1
        except Exception as e:
            print("  [phase1_verify_executor] portfolio fix failed {}: {}".format(pf, e), file=sys.stderr)
    return fixed_count, "fixed {}/{}".format(fixed_count, len(port_files))

def _fix_polymarket_fixed_sizing(dry_run):
    state_path = os.path.join(COMPETITION, "polymarket", "auto_state.json")
    if not os.path.exists(state_path): return False, "auto_state.json missing"
    try:
        with open(state_path) as f: s = json.load(f)
        bots = s.get("bots", [])
        if all(b.get("fixed_sizing") is True for b in bots): return True, "already set"
        if dry_run: return True, "[dry-run] would set on {} bots".format(len(bots))
        bak = state_path + ".bak_{}".format(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"))
        shutil.copy2(state_path, bak)
        for b in bots: b["fixed_sizing"] = True
        s["bots"] = bots; _atomic_write_json(state_path, s)
        return True, "set on {} polymarket bots".format(len(bots))
    except Exception as e: return False, "fix failed: {}".format(e)

def _write_pending_review_entry(alert_id, evidence, dry_run):
    if dry_run: print("  [dry-run] pending_review.flag <- {}".format(alert_id)); return
    state = {"entries":[]}
    if os.path.exists(PENDING_REVIEW):
        try:
            with open(PENDING_REVIEW) as f: state = json.load(f)
            state.setdefault("entries",[])
        except Exception: state = {"entries":[]}
    state["entries"] = [e for e in state["entries"] if e.get("alert_id") != alert_id]
    deadline = (datetime.now(timezone.utc) + timedelta(hours=TIER2_REVIEW_HRS)).isoformat()
    state["entries"].append({
        "alert_id": alert_id, "detected_ts": _ts_iso(), "deadline_ts": deadline,
        "evidence": evidence[:600],
        "proposed_action": "Review sprint timing: check if any league has a pre-cutover sprint still running. Use sprint_backfill.py to backfill to 09:00 UTC (2am PST) and rotate to a new sprint with fixed_sizing=True.",
        "revert_note": "No auto-action for sprint timing -- requires human judgment.",
    })
    state["last_updated"] = _ts_iso(); _atomic_write_json(PENDING_REVIEW, state)

def process_alerts(dry_run=False):
    all_errors = _read_phase1_errors()
    if not all_errors:
        print("[phase1_verify_executor] no phase1_verify error entries in syn_inbox")
        return {"processed":0}
    state = _load_state(); now = _now_utc()
    summary = {"tier1_fixed":0,"tier2_flagged":0,"skipped":0}
    latest = {}
    for rec in all_errors:
        aid = _alert_id(rec); ts = _parse_ts(rec.get("ts"))
        if ts and (now-ts).total_seconds()/3600 <= 24:
            if rec.get("ts","") >= latest.get(aid,{}).get("ts",""):
                latest[aid] = rec
    for aid, rec in latest.items():
        if state["processed"].get(aid): summary["skipped"] += 1; continue
        msg = rec.get("msg","")
        print("  [phase1_verify_executor] {}: {}".format(aid, msg[:120]))
        tier1_leagues = _parse_missing_flag_leagues(msg)
        tier2_needed  = _is_sprint_timing_problem(msg)
        unknown       = not tier1_leagues and not tier2_needed
        tier1_results = []
        for league in tier1_leagues:
            if league == "polymarket":
                ok, detail = _fix_polymarket_fixed_sizing(dry_run)
            else:
                ok1, d1 = _set_fixed_sizing_meta(league, dry_run)
                cnt, d2 = _set_fixed_sizing_portfolios(league, dry_run)
                ok, detail = ok1, "meta: {}; portfolios: {}".format(d1, d2)
            tier1_results.append("{}: {}".format(league, detail))
            print("  [{}] fixed_sizing fix -> {}".format(league, detail))
        if tier1_leagues: summary["tier1_fixed"] += len(tier1_leagues)
        if tier2_needed or unknown:
            _write_pending_review_entry(aid, msg[:600], dry_run)
            summary["tier2_flagged"] += 1
        if not dry_run:
            state["processed"][aid] = {"ts":_ts_iso(),"tier1_fixes":tier1_results,"tier2_flagged":tier2_needed or unknown}
    if not dry_run: _atomic_write_json(STATE_FILE, state)
    return summary

def main():
    p = argparse.ArgumentParser(); p.add_argument("--dry-run", action="store_true"); args = p.parse_args()
    print("[phase1_verify_executor] {}  dry_run={}".format(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M UTC"), args.dry_run))
    summary = process_alerts(dry_run=args.dry_run)
    print("[phase1_verify_executor] done. {}".format(json.dumps(summary)))

if __name__ == "__main__": main()
