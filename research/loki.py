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
import yaml
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
FREYA_RESEARCHER = os.path.join(RESEARCH, "freya_researcher.py")
PM_RESEARCH_DIR  = os.path.join(RESEARCH, "pm")
PM_FLEET_DIR     = os.path.join(WORKSPACE, "fleet", "polymarket")

FREYA_SLOTS = ["mist", "kara", "thrud"]
PM_PERSONAS = {
    "sports":       "You are a sports analytics expert specializing in predicting sporting event outcomes.",
    "politics":     "You are a political analyst specializing in predicting electoral and policy outcomes.",
    "crypto":       "You are a cryptocurrency analyst specializing in predicting crypto-related outcomes.",
    "economics":    "You are an economic data analyst specializing in predicting macroeconomic outcomes.",
    "world_events": "You are a global events analyst specializing in predicting world news outcomes.",
}

GEMINI_SECRET = "/root/.openclaw/secrets/gemini.json"
GEMINI_MODEL  = "gemini-2.5-flash-lite"
GEMINI_BASE   = "https://generativelanguage.googleapis.com/v1beta/models"

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
ALLOWED_CONSTANTS      = {"MIN_TRADES", "POPULATION_SIZE", "SUSPICIOUS_SHARPE", "STALL_ALERT_GENS"}
FREYA_ALLOWED_CONSTS   = {"MIN_BETS", "POPULATION_SIZE"}  # STALL_ALERT_GENS excluded: freya_researcher.py must never have Telegram stall alerts

PM_CODE_CHANGE_KEYWORDS = [
    "freya_researcher", "MIN_BETS", "POPULATION_SIZE",
    "change the constant", "update the constant", "the code should",
    "modify the script", "the researcher script",
]

# Files LOKI must never touch (block list for extra safety)
BLOCKED_FILES = [
    "competition_tick.py", "swing_competition_tick.py", "arb_competition_tick.py",
    "spread_competition_tick.py", "league_watchdog.py", "sys_heartbeat.py",
    "day_daily_restart.py", "/bots/", "backtest.py",
]


# ── Utilities ─────────────────────────────────────────────────────────────────

def tg_send(text, severity="warning"):
    """Route to SYN inbox - never directly to Telegram. SYN decides what reaches the user."""
    inbox = os.path.join(WORKSPACE, "syn_inbox.jsonl")
    entry = json.dumps({"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
                        "source": "loki", "severity": severity, "msg": text})
    try:
        with open(inbox, "a") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"  [loki] inbox write failed: {e}")
    if DRY_RUN:
        print(f"[dry-run SYN-inbox/{severity}] {text}")


def load_gemini_key():
    with open(GEMINI_SECRET) as f:
        data = json.load(f)
    return data.get("gemini_api_key") or data["gemini_api_keys"][0]


def call_gemini(prompt):
    api_key = load_gemini_key()
    url = f"{GEMINI_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 500, "temperature": 0.1},
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


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


def write_loki_log(mimir_ts, league, gen, actions):
    entry = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "mimir_ts": mimir_ts,
        "league":   league,
        "gen":      gen,
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
        response = call_gemini(prompt)
        match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"type": "none"}
    except Exception as e:
        print(f"  [loki] Gemini classification error: {e}")
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


# ── PM-specific helpers ───────────────────────────────────────────────────────

def classify_freya_change(analysis_text):
    """Use Haiku to identify constant changes needed in freya_researcher.py."""
    prompt = (
        "Analyze this Mimir prediction markets research report for code changes "
        "needed in freya_researcher.py.\n\n"
        f"MIMIR ANALYSIS:\n{analysis_text[:3000]}\n\n"
        "Constants in freya_researcher.py that can be changed:\n"
        "- MIN_BETS = 20  (minimum bets required for valid simulation)\n"
        "- POPULATION_SIZE = 5  (elite population size)\n"
        "CRITICAL: freya_researcher.py must have ZERO tg_send() call sites. tg_send() in research scripts routes to SYN inbox only."
        "Does the analysis request changing one of these constants?\n\n"
        "Output ONLY a JSON object:\n"
        '{"type": "none"}\n'
        '{"type": "constant", "constant": "MIN_BETS", "subkey": null, "new_value": 30, "reason": "..."}\n'
        '{"type": "structural", "description": "brief description"}'
    )
    try:
        response = call_gemini(prompt)
        match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"type": "none"}
    except Exception as e:
        print(f"  [loki] Gemini PM classification error: {e}")
        return {"type": "none"}


