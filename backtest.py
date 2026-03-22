#!/usr/bin/env python3
"""
backtest.py - Replay historical Hyperliquid candle data against bot strategy YAML files.

Uses identical indicator and entry/exit logic as competition_tick.py.
Fetches 5-minute OHLCV from Hyperliquid public API (no account required).

Usage:
  python3 backtest.py --bot floki --days 30
  python3 backtest.py --bot bjorn --days 7 --pairs BTC/USD ETH/USD
  python3 backtest.py --all --days 30
"""
import sys
import os
import json
import argparse
import urllib.request
from datetime import datetime, timezone, timedelta

FLAT_THRESHOLD_PCT = 0.15


# ---------------------------------------------------------------------------
# Backtest-aware indicator evaluation
# Uses simulated candle timestamp as "now", not datetime.now()
# ---------------------------------------------------------------------------

def bt_get_price_n_minutes_ago(history, pair, minutes, sim_now_iso):
    """price_store.get_price_n_minutes_ago but relative to sim_now, not real clock."""
    if pair not in history or not history[pair]:
        return None
    sim_now = datetime.fromisoformat(sim_now_iso)
    target_iso = (sim_now - timedelta(minutes=minutes)).isoformat()
    past_ticks = [t for t in history[pair] if t["ts"] <= target_iso]
    if not past_ticks:
        return None
    return past_ticks[-1]["last"]


def bt_get_current_price(history, pair):
    if pair not in history or not history[pair]:
        return None
    return history[pair][-1]["last"]


def bt_get_current_vwap(history, pair):
    if pair not in history or not history[pair]:
        return None
    for tick in reversed(history[pair]):
        if "vwap" in tick:
            return tick["vwap"]
    return None


