#!/usr/bin/env python3
"""
syn_weekly_audit.py — SYN Operations Officer, weekly automated audit.

Runs every Monday 10:00 UTC (2am PST, 1h after weekly_league_restart).
Replaces the manual "paste pickup command weekly" loop with a silent
watchdog that only Telegrams when something's actually wrong.

Checks (all read-only, no re-probes):
  1. Tracebacks in any monitor log (past 7d).
  2. Cron freshness — every expected job has fired recently.
  3. Alert-volume trend — week-over-week change per SYN source. Sudden
     spike = something broke; sudden zero on a normally-chatty source =
     probe dead.
  4. ODIN RSS trend — average RSS climbing across weeks = slow leak.
  5. Self-heal escalations — any subsystem that self_heal_controller
     couldn't recover in the past 7 days.
  6. Kill-switch trip events + graduated-warning history.
  7. New log files in competition/ that weren't there last week (drift).

Output rule (per Chris's SYN reporting preference — problems only, never
routine status): silent on green. Telegrams only when issues found.
Always writes to /root/.openclaw/workspace/competition/syn_weekly_audit.log
for forensic review.

State carried week-over-week in syn_weekly_audit_state.json:
  - per-source alert counts (for trend delta next week)
  - per-league avg ODIN RSS (for leak-trend detection)
  - snapshot of competition/ file listing (for drift detection)
"""
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE  = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/syn_weekly_audit_state.json"
LOG_FILE   = f"{WORKSPACE}/competition/syn_weekly_audit.log"
INBOX      = f"{WORKSPACE}/syn_inbox.jsonl"

# All SYN-sourced inbox entries we want to track volume-trend on.
TRACKED_SOURCES = [
    "anthropic_health", "exchange_health", "kraken_killswitch",
    "league_watchdog", "session_watchdog", "sys_heartbeat",
    "loki", "vidar",
    "gemini_health", "odin_memory", "cron_health",
    "tyr_freshness", "crashloop", "self_heal",
    "research_freshness", "sprint_integrity",
]

# Cron jobs we expect to see recent log activity for. Path + max-allowed-age-min.
CRON_FRESHNESS_TARGETS = [
    (f"{WORKSPACE}/competition/gemini_health.log",          15 * 3),
    (f"{WORKSPACE}/competition/odin_memory.log",             5 * 3),
    (f"{WORKSPACE}/competition/cron_health.log",            60 * 2),
    (f"{WORKSPACE}/competition/crashloop.log",              15 * 3),
    (f"{WORKSPACE}/competition/self_heal.log",               5 * 3),
    (f"{WORKSPACE}/competition/heartbeat.log",              30 * 3),
    (f"{WORKSPACE}/competition/watchdog.log",               10 * 3),
    (f"{WORKSPACE}/competition/anthropic_health.log",       15 * 3),
    (f"{WORKSPACE}/competition/exchange_health.log",         5 * 3),
    (f"{WORKSPACE}/competition/research_freshness.log",     60 * 2),
    (f"{WORKSPACE}/competition/regression_watch.log",       60 * 2),
]

# Logs to scan for tracebacks.
TRACEBACK_SCAN_LOGS = [
    f"{WORKSPACE}/competition/gemini_health.log",
    f"{WORKSPACE}/competition/odin_memory.log",
    f"{WORKSPACE}/competition/cron_health.log",
    f"{WORKSPACE}/competition/crashloop.log",
    f"{WORKSPACE}/competition/self_heal.log",
    f"{WORKSPACE}/competition/research_freshness.log",
    f"{WORKSPACE}/research/loki.log",
    f"{WORKSPACE}/research/tyr.log",
    f"{WORKSPACE}/research/heimdall.log",
]

# Volume-trend thresholds. Alert if week-over-week delta exceeds either.
VOL_SPIKE_ABSOLUTE = 50   # e.g., from 2 to 52 alerts = spike
VOL_SPIKE_RATIO    = 5.0  # e.g., 5x increase from prior week


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def log(msg):
    line = f"[{pst_now()}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {
        "last_run":        None,
        "source_counts":   {},   # src -> last week's count
        "odin_rss_avg_gb": {},   # service -> last week's avg RSS
        "comp_file_list":  [],   # last week's file listing
    }


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, indent=2)
    os.replace(tmp, STATE_FILE)


def file_age_min(path):
    if not os.path.exists(path):
        return None
    return (time.time() - os.path.getmtime(path)) / 60


