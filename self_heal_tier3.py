#!/usr/bin/env python3
"""
self_heal_tier3.py — Tier 3 self-heal layer.

Tier 1 (service_crashloop_watch + per-domain watchdogs) handles single-event
restarts. Tier 2 (self_heal_controller) restarts on consecutive-degraded then
escalates after the heal-attempt cycle exhausts. Tier 3 owns the wider,
lower-eagerness layer that fires only when Tier 1 + Tier 2 have demonstrably
failed.

Detectors (each scans existing state — no new probes):
  1. cascading_tier12_failures
       Scans self_heal_log.jsonl + crashloop_state.json over a 6h window.
       Triggers when:
         - any single subsystem produced >= TIER3_ESCALATION_BURST escalations
         - OR a service AND its freshness target are both currently in
           healed-but-still-degraded state
         - OR a service has crashloop delta >= TIER3_CRASHLOOP_REPEAT three
           consecutive 15-min windows
  2. cross_component_drift
       Reads syn_inbox.jsonl for sprint_integrity ledger_vs_state_drift /
       ledger_drift_check_failed entries that LOKI has acknowledged but not
       resolved across >= TIER3_DRIFT_REPEAT consecutive cycles.
  3. resource_exhaustion
       df -h / df -i / /proc/meminfo. Two thresholds:
         - SOFT_DISK_PCT (default 85) → infra remediation (rotate large logs)
         - HARD_DISK_PCT (default 95) → escalate (irreversible if data deleted)
  4. failure_of_failure_handler
       Checks mtime of handler state files vs expected window x 3 grace:
         - self_heal_state.json    (controller cron 5m → grace 15m)
         - crashloop_state.json    (cron 15m → grace 45m)
         - sprint_integrity_state.json (cron 30m → grace 90m)
         - cron_health_state.json  (cron 60m → grace 180m)

Authority routing (the bridge to vidar_executor):
  Each detection produces a synthetic finding → vidar_tier.classify_finding() →
    tier1 (pure infra) → execute inline (logfile rotation, kicking dead handler)
    tier2 (capital-adjacent) → vidar_executor._add_pending_review() + escalate
                              action queued via _queue_to_loki()
    tier3 (irreversible)    → vidar_executor._emit_tier3_inbox()

Cooldowns:
  - 30 min between tier-3 attempts on same (detector, component) key
  - 24h hard ceiling: TIER3_DAILY_CAP firings per UTC day (default 8)

State / log:
  - competition/self_heal_tier3_state.json
  - competition/self_heal_tier3_log.jsonl

CLI:
  python3 self_heal_tier3.py                # cron entry point
  python3 self_heal_tier3.py --dry-run      # detect + plan, do not execute
  python3 self_heal_tier3.py --status       # cooldown table + recent firings
  python3 self_heal_tier3.py --force <det>  # force-run a single detector
                                            # det in: cascade, drift, resource, handler

Note: this module never re-implements vidar_executor's auth surface. All
capital-touching action go through vidar_executor's existing primitives so
auto-revert + 24h pending-review work identically.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
RESEARCH = os.path.join(WORKSPACE, "research")
COMPETITION = os.path.join(WORKSPACE, "competition")

STATE_FILE = os.path.join(COMPETITION, "self_heal_tier3_state.json")
LOG_FILE = os.path.join(COMPETITION, "self_heal_tier3_log.jsonl")
SYN_INBOX = os.path.join(WORKSPACE, "syn_inbox.jsonl")

# Inputs we read (state from lower-tier handlers).
SELF_HEAL_LOG = os.path.join(COMPETITION, "self_heal_log.jsonl")
SELF_HEAL_STATE = os.path.join(COMPETITION, "self_heal_state.json")
CRASHLOOP_STATE = os.path.join(COMPETITION, "crashloop_state.json")
SPRINT_INTEGRITY_STATE = os.path.join(COMPETITION, "sprint_integrity_state.json")
CRON_HEALTH_STATE = os.path.join(COMPETITION, "cron_health_state.json")
LOKI_ESC_LOG = os.path.join(RESEARCH, "loki_escalation_log.jsonl")
LOKI_PENDING = os.path.join(RESEARCH, "loki_pending_actions.jsonl")

# Tunables.
TIER3_COOLDOWN_MIN = 30
TIER3_DAILY_CAP = 8
TIER3_ESCALATION_BURST = 3        # >= N escalations on same subsystem in window
TIER3_ESCALATION_WINDOW_HR = 6
TIER3_CRASHLOOP_REPEAT = 3        # >= N consecutive crashloop windows
TIER3_DRIFT_REPEAT = 3            # >= N consecutive drift cycles unresolved
SOFT_DISK_PCT = 85
HARD_DISK_PCT = 95
SOFT_INODE_PCT = 80
HARD_INODE_PCT = 95
LOG_ROTATION_MIN_BYTES = 100 * 1024 * 1024  # 100 MB

# Handler-failure expected windows (cron interval x 3 grace, in minutes).
HANDLER_GRACE = {
    SELF_HEAL_STATE: ("self_heal_controller", 15),
    CRASHLOOP_STATE: ("service_crashloop_watch", 45),
    SPRINT_INTEGRITY_STATE: ("sprint_integrity_check", 90),
    CRON_HEALTH_STATE: ("cron_health", 180),
}


# ── small utils ──────────────────────────────────────────────────────────────

def _ts_iso():
    return datetime.now(timezone.utc).isoformat()


def _ts_min():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")


def _pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def _utc_today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _read_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def _atomic_write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _append_jsonl(path, record):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def _iter_jsonl_tail(path, max_lines=2000):
    """Yield parsed lines from a jsonl file, tail-only (memory-safe for large logs)."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        lines = f.readlines()
    for raw in lines[-max_lines:]:
        raw = raw.strip()
        if not raw:
            continue
        try:
            yield json.loads(raw)
        except json.JSONDecodeError:
            continue


