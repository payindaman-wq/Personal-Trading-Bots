#!/usr/bin/env python3
"""
weekly_league_restart.py - Sunday 09:00 UTC restart for Swing, Arb, Spread leagues.

Called by cron: 0 9 * * 0

Directly archives active sprints (via league tick scripts) then starts new ones,
patching started_at to exactly 09:00:00 UTC so all countdown timers align.
"""
import os, sys, json, shutil, argparse, subprocess
from datetime import datetime, timezone, timedelta

WORKSPACE = "/root/.openclaw/workspace"

ODIN_SWING_BEST    = os.path.join(WORKSPACE, "research", "swing", "best_strategy.yaml")
AUTOBOTSWING_STRAT = os.path.join(WORKSPACE, "fleet", "swing", "autobotswing", "strategy.yaml")

FREYA_BEST         = os.path.join(WORKSPACE, "research", "pm", "best_strategy.yaml")
PM_FLEET_DIR       = os.path.join(WORKSPACE, "fleet", "polymarket")
FREYA_SLOTS        = ["mist", "kara", "thrud"]

PM_PERSONAS = {
    "sports":       "You are a sports analytics expert specializing in predicting sporting event outcomes. You analyze team form, head-to-head records, player availability, and situational factors to estimate probabilities.",
    "politics":     "You are a political analyst specializing in predicting electoral and policy outcomes. You analyze polling trends, endorsements, historical patterns, and political dynamics.",
    "crypto":       "You are a cryptocurrency analyst specializing in predicting crypto-related outcomes. You analyze market data, technical indicators, project fundamentals, and news sentiment.",
    "economics":    "You are an economic data analyst specializing in predicting macroeconomic outcomes. You analyze economic indicators, central bank signals, consensus estimates, and historical release patterns.",
    "world_events": "You are a global events analyst specializing in predicting world news outcomes. You analyze geopolitical dynamics, historical precedents, news coverage, and expert consensus to estimate probabilities.",
}

LEAGUES = {
    "swing": {
        "active_dir":   os.path.join(WORKSPACE, "competition", "swing", "active"),
        "tick_script":  os.path.join(WORKSPACE, "swing_competition_tick.py"),
        "start_script": os.path.join(WORKSPACE, "swing_competition_start.py"),
        "start_args":   ["168"],
    },
    "arb": {
        "active_dir":   os.path.join(WORKSPACE, "competition", "arb", "active"),
        "tick_script":  os.path.join(WORKSPACE, "arb_competition_tick.py"),
        "start_script": os.path.join(WORKSPACE, "arb_competition_start.py"),
        "start_args":   [],
    },
    "spread": {
        "active_dir":   os.path.join(WORKSPACE, "competition", "spread", "active"),
        "tick_script":  os.path.join(WORKSPACE, "spread_competition_tick.py"),
        "start_script": os.path.join(WORKSPACE, "spread_competition_start.py"),
        "start_args":   ["168"],
    },
}

POLYMARKET_AUTO_STATE = os.path.join(WORKSPACE, "competition", "polymarket", "auto_state.json")

CYCLE_STATE_FILES = {
    "swing":  os.path.join(WORKSPACE, "competition", "swing", "swing_cycle_state.json"),
    "arb":    os.path.join(WORKSPACE, "competition", "arb",   "arb_cycle_state.json"),
    "spread": os.path.join(WORKSPACE, "competition", "spread","spread_cycle_state.json"),
}


def inject_odin_swing_strategy(dry_run=False):
    if not os.path.exists(ODIN_SWING_BEST):
        print("  [odin-swing] No best_strategy.yaml yet — AutoBotSwing keeps current strategy.")
        return
    if not dry_run:
        shutil.copy2(ODIN_SWING_BEST, AUTOBOTSWING_STRAT)
    print("  [odin-swing] Injected best swing strategy -> " + AUTOBOTSWING_STRAT)


