#!/usr/bin/env python3
"""
day_retroactive_fill.py - Retroactively simulate Day Trading Sprint 2 of Cycle 2.
Sprint 2: 2026-03-18T09:00:00 UTC (2am PDT) to 2026-03-19T09:00:00 UTC.
Fetches Kraken 5-min OHLCV, replays all 12 bots, writes new sprint directory.
"""
import os, sys, json, yaml, urllib.request, shutil
from datetime import datetime, timezone, timedelta

WORKSPACE  = "/root/.openclaw/workspace"
FLEET_DIR  = os.path.join(WORKSPACE, "fleet")
ACTIVE_DIR = os.path.join(WORKSPACE, "competition", "active")
CYCLE_STATE_PATH = os.path.join(WORKSPACE, "competition", "cycle_state.json")

SPRINT_START = datetime(2026, 3, 18, 9, 0, 0, tzinfo=timezone.utc)
SPRINT_END   = datetime(2026, 3, 19, 9, 0, 0, tzinfo=timezone.utc)
SPRINT_ID    = "comp-20260318-0900"
DURATION_H   = 24.0
STARTING_CAPITAL = 1000.0
FEE_RATE     = 0.001
MAX_HISTORY_HOURS = 5
FLAT_THRESHOLD_PCT = 0.15

BOTS = ["floki","bjorn","lagertha","ragnar","leif","gunnar",
        "harald","freydis","sigurd","astrid","ulf","bjarne"]
PAIRS = ["BTC/USD","ETH/USD","SOL/USD","XRP/USD","DOGE/USD","AVAX/USD","LINK/USD"]

KRAKEN_OHLC_PAIRS = {
    "BTC/USD":  "XBTUSD",
    "ETH/USD":  "ETHUSD",
    "SOL/USD":  "SOLUSD",
    "XRP/USD":  "XRPUSD",
    "DOGE/USD": "XDGUSD",
    "AVAX/USD": "AVAXUSD",
    "LINK/USD": "LINKUSD",
}
HISTORY_KEY = {
    "BTC/USD":  "BTC/USD",
    "ETH/USD":  "ETH/USD",
    "SOL/USD":  "SOL/USD",
    "XRP/USD":  "XRP/USD",
    "DOGE/USD": "XDGUSD",
    "AVAX/USD": "AVAXUSD",
    "LINK/USD": "LINKUSD",
}


def fetch_kraken_ohlc(pair_key, interval=5):
    url = "https://api.kraken.com/0/public/OHLC?pair=" + pair_key + "&interval=" + str(interval)
    with urllib.request.urlopen(url, timeout=20) as r:
        data = json.loads(r.read())
    if data.get("error"):
        raise RuntimeError("Kraken OHLC error for " + pair_key + ": " + str(data["error"]))
    result = data["result"]
    key = next(k for k in result if k != "last")
    return result[key]


def build_ticks(all_candles, warmup_start, sprint_start, sim_end):
    all_ts = set()
    for hkey, candles in all_candles.items():
        for c in candles:
            ts = datetime.fromtimestamp(c[0], tz=timezone.utc)
            if warmup_start <= ts <= sim_end:
                all_ts.add(ts)
    all_ts = sorted(all_ts)

    rolling = {}
    ticks = []

    for sim_ts in all_ts:
        sim_iso = sim_ts.isoformat()
        cutoff  = (sim_ts - timedelta(hours=MAX_HISTORY_HOURS)).isoformat()

        for hkey, candles in all_candles.items():
            ts_int = int(sim_ts.timestamp())
            matching = [c for c in candles if c[0] == ts_int]
            if not matching:
                continue
            c = matching[0]
            close_price = float(c[4])
            vwap_price  = float(c[5]) if c[5] else close_price

            if hkey not in rolling:
                rolling[hkey] = []
            rolling[hkey].append({"ts": sim_iso, "last": close_price, "vwap": vwap_price})
            rolling[hkey] = [t for t in rolling[hkey] if t["ts"] >= cutoff]

        if sim_ts >= sprint_start:
            ticks.append((sim_ts, {k: list(v) for k, v in rolling.items()}))

    return ticks


def _get_ago(history, hkey, minutes, sim_ts):
    if hkey not in history or not history[hkey]:
        return None
    target = (sim_ts - timedelta(minutes=minutes)).isoformat()
    past = [t for t in history[hkey] if t["ts"] <= target]
    return past[-1]["last"] if past else None


def _current(history, hkey):
    if hkey not in history or not history[hkey]:
        return None
    return history[hkey][-1]["last"]


