#!/usr/bin/env python3
"""
syn_audit.py — Weekly deterministic infrastructure audit (SYN-tier, no LLM).

Runs Sunday 11:00 UTC via cron. Flags:
  - Cron drift:       entries added/removed vs EXPECTED_CRON manifest.
  - Service coverage: custom systemd units should exist + be active.
  - Stale state:      state files older than per-file thresholds.
  - Orphan scripts:   .py in workspace with no cron/systemd reference.
  - Backup rot:       .bak / .bak.* files older than 30 days.
  - Killswitch health: daemon ran recently, no stale flag.

Alerts via Telegram only when drift is detected (actionable — per user rule).
Log-only when nominal.

When adding new cron/services, update EXPECTED_CRON / EXPECTED_SERVICES below
so this audit doesn't false-alarm.
"""
import glob
import json
import os
import re
import subprocess
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
LOG_FILE  = f"{WORKSPACE}/competition/syn_audit.log"
BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID   = "8154505910"

# Substrings that uniquely identify each expected cron entry (command portion).
EXPECTED_CRON = [
    "competition_tick.py",
    "leaderboard.py --json",
    "swing_price_store.py",
    "swing_competition_tick.py",
    "swing_leaderboard.py --json",
    "dashboard_data.py",
    "session_watchdog.py",
    "weekly_sprint_cron.sh",
    "league_watchdog.py",
    "day_daily_restart.py",
    "sys_heartbeat.py",
    "polymarket_leaderboard.py --json",
    "research/prepare.py",
    "research/pm_collector.py",
    "research/loki.py",
    "weekly_league_restart.py",
    "research/tyr.py",
    "research/heimdall.py",
    "futures_day_competition_tick.py",
    "futures_day_restart.py",
    "futures_swing_competition_tick.py",
    "futures_day_leaderboard.py",
    "futures_swing_leaderboard.py",
    "polymarket_data.py",
    "exchange_health.py",
    "anthropic_health.py",
    "regression_watch.py",
    "research_freshness.py",
    "kraken_killswitch.py",
    "syn_audit.py",
    "self_heal_readiness.py",
    "dashboard/index.html",  # the -nt sync entry
    "openclaw@latest",
    "loki_log.jsonl",        # log trimmer
    "heartbeat.log",         # weekly log trim block
]

EXPECTED_SERVICES = [
    "freya.service",
    "polymarket_syn.service",
    "odin_day.service",
    "odin_swing.service",
    "odin_futures_day.service",
    "odin_futures_swing.service",
]

# state file → max age in minutes before flagged stale
STATE_FILES = {
    f"{WORKSPACE}/research/tyr_state.json":             90,
    f"{WORKSPACE}/research/heimdall_state.json":        90,
    f"{WORKSPACE}/competition/anthropic_health_state.json": 60,
    f"{WORKSPACE}/competition/exchange_health_state.json":  30,
    f"{WORKSPACE}/competition/heartbeat_state.json":    90,
    f"{WORKSPACE}/competition/watchdog.log":            30,
    f"{WORKSPACE}/competition/regression_watch_state.json": 180,
    f"{WORKSPACE}/competition/killswitch_state.json":   30,  # dormant writes no state — see killswitch check
    f"{WORKSPACE}/competition/freshness_state.json":    180,
}

KILLSWITCH_FLAG    = f"{WORKSPACE}/KILLSWITCH_TRIGGERED"
KILLSWITCH_SECRETS = "/root/.openclaw/secrets/kraken.json"


def ts():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M PST")


def log(msg):
    line = f"[{ts()}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


INBOX = "/root/.openclaw/workspace/syn_inbox.jsonl"


