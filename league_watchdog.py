#!/usr/bin/env python3
"""
league_watchdog.py - Auto-restart leagues when no active sprint exists.

Run every 10 minutes via cron. Starts a new sprint for any league that
has no active competition running.

Cron entry:
  */10 * * * * python3 /root/.openclaw/workspace/league_watchdog.py >> /root/.openclaw/workspace/competition/watchdog.log 2>&1
"""
import os
import json
import subprocess
import urllib.request
from datetime import datetime, timezone, timedelta

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
CYCLE_STATE_PATH = os.path.join(WORKSPACE, "competition", "cycle_state.json")

LEAGUES = [
    {
        "name":            "day",
        "tick_interval_min": 5,
        "active_dir":      os.path.join(WORKSPACE, "competition", "active"),
        "start_cmd":       ["python3",
                            "/root/.openclaw/skills/competition-start/scripts/competition_start.py",
                            "24"],
    },
    {
        "name":            "swing",
        "tick_interval_min": 30,
        "active_dir":      os.path.join(WORKSPACE, "competition", "swing", "active"),
        "start_cmd":       ["python3", os.path.join(WORKSPACE, "swing_competition_start.py")],
    },
    {
        "name":            "futures_day",
        "tick_interval_min": 5,
        "active_dir":      os.path.join(WORKSPACE, "competition", "futures_day", "active"),
        "start_cmd":       ["python3", os.path.join(WORKSPACE, "futures_day_restart.py")],
    },
    {
        "name":            "futures_swing",
        "tick_interval_min": 30,
        "active_dir":      os.path.join(WORKSPACE, "competition", "futures_swing", "active"),
        "start_cmd":       ["python3", os.path.join(WORKSPACE, "futures_swing_restart.py")],
    },
]

POLY_STATE  = os.path.join(WORKSPACE, "competition", "polymarket", "auto_state.json")
POLY_CYCLE  = os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_cycle_state.json")

# Health check alerting
from config_loader import config
BOT_TOKEN = config.telegram.bot_token
CHAT_ID   = config.telegram.chat_id
HEALTH_STATE_FILE = os.path.join(WORKSPACE, "competition", "watchdog_health_state.json")
ALERT_COOLDOWN_H  = 6


INBOX = os.path.join(WORKSPACE, "syn_inbox.jsonl")


