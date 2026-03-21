import json, os
from datetime import datetime, timezone, timedelta

STATE = "/root/.openclaw/workspace/competition/heartbeat_syn_state.json"
now = datetime(2026, 3, 20, 21, 0, 0, tzinfo=timezone.utc) # User provided current time: 2026-03-20 21:00 UTC

if os.path.exists(STATE):
    with open(STATE, "r") as f:
        state = json.load(f)
else:
    state = {"alerted": {}}

def already_alerted(key):
    ts = state["alerted"].get(key)
    if not ts:
        return False
    return now - datetime.fromisoformat(ts) < timedelta(hours=24)

def mark_alerted(key):
    state["alerted"][key] = now.isoformat()

def save_state():
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)

problems = []

# --- Pending Alerts ---
pending_alerts_cmd = "ls /root/.openclaw/workspace/alerts/pending_*.txt 2>/dev/null"
pending_alerts_output = os.popen(pending_alerts_cmd).read().strip().split('\n')
if pending_alerts_output and pending_alerts_output[0]:
    for alert_file in pending_alerts_output:
        if os.path.exists(alert_file):
            with open(alert_file, "r") as f:
                alert_content = f.read().strip()
            problems.append({"key": f"pending_alert_{os.path.basename(alert_file)}", "message": alert_content, "action": f"delete_file:{alert_file}"})

# --- Day Trading Tick Health ---
leaderboard_path = "/root/.openclaw/workspace/competition/leaderboard.json"
day_tick_stale = False
mod_time_day = None
if os.path.exists(leaderboard_path):
    mod_time_day = datetime.fromtimestamp(os.path.getmtime(leaderboard_path), tz=timezone.utc)
    if now - mod_time_day > timedelta(minutes=15):
        day_tick_stale = True

active_day_sprints_dir = "/root/.openclaw/workspace/competition/active/"
active_day_sprints = os.listdir(active_day_sprints_dir) if os.path.exists(active_day_sprints_dir) else []

if day_tick_stale and active_day_sprints:
    cron_log_path = "/root/.openclaw/workspace/competition/cron.log"
    cron_log_tail = ""
    if os.path.exists(cron_log_path):
        with open(cron_log_path, "r") as f:
            lines = f.readlines()
            cron_log_tail = "".join(lines[-10:])
    message = f"Day trading tick is stale. Leaderboard last modified: {mod_time_day.isoformat()}. Active sprint detected. Last 10 lines of cron.log:\n{cron_log_tail}"
    problems.append({"key": "day_tick_stale", "message": message})

# --- Swing Trading Tick Health ---
swing_leaderboard_path = "/root/.openclaw/workspace/competition/swing/swing_leaderboard.json"
swing_tick_stale = False
mod_time_swing = None
if os.path.exists(swing_leaderboard_path):
    mod_time_swing = datetime.fromtimestamp(os.path.getmtime(swing_leaderboard_path), tz=timezone.utc)
    if now - mod_time_swing > timedelta(minutes=90):
        swing_tick_stale = True

active_swing_sprints_dir = "/root/.openclaw/workspace/competition/swing/active/"
active_swing_sprints = os.listdir(active_swing_sprints_dir) if os.path.exists(active_swing_sprints_dir) else []

if swing_tick_stale and active_swing_sprints:
    message = f"Swing trading tick is stale. Swing leaderboard last modified: {mod_time_swing.isoformat()}. Active swing sprint detected."
    problems.append({"key": "swing_tick_stale", "message": message})

# --- Active Day Sprint ---
if not active_day_sprints:
    problems.append({"key": "day_no_sprint", "message": "No active day sprint detected.", "action": "restart_day_sprint"})

# --- Sprint End Detection ---
d = "/root/.openclaw/workspace/competition/active"
entries = sorted(os.listdir(d)) if os.path.isdir(d) else []
if entries:
    meta_path = f"{d}/{entries[-1]}/meta.json"
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            meta = json.load(f)
        started = datetime.fromisoformat(meta["started_at"].replace('Z', '+00:00'))
        ends = started + timedelta(hours=meta["duration_hours"])
        if now > ends:
            problems.append({"key": "sprint_expired", "message": f"EXPIRED: {entries[-1]}", "action": f"score_archive:{entries[-1]}"})

# --- Process problems and send alerts ---
new_problems_found = False
for problem in problems:
    if not already_alerted(problem["key"]):
        if problem.get("action") == "restart_day_sprint":
            print("Action: Restarting day sprint...")
            print(os.popen("python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 24").read())
            message_to_send = "ALERT — No active day sprint. Restarted the day sprint.\n"
            print(f"TELEGRAM_MESSAGE:{message_to_send}")
            mark_alerted(problem["key"])
            new_problems_found = True
        elif problem.get("action", "").startswith("score_archive:"):
            comp_id = problem["action"].split(":")[1]
            print(f"Action: Scoring and archiving sprint {comp_id}...")
            print(os.popen(f"python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py {comp_id} --archive").read())
            print(os.popen("python3 /root/.openclaw/workspace/leaderboard.py --json").read())
            print(os.popen("python3 /root/.openclaw/workspace/dashboard_data.py").read())
            # No alert needed for routine sprint end.
            # Continue to next problem without marking as alerted or setting new_problems_found to True
        elif problem.get("action", "").startswith("delete_file:"):
            file_to_delete = problem["action"].split(":")[1]
            message_to_send = f"ALERT — Pending Alert: {problem['message']}"
            print(f"TELEGRAM_MESSAGE:{message_to_send}")
            print(os.popen(f"rm {file_to_delete}").read())
            mark_alerted(problem["key"])
            new_problems_found = True
        else:
            message_to_send = f"ALERT — {problem['message']}"
            print(f"TELEGRAM_MESSAGE:{message_to_send}")
            mark_alerted(problem["key"])
            new_problems_found = True

save_state()

if not new_problems_found:
    print("HEARTBEAT_OK")
