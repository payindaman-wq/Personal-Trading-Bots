import json, os
from datetime import datetime, timezone, timedelta
d = '/root/.openclaw/workspace/competition/active'
entries = sorted(os.listdir(d)) if os.path.isdir(d) else []
if entries:
    meta = json.load(open(f'{d}/{entries[-1]}/meta.json'))
    started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
    duration_hours = meta['duration_hours'] if 'duration_hours' in meta else 24 # Default to 24 hours if not specified
    ends = started + timedelta(hours=duration_hours)
    if datetime.now(timezone.utc) > ends:
        print(f'EXPIRED: {entries[-1]}')
    else:
        print("Sprint is still active.")
else:
    print("No active sprints found.")
