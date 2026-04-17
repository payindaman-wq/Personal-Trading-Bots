#!/usr/bin/env python3
"""
freya_researcher.py - FREYA prediction markets strategy optimizer.

Simulates strategy configurations against 300k+ historical resolved prediction
market records, using Gemini Flash Lite to propose mutations. Triggers Mimir
at every 100-generation milestone for deep analysis.

Usage:
  python3 freya_researcher.py [--sleep 60]
"""
import argparse
import copy
import json
import math
import os
import random
import re
import subprocess
import time
import urllib.request
from datetime import datetime, timezone

import yaml

WORKSPACE       = "/root/.openclaw/workspace"
RESEARCH        = os.path.join(WORKSPACE, "research")
PM_RESEARCH     = os.path.join(RESEARCH, "pm")
PM_DATA         = os.path.join(RESEARCH, "polymarket", "resolved_markets.jsonl")

GEMINI_SECRET   = "/root/.openclaw/secrets/gemini.json"
GEMINI_MODEL    = "gemini-2.5-flash-lite"
GEMINI_BASE     = "https://generativelanguage.googleapis.com/v1beta/models"

MIMIR_SCRIPT    = os.path.join(RESEARCH, "mimir.py")
RESULTS_TSV     = os.path.join(PM_RESEARCH, "results.tsv")
GEN_STATE       = os.path.join(PM_RESEARCH, "gen_state.json")
BEST_STRATEGY   = os.path.join(PM_RESEARCH, "best_strategy.yaml")
PROGRAM_MD      = os.path.join(PM_RESEARCH, "program.md")
POPULATION_DIR  = os.path.join(PM_RESEARCH, "population")
RESEARCHER_LOG  = os.path.join(PM_RESEARCH, "researcher.log")

POPULATION_SIZE   = 5
MIMIR_INTERVAL    = 200
MIMIR_MIN_GAP_HRS = 6   # min wall-clock hours between Mimir calls
SUSPICIOUS_SHARPE = 8.0
MIN_BETS          = 20
# Kalshi taker fee: 2.5% of potential profit per contract
# (e.g. YES at 50c -> $0.0125/contract; low-prob contracts carry heavy fees)
KALSHI_FEE_PROFIT_PCT   = 0.025
KALSHI_MAX_FEE_CONTRACT = 0.07   # cap, not binding in practice at normal odds

# ── PERMANENT KALSHI CONSTRAINTS (do not remove or relax) ────────────────────
# These reflect hard limitations of Kalshi's public API and sprint structure.
# See sanitize_candidate() — enforced on every Gemini mutation.
#   - No sports: Kalshi public endpoint carries no sports markets
#   - max_days_to_resolve <= 7: sprint window is 7 days; longer = locked capital
#   - price_range [0.10, 0.90]: Kalshi fee (2.5% of profit/contract) is brutal
#     at low probabilities — e.g. YES at 0.10 costs 22.5% of position in fees
# ─────────────────────────────────────────────────────────────────────────────
# Sports excluded: Kalshi public API does not serve sports markets
CATEGORIES = ["politics", "crypto", "economics", "world_events"]


def log(msg):
    ts   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)




def load_gemini_key():
    with open(GEMINI_SECRET) as f:
        data = json.load(f)
    keys = data.get("gemini_api_keys") or [data.get("gemini_api_key")]
    keys = [k for k in keys if k]
    return random.choice(keys) if keys else None


