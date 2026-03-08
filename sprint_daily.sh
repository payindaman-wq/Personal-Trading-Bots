#!/bin/bash
# sprint_daily.sh - Run daily competition sprint, self-stop after END_DATE.

END_DATE="2026-03-28"
TODAY=$(date -u +%Y-%m-%d)

if [[ "$TODAY" > "$END_DATE" ]]; then
    echo "[$TODAY] 20-day sprint series complete. Removing daily cron entry."
    # Remove this cron entry
    crontab -l | grep -v "sprint_daily.sh" | crontab -
    exit 0
fi

echo "[$TODAY] Starting 8-hour sprint (day $(($(( $(date -u +%s) - $(date -u -d "2026-03-09" +%s) )) / 86400 + 1)) of 20)..."
python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 8 >> /root/.openclaw/workspace/competition.log 2>&1
