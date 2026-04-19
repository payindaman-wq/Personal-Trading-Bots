#!/usr/bin/env python3
"""
anthropic_health.py — Claude API health + quota + spend monitor.

Runs every 15 min via cron. Actions:
  1. Probe call (max_tokens=1) -> reads anthropic-ratelimit-* response headers.
     Alerts on 401/429/529, or if remaining % < LOW_THRESHOLD_PCT.
  2. Reads research/anthropic_usage.jsonl, sums today's input+output tokens
     across known models, estimates $ spend. Alerts if > DAILY_BUDGET_USD.
Alerts honor a per-key cooldown so we don't spam Telegram.
"""
import json, os, urllib.request, urllib.error, ssl
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")
WORKSPACE = "/root/.openclaw/workspace"
SECRET_PATH = "/root/.openclaw/secrets/anthropic.json"
USAGE_LOG = f"{WORKSPACE}/research/anthropic_usage.jsonl"
STATE_FILE = f"{WORKSPACE}/competition/anthropic_health_state.json"

BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID = "8154505910"

PROBE_MODEL = "claude-haiku-4-5-20251001"
PROBE_URL = "https://api.anthropic.com/v1/messages"

LOW_THRESHOLD_PCT = 10.0
DAILY_BUDGET_USD = 10.0
COOLDOWN_MIN = 360

MODEL_PRICING = {
    "claude-sonnet-4-6":       {"in": 3.0,  "out": 15.0},
    "claude-sonnet-4-5":       {"in": 3.0,  "out": 15.0},
    "claude-opus-4-7":         {"in": 15.0, "out": 75.0},
    "claude-opus-4-6":         {"in": 15.0, "out": 75.0},
    "claude-haiku-4-5-20251001": {"in": 1.0, "out": 5.0},
    "claude-haiku-4-5":        {"in": 1.0,  "out": 5.0},
}


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


INBOX = "/root/.openclaw/workspace/syn_inbox.jsonl"


def tg_send(msg, severity="error"):
    """Write to SYN inbox. sys_heartbeat is the sole Telegram gateway."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "anthropic_health",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[anthropic_health/inbox] {e}")


def load_api_key():
    with open(SECRET_PATH) as f:
        return json.load(f)["anthropic_api_key"]


def probe(api_key):
    payload = json.dumps({
        "model": PROBE_MODEL,
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "hi"}],
    }).encode()
    req = urllib.request.Request(
        PROBE_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            headers = dict(r.headers)
            body = json.loads(r.read().decode())
            return {"ok": True, "status": r.status, "headers": headers, "body": body}
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()[:300]
        except Exception:
            err_body = ""
        return {"ok": False, "status": e.code, "headers": dict(e.headers or {}), "error": err_body}
    except urllib.error.URLError as e:
        return {"ok": False, "status": None, "error": f"URLError: {e.reason}"}
    except Exception as e:
        return {"ok": False, "status": None, "error": f"{type(e).__name__}: {e}"}


def pct(remaining, limit):
    try:
        r = float(remaining)
        l = float(limit)
        if l <= 0:
            return None
        return 100.0 * r / l
    except (TypeError, ValueError):
        return None


def check_rate_limits(headers):
    """Return list of (bucket, pct) where remaining% < LOW_THRESHOLD_PCT."""
    buckets = [
        ("requests", "anthropic-ratelimit-requests-remaining", "anthropic-ratelimit-requests-limit"),
        ("input_tokens", "anthropic-ratelimit-input-tokens-remaining", "anthropic-ratelimit-input-tokens-limit"),
        ("output_tokens", "anthropic-ratelimit-output-tokens-remaining", "anthropic-ratelimit-output-tokens-limit"),
    ]
    low = []
    for name, rem_key, lim_key in buckets:
        p = pct(headers.get(rem_key), headers.get(lim_key))
        if p is not None and p < LOW_THRESHOLD_PCT:
            low.append((name, p, headers.get(rem_key), headers.get(lim_key)))
    return low


def today_spend_utc():
    """Sum today's (UTC date) token usage from usage log and estimate cost."""
    if not os.path.isfile(USAGE_LOG):
        return {"input": 0, "output": 0, "cost_usd": 0.0, "calls": 0, "unknown_models": set()}
    today = datetime.now(timezone.utc).date().isoformat()
    totals = {"input": 0, "output": 0, "cost_usd": 0.0, "calls": 0, "unknown_models": set()}
    try:
        with open(USAGE_LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                ts = rec.get("ts", "")
                if not ts.startswith(today):
                    continue
                model = rec.get("model", "")
                ip = int(rec.get("input_tokens") or 0)
                op = int(rec.get("output_tokens") or 0)
                price = MODEL_PRICING.get(model)
                if price is None:
                    totals["unknown_models"].add(model)
                    price = {"in": 3.0, "out": 15.0}
                totals["input"] += ip
                totals["output"] += op
                totals["cost_usd"] += (ip / 1_000_000.0) * price["in"] + (op / 1_000_000.0) * price["out"]
                totals["calls"] += 1
    except Exception as e:
        print(f"[usage] {e}")
    return totals


def pst_now():
    return datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")


def main():
    state = load_state()
    try:
        api_key = load_api_key()
    except Exception as e:
        if should_alert(state, "auth_load_fail"):
            tg_send(f"<b>SYN: Claude API secret unreadable</b>\nTime: {pst_now()}\nError: {e}")
            mark_alerted(state, "auth_load_fail")
            save_state(state)
        return

    res = probe(api_key)
    if not res["ok"]:
        code = res.get("status")
        key = f"probe_fail_{code or 'net'}"
        if should_alert(state, key):
            tg_send(
                f"<b>SYN: Claude API probe FAILED</b>\n"
                f"Time: {pst_now()}\n"
                f"Status: {code}\n"
                f"Detail: {str(res.get('error', ''))[:300]}"
            )
            mark_alerted(state, key)
        save_state(state)
        return

    headers = res["headers"]
    low_buckets = check_rate_limits(headers)
    if low_buckets:
        key = "rate_limit_low"
        if should_alert(state, key):
            lines = [f"{n}: {r}/{l} ({p:.1f}%)" for (n, p, r, l) in low_buckets]
            tg_send(
                f"<b>SYN: Claude rate limit low</b>\n"
                f"Time: {pst_now()}\n" + "\n".join(lines),
                severity="warning",  # dashboard only; not urgent
            )
            mark_alerted(state, key)

    spend = today_spend_utc()
    if spend["cost_usd"] > DAILY_BUDGET_USD:
        key = f"budget_over_{datetime.now(timezone.utc).date().isoformat()}"
        if should_alert(state, key):
            unk = f" (unknown models: {', '.join(spend['unknown_models'])})" if spend["unknown_models"] else ""
            tg_send(
                f"<b>SYN: Claude daily spend over budget</b>\n"
                f"Time: {pst_now()}\n"
                f"Today: ${spend['cost_usd']:.2f} (budget ${DAILY_BUDGET_USD:.2f})\n"
                f"Tokens: {spend['input']:,} in / {spend['output']:,} out across {spend['calls']} calls{unk}"
            )
            mark_alerted(state, key)

    save_state(state)
    print(
        f"[{pst_now()}] probe=OK "
        f"req_rem={headers.get('anthropic-ratelimit-requests-remaining')} "
        f"in_rem={headers.get('anthropic-ratelimit-input-tokens-remaining')} "
        f"out_rem={headers.get('anthropic-ratelimit-output-tokens-remaining')} "
        f"today=${spend['cost_usd']:.3f} ({spend['calls']} calls)"
    )


if __name__ == "__main__":
    main()
