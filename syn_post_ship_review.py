#!/usr/bin/env python3
"""
syn_post_ship_review.py — one-shot post-audit stability check.

Fired 2026-04-20 10:00 UTC via `at` (scheduled from the 2026-04-19 audit
session). Scans the 5 new SYN monitors shipped 2026-04-19 for false
positives, noise, or silent failure, and posts a verdict to syn_inbox.jsonl
so sys_heartbeat Telegrams it to Chris.
"""
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"

# Ship time — only consider syn_inbox entries after this
SHIP_TS_ISO = "2026-04-19T21:00"

NEW_SOURCES = {
    "gemini_health",
    "odin_memory",
    "cron_health",
    "crashloop",
    "self_heal",
    "tyr_freshness",
}

LOG_FILES = [
    f"{WORKSPACE}/competition/gemini_health.log",
    f"{WORKSPACE}/competition/odin_memory.log",
    f"{WORKSPACE}/competition/cron_health.log",
    f"{WORKSPACE}/competition/crashloop.log",
    f"{WORKSPACE}/competition/self_heal.log",
]

CRON_ENTRIES_EXPECTED = [
    "gemini_health.py",
    "odin_memory_watchdog.py",
    "cron_health.py",
    "service_crashloop_watch.py",
    "self_heal_controller.py",
]


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def file_mtime_iso(path):
    if not os.path.exists(path):
        return None
    return datetime.fromtimestamp(os.path.getmtime(path), timezone.utc).isoformat()


def file_age_min(path):
    if not os.path.exists(path):
        return None
    return (time.time() - os.path.getmtime(path)) / 60


def tail(path, n=400):
    try:
        return subprocess.check_output(["tail", f"-n{n}", path], timeout=10).decode(errors="replace")
    except Exception:
        return ""


def scan_new_source_alerts():
    """Return per-source count of alerts since SHIP_TS_ISO."""
    counts = {src: 0 for src in NEW_SOURCES}
    samples = {src: [] for src in NEW_SOURCES}
    if not os.path.exists(INBOX):
        return counts, samples
    with open(INBOX) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            ts = rec.get("ts", "")
            src = rec.get("source", "")
            if src not in NEW_SOURCES:
                continue
            if ts < SHIP_TS_ISO:
                continue
            counts[src] += 1
            if len(samples[src]) < 3:
                samples[src].append((ts, rec.get("severity", "?"), rec.get("msg", "")[:120]))
    return counts, samples


def crontab_lines():
    try:
        return subprocess.check_output(["crontab", "-l"], timeout=5).decode()
    except Exception:
        return ""


def check_cron_freshness():
    """For each expected cron job, check its log mtime. Flag if log hasn't been
    written to in >2x its expected cadence."""
    cron_text = crontab_lines()
    results = []
    expectations = {
        "gemini_health.py":             (15, f"{WORKSPACE}/competition/gemini_health.log"),
        "odin_memory_watchdog.py":      (5,  f"{WORKSPACE}/competition/odin_memory.log"),
        "cron_health.py":               (60, f"{WORKSPACE}/competition/cron_health.log"),
        "service_crashloop_watch.py":   (15, f"{WORKSPACE}/competition/crashloop.log"),
        "self_heal_controller.py":      (5,  f"{WORKSPACE}/competition/self_heal.log"),
    }
    for script, (cadence_min, log_path) in expectations.items():
        in_cron = script in cron_text
        age = file_age_min(log_path)
        stale = age is None or age > cadence_min * 2
        results.append({
            "script": script,
            "in_cron": in_cron,
            "log_age_min": age,
            "expected_cadence_min": cadence_min,
            "stale": stale,
        })
    return results


def odin_rss_summary():
    """Peek at latest odin_memory.log line for RSS per league."""
    content = tail(f"{WORKSPACE}/competition/odin_memory.log", 5)
    return content.strip().splitlines()[-1] if content.strip() else "(no data)"


