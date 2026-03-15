#!/usr/bin/env python3
"""
arb_competition_tick.py - Statistical arbitrage competition tick engine.

Evaluates z-score conditions for each arb bot and manages spread positions.
Run every 30 minutes via cron (after swing_price_store.py + arb_price_store.py).

Entry logic:
  |z_score| >= z_entry  →  open spread position
    z > 0: SHORT spread (short A, long B) — ratio expected to fall back to mean
    z < 0: LONG  spread (long A, short B) — ratio expected to rise back to mean

Exit logic:
  |z_score| <  z_exit   →  close (mean reversion achieved)
  |z_score| >  z_stop (wrong direction) →  stop loss
  age >= timeout_hours  →  timeout exit

P&L model (simplified ratio-based):
  pnl_usd = (size_usd / 2) * direction_mult * (ratio_now / ratio_entry - 1)
  where direction_mult = +1 for long spread, -1 for short spread
"""
import os
import sys
import json
import yaml
import shutil
from datetime import datetime, timezone, timedelta

WORKSPACE    = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
ACTIVE_DIR   = os.path.join(WORKSPACE, "competition", "arb", "active")
RESULTS_DIR  = os.path.join(WORKSPACE, "competition", "arb", "results")
FLEET_DIR    = os.path.join(WORKSPACE, "fleet", "arb")
STATS_PATH   = os.path.join(WORKSPACE, "competition", "arb", "pair_stats.json")
CYCLE_STATE  = os.path.join(WORKSPACE, "competition", "arb", "arb_cycle_state.json")

BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID   = "8154505910"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso():
    return datetime.now(timezone.utc).isoformat()


def hours_since(iso_str):
    if not iso_str:
        return 0
    return (datetime.now(timezone.utc) - datetime.fromisoformat(iso_str)).total_seconds() / 3600


def load_json(path):
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_strategy(bot_name):
    path = os.path.join(FLEET_DIR, bot_name, "strategy.yaml")
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def load_portfolio(comp_dir, bot):
    return load_json(os.path.join(comp_dir, f"portfolio-{bot}.json"))


def save_portfolio(comp_dir, bot, portfolio):
    save_json(os.path.join(comp_dir, f"portfolio-{bot}.json"), portfolio)


def load_pair_stats():
    data = load_json(STATS_PATH)
    return data.get("pairs", {}) if data else {}


def find_active_comp():
    if not os.path.isdir(ACTIVE_DIR):
        return None, None
    entries = sorted(os.listdir(ACTIVE_DIR))
    if not entries:
        return None, None
    comp_id  = entries[-1]
    comp_dir = os.path.join(ACTIVE_DIR, comp_id)
    meta     = load_json(os.path.join(comp_dir, "meta.json"))
    if not meta:
        return None, None
    return comp_dir, meta


def tg_send(msg):
    try:
        import urllib.request
        data = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode()
        req  = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=data, headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"  Telegram notify failed: {e}")


# ---------------------------------------------------------------------------
# P&L computation
# ---------------------------------------------------------------------------

def spread_pnl(pos, current_ratio):
    """
    Compute P&L for an open spread position.

    For a LONG spread (long A / short B):
      profit when ratio rises  (A outperforms B)

    For a SHORT spread (short A / long B):
      profit when ratio falls  (B outperforms A)

    Returns (pnl_pct, pnl_usd) where pnl_pct is in percent.
    """
    entry_ratio    = pos["entry_ratio"]
    size_usd       = pos["size_usd"]   # total — each leg is half
    direction_mult = 1.0 if pos["direction"] == "long" else -1.0

    if entry_ratio == 0:
        return 0.0, 0.0

    ratio_change = (current_ratio - entry_ratio) / entry_ratio
    pnl_pct  = direction_mult * ratio_change * 100
    pnl_usd  = (size_usd / 2) * direction_mult * ratio_change
    return round(pnl_pct, 4), round(pnl_usd, 2)


# ---------------------------------------------------------------------------
# Exit checking
# ---------------------------------------------------------------------------

