#!/usr/bin/env python3
"""
futures_swing_restart.py - Weekly 09:00 UTC Sunday restart for Futures Swing league.
Called by weekly_league_restart.py and by the swing tick on expiry.
"""
import os, json, shutil, sys
from datetime import datetime, timezone

WORKSPACE        = os.environ.get('WORKSPACE', '/root/.openclaw/workspace')
ACTIVE_DIR       = os.path.join(WORKSPACE, 'competition', 'futures_swing', 'active')
RESULTS_DIR      = os.path.join(WORKSPACE, 'competition', 'futures_swing', 'results')
CYCLE_STATE_PATH = os.path.join(WORKSPACE, 'competition', 'futures_swing', 'cycle_state.json')
FLEET_DIR        = os.path.join(WORKSPACE, 'fleet', 'futures_swing')
ODIN_BEST        = os.path.join(WORKSPACE, 'research', 'futures_swing', 'best_strategy.yaml')
AUTOBOT_STRATEGY = os.path.join(FLEET_DIR, 'autobotswingfutures', 'strategy.yaml')
LOKI_LOG         = os.path.join(WORKSPACE, 'research', 'loki_log.jsonl')

ALL_BOTS = [
    'sigmund', 'sinfjotli', 'hogni', 'atli', 'regin',
    'andvari', 'grimolf', 'audun', 'thorolf', 'autobotswingfutures',
]
ALL_PAIRS = [
    'BTC/USD', 'ETH/USD', 'SOL/USD', 'XRP/USD', 'DOGE/USD', 'AVAX/USD',
    'LINK/USD', 'UNI/USD', 'AAVE/USD', 'NEAR/USD', 'APT/USD', 'SUI/USD',
    'ARB/USD', 'OP/USD', 'ADA/USD', 'POL/USD',
]
STARTING_CAPITAL = 1000.0
LEVERAGE_DEFAULT = 2.0


def load_cycle_state():
    try:
        return json.load(open(CYCLE_STATE_PATH))
    except Exception:
        return {'cycle': 1, 'sprint_in_cycle': 0, 'sprints_per_cycle': 4,
                'status': 'active', 'sprints': []}


def save_cycle_state(state):
    os.makedirs(os.path.dirname(CYCLE_STATE_PATH), exist_ok=True)
    with open(CYCLE_STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)


def find_active():
    if not os.path.isdir(ACTIVE_DIR):
        return None, None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None, None
    comp_dir = os.path.join(ACTIVE_DIR, entries[-1])
    meta_path = os.path.join(comp_dir, 'meta.json')
    if not os.path.isfile(meta_path):
        return None, None
    meta = json.load(open(meta_path))
    return (comp_dir, meta) if meta.get('status') == 'active' else (None, None)


def archive_current(comp_id):
    src = os.path.join(ACTIVE_DIR, comp_id)
    dest = os.path.join(RESULTS_DIR, comp_id)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.move(src, dest)
    print(f'  Archived: {comp_id}')
    return True


def inject_odin_strategy():
    if not os.path.exists(ODIN_BEST):
        print('  [odin] No futures_swing best_strategy.yaml yet — autobotswingfutures keeps current.')
        return
    try:
        shutil.copy2(ODIN_BEST, AUTOBOT_STRATEGY)
        print('  [odin] Injected futures_swing best strategy -> autobotswingfutures')
        entry = {
            'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M'),
            'mimir_ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M'),
            'league': 'futures_swing', 'gen': 'inject',
            'actions': ['odin_inject: autobotswingfutures <- best futures_swing strategy'],
            'dry_run': False,
        }
        with open(LOKI_LOG, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f'  [odin] Injection failed: {e}')


def patch_start_time(comp_id):
    target_ts = datetime.now(timezone.utc).replace(
        hour=9, minute=0, second=0, microsecond=0).isoformat()
    meta_path = os.path.join(ACTIVE_DIR, comp_id, 'meta.json')
    if not os.path.exists(meta_path):
        return
    meta = json.load(open(meta_path))
    meta['started_at'] = target_ts
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f'  Patched started_at -> {target_ts}')


def start_new():
    now = datetime.now(timezone.utc)
    comp_id = now.strftime('fut-swing-%Y%m%d-%H%M')
    comp_dir = os.path.join(ACTIVE_DIR, comp_id)
    os.makedirs(comp_dir, exist_ok=True)

    valid_bots = [b for b in ALL_BOTS
                  if os.path.exists(os.path.join(FLEET_DIR, b, 'strategy.yaml'))]

    for bot in valid_bots:
        portfolio = {
            'bot': bot, 'competition_id': comp_id,
            'duration_hours': 168, 'started_at': now.isoformat(),
            'pairs': ALL_PAIRS, 'starting_capital': STARTING_CAPITAL,
            'fee_rate': 0.0005, 'cash': STARTING_CAPITAL,
            'positions': [], 'closed_trades': [],
            'stats': {
                'total_trades': 0, 'wins': 0, 'losses': 0, 'win_rate': 0.0,
                'total_pnl_usd': 0.0, 'total_pnl_pct': 0.0,
                'total_fees': 0.0, 'max_drawdown_pct': 0.0,
                'current_equity': STARTING_CAPITAL, 'peak_equity': STARTING_CAPITAL,
            },
        }
        with open(os.path.join(comp_dir, f'portfolio-{bot}.json'), 'w') as f:
            json.dump(portfolio, f, indent=2)

    meta = {
        'comp_id': comp_id, 'duration_hours': 168,
        'started_at': now.isoformat(), 'pairs': ALL_PAIRS,
        'bots': valid_bots, 'starting_capital': STARTING_CAPITAL,
        'fee_rate': 0.0005, 'status': 'active',
        'league': 'futures_swing', 'leverage_default': LEVERAGE_DEFAULT,
    }
    with open(os.path.join(comp_dir, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=2)

    cycle_state = load_cycle_state()
    new_sprint_n = cycle_state.get('sprint_in_cycle', 0) + 1
    sprints = cycle_state.get('sprints', [])
    if comp_id not in sprints:
        sprints.append(comp_id)
    cycle_state['sprint_in_cycle'] = new_sprint_n
    cycle_state['sprints'] = sprints
    if not cycle_state.get('cycle_started_at'):
        cycle_state['cycle_started_at'] = now.isoformat()
    save_cycle_state(cycle_state)

    print(f'  Started: {comp_id} (Cycle {cycle_state["cycle"]}, Sprint {new_sprint_n})')
    return comp_id


def main():
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    print(f'[futures_swing_restart] {now}')

    comp_dir, meta = find_active()
    if meta is not None:
        print(f'  Archiving current: {meta["comp_id"]}')
        archive_current(meta['comp_id'])

    inject_odin_strategy()
    new_id = start_new()
    if new_id:
        patch_start_time(new_id)


if __name__ == '__main__':
    main()
