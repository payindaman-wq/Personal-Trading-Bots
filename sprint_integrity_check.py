#!/usr/bin/env python3
"""
sprint_integrity_check.py — SYN verifies sprint counts across all 5 leagues.

Detects:
  • cycle_state.sprints length != sprint_in_cycle (counter drift)
  • sprints listed in cycle_state missing their results directory (phantom sprint)
  • orphan sprint dirs in results/ not in cycle_state.sprints (un-archived)
  • completed-cycle archive directory missing (cycle N>1 but archive/cycle-(N-1) absent)
  • active/ dir contains more than one sprint

On anomaly:
  1. appends alert to syn_inbox.jsonl (Mimir sees it)
  2. queues fix task in research/loki_pending_actions.jsonl (LOKI applies repair)
  3. logs detection to maintenance_log.jsonl (dashboard Maintenance tab)

Invoked by league_watchdog.py every 10 min.
"""
import json
import os
from datetime import datetime, timezone

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
SYN_INBOX = os.path.join(WORKSPACE, "syn_inbox.jsonl")
LOKI_PENDING = os.path.join(WORKSPACE, "research", "loki_pending_actions.jsonl")
MAINTENANCE_LOG = os.path.join(WORKSPACE, "maintenance_log.jsonl")
STATE_FILE = os.path.join(WORKSPACE, "competition", "sprint_integrity_state.json")

LEAGUES = [
    {
        "name": "day",
        "cycle_state": os.path.join(WORKSPACE, "competition", "cycle_state.json"),
        "results_dir": os.path.join(WORKSPACE, "competition", "results"),
        "active_dir": os.path.join(WORKSPACE, "competition", "active"),
        "archive_root": os.path.join(WORKSPACE, "competition", "archive"),
        "archive_pattern": "cycle-{n}",
        "is_score_file_archive": False,
    },
    {
        "name": "swing",
        "cycle_state": os.path.join(WORKSPACE, "competition", "swing", "swing_cycle_state.json"),
        "results_dir": os.path.join(WORKSPACE, "competition", "swing", "results"),
        "active_dir": os.path.join(WORKSPACE, "competition", "swing", "active"),
        "archive_root": os.path.join(WORKSPACE, "competition", "swing", "archive"),
        "archive_pattern": "cycle-{n}",
        "is_score_file_archive": False,
    },
    {
        "name": "futures_day",
        "cycle_state": os.path.join(WORKSPACE, "competition", "futures_day", "cycle_state.json"),
        "results_dir": os.path.join(WORKSPACE, "competition", "futures_day", "results"),
        "active_dir": os.path.join(WORKSPACE, "competition", "futures_day", "active"),
        "archive_root": None,
        "archive_pattern": None,
        "is_score_file_archive": True,
    },
    {
        "name": "futures_swing",
        "cycle_state": os.path.join(WORKSPACE, "competition", "futures_swing", "cycle_state.json"),
        "results_dir": os.path.join(WORKSPACE, "competition", "futures_swing", "results"),
        "active_dir": os.path.join(WORKSPACE, "competition", "futures_swing", "active"),
        "archive_root": None,
        "archive_pattern": None,
        "is_score_file_archive": True,
    },
    {
        "name": "polymarket",
        "cycle_state": os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_cycle_state.json"),
        "results_dir": os.path.join(WORKSPACE, "competition", "polymarket", "auto_results"),
        "active_dir": None,
        "active_state_file": os.path.join(WORKSPACE, "competition", "polymarket", "auto_state.json"),
        "archive_root": os.path.join(WORKSPACE, "competition", "polymarket", "sprint_results"),
        "archive_pattern": "cycle_{n}_archive",
        "is_score_file_archive": True,
    },
]


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def list_sprint_dirs(path):
    if not path or not os.path.isdir(path):
        return []
    out = []
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if os.path.isdir(full) and not name.endswith("_archive") and not name.startswith("cycle"):
            out.append(name)
    return sorted(out)


def sprint_has_results(league_cfg, sprint_id):
    """Check if sprint has its result artifact on disk — active sprint counts too."""
    rdir = league_cfg["results_dir"]
    adir = league_cfg.get("active_dir")
    active_state = league_cfg.get("active_state_file")
    if adir and os.path.isdir(os.path.join(adir, sprint_id)):
        return True
    if active_state:
        st = load_json(active_state)
        if st and st.get("sprint_id") == sprint_id:
            return True
    if os.path.isdir(os.path.join(rdir, sprint_id)):
        return True
    archive_root = league_cfg.get("archive_root")
    if archive_root and os.path.isdir(archive_root):
        for sub in os.listdir(archive_root):
            full = os.path.join(archive_root, sub)
            if os.path.isdir(full) and os.path.isdir(os.path.join(full, sprint_id)):
                return True
    if league_cfg["is_score_file_archive"]:
        score = os.path.join(rdir, f"{sprint_id}_score.json")
        auto = os.path.join(rdir, f"{sprint_id}_auto.json")
        if os.path.isfile(score) or os.path.isfile(auto):
            return True
        return False
    return os.path.isdir(os.path.join(rdir, sprint_id + "_portfolios"))


