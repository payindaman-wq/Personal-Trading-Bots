#!/usr/bin/env python3
"""
research_freshness.py — detects silent research staleness.

Runs hourly via cron. Alerts Telegram on:
  - ODIN per-league: gens_since_best over threshold (stuck evolution)
  - ODIN per-league: researcher.log mtime stale (process silent)
  - FREYA (pm): stall + freshness (same as ODIN)
  - MIMIR: log silent (no entry in N hours)
  - MIMIR: same BUG-N flagged in 3+ of last 5 analyses for a league
  - LOKI: cycle review missing or stale per league
  - TYR / HEIMDALL: log mtime stale

Dedup via freshness_state.json (24h cooldown per key, 48h for MIMIR escalations).
"""
import json, os, re, time, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone

WORKSPACE  = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/freshness_state.json"
BOT_TOKEN  = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID    = "8154505910"

COOLDOWN_MIN = 1440        # 24h
MIMIR_ESCALATION_COOLDOWN_MIN = 2880  # 48h

LEAGUES = ["day", "swing", "futures_day", "futures_swing"]
STALL_THRESH = 500         # gens_since_best threshold (applies to ODIN + FREYA)

LOG_STALE_MIN = {
    "odin":     30,   # researcher.log updates every ~10 min
    "pm":       30,   # freya same
    "mimir":    480,  # 8h — mimir only fires on gen%200 or breakthrough
    "loki":     60,   # cron every 15 min
    "tyr":      45,   # cron every 30 min
    "heimdall": 45,   # cron every 30 min
}

LOKI_STALE_DAYS = {  # per league: days since last cycle review
    "day": 2,
    "futures_day": 2,
    "swing": 10,
    "futures_swing": 10,
}

# Cycle-state paths so the freshness monitor can suppress false-positive
# "never_reviewed" alerts when a league is still within its first cycle.
CYCLE_STATE_PATHS = {
    "day":           f"{WORKSPACE}/competition/cycle_state.json",
    "swing":         f"{WORKSPACE}/competition/swing/swing_cycle_state.json",
    "futures_day":   f"{WORKSPACE}/competition/futures_day/cycle_state.json",
    "futures_swing": f"{WORKSPACE}/competition/futures_swing/cycle_state.json",
}
LOKI_REVIEW_LOG = f"{WORKSPACE}/research/loki_cycle_review_log.jsonl"


def _load_cycle_state(league):
    path = CYCLE_STATE_PATHS.get(league)
    if not path or not os.path.exists(path):
        return None
    try:
        return json.load(open(path))
    except Exception:
        return None


def _league_review_due(league):
    """Return True if LOKI was *expected* to have reviewed at least one cycle
    for this league by now. False suppresses 'never_reviewed' alerts when the
    league is still inside cycle 1 OR when prior cycles predated LOKI.
    """
    cs = _load_cycle_state(league)
    if cs is None:
        return False
    cycle = cs.get("cycle", 1)
    sprint_in_cycle = cs.get("sprint_in_cycle", 0)
    sprints_per_cycle = cs.get("sprints_per_cycle", 7)
    # Still inside the first cycle — no review due yet.
    if cycle == 1 and sprint_in_cycle < sprints_per_cycle:
        return False
    # For cycle > 1: only alert if the current cycle started AFTER LOKI's
    # review log was created (prior cycles may predate LOKI deployment).
    if cycle > 1 and os.path.exists(LOKI_REVIEW_LOG):
        log_mtime = os.path.getmtime(LOKI_REVIEW_LOG)
        cycle_started = cs.get("cycle_started_at", "")
        try:
            started_dt = datetime.fromisoformat(cycle_started.replace("Z", "+00:00"))
            started_epoch = started_dt.timestamp()
            return started_epoch > log_mtime
        except Exception:
            return True
    return True


def now_ts():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            return {}
    return {}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, indent=2)
    os.replace(tmp, STATE_FILE)


def should_alert(state, key, cooldown_min=COOLDOWN_MIN):
    last = state.get(key, {}).get("last_alerted")
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return True
    age_min = (datetime.now(timezone.utc) - last_dt).total_seconds() / 60
    return age_min >= cooldown_min


def record_alert(state, key, detail=""):
    state[key] = {"last_alerted": now_ts(), "detail": detail}


def telegram(msg):
    try:
        data = urllib.parse.urlencode({
            "chat_id": CHAT_ID,
            "text": msg,
            "disable_web_page_preview": "true",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=data, method="POST",
        )
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"[research_freshness] telegram send failed: {e}")
        return False


def mtime_age_min(path):
    if not os.path.exists(path):
        return None
    return (time.time() - os.path.getmtime(path)) / 60


# ── Check 1: ODIN per-league (stall + log freshness) ────────────────────────

