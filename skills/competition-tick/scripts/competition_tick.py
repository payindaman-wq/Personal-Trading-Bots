#!/usr/bin/env python3
"""
competition_tick.py - Core rule engine for the bot competition framework.

Run every 5 minutes via cron. Finds the active competition (if any),
fetches prices, evaluates each bot's strategy rules, and executes trades.

Usage: python3 competition_tick.py [--dry-run]
"""
import sys
import os
import json
import subprocess
import yaml
import urllib.request
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from price_store import append_prices, get_current_price
from indicators import evaluate_entry

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
FLEET_DIR = os.path.join(WORKSPACE, "fleet")
COMP_ACTIVE_DIR = os.path.join(WORKSPACE, "competition", "active")
SKILLS_DIR = os.environ.get("SKILLS_DIR", "/root/.openclaw/skills")
TRADE_EXECUTE = os.path.join(SKILLS_DIR, "trade-execute", "scripts", "trade_execute.py")

KRAKEN_PAIR_MAP = {
    "BTC/USD": "XBTUSD", "ETH/USD": "ETHUSD",
    "SOL/USD": "SOLUSD", "XRP/USD": "XRPUSD",
    "DOGE/USD": "DOGEUSD", "AVAX/USD": "AVAXUSD",
    "LINK/USD": "LINKUSD", "UNI/USD": "UNIUSD",
    "AAVE/USD": "AAVEUSD", "NEAR/USD": "NEARUSD",
    "APT/USD": "APTUSD", "SUI/USD": "SUIUSD",
    "ARB/USD": "ARBUSD", "OP/USD": "OPUSD",
    "WIF/USD": "WIFUSD", "PEPE/USD": "PEPEUSD",
}
KRAKEN_KEY_MAP = {
    "XXBTZUSD": "BTC/USD", "XETHZUSD": "ETH/USD",
    "SOLUSD": "SOL/USD", "XXRPZUSD": "XRP/USD",
    "XDGUSD": "DOGE/USD", "AVAXUSD": "AVAX/USD",
    "LINKUSD": "LINK/USD", "UNIUSD": "UNI/USD",
    "AAVEUSD": "AAVE/USD", "NEARUSD": "NEAR/USD",
    "APTUSD": "APT/USD", "SUIUSD": "SUI/USD",
    "ARBUSD": "ARB/USD", "OPUSD": "OP/USD",
    "WIFUSD": "WIF/USD", "PEPEUSD": "PEPE/USD",
}


def log(msg, comp_dir=None):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line)
    if comp_dir:
        with open(os.path.join(comp_dir, "tick.log"), "a") as f:
            f.write(line + "\n")


def find_active_competition():
    if not os.path.exists(COMP_ACTIVE_DIR):
        return None, None, None
    entries = [
        d for d in os.listdir(COMP_ACTIVE_DIR)
        if os.path.isdir(os.path.join(COMP_ACTIVE_DIR, d))
    ]
    if not entries:
        return None, None, None
    comp_id = sorted(entries)[-1]
    comp_dir = os.path.join(COMP_ACTIVE_DIR, comp_id)
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.exists(meta_path):
        return None, None, None
    with open(meta_path) as f:
        meta = json.load(f)
    return comp_id, meta, comp_dir


def fetch_kraken_prices(pairs):
    kraken_pairs = [KRAKEN_PAIR_MAP.get(p, p.replace("/", "")) for p in pairs]
    url = f"https://api.kraken.com/0/public/Ticker?pair={','.join(kraken_pairs)}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())
    if data.get("error"):
        raise RuntimeError(f"Kraken API error: {data['error']}")
    prices = {}
    for kraken_key, info in data["result"].items():
        label = KRAKEN_KEY_MAP.get(kraken_key, kraken_key)
        prices[label] = {
            "last": float(info["c"][0]),
            "bid": float(info["b"][0]),
            "ask": float(info["a"][0]),
            "vwap": float(info["p"][0]) if "p" in info else None,
        }
    return prices


