#!/usr/bin/env python3
"""
odin_researcher.py - Odin auto-research loop.

Continuously proposes strategy modifications via Gemini Flash (free API),
backtests them against 2yr historical data, and keeps winners.

Usage:
  python3 odin_researcher.py --league day
  python3 odin_researcher.py --league swing
  python3 odin_researcher.py --league day --sleep 90
"""
import argparse
import json
import os
import re
import sys
import subprocess
import time
import urllib.request
from datetime import datetime, timezone

import yaml

WORKSPACE     = "/root/.openclaw/workspace"
RESEARCH      = os.path.join(WORKSPACE, "research")
GEMINI_SECRET = "/root/.openclaw/secrets/gemini.json"
GEMINI_MODEL  = "gemini-2.5-flash-lite"
GEMINI_BASE   = "https://generativelanguage.googleapis.com/v1beta/models"

# Look-ahead bias guard
SUSPICIOUS_SHARPE = 3.5

# Minimum trade count to accept a strategy as new best (prevents overfitting on noise)
MIN_TRADES = {"day": 50, "swing": 20}

ALL_PAIRS = [
    "BTC/USD",  "ETH/USD",  "SOL/USD",  "XRP/USD",
    "DOGE/USD", "AVAX/USD", "LINK/USD", "UNI/USD",
    "AAVE/USD", "NEAR/USD", "APT/USD",  "SUI/USD",
    "ARB/USD",  "OP/USD",   "ADA/USD",  "POL/USD",
]


def load_gemini_key(league):
    with open(GEMINI_SECRET) as f:
        data = json.load(f)
    return data.get(f"gemini_{league}_key") or data["gemini_api_key"]


def league_dir(league):
    return os.path.join(RESEARCH, league)


def load_program_md(league):
    path = os.path.join(league_dir(league), "program.md")
    with open(path) as f:
        return f.read()


def load_best_strategy(league):
    path = os.path.join(league_dir(league), "best_strategy.yaml")
    if not os.path.exists(path):
        return None, None
    with open(path) as f:
        text = f.read()
    return yaml.safe_load(text), text


def save_best_strategy(league, strategy_yaml, sharpe, gen):
    path = os.path.join(league_dir(league), "best_strategy.yaml")
    with open(path, "w") as f:
        f.write(strategy_yaml)
    fleet_path = get_fleet_path(league)
    if fleet_path:
        os.makedirs(os.path.dirname(fleet_path), exist_ok=True)
        with open(fleet_path, "w") as f:
            f.write(strategy_yaml)
    print(f"  *** NEW BEST: Sharpe={sharpe:.4f} at gen {gen} -> saved ***")


def get_fleet_path(league):
    if league == "day":
        return os.path.join(WORKSPACE, "fleet", "autobotday", "strategy.yaml")
    elif league == "swing":
        return os.path.join(WORKSPACE, "fleet", "swing", "autobotswing", "strategy.yaml")
    return None


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
                        "gen":      parts[0],
                        "sharpe":   parts[1],
                        "win_rate": parts[2],
                        "pnl_pct":  parts[3],
                        "trades":   parts[4],
                        "status":   parts[5],
                    })
    return rows


def log_result(league, gen, result, status, description=""):
    path = os.path.join(league_dir(league), "results.tsv")
    write_header = not os.path.exists(path)
    with open(path, "a") as f:
        if write_header:
            f.write("gen\tsharpe\twin_rate\tpnl_pct\ttrades\tstatus\tdescription\tts\n")
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
        sharpe   = result.get("sharpe", 0) if isinstance(result, dict) else 0
        win_rate = result.get("win_rate_pct", 0) if isinstance(result, dict) else 0
        pnl_pct  = result.get("total_pnl_pct", 0) if isinstance(result, dict) else 0
        trades   = result.get("total_trades", 0) if isinstance(result, dict) else 0
        f.write(f"{gen}\t{sharpe:.4f}\t{win_rate:.1f}\t{pnl_pct:.2f}\t{trades}\t{status}\t{description}\t{ts}\n")


def call_gemini(prompt, api_key):
    url = f"{GEMINI_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1500},
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


