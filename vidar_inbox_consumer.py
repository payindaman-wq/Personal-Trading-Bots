#!/usr/bin/env python3
"""
vidar_inbox_consumer.py — SYN self-heal loop closer (VIDAR dispatcher tier).

Runs every 5 min via cron. Polls syn_inbox.jsonl for signals from non-
allowlisted detection sources (gemini_health, odin_memory, cron_health,
tyr_freshness, crashloop, self_heal, syn_weekly_audit, syn_post_ship_review).

For each new signal, applies deterministic classification and routes:
  - CHRIS_ACTION → write to inbox with source=vidar severity=error
                   (vidar IS allowlisted, so sys_heartbeat will Telegram)
  - LOKI_ESCALATE → append to loki_pending_actions.jsonl with type=escalate
                    (LOKI's process_pending_actions picks it up next tick,
                    writes to loki_escalation_log.jsonl → dashboard work order)
  - DROP → log only (successful self-heal, transient noise, etc.)

No LLM calls. Deterministic rules only. VIDAR's Opus remains reserved for
genuine arbitration (revert review, oscillation, restructure) fired elsewhere.

This file closes the loop that the SYN P0/P1 monitors shipped 2026-04-19
opened: they now produce inbox signals that this consumer routes to the
right officer, so Chris is no longer paged on detection-layer events.
"""
import json
import os
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"
STATE_FILE = f"{WORKSPACE}/competition/vidar_inbox_consumer_state.json"
DECISIONS_LOG = f"{WORKSPACE}/research/vidar_inbox_decisions.jsonl"
LOKI_PENDING = f"{WORKSPACE}/research/loki_pending_actions.jsonl"

# Sources this consumer is responsible for — sources already routed elsewhere
# (e.g., sprint_integrity has its own pending-actions pipeline, loki/vidar
# write their own entries) are excluded.
WATCHED_SOURCES = {
    "gemini_health",
    "odin_memory",
    "cron_health",
    "tyr_freshness",
    "crashloop",
    "self_heal",              # self_heal_controller escalation after heal-failed
    "syn_weekly_audit",
    "syn_post_ship_review",
    "data_integrity",         # per-league write-path drift audit
    "mimir_audit",            # MIMIR citation fact-check
    "runtime_state_freshness", # tracked runtime JSON drift (deploy-reset class)
    "league_watchdog",       # dead execution / no MTM / stale tick — must reach LOKI work queue
}

# Patterns that indicate Chris himself must act (the officers cannot fix).
# Keyed by source. Each value is a list of (regex, reason) tuples.
CHRIS_ACTION_RULES = {
    "gemini_health": [
        (r"\b401\b|\b403\b|auth|authentication|invalid.*key|unauthorized",
         "Gemini API auth broken — rotate key in /root/.openclaw/secrets/gemini.json"),
    ],
    "odin_memory": [
        (r"restart FAILED",
         "ODIN service failed to restart after memory threshold — manual systemctl intervention needed"),
    ],
    "self_heal": [
        (r"unable to recover",
         "Self-heal controller exhausted auto-recovery — VIDAR deep-dive + Chris review recommended"),
    ],
    "crashloop": [
        # A second crash-loop alert on the same service within the cooldown
        # means the first restart didn't stop it. That's past officer reach.
        (r"crash-loop detected",
         "Systemd crash-loop persisting — service cannot stay up, investigate root cause"),
    ],
}

# Patterns that indicate successful self-heal — no action needed.
DROP_RULES = {
    "odin_memory": [
        r"restart OK",                          # watchdog restarted successfully
        r"watch for leak",                      # soft-warning, not yet hard
    ],
    "gemini_health": [
        # Transient 5xx will clear on next probe; don't bother LOKI.
        r"\b500\b|\b502\b|\b503\b|\b504\b",
    ],
    "syn_post_ship_review": [
        r"Verdict: STABLE",                     # healthy report, no routing needed
    ],
    "syn_weekly_audit": [
        # syn_weekly_audit only emits when anomalies found — every entry is
        # real. Nothing to drop by default.
    ],
    "data_integrity": [
        r"RECOVERED",                          # write-path cleared
    ],
    "mimir_audit": [
        # Only fires when findings exist — nothing to drop by default.
    ],
    "runtime_state_freshness": [
        r"RECOVERED",                          # freshness returned without auto-heal
        r"self-healed",                        # auto-heal regenerated the file
    ],
    "league_watchdog": [
        r"RECOVERED",                          # future: watchdog recovery notice (none today)
    ],
}


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"last_offset": 0}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, indent=2)
    os.replace(tmp, STATE_FILE)


