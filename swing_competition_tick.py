#!/usr/bin/env python3
"""
swing_competition_tick.py - Evaluate swing bot strategies every 30 minutes.

Reads the active swing competition, checks entry/exit conditions for each
bot against hourly candle data, and updates portfolio files.

Periods in swing strategy YAMLs are in HOURS (period_hours), not minutes.
Timeouts are in HOURS (timeout_hours). TP/SL percentages are wider than
day trading (typically 3-15% TP, 1-3% SL).
"""
import os
import urllib.request
import sys
import json
import yaml
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swing_price_store import get_current_price, update_pair, update_spread_ratios
from swing_indicators import evaluate_entry

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
ACTIVE_DIR   = os.path.join(WORKSPACE, "competition", "swing", "active")
RESULTS_DIR  = os.path.join(WORKSPACE, "competition", "swing", "results")
CYCLE_STATE  = os.path.join(WORKSPACE, "competition", "swing", "swing_cycle_state.json")
BOT_TOKEN    = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID      = "8154505910"
FLEET_DIR    = os.path.join(WORKSPACE, "fleet", "swing")

ALL_PAIRS = [
    "BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "DOGE/USD",
    "AVAX/USD", "LINK/USD", "UNI/USD", "AAVE/USD", "NEAR/USD",
    "APT/USD", "SUI/USD", "ARB/USD", "OP/USD", "WIF/USD",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_strategy(bot_name):
    path = os.path.join(FLEET_DIR, bot_name, "strategy.yaml")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def load_portfolio(comp_dir, bot):
    path = os.path.join(comp_dir, f"portfolio-{bot}.json")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_portfolio(comp_dir, bot, portfolio):
    path = os.path.join(comp_dir, f"portfolio-{bot}.json")
    with open(path, "w") as f:
        json.dump(portfolio, f, indent=2)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def hours_since(iso_str):
    if not iso_str:
        return 0
    dt = datetime.fromisoformat(iso_str)
    return (datetime.now(timezone.utc) - dt).total_seconds() / 3600


# ---------------------------------------------------------------------------
# Position management
# ---------------------------------------------------------------------------

def check_exits(portfolio, strategy, prices):
    """Check TP, SL, and timeout on open positions. Returns updated portfolio."""
    exit_cfg   = strategy.get("exit", {})
    tp_pct     = exit_cfg.get("take_profit_pct", 5.0)
    sl_pct     = exit_cfg.get("stop_loss_pct", 2.0)
    timeout_h  = exit_cfg.get("timeout_hours", 72)
    fee_rate   = strategy.get("position", {}).get("fee_rate", 0.001)

    closed = []
    remaining = []

    for pos in portfolio.get("positions", []):
        pair      = pos["pair"]
        direction = pos["direction"]
        entry     = pos["entry_price"]
        size_usd  = pos["size_usd"]
        opened_at = pos.get("opened_at", now_iso())

        current = prices.get(pair)
        if current is None:
            remaining.append(pos)
            continue

        pnl_pct = ((current - entry) / entry * 100) if direction == "long" \
                  else ((entry - current) / entry * 100)

        age_hours = hours_since(opened_at)
        hit_tp      = pnl_pct >= tp_pct
        hit_sl      = pnl_pct <= -sl_pct
        hit_timeout = age_hours >= timeout_h

        if hit_tp or hit_sl or hit_timeout:
            gross_pnl = size_usd * pnl_pct / 100
            fee       = size_usd * fee_rate
            net_pnl   = gross_pnl - fee
            reason    = "TP" if hit_tp else ("SL" if hit_sl else "TIMEOUT")

            portfolio["equity"] = round(portfolio["equity"] + net_pnl, 2)
            s = portfolio["stats"]
            s["total_trades"]   += 1
            s["total_fees"]      = round(s["total_fees"] + fee, 4)
            s["total_pnl_usd"]   = round(s["total_pnl_usd"] + net_pnl, 2)
            s["total_pnl_pct"]   = round(s["total_pnl_pct"] + pnl_pct, 4)
            if net_pnl > 0:
                s["wins"] += 1
            else:
                s["losses"] += 1
            t = s["total_trades"]
            s["win_rate"] = round(s["wins"] / t * 100, 1) if t > 0 else 0.0

            dd = (portfolio["peak_equity"] - portfolio["equity"]) / portfolio["peak_equity"] * 100
            if dd > s["max_drawdown_pct"]:
                s["max_drawdown_pct"] = round(dd, 4)
            if portfolio["equity"] > portfolio["peak_equity"]:
                portfolio["peak_equity"] = portfolio["equity"]

            s["current_equity"] = portfolio["equity"]
            closed.append((pair, direction, reason, round(pnl_pct, 2), round(net_pnl, 2)))
        else:
            remaining.append(pos)

    portfolio["positions"] = remaining
    return portfolio, closed


def try_entries(portfolio, strategy, prices, comp_pairs):
    """Evaluate entry conditions and open new positions."""
    pos_cfg    = strategy.get("position", {})
    size_pct   = pos_cfg.get("size_pct", 20) / 100
    max_open   = pos_cfg.get("max_open", 2)
    fee_rate   = pos_cfg.get("fee_rate", 0.001)

    risk_cfg   = strategy.get("risk", {})
    stop_pct   = risk_cfg.get("stop_if_down_pct", 20)
    pause_pct  = risk_cfg.get("pause_if_down_pct", 10)
    pause_h    = risk_cfg.get("pause_hours", 24)

    starting   = portfolio.get("starting_capital", 10000)
    equity     = portfolio["equity"]
    drawdown   = (starting - equity) / starting * 100

    if drawdown >= stop_pct:
        return portfolio, []

    if drawdown >= pause_pct:
        paused_at = portfolio.get("paused_at")
        if paused_at and hours_since(paused_at) < pause_h:
            return portfolio, []
        portfolio["paused_at"] = now_iso()
        return portfolio, []

    open_pairs = {p["pair"] for p in portfolio.get("positions", [])}
    if len(open_pairs) >= max_open:
        return portfolio, []

    strategy_pairs = [p for p in strategy.get("pairs", comp_pairs) if p in comp_pairs]
    opened = []

    for pair in strategy_pairs:
        if pair in open_pairs or len(open_pairs) >= max_open:
            break
        current = prices.get(pair)
        if current is None:
            continue


        # Spread bots: evaluate conditions on ratio pair, trade base pair
        spread_cfg    = strategy.get("spread", {})
        analysis_pair = spread_cfg.get("analysis_pair", pair)

        for direction in ["long", "short"]:
            conditions = strategy.get("entry", {}).get(direction, {}).get("conditions", [])
            if not conditions:
                continue
            result = evaluate_entry(conditions, analysis_pair)
            if result is True:
                size_usd = round(equity * size_pct, 2)
                fee      = round(size_usd * fee_rate, 4)
                portfolio["equity"] = round(portfolio["equity"] - fee, 2)
                portfolio["stats"]["total_fees"] = round(
                    portfolio["stats"]["total_fees"] + fee, 4)
                portfolio["stats"]["current_equity"] = portfolio["equity"]

                pos = {
                    "pair":        pair,
                    "direction":   direction,
                    "entry_price": current,
                    "size_usd":    size_usd,
                    "opened_at":   now_iso(),
                }
                portfolio["positions"].append(pos)
                open_pairs.add(pair)
                opened.append((pair, direction, current))
                break

    return portfolio, opened


# ---------------------------------------------------------------------------
# Active competition management
# ---------------------------------------------------------------------------

def find_active_comp():
    if not os.path.isdir(ACTIVE_DIR):
        return None, None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None, None
    comp_id  = entries[-1]
    comp_dir = os.path.join(ACTIVE_DIR, comp_id)
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None, None
    with open(meta_path) as f:
        meta = json.load(f)
    return comp_dir, meta


def tg_send(msg):
    """Send a Telegram message to the configured chat."""
    try:
        import urllib.request as ur
        data = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode()
        req  = ur.Request(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                          data=data, headers={"Content-Type": "application/json"})
        ur.urlopen(req, timeout=5)
    except Exception as e:
        print(f"  Telegram notify failed: {e}")


def update_swing_cycle_state(comp_id):
    """Increment sprint_in_cycle after archiving. Pause and alert if cycle complete."""
    try:
        with open(CYCLE_STATE) as f:
            state = json.load(f)
    except Exception:
        state = {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4,
                 "cycle_started_at": None, "status": "active", "sprints": []}

    # Record this sprint if not already listed
    if comp_id not in state.get("sprints", []):
        state.setdefault("sprints", []).append(comp_id)

    state["sprint_in_cycle"] = len(state["sprints"])
    cycle    = state["cycle"]
    n        = state["sprint_in_cycle"]
    per      = state["sprints_per_cycle"]

    if n >= per:
        state["status"] = "awaiting_review"
        with open(CYCLE_STATE, "w") as f:
            json.dump(state, f, indent=2)
        tg_send(
            f"*Swing Cycle {cycle} complete* — all {per} sprints finished.\n"
            f"Review standings and adjust non-profitable bot strategies, then run:\n"
            f"`python3 /root/.openclaw/workspace/swing_cycle_advance.py`"
        )
        print(f"  Swing Cycle {cycle} complete. Telegram alert sent.")
    else:
        with open(CYCLE_STATE, "w") as f:
            json.dump(state, f, indent=2)
        print(f"  Swing cycle state: Cycle {cycle}, Sprint {n}/{per}")


def archive_competition(comp_dir, meta, bots, prices):
    """Score and archive a finished competition."""
    comp_id = meta["comp_id"]
    rankings = []
    for bot in bots:
        p = load_portfolio(comp_dir, bot)
        if not p:
            continue
        # Close all open positions at current price
        for pos in p.get("positions", []):
            pair    = pos["pair"]
            current = prices.get(pair, pos["entry_price"])
            pnl_pct = ((current - pos["entry_price"]) / pos["entry_price"] * 100) \
                      if pos["direction"] == "long" \
                      else ((pos["entry_price"] - current) / pos["entry_price"] * 100)
            fee    = pos["size_usd"] * meta.get("fee_rate", 0.001)
            net    = pos["size_usd"] * pnl_pct / 100 - fee
            p["equity"] = round(p["equity"] + net, 2)
            p["stats"]["total_trades"] += 1
            p["stats"]["total_pnl_usd"] = round(p["stats"]["total_pnl_usd"] + net, 2)
        p["positions"] = []
        save_portfolio(comp_dir, bot, p)

        s = p["stats"]
        rankings.append({
            "bot":              bot,
            "final_equity":     round(p["equity"], 2),
            "total_pnl_usd":    round(s["total_pnl_usd"], 2),
            "total_pnl_pct":    round(s["total_pnl_pct"], 4),
            "total_trades":     s["total_trades"],
            "wins":             s["wins"],
            "losses":           s["losses"],
            "win_rate":         s["win_rate"],
            "max_drawdown_pct": s["max_drawdown_pct"],
            "total_fees":       round(s["total_fees"], 4),
            "rank":             None,
        })

    rankings.sort(key=lambda x: x["final_equity"], reverse=True)
    for i, r in enumerate(rankings, 1):
        r["rank"] = i

    final = {
        "comp_id":        comp_id,
        "league":         "swing",
        "scored_at":      now_iso(),
        "duration_hours": meta["duration_hours"],
        "pairs":          meta["pairs"],
        "winner":         rankings[0]["bot"] if rankings else None,
        "rankings":       rankings,
    }

    result_dir = os.path.join(RESULTS_DIR, comp_id)
    os.makedirs(result_dir, exist_ok=True)
    with open(os.path.join(result_dir, "final_score.json"), "w") as f:
        json.dump(final, f, indent=2)

    # Move active -> results directory
    import shutil
    shutil.move(comp_dir, os.path.join(RESULTS_DIR, comp_id + "_portfolios"))

    print(f"  Archived: {comp_id}  winner: {final['winner']}")
    update_swing_cycle_state(comp_id)
    return final


# ---------------------------------------------------------------------------
# Main tick
# ---------------------------------------------------------------------------

def main():
    comp_dir, meta = find_active_comp()
    if not comp_dir:
        print("No active swing competition.")
        return

    comp_id = meta["comp_id"]
    bots    = meta.get("bots", [])
    pairs   = meta.get("pairs", ALL_PAIRS)

    # Refresh price data
    print(f"Swing tick: {comp_id}  {now_iso()[:16]}")
    for pair in pairs:
        update_pair(pair, full=False)

    prices = {pair: get_current_price(pair) for pair in pairs}
    update_spread_ratios()

    # Check if competition has expired
    started_at   = datetime.fromisoformat(meta["started_at"])
    duration_h   = meta.get("duration_hours", 168)
    expires_at   = started_at + timedelta(hours=duration_h)
    if datetime.now(timezone.utc) >= expires_at:
        print(f"  Competition expired — archiving...")
        archive_competition(comp_dir, meta, bots, prices)
        return

    hours_left = (expires_at - datetime.now(timezone.utc)).total_seconds() / 3600
    print(f"  {hours_left:.1f}h remaining")

    for bot in bots:
        portfolio = load_portfolio(comp_dir, bot)
        if not portfolio:
            continue
        strategy = load_strategy(bot)
        if not strategy:
            continue

        portfolio, closed = check_exits(portfolio, strategy, prices)
        for pair, direction, reason, pnl_pct, net_pnl in closed:
            sign = "+" if net_pnl >= 0 else ""
            print(f"  CLOSE {bot:8} {direction:5} {pair} [{reason}] "
                  f"{sign}{pnl_pct:.2f}%  {sign}${net_pnl:.2f}")

        portfolio, opened = try_entries(portfolio, strategy, prices, pairs)
        for pair, direction, price in opened:
            print(f"  OPEN  {bot:8} {direction:5} {pair} @ {price}")

        save_portfolio(comp_dir, bot, portfolio)

    print("  Done.")


if __name__ == "__main__":
    main()
