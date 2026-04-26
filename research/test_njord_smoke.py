#!/usr/bin/env python3
"""
test_njord_smoke.py - paper-trading smoke test for NJORD.

Runs one full cycle in a sandbox WORKSPACE without real Kraken keys and
without any network calls (tick prices are injected). Validates:

  1. njord enabled but empty fleet  -> status=no_bots, empty table file
  2. 2-league x 2-bot fleet         -> 4 tier1 rebalances, table well-formed
  3. tier classifier on all action  -> matches expected tier per type
  4. drawdown trip                  -> pause_bot fires (tier1)
  5. njord disabled                 -> silent skip

Exit 0 on full pass, 1 on any failure.

Run:
  python3 research/test_njord_smoke.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

# Sandbox WORKSPACE BEFORE importing anything that reads it at module load.
WORKSPACE_TMP = tempfile.mkdtemp(prefix="njord_smoke_")
os.environ["WORKSPACE"]   = WORKSPACE_TMP
os.environ["CONFIG_PATH"] = os.path.join(WORKSPACE_TMP, "config.yaml")
# Force fallback classifier (avoid network/Anthropic during the smoke test).
os.environ["NJORD_NO_LLM_CLASSIFY"] = "1"
for k in ("KRAKEN_API_KEY", "KRAKEN_API_SECRET", "ANTHROPIC_API_KEY"):
    os.environ.pop(k, None)

CONFIG_YAML_TEMPLATE = """\
config_version: 1
anthropic:
  api_key: ""
  daily_budget_usd: 10
  throttle_at_pct: 80
gemini:
  api_key: ""
kraken:
  api_key: ""
  api_secret: ""
telegram:
  bot_token: ""
  chat_id: ""
vps:
  host: ""
  workspace: "{ws}"
dashboard:
  domain: ""
  branding: "Smoke Test Fleet"
mission:
  target: "Smoke test"
fleet:
  leagues_enabled:
    - day
    - swing
njord:
  enabled: true
  mode: "paper"
  total_capital_usd: 1000
  per_bot_max_pct: 30
  drawdown_kill_pct: 15
  league_weights:
    day: 0.6
    swing: 0.4
  telegram_required_for_tier3: true