def check_odin_leagues(state, alerts):
    for league in LEAGUES:
        d = f"{WORKSPACE}/research/{league}"
        gs_path = f"{d}/gen_state.json"
        log_path = f"{d}/researcher.log"

        if os.path.exists(gs_path):
            try:
                gs = json.load(open(gs_path))
                gsb = gs.get("gens_since_best", 0)
                gen = gs.get("gen", 0)
                if gsb >= STALL_THRESH:
                    key = f"odin_stall:{league}"
                    if should_alert(state, key):
                        alerts.append(
                            f"ODIN stalled [{league}]: {gsb} gens since last best "
                            f"(current gen {gen}, threshold {STALL_THRESH}). "
                            f"Inspect research/{league}/researcher.log + MIMIR guidance."
                        )
                        record_alert(state, key, f"gsb={gsb}")
            except Exception as e:
                alerts.append(f"research_freshness: failed to parse {gs_path}: {e}")

        age = mtime_age_min(log_path)
        if age is None:
            key = f"odin_log_missing:{league}"
            if should_alert(state, key):
                alerts.append(f"ODIN log missing [{league}]: {log_path} does not exist.")
                record_alert(state, key)
        elif age > LOG_STALE_MIN["odin"]:
            key = f"odin_log_stale:{league}"
            if should_alert(state, key):
                alerts.append(
                    f"ODIN log stale [{league}]: last updated {age:.0f} min ago "
                    f"(threshold {LOG_STALE_MIN['odin']} min). Service may be dead or hung."
                )
                record_alert(state, key, f"age_min={age:.0f}")


# ── Check 2: FREYA (pm) stall + freshness ───────────────────────────────────

def check_freya(state, alerts):
    gs_path = f"{WORKSPACE}/research/pm/gen_state.json"
    log_path = f"{WORKSPACE}/research/pm/researcher.log"

    if os.path.exists(gs_path):
        try:
            gs = json.load(open(gs_path))
            gsb = gs.get("gens_since_best", 0)
            gen = gs.get("gen", 0)
            if gsb >= STALL_THRESH:
                key = "freya_stall"
                if should_alert(state, key):
                    alerts.append(
                        f"FREYA stalled: {gsb} gens since last best (current gen {gen}, "
                        f"threshold {STALL_THRESH}). Consider wider price_range, different "
                        f"category, or force random_restart."
                    )
                    record_alert(state, key, f"gsb={gsb}")
        except Exception as e:
            alerts.append(f"research_freshness: failed to parse {gs_path}: {e}")

    age = mtime_age_min(log_path)
    if age is None:
        key = "freya_log_missing"
        if should_alert(state, key):
            alerts.append(f"FREYA log missing: {log_path} does not exist.")
            record_alert(state, key)
    elif age > LOG_STALE_MIN["pm"]:
        key = "freya_log_stale"
        if should_alert(state, key):
            alerts.append(
                f"FREYA log stale: last updated {age:.0f} min ago "
                f"(threshold {LOG_STALE_MIN['pm']} min)."
            )
            record_alert(state, key, f"age_min={age:.0f}")


# ── Check 3: MIMIR freshness + repeat-complaint escalation ──────────────────

BUG_RE = re.compile(r"\bBUG[- ]?(\d+)\b", re.IGNORECASE)

def check_mimir(state, alerts):
    log = f"{WORKSPACE}/research/mimir_log.jsonl"
    if not os.path.exists(log):
        alerts.append(f"MIMIR log missing: {log}")
        return

    age = mtime_age_min(log)
    if age is not None and age > LOG_STALE_MIN["mimir"]:
        key = "mimir_silent"
        if should_alert(state, key):
            alerts.append(
                f"MIMIR silent: mimir_log.jsonl last updated {age:.0f} min ago "
                f"(threshold {LOG_STALE_MIN['mimir']} min). Analysis pipeline may be stuck."
            )
            record_alert(state, key, f"age_min={age:.0f}")

    try:
        with open(log) as f:
            lines = [l for l in f if l.strip()][-100:]
        entries = [json.loads(l) for l in lines]
    except Exception as e:
        alerts.append(f"research_freshness: mimir_log parse error: {e}")
        return

    by_league = {}
    for e in entries:
        lg = e.get("league", "unknown")
        bugs = set(BUG_RE.findall(e.get("analysis", "")))
        by_league.setdefault(lg, []).append(bugs)

    for league, history in by_league.items():
        last_n = history[-5:]
        if len(last_n) < 3:
            continue
        c = Counter()
        for bugs in last_n:
            for b in bugs:
                c[b] += 1
        for bug, cnt in c.items():
            if cnt >= 3:
                key = f"mimir_repeat:{league}:BUG-{bug}"
                if should_alert(state, key, MIMIR_ESCALATION_COOLDOWN_MIN):
                    alerts.append(
                        f"MIMIR repeat-escalation [{league}]: BUG-{bug} flagged in "
                        f"{cnt}/{len(last_n)} recent analyses. Likely unresolved "
                        f"structural issue — see mimir_log.jsonl for prescription."
                    )
                    record_alert(state, key, f"count={cnt}")


