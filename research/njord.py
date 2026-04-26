#!/usr/bin/env python3
"""
njord.py - Capital Allocation Officer.

Reads from Kraken (or paper mock), discovers the bot fleet under
fleet/<league>/<bot>/strategy.yaml, computes target allocations from
config.njord.league_weights, and emits per-bot actions through a
Tier 1/2/3 review gate (reuses research/vidar_tier.classify_finding for
classification, falls back to a built-in action-type table when no
Anthropic key is configured).

Disabled by default - the officer is a framework primitive that activates
when a downstream user funds a real account. Activation flow:

  1. Edit config.yaml: set njord.enabled = true. Keep mode: "paper".
  2. Add the cron line from docs/njord.md.
  3. Run for at least one week. Review competition/njord.log.
  4. Switch njord.mode to "live" only after paper validation.

CLI:
  python3 njord.py run            one cycle (called from cron */30)
  python3 njord.py status         print current allocation table
  python3 njord.py revert <fid>   revert a tier-2 pending action

Tier 3 actions never execute - they write to syn_inbox.jsonl with
severity=critical and tg_allowed=true, and sys_heartbeat surfaces them
to Telegram via TG_ALLOWED_SOURCES = {"njord", ...}.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESEARCH  = os.path.join(WORKSPACE, "research")
COMP      = os.path.join(WORKSPACE, "competition")
FLEET_DIR = os.path.join(WORKSPACE, "fleet")

ALLOC_PATH     = os.path.join(COMP, "njord_allocation.json")
PENDING_REVIEW = os.path.join(COMP, "njord_pending_review.flag")
NJORD_LOG      = os.path.join(COMP, "njord.log")
SYN_INBOX      = os.path.join(WORKSPACE, "syn_inbox.jsonl")

TIER2_REVIEW_DEADLINE_HR = 24

# Static fallback when vidar_tier is unreachable (no Anthropic key, network
# down, NJORD_NO_LLM_CLASSIFY set). Source of truth for known action types.
_NJORD_TIER_FALLBACK = {
    "rebalance":           "tier1",
    "pause_bot":           "tier1",
    "wake_bot":            "tier2",
    "shift_league_weight": "tier2",
    "reduce_total":        "tier2",
    "wallet_op":           "tier3",
    "key_change":          "tier3",
    "retire_league":       "tier3",
    "total_change_25pct":  "tier3",
}


def _ts_iso():
    return datetime.now(timezone.utc).isoformat()


def _ts_short():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")


def _log(line):
    os.makedirs(os.path.dirname(NJORD_LOG), exist_ok=True)
    try:
        with open(NJORD_LOG, "a") as f:
            f.write("[" + _ts_short() + "] " + line + "\n")
    except OSError:
        pass


def _atomic_write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _append_jsonl(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(obj) + "\n")


def _load_json_or(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


# fleet discovery
def discover_fleet(leagues_enabled, fleet_root=None):
    """Return ({league: [bot_names]}, {bot_name: league})."""
    fleet_root = fleet_root or FLEET_DIR
    bots_per_league = {}
    bot_to_league = {}
    for league in leagues_enabled:
        league_dir = os.path.join(fleet_root, league)
        bots = []
        if os.path.isdir(league_dir):
            for entry in sorted(os.listdir(league_dir)):
                if entry.startswith("_"):
                    continue
                if os.path.isfile(os.path.join(league_dir, entry, "strategy.yaml")):
                    bots.append(entry)
                    bot_to_league[entry] = league
        bots_per_league[league] = bots
    return bots_per_league, bot_to_league


def killed_leagues(leagues_enabled):
    out = []
    for league in leagues_enabled:
        flag = os.path.join(COMP, league, "league_paused.flag")
        if os.path.exists(flag):
            out.append(league)
    return out


# tier classification (vidar_tier wrapper with safe fallback)
def classify_action(action):
    """Returns (tier, rationale, source).

    Order: keyword pre-pass -> LLM (if Anthropic key present and not
    explicitly disabled) -> static fallback table keyed by action.type.
    """
    finding = action.to_finding()
    try:
        sys.path.insert(0, RESEARCH)
        import vidar_tier
        try:
            kw = vidar_tier._tier3_keyword_match(finding)
        except Exception:
            kw = None
        if kw:
            return "tier3", "keyword:" + str(kw).lower(), "vidar_tier_keyword"
        if os.environ.get("NJORD_NO_LLM_CLASSIFY"):
            fallback = _NJORD_TIER_FALLBACK.get(action.type, "tier2")
            return fallback, "fallback (LLM disabled by env)", "njord_fallback"
        secret = getattr(vidar_tier, "ANTHROPIC_SECRET", "")
        if secret and os.path.exists(secret):
            try:
                tier, rat = vidar_tier.classify_finding(finding)
                return tier, rat, "vidar_tier_llm"
            except Exception as e:
                _log("vidar_tier LLM error: " + repr(e) + "; using fallback")
    except ImportError:
        pass
    fallback = _NJORD_TIER_FALLBACK.get(action.type, "tier2")
    return fallback, "njord internal action-type table", "njord_fallback"


# tier 2 / tier 3 routing
def _load_pending_review():
    return _load_json_or(PENDING_REVIEW, {"entries": []})


def _save_pending_review(state):
    state["last_updated"] = _ts_iso()
    _atomic_write_json(PENDING_REVIEW, state)


def add_pending_review(action, tier_rationale):
    state = _load_pending_review()
    deadline = (datetime.now(timezone.utc) + timedelta(hours=TIER2_REVIEW_DEADLINE_HR)).isoformat()
    fid = action.to_finding()["id"]
    state["entries"] = [e for e in state["entries"] if e.get("finding_id") != fid]
    state["entries"].append({
        "finding_id":     fid,
        "ts":             _ts_iso(),
        "action_type":    action.type,
        "bot":            action.bot,
        "league":         action.league,
        "from_usd":       action.from_usd,
        "to_usd":         action.to_usd,
        "tier_rationale": tier_rationale,
        "deadline_ts":    deadline,
        "revert_command": "python3 " + os.path.join(RESEARCH, "njord.py") + " revert " + fid,
    })
    _save_pending_review(state)


def emit_tier3(action, tier_rationale, telegram_required):
    rec = {
        "ts":             _ts_short(),
        "source":         "njord",
        "severity":       "critical" if telegram_required else "error",
        "finding_id":     action.to_finding()["id"],
        "title":          "[NJORD tier3] " + action.type + " blocked - Chris ack required",
        "summary":        action._suggested_action_text()[:200],
        "tier":           "tier3",
        "tier_rationale": tier_rationale,
        "action":         action.to_dict(),
        "tg_allowed":     bool(telegram_required),
    }
    _append_jsonl(SYN_INBOX, rec)


# tier 1 execution
def _empty_row():
    return {
        "allocated_usd":          0.0,
        "current_value_usd":      0.0,
        "peak_value_usd":         0.0,
        "drawdown_pct_from_peak": 0.0,
        "kill_state":             "active",
        "last_rebalance_ts":      None,
    }


def _bot_default_symbol(bot, league):
    """Return Kraken pair for a bot. Read strategy.yaml.kraken_pair if set."""
    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml is not None:
        path = os.path.join(FLEET_DIR, league, bot, "strategy.yaml")
        if os.path.isfile(path):
            try:
                with open(path) as f:
                    sd = yaml.safe_load(f) or {}
                pair = sd.get("kraken_pair")
                if pair:
                    return str(pair)
            except (OSError, Exception):
                pass
    if league == "polymarket":
        return ""
    return "XBTUSD"


def execute_tier1(action, kraken, current_table):
    """Mutates current_table in place, places paper/live orders best-effort."""
    bot = action.bot
    if action.type == "pause_bot":
        row = current_table.setdefault(bot, _empty_row())
        row["kill_state"] = "paused"
        row["last_rebalance_ts"] = _ts_iso()
        return {"executed": "paused", "bot": bot}
    if action.type == "rebalance":
        row = current_table.setdefault(bot, _empty_row())
        old = float(row.get("allocated_usd") or 0.0)
        new = float(action.to_usd)
        row["allocated_usd"] = new
        row["last_rebalance_ts"] = _ts_iso()
        delta = new - old
        if abs(delta) >= 1.0:
            symbol = _bot_default_symbol(bot, action.league)
            side = "buy" if delta > 0 else "sell"
            try:
                fill = kraken.place_market_order(symbol, side, abs(delta))
                _log("order " + bot + " " + side + " $" + format(abs(delta), ".2f")
                     + " " + symbol + ": " + json.dumps(fill))
            except Exception as e:
                _log("order " + bot + " failed: " + repr(e) + "; table updated anyway")
        return {"executed": "rebalanced", "bot": bot, "to_usd": new}
    return {"executed": "noop", "type": action.type}


# main cycle
def run_once(kraken_adapter=None):
    sys.path.insert(0, WORKSPACE)
    sys.path.insert(0, RESEARCH)
    from config_loader import config

    njord_cfg = getattr(config, "njord", None)
    if njord_cfg is None:
        _log("njord block missing from config; nothing to do")
        return {"status": "no_config"}
    if not getattr(njord_cfg, "enabled", False):
        _log("njord disabled in config; skipping")
        return {"status": "disabled"}

    leagues_enabled = list(getattr(config.fleet, "leagues_enabled", []) or [])
    bots_per_league, bot_to_league = discover_fleet(leagues_enabled)
    n_bots = sum(len(b) for b in bots_per_league.values())
    _log("cycle start mode=" + njord_cfg.mode + " bots=" + str(n_bots)
         + " leagues=" + ",".join(leagues_enabled))

    if n_bots == 0:
        _atomic_write_json(ALLOC_PATH, {
            "ts":                _ts_iso(),
            "mode":              njord_cfg.mode,
            "total_capital_usd": 0,
            "leagues_enabled":   leagues_enabled,
            "n_bots":            0,
            "table":             {},
            "actions":           [],
            "by_tier":           {"tier1": 0, "tier2": 0, "tier3": 0},
            "note":              "no bots discovered under fleet/<league>/<bot>/strategy.yaml",
        })
        return {"status": "no_bots"}

    if kraken_adapter is None:
        import njord_kraken
        kraken = njord_kraken.from_config(config)
    else:
        kraken = kraken_adapter

    total_capital = float(getattr(njord_cfg, "total_capital_usd", 0) or 0)
    if njord_cfg.mode == "live":
        try:
            total_capital = kraken.get_balance_usd()
        except NotImplementedError as e:
            _log("live balance not implemented: " + str(e) + "; falling back to config")

    weights = {}
    lw_obj = getattr(njord_cfg, "league_weights", None)
    if lw_obj is not None:
        for lg in leagues_enabled:
            weights[lg] = float(getattr(lw_obj, lg, 0.0) or 0.0)

    import njord_allocator as alloc
    target_table = alloc.compute_targets(
        total_capital, weights, bots_per_league,
        float(getattr(njord_cfg, "per_bot_max_pct", 10) or 10),
    )

    prior = _load_json_or(ALLOC_PATH, {"table": {}, "total_capital_usd": 0})
    current_table = prior.get("table", {}) or {}

    if njord_cfg.mode == "paper":
        for bot, row in current_table.items():
            if row.get("current_value_usd") is None:
                row["current_value_usd"] = row.get("allocated_usd", 0.0)

    actions = alloc.build_action_list(
        current_table=current_table,
        target_table=target_table,
        killed_leagues=killed_leagues(leagues_enabled),
        drawdown_kill_pct=float(getattr(njord_cfg, "drawdown_kill_pct", 15) or 15),
        total_capital=total_capital,
        last_total_capital=float(prior.get("total_capital_usd", 0) or 0),
        bot_to_league=bot_to_league,
    )

    telegram_required = bool(getattr(njord_cfg, "telegram_required_for_tier3", True))
    by_tier = {"tier1": 0, "tier2": 0, "tier3": 0}
    executed_records = []

    for action in actions:
        tier, rationale, source = classify_action(action)
        by_tier[tier] = by_tier.get(tier, 0) + 1
        rec = {"action": action.to_dict(), "tier": tier,
               "rationale": rationale, "source": source}
        if tier == "tier1":
            rec["outcome"] = execute_tier1(action, kraken, current_table)
        elif tier == "tier2":
            add_pending_review(action, rationale)
            rec["outcome"] = {"executed": "queued_for_review",
                              "deadline_hr": TIER2_REVIEW_DEADLINE_HR}
        else:
            emit_tier3(action, rationale, telegram_required)
            rec["outcome"] = {"executed": "blocked_chris_ack",
                              "tg": telegram_required}
        executed_records.append(rec)

    for bot, target in target_table.items():
        row = current_table.setdefault(bot, _empty_row())
        cur_v = float(row.get("current_value_usd",
                              row.get("allocated_usd", 0)) or 0)
        peak = max(float(row.get("peak_value_usd", 0) or 0),
                   float(row.get("allocated_usd", 0) or 0), cur_v)
        row["peak_value_usd"] = peak
        row["drawdown_pct_from_peak"] = alloc.compute_drawdown_pct(cur_v, peak)

    out = {
        "ts":                _ts_iso(),
        "mode":              njord_cfg.mode,
        "total_capital_usd": total_capital,
        "leagues_enabled":   leagues_enabled,
        "n_bots":            n_bots,
        "table":             current_table,
        "actions":           executed_records,
        "by_tier":           by_tier,
    }
    _atomic_write_json(ALLOC_PATH, out)
    _log("cycle done actions=" + str(len(actions))
         + " tier1=" + str(by_tier["tier1"])
         + " tier2=" + str(by_tier["tier2"])
         + " tier3=" + str(by_tier["tier3"]))
    return {"status": "ok", "by_tier": by_tier, "n_actions": len(actions)}


def revert(finding_id):
    state = _load_pending_review()
    before = len(state["entries"])
    state["entries"] = [e for e in state["entries"] if e.get("finding_id") != finding_id]
    after = len(state["entries"])
    if before == after:
        print("no pending review entry with finding_id=" + finding_id)
        return 1
    _save_pending_review(state)
    _log("reverted finding_id=" + finding_id)
    print("reverted " + finding_id + " (" + str(before - after) + " entry removed)")
    return 0


def status():
    alloc = _load_json_or(ALLOC_PATH, None)
    pend  = _load_json_or(PENDING_REVIEW, {"entries": []})
    if alloc is None:
        print("no njord_allocation.json yet - run a cycle first")
    else:
        print("NJORD: mode=" + str(alloc.get("mode"))
              + " total=$" + format(alloc.get("total_capital_usd", 0), ".2f")
              + " bots=" + str(alloc.get("n_bots", 0))
              + " actions_last_cycle=" + str(len(alloc.get("actions", []))))
        for bot, row in (alloc.get("table") or {}).items():
            print("  " + bot.ljust(24)
                  + "  alloc=$" + format(row.get("allocated_usd", 0), "8.2f")
                  + "  value=$" + format(row.get("current_value_usd", 0), "8.2f")
                  + "  dd=" + format(row.get("drawdown_pct_from_peak", 0), "4.1f") + "%"
                  + "  state=" + str(row.get("kill_state")))
    print("pending tier-2 reviews: " + str(len(pend.get("entries", []))))
    for e in pend.get("entries", []):
        print("  " + str(e.get("finding_id")) + "  " + str(e.get("action_type"))
              + "  deadline=" + str(e.get("deadline_ts")))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run")
    sub.add_parser("status")
    rv = sub.add_parser("revert")
    rv.add_argument("finding_id")
    args = ap.parse_args()
    if args.cmd == "run":
        result = run_once()
        ok_states = ("ok", "disabled", "no_bots", "no_config")
        sys.exit(0 if result.get("status") in ok_states else 1)
    if args.cmd == "status":
        sys.exit(status())
    if args.cmd == "revert":
        sys.exit(revert(args.finding_id))


if __name__ == "__main__":
    main()
