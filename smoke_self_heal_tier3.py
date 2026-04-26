#!/usr/bin/env python3
"""
smoke_self_heal_tier3.py — exercise each Tier 3 trigger in isolation.

For each detector:
  1. Inject the minimum state required to fire (without touching prod state
     files — we monkeypatch the input paths to point at /tmp fixtures).
  2. Run the detector.
  3. Run the planner+router in --dry-run mode (no inbox writes, no inline
     execution).
  4. Confirm the planner produced a tier classification + route plan.

Cross-component drift uses a fixture inbox file. Resource exhaustion
monkeypatches `_disk_usage_pct`. Handler-failure backdates a temp file.

Result: prints a per-trigger pass/fail line and exits non-zero if any fail.
This is a pure dry-run — no syn_inbox writes, no LOKI queue mutations,
no Chris paging.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone

WORKSPACE = "/root/.openclaw/workspace"
sys.path.insert(0, WORKSPACE)
sys.path.insert(0, os.path.join(WORKSPACE, "research"))

import self_heal_tier3 as t3  # noqa: E402

PASS = []
FAIL = []
SMOKE_AUDIT_TS = "smoke-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def _patched_make_finding(detector, component, title, evidence, suggested_action,
                          severity="error", variant=""):
    """Wrapper that prefixes finding_ids with the smoke audit_ts. Keeps the
    real vidar_tier_cache.json clean of test entries (cache key is
    audit_ts::finding_id; smoke entries cluster under one tombstone key)."""
    today = t3._utc_today()
    variant_tag = f"-{variant}" if variant else ""
    return {
        "id": f"SMOKE-{SMOKE_AUDIT_TS}-{detector}-{component}{variant_tag}-{today}",
        "severity": severity,
        "title": title[:300],
        "evidence": evidence[:1200],
        "suggested_action": suggested_action[:1500],
        "why_it_matters": "Smoke test synthetic finding.",
        "delegable_to_loki": False,
        "league": "global",
    }


t3._make_finding = _patched_make_finding


def _record(name, ok, detail):
    (PASS if ok else FAIL).append((name, detail))
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}: {detail}")


def setup_fixtures():
    """Create a temp dir + redirect t3 input paths into it for the duration
    of the smoke test."""
    fix = tempfile.mkdtemp(prefix="t3_smoke_")
    print(f"[smoke] fixtures dir: {fix}")
    # Redirect every input + output path to the fixture dir.
    t3.SELF_HEAL_LOG = os.path.join(fix, "self_heal_log.jsonl")
    t3.SELF_HEAL_STATE = os.path.join(fix, "self_heal_state.json")
    t3.CRASHLOOP_STATE = os.path.join(fix, "crashloop_state.json")
    t3.SPRINT_INTEGRITY_STATE = os.path.join(fix, "sprint_integrity_state.json")
    t3.CRON_HEALTH_STATE = os.path.join(fix, "cron_health_state.json")
    t3.SYN_INBOX = os.path.join(fix, "syn_inbox.jsonl")
    t3.LOKI_ESC_LOG = os.path.join(fix, "loki_escalation_log.jsonl")
    # Outputs — keep state + log inside fixture dir so we don't pollute prod.
    t3.STATE_FILE = os.path.join(fix, "tier3_state.json")
    t3.LOG_FILE = os.path.join(fix, "tier3_log.jsonl")
    # Refresh handler-grace map to point at the new state paths.
    t3.HANDLER_GRACE = {
        t3.SELF_HEAL_STATE: ("self_heal_controller", 15),
        t3.CRASHLOOP_STATE: ("service_crashloop_watch", 45),
        t3.SPRINT_INTEGRITY_STATE: ("sprint_integrity_check", 90),
        t3.CRON_HEALTH_STATE: ("cron_health", 180),
    }
    return fix


def write_jsonl(path, records):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def _now_iso(offset_min=0):
    dt = datetime.now(timezone.utc) + timedelta(minutes=offset_min)
    return dt.isoformat()


# ── trigger 1: cascading failure ─────────────────────────────────────────────

def test_cascading_failure():
    """3 escalations on odin_day in last 6h → cascade detector should fire."""
    write_jsonl(t3.SELF_HEAL_LOG, [
        {"ts": _now_iso(-90), "subsystem": "odin_day", "event": "heal_attempt",
         "action": "restart:odin_day:ok", "consec_degraded": 2},
        {"ts": _now_iso(-80), "subsystem": "odin_day", "event": "escalated",
         "detail": "still degraded after restart", "cycles_since_heal": 2},
        {"ts": _now_iso(-50), "subsystem": "odin_day", "event": "escalated",
         "detail": "still degraded after restart", "cycles_since_heal": 2},
        {"ts": _now_iso(-15), "subsystem": "odin_day", "event": "escalated",
         "detail": "still degraded after restart", "cycles_since_heal": 2},
    ])
    detections = t3.detect_cascading_tier12_failures()
    if not any(d["component"] == "odin_day" for d in detections):
        _record("cascade.repeated_escalation", False,
                f"expected odin_day in detections, got {detections}")
        return
    d = next(d for d in detections if d["component"] == "odin_day")
    if d["count"] < t3.TIER3_ESCALATION_BURST:
        _record("cascade.repeated_escalation", False,
                f"count {d['count']} < burst {t3.TIER3_ESCALATION_BURST}")
        return

    plan = t3._plan_and_execute_detection(d, "cascade", dry=True)
    if plan.get("status") != "dry_run":
        _record("cascade.repeated_escalation", False, f"plan status: {plan}")
        return
    _record("cascade.repeated_escalation", True,
            f"detected count={d['count']}, dry plan tier={plan.get('tier')}")


def test_paired_degradation():
    """odin_day + researcher_log_day both healed-but-still-degraded →
    cascade detector emits paired_degradation finding for league:day."""
    paired_state = {
        "subsystems": {
            "odin_day": {
                "status": "degraded", "detail": "service up, no work output",
                "consec_degraded": 4, "healed_at": _now_iso(-30),
                "cycles_since_heal": 3,
            },
            "researcher_log_day": {
                "status": "degraded", "detail": "stale:120min>30min",
                "consec_degraded": 6, "healed_at": _now_iso(-30),
                "cycles_since_heal": 4,
            },
        }
    }
    with open(t3.SELF_HEAL_STATE, "w") as f:
        json.dump(paired_state, f)
    detections = t3.detect_cascading_tier12_failures()
    paired = [d for d in detections if d.get("kind") == "paired_degradation"]
    if not paired:
        _record("cascade.paired_degradation", False,
                f"expected paired_degradation, got kinds={[d['kind'] for d in detections]}")
        return
    d = paired[0]
    plan = t3._plan_and_execute_detection(d, "cascade", dry=True)
    if plan.get("tier") not in ("tier1", "tier2", "tier3"):
        _record("cascade.paired_degradation", False, f"no tier: {plan}")
        return
    _record("cascade.paired_degradation", True,
            f"league={d.get('league')}, dry tier={plan['tier']}")


# ── trigger 2: cross-component drift ─────────────────────────────────────────

def test_cross_component_drift():
    """Inject 4 ledger_vs_state_drift inbox entries on polymarket → drift
    detector fires."""
    write_jsonl(t3.SYN_INBOX, [
        {"ts": _now_iso(-180), "source": "sprint_integrity",
         "msg": "polymarket/ledger_vs_state_drift: sprint_in_cycle: ledger=1 disk=0"},
        {"ts": _now_iso(-120), "source": "sprint_integrity",
         "msg": "polymarket/ledger_vs_state_drift: sprint_in_cycle: ledger=2 disk=0"},
        {"ts": _now_iso(-60),  "source": "sprint_integrity",
         "msg": "polymarket/ledger_vs_state_drift: sprint_in_cycle: ledger=3 disk=0"},
        {"ts": _now_iso(-15),  "source": "sprint_integrity",
         "msg": "polymarket/ledger_vs_state_drift: sprint_in_cycle: ledger=4 disk=0"},
    ])
    detections = t3.detect_cross_component_drift()
    pm = [d for d in detections if d.get("league") == "polymarket"]
    if not pm:
        _record("drift.unresolved", False, f"no polymarket drift detected: {detections}")
        return
    d = pm[0]
    plan = t3._plan_and_execute_detection(d, "drift", dry=True)
    if plan.get("status") != "dry_run":
        _record("drift.unresolved", False, f"plan: {plan}")
        return
    _record("drift.unresolved", True,
            f"count={d['count']}, dry tier={plan.get('tier')}")


# ── trigger 3: resource exhaustion ───────────────────────────────────────────

def test_resource_soft():
    """Patch _disk_usage_pct to return 88% (soft) → expect tier1 inline plan."""
    orig = t3._disk_usage_pct
    t3._disk_usage_pct = lambda path="/": (88, 30)
    try:
        detections = t3.detect_resource_exhaustion()
        disk = [d for d in detections if d["kind"] == "disk_full"]
        if not disk:
            _record("resource.disk_soft", False, f"no detections: {detections}")
            return
        d = disk[0]
        plan = t3._plan_and_execute_detection(d, "resource", dry=True)
        if plan.get("tier") != "tier1":
            _record("resource.disk_soft", False,
                    f"expected tier1 (infra log rotation), got {plan.get('tier')}: {plan}")
            return
        _record("resource.disk_soft", True,
                f"level={d['level']}, dry tier=tier1 (would rotate logs inline)")
    finally:
        t3._disk_usage_pct = orig


def test_resource_hard():
    """Patch _disk_usage_pct to return 96% (hard) → expect tier2 or tier3 route
    (vidar_tier classifies; we accept either as long as it's escalating, not
    inline)."""
    orig = t3._disk_usage_pct
    t3._disk_usage_pct = lambda path="/": (96, 30)
    try:
        detections = t3.detect_resource_exhaustion()
        disk = [d for d in detections if d["kind"] == "disk_full" and d.get("severity") == "critical"]
        if not disk:
            _record("resource.disk_hard", False, f"no critical detections: {detections}")
            return
        d = disk[0]
        plan = t3._plan_and_execute_detection(d, "resource", dry=True)
        tier = plan.get("tier")
        if tier == "tier1":
            _record("resource.disk_hard", False,
                    f"hard threshold should not classify as tier1 inline: {plan}")
            return
        _record("resource.disk_hard", True,
                f"level={d['level']}, dry tier={tier} (escalates, not inline)")
    finally:
        t3._disk_usage_pct = orig


# ── trigger 4: failure of failure-handler ────────────────────────────────────

def test_failed_handler():
    """Backdate self_heal_state.json mtime to 30min ago (grace=15min) → handler
    detector fires."""
    # Ensure all handler state files exist + are fresh, except self_heal_state.
    now = time.time()
    for path in (t3.CRASHLOOP_STATE, t3.SPRINT_INTEGRITY_STATE, t3.CRON_HEALTH_STATE):
        with open(path, "w") as f:
            f.write("{}")
        os.utime(path, (now, now))
    with open(t3.SELF_HEAL_STATE, "w") as f:
        f.write('{"subsystems": {}}')
    backdate = now - (30 * 60)
    os.utime(t3.SELF_HEAL_STATE, (backdate, backdate))

    detections = t3.detect_failed_handler()
    stale = [d for d in detections if d.get("component") == "handler:self_heal_controller"]
    if not stale:
        _record("handler.stale", False, f"no stale handler detected: {detections}")
        return
    d = stale[0]
    plan = t3._plan_and_execute_detection(d, "handler", dry=True)
    if plan.get("tier") != "tier1":
        _record("handler.stale", False,
                f"expected tier1 (kick handler inline), got {plan.get('tier')}: {plan}")
        return
    _record("handler.stale", True,
            f"age={d.get('age_min'):.1f}min, dry tier=tier1 (would kick handler inline)")


# ── tier3 routing — verify Chris-action escalation path exists ───────────────

def test_irreversible_routes_to_tier3():
    """Synthesize a finding whose suggested_action explicitly proposes an
    irreversible action; confirm vidar_tier classifies it as tier3 so the
    Chris-action path fires (not tier1 inline)."""
    finding = t3._make_finding(
        "smoke_test", "fake_component",
        "Smoke: irreversible cleanup proposed",
        "Test evidence: simulated state.",
        "Permanently delete all elite_0..elite_9 backups and reseed (irrecoverable).",
        severity="critical",
    )
    sys.path.insert(0, os.path.join(WORKSPACE, "research"))
    from vidar_tier import classify_finding
    tier, rationale = classify_finding(finding, audit_ts="smoke-test")
    if tier != "tier3":
        _record("routing.tier3_keyword", False,
                f"expected tier3 for irreversible action, got {tier} ({rationale})")
        return
    _record("routing.tier3_keyword", True, f"tier3 ({rationale[:70]})")


def main():
    print("== self_heal_tier3 smoke test ==")
    fix = setup_fixtures()
    try:
        test_cascading_failure()
        test_paired_degradation()
        test_cross_component_drift()
        test_resource_soft()
        test_resource_hard()
        test_failed_handler()
        test_irreversible_routes_to_tier3()
    finally:
        # Clean up fixture dir.
        try:
            shutil.rmtree(fix)
        except OSError:
            pass

    print()
    print(f"== summary: {len(PASS)} passed, {len(FAIL)} failed ==")
    for name, detail in FAIL:
        print(f"  FAIL: {name}  {detail}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