def call_gemini(prompt, api_key):
    url = f"{GEMINI_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents":         [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 1200},
    }).encode()
    req = urllib.request.Request(url, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def load_resolved_markets():
    """Load resolved markets filtered to usable records (valid odds 0.03-0.97)."""
    markets = []
    skipped = 0
    with open(PM_DATA) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                m    = json.loads(line)
                odds = m.get("odds_close")
                if odds is None or not (0.03 <= float(odds) <= 0.97):
                    skipped += 1
                    continue
                if float(m.get("volume_usd", 0) or 0) < 50:
                    skipped += 1
                    continue
                if m.get("resolution") not in ("yes", "no"):
                    skipped += 1
                    continue
                markets.append(m)
            except Exception:
                skipped += 1
    log(f"Loaded {len(markets)} usable markets (skipped {skipped})")
    return markets


def compute_base_rates(markets):
    by_cat = {}
    for m in markets:
        cat = m.get("category", "world_events")
        if cat not in by_cat:
            by_cat[cat] = {"yes": 0, "total": 0}
        by_cat[cat]["total"] += 1
        if m.get("resolution") == "yes":
            by_cat[cat]["yes"] += 1
    rates = {cat: v["yes"] / v["total"]
             for cat, v in by_cat.items() if v["total"] >= 10}
    log("Base rates: " + ", ".join(f"{c}={r:.3f}" for c, r in sorted(rates.items())))
    return rates


def simulate_strategy(strategy, markets, base_rates):
    """
    Evaluate strategy against resolved markets.
    Bet when market price deviates from category base rate by more than min_edge_pts.
    """
    cat      = strategy.get("category", "")
    inc_kw   = [k.lower() for k in strategy.get("include_keywords", [])]
    exc_kw   = [k.lower() for k in strategy.get("exclude_keywords", [])]
    pr       = strategy.get("price_range", [0.05, 0.95])
    min_liq  = float(strategy.get("min_liquidity_usd", 500))
    min_edge = float(strategy.get("min_edge_pts", 0.08))
    pos_pct  = float(strategy.get("max_position_pct", 0.10))
    bet_size = 1000.0 * pos_pct

    base_rate = base_rates.get(cat, 0.50) if cat else 0.50
    pr_lo, pr_hi = float(pr[0]), float(pr[1])

    pnl = []
    for m in markets:
        if cat and m.get("category") != cat:
            continue
        q = m.get("question", "").lower()
        if inc_kw and not any(kw in q for kw in inc_kw):
            continue
        if exc_kw and any(kw in q for kw in exc_kw):
            continue
        odds = float(m.get("odds_close", 0))
        if not (pr_lo <= odds <= pr_hi):
            continue
        if float(m.get("volume_usd", 0) or 0) < min_liq:
            continue

        edge_no  = odds - base_rate   # positive -> market overprices YES -> bet NO
        edge_yes = base_rate - odds   # positive -> market underprices YES -> bet YES

        if edge_no >= min_edge:
            bet      = "no"
            bet_odds = 1.0 - odds
        elif edge_yes >= min_edge:
            bet      = "yes"
            bet_odds = odds
        else:
            continue

        if bet_odds < 0.05:  # Kalshi floor: avoid extreme-odds contracts
            continue

        # Kalshi fee: 2.5% of potential profit per contract
        # profit_per_contract = 1 - bet_odds (each contract pays $1 at resolution)
        n_contracts = bet_size / bet_odds
        profit_per_contract = 1.0 - bet_odds
        fee_per_contract = min(KALSHI_FEE_PROFIT_PCT * profit_per_contract,
                               KALSHI_MAX_FEE_CONTRACT)
        fee = fee_per_contract * n_contracts
        res = m.get("resolution")
        if (bet == "yes" and res == "yes") or (bet == "no" and res == "no"):
            pnl.append(bet_size * (1.0 / bet_odds - 1.0) - fee)
        else:
            pnl.append(-bet_size - fee)

    n = len(pnl)
    if n < MIN_BETS:
        return {"roi_pct": 0.0, "win_rate": 0.0, "n_bets": n,
                "sharpe": 0.0, "adj_score": -1.0}

    total_invested = bet_size * n
    total_pnl      = sum(pnl)
    roi_pct        = total_pnl / total_invested * 100
    wins           = sum(1 for p in pnl if p > 0)
    win_rate       = wins / n * 100
    mean           = total_pnl / n
    variance       = sum((p - mean) ** 2 for p in pnl) / max(n - 1, 1)
    std            = variance ** 0.5
    sharpe         = mean / std if std > 0 else 0.0
    adj_score      = sharpe * math.log(n / MIN_BETS + 1)

    return {
        "roi_pct":   round(roi_pct, 3),
        "win_rate":  round(win_rate, 2),
        "n_bets":    n,
        "sharpe":    round(sharpe, 4),
        "adj_score": round(adj_score, 4),
    }




def sanitize_candidate(candidate, best):
    """
    PERMANENT KALSHI CONSTRAINTS — do not remove or relax these.
    Enforces hard limits on every Gemini-generated strategy candidate
    so constraint violations in LLM output are silently corrected.

    Constraints (set 2026-04-13, permanent):
      - category:           must be in CATEGORIES (no sports — Kalshi public API has none)
      - max_days_to_resolve: must be <= 7 (sprint window; longer ties up capital)
      - price_range:        min >= 0.10, max <= 0.90 (fee-efficiency on Kalshi)
      - min_edge_pts:       must be >= 0.04 (avoid fee-crushed near-zero-edge trades)
    """
    # Category
    if candidate.get("category") not in CATEGORIES:
        candidate["category"] = best.get("category", CATEGORIES[0])

    # Sprint window cap
    if candidate.get("max_days_to_resolve", 7) > 7:
        candidate["max_days_to_resolve"] = 7

    # Price range fee-efficiency bounds
    pr = candidate.get("price_range", [0.10, 0.90])
    if not isinstance(pr, list) or len(pr) != 2:
        pr = [0.10, 0.90]
    pr[0] = max(float(pr[0]), 0.10)
    pr[1] = min(float(pr[1]), 0.90)
    candidate["price_range"] = pr

    # Edge floor
    if candidate.get("min_edge_pts", 0.04) < 0.04:
        candidate["min_edge_pts"] = 0.04

    return candidate


def load_strategy(path):
    with open(path) as f:
        return yaml.safe_load(f)


def save_strategy(s, path):
    with open(path, "w") as f:
        yaml.dump(s, f, default_flow_style=False, allow_unicode=True)


DEFAULT_STRATEGY = {
    "name":                "pm_research_best",
    "category":            "politics",
    "include_keywords":    [],
    "exclude_keywords":    [],
    "price_range":         [0.10, 0.90],
    "min_liquidity_usd":   500,
    "max_days_to_resolve": 7,    # hard cap: must close within sprint window
    "min_edge_pts":        0.06,
    "max_position_pct":    0.10,
}


def load_population():
    pop = []
    for i in range(POPULATION_SIZE):
        path = os.path.join(POPULATION_DIR, f"elite_{i}.yaml")
        if os.path.exists(path):
            try:
                pop.append(load_strategy(path))
            except Exception:
                pass
    return pop


def save_population(pop):
    os.makedirs(POPULATION_DIR, exist_ok=True)
    for i, s in enumerate(pop[:POPULATION_SIZE]):
        save_strategy(s, os.path.join(POPULATION_DIR, f"elite_{i}.yaml"))


def update_population(pop, candidate, score):
    candidate = copy.deepcopy(candidate)
    candidate["_adj_score"] = score
    if len(pop) < POPULATION_SIZE:
        pop.append(candidate)
        save_population(pop)
        return pop, True
    scores = [(s.get("_adj_score", -999), i) for i, s in enumerate(pop)]
    worst_score, worst_idx = min(scores)
    if score > worst_score:
        pop[worst_idx] = candidate
        save_population(pop)
        return pop, True
    return pop, False


def load_gen_state():
    if os.path.exists(GEN_STATE):
        try:
            return json.load(open(GEN_STATE))
        except Exception:
            pass
    return {"gen": 0, "gens_since_best": 0}


def save_gen_state(state):
    with open(GEN_STATE, "w") as f:
        json.dump(state, f)


def init_results_tsv():
    if not os.path.exists(RESULTS_TSV):
        with open(RESULTS_TSV, "w") as f:
            f.write("gen\tsharpe\twin_rate\troi_pct\tn_bets\tadj_score\tstatus\tdescription\tts\n")


def append_result(gen, m, status, desc):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
    with open(RESULTS_TSV, "a") as f:
        f.write(
            f"{gen}\t{m['sharpe']}\t{m['win_rate']}\t{m['roi_pct']}\t"
            f"{m['n_bets']}\t{m['adj_score']}\t{status}\t{desc}\t{ts}\n"
        )


def mutate_llm(best, metrics, program_md, api_key):
    strategy_yaml = yaml.dump(best, default_flow_style=False, allow_unicode=True)
    prog = f"\n## Research Program\n{program_md}" if program_md.strip() else ""

    prompt = (
        "You are FREYA, a prediction markets strategy optimizer for KALSHI "
        "(CFTC-regulated US exchange - no sports, politics/crypto/economics/world_events only).\n\n"
        "HOW THE SIMULATOR WORKS:\n"
        "- Filters 300k+ historical resolved Kalshi/Polymarket markets\n"
        "- Kalshi carries: politics, crypto, economics, world_events (NO sports)\n"
        "- Category YES resolution rates: politics=29.1%, crypto=31.5%, "
        "economics=26.0%, world_events=12.0%\n"
        "- KALSHI FEE: 2.5%% of potential profit per contract; low-prob bets "
        "near 0.05-0.15 carry outsized fee drag so avoid them\n"
        "- Keep price_range min>=0.10 and max<=0.90 to stay fee-efficient\n"
        "- Bet direction: market_odds > base_rate + min_edge_pts -> bet NO; "
        "market_odds < base_rate - min_edge_pts -> bet YES\n"
        "- adj_score = sharpe x log(n_bets/20 + 1), needs >=20 bets\n\n"
        f"CURRENT BEST (adj={metrics['adj_score']:.4f}, sharpe={metrics['sharpe']:.4f}, "
        f"roi={metrics['roi_pct']:.1f}%, win={metrics['win_rate']:.1f}%, n={metrics['n_bets']}):\n"
        "```yaml\n" + strategy_yaml + "```" + prog + "\n\n"
        "MUTABLE PARAMETERS:\n"
        "- category: [politics, crypto, economics, world_events] (no sports on Kalshi)\n"
        "- include_keywords: lowercase strings matching Kalshi market titles\n"
        "- exclude_keywords: strings to exclude\n"
        "- price_range: [min>=0.10, max<=0.90] to stay Kalshi fee-efficient\n"
        "- min_liquidity_usd: 100-10000\n"
        "- max_days_to_resolve: 3-7 (hard cap = sprint window; longer locks up capital)\n"
        "- min_edge_pts: 0.04-0.25\n"
        "- max_position_pct: 0.02-0.20\n\n"
        "Propose exactly ONE change to maximize adj_score.\n"
        "Output ONLY the updated strategy YAML, no explanation, no fences."
    )

    try:
        response = call_gemini(prompt, api_key)
        response = re.sub(r"^```(?:yaml)?\s*", "", response, flags=re.MULTILINE)
        response = re.sub(r"\s*```\s*$", "", response, flags=re.MULTILINE)
        candidate = yaml.safe_load(response)
        if not isinstance(candidate, dict):
            return None, "llm_parse_error"
        candidate["name"] = best.get("name", "pm_research_best")
        return candidate, "llm"
    except Exception as e:
        return None, f"llm_error:{str(e)[:60]}"


def mutate_perturbation(best):
    s = copy.deepcopy(best)
    choice = random.choice([
        "min_edge_pts", "price_range_min", "price_range_max",
        "min_liquidity_usd", "max_position_pct", "max_days_to_resolve",
    ])
    if choice == "min_edge_pts":
        s["min_edge_pts"] = round(random.uniform(0.03, 0.25), 3)
    elif choice == "price_range_min":
        s["price_range"] = [round(random.uniform(0.03, 0.20), 2), s["price_range"][1]]
    elif choice == "price_range_max":
        s["price_range"] = [s["price_range"][0], round(random.uniform(0.80, 0.97), 2)]
    elif choice == "min_liquidity_usd":
        s["min_liquidity_usd"] = random.choice([100, 200, 500, 1000, 2000, 5000])
    elif choice == "max_position_pct":
        s["max_position_pct"] = round(random.uniform(0.02, 0.20), 3)
    elif choice == "max_days_to_resolve":
        s["max_days_to_resolve"] = random.choice([3, 5, 7])  # sprint window cap
    return s, f"perturb:{choice}"


def mutate_crossover(population):
    if len(population) < 2:
        return None, "crossover_skip"
    a, b = random.sample(population, 2)
    s = copy.deepcopy(a)
    for key in ["category", "include_keywords", "exclude_keywords", "price_range",
                "min_liquidity_usd", "max_days_to_resolve", "min_edge_pts", "max_position_pct"]:
        if random.random() < 0.40 and key in b:
            s[key] = copy.deepcopy(b[key])
    return s, "crossover"


# Sports removed: Kalshi public API does not carry sports markets
KW_POOL = {
    "politics":     ["election", "president", "senate", "congress", "vote",
                     "party", "candidate", "primary", "governor", "house",
                     "republican", "democrat", "approval", "tariff", "policy"],
    "crypto":       ["bitcoin", "btc", "ethereum", "eth", "solana", "sol",
                     "xrp", "crypto", "price", "above", "below"],
    "economics":    ["cpi", "nfp", "gdp", "inflation", "fed", "interest rate",
                     "unemployment", "recession", "rate hike", "rate cut",
                     "jobs report", "fomc", "powell"],
    "world_events": ["ceasefire", "treaty", "war", "sanction", "trade deal",
                     "agreement", "summit", "nato", "announce", "approve"],
}


def mutate_random_restart():
    cat    = random.choice(CATEGORIES)
    pool   = KW_POOL.get(cat, [])
    inc_kw = random.sample(pool, min(random.randint(0, 3), len(pool)))
    s = {
        "name":                "pm_research_best",
        "category":            cat,
        "include_keywords":    inc_kw,
        "exclude_keywords":    [],
        "price_range":         [round(random.uniform(0.03, 0.15), 2),
                                round(random.uniform(0.85, 0.97), 2)],
        "min_liquidity_usd":   random.choice([100, 200, 500, 1000, 2000]),
        "max_days_to_resolve": random.choice([3, 5, 7]),  # sprint window cap
        "min_edge_pts":        round(random.uniform(0.03, 0.20), 3),
        "max_position_pct":    round(random.uniform(0.05, 0.15), 3),
    }
    return s, "random_restart"


def trigger_mimir(generation):
    log(f"  Triggering Mimir (pm gen {generation})...")
    try:
        result = subprocess.run(
            ["python3", MIMIR_SCRIPT, "--league", "pm", "--generation", str(generation)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            log(f"  Mimir stderr: {result.stderr[:300]}")
        else:
            log("  Mimir complete")
    except Exception as e:
        log(f"  Mimir exception: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep", type=int, default=60)
    args = parser.parse_args()

    os.makedirs(PM_RESEARCH, exist_ok=True)
    os.makedirs(POPULATION_DIR, exist_ok=True)
    init_results_tsv()

    log("FREYA researcher starting...")

    markets    = load_resolved_markets()
    base_rates = compute_base_rates(markets)
    gen_state  = load_gen_state()
    population = load_population()
    api_key    = load_gemini_key()

    if os.path.exists(BEST_STRATEGY):
        best = load_strategy(BEST_STRATEGY)
    else:
        best = copy.deepcopy(DEFAULT_STRATEGY)
        save_strategy(best, BEST_STRATEGY)
        log("Initialized with default strategy")

    best_metrics  = simulate_strategy(best, markets, base_rates)
    best_score    = best_metrics["adj_score"]
    program_md    = open(PROGRAM_MD).read() if os.path.exists(PROGRAM_MD) else ""
    gen           = gen_state["gen"]
    gens_no_best  = gen_state["gens_since_best"]
    stall_alerted = gen_state.get("stall_alerted", False)
    last_mimir_ts = gen_state.get("last_mimir_ts")

    log(f"Gen {gen}: best adj={best_score:.4f} sharpe={best_metrics['sharpe']:.4f} "
        f"n_bets={best_metrics['n_bets']}")

    while True:
        gen          += 1
        gens_no_best += 1

        try:
            r     = random.random()
            stall = gens_no_best > 100

            if r < 0.05 or (stall and r < 0.15):
                candidate, mut_type = mutate_random_restart()
            elif r < 0.15 and population:
                candidate, mut_type = mutate_crossover(population)
                if candidate is None:
                    candidate, mut_type = mutate_perturbation(best)
            elif r < 0.30:
                candidate, mut_type = mutate_perturbation(best)
            else:
                candidate, mut_type = mutate_llm(best, best_metrics, program_md, api_key)
                if candidate is None:
                    candidate, mut_type = mutate_perturbation(best)

            if not isinstance(candidate, dict) or not candidate.get("category"):
                append_result(gen, {"sharpe": 0, "win_rate": 0, "roi_pct": 0,
                                    "n_bets": 0, "adj_score": 0}, "invalid", str(mut_type))
                continue

            candidate = sanitize_candidate(candidate, best)

            metrics = simulate_strategy(candidate, markets, base_rates)
            score   = metrics["adj_score"]
            desc    = (f"{mut_type}|{candidate.get('category')}"
                       f"|kw={len(candidate.get('include_keywords', []))}")

            if metrics["sharpe"] > SUSPICIOUS_SHARPE:
                append_result(gen, metrics, "overfitted", desc)
                continue

            if score > best_score:
                best          = copy.deepcopy(candidate)
                best_score    = score
                best_metrics  = metrics
                gens_no_best  = 0
                save_strategy(best, BEST_STRATEGY)
                update_population(population, best, score)
                append_result(gen, metrics, "new_best", desc)
                log(f"  Gen {gen}: NEW BEST adj={score:.4f} sharpe={metrics['sharpe']:.4f} "
                    f"roi={metrics['roi_pct']:.1f}% win={metrics['win_rate']:.1f}% "
                    f"n={metrics['n_bets']} [{mut_type}]")
            else:
                update_population(population, candidate, score)
                append_result(gen, metrics, "no_improvement", desc)

        except Exception as e:
            log(f"  Gen {gen}: ERROR: {e}")
            append_result(gen, {"sharpe": 0, "win_rate": 0, "roi_pct": 0,
                                "n_bets": 0, "adj_score": 0}, "error", str(e)[:80])


        if gen % MIMIR_INTERVAL == 0:
            now_utc = datetime.now(timezone.utc)
            gap_ok  = True
            if last_mimir_ts:
                try:
                    last_dt = datetime.fromisoformat(last_mimir_ts).replace(tzinfo=timezone.utc)
                    gap_hrs = (now_utc - last_dt).total_seconds() / 3600
                    if gap_hrs < MIMIR_MIN_GAP_HRS:
                        gap_ok = False
                        log(f"  Mimir skipped at gen {gen}: cooldown {gap_hrs:.1f}/{MIMIR_MIN_GAP_HRS}h")
                except Exception:
                    pass
            if gap_ok:
                trigger_mimir(gen)
                last_mimir_ts = now_utc.strftime("%Y-%m-%dT%H:%M")
                if os.path.exists(PROGRAM_MD):
                    program_md = open(PROGRAM_MD).read()

        save_gen_state({"gen": gen, "gens_since_best": gens_no_best, "last_mimir_ts": last_mimir_ts})

        if gen % 10 == 0:
            log(f"  Gen {gen}: best adj={best_score:.4f} "
                f"sharpe={best_metrics['sharpe']:.4f} n={best_metrics['n_bets']} "
                f"stall={gens_no_best}")

        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
