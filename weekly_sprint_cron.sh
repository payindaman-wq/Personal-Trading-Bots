#!/bin/bash
# weekly_sprint_cron.sh - Sunday 10:00 UTC (2:00 AM PST)
# Starts next Swing and Polymarket sprints, sends ONE combined Telegram summary.

WORKSPACE="/root/.openclaw/workspace"
BOT_TOKEN=$(python3 -c "import sys; sys.path.insert(0, '$WORKSPACE'); from config_loader import config; print(config.telegram.bot_token)")
CHAT_ID=$(python3 -c "import sys; sys.path.insert(0, '$WORKSPACE'); from config_loader import config; print(config.telegram.chat_id)")
LOG="$WORKSPACE/competition.log"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [WEEKLY] $1" | tee -a "$LOG"
}

tg_send() {
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"$1\", \"parse_mode\": \"Markdown\"}" \
        > /dev/null
}

log "=== Weekly sprint cron starting ==="

# ── Day Trading: read current state (no action, just report) ──────────────
DAY_MSG=$(python3 - << PYEOF
import json, os
lb_path = "$WORKSPACE/competition/leaderboard.json"
cs_path = "$WORKSPACE/competition/cycle_state.json"
try:
    lb = json.load(open(lb_path))
    cs = json.load(open(cs_path))
    cycle   = cs.get("cycle", "?")
    sprint  = cs.get("sprint_in_cycle", 0)
    per     = cs.get("sprints_per_cycle", 7)
    status  = cs.get("status", "active")
    if status == "awaiting_review":
        state_str = "CYCLE COMPLETE - awaiting review"
    else:
        state_str = f"Sprint {sprint}/{per}"
    rankings = lb.get("rankings", [])
    if rankings:
        top = rankings[0]
        leader = f"{top[bot].title()} {+ if top[cumulative_pnl_usd] >= 0 else }\${top[cumulative_pnl_usd]:.2f}"
    else:
        leader = "no data yet"
    print(f"*Day Trading — Cycle {cycle}, {state_str}*\nLeader: {leader}")
except Exception as e:
    print(f"*Day Trading* — data unavailable ({e})")
PYEOF
)

# ── Swing: start next sprint if eligible ─────────────────────────────────
SWING_CS="$WORKSPACE/competition/swing/swing_cycle_state.json"
SWING_ACTIVE="$WORKSPACE/competition/swing/active"

SWING_CYCLE=$(python3 -c "import json; d=json.load(open()); print(d[cycle])")
SWING_SPRINT=$(python3 -c "import json; d=json.load(open()); print(d[sprint_in_cycle])")
SWING_PER=$(python3 -c "import json; d=json.load(open()); print(d[sprints_per_cycle])")
SWING_STATUS=$(python3 -c "import json; d=json.load(open()); print(d[status])")

if [ "$SWING_STATUS" = "awaiting_review" ]; then
    SWING_MSG="*Swing — Cycle ${SWING_CYCLE}, COMPLETE (${SWING_SPRINT}/${SWING_PER} sprints)*
Awaiting strategy review. Run: python3 $WORKSPACE/swing_cycle_advance.py"
    log "Swing Cycle $SWING_CYCLE awaiting review — skipped."
elif [ "$SWING_SPRINT" -ge "$SWING_PER" ]; then
    python3 -c "
import json
with open() as f: s=json.load(f)
s[status]=awaiting_review
with open(,w) as f: json.dump(s,f,indent=2)
"
    SWING_MSG="*Swing — Cycle ${SWING_CYCLE} COMPLETE (${SWING_SPRINT}/${SWING_PER} sprints)*
All sprints done. Adjust strategies then run: python3 $WORKSPACE/swing_cycle_advance.py"
    log "Swing Cycle $SWING_CYCLE complete — paused."
elif [ "$(ls $SWING_ACTIVE 2>/dev/null | wc -l)" -gt "0" ]; then
    ACTIVE_ID=$(ls "$SWING_ACTIVE" | tail -1)
    SWING_MSG="*Swing — Cycle ${SWING_CYCLE}, Sprint ${SWING_SPRINT}/${SWING_PER}*
