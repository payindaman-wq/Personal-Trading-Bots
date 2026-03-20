#!/usr/bin/env python3
"""
polymarket_init.py — Initialize the Polymarket copy-trading paper competition.
Run once to create state.json. Then start polymarket_tick.py daemon.
"""
import json, os
from datetime import datetime, timezone, timedelta

STATE_DIR  = "/root/.openclaw/workspace/competition/polymarket"
STATE_FILE = f"{STATE_DIR}/state.json"

STARTING_CAPITAL = 1000.0

BOTS = [
    {"name": "sol",      "trader": "SecondWindCapital",  "wallet": "0x8c80d213c0cbad777d06ee3f58f6ca4bc03102c3"},
    {"name": "freyr",    "trader": "beachboy4",           "wallet": "0xc2e7800b5af46e6093872b177b7a5e7f0563be51"},
    {"name": "haakon",     "trader": "WoofMaster",          "wallet": "0x916f7165c2c836aba22edb6453cdbb5f3ea253ba"},
    {"name": "thor",     "trader": "majorexploiter",      "wallet": "0x019782cab5d844f02bafb71f512758be78579f3c"},
    {"name": "torkel",      "trader": "HorizonSplendidView", "wallet": "0x02227b8f5a9636e895607edd3185ed6ee5598ff7"},
    {"name": "bragi",    "trader": "Blessed-Sunshine",    "wallet": "0x59a0744db1f39ff3afccd175f80e6e8dfc239a09"},
    {"name": "heimdall", "trader": "FTWUTB",              "wallet": "0xdb2223cc5202a4718c3069f577ec971f71c96478"},
    {"name": "baldur",   "trader": "UAEVALORANTFAN",      "wallet": "0xc65ca4755436f82d8eb461e65781584b8cadea39"},
    {"name": "vidar",    "trader": "ewelmealt",           "wallet": "0x07921379f7b31ef93da634b688b2fe36897db778"},
    {"name": "hallvard",    "trader": "Countryside",         "wallet": "0xbddf61af533ff524d27154e589d2d7a81510c684"},
]

# Position sizing: each trade uses this fraction of remaining cash
TRADE_SIZE_PCT = 0.10  # 10% of available cash per signal

def make_bot(b):
    return {
        "name": b["name"],
        "trader": b["trader"],
        "wallet": b["wallet"],
        "starting_capital": STARTING_CAPITAL,
        "cash": STARTING_CAPITAL,
        "equity": STARTING_CAPITAL,
        "pnl_usd": 0.0,
        "pnl_pct": 0.0,
        "total_trades": 0,
        "wins": 0,
        "losses": 0,
        "positions": {},           # conditionId -> position dict
        "closed_trades": [],       # settled/resolved trades
        "last_seen_tx": None,      # last processed tx hash for this trader
        "last_seen_ts": 0,         # last processed timestamp
        "sprint_pnl_usd": 0.0,
        "sprint_wins": 0,
        "sprint_trades": 0,
        "sprint_start_equity": STARTING_CAPITAL,
    }

def main():
    if os.path.exists(STATE_FILE):
        print(f"State file already exists: {STATE_FILE}")
        print("Delete it first if you want to reinitialize.")
        return

    os.makedirs(STATE_DIR, exist_ok=True)

    now      = datetime.now(timezone.utc)
    ends_at  = now + timedelta(hours=168)
    state = {
        "generated_at":      now.isoformat(),
        "mode":              "paper",
        "status":            "active",
        "started_at":        now.isoformat(),
        "sprint_id":         f"copy-{now.strftime('%Y%m%d-%H%M')}",
        "sprint_started_at": now.isoformat(),
        "sprint_ends_at":    ends_at.isoformat(),
        "starting_capital":  STARTING_CAPITAL,
        "trade_size_pct": TRADE_SIZE_PCT,
        "poll_interval_sec": 30,
        "bots": [make_bot(b) for b in BOTS],
        "stats": {
            "total_pnl_usd": 0.0,
            "overall_win_rate": 0.0,
            "active_positions": 0,
            "total_trades": 0,
            "total_wins": 0,
            "total_losses": 0,
        },
        "recent_trades": [],
        "tracked_traders": [
            {"trader": b["trader"], "bot": b["name"], "wallet": b["wallet"]}
            for b in BOTS
        ],
    }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print(f"Initialized state.json at {STATE_FILE}")
    print(f"  {len(BOTS)} bots, ${STARTING_CAPITAL:.0f} each, {TRADE_SIZE_PCT*100:.0f}% position sizing")
    for b in BOTS:
        print(f"  {b['name']:<10} -> {b['trader']}")

if __name__ == "__main__":
    main()
