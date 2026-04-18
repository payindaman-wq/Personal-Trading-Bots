#!/usr/bin/env python3
"""
day_daily_restart.py - Daily 09:00 UTC (2:00am PDT) restart for Day Trading League.

Called by cron: 0 9 * * *

Logic:
  - If no active sprint: start new 24h sprint, patch started_at to 09:00:00 UTC.
  - If active sprint >= 20h old: archive directly via competition_score.py,
    start new sprint, patch started_at to 09:00:00 UTC.
  - If active sprint < 20h old: skip (sprint started recently today, keep it).
"""
import os
import json
import subprocess
import sys
from datetime import datetime, timezone

WORKSPACE           = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
ACTIVE_DIR          = os.path.join(WORKSPACE, "competition", "active")
CYCLE_STATE_PATH    = os.path.join(WORKSPACE, "competition", "cycle_state.json")
START_SCRIPT        = "/root/.openclaw/skills/competition-start/scripts/competition_start.py"
SCORE_SCRIPT        = "/root/.openclaw/skills/competition-score/scripts/competition_score.py"
ODIN_BEST_DAY       = os.path.join(WORKSPACE, "research", "day", "best_strategy.yaml")
AUTOBOTDAY_STRATEGY = os.path.join(WORKSPACE, "fleet", "autobotday", "strategy.yaml")
LOKI_LOG            = os.path.join(WORKSPACE, "research", "loki_log.jsonl")


def load_cycle_state():
    try:
        with open(CYCLE_STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 7,
                "status": "active", "sprints": []}


def save_cycle_state(state):
    with open(CYCLE_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def find_active():
    if not os.path.isdir(ACTIVE_DIR):
        return None, None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None, None
    comp_dir  = os.path.join(ACTIVE_DIR, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None, None
    with open(meta_path) as f:
        meta = json.load(f)
    return (comp_dir, meta) if meta.get("status") == "active" else (None, None)


def hours_running(meta):
    started = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - started).total_seconds() / 3600


def write_loki_activity(league, actions):
    """Append an activity record to loki_log.jsonl for dashboard visibility."""
    entry = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "mimir_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "league":   league,
        "gen":      "inject",
        "actions":  actions,
        "dry_run":  False,
    }
    try:
        with open(LOKI_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"  [loki] log write failed: {e}")


def inject_odin_strategy():
    """Copy Odin's current best day strategy into AutoBotDay's fleet slot before sprint starts."""
    if not os.path.exists(ODIN_BEST_DAY):
        print("  [odin] No best_strategy.yaml yet — AutoBotDay keeps current strategy.")
        return
    try:
        import shutil
        shutil.copy2(ODIN_BEST_DAY, AUTOBOTDAY_STRATEGY)
        print(f"  [odin] Injected best day strategy -> {AUTOBOTDAY_STRATEGY}")
        write_loki_activity("day", ["odin_inject: AutoBotDay <- best day strategy"])
    except Exception as e:
        print(f"  [odin] Injection failed: {e} — AutoBotDay keeps current strategy.")


