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


    # cycle_state_wiped: cycle>1 + empty sprints[] + no cycle_started_at, but an
    # active sprint or recent score file exists. LOKI inline-advance or manual
    # reset left the counter orphaned from reality.
    if cycle > 1 and len(sprints) == 0 and state.get("cycle_started_at") in (None, ""):
        live_active = []
        if cfg.get("active_dir") and os.path.isdir(cfg["active_dir"]):
            live_active = list_sprint_dirs(cfg["active_dir"])
        has_recent_score = False
        recent_score_id = None
        if cfg["is_score_file_archive"] and os.path.isdir(cfg["results_dir"]):
            score_files = sorted(
                [f for f in os.listdir(cfg["results_dir"]) if f.endswith("_score.json") or f.endswith("_auto.json")],
                key=lambda f: os.path.getmtime(os.path.join(cfg["results_dir"], f)),
                reverse=True,
            )
            if score_files:
                has_recent_score = True
                recent_score_id = score_files[0].rsplit("_", 1)[0]
        if live_active or has_recent_score:
            detail_bits = []
            if live_active:
                detail_bits.append(f"active has {live_active}")
            if recent_score_id:
                detail_bits.append(f"latest score {recent_score_id}")
            anomalies.append({
                "league": name,
                "kind": "cycle_state_wiped",
                "detail": f"cycle={cycle} sprints=[] cycle_started_at=null but reality disagrees: " + "; ".join(detail_bits),
                "fix_hint": "reseed sprints[] from live active + recent score files; set cycle_started_at from meta.json",
            })

    # futures score-file orphan check: count score files produced since cycle_started_at
    # and compare to len(sprints). Missing entries => sprint started but never recorded.
    if cfg["is_score_file_archive"] and name in ("futures_day", "futures_swing") and state.get("cycle_started_at"):
        try:
            from datetime import datetime as _dt
            cs_ts = _dt.fromisoformat(state["cycle_started_at"].replace("Z", "+00:00"))
            cs_epoch = cs_ts.timestamp()
            if os.path.isdir(cfg["results_dir"]):
                # 5-min buffer: score files archived right at the cycle boundary
                # belong to the PREVIOUS cycle; strict > with buffer avoids false positives.
                BOUNDARY_BUFFER_SEC = 300
                recent_scores = [
                    f for f in os.listdir(cfg["results_dir"])
                    if (f.endswith("_score.json") or f.endswith("_auto.json"))
                    and os.path.getmtime(os.path.join(cfg["results_dir"], f)) > cs_epoch + BOUNDARY_BUFFER_SEC
                ]
                expected = len(recent_scores) + (len(list_sprint_dirs(cfg["active_dir"])) if cfg.get("active_dir") else 0)
                if expected > len(sprints) and expected - len(sprints) >= 1:
                    anomalies.append({
                        "league": name,
                        "kind": "undercount_vs_results",
                        "detail": f"sprints[] has {len(sprints)} but {len(recent_scores)} score files + active imply {expected} since cycle_started_at",
                        "fix_hint": "rebuild sprints[] from score files dated >= cycle_started_at + active dirs",
                    })
        except Exception:
            pass

    # cycle_regressed: cycle_state.cycle lower than evidenced by archive directories.
    # Scoped to day/swing only — futures uses score-file archives (no cycle dirs),
    # and polymarket's cycle_1_archive contains retired-fleet legacy data that would
    # false-positive. Catches the repeated swing/day cycle-counter reset pattern.
    if name in ("day", "swing") and cfg["archive_root"] and cfg["archive_pattern"] and os.path.isdir(cfg["archive_root"]):
        max_archived_cycle = 0
        for sub in os.listdir(cfg["archive_root"]):
            full = os.path.join(cfg["archive_root"], sub)
            if not os.path.isdir(full):
                continue
            if sub.startswith("cycle-") or sub.startswith("cycle_"):
                # Extract N from cycle-N, cycle-N-overflow, cycle_N_archive
                token = sub.replace("cycle-", "").replace("cycle_", "").split("-")[0].split("_")[0]
                try:
                    n = int(token)
                    max_archived_cycle = max(max_archived_cycle, n)
                except ValueError:
                    pass
        # Active cycle must be > max_archived_cycle. If equal or less, the counter has regressed.
        if max_archived_cycle >= cycle:
            anomalies.append({
                "league": name,
                "kind": "cycle_regressed",
                "detail": f"cycle_state.cycle={cycle} but archive/ has cycle-{max_archived_cycle} present — counter regressed",
                "fix_hint": f"set cycle to {max_archived_cycle + 1} and reseed sprints[] from current-cycle entries in results/ + active/",
            })

    # duplicate_day_sprints: same YYYYMMDD date has multiple entries in sprints[] AND
    # at least one of them is a zombie (lacks final_score.json AND is not the live sprint).
    # Legitimate same-day entries (one archived + one currently live) are skipped.
    date_groups = {}
    for sid in sprints:
        parts = sid.split("-")
        for part in parts:
            if len(part) == 8 and part.isdigit():
                date_groups.setdefault(part, []).append(sid)
                break
    live_set = set()
    if cfg.get("active_dir") and os.path.isdir(cfg["active_dir"]):
        live_set = set(list_sprint_dirs(cfg["active_dir"]))
    zombie_dates = []
    zombie_sprints = []
    for date, sids in date_groups.items():
        if len(sids) <= 1:
            continue
        for sid in sids:
            if sid in live_set:
                continue  # live sprint, not a zombie
            # Check for final_score.json in results dir or archive dirs
            has_score = False
            for candidate in [os.path.join(cfg["results_dir"], sid, "final_score.json"),
                              os.path.join(cfg["results_dir"], sid + "_portfolios", "final_score.json")]:
                if os.path.isfile(candidate):
                    has_score = True
                    break
            if not has_score and cfg.get("archive_root") and os.path.isdir(cfg["archive_root"]):
                for sub in os.listdir(cfg["archive_root"]):
                    full = os.path.join(cfg["archive_root"], sub)
                    if not os.path.isdir(full):
                        continue
                    for cand in [os.path.join(full, sid, "final_score.json"),
                                 os.path.join(full, sid + "_portfolios", "final_score.json")]:
                        if os.path.isfile(cand):
                            has_score = True
                            break
                    if has_score:
                        break
            # Score-file archive model (futures/polymarket)
            if not has_score and cfg.get("is_score_file_archive"):
                for cand in [os.path.join(cfg["results_dir"], sid + "_score.json"),
                             os.path.join(cfg["results_dir"], sid + "_auto.json")]:
                    if os.path.isfile(cand):
                        has_score = True
                        break
            if not has_score:
                zombie_dates.append(date)
                zombie_sprints.append(sid)
    if zombie_sprints:
        anomalies.append({
            "league": name,
            "kind": "duplicate_day_sprints",
            "detail": f"sprints[] has zombie entries on date(s) {sorted(set(zombie_dates))}: {zombie_sprints} — no final_score/score_json, not live",
            "zombie_sprints": zombie_sprints,
            "fix_hint": "remove zombie sprint_ids from sprints[] and decrement sprint_in_cycle",
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
        AUTO_FIXABLE_KINDS = {"counter_drift", "multiple_active", "missing_archive_cycle", "orphan_results", "cycle_regressed", "duplicate_day_sprints"}
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
