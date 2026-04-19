#!/usr/bin/env python3
"""
vidar.py -- VIDAR Strategic Arbitration Officer (Executive Staff)

Claude Opus 4.7 (1M context). Fires only on high-stakes triggers, not routine
analysis. MIMIR stays on Sonnet 4.6 for the 10x/day work.

Modes:
  --mode revert_review     LOKI just reverted a change: was the revert correct?
  --mode oscillation_diag  A league hit the oscillation pause: diagnose churn
  --mode restructure       Own program.md rewrite when structure is the bug
  --mode cycle_review      Low-confidence MIMIR fallback
  --mode deep_dive         Manual ad-hoc (requires --topic)

Usage:
  python3 research/vidar.py --mode revert_review --league day --revert-ts 2026-04-19T03:45
  python3 research/vidar.py --mode oscillation_diag --league day
  python3 research/vidar.py --mode deep_dive --league day --topic "why is mean_sharpe flat?"
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

WORKSPACE         = "/root/.openclaw/workspace"
RESEARCH          = os.path.join(WORKSPACE, "research")
ANTHROPIC_SECRET  = "/root/.openclaw/secrets/anthropic.json"
ANTHROPIC_URL     = "https://api.anthropic.com/v1/messages"
VIDAR_MODEL       = "claude-opus-4-7"
VIDAR_MAX_TOKENS  = 6000
VIDAR_LOG         = os.path.join(RESEARCH, "vidar_log.jsonl")
VIDAR_DECISIONS   = os.path.join(RESEARCH, "vidar_decisions.jsonl")
MAINTENANCE_LOG   = os.path.join(WORKSPACE, "maintenance_log.jsonl")
MIMIR_LOG         = os.path.join(RESEARCH, "mimir_log.jsonl")
LOKI_REVERT_HIST  = os.path.join(RESEARCH, "loki_revert_history.json")
LOKI_PAUSES_FILE  = os.path.join(RESEARCH, "loki_structural_pauses.json")
ANTHROPIC_USAGE   = os.path.join(RESEARCH, "anthropic_usage.jsonl")
LOKI_PENDING      = os.path.join(RESEARCH, "loki_pending_actions.jsonl")
RESEARCHER_PY     = os.path.join(RESEARCH, "odin_researcher_v2.py")

TG_BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
TG_CHAT_ID   = "8154505910"


def tg_send(text):
    try:
        data = json.dumps({"chat_id": TG_CHAT_ID, "text": text[:4000]}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
            data=data, headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10).read()
    except Exception as e:
        print(f"  [vidar/tg] {e}")


def load_anthropic_key():
    with open(ANTHROPIC_SECRET) as f:
        return json.load(f)["anthropic_api_key"]


def call_opus(prompt, api_key):
    payload = json.dumps({
        "model":      VIDAR_MODEL,
        "max_tokens": VIDAR_MAX_TOKENS,
        "messages":   [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        ANTHROPIC_URL, data=payload,
        headers={
            "Content-Type":      "application/json",
            "x-api-key":         api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        resp_headers = dict(r.headers)
        data = json.loads(r.read())
    try:
        usage = data.get("usage", {}) or {}
        rec = {
            "ts":            datetime.now(timezone.utc).isoformat(),
            "caller":        "vidar",
            "model":         VIDAR_MODEL,
            "input_tokens":  usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
            "cache_read_input_tokens":     usage.get("cache_read_input_tokens", 0),
            "rl_requests_remaining":       resp_headers.get("anthropic-ratelimit-requests-remaining"),
        }
        with open(ANTHROPIC_USAGE, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception:
        pass
    return data["content"][0]["text"].strip()


def load_recent_mimir(league, n=3):
    if not os.path.exists(MIMIR_LOG):
        return []
    rows = []
    with open(MIMIR_LOG) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if r.get("league") == league:
                    rows.append(r)
            except Exception:
                continue
    return rows[-n:]


def load_recent_reverts(league, n=5):
    if not os.path.exists(LOKI_REVERT_HIST):
        return []
    try:
        h = json.load(open(LOKI_REVERT_HIST))
    except Exception:
        return []
    return (h.get(league, []) or [])[-n:]


def load_results_tail(league, n=100):
    path = os.path.join(RESEARCH, league, "results.tsv")
    if not os.path.exists(path):
        return ""
    with open(path) as f:
        lines = f.readlines()
    header = lines[0] if lines else ""
    tail = "".join(lines[-n:])
    return header + tail


def load_program(league):
    path = os.path.join(RESEARCH, league, "program.md")
    if not os.path.exists(path):
        return "(program.md not found)"
    with open(path) as f:
        return f.read()


def write_decision(record):
    with open(VIDAR_DECISIONS, "a") as f:
        f.write(json.dumps(record) + "\n")


def write_log(record):
    with open(VIDAR_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")


def write_maintenance(league, mode, detail, result="", fix_hint="", phase="arbitrated"):
    try:
        rec = {
            "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
            "phase":    phase,
            "source":   "VIDAR",
            "league":   league,
            "kind":     f"vidar_{mode}",
            "detail":   detail[:180],
            "result":   result[:180],
            "fix_hint": fix_hint[:180],
        }
        with open(MAINTENANCE_LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print(f"  [vidar/maintenance] failed: {e}")


def build_revert_review_prompt(league, revert_ts):
    reverts = load_recent_reverts(league, n=5)
    target_revert = next((r for r in reverts if r.get("ts", "").startswith(revert_ts[:16])), None)
    if not target_revert:
        target_revert = reverts[-1] if reverts else {}
    mimir_recent = load_recent_mimir(league, n=3)
    results_tail = load_results_tail(league, n=80)
    return f"""You are VIDAR, the Strategic Arbitration Officer. You are reviewing a LOKI auto-revert that just fired.

