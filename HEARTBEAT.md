# HEARTBEAT.md — Periodic Checks

**Rules (read first, always):**
- ONLY message Chris when a new problem is detected. Never send status updates, confirmations, or "all clear" messages.
- Each problem has a 24-hour cooldown. If you already reported a problem in the last 24 hours, stay silent — Chris knows about it and is resolving it.
- New/different problems always get reported immediately.
- If nothing is wrong: reply HEARTBEAT_OK and stop. No Telegram message.

---

## How to send a Telegram alert (REQUIRED — do not improvise the recipient)

When you need to message Chris, use this exact pattern. Do NOT use `@heartbeat` or any `@`-handle — Telegram bots cannot resolve usernames to chat IDs and the message will silently bounce.

```python
import json, urllib.request
from config_loader import config
BOT_TOKEN = config.telegram.bot_token
CHAT_ID = config.telegram.chat_id

def tg_send(body):
    msg = f'[SYN/heartbeat] {body}'  # SYN-prefix-applied — required convention
    payload = json.dumps({'chat_id': CHAT_ID, 'text': msg}).encode()
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        data=payload, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=10).read()
```

Every alert body must be prefixed with `[SYN/heartbeat]` (the helper above does this). Never call the OpenClaw `message` tool with channel=Telegram — use the urllib pattern above.

---

## Step 1 — Load alert state

```python
import json, os
from datetime import datetime, timezone, timedelta

STATE = "/root/.openclaw/workspace/competition/heartbeat_syn_state.json"
now = datetime.now(timezone.utc)

if os.path.exists(STATE):
    state = json.load(open(STATE))
else:
    state = {"alerted": {}, "pending": {}}
state.setdefault("pending", {})  # tracks first-seen time for must-persist checks

def already_alerted(key):
    ts = state["alerted"].get(key)
    if not ts:
        return False
    return now - datetime.fromisoformat(ts) < timedelta(hours=24)

def mark_alerted(key):
    state["alerted"][key] = now.isoformat()
    state["pending"].pop(key, None)

def must_persist(key, min_minutes):
    """Return True only if this key has been failing for >= min_minutes.
    Suppresses single-cycle blips that auto-recover before next heartbeat."""
    first_seen = state["pending"].get(key)
    if not first_seen:
        state["pending"][key] = now.isoformat()
        return False
    return now - datetime.fromisoformat(first_seen) >= timedelta(minutes=min_minutes)

def clear_pending(key):
    state["pending"].pop(key, None)

def save_state():
    json.dump(state, open(STATE, "w"), indent=2)
```

---

## Step 2 — Run checks, collect new problems only

### Pending Alerts (always report — these are one-shot)
```bash
ls /root/.openclaw/workspace/alerts/pending_*.txt 2>/dev/null
```
- If any exist: read each, send contents to Telegram, delete the file. No cooldown needed — each file is unique.

### Day Trading Tick Health (must persist 60+ min)
```bash
stat /root/.openclaw/workspace/competition/leaderboard.json
```
- If modified >15 min ago AND a sprint is active: candidate problem key = `day_tick_stale`
- **Only alert if `must_persist('day_tick_stale', 60)` returns True.** This silences single-cycle blips that recover by next heartbeat. If the file is fresh, call `clear_pending('day_tick_stale')`.
- When alerting, include `tail -10 /root/.openclaw/workspace/competition/cron.log` for context.

### Swing Trading Tick Health (must persist 90+ min — already long-window, no extra delay)
```bash
stat /root/.openclaw/workspace/competition/swing/swing_leaderboard.json
```
- If modified >90 min ago AND a sprint is active: problem key = `swing_tick_stale` — alert immediately (90min already exceeds blip window).

### Active Day Sprint
```bash
ls /root/.openclaw/workspace/competition/active/
```
- Between 13:00–13:00 UTC a sprint should always be active. If empty: problem key = `day_no_sprint`
- Auto-fix first: `python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 24`
- Then alert Chris that you restarted it

### Sprint End Detection
```python
import json, os
from datetime import datetime, timezone, timedelta
d = '/root/.openclaw/workspace/competition/active'
entries = sorted(os.listdir(d)) if os.path.isdir(d) else []
if entries:
    meta = json.load(open(f'{d}/{entries[-1]}/meta.json'))
    started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
    ends = started + timedelta(hours=meta['duration_hours'])
    if datetime.now(timezone.utc) > ends:
        print(f'EXPIRED: {entries[-1]}')
```
- If expired: score and archive it (no alert needed — routine)
  ```bash
  python3 /root/.openclaw/skills/competition-score/scripts/competition_score.py <comp_id> --archive
  python3 /root/.openclaw/workspace/leaderboard.py --json
  python3 /root/.openclaw/workspace/dashboard_data.py
  ```

---

## Step 3 — Send alerts for new problems only

For each problem found:
```python
if not already_alerted("problem_key"):
    tg_send("<problem body>")  # uses helper above with [SYN/heartbeat] prefix and numeric chat_id
    mark_alerted("problem_key")

save_state()
```

If no new problems: reply HEARTBEAT_OK. No Telegram. Done.
