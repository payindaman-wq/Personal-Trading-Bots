#!/usr/bin/env python3
"""
sys_heartbeat.py — SYN system health monitor.

Run every 30 minutes via cron. Checks all leagues and services for problems,
attempts auto-remediation where safe, and alerts via Telegram.

Auto-fix (no approval needed): service restarts, Odin restart when Ollama stuck.
Everything else: Telegram alert directing Chris to address with Claude Code.
After any file change: git commit + push to origin/master.
"""
import json, os, subprocess, urllib.request, time, glob, hashlib
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")

WORKSPACE  = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/competition/heartbeat_state.json"
BOT_TOKEN  = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID    = "8154505910"

COOLDOWN_MIN        = 1440    # min gap between repeated alerts for the same problem (24h)
SERVICE_COOLDOWN_MIN = 1440
GEMINI_COOLDOWN_MIN = 1440   # Gemini quota alerts fire at most once per day
PAUSE_FLAG          = f"{WORKSPACE}/competition/heartbeat_paused"

# ── League definitions ──────────────────────────────────────────────────────

LEAGUES = [
    {
        "name":       "day",
        "tick_log":   f"{WORKSPACE}/competition/cron.log",
        "active_dir": f"{WORKSPACE}/competition/active",
        "interval":   5,    # minutes between ticks
        "stale_mul":  3,    # alert if log > interval × stale_mul minutes old
        "error_lines": 30,
    },
    {
        "name":       "swing",
        "tick_log":   f"{WORKSPACE}/competition/swing/tick.log",
        "active_dir": f"{WORKSPACE}/competition/swing/active",
        "interval":   30,
        "stale_mul":  3,
        "error_lines": 30,
    },
    {
        "name":       "arb",
        "tick_log":   f"{WORKSPACE}/competition/arb/tick.log",
        "active_dir": f"{WORKSPACE}/competition/arb/active",
        "interval":   30,
        "stale_mul":  3,
        "error_lines": 30,
    },
    {
        "name":       "spread",
        "tick_log":   f"{WORKSPACE}/competition/spread/tick.log",
        "active_dir": f"{WORKSPACE}/competition/spread/active",
        "interval":   30,
        "stale_mul":  3,
        "error_lines": 30,
    },
]

SERVICES = [
    {"name": "odin_day",   "unit": "odin_day.service"},
    {"name": "odin_swing", "unit": "odin_swing.service"},
    {"name": "polymarket",     "unit": "polymarket.service"},
    {"name": "polymarket_syn", "unit": "polymarket_syn.service"},
]

# ── State / cooldown ────────────────────────────────────────────────────────

def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_alerted": {}, "error_consecutive": {}}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def should_alert(state, key, cooldown_min=None):
    """Return True if cooldown has passed for this problem key."""
    if cooldown_min is None:
        cooldown_min = COOLDOWN_MIN
    last = state["last_alerted"].get(key)
    if not last:
        return True
    last_dt = datetime.fromisoformat(last)
    return datetime.now(timezone.utc) - last_dt > timedelta(minutes=cooldown_min)


def mark_alerted(state, key):
    state["last_alerted"][key] = datetime.now(timezone.utc).isoformat()


def clear_alert(state, key):
    """Remove a resolved problem so it fires immediately if it recurs."""
    state["last_alerted"].pop(key, None)


# ── Telegram ────────────────────────────────────────────────────────────────

