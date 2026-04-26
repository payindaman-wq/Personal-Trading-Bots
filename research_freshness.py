#!/usr/bin/env python3
"""
research_freshness.py — detects silent research staleness.

Runs hourly via cron. Logs every issue it finds; ONLY Telegrams items that are a
call to action for Chris (not routine stalls, not service health, not informational
status). Per feedback_syn_reporting.md: Telegram is reserved for signal, never
noise.

Actionable (Telegram): new LOKI escalations awaiting human decision; MIMIR
repeat-escalation of the same BUG across multiple analyses (terminal-state
signal requiring Chris to decide whether to apply a prescribed patch or redesign).

Informational (log only): ODIN/FREYA stall counts, researcher.log freshness,
MIMIR/LOKI log mtime, cycle-review gaps, TYR/HEIMDALL freshness. These are
covered by sys_heartbeat auto-remediation or are visible on the dashboard.
"""
import json, os, re, time, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone

WORKSPACE  = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/freshness_state.json"
from config_loader import config
BOT_TOKEN = config.telegram.bot_token
CHAT_ID   = config.telegram.chat_id

COOLDOWN_MIN = 1440        # 24h
MIMIR_ESCALATION_COOLDOWN_MIN = 2880  # 48h

LEAGUES = ["day", "swing", "futures_day", "futures_swing"]
STALL_THRESH = 500

LOG_STALE_MIN = {
    "odin":     30,
    "pm":       30,
    "mimir":    480,
    "loki":     60,
    "tyr":      45,
    "heimdall": 45,
}

LOKI_STALE_DAYS = {
    "day": 2,
    "futures_day": 2,
    "swing": 10,
    "futures_swing": 10,
}

CYCLE_STATE_PATHS = {
    "day":           f"{WORKSPACE}/competition/cycle_state.json",
    "swing":         f"{WORKSPACE}/competition/swing/swing_cycle_state.json",
    "futures_day":   f"{WORKSPACE}/competition/futures_day/cycle_state.json",
    "futures_swing": f"{WORKSPACE}/competition/futures_swing/cycle_state.json",
}
LOKI_REVIEW_LOG     = f"{WORKSPACE}/research/loki_cycle_review_log.jsonl"
LOKI_ESCALATION_LOG = f"{WORKSPACE}/research/loki_escalation_log.jsonl"


def _load_cycle_state(league):
    path = CYCLE_STATE_PATHS.get(league)
    if not path or not os.path.exists(path):
        return None
    try:
        return json.load(open(path))
    except Exception:
        return None


def _league_review_due(league):
    """Suppresses false-positive 'never_reviewed' when still in first cycle or
    when prior cycles predated LOKI deployment."""
    cs = _load_cycle_state(league)
    if cs is None:
        return False
    cycle = cs.get("cycle", 1)
    sprint_in_cycle = cs.get("sprint_in_cycle", 0)
    sprints_per_cycle = cs.get("sprints_per_cycle", 7)
    if cycle == 1 and sprint_in_cycle < sprints_per_cycle:
        return False
    if cycle > 1 and os.path.exists(LOKI_REVIEW_LOG):
        log_mtime = os.path.getmtime(LOKI_REVIEW_LOG)
        cycle_started = cs.get("cycle_started_at", "")
        try:
            started_dt = datetime.fromisoformat(cycle_started.replace("Z", "+00:00"))
            return started_dt.timestamp() > log_mtime
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


INBOX = f"{WORKSPACE}/syn_inbox.jsonl"


def telegram(msg, severity="warning"):
    """Write to SYN inbox. sys_heartbeat is the sole Telegram gateway.
    Research-freshness signals are dashboard-only; only true stalls (MIMIR
    silent, LOKI unreachable) surface to Chris via the heartbeat allowlist."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "research_freshness",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
        return True
    except Exception as e:
        print(f"[research_freshness] inbox write failed: {e}")
        return False


def mtime_age_min(path):
    if not os.path.exists(path):
        return None
    return (time.time() - os.path.getmtime(path)) / 60


def info(alerts, msg):
    """Log-only alert: no Telegram. For routine stall/freshness status."""
    alerts.append((False, msg))


def action(alerts, msg):
    """Actionable alert: Telegram + log. Only for call-to-action items requiring
    Chris's decision (per feedback_syn_reporting.md)."""
    alerts.append((True, msg))


