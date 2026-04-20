#!/usr/bin/env python3
"""
gemini_health.py — Gemini API health monitor (SYN/gemini_health).

Runs every 15 min via cron. Mirrors anthropic_health.py pattern.
Probe call to gemini-2.5-flash-lite -> alerts on 4xx/5xx/URLError.
Honors per-key cooldown so we don't spam Telegram.

ODIN calls Gemini inline in research/odin_researcher_v2.py; when Gemini
is down ODIN silently fails. This probe makes the failure visible.
"""
import json, os, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
SECRET_PATH = "/root/.openclaw/secrets/gemini.json"
STATE_FILE = f"{WORKSPACE}/competition/gemini_health_state.json"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"

PROBE_MODEL = "gemini-2.5-flash-lite"
PROBE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{PROBE_MODEL}:generateContent"

COOLDOWN_MIN = 360


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_alerted": {}}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)


def should_alert(state, key):
    last = state["last_alerted"].get(key)
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return True
    return datetime.now(timezone.utc) - last_dt > timedelta(minutes=COOLDOWN_MIN)


def mark_alerted(state, key):
    state["last_alerted"][key] = datetime.now(timezone.utc).isoformat()


def tg_send(msg, severity="error"):
    """Write to SYN inbox. sys_heartbeat is the sole Telegram gateway."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "gemini_health",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[gemini_health/inbox] {e}")


def load_api_key():
    with open(SECRET_PATH) as f:
        return json.load(f)["gemini_api_key"]


def probe(api_key):
    url = f"{PROBE_URL}?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": "hi"}]}],
        "generationConfig": {"maxOutputTokens": 1, "temperature": 0.0},
    }).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return {"ok": True, "status": r.status}
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()[:300]
        except Exception:
            err_body = ""
        return {"ok": False, "status": e.code, "error": err_body}
    except urllib.error.URLError as e:
        return {"ok": False, "status": None, "error": f"URLError: {e.reason}"}
    except Exception as e:
        return {"ok": False, "status": None, "error": f"{type(e).__name__}: {e}"}


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def main():
    state = load_state()
    try:
        api_key = load_api_key()
    except Exception as e:
        if should_alert(state, "auth_load_fail"):
            tg_send(f"<b>SYN: Gemini API secret unreadable</b>\nTime: {pst_now()}\nError: {e}")
            mark_alerted(state, "auth_load_fail")
            save_state(state)
        return

    res = probe(api_key)
    if not res["ok"]:
        code = res.get("status")
        key = f"probe_fail_{code or 'net'}"
        if should_alert(state, key):
            tg_send(
                f"<b>SYN: Gemini API probe FAILED</b>\n"
                f"Time: {pst_now()}\n"
                f"Status: {code}\n"
                f"Detail: {str(res.get('error', ''))[:300]}\n"
                f"Impact: ODIN research may be stalled across all 4 leagues."
            )
            mark_alerted(state, key)
        save_state(state)
        print(f"[{pst_now()}] probe=FAIL status={code}")
        return

    save_state(state)
    print(f"[{pst_now()}] probe=OK status={res['status']}")


if __name__ == "__main__":
    main()
