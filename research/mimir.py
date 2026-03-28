#!/usr/bin/env python3
"""
mimir.py - Mimir deep analysis agent.

Triggered at every 100-generation milestone by the Odin research loop.
Uses Claude Sonnet 4.6 to analyze research results + sprint
performance, then rewrites program.md with improved guidance.

Usage:
  python3 mimir.py --league day --generation 100
  python3 mimir.py --league swing --generation 200
"""
import argparse
import json
import os
import shutil
import urllib.request
from datetime import datetime, timezone

WORKSPACE         = "/root/.openclaw/workspace"
RESEARCH          = os.path.join(WORKSPACE, "research")
ANTHROPIC_SECRET  = "/root/.openclaw/secrets/anthropic.json"
ANTHROPIC_MODEL   = "claude-sonnet-4-6"
ANTHROPIC_URL     = "https://api.anthropic.com/v1/messages"
MIMIR_LOG         = os.path.join(RESEARCH, "mimir_log.jsonl")

DAY_RESULTS_DIR   = os.path.join(WORKSPACE, "competition", "results")
SWING_RESULTS_DIR = os.path.join(WORKSPACE, "competition", "swing", "results")


def load_anthropic_key():
    with open(ANTHROPIC_SECRET) as f:
        return json.load(f)["anthropic_api_key"]