def check_exits(portfolio, strategy, pair_stats):
    z_exit    = strategy.get("z_exit", 0.5)
    z_stop    = strategy.get("z_stop", 4.0)
    timeout_h = strategy.get("timeout_hours", 120)

    pair_key = f"{strategy['pair_a']}/{strategy['pair_b']}"
    stats    = pair_stats.get(pair_key)
    if not stats:
        return portfolio, []

    current_z     = stats["z_score"]
    current_ratio = stats["current_ratio"]
    closed = []
    remaining = []

    for pos in portfolio.get("positions", []):
        pnl_pct, pnl_usd = spread_pnl(pos, current_ratio)
        age_h = hours_since(pos.get("opened_at"))

        reverted   = abs(current_z) < z_exit
        hit_stop   = ((pos["direction"] == "short" and current_z >  z_stop) or
                      (pos["direction"] == "long"  and current_z < -z_stop))
        timed_out  = age_h >= timeout_h

        if reverted or hit_stop or timed_out:
            reason   = "REVERT" if reverted else ("STOP" if hit_stop else "TIMEOUT")
            fee      = pos["size_usd"] * portfolio.get("fee_rate", 0.001)
            net_pnl  = pnl_usd - fee

            portfolio["equity"] = round(portfolio["equity"] + net_pnl, 2)
            s = portfolio["stats"]
            s["total_trades"]  += 1
            s["total_fees"]     = round(s["total_fees"] + fee, 4)
            s["total_pnl_usd"]  = round(s["total_pnl_usd"] + net_pnl, 2)
            s["total_pnl_pct"]  = round(
                s["total_pnl_usd"] / portfolio.get("starting_capital", 1000.0) * 100, 4)
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

            closed.append({
                "spread":    f"{strategy['pair_a']}/{strategy['pair_b']}",
                "direction": pos["direction"],
                "reason":    reason,
                "pnl_pct":   round(pnl_pct, 3),
                "net_pnl":   round(net_pnl, 2),
                "exit_z":    round(current_z, 3),
            })
        else:
            remaining.append(pos)

    portfolio["positions"] = remaining
    return portfolio, closed


# ---------------------------------------------------------------------------
# Entry logic
# ---------------------------------------------------------------------------

def try_entry(portfolio, strategy, pair_stats):
    z_entry   = strategy.get("z_entry", 2.0)
    max_open  = strategy.get("max_positions", 1)
    size_pct  = strategy.get("max_position_pct", 0.35)
    stop_down = strategy.get("stop_if_down_pct", 20)

    starting = portfolio.get("starting_capital", 1000.0)
    equity   = portfolio["equity"]
    drawdown = (starting - equity) / starting * 100
    if drawdown >= stop_down:
        return portfolio, None

    if len(portfolio.get("positions", [])) >= max_open:
        return portfolio, None

    pair_key = f"{strategy['pair_a']}/{strategy['pair_b']}"
    stats    = pair_stats.get(pair_key)
    if not stats:
        return portfolio, None

    current_z     = stats["z_score"]
    current_ratio = stats["current_ratio"]
    price_a       = stats.get("price_a")
    price_b       = stats.get("price_b")

    if abs(current_z) < z_entry:
        return portfolio, None

    direction = "short" if current_z > z_entry else "long"

    size_usd = round(equity * size_pct, 2)
    fee      = round(size_usd * portfolio.get("fee_rate", 0.001), 4)
    portfolio["equity"] = round(portfolio["equity"] - fee, 2)
    s = portfolio["stats"]
    s["total_fees"]    = round(s["total_fees"] + fee, 4)
    s["current_equity"] = portfolio["equity"]

    pos = {
        # Compatibility field for get_live_sprint display
        "pair":          f"{strategy['pair_a']} vs {strategy['pair_b']}",
        "direction":     direction,
        # Arb-specific
        "pair_a":        strategy["pair_a"],
        "pair_b":        strategy["pair_b"],
        "entry_ratio":   current_ratio,
        "entry_z":       current_z,
        "entry_price_a": price_a,
        "entry_price_b": price_b,
        "size_usd":      size_usd,
        "opened_at":     now_iso(),
    }
    portfolio["positions"].append(pos)

    return portfolio, {
        "direction": direction,
        "z":         current_z,
        "ratio":     current_ratio,
        "size_usd":  size_usd,
    }


# ---------------------------------------------------------------------------
# Archive + cycle state
# ---------------------------------------------------------------------------

def close_all_positions(portfolio, strategy, pair_stats):
    """Close all open positions at current prices for end-of-sprint scoring."""
    pair_key = f"{strategy['pair_a']}/{strategy['pair_b']}"
    stats    = pair_stats.get(pair_key, {})
    current_ratio = stats.get("current_ratio")

    for pos in portfolio.get("positions", []):
        ratio = current_ratio if current_ratio else pos["entry_ratio"]
        _, pnl_usd = spread_pnl(pos, ratio)
        fee = pos["size_usd"] * portfolio.get("fee_rate", 0.001)
        net = pnl_usd - fee
        portfolio["equity"] = round(portfolio["equity"] + net, 2)
        s = portfolio["stats"]
        s["total_trades"]  += 1
        s["total_pnl_usd"]  = round(s["total_pnl_usd"] + net, 2)
        s["total_pnl_pct"]  = round(
            s["total_pnl_usd"] / portfolio.get("starting_capital", 1000.0) * 100, 4)
    portfolio["positions"] = []
    return portfolio


