#!/usr/bin/env python3
"""
loki.py — LOKI Implementation Officer (Executive Staff)

Monitors mimir_log.jsonl for new Mimir analyses and automates the relay loop:
1. Confirms program.md was updated by Mimir, git commits it
2. Classifies analysis for code changes to odin_researcher_v2.py
3. Implements safe constant/parameter changes; escalates structural ones
4. Restarts odin service if code changed; reports all actions via Telegram

Runs every 15 minutes via cron.
Usage: python3 research/loki.py [--dry-run]
"""
import json
import os
import re
import shutil
import yaml
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

WORKSPACE        = "/root/.openclaw/workspace"
RESEARCH         = os.path.join(WORKSPACE, "research")
MIMIR_LOG        = os.path.join(RESEARCH, "mimir_log.jsonl")
LOKI_LOG         = os.path.join(RESEARCH, "loki_log.jsonl")
LOKI_ESC_LOG     = os.path.join(RESEARCH, "loki_escalation_log.jsonl")
RESEARCHER       = os.path.join(RESEARCH, "odin_researcher_v2.py")
FREYA_RESEARCHER = os.path.join(RESEARCH, "freya_researcher.py")
PM_RESEARCH_DIR  = os.path.join(RESEARCH, "pm")
PM_FLEET_DIR     = os.path.join(WORKSPACE, "fleet", "polymarket")

FREYA_SLOTS = ["mist", "kara", "thrud"]

LOKI_PENDING_ACTIONS    = os.path.join(RESEARCH, "loki_pending_actions.jsonl")
STRUCTURAL_RATE_FILE    = os.path.join(RESEARCH, "loki_structural_rate.json")
STRUCTURAL_MONITOR_FILE = os.path.join(RESEARCH, "loki_structural_monitor.json")
STRUCTURAL_RATE_MIN     = 360   # 6h between structural code changes per league

# Self-heal audit layer
LOKI_REVERT_HISTORY_FILE   = os.path.join(RESEARCH, "loki_revert_history.json")
LOKI_STRUCTURAL_PAUSES     = os.path.join(RESEARCH, "loki_structural_pauses.json")
VIDAR_SCRIPT               = os.path.join(RESEARCH, "vidar.py")
MAINTENANCE_LOG_GLOBAL     = os.path.join(WORKSPACE, "maintenance_log.jsonl")
AUDIT_MIN_GENS_FIRST             = 20
AUDIT_MIN_GENS_FINAL             = 120
AUDIT_MAX_MINUTES                = 360
AUDIT_STRUCTURAL_FAILURE_RISE_PP = 15
AUDIT_MEAN_SHARPE_DROP           = 0.3
AUDIT_REVERT_OSCILLATION_LIMIT   = 2
AUDIT_PAUSE_HOURS                = 12

# VIDAR fire dedup (prevents duplicate Opus/Sonnet fires on rapid LOKI retries
# or while a league is already paused — see audit 2026-04-20).
VIDAR_FIRE_STATE_FILE            = os.path.join(RESEARCH, "vidar_fire_state.json")
VIDAR_REVERT_REVIEW_COOLDOWN_SEC = 600   # 10 min per (league, mode)

def _vidar_fire_allowed(league, mode, cooldown_sec):
    try:
        state = json.load(open(VIDAR_FIRE_STATE_FILE)) if os.path.exists(VIDAR_FIRE_STATE_FILE) else {}
    except Exception:
        state = {}
    key = f"{league}:{mode}"
    now = datetime.now(timezone.utc).timestamp()
    last = state.get(key, 0)
    if now - last < cooldown_sec:
        return False
    state[key] = now
    try:
        json.dump(state, open(VIDAR_FIRE_STATE_FILE, "w"))
    except Exception:
        pass
    return True
PM_PERSONAS = {
    "sports":       "You are a sports analytics expert specializing in predicting sporting event outcomes.",
    "politics":     "You are a political analyst specializing in predicting electoral and policy outcomes.",
    "crypto":       "You are a cryptocurrency analyst specializing in predicting crypto-related outcomes.",
    "economics":    "You are an economic data analyst specializing in predicting macroeconomic outcomes.",
    "world_events": "You are a global events analyst specializing in predicting world news outcomes.",
}

GEMINI_SECRET = "/root/.openclaw/secrets/gemini.json"
GEMINI_MODEL  = "gemini-2.5-flash-lite"
GEMINI_BASE   = "https://generativelanguage.googleapis.com/v1beta/models"

TG_BOT_TOKEN     = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
TG_CHAT_ID       = "8154505910"

DRY_RUN = "--dry-run" in sys.argv

# Keywords that suggest code changes may be needed in odin_researcher_v2.py
CODE_CHANGE_KEYWORDS = [
    "odin_researcher", "MIN_TRADES", "POPULATION_SIZE", "SUSPICIOUS_SHARPE",
    "STALL_ALERT_GENS", "adj_score", "acceptance criteria", "acceptance criterion",
    "effective score", "the code should", "the researcher script",
    "modify the script", "change the constant", "update the constant",
]

# Only these constants can be changed automatically (hard whitelist)
ALLOWED_CONSTANTS      = {"MIN_TRADES", "POPULATION_SIZE", "SUSPICIOUS_SHARPE", "STALL_ALERT_GENS"}
FREYA_ALLOWED_CONSTS   = {"MIN_BETS", "POPULATION_SIZE"}  # STALL_ALERT_GENS excluded: freya_researcher.py must never have Telegram stall alerts

PM_CODE_CHANGE_KEYWORDS = [
    "freya_researcher", "MIN_BETS", "POPULATION_SIZE",
    "change the constant", "update the constant", "the code should",
    "modify the script", "the researcher script",
]

# Files LOKI must never touch (block list for extra safety)
BLOCKED_FILES = [
    "competition_tick.py", "swing_competition_tick.py", "futures_swing_competition_tick.py",
    "futures_day_competition_tick.py", "league_watchdog.py", "sys_heartbeat.py",
    "day_daily_restart.py", "/bots/", "backtest.py",
]


# ── Utilities ─────────────────────────────────────────────────────────────────

def tg_send(text, severity="warning"):
    """Route to SYN inbox - never directly to Telegram. SYN decides what reaches the user."""
    inbox = os.path.join(WORKSPACE, "syn_inbox.jsonl")
    entry = json.dumps({"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
                        "source": "loki", "severity": severity, "msg": text})
    try:
        with open(inbox, "a") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"  [loki] inbox write failed: {e}")
    if DRY_RUN:
        print(f"[dry-run SYN-inbox/{severity}] {text}")


def load_gemini_key():
    with open(GEMINI_SECRET) as f:
        data = json.load(f)
    return data.get("gemini_api_key") or data["gemini_api_keys"][0]


def call_gemini(prompt, max_tokens=500, temperature=0.1):
    api_key = load_gemini_key()
    url = f"{GEMINI_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature},
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()



def _read_results_tsv(league, last_n=50):
    path = os.path.join(RESEARCH, league, "results.tsv")
    if not os.path.exists(path):
        return []
    try:
        with open(path) as f:
            lines = f.readlines()[1:]
    except Exception:
        return []
    rows = []
    for line in lines[-last_n:]:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        try:
            rows.append({
                "gen":    int(parts[0]),
                "sharpe": float(parts[1]),
                "trades": int(parts[4]),
                "status": parts[5],
            })
        except ValueError:
            continue
    return rows


def compute_league_metrics(league, last_n=50):
    rows = _read_results_tsv(league, last_n)
    if not rows:
        return None
    total = len(rows)
    structural = sum(1 for r in rows if r["trades"] > 450)
    # League-agnostic 'valid' filter: exclude structural failures and errors.
    # structural (trades>450) is captured in its own metric; backtest_error/zero-trade
    # rows skew the mean. Everything else counts.
    valid = [r for r in rows if r["trades"] > 0 and r["trades"] <= 450 and r["status"] != 'backtest_error']
    new_bests = sum(1 for r in rows if r["status"] == "new_best")
    return {
        "gens_in_window":          total,
        "structural_failure_rate": round(structural / total, 4) if total else 0,
        "mean_sharpe_valid":       round(sum(r["sharpe"] for r in valid) / len(valid), 4) if valid else None,
        "new_best_count":          new_bests,
        "latest_gen":              rows[-1]["gen"],
    }


def load_revert_history():
    if os.path.exists(LOKI_REVERT_HISTORY_FILE):
        try:
            return json.load(open(LOKI_REVERT_HISTORY_FILE))
        except Exception:
            pass
    return {}


def save_revert_history(h):
    with open(LOKI_REVERT_HISTORY_FILE, "w") as f:
        json.dump(h, f, indent=2)


def load_structural_pauses():
    if os.path.exists(LOKI_STRUCTURAL_PAUSES):
        try:
            return json.load(open(LOKI_STRUCTURAL_PAUSES))
        except Exception:
            pass
    return {}


def save_structural_pauses(p):
    with open(LOKI_STRUCTURAL_PAUSES, "w") as f:
        json.dump(p, f, indent=2)