LOKI auto-reverted a MIMIR-driven change because post-change metrics degraded past threshold. Your job: was the revert correct?

## THE REVERT
League: {league}
Revert record: {json.dumps(target_revert, indent=2)}

## RECENT REVERT HISTORY (same league)
{json.dumps(reverts, indent=2)}

## LAST 3 MIMIR ANALYSES (same league)
{json.dumps([{"ts": r.get("ts"), "gen": r.get("generation"), "analysis": r.get("analysis", "")[:1500]} for r in mimir_recent], indent=2)}

## LAST 80 RESULTS ROWS
{results_tail}

## YOUR TASK
Answer three questions precisely:

1. **Was the revert mechanically correct?** (Did the post-change metrics actually degrade, or was the audit threshold too tight?)
2. **Was the revert strategically correct?** (Sometimes short-term metric dips precede long-term gains — is this one of those?)
3. **What should happen next?** Options: "accept_revert" (done, continue), "reapply_change" (the original change was good, revert was wrong), "escalate_chris" (pattern suggests deeper issue), "clear_pause" (if oscillation pause was triggered but you judge it premature).

Output EXACTLY this JSON block at the end of your response:

```json
{{"verdict": "revert_correct|revert_wrong|inconclusive", "recommended_action": "accept_revert|reapply_change|escalate_chris|clear_pause", "confidence": "high|medium|low", "rationale": "<2-3 sentences>"}}
```

Before the JSON, write 3-5 paragraphs of your reasoning."""


def build_oscillation_prompt(league):
    reverts = load_recent_reverts(league, n=10)
    mimir_recent = load_recent_mimir(league, n=5)
    pauses = json.load(open(LOKI_PAUSES_FILE)) if os.path.exists(LOKI_PAUSES_FILE) else {}
    return f"""You are VIDAR. A league hit the LOKI oscillation pause (>=2 reverts in 24h). Diagnose the churn.

League: {league}
Pause state: {json.dumps(pauses.get(league), default=str)}

## RECENT REVERTS (last 10)
{json.dumps(reverts, indent=2)}

## LAST 5 MIMIR ANALYSES
{json.dumps([{"ts": r.get("ts"), "gen": r.get("generation"), "program_updated": r.get("program_updated"), "analysis_excerpt": r.get("analysis", "")[:1000]} for r in mimir_recent], indent=2)}

## YOUR TASK
1. What failure mode is MIMIR stuck in? (Same mistake repeated? Over-correction cycle? External data shift?)
2. Is the pause sufficient, or does something deeper need attention?
3. Recommended action: "keep_pause" | "clear_pause" | "manual_program_rewrite" (VIDAR takes over) | "escalate_chris"

End with:

```json
{{"diagnosis": "<short label>", "recommended_action": "keep_pause|clear_pause|manual_program_rewrite|escalate_chris", "rationale": "<2-3 sentences>"}}
```"""


def build_restructure_prompt(league):
    program = load_program(league)
    mimir_recent = load_recent_mimir(league, n=3)
    results_tail = load_results_tail(league, n=60)
    return f"""You are VIDAR. MIMIR has repeatedly flagged that the research program's STRUCTURE (not content) is the failure mode. You own the restructure.

