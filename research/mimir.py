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
ANTHROPIC_MODEL   = "claude-sonnet-4-6"  # overridden by --model flag
ANTHROPIC_URL     = "https://api.anthropic.com/v1/messages"
MIMIR_LOG            = os.path.join(RESEARCH, "mimir_log.jsonl")
SYN_MIMIR_QUEUE      = os.path.join(RESEARCH, "syn_mimir_queue.jsonl")
LOKI_PENDING_ACTIONS = os.path.join(RESEARCH, "loki_pending_actions.jsonl")

DAY_RESULTS_DIR   = os.path.join(WORKSPACE, "competition", "results")
SWING_RESULTS_DIR         = os.path.join(WORKSPACE, "competition", "swing", "results")
FUTURES_DAY_RESULTS_DIR   = os.path.join(WORKSPACE, "competition", "futures_day", "results")
FUTURES_SWING_RESULTS_DIR = os.path.join(WORKSPACE, "competition", "futures_swing", "results")
PM_RESULTS_DIR    = os.path.join(WORKSPACE, "competition", "polymarket", "auto_results")
PM_RESEARCH       = os.path.join(RESEARCH, "pm")


def load_anthropic_key():
    with open(ANTHROPIC_SECRET) as f:
        return json.load(f)["anthropic_api_key"]


def call_claude(prompt, api_key):
    payload = json.dumps({
        "model":      ANTHROPIC_MODEL,
        "max_tokens": 8000,
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
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"].strip()



def load_researcher_constants():
    """Extract current ALLOWED_CONSTANTS values from odin_researcher_v2.py."""
    researcher_path = os.path.join(RESEARCH, "odin_researcher_v2.py")
    if not os.path.exists(researcher_path):
        return {}
    allowed = {"MIN_TRADES", "POPULATION_SIZE", "SUSPICIOUS_SHARPE", "STALL_ALERT_GENS"}
    constants = {}
    with open(researcher_path) as f:
        for line in f:
            stripped = line.strip()
            for name in allowed:
                if stripped.startswith(name + " ="):
                    constants[name] = stripped.split("=", 1)[1].strip()
                    break
    return constants


def load_loki_changes(league, n=20):
    """Load recent LOKI code changes and escalations for this league."""
    loki_log = os.path.join(RESEARCH, "loki_log.jsonl")
    if not os.path.exists(loki_log):
        return []
    entries = []
    with open(loki_log) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
            except Exception:
                continue
            if entry.get("league") != league:
                continue
            actions = entry.get("actions", [])
            notable = [a for a in actions if a.startswith("code:") or a.startswith("escalated")]
            if notable:
                entries.append({
                    "ts":      entry.get("ts", ""),
                    "gen":     entry.get("gen", "?"),
                    "actions": notable,
                })
    return entries[-n:]


def format_self_audit(constants, loki_changes):
    lines = ["## Current Researcher Constants"]
    if constants:
        for k, v in constants.items():
            lines.append(f"  {k} = {v}")
    else:
        lines.append("  (unavailable)")
    lines.append("")
    lines.append("## Your Recent Code Changes (via LOKI)")
    if loki_changes:
        for c in loki_changes:
            lines.append(f"  [{c['ts']} gen={c['gen']}]")
            for a in c["actions"]:
                lines.append(f"    {a}")
    else:
        lines.append("  No code changes on record.")
    return chr(10).join(lines)


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
    if league == "day":              results_dir = DAY_RESULTS_DIR
    elif league == "futures_day":    results_dir = FUTURES_DAY_RESULTS_DIR
    elif league == "futures_swing":  results_dir = FUTURES_SWING_RESULTS_DIR
    else:                            results_dir = SWING_RESULTS_DIR
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



def load_tyr_context():
    """Load TYR macro regime for MIMIR context."""
    tyr_path = os.path.join(RESEARCH, "tyr_state.json")
    if not os.path.exists(tyr_path):
        return None
    try:
        return json.load(open(tyr_path))
    except Exception:
        return None


def format_tyr_context(tyr):
    """Format TYR state as a concise MIMIR context block."""
    if not tyr:
        return "TYR macro data unavailable."
    regime  = tyr.get("regime", "UNKNOWN")
    message = tyr.get("message", "")
    fg      = tyr.get("fear_greed", {})
    dom     = tyr.get("btc_dominance", {})
    ts      = tyr.get("ts", "")[:16].replace("T", " ")
    lines   = [f"Current Regime: {regime} (as of {ts} UTC)"]
    if fg.get("ok"):
        lines.append(f"Fear & Greed Index: {fg['value']} ({fg.get('label','')})")
    if dom.get("ok"):
        lines.append(f"BTC Dominance: {dom['value']}%")
    lines.append(f"Directive: {message}")
    log = tyr.get("log", [])[:10]
    if log:
        lines.append("Recent readings (newest first):")
        for e in log:
            t   = e.get("ts", "")[:16].replace("T", " ")
            r   = e.get("regime", "?")
            fgv = e.get("fear_greed")
            dv  = e.get("btc_dominance")
            lines.append(f"  {t}  {r}  F&G={fgv}  BTC_DOM={dv}%")
    return "\n".join(lines)


def build_prompt(league, program_md, best_strategy_yaml,
                 research_summary, sprint_summary, generation,
                 self_audit="", tyr_context=""):
    if league == "day":              bot_name = "AutoBotDay";    timeframe = "5-minute (day trading)"
    elif league == "swing":          bot_name = "AutoBotSwing";  timeframe = "1-hour (swing trading)"
    elif league == "futures_day":    bot_name = "AutoBotDayFutures";   timeframe = "5-minute (futures day, 2x leverage)"
    elif league == "futures_swing":  bot_name = "AutoBotSwingFutures"; timeframe = "1-hour (futures swing, 2x leverage)"
    else:                            bot_name = "AutoBot";       timeframe = "unknown"

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
## Macro Environment (TYR Risk Officer)

{tyr_context}

---
## Self-Audit: Constants & Your Past Decisions

{self_audit}

---
## Your Task

FIRST — self-audit: review the constants and your past LOKI changes above. Ask yourself:
- Did any constant change coincide with a performance regression or stall beginning?
- Is the current MIN_TRADES threshold consistent with the trade counts that actually produce good Sharpe in the results above?
- If a past change hurt performance, say so explicitly and recommend reversing or adjusting it.

THEN analyze the research results and identify:
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


def load_pm_research_results(n=200):
    """Load last N rows from research/pm/results.tsv."""
    path = os.path.join(PM_RESEARCH, "results.tsv")
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
                    "gen":       parts[0],
                    "sharpe":    parts[1],
                    "win_rate":  parts[2],
                    "roi_pct":   parts[3],
                    "n_bets":    parts[4],
                    "adj_score": parts[5],
                    "status":    parts[6] if len(parts) > 6 else "",
                    "desc":      parts[7] if len(parts) > 7 else "",
                })
    return rows[-n:]


