#!/usr/bin/env bash
# Non-interactive reachability and config validation.
# Depends on config_loader.py at repo root.
# Expected interface:
#   python3 config_loader.py --validate       exits 0 if config.yaml is valid
#   python3 config_loader.py --get <key>      prints value to stdout

set -uo pipefail

PASS=0; WARN=0; FAIL=0

ok()   { echo "[GREEN]  $*"; PASS=$((PASS+1)); }
warn() { echo "[YELLOW] $*"; WARN=$((WARN+1)); }
fail() { echo "[RED]    $*"; FAIL=$((FAIL+1)); }

echo ""
echo "crypto-trading-toolkit sanity check"
echo "------------------------------------"

if [[ ! -f config_loader.py ]]; then
    fail "config_loader.py not found -- ensure it is present at repo root"
    exit 1
fi
if ! python3 config_loader.py --validate > /dev/null 2>&1; then
    fail "config.yaml is invalid or missing -- run ./scripts/setup.sh first"
    exit 1
fi
ok "config.yaml valid (config_version: $(python3 config_loader.py --get config_version))"

get() { python3 config_loader.py --get "$1" 2>/dev/null; }

ANTHROPIC_KEY=$(get anthropic_api_key)
GEMINI_KEY=$(get gemini_api_key)
KRAKEN_KEY=$(get kraken_api_key)
KRAKEN_SECRET=$(get kraken_api_secret)
TG_TOKEN=$(get telegram_bot_token)
TG_CHAT=$(get telegram_chat_id)
VPS_HOST=$(get vps_host)

echo ""
echo "Testing Anthropic..."
ANTHROPIC_RESULT=$(python3 - <<PYEOF
import anthropic
try:
    client = anthropic.Anthropic(api_key="$ANTHROPIC_KEY")
    client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1,
        messages=[{"role": "user", "content": "hi"}]
    )
    print("ok")
except Exception as e:
    print(f"error: {e}")
PYEOF
)
if [[ "$ANTHROPIC_RESULT" == "ok" ]]; then
    ok "Anthropic API reachable"
else
    fail "Anthropic API: $ANTHROPIC_RESULT"
fi

echo "Testing Gemini..."
GEMINI_RESULT=$(python3 - <<PYEOF
import urllib.request, urllib.error, json
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=$GEMINI_KEY"
body = json.dumps({"contents": [{"parts": [{"text": "hi"}]}], "generationConfig": {"maxOutputTokens": 1}}).encode()
try:
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)
    print("ok")
except urllib.error.HTTPError as e:
    print(f"http {e.code}: {e.reason}")
except Exception as e:
    print(f"error: {e}")
PYEOF
)
if [[ "$GEMINI_RESULT" == "ok" ]]; then
    ok "Gemini API reachable"
else
    fail "Gemini API: $GEMINI_RESULT"
fi

if [[ -n "$KRAKEN_KEY" && -n "$KRAKEN_SECRET" ]]; then
    echo "Testing Kraken..."
    KRAKEN_RESULT=$(python3 - <<PYEOF
import urllib.request, urllib.parse, hashlib, hmac, base64, time, json
key = "$KRAKEN_KEY"
secret = "$KRAKEN_SECRET"
nonce = str(int(time.time() * 1000))
data = urllib.parse.urlencode({"nonce": nonce})
path = "/0/private/Balance"
msg = (nonce + data).encode()
mac = hmac.new(base64.b64decode(secret), path.encode() + hashlib.sha256(msg).digest(), hashlib.sha512)
sig = base64.b64encode(mac.digest()).decode()
req = urllib.request.Request(
    "https://api.kraken.com" + path,
    data=data.encode(),
    headers={"API-Key": key, "API-Sign": sig}
)
try:
    res = json.loads(urllib.request.urlopen(req, timeout=10).read())
    if res.get("error"):
        print("api error: " + str(res["error"]))
    else:
        print("ok")
except Exception as e:
    print(f"error: {e}")
PYEOF
    )
    if [[ "$KRAKEN_RESULT" == "ok" ]]; then
        ok "Kraken API reachable and credentials valid"
    else
        fail "Kraken API: $KRAKEN_RESULT"
    fi
else
    warn "Kraken credentials not configured -- skipping"
fi

if [[ -n "$TG_TOKEN" && -n "$TG_CHAT" ]]; then
    echo "Testing Telegram..."
    TG_RESULT=$(python3 - <<PYEOF
import urllib.request, json
token = "$TG_TOKEN"
chat  = "$TG_CHAT"
url   = f"https://api.telegram.org/bot{token}/sendMessage"
body  = json.dumps({"chat_id": chat, "text": "[setup] sanity_check.sh: setup verified"}).encode()
try:
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=10).read())
    print("ok" if res.get("ok") else f"api error: {res}")
except Exception as e:
    print(f"error: {e}")
PYEOF
    )
    if [[ "$TG_RESULT" == "ok" ]]; then
        ok "Telegram bot reachable -- test message sent"
    else
        fail "Telegram: $TG_RESULT"
    fi
else
    warn "Telegram not configured -- skipping"
fi

if [[ -n "$VPS_HOST" ]]; then
    echo "Testing SSH to $VPS_HOST..."
    if ssh -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$VPS_HOST" "exit 0" 2>/dev/null; then
        ok "SSH to $VPS_HOST reachable"
    else
        fail "SSH to $VPS_HOST failed -- check key auth and host"
    fi
else
    warn "vps_host not set -- skipping SSH test"
fi

echo ""
echo "------------------------------------"
echo "Results: ${PASS} GREEN  ${WARN} YELLOW  ${FAIL} RED"
if [[ $FAIL -gt 0 ]]; then
    echo "One or more checks failed. Fix the issues above before deploying."
    exit 1
elif [[ $WARN -gt 0 ]]; then
    echo "All required checks passed. Optional integrations skipped."
    exit 0
else
    echo "All checks passed."
    exit 0
fi
