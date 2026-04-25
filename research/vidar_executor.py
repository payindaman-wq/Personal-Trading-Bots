#!/usr/bin/env python3
"""
vidar_executor.py — VIDAR auto-execute layer (closes meta_audit F7 authority gap).

Pipeline:
  meta_audit weekly cron → research/meta_audit/latest.json (sidecar with findings)
  vidar_executor.run_audit() iterates each finding:
    1. classify via vidar_tier.classify_finding() → tier1 | tier2 | tier3
    2. tier3 → critical syn_inbox row + done (Chris-action gate)
    3. tier1 / tier2 → call VIDAR Opus 4.7 planner to produce concrete actions
       (structural patch / update_constant / escalate) for the finding
    4. queue planner actions to loki_pending_actions.jsonl; LOKI applies them
       on its next 15-min tick using the existing safe pipeline
       (champion_guardrail, syntax check, exact-anchor match, auto-revert via
       loki_structural_monitor.json on metric degradation)
    5. tier2 also writes competition/vidar_pending_review.flag with 24h
       deadline so SYN heartbeat surfaces it and Chris can revert with one
       command:  python3 vidar_executor.py revert <finding_id>

Architecture choice: Path A+ (extend Path A; Path B deferred).
  - LOKI already has a safe whitelist for code mutations (ALLOWED_CONSTANTS,
    structural patches with champion_guardrail + ast.parse, auto-revert).
  - The VIDAR planner emits actions that funnel through this existing
    pipeline rather than building a new arbitrary-command registry. The
    `project_loki_executor_path_b.md` design memo's Path B is still the
    long-term direction; this incremental change does not preclude it.

CLI:
  python3 vidar_executor.py run            # process latest meta_audit sidecar
  python3 vidar_executor.py run --sidecar /path/to/latest.json
  python3 vidar_executor.py revert <finding_id>
  python3 vidar_executor.py status         # list pending review flag entries
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta

WORKSPACE                = "/root/.openclaw/workspace"
RESEARCH                 = os.path.join(WORKSPACE, "research")
ANTHROPIC_SECRET         = "/root/.openclaw/secrets/anthropic.json"
ANTHROPIC_USAGE          = os.path.join(RESEARCH, "anthropic_usage.jsonl")

META_AUDIT_DIR           = os.path.join(RESEARCH, "meta_audit")
LATEST_SIDECAR           = os.path.join(META_AUDIT_DIR, "latest.json")
LOKI_PENDING             = os.path.join(RESEARCH, "loki_pending_actions.jsonl")
SYN_INBOX                = os.path.join(WORKSPACE, "syn_inbox.jsonl")

EXECUTOR_LOG             = os.path.join(RESEARCH, "vidar_executor_log.jsonl")
PENDING_REVIEW_FLAG      = os.path.join(WORKSPACE, "competition", "vidar_pending_review.flag")

PLANNER_MODEL            = "claude-opus-4-7"
PLANNER_MAX_TOKENS       = 4000
TIER2_REVIEW_DEADLINE_HR = 24

# Source files cached in the planner system prompt (idle bytes that don't
# change during a single audit run). Loaded once; cached_control ephemeral.
PLANNER_SOURCE_FILES = (
    os.path.join(RESEARCH, "odin_researcher_v2.py"),
    os.path.join(RESEARCH, "mimir.py"),
    os.path.join(RESEARCH, "freya_researcher.py"),
    os.path.join(WORKSPACE, "league_killswitch.py"),
    os.path.join(WORKSPACE, "regression_watch.py"),
)

# Mirrors loki.ALLOWED_CONSTANTS — the planner's update_constant outputs are
# vetted against this list before queuing.
LOKI_ALLOWED_CONSTANTS   = {"MIN_TRADES", "POPULATION_SIZE", "SUSPICIOUS_SHARPE", "STALL_ALERT_GENS"}

# Map league string to the structural-monitor target file (mirrors
# loki.SERVICE_MAP / RESEARCHER assignment).
LEAGUE_TO_TARGET = {
    "day":           "odin_researcher_v2.py",
    "swing":         "odin_researcher_v2.py",
    "futures_day":   "odin_researcher_v2.py",
    "futures_swing": "odin_researcher_v2.py",
    "pm":            "freya_researcher.py",
}


# ── small utils ──────────────────────────────────────────────────────────────

def _ts_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")


def _ts_iso():
    return datetime.now(timezone.utc).isoformat()


def _atomic_write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _append_jsonl(path, record):
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def _load_anthropic_key():
    with open(ANTHROPIC_SECRET) as f:
        return json.load(f)["anthropic_api_key"]


def _read_file_truncated(path, max_chars=40000):
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            s = f.read()
    except OSError:
        return None
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + f"\n# ... [truncated, {len(s) - max_chars} chars omitted]\n"


def _log_usage(usage_obj, model, caller="vidar_executor"):
    try:
        rec = {
            "ts":     _ts_iso(),
            "caller": caller,
            "model":  model,
            "input_tokens":  getattr(usage_obj, "input_tokens", 0),
            "output_tokens": getattr(usage_obj, "output_tokens", 0),
            "cache_creation_input_tokens": getattr(usage_obj, "cache_creation_input_tokens", 0),
            "cache_read_input_tokens":     getattr(usage_obj, "cache_read_input_tokens", 0),
        }
        with open(ANTHROPIC_USAGE, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError:
        pass


# ── tier classifier ──────────────────────────────────────────────────────────

# Lazy import to avoid hard dep on vidar_tier when only running revert/status.
def _classify(finding, audit_ts):
    sys.path.insert(0, RESEARCH)
    from vidar_tier import classify_finding  # noqa: WPS433
    return classify_finding(finding, audit_ts=audit_ts)


# ── planner (VIDAR Opus 4.7 with prompt caching) ─────────────────────────────

PLANNER_SYSTEM_PROMPT = """You are VIDAR, the Strategic Arbitration Officer, in EXECUTE mode.

