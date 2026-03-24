#!/usr/bin/env python3
"""
sprint_backfill.py -- Retroactively replay 5-min ticks for a missed day sprint start.

When the day league misses its 09:00 UTC reset, run this script to replay
all historical ticks from the intended start time through now, executing
bot logic exactly as it would have run in real time.

Usage:
  python3 sprint_backfill.py
  python3 sprint_backfill.py --dry-run
  python3 sprint_backfill.py --start 2026-03-23T09:00:00
"""
import json, os, sys, yaml, time, math, fcntl, tempfile, urllib.request
from datetime import datetime, timezone, timedelta

WORKSPACE       = "/root/.openclaw/workspace"
FLEET_DIR       = os.path.join(WORKSPACE, "fleet")
COMP_ACTIVE_DIR = os.path.join(WORKSPACE, "competition", "active")
LOCK_FILE       = "/tmp/competition_tick.lock"
FEE_RATE        = 0.001
FLAT_THRESHOLD  = 0.15
WARMUP_HOURS    = 6
HISTORY_WINDOW  = 400

KRAKEN_OHLC_MAP = {
    "BTC/USD": "XBTUSD",  "ETH/USD": "ETHUSD",   "SOL/USD": "SOLUSD",
    "XRP/USD": "XRPUSD",  "DOGE/USD": "XDGUSD",  "AVAX/USD": "AVAXUSD",
    "LINK/USD": "LINKUSD", "ADA/USD": "ADAUSD",   "DOT/USD": "DOTUSD",
}

def fetch_ohlcv(pair, since_ts):
    kraken_pair = KRAKEN_OHLC_MAP.get(pair, pair.replace("/", ""))
    url = ("https://api.kraken.com/0/public/OHLC"
           "?pair=" + kraken_pair + "&interval=5&since=" + str(since_ts))
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.loads(resp.read())
    if data.get("error"):
        raise RuntimeError("Kraken error for " + pair + ": " + str(data["error"]))
    result = data["result"]
    key = next(k for k in result if k != "last")
    return [(int(c[0]), float(c[4]), float(c[5])) for c in result[key]]

def _price_n_ago(h, minutes, sim_now):
    target = (sim_now - timedelta(minutes=minutes)).isoformat()
    past = [t for t in h if t["ts"] <= target]
    return past[-1]["last"] if past else None

def _price_series(h, n, interval_min, sim_now):
    prices = []
    for i in range(n):
        p = h[-1]["last"] if i == 0 else _price_n_ago(h, i * interval_min, sim_now)
        if p is None:
            return None
        prices.append(p)
    return list(reversed(prices))

def _ema(prices, n):
    k = 2.0 / (n + 1)
    v = prices[0]
    for p in prices[1:]:
        v = p * k + v * (1 - k)
    return v

