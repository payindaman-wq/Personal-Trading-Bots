#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

# Get leaderboard output
result = subprocess.run(
    ["python3", "/root/.openclaw/workspace/leaderboard.py"],
    cwd="/root/.openclaw/workspace",
    capture_output=True,
    text=True
)

leaderboard_text = result.stdout

# Write to pending alerts for heartbeat processing
timestamp = datetime.utcnow().isoformat()
alert_file = f"/root/.openclaw/workspace/alerts/pending_leaderboard_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"

with open(alert_file, "w") as f:
    f.write(f"LEADERBOARD UPDATE — {timestamp}\n")
    f.write("=" * 80 + "\n\n")
    f.write(leaderboard_text)

print(f"Leaderboard written to {alert_file}")