def is_structural_paused(league):
    pauses = load_structural_pauses()
    until = pauses.get(league)
    if not until:
        return False, None
    try:
        until_dt = datetime.fromisoformat(until).replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) < until_dt:
            return True, until
        del pauses[league]
        save_structural_pauses(pauses)
    except Exception:
        pass
    return False, None


def _record_revert(league, reason, detail=""):
    history = load_revert_history()
    revert_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
    history.setdefault(league, []).append({
        "ts":     revert_ts,
        "reason": reason,
        "detail": detail[:200],
    })
    cutoff = datetime.now(timezone.utc).timestamp() - 30 * 86400
    kept = []
    for r in history[league]:
        try:
            r_ts = datetime.fromisoformat(r["ts"]).replace(tzinfo=timezone.utc).timestamp()
            if r_ts > cutoff:
                kept.append(r)
        except Exception:
            continue
    history[league] = kept
    save_revert_history(history)

    # Maintenance tab surface — every revert shows up here with source=LOKI.
    try:
        mrec = {
            "ts":       revert_ts,
            "phase":    "reverted",
            "source":   "LOKI",
            "league":   league,
            "kind":     f"audit_revert_{reason}",
            "detail":   detail[:200],
            "result":   "backup_restored",
            "fix_hint": "VIDAR arbitration queued",
        }
        with open(MAINTENANCE_LOG_GLOBAL, "a") as _mf:
            _mf.write(json.dumps(mrec) + "\n")
    except Exception as _e:
        print(f"  [loki/revert/maintenance] failed: {_e}")

    # Fire VIDAR revert_review in background (arbitration — non-blocking).
    # Deduped per (league, mode) with a cooldown window to avoid duplicate
    # fires when LOKI retries the same revert in quick succession.
    if _vidar_fire_allowed(league, "revert_review", VIDAR_REVERT_REVIEW_COOLDOWN_SEC):
        try:
            subprocess.Popen(
                ["python3", VIDAR_SCRIPT,
                 "--mode", "revert_review",
                 "--league", league,
                 "--revert-ts", revert_ts],
                stdout=open(os.path.join(RESEARCH, "vidar.log"), "a"),
                stderr=subprocess.STDOUT,
            )
        except Exception as _e:
            print(f"  [loki/revert/vidar] launch failed: {_e}")
    else:
        print(f"  [loki/revert/vidar] skipped — revert_review for {league} within cooldown")

    # Oscillation guard
    now_ts = datetime.now(timezone.utc).timestamp()
    recent = [r for r in kept
              if (now_ts - datetime.fromisoformat(r["ts"]).replace(tzinfo=timezone.utc).timestamp()) < 86400]
    if len(recent) >= AUDIT_REVERT_OSCILLATION_LIMIT:
        pauses = load_structural_pauses()
        # Detect whether we're already in an active pause window — if so,
        # extend but skip the VIDAR re-fire (it already diagnosed this cycle).
        already_paused = False
        prev_until = pauses.get(league)
        if prev_until:
            try:
                prev_dt = datetime.fromisoformat(prev_until).replace(tzinfo=timezone.utc)
                if prev_dt > datetime.now(timezone.utc):
                    already_paused = True
            except Exception:
                pass
        until = datetime.now(timezone.utc) + timedelta(hours=AUDIT_PAUSE_HOURS)
        pauses[league] = until.strftime("%Y-%m-%dT%H:%M")
        save_structural_pauses(pauses)
        if already_paused:
            print(f"  [loki-oscillation] {league} pause extended (already paused until {prev_until}); skipping VIDAR re-fire")
        else:
            print(f"  [loki-oscillation] {league} paused {AUDIT_PAUSE_HOURS}h after {len(recent)} reverts in 24h -- VIDAR oscillation_diag will review")
            try:
                subprocess.Popen(
                    ["python3", VIDAR_SCRIPT,
                     "--mode", "oscillation_diag",
                     "--league", league],
                    stdout=open(os.path.join(RESEARCH, "vidar.log"), "a"),
                    stderr=subprocess.STDOUT,
                )
            except Exception as _e:
                print(f"  [loki/oscillation/vidar] launch failed: {_e}")


def _audit_verdict(baseline, current):
    if not baseline or not current:
        return "insufficient_data", "missing_metrics"
    b_sfr = baseline.get("structural_failure_rate")
    c_sfr = current.get("structural_failure_rate")
    if b_sfr is not None and c_sfr is not None:
        rise = c_sfr - b_sfr
        if rise * 100 >= AUDIT_STRUCTURAL_FAILURE_RISE_PP:
            return "degraded", f"structural_failure_rate rose {rise*100:.1f}pp ({b_sfr:.2f} -> {c_sfr:.2f})"
    b_s = baseline.get("mean_sharpe_valid")
    c_s = current.get("mean_sharpe_valid")
    if b_s is not None and c_s is not None:
        drop = b_s - c_s
        if drop >= AUDIT_MEAN_SHARPE_DROP:
            return "degraded", f"mean_sharpe_valid dropped {drop:.3f} ({b_s:.3f} -> {c_s:.3f})"
    return "healthy", ""