def _vwap(history, hkey):
    if hkey not in history or not history[hkey]:
        return None
    for t in reversed(history[hkey]):
        if "vwap" in t:
            return t["vwap"]
    return None


def _series(history, hkey, n, sim_ts):
    prices = []
    for i in range(n):
        p = _current(history, hkey) if i == 0 else _get_ago(history, hkey, i * 5, sim_ts)
        if p is None:
            return None
        prices.append(p)
    return list(reversed(prices))


def _ema(prices, n):
    k = 2 / (n + 1)
    e = prices[0]
    for p in prices[1:]:
        e = p * k + e * (1 - k)
    return e


def compute_indicator(name, history, hkey, period_minutes, sim_ts):
    cur = _current(history, hkey)
    if cur is None:
        return None

    if name == "price_change_pct":
        past = _get_ago(history, hkey, period_minutes, sim_ts)
        if past is None or past == 0:
            return None
        return (cur - past) / past * 100

    if name == "trend":
        past = _get_ago(history, hkey, period_minutes, sim_ts)
        if past is None or past == 0:
            return None
        chg = (cur - past) / past * 100
        if chg > FLAT_THRESHOLD_PCT:  return "up"
        if chg < -FLAT_THRESHOLD_PCT: return "down"
        return "flat"

    if name == "momentum_accelerating":
        half  = period_minutes // 2
        mid   = _get_ago(history, hkey, half, sim_ts)
        start = _get_ago(history, hkey, period_minutes, sim_ts)
        if any(v is None or v == 0 for v in [cur, mid, start]):
            return None
        return abs((cur - mid) / mid * 100) > abs((mid - start) / start * 100)

    if name == "price_vs_vwap":
        vwap = _vwap(history, hkey)
        if vwap is None or vwap == 0:
            return None
        diff = (cur - vwap) / vwap * 100
        if diff > 0.05:  return "above"
        if diff < -0.05: return "below"
        return "at"

    if name == "rsi":
        n = max(period_minutes // 5, 2)
        prices = _series(history, hkey, n + 1, sim_ts)
        if prices is None:
            return None
        changes = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        gains   = [max(c, 0) for c in changes]
        losses  = [abs(min(c, 0)) for c in changes]
        ag = sum(gains) / len(gains)
        al = sum(losses) / len(losses)
        if al == 0:
            return 100.0
        return round(100 - 100 / (1 + ag / al), 2)

    if name == "price_vs_ema":
        n = max(period_minutes // 5, 2)
        prices = _series(history, hkey, n, sim_ts)
        if prices is None:
            return None
        ema_val = _ema(prices, n)
        diff = (cur - ema_val) / ema_val * 100
        if diff > 0.05:  return "above"
        if diff < -0.05: return "below"
        return "at"

    if name == "bollinger_position":
        n = max(period_minutes // 5, 2)
        prices = _series(history, hkey, n, sim_ts)
        if prices is None:
            return None
        mean = sum(prices) / len(prices)
        std  = (sum((p - mean) ** 2 for p in prices) / len(prices)) ** 0.5
        if std == 0:
            return "inside"
        if cur > mean + 2 * std: return "above_upper"
        if cur < mean - 2 * std: return "below_lower"
        return "inside"

    if name == "macd_signal":
        slow_n   = max(period_minutes // 5, 4)
        fast_n   = max(slow_n * 12 // 26, 2)
        signal_n = max(slow_n * 9  // 26, 2)
        prices   = _series(history, hkey, slow_n + signal_n - 1, sim_ts)
        if prices is None:
            return None
        macd_vals = []
        for i in range(signal_n):
            w = prices[i:i + slow_n]
            macd_vals.append(_ema(w[slow_n - fast_n:], fast_n) - _ema(w, slow_n))
        hist = macd_vals[-1] - _ema(macd_vals, signal_n)
        if hist > 0:  return "bullish"
        if hist < 0:  return "bearish"
        return "neutral"

    return None


def eval_condition(cond, history, hkey, sim_ts):
    actual = compute_indicator(cond["indicator"], history, hkey,
                               cond.get("period_minutes", 5), sim_ts)
    if actual is None:
        return None
    expected = cond["value"]
    op = cond["operator"]
    if isinstance(expected, str):
        if expected.lower() == "true":  expected = True
        elif expected.lower() == "false": expected = False
    if op == "lt":  return actual < expected
    if op == "gt":  return actual > expected
    if op == "lte": return actual <= expected
    if op == "gte": return actual >= expected
    if op == "eq":  return actual == expected
    if op == "in":  return actual in expected
    return None


def eval_entry(conditions, history, hkey, sim_ts):
    results = [eval_condition(c, history, hkey, sim_ts) for c in conditions]
    if None in results:
        return None
    return all(results)


def make_portfolio(bot):
    return {
        "bot": bot,
        "competition_id": SPRINT_ID,
        "duration_hours": DURATION_H,
        "started_at": SPRINT_START.isoformat(),
        "pairs": PAIRS,
        "starting_capital": STARTING_CAPITAL,
        "fee_rate": FEE_RATE,
        "cash": STARTING_CAPITAL,
        "positions": [],
        "closed_trades": [],
        "stats": {
            "total_trades": 0, "wins": 0, "losses": 0,
            "win_rate": 0.0, "total_pnl_usd": 0.0, "total_pnl_pct": 0.0,
            "total_fees": 0.0, "max_drawdown_pct": 0.0,
            "largest_win_pct": 0.0, "largest_loss_pct": 0.0,
            "current_equity": STARTING_CAPITAL, "peak_equity": STARTING_CAPITAL,
        },
    }


def recalc(portfolio):
    return portfolio["cash"] + sum(p["cost_basis"] for p in portfolio["positions"])


def upd_draw(portfolio):
    eq   = recalc(portfolio)
    peak = portfolio["stats"]["peak_equity"]
    portfolio["stats"]["current_equity"] = round(eq, 2)
    if eq > peak:
        portfolio["stats"]["peak_equity"] = round(eq, 2)
    else:
        dd = (peak - eq) / peak * 100
        if dd > portfolio["stats"]["max_drawdown_pct"]:
            portfolio["stats"]["max_drawdown_pct"] = round(dd, 4)


def trade_open(p, pair, direction, price, size_pct, sl, tp, sim_ts):
    cash    = p["cash"]
    deploy  = cash * (size_pct / 100.0)
    fee     = deploy * FEE_RATE
    cost    = deploy - fee
    qty     = cost / price
    if deploy > cash:
        return False
    p["cash"] = round(cash - deploy, 8)
    p["positions"].append({
        "pair": pair, "direction": direction,
        "entry_price": price, "quantity": round(qty, 8),
        "cost_basis": round(cost, 2), "entry_fee": round(fee, 2),
        "stop_loss": round(sl, 2), "take_profit": round(tp, 2),
        "opened_at": sim_ts.isoformat(),
    })
    p["stats"]["total_fees"] = round(p["stats"]["total_fees"] + fee, 2)
    upd_draw(p)
    return True


def trade_close(p, pair, price, reason, sim_ts):
    pos_list = [x for x in p["positions"] if x["pair"] == pair]
    if not pos_list:
        return
    pos  = pos_list[0]
    cost = pos["cost_basis"]
    qty  = pos["quantity"]
    gp   = (price - pos["entry_price"]) * qty if pos["direction"] == "long" \
           else (pos["entry_price"] - price) * qty
    fee  = cost * FEE_RATE
    net  = gp - fee
    pct  = round(net / cost * 100, 4)
    won  = net > 0

    p["cash"] = round(p["cash"] + cost + net, 8)
    p["positions"] = [x for x in p["positions"] if x["pair"] != pair]
    p["closed_trades"].append({
        "pair": pair, "direction": pos["direction"],
        "entry_price": pos["entry_price"], "exit_price": price,
        "quantity": qty, "cost_basis": cost,
        "gross_pnl": round(gp, 2), "close_fee": round(fee, 2),
        "net_pnl": round(net, 2), "pnl_pct": pct,
        "reason": reason, "opened_at": pos["opened_at"],
        "closed_at": sim_ts.isoformat(),
    })

    s = p["stats"]
    s["total_trades"] += 1
    s["wins"]   += 1 if won else 0
    s["losses"] += 0 if won else 1
    s["win_rate"] = round(s["wins"] / s["total_trades"] * 100, 1)
    s["total_pnl_usd"] = round(s["total_pnl_usd"] + net, 2)
    s["total_pnl_pct"] = round(s["total_pnl_usd"] / STARTING_CAPITAL * 100, 4)
    s["total_fees"] = round(s["total_fees"] + fee, 2)
    if pct > s["largest_win_pct"]:   s["largest_win_pct"] = pct
    if pct < s["largest_loss_pct"]:  s["largest_loss_pct"] = pct
    upd_draw(p)


def sim_tick(portfolios, strategies, risk_state, history, sim_ts):
    sim_iso = sim_ts.isoformat()
    for bot, portfolio in portfolios.items():
        strategy = strategies.get(bot)
        if not strategy:
            continue

        bot_risk = risk_state.get(bot, {})
        if bot_risk.get("stopped"):
            continue
        paused = bot_risk.get("paused_until")
        if paused and sim_iso < paused:
            continue

        risk_rules = strategy.get("risk", {})
        total_pct  = portfolio["stats"]["total_pnl_pct"]
        stop_pct   = risk_rules.get("stop_if_down_pct", 10)
        pause_pct  = risk_rules.get("pause_if_down_pct", 5)
        pause_min  = risk_rules.get("pause_minutes", 60)

        if total_pct <= -stop_pct:
            risk_state[bot] = {"stopped": True, "paused_until": None}
            continue
        if total_pct <= -pause_pct:
            risk_state[bot] = {"stopped": False,
                               "paused_until": (sim_ts + timedelta(minutes=pause_min)).isoformat()}
            continue

        exit_rules  = strategy.get("exit", {})
        tp_pct      = exit_rules.get("take_profit_pct", 0.5) / 100
        sl_pct      = exit_rules.get("stop_loss_pct",   0.3) / 100
        timeout_min = exit_rules.get("timeout_minutes",  30)

        for pos in list(portfolio["positions"]):
            pair    = pos["pair"]
            hkey    = HISTORY_KEY.get(pair, pair)
            cur     = _current(history, hkey)
            if cur is None:
                continue
            entry   = pos["entry_price"]
            age_min = (sim_ts - datetime.fromisoformat(pos["opened_at"])).total_seconds() / 60
            pnl_pos = (cur - entry) / entry if pos["direction"] == "long" else (entry - cur) / entry

            reason = None
            if pnl_pos >= tp_pct:       reason = "target"
            elif pnl_pos <= -sl_pct:    reason = "stop"
            elif age_min >= timeout_min: reason = "timeout"

            if reason:
                trade_close(portfolio, pair, cur, reason, sim_ts)

        pos_config = strategy.get("position", {})
        max_open   = pos_config.get("max_open", 1)
        size_pct   = pos_config.get("size_pct", 20)
        tp_e       = exit_rules.get("take_profit_pct", 0.5) / 100
        sl_e       = exit_rules.get("stop_loss_pct",   0.3) / 100

        open_pairs = {p["pair"] for p in portfolio["positions"]}
        if len(open_pairs) >= max_open:
            continue

        entry_rules = strategy.get("entry", {})
        for pair in strategy.get("pairs", []):
            if len(open_pairs) >= max_open:
                break
            if pair in open_pairs:
                continue
            hkey = HISTORY_KEY.get(pair, pair)
            cur  = _current(history, hkey)
            if cur is None:
                continue

            for direction in ["long", "short"]:
                conditions = entry_rules.get(direction, {}).get("conditions", [])
                if not conditions:
                    continue
                signal = eval_entry(conditions, history, hkey, sim_ts)
                if not signal:
                    continue

                sl = cur * (1 - sl_e) if direction == "long" else cur * (1 + sl_e)
                tp = cur * (1 + tp_e) if direction == "long" else cur * (1 - tp_e)
                ok = trade_open(portfolio, pair, direction, cur, size_pct, sl, tp, sim_ts)
                if ok:
                    open_pairs.add(pair)
                    break


def load_strategy(bot):
    path = os.path.join(FLEET_DIR, bot, "strategy.yaml")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    now     = datetime.now(timezone.utc)
    sim_end = min(now, SPRINT_END)
    warmup  = SPRINT_START - timedelta(hours=6)

    print("Sprint 2 retroactive fill")
    print("  Sprint start: " + SPRINT_START.isoformat())
    print("  Sim end:      " + sim_end.isoformat())

    print("\nFetching Kraken OHLCV...")
    all_candles = {}
    for pair in PAIRS:
        kraken_key = KRAKEN_OHLC_PAIRS[pair]
        hkey       = HISTORY_KEY[pair]
        print("  " + pair + " (" + kraken_key + ")...", end=" ", flush=True)
        try:
            candles = fetch_kraken_ohlc(kraken_key)
            all_candles[hkey] = candles
            first = datetime.fromtimestamp(candles[0][0], tz=timezone.utc).strftime("%m-%d %H:%M")
            last  = datetime.fromtimestamp(candles[-1][0], tz=timezone.utc).strftime("%m-%d %H:%M")
            print(str(len(candles)) + " candles (" + first + " to " + last + ")")
        except Exception as e:
            print("FAILED: " + str(e))
            sys.exit(1)

    print("\nBuilding tick sequence...")
    ticks = build_ticks(all_candles, warmup, SPRINT_START, sim_end)
    print("  " + str(len(ticks)) + " ticks in sprint period")
    if not ticks:
        print("ERROR: no ticks in sprint period")
        sys.exit(1)

    strategies = {}
    for bot in BOTS:
        s = load_strategy(bot)
        if s:
            strategies[bot] = s
        else:
            print("  WARNING: no strategy for " + bot)

    portfolios = {bot: make_portfolio(bot) for bot in BOTS}
    risk_state = {}

    print("\nRunning simulation (" + str(len(ticks)) + " ticks x " + str(len(BOTS)) + " bots)...")
    for i, (sim_ts, history) in enumerate(ticks):
        sim_tick(portfolios, strategies, risk_state, history, sim_ts)
        if i % 60 == 0:
            print("  [" + str(i+1) + "/" + str(len(ticks)) + "] " + sim_ts.strftime("%m-%d %H:%M UTC"))

    print("  Done. Final tick: " + ticks[-1][0].strftime("%m-%d %H:%M UTC"))

    # Archive and remove old sprint
    old_sprint = os.path.join(ACTIVE_DIR, "comp-20260318-2030")
    if os.path.exists(old_sprint):
        results_dir = os.path.join(WORKSPACE, "competition", "results", "comp-20260318-2030")
        if not os.path.exists(results_dir):
            shutil.copytree(old_sprint, results_dir)
        shutil.rmtree(old_sprint)
        print("\nArchived old sprint comp-20260318-2030")

    # Create new sprint directory
    comp_dir = os.path.join(ACTIVE_DIR, SPRINT_ID)
    if os.path.exists(comp_dir):
        shutil.rmtree(comp_dir)
    os.makedirs(comp_dir, exist_ok=True)

    meta = {
        "comp_id":          SPRINT_ID,
        "duration_hours":   DURATION_H,
        "started_at":       SPRINT_START.isoformat(),
        "pairs":            PAIRS,
        "bots":             BOTS,
        "starting_capital": STARTING_CAPITAL,
        "fee_rate":         FEE_RATE,
        "status":           "active",
        "cycle":            2,
        "sprint_in_cycle":  2,
    }
    with open(os.path.join(comp_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    for bot, portfolio in portfolios.items():
        with open(os.path.join(comp_dir, "portfolio-" + bot + ".json"), "w") as f:
            json.dump(portfolio, f, indent=2)

    with open(os.path.join(comp_dir, "price_history.json"), "w") as f:
        json.dump(ticks[-1][1], f)

    with open(os.path.join(comp_dir, "risk_state.json"), "w") as f:
        json.dump(risk_state, f, indent=2)

    with open(os.path.join(comp_dir, "tick.log"), "w") as f:
        f.write("[retroactive] Sprint 2 filled " + SPRINT_START.isoformat() + " to " + ticks[-1][0].isoformat() + "\n")
        f.write("[retroactive] " + str(len(ticks)) + " ticks simulated for " + str(len(BOTS)) + " bots\n")

    # Update cycle_state
    cycle_state = {
        "cycle":            2,
        "sprint_in_cycle":  2,
        "sprints_per_cycle": 7,
        "status":           "active",
        "cycle_started_at": "2026-03-15T17:26:45.108764+00:00",
        "sprints":          ["comp-20260315-1726", "comp-20260317-0900", SPRINT_ID],
    }
    with open(CYCLE_STATE_PATH, "w") as f:
        json.dump(cycle_state, f, indent=2)

    print("\nResults summary:")
    results = []
    for bot, p in portfolios.items():
        results.append((bot, p["stats"]["current_equity"],
                        p["stats"]["total_pnl_usd"],
                        p["stats"]["total_trades"],
                        p["stats"]["wins"]))
    results.sort(key=lambda x: x[2], reverse=True)
    for rank, (bot, equity, pnl, trades, wins) in enumerate(results, 1):
        wr = str(wins) + "/" + str(trades) if trades else "0/0"
        print("  #" + str(rank).rjust(2) + " " + bot.ljust(10) +
              " equity=$" + "{:,.2f}".format(equity) +
              "  pnl=" + "{:+.2f}".format(pnl) +
              "  trades=" + wr)

    print("\ncycle_state.json updated: Cycle 2, Sprint 2 active")
    print("Sprint directory: " + comp_dir)
    print("Done.")


if __name__ == "__main__":
    main()