def compute_indicator(name, history, pair, period_minutes, sim_now):
    h = history.get(pair, [])
    if not h:
        return None
    current = h[-1]["last"]
    if name == "price_change_pct":
        past = _price_n_ago(h, period_minutes, sim_now)
        if not past or past == 0: return None
        return (current - past) / past * 100
    if name == "trend":
        past = _price_n_ago(h, period_minutes, sim_now)
        if not past or past == 0: return None
        ch = (current - past) / past * 100
        return "up" if ch > FLAT_THRESHOLD else ("down" if ch < -FLAT_THRESHOLD else "flat")
    if name == "momentum_accelerating":
        half = period_minutes // 2
        mid   = _price_n_ago(h, half, sim_now)
        start = _price_n_ago(h, period_minutes, sim_now)
        if any(v is None or v == 0 for v in [mid, start]): return None
        return abs((current - mid) / mid * 100) > abs((mid - start) / start * 100)
    if name == "price_vs_vwap":
        vwap = next((t["vwap"] for t in reversed(h) if "vwap" in t), None)
        if not vwap or vwap == 0: return None
        d = (current - vwap) / vwap * 100
        return "above" if d > 0.05 else ("below" if d < -0.05 else "at")
    if name == "rsi":
        n = max(period_minutes // 5, 2)
        prices = _price_series(h, n + 1, 5, sim_now)
        if prices is None: return None
        ch = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        ag = sum(max(c, 0) for c in ch) / len(ch)
        al = sum(abs(min(c, 0)) for c in ch) / len(ch)
        if al == 0: return 100.0
        return round(100 - 100 / (1 + ag / al), 2)
    if name == "price_vs_ema":
        n = max(period_minutes // 5, 2)
        prices = _price_series(h, n, 5, sim_now)
        if prices is None: return None
        ema = _ema(prices, n)
        d = (current - ema) / ema * 100
        return "above" if d > 0.05 else ("below" if d < -0.05 else "at")
    if name == "bollinger_position":
        n = max(period_minutes // 5, 2)
        prices = _price_series(h, n, 5, sim_now)
        if prices is None: return None
        mean = sum(prices) / len(prices)
        std  = math.sqrt(sum((p - mean) ** 2 for p in prices) / len(prices))
        if std == 0: return "inside"
        return ("above_upper" if current > mean + 2 * std
                else "below_lower" if current < mean - 2 * std else "inside")
    if name == "macd_signal":
        slow_n = max(period_minutes // 5, 4)
        fast_n = max(slow_n * 12 // 26, 2)
        sig_n  = max(slow_n * 9  // 26, 2)
        prices = _price_series(h, slow_n + sig_n - 1, 5, sim_now)
        if prices is None: return None
        mv = []
        for i in range(sig_n):
            w = prices[i:i + slow_n]
            mv.append(_ema(w[slow_n - fast_n:], fast_n) - _ema(w, slow_n))
        h_val = mv[-1] - _ema(mv, sig_n)
        return "bullish" if h_val > 0 else ("bearish" if h_val < 0 else "neutral")
    return None

def evaluate_entry(conditions, history, pair, sim_now):
    for cond in conditions:
        val = compute_indicator(cond["indicator"], history, pair,
                                cond.get("period_minutes", 5), sim_now)
        if val is None:
            return None
        exp = cond["value"]
        op  = cond["operator"]
        if isinstance(exp, str):
            if exp.lower() == "true":    exp = True
            elif exp.lower() == "false": exp = False
        if op == "eq":    ok = val == exp
        elif op == "in":  ok = val in exp
        elif op == "lt":  ok = val < exp
        elif op == "gt":  ok = val > exp
        elif op == "lte": ok = val <= exp
        elif op == "gte": ok = val >= exp
        else: return None
        if not ok: return False
    return True

def recalc_equity(p):
    return p["cash"] + sum(pos["cost_basis"] for pos in p["positions"])

def _update_dd(p):
    eq = p["stats"]["current_equity"]
    pk = p["stats"]["peak_equity"]
    if eq > pk:
        p["stats"]["peak_equity"] = eq
    elif pk > 0:
        dd = (pk - eq) / pk * 100
        if dd > p["stats"]["max_drawdown_pct"]:
            p["stats"]["max_drawdown_pct"] = round(dd, 4)

def trade_open(portfolio, pair, direction, price, size_pct, sl, tp, sim_now):
    deploy = portfolio["cash"] * (size_pct / 100.0)
    if deploy < 1.0 or deploy > portfolio["cash"]: return False
    fee  = deploy * FEE_RATE
    cost = deploy - fee
    qty  = cost / price
    portfolio["cash"] = round(portfolio["cash"] - deploy, 8)
    portfolio["positions"].append({
        "pair": pair, "direction": direction,
        "entry_price": price, "quantity": round(qty, 8),
        "cost_basis": round(cost, 2), "entry_fee": round(fee, 2),
        "stop_loss": round(sl, 2), "take_profit": round(tp, 2),
        "opened_at": sim_now.isoformat(),
    })
    portfolio["stats"]["total_fees"]      = round(portfolio["stats"]["total_fees"] + fee, 2)
    portfolio["stats"]["current_equity"]  = round(recalc_equity(portfolio), 2)
    _update_dd(portfolio)
    return True

def trade_close(portfolio, pair, price, reason, sim_now):
    pos_list = [p for p in portfolio["positions"] if p["pair"] == pair]
    if not pos_list: return None
    pos   = pos_list[0]
    entry = pos["entry_price"]
    qty   = pos["quantity"]
    cost  = pos["cost_basis"]
    gross = (price - entry) * qty if pos["direction"] == "long" else (entry - price) * qty
    fee   = cost * FEE_RATE
    net   = gross - fee
    pnl_pct = round(net / cost * 100, 4)
    portfolio["cash"]      = round(portfolio["cash"] + cost + net, 8)
    portfolio["positions"] = [p for p in portfolio["positions"] if p["pair"] != pair]
    portfolio["closed_trades"].append({
        "pair": pair, "direction": pos["direction"],
        "entry_price": entry, "exit_price": price,
        "quantity": qty, "cost_basis": cost,
        "gross_pnl": round(gross, 2), "close_fee": round(fee, 2),
        "net_pnl": round(net, 2), "pnl_pct": pnl_pct,
        "reason": reason, "opened_at": pos["opened_at"],
        "closed_at": sim_now.isoformat(),
    })
    s = portfolio["stats"]
    s["total_trades"] += 1
    won = net > 0
    s["wins"]   += 1 if won else 0
    s["losses"] += 0 if won else 1
    s["win_rate"]       = round(s["wins"] / s["total_trades"] * 100, 1)
    s["total_pnl_usd"]  = round(s["total_pnl_usd"] + net, 2)
    s["total_pnl_pct"]  = round(s["total_pnl_usd"] / portfolio["starting_capital"] * 100, 4)
    s["total_fees"]     = round(s["total_fees"] + fee, 2)
    s["current_equity"] = round(recalc_equity(portfolio), 2)
    _update_dd(portfolio)
    if pnl_pct > s["largest_win_pct"]:  s["largest_win_pct"]  = pnl_pct
    if pnl_pct < s["largest_loss_pct"]: s["largest_loss_pct"] = pnl_pct
    return pnl_pct

def check_risk(portfolio, strategy, risk_state, sim_now):
    bot = portfolio["bot"]
    st  = risk_state.get(bot, {})
    if st.get("stopped"): return "stopped"
    pu = st.get("paused_until")
    if pu and sim_now.isoformat() < pu: return "paused"
    rules     = strategy.get("risk", {})
    pnl_pct   = portfolio["stats"]["total_pnl_pct"]
    stop_pct  = rules.get("stop_if_down_pct", 10)
    pause_pct = rules.get("pause_if_down_pct", 5)
    pause_min = rules.get("pause_minutes", 60)
    if pnl_pct <= -stop_pct:
        risk_state[bot] = {"stopped": True, "paused_until": None}
        return "stopped"
    if pnl_pct <= -pause_pct:
        risk_state[bot] = {"stopped": False,
                           "paused_until": (sim_now + timedelta(minutes=pause_min)).isoformat()}
        return "paused"
    return "ok"

def main():
    dry_run = "--dry-run" in sys.argv
    sprint_start = datetime(2026, 3, 23, 9, 0, 0, tzinfo=timezone.utc)
    for i, arg in enumerate(sys.argv):
        if arg == "--start" and i + 1 < len(sys.argv):
            ts_str = sys.argv[i + 1]
            sprint_start = datetime.fromisoformat(ts_str).replace(tzinfo=timezone.utc)
    lock_fh = open(LOCK_FILE, "w")
    fcntl.flock(lock_fh, fcntl.LOCK_EX)
    try:
        _run(dry_run, sprint_start)
    finally:
        fcntl.flock(lock_fh, fcntl.LOCK_UN)
        lock_fh.close()

def _run(dry_run, sprint_start):
    entries = sorted([d for d in os.listdir(COMP_ACTIVE_DIR)
                      if os.path.isdir(os.path.join(COMP_ACTIVE_DIR, d)) and not d.startswith(".")])
    if not entries:
        print("No active sprint found."); return
    comp_id  = entries[-1]
    comp_dir = os.path.join(COMP_ACTIVE_DIR, comp_id)
    with open(os.path.join(comp_dir, "meta.json")) as f:
        meta = json.load(f)
    pairs   = meta["pairs"]
    bots    = meta["bots"]
    now_utc = datetime.now(timezone.utc)
    print("[backfill] Sprint:       " + comp_id)
    print("[backfill] Sprint start: " + sprint_start.isoformat() + " (retroactive)")
    print("[backfill] Now:          " + now_utc.strftime("%Y-%m-%dT%H:%MZ"))
    print("[backfill] Pairs:        " + ", ".join(pairs))
    print("[backfill] Bots:         " + ", ".join(bots))
    print("[backfill] Dry run:      " + str(dry_run))
    fetch_from = sprint_start - timedelta(hours=WARMUP_HOURS)
    since_ts   = int(fetch_from.timestamp())
    print("\n[backfill] Fetching 5-min OHLCV from " + fetch_from.strftime("%Y-%m-%d %H:%MZ") + " ...")
    ohlcv = {}
    for pair in pairs:
        try:
            candles = fetch_ohlcv(pair, since_ts)
            ohlcv[pair] = candles
            print("  " + pair.ljust(10) + ": " + str(len(candles)) + " candles")
            time.sleep(0.4)
        except Exception as e:
            print("  " + pair.ljust(10) + ": FETCH ERROR -- " + str(e))
            ohlcv[pair] = []
    all_ts = sorted(set(ts for clist in ohlcv.values() for ts, _, _ in clist))
    by_ts  = {pair: {ts: (cl, vw) for ts, cl, vw in ohlcv[pair]} for pair in pairs}
    portfolios = {}
    for bot in bots:
        with open(os.path.join(comp_dir, "portfolio-" + bot + ".json")) as f:
            portfolios[bot] = json.load(f)
    strategies = {}
    for bot in bots:
        p = os.path.join(FLEET_DIR, bot, "strategy.yaml")
        if os.path.exists(p):
            with open(p) as f:
                strategies[bot] = yaml.safe_load(f)
    history    = {pair: [] for pair in pairs}
    risk_state = {}
    log_path   = os.path.join(comp_dir, "tick.log")
    def tlog(msg):
        print(msg)
        if not dry_run:
            with open(log_path, "a") as f:
                f.write(msg + "\n")
    sep = "=" * 60
    tlog("\n" + sep)
    tlog("[backfill] RETROACTIVE REPLAY -- " + sprint_start.strftime("%Y-%m-%d %H:%MZ") + " to " + now_utc.strftime("%H:%MZ"))
    tlog(sep)
    sprint_ticks = 0
    total_trades = 0
    for unix_ts in all_ts:
        sim_now = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
        prices_tick = {}
        for pair in pairs:
            entry = by_ts[pair].get(unix_ts)
            if entry:
                cl, vw = entry
                tick = {"ts": sim_now.isoformat(), "last": cl}
                if vw and vw != 0:
                    tick["vwap"] = vw
                history[pair].append(tick)
                if len(history[pair]) > HISTORY_WINDOW:
                    history[pair] = history[pair][-HISTORY_WINDOW:]
                prices_tick[pair] = {"last": cl, "vwap": vw}
        if sim_now < sprint_start:
            continue
        sprint_ticks += 1
        ts_str = sim_now.strftime("%Y-%m-%dT%H:%MZ")
        for bot in bots:
            strategy  = strategies.get(bot)
            portfolio = portfolios.get(bot)
            if not strategy or not portfolio: continue
            status = check_risk(portfolio, strategy, risk_state, sim_now)
            if status in ("paused", "stopped"): continue
            exit_rules  = strategy.get("exit", {})
            tp_pct      = exit_rules.get("take_profit_pct", 0.5) / 100
            sl_pct_val  = exit_rules.get("stop_loss_pct", 0.3) / 100
            timeout_min = exit_rules.get("timeout_minutes", 30)
            for pos in list(portfolio.get("positions", [])):
                pair    = pos["pair"]
                current = prices_tick.get(pair, {}).get("last")
                if current is None: continue
                entry   = pos["entry_price"]
                dirn    = pos["direction"]
                opened  = datetime.fromisoformat(pos["opened_at"])
                age_min = (sim_now - opened).total_seconds() / 60
                pnl_frac = ((current - entry) / entry if dirn == "long"
                            else (entry - current) / entry)
                reason = None
                if pnl_frac >= tp_pct:        reason = "target"
                elif pnl_frac <= -sl_pct_val: reason = "stop"
                elif age_min >= timeout_min:  reason = "timeout"
                if reason:
                    pct = trade_close(portfolio, pair, current, reason, sim_now)
                    if pct is not None:
                        total_trades += 1
                        tlog("[" + ts_str + "]   [" + bot + "] CLOSE " + dirn.upper() +
                             " " + pair + " @ $" + str(round(current, 2)) +
                             " | " + reason + " | pnl=" + str(pct) + "%")
            pos_cfg    = strategy.get("position", {})
            max_open   = pos_cfg.get("max_open", 1)
            size_pct   = pos_cfg.get("size_pct", 20)
            open_pairs = {p["pair"] for p in portfolio.get("positions", [])}
            if len(open_pairs) >= max_open: continue
            entry_rules = strategy.get("entry", {})
            for pair in strategy.get("pairs", []):
                if pair in open_pairs or len(open_pairs) >= max_open: break
                current = prices_tick.get(pair, {}).get("last")
                if current is None: continue
                for dirn in ["long", "short"]:
                    conds = entry_rules.get(dirn, {}).get("conditions", [])
                    if not conds: continue
                    sig = evaluate_entry(conds, history, pair, sim_now)
                    if not sig: continue
                    sl_p = current * (1 - sl_pct_val) if dirn == "long" else current * (1 + sl_pct_val)
                    tp_p = current * (1 + tp_pct)     if dirn == "long" else current * (1 - tp_pct)
                    if not dry_run:
                        ok = trade_open(portfolio, pair, dirn, current, size_pct, sl_p, tp_p, sim_now)
                        if ok:
                            total_trades += 1
                            open_pairs.add(pair)
                            tlog("[" + ts_str + "]   [" + bot + "] OPEN " + dirn.upper() +
                                 " " + pair + " @ $" + str(round(current, 2)))
                            break
    tlog("\n[backfill] Replay complete -- " + str(sprint_ticks) + " ticks, " + str(total_trades) + " trades")
    if dry_run:
        print("\n[backfill] DRY RUN -- no files written.")
        return
    for bot in bots:
        path = os.path.join(comp_dir, "portfolio-" + bot + ".json")
        with tempfile.NamedTemporaryFile("w", dir=comp_dir, delete=False, suffix=".tmp") as tf:
            json.dump(portfolios[bot], tf, indent=2)
            tmp = tf.name
        os.replace(tmp, path)
    meta["started_at"] = sprint_start.isoformat()
    with tempfile.NamedTemporaryFile("w", dir=comp_dir, delete=False, suffix=".tmp") as tf:
        json.dump(meta, tf, indent=2)
        tmp = tf.name
    os.replace(tmp, os.path.join(comp_dir, "meta.json"))
    cutoff    = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
    live_hist = {pair: [t for t in history[pair] if t["ts"] >= cutoff] for pair in pairs}
    with open(os.path.join(comp_dir, "price_history.json"), "w") as f:
        json.dump(live_hist, f)
    with open(os.path.join(comp_dir, "risk_state.json"), "w") as f:
        json.dump(risk_state, f, indent=2)
    tlog("[backfill] meta.json updated: started_at -> " + sprint_start.isoformat())
    tlog("[backfill] Sprint " + comp_id + " now officially starts " + sprint_start.strftime("%Y-%m-%d %H:%MZ") + " (2am PST)")

if __name__ == "__main__":
    main()
