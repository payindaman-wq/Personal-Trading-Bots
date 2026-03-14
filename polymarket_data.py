#!/usr/bin/env python3
"""
polymarket_data.py — Generate /var/www/dashboard/api/polymarket.json
Reads from /root/.openclaw/workspace/competition/polymarket/state.json if it exists.
Otherwise outputs the pending_setup structure.
"""
import json
import os
from datetime import datetime, timezone

STATE_FILE   = '/root/.openclaw/workspace/competition/polymarket/state.json'
OUTPUT_FILE  = '/var/www/dashboard/api/polymarket.json'

def pending_setup():
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "paper",
        "status": "pending_setup",
        "stats": {
            "total_pnl_usd": 0.0,
            "overall_win_rate": 0.0,
            "active_positions": 0,
            "total_trades": 0,
            "total_wins": 0,
            "total_losses": 0
        },
        "bots": [],
        "tracked_traders": [],
        "recent_trades": []
    }

def main():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
            # Always stamp generated_at
            data['generated_at'] = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            print(f'[polymarket_data] Error reading state file: {e}')
            data = pending_setup()
    else:
        data = pending_setup()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'[polymarket_data] Wrote {OUTPUT_FILE} (status={data.get("status")})')

if __name__ == '__main__':
    main()
