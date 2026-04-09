#!/usr/bin/env python3
"""
futures_swing_competition_tick.py - 30-min tick engine for Futures Swing league.
Same as swing_competition_tick.py but with futures mechanics (leverage, funding, liquidation).
"""
import sys, os, json, yaml, fcntl
from datetime import datetime, timezone, timedelta

WORKSPACE      = os.environ.get('WORKSPACE', '/root/.openclaw/workspace')
FLEET_DIR      = os.path.join(WORKSPACE, 'fleet', 'futures_swing')
ACTIVE_DIR     = os.path.join(WORKSPACE, 'competition', 'futures_swing', 'active')
RESULTS_DIR    = os.path.join(WORKSPACE, 'competition', 'futures_swing', 'results')
TYR_STATE_PATH = os.path.join(WORKSPACE, 'research', 'tyr_state.json')
LOCK_FILE      = '/tmp/futures_swing_tick.lock'

sys.path.insert(0, WORKSPACE)
from swing_price_store import get_current_price, update_pair
from swing_indicators import evaluate_entry

MAINTENANCE_MARGIN = 0.05
DEFAULT_FUNDING_8H = 0.0001

ALL_PAIRS = [
    'BTC/USD', 'ETH/USD', 'SOL/USD', 'XRP/USD', 'DOGE/USD', 'AVAX/USD',
    'LINK/USD', 'UNI/USD', 'AAVE/USD', 'NEAR/USD', 'APT/USD', 'SUI/USD',
    'ARB/USD', 'OP/USD', 'ADA/USD', 'POL/USD',
]

lock_fh = open(LOCK_FILE, 'w')
try:
    fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print('Another futures_swing tick running. Exiting.')
    sys.exit(0)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def get_funding_rate():
    try:
        state = json.load(open(TYR_STATE_PATH))
        rate = (state.get('funding_rates') or {}).get('avg_pct')
        if rate is not None:
            return abs(float(rate)) / 100
    except Exception:
        pass
    return DEFAULT_FUNDING_8H


def get_tyr_regime(started_at_iso, ended_at_iso=None):
    if not os.path.exists(TYR_STATE_PATH):
        return None
    try:
        state = json.load(open(TYR_STATE_PATH))
        entries = state.get('log', [])
        window = [e for e in entries if e.get('ts', '') >= started_at_iso
                  and (ended_at_iso is None or e.get('ts', '') <= ended_at_iso)]
        if not window:
            window = [entries[-1]] if entries else []
        if not window:
            return state.get('regime')
        counts = {}
        for e in window:
            r = e.get('regime', 'NORMAL')
            counts[r] = counts.get(r, 0) + 1
        return max(counts, key=counts.get)
    except Exception:
        return None


def find_active():
    if not os.path.isdir(ACTIVE_DIR):
        return None, None, None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None, None, None
    comp_id = entries[-1]
    comp_dir = os.path.join(ACTIVE_DIR, comp_id)
    meta_path = os.path.join(comp_dir, 'meta.json')
    if not os.path.isfile(meta_path):
        return None, None, None
    return comp_id, json.load(open(meta_path)), comp_dir


def load_strategy(bot):
    path = os.path.join(FLEET_DIR, bot, 'strategy.yaml')
    return yaml.safe_load(open(path)) if os.path.exists(path) else None


def load_portfolio(comp_dir, bot):
    path = os.path.join(comp_dir, f'portfolio-{bot}.json')
    return json.load(open(path)) if os.path.exists(path) else None


def save_portfolio(comp_dir, bot, portfolio):
    with open(os.path.join(comp_dir, f'portfolio-{bot}.json'), 'w') as f:
        json.dump(portfolio, f, indent=2)


