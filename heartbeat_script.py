
import json, os, glob
from datetime import datetime, timezone, timedelta

STATE = "/root/.openclaw/workspace/competition/heartbeat_syn_state.json"
now = datetime.now(timezone.utc)

state = {"alerted": {}}
if os.path.exists(STATE):
    try:
        with open(STATE, 'r') as f:
            state = json.load(f)
    except json.JSONDecodeError:
        state = {"alerted": {}}

def already_alerted(key):
    ts = state["alerted"].get(key)
    if not ts:
        return False
    if isinstance(ts, str):
        try:
            return now - datetime.fromisoformat(ts) < timedelta(hours=24)
        except ValueError:
            return False
    return False

def mark_alerted(key):
    state["alerted"][key] = now.isoformat()

def save_state():
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)

problems = []

# Pending Alerts
pending_alert_files = glob.glob("/root/.openclaw/workspace/alerts/pending_*.txt")
if pending_alert_files:
    for alert_file in pending_alert_files:
        if not already_alerted(f"alert_{os.path.basename(alert_file)}"):
            problems.append({"key": f"alert_{os.path.basename(alert_file)}", "type": "pending_alert", "file": alert_file})

# Active Day Sprint check
day_active_sprint_dir = "/root/.openclaw/workspace/competition/active/"
day_sprint_entries = []
if os.path.isdir(day_active_sprint_dir):
    day_sprint_entries = sorted(os.listdir(day_active_sprint_dir))
is_day_sprint_active = bool(day_sprint_entries)

# Day Trading Tick Health
leaderboard_file = "/root/.openclaw/workspace/competition/leaderboard.json"
if os.path.exists(leaderboard_file) and is_day_sprint_active:
    leaderboard_mod_time = datetime.fromtimestamp(os.path.getmtime(leaderboard_file), tz=timezone.utc)
    if now - leaderboard_mod_time > timedelta(minutes=15):
        if not already_alerted("day_tick_stale"):
            problems.append({"key": "day_tick_stale", "type": "tick_health", "sprint_type": "day"})
elif is_day_sprint_active and not os.path.exists(leaderboard_file):
    if not already_alerted("day_tick_stale_no_file"):
        problems.append({"key": "day_tick_stale_no_file", "type": "tick_health", "sprint_type": "day", "message": "leaderboard.json missing"})

# Swing Trading Tick Health
swing_leaderboard_file = "/root/.openclaw/workspace/competition/swing/swing_leaderboard.json"
swing_active_sprint_dir = "/root/.openclaw/workspace/competition/swing/active/"
swing_sprint_entries = []
if os.path.isdir(swing_active_sprint_dir):
    swing_sprint_entries = sorted(os.listdir(swing_active_sprint_dir))
is_swing_sprint_active = bool(swing_sprint_entries)

if os.path.exists(swing_leaderboard_file) and is_swing_sprint_active:
    swing_leaderboard_mod_time = datetime.fromtimestamp(os.path.getmtime(swing_leaderboard_file), tz=timezone.utc)
    if now - swing_leaderboard_mod_time > timedelta(minutes=90):
        if not already_alerted("swing_tick_stale"):
            problems.append({"key": "swing_tick_stale", "type": "tick_health", "sprint_type": "swing"})
elif is_swing_sprint_active and not os.path.exists(swing_leaderboard_file):
    if not already_alerted("swing_tick_stale_no_file"):
        problems.append({"key": "swing_tick_stale_no_file", "type": "tick_health", "sprint_type": "swing", "message": "swing_leaderboard.json missing"})

# Active Day Sprint (auto-fix and then alert)
if not day_sprint_entries:
    if not already_alerted("day_no_sprint"):
        problems.append({"key": "day_no_sprint", "type": "sprint_status", "action": "restart"})

# Sprint End Detection
d_sprint_end_path = '/root/.openclaw/workspace/competition/active'
entries = []
if os.path.isdir(d_sprint_end_path):
    entries = sorted(os.listdir(d_sprint_end_path))
if entries:
    meta_path = f'{d_sprint_end_path}/{entries[-1]}/meta.json'
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
            started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
            ends = started + timedelta(hours=meta['duration_hours'])
            if now > ends:
                if not already_alerted(f"sprint_expired_{entries[-1]}"):
                    problems.append({"key": f"sprint_expired_{entries[-1]}", "type": "sprint_end", "comp_id": entries[-1]})
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            if not already_alerted(f"sprint_meta_error_{entries[-1]}"):
                problems.append({"key": f"sprint_meta_error_{entries[-1]}", "type": "error", "message": f"Error reading meta.json for {entries[-1]}: {e}"})

# Process problems and send alerts
for problem in problems:
    if problem["type"] == "pending_alert":
        with open(problem["file"], 'r') as f:
            alert_content = f.read()
        print(f"MESSAGE: {alert_content}")
        mark_alerted(problem["key"])
        os.remove(problem["file"])
    elif problem["type"] == "tick_health":
        message_text = f"ALERT — {problem['sprint_type'].capitalize()} Trading Tick Stalled.\n"
        if "message" in problem:
            message_text += f"Reason: {problem['message']}\n"
        message_text += f"Leaderboard file not updated in over {'15 minutes' if problem['sprint_type'] == 'day' else '90 minutes'}.\n"
        print(f"MESSAGE: {message_text}")
        mark_alerted(problem["key"])
    elif problem["type"] == "sprint_status" and problem["key"] == "day_no_sprint":
        print("EXEC: python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 24")
        print("MESSAGE: ALERT — Day Trading Sprint Restarted.\nNo active sprint detected. Initiated new 24-hour sprint.")
        mark_alerted(problem["key"])
    elif problem["type"] == "sprint_end":
        comp_id = problem["comp_id"]
        print(f"EXEC: python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py {comp_id} --archive")
        print("EXEC: python3 /root/.openclaw/workspace/leaderboard.py --json")
        print("EXEC: python3 /root/.openclaw/workspace/dashboard_data.py")
        mark_alerted(problem["key"])
    elif problem["type"] == "error":
        print(f"MESSAGE: ALERT — Internal Error: {problem['message']}")
        mark_alerted(problem["key"])

save_state()

if not problems:
    print("HEARTBEAT_OK")