def tg_send(msg):
    try:
        payload = json.dumps({
            "chat_id":    CHAT_ID,
            "text":       msg,
            "parse_mode": "HTML",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[tg_send] failed: {e}")


# ── Checks ──────────────────────────────────────────────────────────────────

def attempt_auto_restart(unit):
    """Restart a systemd unit. Returns True if active afterwards."""
    try:
        subprocess.run(["systemctl", "restart", unit], timeout=15, check=False)
        time.sleep(5)
        r = subprocess.run(["systemctl", "is-active", unit],
                           capture_output=True, text=True, timeout=5)
        return r.stdout.strip() == "active"
    except Exception as e:
        print(f"  [auto-restart] {unit} failed: {e}")
        return False


def git_commit_push(message):
    """Commit any dirty workspace files and push to remote. No-op if nothing changed."""
    try:
        subprocess.run(["git", "-C", WORKSPACE, "add", "-A"], timeout=30, check=False)
        dirty = subprocess.run(
            ["git", "-C", WORKSPACE, "diff", "--cached", "--quiet"], timeout=10
        )
        if dirty.returncode == 0:
            print(f"  [git] nothing to commit for: {message}")
            return
        subprocess.run(
            ["git", "-C", WORKSPACE, "commit", "-m", f"SYN auto-fix: {message}"],
            timeout=30, check=False
        )
        subprocess.run(["git", "-C", WORKSPACE, "push", "origin", "master"],
                       timeout=60, check=False)
        print(f"  [git] pushed: {message}")
    except Exception as e:
        print(f"  [git] push failed: {e}")



def check_tick_freshness(league):
    """Return problem string if tick log is stale, else None."""
    log = league["tick_log"]
    if not os.path.isfile(log):
        return f"tick log missing: {os.path.basename(log)}"
    age_sec = time.time() - os.path.getmtime(log)
    threshold_sec = league["interval"] * league["stale_mul"] * 60
    if age_sec > threshold_sec:
        age_min = int(age_sec / 60)
        return f"stale — last tick {age_min}m ago (expected every {league['interval']}m) — address with Claude Code"
    return None


def check_tick_errors(league):
    """Return last error snippet if recent log lines contain tracebacks/errors."""
    log = league["tick_log"]
    if not os.path.isfile(log):
        return None
    try:
        with open(log) as f:
            lines = f.readlines()
    except Exception:
        return None

    recent = lines[-league["error_lines"]:]
    error_keywords = ("Traceback", "KeyError", "AttributeError", "TypeError",
                      "ValueError", "Exception", "ERROR", "CRITICAL", "SyntaxError")
    hits = [l.rstrip() for l in recent if any(k in l for k in error_keywords)]
    if hits:
        snippet = hits[-1][:120]
        return f"errors in log — {snippet} — address with Claude Code"
    return None


def check_active_sprint(league):
    """Return problem string if no active sprint found."""
    active_dir = league["active_dir"]
    if not os.path.isdir(active_dir):
        return "active dir missing"
    entries = sorted(e for e in os.listdir(active_dir) if not e.startswith("."))
    if not entries:
        return "no active sprint"
    meta_path = os.path.join(active_dir, entries[-1], "meta.json")
    if not os.path.isfile(meta_path):
        return "no active sprint (no meta.json)"
    try:
        with open(meta_path) as f:
            meta = json.load(f)
        if meta.get("status") != "active":
            return f"sprint status={meta.get('status', '?')}"
    except Exception:
        return "meta.json unreadable"
    return None


def check_service(svc):
    """Return problem string if service is not active+running."""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", svc["unit"]],
            capture_output=True, text=True, timeout=5,
        )
        status = result.stdout.strip()
        if status != "active":
            return f"service {svc['unit']} is {status}"
    except Exception as e:
        return f"systemctl check failed: {e}"
    return None


def check_gemini_quota(state):
    """Warn if any Gemini key is exhausted or daily count is high."""
    state_path = f"{WORKSPACE}/competition/polymarket/auto_state.json"
    if not os.path.isfile(state_path):
        return None
    try:
        with open(state_path) as f:
            s = json.load(f)
        gd = s.get("gemini_daily", {})
        exhausted = gd.get("exhausted", [])
        counts    = gd.get("counts", [])
        if exhausted:
            return f"{len(exhausted)}/3 Gemini keys exhausted today — address with Claude Code"
        if counts and max(counts) > 1100:
            return f"Gemini key approaching daily limit ({max(counts)}/1200) — address with Claude Code"
    except Exception:
        pass
    return None




def check_odin_health(league):
    """Return problem string if Odin has had no successful generation in >6h."""
    results_path = f"{WORKSPACE}/research/{league}/results.tsv"
    if not os.path.exists(results_path):
        return None  # not started yet — service check covers this
    successful_statuses = {"new_best", "discarded", "rejected_lookahead"}
    last_success_ts = None
    with open(results_path) as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("gen")]
    if not lines:
        return None
    for line in lines:
        parts = line.split("	")
        if len(parts) >= 8:
            status = parts[5]
            ts_str = parts[7]
            if status in successful_statuses:
                last_success_ts = ts_str
    if last_success_ts:
        try:
            from datetime import timezone
            last_dt = datetime.fromisoformat(last_success_ts).replace(tzinfo=timezone.utc)
            age_h = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
            if age_h > 6:
                return f"no successful generation in {age_h:.1f}h"
        except Exception:
            pass
    return None


def check_odin_backtest_errors(league):
    """Alert if 3+ of the last 5 generations are backtest_error (fast data failure detection)."""
    results_path = f"{WORKSPACE}/research/{league}/results.tsv"
    if not os.path.exists(results_path):
        return None
    try:
        with open(results_path) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("gen")]
        recent = lines[-5:]
        if len(recent) < 3:
            return None
        errors = [l for l in recent if len(l.split("	")) > 5 and "error" in l.split("	")[5]]
        if len(errors) >= 3:
            parts = errors[-1].split("	")
            msg = parts[6][:100] if len(parts) > 6 else "backtest_error"
            return f"{len(errors)}/5 recent gens are backtest_error: {msg} — address with Claude Code"
    except Exception:
        pass
    return None


