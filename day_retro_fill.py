#!/usr/bin/env python3
"""
day_retro_fill.py - Retroactively fill a Day Trading sprint with real historical data.

Fetches 5-min OHLCV from Kraken for all sprint pairs from sprint.started_at to now,
then replays the full tick logic for each candle using sim_time-based indicator
evaluation. Writes results directly to the active competition portfolio files.

Usage:
  python3 day_retro_fill.py              # fill and write
  python3 day_retro_fill.py --dry-run    # show signals without writing
"""
import os, sys, json, yaml, math, time
import urllib.request
from datetime import datetime, timezone, timedelta

WORKSPACE   = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
ACTIVE_DIR  = os.path.join(WORKSPACE, "competition", "active")
FLEET_DIR   = os.path.join(WORKSPACE, "fleet")
FEE_RATE    = 0.001
FLAT_THRESHOLD = 0.15
MAX_HISTORY    = 72   # 6h of 5-min ticks — enough for all indicators

KRAKEN_MAP = {
    "BTC/USD":  "XBTUSD",
    "ETH/USD":  "ETHUSD",
    "SOL/USD":  "SOLUSD",
    "XRP/USD":  "XRPUSD",
    "DOGE/USD": "XDGUSD",
    "AVAX/USD": "AVAXUSD",
    "LINK/USD": "LINKUSD",
}


# ---------------------------------------------------------------------------
# Sprint / portfolio helpers
# ---------------------------------------------------------------------------

def find_active():
    if not os.path.isdir(ACTIVE_DIR):
        return None, None, None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None, None, None
    comp_id  = entries[-1]
    comp_dir = os.path.join(ACTIVE_DIR, comp_id)
    with open(os.path.join(comp_dir, "meta.json")) as f:
        meta = json.load(f)
    return comp_id, comp_dir, meta


def load_portfolio(comp_dir, bot):
    with open(os.path.join(comp_dir, f"portfolio-{bot}.json")) as f:
        return json.load(f)


def save_portfolio(comp_dir, bot, p):
    import tempfile
    path = os.path.join(comp_dir, f"portfolio-{bot}.json")
    dir_ = os.path.dirname(path)
    with tempfile.NamedTemporaryFile("w", dir=dir_, delete=False, suffix=".tmp") as tf:
        json.dump(p, tf, indent=2)
        tmp = tf.name
    os.replace(tmp, path)


def load_strategy(bot):
    path = os.path.join(FLEET_DIR, bot, "strategy.yaml")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Kraken OHLC fetching
# ---------------------------------------------------------------------------

def fetch_ohlc(pair, since_ts):
    """Fetch 5-min OHLC from Kraken since unix timestamp.
    Returns list of (unix_ts, close, vwap)."""
    kraken_pair = KRAKEN_MAP.get(pair, pair.replace("/", ""))
    url = (f"https://api.kraken.com/0/public/OHLC"
           f"?pair={kraken_pair}&interval=5&since={int(since_ts)}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                data = json.loads(r.read())
            break
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)
    if data.get("error"):
        raise RuntimeError(f"Kraken error for {pair}: {data['error']}")
    result_key = next(k for k in data["result"] if k != "last")
    # [time, open, high, low, close, vwap, volume, count]
    return [(int(c[0]), float(c[4]), float(c[5])) for c in data["result"][result_key]]


# ---------------------------------------------------------------------------
# Indicators — all accept explicit sim_now (no datetime.now() calls)
# ---------------------------------------------------------------------------

