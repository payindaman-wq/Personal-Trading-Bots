#!/usr/bin/env python3
"""
spread_cycle_advance.py — End-of-cycle automation for the Spread League.

Run manually after the last sprint of a cycle completes. Does:
  1. Runs fresh cointegration health check
  2. RETIRE pairs: auto-replaces with best available candidate (updates strategy.yaml)
  3. WEAK pairs:   tracks strike count — replaces on 2nd consecutive weak cycle
  4. Archives cycle results, advances cycle counter
  5. Sends Telegram summary of what changed

Usage: python3 spread_cycle_advance.py [--dry-run]
"""
import argparse, json, os, shutil, sys, urllib.request
from datetime import datetime, timezone

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("WARNING: pyyaml not installed — strategy.yaml updates disabled", file=sys.stderr)

WORKSPACE   = "/root/.openclaw/workspace"
FLEET_DIR   = os.path.join(WORKSPACE, "fleet", "spread")
RESULTS_DIR = os.path.join(WORKSPACE, "competition", "spread", "results")
ARCHIVE_DIR = os.path.join(WORKSPACE, "competition", "spread", "archive")
CYCLE_STATE = os.path.join(WORKSPACE, "competition", "spread", "spread_cycle_state.json")
COINT_RPT   = os.path.join(WORKSPACE, "competition", "spread", "cointegration_report.json")

BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
CHAT_ID   = "8154505910"


# ── Helpers ──────────────────────────────────────────────────────────────────

def tg_send(msg):
    try:
        data = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req  = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  [tg] failed: {e}")


def load_cycle_state():
    if os.path.isfile(CYCLE_STATE):
        with open(CYCLE_STATE) as f:
            return json.load(f)
    return {
        "cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4,
        "status": "active", "weak_strikes": {},
    }


def save_cycle_state(state):
    os.makedirs(os.path.dirname(CYCLE_STATE), exist_ok=True)
    with open(CYCLE_STATE, "w") as f:
        json.dump(state, f, indent=2)


def load_bot_pairs():
    """Return {bot: analysis_pair} from strategy.yaml files."""
    result = {}
    if not os.path.isdir(FLEET_DIR) or not HAS_YAML:
        return result
    for bot in os.listdir(FLEET_DIR):
        path = os.path.join(FLEET_DIR, bot, "strategy.yaml")
        if not os.path.isfile(path):
            continue
        try:
            with open(path) as f:
                d = yaml.safe_load(f)
            sp = d.get("spread", {})
            result[bot] = sp.get("analysis_pair", "")
        except Exception:
            pass
    return result


def update_bot_pair(bot, new_base, new_quote, dry_run=False):
    """Update a bot's strategy.yaml with a new pair. Returns True on success."""
    if not HAS_YAML:
        return False
    path = os.path.join(FLEET_DIR, bot, "strategy.yaml")
    if not os.path.isfile(path):
        return False
    try:
        with open(path) as f:
            d = yaml.safe_load(f)
        base_sym  = new_base.replace("/USD", "")
        quote_sym = new_quote.replace("/USD", "")
        analysis  = f"{base_sym}_{quote_sym}_RATIO"
        d.setdefault("spread", {})
        d["spread"]["base"]          = new_base
        d["spread"]["quote"]         = new_quote
        d["spread"]["analysis_pair"] = analysis
        if not dry_run:
            with open(path, "w") as f:
                yaml.dump(d, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"  ERROR updating {bot} strategy.yaml: {e}")
        return False


