#!/usr/bin/env python3
"""
odin_backtest.py - Research backtest engine for Odin.

Reads local CSV data (from prepare.py), runs a strategy dict against it,
returns Sharpe ratio + standard metrics. Used by odin_researcher.py.

Supports both day (period_minutes) and swing (period_hours) strategy YAMLs.
"""
import csv
import math
import os
from collections import deque
from datetime import datetime, timezone, timedelta

DATA_DIR       = "/root/.openclaw/workspace/research/data"
STARTING_CAP   = 10_000.0
FEE_RATE       = 0.001
FLAT_THRESHOLD = 0.15
SUSPICIOUS_SHARPE   = 3.5
SUSPICIOUS_WINRATE  = 85.0


# ---------------------------------------------------------------------------
# CSV loader (cached — data files don't change during a research run)
# ---------------------------------------------------------------------------

_csv_cache: dict = {}

def load_csv(path):
    if path in _csv_cache:
        return _csv_cache[path]
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "ts_ms":  int(row["timestamp"]),
                "open":   float(row["open"]),
                "high":   float(row["high"]),
                "low":    float(row["low"]),
                "close":  float(row["close"]),
                "volume": float(row["volume"]),
            })
    _csv_cache[path] = rows
    return rows


# ---------------------------------------------------------------------------
# Rolling VWAP (24h: 288 candles @ 5m, 24 candles @ 1h)
# ---------------------------------------------------------------------------

def make_vwap_calc(window):
    buf = deque(maxlen=window)
    def calc(high, low, close, volume):
        tp = (high + low + close) / 3
        buf.append((tp * volume, volume))
        cum_tpv = sum(x[0] for x in buf)
        cum_vol = sum(x[1] for x in buf)
        return cum_tpv / cum_vol if cum_vol > 0 else close
    return calc


# ---------------------------------------------------------------------------
# Indicator functions
# ---------------------------------------------------------------------------

def _get_price_n_ago(history, minutes, sim_now_iso):
    target = (datetime.fromisoformat(sim_now_iso) - timedelta(minutes=minutes)).isoformat()
    ticks = [t for t in history if t["ts"] <= target]
    return ticks[-1]["last"] if ticks else None


def _get_price_series(history, n, sim_now_iso, interval_minutes):
    prices = []
    for i in range(n):
        mins = i * interval_minutes
        p = history[-1]["last"] if mins == 0 else _get_price_n_ago(history, mins, sim_now_iso)
        if p is None:
            return None
        prices.append(p)
    return list(reversed(prices))