def tg_send(msg, severity="error", alert_id=None):
    """Write to SYN inbox. sys_heartbeat is the sole Telegram gateway."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "league_watchdog",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        if alert_id:
            rec["alert_id"] = alert_id
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"  [league_watchdog/inbox] failed: {e}")


def load_health_state():
    try:
        with open(HEALTH_STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"last_alerted": {}}


def save_health_state(state):
    os.makedirs(os.path.dirname(HEALTH_STATE_FILE), exist_ok=True)
    with open(HEALTH_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def should_alert(state, key):
    last = state["last_alerted"].get(key)
    if not last:
        return True
    return datetime.now(timezone.utc) - datetime.fromisoformat(last) > timedelta(hours=ALERT_COOLDOWN_H)


def mark_alerted(state, key):
    state["last_alerted"][key] = datetime.now(timezone.utc).isoformat()


def clear_alert(state, key):
    state["last_alerted"].pop(key, None)


def check_execution_health(league_name, meta, comp_dir, tick_interval_min):
    problems = []
    now = datetime.now(timezone.utc)

    started_at_str = meta.get("started_at", "")
    if not started_at_str:
        return problems
    try:
        started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
    except Exception:
        return problems
    sprint_age_h = (now - started_at).total_seconds() / 3600

    grace_h = 6.0 if "swing" in league_name else 2.0
    if sprint_age_h < grace_h:
        return problems

    bots = meta.get("bots", [])
    if not bots:
        return problems

    total_open     = 0
    total_closed   = 0
    missing_mtm    = 0
    stale_files    = 0
    found_files    = 0
    stale_thresh_m = tick_interval_min * 3

    for bot in bots:
        pf_path = os.path.join(comp_dir, f"portfolio-{bot}.json")
        if not os.path.exists(pf_path):
            continue
        found_files += 1
        age_min = (now.timestamp() - os.path.getmtime(pf_path)) / 60
        if age_min > stale_thresh_m:
            stale_files += 1
        try:
            with open(pf_path) as f:
                pf = json.load(f)
            total_open   += len(pf.get("positions", []))
            total_closed += len(pf.get("closed_trades", []))
            if "live_equity_mtm" not in pf.get("stats", {}):
                missing_mtm += 1
        except Exception:
            pass

    if found_files == 0:
        return problems

    comp_id = meta.get("comp_id", "?")
    sprint_start_utc = started_at.strftime("%Y-%m-%dT09:00:00+00:00")
    fix_prompt = (
        f"Fix {league_name} sprint {comp_id}: diagnose and repair the issue, "
        f"then backfill from {sprint_start_utc} to now."
    )

    if total_open == 0 and total_closed == 0:
        lines = [
            f"\u26a0\ufe0f <b>[{league_name}] DEAD EXECUTION</b>",
            f"Sprint <code>{comp_id}</code> \u2014 {len(bots)} bots, {sprint_age_h:.1f}h running, <b>0 positions + 0 closed trades</b>",
            "Tick not persisting trades.",
            f"<code>{fix_prompt}</code>",
        ]
        problems.append((f"{league_name}:dead_execution", "\n".join(lines), comp_id))

    if missing_mtm == found_files and missing_mtm > 0:
        lines = [
            f"\u26a0\ufe0f <b>[{league_name}] NO MTM TRACKING</b>",
            f"Sprint <code>{comp_id}</code> \u2014 <code>live_equity_mtm</code> missing from all {found_files} bots.",
            "Tick not updating equity stats.",
            f"<code>{fix_prompt}</code>",
        ]
        problems.append((f"{league_name}:no_mtm", "\n".join(lines), comp_id))

    if stale_files == found_files:
        lines = [
            f"\u26a0\ufe0f <b>[{league_name}] TICK STALE</b>",
            f"Sprint <code>{comp_id}</code> \u2014 all {found_files} portfolio files >{stale_thresh_m:.0f}m old (tick every {tick_interval_min}m).",
            "Cron or tick script may be down.",
            f"<code>{fix_prompt}</code>",
        ]
        problems.append((f"{league_name}:stale_tick", "\n".join(lines), comp_id))

    return problems


def find_active(active_dir):
    if not os.path.isdir(active_dir):
        return None, False
    entries = sorted([e for e in os.listdir(active_dir) if not e.startswith('.')])
    if not entries:
        return None, False
    has_multiple = len(entries) > 1
    if has_multiple:
        print(f"  WARNING: {len(entries)} entries in {active_dir} — orphaned sprints detected: {entries[:-1]}")
    comp_dir  = os.path.join(active_dir, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None, has_multiple
    with open(meta_path) as f:
        meta = json.load(f)
    result = meta if meta.get("status") == "active" else None
    return result, has_multiple


def find_polymarket_active():
    if not os.path.isfile(POLY_STATE):
        return None
    if os.path.isfile(POLY_CYCLE):
        with open(POLY_CYCLE) as f:
            cs = json.load(f)
        if cs.get("status") == "awaiting_review":
            return "awaiting_review"
    with open(POLY_STATE) as f:
        state = json.load(f)
    if state.get("status") != "active":
        return None
    ends_at = state.get("sprint_ends_at")
    if ends_at:
        end_dt = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))
        if datetime.now(timezone.utc) > end_dt:
            return None
    return state.get("sprint_id", "active")


def _update_day_cycle_state(comp_id):
    try:
        with open(CYCLE_STATE_PATH) as f:
            cs = json.load(f)
        if comp_id not in cs.get("sprints", []):
            cs.setdefault("sprints", []).append(comp_id)
            cs["sprint_in_cycle"] = len(cs["sprints"])
            if not cs.get("cycle_started_at"):
                cs["cycle_started_at"] = datetime.now(timezone.utc).isoformat()
            with open(CYCLE_STATE_PATH, "w") as f:
                json.dump(cs, f, indent=2)
            print(f"  [day] cycle_state updated: cycle={cs['cycle']} sprint={cs['sprint_in_cycle']}")
    except Exception as e:
        print(f"  [day] WARNING: could not update cycle_state: {e}")


def start_league(league):
    result = subprocess.run(
        league["start_cmd"],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            comp_id = data.get("comp_id", data.get("sprint_id", "?"))
            print(f"  [{league['name']}] started: {comp_id}")
            if league["name"] == "day" and comp_id != "?":
                _update_day_cycle_state(comp_id)
        except Exception:
            print(f"  [{league['name']}] started OK")
    else:
        print(f"  [{league['name']}] ERROR: {result.stderr[:300]}")


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[league_watchdog] {now}")

    health_state = load_health_state()
    health_dirty = False

    for league in LEAGUES:
        meta, has_multiple = find_active(league["active_dir"])
        if meta:
            print(f"  [{league['name']}] OK \u2014 {meta['comp_id']}")

            comp_dir = os.path.join(league["active_dir"], meta["comp_id"])
            tick_min = league.get("tick_interval_min", 30)
            problems = check_execution_health(league["name"], meta, comp_dir, tick_min)
            for alert_key, alert_msg, comp_id in problems:
                print(f"  [{league['name']}] HEALTH WARN: {alert_key}")
                if should_alert(health_state, alert_key):
                    tg_send(alert_msg, alert_id=f"{alert_key}:{comp_id}")
                    mark_alerted(health_state, alert_key)
                    health_dirty = True
            for check_suffix in ("dead_execution", "no_mtm", "stale_tick"):
                key = f"{league['name']}:{check_suffix}"
                if key not in [p[0] for p in problems]:
                    if key in health_state["last_alerted"]:
                        clear_alert(health_state, key)
                        health_dirty = True
        else:
            active_dir = league["active_dir"]
            real_files = [f for f in os.listdir(active_dir) if not f.startswith('.')] if os.path.isdir(active_dir) else []
            if real_files:
                print(f"  [{league['name']}] WARNING: no active sprint but active/ is non-empty \u2014 skipping restart to avoid stacking")
            else:
                print(f"  [{league['name']}] IDLE \u2014 restarting...")
                start_league(league)

    poly = find_polymarket_active()
    if poly == "awaiting_review":
        print(f"  [polymarket] awaiting_review \u2014 skipping auto-restart")
    elif poly:
        print(f"  [polymarket] OK \u2014 {poly}")
    else:
        print(f"  [polymarket] IDLE \u2014 restarting...")
        start_league({
            "name":      "polymarket",
            "start_cmd": ["python3", os.path.join(WORKSPACE, "polymarket_sprint_start.py")],
        })

    if health_dirty:
        save_health_state(health_state)

    # Sprint integrity check (SYN) — detects orphan/phantom sprints, counter drift, missing archives
    try:
        subprocess.run(['python3', os.path.join(WORKSPACE, 'sprint_integrity_check.py')], timeout=30, check=False)
    except Exception as e:
        print(f'  [sprint_integrity] check failed: {e}')



if __name__ == "__main__":
    main()