def close_position(portfolio, pos, exit_price, reason, leverage):
    pair = pos['pair']
    entry = pos['entry_price']
    qty = pos.get('quantity', 0)
    cost = pos.get('cost_basis', 0)
    direction = pos['direction']
    opened_at = datetime.fromisoformat(pos['opened_at'])
    age_h = (datetime.now(timezone.utc) - opened_at).total_seconds() / 3600

    raw_pnl = ((exit_price - entry) * qty if direction == 'long'
               else (entry - exit_price) * qty)
    lev_pnl = raw_pnl * leverage
    funding_cost = get_funding_rate() * leverage * cost * int(age_h / 8)
    net_pnl = lev_pnl - funding_cost
    net_pct = (net_pnl / cost * 100) if cost > 0 else 0

    portfolio['cash'] = portfolio.get('cash', 0) + cost + net_pnl
    portfolio['positions'] = [p for p in portfolio.get('positions', [])
                               if not (p['pair'] == pair and p['opened_at'] == pos['opened_at'])]
    portfolio.setdefault('closed_trades', []).append({
        'pair': pair, 'direction': direction, 'reason': reason,
        'entry_price': entry, 'exit_price': exit_price,
        'pnl_usd': round(net_pnl, 4), 'pnl_pct': round(net_pct, 4),
        'funding_cost': round(funding_cost, 4), 'leverage': leverage,
        'won': net_pnl > 0,
        'opened_at': pos['opened_at'],
        'closed_at': now_iso(),
    })
    s = portfolio.setdefault('stats', {})
    s['total_trades'] = s.get('total_trades', 0) + 1
    if net_pnl > 0:
        s['wins'] = s.get('wins', 0) + 1
    else:
        s['losses'] = s.get('losses', 0) + 1
    s['total_pnl_usd'] = round(s.get('total_pnl_usd', 0) + net_pnl, 4)
    eq = portfolio['cash']
    s['current_equity'] = round(eq, 2)
    start = portfolio.get('starting_capital', 1000.0)
    s['total_pnl_pct'] = round((eq - start) / start * 100, 4)
    if eq > s.get('peak_equity', start):
        s['peak_equity'] = eq
    total = s['total_trades']
    s['win_rate'] = round(s.get('wins', 0) / total * 100, 2) if total > 0 else 0.0


def check_exits(portfolio, strategy, prices, leverage):
    exit_rules = strategy.get('exit', {})
    tp_pct = exit_rules.get('take_profit_pct', 5.0) / 100
    sl_pct = exit_rules.get('stop_loss_pct', 2.5) / 100
    if 'timeout_hours' in exit_rules:
        timeout_min = float(exit_rules['timeout_hours']) * 60
    else:
        timeout_min = float(exit_rules.get('timeout_minutes', 4320))
    liq_threshold = (1.0 / leverage) * (1 - MAINTENANCE_MARGIN)
    actions = []

    for pos in list(portfolio.get('positions', [])):
        pair = pos['pair']
        current = prices.get(pair)
        if current is None:
            continue
        entry = pos['entry_price']
        direction = pos['direction']
        opened_at = datetime.fromisoformat(pos['opened_at'])
        age_min = (datetime.now(timezone.utc) - opened_at).total_seconds() / 60
        pnl_r = ((current - entry) / entry if direction == 'long'
                 else (entry - current) / entry)

        reason = None
        if pnl_r <= -liq_threshold:
            reason = 'liquidated'
        elif pnl_r >= tp_pct:
            reason = 'target'
        elif pnl_r <= -sl_pct:
            reason = 'stop'
        elif age_min >= timeout_min:
            reason = 'timeout'

        if reason:
            close_position(portfolio, pos, current, reason, leverage)
            sign = '+' if (pnl_r * leverage * 100) >= 0 else ''
            print(f'  CLOSE {pos["direction"]:5} {pair} [{reason}] {sign}{pnl_r * leverage * 100:.2f}%')
            actions.append({'pair': pair, 'reason': reason})
    return actions


def check_entries(portfolio, strategy, prices, leverage):
    pos_cfg = strategy.get('position', {})
    max_open = pos_cfg.get('max_open', 2)
    size_pct = pos_cfg.get('size_pct', 15)
    exit_rules = strategy.get('exit', {})
    sl_pct = exit_rules.get('stop_loss_pct', 2.5) / 100
    tp_pct = exit_rules.get('take_profit_pct', 5.0) / 100
    entry_rules = strategy.get('entry', {})
    open_pairs = {p['pair'] for p in portfolio.get('positions', [])}
    actions = []

    if len(open_pairs) >= max_open:
        return actions

    for pair in ALL_PAIRS:
        if len(open_pairs) >= max_open:
            break
        if pair in open_pairs:
            continue
        current = prices.get(pair)
        if current is None:
            continue
        for direction in ['long', 'short']:
            conds = (entry_rules.get(direction) or {}).get('conditions', [])
            if not conds:
                continue
            if evaluate_entry(conds, pair):
                eq = portfolio['stats'].get('current_equity',
                                            portfolio.get('starting_capital', 1000.0))
                margin = eq * size_pct / 100
                qty = (margin * leverage) / current
                portfolio.setdefault('positions', []).append({
                    'pair': pair, 'direction': direction, 'entry_price': current,
                    'quantity': round(qty, 8), 'cost_basis': round(margin, 4),
                    'leverage': leverage,
                    'opened_at': now_iso(),
                })
                portfolio['cash'] = portfolio.get('cash', eq) - margin
                open_pairs.add(pair)
                print(f'  OPEN  {direction:5} {pair} @ {current}')
                actions.append({'pair': pair, 'direction': direction})
                break
    return actions


