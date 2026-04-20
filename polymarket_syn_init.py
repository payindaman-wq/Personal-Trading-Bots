#!/usr/bin/env python3
"""
polymarket_syn_init.py — Initialize 12 autonomous Polymarket bot states (Cycle 2+).
Run once before starting polymarket_syn.service. Deletes and recreates auto_state.json.
"""
import json, os
from datetime import datetime, timezone, timedelta

AUTO_STATE_FILE  = "/root/.openclaw/workspace/competition/polymarket/auto_state.json"
RESULTS_DIR      = "/root/.openclaw/workspace/competition/polymarket/auto_results"
SPRINT_HOURS     = 168  # 7 days

BOT_ROSTER = [
    # Sports (2)
    {"name": "hlin",   "category": "sports",          "type": "opinion"},
    {"name": "tora",   "category": "sports",          "type": "opinion"},
    # Politics (1)
    {"name": "var",    "category": "politics",        "type": "opinion"},
    # Crypto (3)
    {"name": "njal",   "category": "crypto",          "type": "opinion"},
    {"name": "gerd",   "category": "crypto",          "type": "opinion"},
    {"name": "skadi",  "category": "crypto",          "type": "opinion"},
    # World Economics (1)
    {"name": "hermod", "category": "world_economics", "type": "opinion"},
    # Science (1)
    {"name": "eir",    "category": "science",         "type": "opinion"},
    # Arb (1)
    {"name": "muninn", "category": "arb",             "type": "arb"},
    # FREYA research slots — disabled until FREYA assigns strategies
    {"name": "autobotpred1",   "category": "research",        "type": "disabled"},
    {"name": "autobotpred2",   "category": "research",        "type": "disabled"},
    {"name": "autobotpred3",  "category": "research",        "type": "disabled"},
]

def make_bot(meta):
    return {
        "name":             meta["name"],
        "category":         meta["category"],
        "type":             meta["type"],
        "starting_capital": 1000.0,
        "cash":             1000.0,
        "equity":           1000.0,
        "pnl_usd":          0.0,
        "pnl_pct":          0.0,
        "total_trades":     0,
        "wins":             0,
        "losses":           0,
        "total_fees":       0.0,
        "positions":        {},
        "closed_trades":    [],
        "scan_count":       0,
        "gemini_calls":     0,
        "last_scan_at":     None,
        "stopped":          False,
    }

def main():
    now       = datetime.now(timezone.utc)
    sprint_id = f"poly-auto-{now.strftime('%Y%m%d-%H%M')}"
    ends_at   = (now + timedelta(hours=SPRINT_HOURS)).isoformat()

    state = {
        "generated_at":      now.isoformat(),
        "mode":              "paper",
        "status":            "active",
        "sprint_id":         sprint_id,
        "sprint_started_at": now.isoformat(),
        "sprint_ends_at":    ends_at,
        "sprint_hours":      SPRINT_HOURS,
        "bots":              [make_bot(m) for m in BOT_ROSTER],
    }

    os.makedirs(os.path.dirname(AUTO_STATE_FILE), exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(AUTO_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print(f"Initialized {AUTO_STATE_FILE}")
    print(f"Sprint: {sprint_id}")
    print(f"Ends:   {ends_at}")
    print(f"Bots:   {len(BOT_ROSTER)}")
    for b in BOT_ROSTER:
        print(f"  {b['name']:<12} [{b['category']:<12}] {b['type']}")

if __name__ == "__main__":
    main()