def apply_freya_constant(constant, new_value):
    """Apply a simple constant change to freya_researcher.py."""
    if constant not in FREYA_ALLOWED_CONSTS:
        return False, f"{constant} not in FREYA allowed-constants whitelist"
    with open(FREYA_RESEARCHER) as f:
        content = f.read()
    original = content
    pattern  = rf'^({re.escape(constant)}\s*=\s*)\S+$'
    new_content = re.sub(pattern, rf'\g<1>{new_value}', content, flags=re.MULTILINE)
    if new_content == original:
        return False, f"Regex pattern for {constant} not found — no change made"
    if not DRY_RUN:
        backup = FREYA_RESEARCHER + f".loki_{datetime.now().strftime('%Y%m%d_%H%M')}.bak"
        shutil.copy2(FREYA_RESEARCHER, backup)
        with open(FREYA_RESEARCHER, "w") as f:
            f.write(new_content)
    return True, f"Changed {constant} -> {new_value}"



def loki_inject_freya_strategy(gen):
    """Inject current FREYA best_strategy into mist/kara/thrud at every Mimir milestone."""
    best_path = os.path.join(PM_RESEARCH_DIR, "best_strategy.yaml")
    if not os.path.exists(best_path):
        print("  [loki] inject: no best_strategy.yaml yet — skipping")
        return []

    with open(best_path) as f:
        best = yaml.safe_load(f)

    cat     = best.get("category", "world_events")
    persona = PM_PERSONAS.get(cat, PM_PERSONAS["world_events"])
    injected = []

    for i, bot_name in enumerate(FREYA_SLOTS):
        strat_path = os.path.join(PM_FLEET_DIR, bot_name, "strategy.yaml")
        if not os.path.exists(os.path.dirname(strat_path)):
            print("  [loki] inject: " + bot_name + " fleet dir missing — skipping")
            continue

        edge_base = best.get("min_edge_pts", 0.08)
        if i == 1:
            edge = round(min(0.25, edge_base + 0.03), 3)   # kara: conservative
        elif i == 2:
            edge = round(max(0.03, edge_base - 0.02), 3)   # thrud: aggressive
        else:
            edge = edge_base                                # mist: exact champion

        strategy = {
            "name":           bot_name,
            "category":       cat,
            "type":           "opinion",
            "description":    "FREYA research slot — gen " + str(gen) + " evolved strategy",
            "prompt_persona": persona,
            "market_filter": {
                "include_keywords":    list(best.get("include_keywords", [])),
                "exclude_keywords":    list(best.get("exclude_keywords", [])),
                "price_range":         list(best.get("price_range", [0.05, 0.90])),
                "min_liquidity_usd":   best.get("min_liquidity_usd", 500),
                "max_days_to_resolve": best.get("max_days_to_resolve", 30),
            },
            "edge": {
                "min_edge_pts":     edge,
                "min_confidence":   "medium",
                "max_positions":    8,
                "max_position_pct": best.get("max_position_pct", 0.10),
            },
            "risk": {
                "stop_if_down_pct": 20,
                "starting_capital": 1000.0,
            },
        }

        if not DRY_RUN:
            with open(strat_path, "w") as f:
                yaml.dump(strategy, f, default_flow_style=False, allow_unicode=True)

        print("  [loki] inject: " + bot_name + " <- gen " + str(gen) + " champion (cat=" + cat + ", edge=" + str(edge) + ")")
        injected.append(bot_name)

    if injected and not DRY_RUN:
        rel_paths = [os.path.relpath(os.path.join(PM_FLEET_DIR, b, "strategy.yaml"), WORKSPACE)
                     for b in injected]
        git_commit(rel_paths, "[loki] MIMIR/PM Gen " + str(gen) + ": inject FREYA champion -> " + ", ".join(injected))

    return injected

