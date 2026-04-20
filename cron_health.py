#!/usr/bin/env python3
"""
cron_health.py — detect Python tracebacks in cron-driven officer logs (SYN/cron_health).

Runs hourly via cron. For each watched log:
  - Tail last 300 lines.
  - Find Python tracebacks ("Traceback (most recent call last):").
  - Capture the exception signature (last non-blank line of the traceback).
  - Dedup against state — alert once per unique signature per 24h.
Silent failures — LOKI/TYR/HEIMDALL/MIMIR/ODIN python exceptions — become visible.
"""
import json, os, re, subprocess
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/cron_health_state.json"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"

TAIL_LINES = 300
COOLDOWN_MIN = 1440  # 24h per-signature dedup

WATCHED_LOGS = [
    f"{WORKSPACE}/research/loki.log",
    f"{WORKSPACE}/research/tyr.log",
    f"{WORKSPACE}/research/heimdall.log",
    f"{WORKSPACE}/research/day/researcher.log",
    f"{WORKSPACE}/research/swing/researcher.log",
    f"{WORKSPACE}/research/futures_day/researcher.log",
    f"{WORKSPACE}/research/futures_swing/researcher.log",
    f"{WORKSPACE}/research/pm/researcher.log",
    f"{WORKSPACE}/competition/watchdog.log",
    f"{WORKSPACE}/competition/exchange_health.log",
    f"{WORKSPACE}/competition/anthropic_health.log",
    f"{WORKSPACE}/competition/gemini_health.log",
    f"{WORKSPACE}/competition/odin_memory.log",
    f"{WORKSPACE}/competition/research_freshness.log",
    f"{WORKSPACE}/competition/heartbeat.log",
    f"{WORKSPACE}/competition/killswitch.log",
]

TRACEBACK_START = "Traceback (most recent call last):"


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"alerted": {}}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)


def should_alert(state, key):
    last = state["alerted"].get(key)
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return True
    return datetime.now(timezone.utc) - last_dt > timedelta(minutes=COOLDOWN_MIN)


def mark_alerted(state, key):
    state["alerted"][key] = datetime.now(timezone.utc).isoformat()


def inbox_write(msg, severity="error"):
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "cron_health",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[cron_health/inbox] {e}")


def tail_lines(path, n):
    try:
        out = subprocess.check_output(["tail", f"-n{n}", path], timeout=10).decode(errors="replace")
        return out.splitlines()
    except Exception:
        return []


def extract_tracebacks(lines):
    """Return list of (signature, full_traceback_text). Signature is the exception
    line (e.g. 'KeyError: foo') used for dedup."""
    tracebacks = []
    i = 0
    while i < len(lines):
        if TRACEBACK_START in lines[i]:
            start = i
            i += 1
            # Exception line is the last non-blank line before dedent or next TB.
            last_exc = None
            while i < len(lines):
                if TRACEBACK_START in lines[i]:
                    break
                line = lines[i]
                # exception lines match "SomeError: msg" — no leading whitespace,
                # and contain a colon.
                if line and not line.startswith((" ", "\t")) and ":" in line:
                    m = re.match(r"([A-Za-z_][A-Za-z_0-9.]*(?:Error|Exception|Warning|Interrupt|Timeout)):", line)
                    if m:
                        last_exc = line.strip()
                i += 1
            if last_exc:
                sig = last_exc[:200]
                tracebacks.append((sig, "\n".join(lines[start:i])[:1500]))
        else:
            i += 1
    return tracebacks


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def main():
    state = load_state()
    total_found = 0
    total_alerted = 0

    for log in WATCHED_LOGS:
        if not os.path.exists(log):
            continue
        lines = tail_lines(log, TAIL_LINES)
        if not lines:
            continue
        tbs = extract_tracebacks(lines)
        for sig, tb_text in tbs:
            total_found += 1
            log_basename = os.path.basename(log)
            dedup_key = f"{log_basename}::{sig}"
            if should_alert(state, dedup_key):
                tb_snippet = tb_text[-800:]  # last 800 chars of traceback
                inbox_write(
                    f"<b>SYN: traceback in {log_basename}</b>\n"
                    f"Time: {pst_now()}\n"
                    f"Log: {log}\n"
                    f"Signature: {sig}\n"
                    f"Tail:\n<pre>{tb_snippet}</pre>",
                    severity="error",
                )
                mark_alerted(state, dedup_key)
                total_alerted += 1

    save_state(state)
    print(f"[{pst_now()}] scanned={len(WATCHED_LOGS)} logs, tracebacks_found={total_found}, newly_alerted={total_alerted}")


if __name__ == "__main__":
    main()