def inject_freya_strategy(dry_run=False):
    """Apply FREYA best_strategy.yaml to the three FREYA research slots (mist/kara/thrud)."""
    if not os.path.exists(FREYA_BEST):
        print("  [freya] No best_strategy.yaml yet — FREYA slots stay disabled.")
        return
    try:
        import yaml
    except ImportError:
        print("  [freya] PyYAML not available — skipping injection.")
        return

    with open(FREYA_BEST) as f:
        best = yaml.safe_load(f)

    cat     = best.get("category", "world_events")
    persona = PM_PERSONAS.get(cat, PM_PERSONAS["world_events"])

    for i, bot_name in enumerate(FREYA_SLOTS):
        strat_path = os.path.join(PM_FLEET_DIR, bot_name, "strategy.yaml")
        if not os.path.exists(os.path.dirname(strat_path)):
            print(f"  [freya] {bot_name}: fleet dir missing — skipping")
            continue

        # Build full strategy from research params
        strategy = {
            "name":           bot_name,
            "category":       cat,
            "type":           "opinion",
            "description":    f"FREYA research slot — gen {best.get('_gen', '?')} evolved strategy",
            "prompt_persona": persona,
            "market_filter": {
                "include_keywords": list(best.get("include_keywords", [])),
                "exclude_keywords": list(best.get("exclude_keywords", [])),
                "price_range":      list(best.get("price_range", [0.05, 0.90])),
                "min_liquidity_usd": best.get("min_liquidity_usd", 500),
                "max_days_to_resolve": best.get("max_days_to_resolve", 30),
            },
            "edge": {
                "min_edge_pts":    best.get("min_edge_pts", 0.08),
                "min_confidence":  "medium",
                "max_positions":   8,
                "max_position_pct": best.get("max_position_pct", 0.10),
            },
            "risk": {
                "stop_if_down_pct": 20,
                "starting_capital": 1000.0,
            },
        }
        # Slight variation per slot: kara gets tighter edge, thrud gets wider
        if i == 1:   # kara — conservative variant
            strategy["edge"]["min_edge_pts"] = round(
                min(0.25, best.get("min_edge_pts", 0.08) + 0.03), 3)
        elif i == 2:  # thrud — aggressive variant
            strategy["edge"]["min_edge_pts"] = round(
                max(0.03, best.get("min_edge_pts", 0.08) - 0.02), 3)

        if not dry_run:
            with open(strat_path, "w") as f:
                yaml.dump(strategy, f, default_flow_style=False, allow_unicode=True)
        print(f"  [freya] Injected strategy -> {bot_name} "
              f"(cat={cat}, edge={strategy['edge']['min_edge_pts']})")


def find_active_meta(active_dir):
    if not os.path.isdir(active_dir):
        return None, None
    entries = sorted(os.listdir(active_dir))
    if not entries:
        return None, None
    comp_dir  = os.path.join(active_dir, entries[-1])
    meta_path = os.path.join(comp_dir, "meta.json")
    if not os.path.isfile(meta_path):
        return None, None
    with open(meta_path) as f:
        meta = json.load(f)
    return (comp_dir, meta) if meta.get("status") == "active" else (None, None)