def check_league(cfg):
    anomalies = []
    state = load_json(cfg["cycle_state"])
    name = cfg["name"]

    if not state:
        return [{"league": name, "kind": "cycle_state_missing", "detail": f"{cfg['cycle_state']} unreadable"}]

    sprints = state.get("sprints", [])
    sprint_in_cycle = state.get("sprint_in_cycle", 0)
    cycle = state.get("cycle", 1)
    status = state.get("status", "active")

    if len(sprints) != sprint_in_cycle:
        anomalies.append({
            "league": name,
            "kind": "counter_drift",
            "detail": f"sprints[] has {len(sprints)} entries but sprint_in_cycle={sprint_in_cycle}",
            "fix_hint": "sync sprint_in_cycle = len(sprints)",
        })

    for sid in sprints:
        if not sprint_has_results(cfg, sid):
            anomalies.append({
                "league": name,
                "kind": "phantom_sprint",
                "detail": f"cycle_state references {sid} but no results artifact found",
                "sprint_id": sid,
                "fix_hint": "remove from sprints[] or restore results",
            })

    if cfg["active_dir"]:
        actives = list_sprint_dirs(cfg["active_dir"])
        if len(actives) > 1:
            anomalies.append({
                "league": name,
                "kind": "multiple_active",
                "detail": f"active/ contains {len(actives)} sprints: {actives}",
                "fix_hint": "archive stale active sprint dirs",
            })

    if cfg["archive_root"] and cfg["archive_pattern"] and cycle > 1:
        for n in range(1, cycle):
            sub = cfg["archive_pattern"].format(n=n)
            full = os.path.join(cfg["archive_root"], sub)
            if not os.path.isdir(full):
                anomalies.append({
                    "league": name,
                    "kind": "missing_archive_cycle",
                    "detail": f"cycle={cycle} but {cfg['archive_root']}/{sub} missing — prior cycle not archived",
                    "missing_cycle": n,
                    "fix_hint": f"move results/ sprints for cycle {n} into {sub}",
                })

    if cfg["archive_root"] and cfg["archive_pattern"] and name in ("day", "swing"):
        current_cycle_sprints = set(sprints)
        orphans = [s for s in list_sprint_dirs(cfg["results_dir"]) if s not in current_cycle_sprints]
        if orphans:
            anomalies.append({
                "league": name,
                "kind": "orphan_results",
                "detail": f"results/ holds {len(orphans)} sprint dirs not in current cycle: {orphans[:3]}{'...' if len(orphans) > 3 else ''}",
                "orphan_ids": orphans,
                "fix_hint": "move orphan sprint dirs into archive/cycle-N/ matching their cycle",
            })

    return anomalies


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"seen": {}}


def save_state(st):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(st, f, indent=2)


def anomaly_key(a):
    return f"{a['league']}|{a['kind']}|{a.get('sprint_id','')}|{a.get('missing_cycle','')}"


def append_jsonl(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "a") as f:
        f.write(json.dumps(obj) + "\n")


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
    state = load_state()
    seen = state.get("seen", {})

    all_anoms = []
    for cfg in LEAGUES:
        all_anoms.extend(check_league(cfg))

    new_anoms = []
    for a in all_anoms:
        k = anomaly_key(a)
        if k not in seen:
            new_anoms.append(a)
            seen[k] = now

    still_active = {anomaly_key(a) for a in all_anoms}
    seen = {k: v for k, v in seen.items() if k in still_active}

    if new_anoms:
        # Split: LOKI auto-fixable vs requires human review. Only human-review anomalies
        # go to SYN_INBOX with severity=error (Telegram alert). Auto-fixable kinds are
        # handled silently by LOKI; dashboard Maintenance tab still sees them via MAINTENANCE_LOG.
        AUTO_FIXABLE_KINDS = {"counter_drift", "multiple_active", "missing_archive_cycle", "orphan_results"}
        human_anoms = [a for a in new_anoms if a.get("kind") not in AUTO_FIXABLE_KINDS]

        if human_anoms:
            human_summary = "; ".join(f"{a['league']}:{a['kind']}" for a in human_anoms[:5])
            append_jsonl(SYN_INBOX, {
                "ts": now,
                "source": "sprint_integrity",
                "severity": "error",
                "msg": f"[SYN] sprint integrity needs human review ({len(human_anoms)}): {human_summary}",
                "anomalies": human_anoms,
            })

        append_jsonl(LOKI_PENDING, {
            "ts": now,
            "source": "sprint_integrity",
            "league": "multi",
            "actions": [{
                "type": "sprint_integrity_fix",
                "anomalies": new_anoms,
            }],
        })

        for a in new_anoms:
            append_jsonl(MAINTENANCE_LOG, {
                "ts": now,
                "phase": "detected",
                "source": "SYN",
                "league": a["league"],
                "kind": a["kind"],
                "detail": a["detail"],
                "fix_hint": a.get("fix_hint", ""),
            })

        print(f"[sprint_integrity] {len(new_anoms)} new anomaly/ies queued for LOKI ({len(human_anoms)} need human review)")
        for a in new_anoms:
            print(f"  {a['league']}/{a['kind']}: {a['detail']}")
    else:
        if all_anoms:
            print(f"[sprint_integrity] {len(all_anoms)} anomaly/ies still open (already reported)")
        else:
            print("[sprint_integrity] OK — all leagues consistent")

    state["seen"] = seen
    state["last_check"] = now
    save_state(state)


if __name__ == "__main__":
    main()