def check_program_halt(league):
    """Alert if program.md contains an active CRITICAL HALT directive."""
    prog_path = f"{WORKSPACE}/research/{league}/program.md"
    if not os.path.exists(prog_path):
        return None
    try:
        with open(prog_path) as f:
            content = f.read()
        if "CRITICAL HALT — ACTIVE" in content:
            return "program.md has active CRITICAL HALT — address with Claude Code"
    except Exception:
        pass
    return None


def check_research_stall(league):
    """Alert when a league research is structurally stuck with no viable progress.

    Fires if BOTH:
      - gens_since_best > 500 (500 gens without any improvement)
      - best Sharpe across all time is still negative
    This indicates a paradigm failure, not a tuning issue.
    """
    state_path   = f"{WORKSPACE}/research/{league}/gen_state.json"
    results_path = f"{WORKSPACE}/research/{league}/results.tsv"
    if not os.path.exists(state_path) or not os.path.exists(results_path):
        return None
    try:
        import json as _json
        state = _json.load(open(state_path))
        gens_since_best = state.get("gens_since_best", 0)
        total_gen       = state.get("gen", 0)
    except Exception:
        return None
    if gens_since_best < 500:
        return None
    # Check if best Sharpe ever achieved is still negative
    try:
        best_sharpe = -999.0
        with open(results_path) as f:
            for line in f:
                if not line.strip() or line.startswith("gen"):
                    continue
                parts = line.strip().split("	")
                if len(parts) >= 2:
                    try:
                        s = float(parts[1])
                        if s > best_sharpe:
                            best_sharpe = s
                    except ValueError:
                        pass
    except Exception:
        return None
    if best_sharpe >= 0:
        return None  # at least one positive Sharpe achieved — not a paradigm failure
    return (
        f"{gens_since_best} gens since last improvement — "
        f"best Sharpe ever: {best_sharpe:.2f} (never positive after {total_gen} gens) — "
        f"paradigm failure, consult Claude Code for full research rewrite"
    )

def check_polymarket_syn_freshness():
    """Check syn_tick.log freshness — service being 'active' doesn't mean it's ticking."""
    log = f"{WORKSPACE}/competition/polymarket/syn_tick.log"
    if not os.path.isfile(log):
        return "syn_tick.log missing"
    age_sec = time.time() - os.path.getmtime(log)
    if age_sec > 35 * 60:  # 15 min interval × 2.3
        return f"stale — last tick {int(age_sec/60)}m ago (expected every 15m) — address with Claude Code"
    return None




def check_disk_space():
    """Alert if disk usage on / exceeds 80%."""
    try:
        result = subprocess.run(["df", "/", "--output=pcent"],
                                capture_output=True, text=True, timeout=5)
        pct = int(result.stdout.strip().split("\n")[-1].strip().rstrip("%"))
        if pct >= 80:
            return f"disk {pct}% full — address with Claude Code"
    except Exception:
        pass
    return None


# ── Main ─────────────────────────────────────────────────────────────────────