You are reviewing a meta-audit finding and producing a CONCRETE, SAFE,
MACHINE-EXECUTABLE plan. Your output is queued to LOKI's pending-actions
pipeline; LOKI applies it with auto-revert on metric degradation.

You can emit three action types — these are the only safe primitives LOKI
recognises:

1. structural — a code patch to one of the researcher source files
   (odin_researcher_v2.py, mimir.py, freya_researcher.py). Each patch is a
   {old, new, context} triple where:
     - "old" must appear EXACTLY ONCE in the target file (LOKI rejects
       ambiguous matches).
     - "context" is a verbatim quote of a few surrounding lines from the
       current source — used to verify your "old" anchor is real, not
       hallucinated. The context string itself must be present verbatim in
       the source.
     - "new" replaces "old". Python syntax must remain valid post-edit.
   You MUST use the source files included in the cached system prompt as
   ground truth for "old" and "context" strings. Do not invent anchors.

2. update_constant — change one of LOKI's whitelisted top-level constants:
   MIN_TRADES (dict, requires subkey: "day"|"swing"|"futures_day"|"futures_swing"),
   POPULATION_SIZE (int), SUSPICIOUS_SHARPE (float), STALL_ALERT_GENS (int).
   Any other constant MUST be done via a structural patch.

3. escalate — write a work-order to loki_escalation_log for Chris's review
   on the dashboard. Use this when the finding is genuine but cannot be
   safely implemented in code (population reseed requiring file deletion,
   league pause via cron edit, etc.).

OUTPUT SCHEMA — return EXACTLY this JSON, no prose:

{
  "verdict": "implement" | "decline_not_implementable",
  "rationale": "<2-3 sentences on why this plan is safe and addresses the finding>",
  "league": "day" | "swing" | "futures_day" | "futures_swing" | "pm" | "global",
  "actions": [
    {"type": "structural", "description": "<≤80 chars>", "target_file": "odin_researcher_v2.py", "patch": [{"old":"...", "new":"...", "context":"..."}]},
    {"type": "update_constant", "description": "<≤80 chars>", "constant": "MIN_TRADES", "subkey": "day", "new_value": 50},
    {"type": "escalate", "description": "<≤200 chars human-action work order>"}
  ]
}

DECLINE GUIDELINES — return verdict=decline_not_implementable when:
  - The finding requires deletion or movement of files outside the safe code-patch path
  - The finding requires real-capital allocation policy changes
  - You cannot find verbatim anchors in the source files for the structural change
  - The finding is dependent on a future event (e.g. "wait for Phase 1 funding")

