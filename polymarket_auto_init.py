#!/usr/bin/env python3
"""
polymarket_auto_init.py -- Initialize Ullr autonomous bot state.
Run once before starting polymarket_auto.service.
"""
import json, os
from datetime import datetime, timezone

AUTO_STATE_FILE = "/root/.openclaw/workspace/competition/polymarket/auto_state.json"

def main():
    if os.path.exists(AUTO_STATE_FILE):
        print(f"State file already exists: {AUTO_STATE_FILE}")
        print("Delete it first if you want to reset.")
        return

    now = datetime.now(timezone.utc).isoformat()
    state = {
        "generated_at": now,
        "mode": "paper",
        "status": "active",
        "started_at": now,
        "bots": [
            {
                "name": "ullr",
                "type": "autonomous",
                "category": "sports",
                "starting_capital": 1000.0,
                "cash": 1000.0,
                "equity": 1000.0,
                "pnl_usd": 0.0,
                "pnl_pct": 0.0,
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "positions": {},
                "closed_trades": [],
                "scan_count": 0,
                "gemini_calls": 0,
                "last_scan_at": None
            }
        ]
    }

    os.makedirs(os.path.dirname(AUTO_STATE_FILE), exist_ok=True)
    with open(AUTO_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print(f"Initialized: {AUTO_STATE_FILE}")
    print(f"Bot: ullr | Capital: $1000.00 | Mode: paper")

if __name__ == "__main__":
    main()
