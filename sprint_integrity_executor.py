#!/usr/bin/env python3
"""
sprint_integrity_executor.py — auto-heal layer for sprint_integrity anomalies.

Polls syn_inbox.jsonl for source=="sprint_integrity" entries and applies
deterministic fixes based on anomaly kind:

  Tier 1 (auto):   cycle_regressed, undercount_vs_results
                   — backup JSON, apply fix, re-verify; revert+escalate on failure
  Tier 2 (flag):   phantom_sprint, duplicate_day_sprints
                   — write <league_dir>/sprint_integrity_pending_review.flag
                     with proposed action + alternative (vidar_pending_review schema)
  Tier 3 (skip):   ledger_vs_state_drift
                   — shadow-mode; record state=shadow_mode_skipped, no alert

Classifier uses the vidar_tier rubric via deterministic kind mapping for known
anomaly types; falls back to tier2 for unknown kinds (safe default: flag for
human review rather than auto-apply).

State: competition/sprint_integrity_executor_state.json
Cron:  */15 * * * *

CLI:
  python3 sprint_integrity_executor.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta

WORKSPACE        = "/root/.openclaw/workspace"
RESEARCH         = os.path.join(WORKSPACE, "research")
SYN_INBOX        = os.path.join(WORKSPACE, "syn_inbox.jsonl")
EXECUTOR_STATE   = os.path.join(WORKSPACE, "competition", "sprint_integrity_executor_state.json")
MAINTENANCE_LOG  = os.path.join(WORKSPACE, "maintenance_log.jsonl")

sys.path.insert(0, WORKSPACE)
sys.path.insert(0, RESEARCH)

# Deterministic tier mapping — mirrors the vidar_tier rubric for these kinds.
# Tier 1: pure state reconciliation, filesystem-verifiable, auto-revertable from backup.
# Tier 2: involves choosing between options — flag for 24h human review.
# Tier 3 skip: fix_hint explicitly says "do NOT auto-fix" (Phase 2 shadow-mode).
TIER1_KINDS      = {"cycle_regressed", "undercount_vs_results"}
TIER2_KINDS      = {"phantom_sprint", "duplicate_day_sprints"}
TIER3_SKIP_KINDS = {"ledger_vs_state_drift"}

SCORE_SUFFIXES   = ("_score.json", "_auto.json")
BOUNDARY_BUF_SEC = 300   # matches sprint_integrity_check.py cycle_started_at buffer
MAX_ATTEMPTS     = 3     # give up after 3 consecutive fix failures
TIER2_REVIEW_HR  = 24    # hours before pending-review flag expires


# ── small utils ───────────────────────────────────────────────────────────────

def _ts_iso():
    return datetime.now(timezone.utc).isoformat()


def _ts_compact():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def _atomic_write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _append_jsonl(path, record):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


# ── state ─────────────────────────────────────────────────────────────────────

def _load_state():
    if not os.path.exists(EXECUTOR_STATE):
        return {}
    try:
        with open(EXECUTOR_STATE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state):
    _atomic_write_json(EXECUTOR_STATE, state)


# ── league config ──────────────────────────────────────────────────────────────

def _load_league_config(league_name):
    """Return the matching cfg dict from sprint_integrity_check.LEAGUES."""
    import sprint_integrity_check as sic
    for cfg in sic.LEAGUES:
        if cfg["name"] == league_name:
            return cfg
    return None


# ── anomaly key ────────────────────────────────────────────────────────────────

def _stable_anomaly_key(a):
    """Compute stable anomaly_key from an anomaly dict.

    Mirrors make_anomaly_key() in sprint_integrity_check.py — used as
    fallback for inbox entries that predate the field addition.
    """
    if "anomaly_key" in a:
        return a["anomaly_key"]
    league = a.get("league", "")
    kind   = a.get("kind", "")
    if kind == "phantom_sprint":
        sub = a.get("sprint_id", "")
    elif kind == "duplicate_day_sprints":
        sub = ",".join(sorted(a.get("zombie_sprints", [])))
    elif kind == "ledger_vs_state_drift":
        sub = ",".join(sorted(a.get("fields", [])))
    elif kind == "missing_archive_cycle":
        sub = str(a.get("missing_cycle", ""))
    else:
        sub = ""
    return f"{league}:{kind}:{sub}"


# ── tier classification ────────────────────────────────────────────────────────

def _classify_kind(kind):
    """Return tier string for this anomaly kind.

    Known kinds are mapped deterministically (no LLM cost).
    Unknown kinds default to tier2 (flag for human review — safe default).
    """
    if kind in TIER1_KINDS:
        return "tier1"
    if kind in TIER3_SKIP_KINDS:
        return "tier3_skip"
    if kind in TIER2_KINDS:
        return "tier2"
    return "tier2"


# ── syn_inbox reader ───────────────────────────────────────────────────────────

def _read_syn_inbox_anomalies():
    """Read all sprint_integrity entries from syn_inbox, flatten anomalies list."""
    if not os.path.exists(SYN_INBOX):
        return []
    anomalies = []
    try:
        with open(SYN_INBOX) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("source") != "sprint_integrity":
                    continue
                for a in rec.get("anomalies", []):
                    a = dict(a)
                    a.setdefault("_inbox_ts", rec.get("ts", ""))
                    a["anomaly_key"] = _stable_anomaly_key(a)
                    anomalies.append(a)
    except OSError:
        return []
    return anomalies


def _deduplicate_anomalies(anomalies):
    """Keep the most recent inbox entry per anomaly_key."""
    seen: dict = {}
    for a in anomalies:
        key = a["anomaly_key"]
        if key not in seen or a["_inbox_ts"] > seen[key]["_inbox_ts"]:
            seen[key] = a
    return list(seen.values())


# ── Tier 1 fix implementations ─────────────────────────────────────────────────

def _backup_file(path):
    """Backup path.bak.pre_integrity_heal_<ts>. Returns backup path."""
    bak = f"{path}.bak.pre_integrity_heal_{_ts_compact()}"
    shutil.copy2(path, bak)
    return bak


def _fix_cycle_regressed(anomaly, cfg, dry_run):
    """Set cycle = max_archived_cycle + 1; reseed sprints[] from results/ and active/."""
    archive_root     = cfg["archive_root"]
    results_dir      = cfg["results_dir"]
    active_dir       = cfg.get("active_dir")
    cycle_state_path = cfg["cycle_state"]

    # Re-derive max_archived_cycle from the filesystem (don't trust the detail string).
    max_archived = 0
    if archive_root and os.path.isdir(archive_root):
        for sub in os.listdir(archive_root):
            if not os.path.isdir(os.path.join(archive_root, sub)):
                continue
            token = sub.replace("cycle-", "").replace("cycle_", "").split("-")[0].split("_")[0]
            try:
                max_archived = max(max_archived, int(token))
            except ValueError:
                pass
    if max_archived == 0:
        return {"ok": False, "msg": "cannot determine max_archived_cycle from archive dir", "backup": None}

    new_cycle = max_archived + 1

    # Sprint IDs already in any archive subdir belong to past cycles.
    archived_ids: set = set()
    if archive_root and os.path.isdir(archive_root):
        for sub in os.listdir(archive_root):
            subpath = os.path.join(archive_root, sub)
            if os.path.isdir(subpath):
                for name in os.listdir(subpath):
                    if os.path.isdir(os.path.join(subpath, name)):
                        archived_ids.add(name)

    current_sprints: set = set()
    if results_dir and os.path.isdir(results_dir):
        for name in os.listdir(results_dir):
            full = os.path.join(results_dir, name)
            if os.path.isdir(full) and name not in archived_ids and not name.startswith("cycle"):
                current_sprints.add(name)
    if active_dir and os.path.isdir(active_dir):
        for name in os.listdir(active_dir):
            full = os.path.join(active_dir, name)
            if os.path.isdir(full) and name not in archived_ids:
                current_sprints.add(name)

    new_sprints = sorted(current_sprints)
    msg = f"set cycle={new_cycle}, sprints={new_sprints}"

    if dry_run:
        print(f"    [DRY-RUN] cycle_regressed: {msg}")
        return {"ok": True, "msg": msg, "backup": None}

    with open(cycle_state_path) as f:
        state = json.load(f)
    bak = _backup_file(cycle_state_path)
    state["cycle"] = new_cycle
    state["sprints"] = new_sprints
    state["sprint_in_cycle"] = len(new_sprints)
    _atomic_write_json(cycle_state_path, state)
    return {"ok": True, "msg": f"{msg}, backup={bak}", "backup": bak}


def _fix_undercount_vs_results(anomaly, cfg, dry_run):
    """Rebuild sprints[] from score files dated >= cycle_started_at + active dirs."""
    cycle_state_path = cfg["cycle_state"]
    results_dir      = cfg["results_dir"]
    active_dir       = cfg.get("active_dir")

    with open(cycle_state_path) as f:
        state = json.load(f)

    cycle_started_at = state.get("cycle_started_at")
    if not cycle_started_at:
        return {"ok": False, "msg": "cycle_started_at missing from state", "backup": None}
    try:
        cs_epoch = datetime.fromisoformat(cycle_started_at.replace("Z", "+00:00")).timestamp()
    except ValueError as e:
        return {"ok": False, "msg": f"cannot parse cycle_started_at: {e}", "backup": None}

    score_ids = []
    if results_dir and os.path.isdir(results_dir):
        for fname in os.listdir(results_dir):
            fpath = os.path.join(results_dir, fname)
            if not os.path.isfile(fpath):
                continue
            for suffix in SCORE_SUFFIXES:
                if fname.endswith(suffix) and os.path.getmtime(fpath) > cs_epoch + BOUNDARY_BUF_SEC:
                    score_ids.append(fname[: -len(suffix)])
                    break

    active_ids = []
    if active_dir and os.path.isdir(active_dir):
        for name in os.listdir(active_dir):
            if os.path.isdir(os.path.join(active_dir, name)):
                active_ids.append(name)

    new_sprints = sorted(set(score_ids + active_ids))
    msg = f"rebuilt sprints={new_sprints}"

    if dry_run:
        print(f"    [DRY-RUN] undercount_vs_results: {msg}")
        return {"ok": True, "msg": msg, "backup": None}

    bak = _backup_file(cycle_state_path)
    state["sprints"] = new_sprints
    state["sprint_in_cycle"] = len(new_sprints)
    _atomic_write_json(cycle_state_path, state)
    return {"ok": True, "msg": f"{msg}, backup={bak}", "backup": bak}


def _apply_tier1_fix(anomaly, cfg, dry_run):
    kind = anomaly.get("kind")
    if kind == "cycle_regressed":
        return _fix_cycle_regressed(anomaly, cfg, dry_run)
    if kind == "undercount_vs_results":
        return _fix_undercount_vs_results(anomaly, cfg, dry_run)
    return {"ok": False, "msg": f"no Tier 1 fix for kind={kind}", "backup": None}


# ── current-state check ────────────────────────────────────────────────────────

def _anomaly_check(anomaly, cfg):
    """Return (still_present, detail). check_league() is the authoritative source of truth."""
    import sprint_integrity_check as sic
    try:
        current = sic.check_league(cfg)
    except Exception as e:
        # If the check itself fails, assume still present (safe default).
        return True, f"check_league raised: {e}"
    target = _stable_anomaly_key(anomaly)
    for a in current:
        if _stable_anomaly_key(a) == target:
            return True, a.get("detail", "present")
    return False, "not found in current check"


# ── Tier 2 pending review flag ─────────────────────────────────────────────────

def _flag_path(cfg):
    """Flag lives in the same directory as cycle_state.json for that league."""
    return os.path.join(os.path.dirname(cfg["cycle_state"]), "sprint_integrity_pending_review.flag")


def _write_tier2_flag(anomaly, cfg, dry_run):
    kind   = anomaly.get("kind", "")
    akey   = anomaly["anomaly_key"]
    detail = anomaly.get("detail", "")

    if kind == "phantom_sprint":
        sid      = anomaly.get("sprint_id", "?")
        proposed = f"Remove {sid} from sprints[] in {cfg['cycle_state']}"
        alt      = f"Restore results artifact for {sid} manually"
    elif kind == "duplicate_day_sprints":
        zombies  = anomaly.get("zombie_sprints", [])
        proposed = f"Remove zombie sprint_id(s) {zombies} from sprints[] and decrement sprint_in_cycle"
        alt      = "Manually verify which sprint_id to keep if both have partial data"
    else:
        proposed = anomaly.get("fix_hint", "manual review required")
        alt      = "Manual investigation required"

    deadline = (datetime.now(timezone.utc) + timedelta(hours=TIER2_REVIEW_HR)).isoformat()
    fpath    = _flag_path(cfg)

    if dry_run:
        print(f"    [DRY-RUN] Tier 2 flag -> {fpath}")
        print(f"      proposed:    {proposed}")
        print(f"      alternative: {alt}")
        return {"ok": True, "msg": f"would write {fpath}"}

    existing = {"entries": []}
    if os.path.exists(fpath):
        try:
            with open(fpath) as f:
                existing = json.load(f)
            existing.setdefault("entries", [])
        except (json.JSONDecodeError, OSError):
            pass
    existing["entries"] = [e for e in existing["entries"] if e.get("anomaly_key") != akey]
    existing["entries"].append({
        "anomaly_key": akey,
        "kind":        kind,
        "league":      anomaly.get("league"),
        "detail":      detail[:400],
        "proposed":    proposed[:400],
        "alternative": alt[:300],
        "deadline_ts": deadline,
        "inbox_ts":    anomaly.get("_inbox_ts", ""),
        "revert_command": f"# Manual: edit {fpath} + fix {cfg['cycle_state']} as appropriate",
    })
    existing["last_updated"] = _ts_iso()
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    _atomic_write_json(fpath, existing)
    return {"ok": True, "msg": f"flag written at {fpath}"}


# ── SYN escalation ─────────────────────────────────────────────────────────────

def _escalate(anomaly, reason):
    """Write critical entry to syn_inbox for anomalies that need Chris action."""
    _append_jsonl(SYN_INBOX, {
        "ts":              _ts_iso(),
        "source":          "sprint_integrity_executor",
        "severity":        "critical",
        "kind":            anomaly.get("kind"),
        "league":          anomaly.get("league"),
        "anomaly_key":     anomaly.get("anomaly_key"),
        "detail":          anomaly.get("detail", "")[:300],
        "reason":          reason[:300],
        "action_required": "Chris review required — auto-heal failed or post-fix check failed.",
        "tg_allowed":      True,
    })


# ── per-anomaly processor ──────────────────────────────────────────────────────

def process_anomaly(anomaly, exec_state, dry_run):
    """Process one anomaly end-to-end. Returns updated state entry."""
    akey   = anomaly["anomaly_key"]
    kind   = anomaly.get("kind", "")
    league = anomaly.get("league", "")
    tier   = _classify_kind(kind)

    prior    = exec_state.get(akey, {})
    attempts = prior.get("attempts", 0)
    status   = prior.get("status", "")

    print(f"  [{league}/{kind}] tier={tier} attempts={attempts} status={status!r}")

    # Terminal states — skip without a fresh filesystem check.
    if status in ("resolved", "resolved_externally", "shadow_mode_skipped"):
        print(f"    -> already {status}")
        return prior

    # Tier 3 / shadow-mode: record skip, no alert, no filesystem change.
    if tier == "tier3_skip":
        print(f"    -> shadow-mode skip, no auto-fix (Phase 2 ledger drift — deferred)")
        if dry_run:
            print(f"    [DRY-RUN] would record shadow_mode_skipped in state")
            return prior
        return {
            "anomaly_key":    akey,
            "kind":           kind,
            "league":         league,
            "first_seen":     prior.get("first_seen", _ts_iso()),
            "attempts":       0,
            "last_action_ts": _ts_iso(),
            "status":         "shadow_mode_skipped",
        }

    # Max attempts guard.
    if attempts >= MAX_ATTEMPTS:
        print(f"    -> max attempts ({MAX_ATTEMPTS}) reached, skipping (already escalated)")
        return prior

    # Load league config.
    cfg = _load_league_config(league)
    if cfg is None:
        print(f"    -> no config found for league {league!r}")
        return {**prior, "status": "config_not_found", "last_action_ts": _ts_iso(),
                "first_seen": prior.get("first_seen", _ts_iso())}

    # Pre-check: is the anomaly still present in the live filesystem?
    # Historical syn_inbox entries may have been resolved manually already.
    still_present, current_detail = _anomaly_check(anomaly, cfg)
    if not still_present:
        print(f"    -> not present in current check; resolved externally")
        if dry_run:
            print(f"    [DRY-RUN] would mark resolved_externally")
            return prior
        return {
            "anomaly_key":    akey,
            "kind":           kind,
            "league":         league,
            "first_seen":     prior.get("first_seen", _ts_iso()),
            "attempts":       attempts,
            "last_action_ts": _ts_iso(),
            "status":         "resolved_externally",
        }

    # Tier 2 already flagged: anomaly is still present, waiting for human action.
    if status == "tier2_flagged":
        print(f"    -> tier2 already flagged, anomaly still present — waiting for human")
        return prior

    if tier == "tier1":
        result = _apply_tier1_fix(anomaly, cfg, dry_run)
        print(f"    -> fix: ok={result['ok']} {result['msg']}")

        if dry_run:
            return prior

        new_attempts = attempts + 1

        if not result["ok"]:
            if new_attempts >= MAX_ATTEMPTS:
                _escalate(anomaly, f"Tier 1 fix failed after {new_attempts} attempts: {result['msg']}")
            return {
                "anomaly_key": akey, "kind": kind, "league": league,
                "first_seen": prior.get("first_seen", _ts_iso()),
                "attempts": new_attempts, "last_action_ts": _ts_iso(),
                "status": "fix_failed", "last_error": result["msg"],
            }

        # Post-fix re-verify via fresh check_league call.
        still_after, verify_detail = _anomaly_check(anomaly, cfg)
        print(f"    -> post-fix check: still_present={still_after} {verify_detail}")

        if not still_after:
            _append_jsonl(MAINTENANCE_LOG, {
                "ts": _ts_iso(), "phase": "auto_healed",
                "source": "sprint_integrity_executor",
                "league": league, "kind": kind,
                "detail": anomaly.get("detail", ""),
                "resolution": result["msg"],
            })
            return {
                "anomaly_key": akey, "kind": kind, "league": league,
                "first_seen": prior.get("first_seen", _ts_iso()),
                "attempts": new_attempts, "last_action_ts": _ts_iso(),
                "status": "resolved", "resolution": result["msg"],
            }
        else:
            # Auto-heal didn't resolve the anomaly — revert from backup immediately.
            bak = result.get("backup")
            revert_ok = False
            if bak and os.path.exists(bak):
                shutil.copy2(bak, cfg["cycle_state"])
                revert_ok = True
                print(f"    -> REVERTED from backup {bak}")
            else:
                print(f"    -> WARNING: no backup available for revert")
            _escalate(anomaly, f"auto-heal applied but anomaly persists ({verify_detail}); reverted={revert_ok}")
            return {
                "anomaly_key": akey, "kind": kind, "league": league,
                "first_seen": prior.get("first_seen", _ts_iso()),
                "attempts": new_attempts, "last_action_ts": _ts_iso(),
                "status": "reverted_and_escalated", "verify_error": verify_detail,
            }

    elif tier == "tier2":
        result = _write_tier2_flag(anomaly, cfg, dry_run)
        print(f"    -> flag: ok={result['ok']} {result['msg']}")
        if dry_run:
            return prior
        return {
            "anomaly_key": akey, "kind": kind, "league": league,
            "first_seen": prior.get("first_seen", _ts_iso()),
            "attempts": attempts + 1, "last_action_ts": _ts_iso(),
            "status": "tier2_flagged", "flag_msg": result["msg"],
        }

    return prior


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="sprint_integrity_executor — auto-heal sprint anomalies")
    p.add_argument("--dry-run", action="store_true", help="print what would be done; no file writes")
    args = p.parse_args()
    dry_run = args.dry_run

    if dry_run:
        print("[sprint_integrity_executor] DRY-RUN mode — no writes")

    raw     = _read_syn_inbox_anomalies()
    deduped = _deduplicate_anomalies(raw)

    if not deduped:
        print("[sprint_integrity_executor] no sprint_integrity anomalies in syn_inbox")
        return

    print(f"[sprint_integrity_executor] {len(deduped)} unique anomaly/ies from syn_inbox")

    state = _load_state()

    for anomaly in deduped:
        akey = anomaly["anomaly_key"]
        if akey not in state:
            state[akey] = {
                "anomaly_key":    akey,
                "kind":           anomaly.get("kind"),
                "league":         anomaly.get("league"),
                "first_seen":     _ts_iso(),
                "attempts":       0,
                "last_action_ts": None,
                "status":         "pending",
            }
        updated = process_anomaly(anomaly, state, dry_run)
        if not dry_run:
            state[akey] = updated

    if not dry_run:
        _save_state(state)
        print("[sprint_integrity_executor] state saved")


if __name__ == "__main__":
    main()
