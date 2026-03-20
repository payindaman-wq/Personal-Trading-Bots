#!/usr/bin/env python3
"""
day_daily_restart.py - Daily 09:00 UTC (2:00am PDT) restart for Day Trading League.

Called by cron: 0 9 * * *

Logic:
  - If no active sprint: start new 24h sprint immediately.
  - If active sprint >= 20h old: expire it by patching duration_hours so the
    tick archives it on its next run; watchdog restarts within 10 min.
  - If active sprint < 20h old: skip (sprint started recently today, keep it).
"""
import os
import json
import subprocess
from datetime import datetime, timezone

WORKSPACE           = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
ACTIVE_DIR          = os.path.join(WORKSPACE, "competition", "active")
CYCLE_STATE_PATH    = os.path.join(WORKSPACE, "competition", "cycle_state.json")
START_SCRIPT        = "/root/.openclaw/skills/competition-start/scripts/competition_start.py"
VOLVA_BEST_DAY      = os.path.join(WORKSPACE, "research", "day", "best_strategy.yaml")
AUTOBOTDAY_STRATEGY = os.path.join(WORKSPACE, "fleet", "autobotday", "strategy.yaml")


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


def inject_volva_strategy():
    """Copy Volva's current best day strategy into AutoBotDay's fleet slot before sprint starts."""
    if not os.path.exists(VOLVA_BEST_DAY):
        print("  [volva] No best_strategy.yaml yet — AutoBotDay keeps current strategy.")
        return
    try:
        import shutil
        shutil.copy2(VOLVA_BEST_DAY, AUTOBOTDAY_STRATEGY)
        print(f"  [volva] Injected best day strategy -> {AUTOBOTDAY_STRATEGY}")
    except Exception as e:
        print(f"  [volva] Injection failed: {e} — AutoBotDay keeps current strategy.")


def start_new():
    cycle_state = load_cycle_state()
    new_sprint_n = cycle_state.get("sprint_in_cycle", 0) + 1
    result = subprocess.run(
        ["python3", START_SCRIPT, "24"],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        comp_id = data["comp_id"]
        print(f"  Started: {comp_id}")
        # Update cycle state
        sprints = cycle_state.get("sprints", [])
        if comp_id not in sprints:
            sprints.append(comp_id)
        cycle_state["sprint_in_cycle"] = new_sprint_n
        cycle_state["sprints"] = sprints
        save_cycle_state(cycle_state)
        print(f"  Cycle {cycle_state['cycle']}, Sprint {new_sprint_n} started")
    else:
        print(f"  ERROR starting: {result.stderr[:300]}")


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[day_daily_restart] {now}")

    comp_dir, meta = find_active()

    if meta is None:
        print("  No active sprint — starting new 24h sprint.")
        inject_volva_strategy()
        start_new()
        return

    elapsed = hours_running(meta)
    print(f"  Active: {meta['comp_id']}  ({elapsed:.1f}h elapsed)")

    if elapsed >= 20.0:
        print(f"  Sprint >= 20h — patching to expire now. Tick will archive; watchdog restarts.")
        inject_volva_strategy()
        meta["duration_hours"] = round(elapsed - 0.01, 4)
        with open(os.path.join(comp_dir, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)
    else:
        print(f"  Sprint < 20h old — keeping current sprint.")


if __name__ == "__main__":
    main()
