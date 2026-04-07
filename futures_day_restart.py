#!/usr/bin/env python3
"""
futures_day_restart.py - Daily 09:00 UTC restart for Futures Day league.
Same logic as day_daily_restart.py but targets futures_day fleet and competition dirs.
"""
import os, json, subprocess, sys, shutil
from datetime import datetime, timezone

WORKSPACE        = os.environ.get('WORKSPACE', '/root/.openclaw/workspace')
ACTIVE_DIR       = os.path.join(WORKSPACE, 'competition', 'futures_day', 'active')
RESULTS_DIR      = os.path.join(WORKSPACE, 'competition', 'futures_day', 'results')
CYCLE_STATE_PATH = os.path.join(WORKSPACE, 'competition', 'futures_day', 'cycle_state.json')
FLEET_DIR        = os.path.join(WORKSPACE, 'fleet', 'futures_day')
ODIN_BEST        = os.path.join(WORKSPACE, 'research', 'futures_day', 'best_strategy.yaml')
AUTOBOT_STRATEGY = os.path.join(FLEET_DIR, 'autobotdayfutures', 'strategy.yaml')
LOKI_LOG         = os.path.join(WORKSPACE, 'research', 'loki_log.jsonl')

ALL_BOTS = [
    'brandr', 'ketil', 'vikar', 'starkad', 'orvar', 'asmund',
    'helgi', 'kveldulf', 'ulfhedinn', 'haki', 'hakon', 'vemund',
    'autobotdayfutures',
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
        return {'cycle': 1, 'sprint_in_cycle': 0, 'sprints_per_cycle': 7,
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


def hours_running(meta):
    started = datetime.fromisoformat(meta['started_at'].replace('Z', '+00:00'))
    return (datetime.now(timezone.utc) - started).total_seconds() / 3600


def write_loki_activity(actions):
    entry = {
        'ts':       datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M'),
        'mimir_ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M'),
        'league':   'futures_day',
        'gen':      'inject',
        'actions':  actions,
        'dry_run':  False,
    }
    try:
        with open(LOKI_LOG, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f'  [loki] log write failed: {e}')


def inject_odin_strategy():
    if not os.path.exists(ODIN_BEST):
        print('  [odin] No futures_day best_strategy.yaml yet — autobotdayfutures keeps current strategy.')
        return
    try:
        shutil.copy2(ODIN_BEST, AUTOBOT_STRATEGY)
        print(f'  [odin] Injected futures_day best strategy -> autobotdayfutures')
        write_loki_activity(['odin_inject: autobotdayfutures <- best futures_day strategy'])
    except Exception as e:
        print(f'  [odin] Injection failed: {e}')


def archive_current(comp_id):
    import subprocess as sp
    score_script = os.path.join(WORKSPACE, 'skills', 'competition-score', 'scripts', 'competition_score.py')
    # Use built-in archiving via futures tick (already handles futures P&L)
    # Fallback: just move the directory
    src = os.path.join(ACTIVE_DIR, comp_id)
    dest = os.path.join(RESULTS_DIR, comp_id)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.move(src, dest)
    print(f'  Archived: {comp_id}')
    return True


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
    comp_id = now.strftime('fut-day-%Y%m%d-%H%M')
    comp_dir = os.path.join(ACTIVE_DIR, comp_id)
    os.makedirs(comp_dir, exist_ok=True)

    valid_bots = [b for b in ALL_BOTS
                  if os.path.exists(os.path.join(FLEET_DIR, b, 'strategy.yaml'))]

    for bot in valid_bots:
        portfolio = {
            'bot': bot, 'competition_id': comp_id,
            'duration_hours': 24, 'started_at': now.isoformat(),
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
        'comp_id': comp_id, 'duration_hours': 24,
        'started_at': now.isoformat(), 'pairs': ALL_PAIRS,
        'bots': valid_bots, 'starting_capital': STARTING_CAPITAL,
        'fee_rate': 0.0005, 'status': 'active',
        'league': 'futures_day', 'leverage_default': LEVERAGE_DEFAULT,
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
    print(f'[futures_day_restart] {now}')

    comp_dir, meta = find_active()

    if meta is None:
        print('  No active sprint — starting new.')
        inject_odin_strategy()
        new_id = start_new()
        if new_id:
            patch_start_time(new_id)
        return

    elapsed = hours_running(meta)
    print(f'  Active: {meta["comp_id"]} ({elapsed:.1f}h elapsed)')

    if elapsed >= 20.0:
        print('  Sprint >= 20h — archiving and starting new.')
        inject_odin_strategy()
        if archive_current(meta['comp_id']):
            new_id = start_new()
            if new_id:
                patch_start_time(new_id)
    else:
        print('  Sprint < 20h — keeping current sprint.')


if __name__ == '__main__':
    main()
