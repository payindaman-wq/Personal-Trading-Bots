# HEARTBEAT.md - Periodic Checks

## Send Pending Trading Alerts
Check for pending alerts written by the monitoring cron job and send them to Telegram.
- Directory: `/root/.openclaw/workspace/alerts/`
- Pattern: `pending_*.txt`
- Action: Read each file, send to Telegram, delete the file
- Frequency: Every heartbeat (runs every ~30 minutes alongside cron checks)