def summarize_pm_research(rows):
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
        f"Total generations analyzed: {total}",
        f"Improvements (new_best): {len(improvements)}",
        f"Error generations: {len(errors)}",
    ]
    if sharpes:
        lines.append(f"Sharpe range: {min(sharpes):.4f} to {max(sharpes):.4f}")
    lines.append("\nAll improvement events (new_best):")
    for r in improvements:
        lines.append(
            f"  Gen {r['gen']}: adj={r['adj_score']}  sharpe={r['sharpe']}"
            f"  roi={r['roi_pct']}%  win={r['win_rate']}%  bets={r['n_bets']}"
            f"  [{r['desc']}]"
        )
    lines.append("\nLast 20 generations:")
    for r in rows[-20:]:
        marker = " ***" if r["status"] == "new_best" else ""
        lines.append(
            f"  Gen {r['gen']}: adj={r['adj_score']}  sharpe={r['sharpe']}"
            f"  bets={r['n_bets']}  [{r['status']}]{marker}"
        )
    return "\n".join(lines)


def load_pm_sprint_results(n=5):
    """Load last N completed PM sprint results for FREYA research bots."""
    freya_bots = {"mist", "kara", "thrud"}
    if not os.path.isdir(PM_RESULTS_DIR):
        return {}
    results = {b: [] for b in freya_bots}
    for sprint_dir in sorted(os.listdir(PM_RESULTS_DIR), reverse=True):
        score_path = os.path.join(PM_RESULTS_DIR, sprint_dir, "final_score.json")
        if not os.path.exists(score_path):
            continue
        try:
            score      = json.load(open(score_path))
            all_bots   = score.get("bots", [])
            total_bots = len(all_bots)
            for entry in all_bots:
                bot = entry.get("bot", "")
                if bot in results and len(results[bot]) < n:
                    results[bot].append({
                        "sprint_id": sprint_dir,
                        "total_bots": total_bots,
                        "pnl_pct":   entry.get("sprint_pnl_pct", 0),
                        "trades":    entry.get("sprint_trades", 0),
                        "wins":      entry.get("sprint_wins", 0),
                        "win_rate":  entry.get("win_rate", 0),
                    })
        except Exception:
            continue
    return results