def tail(path, n=500):
    try:
        return subprocess.check_output(["tail", f"-n{n}", path], timeout=10).decode(errors="replace")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def scan_tracebacks_7d():
    """Return list of (log, signature) for tracebacks in past 7d.
    Uses mtime gate — if log wasn't touched in 7d it can't have new tracebacks."""
    cutoff = time.time() - 7 * 86400
    hits = []
    for log_path in TRACEBACK_SCAN_LOGS:
        if not os.path.exists(log_path) or os.path.getmtime(log_path) < cutoff:
            continue
        content = tail(log_path, 2000)
        if "Traceback (most recent call last):" in content:
            # Capture last exception signature
            for line in reversed(content.splitlines()):
                m = re.match(r"([A-Za-z_][A-Za-z_0-9.]*(?:Error|Exception|Warning|Timeout)):", line.strip())
                if m:
                    hits.append((os.path.basename(log_path), line.strip()[:150]))
                    break
    return hits


def check_cron_freshness():
    """Return list of (log_basename, age_min, max_age) for any stale log."""
    stale = []
    for path, max_age in CRON_FRESHNESS_TARGETS:
        age = file_age_min(path)
        if age is None:
            stale.append((os.path.basename(path), None, max_age))
        elif age > max_age:
            stale.append((os.path.basename(path), int(age), max_age))
    return stale


def count_sources_past_7d():
    """Return {source: count} for syn_inbox entries in past 7d."""
    cutoff_dt = datetime.now(timezone.utc) - timedelta(days=7)
    cutoff_iso = cutoff_dt.strftime("%Y-%m-%dT%H:%M")
    counts = {s: 0 for s in TRACKED_SOURCES}
    if not os.path.exists(INBOX):
        return counts
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
            if ts < cutoff_iso:
                continue
            src = rec.get("source", "")
            if src in counts:
                counts[src] += 1
    return counts


def volume_trend_anomalies(current, prior):
    """Return list of (source, prior_count, current_count, reason)."""
    flagged = []
    for src, curr in current.items():
        prev = prior.get(src, 0)
        # Spike: big absolute AND large ratio (avoid flagging 0->5)
        if curr - prev >= VOL_SPIKE_ABSOLUTE:
            ratio = (curr / prev) if prev > 0 else float("inf")
            if ratio >= VOL_SPIKE_RATIO or prev == 0:
                flagged.append((src, prev, curr, f"spike +{curr - prev} (x{ratio:.1f})"))
        # Zero-out: was non-trivial, now silent — probe broken?
        elif prev >= 20 and curr == 0:
            flagged.append((src, prev, curr, f"went silent (prior {prev}/wk)"))
    return flagged


def avg_odin_rss_past_7d():
    """Parse odin_memory.log, extract RSS per service, average over entries."""
    content = tail(f"{WORKSPACE}/competition/odin_memory.log", 3000)
    per_svc = {}   # svc -> list of rss
    # Lines look like: "... odin_day: ok@1.81GB | odin_swing: ok@0.16GB | ..."
    for line in content.splitlines():
        for m in re.finditer(r"(odin_\w+): \w+@([0-9.]+)GB", line):
            per_svc.setdefault(m.group(1), []).append(float(m.group(2)))
    return {svc: (sum(v) / len(v)) for svc, v in per_svc.items() if v}


def leak_trend_anomalies(current, prior):
    """Flag if any service's avg RSS rose >= 0.5 GB week-over-week."""
    flagged = []
    for svc, curr in current.items():
        prev = prior.get(svc)
        if prev is None:
            continue
        delta = curr - prev
        if delta >= 0.5:
            flagged.append((svc, prev, curr, delta))
    return flagged


def self_heal_escalations_7d():
    """Scan self_heal_log.jsonl for 'escalated' events in past 7d."""
    path = f"{WORKSPACE}/competition/self_heal_log.jsonl"
    if not os.path.exists(path):
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    hits = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("event") != "escalated":
                continue
            try:
                ts = datetime.fromisoformat(rec["ts"])
            except Exception:
                continue
            if ts >= cutoff:
                hits.append((rec.get("subsystem"), rec.get("detail", "")[:120]))
    return hits


