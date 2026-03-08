---
name: competition-schedule
description: Schedule the next competition sprint to start at a specific time. Accepts natural language like "Monday 5am PST" or "tomorrow 9am PST". Also supports listing or cancelling scheduled sprints. Use this when the user asks to schedule, plan, or time the next competition.
---

# competition-schedule

Schedules a future competition sprint by adding a one-time cron entry on the server.
Accepts natural language time expressions in PST.

## Usage

```bash
# Schedule a 4-hour sprint for Monday at 5am PST
python3 /root/.openclaw/skills/competition-schedule/scripts/competition_schedule.py "Monday 5am PST"

# Schedule a 6-hour sprint for tomorrow at 9am PST
python3 /root/.openclaw/skills/competition-schedule/scripts/competition_schedule.py "tomorrow 9am PST" --hours 6

# List currently scheduled sprints
python3 /root/.openclaw/skills/competition-schedule/scripts/competition_schedule.py --list

# Cancel all scheduled sprints
python3 /root/.openclaw/skills/competition-schedule/scripts/competition_schedule.py --cancel
```

## Notes

- PST = UTC-8 (no DST adjustment — crypto runs 24/7, we use fixed offset)
- Replaces any previously scheduled sprint (only one can be queued at a time)
- Default duration is 4 hours
- Best windows for active trading: 5am-1pm PST (US session overlap)
- Dead zone to avoid: 8pm-2am PST Saturday/Sunday (lowest crypto volume)

## After Scheduling

Confirm with:
```bash
crontab -l
```