def load_strategy(bot_name):
    path = os.path.join(FLEET_DIR, bot_name, "strategy.yaml")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def load_portfolio(comp_dir, bot_name):
    path = os.path.join(comp_dir, f"portfolio-{bot_name}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def load_risk_state(comp_dir):
    path = os.path.join(comp_dir, "risk_state.json")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def save_risk_state(comp_dir, state):
    path = os.path.join(comp_dir, "risk_state.json")
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def run_trade(action, portfolio_path, pair=None, direction=None, price=None,
              size_pct=None, stop_loss=None, take_profit=None, reason=None, dry_run=False):
    cmd = ["python3", TRADE_EXECUTE, action, "--portfolio", portfolio_path]
    if action == "open":
        cmd += ["--pair", pair, "--direction", direction,
                "--entry-price", str(price), "--size-pct", str(size_pct)]
        if stop_loss:
            cmd += ["--stop-loss", str(round(stop_loss, 2))]
        if take_profit:
            cmd += ["--take-profit", str(round(take_profit, 2))]
    elif action == "close":
        cmd += ["--pair", pair, "--exit-price", str(price), "--reason", reason]

    if dry_run:
        return {"dry_run": True, "cmd": " ".join(cmd)}

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    return json.loads(result.stdout)


def check_exits(portfolio, strategy, prices, comp_dir, dry_run):
    actions = []
    portfolio_path = os.path.join(comp_dir, f"portfolio-{portfolio['bot']}.json")
    exit_rules = strategy.get("exit", {})
    tp_pct = exit_rules.get("take_profit_pct", 0.5) / 100
    sl_pct = exit_rules.get("stop_loss_pct", 0.3) / 100
    timeout_min = exit_rules.get("timeout_minutes", 30)

    for pos in portfolio.get("positions", []):
        pair = pos["pair"]
        current = prices.get(pair, {}).get("last")
        if current is None:
            continue

        entry = pos["entry_price"]
        direction = pos["direction"]
        opened_at = datetime.fromisoformat(pos["opened_at"])
        age_minutes = (datetime.now(timezone.utc) - opened_at).total_seconds() / 60

        if direction == "long":
            pnl_pct = (current - entry) / entry
        else:
            pnl_pct = (entry - current) / entry

        hit_tp = pnl_pct >= tp_pct
        hit_sl = pnl_pct <= -sl_pct

        reason = None
        if hit_tp:
            reason = "target"
        elif hit_sl:
            reason = "stop"
        elif age_minutes >= timeout_min:
            reason = "timeout"

        if reason:
            result = run_trade("close", portfolio_path, pair=pair, price=current,
                               reason=reason, dry_run=dry_run)
            actions.append({"action": "close", "pair": pair, "reason": reason, "result": result})

    return actions


def check_entries(portfolio, strategy, history, prices, comp_dir, dry_run):
    actions = []
    portfolio_path = os.path.join(comp_dir, f"portfolio-{portfolio['bot']}.json")
    pos_config = strategy.get("position", {})
    max_open = pos_config.get("max_open", 1)
    size_pct = pos_config.get("size_pct", 20)

    exit_rules = strategy.get("exit", {})
    tp_pct = exit_rules.get("take_profit_pct", 0.5) / 100
    sl_pct = exit_rules.get("stop_loss_pct", 0.3) / 100

    open_pairs = {p["pair"] for p in portfolio.get("positions", [])}
    if len(open_pairs) >= max_open:
        return actions

    entry_rules = strategy.get("entry", {})

    for pair in strategy.get("pairs", []):
        if len(open_pairs) >= max_open:
            break
        if pair in open_pairs:
            continue

        current = prices.get(pair, {}).get("last")
        if current is None:
            continue

        for direction in ["long", "short"]:
            conditions = entry_rules.get(direction, {}).get("conditions", [])
            if not conditions:
                continue

            signal = evaluate_entry(conditions, history, pair)
            if not signal:
                continue

            if direction == "long":
                stop_price = current * (1 - sl_pct)
                tp_price = current * (1 + tp_pct)
            else:
                stop_price = current * (1 + sl_pct)
                tp_price = current * (1 - tp_pct)

            result = run_trade("open", portfolio_path, pair=pair, direction=direction,
                               price=current, size_pct=size_pct,
                               stop_loss=stop_price, take_profit=tp_price,
                               dry_run=dry_run)
            actions.append({"action": "open", "pair": pair, "direction": direction, "result": result})
            open_pairs.add(pair)
            break

    return actions


def check_risk(portfolio, strategy, risk_state, comp_dir, now_iso):
    bot = portfolio["bot"]
    bot_state = risk_state.get(bot, {})

    if bot_state.get("stopped"):
        return "stopped"

    paused_until = bot_state.get("paused_until")
    if paused_until and now_iso < paused_until:
        return "paused"

    risk_rules = strategy.get("risk", {})
    total_pnl_pct = portfolio["stats"]["total_pnl_pct"]

    stop_pct = risk_rules.get("stop_if_down_pct", 10)
    pause_pct = risk_rules.get("pause_if_down_pct", 5)
    pause_min = risk_rules.get("pause_minutes", 60)

    if total_pnl_pct <= -stop_pct:
        risk_state[bot] = {"stopped": True, "paused_until": None}
        return "stopped"

    if total_pnl_pct <= -pause_pct:
        pause_until = (
            datetime.now(timezone.utc) + timedelta(minutes=pause_min)
        ).isoformat()
        risk_state[bot] = {"stopped": False, "paused_until": pause_until}
        return "paused"

    return "ok"


def is_competition_expired(meta):
    started = datetime.fromisoformat(meta["started_at"])
    end_time = started + timedelta(hours=meta["duration_hours"])
    return datetime.now(timezone.utc) >= end_time


def main():
    dry_run = "--dry-run" in sys.argv

    comp_id, meta, comp_dir = find_active_competition()
    if comp_id is None:
        print("No active competition. Exiting.")
        return

    log(f"Tick: {comp_id} | dry_run={dry_run}", comp_dir)

    if is_competition_expired(meta):
        log("Competition window expired. Running final score.", comp_dir)
        score_script = os.path.join(
            SKILLS_DIR, "competition-score", "scripts", "competition_score.py"
        )
        r = subprocess.run(
            ["python3", score_script, comp_id, "--archive"],
            capture_output=True, text=True
        )
        if r.returncode == 0:
            log("Competition scored and archived.", comp_dir)
            print(r.stdout)
        else:
            log(f"Score failed: {r.stderr}", comp_dir)
        return

    try:
        prices = fetch_kraken_prices(meta["pairs"])
    except Exception as e:
        log(f"Price fetch failed: {e}", comp_dir)
        return

    history = append_prices(comp_dir, prices)

    price_summary = " | ".join(f"{p}: ${v['last']:,.2f}" for p, v in prices.items())
    log(f"Prices: {price_summary}", comp_dir)

    risk_state = load_risk_state(comp_dir)
    now_iso = datetime.now(timezone.utc).isoformat()

    for bot_name in meta["bots"]:
        strategy = load_strategy(bot_name)
        if strategy is None:
            log(f"  [{bot_name}] No strategy.yaml found, skipping", comp_dir)
            continue

        portfolio = load_portfolio(comp_dir, bot_name)
        if portfolio is None:
            log(f"  [{bot_name}] No portfolio found, skipping", comp_dir)
            continue

        status = check_risk(portfolio, strategy, risk_state, comp_dir, now_iso)
        if status in ("paused", "stopped"):
            log(f"  [{bot_name}] {status.upper()} -- skipping this tick", comp_dir)
            continue

        exit_actions = check_exits(portfolio, strategy, prices, comp_dir, dry_run)
        for a in exit_actions:
            log(f"  [{bot_name}] CLOSE {a['pair']} reason={a['reason']} | {a['result']}", comp_dir)

        portfolio = load_portfolio(comp_dir, bot_name)

        entry_actions = check_entries(portfolio, strategy, history, prices, comp_dir, dry_run)
        for a in entry_actions:
            log(f"  [{bot_name}] OPEN {a['direction'].upper()} {a['pair']} | {a['result']}", comp_dir)

        # Mark-to-market: reload portfolio then write live equity every tick
        portfolio = load_portfolio(comp_dir, bot_name) or portfolio
        starting_capital = meta.get("starting_capital", 1000.0)
        positions = portfolio.get("positions", [])
        base_equity = portfolio["stats"]["current_equity"]
        cash = base_equity - sum(p.get("cost_basis", 0) for p in positions)
        live_equity = cash
        for pos in positions:
            cp   = prices.get(pos["pair"], {}).get("last")
            qty  = pos.get("quantity", 0)
            ep   = pos.get("entry_price", 0)
            cost = pos.get("cost_basis", 0)
            if cp:
                mv = qty * cp if pos.get("direction") == "long" else cost + (ep - cp) * qty
            else:
                mv = cost
            live_equity += mv
        portfolio["stats"]["live_equity_mtm"] = round(live_equity, 2)
        portfolio["stats"]["live_pnl_usd"]    = round(live_equity - starting_capital, 2)
        portfolio["stats"]["live_pnl_pct"]    = round((live_equity - starting_capital) / starting_capital * 100, 4)
        pfile_path = os.path.join(comp_dir, f"portfolio-{bot_name}.json")
        with open(pfile_path, "w") as f:
            json.dump(portfolio, f, indent=2)

        if not exit_actions and not entry_actions:
            equity = portfolio["stats"]["live_equity_mtm"]
            pnl = portfolio["stats"]["live_pnl_pct"]
            log(f"  [{bot_name}] no signal | equity=${equity:,.2f} | pnl={pnl:+.2f}%", comp_dir)

    save_risk_state(comp_dir, risk_state)
    log("Tick complete.", comp_dir)


if __name__ == "__main__":
    main()