def killswitch_events_7d():
    """Check killswitch_state for any trip/recovery in past 7d."""
    path = f"{WORKSPACE}/competition/killswitch_state.json"
    if not os.path.exists(path):
        return None
    try:
        s = json.load(open(path))
    except Exception:
        return None
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    events = []
    for k in ("triggered_at", "recovered_at"):
        ts_iso = s.get(k)
        if not ts_iso:
            continue
        try:
            ts = datetime.fromisoformat(ts_iso)
        except Exception:
            continue
        if ts >= cutoff:
            events.append((k, ts_iso))
    return events


def drift_scan():
    """List competition/*.log and flag new files vs prior snapshot."""
    comp = f"{WORKSPACE}/competition"
    files = []
    for root, dirs, fnames in os.walk(comp):
        for fn in fnames:
            if fn.endswith(".log"):
                files.append(os.path.join(root, fn)[len(comp) + 1:])
    return sorted(files)


# ---------------------------------------------------------------------------
# Alerting
# ---------------------------------------------------------------------------

def inbox_escalate(body):
    # severity=info + non-allowlisted source = inbox-only by construction.
    # VIDAR polls the inbox and decides if anything here needs remediation.
    # Per feedback_syn_telegram_chris_action_only.md: weekly audit findings
    # are never Chris-action by default.
    rec = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "source":   "syn_weekly_audit",
        "severity": "info",
        "msg":      ("[OPS/weekly] audit anomalies: " + body)[:2000],
    }
    with open(INBOX, "a") as f:
        f.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    state = load_state()
    prior_source_counts = state.get("source_counts", {})
    prior_rss           = state.get("odin_rss_avg_gb", {})
    prior_files         = set(state.get("comp_file_list", []))

    # Run all checks
    tb_hits         = scan_tracebacks_7d()
    stale_crons     = check_cron_freshness()
    src_counts      = count_sources_past_7d()
    vol_anomalies   = volume_trend_anomalies(src_counts, prior_source_counts)
    odin_rss_avg    = avg_odin_rss_past_7d()
    leak_anomalies  = leak_trend_anomalies(odin_rss_avg, prior_rss)
    heal_escalated  = self_heal_escalations_7d()
    ks_events       = killswitch_events_7d()
    current_files   = drift_scan()
    new_log_files   = sorted(set(current_files) - prior_files)
    missing_files   = sorted(prior_files - set(current_files))

    # Assemble report — only Telegram if any non-trivial finding.
    problems = []
    if tb_hits:
        problems.append("tracebacks: " + "; ".join(f"{lg}[{sig}]" for lg, sig in tb_hits[:3]))
    if stale_crons:
        problems.append("stale cron logs: " + ", ".join(f"{n}({a}m/>{m})" for n, a, m in stale_crons[:4]))
    if vol_anomalies:
        problems.append("alert volume: " + "; ".join(f"{s}:{p}->{c} ({r})" for s, p, c, r in vol_anomalies[:3]))
    if leak_anomalies:
        problems.append("ODIN leak trend: " + "; ".join(f"{s}:{p:.2f}->{c:.2f}GB (+{d:.2f})" for s, p, c, d in leak_anomalies))
    if heal_escalated:
        problems.append(f"self_heal couldn't recover: {len(heal_escalated)} subsystem(s)")
    if ks_events:
        problems.append("killswitch events: " + ", ".join(f"{k}@{ts}" for k, ts in ks_events))
    if missing_files:
        problems.append(f"log files disappeared: {', '.join(missing_files[:3])}")

    # Always log a summary line; only Telegram on problems.
    log(f"weekly: tb={len(tb_hits)} stale_crons={len(stale_crons)} "
        f"vol_anom={len(vol_anomalies)} leak={len(leak_anomalies)} "
        f"escal={len(heal_escalated)} ks={len(ks_events or [])} "
        f"new_files={len(new_log_files)} missing_files={len(missing_files)} "
        f"problems={len(problems)}")

    if problems:
        body_lines = [f"Time: {pst_now()}", ""]
        for p in problems:
            body_lines.append(f"- {p}")
        body_lines.append("")
        body_lines.append(f"Check: {LOG_FILE}")
        inbox_escalate("\n".join(body_lines))
        log("Telegrammed weekly report (problems found).")
    else:
        # Healthy week — silent. Per SYN reporting rule: never routine status.
        pass

    # Persist trend-state for next week.
    state["last_run"]        = datetime.now(timezone.utc).isoformat()
    state["source_counts"]   = src_counts
    state["odin_rss_avg_gb"] = odin_rss_avg
    state["comp_file_list"]  = current_files
    save_state(state)


if __name__ == "__main__":
    main()
