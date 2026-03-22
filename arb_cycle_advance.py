#!/usr/bin/env python3
"""
arb_cycle_advance.py — End-of-cycle cleanup for the Arb League.

Run manually after the last sprint of a cycle completes.
  1. Archives cycle results
  2. Advances cycle counter
  3. Sends Telegram summary

Pair health check and replacement happen at cycle START via arb_start_cycle.py.

Usage: python3 arb_cycle_advance.py [--dry-run]
"""
import argparse, json, os, shutil, urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PST = ZoneInfo("America/Los_Angeles")

WORKSPACE   = "/root/.openclaw/workspace"
RESULTS_DIR = os.path.join(WORKSPACE, "competition", "arb", "results")
ARCHIVE_DIR = os.path.join(WORKSPACE, "competition", "arb", "archive")
CYCLE_STATE = os.path.join(WORKSPACE, "competition", "arb", "arb_cycle_state.json")

BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID   = "8154505910"


def tg_send(msg):
    try:
        data = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req  = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  [tg] failed: {e}")


def load_cycle_state():
    if os.path.isfile(CYCLE_STATE):
        with open(CYCLE_STATE) as f:
            return json.load(f)
    return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4, "status": "active"}


def save_cycle_state(state):
    os.makedirs(os.path.dirname(CYCLE_STATE), exist_ok=True)
    with open(CYCLE_STATE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making changes")
    args = parser.parse_args()
    dry  = args.dry_run

    now_str = datetime.now(PST).strftime("%Y-%m-%d %H:%M %Z")
    print(f"\n{'='*60}")
    print(f"  ARB CYCLE ADVANCE  |  {now_str}")
    if dry:
        print("  DRY RUN — no changes will be made")
    print(f"{'='*60}\n")

    cycle_state = load_cycle_state()
    old_cycle   = cycle_state.get("cycle", 1)
    new_cycle   = old_cycle + 1

    # ── 1. Archive cycle results ──────────────────────────────────────────
    print(f"Archiving Arb Cycle {old_cycle} results...")
    archive_dest = os.path.join(ARCHIVE_DIR, f"cycle-{old_cycle}")
    if not dry and os.path.isdir(RESULTS_DIR) and os.listdir(RESULTS_DIR):
        os.makedirs(archive_dest, exist_ok=True)
        for entry in os.listdir(RESULTS_DIR):
            shutil.move(os.path.join(RESULTS_DIR, entry),
                        os.path.join(archive_dest, entry))
        print(f"  Archived to {archive_dest}")
    elif dry:
        print(f"  [dry] would archive to {archive_dest}")
    else:
        print("  Nothing to archive (results dir empty)")

    # ── 2. Advance cycle state ────────────────────────────────────────────
    cycle_state["cycle"]            = new_cycle
    cycle_state["sprint_in_cycle"]  = 0
    cycle_state["status"]           = "active"
    cycle_state["cycle_started_at"] = None
    cycle_state["sprints"]          = []

    if not dry:
        save_cycle_state(cycle_state)

    print(f"Cycle advanced: {old_cycle} -> {new_cycle}")

    # ── 3. Telegram summary ───────────────────────────────────────────────
    lines = [
        f"<b>Arb League — Cycle {old_cycle} Complete</b>",
        f"Cycle {new_cycle} ready.",
        f"\nStart new cycle (runs pair health check + sprint start):",
        f"python3 arb_start_cycle.py",
    ]
    msg = "\n".join(lines)
    print(f"\n{msg}")
    if not dry:
        tg_send(msg)

    print(f"\n{'='*60}")
    print(f"  {'DRY RUN complete — no files modified.' if dry else f'Cycle {new_cycle} ready. Run arb_start_cycle.py to begin.'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
