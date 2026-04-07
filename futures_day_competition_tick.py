#!/usr/bin/env python3
"""
futures_day_competition_tick.py - 5-min tick engine for Futures Day league.

Identical to competition_tick.py but with futures mechanics:
  - Leverage applied to PnL (from strategy.yaml leverage field, default 2x)
  - Funding rate cost deducted every 8h on open positions (from TYR)
  - Liquidation: force-close if adverse move > 1/leverage - maintenance_margin
"""
import sys, os, json, yaml, urllib.request, fcntl
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'skills', 'competition-tick', 'scripts'))
from price_store import append_prices
from indicators import evaluate_entry

WORKSPACE      = os.environ.get('WORKSPACE', '/root/.openclaw/workspace')
FLEET_DIR      = os.path.join(WORKSPACE, 'fleet', 'futures_day')
ACTIVE_DIR     = os.path.join(WORKSPACE, 'competition', 'futures_day', 'active')
RESULTS_DIR    = os.path.join(WORKSPACE, 'competition', 'futures_day', 'results')
TYR_STATE_PATH = os.path.join(WORKSPACE, 'research', 'tyr_state.json')
LOCK_FILE      = '/tmp/futures_day_tick.lock'

MAINTENANCE_MARGIN = 0.05
DEFAULT_FUNDING_8H = 0.0001

KRAKEN_PAIR_MAP = {
    'BTC/USD': 'XBTUSD',  'ETH/USD': 'ETHUSD',  'SOL/USD': 'SOLUSD',
    'XRP/USD': 'XRPUSD',  'DOGE/USD':'DOGEUSD', 'AVAX/USD':'AVAXUSD',
    'LINK/USD':'LINKUSD', 'UNI/USD': 'UNIUSD',  'AAVE/USD':'AAVEUSD',
    'NEAR/USD':'NEARUSD', 'APT/USD': 'APTUSD',  'SUI/USD': 'SUIUSD',
    'ARB/USD': 'ARBUSD',  'OP/USD':  'OPUSD',   'ADA/USD': 'ADAUSD',
    'POL/USD': 'POLUSD',
}
KRAKEN_KEY_MAP = {
    'XXBTZUSD':'BTC/USD','XETHZUSD':'ETH/USD','SOLUSD':'SOL/USD','XXRPZUSD':'XRP/USD',
    'XDGUSD':'DOGE/USD','AVAXUSD':'AVAX/USD','LINKUSD':'LINK/USD','UNIUSD':'UNI/USD',
    'AAVEUSD':'AAVE/USD','NEARUSD':'NEAR/USD','APTUSD':'APT/USD','SUIUSD':'SUI/USD',
    'ARBUSD':'ARB/USD','OPUSD':'OP/USD','ADAUSD':'ADA/USD','POLUSD':'POL/USD',
}

lock_fh = open(LOCK_FILE, 'w')
try:
    fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print('Another futures_day tick running. Exiting.')
    sys.exit(0)


def log(msg, comp_dir=None):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f'[{ts}] {msg}'
    print(line)
    if comp_dir:
        with open(os.path.join(comp_dir, 'tick.log'), 'a') as f:
            f.write(line + '\n')


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
    if not os.path.exists(ACTIVE_DIR):
        return None, None, None
    entries = [d for d in os.listdir(ACTIVE_DIR)
               if os.path.isdir(os.path.join(ACTIVE_DIR, d))]
    if not entries:
        return None, None, None
    comp_id = sorted(entries)[-1]
    comp_dir = os.path.join(ACTIVE_DIR, comp_id)
    meta_path = os.path.join(comp_dir, 'meta.json')
    if not os.path.exists(meta_path):
        return None, None, None
    return comp_id, json.load(open(meta_path)), comp_dir


def fetch_prices(pairs):
    kraken_pairs = [KRAKEN_PAIR_MAP.get(p, p.replace('/', '')) for p in pairs]
    url = f"https://api.kraken.com/0/public/Ticker?pair={','.join(kraken_pairs)}"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())
    if data.get('error'):
        raise RuntimeError(str(data['error']))
    result = {}
    for k, v in data['result'].items():
        label = KRAKEN_KEY_MAP.get(k, k)
        result[label] = {'last': float(v['c'][0]), 'bid': float(v['b'][0]),
                         'ask': float(v['a'][0])}
    return result


def load_strategy(bot):
    path = os.path.join(FLEET_DIR, bot, 'strategy.yaml')
    return yaml.safe_load(open(path)) if os.path.exists(path) else None