League: {league}

## CURRENT program.md ({len(program.split())} words)
{program}

## LAST 3 MIMIR ANALYSES
{json.dumps([{"ts": r.get("ts"), "analysis": r.get("analysis", "")[:1200]} for r in mimir_recent], indent=2)}

## RECENT RESULTS (last 60)
{results_tail}

## YOUR TASK
Produce a radically simplified program.md that the 8b gen-time LLM (Llama-3.1-8b-instant) can reliably follow. Rules:
- Put the YAML template FIRST, before any preamble
- Operator checks must be INLINE in the YAML as comments + restated in a single checklist immediately after
- Target < 600 words total
- Strip all narrative ("WHY THIS MATTERS", "FAILURE SIGNATURES" beyond 1 short line, historical context)
- Keep only: template, checklist, target table, acceptance criteria, fixed fields, one-line failure fingerprints

Output EXACTLY two sections:

### RATIONALE
(2-3 paragraphs explaining what changed and why)

### NEW PROGRAM
```markdown
(the complete rewritten program.md)
```"""


def build_patch_repair_prompt(league, mimir_ts):
    mimir_entry = None
    with open(MIMIR_LOG) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if r.get("league") == league and r.get("ts", "").startswith(mimir_ts[:16]):
                    mimir_entry = r
                    break
            except Exception:
                continue
    if not mimir_entry:
        return None, None
    with open(RESEARCHER_PY) as f:
        source = f.read()
    failed_patch = mimir_entry.get("patch", [])
    analysis = mimir_entry.get("analysis", "")
    return mimir_entry, f"""You are VIDAR. MIMIR proposed a structural code patch that LOKI could not apply because the "old" anchor string no longer exists in the current source (MIMIR's patch is stale).

Your job: read MIMIR's analysis, read the ACTUAL current source, and either (a) produce a corrected {{"old": "...", "new": "..."}} patch that applies cleanly to the current source and preserves MIMIR's intent, or (b) decline as "not actionable" (maybe the code already evolved past the issue).

League: {league}
MIMIR generation: {mimir_entry.get("generation")}
MIMIR ts: {mimir_entry.get("ts")}

## MIMIR's Analysis
{analysis}

## MIMIR's Failed Patch (old string not found in current source)
{json.dumps(failed_patch, indent=2)}

## Current odin_researcher_v2.py ({len(source.splitlines())} lines)
```python
{source}
```

## Rules for a corrected patch
- Each "old" string must appear EXACTLY ONCE in the current source
- The replacement must be minimal and preserve surrounding structure
- Python syntax must remain valid after the change
- If the intent of MIMIR's original patch no longer applies (code already fixes it, or the concern is moot), decline with "not_actionable"

## Output
Write 2-3 paragraphs of reasoning (what MIMIR was trying to achieve, what's actually in the code, whether the patch is still relevant).

Then output EXACTLY this JSON block at the end:

```json
{{"verdict": "patch_repaired|not_actionable|escalate_chris", "rationale": "<2-3 sentences>", "patch": [{{"old": "<exact unique string>", "new": "<replacement>"}}], "description": "<short description for LOKI>"}}
```

If verdict is "not_actionable" or "escalate_chris", pass `"patch": []`."""


def build_deep_dive_prompt(league, topic):
    program = load_program(league)
    mimir_recent = load_recent_mimir(league, n=3)
    results_tail = load_results_tail(league, n=150)
    return f"""You are VIDAR. Chris requested a deep-dive on this topic.

League: {league}
Topic: {topic}

## program.md
{program[:3000]}

## LAST 3 MIMIR ANALYSES
{json.dumps([{"ts": r.get("ts"), "analysis": r.get("analysis", "")[:1500]} for r in mimir_recent], indent=2)}

## RESULTS (last 150)
{results_tail}

Give Chris your honest strategic read: root cause, second-order effects he may be missing, concrete recommendation. Be direct; no hedging."""


def run_mode(args, api_key):
    if args.mode == "revert_review":
        if not args.revert_ts:
            print("--revert-ts required for revert_review")
            sys.exit(1)
        prompt = build_revert_review_prompt(args.league, args.revert_ts)
    elif args.mode == "oscillation_diag":
        prompt = build_oscillation_prompt(args.league)
    elif args.mode == "restructure":
        prompt = build_restructure_prompt(args.league)
    elif args.mode == "cycle_review":
        prompt = build_deep_dive_prompt(args.league, "cycle review — low-confidence MIMIR fallback")
    elif args.mode == "patch_repair":
        if not args.mimir_ts:
            print("--mimir-ts required for patch_repair")
            sys.exit(1)
        mimir_entry, prompt = build_patch_repair_prompt(args.league, args.mimir_ts)
        if not prompt:
            print(f"[vidar] no MIMIR entry found for {args.league} @ {args.mimir_ts}")
            sys.exit(1)
    elif args.mode == "deep_dive":
        if not args.topic:
            print("--topic required for deep_dive")
            sys.exit(1)
        prompt = build_deep_dive_prompt(args.league, args.topic)
    else:
        print(f"unknown mode: {args.mode}")
        sys.exit(1)

    print(f"[vidar] firing Opus ({args.mode}, {args.league}) — prompt {len(prompt)} chars")
    try:
        response = call_opus(prompt, api_key)
    except Exception as e:
        tg_send(f"[SYN/VIDAR] API call failed ({args.mode}/{args.league}): {e}")
        raise

    record = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "mode":     args.mode,
        "league":   args.league,
        "topic":    args.topic,
        "revert_ts": args.revert_ts,
        "response": response,
    }
    write_log(record)

    decision = None
    if "```json" in response:
        try:
            json_block = response.split("```json", 1)[1].split("```", 1)[0].strip()
            decision = json.loads(json_block)
        except Exception as e:
            print(f"[vidar] failed to parse decision JSON: {e}")

    if decision:
        decision_record = {
            "ts":        record["ts"],
            "mode":      args.mode,
            "league":    args.league,
            "decision":  decision,
            "log_ref":   record["ts"],
        }
        write_decision(decision_record)

        # patch_repair: if VIDAR produced a valid corrected patch, queue it to LOKI
        if args.mode == "patch_repair" and decision.get("verdict") == "patch_repaired":
            patch = decision.get("patch", [])
            if patch:
                try:
                    queue_entry = {
                        "ts":     record["ts"],
                        "league": args.league,
                        "source": "VIDAR_patch_repair",
                        "mimir_ts": args.mimir_ts,
                        "actions": [{
                            "type":        "structural",
                            "description": decision.get("description", f"VIDAR-repaired patch from MIMIR {args.mimir_ts}"),
                            "patch":       patch,
                        }],
                        "processed": False,
                    }
                    with open(LOKI_PENDING, "a") as f:
                        f.write(json.dumps(queue_entry) + "\n")
                    print(f"[vidar] queued corrected patch to loki_pending_actions.jsonl ({len(patch)} pairs)")
                except Exception as e:
                    print(f"[vidar] failed to queue patch: {e}")
        action = decision.get("recommended_action", "?")
        rationale = decision.get("rationale", "")
        verdict = decision.get("verdict") or decision.get("diagnosis") or ""
        detail_str = f"{args.topic or args.revert_ts or ''}".strip() or f"{args.mode} review"
        write_maintenance(
            args.league, args.mode,
            detail=detail_str,
            result=f"{verdict} -> {action}".strip(" ->"),
            fix_hint=rationale,
        )
        # Telegram ONLY when the decision routes back to Chris. Autonomous
        # actions (patch_repaired, accept_revert, declined-as-not-actionable,
        # keep_pause) are logged to the Maintenance tab and SYN stays silent.
        action_requires_chris = action in ("escalate_chris", "reapply_change")
        if action_requires_chris:
            tg_send(f"[SYN/VIDAR] {args.mode} ({args.league}) NEEDS YOU: {action} — {rationale[:240]}")
    else:
        write_maintenance(
            args.league, args.mode,
            detail=f"{args.topic or args.revert_ts or args.mode}",
            result="completed_no_decision",
            fix_hint="see vidar_log.jsonl",
        )
        # No decision block parsed (typically deep_dive / manual modes). Silent —
        # output is on the Maintenance tab + vidar_log.jsonl.

    print(f"[vidar] done. response {len(response)} chars. decision={bool(decision)}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", required=True,
                   choices=["revert_review", "oscillation_diag", "restructure", "cycle_review", "deep_dive", "patch_repair"])
    p.add_argument("--league", required=True)
    p.add_argument("--revert-ts", default=None, help="for revert_review")
    p.add_argument("--mimir-ts", default=None, help="for patch_repair")
    p.add_argument("--topic", default=None, help="for deep_dive")
    args = p.parse_args()
    api_key = load_anthropic_key()
    run_mode(args, api_key)


if __name__ == "__main__":
    main()