def build_prompt(league, program_md, current_strategy_yaml, results_history, gen, best_sharpe):
    recent = results_history[-10:] if len(results_history) >= 10 else results_history
    results_text = "\n".join(
        f"  Gen {r['gen']}: sharpe={r['sharpe']}  win_rate={r['win_rate']}%  "
        f"pnl={r['pnl_pct']}%  trades={r['trades']}  [{r['status']}]"
        for r in recent
    )
    if not results_text:
        results_text = "  (no results yet - this is generation 1)"

    return (
        program_md
        + "\n\n---\n"
        + f"## Current Best Strategy (Sharpe={best_sharpe:.4f})\n\n"
        + "```yaml\n" + current_strategy_yaml + "\n```\n\n"
        + f"## Recent Results (last {len(recent)} generations)\n\n"
        + results_text
        + "\n\n---\n"
        + "## Your Task\n\n"
        + f"Generation {gen}. Propose ONE focused improvement to the strategy above.\n"
        + "Output ONLY the complete modified strategy YAML between ```yaml and ``` markers.\n"
        + "Do not explain or add commentary outside the YAML block.\n"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league", choices=["day", "swing"], required=True)
    parser.add_argument("--sleep", type=int, default=90,
                        help="Seconds to sleep between cycles (default 60)")
    parser.add_argument("--offset", type=int, default=0,
                        help="Startup delay in seconds to stagger instances")
    args = parser.parse_args()
    league = args.league

    sys.path.insert(0, RESEARCH)
    from odin_backtest import run_backtest

    api_key = load_gemini_key(league)

    if args.offset > 0:
        print(f"[odin/{league}] Startup offset {args.offset}s...")
        time.sleep(args.offset)

    os.makedirs(league_dir(league), exist_ok=True)
    program_md = load_program_md(league)
    best_strategy, best_strategy_yaml = load_best_strategy(league)

    if best_strategy is None:
        print(f"[odin/{league}] No best_strategy.yaml found. Checking fleet for seed...")
        fleet_path = get_fleet_path(league)
        if fleet_path and os.path.exists(fleet_path):
            with open(fleet_path) as f:
                best_strategy_yaml = f.read()
            best_strategy = yaml.safe_load(best_strategy_yaml)
            print(f"  Seeded from {fleet_path}")
        else:
            print("  No seed found. Create best_strategy.yaml manually.")
            sys.exit(1)

    results_history = load_results(league)
    # Persist gen counter in state to survive restarts
    state_path = os.path.join(league_dir(league), "gen_state.json")
    if os.path.exists(state_path):
        with open(state_path) as _f:
            _gs = json.load(_f)
        gen = _gs.get("gen", len(results_history) + 1)
    else:
        gen = len(results_history) + 1
    state = {"consec_429": 0}

    print(f"[odin/{league}] Establishing baseline Sharpe for seed strategy...")
    baseline = run_backtest(best_strategy, league, ALL_PAIRS)
    if "error" in baseline:
        print(f"  ERROR: {baseline['error']}")
        sys.exit(1)
    best_sharpe = baseline["sharpe"]
    min_t = MIN_TRADES.get(league, 30)
    if baseline["total_trades"] < min_t:
        print(f"  WARNING: seed has only {baseline['total_trades']} trades (< {min_t} minimum) — "
              f"likely overfitted. Resetting baseline to 0.0 for fresh search.")
        best_sharpe = 0.0
    print(f"  Baseline Sharpe={best_sharpe:.4f}  pnl={baseline['total_pnl_pct']:+.2f}%  "
          f"trades={baseline['total_trades']}  win_rate={baseline['win_rate_pct']}%")
    print(f"\n[odin/{league}] Starting research loop (Gemini/{GEMINI_MODEL}, {args.sleep}s sleep).\n")

    while True:
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(f"[{ts}] Gen {gen} | best_sharpe={best_sharpe:.4f}", end=" ", flush=True)

        # 1. Call Groq
        try:
            prompt   = build_prompt(league, program_md, best_strategy_yaml,
                                    results_history, gen, best_sharpe)
            response = call_gemini(prompt, api_key)
        except Exception as e:
            err_str = str(e)
            print(f"| GEMINI ERROR: {err_str}")
            log_result(league, gen, {}, "gemini_error", err_str[:80])
            gen += 1
            # 429 rate limit: exponential backoff
            consec_429 = state.get("consec_429", 0)
            if "429" in err_str:
                consec_429 += 1
                state["consec_429"] = consec_429
                wait = min(60 * (2 ** (consec_429 - 1)), 600)
            else:
                state["consec_429"] = 0
                wait = 60
            time.sleep(wait)
            continue

        # 2. Extract YAML
        strategy_yaml = extract_yaml(response)
        if not strategy_yaml:
            print("| YAML_NOT_FOUND")
            log_result(league, gen, {}, "yaml_not_found")
            gen += 1
            time.sleep(args.sleep)
            continue

        # 3. Parse YAML
        try:
            strategy = yaml.safe_load(strategy_yaml)
            if not isinstance(strategy, dict):
                raise ValueError("Not a dict")
        except Exception as e:
            print(f"| YAML_PARSE_ERROR: {e}")
            log_result(league, gen, {}, "yaml_parse_error", str(e)[:80])
            gen += 1
            time.sleep(args.sleep)
            continue

        # 4. Backtest
        try:
            result = run_backtest(strategy, league, ALL_PAIRS)
        except Exception as e:
            print(f"| BACKTEST_ERROR: {e}")
            log_result(league, gen, {}, "backtest_error", str(e)[:80])
            gen += 1
            time.sleep(args.sleep)
            continue

        if "error" in result:
            print(f"| BACKTEST_ERROR: {result['error']}")
            log_result(league, gen, {}, "backtest_error", result["error"][:80])
            gen += 1
            time.sleep(args.sleep)
            continue

        sharpe   = result["sharpe"]
        win_rate = result["win_rate_pct"]
        pnl_pct  = result["total_pnl_pct"]
        trades   = result["total_trades"]

        # 5. Look-ahead bias check
        if result["suspicious"]:
            reason = result["suspicious_reason"]
            print(f"| sharpe={sharpe:.4f} REJECTED (look-ahead: {reason})")
            log_result(league, gen, result, "rejected_lookahead", reason)
            results_history.append({"gen": str(gen), "sharpe": f"{sharpe:.4f}",
                                     "win_rate": f"{win_rate:.1f}", "pnl_pct": f"{pnl_pct:.2f}",
                                     "trades": str(trades), "status": "rejected_lookahead"})
            gen += 1
            time.sleep(args.sleep)
            continue

        # 5b. Minimum trade count guard — prevents overfitting on low-sample noise
        min_t = MIN_TRADES.get(league, 30)
        if trades < min_t:
            print(f"| sharpe={sharpe:.4f}  win={win_rate}%  trades={trades}  "
                  f"[low_trades < {min_t}]")
            log_result(league, gen, result, "low_trades", f"trades={trades} < {min_t}")
            results_history.append({"gen": str(gen), "sharpe": f"{sharpe:.4f}",
                                     "win_rate": f"{win_rate:.1f}", "pnl_pct": f"{pnl_pct:.2f}",
                                     "trades": str(trades), "status": "low_trades"})
            gen += 1
            with open(state_path, "w") as _f:
                json.dump({"gen": gen}, _f)
            time.sleep(args.sleep)
            continue

        # 6. Compare to best
        if sharpe > best_sharpe:
            status = "new_best"
            save_best_strategy(league, strategy_yaml, sharpe, gen)
            best_sharpe        = sharpe
            best_strategy      = strategy
            best_strategy_yaml = strategy_yaml
        else:
            status = "discarded"

        print(f"| sharpe={sharpe:.4f}  win={win_rate}%  pnl={pnl_pct:+.2f}%  "
              f"trades={trades}  [{status}]")

        log_result(league, gen, result, status)
        results_history.append({"gen": str(gen), "sharpe": f"{sharpe:.4f}",
                                 "win_rate": f"{win_rate:.1f}", "pnl_pct": f"{pnl_pct:.2f}",
                                 "trades": str(trades), "status": status})
        # Cap in-memory history to prevent unbounded growth
        if len(results_history) > 200:
            results_history = results_history[-200:]

        # Mimir milestone: deep analysis every 100 generations
        if gen % 100 == 0:
            print(f'  [mimir] Gen {gen} milestone — launching deep analysis...')
            try:
                subprocess.Popen(
                    ['python3', os.path.join(RESEARCH, 'mimir.py'),
                     '--league', league, '--generation', str(gen)],
                    stdout=open(os.path.join(league_dir(league), 'mimir.log'), 'a'),
                    stderr=subprocess.STDOUT,
                )
            except Exception as e:
                print(f'  [mimir] Failed to launch: {e}')

        gen += 1
        # Persist gen counter
        with open(state_path, "w") as _f:
            json.dump({"gen": gen}, _f)
        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