def load_portfolio(comp_dir, bot):
    path = os.path.join(comp_dir, f'portfolio-{bot}.json')
    return json.load(open(path)) if os.path.exists(path) else None


def save_portfolio(comp_dir, bot, portfolio):
    with open(os.path.join(comp_dir, f'portfolio-{bot}.json'), 'w') as f:
        json.dump(portfolio, f, indent=2)


def load_risk_state(comp_dir):
    path = os.path.join(comp_dir, 'risk_state.json')
    return json.load(open(path)) if os.path.exists(path) else {}


def save_risk_state(comp_dir, state):
    with open(os.path.join(comp_dir, 'risk_state.json'), 'w') as f:
        json.dump(state, f, indent=2)


def close_position(portfolio, pos, exit_price, reason, leverage):
    pair = pos['pair']
    entry = pos['entry_price']
    qty = pos.get('quantity', 0)
    cost = pos.get('cost_basis', 0)
    direction = pos['direction']
    opened_at = datetime.fromisoformat(pos['opened_at'])
    age_h = (datetime.now(timezone.utc) - opened_at).total_seconds() / 3600

    if direction == 'long':
        raw_pnl = (exit_price - entry) * qty
    else:
        raw_pnl = (entry - exit_price) * qty

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
        'closed_at': datetime.now(timezone.utc).isoformat(),
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
    tp_pct = exit_rules.get('take_profit_pct', 1.5) / 100
    sl_pct = exit_rules.get('stop_loss_pct', 0.8) / 100
    timeout_min = exit_rules.get('timeout_minutes', 60)
    liq_threshold = (1.0 / leverage) * (1 - MAINTENANCE_MARGIN)
    actions = []

    for pos in list(portfolio.get('positions', [])):
        pair = pos['pair']
        current = (prices.get(pair) or {}).get('last')
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
            actions.append({'pair': pair, 'reason': reason})
    return actions


def check_entries(portfolio, strategy, history, prices, leverage):
    pos_cfg = strategy.get('position', {})
    max_open = pos_cfg.get('max_open', 2)
    size_pct = pos_cfg.get('size_pct', 12)
    exit_rules = strategy.get('exit', {})
    sl_pct = exit_rules.get('stop_loss_pct', 0.8) / 100
    tp_pct = exit_rules.get('take_profit_pct', 1.5) / 100
    entry_rules = strategy.get('entry', {})
    open_pairs = {p['pair'] for p in portfolio.get('positions', [])}
    actions = []

    if len(open_pairs) >= max_open:
        return actions

    for pair in strategy.get('pairs', []):
        if len(open_pairs) >= max_open:
            break
        if pair in open_pairs:
            continue
        current = (prices.get(pair) or {}).get('last')
        if current is None:
            continue
        for direction in ['long', 'short']:
            conds = (entry_rules.get(direction) or {}).get('conditions', [])
            if not conds:
                continue
            if evaluate_entry(conds, history, pair):
                eq = portfolio['stats'].get('current_equity',
                                            portfolio.get('starting_capital', 1000.0))
                margin = eq * size_pct / 100
                qty = (margin * leverage) / current
                portfolio.setdefault('positions', []).append({
                    'pair': pair, 'direction': direction, 'entry_price': current,
                    'quantity': round(qty, 8), 'cost_basis': round(margin, 4),
                    'leverage': leverage,
                    'opened_at': datetime.now(timezone.utc).isoformat(),
                })
                portfolio['cash'] = portfolio.get('cash', eq) - margin
                open_pairs.add(pair)
                actions.append({'pair': pair, 'direction': direction})
                break
    return actions


def check_risk(portfolio, strategy, risk_state, now_iso):
    bot = portfolio['bot']
    bot_state = risk_state.get(bot, {})
    if bot_state.get('stopped'):
        return 'stopped'
    paused_until = bot_state.get('paused_until')
    if paused_until and now_iso < paused_until:
        return 'paused'
    rules = strategy.get('risk', {})
    pnl_pct = portfolio['stats'].get('total_pnl_pct', 0)
    stop_pct = rules.get('stop_if_down_pct', 12)
    pause_pct = rules.get('pause_if_down_pct', 5)
    pause_min = rules.get('pause_minutes', 30)
    if pnl_pct <= -stop_pct:
        risk_state[bot] = {'stopped': True, 'paused_until': None}
        return 'stopped'
    if pnl_pct <= -pause_pct:
        pause_until = (datetime.now(timezone.utc) + timedelta(minutes=pause_min)).isoformat()
        risk_state[bot] = {'stopped': False, 'paused_until': pause_until}
        return 'paused'
    return 'ok'


