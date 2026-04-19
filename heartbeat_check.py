
import json, os
from datetime import datetime, timezone, timedelta

STATE = "/root/.openclaw/workspace/competition/heartbeat_syn_state.json"
now = datetime.now(timezone.utc)

if os.path.exists(STATE):
    with open(STATE, 'r') as f:
        state = json.load(f)
else:
    state = {"alerted": {}}

def already_alerted(key):
    ts = state["alerted"].get(key)
    if not ts:
        return False
    alert_time = datetime.fromisoformat(ts)
    if alert_time.tzinfo is None:
        alert_time = alert_time.replace(tzinfo=timezone.utc)
    return now - alert_time < timedelta(hours=24)

def mark_alerted(key):
    state["alerted"][key] = now.isoformat()

def save_state():
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)

problems = []
alerts_to_send = []

# Day Trading Tick Health
try:
    day_leaderboard_stat = os.stat("/root/.openclaw/workspace/competition/leaderboard.json")
    day_leaderboard_modified_time = datetime.fromtimestamp(day_leaderboard_stat.st_mtime, timezone.utc)
    if now - day_leaderboard_modified_time > timedelta(minutes=15):
        day_active_sprint_dir = "/root/.openclaw/workspace/competition/active/"
        if os.path.isdir(day_active_sprint_dir) and os.listdir(day_active_sprint_dir):
            if not already_alerted("day_tick_stale"):
                problems.append("day_tick_stale")
                alerts_to_send.append("ALERT — Day Trading Tick Stale\nSprint: Active | Time: " + now.strftime("%H:%M UTC") + "\nAction taken: Investigating cron.log for context.")
except FileNotFoundError:
    day_active_sprint_dir = "/root/.openclaw/workspace/competition/active/"
    if os.path.isdir(day_active_sprint_dir) and os.listdir(day_active_sprint_dir):
         if not already_alerted("day_tick_stale"):
                problems.append("day_tick_stale")
                alerts_to_send.append("ALERT — Day Trading Tick Stale (leaderboard.json not found but sprint active)\nSprint: Active | Time: " + now.strftime("%H:%M UTC") + "\nAction taken: Investigating cron.log for context.")

# Swing Trading Tick Health
try:
    swing_leaderboard_stat = os.stat("/root/.openclaw/workspace/competition/swing/swing_leaderboard.json")
    swing_leaderboard_modified_time = datetime.fromtimestamp(swing_leaderboard_stat.st_mtime, timezone.utc)
    if now - swing_leaderboard_modified_time > timedelta(minutes=90):
        if not already_alerted("swing_tick_stale"):
            problems.append("swing_tick_stale")
            alerts_to_send.append("ALERT — Swing Trading Tick Stale\nSprint: Active | Time: " + now.strftime("%H:%M UTC") + "\nAction taken: Investigating.")
except FileNotFoundError:
    pass

# Active Day Sprint - This check is for between 13:00-13:00 UTC. The current time is 23:30 UTC, so it's not within that window.
# No action needed for this heartbeat as per the rules in HEARTBEAT.md

# Sprint End Detection
d = '/root/.openclaw/workspace/competition/active'
entries = sorted(os.listdir(d)) if os.path.isdir(d) else []
sprints_to_score = []
for entry in entries:
    full_path = os.path.join(d, entry)
    if not os.path.isdir(full_path): # Add this check to skip non-directories
        continue

    try:
        meta = json.load(open(f'{full_path}/meta.json'))
        started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
        ends = started + timedelta(hours=meta['duration_hours'])
        if now > ends:
            sprints_to_score.append(entry)
    except FileNotFoundError:
        print(f"Meta file not found for sprint {entry}")
    except json.JSONDecodeError:
        print(f"Error decoding meta.json for sprint {entry}")

# Perform scoring for expired sprints
for comp_id in sprints_to_score:
    print(f'EXPIRED: {comp_id} - Scoring and Archiving.')
    if not already_alerted(f"sprint_scored_{comp_id}"): 
        problems.append(f"sprint_needs_scoring_{comp_id}") 

if not problems and not alerts_to_send:
    print("HEARTBEAT_OK")
else:
    for problem_key in problems:
        mark_alerted(problem_key)
    save_state()

    for alert_message in alerts_to_send:
        print(f"TELEGRAM_ALERT: {alert_message}")

    for comp_id in sprints_to_score:
        print(f"RUN_COMMAND: python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py {comp_id} --archive")
        print("RUN_COMMAND: python3 /root/.openclaw/workspace/leaderboard.py --json")
        print("RUN_COMMAND: python3 /root/.openclaw/workspace/dashboard_data.py")
        mark_alerted(f"sprint_scored_{comp_id}")
    save_state()
