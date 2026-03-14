#!/usr/bin/env python3
"""
polymarket_syn_init.py — Initialize all 15 autonomous Polymarket bot states.
Run once before starting polymarket_syn.service. Deletes and recreates auto_state.json.
"""
import json, os
from datetime import datetime, timezone, timedelta

AUTO_STATE_FILE  = "/root/.openclaw/workspace/competition/polymarket/auto_state.json"
RESULTS_DIR      = "/root/.openclaw/workspace/competition/polymarket/auto_results"
SPRINT_HOURS     = 168  # 7 days

BOT_ROSTER = [
    # Sports
    {"name": "ullr",     "category": "sports",       "type": "opinion"},
    {"name": "sigyn",    "category": "sports",       "type": "opinion"},
    {"name": "hlin",     "category": "sports",       "type": "opinion"},
    # Politics
    {"name": "freya",    "category": "politics",     "type": "opinion"},
    {"name": "var",      "category": "politics",     "type": "opinion"},
    {"name": "saga",     "category": "politics",     "type": "opinion"},
    # Crypto
    {"name": "mimir",    "category": "crypto",       "type": "opinion"},
    {"name": "gerd",     "category": "crypto",       "type": "opinion"},
    {"name": "skadi",    "category": "crypto",       "type": "opinion"},
    # Macro
    {"name": "rind",     "category": "macro",        "type": "opinion"},
    {"name": "aegir",    "category": "macro",        "type": "opinion"},
    {"name": "jord",     "category": "macro",        "type": "opinion"},
    # World Events
    {"name": "verdandi", "category": "world_events", "type": "opinion"},
    {"name": "urd",      "category": "world_events", "type": "opinion"},
    {"name": "ran",      "category": "world_events", "type": "opinion"},
    # Arb
    {"name": "loki",     "category": "arb",          "type": "arb"},
    {"name": "huginn",   "category": "arb",          "type": "arb"},
    {"name": "muninn",   "category": "arb",          "type": "arb"},
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
        "positions":        {},
        "closed_trades":    [],
        "scan_count":       0,
        "gemini_calls":     0,
        "last_scan_at":     None,
    }

def main():
    now       = datetime.now(timezone.utc)
    sprint_id = f"poly-auto-{now.strftime('%Y%m%d-%H%M')}"
    ends_at   = (now + timedelta(hours=SPRINT_HOURS)).isoformat()

    state = {
        "generated_at":    now.isoformat(),
        "mode":            "paper",
        "status":          "active",
        "sprint_id":       sprint_id,
        "sprint_started_at": now.isoformat(),
        "sprint_ends_at":  ends_at,
        "sprint_hours":    SPRINT_HOURS,
        "bots":            [make_bot(m) for m in BOT_ROSTER],
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
        print(f"  {b['name']:<12} [{b['category']:<12}] ${1000:.0f}")

if __name__ == "__main__":
    main()
