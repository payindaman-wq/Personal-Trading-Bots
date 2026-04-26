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
import hashlib
import copy
import json
import math
import os
import random
import sys as _sys
_sys.path.insert(0, "/root/.openclaw/workspace")
_sys.path.insert(0, "/root/.openclaw/workspace/research")
import kraken_leverage
import re
import sys
import subprocess
import time
import urllib.request
from collections import deque
from datetime import datetime, timezone
try:
    import backtest_drift
except ImportError:
    backtest_drift = None

import yaml

WORKSPACE     = "/root/.openclaw/workspace"
RESEARCH      = os.path.join(WORKSPACE, "research")
GEMINI_SECRET = "/root/.openclaw/secrets/gemini.json"
GEMINI_MODEL  = "gemini-2.5-flash-lite"
GEMINI_BASE   = "https://generativelanguage.googleapis.com/v1beta/models"

SUSPICIOUS_SHARPE   = 3.5
POPULATION_SIZE     = 10

# LLM cost control: if recent LLM attempts rarely yield a population hit,
# down-weight LLM calls and redirect to free local perturbation. Saves Gemini
# spend during narrow-plateau phases where LLM proposals aren't beating local
# perturbations anyway. Window re-fills as soon as an LLM call wins again.
LLM_WINDOW              = 20
LLM_PLATEAU_THRESHOLD   = 0.10   # <10% recent hits → cut llm weight to 0.20
LLM_PLATEAU_WEIGHT      = 0.20
_llm_history = deque(maxlen=LLM_WINDOW)

# F5: Gemini prompt dedup. On stalled leagues the system_instruction +
# user_message are near-identical gen-over-gen (same best_yaml, same
# mode-collapsed population). After LLM_DEDUP_THRESHOLD identical prompts
# in the last LLM_DEDUP_WINDOW recent calls, the next "llm" draw is flipped
# to "perturb" — free local mutation instead of paid Gemini call. Layered
# on top of LLM_PLATEAU_WEIGHT; cuts remaining LLM spend ~50% on stalls.
import hashlib as _hashlib
LLM_DEDUP_WINDOW    = 30
LLM_DEDUP_THRESHOLD = 3
_llm_prompt_hashes  = deque(maxlen=LLM_DEDUP_WINDOW)

def _llm_prompt_fingerprint(system_instruction, user_message):
    h = _hashlib.sha1()
    h.update(system_instruction.encode("utf-8", errors="replace"))
    h.update(b"|")
    h.update(user_message.encode("utf-8", errors="replace"))
    return h.hexdigest()

def _llm_plateau():
    if len(_llm_history) < LLM_WINDOW:
        return False
    return (sum(_llm_history) / LLM_WINDOW) < LLM_PLATEAU_THRESHOLD

MIN_TRADES = {"day": 280, "futures_day": 200, "futures_swing": 50}  # futures_day lowered 1700->600->200 on 2026-04-23 for BTC/ETH/SOL-only universe
SWING_MIN_TRADES    = 30   # IMMUTABLE - DO NOT MODIFY via LOKI (Item 4)
MIMIR_MIN_GAP_HRS   = 6    # min wall-clock hours between Mimir calls per league
# F12: stretched milestone cadence on stalled leagues. A league counts as
# stalled once gens_since_best >= MIMIR_STALL_FLOOR; its baseline MIMIR
# cadence drops from every 200 gens to every MIMIR_STALL_GAP_GENS.
MIMIR_STALL_FLOOR    = 500
MIMIR_STALL_GAP_GENS = 1000
SWING_MAX_TRADES    = 60   # swing hard upper bound (Item 3)
SWING_ALLOWED_PAIRS = frozenset({"BTC/USD", "ETH/USD", "SOL/USD"})  # Item 7
FUTURES_ALLOWED_PAIRS = frozenset({"BTC/USD", "ETH/USD", "SOL/USD"})  # Kraken Derivatives US universe

# F4 (mode-collapse): force a random genome into the candidate pool every
# FORCE_RANDOM_EVERY gens once gens_since_best >= FORCE_RANDOM_FLOOR. Breaks
# hill-climbing stalls where every perturbation lands in the same basin.
FORCE_RANDOM_FLOOR   = 500
FORCE_RANDOM_EVERY   = 500
# F8 (meta_audit 2026-04-25): hard OOS floor — candidate OOS must clear this
# regardless of champion_oos.
OOS_HARD_FLOOR       = 0.0
# F3 (meta_audit 2026-04-25): diversity injection thresholds.
DIVERSITY_UNIQUE_FLOOR = 3
DIVERSITY_STALL_FLOOR  = 500
DIVERSITY_KEEP_TOP     = 5
# F4: tighter elite dedup — reject insertions whose Sharpe matches an
# existing elite within this epsilon. Catches no-op perturbations that
# reproduce the parent exactly.
ELITE_SHARPE_EPS     = 0.001

_THROTTLE_FILE = os.path.join(RESEARCH, "anthropic_throttle.json")

def _is_anthropic_throttled():
    """Return True if daily budget throttle is active for today (UTC)."""
    try:
        import json as _j
        from datetime import date as _d
        with open(_THROTTLE_FILE) as _f:
            _td = _j.load(_f)
        return bool(_td.get("throttled")) and _td.get("date_utc") == _d.today().isoformat()
    except Exception:
        return False