def summarize_pm_sprints(sprint_results):
    lines = []
    for bot, sprints in sprint_results.items():
        if not sprints:
            lines.append(f"{bot}: no completed sprints (disabled research slot)")
        else:
            lines.append(f"\n{bot} ({len(sprints)} sprints):")
            for s in sprints:
                lines.append(
                    f"  {s['sprint_id']}: pnl={s['pnl_pct']:+.1f}%"
                    f"  trades={s['trades']}  wins={s['wins']}"
                    f"  win_rate={s['win_rate']:.1f}%"
                )
    return "\n".join(lines) if lines else "No PM sprint data."


def build_pm_prompt(program_md, best_strategy_yaml, research_summary,
                    sprint_summary, generation):
    return f"""You are MIMIR, a prediction markets strategy analyst. You are reviewing {generation} generations of automated research from FREYA, a strategy optimization loop for prediction markets.

FREYA works by asking Gemini Flash Lite to propose ONE change to the current best strategy (keyword filters, category, edge threshold, etc.), then simulating it against 300k+ historical resolved markets. If adj_score (sharpe x log(n_bets/20+1)) improves, the change is kept.

SIMULATION MODEL:
- Category base rates (historical YES resolution): sports=30.6%, politics=29.1%, crypto=31.5%, economics=26.0%, world_events=12.0%
- Bet: if market_odds > base_rate + min_edge_pts -> bet NO; if market_odds < base_rate - min_edge_pts -> bet YES
- Fee: 2% per bet
- adj_score = sharpe x log(n_bets/20 + 1)

---
## Current Research Program

{program_md}

---
## Current Best Strategy

```yaml
{best_strategy_yaml}
```

---
## Simulation Research Results

{research_summary}

---
## Live Competition (FREYA research slots: mist, kara, thrud)

{sprint_summary}

---
## Your Task

Analyze and identify:
1. What category/keyword combinations improve adj_score vs. what fails?
2. What does the simulation reveal about prediction market calibration patterns?
3. Are live sprint results consistent with simulation findings?
4. What should FREYA prioritize in the next 100 generations?

Output EXACTLY two sections:

### ANALYSIS
(3-5 paragraphs)

### UPDATED PROGRAM
(Complete rewritten program.md — same structure, improved guidance)"""


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