def archive_competition(comp_dir, meta, prices):
    import shutil
    comp_id = meta['comp_id']
    now_iso = datetime.now(timezone.utc).isoformat()
    regime = get_tyr_regime(meta['started_at'], now_iso)
    leverage = float(meta.get('leverage_default', 2.0))
    scores = []
    for bot in meta['bots']:
        portfolio = load_portfolio(comp_dir, bot)
        if not portfolio:
            continue
        for pos in list(portfolio.get('positions', [])):
            cp = (prices.get(pos['pair']) or {}).get('last')
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
        'comp_id': comp_id, 'league': 'futures_day',
        'started_at': meta['started_at'], 'ended_at': now_iso,
        'duration_hours': meta.get('duration_hours', 24),
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
    log(f'Archived {comp_id} | winner: {final["winner"]} | regime: {regime}')


def main():
    comp_id, meta, comp_dir = find_active()
    if comp_id is None:
        print('No active futures_day competition.')
        return

    log(f'Futures day tick: {comp_id}', comp_dir)

    started = datetime.fromisoformat(meta['started_at'])
    expires_at = started + timedelta(hours=meta.get('duration_hours', 24))
    if datetime.now(timezone.utc) >= expires_at:
        log('Expired — archiving.', comp_dir)
        try:
            prices = fetch_prices(meta['pairs'])
        except Exception:
            prices = {}
        archive_competition(comp_dir, meta, prices)
        return

    try:
        prices = fetch_prices(meta['pairs'])
    except Exception as e:
        log(f'Price fetch failed: {e}', comp_dir)
        return

    history = append_prices(comp_dir, prices)
    risk_state = load_risk_state(comp_dir)
    now_iso = datetime.now(timezone.utc).isoformat()
    default_leverage = float(meta.get('leverage_default', 2.0))

    for bot in meta['bots']:
        strategy = load_strategy(bot)
        if strategy is None:
            continue
        portfolio = load_portfolio(comp_dir, bot)
        if portfolio is None:
            continue
        leverage = float(strategy.get('leverage', default_leverage))

        status = check_risk(portfolio, strategy, risk_state, now_iso)
        if status in ('paused', 'stopped'):
            log(f'  [{bot}] {status.upper()}', comp_dir)
            continue

        exits = check_exits(portfolio, strategy, prices, leverage)
        for a in exits:
            log(f'  [{bot}] CLOSE {a["pair"]} [{a["reason"]}]', comp_dir)

        portfolio = load_portfolio(comp_dir, bot)
        entries = check_entries(portfolio, strategy, history, prices, leverage)
        for a in entries:
            log(f'  [{bot}] OPEN {a["direction"].upper()} {a["pair"]}', comp_dir)

        portfolio = load_portfolio(comp_dir, bot)
        starting = meta.get('starting_capital', 1000.0)
        cash = portfolio.get('cash', starting)
        unrealized = 0.0
        for pos in portfolio.get('positions', []):
            cp = (prices.get(pos['pair']) or {}).get('last')
            if cp:
                ep = pos['entry_price']
                qty = pos.get('quantity', 0)
                pos_lev = float(pos.get('leverage', leverage))
                raw = (cp - ep) * qty if pos['direction'] == 'long' else (ep - cp) * qty
                unrealized += raw * pos_lev
        live_eq = cash + unrealized
        portfolio['stats']['live_equity_mtm'] = round(live_eq, 2)
        portfolio['stats']['live_pnl_usd'] = round(live_eq - starting, 2)
        portfolio['stats']['live_pnl_pct'] = round((live_eq - starting) / starting * 100, 4)
        save_portfolio(comp_dir, bot, portfolio)

        if not exits and not entries:
            eq = portfolio['stats']['live_equity_mtm']
            pnl = portfolio['stats']['live_pnl_pct']
            log(f'  [{bot}] no signal | eq=${eq:,.2f} | pnl={pnl:+.2f}%', comp_dir)

    save_risk_state(comp_dir, risk_state)
    log('Tick complete.', comp_dir)


if __name__ == '__main__':
    try:
        main()
    finally:
        fcntl.flock(lock_fh, fcntl.LOCK_UN)
        lock_fh.close()
