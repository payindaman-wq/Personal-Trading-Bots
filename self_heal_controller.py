#!/usr/bin/env python3
"""
self_heal_controller.py — Tier 2 central controller (SYN/self_heal).

Runs every 5 min via cron. The audit+heal+escalate layer that sits ON TOP of
the individual watchdogs:
  - Does NOT re-probe APIs (the per-domain health checks already do that).
  - Reads EXISTING state signals: systemctl is-active + file mtimes.
  - For each registered subsystem, tracks consecutive-run health.
  - On 2nd consecutive "degraded" → attempt self-heal (systemctl restart).
  - If still degraded 2 cycles AFTER heal attempt → escalate via SYN (error).
  - On transition back to healthy → log recovery, reset counter.

Subsystem registry — all fields read from existing state; no new probes:
  - Liveness: odin_* services, freya, polymarket_syn.
  - Freshness: tyr_state.json (45m), heimdall_state.json (45m),
               per-league researcher.log (30m for odin, 60m for freya).

Writes unified:
  - self_heal_log.jsonl (every transition)
  - self_heal_state.json (per-subsystem rolling state)

Framework: Tier 2 rule #2. Tier 2 rule #1 is service_crashloop_watch.py.
"""
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/self_heal_state.json"
LOG_FILE = f"{WORKSPACE}/competition/self_heal_log.jsonl"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"
EXCHANGE_PAUSE_FLAG = f"{WORKSPACE}/competition/exchange_paused"
EXCHANGE_PAUSED_SERVICES = {"polymarket_syn"}

HEAL_AFTER_CONSECUTIVE = 2   # attempt self-heal at this many consecutive degraded runs
ESCALATE_AFTER_HEAL    = 2   # escalate if still degraded this many runs AFTER heal attempt

# ---------------------------------------------------------------------------
# Subsystem registry
# ---------------------------------------------------------------------------
# Each entry:
#   kind: "service" (uses systemctl is-active + systemctl restart)
#         "freshness" (mtime check; heal action optional)
#   name: identifier / service name / short slug
#   path: (freshness only) file to check mtime
#   max_age_min: (freshness only) threshold
#   heal_service: (freshness only, optional) systemctl service to restart on heal

SERVICES = [
    "odin_day",
    "odin_swing",
    "odin_futures_day",
    "odin_futures_swing",
    "freya",
    "polymarket_syn",
]

FRESHNESS_TARGETS = [
    {
        "name": "tyr_state",
        "path": f"{WORKSPACE}/research/tyr_state.json",
        "max_age_min": 45,
        "heal_service": None,  # tyr.py is cron-driven; no service to restart
    },
    {
        "name": "heimdall_state",
        "path": f"{WORKSPACE}/research/heimdall_state.json",
        "max_age_min": 45,
        "heal_service": None,
    },
    {
        "name": "researcher_log_day",
        "path": f"{WORKSPACE}/research/day/researcher.log",
        "max_age_min": 30,
        "heal_service": "odin_day",
    },
    {
        "name": "researcher_log_swing",
        "path": f"{WORKSPACE}/research/swing/researcher.log",
        "max_age_min": 30,
        "heal_service": "odin_swing",
    },
    {
        "name": "researcher_log_futures_day",
        "path": f"{WORKSPACE}/research/futures_day/researcher.log",
        "max_age_min": 30,
        "heal_service": "odin_futures_day",
    },
    {
        "name": "researcher_log_futures_swing",
        "path": f"{WORKSPACE}/research/futures_swing/researcher.log",
        "max_age_min": 30,
        "heal_service": "odin_futures_swing",
    },
    {
        "name": "researcher_log_pm",
        "path": f"{WORKSPACE}/research/pm/researcher.log",
        "max_age_min": 60,
        "heal_service": "freya",
    },
]


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"subsystems": {}}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, indent=2)
    os.replace(tmp, STATE_FILE)


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def log_jsonl(record):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        print(f"[self_heal/log] {e}")


def inbox_write(msg, severity="error"):
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "self_heal",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[self_heal/inbox] {e}")


def systemctl_is_active(service):
    try:
        out = subprocess.check_output(
            ["systemctl", "is-active", service],
            stderr=subprocess.STDOUT, timeout=5,
        ).decode().strip()
        return out == "active", out
    except subprocess.CalledProcessError as e:
        return False, e.output.decode(errors="replace").strip() if e.output else "failed"
    except Exception as e:
        return False, f"probe_error:{e}"


def systemctl_restart(service):
    try:
        subprocess.check_call(["systemctl", "restart", service], timeout=30)
        return True, "restart ok"
    except Exception as e:
        return False, f"restart_failed:{e}"


def check_service(name):
    active, detail = systemctl_is_active(name)
    if active:
        return "healthy", detail
    # Respect exchange_health pause: do not flag exchange-dependent services
    # as degraded while the exchange is intentionally paused.
    if name in EXCHANGE_PAUSED_SERVICES and os.path.exists(EXCHANGE_PAUSE_FLAG):
        return "healthy", f"paused_by_exchange_health:{detail}"
    return "degraded", detail