def process_syn_alerts():
    """Read SYN alert queue, analyze each with Claude, write structured actions to LOKI."""
    if not os.path.exists(SYN_MIMIR_QUEUE):
        print("[mimir/syn_alert] No queue file — nothing to do")
        return

    api_key = load_anthropic_key()

    with open(SYN_MIMIR_QUEUE) as f:
        entries = [json.loads(l) for l in f if l.strip()]

    unprocessed = [e for e in entries if not e.get("processed")]
    if not unprocessed:
        print("[mimir/syn_alert] No unprocessed alerts")
        return

    print(f"[mimir/syn_alert] Processing {len(unprocessed)} alert(s)")

    for entry in unprocessed:
        league     = entry.get("league", "unknown")
        error_type = entry.get("error_type", "unknown")
        message    = entry.get("message", "")
        context    = entry.get("context", {})
        print(f"  [{league}/{error_type}] analyzing...")

        # Gather research context
        results_tail = ""
        results_path = os.path.join(RESEARCH, league, "results.tsv")
        if os.path.exists(results_path):
            with open(results_path) as f:
                lines = f.readlines()
            results_tail = "".join(lines[-20:])

        gen_state = context.get("gen_state", {})
        prog_path = os.path.join(RESEARCH, league, "program.md")
        prog_snippet = ""
        if os.path.exists(prog_path):
            with open(prog_path) as f:
                prog_snippet = f.read()[-2000:]

        prompt = f"""You are Mimir, analysis officer for a crypto trading research system.

SYN (system monitor) detected:
League: {league}
Error type: {error_type}
Message: {message}
Gen state: {json.dumps(gen_state)}

Recent research results (last 20 gens):
{results_tail}

Bottom of program.md:
{prog_snippet}

Diagnose the root cause and output a JSON object with recommended LOKI actions:
{{
  "analysis": "brief root cause diagnosis (2-3 sentences)",
  "actions": [
    {{"type": "restart_service", "unit": "service_name.service", "reason": "..."}},
    {{"type": "update_constant", "constant": "NAME", "subkey": "key_or_null", "new_value": 50, "reason": "..."}},
    {{"type": "structural", "description": "specific change needed", "analysis": "detailed context for code patch generation"}},
    {{"type": "escalate", "description": "what needs human attention"}}
  ]
}}

Only include actions that directly address the detected problem. Be conservative.
Output the JSON object only — no surrounding text."""

        try:
            response = call_claude(prompt, api_key)
            import re as _re
            m = _re.search(r'\{[\s\S]*\}', response)
            rec = json.loads(m.group()) if m else {"analysis": response[:200], "actions": [{"type": "escalate", "description": "Could not parse Mimir response"}]}
        except Exception as e:
            rec = {"analysis": f"Mimir analysis error: {e}", "actions": [{"type": "escalate", "description": str(e)}]}

        pending = {
            "ts":             datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "source":         "syn_alert",
            "league":         league,
            "error_type":     error_type,
            "mimir_analysis": rec.get("analysis", ""),
            "actions":        rec.get("actions", []),
            "processed":      False,
        }
        with open(LOKI_PENDING_ACTIONS, "a") as f:
            f.write(json.dumps(pending) + "\n")

        entry["processed"]    = True
        entry["processed_ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
        print(f"  [{league}/{error_type}] -> {len(rec.get('actions', []))} action(s) queued for LOKI")

    # Rewrite queue with processed flags
    with open(SYN_MIMIR_QUEUE, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")
    print("[mimir/syn_alert] Done")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league",      choices=["day", "swing", "pm", "futures_day", "futures_swing"], required=False)
    parser.add_argument("--generation",  type=int,                       required=False)
    parser.add_argument("--model",       default=None, help="Override Claude model (e.g. claude-opus-4-6)")
    parser.add_argument("--mode",        choices=["standard", "syn_alert"], default="standard")
    args = parser.parse_args()

    if args.mode == "syn_alert":
        process_syn_alerts()
        return

    if not args.league or args.generation is None:
        parser.error("--league and --generation are required in standard mode")

    league     = args.league
    generation = args.generation
    if args.model:
        global ANTHROPIC_MODEL
        ANTHROPIC_MODEL = args.model

    print(f"[mimir/{league}] Gen {generation} milestone — deep analysis starting...")

    api_key = load_anthropic_key()

    if league == "pm":
        program_path  = os.path.join(PM_RESEARCH, "program.md")
        best_path     = os.path.join(PM_RESEARCH, "best_strategy.yaml")
        program_md    = open(program_path).read()  if os.path.exists(program_path) else ""
        best_strategy = open(best_path).read()     if os.path.exists(best_path)    else ""
        research_rows    = load_pm_research_results()
        research_summary = summarize_pm_research(research_rows)
        sprint_data      = load_pm_sprint_results()
        sprint_summary   = summarize_pm_sprints(sprint_data)
        prompt = build_pm_prompt(program_md, best_strategy,
                                 research_summary, sprint_summary, generation)
    else:
        if league == "day":             bot_name = "autobotday"
        elif league == "swing":         bot_name = "autobotswing"
        elif league == "futures_day":   bot_name = "autobotdayfutures"
        elif league == "futures_swing": bot_name = "autobotswingfutures"
        else:                           bot_name = "autobotday"
        program_path  = os.path.join(RESEARCH, league, "program.md")
        best_path     = os.path.join(RESEARCH, league, "best_strategy.yaml")
        program_md    = open(program_path).read()  if os.path.exists(program_path) else ""
        best_strategy = open(best_path).read()     if os.path.exists(best_path)    else ""
        research_rows    = load_research_results(league)
        research_summary = summarize_research(research_rows)
        sprint_results   = load_sprint_results(league, bot_name)
        sprint_summary   = summarize_sprints(sprint_results, bot_name)
        constants        = load_researcher_constants()
        loki_changes     = load_loki_changes(league)
        self_audit       = format_self_audit(constants, loki_changes)
        tyr     = load_tyr_context()
        tyr_ctx = format_tyr_context(tyr)
        prompt = build_prompt(
            league, program_md, best_strategy,
            research_summary, sprint_summary, generation,
            self_audit=self_audit,
            tyr_context=tyr_ctx,
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
        "model":           ANTHROPIC_MODEL,
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
