#!/bin/bash
# sprint_daily.sh - Start a 24h competition sprint daily. Self-removes after END_DATE.

END_DATE="2026-03-31"
TODAY=$(date -u +%Y-%m-%d)

if [[ "$TODAY" > "$END_DATE" ]]; then
    echo "[$TODAY] 20-day sprint series complete. Removing daily cron entry."
    crontab -l | grep -v "sprint_daily.sh" | crontab -
    exit 0
fi

DAY_NUM=$(( ( $(date -u +%s) - $(date -u -d "2026-03-09" +%s) ) / 86400 + 1 ))
echo "[$TODAY 13:00 UTC] Starting 24h sprint (day ${DAY_NUM} of 20)..."
python3 /root/.openclaw/skills/competition-start/scripts/competition_start.py 24 >> /root/.openclaw/workspace/competition.log 2>&1
