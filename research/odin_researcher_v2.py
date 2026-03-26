#!/usr/bin/env python3
"""
odin_researcher_v2.py - Population-based evolutionary strategy optimizer.

Improvements over v1:
- Keeps elite population of top-10 strategies (escapes local optima)
- Multiple mutation types: LLM, perturbation, crossover, random restart
- Dynamic LLM prompting with parameter sensitivity analysis
- Adaptive exploration: random restart weight increases during stalls

Usage:
  python3 odin_researcher_v2.py --league day
  python3 odin_researcher_v2.py --league swing
"""
import argparse
import copy
import json
import math
import os
import random
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

import yaml

WORKSPACE     = "/root/.openclaw/workspace"
RESEARCH      = os.path.join(WORKSPACE, "research")
GEMINI_SECRET = "/root/.openclaw/secrets/gemini.json"
GEMINI_MODEL  = "gemini-2.5-flash-lite"
GEMINI_BASE   = "https://generativelanguage.googleapis.com/v1beta/models"

SUSPICIOUS_SHARPE   = 3.5
POPULATION_SIZE     = 10
STALL_ALERT_GENS    = 300
TG_BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
TG_CHAT_ID   = "8154505910"
MIN_TRADES = {"day": 50, "swing": 20}

ALL_PAIRS = [
    "BTC/USD",  "ETH/USD",  "SOL/USD",  "XRP/USD",
    "DOGE/USD", "AVAX/USD", "LINK/USD", "UNI/USD",
    "AAVE/USD", "NEAR/USD", "APT/USD",  "SUI/USD",
    "ARB/USD",  "OP/USD",   "ADA/USD",  "POL/USD",
]

DAY_RANGES = {
    "take_profit_pct": (0.8, 6.0),
    "stop_loss_pct": (0.8, 4.0),
    "timeout_minutes": (60, 720),
    "size_pct": (10, 35),
    "max_open": (1, 4),
}
SWING_RANGES = {
    "take_profit_pct": (3.0, 12.0),
    "stop_loss_pct": (2.0, 5.0),
    "timeout_hours": (48, 240),
    "size_pct": (15, 30),
    "max_open": (1, 3),
}

INDICATORS = {
    "trend": {
        "long": {"operator": "eq", "value": "up"},
        "short": {"operator": "eq", "value": "down"},
        "periods_day": [60, 120, 180, 240, 360, 480],
        "periods_swing_h": [24, 48, 72, 168],
    },
    "macd_signal": {
        "long": {"operator": "eq", "value": "bullish"},
        "short": {"operator": "eq", "value": "bearish"},
        "periods_day": [15, 30, 60, 120],
        "periods_swing_h": [12, 24, 26, 48],
    },
    "price_change_pct": {
        "long": {"operator": "lt", "range": (-2.0, -0.1)},
        "short": {"operator": "gt", "range": (0.1, 2.0)},
        "periods_day": [5, 10, 15, 30, 60],
        "periods_swing_h": [6, 12, 24, 48, 72],
    },
    "rsi": {
        "long_op": "lt", "long_range": (25, 48),
        "short_op": "gt", "short_range": (52, 75),
        "periods_day": [7, 14, 21, 30],
        "periods_swing_h": [7, 14, 21],
    },
    "price_vs_vwap": {
        "long": {"operator": "eq", "values": ["above", "below"]},
        "short": {"operator": "eq", "values": ["above", "below"]},
        "periods_day": [5],
        "periods_swing_h": [24],
    },
    "price_vs_ema": {
        "long": {"operator": "eq", "values": ["above", "below"]},
        "short": {"operator": "eq", "values": ["above", "below"]},
        "periods_day": [60, 120, 240],
        "periods_swing_h": [24, 48, 168],
    },
    "bollinger_position": {
        "long": {"operator": "eq", "values": ["below_lower", "inside"]},
        "short": {"operator": "eq", "values": ["above_upper", "inside"]},
        "periods_day": [60, 120, 240],
        "periods_swing_h": [24, 48, 168],
    },
    "momentum_accelerating": {
        "long": {"operator": "eq", "values": [True, False]},
        "short": {"operator": "eq", "values": [True, False]},
        "periods_day": [60, 120, 240],
        "periods_swing_h": [24, 48, 168],
    },
}