# F10 (meta_audit): horizon-matched secondary gate for day leagues. Primary
# Sharpe is 2yr annualised; day sprints run 24h. A champion can have strong
# 2yr Sharpe but mediocre typical-24h Sharpe (regime-blended), which is what
# the sprint actually experiences. The gate requires candidate 24h-median
# Sharpe to be at least 80% of the champion's, so promotions don't regress
# the sprint-horizon metric. Swing leagues defer (need 7d window).
DAY_24H_GATE_LEAGUES = {"day", "futures_day"}
DAY_24H_GATE_FLOOR_FRAC = 0.8

# Known-bad result fingerprints — sharpe values that always indicate a poison attractor.
POISON_RESULT_FINGERPRINTS = {
    "futures_day":   {-2.7990, -3.3113, -4.8702},
    "futures_swing": {-1.0406, -0.8033},
}

ALL_PAIRS = [
    "BTC/USD",  "ETH/USD",  "SOL/USD",  "XRP/USD",
    "DOGE/USD", "AVAX/USD", "LINK/USD", "UNI/USD",
    "AAVE/USD", "NEAR/USD", "APT/USD",  "SUI/USD",
    "ARB/USD",  "OP/USD",   "ADA/USD",  "POL/USD",
]

def get_pairs(league):
    return ALL_PAIRS


def is_poison_yaml(candidate, league):
    if league == "futures_day":
        try:
            long_rsi = next(
                float(c["value"]) for c in candidate["entry"]["long"]["conditions"]
                if c.get("indicator") == "rsi"
            )
            short_rsi = next(
                float(c["value"]) for c in candidate["entry"]["short"]["conditions"]
                if c.get("indicator") == "rsi"
            )
            # REMOVED 2026-04-17: LOKI's rsi~29.56 poison rule was blocking the champion (rsi_long=29.33)
            if long_rsi >= short_rsi:
                return True, f"rsi_long({long_rsi}) >= rsi_short({short_rsi})"
        except (StopIteration, KeyError, TypeError):
            pass
    return False, ""

