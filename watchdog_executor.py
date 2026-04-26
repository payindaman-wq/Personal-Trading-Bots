#!/usr/bin/env python3
"""
watchdog_executor.py — auto-fix layer for league_watchdog alerts.

Polls syn_inbox.jsonl for source==league_watchdog entries with severity in
{error, warning} and applies tier-classified remediation:

  tier1 (auto):     stale_tick, no_mtm -> run the league tick script directly.
                    Up to 3 attempts in 30 min before escalating to tier3.
  tier2 (flag):     dead_execution -> write competition/watchdog_pending_review.flag
                    with proposed backfill/restart action. Human ack within 24h.
  tier3 (escalate): cascading failures -> emit syn_inbox critical with
                    tg_allowed:true so sys_heartbeat pages Chris.

State:  competition/watchdog_executor_state.json
  {version, alerts: {alert_id: {attempts, first_seen, last_action_ts, status, ...}}}

Idempotent: already-resolved or already-escalated alerts are skipped.

Tiers for known alert types (deterministic, no LLM spend):
  tier1: stale_tick, no_mtm
  tier2: dead_execution
  unknown types fall through to vidar_tier.classify_finding() (Sonnet 4.6, cached).
  No new Anthropic client — vidar_tier owns that.

Cron: */10 * * * *
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta

WORKSPACE           = "/root/.openclaw/workspace"
COMPETITION         = os.path.join(WORKSPACE, "competition")
RESEARCH            = os.path.join(WORKSPACE, "research")
SYN_INBOX           = os.path.join(WORKSPACE, "syn_inbox.jsonl")
STATE_FILE          = os.path.join(COMPETITION, "watchdog_executor_state.json")
PENDING_REVIEW_FLAG = os.path.join(COMPETITION, "watchdog_pending_review.flag")

# Cron-based tick scripts — no systemd service exists for league ticks.
TICK_COMMANDS = {
    "day":           ["python3", "/root/.openclaw/skills/competition-tick/scripts/competition_tick.py"],
    "swing":         ["python3", os.path.join(WORKSPACE, "swing_competition_tick.py")],
    "futures_day":   ["python3", os.path.join(WORKSPACE, "futures_day_competition_tick.py")],
    "futures_swing": ["python3", os.path.join(WORKSPACE, "futures_swing_competition_tick.py")],
}

# Deterministic tiers for known alert types.
# Unknown types fall through to vidar_tier.classify_finding() (Sonnet 4.6, cached).
TIER1_ALERT_TYPES = {"stale_tick", "no_mtm"}
TIER2_ALERT_TYPES = {"dead_execution"}

MAX_TIER1_ATTEMPTS        = 3
TIER1_WINDOW_MINUTES      = 30
REOPEN_ESCALATE_HOURS     = 1
# watchdog health-state cooldown is 6h; +1h buffer for clock skew.
ALERT_ACTIVE_WINDOW_HOURS = 7


# ── utilities ─────────────────────────────────────────────────────────────────

def _ts_iso():
    return datetime.now(timezone.utc).isoformat()


def _now_utc():
    return datetime.now(timezone.utc)


def _parse_ts(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def _atomic_write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _append_jsonl(path, rec):
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")


# ── state ─────────────────────────────────────────────────────────────────────

def _load_state():
    if not os.path.exists(STATE_FILE):
        return {"version": 1, "alerts": {}}
    try:
        with open(STATE_FILE) as f:
            d = json.load(f)
        d.setdefault("alerts", {})
        return d
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "alerts": {}}


# ── pending review flag (same schema as vidar_pending_review.flag) ─────────────

def _load_pending_review():
    if not os.path.exists(PENDING_REVIEW_FLAG):
        return {"entries": []}
    try:
        with open(PENDING_REVIEW_FLAG) as f:
            d = json.load(f)
        d.setdefault("entries", [])
        return d
    except (json.JSONDecodeError, OSError):
        return {"entries": []}


def _write_pending_review_entry(league, alert_id, sprint_id, evidence, dry_run):
    if dry_run:
        print(f"  [dry-run] watchdog_pending_review.flag <- {alert_id}")
        return
    state = _load_pending_review()
    deadline = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    state["entries"] = [e for e in state["entries"] if e.get("alert_id") != alert_id]
    state["entries"].append({
        "alert_id":        alert_id,
        "league":          league,
        "sprint_id":       sprint_id,
        "detected_ts":     _ts_iso(),
        "deadline_ts":     deadline,
        "proposed_action": (
            f"Diagnose {league} sprint {sprint_id}: check "
            f"competition/{league}/tick.log and competition/cron.log. "
            f"Use sprint_backfill.py to backfill from 09:00 UTC reset, "
            f"or abandon sprint and start fresh if trades are truly absent."
        ),
        "revert_note":     "No auto-action taken for dead_execution — human ack required.",
        "evidence":        evidence[:400],
    })
    state["last_updated"] = _ts_iso()
    _atomic_write_json(PENDING_REVIEW_FLAG, state)


# ── syn_inbox parsing ──────────────────────────────────────────────────────────

def _read_watchdog_errors():
    """All league_watchdog error/warning rows from syn_inbox, sorted by ts."""
    if not os.path.exists(SYN_INBOX):
        return []
    rows = []
    try:
        with open(SYN_INBOX) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if (rec.get("source") == "league_watchdog"
                        and rec.get("severity") in ("error", "warning")):
                    rows.append(rec)
    except OSError:
        return []
    rows.sort(key=lambda r: r.get("ts", ""))
    return rows


def _parse_alert_id(rec):
    """
    Return alert_id string for a league_watchdog inbox record.

    New records carry an explicit alert_id field (added in the league_watchdog.py
    edit that ships with this module).

    Legacy records are derived from the HTML msg body:
      - league:  extracted from [<league>] header tag
      - type:    extracted from DEAD EXECUTION / NO MTM TRACKING / TICK STALE
      - sprint:  first <code>...</code> block matching only [\\w-]+ chars
                 (the fix-prompt block has spaces so it won't match)
    """
    if rec.get("alert_id"):
        return rec["alert_id"]

    msg = rec.get("msg", "")
    league = None
    for lg in ("futures_day", "futures_swing", "day", "swing"):
        if f"[{lg}]" in msg:
            league = lg
            break
    if not league:
        return None

    atype = None
    if "DEAD EXECUTION" in msg:
        atype = "dead_execution"
    elif "NO MTM TRACKING" in msg:
        atype = "no_mtm"
    elif "TICK STALE" in msg:
        atype = "stale_tick"
    if not atype:
        return None

    m = re.search(r"<code>([\w-]+)</code>", msg)
    sprint_id = m.group(1) if m else "unknown"
    return f"{league}:{atype}:{sprint_id}"


# ── tier classification ────────────────────────────────────────────────────────

def _classify_alert(alert_id):
    """
    Fast-path deterministic classification for known alert types.
    Falls back to vidar_tier.classify_finding() (Sonnet 4.6, prompt-cached)
    for unrecognised types. No new Anthropic client here — vidar_tier owns it.
    """
    parts      = alert_id.split(":") if alert_id else []
    alert_type = parts[1] if len(parts) >= 2 else ""

    if alert_type in TIER1_ALERT_TYPES:
        return "tier1", f"auto-fix: {alert_type} is reversible (run tick script)"
    if alert_type in TIER2_ALERT_TYPES:
        return "tier2", f"capital-adjacent: {alert_type} requires human review"

    sys.path.insert(0, RESEARCH)
    try:
        from vidar_tier import classify_finding  # noqa: WPS433
        finding = {
            "id":               alert_id,
            "severity":         "error",
            "title":            f"League watchdog unknown alert: {alert_id}",
            "evidence":         f"league_watchdog emitted alert_id={alert_id}; no known handler",
            "suggested_action": "Restart the affected league tick script and monitor for recovery.",
        }
        return classify_finding(finding, audit_ts="watchdog_executor_v1")
    except Exception as e:
        print(f"  [watchdog_executor] vidar_tier fallback error ({e}); defaulting tier1", file=sys.stderr)
        return "tier1", "vidar_tier unavailable, conservative default"


# ── cascading detection ────────────────────────────────────────────────────────

def _is_cascading(entry, now):
    """
    Returns (True, reason_str) when tier3 escalation is warranted:
      - >= MAX_TIER1_ATTEMPTS within TIER1_WINDOW_MINUTES, OR
      - alert reappeared within REOPEN_ESCALATE_HOURS of last resolution.
    """
    attempts   = entry.get("attempts", 0)
    first_seen = _parse_ts(entry.get("first_seen"))
    last_res   = _parse_ts(entry.get("last_resolved_ts"))

    if attempts >= MAX_TIER1_ATTEMPTS and first_seen:
        elapsed_min = (now - first_seen).total_seconds() / 60
        if elapsed_min <= TIER1_WINDOW_MINUTES:
            return True, f"{attempts} attempts in {elapsed_min:.0f}m (<={TIER1_WINDOW_MINUTES}m limit)"

    if last_res:
        reopen_h = (now - last_res).total_seconds() / 3600
        if reopen_h <= REOPEN_ESCALATE_HOURS:
            return True, f"reopened {reopen_h:.1f}h after last resolution (<={REOPEN_ESCALATE_HOURS}h limit)"

    return False, ""


# ── actions ────────────────────────────────────────────────────────────────────

def _run_tick(league, dry_run):
    cmd = TICK_COMMANDS.get(league)
    if not cmd:
        return False, f"no tick command configured for league={league}"
    if dry_run:
        return True, f"[dry-run] would run: {' '.join(cmd)}"
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            cwd=WORKSPACE, timeout=120,
        )
        ok      = result.returncode == 0
        snippet = (result.stdout + result.stderr).strip()[:500]
        return ok, snippet
    except subprocess.TimeoutExpired:
        return False, "tick script timed out after 120s"
    except Exception as e:
        return False, str(e)[:300]


def _emit_critical(alert_id, reason, dry_run):
    rec = {
        "ts":         _ts_iso(),
        "source":     "watchdog_executor",
        "severity":   "critical",
        "alert_id":   alert_id,
        "msg":        (
            f"[OPS/watchdog_executor] Cascading failure on {alert_id}: "
            f"{reason}. Manual intervention required."
        ),
        "tg_allowed": True,
    }
    if dry_run:
        print(f"  [dry-run] emit_critical: {json.dumps(rec)}")
        return
    _append_jsonl(SYN_INBOX, rec)


# ── main processing loop ───────────────────────────────────────────────────────

def process_alerts(dry_run=False):
    all_errors = _read_watchdog_errors()
    if not all_errors:
        print("[watchdog_executor] no league_watchdog error entries in syn_inbox")
        return {"processed": 0}

    state = _load_state()
    now   = _now_utc()

    # Most-recent error record per alert_id
    latest: dict[str, dict] = {}
    for rec in all_errors:
        aid = _parse_alert_id(rec)
        if not aid:
            continue
        if rec.get("ts", "") >= latest.get(aid, {}).get("ts", ""):
            latest[aid] = rec

    # Active = within the health-state cooldown window (ALERT_ACTIVE_WINDOW_HOURS)
    active: dict[str, dict] = {}
    for aid, rec in latest.items():
        ts = _parse_ts(rec.get("ts"))
        if ts and (now - ts).total_seconds() / 3600 <= ALERT_ACTIVE_WINDOW_HOURS:
            active[aid] = rec

    summary = {
        "tier1_fix":      0,
        "tier2_flag":     0,
        "tier3_escalate": 0,
        "skipped":        0,
        "resolved":       0,
    }

    # Mark state entries as resolved when no longer active
    for aid, entry in list(state["alerts"].items()):
        if (aid not in active
                and entry.get("status") not in ("resolved", "escalated", "transient_documented")):
            print(f"  [watchdog_executor] {aid}: no longer active -> resolved")
            if not dry_run:
                entry["status"]           = "resolved"
                entry["last_resolved_ts"] = _ts_iso()
            summary["resolved"] += 1

    # Process each active alert
    for aid, rec in active.items():
        parts      = aid.split(":")
        league     = parts[0] if len(parts) >= 1 else "unknown"
        sprint_id  = parts[2] if len(parts) >= 3 else "unknown"

        # Known transient: futures_day resume cycle fired a stale_tick at
        # 2026-04-25T23:30 while the service was re-initialising post-resume
        # (commit 8c6585a). Document in state; do not run tick.
        if aid == "futures_day:stale_tick:fut-day-20260425-0900":
            if aid not in state["alerts"]:
                print(
                    f"  [watchdog_executor] {aid}: known futures_day resume "
                    f"transient (2026-04-25); documenting in state, no action"
                )
                if not dry_run:
                    state["alerts"][aid] = {
                        "alert_id":        aid,
                        "tier":            "tier1",
                        "first_seen":      rec.get("ts", _ts_iso()),
                        "attempts":        0,
                        "last_action_ts":  None,
                        "status":          "transient_documented",
                        "last_resolved_ts": None,
                        "note": (
                            "futures_day resume cycle transient 2026-04-25T23:30; "
                            "no action per spec (commit 8c6585a re-init window)"
                        ),
                    }
            else:
                print(f"  [watchdog_executor] {aid}: transient already documented")
            summary["skipped"] += 1
            continue

        # Initialise state for new alerts
        if aid not in state["alerts"]:
            state["alerts"][aid] = {
                "alert_id":        aid,
                "first_seen":      rec.get("ts", _ts_iso()),
                "attempts":        0,
                "last_action_ts":  None,
                "status":          "pending",
                "last_resolved_ts": None,
            }
        entry = state["alerts"][aid]

        # Terminal states — skip until next watchdog run clears or re-fires
        if entry.get("status") in ("escalated", "flagged"):
            print(f"  [watchdog_executor] {aid}: skipped (status={entry['status']})")
            summary["skipped"] += 1
            continue

        # Cascading check overrides normal classification
        cascading, cascade_reason = _is_cascading(entry, now)
        if cascading:
            tier           = "tier3"
            tier_rationale = f"cascading: {cascade_reason}"
        else:
            tier, tier_rationale = _classify_alert(aid)

        print(f"  [watchdog_executor] {aid}: tier={tier}  ({tier_rationale[:100]})")
        if not dry_run:
            entry["tier"] = tier

        if tier == "tier3":
            _emit_critical(aid, cascade_reason or tier_rationale, dry_run)
            if not dry_run:
                entry["status"]         = "escalated"
                entry["last_action_ts"] = _ts_iso()
            summary["tier3_escalate"] += 1

        elif tier == "tier1":
            ok, output = _run_tick(league, dry_run)
            if not dry_run:
                entry["attempts"]       = entry.get("attempts", 0) + 1
                entry["last_action_ts"] = _ts_iso()
                entry["status"]         = "auto_fix_attempted"
                entry["last_tick_ok"]   = ok
                entry["last_output"]    = output[:300]
            label = "ok" if ok else "FAILED"
            print(f"  [watchdog_executor] {aid}: tick {label}  | {output[:120]}")
            summary["tier1_fix"] += 1

        elif tier == "tier2":
            _write_pending_review_entry(
                league, aid, sprint_id, rec.get("msg", "")[:400], dry_run,
            )
            if not dry_run:
                entry["status"]         = "flagged"
                entry["last_action_ts"] = _ts_iso()
            summary["tier2_flag"] += 1

    if not dry_run:
        _atomic_write_json(STATE_FILE, state)

    return summary


def main():
    p = argparse.ArgumentParser(
        description="watchdog_executor — auto-fix layer for league_watchdog alerts"
    )
    p.add_argument("--dry-run", action="store_true",
                   help="show what would happen; no writes, no commands")
    args = p.parse_args()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M UTC")
    print(f"[watchdog_executor] {now_str}  dry_run={args.dry_run}")
    summary = process_alerts(dry_run=args.dry_run)
    print(f"[watchdog_executor] done. {json.dumps(summary)}")


if __name__ == "__main__":
    main()
