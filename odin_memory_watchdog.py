#!/usr/bin/env python3
"""
odin_memory_watchdog.py — detect ODIN memory leak, auto-restart (SYN/odin_memory).

Runs every 5 min via cron. For each of the 4 ODIN services:
  - Look up MainPID via systemctl
  - Read RSS from /proc/<pid>/status
  - If RSS > HARD_THRESHOLD_GB, systemctl restart and alert
  - If RSS > SOFT_THRESHOLD_GB, log to inbox as warning (no restart)
Per-service cooldown prevents restart loops.

Observed baseline 2026-04-19: day=1.81GB, futures_day=1.59GB,
swing=0.16GB, futures_swing=0.16GB. Threshold set with ~65% headroom
on the largest; adjust after 2 weeks of data.
"""
import json, os, subprocess
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/odin_memory_state.json"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"

SERVICES = ["odin_day", "odin_swing", "odin_futures_swing"]  # PAUSED odin_futures_day 2026-04-25 meta_audit F2

SOFT_THRESHOLD_GB = 2.5
HARD_THRESHOLD_GB = 3.0
RESTART_COOLDOWN_MIN = 60   # don't thrash-restart the same service
WARN_COOLDOWN_MIN = 360


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"last_restarted": {}, "last_warned": {}}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)


def cooldown_elapsed(state_dict, key, minutes):
    last = state_dict.get(key)
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return True
    return datetime.now(timezone.utc) - last_dt > timedelta(minutes=minutes)


def mark_now(state_dict, key):
    state_dict[key] = datetime.now(timezone.utc).isoformat()


def inbox_write(msg, severity="error"):
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "odin_memory",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[odin_memory/inbox] {e}")


def service_main_pid(service):
    try:
        out = subprocess.check_output(
            ["systemctl", "show", "--property=MainPID", service],
            timeout=5,
        ).decode().strip()
        pid = int(out.split("=", 1)[1])
        return pid if pid > 0 else None
    except Exception:
        return None


def pid_rss_gb(pid):
    try:
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    kb = int(line.split()[1])
                    return kb / 1024 / 1024
    except Exception:
        return None
    return None


def restart_service(service):
    try:
        subprocess.check_call(
            ["systemctl", "restart", service],
            timeout=30,
        )
        return True
    except Exception as e:
        print(f"[odin_memory] restart {service} failed: {e}")
        return False


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def main():
    state = load_state()
    summary = []

    for svc in SERVICES:
        pid = service_main_pid(svc)
        if pid is None:
            inbox_write(
                f"<b>SYN: {svc} has no MainPID (service down?)</b>\n"
                f"Time: {pst_now()}",
                severity="error",
            )
            summary.append(f"{svc}: PID_MISSING")
            continue

        rss_gb = pid_rss_gb(pid)
        if rss_gb is None:
            summary.append(f"{svc}: RSS_UNREADABLE(pid={pid})")
            continue

        if rss_gb > HARD_THRESHOLD_GB:
            if cooldown_elapsed(state["last_restarted"], svc, RESTART_COOLDOWN_MIN):
                ok = restart_service(svc)
                mark_now(state["last_restarted"], svc)
                inbox_write(
                    f"<b>SYN: {svc} memory {rss_gb:.2f}GB > {HARD_THRESHOLD_GB}GB — restart {'OK' if ok else 'FAILED'}</b>\n"
                    f"Time: {pst_now()}\n"
                    f"PID was: {pid}\n"
                    f"Thresholds: soft {SOFT_THRESHOLD_GB}GB / hard {HARD_THRESHOLD_GB}GB\n"
                    f"Action: systemctl restart {svc}",
                    severity="error",
                )
                summary.append(f"{svc}: RESTART@{rss_gb:.2f}GB ({'ok' if ok else 'fail'})")
            else:
                summary.append(f"{svc}: over_threshold_but_in_cooldown@{rss_gb:.2f}GB")
        elif rss_gb > SOFT_THRESHOLD_GB:
            if cooldown_elapsed(state["last_warned"], svc, WARN_COOLDOWN_MIN):
                inbox_write(
                    f"<b>SYN: {svc} memory {rss_gb:.2f}GB > soft {SOFT_THRESHOLD_GB}GB (watch for leak)</b>\n"
                    f"Time: {pst_now()}\n"
                    f"Hard threshold: {HARD_THRESHOLD_GB}GB\n"
                    f"No action taken.",
                    severity="warning",
                )
                mark_now(state["last_warned"], svc)
            summary.append(f"{svc}: warn@{rss_gb:.2f}GB")
        else:
            summary.append(f"{svc}: ok@{rss_gb:.2f}GB")

    save_state(state)
    print(f"[{pst_now()}] " + " | ".join(summary))


if __name__ == "__main__":
    main()
