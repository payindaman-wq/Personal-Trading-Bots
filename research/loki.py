#!/usr/bin/env python3
"""
loki.py — LOKI Implementation Officer (Executive Staff)

Monitors mimir_log.jsonl for new Mimir analyses and automates the relay loop:
1. Confirms program.md was updated by Mimir, git commits it
2. Classifies analysis for code changes to odin_researcher_v2.py
3. Implements safe constant/parameter changes; escalates structural ones
4. Restarts odin service if code changed; reports all actions via Telegram

Runs every 15 minutes via cron.
Usage: python3 research/loki.py [--dry-run]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

WORKSPACE        = "/root/.openclaw/workspace"
RESEARCH         = os.path.join(WORKSPACE, "research")
MIMIR_LOG        = os.path.join(RESEARCH, "mimir_log.jsonl")
LOKI_LOG         = os.path.join(RESEARCH, "loki_log.jsonl")
LOKI_ESC_LOG     = os.path.join(RESEARCH, "loki_escalation_log.jsonl")
RESEARCHER       = os.path.join(RESEARCH, "odin_researcher_v2.py")

ANTHROPIC_SECRET = "/root/.openclaw/secrets/anthropic.json"
ANTHROPIC_MODEL  = "claude-haiku-4-5-20251001"
ANTHROPIC_URL    = "https://api.anthropic.com/v1/messages"

TG_BOT_TOKEN     = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
TG_CHAT_ID       = "8154505910"

DRY_RUN = "--dry-run" in sys.argv

# Keywords that suggest code changes may be needed in odin_researcher_v2.py
CODE_CHANGE_KEYWORDS = [
    "odin_researcher", "MIN_TRADES", "POPULATION_SIZE", "SUSPICIOUS_SHARPE",
    "STALL_ALERT_GENS", "adj_score", "acceptance criteria", "acceptance criterion",
    "effective score", "the code should", "the researcher script",
    "modify the script", "change the constant", "update the constant",
]

# Only these constants can be changed automatically (hard whitelist)
ALLOWED_CONSTANTS = {"MIN_TRADES", "POPULATION_SIZE", "SUSPICIOUS_SHARPE", "STALL_ALERT_GENS"}

# Files LOKI must never touch (block list for extra safety)
BLOCKED_FILES = [
    "competition_tick.py", "swing_competition_tick.py", "arb_competition_tick.py",
    "spread_competition_tick.py", "league_watchdog.py", "sys_heartbeat.py",
    "day_daily_restart.py", "/bots/", "backtest.py",
]


# ── Utilities ─────────────────────────────────────────────────────────────────

def tg_send(text):
    if DRY_RUN:
        print(f"[dry-run TG] {text}")
        return
    try:
        payload = json.dumps({
            "chat_id":    TG_CHAT_ID,
            "text":       text,
            "parse_mode": "HTML",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  [loki] TG send failed: {e}")


def load_anthropic_key():
    with open(ANTHROPIC_SECRET) as f:
        return json.load(f)["anthropic_api_key"]


def call_haiku(prompt):
    api_key = load_anthropic_key()
    payload = json.dumps({
        "model":      ANTHROPIC_MODEL,
        "max_tokens": 500,
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
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"].strip()


# ── State tracking ─────────────────────────────────────────────────────────────

def load_processed():
    """Return set of (ts, league) tuples LOKI has already handled."""
    if not os.path.exists(LOKI_LOG):
        return set()
    processed = set()
    with open(LOKI_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                processed.add((e["mimir_ts"], e["league"]))
            except Exception:
                pass
    return processed


def write_loki_log(mimir_ts, league, actions):
    entry = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "mimir_ts": mimir_ts,
        "league":   league,
        "actions":  actions,
        "dry_run":  DRY_RUN,
    }
    if not DRY_RUN:
        with open(LOKI_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    else:
        print(f"[dry-run] Would log: {json.dumps(entry)}")


def write_escalation_log(mimir_ts, league, gen, description):
    entry = {
        "ts":          datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "mimir_ts":    mimir_ts,
        "league":      league,
        "generation":  gen,
        "description": description,
        "phase":       2,
    }
    if not DRY_RUN:
        with open(LOKI_ESC_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    print(f"  [loki] Phase 2 escalation logged: {description[:80]}")


# ── Git and service operations ─────────────────────────────────────────────────

def git_commit(files, message):
    if DRY_RUN:
        print(f"[dry-run] Would commit {files}: {message}")
        return True
    try:
        subprocess.run(
            ["git", "-C", WORKSPACE, "add"] + files,
            check=True, capture_output=True,
        )
        diff = subprocess.run(
            ["git", "-C", WORKSPACE, "diff", "--cached", "--quiet"],
            capture_output=True,
        )
        if diff.returncode == 0:
            print("  [loki] Nothing staged — no commit needed.")
            return False
        subprocess.run(
            ["git", "-C", WORKSPACE, "commit", "-m", message],
            check=True, capture_output=True,
        )
        print(f"  [loki] Committed: {message}")
        return True
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if e.stderr else str(e)
        print(f"  [loki] git error: {stderr}")
        return False


def restart_service(league):
    service = f"odin_{league}.service"
    if DRY_RUN:
        print(f"[dry-run] Would restart {service}")
        return True
    try:
        subprocess.run(["systemctl", "restart", service], check=True, capture_output=True)
        print(f"  [loki] Restarted {service}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [loki] Failed to restart {service}: {e}")
        return False


# ── Code change detection and application ─────────────────────────────────────

def detect_code_change_keywords(analysis_text):
    """Quick keyword scan — True if analysis likely discusses code changes."""
    text_lower = analysis_text.lower()
    for kw in CODE_CHANGE_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False


def classify_code_change(analysis_text, league):
    """
    Use Haiku to identify specific code change request from Mimir analysis.
    Returns dict with type: "none" | "constant" | "structural"
    """
    prompt = (
        f"Analyze this Mimir crypto strategy research report for code changes "
        f"needed in odin_researcher_v2.py.\n\n"
        f"MIMIR ANALYSIS ({league.upper()}):\n{analysis_text[:3000]}\n\n"
        f"Constants in odin_researcher_v2.py that can be changed:\n"
        f'- MIN_TRADES = {{"day": 50, "swing": 45}}  (minimum trades per strategy)\n'
        f"- POPULATION_SIZE = 10  (elite population size)\n"
        f"- SUSPICIOUS_SHARPE = 3.5  (reject overfitted strategies above this)\n"
        f"- STALL_ALERT_GENS = 300  (alert after N consecutive non-improving gens)\n\n"
        f"Does the analysis request changing one of these constants? Or structural code changes?\n\n"
        f"Output ONLY a JSON object, no explanation:\n"
        f'{{"type": "none"}}\n'
        f'{{"type": "constant", "constant": "MIN_TRADES", "subkey": "day", "new_value": 200, "reason": "..."}}\n'
        f'{{"type": "constant", "constant": "POPULATION_SIZE", "subkey": null, "new_value": 15, "reason": "..."}}\n'
        f'{{"type": "structural", "description": "brief description of structural change needed"}}'
    )
    try:
        response = call_haiku(prompt)
        match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"type": "none"}
    except Exception as e:
        print(f"  [loki] Haiku classification error: {e}")
        return {"type": "none"}


def apply_constant_change(constant, subkey, new_value):
    """
    Apply a simple constant change to odin_researcher_v2.py using regex.
    Returns (success: bool, description: str)
    """
    if constant not in ALLOWED_CONSTANTS:
        return False, f"{constant} not in LOKI allowed-constants whitelist"

    with open(RESEARCHER) as f:
        content = f.read()

    original = content

    if subkey:
        # Dict constant: MIN_TRADES = {"day": 50, "swing": 45}
        pattern = rf'({re.escape(constant)}\s*=\s*\{{[^}}]*"{re.escape(subkey)}"\s*:\s*)\d+'
        replacement = rf'\g<1>{new_value}'
        new_content = re.sub(pattern, replacement, content)
    else:
        # Simple assignment: POPULATION_SIZE = 10
        pattern = rf'^({re.escape(constant)}\s*=\s*)\S+$'
        replacement = rf'\g<1>{new_value}'
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    if new_content == original:
        return False, f"Regex pattern for {constant} not found — no change made"

    if not DRY_RUN:
        backup = RESEARCHER + f".loki_{datetime.now().strftime('%Y%m%d_%H%M')}.bak"
        shutil.copy2(RESEARCHER, backup)
        with open(RESEARCHER, "w") as f:
            f.write(new_content)

    label = f"{constant}[{subkey}]" if subkey else constant
    return True, f"Changed {label} -> {new_value}"


# ── Main processing ────────────────────────────────────────────────────────────

def process_entry(entry):
    ts              = entry.get("ts", "")
    league          = entry.get("league", "")
    gen             = entry.get("generation", "?")
    analysis        = entry.get("analysis", "")
    program_updated = entry.get("program_updated", False)

    league_up = league.upper()
    print(f"\n[loki] MIMIR/{league_up} Gen {gen} ({ts})")
    actions = []

    # Step 1: Commit program.md if Mimir updated it
    program_path = os.path.join(RESEARCH, league, "program.md")
    if program_updated and os.path.exists(program_path):
        rel_path = os.path.relpath(program_path, WORKSPACE)
        committed = git_commit(
            [rel_path],
            f"[loki] MIMIR/{league_up} Gen {gen}: apply program.md update",
        )
        actions.append("program.md committed" if committed else "program.md already committed")
    else:
        print(f"  [loki] program_updated={program_updated} — no program.md commit")

    # Step 2: Check analysis for code changes to odin_researcher_v2.py
    if detect_code_change_keywords(analysis):
        print(f"  [loki] Code change keywords found — classifying with Haiku...")
        change = classify_code_change(analysis, league)
        print(f"  [loki] Classification: {change}")

        if change.get("type") == "constant":
            constant  = change.get("constant", "")
            subkey    = change.get("subkey")
            new_value = change.get("new_value")
            reason    = change.get("reason", "")

            if constant in ALLOWED_CONSTANTS and new_value is not None:
                success, desc = apply_constant_change(constant, subkey, new_value)
                if success:
                    rel_researcher = os.path.relpath(RESEARCHER, WORKSPACE)
                    git_commit(
                        [rel_researcher],
                        f"[loki] MIMIR/{league_up} Gen {gen}: {desc} — {reason[:60]}",
                    )
                    restart_service(league)
                    actions.append(f"code: {desc}")
                else:
                    actions.append(f"code-skip: {desc}")
            else:
                actions.append(f"code-skip: {constant} not in whitelist or value missing")

        elif change.get("type") == "structural":
            desc = change.get("description", "see Mimir analysis")
            write_escalation_log(ts, league, gen, desc)
            actions.append(f"escalated(Phase2): {desc[:60]}")
            tg_send(
                f"<b>[LOKI/{league_up}]</b> Gen {gen} — structural change needed "
                f"(Phase 2 scope). Logged for later.\n<i>{desc[:200]}</i>"
            )
    else:
        print(f"  [loki] No code change keywords — program.md only")

    # Step 3: Summary report (skip if escalation already sent its own message)
    summary = "; ".join(actions) if actions else "no actions taken"
    if not any("escalated" in a for a in actions):
        tg_send(f"<b>[LOKI/{league_up}]</b> Gen {gen} — {summary}")

    write_loki_log(ts, league, actions)


def main():
    if DRY_RUN:
        print("[loki] *** DRY-RUN MODE — no changes will be applied ***")

    if not os.path.exists(MIMIR_LOG):
        print("[loki] No mimir_log.jsonl — nothing to do")
        return

    processed = load_processed()

    new_entries = []
    with open(MIMIR_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            key = (entry.get("ts", ""), entry.get("league", ""))
            if key not in processed:
                new_entries.append(entry)

    if not new_entries:
        print("[loki] No new Mimir entries.")
        return

    count = len(new_entries)
    print(f"[loki] {count} new Mimir {'entry' if count == 1 else 'entries'} to process")

    for entry in new_entries:
        try:
            process_entry(entry)
        except Exception as e:
            league = entry.get("league", "?").upper()
            gen    = entry.get("generation", "?")
            print(f"  [loki] ERROR on MIMIR/{league} Gen {gen}: {e}")
            tg_send(f"<b>[LOKI ERROR]</b> MIMIR/{league} Gen {gen}: {e}")
            # Still mark processed to prevent infinite error loop
            write_loki_log(entry.get("ts", ""), entry.get("league", ""), [f"ERROR: {e}"])


if __name__ == "__main__":
    main()