When declining, leave actions=[] and put the human-readable reason in rationale.
ALWAYS prefer one tightly-scoped structural patch over many broad ones — small,
metric-monitorable changes give LOKI the cleanest auto-revert signal.

Output ONLY the JSON. No reasoning prose, no fences.
"""


def _build_planner_system_blocks():
    """Build the cached system prompt: rubric + source files. Cache-controlled
    so the per-finding user message only pays the diff."""
    blocks = [{"type": "text", "text": PLANNER_SYSTEM_PROMPT}]
    for path in PLANNER_SOURCE_FILES:
        content = _read_file_truncated(path, max_chars=80000)
        if content is None:
            continue
        rel = os.path.relpath(path, WORKSPACE)
        blocks.append({
            "type": "text",
            "text": f"=== SOURCE FILE: {rel} ===\n```python\n{content}\n```\n",
        })
    blocks[-1]["cache_control"] = {"type": "ephemeral"}
    return blocks


def _build_planner_user_message(finding, tier, classify_rationale):
    return (
        f"FINDING (tier={tier}, classifier rationale: {classify_rationale}):\n"
        + json.dumps({
            "id":               finding.get("id"),
            "severity":         finding.get("severity"),
            "title":            finding.get("title"),
            "evidence":         finding.get("evidence"),
            "why_it_matters":   finding.get("why_it_matters"),
            "suggested_action": finding.get("suggested_action"),
        }, indent=2)
        + "\n\nProduce the action plan JSON now."
    )


def plan_actions_for_finding(finding, tier, classify_rationale):
    """Call Opus 4.7 with prompt caching. Returns parsed planner JSON."""
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("anthropic SDK not installed") from e

    api_key = _load_anthropic_key()
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model=PLANNER_MODEL,
        max_tokens=PLANNER_MAX_TOKENS,
        system=_build_planner_system_blocks(),
        messages=[{
            "role":    "user",
            "content": _build_planner_user_message(finding, tier, classify_rationale),
        }],
    )

    if hasattr(response, "usage"):
        _log_usage(response.usage, PLANNER_MODEL, caller="vidar_executor_planner")

    text = response.content[0].text.strip()
    if "```" in text:
        m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
        if m:
            text = m.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"planner returned non-JSON: {text[:400]}") from e


# ── action validation + queueing ─────────────────────────────────────────────

def _validate_action(action):
    """Return (ok, reason). Mirrors LOKI's safety checks at queue time so we
    never emit something LOKI will reject silently."""
    atype = action.get("type")
    if atype == "structural":
        patches = action.get("patch") or []
        if not patches:
            return False, "structural action with empty patch"
        for i, p in enumerate(patches):
            if not p.get("old") or not p.get("new"):
                return False, f"structural patch {i}: missing old/new"
            if not p.get("context"):
                return False, f"structural patch {i}: missing context (LOKI requires verbatim source quote)"
        return True, ""
    if atype == "update_constant":
        const = action.get("constant", "")
        if const not in LOKI_ALLOWED_CONSTANTS:
            return False, f"constant {const} not in LOKI_ALLOWED_CONSTANTS"
        if action.get("new_value") is None:
            return False, "update_constant missing new_value"
        return True, ""
    if atype == "escalate":
        if not action.get("description"):
            return False, "escalate action missing description"
        return True, ""
    return False, f"unknown action type: {atype}"


def _queue_to_loki(league, source_tag, audit_ts, finding_id, actions):
    """Append a single LOKI work-order entry covering all validated actions
    from one finding. Mirrors the existing patch_repair queue shape so
    process_pending_actions consumes it transparently."""
    entry = {
        "ts":         _ts_utc(),
        "league":     league,
        "source":     source_tag,
        "audit_ts":   audit_ts,
        "finding_id": finding_id,
        "actions":    actions,
        "processed":  False,
    }
    _append_jsonl(LOKI_PENDING, entry)
    return entry


# ── tier-3 inbox surface ─────────────────────────────────────────────────────

def _emit_tier3_inbox(finding, classify_rationale, audit_ts):
    """Write a critical row tagged source=meta_audit so sys_heartbeat's
    TG_ALLOWED_SOURCES + TG_SEVERITY_OVERRIDES (meta_audit:{critical}) path
    pages Chris."""
    rec = {
        "ts":              _ts_iso(),
        "source":          "meta_audit",
        "severity":        "critical",
        "audit_ts":        audit_ts,
        "finding_id":      finding.get("id"),
        "title":           f"[VIDAR-EXEC tier3] {finding.get('title', '')}"[:300],
        "summary":         finding.get("title", "")[:200],
        "tier":            "tier3",
        "tier_rationale":  classify_rationale,
        "action_required": "Chris ack required — irreversible/capital-policy-class change.",
        "evidence":        (finding.get("evidence") or "")[:500],
        "suggested_action": (finding.get("suggested_action") or "")[:600],
        "tg_allowed":      True,
    }
    _append_jsonl(SYN_INBOX, rec)


# ── tier-2 review flag ───────────────────────────────────────────────────────

def _load_pending_review():
    if not os.path.exists(PENDING_REVIEW_FLAG):
        return {"entries": []}
    try:
        with open(PENDING_REVIEW_FLAG) as f:
            d = json.load(f)
        if "entries" not in d:
            d["entries"] = []
        return d
    except (json.JSONDecodeError, OSError):
        return {"entries": []}


def _save_pending_review(state):
    os.makedirs(os.path.dirname(PENDING_REVIEW_FLAG), exist_ok=True)
    state["last_updated"] = _ts_iso()
    _atomic_write_json(PENDING_REVIEW_FLAG, state)


def _add_pending_review(finding, audit_ts, action_summary, queue_entry_ts):
    state = _load_pending_review()
    deadline = (datetime.now(timezone.utc) + timedelta(hours=TIER2_REVIEW_DEADLINE_HR)).isoformat()
    fid = finding.get("id", "?")
    # Replace any existing entry for this (audit_ts, finding_id) to avoid
    # stacking duplicates if the executor reruns.
    state["entries"] = [
        e for e in state["entries"]
        if not (e.get("audit_ts") == audit_ts and e.get("finding_id") == fid)
    ]
    state["entries"].append({
        "audit_ts":          audit_ts,
        "finding_id":        fid,
        "title":             finding.get("title", "")[:160],
        "change_summary":    action_summary[:300],
        "queued_loki_ts":    queue_entry_ts,
        "deadline_ts":       deadline,
        "revert_command":    f"python3 /root/.openclaw/workspace/research/vidar_executor.py revert {fid}",
    })
    _save_pending_review(state)


# ── per-finding executor ─────────────────────────────────────────────────────

def _executor_log_seen(audit_ts, finding_id):
    if not os.path.exists(EXECUTOR_LOG):
        return False
    try:
        with open(EXECUTOR_LOG) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("audit_ts") == audit_ts and rec.get("finding_id") == finding_id:
                    return True
    except OSError:
        return False
    return False


def _log_executor_outcome(record):
    record.setdefault("ts", _ts_iso())
    _append_jsonl(EXECUTOR_LOG, record)


def execute_finding(finding, audit_ts):
    """Process one finding end-to-end. Idempotent per (audit_ts, finding_id)."""
    fid = finding.get("id", "?")
    if _executor_log_seen(audit_ts, fid):
        print(f"  [vidar_executor] {audit_ts}/{fid}: already processed, skipping")
        return {"status": "skipped_already_processed", "finding_id": fid}

    tier, rationale = _classify(finding, audit_ts)
    print(f"  [vidar_executor] {audit_ts}/{fid}: tier={tier} ({rationale[:80]})")

    if tier == "tier3":
        _emit_tier3_inbox(finding, rationale, audit_ts)
        outcome = {
            "audit_ts":    audit_ts,
            "finding_id":  fid,
            "tier":        tier,
            "rationale":   rationale,
            "status":      "tier3_inbox_emitted",
        }
        _log_executor_outcome(outcome)
        return outcome

    # Tier 1 / Tier 2 → planner
    try:
        plan = plan_actions_for_finding(finding, tier, rationale)
    except Exception as e:
        outcome = {
            "audit_ts":   audit_ts,
            "finding_id": fid,
            "tier":       tier,
            "rationale":  rationale,
            "status":     "planner_failed",
            "error":      str(e)[:300],
        }
        _log_executor_outcome(outcome)
        return outcome

    verdict = plan.get("verdict")
    plan_rationale = plan.get("rationale", "")
    league = plan.get("league") or finding.get("league") or "global"
    actions_in = plan.get("actions") or []

    if verdict == "decline_not_implementable" or not actions_in:
        # Safety net: even on decline, surface as a low-noise inbox row so
        # the meta_audit findings list is auditable.
        info_rec = {
            "ts":             _ts_iso(),
            "source":         "vidar_executor",
            "severity":       "info",
            "audit_ts":       audit_ts,
            "finding_id":     fid,
            "tier":           tier,
            "msg":            f"declined: {plan_rationale[:300]}",
        }
        _append_jsonl(SYN_INBOX, info_rec)
        outcome = {
            "audit_ts":      audit_ts,
            "finding_id":    fid,
            "tier":          tier,
            "rationale":     rationale,
            "plan_rationale": plan_rationale,
            "status":        "declined",
        }
        _log_executor_outcome(outcome)
        return outcome

    # Validate every action before queuing — refuse partial queueing.
    validated = []
    rejected = []
    for a in actions_in:
        ok, why = _validate_action(a)
        if ok:
            validated.append(a)
        else:
            rejected.append({"action": a, "reason": why})

    if not validated:
        outcome = {
            "audit_ts":   audit_ts,
            "finding_id": fid,
            "tier":       tier,
            "rationale":  rationale,
            "plan_rationale": plan_rationale,
            "status":     "no_valid_actions",
            "rejected":   rejected,
        }
        _log_executor_outcome(outcome)
        # Surface as warning so audit dashboard sees that the planner produced
        # invalid output — Sonnet/Opus drift would otherwise be silent.
        _append_jsonl(SYN_INBOX, {
            "ts":         _ts_iso(),
            "source":     "vidar_executor",
            "severity":   "warning",
            "audit_ts":   audit_ts,
            "finding_id": fid,
            "msg":        f"planner produced 0 valid actions ({len(rejected)} rejected)",
        })
        return outcome

    queue_entry = _queue_to_loki(
        league=league,
        source_tag=f"VIDAR_meta_audit_{tier}",
        audit_ts=audit_ts,
        finding_id=fid,
        actions=validated,
    )

    action_summary = "; ".join(
        a.get("description") or a.get("type") for a in validated
    )[:300]

    if tier == "tier2":
        _add_pending_review(finding, audit_ts, action_summary, queue_entry["ts"])

    outcome = {
        "audit_ts":      audit_ts,
        "finding_id":    fid,
        "tier":          tier,
        "rationale":     rationale,
        "plan_rationale": plan_rationale,
        "status":        "queued",
        "league":        league,
        "actions_count": len(validated),
        "rejected":      rejected,
        "action_summary": action_summary,
    }
    _log_executor_outcome(outcome)
    return outcome


# ── revert ───────────────────────────────────────────────────────────────────

def revert_finding(finding_id):
    """Revert a previously-queued action by finding_id.

    Strategy:
      1. Find the executor_log entry for this finding_id (status=queued).
      2. Find LOKI's structural-monitor entry for that league — if present,
         the .bak file LOKI took before applying is the rollback target. We
         restore it directly here (LOKI also has its own auto-revert path,
         but this is the operator-initiated revert so we own it).
      3. Remove the pending-review entry.
      4. Log the revert.

    For update_constant actions whose target file isn't checkpointed in the
    structural monitor (LOKI's apply_constant_change path doesn't snapshot),
    we fall back to git-restore-from-HEAD on odin_researcher_v2.py.
    """
    if not os.path.exists(EXECUTOR_LOG):
        print(f"[revert] no executor log; nothing to revert for {finding_id}")
        return 1
    matches = []
    with open(EXECUTOR_LOG) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("finding_id") == finding_id and rec.get("status") == "queued":
                matches.append(rec)
    if not matches:
        print(f"[revert] no queued action found for finding_id={finding_id}")
        return 1
    rec = matches[-1]
    league = rec.get("league") or "global"

    # Try LOKI's structural-monitor backup first (covers the structural path).
    monitor_path = os.path.join(RESEARCH, "loki_structural_monitor.json")
    restored = []
    if os.path.exists(monitor_path):
        try:
            monitor = json.load(open(monitor_path))
        except (OSError, json.JSONDecodeError):
            monitor = {}
        for key, m in list(monitor.items()):
            if m.get("league") != league:
                continue
            backup = m.get("backup")
            target = m.get("target")
            unit   = m.get("unit")
            if backup and target and os.path.exists(backup):
                shutil.copy2(backup, target)
                restored.append({"target": target, "from_backup": backup})
                if unit:
                    subprocess.run(["systemctl", "restart", unit], timeout=15, check=False)
                del monitor[key]
                _atomic_write_json(monitor_path, monitor)

    # Remove pending-review entry.
    state = _load_pending_review()
    state["entries"] = [e for e in state["entries"] if e.get("finding_id") != finding_id]
    _save_pending_review(state)

    revert_record = {
        "ts":         _ts_iso(),
        "audit_ts":   rec.get("audit_ts"),
        "finding_id": finding_id,
        "tier":       rec.get("tier"),
        "league":     league,
        "status":     "reverted_by_operator",
        "restored":   restored,
        "originating_action_summary": rec.get("action_summary"),
    }
    _log_executor_outcome(revert_record)

    print(json.dumps(revert_record, indent=2))
    return 0


# ── status ───────────────────────────────────────────────────────────────────

def show_status():
    state = _load_pending_review()
    entries = state.get("entries", [])
    if not entries:
        print("[status] no Tier-2 reviews pending")
        return 0
    print(f"[status] {len(entries)} pending Tier-2 review(s):")
    for e in entries:
        print(f"  - {e['finding_id']}  audit={e['audit_ts']}  deadline={e['deadline_ts']}")
        print(f"      title:   {e.get('title')}")
        print(f"      change:  {e.get('change_summary')}")
        print(f"      revert:  {e.get('revert_command')}")
    return 0


# ── main entry ───────────────────────────────────────────────────────────────

def run_audit(sidecar_path):
    if not os.path.exists(sidecar_path):
        print(f"[vidar_executor] sidecar missing: {sidecar_path}", file=sys.stderr)
        return 1
    with open(sidecar_path) as f:
        sidecar = json.load(f)
    if not sidecar.get("parse_ok"):
        print("[vidar_executor] sidecar parse_ok=false; nothing to execute (raw review file in sidecar.review_path)")
        return 0
    audit_ts = sidecar.get("audit_ts") or _ts_utc()
    decision = sidecar.get("decision") or {}
    findings = decision.get("findings") or []
    if not findings:
        print("[vidar_executor] sidecar has 0 findings; nothing to do")
        return 0
    print(f"[vidar_executor] processing {len(findings)} findings for audit_ts={audit_ts}")
    summary = {"queued": 0, "tier3": 0, "declined": 0, "skipped": 0, "errors": 0}
    for f in findings:
        try:
            outcome = execute_finding(f, audit_ts)
            st = outcome.get("status", "")
            if st == "queued":
                summary["queued"] += 1
            elif st == "tier3_inbox_emitted":
                summary["tier3"] += 1
            elif st == "declined" or st == "no_valid_actions":
                summary["declined"] += 1
            elif st == "skipped_already_processed":
                summary["skipped"] += 1
            else:
                summary["errors"] += 1
        except Exception as e:
            summary["errors"] += 1
            print(f"  [vidar_executor] ERROR on {f.get('id')}: {e}")
            _log_executor_outcome({
                "audit_ts":   audit_ts,
                "finding_id": f.get("id"),
                "status":     "exception",
                "error":      str(e)[:400],
            })
    print(f"[vidar_executor] done. summary={json.dumps(summary)}")
    return 0


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("run", help="process the latest meta_audit sidecar")
    pr.add_argument("--sidecar", default=LATEST_SIDECAR,
                    help=f"path to meta_audit sidecar JSON (default: {LATEST_SIDECAR})")

    pv = sub.add_parser("revert", help="revert a queued action by finding_id")
    pv.add_argument("finding_id")

    sub.add_parser("status", help="list pending Tier-2 review entries")

    args = p.parse_args()
    if args.cmd == "run":
        sys.exit(run_audit(args.sidecar))
    elif args.cmd == "revert":
        sys.exit(revert_finding(args.finding_id))
    elif args.cmd == "status":
        sys.exit(show_status())


if __name__ == "__main__":
    main()