# ── Check 1: ODIN per-league (stall + log freshness) — INFO ONLY ────────────

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
                        info(alerts, f"ODIN stalled [{league}]: {gsb} gens since last best "
                                     f"(current gen {gen}).")
                        record_alert(state, key, f"gsb={gsb}")
            except Exception as e:
                info(alerts, f"parse error {gs_path}: {e}")

        age = mtime_age_min(log_path)
        if age is None:
            key = f"odin_log_missing:{league}"
            if should_alert(state, key):
                info(alerts, f"ODIN log missing [{league}]: {log_path}")
                record_alert(state, key)
        elif age > LOG_STALE_MIN["odin"]:
            key = f"odin_log_stale:{league}"
            if should_alert(state, key):
                info(alerts, f"ODIN log stale [{league}]: {age:.0f} min "
                             f"(threshold {LOG_STALE_MIN['odin']}).")
                record_alert(state, key, f"age_min={age:.0f}")


# ── Check 2: FREYA stall + freshness — INFO ONLY ────────────────────────────

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
                    info(alerts, f"FREYA stalled: {gsb} gens since last best (current gen {gen}).")
                    record_alert(state, key, f"gsb={gsb}")
        except Exception as e:
            info(alerts, f"parse error {gs_path}: {e}")

    age = mtime_age_min(log_path)
    if age is None:
        key = "freya_log_missing"
        if should_alert(state, key):
            info(alerts, f"FREYA log missing: {log_path}")
            record_alert(state, key)
    elif age > LOG_STALE_MIN["pm"]:
        key = "freya_log_stale"
        if should_alert(state, key):
            info(alerts, f"FREYA log stale: {age:.0f} min (threshold {LOG_STALE_MIN['pm']}).")
            record_alert(state, key, f"age_min={age:.0f}")


# ── Check 3: MIMIR — freshness INFO; repeat-escalation ACTIONABLE ───────────

BUG_RE = re.compile(r"\bBUG[- ]?(\d+)\b", re.IGNORECASE)

def check_mimir(state, alerts):
    log = f"{WORKSPACE}/research/mimir_log.jsonl"
    if not os.path.exists(log):
        info(alerts, f"MIMIR log missing: {log}")
        return

    age = mtime_age_min(log)
    if age is not None and age > LOG_STALE_MIN["mimir"]:
        key = "mimir_silent"
        if should_alert(state, key):
            info(alerts, f"MIMIR silent: log updated {age:.0f} min ago "
                         f"(threshold {LOG_STALE_MIN['mimir']}).")
            record_alert(state, key, f"age_min={age:.0f}")

    try:
        with open(log) as f:
            lines = [l for l in f if l.strip()][-100:]
        entries = [json.loads(l) for l in lines]
    except Exception as e:
        info(alerts, f"mimir_log parse error: {e}")
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
                    action(alerts,
                        f"MIMIR terminal-state signal [{league}]: BUG-{bug} flagged in "
                        f"{cnt}/{len(last_n)} recent analyses. Decision needed — apply the "
                        f"prescribed patch or redesign the search space.\n"
                        f"Review: /root/.openclaw/workspace/research/mimir_log.jsonl"
                    )
                    record_alert(state, key, f"count={cnt}")


# ── Check 4: LOKI cycle-review gaps — INFO ONLY ─────────────────────────────

def check_loki(state, alerts):
    loki_log = f"{WORKSPACE}/research/loki.log"
    age_min = mtime_age_min(loki_log)
    if age_min is not None and age_min > LOG_STALE_MIN["loki"]:
        key = "loki_log_stale"
        if should_alert(state, key):
            info(alerts, f"LOKI log stale: {age_min:.0f} min (threshold {LOG_STALE_MIN['loki']}).")
            record_alert(state, key, f"age_min={age_min:.0f}")

    latest_per_league = {}
    log = LOKI_REVIEW_LOG
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
            info(alerts, f"loki_cycle_review_log parse error: {e}")
            return

    for league in LEAGUES:
        ts = latest_per_league.get(league)
        threshold_days = LOKI_STALE_DAYS[league]
        if ts is None:
            if not _league_review_due(league):
                continue
            key = f"loki_never_reviewed:{league}"
            if should_alert(state, key):
                info(alerts, f"LOKI never reviewed [{league}] since first post-LOKI cycle boundary.")
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
                    info(alerts, f"LOKI cycle review stale [{league}]: {age_days:.1f}d "
                                 f"(threshold {threshold_days}d).")
                    record_alert(state, key, f"age_days={age_days:.1f}")
        except Exception as e:
            info(alerts, f"bad timestamp in loki log for {league} ({ts!r}): {e}")


# ── Check 5: LOKI escalations awaiting human review — INFO ONLY ────────────

