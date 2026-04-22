#!/usr/bin/env python3
"""meta_audit_freshness.py — stale-mtime SYN alert for the weekly meta_audit cron.

The weekly meta_audit fires Saturday 10:00 UTC. If the cron silently breaks
(service stopped, command crashes, crontab wiped), the sidecar stops being
written and nobody notices. This detector compares the mtime of
research/meta_audit/latest.json to a staleness threshold and writes a
severity=error row to syn_inbox so SYN dispatches to Telegram.

Dedup: once per calendar day. If still stale tomorrow, re-fires once.

Cron: 0 */6 * * *  (every 6 hours — four chances per day to catch it)

F3 from meta_audit review 2026-04-22.
"""
import json
import os
import time
from datetime import datetime, timezone

WORKSPACE       = "/root/.openclaw/workspace"
LATEST_SIDECAR  = os.path.join(WORKSPACE, "research", "meta_audit", "latest.json")
STATE_FILE      = os.path.join(WORKSPACE, "research", "meta_audit", "freshness_state.json")
SYN_INBOX       = os.path.join(WORKSPACE, "syn_inbox.jsonl")

# Weekly run + 1 full day slack. Cron fires Sat 10:00 UTC; we alert after
# 8 days of no sidecar write.
STALE_SECONDS   = 8 * 24 * 3600


def _load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_state(state):
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, STATE_FILE)


def _emit(summary, severity="error", extra=None):
    row = {
        "ts":       datetime.now(timezone.utc).isoformat(),
        "source":   "meta_audit_freshness",
        "severity": severity,
        "summary":  summary,
    }
    if extra:
        row.update(extra)
    with open(SYN_INBOX, "a") as f:
        f.write(json.dumps(row) + "\n")


def main():
    if not os.path.exists(LATEST_SIDECAR):
        # First-run grace: don't alert if meta_audit has never written a
        # sidecar. Once state tracks a prior mtime, absence becomes an alert.
        state = _load_state()
        if "last_seen_mtime" in state:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if state.get("last_alert_date") != today:
                _emit(
                    "meta_audit latest.json missing (was previously present) — sidecar deleted or cron broken",
                    severity="error",
                    extra={"last_seen_mtime": state.get("last_seen_mtime")},
                )
                state["last_alert_date"] = today
                _save_state(state)
        return

    mtime = os.path.getmtime(LATEST_SIDECAR)
    age_s = time.time() - mtime
    age_days = age_s / 86400

    state = _load_state()
    state["last_seen_mtime"] = datetime.fromtimestamp(mtime, timezone.utc).isoformat()

    if age_s > STALE_SECONDS:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if state.get("last_alert_date") != today:
            _emit(
                f"meta_audit stale: latest.json is {age_days:.1f} days old (threshold 8d); weekly cron may be broken",
                severity="error",
                extra={"sidecar_age_days": round(age_days, 2), "sidecar_mtime": state["last_seen_mtime"]},
            )
            state["last_alert_date"] = today
    else:
        # Fresh again — clear any stale alert tracker so a future stall re-fires.
        state.pop("last_alert_date", None)

    _save_state(state)


if __name__ == "__main__":
    main()