def _calc_ema(prices, n):
    """EMA over price list (oldest-first). n = number of periods."""
    k = 2 / (n + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema


def bt_get_price_series(history, pair, n_points, sim_now_iso, interval_minutes=5):
    """
    Returns list of n_points prices sampled at interval_minutes spacing,
    ordered oldest-first. Returns None if insufficient history.
    Mirrors _get_price_series in indicators.py but uses sim_now_iso.
    """
    prices = []
    for i in range(n_points):
        if i == 0:
            price = bt_get_current_price(history, pair)
        else:
            price = bt_get_price_n_minutes_ago(history, pair, i * interval_minutes, sim_now_iso)
        if price is None:
            return None
        prices.append(price)
    return list(reversed(prices))  # oldest -> newest


def bt_compute_indicator(name, history, pair, period_minutes, sim_now_iso):
    if name == "price_vs_vwap":
        current = bt_get_current_price(history, pair)
        vwap = bt_get_current_vwap(history, pair)
        if current is None or vwap is None or vwap == 0:
            return None
        diff_pct = (current - vwap) / vwap * 100
        if diff_pct > 0.05:
            return "above"
        if diff_pct < -0.05:
            return "below"
        return "at"

    if name == "price_change_pct":
        current = bt_get_current_price(history, pair)
        past = bt_get_price_n_minutes_ago(history, pair, period_minutes, sim_now_iso)
        if current is None or past is None or past == 0:
            return None
        return (current - past) / past * 100

    if name == "trend":
        current = bt_get_current_price(history, pair)
        past = bt_get_price_n_minutes_ago(history, pair, period_minutes, sim_now_iso)
        if current is None or past is None or past == 0:
            return None
        change = (current - past) / past * 100
        if change > FLAT_THRESHOLD_PCT:
            return "up"
        if change < -FLAT_THRESHOLD_PCT:
            return "down"
        return "flat"

    if name == "momentum_accelerating":
        half = period_minutes // 2
        if half < 1:
            return None
        current = bt_get_current_price(history, pair)
        mid = bt_get_price_n_minutes_ago(history, pair, half, sim_now_iso)
        start = bt_get_price_n_minutes_ago(history, pair, period_minutes, sim_now_iso)
        if any(v is None or v == 0 for v in [current, mid, start]):
            return None
        recent = abs((current - mid) / mid * 100)
        prior = abs((mid - start) / start * 100)
        return recent > prior

    if name == "rsi":
        n = max(period_minutes // 5, 2)
        prices = bt_get_price_series(history, pair, n + 1, sim_now_iso)
        if prices is None:
            return None
        changes = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
        gains = [max(c, 0) for c in changes]
        losses = [abs(min(c, 0)) for c in changes]
        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)

    if name == "price_vs_ema":
        n = max(period_minutes // 5, 2)
        prices = bt_get_price_series(history, pair, n, sim_now_iso)
        if prices is None:
            return None
        ema_val = _calc_ema(prices, n)
        current = bt_get_current_price(history, pair)
        if current is None:
            return None
        diff = (current - ema_val) / ema_val * 100
        if diff > 0.05:
            return "above"
        if diff < -0.05:
            return "below"
        return "at"

    if name == "bollinger_position":
        n = max(period_minutes // 5, 2)
        prices = bt_get_price_series(history, pair, n, sim_now_iso)
        if prices is None:
            return None
        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        std = variance ** 0.5
        if std == 0:
            return "inside"
        upper = mean + 2 * std
        lower = mean - 2 * std
        current = bt_get_current_price(history, pair)
        if current is None:
            return None
        if current > upper:
            return "above_upper"
        if current < lower:
            return "below_lower"
        return "inside"

    if name == "macd_signal":
        slow_n = max(period_minutes // 5, 4)
        fast_n = max(slow_n * 12 // 26, 2)
        signal_n = max(slow_n * 9 // 26, 2)
        total_needed = slow_n + signal_n - 1
        prices = bt_get_price_series(history, pair, total_needed, sim_now_iso)
        if prices is None:
            return None
        macd_values = []
        for i in range(signal_n):
            window = prices[i:i + slow_n]
            slow_ema = _calc_ema(window, slow_n)
            fast_ema = _calc_ema(window[slow_n - fast_n:], fast_n)
            macd_values.append(fast_ema - slow_ema)
        signal_line = _calc_ema(macd_values, signal_n)
        histogram = macd_values[-1] - signal_line
        if histogram > 0:
            return "bullish"
        if histogram < 0:
            return "bearish"
        return "neutral"

    raise ValueError(f"Unknown indicator: {name}")


def bt_evaluate_entry(conditions, history, pair, sim_now_iso):
    """Same AND logic as indicators.evaluate_entry but using simulated time."""
    results = []
    for cond in conditions:
        name = cond["indicator"]
        period = cond.get("period_minutes", 5)
        operator = cond["operator"]
        expected = cond["value"]
        if isinstance(expected, str):
            if expected.lower() == "true":
                expected = True
            elif expected.lower() == "false":
                expected = False
        actual = bt_compute_indicator(name, history, pair, period, sim_now_iso)
        if actual is None:
            results.append(None)
            continue
        if operator == "lt":
            results.append(actual < expected)
        elif operator == "gt":
            results.append(actual > expected)
        elif operator == "lte":
            results.append(actual <= expected)
        elif operator == "gte":
            results.append(actual >= expected)
        elif operator == "eq":
            results.append(actual == expected)
        elif operator == "in":
            results.append(actual in expected)
        else:
            raise ValueError(f"Unknown operator: {operator}")
    if None in results:
        return None
    return all(results)

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
FLEET_DIR = os.path.join(WORKSPACE, "fleet")
STARTING_CAPITAL = 10_000.0
FEE_RATE = 0.001
CANDLE_INTERVAL = "5m"
MAX_HISTORY_MINUTES = 360  # 6 hours rolling window (covers MACD warmup + 240min trend lookback)

KRAKEN_TO_HL = {
    "BTC/USD": "BTC",
    "ETH/USD": "ETH",
    "SOL/USD": "SOL",
    "XRP/USD": "XRP",
    "DOGE/USD": "DOGE",
    "AVAX/USD": "AVAX",
    "LINK/USD": "LINK",
    "UNI/USD": "UNI",
    "AAVE/USD": "AAVE",
    "NEAR/USD": "NEAR",
    "APT/USD": "APT",
    "SUI/USD": "SUI",
    "ARB/USD": "ARB",
    "OP/USD": "OP",
    "ADA/USD": "ADA",
    "POL/USD": "POL",
}


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_candles(coin, days):
    end = int(datetime.now(timezone.utc).timestamp() * 1000)
    start = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp() * 1000)
    payload = {
        "type": "candleSnapshot",
        "req": {"coin": coin, "interval": CANDLE_INTERVAL, "startTime": start, "endTime": end}
    }
    req = urllib.request.Request(
        "https://api.hyperliquid.xyz/info",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def load_strategy(bot_name):
    import yaml
    path = os.path.join(FLEET_DIR, bot_name, "strategy.yaml")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Price history (mirrors price_store.py format exactly)
# ---------------------------------------------------------------------------

def append_tick(history, pair, ts_iso, price, vwap=None):
    if pair not in history:
        history[pair] = []
    tick = {"ts": ts_iso, "last": price}
    if vwap is not None:
        tick["vwap"] = vwap
    history[pair].append(tick)
    cutoff = (datetime.fromisoformat(ts_iso) - timedelta(minutes=MAX_HISTORY_MINUTES)).isoformat()
    history[pair] = [t for t in history[pair] if t["ts"] >= cutoff]


def compute_vwap(candles, current_index, lookback_candles=288):
    """Rolling VWAP over last N candles. typical_price = (h+l+c)/3."""
    start = max(0, current_index - lookback_candles + 1)
    window = candles[start:current_index + 1]
    cum_tp_vol = sum((float(c["h"]) + float(c["l"]) + float(c["c"])) / 3 * float(c["v"]) for c in window)
    cum_vol = sum(float(c["v"]) for c in window)
    if cum_vol == 0:
        return None
    return cum_tp_vol / cum_vol


# ---------------------------------------------------------------------------
# Portfolio management (mirrors trade_execute.py logic exactly)
# ---------------------------------------------------------------------------

def make_portfolio(bot_name):
    return {
        "bot": bot_name,
        "cash": STARTING_CAPITAL,
        "positions": [],
        "closed_trades": [],
        "stats": {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "total_pnl_usd": 0.0,
            "total_pnl_pct": 0.0,
            "total_fees": 0.0,
            "max_drawdown_pct": 0.0,
            "largest_win_pct": 0.0,
            "largest_loss_pct": 0.0,
            "current_equity": STARTING_CAPITAL,
            "peak_equity": STARTING_CAPITAL,
        }
    }


def recalc_equity(portfolio):
    return portfolio["cash"] + sum(p["cost_basis"] for p in portfolio["positions"])


def update_drawdown(portfolio):
    equity = portfolio["stats"]["current_equity"]
    peak = portfolio["stats"]["peak_equity"]
    if equity > peak:
        portfolio["stats"]["peak_equity"] = equity
    else:
        dd = (peak - equity) / peak * 100
        if dd > portfolio["stats"]["max_drawdown_pct"]:
            portfolio["stats"]["max_drawdown_pct"] = round(dd, 4)


def open_position(portfolio, pair, direction, price, size_pct, sl_pct, tp_pct, ts_iso):
    if any(p["pair"] == pair for p in portfolio["positions"]):
        return None
    cash = portfolio["cash"]
    deploy = cash * (size_pct / 100)
    entry_fee = deploy * FEE_RATE
    cost_basis = deploy - entry_fee
    quantity = cost_basis / price
    portfolio["cash"] = round(cash - deploy, 8)
    sl_price = price * (1 - sl_pct) if direction == "long" else price * (1 + sl_pct)
    tp_price = price * (1 + tp_pct) if direction == "long" else price * (1 - tp_pct)
    portfolio["positions"].append({
        "pair": pair, "direction": direction, "entry_price": price,
        "quantity": round(quantity, 8), "cost_basis": round(cost_basis, 2),
        "entry_fee": round(entry_fee, 2), "stop_loss": round(sl_price, 4),
        "take_profit": round(tp_price, 4), "opened_at": ts_iso,
    })
    portfolio["stats"]["total_fees"] = round(portfolio["stats"]["total_fees"] + entry_fee, 2)
    portfolio["stats"]["current_equity"] = round(recalc_equity(portfolio), 2)
    update_drawdown(portfolio)
    return {"pair": pair, "direction": direction, "entry": price, "sl": sl_price, "tp": tp_price}


def close_position(portfolio, pair, price, reason, ts_iso):
    pos_list = [p for p in portfolio["positions"] if p["pair"] == pair]
    if not pos_list:
        return None
    pos = pos_list[0]
    entry = pos["entry_price"]
    qty = pos["quantity"]
    cost_basis = pos["cost_basis"]
    direction = pos["direction"]
    gross_pnl = (price - entry) * qty if direction == "long" else (entry - price) * qty
    close_fee = cost_basis * FEE_RATE
    net_pnl = gross_pnl - close_fee
    proceeds = cost_basis + net_pnl
    pnl_pct = round(net_pnl / cost_basis * 100, 4)
    won = net_pnl > 0
    portfolio["cash"] = round(portfolio["cash"] + proceeds, 8)
    portfolio["positions"] = [p for p in portfolio["positions"] if p["pair"] != pair]
    portfolio["closed_trades"].append({
        "pair": pair, "direction": direction, "entry_price": entry,
        "exit_price": price, "net_pnl": round(net_pnl, 2),
        "pnl_pct": pnl_pct, "reason": reason,
        "opened_at": pos["opened_at"], "closed_at": ts_iso,
    })
    stats = portfolio["stats"]
    stats["total_trades"] += 1
    stats["wins"] += 1 if won else 0
    stats["losses"] += 0 if won else 1
    stats["win_rate"] = round(stats["wins"] / stats["total_trades"] * 100, 1)
    stats["total_pnl_usd"] = round(stats["total_pnl_usd"] + net_pnl, 2)
    stats["total_pnl_pct"] = round(stats["total_pnl_usd"] / STARTING_CAPITAL * 100, 4)
    stats["total_fees"] = round(stats["total_fees"] + close_fee, 2)
    stats["current_equity"] = round(recalc_equity(portfolio), 2)
    update_drawdown(portfolio)
    if pnl_pct > stats["largest_win_pct"]:
        stats["largest_win_pct"] = pnl_pct
    if pnl_pct < stats["largest_loss_pct"]:
        stats["largest_loss_pct"] = pnl_pct
    return {"pair": pair, "direction": direction, "exit": price,
            "net_pnl": round(net_pnl, 2), "pnl_pct": pnl_pct, "reason": reason}


# ---------------------------------------------------------------------------
# Risk management (mirrors competition_tick.py exactly)
# ---------------------------------------------------------------------------

def check_risk(portfolio, strategy, risk_state):
    bot = portfolio["bot"]
    bot_state = risk_state.get(bot, {})
    if bot_state.get("stopped"):
        return "stopped"
    risk_rules = strategy.get("risk", {})
    total_pnl_pct = portfolio["stats"]["total_pnl_pct"]
    if total_pnl_pct <= -risk_rules.get("stop_if_down_pct", 10):
        risk_state[bot] = {"stopped": True}
        return "stopped"
    if total_pnl_pct <= -risk_rules.get("pause_if_down_pct", 5):
        return "paused"
    return "ok"


# ---------------------------------------------------------------------------
# Core backtest loop
# ---------------------------------------------------------------------------

def run_backtest(bot_name, pairs, days, verbose=False):
    strategy = load_strategy(bot_name)
    if strategy is None:
        return {"bot": bot_name, "error": "No strategy.yaml found"}

    has_conditions = any(
        strategy.get("entry", {}).get(d, {}).get("conditions", [])
        for d in ["long", "short"]
    )
    if not has_conditions:
        return {"bot": bot_name, "error": "No entry conditions (placeholder strategy)"}

    print(f"  Fetching {days}d of {CANDLE_INTERVAL} candles...")
    candle_data = {}
    for pair in pairs:
        coin = KRAKEN_TO_HL.get(pair)
        if not coin:
            continue
        candle_data[pair] = fetch_candles(coin, days)
        print(f"    {pair}: {len(candle_data[pair])} candles")

    if not candle_data:
        return {"bot": bot_name, "error": "No candle data fetched"}

    all_timestamps = sorted(set(
        c["t"] for pc in candle_data.values() for c in pc
    ))

    portfolio = make_portfolio(bot_name)
    history = {}
    risk_state = {}
    exit_cfg = strategy.get("exit", {})
    pos_cfg = strategy.get("position", {})
    tp_pct = exit_cfg.get("take_profit_pct", 1.0) / 100
    sl_pct = exit_cfg.get("stop_loss_pct", 0.5) / 100
    timeout_min = exit_cfg.get("timeout_minutes", 60)
    size_pct = pos_cfg.get("size_pct", 20)
    max_open = pos_cfg.get("max_open", 1)
    entry_rules = strategy.get("entry", {})
    trades_log = []
    prices = {}

    # Build index lookup for fast candle access
    candle_index = {pair: {c["t"]: i for i, c in enumerate(candles)}
                    for pair, candles in candle_data.items()}

    for ts_ms in all_timestamps:
        ts_iso = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()
        for pair, candles in candle_data.items():
            idx = candle_index[pair].get(ts_ms)
            if idx is not None:
                c = candles[idx]
                prices[pair] = float(c["c"])
                vwap = compute_vwap(candles, idx)
                append_tick(history, pair, ts_iso, prices[pair], vwap=vwap)

        status = check_risk(portfolio, strategy, risk_state)
        if status == "stopped":
            break
        if status == "paused":
            continue

        # Check exits
        for pos in list(portfolio["positions"]):
            pair = pos["pair"]
            current = prices.get(pair)
            if current is None:
                continue
            entry = pos["entry_price"]
            direction = pos["direction"]
            opened_dt = datetime.fromisoformat(pos["opened_at"])
            current_dt = datetime.fromisoformat(ts_iso)
            age_min = (current_dt - opened_dt).total_seconds() / 60
            pnl_pct = ((current - entry) / entry) if direction == "long" else ((entry - current) / entry)
            reason = None
            if pnl_pct >= tp_pct:
                reason = "target"
            elif pnl_pct <= -sl_pct:
                reason = "stop"
            elif age_min >= timeout_min:
                reason = "timeout"
            if reason:
                result = close_position(portfolio, pair, current, reason, ts_iso)
                if result:
                    if verbose:
                        print(f"    CLOSE {result['direction'].upper()} {pair} "
                              f"pnl={result['pnl_pct']:+.2f}% [{reason}] @ {ts_iso[:16]}")
                    trades_log.append({**result, "ts": ts_iso})

        # Check entries
        open_pairs = {p["pair"] for p in portfolio["positions"]}
        if len(open_pairs) < max_open:
            for pair in strategy.get("pairs", []):
                if pair in open_pairs or len(open_pairs) >= max_open:
                    break
                current = prices.get(pair)
                if current is None:
                    continue
                for direction in ["long", "short"]:
                    conditions = entry_rules.get(direction, {}).get("conditions", [])
                    if not conditions:
                        continue
                    signal = bt_evaluate_entry(conditions, history, pair, ts_iso)
                    if signal:
                        result = open_position(portfolio, pair, direction, current,
                                               size_pct, sl_pct, tp_pct, ts_iso)
                        if result:
                            if verbose:
                                print(f"    OPEN {direction.upper()} {pair} @ {current} "
                                      f"sl={result['sl']:.2f} tp={result['tp']:.2f} @ {ts_iso[:16]}")
                            open_pairs.add(pair)
                            break

    # Force-close open positions at last known price
    for pos in list(portfolio["positions"]):
        pair = pos["pair"]
        last = prices.get(pair)
        if last:
            close_position(portfolio, pair, last, "timeout", ts_iso)

    stats = portfolio["stats"]
    return {
        "bot": bot_name,
        "days": days,
        "candles_processed": len(all_timestamps),
        "total_trades": stats["total_trades"],
        "wins": stats["wins"],
        "losses": stats["losses"],
        "win_rate_pct": stats["win_rate"],
        "total_pnl_usd": stats["total_pnl_usd"],
        "total_pnl_pct": stats["total_pnl_pct"],
        "total_fees_usd": stats["total_fees"],
        "max_drawdown_pct": stats["max_drawdown_pct"],
        "largest_win_pct": stats["largest_win_pct"],
        "largest_loss_pct": stats["largest_loss_pct"],
        "final_equity": stats["current_equity"],
        "trades": trades_log,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Backtest bot strategies against historical data")
    parser.add_argument("--bot", help="Bot name (e.g. floki)")
    parser.add_argument("--all", action="store_true", help="Run all bots with assigned strategies")
    parser.add_argument("--days", type=int, default=30, help="Days of history (default: 30)")
    parser.add_argument("--pairs", nargs="+", default=["BTC/USD", "ETH/USD"])
    parser.add_argument("--verbose", action="store_true", help="Print each trade as it happens")
    args = parser.parse_args()

    bots = []
    if args.all:
        bots = ["floki", "bjorn", "lagertha"]
    elif args.bot:
        bots = [args.bot]
    else:
        parser.print_help()
        sys.exit(1)

    user_specified_pairs = "--pairs" in " ".join(sys.argv)
    results = []
    for bot in bots:
        pairs = args.pairs
        if not user_specified_pairs:
            strategy = load_strategy(bot)
            if strategy and strategy.get("pairs"):
                pairs = strategy["pairs"]
        print(); print("Backtesting", bot, "over", args.days, "days...")
        result = run_backtest(bot, pairs, args.days, verbose=args.verbose)
        results.append(result)
    print("\n" + "=" * 60)
    print(f"BACKTEST RESULTS  {args.days}d | $10,000 starting capital")
    print("=" * 60)
    for r in results:
        if "error" in r:
            print(f"\n{r.get('bot', '?')}: SKIP -- {r['error']}")
            continue
        sign = "+" if r["total_pnl_usd"] >= 0 else ""
        print(f"\n{r['bot'].upper()}")
        print(f"  Trades:       {r['total_trades']} ({r['wins']}W / {r['losses']}L)  {r['win_rate_pct']}% win rate")
        print(f"  PnL:          {sign}${r['total_pnl_usd']:,.2f} ({sign}{r['total_pnl_pct']:.2f}%)")
        print(f"  Final equity: ${r['final_equity']:,.2f}")
        print(f"  Fees paid:    ${r['total_fees_usd']:,.2f}")
        print(f"  Max drawdown: {r['max_drawdown_pct']:.2f}%")
        print(f"  Largest win:  {r['largest_win_pct']:+.2f}%")
        print(f"  Largest loss: {r['largest_loss_pct']:+.2f}%")
        print(f"  Candles:      {r['candles_processed']:,}")

    print("\n" + "=" * 60)
    out_path = os.path.join(WORKSPACE, "competition", "backtest_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Full results saved to {out_path}")


if __name__ == "__main__":
    main()