def update_arb_cycle_state(comp_id):
    try:
        with open(CYCLE_STATE) as f:
            state = json.load(f)
    except Exception:
        state = {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4,
                 "status": "active", "sprints": []}

    if comp_id not in state.get("sprints", []):
        state.setdefault("sprints", []).append(comp_id)

    state["sprint_in_cycle"] = len(state["sprints"])
    cycle = state["cycle"]
    n     = state["sprint_in_cycle"]
    per   = state["sprints_per_cycle"]

    if n >= per:
        state["status"] = "awaiting_review"
        save_json(CYCLE_STATE, state)
        tg_send(
            f"*Arb Cycle {cycle} complete* — all {per} sprints finished.\n"
            f"Review standings and adjust bot strategies if needed."
        )
        print(f"  Arb Cycle {cycle} complete.")
    else:
        save_json(CYCLE_STATE, state)
        print(f"  Arb cycle state: Cycle {cycle}, Sprint {n}/{per}")


def archive_competition(comp_dir, meta, bots, pair_stats):
    comp_id  = meta["comp_id"]
    rankings = []

    for bot in bots:
        p = load_portfolio(comp_dir, bot)
        if not p:
            continue
        s_yaml = load_strategy(bot)
        if s_yaml:
            p = close_all_positions(p, s_yaml, pair_stats)
        save_portfolio(comp_dir, bot, p)

        s = p["stats"]
        rankings.append({
            "bot":              bot,
            "final_equity":     round(p["equity"], 2),
            "total_pnl_usd":    round(s["total_pnl_usd"], 2),
            "total_pnl_pct":    round(s.get("total_pnl_pct", 0.0), 4),
            "total_trades":     s["total_trades"],
            "wins":             s["wins"],
            "losses":           s["losses"],
            "win_rate":         s["win_rate"],
            "max_drawdown_pct": s["max_drawdown_pct"],
            "rank":             None,
        })

    rankings.sort(key=lambda x: x["final_equity"], reverse=True)
    for i, r in enumerate(rankings, 1):
        r["rank"] = i

    final = {
        "comp_id":        comp_id,
        "league":         "arb",
        "scored_at":      now_iso(),
        "duration_hours": meta["duration_hours"],
        "pairs":          meta.get("pairs", []),
        "winner":         rankings[0]["bot"] if rankings else None,
        "rankings":       rankings,
    }

    os.makedirs(os.path.join(RESULTS_DIR, comp_id), exist_ok=True)
    save_json(os.path.join(RESULTS_DIR, comp_id, "final_score.json"), final)
    shutil.move(comp_dir, os.path.join(RESULTS_DIR, comp_id + "_portfolios"))

    print(f"  Archived: {comp_id}  winner: {final['winner']}")
    update_arb_cycle_state(comp_id)
    return final


# ---------------------------------------------------------------------------
# Main tick
# ---------------------------------------------------------------------------

def main():
    comp_dir, meta = find_active_comp()
    if not comp_dir:
        print("No active arb competition.")
        return

    comp_id = meta["comp_id"]
    bots    = meta.get("bots", [])

    print(f"Arb tick: {comp_id}  {now_iso()[:16]}")

    pair_stats = load_pair_stats()
    if not pair_stats:
        print("  WARNING: pair_stats.json missing — run arb_price_store.py first")
        return

    # Check if the stats are stale (> 2 hours old)
    gen = pair_stats.get(list(pair_stats.keys())[0], {}).get("computed_at") if pair_stats else None
    if gen:
        age_h = hours_since(gen)
        if age_h > 2:
            print(f"  WARNING: pair_stats are {age_h:.1f}h old — consider running arb_price_store.py")

    # Check expiry
    started_at  = datetime.fromisoformat(meta["started_at"])
    duration_h  = meta.get("duration_hours", 168)
    expires_at  = started_at + timedelta(hours=duration_h)
    if datetime.now(timezone.utc) >= expires_at:
        print("  Competition expired — archiving...")
        archive_competition(comp_dir, meta, bots, pair_stats)
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

        portfolio, closed = check_exits(portfolio, strategy, pair_stats)
        for c in closed:
            sign = "+" if c["net_pnl"] >= 0 else ""
            print(f"  CLOSE {bot:12} {c['direction']:5} {c['spread']}"
                  f" [{c['reason']}] z={c['exit_z']:+.2f}  {sign}${c['net_pnl']:.2f}")

        portfolio, opened = try_entry(portfolio, strategy, pair_stats)
        if opened:
            spread = f"{strategy['pair_a']}/{strategy['pair_b']}"
            print(f"  OPEN  {bot:12} {opened['direction']:5} {spread}"
                  f" z={opened['z']:+.2f}  ratio={opened['ratio']:.6f}  ${opened['size_usd']:.0f}")

        save_portfolio(comp_dir, bot, portfolio)

    print("  Done.")


if __name__ == "__main__":
    main()