def archive_current(comp_id):
    """Score and archive the current sprint directly (no watchdog wait)."""
    result = subprocess.run(
        ["python3", SCORE_SCRIPT, comp_id, "--archive"],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        print(f"  Archived: {comp_id}")
        return True
    else:
        print(f"  ERROR archiving {comp_id}: {result.stderr[:300]}")
        return False


def patch_start_time(comp_id):
    """Patch the new sprint's started_at to exactly 09:00:00 UTC today."""
    target_ts = datetime.now(timezone.utc).replace(
        hour=9, minute=0, second=0, microsecond=0
    ).isoformat()
    meta_path = os.path.join(ACTIVE_DIR, comp_id, "meta.json")
    if not os.path.exists(meta_path):
        print(f"  WARNING: meta.json not found for {comp_id} — cannot patch start time.")
        return
    with open(meta_path) as f:
        meta = json.load(f)
    meta["started_at"] = target_ts
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  Patched started_at -> {target_ts}")


def advance_cycle_if_needed(cycle_state):
    """If cycle is complete, set awaiting_review for LOKI to handle. Returns (state, paused)."""
    sprint_in_cycle   = cycle_state.get("sprint_in_cycle", 0)
    sprints_per_cycle = cycle_state.get("sprints_per_cycle", 7)
    if sprint_in_cycle < sprints_per_cycle:
        return cycle_state, False  # still within cycle

    old_cycle = cycle_state.get("cycle", 1)
    cycle_state["status"] = "awaiting_review"
    save_cycle_state(cycle_state)
    print(f"  [cycle] Day Cycle {old_cycle} complete ({sprints_per_cycle} sprints) — awaiting LOKI review")
    # Write to SYN inbox so the alert reaches user if LOKI is delayed
    try:
        import json as _json
        from datetime import datetime as _dt, timezone as _tz
        inbox = os.path.join(WORKSPACE, "syn_inbox.jsonl")
        entry = _json.dumps({"ts": _dt.now(_tz.utc).strftime("%Y-%m-%dT%H:%M"),
                             "source": "day_restart", "severity": "info",
                             "msg": f"Day Cycle {old_cycle} complete — LOKI restructure pending"})
        with open(inbox, "a") as _f:
            _f.write(entry + "\n")
    except Exception:
        pass
    return cycle_state, True


def start_new():
    """Start a new 24h sprint. Returns new comp_id on success, None on failure."""
    cycle_state  = load_cycle_state()
    cycle_state, paused = advance_cycle_if_needed(cycle_state)
    if paused:
        return None  # LOKI will handle restructure and trigger next sprint
    new_sprint_n = cycle_state.get("sprint_in_cycle", 0) + 1
    result = subprocess.run(
        ["python3", START_SCRIPT, "24"],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        data    = json.loads(result.stdout)
        comp_id = data["comp_id"]
        print(f"  Started: {comp_id}")
        sprints = cycle_state.get("sprints", [])
        if comp_id not in sprints:
            sprints.append(comp_id)
        cycle_state["sprint_in_cycle"] = new_sprint_n
        cycle_state["sprints"]         = sprints
        if not cycle_state.get("cycle_started_at"):
            cycle_state["cycle_started_at"] = datetime.now(timezone.utc).isoformat()
        save_cycle_state(cycle_state)
        print(f"  Cycle {cycle_state['cycle']}, Sprint {new_sprint_n} started")
        return comp_id
    else:
        print(f"  ERROR starting: {result.stderr[:300]}")
        return None


def check_cycle_boundary_early():
    """Guard against prior archive crash: if the last completed sprint closed a
    cycle but status was never flipped to awaiting_review (e.g., archive_current
    raised before advance_cycle_if_needed ran), flip it now and exit so LOKI can
    process the cycle. Idempotent and safe when cycle is mid-flight.
    Returns True if main() should exit early."""
    cs = load_cycle_state()
    if cs.get("status") == "awaiting_review":
        print(f"  [cycle] Day Cycle {cs.get('cycle')} already awaiting LOKI review — skipping restart.")
        return True
    sprint_in_cycle   = cs.get("sprint_in_cycle", 0)
    sprints_per_cycle = cs.get("sprints_per_cycle", 7)
    if sprint_in_cycle >= sprints_per_cycle:
        old_cycle = cs.get("cycle", 1)
        cs["status"] = "awaiting_review"
        save_cycle_state(cs)
        print(f"  [cycle] Day Cycle {old_cycle} boundary recovered from stale state "
              f"({sprint_in_cycle}/{sprints_per_cycle}) — awaiting LOKI review.")
        try:
            inbox = os.path.join(WORKSPACE, "syn_inbox.jsonl")
            entry = json.dumps({
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
                "source": "day_restart", "severity": "warning",
                "msg": f"Day Cycle {old_cycle} boundary recovered from stale state — LOKI restructure pending",
            })
            with open(inbox, "a") as _f:
                _f.write(entry + "\n")
        except Exception:
            pass
        return True
    return False


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[day_daily_restart] {now}")

    if check_cycle_boundary_early():
        return

    comp_dir, meta = find_active()

    if meta is None:
        print("  No active sprint — starting new 24h sprint.")
        subprocess.run([sys.executable, "promotion_check.py"], cwd=WORKSPACE)
        inject_odin_strategy()
        new_comp_id = start_new()
        if new_comp_id:
            patch_start_time(new_comp_id)
        return

    elapsed = hours_running(meta)
    print(f"  Active: {meta['comp_id']}  ({elapsed:.1f}h elapsed)")

    if elapsed >= 20.0:
        print(f"  Sprint >= 20h — archiving directly and starting new sprint.")
        subprocess.run([sys.executable, "promotion_check.py"], cwd=WORKSPACE)
        inject_odin_strategy()
        if archive_current(meta["comp_id"]):
            new_comp_id = start_new()
            if new_comp_id:
                patch_start_time(new_comp_id)
    else:
        print(f"  Sprint < 20h old — keeping current sprint.")


if __name__ == "__main__":
    main()