Sprint still active: ${ACTIVE_ID}"
    log "Swing sprint already active: $ACTIVE_ID — skipped."
else
    NEXT_SPRINT=$(( SWING_SPRINT + 1 ))
    RESULT=$(python3 "$WORKSPACE/swing_competition_start.py" 168 --cycle "$SWING_CYCLE" --sprint-in-cycle "$NEXT_SPRINT" 2>>"$LOG")
    if [ $? -eq 0 ]; then
        COMP_ID=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)[comp_id])")
        python3 - << PYEOF
import json
from datetime import datetime, timezone
with open() as f: state=json.load(f)
state[sprint_in_cycle] = $NEXT_SPRINT
if state[cycle_started_at] is None:
    state[cycle_started_at] = datetime.now(timezone.utc).isoformat()
state.setdefault(sprints,[]).append()
with open(,w) as f: json.dump(state,f,indent=2)
PYEOF
        SWING_MSG="*Swing — Cycle ${SWING_CYCLE}, Sprint ${NEXT_SPRINT}/${SWING_PER} started*
Sprint ID: ${COMP_ID} (7 days)"
        log "Swing sprint started: $COMP_ID"
    else
        SWING_MSG="*Swing — ERROR starting sprint* Check $LOG"
        log "ERROR: swing_competition_start.py failed"
    fi
fi

# ── Polymarket: start next sprint if eligible ─────────────────────────────
POLY_CS="$WORKSPACE/competition/polymarket/polymarket_cycle_state.json"

POLY_CYCLE=$(python3 -c "import json; d=json.load(open()); print(d[cycle])")
POLY_SPRINT=$(python3 -c "import json; d=json.load(open()); print(d[sprint_in_cycle])")
POLY_PER=$(python3 -c "import json; d=json.load(open()); print(d[sprints_per_cycle])")
POLY_STATUS=$(python3 -c "import json; d=json.load(open()); print(d[status])")
POLY_AUTO_STATUS=$(python3 -c "import json; d=json.load(open(/competition/polymarket/auto_state.json)); print(d.get(status,active))")

if [ "$POLY_STATUS" = "awaiting_review" ]; then
    POLY_MSG="*Polymarket — Cycle ${POLY_CYCLE}, COMPLETE (${POLY_SPRINT}/${POLY_PER} sprints)*
Awaiting strategy review. Run: python3 $WORKSPACE/polymarket_cycle_advance.py"
    log "Polymarket Cycle $POLY_CYCLE awaiting review — skipped."
elif [ "$POLY_AUTO_STATUS" = "active" ]; then
    POLY_MSG="*Polymarket — Cycle ${POLY_CYCLE}, Sprint ${POLY_SPRINT}/${POLY_PER}*
Sprint still active — no action needed."
    log "Polymarket sprint still active — skipped."
else
    RESULT=$(python3 "$WORKSPACE/polymarket_sprint_start.py" 2>>"$LOG")
    if [ $? -eq 0 ]; then
        SPRINT_ID=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)[sprint_id])")
        NEXT_N=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)[sprint_in_cycle])")
        POLY_MSG="*Polymarket — Cycle ${POLY_CYCLE}, Sprint ${NEXT_N}/${POLY_PER} started*
Sprint ID: ${SPRINT_ID} (7 days)"
        log "Polymarket sprint started: $SPRINT_ID"
    else
        POLY_MSG="*Polymarket — ERROR starting sprint* Check $LOG"
        log "ERROR: polymarket_sprint_start.py failed"
    fi
fi

# ── Send one combined Telegram message ────────────────────────────────────
DATE_STR=$(date -u +"%b %-d, %Y")
FULL_MSG="*Weekly Fleet Update — ${DATE_STR}*

${DAY_MSG}

${SWING_MSG}

${POLY_MSG}"

# Telegram silenced — this script's python snippets are all syntactically
# broken (every open() and dict access was stripped of its arguments/quotes)
# so the message body is mostly empty placeholders. The actual weekly league
# restart happens in weekly_league_restart.py; no user-facing summary needed.
# tg_send "$FULL_MSG"
log "Combined weekly Telegram message: silenced (script body broken; replaced by weekly_league_restart.py)."
log "=== Weekly sprint cron done ==="
