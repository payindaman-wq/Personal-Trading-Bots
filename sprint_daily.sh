#!/bin/bash
# sprint_daily.sh - Start a daily 24h competition sprint.
# Runs at 10:10 UTC (2:10 AM PST) via cron — 10-min offset lets the tick
# archive the previous sprint before this script fires.
# Tracks cycle state: 7 sprints per cycle, then pauses for strategy review.

WORKSPACE="/root/.openclaw/workspace"
CYCLE_STATE="$WORKSPACE/competition/cycle_state.json"
ACTIVE_DIR="$WORKSPACE/competition/active"
BOT_TOKEN="8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID="8154505910"
LOG="$WORKSPACE/competition.log"
COMP_START="/root/.openclaw/skills/competition-start/scripts/competition_start.py"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1" | tee -a "$LOG"
}

tg_send() {
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"$1\", \"parse_mode\": \"Markdown\"}" \
        > /dev/null
}

# --- Read cycle state ---
CYCLE=$(python3 -c "import json; d=json.load(open('$CYCLE_STATE')); print(d['cycle'])")
SPRINT_IN_CYCLE=$(python3 -c "import json; d=json.load(open('$CYCLE_STATE')); print(d['sprint_in_cycle'])")
SPRINTS_PER_CYCLE=$(python3 -c "import json; d=json.load(open('$CYCLE_STATE')); print(d['sprints_per_cycle'])")
STATUS=$(python3 -c "import json; d=json.load(open('$CYCLE_STATE')); print(d['status'])")

# --- Paused for review ---
if [ "$STATUS" = "awaiting_review" ]; then
    log "Cycle $CYCLE is awaiting strategy review. No sprint started."
    exit 0
fi

# --- Cycle complete ---
if [ "$SPRINT_IN_CYCLE" -ge "$SPRINTS_PER_CYCLE" ]; then
    log "Cycle $CYCLE complete ($SPRINT_IN_CYCLE/$SPRINTS_PER_CYCLE). Pausing for review."
    python3 -c "
import json
with open('$CYCLE_STATE') as f:
    s = json.load(f)
s['status'] = 'awaiting_review'
with open('$CYCLE_STATE', 'w') as f:
    json.dump(s, f, indent=2)
"
    tg_send "*Day Trading Cycle ${CYCLE} complete* — all ${SPRINTS_PER_CYCLE} sprints finished. Review standings and adjust strategies, then run: python3 $WORKSPACE/cycle_advance.py"
    log "Telegram alert sent. Cycle $CYCLE paused."
    exit 0
fi

# --- Guard: skip if a sprint is already active ---
ACTIVE_COUNT=$(ls "$ACTIVE_DIR" 2>/dev/null | wc -l)
if [ "$ACTIVE_COUNT" -gt "0" ]; then
    ACTIVE_ID=$(ls "$ACTIVE_DIR" | tail -1)
    log "Active sprint already running: $ACTIVE_ID — skipping start."
    exit 0
fi

# --- Start next sprint ---
NEXT_SPRINT=$(( SPRINT_IN_CYCLE + 1 ))
log "Starting Cycle $CYCLE, Sprint $NEXT_SPRINT of $SPRINTS_PER_CYCLE..."

RESULT=$(python3 "$COMP_START" 24 --cycle "$CYCLE" --sprint-in-cycle "$NEXT_SPRINT" 2>>"$LOG")
if [ $? -ne 0 ]; then
    log "ERROR: competition_start.py failed."
    exit 1
fi

COMP_ID=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['comp_id'])")
log "Started: $COMP_ID (Cycle $CYCLE, Sprint $NEXT_SPRINT/$SPRINTS_PER_CYCLE)"

# --- Update cycle state ---
python3 -c "
import json
from datetime import datetime, timezone
with open('$CYCLE_STATE') as f:
    state = json.load(f)
state['sprint_in_cycle'] = $NEXT_SPRINT
if state['cycle_started_at'] is None:
    state['cycle_started_at'] = datetime.now(timezone.utc).isoformat()
state['sprints'].append('$COMP_ID')
with open('$CYCLE_STATE', 'w') as f:
    json.dump(state, f, indent=2)
"

log "Cycle state updated: sprint_in_cycle=$NEXT_SPRINT"