# ----------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------

def tg_send(msg):
    try:
        payload = json.dumps({
            "chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "HTML",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
            data=payload, headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


def load_gemini_key(league):
    with open(GEMINI_SECRET) as f:
        data = json.load(f)
    return data.get(f"gemini_{league}_key") or data["gemini_api_key"]


def call_gemini(prompt, api_key):
    url = f"{GEMINI_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 2000},
    }).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def extract_yaml(text):
    m = re.search(r"```yaml\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(name:.*)", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def league_dir(league):
    return os.path.join(RESEARCH, league)


def pop_dir(league):
    d = os.path.join(league_dir(league), "population")
    os.makedirs(d, exist_ok=True)
    return d


def get_fleet_path(league):
    if league == "day":
        return os.path.join(WORKSPACE, "fleet", "autobotday", "strategy.yaml")
    elif league == "swing":
        return os.path.join(WORKSPACE, "fleet", "swing", "autobotswing", "strategy.yaml")
    return None


def get_ranges(league):
    return DAY_RANGES if league == "day" else SWING_RANGES


# ----------------------------------------------------------------
# Population management
# ----------------------------------------------------------------

class Population:
    def __init__(self, league):
        self.league = league
        self.elites = []  # list of (sharpe, strategy_dict, yaml_str)

    def load(self):
        d = pop_dir(self.league)
        self.elites = []
        for i in range(POPULATION_SIZE):
            path = os.path.join(d, f"elite_{i}.yaml")
            if os.path.exists(path):
                with open(path) as f:
                    text = f.read()
                strat = yaml.safe_load(text)
                sharpe = strat.get("_sharpe", 0.0)
                self.elites.append((sharpe, strat, text))
        self.elites.sort(key=lambda x: x[0], reverse=True)

    def save(self):
        d = pop_dir(self.league)
        for i, (sharpe, strat, _) in enumerate(self.elites):
            strat["_sharpe"] = sharpe
            path = os.path.join(d, f"elite_{i}.yaml")
            text = yaml.dump(strat, default_flow_style=False, sort_keys=False)
            with open(path, "w") as f:
                f.write(text)
            # Update tuple with fresh text
            self.elites[i] = (sharpe, strat, text)
        # Remove any stale files beyond current population
        for i in range(len(self.elites), POPULATION_SIZE):
            path = os.path.join(d, f"elite_{i}.yaml")
            if os.path.exists(path):
                os.remove(path)

    def seed_from(self, strategy_dict, strategy_yaml, sharpe):
        strategy_dict["_sharpe"] = sharpe
        self.elites = [(sharpe, strategy_dict, strategy_yaml)]
        self.save()

    def best_sharpe(self):
        return self.elites[0][0] if self.elites else 0.0

    def worst_sharpe(self):
        return self.elites[-1][0] if self.elites else -999.0

    def try_insert(self, strategy_dict, strategy_yaml, sharpe):
        """Returns (inserted, is_new_best)."""
        strategy_dict["_sharpe"] = sharpe
        entry = (sharpe, strategy_dict, strategy_yaml)
        is_new_best = sharpe > self.best_sharpe() if self.elites else True

        if len(self.elites) < POPULATION_SIZE:
            self.elites.append(entry)
            self.elites.sort(key=lambda x: x[0], reverse=True)
            self.save()
            if is_new_best:
                self._save_fleet(strategy_yaml)
            return True, is_new_best

        if sharpe > self.worst_sharpe():
            self.elites[-1] = entry
            self.elites.sort(key=lambda x: x[0], reverse=True)
            self.save()
            if is_new_best:
                self._save_fleet(strategy_yaml)
            return True, is_new_best

        return False, False

    def _save_fleet(self, yaml_text):
        strat = yaml.safe_load(yaml_text)
        strat.pop("_sharpe", None)
        clean = yaml.dump(strat, default_flow_style=False, sort_keys=False)
        fleet = get_fleet_path(self.league)
        if fleet:
            os.makedirs(os.path.dirname(fleet), exist_ok=True)
            with open(fleet, "w") as f:
                f.write(clean)
        with open(os.path.join(league_dir(self.league), "best_strategy.yaml"), "w") as f:
            f.write(clean)

    def pick_parent(self):
        if len(self.elites) <= 3:
            return random.choice(self.elites)
        return max(random.sample(self.elites, 3), key=lambda x: x[0])

    def pick_two_parents(self):
        if len(self.elites) < 2:
            p = self.elites[0]
            return p, p
        return tuple(random.sample(self.elites, 2))

    def summary(self):
        lines = []
        for i, (sharpe, strat, _) in enumerate(self.elites):
            ex = strat.get("exit", {})
            ps = strat.get("position", {})
            tp = ex.get("take_profit_pct", "?")
            sl = ex.get("stop_loss_pct", "?")
            to = ex.get("timeout_minutes") or ex.get("timeout_hours", "?")
            to_u = "m" if "timeout_minutes" in ex else "h"
            nl = len(strat.get("entry", {}).get("long", {}).get("conditions", []))
            ns = len(strat.get("entry", {}).get("short", {}).get("conditions", []))
            np_ = len(strat.get("pairs", []))
            lines.append(
                f"  {i+1}. Sharpe={sharpe:.4f} | TP={tp}% SL={sl}% "
                f"TO={to}{to_u} | size={ps.get('size_pct','?')}% "
                f"max_open={ps.get('max_open','?')} | {nl}L/{ns}S conds | {np_}p"
            )
        return "\n".join(lines)

# ----------------------------------------------------------------
# Mutations
# ----------------------------------------------------------------

def perturb(strategy, league):
    """Randomly tweak one numeric parameter."""
    s = copy.deepcopy(strategy)
    s.pop("_sharpe", None)
    r = get_ranges(league)
    ex = s.setdefault("exit", {})
    ps = s.setdefault("position", {})

    params = []
    params.append(("tp", ex, "take_profit_pct", r["take_profit_pct"]))
    params.append(("sl", ex, "stop_loss_pct", r["stop_loss_pct"]))
    to_key = "timeout_minutes" if league == "day" else "timeout_hours"
    params.append(("to", ex, to_key, r[to_key]))
    params.append(("sz", ps, "size_pct", r["size_pct"]))
    params.append(("mo", ps, "max_open", r["max_open"]))

    # Collect numeric condition values
    for side in ["long", "short"]:
        conds = s.get("entry", {}).get(side, {}).get("conditions", [])
        for ci, cond in enumerate(conds):
            val = cond.get("value")
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                ind = cond.get("indicator", "")
                if ind == "rsi":
                    lo, hi = (25, 48) if side == "long" else (52, 75)
                elif ind == "price_change_pct":
                    lo, hi = (-2.0, -0.1) if side == "long" else (0.1, 2.0)
                else:
                    lo, hi = val * 0.5, val * 2.0
                params.append((f"cond_{side}_{ci}", cond, "value", (lo, hi)))

    if not params:
        return s, "perturb_no_params"

    name, obj, key, (lo, hi) = random.choice(params)
    old_val = obj.get(key, (lo + hi) / 2)
    new_val = old_val * random.uniform(0.7, 1.3)

    if name in ("to", "mo"):
        new_val = int(round(new_val))
    new_val = max(lo, min(hi, new_val))
    if isinstance(new_val, float):
        new_val = round(new_val, 2)

    obj[key] = new_val
    return s, f"perturb {name}: {old_val}->{new_val}"


def crossover(parent_a, parent_b, league):
    """Entry from A, exit+position from B."""
    s = copy.deepcopy(parent_a)
    s.pop("_sharpe", None)
    s["exit"] = copy.deepcopy(parent_b.get("exit", {}))
    s["position"] = copy.deepcopy(parent_b.get("position", {}))
    s["name"] = "crossover"
    return s, "crossover(A_entry+B_exit)"


def random_condition(indicator_name, side, league):
    """Generate one random condition."""
    ind = INDICATORS[indicator_name]
    cond = {"indicator": indicator_name}

    if league == "day":
        cond["period_minutes"] = random.choice(ind.get("periods_day", [60]))
    else:
        cond["period_hours"] = random.choice(ind.get("periods_swing_h", [24]))

    if indicator_name == "rsi":
        if side == "long":
            cond["operator"] = ind["long_op"]
            cond["value"] = round(random.uniform(*ind["long_range"]), 1)
        else:
            cond["operator"] = ind["short_op"]
            cond["value"] = round(random.uniform(*ind["short_range"]), 1)
    elif "range" in ind.get(side, {}):
        c = ind[side]
        cond["operator"] = c["operator"]
        cond["value"] = round(random.uniform(*c["range"]), 2)
    elif "values" in ind.get(side, {}):
        c = ind[side]
        cond["operator"] = c["operator"]
        cond["value"] = random.choice(c["values"])
    elif "value" in ind.get(side, {}):
        c = ind[side]
        cond["operator"] = c["operator"]
        cond["value"] = c["value"]

    return cond


def random_strategy(league):
    """Generate a completely new random strategy."""
    r = get_ranges(league)
    n_conds = random.randint(2, 4)
    chosen = random.sample(list(INDICATORS.keys()), min(n_conds, len(INDICATORS)))

    long_conds = [random_condition(n, "long", league) for n in chosen]
    short_conds = [random_condition(n, "short", league) for n in chosen]

    n_pairs = random.randint(3, 8)
    pairs = random.sample(ALL_PAIRS, n_pairs)

    tp = round(random.uniform(*r["take_profit_pct"]), 1)
    sl = round(random.uniform(*r["stop_loss_pct"]), 1)
    to_key = "timeout_minutes" if league == "day" else "timeout_hours"
    to_val = int(random.uniform(*r[to_key]))
    sz = int(random.uniform(*r["size_pct"]))
    mo = random.randint(*r["max_open"])

    strategy = {
        "name": "random_restart",
        "style": "randomly generated",
        "pairs": pairs,
        "position": {"size_pct": sz, "max_open": mo, "fee_rate": 0.001},
        "entry": {
            "long": {"conditions": long_conds},
            "short": {"conditions": short_conds},
        },
        "exit": {"take_profit_pct": tp, "stop_loss_pct": sl, to_key: to_val},
        "risk": {
            "pause_if_down_pct": 4 if league == "day" else 8,
            "stop_if_down_pct": 10 if league == "day" else 18,
        },
    }
    if league == "day":
        strategy["risk"]["pause_minutes"] = 60
    else:
        strategy["risk"]["pause_hours"] = 48

    return strategy, f"random({n_conds}conds,{n_pairs}pairs)"

# ----------------------------------------------------------------
# LLM Mutation
# ----------------------------------------------------------------

def build_llm_prompt(league, best_yaml, population):
    pop_summary = population.summary()
    import yaml as _yaml
    try:
        best_strat = _yaml.safe_load(best_yaml)
        long_conds = best_strat.get("entry", {}).get("long", {}).get("conditions", [])
        n_conds = len(long_conds)
        cond_names = [c.get("indicator", "?") for c in long_conds]
    except Exception:
        n_conds = 0
        cond_names = []
    cond_list = ", ".join(cond_names) if cond_names else "unknown"
    if league == "day":
        ranges_desc = (
            "TP: 0.8-6.0%, SL: 0.8-4.0%, timeout: 60-720min, size_pct: 10-35%, max_open: 1-4\n"
            "RSI long: lt 25-48, RSI short: gt 52-75\n"
            "price_change_pct long: lt -2.0 to -0.1, short: gt 0.1 to 2.0\n"
            "trend periods: 60,120,180,240,360,480min\n"
            "macd_signal periods: 15,30,60,120min"
        )
    else:
        ranges_desc = (
            "TP: 3.0-12.0%, SL: 2.0-5.0%, timeout: 48-240h, size_pct: 15-30%, max_open: 1-3\n"
            "RSI long: lt 25-48, RSI short: gt 52-75\n"
            "price_change_pct long: lt -2.0 to -0.1, short: gt 0.1 to 2.0\n"
            "trend periods: 24,48,72,168h\n"
            "macd_signal periods: 12,24,26,48h"
        )
    parts = [
        f"You are a crypto {league} trading strategy optimizer."
          " Iterate on what works - do not explore random alternatives.\n\n",
        "## Current Best Strategy (ANCHOR - always start from this)\n",
        f"```yaml\n{best_yaml}```\n",
        f"This strategy has {n_conds} entry conditions: {cond_list}\n\n",
        "## Elite Population (context only - avoid duplicating)\n",
        f"{pop_summary}\n\n",
        "## Constraints\n",
        f"{ranges_desc}\n",
        "Minimum 50 trades required - strategies below this are invalid.\n",
        "stop_loss_pct minimum: 0.8%% (noise floor).\n\n",
        "## Your Task\n",
        "Make ONE small targeted modification to the current best strategy. Output a complete modified copy.\n\n",
        "Allowed changes (pick exactly one):\n",
        "- Loosen a threshold to increase trade frequency"
          "  (e.g. RSI long from 30 to 40, or remove momentum_accelerating)\n",
        "- Tighten a threshold to improve signal quality\n",
        "- Adjust TP, SL (min 0.8%%), or timeout\n",
        "- Change a condition lookback period\n",
        "- Add or remove one pair\n\n",
        "Rules:\n",
        "- Do NOT restructure or replace the core framework - modify this strategy only\n",
        f"- Do NOT exceed {n_conds + 1} total conditions\n",
        "- If strategy has more than 5 conditions, prefer removing one over adding\n",
        "- momentum_accelerating is often overfitting - consider removing it if present\n",
        "- Prioritize changes that increase trade count while preserving Sharpe\n\n",
        "Output ONLY the complete modified strategy YAML between ```yaml and ``` markers.",
    ]
    return "".join(parts)


def llm_mutate(best_yaml, league, population, api_key):
    prompt = build_llm_prompt(league, best_yaml, population)
    response = call_gemini(prompt, api_key)
    yaml_str = extract_yaml(response)
    if not yaml_str:
        return None, None, "yaml_not_found"
    try:
        strategy = yaml.safe_load(yaml_str)
        if not isinstance(strategy, dict):
            raise ValueError("Not a dict")
    except Exception as e:
        return None, None, f"yaml_parse: {e}"
    return strategy, yaml_str, None


# ----------------------------------------------------------------
# Results logging
# ----------------------------------------------------------------

def load_results(league):
    path = os.path.join(league_dir(league), "results.tsv")
    if not os.path.exists(path):
        return []
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("gen"):
                parts = line.split("\t")
                if len(parts) >= 6:
                    rows.append({
                        "gen": parts[0], "sharpe": parts[1],
                        "win_rate": parts[2], "pnl_pct": parts[3],
                        "trades": parts[4], "status": parts[5],
                    })
    return rows


def log_result(league, gen, result, status, description=""):
    path = os.path.join(league_dir(league), "results.tsv")
    write_header = not os.path.exists(path)
    with open(path, "a") as f:
        if write_header:
            f.write("gen\tsharpe\twin_rate\tpnl_pct\ttrades\tstatus\tdescription\tts\n")
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
        sharpe = result.get("sharpe", 0) if isinstance(result, dict) else 0
        win_rate = result.get("win_rate_pct", 0) if isinstance(result, dict) else 0
        pnl_pct = result.get("total_pnl_pct", 0) if isinstance(result, dict) else 0
        trades = result.get("total_trades", 0) if isinstance(result, dict) else 0
        f.write(f"{gen}\t{sharpe:.4f}\t{win_rate:.1f}\t{pnl_pct:.2f}\t"
                f"{trades}\t{status}\t{description}\t{ts}\n")


# ----------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league", choices=["day", "swing"], required=True)
    parser.add_argument("--sleep", type=int, default=60)
    parser.add_argument("--seed", default=None, help="Seed strategy YAML path")
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()
    league = args.league

    sys.path.insert(0, RESEARCH)
    from odin_backtest import run_backtest

    api_key = load_gemini_key(league)

    if args.offset > 0:
        time.sleep(args.offset)

    os.makedirs(league_dir(league), exist_ok=True)

    # Load or create population
    pop = Population(league)
    pop.load()

    if not pop.elites:
        seed_path = args.seed or os.path.join(league_dir(league), "best_strategy.yaml")
        fleet_path = get_fleet_path(league)
        if os.path.exists(seed_path):
            path = seed_path
        elif fleet_path and os.path.exists(fleet_path):
            path = fleet_path
        else:
            print(f"[odin-v2/{league}] No seed strategy found. Provide --seed.")
            sys.exit(1)

        with open(path) as f:
            seed_yaml = f.read()
        seed_strat = yaml.safe_load(seed_yaml)

        print(f"[odin-v2/{league}] Seeding population from {path}...")
        baseline = run_backtest(seed_strat, league, ALL_PAIRS)
        if "error" in baseline:
            print(f"  ERROR: {baseline['error']}")
            sys.exit(1)
        seed_sharpe = baseline["sharpe"]
        print(f"  Seed Sharpe={seed_sharpe:.4f} trades={baseline['total_trades']}")
        pop.seed_from(seed_strat, seed_yaml, seed_sharpe)

    # Load state
    results_history = load_results(league)
    state_path = os.path.join(league_dir(league), "gen_state.json")
    if os.path.exists(state_path):
        with open(state_path) as f:
            gs = json.load(f)
        gen = gs.get("gen", len(results_history) + 1)
        gens_since_best = gs.get("gens_since_best", 0)
    else:
        gen = len(results_history) + 1
        gens_since_best = 0

    min_t = MIN_TRADES.get(league, 30)

    print(f"[odin-v2/{league}] Pop: {len(pop.elites)} elites, best={pop.best_sharpe():.4f}")
    print(f"  Gen {gen}, stall={gens_since_best}, sleep={args.sleep}s")
    print()

    consec_429 = 0

    while True:
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        best_s = pop.best_sharpe()

        # Adaptive weights
        if gens_since_best < 100:
            weights = {"llm": 0.50, "perturb": 0.35, "crossover": 0.10, "random": 0.05}
        elif gens_since_best < 300:
            weights = {"llm": 0.45, "perturb": 0.35, "crossover": 0.10, "random": 0.10}
        else:
            weights = {"llm": 0.40, "perturb": 0.45, "crossover": 0.05, "random": 0.10}

        # Select mutation
        r = random.random()
        cum = 0
        mutation_type = "llm"
        for mt, w in weights.items():
            cum += w
            if r <= cum:
                mutation_type = mt
                break

        print(f"[{ts}] Gen {gen} | best={best_s:.4f} | stall={gens_since_best} | {mutation_type}",
              end=" ", flush=True)

        candidate = None
        candidate_yaml = None
        description = mutation_type

        if mutation_type == "llm":
            _, best_strat, _ = pop.elites[0]
            clean = copy.deepcopy(best_strat)
            clean.pop("_sharpe", None)
            best_yaml_str = yaml.dump(clean, default_flow_style=False, sort_keys=False)
            try:
                candidate, candidate_yaml, err = llm_mutate(
                    best_yaml_str, league, pop, api_key
                )
                if err:
                    print(f"| {err}")
                    log_result(league, gen, {}, f"llm_{err}")
                    gen += 1
                    if "429" in str(err):
                        consec_429 += 1
                        time.sleep(min(60 * (2 ** (consec_429 - 1)), 600))
                    else:
                        consec_429 = 0
                        time.sleep(args.sleep)
                    continue
                consec_429 = 0
            except Exception as e:
                err_s = str(e)
                print(f"| GEMINI: {err_s[:60]}")
                log_result(league, gen, {}, "gemini_error", err_s[:80])
                gen += 1
                if "429" in err_s:
                    consec_429 += 1
                    time.sleep(min(60 * (2 ** (consec_429 - 1)), 600))
                else:
                    consec_429 = 0
                    time.sleep(60)
                continue

        elif mutation_type == "perturb":
            _, parent_strat, _ = pop.pick_parent()
            candidate, description = perturb(parent_strat, league)
            candidate_yaml = yaml.dump(candidate, default_flow_style=False, sort_keys=False)

        elif mutation_type == "crossover":
            (_, a, _), (_, b, _) = pop.pick_two_parents()
            candidate, description = crossover(a, b, league)
            candidate_yaml = yaml.dump(candidate, default_flow_style=False, sort_keys=False)

        elif mutation_type == "random":
            candidate, description = random_strategy(league)
            candidate_yaml = yaml.dump(candidate, default_flow_style=False, sort_keys=False)

        if candidate is None:
            print("| no candidate")
            gen += 1
            time.sleep(args.sleep)
            continue

        # Backtest
        try:
            result = run_backtest(candidate, league, ALL_PAIRS)
        except Exception as e:
            print(f"| BT_ERR: {e}")
            log_result(league, gen, {}, "backtest_error", str(e)[:80])
            gen += 1
            time.sleep(args.sleep)
            continue

        if "error" in result:
            print(f"| BT_ERR: {result['error'][:50]}")
            log_result(league, gen, {}, "backtest_error", result["error"][:80])
            gen += 1
            time.sleep(args.sleep)
            continue

        sharpe = result["sharpe"]
        win_rate = result["win_rate_pct"]
        pnl_pct = result["total_pnl_pct"]
        trades = result["total_trades"]

        # Filters
        if result["suspicious"]:
            print(f"| sharpe={sharpe:.4f} REJECTED (suspicious)")
            log_result(league, gen, result, "rejected_suspicious")
            gen += 1
            time.sleep(args.sleep)
            continue

        if trades < min_t:
            print(f"| sharpe={sharpe:.4f} trades={trades} [low_trades]")
            log_result(league, gen, result, "low_trades", f"trades={trades}")
            gen += 1
            with open(state_path, "w") as f:
                json.dump({"gen": gen, "gens_since_best": gens_since_best}, f)
            time.sleep(args.sleep)
            continue

        # Population insertion
        inserted, is_new_best = pop.try_insert(candidate, candidate_yaml, sharpe)

        if is_new_best:
            status = "new_best"
            gens_since_best = 0
            print(f"| *** NEW BEST: sharpe={sharpe:.4f} win={win_rate}% "
                  f"pnl={pnl_pct:+.2f}% trades={trades} ***")
        elif inserted:
            status = "new_elite"
            gens_since_best += 1
            print(f"| sharpe={sharpe:.4f} [new_elite]")
        else:
            status = "discarded"
            gens_since_best += 1
            print(f"| sharpe={sharpe:.4f} win={win_rate}% trades={trades} [disc]")


        log_result(league, gen, result, status, description[:80])
        results_history.append({
            "gen": str(gen), "sharpe": f"{sharpe:.4f}",
            "win_rate": f"{win_rate:.1f}", "pnl_pct": f"{pnl_pct:.2f}",
            "trades": str(trades), "status": status,
        })
        if len(results_history) > 300:
            results_history = results_history[-300:]

        gen += 1
        with open(state_path, "w") as f:
            json.dump({"gen": gen, "gens_since_best": gens_since_best}, f)
        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