def self_heal_summary():
    """Count 'ok' vs non-ok subsystems across last hour of self_heal.log."""
    content = tail(f"{WORKSPACE}/competition/self_heal.log", 30)
    if not content:
        return "(no data)", 0, 0
    # Each line ends like: "a:ok | b:ok | c:degraded(...)"
    lines = [ln for ln in content.splitlines() if "|" in ln]
    if not lines:
        return "(no data)", 0, 0
    last = lines[-1]
    ok_count = last.count(":ok")
    degraded_count = last.count(":degraded")
    return last[last.index("]") + 1:].strip() if "]" in last else last, ok_count, degraded_count


def traceback_scan():
    """Any Python tracebacks in the new monitor logs themselves?"""
    hits = []
    for log in LOG_FILES:
        content = tail(log, 300)
        if "Traceback (most recent call last):" in content:
            hits.append(os.path.basename(log))
    return hits


def write_memory_success():
    """If all clean, leave a breadcrumb on disk for the next Claude session."""
    path = f"{WORKSPACE}/syn_post_ship_verdict.json"
    with open(path, "w") as f:
        json.dump({
            "verdict": "stable",
            "fired_at": datetime.now(timezone.utc).isoformat(),
            "note": "SYN P0/P1/Tier 2 layer shipped 2026-04-19 — stable after 24h bake.",
        }, f, indent=2)


def post_to_inbox(verdict, body_lines, severity):
    # Per feedback_syn_telegram_chris_action_only.md: post-ship review is
    # diagnostic, not Chris-action. source is non-allowlisted so even if
    # severity accidentally escalates, sys_heartbeat won't Telegram.
    rec = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "source":   "syn_post_ship_review",  # NOT allowlisted — inbox only by design
        "severity": "info",
        "msg":      ("[OPS/post-ship] 24h bake review\n"
                     f"Verdict: {verdict}\n" + "\n".join(body_lines))[:2000],
    }
    with open(INBOX, "a") as f:
        f.write(json.dumps(rec) + "\n")


def main():
    counts, samples = scan_new_source_alerts()
    cron_status = check_cron_freshness()
    odin_rss = odin_rss_summary()
    sh_line, sh_ok, sh_degraded = self_heal_summary()
    tb_hits = traceback_scan()

    stale_crons = [c for c in cron_status if c["stale"]]
    missing_crons = [c for c in cron_status if not c["in_cron"]]
    total_alerts = sum(counts.values())

    body = []
    body.append(f"Time: {pst_now()}")
    body.append("")
    body.append(f"Alerts from new sources since ship ({SHIP_TS_ISO}Z):")
    for src, n in sorted(counts.items()):
        body.append(f"  {src}: {n}")
        if n and samples[src]:
            body.append(f"    sample: {samples[src][0][2]}")
    body.append("")
    body.append(f"Cron health:")
    body.append(f"  in_cron: {sum(1 for c in cron_status if c['in_cron'])}/{len(cron_status)}")
    body.append(f"  stale logs: {len(stale_crons)}")
    if stale_crons:
        for c in stale_crons:
            body.append(f"    - {c['script']} (age {c['log_age_min']} min, expected <{c['expected_cadence_min']*2})")
    body.append("")
    body.append(f"ODIN RSS latest: {odin_rss[:200]}")
    body.append(f"Self-heal latest: {sh_ok} ok / {sh_degraded} degraded")
    if tb_hits:
        body.append(f"*** Tracebacks in new monitor logs: {', '.join(tb_hits)}")

    # Verdict logic. Severity is informational only — VIDAR reads the inbox
    # and decides whether any finding needs remediation or Chris-escalation.
    critical = bool(tb_hits) or bool(missing_crons) or sh_degraded > 0
    needs_tuning = total_alerts > 20 or len(stale_crons) > 0
    if critical:
        verdict = "NEEDS ROLLBACK"
    elif needs_tuning:
        verdict = "NEEDS TUNING"
    else:
        verdict = "STABLE"
        write_memory_success()
    severity = "info"

    body.append("")
    body.append("Next: MIMIR output audit + data-source integrity drift (Tier 3 candidates).")

    post_to_inbox(verdict, body, severity)
    print(f"[{pst_now()}] verdict={verdict} alerts={total_alerts} stale_crons={len(stale_crons)} tbs={len(tb_hits)}")


if __name__ == "__main__":
    main()