def check_loki_escalations(state, alerts):
    """LOKI logs structural-code recommendations from MIMIR into the escalation
    log. Per feedback_loki_escalation_autonomy: LOKI escalations are work
    orders, not decision requests — they are surfaced on the dashboard for
    audit only, never paged to Telegram. VIDAR handles the judgment calls."""
    if not os.path.exists(LOKI_ESCALATION_LOG):
        return
    try:
        with open(LOKI_ESCALATION_LOG) as f:
            entries = [json.loads(l) for l in f if l.strip()]
    except Exception as e:
        info(alerts, f"loki_escalation_log parse error: {e}")
        return
    if not entries:
        return
    last_seen_ts = state.get("loki_escalations_last_seen", {}).get("ts", "")
    new_entries = [e for e in entries if e.get("ts", "") > last_seen_ts]
    if not new_entries:
        return
    summary_lines = []
    for e in new_entries[-5:]:
        lg = e.get("league", "?")
        gen = e.get("generation", "?")
        desc = (e.get("description", "") or "")[:240].replace("\n", " ")
        summary_lines.append(f"[{lg} gen {gen}] {desc}")
    body = "\n  ".join(summary_lines)
    extra = f" (+{len(new_entries) - 5} older)" if len(new_entries) > 5 else ""
    info(alerts,
        f"LOKI has {len(new_entries)} unreviewed escalation(s){extra} — work orders on dashboard:\n  {body}"
    )
    latest_ts = max(e.get("ts", "") for e in new_entries)
    state["loki_escalations_last_seen"] = {"ts": latest_ts, "recorded_at": now_ts()}


# ── Check 6: TYR / HEIMDALL freshness — INFO ONLY ───────────────────────────

def _inbox_error(msg):
    """Write severity=error to SYN inbox with source=tyr_freshness for Telegram routing."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "tyr_freshness",
            "severity": "error",
            "msg":      msg[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + chr(10))
    except Exception as e:
        print(f"[research_freshness/tyr_inbox] {e}")


def check_tyr_heimdall(state, alerts):
    # Upgraded 2026-04-19: stale TYR/HEIMDALL = consumers (tick scripts, mimir)
    # fall back to regime=None, so bots lose their risk multiplier.
    # Routes through source=tyr_freshness (allowlisted) + severity=error so it
    # reaches Chris via Telegram, while LOKI-escalation alerts stay dashboard-only.
    for officer in ["tyr", "heimdall"]:
        log = f"{WORKSPACE}/research/{officer}.log"
        age = mtime_age_min(log)
        if age is None:
            key = f"{officer}_missing"
            if should_alert(state, key):
                msg = f"{officer.upper()} log missing: {log} — officer not running?"
                info(alerts, msg)
                _inbox_error(f"[OPS/tyr_freshness] {msg}")
                record_alert(state, key)
        elif age > LOG_STALE_MIN[officer]:
            key = f"{officer}_stale"
            if should_alert(state, key):
                msg = (f"{officer.upper()} log stale: {age:.0f} min "
                       f"(threshold {LOG_STALE_MIN[officer]}) — consumers degrading to fallback.")
                info(alerts, msg)
                _inbox_error(f"[OPS/tyr_freshness] {msg}")
                record_alert(state, key, f"age_min={age:.0f}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    import sys
    dry_run = "--dry-run" in sys.argv

    state = load_state()
    alerts = []  # list of (actionable: bool, msg: str)

    check_odin_leagues(state, alerts)
    check_freya(state, alerts)
    check_mimir(state, alerts)
    check_loki(state, alerts)
    check_loki_escalations(state, alerts)
    check_tyr_heimdall(state, alerts)

    actionable = [m for a, m in alerts if a]
    informational = [m for a, m in alerts if not a]

    # Always log both tiers to stdout (→ research_freshness.log via cron redirect)
    ts = now_ts()
    if not alerts:
        print(f"[research_freshness] {ts}: all research signals fresh.")
    else:
        print(f"[research_freshness] {ts}: {len(actionable)} actionable, "
              f"{len(informational)} informational.")
        if actionable:
            print("  ACTIONABLE:")
            for m in actionable:
                print(f"    - {m}")
        if informational:
            print("  INFO:")
            for m in informational:
                print(f"    - {m}")

    # Telegram ONLY actionable items (per feedback_syn_reporting.md)
    if actionable and not dry_run:
        header = f"[research_freshness] {len(actionable)} item(s) need your decision:"
        body = "\n\n".join(f"- {m}" for m in actionable)
        msg = f"{header}\n\n{body}"
        if len(msg) > 3900:
            msg = msg[:3900] + "\n\n(truncated)"
        telegram(msg)

    if not dry_run:
        save_state(state)
    else:
        print("\n[DRY RUN — no Telegram, no state saved]")


if __name__ == "__main__":
    main()