def process_pm_entry(entry):
    """Handle PM league Mimir entries."""
    ts              = entry.get("ts", "")
    gen             = entry.get("generation", "?")
    analysis        = entry.get("analysis", "")
    program_updated = entry.get("program_updated", False)
    actions         = []

    print(f"\n[loki] MIMIR/PM Gen {gen} ({ts})")

    # Step 1: Commit program.md
    program_path = os.path.join(PM_RESEARCH_DIR, "program.md")
    if program_updated and os.path.exists(program_path):
        rel_path  = os.path.relpath(program_path, WORKSPACE)
        committed = git_commit(
            [rel_path],
            f"[loki] MIMIR/PM Gen {gen}: apply program.md update",
        )
        actions.append("pm/program.md committed" if committed else "pm/program.md already committed")
    else:
        print(f"  [loki] program_updated={program_updated} — no program.md commit")

    # Step 2: Check for freya_researcher.py constant changes
    text_lower = analysis.lower()
    has_code_kw = any(kw.lower() in text_lower for kw in PM_CODE_CHANGE_KEYWORDS)
    if has_code_kw:
        print(f"  [loki] PM code change keywords found — classifying...")
        change = classify_freya_change(analysis)
        print(f"  [loki] PM classification: {change}")
        if change.get("type") == "constant":
            constant  = change.get("constant", "")
            new_value = change.get("new_value")
            reason    = change.get("reason", "")
            if constant in FREYA_ALLOWED_CONSTS and new_value is not None:
                success, desc = apply_freya_constant(constant, new_value)
                if success:
                    rel_freya = os.path.relpath(FREYA_RESEARCHER, WORKSPACE)
                    git_commit(
                        [rel_freya],
                        f"[loki] MIMIR/PM Gen {gen}: {desc} — {reason[:60]}",
                    )
                    if not DRY_RUN:
                        try:
                            subprocess.run(["systemctl", "restart", "freya.service"],
                                           check=True, capture_output=True)
                            print("  [loki] Restarted freya.service")
                        except Exception as e:
                            print(f"  [loki] freya.service restart failed: {e}")
                    actions.append(f"freya_code: {desc}")
                else:
                    actions.append(f"freya_code-skip: {desc}")
        elif change.get("type") == "structural":
            desc = change.get("description", "see Mimir analysis")
            write_escalation_log(ts, "pm", gen, desc)
            actions.append(f"escalated(Phase2): {desc[:60]}")
    else:
        print(f"  [loki] No PM code change keywords — program.md only")

    # Step 3: Inject current best strategy into mist/kara/thrud
    injected = loki_inject_freya_strategy(gen)
    if injected:
        actions.append("freya_inject: " + ", ".join(injected))
    else:
        actions.append("freya_inject: skipped")

    write_loki_log(ts, "pm", gen, actions)


# ── Main processing ────────────────────────────────────────────────────────────

def process_entry(entry):
    league = entry.get("league", "")
    if league == "pm":
        process_pm_entry(entry)
        return
    # futures leagues handled same as spot leagues below

    ts              = entry.get("ts", "")
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
            print(f"  [loki] Structural change logged to escalation log — visible in dashboard")
    else:
        print(f"  [loki] No code change keywords — program.md only")

    write_loki_log(ts, league, gen, actions)


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
            # Still mark processed to prevent infinite error loop
            write_loki_log(entry.get("ts", ""), entry.get("league", ""), entry.get("generation", "?"), [f"ERROR: {e}"])


if __name__ == "__main__":
    main()