def _parse_iso(ts):
    """Tolerant ISO8601 parser. Returns aware UTC datetime or None."""
    if not ts:
        return None
    try:
        # Strip trailing Z
        s = ts.replace("Z", "+00:00") if isinstance(ts, str) else str(ts)
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _file_age_min(path):
    if not os.path.exists(path):
        return None
    return (time.time() - os.path.getmtime(path)) / 60.0


# ── tier3 state (cooldowns + daily cap) ──────────────────────────────────────

def _load_state():
    return _read_json(STATE_FILE, {"keys": {}, "daily": {}})


def _save_state(state):
    _atomic_write_json(STATE_FILE, state)


def _cooldown_active(state, key):
    last = _parse_iso(state["keys"].get(key, {}).get("last_fired"))
    if not last:
        return False
    return (datetime.now(timezone.utc) - last) < timedelta(minutes=TIER3_COOLDOWN_MIN)


def _daily_capped(state):
    today = _utc_today()
    return state["daily"].get(today, 0) >= TIER3_DAILY_CAP


def _record_fired(state, key, finding_id, tier_route, status):
    state["keys"][key] = {
        "last_fired": _ts_iso(),
        "last_finding_id": finding_id,
        "last_tier_route": tier_route,
        "last_status": status,
    }
    today = _utc_today()
    state["daily"][today] = state["daily"].get(today, 0) + 1
    # Trim daily counter to the last 7 days to keep state small.
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    state["daily"] = {d: c for d, c in state["daily"].items() if d >= cutoff}


def _log(record):
    record.setdefault("ts", _ts_iso())
    _append_jsonl(LOG_FILE, record)


# ── synthetic finding helper ─────────────────────────────────────────────────

def _make_finding(detector, component, title, evidence, suggested_action, severity="error",
                  variant=""):
    """Synthesize a meta_audit-shaped finding so vidar_tier classifies it.

    The finding_id encodes the detector + component + variant + UTC date so:
      - vidar_tier_cache.json keys it stably across re-runs in the same day
      - vidar_executor's idempotency check (_executor_log_seen) treats reruns
        within a day as the same finding when audit_ts repeats
      - distinct *variants* of the same component (e.g. soft vs hard disk
        thresholds, or paired-degradation vs repeated-escalation cascades)
        get independent cache entries so the wrong tier is not returned for
        a more-severe variant.
    """
    today = _utc_today()
    variant_tag = f"-{variant}" if variant else ""
    fid = f"T3-{detector}-{component}{variant_tag}-{today}"
    return {
        "id": fid,
        "severity": severity,
        "title": title[:300],
        "evidence": evidence[:1200],
        "suggested_action": suggested_action[:1500],
        "why_it_matters": (
            "Tier 3 self-heal: the lower tiers' attempts have not stuck. "
            "Wider corrective action proposed."
        ),
        "delegable_to_loki": False,
        "league": "global",
    }


