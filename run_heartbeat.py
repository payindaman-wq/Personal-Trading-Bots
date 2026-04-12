
import json, os, subprocess
from datetime import datetime, timezone, timedelta

STATE_FILE = "/root/.openclaw/workspace/competition/heartbeat_syn_state.json"
now = datetime.now(timezone.utc)
problems = []

# Step 1: Load alert state
state = {"alerted": {}}
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    except json.JSONDecodeError:
        # Handle case where file is empty or malformed
        pass

def already_alerted(key):
    ts = state["alerted"].get(key)
    if not ts:
        return False
    try:
        alert_time = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
        return now - alert_time < timedelta(hours=24)
    except ValueError:
        # Handle invalid isoformat string in state file
        return False

def mark_alerted(key):
    state["alerted"][key] = now.isoformat()

def save_state():
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# Step 2: Run checks, collect new problems only

# Pending Alerts
pending_alerts_path = "/root/.openclaw/workspace/alerts/pending_*.txt"
alert_files_cmd = f"ls {pending_alerts_path} 2>/dev/null"
alert_files_process = subprocess.run(alert_files_cmd, shell=True, capture_output=True, text=True)
alert_files = alert_files_process.stdout.strip().split('\n')
if alert_files and alert_files[0]: # Check if any files were found
    for alert_file in alert_files:
        if os.path.exists(alert_file):
            try:
                with open(alert_file, 'r') as f:
                    alert_content = f.read().strip()
                problems.append(f"ALERT - Pending Alert File: {os.path.basename(alert_file)}\n{alert_content}")
                mark_alerted(f"pending_alert_{os.path.basename(alert_file)}_{now.isoformat()}") # Unique key
                os.remove(alert_file)
            except Exception as e:
                problems.append(f"ERROR: Could not process alert file {alert_file}: {e}")

# Day Trading Tick Health
leaderboard_path = "/root/.openclaw/workspace/competition/leaderboard.json"
day_tick_stale_key = "day_tick_stale"
if os.path.exists(leaderboard_path):
    stat_cmd_day = f"stat -c %Y {leaderboard_path}"
    stat_process_day = subprocess.run(stat_cmd_day, shell=True, capture_output=True, text=True)
    if stat_process_day.returncode == 0 and stat_process_day.stdout.strip().isdigit():
        last_mod_timestamp = int(stat_process_day.stdout.strip())
        last_mod_dt = datetime.fromtimestamp(last_mod_timestamp, timezone.utc)
        if now - last_mod_dt > timedelta(minutes=15):
            active_dir_contents = os.listdir('/root/.openclaw/workspace/competition/active') if os.path.exists('/root/.openclaw/workspace/competition/active') else []
            if active_dir_contents:
                if not already_alerted(day_tick_stale_key):
                    cron_log = ""
                    try:
                        with open('/root/.openclaw/workspace/competition/cron.log', 'r') as f:
                            cron_log = "\n".join(f.readlines()[-10:]).strip()
                    except FileNotFoundError:
                        cron_log = "cron.log not found."
                    problems.append(f"ALERT - Day Trading Tick Stale\nleaderboard.json last modified {now - last_mod_dt} ago. Sprint active.\nLast 10 lines of cron.log:\n{cron_log}")
                    mark_alerted(day_tick_stale_key)
    else:
        problems.append(f"ERROR: Could not get modification time for {leaderboard_path}")
else:
    problems.append(f"ALERT - Day Trading Tick: {leaderboard_path} not found. Tick may be stalled.")
    if not already_alerted(day_tick_stale_key):
        problems.append(f"ALERT - Day Trading Tick Stale\n{leaderboard_path} not found. Tick may be stalled.")
        mark_alerted(day_tick_stale_key)


# Swing Trading Tick Health
swing_leaderboard_path = "/root/.openclaw/workspace/competition/swing/swing_leaderboard.json"
swing_tick_stale_key = "swing_tick_stale"
if os.path.exists(swing_leaderboard_path):
    stat_cmd_swing = f"stat -c %Y {swing_leaderboard_path}"
    stat_process_swing = subprocess.run(stat_cmd_swing, shell=True, capture_output=True, text=True)
    if stat_process_swing.returncode == 0 and stat_process_swing.stdout.strip().isdigit():
        last_mod_timestamp = int(stat_process_swing.stdout.strip())
        last_mod_dt = datetime.fromtimestamp(last_mod_timestamp, timezone.utc)
        if now - last_mod_dt > timedelta(minutes=90):
            swing_active_dir = '/root/.openclaw/workspace/competition/swing/active'
            swing_active_dir_contents = os.listdir(swing_active_dir) if os.path.exists(swing_active_dir) else []
            if swing_active_dir_contents:
                if not already_alerted(swing_tick_stale_key):
                    problems.append(f"ALERT - Swing Trading Tick Stale\nswing_leaderboard.json last modified {now - last_mod_dt} ago. Swing sprint active.")
                    mark_alerted(swing_tick_stale_key)
    else:
        problems.append(f"ERROR: Could not get modification time for {swing_leaderboard_path}")
else:
    problems.append(f"ALERT - Swing Trading Tick: {swing_leaderboard_path} not found. Tick may be stalled.")
    if not already_alerted(swing_tick_stale_key):
        problems.append(f"ALERT - Swing Trading Tick Stale\n{swing_leaderboard_path} not found. Tick may be stalled.")
        mark_alerted(swing_tick_stale_key)

# Active Day Sprint Check
day_no_sprint_key = "day_no_sprint"
active_day_sprint_path = "/root/.openclaw/workspace/competition/active/"
active_day_sprint_entries = sorted(os.listdir(active_day_sprint_path)) if os.path.isdir(active_day_sprint_path) else []

if not active_day_sprint_entries:
    if not already_alerted(day_no_sprint_key):
        restart_cmd = "python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 24"
        restart_process = subprocess.run(restart_cmd, shell=True, capture_output=True, text=True)
        if restart_process.returncode == 0:
            problems.append(f"ALERT - Active Day Sprint: No day sprint active. Auto-restarted with '{restart_cmd}'.")
        else:
            problems.append(f"ALERT - Active Day Sprint: No day sprint active. Attempted auto-restart failed: {restart_process.stderr.strip()}")
        mark_alerted(day_no_sprint_key)

# Sprint End Detection
d = '/root/.openclaw/workspace/competition/active'
if os.path.isdir(d):
    entries = sorted(os.listdir(d))
    if entries:
        try:
            meta = json.load(open(f'{d}/{entries[-1]}/meta.json'))
            started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
            duration_hours = meta.get('duration_hours', 24)
            ends = started + timedelta(hours=duration_hours)
            if now > ends:
                comp_id = entries[-1]
                score_cmd = f"python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py {comp_id} --archive"
                leaderboard_cmd = "python3 /root/.openclaw/workspace/leaderboard.py --json"
                dashboard_cmd = "python3 /root/.openclaw/workspace/dashboard_data.py"

                subprocess.run(score_cmd, shell=True, capture_output=True, text=True)
                subprocess.run(leaderboard_cmd, shell=True, capture_output=True, text=True)
                subprocess.run(dashboard_cmd, shell=True, capture_output=True, text=True)
        except Exception as e:
            problems.append(f"ERROR: Could not process sprint end detection for {entries[-1]}: {e}")

# Step 3: Send alerts for new problems only
save_state()

if problems:
    for problem_message in problems:
        print(problem_message)
else:
    print("HEARTBEAT_OK")