# ── Check 4: LOKI cycle review staleness ────────────────────────────────────

def check_loki(state, alerts):
    log = f"{WORKSPACE}/research/loki_cycle_review_log.jsonl"

    loki_log = f"{WORKSPACE}/research/loki.log"
    age_min = mtime_age_min(loki_log)
    if age_min is not None and age_min > LOG_STALE_MIN["loki"]:
        key = "loki_log_stale"
        if should_alert(state, key):
            alerts.append(
                f"LOKI log stale: loki.log last updated {age_min:.0f} min ago "
                f"(threshold {LOG_STALE_MIN['loki']} min)."
            )
            record_alert(state, key, f"age_min={age_min:.0f}")

    latest_per_league = {}
    if os.path.exists(log):
        try:
            with open(log) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    e = json.loads(line)
                    lg = e.get("league", "unknown")
                    ts = e.get("ts", "")
                    if lg not in latest_per_league or ts > latest_per_league[lg]:
                        latest_per_league[lg] = ts
        except Exception as e:
            alerts.append(f"research_freshness: loki_cycle_review_log parse error: {e}")
            return

    for league in LEAGUES:
        ts = latest_per_league.get(league)
        threshold_days = LOKI_STALE_DAYS[league]
        if ts is None:
            if not _league_review_due(league):
                continue  # still in first cycle, or prior cycles predated LOKI
            key = f"loki_never_reviewed:{league}"
            if should_alert(state, key):
                alerts.append(
                    f"LOKI has never reviewed cycles for [{league}] since its first "
                    f"post-LOKI cycle boundary. Losers not being retuned. "
                    f"Inspect loki.log around the cycle_started_at timestamp."
                )
                record_alert(state, key)
            continue
        try:
            ts_norm = ts if "+" in ts or ts.endswith("Z") else ts + "+00:00"
            ts_norm = ts_norm.replace("Z", "+00:00")
            last_dt = datetime.fromisoformat(ts_norm)
            age_days = (datetime.now(timezone.utc) - last_dt).total_seconds() / 86400
            if age_days > threshold_days:
                key = f"loki_stale:{league}"
                if should_alert(state, key):
                    alerts.append(
                        f"LOKI cycle review stale [{league}]: last entry "
                        f"{age_days:.1f}d ago (threshold {threshold_days}d)."
                    )
                    record_alert(state, key, f"age_days={age_days:.1f}")
        except Exception as e:
            alerts.append(
                f"research_freshness: bad timestamp in loki log for {league} ({ts!r}): {e}"
            )


# ── Check 5: TYR / HEIMDALL freshness ───────────────────────────────────────

def check_tyr_heimdall(state, alerts):
    for officer in ["tyr", "heimdall"]:
        log = f"{WORKSPACE}/research/{officer}.log"
        age = mtime_age_min(log)
        if age is None:
            key = f"{officer}_missing"
            if should_alert(state, key):
                alerts.append(f"{officer.upper()} log missing: {log}")
                record_alert(state, key)
        elif age > LOG_STALE_MIN[officer]:
            key = f"{officer}_stale"
            if should_alert(state, key):
                alerts.append(
                    f"{officer.upper()} log stale: last updated {age:.0f} min ago "
                    f"(threshold {LOG_STALE_MIN[officer]} min)."
                )
                record_alert(state, key, f"age_min={age:.0f}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    import sys
    dry_run = "--dry-run" in sys.argv

    state = load_state()
    alerts = []

    check_odin_leagues(state, alerts)
    check_freya(state, alerts)
    check_mimir(state, alerts)
    check_loki(state, alerts)
    check_tyr_heimdall(state, alerts)

    if alerts:
        header = f"[research_freshness] {len(alerts)} issue(s) at {now_ts()}:"
        body = "\n\n".join(f"- {a}" for a in alerts)
        msg = f"{header}\n\n{body}"
        if len(msg) > 3900:
            msg = msg[:3900] + "\n\n(truncated)"
        print(msg)
        if not dry_run:
            telegram(msg)
            save_state(state)
        else:
            print("\n[DRY RUN — no Telegram, no state saved]")
    else:
        print(f"[research_freshness] {now_ts()}: all research signals fresh.")
        if not dry_run:
            save_state(state)


if __name__ == "__main__":
    main()