def main():
    now_str = datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")
    print(f"[sys_heartbeat] {now_str}")


    if os.path.isfile(PAUSE_FLAG):
        print("  Paused — alerts suppressed. Delete heartbeat_paused to resume.")
        return

    state    = load_state()
    problems = []   # list of (key, message)
    resolved = []   # keys that were alerting but are now clear

    # ── League checks ──────────────────────────────────────────────────────
    for league in LEAGUES:
        name = league["name"]

        for check_fn, suffix in [
            (check_tick_freshness, "stale"),
            (check_tick_errors,    "errors"),
            (check_active_sprint,  "sprint"),
        ]:
            key = f"{name}_{suffix}"
            problem = check_fn(league)
            if problem:
                if suffix == "errors":
                    # Dedup: only alert after 2 consecutive runs with an error
                    ec = state.setdefault("error_consecutive", {})
                    ec[key] = ec.get(key, 0) + 1
                    if ec[key] >= 2 and should_alert(state, key):
                        problems.append((key, f"[{name.upper()}] {problem}"))
                else:
                    if should_alert(state, key):
                        problems.append((key, f"[{name.upper()}] {problem}"))
            else:
                if suffix == "errors":
                    state.setdefault("error_consecutive", {})[key] = 0
                    # Do NOT clear error cooldown on resolve — let 24h expire naturally
                    # This prevents transient errors from re-alerting every 30 min
                else:
                    if key in state["last_alerted"]:
                        resolved.append(key)
                    clear_alert(state, key)

    # ── Service checks — attempt auto-restart before alerting ────────────
    for svc in SERVICES:
        key     = f"svc_{svc['name']}"
        problem = check_service(svc)
        if problem:
            print(f"  [{svc['name']}] {problem} — attempting auto-restart...")
            restarted = attempt_auto_restart(svc["unit"])
            if restarted:
                git_commit_push(f"heartbeat auto-restarted {svc['unit']}")
                clear_alert(state, key)
                print(f"  [{svc['name']}] auto-restarted successfully")
            else:
                if should_alert(state, key, cooldown_min=SERVICE_COOLDOWN_MIN):
                    problems.append((key, f"[SERVICE] {problem} — auto-restart failed — address with Claude Code"))
        else:
            if key in state["last_alerted"]:
                resolved.append(key)
            clear_alert(state, key)

    # ── Odin researcher health — alert if no successful generation in >6h ─────────
    for vleague in ["day", "swing", "futures_day", "futures_swing"]:
        key     = f"odin_{vleague}_health"
        problem = check_odin_health(vleague)
        if problem:
            if should_alert(state, key):
                problems.append((key, f"[ODIN/{vleague.upper()}] {problem} — address with Claude Code"))
        else:
            if key in state["last_alerted"]:
                resolved.append(key)
            clear_alert(state, key)


    # ── Odin backtest error storm — alert within 1-2 heartbeats of sustained failures ──
    for vleague in ["day", "swing", "futures_day", "futures_swing"]:
        key     = f"odin_{vleague}_backtest_errors"
        problem = check_odin_backtest_errors(vleague)
        if problem:
            if should_alert(state, key):
                problems.append((key, f"[ODIN/{vleague.upper()}] {problem}"))
        else:
            clear_alert(state, key)

    # ── Program HALT directive — alert once per day if active ─────────────────
    for vleague in ["day", "swing", "futures_day", "futures_swing"]:
        key     = f"odin_{vleague}_program_halt"
        problem = check_program_halt(vleague)
        if problem:
            if should_alert(state, key):
                problems.append((key, f"[ODIN/{vleague.upper()}] {problem}"))
        else:
            clear_alert(state, key)

    # ── Research paradigm stall — alert when a league has never achieved positive Sharpe ──
    for vleague in ["day", "swing", "futures_day", "futures_swing"]:
        key     = f"odin_{vleague}_research_stall"
        problem = check_research_stall(vleague)
        if problem:
            if should_alert(state, key, cooldown_min=1440):  # once per day max
                problems.append((key, f"[ODIN/{vleague.upper()}] [RESEARCH_STALL] {problem}"))
        else:
            clear_alert(state, key)

    # ── Polymarket SYN tick freshness ──────────────────────────────────────
    key     = "polysyn_stale"
    problem = check_polymarket_syn_freshness()
    if problem:
        if should_alert(state, key):
            problems.append((key, f"[POLYMARKET_SYN] {problem}"))
    else:
        clear_alert(state, key)

    # ── Disk space ────────────────────────────────────────────────────────
    key     = "disk_space"
    problem = check_disk_space()
    if problem:
        if should_alert(state, key):
            problems.append((key, f"[SYSTEM] {problem}"))
    else:
        clear_alert(state, key)

    # ── Gemini quota check (4h cooldown, no clear-on-resolve — prevents flicker spam)
    key     = "gemini_quota"
    problem = check_gemini_quota(state)
    if problem:
        last = state["last_alerted"].get(key)
        if not last or datetime.now(timezone.utc) - datetime.fromisoformat(last) > timedelta(minutes=GEMINI_COOLDOWN_MIN):
            problems.append((key, f"[GEMINI] {problem}"))
    # intentionally not clearing on resolve — quota flickers; let cooldown expire naturally

    # ── SYN inbox — escalations from LOKI/other officers (critical/error only) ──
    inbox_path = f"{WORKSPACE}/syn_inbox.jsonl"
    inbox_offset_key = "syn_inbox_offset"
    inbox_offset = state.get(inbox_offset_key, 0)
    if os.path.exists(inbox_path):
        with open(inbox_path) as inbox_f:
            inbox_lines = inbox_f.readlines()
        new_lines = inbox_lines[inbox_offset:]
        state[inbox_offset_key] = len(inbox_lines)
        for line in new_lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                severity = entry.get("severity", "info")
                if severity in ("error", "critical"):
                    source = entry.get("source", "unknown").upper()
                    msg = entry.get("msg", "")[:200]
                    key = "inbox_" + hashlib.md5(f"{source}:{msg}".encode()).hexdigest()[:12]
                    if should_alert(state, key):
                        problems.append((key, f"[{source}] {msg}"))
            except Exception:
                pass

    # ── Send alerts ────────────────────────────────────────────────────────
    if problems:
        lines = [f"<b>SYN ALERT</b> — {now_str}", ""]
        for key, msg in problems:
            lines.append(f"• {msg}")
            mark_alerted(state, key)
            print(f"  ALERT: {msg}")
        tg_send("\n".join(lines))
    else:
        print("  All systems nominal.")

    save_state(state)


if __name__ == "__main__":
    main()