def register_new_sprint_in_cycle(league, comp_id, active_dir):
    """Register a newly started sprint in the cycle state and stamp meta.json.

    Called immediately after each new sprint starts so sprint_in_cycle is always
    correct — including while the sprint is still live, not just after it ends.
    """
    cs_path = CYCLE_STATE_FILES.get(league)
    if not cs_path:
        return

    try:
        with open(cs_path) as f:
            cs = json.load(f)
    except Exception:
        cs = {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4,
              "status": "active", "sprints": []}

    if comp_id not in cs.get("sprints", []):
        cs.setdefault("sprints", []).append(comp_id)
    cs["sprint_in_cycle"] = len(cs["sprints"])

    with open(cs_path, "w") as f:
        json.dump(cs, f, indent=2)

    # Stamp cycle + sprint_in_cycle into meta.json
    meta_path = os.path.join(active_dir, comp_id, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
        meta["cycle"]          = cs.get("cycle", 1)
        meta["sprint_in_cycle"] = cs["sprint_in_cycle"]
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

    print(f"  [{league.upper()}] Cycle {cs.get('cycle',1)}, Sprint {cs['sprint_in_cycle']}/{cs.get('sprints_per_cycle',4)} registered in cycle state.")


def expire_and_archive(league, cfg, now, dry_run):
    """
    Expire and archive the active sprint directly via the league's tick script.
    Returns True if we should proceed to start a new sprint, False to skip.
    """
    comp_dir, meta = find_active_meta(cfg["active_dir"])
    if not meta:
        print(f"  [{league.upper()}] No active sprint — will start fresh.")
        return True

    started = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    hrs     = (now - started).total_seconds() / 3600

    if hrs < 24:
        print(f"  [{league.upper()}] Sprint only {hrs:.1f}h old — skipping.")
        return False

    print(f"  [{league.upper()}] Sprint {hrs:.1f}h old — expiring and archiving...")

    if dry_run:
        print(f"  [{league.upper()}] [DRY RUN] Would archive {meta['comp_id']}")
        return True

    # Patch duration_hours so the tick script detects expiry
    meta["duration_hours"] = round(hrs - 0.01, 4)
    with open(os.path.join(comp_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    # Call tick script — it detects expiry, closes positions at current prices, archives
    result = subprocess.run(
        ["python3", cfg["tick_script"]],
        capture_output=True, text=True, cwd=WORKSPACE,
    )
    if result.returncode == 0:
        output = result.stdout.strip()
        if output:
            print("    " + "\n    ".join(output.splitlines()))
        return True
    else:
        print(f"  [{league.upper()}] ERROR archiving: {result.stderr[:300]}")
        return False


def start_new_sprint(league, cfg, target_ts, dry_run):
    """Start a new sprint and patch started_at to target_ts."""
    if dry_run:
        print(f"  [{league.upper()}] [DRY RUN] Would start new sprint, timestamp -> {target_ts}")
        return

    cmd    = ["python3", cfg["start_script"]] + cfg["start_args"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    if result.returncode != 0:
        print(f"  [{league.upper()}] ERROR starting: {result.stderr[:300]}")
        return

    data    = json.loads(result.stdout)
    comp_id = data["comp_id"]
    print(f"  [{league.upper()}] Started: {comp_id}")

    # Patch started_at in meta.json to exact 09:00:00 UTC
    meta_path = os.path.join(cfg["active_dir"], comp_id, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
        meta["started_at"] = target_ts
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"  [{league.upper()}] Patched started_at -> {target_ts}")

    register_new_sprint_in_cycle(league, comp_id, cfg["active_dir"])


parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

now       = datetime.now(timezone.utc)
target_ts = now.replace(hour=9, minute=0, second=0, microsecond=0).isoformat()
print("weekly_league_restart @ " + now.strftime("%Y-%m-%d %H:%M UTC"))
print(f"  Target start timestamp: {target_ts}")

for league, cfg in LEAGUES.items():
    archived = expire_and_archive(league, cfg, now, args.dry_run)
    if archived:
        if league == "swing":
            inject_odin_swing_strategy(args.dry_run)
        start_new_sprint(league, cfg, target_ts, args.dry_run)

# Polymarket: expire + immediate service restart so tick fires now
try:
    with open(POLYMARKET_AUTO_STATE) as f:
        state = json.load(f)
    sprint_start = state.get("sprint_started_at", "")
    if sprint_start:
        started_dt = datetime.fromisoformat(sprint_start.replace("Z", "+00:00"))
        hrs        = (now - started_dt).total_seconds() / 3600
        if hrs < 24:
            print(f"  [POLYMARKET] Sprint only {hrs:.1f}h old — skipping.")
        else:
            inject_freya_strategy(args.dry_run)
            if not args.dry_run:
                state["sprint_ends_at"] = (now - timedelta(seconds=1)).isoformat()
                with open(POLYMARKET_AUTO_STATE, "w") as f:
                    json.dump(state, f, indent=2)
                subprocess.run(["systemctl", "restart", "polymarket_syn.service"],
                               capture_output=True)
            print(f"  [POLYMARKET] Expired after {hrs:.1f}h. Service restarted.")
except Exception as e:
    print("  [POLYMARKET] Error: " + str(e))

print("Done.")