def log_decision(rec):
    try:
        os.makedirs(os.path.dirname(DECISIONS_LOG), exist_ok=True)
        with open(DECISIONS_LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[vidar_inbox/log] {e}")


def classify(entry):
    """Return (verdict, reason). verdict in {CHRIS_ACTION, LOKI_ESCALATE, DROP}."""
    src = entry.get("source", "")
    msg = entry.get("msg", "")

    # 1. Chris-action patterns take precedence.
    for pattern, reason in CHRIS_ACTION_RULES.get(src, []):
        if re.search(pattern, msg, re.IGNORECASE):
            return "HUMAN_ACTION", reason

    # 2. Drop patterns — informational / already-resolved.
    for pattern in DROP_RULES.get(src, []):
        if re.search(pattern, msg, re.IGNORECASE):
            return "DROP", f"matched drop rule: {pattern}"

    # 3. Everything else → LOKI escalation (dashboard work order).
    return "LOKI_ESCALATE", "default route — LOKI escalation"


def route_chris_action(original, reason):
    """Write allowlisted vidar-source entry so sys_heartbeat Telegrams."""
    payload = (
        f"<b>SYN/VIDAR: manual action required</b>\n"
        f"Time: {pst_now()}\n"
        f"Source: {original.get('source')}\n"
        f"Signal: {str(original.get('msg', ''))[:300]}\n"
        f"Reason: {reason}"
    )
    rec = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "source":   "vidar",   # allowlisted
        "severity": "error",
        "msg":      payload[:2000],
    }
    with open(INBOX, "a") as f:
        f.write(json.dumps(rec) + "\n")


def route_loki_escalate(original, reason):
    """Append to loki_pending_actions.jsonl. LOKI picks it up next tick."""
    src = original.get("source", "?")
    orig_msg = str(original.get("msg", ""))[:500]
    description = f"[{src}] {orig_msg}"
    entry = {
        "ts":     datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "source": "vidar_inbox_consumer",
        "league": "multi",
        "actions": [{"type": "escalate", "description": description[:600]}],
        "processed": False,
    }
    os.makedirs(os.path.dirname(LOKI_PENDING), exist_ok=True)
    with open(LOKI_PENDING, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    state = load_state()
    offset = state.get("last_offset", 0)

    if not os.path.exists(INBOX):
        print(f"[{pst_now()}] inbox not found")
        return

    with open(INBOX) as f:
        lines = f.readlines()

    new_lines = lines[offset:]
    if not new_lines:
        print(f"[{pst_now()}] no new inbox entries (offset={offset}, total={len(lines)})")
        return

    counts = {"HUMAN_ACTION": 0, "LOKI_ESCALATE": 0, "DROP": 0, "IGNORED": 0}

    for line in new_lines:
        line = line.strip()
        if not line:
            counts["IGNORED"] += 1
            continue
        try:
            entry = json.loads(line)
        except Exception:
            counts["IGNORED"] += 1
            continue

        src = entry.get("source", "")
        if src not in WATCHED_SOURCES:
            counts["IGNORED"] += 1
            continue

        verdict, reason = classify(entry)
        counts[verdict] += 1

        if verdict == "HUMAN_ACTION":
            route_chris_action(entry, reason)
        elif verdict == "LOKI_ESCALATE":
            route_loki_escalate(entry, reason)

        log_decision({
            "ts":       datetime.now(timezone.utc).isoformat(),
            "verdict":  verdict,
            "reason":   reason,
            "original": entry,
        })

    state["last_offset"] = len(lines)
    save_state(state)
    print(f"[{pst_now()}] processed {len(new_lines)} lines | "
          f"human={counts['HUMAN_ACTION']} loki={counts['LOKI_ESCALATE']} "
          f"drop={counts['DROP']} ignored={counts['IGNORED']}")


if __name__ == "__main__":
    main()
