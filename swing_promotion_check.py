#!/usr/bin/env python3
"""
swing_promotion_check.py - Auto-promotion check for Swing League.

Called from swing_competition_tick.py when a sprint is archived.
Checks if autobotswing qualifies for promotion (top-3 for 2 consecutive sprints).

On promotion: copies autobotswing's strategy.yaml to fleet/swing/{champion}/strategy.yaml.
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

WORKSPACE           = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESULTS_DIR         = os.path.join(WORKSPACE, "competition", "swing", "results")
TRACKER_PATH        = os.path.join(WORKSPACE, "competition", "swing", "promotion_tracker.json")
FLEET_DIR           = os.path.join(WORKSPACE, "fleet", "swing")
SYN_ALERT           = os.path.join(WORKSPACE, "syn_alert.py")

CHALLENGER          = "autobotswing"
PROMOTION_THRESHOLD = 2  # consecutive top-3 finishes required (7-day sprints)

DEFAULT_TRACKER = {
    "champion":        "solveig",
    "challenger":      CHALLENGER,
    "challenger_wins": 0,
    "champion_wins":   0,
    "history":         [],
}


def load_tracker():
    if not os.path.exists(TRACKER_PATH):
        return dict(DEFAULT_TRACKER)
    with open(TRACKER_PATH) as f:
        return json.load(f)


def save_tracker(tracker):
    with open(TRACKER_PATH, "w") as f:
        json.dump(tracker, f, indent=2)


def send_alert(message):
    try:
        subprocess.run([sys.executable, SYN_ALERT, message], cwd=WORKSPACE, timeout=10)
    except Exception as e:
        print(f"  [promo/swing] Alert failed: {e}")


def find_latest_archived_sprint():
    """Return (comp_id, final_score dict) for the most recently archived swing sprint."""
    if not os.path.isdir(RESULTS_DIR):
        print("  [promo/swing] Results dir not found.")
        return None, None
    entries = sorted(e for e in os.listdir(RESULTS_DIR) if not e.startswith("."))
    for entry in reversed(entries):
        score_path = os.path.join(RESULTS_DIR, entry, "final_score.json")
        if not os.path.isfile(score_path):
            continue
        with open(score_path) as f:
            data = json.load(f)
        return entry, data
    return None, None


def get_autobot_rank(final_score):
    for r in final_score.get("rankings", []):
        if r["bot"] == CHALLENGER:
            return r["rank"], r.get("total_pnl_pct", 0.0)
    return None, None


def already_processed(tracker, sprint_id):
    return any(h["sprint"] == sprint_id for h in tracker.get("history", []))


def do_promote(tracker):
    champion = tracker["champion"]
    src = os.path.join(FLEET_DIR, CHALLENGER, "strategy.yaml")
    dst = os.path.join(FLEET_DIR, champion, "strategy.yaml")
    try:
        shutil.copy2(src, dst)
        print(f"  [promo/swing] Copied {CHALLENGER}/strategy.yaml -> fleet/swing/{champion}/strategy.yaml")
    except Exception as e:
        print(f"  [promo/swing] Strategy copy failed: {e}")
        return
    send_alert(
        f"PROMOTION: {CHALLENGER} strategy promoted to {champion} "
        f"after {PROMOTION_THRESHOLD} consecutive top-3 finishes"
    )


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[promotion_check/swing] {now}")

    comp_id, final_score = find_latest_archived_sprint()
    if comp_id is None:
        print("  No archived sprints found.")
        return

    print(f"  Latest sprint: {comp_id}")
    tracker = load_tracker()

    if already_processed(tracker, comp_id):
        print(f"  Sprint {comp_id} already processed — nothing to do.")
        return

    rank, pnl_pct = get_autobot_rank(final_score)
    if rank is None:
        print(f"  {CHALLENGER} not found in {comp_id} — skipping.")
        tracker["history"].append({
            "sprint": comp_id,
            "winner": final_score.get("winner", "?"),
            "autobot_rank": None,
            "autobot_pnl": None,
            "top3": False,
            "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        })
        save_tracker(tracker)
        return

    top3 = rank <= 3
    winner = final_score.get("winner", "?")
    print(f"  {CHALLENGER}: rank #{rank}, pnl {pnl_pct:+.4f}%  top3={top3}  winner={winner}")

    if top3:
        tracker["challenger_wins"] += 1
    else:
        tracker["champion_wins"] += 1
        tracker["challenger_wins"] = 0

    tracker["history"].append({
        "sprint":       comp_id,
        "winner":       winner,
        "autobot_rank": rank,
        "autobot_pnl":  round(pnl_pct, 4),
        "top3":         top3,
        "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
    })

    consecutive = tracker["challenger_wins"]
    print(f"  Consecutive top-3: {consecutive}/{PROMOTION_THRESHOLD}")

    if consecutive >= PROMOTION_THRESHOLD:
        print(f"  *** PROMOTION TRIGGERED ***")
        do_promote(tracker)
        tracker["challenger_wins"] = 0
        tracker["champion_wins"]   = 0
    elif consecutive == PROMOTION_THRESHOLD - 1:
        send_alert(
            f"PROMOTION WATCH: {CHALLENGER} rank #{rank} in {comp_id} "
            f"— {consecutive}/{PROMOTION_THRESHOLD} consecutive top-3. One more to promote!"
        )
        print(f"  Alert: one sprint away from promotion.")

    save_tracker(tracker)
    print(f"  Tracker saved.")


if __name__ == "__main__":
    main()