DAY_RANGES = {
    "take_profit_pct": (0.2, 1.0),
    "stop_loss_pct": (0.15, 0.5),
    "timeout_minutes": (20, 90),
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
FUTURES_DAY_RANGES = {
    "take_profit_pct": (0.8, 8.0),
    "stop_loss_pct":   (0.5, 4.5),
    "timeout_minutes": (30, 480),
    "size_pct":        (8, 20),
    "max_open":        (1, 4),
    "leverage":        (1.5, 3.0),
}
FUTURES_SWING_RANGES = {
    "take_profit_pct": (3.0, 10.0),
    "stop_loss_pct":   (1.5, 4.0),
    "timeout_hours":   (48, 192),
    "size_pct":        (10, 25),
    "max_open":        (1, 3),
    "leverage":        (1.5, 3.0),
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



def load_gemini_key(league):
    with open(GEMINI_SECRET) as f:
        data = json.load(f)
    return data.get(f"gemini_{league}_key") or data["gemini_api_key"]


def call_gemini(prompt, api_key, system_instruction=None, cached_content=None):
    url = f"{GEMINI_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 2000},
    }
    if cached_content:
        body["cachedContent"] = cached_content
    elif system_instruction:
        body["systemInstruction"] = {"parts": [{"text": system_instruction}]}
    payload = json.dumps(body).encode()
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
    elif league == "futures_day":
        return os.path.join(WORKSPACE, "fleet", "futures_day", "autobotdayfutures", "strategy.yaml")
    elif league == "futures_swing":
        return os.path.join(WORKSPACE, "fleet", "futures_swing", "autobotswingfutures", "strategy.yaml")
    return None


def get_ranges(league):
    if league == "futures_day":   return FUTURES_DAY_RANGES
    if league == "futures_swing": return FUTURES_SWING_RANGES
    return DAY_RANGES if league == "day" else SWING_RANGES


# F1 (meta_audit 2026-04-25): blend adj_score = 0.6 * backtest_sharpe + 0.4 * live_pnl_z.
def adj_score(sharpe, trades, target=50, league=None):
    base = sharpe
    if league is None or backtest_drift is None:
        return base
    try:
        z = float(backtest_drift.get_live_pnl_z(league))
    except Exception:
        z = 0.0
    return 0.6 * base + 0.4 * z


# ----------------------------------------------------------------
# Population management
# ----------------------------------------------------------------

class Population:
    def __init__(self, league):
        self.league = league
        self.elites = []  # list of (adj_score, strategy_dict, yaml_str)

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
                trades = strat.get("_trades", 30)  # default 30 for legacy files
                score = adj_score(sharpe, trades, league=self.league)
                self.elites.append((score, strat, text))
        self.elites.sort(key=lambda x: x[0], reverse=True)

    def save(self):
        d = pop_dir(self.league)
        for i, (score, strat, _) in enumerate(self.elites):
            # _sharpe and _trades already stored in strat by try_insert/seed_from
            path = os.path.join(d, f"elite_{i}.yaml")
            text = yaml.dump(strat, default_flow_style=False, sort_keys=False)
            with open(path, "w") as f:
                f.write(text)
            # Update tuple with fresh text
            self.elites[i] = (score, strat, text)
        # Remove any stale files beyond current population
        for i in range(len(self.elites), POPULATION_SIZE):
            path = os.path.join(d, f"elite_{i}.yaml")
            if os.path.exists(path):
                os.remove(path)

    def seed_from(self, strategy_dict, strategy_yaml, sharpe, trades=0):
        strategy_dict["_sharpe"] = sharpe
        strategy_dict["_trades"] = trades
        score = adj_score(sharpe, trades, league=self.league)
        self.elites = [(score, strategy_dict, strategy_yaml)]
        self.save()

    def best_sharpe(self):
        """Best RAW sharpe across all elites (Item 8 - not adj_score)."""
        if not self.elites:
            return 0.0
        return max(s.get("_sharpe", 0.0) for _, s, _ in self.elites)

    def worst_adj(self):
        return self.elites[-1][0] if self.elites else -999.0

    def try_insert(self, strategy_dict, strategy_yaml, sharpe, trades):
        """Returns (inserted, is_new_best). is_new_best uses raw Sharpe (Item 8)."""
        strategy_dict["_sharpe"] = sharpe
        strategy_dict["_trades"] = trades
        score = adj_score(sharpe, trades, league=self.league)
        entry = (score, strategy_dict, strategy_yaml)
        # Drift-aware gate: if backtest Sharpe has been historically overstating
        # live realised Sharpe for this league, a new champion must beat the
        # current best by more than just +0 to count. gate_bonus defaults to 0
        # when drift data is absent (cold-start or pre-first-sprint).
        gate = 0.0
        if backtest_drift is not None:
            try:
                gate = float(backtest_drift.get_gate_bonus(self.league))
            except Exception:
                gate = 0.0
        is_new_best = sharpe > (self.best_sharpe() + gate) if self.elites else True

        # F1 (meta_audit 2026-04-25): veto new_best when rolling 5-sprint live
        # PnL median < 0 (>=5 sprints required, brand-new champions skip veto).
        if is_new_best and backtest_drift is not None:
            try:
                if backtest_drift.get_veto_signal(self.league):
                    print(f"| VETO_NEW_BEST: 5sprint_median<0 league={self.league}")
                    is_new_best = False
            except Exception:
                pass

        # F4: reject clones — if a non-new-best candidate matches an existing
        # elite Sharpe within ELITE_SHARPE_EPS, do not add it. Keeps the
        # population from filling up with identical-Sharpe no-op perturbations.
        if not is_new_best and self.elites:
            for _, _e_strat, _ in self.elites:
                if abs(sharpe - float(_e_strat.get("_sharpe", 0.0))) < ELITE_SHARPE_EPS:
                    return False, False

        if len(self.elites) < POPULATION_SIZE:
            self.elites.append(entry)
            self.elites.sort(key=lambda x: x[0], reverse=True)
            self.save()
            # Sync best_strategy.yaml to current top elite after EVERY insertion,
            # not only on strict new_best. elites[0] can shift via adj_score
            # ranking without strict sharpe improvement; prior logic let the
            # deployed YAML drift out of sync with the live champion.
            self._save_fleet(self.elites[0][2])
            return True, is_new_best

        if score > self.worst_adj():
            self.elites[-1] = entry
            self.elites.sort(key=lambda x: x[0], reverse=True)
            self.save()
            self._save_fleet(self.elites[0][2])
            return True, is_new_best

        return False, False

    def _save_fleet(self, yaml_text):
        strat = yaml.safe_load(yaml_text)
        meta = {
            "sharpe":    float(strat.get("_sharpe", 0.0)),
            "trades":    int(strat.get("_trades", 0)),
            "saved_at":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        strat.pop("_sharpe", None)
        strat.pop("_trades", None)
        clean = yaml.dump(strat, default_flow_style=False, sort_keys=False)
        fleet = get_fleet_path(self.league)
        if fleet:
            os.makedirs(os.path.dirname(fleet), exist_ok=True)
            with open(fleet, "w") as f:
                f.write(clean)
        league_path = league_dir(self.league)
        with open(os.path.join(league_path, "best_strategy.yaml"), "w") as f:
            f.write(clean)
        # Sidecar for backtest-vs-live drift tracking — snapshotted into each
        # sprint's deployed_strategy.meta.json at sprint-start.
        with open(os.path.join(league_path, "best_strategy.meta.json"), "w") as f:
            import json as _json
            _json.dump(meta, f, indent=2)

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
        for i, (score, strat, _) in enumerate(self.elites):
            ex = strat.get("exit", {})
            ps = strat.get("position", {})
            tp = ex.get("take_profit_pct", "?")
            sl = ex.get("stop_loss_pct", "?")
            to = ex.get("timeout_minutes") or ex.get("timeout_hours", "?")
            to_u = "m" if "timeout_minutes" in ex else "h"
            nl = len(strat.get("entry", {}).get("long", {}).get("conditions", []))
            ns = len(strat.get("entry", {}).get("short", {}).get("conditions", []))
            np_ = len(strat.get("pairs", []))
            raw_sharpe = strat.get("_sharpe", 0.0)
            raw_trades = strat.get("_trades", 0)
            lines.append(
                f"  {i+1}. adj={score:.4f} sharpe={raw_sharpe:.4f} trades={raw_trades} | "
                f"TP={tp}% SL={sl}% TO={to}{to_u} | "
                f"size={ps.get('size_pct','?')}% max_open={ps.get('max_open','?')} | "
                f"{nl}L/{ns}S conds | {np_}p"
            )
        return "\n".join(lines)

# ----------------------------------------------------------------
# Mutations
# ----------------------------------------------------------------

def perturb(strategy, league):
    """Randomly tweak one numeric parameter."""
    s = copy.deepcopy(strategy)
    s.pop("_sharpe", None)
    s.pop("_trades", None)
    r = get_ranges(league)
    ex = s.setdefault("exit", {})
    ps = s.setdefault("position", {})

    params = []
    params.append(("tp", ex, "take_profit_pct", r["take_profit_pct"]))
    params.append(("sl", ex, "stop_loss_pct", r["stop_loss_pct"]))
    to_key = "timeout_minutes" if league in ("day", "futures_day") else "timeout_hours"
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
    s.pop("_trades", None)
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
    pairs = random.sample(get_pairs(league), n_pairs)

    tp = round(random.uniform(*r["take_profit_pct"]), 1)
    sl = round(random.uniform(*r["stop_loss_pct"]), 1)
    to_key = "timeout_minutes" if league in ("day", "futures_day") else "timeout_hours"
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
            "pause_if_down_pct": 5 if league in ("day", "futures_day") else 8,
            "stop_if_down_pct": 12 if league in ("day", "futures_day") else 18,
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


def load_program_md(league):
    path = os.path.join(league_dir(league), "program.md")
    if not os.path.exists(path):
        return ""
    with open(path) as f:
        return f.read().strip()


def build_llm_prompt(league, best_yaml, population):
    """Returns (system_instruction, user_message).

    The system_instruction is stable across gens for a given league + current
    MIMIR guidance and is cached via gemini_cache to reduce input-token cost.
    The user_message carries per-gen dynamic data (best_yaml, population,
    n_conds reminder).
    """
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

    system_parts = [
        f"You are a crypto {league} trading strategy optimizer."
          " Iterate on what works - do not explore random alternatives.\n\n",
        "## Constraints\n",
        f"{ranges_desc}\n",
        "Trade count HARD LIMITS: min 30, max 60 -- strategies outside this range are REJECTED.\n",
        "AIM for ~40-50 trades. Tighten conditions to reduce trade frequency.\n",
        "stop_loss_pct minimum: 0.8%% (noise floor).\n\n",
        # MIMIR guidance (program.md, updated every 100 gens by MIMIR)
        *(['## MIMIR Research Guidance\n',
          load_program_md(league) + '\n\n']
         if load_program_md(league) else []),
        "## Task\n",
        "You will be given a Current Best Strategy and an Elite Population.\n",
        "Make ONE small targeted modification to the current best strategy."
          " Output a complete modified copy.\n\n",
        "Allowed changes (pick exactly one):\n",
        "- Loosen a threshold to increase trade frequency"
          "  (e.g. RSI long from 30 to 40, or remove momentum_accelerating)\n",
        "- Tighten a threshold to improve signal quality\n",
        "- Adjust TP, SL (min 0.8%%), or timeout\n",
        "- Change a condition lookback period\n",
        "- Add or remove one pair\n\n",
        "Rules:\n",
        "- Do NOT restructure or replace the core framework - modify the given strategy only\n",
        "- If strategy has more than 5 conditions, prefer removing one over adding\n",
        "- momentum_accelerating is often overfitting - consider removing it if present\n",
        "- The current strategy likely generates TOO MANY trades. Tighten thresholds to REDUCE to <=60\n\n",
        "Output ONLY the complete modified strategy YAML between ```yaml and ``` markers.",
    ]
    system_instruction = "".join(system_parts)

    user_parts = [
        "## Current Best Strategy (ANCHOR - always start from this)\n",
        f"```yaml\n{best_yaml}```\n",
        f"This strategy has {n_conds} entry conditions: {cond_list}\n\n",
        "## Elite Population (context only - avoid duplicating)\n",
        f"{pop_summary}\n\n",
        f"Reminder: Do NOT exceed {n_conds + 1} total conditions.\n",
        "Output ONLY the complete modified strategy YAML between ```yaml and ``` markers.",
    ]
    user_message = "".join(user_parts)
    return system_instruction, user_message


def llm_mutate(best_yaml, league, population, api_key):
    system_instruction, user_message = build_llm_prompt(league, best_yaml, population)
    cache_name = None
    try:
        import gemini_cache
        cache_name = gemini_cache.get_cache_name(
            scope=f"odin_{league}",
            system_instruction=system_instruction,
            api_key=api_key,
        )
    except Exception:
        cache_name = None
    response = call_gemini(
        user_message, api_key,
        system_instruction=None if cache_name else system_instruction,
        cached_content=cache_name,
    )
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
        desc_clean = str(description).replace("\n", " ").replace("\r", " ").replace("\t", " ")[:200]
        f.write(f"{gen}\t{sharpe:.4f}\t{win_rate:.1f}\t{pnl_pct:.2f}\t"
                f"{trades}\t{status}\t{desc_clean}\t{ts}\n")


# ----------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league", choices=["day", "swing", "futures_day", "futures_swing"], required=True)
    parser.add_argument("--sleep", type=int, default=60)
    parser.add_argument("--seed", default=None, help="Seed strategy YAML path")
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()
    league = args.league

    sys.path.insert(0, RESEARCH)
    from odin_backtest import run_backtest, run_backtest_oos

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
        baseline = run_backtest(seed_strat, league, get_pairs(league))
        if "error" in baseline:
            print(f"  ERROR: {baseline['error']}")
            sys.exit(1)
        seed_sharpe = baseline["sharpe"]
        seed_trades = baseline["total_trades"]
        print(f"  Seed Sharpe={seed_sharpe:.4f} trades={seed_trades}")
        pop.seed_from(seed_strat, seed_yaml, seed_sharpe, seed_trades)

    # Load state
    results_history = load_results(league)
    state_path = os.path.join(league_dir(league), "gen_state.json")
    gen = len(results_history) + 1
    gens_since_best = 0
    last_mimir_gen = 0
    last_mimir_ts  = None
    diversity_injected_this_stall = False  # F3: one-shot per stall window
    if os.path.exists(state_path):
        try:
            with open(state_path) as f:
                gs = json.load(f)
            gen = gs.get("gen", gen)
            gens_since_best = gs.get("gens_since_best", 0)
            last_mimir_gen = gs.get("last_mimir_gen", 0)
            last_mimir_ts  = gs.get("last_mimir_ts")
            diversity_injected_this_stall = bool(gs.get("diversity_injected_this_stall", False))
        except Exception:
            pass

    min_t = SWING_MIN_TRADES if league == "swing" else MIN_TRADES.get(league, 30)  # Item 4

    print(f"[odin-v2/{league}] Pop: {len(pop.elites)} elites, best_adj={pop.best_sharpe():.4f}")
    print(f"  Gen {gen}, stall={gens_since_best}, sleep={args.sleep}s")
    print()

    consec_429 = 0
    seen_configs = set()  # Item 2: dedup cache

    while True:
        # ── Program halt check — Python-enforced, cannot be overridden by LLM ──────
        _prog = load_program_md(league)
        if "CRITICAL HALT — ACTIVE" in _prog:
            _ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
            print(f"[{_ts}] Gen {gen} | ODIN HALTED — program.md has active CRITICAL HALT — sleeping 60s", flush=True)
            time.sleep(60)
            continue

        # External diversity injection signal from odin_health_executor.
        # Written when gens_since_best exceeds the stall threshold.
        _signal_path = os.path.join(league_dir(league), "diversity_inject_signal")
        if os.path.exists(_signal_path):
            try:
                os.remove(_signal_path)
                diversity_injected_this_stall = False
                _sig_ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
                print(f"[{_sig_ts}] DIVERSITY_INJECT_SIGNAL: external trigger, re-arm F3", flush=True)
            except OSError:
                pass

        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        best_s = pop.best_sharpe()

        # F3 (meta_audit 2026-04-25): diversity injection on mode collapse.
        if pop.elites and not diversity_injected_this_stall:
            _u_sharpe = len({float(s.get("_sharpe", 0.0)) for _, s, _ in pop.elites})
            if _u_sharpe < DIVERSITY_UNIQUE_FLOOR or gens_since_best > DIVERSITY_STALL_FLOOR:
                _keep = pop.elites[:DIVERSITY_KEEP_TOP]
                _new_bottom = []
                for _i in range(POPULATION_SIZE - DIVERSITY_KEEP_TOP):
                    _rs, _ = random_strategy(league)
                    _rs["_sharpe"] = 0.0
                    _rs["_trades"] = 0
                    _ry = yaml.dump(_rs, default_flow_style=False, sort_keys=False)
                    _score = adj_score(0.0, 0, league=league)
                    _new_bottom.append((_score, _rs, _ry))
                pop.elites = _keep + _new_bottom
                pop.save()
                diversity_injected_this_stall = True
                print(f"[{ts}] DIVERSITY_INJECT: unique_sharpe={_u_sharpe} stall={gens_since_best} replaced bottom {POPULATION_SIZE - DIVERSITY_KEEP_TOP}")

        # Adaptive weights
        if gens_since_best < 100:
            weights = {"llm": 0.50, "perturb": 0.35, "crossover": 0.10, "random": 0.05}
        elif gens_since_best < 300:
            weights = {"llm": 0.45, "perturb": 0.35, "crossover": 0.10, "random": 0.10}
        else:
            weights = {"llm": 0.40, "perturb": 0.45, "crossover": 0.05, "random": 0.10}

        # Plateau override: if last N LLM attempts yielded <10% pop-hits,
        # cut llm weight and redirect the delta to local perturb (free).
        if _llm_plateau():
            llm_cut = weights["llm"] - LLM_PLATEAU_WEIGHT
            weights["llm"] = LLM_PLATEAU_WEIGHT
            weights["perturb"] = weights.get("perturb", 0) + llm_cut

        # Select mutation
        r = random.random()
        cum = 0
        mutation_type = "llm"
        for mt, w in weights.items():
            cum += w
            if r <= cum:
                mutation_type = mt
                break

        description = mutation_type

        # F4: periodic forced-random injection to escape hill-climb stalls.
        # Set description before the unconditional assignment below was
        # clobbering it — label preserved so meta_audit can grep fires.
        if (gens_since_best >= FORCE_RANDOM_FLOOR
                and (gens_since_best - FORCE_RANDOM_FLOOR) % FORCE_RANDOM_EVERY == 0):
            mutation_type = "random"
            description = "forced_random_diversity"

        print(f"[{ts}] Gen {gen} | best={best_s:.4f} | stall={gens_since_best} | {mutation_type}",
              end=" ", flush=True)

        candidate = None
        candidate_yaml = None

        # F5: pre-Gemini prompt-hash dedup. If the prompt we are about to
        # send matches LLM_DEDUP_THRESHOLD recent calls, skip Gemini and
        # substitute a free perturb. The hash is computed from the exact
        # (system_instruction, user_message) build_llm_prompt would produce.
        if mutation_type == "llm":
            _, _dd_best_strat, _ = pop.elites[0]
            _dd_clean = copy.deepcopy(_dd_best_strat)
            _dd_clean.pop("_sharpe", None)
            _dd_clean.pop("_trades", None)
            _dd_best_yaml = yaml.dump(_dd_clean, default_flow_style=False, sort_keys=False)
            _dd_sys, _dd_user = build_llm_prompt(league, _dd_best_yaml, pop)
            _dd_fp = _llm_prompt_fingerprint(_dd_sys, _dd_user)
            _dd_count = _llm_prompt_hashes.count(_dd_fp)
            if _dd_count >= LLM_DEDUP_THRESHOLD:
                log_result(league, gen, {}, "llm_dedup_skip",
                           f"fp={_dd_fp[:8]} seen={_dd_count}")
                mutation_type = "perturb"
                description = "llm_dedup_perturb"
            else:
                _llm_prompt_hashes.append(_dd_fp)

        if mutation_type == "llm":
            _, best_strat, _ = pop.elites[0]
            clean = copy.deepcopy(best_strat)
            clean.pop("_sharpe", None)
            clean.pop("_trades", None)
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
            log_result(league, gen, {}, "no_candidate", f"mutation_type={mutation_type}")
            gen += 1
            time.sleep(args.sleep)
            continue

        # Item 7: pairs whitelist for swing (after candidate is generated)
        if league == "swing":
            _bad_pairs = set(candidate.get("pairs", [])) - SWING_ALLOWED_PAIRS
            if _bad_pairs:
                candidate["pairs"] = [p for p in candidate.get("pairs", []) if p in SWING_ALLOWED_PAIRS] or ["BTC/USD", "ETH/USD", "SOL/USD"]
                import yaml as _yaml2
                candidate_yaml = _yaml2.dump(candidate, default_flow_style=False, sort_keys=False)

        # Kraken Derivatives US constraints: pairs whitelist + per-strategy leverage cap
        if league in ("futures_day", "futures_swing"):
            _bad_pairs = set(candidate.get("pairs", [])) - FUTURES_ALLOWED_PAIRS
            if _bad_pairs:
                print(f"  [universe] {league} gen {gen}: dropping untradable pairs {sorted(_bad_pairs)} (Kraken Derivatives US = BTC/ETH/SOL only)")
                candidate["pairs"] = [p for p in candidate.get("pairs", []) if p in FUTURES_ALLOWED_PAIRS] or ["BTC/USD", "ETH/USD", "SOL/USD"]
            _cap = kraken_leverage.cap_for_strategy(candidate.get("pairs", []))
            if float(candidate.get("leverage", 1.0)) > _cap:
                candidate["leverage"] = _cap
            # Belt-and-suspenders assertion: candidate that reaches backtest must be a subset of tradable.
            assert set(candidate.get("pairs", [])).issubset(FUTURES_ALLOWED_PAIRS), \
                f"pairs whitelist post-filter produced non-tradable pair: {candidate.get('pairs')}"
            import yaml as _yaml2
            candidate_yaml = _yaml2.dump(candidate, default_flow_style=False, sort_keys=False)

        # Canonical dedup — hash structure (sort_keys) so whitespace/key-order doesn't evade
        _canon = yaml.dump(candidate, default_flow_style=False, sort_keys=True)
        _h = hashlib.md5(_canon.encode()).hexdigest()
        if _h in seen_configs:
            print(f"| [DEDUP_REJECT]")
            log_result(league, gen, {}, "dedup_reject", "duplicate config")
            gen += 1
            gens_since_best += 1  # 2026-04-23: count dedup rejects toward stall so FORCE_RANDOM/MIMIR machinery activates
            with open(state_path, "w") as f:
                json.dump({"gen": gen, "gens_since_best": gens_since_best, "last_mimir_gen": last_mimir_gen, "last_mimir_ts": last_mimir_ts, "diversity_injected_this_stall": diversity_injected_this_stall}, f)
            time.sleep(args.sleep)
            continue
        seen_configs.add(_h)

        # Pre-backtest poison check
        _poison, _poison_reason = is_poison_yaml(candidate, league)
        if _poison:
            print(f"| POISON_YAML: {_poison_reason}")
            log_result(league, gen, {}, "poison_reject", _poison_reason[:80])
            gen += 1
            with open(state_path, "w") as f:
                json.dump({"gen": gen, "gens_since_best": gens_since_best, "last_mimir_gen": last_mimir_gen, "last_mimir_ts": last_mimir_ts, "diversity_injected_this_stall": diversity_injected_this_stall}, f)
            time.sleep(args.sleep)
            continue

        # Backtest
        try:
            result = run_backtest(candidate, league, get_pairs(league))
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
        _fp = POISON_RESULT_FINGERPRINTS.get(league, set())
        if _fp and round(sharpe, 4) in _fp:
            print(f"| POISON_FP: sharpe={sharpe:.4f} matches known attractor")
            log_result(league, gen, result, "poison_reject", f"attractor sharpe={sharpe:.4f}")
            gen += 1
            with open(state_path, "w") as f:
                json.dump({"gen": gen, "gens_since_best": gens_since_best, "last_mimir_gen": last_mimir_gen, "last_mimir_ts": last_mimir_ts, "diversity_injected_this_stall": diversity_injected_this_stall}, f)
            time.sleep(args.sleep)
            continue

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
            gens_since_best += 1  # 2026-04-23: count low_trades rejects toward stall so FORCE_RANDOM/MIMIR machinery activates
            with open(state_path, "w") as f:
                json.dump({"gen": gen, "gens_since_best": gens_since_best, "last_mimir_gen": last_mimir_gen, "last_mimir_ts": last_mimir_ts, "diversity_injected_this_stall": diversity_injected_this_stall}, f)
            time.sleep(args.sleep)
            continue

        # Item 3: MAX_TRADES for swing
        if league == "swing" and trades > SWING_MAX_TRADES:
            print(f"| [MAX_TRADES_REJECT trades={trades}]")
            log_result(league, gen, {}, "max_trades_reject", f"trades={trades}>{SWING_MAX_TRADES}")
            gen += 1
            time.sleep(args.sleep)
            continue
        # MIMIR gen 11679: cap day trades to block structural failures (1000+ trade blowouts)
        if league == "day" and trades > 450:
            print(f"| [MAX_TRADES_REJECT trades={trades}]")
            log_result(league, gen, {}, "max_trades_reject", f"trades={trades}>450")
            gen += 1
            time.sleep(args.sleep)
            continue
        # OOS overfit gate: if candidate beats current best (raw, ignoring drift
        # bonus), validate on held-out last 6mo. Reject if OOS sharpe goes
        # negative or underperforms the champion's OOS. Keeps in-sample hill
        # climbing from promoting overfit configs that don't generalise.
        # Cost: ~1 extra backtest on ~5-15% of gens (only improvement candidates).
        if pop.elites and sharpe > pop.best_sharpe():
            oos_result = run_backtest_oos(candidate, league, get_pairs(league))
            if "error" in oos_result:
                print(f"| OOS_GATE_ERROR: {oos_result['error']}")
                log_result(league, gen, result, "oos_error", oos_result["error"])
                gen += 1
                time.sleep(args.sleep)
                continue
            oos_sharpe    = float(oos_result.get("sharpe", -999.0))
            oos_trades    = int(oos_result.get("total_trades", 0))
            champion_oos  = float(pop.elites[0][1].get("_oos_sharpe", 0.0)) if pop.elites else 0.0
            min_oos_trades = max(1, min_t // 4)
            # F8 (meta_audit 2026-04-25): regime-shift reset — frozen population
            # (gens_since_best > 1500 AND only 1 unique sharpe across elites)
            # collapses champion_oos to 0.0 so the hard floor governs alone.
            _unique_sharpe = len({float(s.get("_sharpe", 0.0)) for _, s, _ in pop.elites}) if pop.elites else 0
            if gens_since_best > 1500 and _unique_sharpe == 1:
                print(f"| OOS_ANCHOR_RESET: gens_since_best={gens_since_best} unique_sharpe=1 prev_champ_oos={champion_oos:.4f} -> 0.0")
                champion_oos = 0.0
            # F8: OOS hard floor (0.0) — candidates must clear max(floor, champion).
            oos_bar = max(OOS_HARD_FLOOR, champion_oos)
            oos_ok = (
                oos_sharpe >= oos_bar
                and oos_trades >= min_oos_trades
            )
            if not oos_ok:
                print(f"| OOS_GATE_REJECT: oos_sharpe={oos_sharpe:.4f} "
                      f"oos_trades={oos_trades} champion_oos={champion_oos:.4f} bar={oos_bar:.4f}")
                log_result(league, gen, result, "oos_reject",
                           f"oos_sharpe={oos_sharpe:.4f} oos_trades={oos_trades} champion_oos={champion_oos:.4f} bar={oos_bar:.4f}")
                gen += 1
                time.sleep(args.sleep)
                continue
            candidate["_oos_sharpe"] = round(oos_sharpe, 4)
            candidate["_oos_trades"] = oos_trades

            # F10: horizon-matched 24h-median Sharpe gate (day leagues only).
            # Fires alongside the OOS gate on improvement candidates: a new
            # champion must hold >= 80% of the current champion's typical 24h
            # Sharpe. Prevents promotions that beat 2yr but degrade the
            # sprint-horizon metric. Swing leagues skip (24h window mismatch).
            if league in DAY_24H_GATE_LEAGUES:
                cand_24h  = float(result.get("sharpe_24h_median", 0.0))
                champ_24h = float(pop.elites[0][1].get("_sharpe_24h_median", 0.0)) if pop.elites else 0.0
                floor_24h = champ_24h * DAY_24H_GATE_FLOOR_FRAC  # no max(0.0,...): for negative champ, floor is less-negative (allows improvement; max was blocking all -ve candidates)
                if cand_24h < floor_24h:
                    print(f"| H24_GATE_REJECT: sharpe_24h_median={cand_24h:.4f} "
                          f"floor={floor_24h:.4f} champ={champ_24h:.4f}")
                    log_result(league, gen, result, "h24_reject",
                               f"cand_24h={cand_24h:.4f} champ_24h={champ_24h:.4f} floor={floor_24h:.4f}")
                    gen += 1
                    gens_since_best += 1  # count h24 rejects toward stall (FORCE_RANDOM/MIMIR activation)
                    time.sleep(args.sleep)
                    continue
                candidate["_sharpe_24h_median"] = round(cand_24h, 4)

            import yaml as _yaml3
            candidate_yaml = _yaml3.dump(candidate, default_flow_style=False, sort_keys=False)

        # Population insertion
        inserted, is_new_best = pop.try_insert(candidate, candidate_yaml, sharpe, trades)

        if is_new_best:
            status = "new_best"
            gens_since_best = 0
            diversity_injected_this_stall = False  # F3: clear flag for next stall window
            score = adj_score(sharpe, trades, league=league)
            print(f"| *** NEW BEST: adj={score:.4f} sharpe={sharpe:.4f} win={win_rate}% "
                  f"pnl={pnl_pct:+.2f}% trades={trades} ***")
        elif inserted:
            status = "new_elite"
            gens_since_best += 1
            print(f"| sharpe={sharpe:.4f} [new_elite]")
        else:
            status = "discarded"
            gens_since_best += 1
            print(f"| sharpe={sharpe:.4f} win={win_rate}% trades={trades} [disc]")

        if mutation_type == "llm":
            _llm_history.append(inserted)


        log_result(league, gen, result, status, description[:80])
        results_history.append({
            "gen": str(gen), "sharpe": f"{sharpe:.4f}",
            "win_rate": f"{win_rate:.1f}", "pnl_pct": f"{pnl_pct:.2f}",
            "trades": str(trades), "status": status,
        })
        if len(results_history) > 300:
            results_history = results_history[-300:]

        # Mimir milestone: deep analysis every 200 gens on active leagues
        # (baseline cadence) or immediately after a breakthrough (min 100
        # gens since last Mimir). Structural-failure storm: 3+ of last 10
        # had trades>450 — fire early (requires 50+ gens since last MIMIR
        # to avoid spam on a single cluster). Wall-clock cooldown
        # (MIMIR_MIN_GAP_HRS) caps per-league Claude spend.
        #
        # F12 (meta_audit): on stalled leagues (gens_since_best >=
        # MIMIR_STALL_FLOOR) stretch the baseline cadence from 200 to
        # MIMIR_STALL_GAP_GENS — Sonnet has nothing new to analyze on a
        # frozen population, so most milestone fires are waste. Breakthrough
        # and structural-storm branches still trigger immediately because
        # those ARE new information.
        last_10_trades = [int(r.get('trades', '0')) for r in results_history[-10:] if str(r.get('trades', '0')).isdigit()]
        structural_storm = sum(1 for t in last_10_trades if t > 450) >= 3
        _mimir_stalled   = gens_since_best >= MIMIR_STALL_FLOOR
        _mimir_throttled = _is_anthropic_throttled()
        _baseline_gap    = MIMIR_STALL_GAP_GENS if _mimir_stalled else (500 if _mimir_throttled else 200)
        trigger_mimir = (
            ((gen - last_mimir_gen) >= _baseline_gap)
            or (is_new_best and (gen - last_mimir_gen) >= 100)
            or (structural_storm and (gen - last_mimir_gen) >= 50)
        )
        if trigger_mimir:
            now_utc = datetime.now(timezone.utc)
            gap_ok  = True
            if last_mimir_ts:
                try:
                    last_dt = datetime.fromisoformat(last_mimir_ts).replace(tzinfo=timezone.utc)
                    gap_hrs = (now_utc - last_dt).total_seconds() / 3600
                    if gap_hrs < MIMIR_MIN_GAP_HRS:
                        gap_ok = False
                        print(f"  [mimir] Gen {gen} skipped: cooldown {gap_hrs:.1f}/{MIMIR_MIN_GAP_HRS}h")
                except Exception:
                    pass
            if gap_ok:
                last_mimir_gen = gen
                last_mimir_ts  = now_utc.strftime("%Y-%m-%dT%H:%M")
                if is_new_best and (gen - last_mimir_gen) >= 100:
                    reason = "breakthrough"
                elif structural_storm:
                    reason = "structural_storm"
                elif _mimir_stalled:
                    reason = "stalled_milestone"
                else:
                    reason = "milestone"
                print(f"  [mimir] Gen {gen} {reason} — launching deep analysis...")
                try:
                    subprocess.Popen(
                        ["python3", os.path.join(RESEARCH, "mimir.py"),
                         "--league", league, "--generation", str(gen)],
                        stdout=open(os.path.join(league_dir(league), "mimir.log"), "a"),
                        stderr=subprocess.STDOUT,
                    )
                except Exception as e:
                    print(f"  [mimir] Failed to launch: {e}")

        gen += 1
        with open(state_path, "w") as f:
            json.dump({"gen": gen, "gens_since_best": gens_since_best, "last_mimir_gen": last_mimir_gen, "last_mimir_ts": last_mimir_ts, "diversity_injected_this_stall": diversity_injected_this_stall}, f)
        time.sleep(args.sleep)


if __name__ == "__main__":
    import sys as _sys; _sys.path.insert(0, '/root/.openclaw/workspace')
    try:
        from config_loader import config as _cfg
        if getattr(_cfg, "mode", "full") != "full":
            print("[odin-v2] mode=lite -- exiting (AI research disabled)", flush=True); _sys.exit(0)
    except Exception:
        pass
    main()