def archive_competition(comp_dir, meta, bots, prices):
    import shutil
    comp_id = meta['comp_id']
    end_iso = now_iso()
    regime = get_tyr_regime(meta['started_at'], end_iso)
    leverage = float(meta.get('leverage_default', 2.0))
    scores = []
    for bot in bots:
        portfolio = load_portfolio(comp_dir, bot)
        if not portfolio:
            continue
        for pos in list(portfolio.get('positions', [])):
            cp = prices.get(pos['pair'])
            if cp:
                close_position(portfolio, pos, cp, 'timeout', leverage)
        save_portfolio(comp_dir, bot, portfolio)
        s = portfolio['stats']
        scores.append({'bot': bot,
                       'final_equity': round(s.get('current_equity', 1000), 2),
                       'total_pnl_pct': round(s.get('total_pnl_pct', 0), 4),
                       'total_trades': s.get('total_trades', 0),
                       'win_rate': s.get('win_rate', 0)})
    scores.sort(key=lambda x: x['total_pnl_pct'], reverse=True)
    final = {
        'comp_id': comp_id, 'league': 'futures_swing',
        'started_at': meta['started_at'], 'ended_at': end_iso,
        'duration_hours': meta.get('duration_hours', 168),
        'tyr_regime': regime, 'scores': scores,
        'winner': scores[0]['bot'] if scores else None,
    }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, f'{comp_id}_score.json'), 'w') as f:
        json.dump(final, f, indent=2)
    dest = os.path.join(RESULTS_DIR, comp_id)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.move(comp_dir, dest)
    print(f'  Archived {comp_id} | winner: {final["winner"]} | regime: {regime}')


def main():
    comp_id, meta, comp_dir = find_active()
    if comp_id is None:
        print('No active futures_swing competition.')
        return

    bots = meta.get('bots', [])
    pairs = meta.get('pairs', ALL_PAIRS)
    leverage = float(meta.get('leverage_default', 2.0))

    print(f'Futures swing tick: {comp_id}  {now_iso()[:16]}')

    # Refresh price data
    for pair in pairs:
        update_pair(pair, full=False)
    prices = {pair: get_current_price(pair) for pair in pairs}

    started_at = datetime.fromisoformat(meta['started_at'])
    expires_at = started_at + timedelta(hours=meta.get('duration_hours', 168))
    if datetime.now(timezone.utc) >= expires_at:
        print('  Competition expired — archiving...')
        archive_competition(comp_dir, meta, bots, prices)
        import subprocess
        subprocess.run([sys.executable,
                        os.path.join(WORKSPACE, 'futures_swing_restart.py')],
                       cwd=WORKSPACE)
        return

    hours_left = (expires_at - datetime.now(timezone.utc)).total_seconds() / 3600
    print(f'  {hours_left:.1f}h remaining')

    for bot in bots:
        portfolio = load_portfolio(comp_dir, bot)
        if not portfolio:
            continue
        strategy = load_strategy(bot)
        if not strategy:
            continue
        bot_leverage = float(strategy.get('leverage', leverage))

        check_exits(portfolio, strategy, prices, bot_leverage)
        save_portfolio(comp_dir, bot, portfolio)

        portfolio = load_portfolio(comp_dir, bot)
        check_entries(portfolio, strategy, prices, bot_leverage)
        save_portfolio(comp_dir, bot, portfolio)

        # Update live MTM equity
        # cash = starting - deployed_margins + realized_pnl; add margins back + unrealized
        portfolio = load_portfolio(comp_dir, bot)
        starting = portfolio.get('starting_capital', meta.get('starting_capital', 1000.0))
        cash = portfolio.get('cash', starting)
        unrealized = 0.0
        margin_deployed = 0.0
        for pos in portfolio.get('positions', []):
            cp = prices.get(pos['pair'])
            if cp:
                ep = pos['entry_price']
                qty = pos.get('quantity', 0)
                cost = pos.get('cost_basis', 0)
                margin_deployed += cost
                if pos['direction'] == 'long':
                    unrealized += (cp - ep) * qty
                else:
                    unrealized += (ep - cp) * qty
        live_eq = cash + margin_deployed + unrealized
        portfolio.setdefault('stats', {})['live_equity_mtm'] = round(live_eq, 2)
        portfolio['stats']['live_pnl_usd'] = round(live_eq - starting, 2)
        portfolio['stats']['live_pnl_pct'] = round((live_eq - starting) / starting * 100, 4)
        save_portfolio(comp_dir, bot, portfolio)

    print('  Done.')


if __name__ == '__main__':
    try:
        main()
    finally:
        fcntl.flock(lock_fh, fcntl.LOCK_UN)
        lock_fh.close()
