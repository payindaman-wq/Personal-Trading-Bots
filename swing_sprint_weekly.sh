#!/bin/bash
# swing_sprint_weekly.sh - Start a 7-day swing sprint every Sunday at 10:00 UTC (2:00 AM PST).
# Reads swing_cycle_state.json: pauses after sprints_per_cycle, alerts Telegram.

WORKSPACE="/root/.openclaw/workspace"
CYCLE_STATE="$WORKSPACE/competition/swing/swing_cycle_state.json"
ACTIVE_DIR="$WORKSPACE/competition/swing/active"
BOT_TOKEN="8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID="8154505910"
LOG="$WORKSPACE/competition.log"
COMP_START="$WORKSPACE/swing_competition_start.py"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [SWING] $1" | tee -a "$LOG"
}

tg_send() {
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"$1\", \"parse_mode\": \"Markdown\"}" \
        > /dev/null
}

# --- Read cycle state ---
CYCLE=$(python3 -c "import json; d=json.load(open()); print(d[cycle])")
SPRINT_IN_CYCLE=$(python3 -c "import json; d=json.load(open()); print(d[sprint_in_cycle])")
SPRINTS_PER_CYCLE=$(python3 -c "import json; d=json.load(open()); print(d[sprints_per_cycle])")
STATUS=$(python3 -c "import json; d=json.load(open()); print(d[status])")

# --- Paused for review ---
if [ "$STATUS" = "awaiting_review" ]; then
    log "Cycle $CYCLE awaiting strategy review. No sprint started."
    exit 0
fi

# --- Cycle complete ---
if [ "$SPRINT_IN_CYCLE" -ge "$SPRINTS_PER_CYCLE" ]; then
    log "Swing Cycle $CYCLE complete ($SPRINT_IN_CYCLE/$SPRINTS_PER_CYCLE). Pausing for review."
    python3 -c "
import json
with open() as f:
    s = json.load(f)
s[status] = awaiting_review
with open(, w) as f:
    json.dump(s, f, indent=2)
"
    tg_send "*Swing Cycle ${CYCLE} complete* — all ${SPRINTS_PER_CYCLE} sprints finished. Review standings and adjust non-profitable bot strategies, then run: python3 $WORKSPACE/swing_cycle_advance.py"
    log "Telegram alert sent. Swing Cycle $CYCLE paused."
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
log "Starting Swing Cycle $CYCLE, Sprint $NEXT_SPRINT of $SPRINTS_PER_CYCLE..."

RESULT=$(python3 "$COMP_START" 168 --cycle "$CYCLE" --sprint-in-cycle "$NEXT_SPRINT" 2>>"$LOG")
if [ $? -ne 0 ]; then
    log "ERROR: swing_competition_start.py failed."
    exit 1
fi

COMP_ID=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)[comp_id])")
log "Started: $COMP_ID (Swing Cycle $CYCLE, Sprint $NEXT_SPRINT/$SPRINTS_PER_CYCLE)"

# --- Update cycle state ---
python3 - << PYEOF
import json
from datetime import datetime, timezone
with open() as f:
    state = json.load(f)
state[sprint_in_cycle] = $NEXT_SPRINT
if state[cycle_started_at] is None:
    state[cycle_started_at] = datetime.now(timezone.utc).isoformat()
state[sprints].append()
with open(, w) as f:
    json.dump(state, f, indent=2)
PYEOF

log "Swing cycle state updated: sprint_in_cycle=$NEXT_SPRINT"