def tg_actionable(msg, severity="warning"):
    """Write to SYN inbox. Audit findings are dashboard-only drift reports."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "syn_audit",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        log(f"[syn_audit/inbox] {e}")


def check_cron(findings):
    try:
        out = subprocess.check_output(["crontab", "-l"], text=True)
    except Exception as e:
        findings.append(f"cron: cannot read crontab ({e})")
        return
    # Filter comments and blanks
    live = [ln for ln in out.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    for expected in EXPECTED_CRON:
        if not any(expected in ln for ln in live):
            findings.append(f"cron MISSING: no entry matching '{expected}'")
    # Detect unknown entries (not matching any expected substring)
    for ln in live:
        if not any(e in ln for e in EXPECTED_CRON):
            findings.append(f"cron UNKNOWN: {ln[:120]}")


def check_services(findings):
    for svc in EXPECTED_SERVICES:
        try:
            r = subprocess.run(
                ["systemctl", "is-active", svc],
                capture_output=True, text=True, timeout=10,
            )
            state = r.stdout.strip()
            if state != "active":
                findings.append(f"service {svc}: state={state}")
        except Exception as e:
            findings.append(f"service {svc}: check failed ({e})")


def check_state_staleness(findings):
    now = time.time()
    for path, max_min in STATE_FILES.items():
        if not os.path.isfile(path):
            # Killswitch state is expected absent while dormant — skip
            if "killswitch_state" in path and not os.path.isfile(KILLSWITCH_SECRETS):
                continue
            findings.append(f"state MISSING: {path}")
            continue
        age_min = (now - os.path.getmtime(path)) / 60
        if age_min > max_min:
            findings.append(f"state STALE: {os.path.basename(path)} age={age_min:.0f}min (max {max_min})")


def check_orphan_scripts(findings):
    # All *.py in workspace root + research/
    candidates = []
    for pattern in [f"{WORKSPACE}/*.py", f"{WORKSPACE}/research/*.py"]:
        candidates.extend(glob.glob(pattern))
    # Gather all referenced scripts from crontab + systemd unit files + all .py source
    try:
        cron_txt = subprocess.check_output(["crontab", "-l"], text=True)
    except Exception:
        cron_txt = ""
    unit_txt = ""
    for unit in glob.glob("/etc/systemd/system/*.service"):
        try:
            with open(unit) as f:
                unit_txt += f.read()
        except Exception:
            pass
    source_txt = ""
    for src in candidates:
        try:
            with open(src) as f:
                source_txt += f.read()
        except Exception:
            pass
    referenced = cron_txt + unit_txt + source_txt

    # One-shot tools and legacy scripts — intentionally kept, manually invoked
    MANUAL_TOOLS = {
        "sprint_backfill.py", "patch_futures_research.py",
        "backfill_odin_tsv.py", "odin_grid_search.py", "odin_backtest.py",
        "volva_backtest.py", "sn8_scout.py", "send_alerts.py",
        "send-leaderboard.py", "process_alerts.py",
        "polymarket_init.py", "polymarket_auto_init.py", "polymarket_syn_init.py",
        "polymarket_sprint_start.py", "swing_competition_start.py",
        "day_retroactive_fill.py", "day_retro_fill.py",
        "heartbeat_check.py", "heartbeat_script.py",
        "check_sprint_end.py",
    }
    for path in candidates:
        name = os.path.basename(path)
        if name.endswith(".bak") or ".bak" in name or name.startswith("_"):
            continue
        if name in MANUAL_TOOLS:
            continue
        # Match name or bare basename (e.g., "mimir.py" or "research/mimir.py")
        if name not in referenced:
            findings.append(f"orphan script: {path.replace(WORKSPACE + '/', '')} (no cron/systemd/source ref)")


def check_backup_rot(findings):
    now = time.time()
    stale = []
    for pattern in [f"{WORKSPACE}/*.bak*", f"{WORKSPACE}/**/*.bak*"]:
        for path in glob.glob(pattern, recursive=True):
            try:
                age_days = (now - os.path.getmtime(path)) / 86400
                if age_days > 30:
                    stale.append((age_days, path))
            except Exception:
                pass
    if stale:
        findings.append(f"backup rot: {len(stale)} .bak files older than 30 days (oldest: {max(stale)[0]:.0f}d)")


def check_killswitch(findings):
    if os.path.isfile(KILLSWITCH_FLAG):
        findings.append(f"KILLSWITCH TRIGGERED — flag present at {KILLSWITCH_FLAG}")
    # When dormant (no kraken.json), skip state-file freshness. When active, fold into STATE_FILES check.


def report_dedup_stats():
    """Per-league dedup_reject rollup — informational log line, no SYN alert."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M")
    for league in ("day", "futures_day", "swing", "futures_swing"):
        tsv = f"{WORKSPACE}/research/{league}/results.tsv"
        if not os.path.isfile(tsv):
            continue
        total = last_7d = 0
        try:
            with open(tsv) as f:
                for ln in f:
                    cols = ln.rstrip("\n").split("\t")
                    if len(cols) >= 8 and cols[5] == "dedup_reject":
                        total += 1
                        if cols[7] >= cutoff:
                            last_7d += 1
            log(f"dedup {league}: total={total} last_7d={last_7d}")
        except Exception as e:
            log(f"dedup {league}: read failed ({e})")


def main():
    log("=== SYN audit starting ===")
    findings = []

    for check in (check_cron, check_services, check_state_staleness,
                  check_orphan_scripts, check_backup_rot, check_killswitch):
        try:
            check(findings)
        except Exception as e:
            findings.append(f"{check.__name__} errored: {e}")

    report_dedup_stats()

    if not findings:
        log("audit clean: no drift detected")
        return

    for f in findings:
        log(f"  FINDING: {f}")

    body = "\n".join(f"• {f[:200]}" for f in findings[:25])
    tg_actionable(
        f"<b>SYN AUDIT — drift detected</b>\n"
        f"{ts()}\n\n"
        f"{body}\n\n"
        f"Full log: {LOG_FILE}"
    )


if __name__ == "__main__":
    main()
