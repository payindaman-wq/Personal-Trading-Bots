#!/bin/bash
# Test AIzaSyCdVM key for Swing researcher and switch if working

KEY="AIzaSyCdVM-Q611QKvSTPz5MMS2F0xdS5TLk1Z0"
LOG="/root/.openclaw/workspace/retry_swing_key.log"

echo "[$(date -u)] Testing key AIzaSyCdVM... for Swing" >> "$LOG"

RESULT=$(curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=$KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"say hi"}]}]}' 2>&1)

if echo "$RESULT" | grep -q '"candidates"'; then
    echo "[$(date -u)] Key works — switching Swing to AIzaSyCdVM" >> "$LOG"
    python3 -c "
import json
with open('/root/.openclaw/secrets/gemini.json') as f:
    d = json.load(f)
d['gemini_swing_key'] = '$KEY'
with open('/root/.openclaw/secrets/gemini.json', 'w') as f:
    json.dump(d, f, indent=2)
print('gemini_swing_key updated')
" >> "$LOG" 2>&1
    systemctl restart volva_swing.service
    echo "[$(date -u)] volva_swing.service restarted with new key" >> "$LOG"
else
    echo "[$(date -u)] Key still failing — keeping current key. Response: $RESULT" >> "$LOG"
fi