def load_structural_rate():
    if os.path.exists(STRUCTURAL_RATE_FILE):
        try:
            with open(STRUCTURAL_RATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_structural_rate(rate):
    with open(STRUCTURAL_RATE_FILE, "w") as f:
        json.dump(rate, f)


def load_structural_monitor():
    if os.path.exists(STRUCTURAL_MONITOR_FILE):
        try:
            with open(STRUCTURAL_MONITOR_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_structural_monitor(m):
    with open(STRUCTURAL_MONITOR_FILE, "w") as f:
        json.dump(m, f)


def check_structural_monitors():
    monitor = load_structural_monitor()
    if not monitor:
        return
    changed = False
    for monitor_key, m in list(monitor.items()):
        league = m.get("league", monitor_key.split("__")[0])
        try:
            ts = datetime.fromisoformat(m["ts"]).replace(tzinfo=timezone.utc)
        except Exception:
            del monitor[monitor_key]; changed = True
            continue
        age_min = (datetime.now(timezone.utc) - ts).total_seconds() / 60
        unit     = m.get("unit")
        backup   = m.get("backup")
        target   = m.get("target")
        baseline = m.get("baseline", {})
        kind     = m.get("kind", "code")

        if unit and age_min >= 5:
            try:
                result = subprocess.run(
                    ["systemctl", "is-active", unit],
                    capture_output=True, text=True, timeout=5,
                )
                if result.stdout.strip() != "active":
                    print(f"  [loki-audit] CRASH REVERT: {unit} inactive after {kind} change ({league})")
                    if backup and target and os.path.exists(backup):
                        shutil.copy2(backup, target)
                        subprocess.run(["systemctl", "restart", unit], timeout=15, check=False)
                    _record_revert(league, "service_crash", f"{unit} inactive after {kind} change")
                    print(f"  [loki-audit] {unit} crashed after {kind} change -- backup restored, VIDAR revert_review fired")
                    del monitor[monitor_key]; changed = True
                    continue
            except Exception as e:
                print(f"  [loki-audit] is-active check failed: {e}")

        current = compute_league_metrics(league, last_n=50)
        baseline_gen = baseline.get("latest_gen")
        current_gen  = (current or {}).get("latest_gen")
        gens_elapsed = (current_gen - baseline_gen) if (baseline_gen and current_gen) else 0

        if age_min >= AUDIT_MAX_MINUTES:
            print(f"  [loki-audit] {league} {kind} change cleared (timeout {age_min:.0f}m, gens_elapsed={gens_elapsed})")
            del monitor[monitor_key]; changed = True
            continue

        if gens_elapsed < AUDIT_MIN_GENS_FIRST:
            continue

        verdict, reason = _audit_verdict(baseline, current)
        if verdict == "degraded":
            print(f"  [loki-audit] METRIC REVERT ({league}/{kind}): {reason}")
            if backup and target and os.path.exists(backup):
                shutil.copy2(backup, target)
                if unit:
                    subprocess.run(["systemctl", "restart", unit], timeout=15, check=False)
            _record_revert(league, "metric_degradation", reason)
            print(f"  [loki-audit] metric revert {league}/{kind}: {reason} -- VIDAR revert_review fired")
            del monitor[monitor_key]; changed = True
            continue

        if gens_elapsed >= AUDIT_MIN_GENS_FINAL:
            print(f"  [loki-audit] {league} {kind} change healthy at +{gens_elapsed} gens -- clearing monitor")
            del monitor[monitor_key]; changed = True

    if changed:
        save_structural_monitor(monitor)


SERVICE_MAP = {
    "day":           "odin_day.service",
    "swing":         "odin_swing.service",
    "futures_day":   "odin_futures_day.service",
    "futures_swing": "odin_futures_swing.service",
    "pm":            "freya.service",
}


def champion_guardrail(new_code, league):
    """Reject a candidate odin_researcher_v2.py if its is_poison_yaml would flag any league champion.

    Prevents a repeat of the 2026-04-14 incident where LOKI installed a poison rule matching
    the champion itself (rsi_long=29.33 hit by abs(long_rsi - 29.56) < 0.3), blocking all
    exploration near the actual best strategy for 72.6h.
    """
    import tempfile
    leagues = [league] if league in ("day", "swing", "futures_day", "futures_swing") else \
              ["day", "swing", "futures_day", "futures_swing"]
    tf = tempfile.NamedTemporaryFile(mode="w", suffix="_candidate.py", delete=False)
    tf.write(new_code); tf.close()
    try:
        for lg in leagues:
            champ_path = os.path.join(RESEARCH, lg, "best_strategy.yaml")
            if not os.path.exists(champ_path):
                continue
            validator = (
                "import sys, yaml, importlib.util\n"
                f'spec = importlib.util.spec_from_file_location("cand", "{tf.name}")\n'
                "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
                'if not hasattr(m, "is_poison_yaml"):\n    sys.exit(0)\n'
                f'champ = yaml.safe_load(open("{champ_path}"))\n'
                f'poison, reason = m.is_poison_yaml(champ, "{lg}")\n'
                "if poison:\n    print(reason); sys.exit(2)\n"
            )
            r = subprocess.run(["python3", "-c", validator],
                               capture_output=True, text=True, timeout=15)
            if r.returncode == 2:
                return False, f"would poison-reject {lg} champion: {r.stdout.strip()}"
            if r.returncode not in (0, 2):
                return False, f"guardrail validator error on {lg}: {r.stderr.strip()[:200]}"
    finally:
        try: os.unlink(tf.name)
        except OSError: pass
    return True, ""


def apply_structural_change(league, description, patches):
    """Apply a structural patch generated by Mimir. patches is a list of {old, new} dicts."""
    if not patches:
        return False, "no patch provided (Mimir did not generate a structural patch)"

    paused, until = is_structural_paused(league)
    if paused:
        return False, f"structural changes paused for {league} until {until} (oscillation guard)"

    rate    = load_structural_rate()
    last_ts = rate.get(league or "global")
    if last_ts:
        last_dt = datetime.fromisoformat(last_ts).replace(tzinfo=timezone.utc)
        age_min = (datetime.now(timezone.utc) - last_dt).total_seconds() / 60
        if age_min < STRUCTURAL_RATE_MIN:
            wait = int(STRUCTURAL_RATE_MIN - age_min)
            return False, f"rate limited: {wait}m until next structural change for {league}"

    target = RESEARCHER if league in ("day", "swing", "futures_day", "futures_swing") else FREYA_RESEARCHER
    if not os.path.exists(target):
        return False, f"target file not found: {os.path.basename(target)}"

    with open(target) as f:
        code = f.read()

    new_code = code
    for i, patch in enumerate(patches):
        old_str = patch.get("old", "")
        new_str = patch.get("new", "")
        if not old_str:
            return False, f"patch {i}: empty old string"
        count = code.count(old_str)
        if count != 1:
            return False, f"patch {i}: old string found {count}x (need exactly 1)"
        new_code = new_code.replace(old_str, new_str, 1)

    try:
        import ast
        ast.parse(new_code)
    except SyntaxError as e:
        return False, f"patch fails syntax check: {e}"

    ok, reason = champion_guardrail(new_code, league)
    if not ok:
        return False, f"champion guardrail blocked: {reason}"

    if DRY_RUN:
        return True, f"DRY_RUN: would apply {len(patches)} patches to {os.path.basename(target)}"

    ts_str = datetime.now().strftime('%Y%m%d_%H%M')
    backup = target + f".structural_{ts_str}.bak"
    shutil.copy2(target, backup)
    with open(target, "w") as f:
        f.write(new_code)

    unit = SERVICE_MAP.get(league)
    if unit:
        subprocess.run(["systemctl", "restart", unit], timeout=15, check=False)

    baseline = compute_league_metrics(league, last_n=50) or {}
    monitor = load_structural_monitor()
    monitor[league] = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "league":   league,
        "unit":     unit,
        "backup":   backup,
        "target":   target,
        "desc":     description[:80],
        "kind":     "code",
        "baseline": baseline,
    }
    save_structural_monitor(monitor)
    rate[league or "global"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
    save_structural_rate(rate)
    rel = os.path.relpath(target, WORKSPACE)
    git_commit([rel], f"[loki-structural] {league}: {description[:60]}")
    return True, f"applied {len(patches)} patches to {os.path.basename(target)}"



# ── Sprint integrity fixes (SYN-queued) ───────────────────────────────────────
MAINTENANCE_LOG_PATH = "/root/.openclaw/workspace/maintenance_log.jsonl"


def _maintenance_log(league, kind, detail, phase, result="", fix_hint=""):
    try:
        import json as _j, os as _o
        from datetime import datetime as _dt, timezone as _tz
        rec = {
            "ts":       _dt.now(_tz.utc).strftime("%Y-%m-%dT%H:%M"),
            "phase":    phase,
            "source":   "LOKI",
            "league":   league,
            "kind":     kind,
            "detail":   detail,
            "result":   result,
            "fix_hint": fix_hint,
        }
        with open(MAINTENANCE_LOG_PATH, "a") as _f:
            _f.write(_j.dumps(rec) + "\n")
    except Exception as _e:
        print(f"  [loki/maintenance_log] failed: {_e}")


# ── Sprint integrity path tables (shared across fix handlers) ────────────────
_CS_PATHS = {
    "day":           "/root/.openclaw/workspace/competition/cycle_state.json",
    "swing":         "/root/.openclaw/workspace/competition/swing/swing_cycle_state.json",
    "futures_day":   "/root/.openclaw/workspace/competition/futures_day/cycle_state.json",
    "futures_swing": "/root/.openclaw/workspace/competition/futures_swing/cycle_state.json",
    "polymarket":    "/root/.openclaw/workspace/competition/polymarket/polymarket_cycle_state.json",
}
_ACTIVE_PATHS = {
    "day":           ("/root/.openclaw/workspace/competition/active",               "/root/.openclaw/workspace/competition/results"),
    "swing":         ("/root/.openclaw/workspace/competition/swing/active",         "/root/.openclaw/workspace/competition/swing/results"),
    "futures_day":   ("/root/.openclaw/workspace/competition/futures_day/active",   "/root/.openclaw/workspace/competition/futures_day/results"),
    "futures_swing": ("/root/.openclaw/workspace/competition/futures_swing/active", "/root/.openclaw/workspace/competition/futures_swing/results"),
}
# (results_dir, archive_root, archive_pattern) for leagues that use cycle archives.
_ARCHIVE_PATHS = {
    "day":        ("/root/.openclaw/workspace/competition/results",              "/root/.openclaw/workspace/competition/archive",              "cycle-{n}"),
    "swing":      ("/root/.openclaw/workspace/competition/swing/results",        "/root/.openclaw/workspace/competition/swing/archive",        "cycle-{n}"),
    "polymarket": ("/root/.openclaw/workspace/competition/polymarket/auto_results", "/root/.openclaw/workspace/competition/polymarket/sprint_results", "cycle_{n}_archive"),
}

ESCALATION_DEDUPE_FILE = os.path.join(RESEARCH, "loki_escalation_dedupe.json")
ESCALATION_COOLDOWN_MIN = 360  # 6h — don't re-escalate the same anomaly within this window


def _load_escalation_dedupe():
    try:
        with open(ESCALATION_DEDUPE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_escalation_dedupe(state):
    try:
        with open(ESCALATION_DEDUPE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"  [loki/dedupe] save failed: {e}")


def _should_escalate(key):
    """Return True if this anomaly hasn't been escalated in the last ESCALATION_COOLDOWN_MIN."""
    state = _load_escalation_dedupe()
    now_dt = datetime.now(timezone.utc)
    last = state.get(key)
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            if (now_dt - last_dt).total_seconds() / 60.0 < ESCALATION_COOLDOWN_MIN:
                return False
        except Exception:
            pass
    # Also purge stale entries older than cooldown so the file doesn't grow forever
    cutoff = now_dt.timestamp() - (ESCALATION_COOLDOWN_MIN * 60)
    fresh = {}
    for k, v in state.items():
        try:
            t = datetime.fromisoformat(v)
            if t.tzinfo is None:
                t = t.replace(tzinfo=timezone.utc)
            if t.timestamp() >= cutoff:
                fresh[k] = v
        except Exception:
            pass
    fresh[key] = now_dt.isoformat()
    _save_escalation_dedupe(fresh)
    return True


def _current_cycle_sprints(league):
    """Return (cycle_number, set_of_sprint_ids_in_current_cycle). Empty set on error."""
    path = _CS_PATHS.get(league)
    if not path or not os.path.exists(path):
        return 1, set()
    try:
        st = json.load(open(path))
        return int(st.get("cycle", 1)), set(st.get("sprints", []))
    except Exception:
        return 1, set()


def _archive_orphans(league, target_cycle_n, orphan_ids=None):
    """Move sprint dirs in results/ into archive/cycle-N/. Returns (moved_list, error_or_None).

    If orphan_ids given, move exactly those. Otherwise infer from results/ minus current-cycle sprints.
    """
    import shutil as _sh, os as _o
    paths = _ARCHIVE_PATHS.get(league)
    if not paths:
        return [], f"no archive config for league {league}"
    results_dir, archive_root, pattern = paths
    if not _o.path.isdir(results_dir):
        return [], f"results_dir missing: {results_dir}"
    _, current_sprints = _current_cycle_sprints(league)
    if orphan_ids is None:
        orphan_ids = [
            d for d in _o.listdir(results_dir)
            if _o.path.isdir(_o.path.join(results_dir, d))
            and not d.startswith("cycle")
            and not d.endswith("_archive")
            and d not in current_sprints
        ]
    if not orphan_ids:
        return [], None
    dest_dir = _o.path.join(archive_root, pattern.format(n=target_cycle_n))
    _o.makedirs(dest_dir, exist_ok=True)
    moved = []
    for sid in orphan_ids:
        src = _o.path.join(results_dir, sid)
        if not _o.path.isdir(src):
            continue
        dst = _o.path.join(dest_dir, sid)
        if _o.path.exists(dst):
            _sh.rmtree(src)
            moved.append(sid + "(dup)")
        else:
            _sh.move(src, dst)
            moved.append(sid)
    return moved, None


def _apply_sprint_integrity_fix(anomalies):
    """For each anomaly, log to maintenance_log; auto-apply safe fixes, escalate the rest."""
    import shutil, os as _o
    outcomes = []
    for a in anomalies:
        league = a.get("league", "?")
        kind   = a.get("kind", "?")
        detail = a.get("detail", "")
        hint   = a.get("fix_hint", "")
        _maintenance_log(league, kind, detail, "attempted", fix_hint=hint)

        if kind == "counter_drift":
            # Safe: sync sprint_in_cycle to len(sprints)
            try:
                cpath = _CS_PATHS[league]
                st = json.load(open(cpath))
                st["sprint_in_cycle"] = len(st.get("sprints", []))
                json.dump(st, open(cpath, "w"), indent=2)
                _maintenance_log(league, kind, detail, "fixed", result=f"synced sprint_in_cycle={st['sprint_in_cycle']}")
                outcomes.append(f"{league}:counter_drift:fixed")
            except Exception as e:
                _maintenance_log(league, kind, detail, "failed", result=str(e))
                outcomes.append(f"{league}:counter_drift:fail:{e}")

        elif kind == "multiple_active":
            # Safe: move all but the latest active dir into results
            try:
                adir, rdir = _ACTIVE_PATHS[league]
                dirs = sorted([d for d in _o.listdir(adir) if _o.path.isdir(_o.path.join(adir, d))])
                to_move = dirs[:-1]  # keep the most recent (lex-sorted by date-suffix name)
                moved = []
                for d in to_move:
                    src_p = _o.path.join(adir, d)
                    dst_p = _o.path.join(rdir, d)
                    if not _o.path.exists(dst_p):
                        shutil.move(src_p, dst_p)
                        moved.append(d)
                    else:
                        shutil.rmtree(src_p)
                        moved.append(d + "(dup)")
                _maintenance_log(league, kind, detail, "fixed", result=f"moved {moved} from active/ to results/")
                outcomes.append(f"{league}:multiple_active:fixed:{len(moved)}")
            except Exception as e:
                _maintenance_log(league, kind, detail, "failed", result=str(e))
                outcomes.append(f"{league}:multiple_active:fail:{e}")

        elif kind == "missing_archive_cycle":
            # Safe: create archive/cycle-N/ and move orphaned results/ dirs into it.
            # Never touches cycle_state.json, never modifies sprint counters.
            try:
                target_n = int(a.get("missing_cycle", 0)) or None
                if not target_n:
                    # Fall back: derive from detail "cycle=X" if parseable
                    m = re.search(r"cycle=(\d+)", detail)
                    if m:
                        cur = int(m.group(1))
                        target_n = max(1, cur - 1)
                if not target_n:
                    raise ValueError("could not determine target cycle number")
                moved, err = _archive_orphans(league, target_n, orphan_ids=None)
                if err:
                    _maintenance_log(league, kind, detail, "failed", result=err)
                    outcomes.append(f"{league}:missing_archive_cycle:fail:{err}")
                else:
                    _maintenance_log(league, kind, detail, "fixed",
                        result=f"archived cycle-{target_n}: moved {len(moved)} sprint dirs")
                    outcomes.append(f"{league}:missing_archive_cycle:fixed:{len(moved)}")
            except Exception as e:
                _maintenance_log(league, kind, detail, "failed", result=str(e))
                outcomes.append(f"{league}:missing_archive_cycle:fail:{e}")

        elif kind == "orphan_results":
            # Safe: move orphan sprint dirs from results/ into archive/cycle-(current-1)/.
            # Never touches cycle_state.json, never modifies sprint counters.
            try:
                current_n, _ = _current_cycle_sprints(league)
                target_n = max(1, current_n - 1)
                orphan_ids = a.get("orphan_ids") or None
                moved, err = _archive_orphans(league, target_n, orphan_ids=orphan_ids)
                if err:
                    _maintenance_log(league, kind, detail, "failed", result=err)
                    outcomes.append(f"{league}:orphan_results:fail:{err}")
                else:
                    _maintenance_log(league, kind, detail, "fixed",
                        result=f"archived into cycle-{target_n}: moved {len(moved)} orphan dirs")
                    outcomes.append(f"{league}:orphan_results:fixed:{len(moved)}")
            except Exception as e:
                _maintenance_log(league, kind, detail, "failed", result=str(e))
                outcomes.append(f"{league}:orphan_results:fail:{e}")

        else:
            # Remaining risky fixes (phantom_sprint, cycle_state_missing, unknown) — escalate with dedupe.
            dedupe_key = f"{league}|{kind}|{detail}"
            if _should_escalate(dedupe_key):
                write_escalation_log("syn_sprint_integrity", league, 0,
                    f"{kind}: {detail} | hint: {hint}")
                _maintenance_log(league, kind, detail, "escalated", result="logged to loki_escalation_log for human review")
                outcomes.append(f"{league}:{kind}:escalated")
            else:
                outcomes.append(f"{league}:{kind}:escalation_suppressed_cooldown")

    return outcomes



def process_pending_actions():
    if not os.path.exists(LOKI_PENDING_ACTIONS):
        return
    with open(LOKI_PENDING_ACTIONS) as f:
        entries = [json.loads(l) for l in f if l.strip()]
    unprocessed = [e for e in entries if not e.get("processed")]
    if not unprocessed:
        return
    print(f"[loki] {len(unprocessed)} pending SYN-Mimir action(s)")
    for entry in unprocessed:
        league  = entry.get("league", "unknown")
        results = []
        for action in entry.get("actions", []):
            atype = action.get("type")
            if atype == "restart_service":
                unit = action.get("unit", "")
                try:
                    subprocess.run(["systemctl", "restart", unit], timeout=15, check=False)
                    results.append(f"restarted:{unit}")
                except Exception:
                    results.append(f"restart_fail:{unit}")
            elif atype == "update_constant":
                const  = action.get("constant", "")
                subkey = action.get("subkey")
                newval = action.get("new_value")
                if const in ALLOWED_CONSTANTS and newval is not None:
                    ok, desc = apply_constant_change(const, subkey, newval)
                    status = "ok" if ok else "skip"
                    results.append(f"constant:{status}:{desc[:60]}")
                else:
                    results.append(f"constant:blocked:{const}")
            elif atype == "structural":
                ok, desc = apply_structural_change(
                    league, action.get("description", ""), action.get("patch", []),
                )
                status = "ok" if ok else "fail"
                results.append(f"structural:{status}:{desc[:60]}")
                print(f"  [loki/pending] structural: {desc}")
            elif atype == "sprint_integrity_fix":
                anoms = action.get("anomalies", [])
                fix_results = _apply_sprint_integrity_fix(anoms)
                results.extend(fix_results)
            elif atype == "escalate":
                esc_desc = action.get("description", "")
                write_escalation_log("syn_alert", league, 0, esc_desc)
                results.append(f"escalated:{esc_desc[:50]}")
        entry["processed"]    = True
        entry["processed_ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
        entry["results"]      = results
    with open(LOKI_PENDING_ACTIONS, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


# ── State tracking ─

def load_processed():
    """Return set of (ts, league) tuples LOKI has already handled."""
    if not os.path.exists(LOKI_LOG):
        return set()
    processed = set()
    with open(LOKI_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                processed.add((e["mimir_ts"], e["league"]))
            except Exception:
                pass
    return processed


def write_loki_log(mimir_ts, league, gen, actions):
    entry = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "mimir_ts": mimir_ts,
        "league":   league,
        "gen":      gen,
        "actions":  actions,
        "dry_run":  DRY_RUN,
    }
    if not DRY_RUN:
        with open(LOKI_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    else:
        print(f"[dry-run] Would log: {json.dumps(entry)}")


def write_escalation_log(mimir_ts, league, gen, description):
    entry = {
        "ts":          datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "mimir_ts":    mimir_ts,
        "league":      league,
        "generation":  gen,
        "description": description,
        "phase":       2,
    }
    if not DRY_RUN:
        with open(LOKI_ESC_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    print(f"  [loki] Phase 2 escalation logged: {description[:80]}")


# ── Git and service operations ─────────────────────────────────────────────────

def git_commit(files, message):
    if DRY_RUN:
        print(f"[dry-run] Would commit {files}: {message}")
        return True
    try:
        subprocess.run(
            ["git", "-C", WORKSPACE, "add"] + files,
            check=True, capture_output=True,
        )
        diff = subprocess.run(
            ["git", "-C", WORKSPACE, "diff", "--cached", "--quiet"],
            capture_output=True,
        )
        if diff.returncode == 0:
            print("  [loki] Nothing staged — no commit needed.")
            return False
        subprocess.run(
            ["git", "-C", WORKSPACE, "commit", "-m", message],
            check=True, capture_output=True,
        )
        print(f"  [loki] Committed: {message}")
        return True
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if e.stderr else str(e)
        print(f"  [loki] git error: {stderr}")
        return False


def restart_service(league):
    service = f"odin_{league}.service"
    if DRY_RUN:
        print(f"[dry-run] Would restart {service}")
        return True
    try:
        subprocess.run(["systemctl", "restart", service], check=True, capture_output=True)
        print(f"  [loki] Restarted {service}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [loki] Failed to restart {service}: {e}")
        return False


# ── Code change detection and application ─────────────────────────────────────

def detect_code_change_keywords(analysis_text):
    """Quick keyword scan — True if analysis likely discusses code changes."""
    text_lower = analysis_text.lower()
    for kw in CODE_CHANGE_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False


def classify_code_change(analysis_text, league):
    """
    Use Haiku to identify specific code change request from Mimir analysis.
    Returns dict with type: "none" | "constant" | "structural"
    """
    prompt = (
        f"Analyze this Mimir crypto strategy research report for code changes "
        f"needed in odin_researcher_v2.py.\n\n"
        f"MIMIR ANALYSIS ({league.upper()}):\n{analysis_text[:3000]}\n\n"
        f"Constants in odin_researcher_v2.py that can be changed:\n"
        f'- MIN_TRADES = {{"day": 50, "swing": 45}}  (minimum trades per strategy)\n'
        f"- POPULATION_SIZE = 10  (elite population size)\n"
        f"- SUSPICIOUS_SHARPE = 3.5  (reject overfitted strategies above this)\n"
        f"- STALL_ALERT_GENS = 300  (alert after N consecutive non-improving gens)\n\n"
        f"Does the analysis request changing one of these constants? Or structural code changes?\n\n"
        f"Output ONLY a JSON object, no explanation:\n"
        f'{{"type": "none"}}\n'
        f'{{"type": "constant", "constant": "MIN_TRADES", "subkey": "day", "new_value": 200, "reason": "..."}}\n'
        f'{{"type": "constant", "constant": "POPULATION_SIZE", "subkey": null, "new_value": 15, "reason": "..."}}\n'
        f'{{"type": "structural", "description": "brief description of structural change needed"}}'
    )
    try:
        response = call_gemini(prompt)
        match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"type": "none"}
    except Exception as e:
        print(f"  [loki] Gemini classification error: {e}")
        return {"type": "none"}


def apply_constant_change(constant, subkey, new_value):
    """
    Apply a simple constant change to odin_researcher_v2.py using regex.
    Returns (success: bool, description: str)
    """
    if constant not in ALLOWED_CONSTANTS:
        return False, f"{constant} not in LOKI allowed-constants whitelist"
    # Item 4: SWING_MIN_TRADES is immutable - block any swing subkey change
    if constant == "MIN_TRADES" and subkey == "swing":
        return False, "[LOKI_BLOCKED] MIN_TRADES[swing] is immutable — modify SWING_MIN_TRADES in code directly"

    with open(RESEARCHER) as f:
        content = f.read()

    original = content

    if subkey:
        # Dict constant: MIN_TRADES = {"day": 50, "swing": 45}
        pattern = rf'({re.escape(constant)}\s*=\s*\{{[^}}]*"{re.escape(subkey)}"\s*:\s*)\d+'
        replacement = rf'\g<1>{new_value}'
        new_content = re.sub(pattern, replacement, content)
    else:
        # Simple assignment: POPULATION_SIZE = 10
        pattern = rf'^({re.escape(constant)}\s*=\s*)\S+$'
        replacement = rf'\g<1>{new_value}'
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    if new_content == original:
        return False, f"Regex pattern for {constant} not found — no change made"

    if not DRY_RUN:
        backup = RESEARCHER + f".loki_{datetime.now().strftime('%Y%m%d_%H%M')}.bak"
        shutil.copy2(RESEARCHER, backup)
        with open(RESEARCHER, "w") as f:
            f.write(new_content)

    label = f"{constant}[{subkey}]" if subkey else constant
    return True, f"Changed {label} -> {new_value}"


# ── PM-specific helpers ───────────────────────────────────────────────────────

def classify_freya_change(analysis_text):
    """Use Haiku to identify constant changes needed in freya_researcher.py."""
    prompt = (
        "Analyze this Mimir prediction markets research report for code changes "
        "needed in freya_researcher.py.\n\n"
        f"MIMIR ANALYSIS:\n{analysis_text[:3000]}\n\n"
        "Constants in freya_researcher.py that can be changed:\n"
        "- MIN_BETS = 20  (minimum bets required for valid simulation)\n"
        "- POPULATION_SIZE = 5  (elite population size)\n"
        "CRITICAL: freya_researcher.py must have ZERO tg_send() call sites. tg_send() in research scripts routes to SYN inbox only."
        "Does the analysis request changing one of these constants?\n\n"
        "Output ONLY a JSON object:\n"
        '{"type": "none"}\n'
        '{"type": "constant", "constant": "MIN_BETS", "subkey": null, "new_value": 30, "reason": "..."}\n'
        '{"type": "structural", "description": "brief description"}'
    )
    try:
        response = call_gemini(prompt)
        match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"type": "none"}
    except Exception as e:
        print(f"  [loki] Gemini PM classification error: {e}")
        return {"type": "none"}


def apply_freya_constant(constant, new_value):
    """Apply a simple constant change to freya_researcher.py."""
    if constant not in FREYA_ALLOWED_CONSTS:
        return False, f"{constant} not in FREYA allowed-constants whitelist"
    with open(FREYA_RESEARCHER) as f:
        content = f.read()
    original = content
    pattern  = rf'^({re.escape(constant)}\s*=\s*)\S+$'
    new_content = re.sub(pattern, rf'\g<1>{new_value}', content, flags=re.MULTILINE)
    if new_content == original:
        return False, f"Regex pattern for {constant} not found — no change made"
    if not DRY_RUN:
        backup = FREYA_RESEARCHER + f".loki_{datetime.now().strftime('%Y%m%d_%H%M')}.bak"
        shutil.copy2(FREYA_RESEARCHER, backup)
        with open(FREYA_RESEARCHER, "w") as f:
            f.write(new_content)
    return True, f"Changed {constant} -> {new_value}"



def loki_inject_freya_strategy(gen):
    """Inject current FREYA best_strategy into mist/kara/thrud at every Mimir milestone."""
    best_path = os.path.join(PM_RESEARCH_DIR, "best_strategy.yaml")
    if not os.path.exists(best_path):
        print("  [loki] inject: no best_strategy.yaml yet — skipping")
        return []

    with open(best_path) as f:
        best = yaml.safe_load(f)

    cat     = best.get("category", "world_events")
    persona = PM_PERSONAS.get(cat, PM_PERSONAS["world_events"])
    injected = []

    for i, bot_name in enumerate(FREYA_SLOTS):
        strat_path = os.path.join(PM_FLEET_DIR, bot_name, "strategy.yaml")
        if not os.path.exists(os.path.dirname(strat_path)):
            print("  [loki] inject: " + bot_name + " fleet dir missing — skipping")
            continue

        edge_base = best.get("min_edge_pts", 0.08)
        if i == 1:
            edge = round(min(0.25, edge_base + 0.03), 3)   # kara: conservative
        elif i == 2:
            edge = round(max(0.03, edge_base - 0.02), 3)   # thrud: aggressive
        else:
            edge = edge_base                                # mist: exact champion

        strategy = {
            "name":           bot_name,
            "category":       cat,
            "type":           "opinion",
            "description":    "FREYA research slot — gen " + str(gen) + " evolved strategy",
            "prompt_persona": persona,
            "market_filter": {
                "include_keywords":    list(best.get("include_keywords", [])),
                "exclude_keywords":    list(best.get("exclude_keywords", [])),
                "price_range":         list(best.get("price_range", [0.05, 0.90])),
                "min_liquidity_usd":   best.get("min_liquidity_usd", 500),
                "max_days_to_resolve": best.get("max_days_to_resolve", 30),
            },
            "edge": {
                "min_edge_pts":     edge,
                "min_confidence":   "medium",
                "max_positions":    8,
                "max_position_pct": best.get("max_position_pct", 0.10),
            },
            "risk": {
                "stop_if_down_pct": 20,
                "starting_capital": 1000.0,
            },
        }

        if not DRY_RUN:
            with open(strat_path, "w") as f:
                yaml.dump(strategy, f, default_flow_style=False, allow_unicode=True)

        print("  [loki] inject: " + bot_name + " <- gen " + str(gen) + " champion (cat=" + cat + ", edge=" + str(edge) + ")")
        injected.append(bot_name)

    if injected and not DRY_RUN:
        rel_paths = [os.path.relpath(os.path.join(PM_FLEET_DIR, b, "strategy.yaml"), WORKSPACE)
                     for b in injected]
        git_commit(rel_paths, "[loki] MIMIR/PM Gen " + str(gen) + ": inject FREYA champion -> " + ", ".join(injected))

    return injected

def process_pm_entry(entry):
    """Handle PM league Mimir entries."""
    ts              = entry.get("ts", "")
    gen             = entry.get("generation", "?")
    analysis        = entry.get("analysis", "")
    program_updated = entry.get("program_updated", False)
    actions         = []

    print(f"\n[loki] MIMIR/PM Gen {gen} ({ts})")

    # Step 1: Commit program.md
    program_path = os.path.join(PM_RESEARCH_DIR, "program.md")
    if program_updated and os.path.exists(program_path):
        rel_path  = os.path.relpath(program_path, WORKSPACE)
        committed = git_commit(
            [rel_path],
            f"[loki] MIMIR/PM Gen {gen}: apply program.md update",
        )
        actions.append("pm/program.md committed" if committed else "pm/program.md already committed")
    else:
        print(f"  [loki] program_updated={program_updated} — no program.md commit")

    # Step 2: Check for freya_researcher.py constant changes
    text_lower = analysis.lower()
    has_code_kw = any(kw.lower() in text_lower for kw in PM_CODE_CHANGE_KEYWORDS)
    if has_code_kw:
        print(f"  [loki] PM code change keywords found — classifying...")
        change = classify_freya_change(analysis)
        print(f"  [loki] PM classification: {change}")
        if change.get("type") == "constant":
            constant  = change.get("constant", "")
            new_value = change.get("new_value")
            reason    = change.get("reason", "")
            if constant in FREYA_ALLOWED_CONSTS and new_value is not None:
                success, desc = apply_freya_constant(constant, new_value)
                if success:
                    rel_freya = os.path.relpath(FREYA_RESEARCHER, WORKSPACE)
                    git_commit(
                        [rel_freya],
                        f"[loki] MIMIR/PM Gen {gen}: {desc} — {reason[:60]}",
                    )
                    if not DRY_RUN:
                        try:
                            subprocess.run(["systemctl", "restart", "freya.service"],
                                           check=True, capture_output=True)
                            print("  [loki] Restarted freya.service")
                        except Exception as e:
                            print(f"  [loki] freya.service restart failed: {e}")
                    actions.append(f"freya_code: {desc}")
                else:
                    actions.append(f"freya_code-skip: {desc}")
        elif change.get("type") == "structural":
            desc = change.get("description", "see Mimir analysis")
            ok, patch_desc = apply_structural_change("pm", desc, entry.get("patch", []))
            if ok:
                actions.append(f"structural: {patch_desc}")
            else:
                write_escalation_log(ts, "pm", gen, desc)
                actions.append(f"escalated(Phase2): {patch_desc[:60]}")
    else:
        print(f"  [loki] No PM code change keywords — program.md only")

    # Step 3: Inject current best strategy into mist/kara/thrud
    injected = loki_inject_freya_strategy(gen)
    if injected:
        actions.append("freya_inject: " + ", ".join(injected))
    else:
        actions.append("freya_inject: skipped")

    write_loki_log(ts, "pm", gen, actions)



# ── Cycle End Restructure ──────────────────────────────────────────────────────

CYCLE_REVIEW_LOG = os.path.join(RESEARCH, "loki_cycle_review_log.jsonl")

# All 5 active leagues. Autobots excluded from strategy adjustment.
CYCLE_LEAGUE_CONFIGS = {
    "day": {
        "cycle_state":  os.path.join(WORKSPACE, "competition", "cycle_state.json"),
        "leaderboard":  os.path.join(WORKSPACE, "competition", "leaderboard.json"),
        "fleet_dir":    os.path.join(WORKSPACE, "fleet"),
        "strategy_fmt": "day_conditions",
        "advance_cmd":  ["python3", os.path.join(WORKSPACE, "cycle_advance.py")],
        "start_cmd":    [None],   # day restart handled by cron — no explicit start needed
        "autobots":     {"autobotday"},
    },
    "futures_day": {
        "cycle_state":  os.path.join(WORKSPACE, "competition", "futures_day", "cycle_state.json"),
        "leaderboard":  os.path.join(WORKSPACE, "competition", "futures_day", "futures_day_leaderboard.json"),
        "fleet_dir":    os.path.join(WORKSPACE, "fleet", "futures_day"),
        "strategy_fmt": "day_conditions",
        "advance_cmd":  None,   # inline advance
        "start_cmd":    [None],  # futures_day restart handled by cron
        "autobots":     {"autobotdayfutures"},
    },
    "swing": {
        "cycle_state":  os.path.join(WORKSPACE, "competition", "swing", "swing_cycle_state.json"),
        "leaderboard":  os.path.join(WORKSPACE, "competition", "swing", "swing_leaderboard.json"),
        "fleet_dir":    os.path.join(WORKSPACE, "fleet", "swing"),
        "strategy_fmt": "swing_conditions",
        "advance_cmd":  ["python3", os.path.join(WORKSPACE, "swing_cycle_advance.py")],
        "start_cmd":    "swing_needs_cycle",   # sentinel: built dynamically with new cycle num
        "autobots":     {"autobotswing"},
    },
    "futures_swing": {
        "cycle_state":  os.path.join(WORKSPACE, "competition", "futures_swing", "cycle_state.json"),
        "leaderboard":  os.path.join(WORKSPACE, "competition", "futures_swing", "futures_swing_leaderboard.json"),
        "fleet_dir":    os.path.join(WORKSPACE, "fleet", "futures_swing"),
        "strategy_fmt": "swing_conditions",
        "advance_cmd":  None,   # inline advance
        "start_cmd":    ["python3", os.path.join(WORKSPACE, "futures_swing_restart.py")],
        "autobots":     {"autobotswingfutures"},
    },
    "pm": {
        "cycle_state":  os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_cycle_state.json"),
        "leaderboard":  os.path.join(WORKSPACE, "competition", "polymarket", "polymarket_leaderboard.json"),
        "fleet_dir":    os.path.join(WORKSPACE, "fleet", "polymarket"),
        "strategy_fmt": "pm",
        "advance_cmd":  ["python3", os.path.join(WORKSPACE, "polymarket_cycle_advance.py")],
        "start_cmd":    None,   # advance includes sprint start
        "autobots":     {"mist", "kara", "thrud"},
    },
}


def load_cycle_review_log():
    """Return set of (league, cycle) whose strategies have already been adjusted this cycle."""
    if not os.path.exists(CYCLE_REVIEW_LOG):
        return set()
    seen = set()
    with open(CYCLE_REVIEW_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                seen.add((e["league"], e["cycle"]))
            except Exception:
                pass
    return seen


def write_cycle_review_entry(league, cycle, actions):
    entry = {
        "ts":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "league":  league,
        "cycle":   cycle,
        "actions": actions,
        "dry_run": DRY_RUN,
    }
    if not DRY_RUN:
        with open(CYCLE_REVIEW_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    else:
        print(f"  [dry-run] cycle review log: {json.dumps(entry)}")


def build_restructure_prompt(bot_name, perf, strategy_yaml, fmt):
    stats = "\n".join([
        f"Cumulative PnL: {perf.get('cumulative_pnl_usd', 0):.2f} USD ({perf.get('cumulative_pnl_pct', 0):.1f}%)",
        f"Win rate: {perf.get('overall_win_rate', 0):.1f}%",
        f"Total trades: {perf.get('total_trades', 0)}",
        f"Total fees: {perf.get('total_fees_usd', 0):.2f} USD",
        f"Best sprint: {perf.get('best_sprint_pnl_pct', 0):.1f}%",
        f"Worst sprint: {perf.get('worst_sprint_pnl_pct', 0):.1f}%",
        f"Sprint wins: {perf.get('sprint_wins', 0)}",
    ])
    if fmt == "day_conditions":
        return "\n".join([
            "You are tuning a losing intraday crypto trading bot (24h sprints, 5-min ticks).",
            "Make targeted changes to improve performance. Output ONLY the complete updated YAML — no explanation, no markdown.",
            "",
            f"BOT: {bot_name}",
            f"PERFORMANCE (full cycle):\n{stats}",
            "",
            f"CURRENT STRATEGY YAML:\n{strategy_yaml}",
            "",
            "RULES:",
            "- Do NOT change: name, style, inspiration, pairs list, fee_rate, league, leverage",
            "- You MAY change: position.size_pct, position.max_open, entry conditions,",
            "  exit.take_profit_pct, exit.stop_loss_pct, exit.timeout_minutes, risk thresholds",
            "- Use period_minutes (NOT period_hours) for all indicators",
            "- Available indicators: trend, price_vs_ema, macd_signal, rsi, momentum_accelerating,",
            "  volume_above_avg, price_vs_vwap, bollinger_position",
            "- Day league typical ranges: TP 0.5-3%, SL 0.3-1.5%, timeout 30-180min",
            "- Overtrading (many trades, negative PnL): reduce max_open, add volume_above_avg",
            "- 0% win rate: reduce max_open, add tighter RSI filter",
            "",
            "Output the complete YAML only:",
        ])
    elif fmt == "swing_conditions":
        return "\n".join([
            "You are tuning a losing crypto swing trading bot (7-day sprints).",
            "Make targeted changes to improve performance. Output ONLY the complete updated YAML — no explanation, no markdown.",
            "",
            f"BOT: {bot_name}",
            f"PERFORMANCE (full cycle):\n{stats}",
            "",
            f"CURRENT STRATEGY YAML:\n{strategy_yaml}",
            "",
            "RULES:",
            "- Do NOT change: name, style, inspiration, pairs list, fee_rate, league, leverage",
            "- You MAY change: position.size_pct, position.max_open, entry conditions,",
            "  exit.take_profit_pct, exit.stop_loss_pct, exit.timeout_hours, risk thresholds",
            "- Use period_hours (NOT period_minutes) for swing indicators",
            "- Available indicators: trend, price_vs_ema, macd_signal, rsi, momentum_accelerating,",
            "  volume_above_avg, price_vs_vwap, bollinger_position",
            "- bollinger_position values: above_upper, above_middle, below_middle, below_lower",
            "- volume_above_avg: no period_hours, operator eq, value true",
            "- Overtrading: reduce max_open to 2, add volume_above_avg",
            "- 0% win rate: reduce take_profit_pct; SL too tight: increase stop_loss_pct",
            "",
            "Output the complete YAML only:",
        ])
    elif fmt == "pm":
        return "\n".join([
            "You are tuning a losing prediction markets bot.",
            "Make targeted changes to improve performance. Output ONLY the complete updated YAML — no explanation, no markdown.",
            "",
            f"BOT: {bot_name}",
            f"PERFORMANCE (full cycle):\n{stats}",
            "",
            f"CURRENT STRATEGY YAML:\n{strategy_yaml}",
            "",
            "RULES:",
            "- Do NOT change: name, category, type, description, prompt_persona",
            "- You MAY change: market_filter.price_range [min,max], market_filter.min_liquidity_usd,",
            "  market_filter.max_days_to_resolve, edge.min_edge_pts (0.03-0.25),",
            "  edge.max_positions, edge.max_position_pct",
            "- 0% win rate: increase min_edge_pts significantly",
            "- Low win rate + many trades: tighten price_range to [0.15, 0.85], reduce max_positions",
            "",
            "Output the complete YAML only:",
        ])
    return ""


def adjust_bot_strategy(bot_name, perf, fleet_dir, fmt):
    """Use Gemini Flash Lite to generate an improved strategy for a losing bot."""
    strat_path = os.path.join(fleet_dir, bot_name, "strategy.yaml")
    if not os.path.exists(strat_path):
        return False, f"{bot_name}: strategy.yaml not found"

    with open(strat_path) as f:
        strategy_yaml = f.read()

    prompt = build_restructure_prompt(bot_name, perf, strategy_yaml, fmt)
    if not prompt:
        return False, f"{bot_name}: unsupported fmt {fmt}"

    try:
        new_yaml_str = call_gemini(prompt, max_tokens=1500, temperature=0.2)
    except Exception as e:
        return False, f"{bot_name}: Gemini failed: {e}"

    # Strip markdown fencing if Gemini adds it despite instructions
    lines = new_yaml_str.splitlines()
    if lines and lines[0].startswith("```"):
        lines = [l for l in lines if not l.startswith("```")]
        new_yaml_str = "\n".join(lines)

    try:
        new_data = yaml.safe_load(new_yaml_str)
    except Exception as e:
        return False, f"{bot_name}: YAML parse failed: {e}"

    if not isinstance(new_data, dict):
        return False, f"{bot_name}: Gemini returned non-dict"

    if new_data.get("name") != bot_name:
        return False, f"{bot_name}: Gemini changed name to '{new_data.get('name')}' — rejected"

    if DRY_RUN:
        print(f"  [dry-run] Would write adjusted strategy for {bot_name}")
        return True, f"{bot_name}: adjusted (dry-run)"

    backup = strat_path + f".pre_cycle_{datetime.now().strftime('%Y%m%d_%H%M')}.bak"
    shutil.copy2(strat_path, backup)
    with open(strat_path, "w") as f:
        f.write(new_yaml_str.rstrip() + "\n")
    return True, f"{bot_name}: strategy adjusted"


def run_cycle_advance_and_start(league, cfg, old_cycle):
    """Run advance + start for a league after strategies have been adjusted."""
    actions = []

    advance_cmd = cfg.get("advance_cmd")
    if advance_cmd:
        if DRY_RUN:
            print(f"  [dry-run] Would run: {os.path.basename(advance_cmd[-1])}")
            actions.append("cycle_advanced (dry-run)")
        else:
            r = subprocess.run(advance_cmd, capture_output=True, text=True, cwd=WORKSPACE)
            if r.returncode == 0:
                print(f"  [loki] Cycle advance OK")
                actions.append("cycle_advanced")
            else:
                print(f"  [loki] Cycle advance FAILED: {r.stderr[:150]}")
                tg_send(f"[LOKI] {league.upper()} cycle advance FAILED: {r.stderr[:100]}", severity="error")
                return actions   # abort — don't start if advance failed
    else:
        # Inline advance for leagues without a dedicated advance script
        try:
            with open(cfg["cycle_state"]) as f:
                cs = json.load(f)
            cs["cycle"]            = old_cycle + 1
            cs["sprint_in_cycle"]  = 0
            cs["status"]           = "active"
            cs["cycle_started_at"] = None
            cs["sprints"]          = []
            if not DRY_RUN:
                with open(cfg["cycle_state"], "w") as f:
                    json.dump(cs, f, indent=2)
            print(f"  [loki] {league}: cycle {old_cycle} -> {old_cycle + 1} (inline advance)")
            actions.append(f"cycle_advanced_inline: {old_cycle}->{old_cycle + 1}")
        except Exception as e:
            print(f"  [loki] Inline advance failed [{league}]: {e}")
            tg_send(f"[LOKI] {league.upper()} inline advance FAILED: {e}", severity="error")
            return actions

    # Start command
    start_cmd = cfg.get("start_cmd")
    if start_cmd == "swing_needs_cycle":
        new_cycle = old_cycle + 1
        start_cmd = [
            "python3", os.path.join(WORKSPACE, "swing_competition_start.py"),
            "--cycle", str(new_cycle), "--sprint-in-cycle", "1",
        ]
    # [None] sentinel means cron handles restart; skip explicit start
    if start_cmd and start_cmd != [None]:
        if DRY_RUN:
            print(f"  [dry-run] Would start: {os.path.basename(start_cmd[1])}")
            actions.append("sprint_started (dry-run)")
        else:
            r = subprocess.run(start_cmd, capture_output=True, text=True, cwd=WORKSPACE)
            if r.returncode == 0:
                print(f"  [loki] Cycle {old_cycle + 1} sprint 1 started")
                actions.append("sprint_started")
            else:
                print(f"  [loki] Sprint start FAILED: {r.stderr[:150]}")
                tg_send(f"[LOKI] {league.upper()} sprint start FAILED: {r.stderr[:100]}", severity="error")
    elif start_cmd == [None]:
        print(f"  [loki] {league}: start handled by cron/watchdog")
        actions.append("start_deferred_to_cron")

    # Pin regression_watch baselines for the new cycle (fire-and-forget — backtest can take minutes)
    if league in ("day", "futures_day", "swing", "futures_swing") and not DRY_RUN:
        try:
            log_path = os.path.join(WORKSPACE, "competition", "regression_watch.log")
            subprocess.Popen(
                ["nohup", "python3", os.path.join(WORKSPACE, "regression_watch.py"),
                 "--refresh-baseline", "--league", league],
                stdout=open(log_path, "a"), stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            actions.append("regression_baseline_refresh_queued")
        except Exception as e:
            print(f"  [loki] regression baseline refresh queue failed: {e}")

    return actions


def handle_cycle_review(league, cfg, cycle):
    """Adjust losing bots for one league, then advance the cycle."""
    print(f"\n[loki] CYCLE REVIEW: {league.upper()} Cycle {cycle}")
    all_actions = []

    try:
        with open(cfg["leaderboard"]) as f:
            lb = json.load(f)
    except Exception as e:
        print(f"  [loki] Cannot load leaderboard [{league}]: {e}")
        return

    rankings  = lb.get("rankings", [])
    autobots  = cfg.get("autobots", set())
    fleet_dir = cfg["fleet_dir"]
    fmt       = cfg["strategy_fmt"]

    losers = [r for r in rankings
              if r["bot"] not in autobots and r.get("cumulative_pnl_usd", 0) < 0]

    if not losers:
        print(f"  [loki] No losers — all bots profitable")
        all_actions.append("no_losers")
    else:
        print(f"  [loki] {len(losers)} loser(s): {[r['bot'] for r in losers]}")
        adjusted, failed_list = [], []
        for r in losers:
            bot = r["bot"]
            perf = {k: r.get(k, 0) for k in [
                "cumulative_pnl_usd", "cumulative_pnl_pct", "overall_win_rate",
                "total_trades", "total_fees_usd", "best_sprint_pnl_pct",
                "worst_sprint_pnl_pct", "sprint_wins",
            ]}
            ok, desc = adjust_bot_strategy(bot, perf, fleet_dir, fmt)
            print(f"  [loki]   {desc}")
            if ok:
                adjusted.append(bot)
            else:
                failed_list.append(desc)

        if adjusted:
            rel_paths = [
                os.path.relpath(os.path.join(fleet_dir, b, "strategy.yaml"), WORKSPACE)
                for b in adjusted
            ]
            git_commit(rel_paths,
                       f"[loki] {league.upper()} Cycle {cycle} restructure: {len(adjusted)} bots tuned")
            all_actions.append(f"adjusted: {', '.join(adjusted)}")
        if failed_list:
            all_actions.append(f"adjust_failed: {len(failed_list)}")

    # Write review log BEFORE advance (prevents re-applying strategies on LOKI retry)
    write_cycle_review_entry(league, cycle, all_actions)

    # Advance cycle + start sprint 1
    advance_actions = run_cycle_advance_and_start(league, cfg, cycle)
    all_actions.extend(advance_actions)

    tg_send(
        f"[LOKI] {league.upper()} Cycle {cycle} restructure: "
        f"{len(losers)} loser(s) tuned, Cycle {cycle + 1} started.",
        severity="info",
    )


def handle_all_cycle_reviews():
    """Check all 5 leagues for awaiting_review status and process each."""
    already_reviewed = load_cycle_review_log()

    for league, cfg in CYCLE_LEAGUE_CONFIGS.items():
        try:
            if not os.path.exists(cfg["cycle_state"]):
                continue
            with open(cfg["cycle_state"]) as f:
                cs = json.load(f)
            if cs.get("status") != "awaiting_review":
                continue
            # Skip restructure if manually flagged (e.g. manual strategy overhaul)
            if cs.get("skip_loki_restructure"):
                cycle = cs.get("cycle", 1)
                print(f"  [loki] {league.upper()} Cycle {cycle}: skip_loki_restructure set — {cs.get('skip_reason', 'no reason')}. Advancing without tuning.")
                # Remove the flag so next cycle proceeds normally
                cs.pop("skip_loki_restructure", None)
                cs.pop("skip_reason", None)
                with open(cfg["cycle_state"], "w") as wf:
                    json.dump(cs, wf, indent=2)
                write_cycle_review_entry(league, cycle, ["skipped: manual overhaul"])
                run_cycle_advance_and_start(league, cfg, cycle)
                continue
            cycle = cs.get("cycle", 1)
            if (league, cycle) in already_reviewed:
                # Strategies done — retry advance/start only (previous run may have failed mid-way)
                print(f"  [loki] {league.upper()} Cycle {cycle}: strategies done, retrying advance/start")
                run_cycle_advance_and_start(league, cfg, cycle)
                continue
            handle_cycle_review(league, cfg, cycle)
        except Exception as e:
            print(f"  [loki] Cycle review error [{league}]: {e}")


# ── Main processing ────────────────────────────────────────────────────────────

def process_entry(entry):
    league = entry.get("league", "")
    if league == "pm":
        process_pm_entry(entry)
        return
    # futures leagues handled same as spot leagues below

    ts              = entry.get("ts", "")
    gen             = entry.get("generation", "?")
    analysis        = entry.get("analysis", "")
    program_updated = entry.get("program_updated", False)

    league_up = league.upper()
    print(f"\n[loki] MIMIR/{league_up} Gen {gen} ({ts})")
    actions = []

    # Step 1: Commit program.md if Mimir updated it + register audit monitor
    program_path = os.path.join(RESEARCH, league, "program.md")
    if program_updated and os.path.exists(program_path):
        rel_path = os.path.relpath(program_path, WORKSPACE)
        committed = git_commit(
            [rel_path],
            f"[loki] MIMIR/{league_up} Gen {gen}: apply program.md update",
        )
        actions.append("program.md committed" if committed else "program.md already committed")
        # Snapshot baseline + register monitor so a bad rewrite gets auto-reverted.
        # MIMIR already wrote the new program.md; we preserve the prior version as
        # a pre-change backup for revert.
        try:
            ts_str = datetime.now().strftime("%Y%m%d_%H%M")
            prog_backup = program_path + f".pre_mimir_gen{gen}_{ts_str}.bak"
            # Use the most recent git blob for program.md as the pre-change state
            prior = subprocess.run(
                ["git", "-C", WORKSPACE, "show", f"HEAD~1:{rel_path}"],
                capture_output=True, text=True, timeout=10,
            )
            if prior.returncode == 0 and prior.stdout:
                with open(prog_backup, "w") as f:
                    f.write(prior.stdout)
                baseline = compute_league_metrics(league, last_n=50) or {}
                monitor = load_structural_monitor()
                # Preserve an existing code-patch monitor (same league) — both can coexist
                # by keying on kind via a composite league key.
                monitor[f"{league}__program"] = {
                    "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
                    "league":   league,
                    "unit":     SERVICE_MAP.get(league),
                    "backup":   prog_backup,
                    "target":   program_path,
                    "desc":     f"program.md rewrite gen {gen}",
                    "kind":     "program",
                    "baseline": baseline,
                }
                save_structural_monitor(monitor)
                actions.append("program.md audit registered")
            else:
                print(f"  [loki-audit] skipped monitor: no prior program.md blob in git (returncode={prior.returncode})")
        except Exception as e:
            print(f"  [loki-audit] failed to register program.md monitor: {e}")
    else:
        print(f"  [loki] program_updated={program_updated} -- no program.md commit")

    # Step 2: Check analysis for code changes to odin_researcher_v2.py
    if detect_code_change_keywords(analysis):
        print(f"  [loki] Code change keywords found — classifying with Haiku...")
        change = classify_code_change(analysis, league)
        print(f"  [loki] Classification: {change}")

        if change.get("type") == "constant":
            constant  = change.get("constant", "")
            subkey    = change.get("subkey")
            new_value = change.get("new_value")
            reason    = change.get("reason", "")

            if constant in ALLOWED_CONSTANTS and new_value is not None:
                success, desc = apply_constant_change(constant, subkey, new_value)
                if success:
                    rel_researcher = os.path.relpath(RESEARCHER, WORKSPACE)
                    git_commit(
                        [rel_researcher],
                        f"[loki] MIMIR/{league_up} Gen {gen}: {desc} — {reason[:60]}",
                    )
                    restart_service(league)
                    actions.append(f"code: {desc}")
                else:
                    actions.append(f"code-skip: {desc}")
            else:
                actions.append(f"code-skip: {constant} not in whitelist or value missing")

        elif change.get("type") == "structural":
            desc = change.get("description", "see Mimir analysis")
            ok, patch_desc = apply_structural_change(league, desc, entry.get("patch", []))
            if ok:
                actions.append(f"structural: {patch_desc}")
                print(f"  [loki] Structural change applied: {patch_desc}")
            else:
                # MIMIR's patch did not apply (usually stale anchor). Fire VIDAR
                # patch_repair before escalating to Chris — VIDAR will produce a
                # corrected patch, decline as "not actionable", or escalate.
                try:
                    subprocess.Popen(
                        ["python3", VIDAR_SCRIPT,
                         "--mode", "patch_repair",
                         "--league", league,
                         "--mimir-ts", ts],
                        stdout=open(os.path.join(RESEARCH, "vidar.log"), "a"),
                        stderr=subprocess.STDOUT,
                    )
                    actions.append(f"vidar_patch_repair_fired: {patch_desc[:50]}")
                except Exception as _e:
                    print(f"  [loki/vidar] patch_repair launch failed: {_e}")
                write_escalation_log(ts, league, gen, desc)
                actions.append(f"escalated(Phase2): {patch_desc[:60]}")
                print(f"  [loki] Structural escalated (VIDAR repair fired): {patch_desc}")
    else:
        print(f"  [loki] No code change keywords — program.md only")

    write_loki_log(ts, league, gen, actions)


def main():
    if DRY_RUN:
        print("[loki] *** DRY-RUN MODE — no changes will be applied ***")

    check_structural_monitors()  # verify recently patched services are alive
    process_pending_actions()    # execute actions queued by SYN-Mimir pipeline
    handle_all_cycle_reviews()

    if not os.path.exists(MIMIR_LOG):
        print("[loki] No mimir_log.jsonl — nothing to do")
        return

    processed = load_processed()

    new_entries = []
    with open(MIMIR_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            key = (entry.get("ts", ""), entry.get("league", ""))
            if key not in processed:
                new_entries.append(entry)

    if not new_entries:
        print("[loki] No new Mimir entries.")
        return

    count = len(new_entries)
    print(f"[loki] {count} new Mimir {'entry' if count == 1 else 'entries'} to process")

    for entry in new_entries:
        try:
            process_entry(entry)
        except Exception as e:
            league = entry.get("league", "?").upper()
            gen    = entry.get("generation", "?")
            print(f"  [loki] ERROR on MIMIR/{league} Gen {gen}: {e}")
            # Still mark processed to prevent infinite error loop
            write_loki_log(entry.get("ts", ""), entry.get("league", ""), entry.get("generation", "?"), [f"ERROR: {e}"])


if __name__ == "__main__":
    main()