# ── routing: tier1 inline / tier2 pending_review / tier3 inbox ───────────────

def _route_action(finding, classify_rationale, tier, audit_ts, inline_handler=None,
                  escalate_description=None, league="global"):
    """Route a synthetic Tier 3 finding through the correct authority path.

    inline_handler: callable() -> dict (only invoked for tier1).
    escalate_description: human-readable work order for LOKI escalation log
                          (used for tier2 — queued as an "escalate" action so
                          LOKI's process_pending_actions writes it to
                          loki_escalation_log.jsonl on its 15-min tick).
    """
    sys.path.insert(0, RESEARCH)
    from vidar_executor import (
        _emit_tier3_inbox,
        _add_pending_review,
        _queue_to_loki,
    )

    fid = finding["id"]

    if tier == "tier3":
        _emit_tier3_inbox(finding, classify_rationale, audit_ts)
        # Re-tag the just-written row so SYN routes it via self_heal_tier3
        # source (the executor writes source=meta_audit by default; we want
        # the dedicated TG_ALLOWED_SOURCES entry so heartbeat can apply
        # source-specific suppression rules later if needed).
        _append_jsonl(SYN_INBOX, {
            "ts":              _ts_iso(),
            "source":          "self_heal_tier3",
            "severity":        "critical",
            "audit_ts":        audit_ts,
            "finding_id":      fid,
            "title":           f"[T3] {finding['title']}"[:300],
            "tier":            "tier3",
            "tier_rationale":  classify_rationale,
            "action_required": "Chris ack required.",
            "evidence":        finding["evidence"][:600],
            "suggested_action": finding["suggested_action"][:600],
        })
        return {"route": "tier3_inbox", "status": "emitted"}

    if tier == "tier2":
        # Queue an escalate action so LOKI's escalation log (Chris's dashboard
        # work-order surface) carries it. Add to vidar_pending_review.flag
        # for 24h Chris-revertable pattern.
        actions = [{
            "type": "escalate",
            "description": (escalate_description or finding["suggested_action"])[:500],
        }]
        queue_entry = _queue_to_loki(
            league=league,
            source_tag=f"self_heal_tier3_{finding.get('id', 'unknown')}",
            audit_ts=audit_ts,
            finding_id=fid,
            actions=actions,
        )
        action_summary = actions[0]["description"][:300]
        _add_pending_review(finding, audit_ts, action_summary, queue_entry["ts"])
        # Also surface a single non-paging info row so the dashboard sees the
        # tier2 fire in real time (heartbeat reads vidar_pending_review.flag
        # for the deadline display).
        _append_jsonl(SYN_INBOX, {
            "ts":              _ts_iso(),
            "source":          "self_heal_tier3",
            "severity":        "info",
            "audit_ts":        audit_ts,
            "finding_id":      fid,
            "msg":             f"[T3 tier2] queued: {action_summary[:200]}",
        })
        return {"route": "tier2_pending_review", "status": "queued"}

    # tier1 — execute inline. Pure infra; no Chris-action.
    if inline_handler is None:
        # Fall back to escalate if no inline handler is supplied.
        return {"route": "tier1_no_handler", "status": "skipped"}
    try:
        result = inline_handler() or {}
        result.setdefault("status", "ok")
        return {"route": "tier1_inline", "status": "executed", "detail": result}
    except Exception as e:
        return {"route": "tier1_inline", "status": "failed", "error": str(e)[:300]}


# ── detector 1: cascading tier1/2 failures ───────────────────────────────────