"""


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def _write_config(ws):
    _write(os.path.join(ws, "config.yaml"), CONFIG_YAML_TEMPLATE.format(ws=ws))


def _build_fleet(ws, layout):
    for league, bots in layout.items():
        for b in bots:
            _write(os.path.join(ws, "fleet", league, b, "strategy.yaml"),
                   "name: " + b + "\nkraken_pair: XBTUSD\nrisk:\n  starting_capital: 100\n")


def _setup_repo_paths():
    """Make NJORD modules importable from the production research dir."""
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    repo_root = os.path.dirname(here)
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


def _drop_modules():
    for mod in list(sys.modules):
        if mod.startswith(("njord", "config_loader")):
            del sys.modules[mod]


PASS = "OK  "
FAIL = "FAIL"


class Recorder:
    def __init__(self):
        self.fails = 0

    def check(self, cond, label):
        tag = PASS if cond else FAIL
        print("  [" + tag + "] " + label)
        if not cond:
            self.fails += 1


def main():
    _setup_repo_paths()
    print("[smoke] sandbox WORKSPACE=" + WORKSPACE_TMP)
    _write_config(WORKSPACE_TMP)

    rec = Recorder()

    # scenario 1: empty fleet
    print("[smoke] scenario 1: enabled but empty fleet")
    _drop_modules()
    import njord
    result = njord.run_once()
    rec.check(result.get("status") == "no_bots",
              "empty fleet -> status=no_bots (got " + str(result.get("status")) + ")")
    af = json.load(open(njord.ALLOC_PATH))
    rec.check(af.get("table") == {}, "allocation table is empty")
    rec.check(af.get("n_bots") == 0, "n_bots == 0")

    # scenario 2: 2-league x 2-bot fleet, paper, injected tick
    print("[smoke] scenario 2: 2x2 fleet, rebalance from zero")
    _build_fleet(WORKSPACE_TMP, {"day": ["alice", "bob"], "swing": ["carol", "dave"]})
    _drop_modules()
    import njord
    import njord_kraken
    import njord_allocator as alloc

    kraken = njord_kraken.KrakenAdapter(
        api_key="", api_secret="", paper_balance_usd=1000.0,
        paper_state_path=os.path.join(WORKSPACE_TMP, "competition", "njord_paper_state.json"),
        tick_provider=lambda symbol: 50000.0,
    )
    result = njord.run_once(kraken_adapter=kraken)
    rec.check(result.get("status") == "ok",
              "2x2 cycle -> status=ok (got " + str(result.get("status")) + ")")
    by_tier = result.get("by_tier", {})
    rec.check(by_tier.get("tier1", 0) >= 4,
              "tier1 rebalances >= 4 (got " + str(by_tier.get("tier1", 0)) + ")")
    rec.check(by_tier.get("tier3", 0) == 0,
              "no tier3 in vanilla rebalance (got " + str(by_tier.get("tier3", 0)) + ")")

    af = json.load(open(njord.ALLOC_PATH))
    table = af.get("table", {})
    expected_bots = {"alice", "bob", "carol", "dave"}
    rec.check(set(table.keys()) == expected_bots,
              "table contains all 4 bots (got " + str(sorted(table)) + ")")
    # day weight 0.6 / 2 bots = $300; swing weight 0.4 / 2 bots = $200.
    expected_alloc = {"alice": 300.0, "bob": 300.0, "carol": 200.0, "dave": 200.0}
    for bot, exp in expected_alloc.items():
        actual = table.get(bot, {}).get("allocated_usd", 0.0)
        rec.check(abs(actual - exp) < 0.01,
                  bot + " alloc=$" + format(actual, ".2f") + " expected=$"
                  + format(exp, ".2f"))

    # scenario 3: tier classifier on full action vocabulary
    print("[smoke] scenario 3: tier classifier vocabulary")
    cases = [
        (alloc.Action(type="rebalance", bot="x", from_usd=100, to_usd=110), "tier1"),
        (alloc.Action(type="pause_bot", bot="x", from_usd=20),               "tier1"),
        (alloc.Action(type="wake_bot", bot="x"),                             "tier2"),
        (alloc.Action(type="shift_league_weight", league="day"),             "tier2"),
        (alloc.Action(type="reduce_total"),                                  "tier2"),
        (alloc.Action(type="wallet_op"),                                     "tier3"),
        (alloc.Action(type="key_change"),                                    "tier3"),
        (alloc.Action(type="retire_league", league="day"),                   "tier3"),
        (alloc.Action(type="total_change_25pct", from_usd=1000, to_usd=2000),"tier3"),
    ]
    for action, expected in cases:
        tier, rationale, source = njord.classify_action(action)
        rec.check(tier == expected,
                  action.type.ljust(22) + " -> " + tier + " (" + source + ")"
                  + (" expected=" + expected if tier != expected else ""))

    # scenario 4: drawdown trip -> pause_bot
    print("[smoke] scenario 4: drawdown trip on alice")
    af = json.load(open(njord.ALLOC_PATH))
    af["table"]["alice"]["current_value_usd"] = 200.0
    af["table"]["alice"]["peak_value_usd"]    = 300.0
    with open(njord.ALLOC_PATH, "w") as f:
        json.dump(af, f)
    result = njord.run_once(kraken_adapter=kraken)
    af = json.load(open(njord.ALLOC_PATH))
    rec.check(af["table"]["alice"].get("kill_state") == "paused",
              "alice paused after 33% drawdown trip (state="
              + str(af["table"]["alice"].get("kill_state")) + ")")

    # scenario 5: disabled -> silent skip
    print("[smoke] scenario 5: njord disabled -> silent skip")
    cfg_path = os.path.join(WORKSPACE_TMP, "config.yaml")
    with open(cfg_path) as f:
        body = f.read()
    with open(cfg_path, "w") as f:
        f.write(body.replace("enabled: true", "enabled: false"))
    _drop_modules()
    import njord as njord2
    result = njord2.run_once()
    rec.check(result.get("status") == "disabled",
              "disabled cycle -> status=disabled (got " + str(result.get("status")) + ")")

    print("[smoke] " + "=" * 60)
    if rec.fails:
        print("[smoke] " + str(rec.fails) + " failure(s)")
        shutil.rmtree(WORKSPACE_TMP, ignore_errors=True)
        sys.exit(1)
    print("[smoke] all checks passed")
    shutil.rmtree(WORKSPACE_TMP, ignore_errors=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