def call_claude(prompt, api_key):
    payload = json.dumps({
        "model":      ANTHROPIC_MODEL,
        "max_tokens": 4000,
        "messages":   [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        ANTHROPIC_URL,
        data=payload,
        headers={
            "Content-Type":      "application/json",
            "x-api-key":         api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"].strip()


def load_research_results(league):
    path = os.path.join(RESEARCH, league, "results.tsv")
    if not os.path.exists(path):
        return []
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("gen"):
                continue
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


def summarize_research(rows):
    if not rows:
        return "No research results yet."

    total        = len(rows)
    improvements = [r for r in rows if r["status"] == "new_best"]
    errors       = [r for r in rows if "error" in r["status"]]

    sharpes = []
    for r in rows:
        try:
            sharpes.append(float(r["sharpe"]))
        except ValueError:
            pass

    lines = [
        f"Total generations: {total}",
        f"Improvements (new_best): {len(improvements)}",
        f"Error generations: {len(errors)}",
    ]
    if sharpes:
        lines.append(f"Sharpe range: {min(sharpes):.4f} to {max(sharpes):.4f}")

    lines.append("\nImprovement history (all new_best events):")
    for r in improvements:
        lines.append(
            f"  Gen {r['gen']}: sharpe={r['sharpe']}  win_rate={r['win_rate']}%"
            f"  trades={r['trades']}"
        )

    lines.append("\nLast 20 generations:")
    for r in rows[-20:]:
        marker = " ***" if r["status"] == "new_best" else ""
        lines.append(
            f"  Gen {r['gen']}: sharpe={r['sharpe']}  win_rate={r['win_rate']}%"
            f"  trades={r['trades']}  [{r['status']}]{marker}"
        )

    return "\n".join(lines)


def load_sprint_results(league, bot_name, n=10):
    results_dir = DAY_RESULTS_DIR if league == "day" else SWING_RESULTS_DIR
    if not os.path.isdir(results_dir):
        return []

    sprints = []
    for entry in sorted(os.listdir(results_dir), reverse=True):
        score_path = os.path.join(results_dir, entry, "final_score.json")
        if not os.path.exists(score_path):
            continue
        try:
            score = json.load(open(score_path))
            rankings = score.get("rankings", [])
            for r in rankings:
                if r.get("bot", "").lower() == bot_name.lower():
                    sprints.append({
                        "sprint_id":  entry,
                        "rank":       r.get("rank"),
                        "total_bots": len(rankings),
                        "pnl_pct":    r.get("total_pnl_pct", 0),
                        "trades":     r.get("total_trades", 0),
                        "win_rate":   r.get("win_rate", 0),
                    })
                    break
        except Exception:
            continue
        if len(sprints) >= n:
            break
    return sprints


def summarize_sprints(sprint_results, bot_name):
    if not sprint_results:
        return f"{bot_name} has not appeared in any completed sprints yet."
    lines = [f"Last {len(sprint_results)} sprint results for {bot_name}:"]
    for s in sprint_results:
        lines.append(
            f"  {s['sprint_id']}: rank {s['rank']}/{s['total_bots']}"
            f"  pnl={s['pnl_pct']:+.2f}%  trades={s['trades']}"
            f"  win_rate={s['win_rate']:.1f}%"
        )
    return "\n".join(lines)


def build_prompt(league, program_md, best_strategy_yaml,
                 research_summary, sprint_summary, generation):
    bot_name  = "AutoBotDay"  if league == "day"   else "AutoBotSwing"
    timeframe = "5-minute (day trading)" if league == "day" else "1-hour (swing trading)"

    return f"""You are MIMIR, a senior crypto trading strategy analyst. You are analyzing {generation} generations of automated research from ODIN, a strategy optimization loop.

ODIN works by asking a small LLM (llama-3.1-8b-instant) to propose ONE change to the current best strategy, then backtesting it on 2 years of {timeframe} BTC/USD, ETH/USD, SOL/USD data. If Sharpe improves, the change is kept.

---
## Current Research Program (instructions ODIN gives the LLM)

{program_md}

---
## Current Best Strategy

```yaml
{best_strategy_yaml}
```

---
## Research Results

{research_summary}

---
## Live Competition Performance ({bot_name})

{sprint_summary}

---
## Your Task

Analyze the above and identify:
1. What types of changes improve Sharpe vs. what consistently fails
2. Failure patterns — what mistakes does the small LLM keep making?
3. Gaps between backtest Sharpe and live sprint performance (if any)
4. What the current best strategy is doing well vs. where it is weak
5. What guidance would make the next 100 generations more productive

Then produce an improved version of the research program.

Output EXACTLY two sections, using these exact headers:

### ANALYSIS
(3-5 paragraphs of findings)

### UPDATED PROGRAM
(The complete rewritten program.md — same structure, improved guidance)"""


def parse_response(response):
    analysis = ""
    program  = ""
    if "### ANALYSIS" in response and "### UPDATED PROGRAM" in response:
        parts    = response.split("### UPDATED PROGRAM", 1)
        analysis = parts[0].replace("### ANALYSIS", "").strip()
        program  = parts[1].strip()
    elif "### UPDATED PROGRAM" in response:
        parts   = response.split("### UPDATED PROGRAM", 1)
        program = parts[1].strip()
    else:
        analysis = response
    return analysis, program


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league",      choices=["day", "swing"], required=True)
    parser.add_argument("--generation",  type=int,                 required=True)
    args = parser.parse_args()

    league     = args.league
    generation = args.generation
    bot_name   = "autobotday" if league == "day" else "autobotswing"

    print(f"[mimir/{league}] Gen {generation} milestone — deep analysis starting...")

    api_key = load_anthropic_key()

    program_path  = os.path.join(RESEARCH, league, "program.md")
    best_path     = os.path.join(RESEARCH, league, "best_strategy.yaml")
    program_md    = open(program_path).read()  if os.path.exists(program_path) else ""
    best_strategy = open(best_path).read()     if os.path.exists(best_path)    else ""

    research_rows    = load_research_results(league)
    research_summary = summarize_research(research_rows)
    sprint_results   = load_sprint_results(league, bot_name)
    sprint_summary   = summarize_sprints(sprint_results, bot_name)

    prompt = build_prompt(
        league, program_md, best_strategy,
        research_summary, sprint_summary, generation,
    )

    print(f"  Calling Claude ({ANTHROPIC_MODEL})...")
    try:
        response = call_claude(prompt, api_key)
    except Exception as e:
        print(f"  ERROR calling Claude: {e}")
        return

    analysis, new_program = parse_response(response)

    program_updated = False
    if new_program and len(new_program) > 200:
        backup = program_path + f".gen{generation}.bak"
        shutil.copy2(program_path, backup)
        with open(program_path, "w") as f:
            f.write(new_program)
        program_updated = True
        print(f"  program.md updated (backup: {backup})")
    else:
        print("  WARNING: No valid updated program in response — keeping existing.")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
    log_entry = {
        "ts":              ts,
        "league":          league,
        "generation":      generation,
        "analysis":        analysis,
        "program_updated": program_updated,
    }
    with open(MIMIR_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\n[mimir/{league}] Analysis summary:")
    print(analysis[:600] + "..." if len(analysis) > 600 else analysis)
    print(f"\n[mimir/{league}] Done.")


if __name__ == "__main__":
    main()