def pair_display(base, quote):
    return f"{base.replace('/USD','')}/{quote.replace('/USD','')}"


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making changes")
    args = parser.parse_args()
    dry  = args.dry_run

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"\n{'='*60}")
    print(f"  SPREAD CYCLE ADVANCE  |  {now_str}")
    if dry:
        print("  DRY RUN — no changes will be made")
    print(f"{'='*60}\n")

    # ── 1. Run fresh cointegration check ─────────────────────────────────
    print("Running cointegration health check...")
    sys.path.insert(0, WORKSPACE)
    try:
        import spread_cointegration_check
        report = spread_cointegration_check.run()
    except Exception as e:
        print(f"  ERROR running check: {e}")
        print("  Attempting to load existing report...")
        if not os.path.isfile(COINT_RPT):
            print("  No report found — aborting.")
            sys.exit(1)
        with open(COINT_RPT) as f:
            report = json.load(f)

    summary    = report.get("summary", {})
    candidates = report.get("candidates", [])
    retire     = summary.get("retire", [])
    weak       = summary.get("weak", [])
    strong     = summary.get("strong", [])

    # ── 2. Load state and bot assignments ────────────────────────────────
    cycle_state  = load_cycle_state()
    old_cycle    = cycle_state.get("cycle", 1)
    weak_strikes = cycle_state.setdefault("weak_strikes", {})

    bot_pairs    = load_bot_pairs()   # {bot: analysis_pair}
    pair_to_bots = {}                 # {analysis_pair: [bot, ...]}
    for bot, ap in bot_pairs.items():
        pair_to_bots.setdefault(ap, []).append(bot)

    # Track which pairs are already in use (by base/quote) to avoid duplicate assignments
    active_pairs_data = report.get("active_pairs", {})
    used_pairs = set()
    for ap, r in active_pairs_data.items():
        used_pairs.add((r.get("base", ""), r.get("quote", "")))

    changes = []   # list of (bot, old_pair, new_pair, reason)

    def assign_replacement(bots_to_replace, reason):
        for cand in candidates:
            b, q = cand.get("base", ""), cand.get("quote", "")
            if (b, q) in used_pairs:
                continue
            if cand.get("verdict") not in ("STRONG", "WATCH"):
                continue
            used_pairs.add((b, q))
            pair_str = pair_display(b, q)
            for bot in bots_to_replace:
                old_ap = bot_pairs.get(bot, "?")
                print(f"  REPLACE {bot}: {old_ap} -> {pair_str}  [{reason}]")
                if not dry:
                    update_bot_pair(bot, b, q)
                changes.append((bot, old_ap, pair_str, reason))
            return pair_str
        print(f"  WARNING: no suitable replacement found for {bots_to_replace}")
        return None

    # ── 3. Handle RETIRE pairs ───────────────────────────────────────────
    print(f"RETIRE pairs: {retire if retire else 'none'}")
    for ap in retire:
        bots = pair_to_bots.get(ap, [])
        if bots:
            assign_replacement(bots, "RETIRE")
        weak_strikes.pop(ap, None)

    # ── 4. Handle WEAK pairs (second-strike rule) ────────────────────────
    print(f"WEAK pairs:   {weak if weak else 'none'}")
    for ap in weak:
        strikes = weak_strikes.get(ap, 0) + 1
        if strikes >= 2:
            bots = pair_to_bots.get(ap, [])
            print(f"  {ap}: strike {strikes} — auto-retiring")
            if bots:
                assign_replacement(bots, f"WEAK x{strikes}")
            weak_strikes.pop(ap, None)
        else:
            weak_strikes[ap] = strikes
            print(f"  {ap}: strike {strikes}/2 — watching, no change this cycle")

    # Clear strikes for pairs that recovered
    for ap in list(weak_strikes.keys()):
        if ap not in weak and ap not in retire:
            print(f"  {ap}: recovered — clearing strike history")
            del weak_strikes[ap]

    # ── 5. Archive cycle results ─────────────────────────────────────────
    print(f"\nArchiving Cycle {old_cycle} results...")
    archive_dest = os.path.join(ARCHIVE_DIR, f"cycle-{old_cycle}")
    if not dry and os.path.isdir(RESULTS_DIR) and os.listdir(RESULTS_DIR):
        os.makedirs(archive_dest, exist_ok=True)
        for entry in os.listdir(RESULTS_DIR):
            shutil.move(os.path.join(RESULTS_DIR, entry),
                        os.path.join(archive_dest, entry))
        print(f"  Archived to {archive_dest}")
    elif dry:
        print(f"  [dry] would archive to {archive_dest}")
    else:
        print(f"  Nothing to archive (results dir empty)")

    # ── 6. Advance cycle state ───────────────────────────────────────────
    new_cycle = old_cycle + 1
    cycle_state["cycle"]            = new_cycle
    cycle_state["sprint_in_cycle"]  = 0
    cycle_state["status"]           = "active"
    cycle_state["cycle_started_at"] = None
    cycle_state["sprints"]          = []
    cycle_state["weak_strikes"]     = weak_strikes

    if not dry:
        save_cycle_state(cycle_state)

    print(f"Cycle advanced: {old_cycle} -> {new_cycle}")

    # ── 7. Telegram summary ──────────────────────────────────────────────
    lines = [f"<b>Spread League — Cycle {old_cycle} Complete</b>",
             f"Pair health: {len(strong)} STRONG | {len(weak)} WEAK | {len(retire)} RETIRE"]

    if changes:
        lines.append(f"\nPair changes for Cycle {new_cycle}:")
        for bot, old_ap, new_pair, reason in changes:
            lines.append(f"  {bot}: {old_ap} -> {new_pair} ({reason})")
    else:
        lines.append("No pair changes — all active pairs healthy.")

    watching = [(ap, weak_strikes[ap]) for ap in weak if ap in weak_strikes]
    if watching:
        lines.append("\nWatching (replace if WEAK again next cycle):")
        for ap, s in watching:
            bots = pair_to_bots.get(ap, [])
            lines.append(f"  {ap} [{', '.join(bots)}] — strike {s}/2")

    lines.append(f"\nStart Cycle {new_cycle} sprint 1:")
    lines.append(f"python3 spread_competition_start.py --cycle {new_cycle} --sprint-in-cycle 1")

    msg = "\n".join(lines)
    print(f"\n{msg}")
    if not dry:
        tg_send(msg)

    print(f"\n{'='*60}")
    print(f"  {'DRY RUN complete — no files modified.' if dry else f'Cycle {new_cycle} ready. Start the first sprint to begin.'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