def check_freshness(target):
    path = target["path"]
    if not os.path.exists(path):
        return "degraded", f"missing:{path}"
    age_min = (time.time() - os.path.getmtime(path)) / 60
    if age_min > target["max_age_min"]:
        return "degraded", f"stale:{age_min:.0f}min>{target['max_age_min']}min"
    return "healthy", f"fresh:{age_min:.0f}min"


def evaluate_and_heal(entry, state):
    """entry is a dict with 'name' (+ 'path'/'heal_service' if freshness).
    Returns updated per-subsystem state dict."""
    subs = state["subsystems"]
    name = entry["name"]
    kind = entry["kind"]

    if kind == "service":
        status, detail = check_service(name)
    else:
        status, detail = check_freshness(entry)

    prev = subs.get(name, {})
    consec_degraded = prev.get("consec_degraded", 0)
    healed_at = prev.get("healed_at")  # ISO timestamp of last heal attempt
    cycles_since_heal = prev.get("cycles_since_heal", 0)
    prev_status = prev.get("status", "unknown")

    if status == "healthy":
        # Transition to healthy — log recovery, reset counters
        if prev_status != "healthy":
            log_jsonl({
                "ts": datetime.now(timezone.utc).isoformat(),
                "subsystem": name,
                "event": "recovered",
                "detail": detail,
                "prev_consec_degraded": consec_degraded,
            })
        new = {"status": "healthy", "detail": detail, "consec_degraded": 0,
               "healed_at": None, "cycles_since_heal": 0,
               "last_check": datetime.now(timezone.utc).isoformat()}
        subs[name] = new
        return f"{name}:ok"

    # status == "degraded"
    consec_degraded += 1

    # Has a heal been attempted recently?
    if healed_at:
        cycles_since_heal += 1

    # Decide action
    action = "none"
    if healed_at is None and consec_degraded >= HEAL_AFTER_CONSECUTIVE:
        # First heal attempt
        heal_svc = entry.get("heal_service") if kind == "freshness" else name
        if heal_svc:
            ok, hdetail = systemctl_restart(heal_svc)
            action = f"restart:{heal_svc}:{'ok' if ok else 'fail'}"
            log_jsonl({
                "ts": datetime.now(timezone.utc).isoformat(),
                "subsystem": name,
                "event": "heal_attempt",
                "action": action,
                "heal_detail": hdetail,
                "degraded_detail": detail,
                "consec_degraded": consec_degraded,
            })
            healed_at = datetime.now(timezone.utc).isoformat()
            cycles_since_heal = 0
        else:
            action = "no_heal_action_defined"
            log_jsonl({
                "ts": datetime.now(timezone.utc).isoformat(),
                "subsystem": name,
                "event": "degraded_no_heal",
                "detail": detail,
                "consec_degraded": consec_degraded,
            })
    elif healed_at and cycles_since_heal >= ESCALATE_AFTER_HEAL:
        # Heal didn't help — escalate
        action = "escalate"
        inbox_write(
            f"<b>SYN: self_heal unable to recover {name}</b>\n"
            f"Time: {pst_now()}\n"
            f"Degraded: {detail}\n"
            f"Heal attempted: {healed_at}\n"
            f"Cycles since heal (still degraded): {cycles_since_heal}\n"
            f"Action required: manual investigation.",
            severity="error",
        )
        log_jsonl({
            "ts": datetime.now(timezone.utc).isoformat(),
            "subsystem": name,
            "event": "escalated",
            "detail": detail,
            "healed_at": healed_at,
            "cycles_since_heal": cycles_since_heal,
        })
        # Reset heal cycle so we don't escalate every run — back off and retry
        healed_at = None
        cycles_since_heal = 0
        # Tier 2 retry budget exhausted -> hand off to Tier 3 immediately.
        # Tier 3 enforces its own 30-min/component cooldown and 24h daily cap,
        # so repeated handoffs from this code path are safe (cooldown-skipped).
        try:
            subprocess.Popen(
                ["python3", f"{WORKSPACE}/self_heal_tier3.py",
                 "--force", "cascade"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except Exception as _t3_err:
            log_jsonl({
                "ts": datetime.now(timezone.utc).isoformat(),
                "subsystem": name,
                "event": "tier3_handoff_failed",
                "error": str(_t3_err)[:200],
            })

    subs[name] = {
        "status": "degraded",
        "detail": detail,
        "consec_degraded": consec_degraded,
        "healed_at": healed_at,
        "cycles_since_heal": cycles_since_heal,
        "last_action": action,
        "last_check": datetime.now(timezone.utc).isoformat(),
    }
    return f"{name}:degraded({action})"


def main():
    state = load_state()
    summary = []

    # Services
    for svc in SERVICES:
        r = evaluate_and_heal({"kind": "service", "name": svc}, state)
        summary.append(r)

    # Freshness targets
    for tgt in FRESHNESS_TARGETS:
        entry = dict(tgt)
        entry["kind"] = "freshness"
        r = evaluate_and_heal(entry, state)
        summary.append(r)

    save_state(state)
    print(f"[{pst_now()}] " + " | ".join(summary))


if __name__ == "__main__":
    main()