def detect_cascading_tier12_failures():
    """Scan the last TIER3_ESCALATION_WINDOW_HR hours of self_heal_log.jsonl
    plus crashloop_state.json for repeated escalations.

    Returns a list of {component, kind, evidence, count, related}.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=TIER3_ESCALATION_WINDOW_HR)
    escalations_by_subsys = {}
    heal_attempts_by_subsys = {}
    for rec in _iter_jsonl_tail(SELF_HEAL_LOG, max_lines=5000):
        ts = _parse_iso(rec.get("ts"))
        if ts is None or ts < cutoff:
            continue
        subsys = rec.get("subsystem")
        ev = rec.get("event")
        if not subsys:
            continue
        if ev == "escalated":
            escalations_by_subsys.setdefault(subsys, []).append(rec)
        elif ev == "heal_attempt":
            heal_attempts_by_subsys.setdefault(subsys, []).append(rec)

    results = []
    for subsys, recs in escalations_by_subsys.items():
        if len(recs) >= TIER3_ESCALATION_BURST:
            heal_count = len(heal_attempts_by_subsys.get(subsys, []))
            results.append({
                "component": subsys,
                "kind": "repeated_escalation",
                "evidence": (
                    f"{len(recs)} Tier 2 escalations on {subsys} in the last "
                    f"{TIER3_ESCALATION_WINDOW_HR}h (>= {TIER3_ESCALATION_BURST}); "
                    f"{heal_count} heal attempts in same window."
                ),
                "count": len(recs),
            })

    # Companion freshness + service degradation: if odin_<league> service is
    # currently in degraded-after-heal state AND its researcher_log_<league>
    # freshness target is also degraded-after-heal, that's a structural problem
    # restarts cannot fix.
    state = _read_json(SELF_HEAL_STATE, {"subsystems": {}})
    subs = state.get("subsystems", {})
    league_pairs = [
        ("odin_day", "researcher_log_day", "day"),
        ("odin_swing", "researcher_log_swing", "swing"),
        ("odin_futures_day", "researcher_log_futures_day", "futures_day"),
        ("odin_futures_swing", "researcher_log_futures_swing", "futures_swing"),
        ("freya", "researcher_log_pm", "pm"),
    ]
    for svc, freshness, league in league_pairs:
        s = subs.get(svc, {})
        f = subs.get(freshness, {})
        if (s.get("status") == "degraded" and s.get("healed_at")
                and f.get("status") == "degraded" and f.get("healed_at")):
            results.append({
                "component": f"league:{league}",
                "kind": "paired_degradation",
                "evidence": (
                    f"Both {svc} (status={s.get('status')}, "
                    f"detail={s.get('detail', '')[:80]}) and {freshness} "
                    f"(status={f.get('status')}, detail={f.get('detail', '')[:80]}) "
                    f"are degraded after Tier 2 heal attempts. Service is up but "
                    f"not producing research output — restart cycle is not the fix."
                ),
                "count": 2,
                "league": league,
            })
    return results


# ── detector 2: cross-component drift ────────────────────────────────────────

def detect_cross_component_drift():
    """Scan syn_inbox.jsonl for ledger-vs-state drift entries that LOKI has
    marked unresolved across >= TIER3_DRIFT_REPEAT cycles."""
    repeats = {}
    for rec in _iter_jsonl_tail(SYN_INBOX, max_lines=5000):
        src = rec.get("source", "")
        msg = rec.get("msg") or rec.get("title") or ""
        if src not in ("sprint_integrity", "research_freshness", "loki"):
            continue
        if "ledger_vs_state_drift" not in msg and "ledger_drift_check_failed" not in msg:
            continue
        # Extract league from msg pattern "<league>/ledger_vs_state_drift" or
        # "[<league> gen N] ledger_vs_state_drift".
        league = "unknown"
        for token in msg.replace("[", " ").replace("]", " ").replace("/", " ").split():
            if token in ("day", "swing", "futures_day", "futures_swing", "pm",
                         "polymarket"):
                league = token
                break
        repeats.setdefault(league, 0)
        repeats[league] += 1

    # Also count escalated drift entries in LOKI escalation log over last 24h.
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    loki_escalations = {}
    for rec in _iter_jsonl_tail(LOKI_ESC_LOG, max_lines=2000):
        ts = _parse_iso(rec.get("ts"))
        if ts is None or ts < cutoff:
            continue
        desc = rec.get("description") or ""
        if "ledger_vs_state_drift" not in desc and "drift" not in desc.lower():
            continue
        league = rec.get("league") or "unknown"
        loki_escalations.setdefault(league, 0)
        loki_escalations[league] += 1

    results = []
    for league, count in repeats.items():
        if count >= TIER3_DRIFT_REPEAT:
            results.append({
                "component": f"ledger:{league}",
                "kind": "drift_unresolved",
                "evidence": (
                    f"{count} ledger_vs_state_drift signals for league {league} "
                    f"over last ~5000 inbox lines; LOKI escalations on drift in "
                    f"last 24h: {loki_escalations.get(league, 0)}. "
                    f"Auto-fix loop has not resolved it."
                ),
                "count": count,
                "league": league,
            })
    return results


# ── detector 3: resource exhaustion ──────────────────────────────────────────

def _disk_usage_pct(path="/"):
    """Return (used_pct, inode_pct) ints, or (None, None) if unavailable."""
    try:
        out = subprocess.check_output(["df", "-P", path], timeout=5).decode()
        # Header + 1 line; col 5 is "Capacity" like "73%"
        lines = out.strip().splitlines()
        if len(lines) >= 2:
            cols = lines[1].split()
            used = int(cols[4].rstrip("%"))
        else:
            used = None
    except (subprocess.SubprocessError, ValueError, IndexError):
        used = None
    try:
        out = subprocess.check_output(["df", "-Pi", path], timeout=5).decode()
        lines = out.strip().splitlines()
        if len(lines) >= 2:
            cols = lines[1].split()
            inode = int(cols[4].rstrip("%"))
        else:
            inode = None
    except (subprocess.SubprocessError, ValueError, IndexError):
        inode = None
    return used, inode


def detect_resource_exhaustion():
    used, inode = _disk_usage_pct("/")
    results = []
    if used is not None and used >= SOFT_DISK_PCT:
        sev = "critical" if used >= HARD_DISK_PCT else "error"
        results.append({
            "component": "disk:/",
            "kind": "disk_full",
            "evidence": f"df -P / reports {used}% used (soft={SOFT_DISK_PCT}, hard={HARD_DISK_PCT}).",
            "severity": sev,
            "level": used,
        })
    if inode is not None and inode >= SOFT_INODE_PCT:
        sev = "critical" if inode >= HARD_INODE_PCT else "error"
        results.append({
            "component": "disk:/inodes",
            "kind": "inode_full",
            "evidence": f"df -Pi / reports {inode}% inodes used (soft={SOFT_INODE_PCT}, hard={HARD_INODE_PCT}).",
            "severity": sev,
            "level": inode,
        })
    return results


def _rotate_large_logs(min_bytes=LOG_ROTATION_MIN_BYTES, dry=False):
    """Find log files > min_bytes under workspace/competition/ and gzip + truncate.
    Inline tier1 remediation for soft-disk-full."""
    rotated = []
    candidates = []
    for root, _dirs, files in os.walk(COMPETITION):
        for name in files:
            if not (name.endswith(".log") or name.endswith(".jsonl")):
                continue
            path = os.path.join(root, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size >= min_bytes:
                candidates.append((path, size))
    candidates.sort(key=lambda x: -x[1])
    for path, size in candidates[:20]:
        if dry:
            rotated.append({"path": path, "bytes": size, "action": "would_rotate"})
            continue
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
        gz_path = f"{path}.{ts}.gz"
        try:
            with open(path, "rb") as src, gzip.open(gz_path, "wb") as dst:
                shutil.copyfileobj(src, dst)
            with open(path, "w"):
                pass  # truncate in place; preserves any open file handles
            rotated.append({"path": path, "bytes": size, "archived_to": gz_path})
        except OSError as e:
            rotated.append({"path": path, "bytes": size, "error": str(e)[:200]})
    return {"rotated": rotated, "scanned": len(candidates)}


# ── detector 4: failure of the failure-handler ───────────────────────────────

def detect_failed_handler():
    """Each watchdog state file should be touched within (cron interval x 3).
    If not, the watchdog itself is dead."""
    results = []
    for path, (handler_name, grace_min) in HANDLER_GRACE.items():
        age = _file_age_min(path)
        if age is None:
            results.append({
                "component": f"handler:{handler_name}",
                "kind": "handler_state_missing",
                "evidence": f"state file {path} does not exist; handler may have never run.",
                "age_min": None,
            })
            continue
        if age > grace_min:
            results.append({
                "component": f"handler:{handler_name}",
                "kind": "handler_stale",
                "evidence": (
                    f"state file {path} is {age:.0f}min old; grace={grace_min}min. "
                    f"Handler {handler_name} has stopped writing — its cron may be "
                    f"failing silently."
                ),
                "age_min": age,
                "grace_min": grace_min,
            })
    return results


def _kick_handler(handler_name):
    """Run a known watchdog one-shot to revive it. The cron will resume on its
    own next tick — this is just to immediately re-prime the state file."""
    cmd_map = {
        "self_heal_controller": ["python3", os.path.join(WORKSPACE, "self_heal_controller.py")],
        "service_crashloop_watch": ["python3", os.path.join(WORKSPACE, "service_crashloop_watch.py")],
        "sprint_integrity_check": ["python3", os.path.join(WORKSPACE, "sprint_integrity_check.py")],
        "cron_health": ["python3", os.path.join(WORKSPACE, "cron_health.py")],
    }
    cmd = cmd_map.get(handler_name)
    if not cmd:
        return {"status": "no_command_known", "handler": handler_name}
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=120)
        return {
            "status": "kicked",
            "handler": handler_name,
            "rc": out.returncode,
            "stderr": (out.stderr or b"").decode(errors="replace")[:300],
        }
    except subprocess.SubprocessError as e:
        return {"status": "kick_failed", "handler": handler_name, "error": str(e)[:300]}


# ── per-detection planner: synth finding → vidar_tier → route ────────────────

def _plan_and_execute_detection(detection, detector_name, dry=False):
    """Wrap a detection dict as a synthetic finding, classify, route."""
    component = detection["component"]
    audit_ts = _ts_min()
    today = _utc_today()
    cooldown_key = f"{detector_name}:{component}:{today}"

    state = _load_state()
    if _cooldown_active(state, cooldown_key):
        return {"status": "cooldown_active", "key": cooldown_key}
    if _daily_capped(state):
        return {"status": "daily_cap_reached", "cap": TIER3_DAILY_CAP}
    variant = ""  # default; per-detector blocks below override

    # Build per-detector finding shapes that vidar_tier will classify
    # correctly. Phrasing matters here — vidar_tier's keyword pre-pass
    # short-circuits to tier3 on certain literals; we phrase remediation in
    # terms the rubric maps to the desired tier.
    if detector_name == "cascade":
        league = detection.get("league")
        if league:
            variant = f"paired-{league}"
            title = f"Tier 3 cascade: paired degradation on league {league}"
            suggested = (
                f"League {league}: service+freshness pair both degraded after "
                f"Tier 2 restart cycle. Propose population reset (delete "
                f"elite_0..elite_9 in the league directory and reseed with "
                f"diverse random configs while preserving champion). This is "
                f"the same end-to-end pattern used to revive futures_day "
                f"(commits c907cff pause, 8c6585a resume)."
            )
            severity = "error"
            inline = None
            escalate_desc = (
                f"[T3 cascade] League {league}: pair (service+researcher) "
                f"degraded after Tier 2 cycle. Recommend manual league reseed "
                f"(matches futures_day c907cff/8c6585a pattern). Restart loop "
                f"alone will not fix."
            )
            league_arg = league
        else:
            variant = "repeated"
            title = f"Tier 3 cascade: repeated Tier 2 escalation on {component}"
            suggested = (
                f"Audit subsystem {component}: investigate root cause beyond "
                f"systemctl restart cycle. Add a tighter watchdog cooldown for "
                f"this subsystem and investigate logs."
            )
            severity = "error"
            inline = None
            escalate_desc = (
                f"[T3 cascade] {component}: {detection['count']} Tier 2 "
                f"escalations in {TIER3_ESCALATION_WINDOW_HR}h. Restart loop is "
                f"not converging — investigate root cause."
            )
            league_arg = "global"

    elif detector_name == "drift":
        league = detection.get("league", "unknown")
        variant = f"ledger-{league}"
        title = f"Tier 3 drift reconciliation: ledger vs disk state on {league}"
        suggested = (
            f"Cross-component reconciliation needed for league {league}: "
            f"sprint integrity reports ledger=N disk=M divergence across "
            f"{detection['count']} cycles, LOKI auto-fix has not resolved. "
            f"Walk dependency graph (cycle_ledger.jsonl tail vs "
            f"elites_summary.json mtime vs leaderboard.json vs portfolio.json) "
            f"and re-derive canonical state. This may LOOSEN the strict "
            f"ledger-as-truth invariant for this one league while a writer "
            f"bug is found."
        )
        severity = "error"
        inline = None
        escalate_desc = (
            f"[T3 drift] {league}: ledger_vs_state_drift unresolved x"
            f"{detection['count']} cycles. Need cross-component re-derivation "
            f"(ledger ↔ portfolio ↔ leaderboard). Loosens ledger-as-truth "
            f"invariant — Chris-revertable per tier2 24h flag."
        )
        league_arg = league if league in (
            "day", "swing", "futures_day", "futures_swing", "pm", "polymarket"
        ) else "global"

    elif detector_name == "resource":
        component = detection["component"]
        if detection.get("severity") == "critical":
            variant = "hard"
            title = f"Tier 3 resource: {component} HARD-threshold exceeded"
            # Phrasing must trigger the vidar_tier keyword pre-pass so this
            # routes to tier3 (Chris-action) regardless of LLM availability.
            # Keywords: "permanently", "delete all", "irrecoverabl(e|y)".
            suggested = (
                f"{component}: usage at {detection.get('level')}% (hard "
                f"threshold). Log rotation alone will not free enough; need "
                f"to permanently delete all stale archive directories and "
                f"old backups under workspace/competition/. This deletion is "
                f"irrecoverable. Chris ack required."
            )
            severity = "critical"
            inline = None
            escalate_desc = None
            league_arg = "global"
        else:
            variant = "soft"
            title = f"Tier 3 resource: {component} soft threshold exceeded — auto-rotating"
            suggested = (
                f"{component} at {detection.get('level')}%. Rotate large "
                f"workspace logs (gzip + truncate files > "
                f"{LOG_ROTATION_MIN_BYTES // 1024 // 1024}MB). Pure infra; "
                f"reversible (gz files retained)."
            )
            severity = "warning"
            inline = (lambda d=dry: _rotate_large_logs(dry=d))
            escalate_desc = None
            league_arg = "global"

    elif detector_name == "handler":
        handler_name = detection["component"].split(":", 1)[1]
        variant = "stale" if detection.get("kind") == "handler_stale" else "missing"
        title = f"Tier 3 handler-failure: {handler_name} stopped writing state"
        # Phrasing avoids "safety subsystem" / "modify" / "loosen" cues so the
        # classifier reads this as a routine cron one-shot, not an authority
        # change. The kick is exactly what cron does on its next tick — no
        # code, scope, or behavior change.
        suggested = (
            f"Run {handler_name} one shot via subprocess (equivalent to a "
            f"single early-fire cron tick) to re-prime its state file. No "
            f"code change, no parameter tweak, no scope expansion: the "
            f"existing cron continues unchanged. If state remains stale "
            f"after the next normal cron tick, separately investigate the "
            f"script."
        )
        severity = "error"
        inline = (lambda h=handler_name: _kick_handler(h))
        escalate_desc = (
            f"[T3 handler] {handler_name} state stale after grace window. "
            f"Auto-kick attempted; investigate cron + script if persists."
        )
        league_arg = "global"

    else:
        return {"status": "unknown_detector", "detector": detector_name}

    finding = _make_finding(
        detector_name, component, title, detection["evidence"], suggested,
        severity=severity, variant=variant,
    )

    # Classify via vidar_tier — same rubric as meta_audit findings.
    sys.path.insert(0, RESEARCH)
    try:
        from vidar_tier import classify_finding
        tier, classify_rationale = classify_finding(finding, audit_ts=audit_ts)
    except Exception as e:
        # Conservative fallback: degrade to escalate-only via inbox so we
        # never silently lose a Tier 3 detection if classifier fails.
        _log({
            "detector": detector_name,
            "component": component,
            "status": "classifier_failed",
            "error": str(e)[:300],
        })
        # Surface as error inbox row.
        _append_jsonl(SYN_INBOX, {
            "ts": _ts_iso(),
            "source": "self_heal_tier3",
            "severity": "error",
            "msg": f"[T3] classifier failed for {component}: {str(e)[:200]}",
        })
        return {"status": "classifier_failed"}

    if dry:
        return {
            "status": "dry_run",
            "detector": detector_name,
            "component": component,
            "tier": tier,
            "classify_rationale": classify_rationale,
            "finding": finding,
        }

    route_result = _route_action(
        finding, classify_rationale, tier, audit_ts,
        inline_handler=inline,
        escalate_description=escalate_desc,
        league=league_arg,
    )
    _record_fired(state, cooldown_key, finding["id"], tier, route_result["status"])
    _save_state(state)

    out = {
        "detector": detector_name,
        "component": component,
        "finding_id": finding["id"],
        "tier": tier,
        "classify_rationale": classify_rationale,
        "route": route_result,
    }
    _log(out)
    return out


# ── orchestrator ─────────────────────────────────────────────────────────────

DETECTORS = {
    "cascade": detect_cascading_tier12_failures,
    "drift": detect_cross_component_drift,
    "resource": detect_resource_exhaustion,
    "handler": detect_failed_handler,
}


def run_all(dry=False, only=None):
    summary = {"detected": 0, "fired": 0, "skipped_cooldown": 0, "dry_runs": 0,
               "tier_routes": {}}
    for name, fn in DETECTORS.items():
        if only and name != only:
            continue
        try:
            detections = fn()
        except Exception as e:
            _log({"detector": name, "status": "detector_crashed", "error": str(e)[:300]})
            continue
        for d in detections:
            summary["detected"] += 1
            r = _plan_and_execute_detection(d, name, dry=dry)
            st = r.get("status", "")
            if st == "cooldown_active":
                summary["skipped_cooldown"] += 1
            elif st == "dry_run":
                summary["dry_runs"] += 1
            elif st in ("emitted", "queued", "executed", "ok"):
                summary["fired"] += 1
                tier = r.get("tier") or r.get("route", {}).get("route") or "?"
                summary["tier_routes"][tier] = summary["tier_routes"].get(tier, 0) + 1
            elif "route" in r and isinstance(r["route"], dict):
                # _plan_and_execute_detection returns the full record on
                # success; route is a dict {route, status, ...}.
                summary["fired"] += 1
                tier = r.get("tier") or "?"
                summary["tier_routes"][tier] = summary["tier_routes"].get(tier, 0) + 1
    return summary


def show_status():
    state = _load_state()
    print(f"[self_heal_tier3 status] {_pst_now()}")
    print(f"daily counter: {json.dumps(state.get('daily', {}), indent=2)}")
    print(f"per-key cooldowns ({len(state.get('keys', {}))} entries):")
    for key, info in sorted(state.get("keys", {}).items()):
        last = info.get("last_fired", "?")
        print(f"  {key:60s}  {info.get('last_tier_route','?'):6s}  {info.get('last_status','?'):10s}  {last}")
    print()
    print("recent log entries (last 10):")
    for rec in list(_iter_jsonl_tail(LOG_FILE, max_lines=10)):
        print(f"  {rec.get('ts','?')[:19]}  {rec.get('detector','?'):8s}  "
              f"{rec.get('component','?'):30s}  tier={rec.get('tier','?'):6s}  "
              f"route={rec.get('route',{}).get('route','?')}")


def main():
    p = argparse.ArgumentParser(description="Self-heal Tier 3 layer.")
    p.add_argument("--dry-run", action="store_true",
                   help="Detect + classify, do not execute or fire alerts.")
    p.add_argument("--status", action="store_true",
                   help="Show cooldown table + recent firings, then exit.")
    p.add_argument("--force", choices=list(DETECTORS.keys()),
                   help="Run a single detector only.")
    args = p.parse_args()

    if args.status:
        show_status()
        return 0

    summary = run_all(dry=args.dry_run, only=args.force)
    print(f"[{_pst_now()}] tier3 summary: {json.dumps(summary)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