def _calc_ema(prices, n):
    k = 2 / (n + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema


def _current(history, pair, sim_now):
    iso = sim_now.isoformat()
    ticks = [t for t in history.get(pair, []) if t["ts"] <= iso]
    return ticks[-1]["last"] if ticks else None


def _n_ago(history, pair, minutes, sim_now):
    iso = (sim_now - timedelta(minutes=minutes)).isoformat()
    ticks = [t for t in history.get(pair, []) if t["ts"] <= iso]
    return ticks[-1]["last"] if ticks else None


def _vwap(history, pair, sim_now):
    iso = sim_now.isoformat()
    ticks = [t for t in history.get(pair, []) if t["ts"] <= iso and "vwap" in t]
    return ticks[-1]["vwap"] if ticks else None


def _series(history, pair, n, interval_min, sim_now):
    prices = []
    for i in range(n):
        p = (_current(history, pair, sim_now) if i == 0
             else _n_ago(history, pair, i * interval_min, sim_now))
        if p is None:
            return None
        prices.append(p)
    return list(reversed(prices))


def ind_price_change_pct(history, pair, period, sim_now):
    cur = _current(history, pair, sim_now)
    old = _n_ago(history, pair, period, sim_now)
    if cur is None or old is None or old == 0:
        return None
    return (cur - old) / old * 100


def ind_trend(history, pair, period, sim_now):
    chg = ind_price_change_pct(history, pair, period, sim_now)
    if chg is None:
        return None
    return "up" if chg > FLAT_THRESHOLD else ("down" if chg < -FLAT_THRESHOLD else "flat")


def ind_momentum_accelerating(history, pair, period, sim_now):
    half = period // 2
    cur = _current(history, pair, sim_now)
    mid = _n_ago(history, pair, half, sim_now)
    start = _n_ago(history, pair, period, sim_now)
    if any(v is None or v == 0 for v in [cur, mid, start]):
        return None
    return abs((cur - mid) / mid * 100) > abs((mid - start) / start * 100)


def ind_price_vs_vwap(history, pair, period, sim_now):
    cur = _current(history, pair, sim_now)
    vwap = _vwap(history, pair, sim_now)
    if cur is None or vwap is None or vwap == 0:
        return None
    diff = (cur - vwap) / vwap * 100
    return "above" if diff > 0.05 else ("below" if diff < -0.05 else "at")


def ind_rsi(history, pair, period, sim_now):
    n = max(period // 5, 2)
    prices = _series(history, pair, n + 1, 5, sim_now)
    if prices is None:
        return None
    changes = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
    avg_gain = sum(max(c, 0) for c in changes) / len(changes)
    avg_loss = sum(abs(min(c, 0)) for c in changes) / len(changes)
    if avg_loss == 0:
        return 100.0
    return round(100 - 100 / (1 + avg_gain / avg_loss), 2)


def ind_price_vs_ema(history, pair, period, sim_now):
    n = max(period // 5, 2)
    prices = _series(history, pair, n, 5, sim_now)
    if prices is None:
        return None
    ema_val = _calc_ema(prices, n)
    cur = _current(history, pair, sim_now)
    if cur is None:
        return None
    diff = (cur - ema_val) / ema_val * 100
    return "above" if diff > 0.05 else ("below" if diff < -0.05 else "at")


def ind_bollinger_position(history, pair, period, sim_now):
    n = max(period // 5, 2)
    prices = _series(history, pair, n, 5, sim_now)
    if prices is None:
        return None
    mean = sum(prices) / len(prices)
    std  = math.sqrt(sum((p - mean) ** 2 for p in prices) / len(prices))
    cur  = _current(history, pair, sim_now)
    if cur is None or std == 0:
        return "inside"
    if cur > mean + 2 * std:
        return "above_upper"
    if cur < mean - 2 * std:
        return "below_lower"
    return "inside"


def ind_macd_signal(history, pair, period, sim_now):
    slow_n   = max(period // 5, 4)
    fast_n   = max(slow_n * 12 // 26, 2)
    signal_n = max(slow_n * 9 // 26, 2)
    total    = slow_n + signal_n - 1
    prices   = _series(history, pair, total, 5, sim_now)
    if prices is None:
        return None
    macd_vals = []
    for i in range(signal_n):
        w = prices[i:i + slow_n]
        macd_vals.append(_calc_ema(w[slow_n - fast_n:], fast_n) - _calc_ema(w, slow_n))
    hist = macd_vals[-1] - _calc_ema(macd_vals, signal_n)
    return "bullish" if hist > 0 else ("bearish" if hist < 0 else "neutral")


INDICATOR_FNS = {
    "price_change_pct":      ind_price_change_pct,
    "trend":                 ind_trend,
    "momentum_accelerating": ind_momentum_accelerating,
    "price_vs_vwap":         ind_price_vs_vwap,
    "rsi":                   ind_rsi,
    "price_vs_ema":          ind_price_vs_ema,
    "bollinger_position":    ind_bollinger_position,
    "macd_signal":           ind_macd_signal,
}


def evaluate_entry(conditions, history, pair, sim_now):
    """Returns True (all conditions met), False (any failed), None (insufficient data)."""
    for cond in conditions:
        fn = INDICATOR_FNS.get(cond["indicator"])
        if fn is None:
            raise ValueError(f"Unknown indicator: {cond['indicator']}")
        actual = fn(history, pair, cond.get("period_minutes", 5), sim_now)
        if actual is None:
            return None
        expected = cond["value"]
        if isinstance(expected, str):
            if expected.lower() == "true":
                expected = True
            elif expected.lower() == "false":
                expected = False
        op = cond["operator"]
        if   op == "lt":  passed = actual < expected
        elif op == "gt":  passed = actual > expected
        elif op == "lte": passed = actual <= expected
        elif op == "gte": passed = actual >= expected
        elif op == "eq":  passed = actual == expected
        elif op == "in":  passed = actual in expected
        else: raise ValueError(f"Unknown operator: {op}")
        if not passed:
            return False
    return True


# ---------------------------------------------------------------------------
# Portfolio trade execution (matches trade_execute.py exactly)
# ---------------------------------------------------------------------------

def recalc_equity(p):
    return p["cash"] + sum(pos["cost_basis"] for pos in p["positions"])


def open_trade(p, pair, direction, price, size_pct, tp_pct, sl_pct, sim_now):
    if any(pos["pair"] == pair for pos in p["positions"]):
        return None
    deploy = p["cash"] * (size_pct / 100.0)
    if deploy <= 0 or deploy > p["cash"]:
        return None
    entry_fee  = deploy * FEE_RATE
    cost_basis = deploy - entry_fee
    quantity   = cost_basis / price
    if direction == "long":
        stop_p = price * (1 - sl_pct / 100)
        tp_p   = price * (1 + tp_pct / 100)
    else:
        stop_p = price * (1 + sl_pct / 100)
        tp_p   = price * (1 - tp_pct / 100)
    p["cash"] = round(p["cash"] - deploy, 8)
    p["positions"].append({
        "pair":        pair,
        "direction":   direction,
        "entry_price": price,
        "quantity":    round(quantity, 8),
        "cost_basis":  round(cost_basis, 2),
        "entry_fee":   round(entry_fee, 2),
        "stop_loss":   round(stop_p, 6),
        "take_profit": round(tp_p, 6),
        "opened_at":   sim_now.isoformat(),
    })
    s = p["stats"]
    s["total_fees"]     = round(s["total_fees"] + entry_fee, 2)
    s["current_equity"] = round(recalc_equity(p), 2)
    if s["current_equity"] > s["peak_equity"]:
        s["peak_equity"] = s["current_equity"]
    return {"action": "open", "pair": pair, "direction": direction,
            "price": price, "qty": round(quantity, 8), "fee": round(entry_fee, 2)}


def close_trade(p, pair, price, reason, sim_now):
    pos_list = [pos for pos in p["positions"] if pos["pair"] == pair]
    if not pos_list:
        return None
    pos        = pos_list[0]
    direction  = pos["direction"]
    cost_basis = pos["cost_basis"]
    qty        = pos["quantity"]
    entry      = pos["entry_price"]
    gross_pnl  = ((price - entry) * qty if direction == "long"
                  else (entry - price) * qty)
    close_fee  = cost_basis * FEE_RATE
    net_pnl    = gross_pnl - close_fee
    proceeds   = cost_basis + net_pnl
    pnl_pct    = round(net_pnl / cost_basis * 100, 4)
    won        = net_pnl > 0
    p["cash"]  = round(p["cash"] + proceeds, 8)
    p["positions"] = [pos for pos in p["positions"] if pos["pair"] != pair]
    p["closed_trades"].append({
        "pair": pair, "direction": direction,
        "entry_price": entry, "exit_price": price, "quantity": qty,
        "cost_basis": cost_basis, "gross_pnl": round(gross_pnl, 2),
        "close_fee": round(close_fee, 2), "net_pnl": round(net_pnl, 2),
        "pnl_pct": pnl_pct, "reason": reason,
        "opened_at": pos["opened_at"], "closed_at": sim_now.isoformat(),
    })
    s = p["stats"]
    s["total_trades"] += 1
    s["wins"]          += 1 if won else 0
    s["losses"]        += 0 if won else 1
    s["win_rate"]       = round(s["wins"] / s["total_trades"] * 100, 1)
    s["total_pnl_usd"]  = round(s["total_pnl_usd"] + net_pnl, 2)
    s["total_pnl_pct"]  = round(s["total_pnl_usd"] / p["starting_capital"] * 100, 4)
    s["total_fees"]     = round(s["total_fees"] + close_fee, 2)
    s["current_equity"] = round(recalc_equity(p), 2)
    peak = s["peak_equity"]
    if s["current_equity"] > peak:
        s["peak_equity"] = s["current_equity"]
    else:
        dd = (peak - s["current_equity"]) / peak * 100
        if dd > s["max_drawdown_pct"]:
            s["max_drawdown_pct"] = round(dd, 4)
    if pnl_pct > s["largest_win_pct"]:
        s["largest_win_pct"] = pnl_pct
    if pnl_pct < s["largest_loss_pct"]:
        s["largest_loss_pct"] = pnl_pct
    return {"action": "close", "pair": pair, "direction": direction,
            "price": price, "net_pnl": round(net_pnl, 2),
            "pnl_pct": pnl_pct, "reason": reason}


# ---------------------------------------------------------------------------
# Risk check (mirrors competition_tick.py)
# ---------------------------------------------------------------------------

def check_risk(p, strategy, risk_state, sim_now):
    bot   = p["bot"]
    state = risk_state.get(bot, {})
    if state.get("stopped"):
        return "stopped"
    paused_until = state.get("paused_until")
    if paused_until and sim_now.isoformat() < paused_until:
        return "paused"
    risk   = strategy.get("risk", {})
    pnl    = p["stats"]["total_pnl_pct"]
    stop_p = risk.get("stop_if_down_pct", 10)
    pause_p = risk.get("pause_if_down_pct", 5)
    pause_m = risk.get("pause_minutes", 60)
    if pnl <= -stop_p:
        risk_state[bot] = {"stopped": True, "paused_until": None}
        return "stopped"
    if pnl <= -pause_p:
        risk_state[bot] = {
            "stopped": False,
            "paused_until": (sim_now + timedelta(minutes=pause_m)).isoformat(),
        }
        return "paused"
    return "ok"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    dry_run = "--dry-run" in sys.argv

    comp_id, comp_dir, meta = find_active()
    if not comp_dir:
        print("No active day trading sprint found.")
        sys.exit(1)

    start_dt = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    now_dt   = datetime.now(timezone.utc)
    pairs    = meta["pairs"]
    bots     = meta["bots"]

    # Kraken returns the last-closed candle, so the most recent candle
    # may be up to 5 min old. Cut off 5 min from the end.
    fill_until = now_dt - timedelta(minutes=5)

    print(f"Retro fill: {comp_id}")
    print(f"  From   : {start_dt.strftime('%Y-%m-%d %H:%M UTC')} (sprint start)")
    print(f"  Through: {fill_until.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Pairs  : {', '.join(pairs)}")
    print(f"  Bots   : {', '.join(bots)}")
    if dry_run:
        print("  Mode   : DRY RUN — no changes will be written")

    # --- Fetch OHLC ---
    since_ts   = int(start_dt.timestamp()) - 300
    ohlc_data  = {}
    print(f"\nFetching 5-min OHLC from Kraken...")
    for pair in pairs:
        try:
            candles = fetch_ohlc(pair, since_ts)
            candles = [(ts, close, vwap) for (ts, close, vwap) in candles
                       if start_dt.timestamp() <= ts <= fill_until.timestamp()]
            ohlc_data[pair] = sorted(candles, key=lambda c: c[0])
            print(f"  {pair:<12} {len(candles)} candles")
            time.sleep(0.25)
        except Exception as e:
            print(f"  {pair:<12} ERROR: {e}")
            ohlc_data[pair] = []

    if all(len(v) == 0 for v in ohlc_data.values()):
        print("No OHLC data fetched. Aborting.")
        sys.exit(1)

    # --- Build unified 5-min timeline ---
    all_ts = sorted(set(ts for c in ohlc_data.values() for (ts, _, _) in c))
    print(f"\nTimeline: {len(all_ts)} ticks  "
          f"({(all_ts[-1]-all_ts[0])//3600}h {((all_ts[-1]-all_ts[0])%3600)//60}m covered)")

    # Fast lookup: pair -> {ts: (close, vwap)}
    candle_map = {}
    for pair in pairs:
        candle_map[pair] = {ts: (close, vwap) for (ts, close, vwap) in ohlc_data.get(pair, [])}

    # --- Load portfolios / strategies ---
    portfolios = {bot: load_portfolio(comp_dir, bot) for bot in bots}
    strategies = {bot: load_strategy(bot) for bot in bots}
    risk_path  = os.path.join(comp_dir, "risk_state.json")
    risk_state = {}
    if os.path.isfile(risk_path):
        with open(risk_path) as f:
            risk_state = json.load(f)

    # Incremental price history built tick by tick
    history  = {pair: [] for pair in pairs}
    trade_log = []

    print(f"\nReplaying...")
    for tick_i, ts in enumerate(all_ts):
        sim_now = datetime.fromtimestamp(ts, tz=timezone.utc)

        # Append this candle to rolling history for all pairs
        for pair in pairs:
            if ts in candle_map.get(pair, {}):
                close, vwap = candle_map[pair][ts]
                history[pair].append({"ts": sim_now.isoformat(), "last": close, "vwap": vwap})
                if len(history[pair]) > MAX_HISTORY:
                    history[pair] = history[pair][-MAX_HISTORY:]

        # Current prices at this tick
        cur_prices = {pair: candle_map[pair][ts][0]
                      for pair in pairs if ts in candle_map.get(pair, {})}
        if not cur_prices:
            continue

        for bot in bots:
            strategy = strategies.get(bot)
            p        = portfolios[bot]
            if strategy is None:
                continue

            status = check_risk(p, strategy, risk_state, sim_now)
            if status in ("paused", "stopped"):
                continue

            exit_rules  = strategy.get("exit", {})
            tp_pct      = exit_rules.get("take_profit_pct", 0.5)
            sl_pct      = exit_rules.get("stop_loss_pct", 0.3)
            timeout_min = exit_rules.get("timeout_minutes", 30)

            # --- Exits ---
            for pos in list(p.get("positions", [])):
                pair = pos["pair"]
                cur  = cur_prices.get(pair)
                if cur is None:
                    continue
                direction = pos["direction"]
                entry     = pos["entry_price"]
                pnl_pct   = ((cur - entry) / entry if direction == "long"
                             else (entry - cur) / entry) * 100
                age_min   = (sim_now - datetime.fromisoformat(
                    pos["opened_at"].replace("Z", "+00:00"))).total_seconds() / 60

                reason = None
                if pnl_pct >= tp_pct:
                    reason = "target"
                elif pnl_pct <= -sl_pct:
                    reason = "stop"
                elif age_min >= timeout_min:
                    reason = "timeout"

                if reason:
                    r = close_trade(p, pair, cur, reason, sim_now)
                    if r:
                        trade_log.append({"tick": sim_now.isoformat(), "bot": bot, **r})
                        sign = "+" if r["pnl_pct"] >= 0 else ""
                        print(f"  {sim_now.strftime('%m-%d %H:%M')} {bot:10} "
                              f"CLOSE {direction:5} {pair:10} "
                              f"{reason:8} {sign}{r['pnl_pct']:.2f}%  "
                              f"${r['net_pnl']:+.2f}")

            # --- Entries ---
            pos_cfg  = strategy.get("position", {})
            max_open = pos_cfg.get("max_open", 1)
            size_pct = pos_cfg.get("size_pct", 20)
            open_pairs = {pos["pair"] for pos in p.get("positions", [])}

            if len(open_pairs) >= max_open:
                continue

            entry_rules = strategy.get("entry", {})
            for pair in strategy.get("pairs", []):
                if pair in open_pairs or len(open_pairs) >= max_open:
                    break
                cur = cur_prices.get(pair)
                if cur is None:
                    continue
                for direction in ["long", "short"]:
                    conditions = entry_rules.get(direction, {}).get("conditions", [])
                    if not conditions:
                        continue
                    signal = evaluate_entry(conditions, history, pair, sim_now)
                    if not signal:
                        continue
                    r = open_trade(p, pair, direction, cur, size_pct, tp_pct, sl_pct, sim_now)
                    if r:
                        trade_log.append({"tick": sim_now.isoformat(), "bot": bot, **r})
                        open_pairs.add(pair)
                        print(f"  {sim_now.strftime('%m-%d %H:%M')} {bot:10} "
                              f"OPEN  {direction:5} {pair:10} "
                              f"@ ${cur:>10.4f}")
                    break

        if (tick_i + 1) % 50 == 0:
            pct = (tick_i + 1) / len(all_ts) * 100
            print(f"  ... {tick_i+1}/{len(all_ts)} ticks ({pct:.0f}%)")

    # --- Write results ---
    if not dry_run:
        for bot in bots:
            save_portfolio(comp_dir, bot, portfolios[bot])
        with open(risk_path, "w") as f:
            json.dump(risk_state, f, indent=2)
        print(f"\nWrote {len(bots)} portfolios to {comp_dir}")

    # --- Summary table ---
    print(f"\n{'BOT':12} {'TRADES':>7} {'WINS':>5} {'PNL USD':>10} {'EQUITY':>10}")
    print("─" * 52)
    total_trades = 0
    for bot in sorted(bots):
        s = portfolios[bot]["stats"]
        sign = "+" if s["total_pnl_usd"] >= 0 else ""
        print(f"{bot:12} {s['total_trades']:>7} {s['wins']:>5} "
              f"{sign}${s['total_pnl_usd']:>8.2f}   ${s['current_equity']:>8.2f}")
        total_trades += s["total_trades"]
    print("─" * 52)
    print(f"Total trades retroactively filled: {total_trades}")
    if dry_run:
        print("(dry-run — no changes written)")


if __name__ == "__main__":
    main()
