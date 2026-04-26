#!/usr/bin/env python3
"""Self-heal framework Tier 2 readiness checker.

Fires a one-shot SYN alert when Tier 1 (LOKI audit layer) has accumulated
enough real-world revert data to calibrate Tier 2 thresholds.

Criteria (all must be true):
  - >= 14 days since Tier 1 ship date (2026-04-19)
  - >= 3 reverts in loki_revert_history.json
  - >= 2 distinct leagues represented in those reverts

State file prevents repeat firings.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone

TIER1_SHIP_DATE = "2026-04-19"
MIN_DAYS = 14
MIN_REVERTS = 3
MIN_LEAGUES = 2

RESEARCH = "/root/.openclaw/workspace/research"
REVERT_PATH = os.path.join(RESEARCH, "loki_revert_history.json")
STATE_PATH = os.path.join(RESEARCH, "self_heal_readiness_state.json")

from config_loader import config
BOT_TOKEN = config.telegram.bot_token
CHAT_ID   = config.telegram.chat_id


INBOX = "/root/.openclaw/workspace/syn_inbox.jsonl"


def tg_send(msg, severity="info"):
    """Write to SYN inbox. Tier-2 readiness is a dashboard announcement."""
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":   "self_heal_readiness",
            "severity": severity,
            "msg":      (msg if isinstance(msg, str) else str(msg))[:2000],
        }
        with open(INBOX, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"[self_heal_readiness/inbox] {e}")


def load_state():
    if not os.path.exists(STATE_PATH):
        return {"alerted": False}
    try:
        return json.load(open(STATE_PATH))
    except Exception:
        return {"alerted": False}


def save_state(s):
    with open(STATE_PATH, "w") as f:
        json.dump(s, f, indent=2)


def load_reverts():
    if not os.path.exists(REVERT_PATH):
        return []
    try:
        data = json.load(open(REVERT_PATH))
    except Exception:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rows = []
        for lg, entries in data.items():
            if isinstance(entries, list):
                for e in entries:
                    if isinstance(e, dict):
                        e = dict(e)
                        e.setdefault("league", lg)
                        rows.append(e)
        return rows
    return []


def main():
    state = load_state()
    if state.get("alerted"):
        return

    ship = datetime.fromisoformat(TIER1_SHIP_DATE).replace(tzinfo=timezone.utc)
    days = (datetime.now(timezone.utc) - ship).days
    reverts = load_reverts()
    leagues = {r.get("league") for r in reverts if r.get("league")}

    ready = (days >= MIN_DAYS) and (len(reverts) >= MIN_REVERTS) and (len(leagues) >= MIN_LEAGUES)

    print(f"days_since_ship={days} reverts={len(reverts)} leagues={len(leagues)} ready={ready}")

    if ready:
        msg = (
            f"Tier 1 calibration window complete — ready to scope Tier 2 build.\n"
            f"Days since ship: {days} | Reverts: {len(reverts)} | Leagues: {len(leagues)} ({', '.join(sorted(leagues))})\n"
            f"Next step: ask Claude to build self_heal_controller.py with calibrated thresholds."
        )
        tg_send(msg)
        state["alerted"] = True
        state["alerted_ts"] = datetime.now(timezone.utc).isoformat()
        state["snapshot"] = {"days": days, "reverts": len(reverts), "leagues": sorted(leagues)}
        save_state(state)


if __name__ == "__main__":
    main()
