#!/usr/bin/env python3
"""
weekly_league_restart.py - Sunday 09:00 UTC restart for Swing, Arb, Spread leagues.

Called by cron: 0 9 * * 0

Directly archives active sprints (via league tick scripts) then starts new ones,
patching started_at to exactly 09:00:00 UTC so all countdown timers align.
"""
import os, sys, json, shutil, argparse, subprocess
from datetime import datetime, timezone, timedelta

WORKSPACE = "/root/.openclaw/workspace"

ODIN_SWING_BEST    = os.path.join(WORKSPACE, "research", "swing", "best_strategy.yaml")
AUTOBOTSWING_STRAT = os.path.join(WORKSPACE, "fleet", "swing", "autobotswing", "strategy.yaml")

LEAGUES = {
    "swing": {
        "active_dir":   os.path.join(WORKSPACE, "competition", "swing", "active"),
        "tick_script":  os.path.join(WORKSPACE, "swing_competition_tick.py"),
        "start_script": os.path.join(WORKSPACE, "swing_competition_start.py"),
        "start_args":   ["168"],
    },
    "arb": {
        "active_dir":   os.path.join(WORKSPACE, "competition", "arb", "active"),
        "tick_script":  os.path.join(WORKSPACE, "arb_competition_tick.py"),
        "start_script": os.path.join(WORKSPACE, "arb_competition_start.py"),
        "start_args":   [],
    },
    "spread": {
        "active_dir":   os.path.join(WORKSPACE, "competition", "spread", "active"),
        "tick_script":  os.path.join(WORKSPACE, "spread_competition_tick.py"),
        "start_script": os.path.join(WORKSPACE, "spread_competition_start.py"),
        "start_args":   ["168"],
    },
}

POLYMARKET_AUTO_STATE = os.path.join(WORKSPACE, "competition", "polymarket", "auto_state.json")


def inject_odin_swing_strategy(dry_run=False):
    if not os.path.exists(ODIN_SWING_BEST):
        print("  [odin-swing] No best_strategy.yaml yet — AutoBotSwing keeps current strategy.")
        return
    if not dry_run:
        shutil.copy2(ODIN_SWING_BEST, AUTOBOTSWING_STRAT)
    print("  [odin-swing] Injected best swing strategy -> " + AUTOBOTSWING_STRAT)


def find_active_meta(active_dir):
    if not os.path.isdir(active_dir):
        return None, None
    entries = sorted(os.listdir(active_dir))
    if not entries:
        return None, None
    comp_dir  = os.path.join(active_dir, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None, None
    with open(meta_path) as f:
        meta = json.load(f)
    return (comp_dir, meta) if meta.get("status") == "active" else (None, None)


def expire_and_archive(league, cfg, now, dry_run):
    """
    Expire and archive the active sprint directly via the league's tick script.
    Returns True if we should proceed to start a new sprint, False to skip.
    """
    comp_dir, meta = find_active_meta(cfg["active_dir"])
    if not meta:
        print(f"  [{league.upper()}] No active sprint — will start fresh.")
        return True

    started = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    hrs     = (now - started).total_seconds() / 3600

    if hrs < 24:
        print(f"  [{league.upper()}] Sprint only {hrs:.1f}h old — skipping.")
        return False

    print(f"  [{league.upper()}] Sprint {hrs:.1f}h old — expiring and archiving...")

    if dry_run:
        print(f"  [{league.upper()}] [DRY RUN] Would archive {meta['comp_id']}")
        return True

    # Patch duration_hours so the tick script detects expiry
    meta["duration_hours"] = round(hrs - 0.01, 4)
    with open(os.path.join(comp_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    # Call tick script — it detects expiry, closes positions at current prices, archives
    result = subprocess.run(
        ["python3", cfg["tick_script"]],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        output = result.stdout.strip()
        if output:
            print("    " + "\n    ".join(output.splitlines()))
        return True
    else:
        print(f"  [{league.upper()}] ERROR archiving: {result.stderr[:300]}")
        return False


def start_new_sprint(league, cfg, target_ts, dry_run):
    """Start a new sprint and patch started_at to target_ts."""
    if dry_run:
        print(f"  [{league.upper()}] [DRY RUN] Would start new sprint, timestamp -> {target_ts}")
        return

    cmd    = ["python3", cfg["start_script"]] + cfg["start_args"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    if result.returncode != 0:
        print(f"  [{league.upper()}] ERROR starting: {result.stderr[:300]}")
        return

    data    = json.loads(result.stdout)
    comp_id = data["comp_id"]
    print(f"  [{league.upper()}] Started: {comp_id}")

    # Patch started_at in meta.json to exact 09:00:00 UTC
    meta_path = os.path.join(cfg["active_dir"], comp_id, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
        meta["started_at"] = target_ts
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"  [{league.upper()}] Patched started_at -> {target_ts}")


parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

now       = datetime.now(timezone.utc)
target_ts = now.replace(hour=9, minute=0, second=0, microsecond=0).isoformat()
print("weekly_league_restart @ " + now.strftime("%Y-%m-%d %H:%M UTC"))
print(f"  Target start timestamp: {target_ts}")

for league, cfg in LEAGUES.items():
    archived = expire_and_archive(league, cfg, now, args.dry_run)
    if archived:
        if league == "swing":
            inject_odin_swing_strategy(args.dry_run)
        start_new_sprint(league, cfg, target_ts, args.dry_run)

# Polymarket: expire + immediate service restart so tick fires now
try:
    with open(POLYMARKET_AUTO_STATE) as f:
        state = json.load(f)
    sprint_start = state.get("sprint_started_at", "")
    if sprint_start:
        started_dt = datetime.fromisoformat(sprint_start.replace("Z", "+00:00"))
        hrs        = (now - started_dt).total_seconds() / 3600
        if hrs < 24:
            print(f"  [POLYMARKET] Sprint only {hrs:.1f}h old — skipping.")
        else:
            if not args.dry_run:
                state["sprint_ends_at"] = (now - timedelta(seconds=1)).isoformat()
                with open(POLYMARKET_AUTO_STATE, "w") as f:
                    json.dump(state, f, indent=2)
                subprocess.run(["systemctl", "restart", "polymarket_syn.service"],
                               capture_output=True)
            print(f"  [POLYMARKET] Expired after {hrs:.1f}h. Service restarted.")
except Exception as e:
    print("  [POLYMARKET] Error: " + str(e))

print("Done.")
