# HEARTBEAT.md — Periodic Checks

Run these every heartbeat (~30 min). Be brief. Only message Chris if something needs attention.

---

## 1. Pending Alerts
- Directory: `/root/.openclaw/workspace/alerts/`
- Pattern: `pending_*.txt`
- Action: Read, send to Telegram, delete

---

## 2. Day Trading Tick Health
```bash
stat /root/.openclaw/workspace/competition/leaderboard.json
```
- If modified >15 min ago and a sprint is active — tick is stalled
- Check: `tail -20 /root/.openclaw/workspace/competition/cron.log`
- Action if stalled: alert Chris with the last log lines

---

## 3. Swing Trading Tick Health
```bash
stat /root/.openclaw/workspace/competition/swing/swing_leaderboard.json
```
- If modified >90 min ago and a sprint is active — tick is stalled
- Check: `tail -20 /root/.openclaw/workspace/competition/swing/tick.log`
- Action if stalled: alert Chris with the last log lines

---

## 4. Active Sprint Check
```bash
ls /root/.openclaw/workspace/competition/active/
```
- Between 13:00 UTC and 13:00 UTC+24h a day sprint should always be active
- If directory is empty during this window: restart sprint, notify Chris
  ```bash
  python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 24
  ```

---

## 5. Sprint End Detection
```bash
# Check if active sprint has expired
python3 -c "
import json, os
from datetime import datetime, timezone, timedelta
d = '/root/.openclaw/workspace/competition/active'
entries = sorted(os.listdir(d)) if os.path.isdir(d) else []
if entries:
    meta = json.load(open(f'{d}/{entries[0]}/meta.json'))
    started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
    ends = started + timedelta(hours=meta['duration_hours'])
    now = datetime.now(timezone.utc)
    if now > ends:
        print(f'EXPIRED: {entries[0]} ended {ends.strftime(\"%H:%M UTC\")}')
    else:
        print(f'ACTIVE: {entries[0]} ends {ends.strftime(\"%H:%M UTC\")}')
else:
    print('NO ACTIVE SPRINT')
"
```
- If sprint has expired: score it, archive it, update leaderboard, send summary to Telegram
  ```bash
  python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py <comp_id> --archive
  python3 /root/.openclaw/workspace/leaderboard.py --json
  python3 /root/.openclaw/workspace/dashboard_data.py
  ```

---

## 6. Dashboard Availability (once per day is enough)
```bash
curl -s -o /dev/null -w "%{http_code}" http://5.78.188.151/
```
- Expected: 200
- If not 200: `systemctl restart nginx` and alert Chris

---

## Silent if all clear. Only speak when something needs attention.