def _calc_ema(prices, n):
    k = 2 / (n + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema


def compute_indicator(name, history, period_minutes, sim_now_iso, interval_minutes):
    if not history:
        return None
    current = history[-1]["last"]
    vwap    = history[-1].get("vwap")

    if name == "price_vs_vwap":
        if not vwap or vwap == 0:
            return None
        d = (current - vwap) / vwap * 100
        return "above" if d > 0.05 else ("below" if d < -0.05 else "at")

    if name == "price_change_pct":
        past = _get_price_n_ago(history, period_minutes, sim_now_iso)
        if not past or past == 0:
            return None
        return (current - past) / past * 100

    if name == "trend":
        past = _get_price_n_ago(history, period_minutes, sim_now_iso)
        if not past or past == 0:
            return None
        ch = (current - past) / past * 100
        return "up" if ch > FLAT_THRESHOLD else ("down" if ch < -FLAT_THRESHOLD else "flat")

    if name == "momentum_accelerating":
        half = period_minutes // 2
        if half < 1:
            return None
        mid   = _get_price_n_ago(history, half, sim_now_iso)
        start = _get_price_n_ago(history, period_minutes, sim_now_iso)
        if not mid or not start or start == 0:
            return None
        recent = abs((current - mid) / mid * 100)
        prior  = abs((mid - start) / start * 100)
        return recent > prior

    if name == "rsi":
        n = max(period_minutes // interval_minutes, 2)
        prices = _get_price_series(history, n + 1, sim_now_iso, interval_minutes)
        if prices is None:
            return None
        changes = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        ag = sum(max(c, 0) for c in changes) / len(changes)
        al = sum(abs(min(c, 0)) for c in changes) / len(changes)
        if al == 0:
            return 100.0
        return round(100 - 100 / (1 + ag / al), 2)

    if name == "price_vs_ema":
        n = max(period_minutes // interval_minutes, 2)
        prices = _get_price_series(history, n, sim_now_iso, interval_minutes)
        if prices is None:
            return None
        ema = _calc_ema(prices, n)
        d = (current - ema) / ema * 100
        return "above" if d > 0.05 else ("below" if d < -0.05 else "at")

    if name == "bollinger_position":
        n = max(period_minutes // interval_minutes, 2)
        prices = _get_price_series(history, n, sim_now_iso, interval_minutes)
        if prices is None:
            return None
        mean = sum(prices) / len(prices)
        std  = math.sqrt(sum((p - mean)**2 for p in prices) / len(prices))
        if std == 0:
            return "inside"
        upper = mean + 2 * std
        lower = mean - 2 * std
        return "above_upper" if current > upper else ("below_lower" if current < lower else "inside")

    if name == "macd_signal":
        slow_n   = max(period_minutes // interval_minutes, 4)
        fast_n   = max(slow_n * 12 // 26, 2)
        signal_n = max(slow_n * 9  // 26, 2)
        total    = slow_n + signal_n - 1
        prices = _get_price_series(history, total, sim_now_iso, interval_minutes)
        if prices is None:
            return None
        macd_vals = []
        for i in range(signal_n):
            w = prices[i:i + slow_n]
            macd_vals.append(_calc_ema(w[slow_n - fast_n:], fast_n) - _calc_ema(w, slow_n))
        sig_line = _calc_ema(macd_vals, signal_n)
        h = macd_vals[-1] - sig_line
        return "bullish" if h > 0 else ("bearish" if h < 0 else "neutral")

    return None


def evaluate_entry(conditions, history, sim_now_iso, interval_minutes):
    for cond in conditions:
        name     = cond["indicator"]
        # Support both period_minutes (day) and period_hours (swing)
        if "period_hours" in cond:
            period_m = cond["period_hours"] * 60
        else:
            period_m = cond.get("period_minutes", 5)
        operator = cond["operator"]
        expected = cond["value"]
        if isinstance(expected, str) and expected.lower() in ("true", "false"):
            expected = expected.lower() == "true"
        actual = compute_indicator(name, history, period_m, history[-1]["ts"], interval_minutes)
        if actual is None:
            return None
        if operator == "eq":
            ok = actual == expected
        elif operator == "in":
            ok = actual in expected
        elif operator == "lt":
            ok = actual < expected
        elif operator == "gt":
            ok = actual > expected
        elif operator == "lte":
            ok = actual <= expected
        elif operator == "gte":
            ok = actual >= expected
        else:
            return None
        if not ok:
            return False
    return True


# ---------------------------------------------------------------------------
# Portfolio helpers
# ---------------------------------------------------------------------------

def make_portfolio():
    return {
        "cash": STARTING_CAP,
        "positions": [],
        "closed_trades": [],
        "equity_snapshots": [],
        "peak_equity": STARTING_CAP,
        "max_drawdown": 0.0,
    }


def current_equity(p):
    return p["cash"] + sum(pos["cost_basis"] for pos in p["positions"])


def snapshot_equity(p, ts_ms):
    eq = current_equity(p)
    p["equity_snapshots"].append((ts_ms, eq))
    if eq > p["peak_equity"]:
        p["peak_equity"] = eq
    elif p["peak_equity"] > 0:
        dd = (p["peak_equity"] - eq) / p["peak_equity"] * 100
        if dd > p["max_drawdown"]:
            p["max_drawdown"] = dd


def open_pos(p, pair, direction, price, size_pct, sl_pct, tp_pct, ts_iso):
    if any(pos["pair"] == pair for pos in p["positions"]):
        return False
    deploy   = p["cash"] * (size_pct / 100)
    fee      = deploy * FEE_RATE
    cost     = deploy - fee
    quantity = cost / price
    p["cash"] -= deploy
    sl = price * (1 - sl_pct) if direction == "long" else price * (1 + sl_pct)
    tp = price * (1 + tp_pct) if direction == "long" else price * (1 - tp_pct)
    p["positions"].append({
        "pair": pair, "direction": direction, "entry_price": price,
        "quantity": quantity, "cost_basis": cost, "stop_loss": sl,
        "take_profit": tp, "opened_at": ts_iso,
    })
    return True


def close_pos(p, pair, price, reason, ts_iso):
    for pos in list(p["positions"]):
        if pos["pair"] != pair:
            continue
        entry = pos["entry_price"]
        qty   = pos["quantity"]
        cost  = pos["cost_basis"]
        gross = (price - entry) * qty if pos["direction"] == "long" else (entry - price) * qty
        fee   = cost * FEE_RATE
        net   = gross - fee
        p["cash"] += cost + net
        p["positions"] = [x for x in p["positions"] if x["pair"] != pair]
        p["closed_trades"].append({"pnl_pct": net / cost * 100, "won": net > 0})
        return net / cost * 100
    return None


# ---------------------------------------------------------------------------
# Sharpe (daily equity-based, annualised)
# ---------------------------------------------------------------------------

def compute_sharpe(snapshots):
    if len(snapshots) < 2:
        return 0.0
    day_eq = {}
    for ts_ms, eq in snapshots:
        day = ts_ms // 86_400_000
        day_eq[day] = eq
    days = sorted(day_eq.keys())
    if len(days) < 2:
        return 0.0
    rets = [(day_eq[days[i]] - day_eq[days[i-1]]) / day_eq[days[i-1]]
            for i in range(1, len(days)) if day_eq[days[i-1]] > 0]
    if len(rets) < 2:
        return 0.0
    mean_r = sum(rets) / len(rets)
    std_r  = math.sqrt(sum((r - mean_r)**2 for r in rets) / len(rets))
    if std_r == 0:
        return -999.0  # flat equity = 0 trades = always worse than any trading strategy
    return round(mean_r / std_r * math.sqrt(365), 4)


# ---------------------------------------------------------------------------
# Main backtest
# ---------------------------------------------------------------------------

def run_backtest(strategy, league, pairs=None):
    """
    Run strategy dict against 2yr local CSV data.

    Returns dict with: sharpe, win_rate_pct, total_pnl_pct, total_trades,
                       max_drawdown_pct, final_equity, suspicious, suspicious_reason
    """
    interval_minutes = 5 if league == "day" else 60
    vwap_window      = 288 if league == "day" else 24
    interval_label   = "5m" if league == "day" else "1h"
    max_history_min  = 10_200 if league == "swing" else 400

    test_pairs = pairs or strategy.get("pairs", ["BTC/USD"])

    # Load CSV data
    candle_data = {}
    for pair in test_pairs:
        fname = pair.replace("/", "_") + "_" + interval_label + ".csv"
        path  = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            return {"error": "Missing data: " + path + ". Run prepare.py first."}
        candle_data[pair] = load_csv(path)

    if not candle_data:
        return {"error": "No data loaded"}

    all_ts  = sorted(set(c["ts_ms"] for rows in candle_data.values() for c in rows))
    idx_map = {pair: {c["ts_ms"]: i for i, c in enumerate(rows)}
               for pair, rows in candle_data.items()}
    vwap_calcs = {pair: make_vwap_calc(vwap_window) for pair in test_pairs}

    # Strategy params
    exit_cfg = strategy.get("exit", {})
    pos_cfg  = strategy.get("position", {})
    tp_pct   = exit_cfg.get("take_profit_pct", 1.0) / 100
    sl_pct   = exit_cfg.get("stop_loss_pct",   0.5) / 100
    if "timeout_hours" in exit_cfg:
        timeout_min = exit_cfg["timeout_hours"] * 60
    else:
        timeout_min = exit_cfg.get("timeout_minutes", 120)
    size_pct  = pos_cfg.get("size_pct", 20)
    max_open  = pos_cfg.get("max_open", 1)
    stop_pct  = strategy.get("risk", {}).get("stop_if_down_pct", 15)
    entry_rules = strategy.get("entry", {})

    portfolio = make_portfolio()
    history   = {pair: [] for pair in test_pairs}
    prices    = {}
    ts_iso    = ""
    snap_every = 12 if league == "day" else 1

    for tick_i, ts_ms in enumerate(all_ts):
        ts_iso = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()

        # Update rolling history
        for pair, rows in candle_data.items():
            idx = idx_map[pair].get(ts_ms)
            if idx is None:
                continue
            row   = rows[idx]
            price = row["close"]
            vwap  = vwap_calcs[pair](row["high"], row["low"], price, row["volume"])
            prices[pair] = price
            cutoff = (datetime.fromisoformat(ts_iso) - timedelta(minutes=max_history_min)).isoformat()
            history[pair] = [t for t in history[pair] if t["ts"] >= cutoff]
            history[pair].append({"ts": ts_iso, "last": price, "vwap": vwap})

        if tick_i % snap_every == 0:
            snapshot_equity(portfolio, ts_ms)

        # Risk stop
        total_pnl = (current_equity(portfolio) - STARTING_CAP) / STARTING_CAP * 100
        if total_pnl <= -stop_pct:
            break

        # Exits
        for pos in list(portfolio["positions"]):
            pair    = pos["pair"]
            current = prices.get(pair)
            if current is None:
                continue
            direction = pos["direction"]
            entry     = pos["entry_price"]
            opened_dt = datetime.fromisoformat(pos["opened_at"])
            age_min   = (datetime.fromisoformat(ts_iso) - opened_dt).total_seconds() / 60
            pnl_r     = (current - entry) / entry if direction == "long" else (entry - current) / entry
            reason = None
            if pnl_r >= tp_pct:
                reason = "target"
            elif pnl_r <= -sl_pct:
                reason = "stop"
            elif age_min >= timeout_min:
                reason = "timeout"
            if reason:
                close_pos(portfolio, pair, current, reason, ts_iso)

        # Entries
        open_pairs = {pos["pair"] for pos in portfolio["positions"]}
        if len(open_pairs) < max_open:
            for pair in strategy.get("pairs", test_pairs):
                if pair not in prices or pair in open_pairs or len(open_pairs) >= max_open:
                    continue
                hist = history.get(pair, [])
                if len(hist) < 3:
                    continue
                for direction in ["long", "short"]:
                    conds = entry_rules.get(direction, {}).get("conditions", [])
                    if not conds:
                        continue
                    sig = evaluate_entry(conds, hist, ts_iso, interval_minutes)
                    if sig:
                        if open_pos(portfolio, pair, direction, prices[pair],
                                    size_pct, sl_pct, tp_pct, ts_iso):
                            open_pairs.add(pair)
                            break

    # Force-close remaining
    for pos in list(portfolio["positions"]):
        pair = pos["pair"]
        if pair in prices:
            close_pos(portfolio, pair, prices[pair], "timeout", ts_iso)
    snapshot_equity(portfolio, all_ts[-1] if all_ts else 0)

    trades   = portfolio["closed_trades"]
    total    = len(trades)
    wins     = sum(1 for t in trades if t["won"])
    pnl_pct  = (current_equity(portfolio) - STARTING_CAP) / STARTING_CAP * 100
    sharpe   = compute_sharpe(portfolio["equity_snapshots"])
    win_rate = round(wins / total * 100, 1) if total > 0 else 0.0

    suspicious        = False
    suspicious_reason = ""
    if sharpe > SUSPICIOUS_SHARPE:
        suspicious        = True
        suspicious_reason = f"Sharpe {sharpe:.2f} > {SUSPICIOUS_SHARPE} threshold"
    elif win_rate > SUSPICIOUS_WINRATE and total > 10:
        suspicious        = True
        suspicious_reason = f"Win rate {win_rate}% > {SUSPICIOUS_WINRATE}% threshold"

    return {
        "sharpe":            sharpe,
        "win_rate_pct":      win_rate,
        "total_pnl_pct":     round(pnl_pct, 4),
        "total_trades":      total,
        "wins":              wins,
        "losses":            total - wins,
        "max_drawdown_pct":  round(portfolio["max_drawdown"], 4),
        "final_equity":      round(current_equity(portfolio), 2),
        "suspicious":        suspicious,
        "suspicious_reason": suspicious_reason,
        "candles_processed": len(all_ts),
    }
