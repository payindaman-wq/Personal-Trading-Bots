
import json, os
from datetime import datetime, timezone, timedelta

# STATE file for alerts
STATE = "/root/.openclaw/workspace/competition/heartbeat_syn_state.json"
now = datetime.now(timezone.utc)

# Load state
state = {"alerted": {}}
if os.path.exists(STATE):
    try:
        with open(STATE, 'r') as f:
            state = json.load(f)
    except json.JSONDecodeError:
        print("Warning: Could not decode existing heartbeat_syn_state.json. Starting fresh.")
        state = {"alerted": {}}

def already_alerted(key):
    ts = state["alerted"].get(key)
    if not ts:
        return False
    ts_dt = datetime.fromisoformat(ts)
    if ts_dt.tzinfo is None and now.tzinfo is not None:
        ts_dt = ts_dt.replace(tzinfo=timezone.utc)
    return now - ts_dt < timedelta(hours=24)

def mark_alerted(key):
    state["alerted"][key] = now.isoformat()

def save_state():
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)

messages_to_send = []
problems_found = False

# Helper to check if a sprint is active
def is_sprint_active(competition_dir):
    active_dir = os.path.join(competition_dir, 'active')
    if not os.path.isdir(active_dir):
        return False
    entries = sorted(os.listdir(active_dir))
    return bool(entries)

# --- Step 2: Run checks, collect new problems only ---

# Pending Alerts (always report — these are one-shot)
pending_alerts_cmd = "ls /root/.openclaw/workspace/alerts/pending_*.txt 2>/dev/null"
pending_alerts_output = os.popen(pending_alerts_cmd).read().strip().split('\n')
if pending_alerts_output and pending_alerts_output[0]: # Check if not empty
    for alert_file in pending_alerts_output:
        if alert_file and os.path.exists(alert_file): # Ensure file path is not empty
            with open(alert_file, 'r') as f:
                alert_content = f.read().strip()
            messages_to_send.append(alert_content)
            os.remove(alert_file) # Delete after reading
            problems_found = True

# Day Trading Tick Health
day_tick_stale_key = "day_tick_stale"
day_leaderboard_path = "/root/.openclaw/workspace/competition/leaderboard.json"
day_tick_stale = False

if is_sprint_active("/root/.openclaw/workspace/competition"):
    try:
        stat_output = os.popen(f"stat -c %Y {day_leaderboard_path}").read().strip()
        if stat_output:
            last_modified_timestamp = int(stat_output)
            last_modified_dt = datetime.fromtimestamp(last_modified_timestamp, timezone.utc)
            if (now - last_modified_dt) > timedelta(minutes=15):
                day_tick_stale = True
        else: # stat command failed or returned empty, likely file missing
            day_tick_stale = True
    except Exception as e:
        day_tick_stale = True # Assume stale if stat fails

if day_tick_stale and not already_alerted(day_tick_stale_key):
    cron_log_cmd = "tail -10 /root/.openclaw/workspace/competition/cron.log"
    cron_log_output = os.popen(cron_log_cmd).read().strip()
    alert_message = "ALERT — Day Trading Tick Stale\nSprint: active | Time: {time}\nLeaderboard not updated in >15 min.\nLast 10 lines of cron.log:\n{log}".format(time=now.strftime('%H:%M UTC'), log=cron_log_output)
    messages_to_send.append(alert_message)
    mark_alerted(day_tick_stale_key)
    problems_found = True


# Swing Trading Tick Health
swing_tick_stale_key = "swing_tick_stale"
swing_leaderboard_path = "/root/.openclaw/workspace/competition/swing/swing_leaderboard.json"
swing_tick_stale = False

if is_sprint_active("/root/.openclaw/workspace/competition/swing"):
    try:
        stat_output = os.popen(f"stat -c %Y {swing_leaderboard_path}").read().strip()
        if stat_output:
            last_modified_timestamp = int(stat_output)
            last_modified_dt = datetime.fromtimestamp(last_modified_timestamp, timezone.utc)
            if (now - last_modified_dt) > timedelta(minutes=90):
                swing_tick_stale = True
        else:
            swing_tick_stale = True
    except Exception as e:
        swing_tick_stale = True

if swing_tick_stale and not already_alerted(swing_tick_stale_key):
    alert_message = "ALERT — Swing Trading Tick Stale\nSprint: active | Time: {time}\nSwing leaderboard not updated in >90 min.".format(time=now.strftime('%H:%M UTC'))
    messages_to_send.append(alert_message)
    mark_alerted(swing_tick_stale_key)
    problems_found = True

# Active Day Sprint Check
day_no_sprint_key = "day_no_sprint"
day_active_dir = '/root/.openclaw/workspace/competition/active'
day_sprint_missing = False

if not is_sprint_active("/root/.openclaw/workspace/competition"):
    day_sprint_missing = True

if day_sprint_missing and not already_alerted(day_no_sprint_key):
    # Attempt to auto-fix
    start_cmd = "python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 24"
    os.popen(start_cmd).read() # Execute the restart, ignore output for now

    alert_message = "ALERT — Day Sprint Missing\nSprint: none | Time: {time}\nNo active day sprint found. Attempted to restart it.".format(time=now.strftime('%H:%M UTC'))
    messages_to_send.append(alert_message)
    mark_alerted(day_no_sprint_key)
    problems_found = True

# Sprint End Detection
day_competition_active_dir = '/root/.openclaw/workspace/competition/active'
day_entries = sorted(os.listdir(day_competition_active_dir)) if os.path.isdir(day_competition_active_dir) else []

if day_entries:
    try:
        current_comp_id = day_entries[-1]
        meta_path = os.path.join(day_competition_active_dir, current_comp_id, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                meta = json.load(f)
            started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
            ends = started + timedelta(hours=meta['duration_hours'])

            if datetime.now(timezone.utc) > ends:
                # Sprint expired, score and archive it (no alert needed — routine)
                score_cmd = f"python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py {current_comp_id} --archive"
                os.popen(score_cmd).read()
                os.popen("python3 /root/.openclaw/workspace/leaderboard.py --json").read()
                os.popen("python3 /root/.openclaw/workspace/dashboard_data.py").read()
                problems_found = True # This is a routine action, but it's an action, so mark as "found"

    except Exception as e:
        print(f"Error checking day sprint end: {e}")


# --- Step 3: Send alerts for new problems only ---
save_state()

if not problems_found:
    print("HEARTBEAT_OK")
else:
    for msg in messages_to_send:
        print(f"ALERT_MESSAGE_TO_SEND: {msg}")
