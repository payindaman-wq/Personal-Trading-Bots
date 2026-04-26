#!/usr/bin/env python3
"""Smoke test for unified deployment gate (Session 3.5, 2026-04-26).

Closes the parallel-promotion-path gap: best_strategy.yaml deployment now
consults the same is_new_best signal that gates new_best promotion. Replaces
the legacy raw<0 elites[0] guard with a single authoritative gate.

Acceptance:
  S1. (the exact bug) All elites raw<0; candidate raw=0.1 fails adj gate.
      best_strategy.yaml mtime UNCHANGED + deploy_skipped emitted.
  S2. Legitimate champion clears Session 2's gate -> best_strategy.yaml
      written with the new candidate.
  S3. Replay futures_day raw=-2.5267 promotion event -> best_strategy.yaml
      NOT updated under the unified path.

Run: python3 /root/.openclaw/workspace/research/smoke_deploy_gate.py
"""
import json
import os
import sys
import time

sys.path.insert(0, "/root/.openclaw/workspace")
sys.path.insert(0, "/root/.openclaw/workspace/research")

from odin_researcher_v2 import Population, adj_score, SYN_INBOX_PATH
import odin_researcher_v2 as odin


def inbox_marker():
    if not os.path.exists(SYN_INBOX_PATH):
        return 0
    with open(SYN_INBOX_PATH) as f:
        return sum(1 for _ in f)


def new_inbox_entries(start, source="odin"):
    if not os.path.exists(SYN_INBOX_PATH):
        return []
    with open(SYN_INBOX_PATH) as f:
        lines = f.readlines()
    out = []
    for line in lines[start:]:
        try:
            rec = json.loads(line)
            if rec.get("source") == source:
                out.append(rec)
        except json.JSONDecodeError:
            continue
    return out


def best_strategy_path(league):
    return os.path.join("/root/.openclaw/workspace/research", league,
                        "best_strategy.yaml")


# ---------------------------------------------------------------------------
# S1: the exact bug — all elites raw<0, candidate raw=0.1 fails adj gate.
#     best_strategy.yaml mtime unchanged + deploy_skipped emitted.
# ---------------------------------------------------------------------------
def test_s1_raw_positive_no_adj_no_deploy():
    league = "futures_day"
    path = best_strategy_path(league)
    assert os.path.exists(path), f"S1: precondition — {path} must exist"
    pre_mtime = os.path.getmtime(path)
    pre_bytes = open(path, "rb").read()

    pop = Population(league)
    # Stage: champion adj_score sits HIGH (0.45) so a raw=0.1 candidate's
    # adj cannot beat it. Champion's raw is intentionally negative — the
    # exact reseed state Session 3 flagged. Force the non-sparse path so
    # the gate evaluates adj_score_no_beat (not the sparse-history raw
    # floor, which would let raw>0 through and miss the bug).
    pop.elites = [(0.45, {"_sharpe": -0.5, "_trades": 30}, "name: stub\n")]
    pop._live_history_sparse = lambda: False
    if odin.backtest_drift is not None:
        original_bonus = odin.backtest_drift.get_gate_bonus
        original_veto = odin.backtest_drift.get_veto_signal
        odin.backtest_drift.get_gate_bonus = lambda lg: 0.0
        odin.backtest_drift.get_veto_signal = lambda lg: False
    try:
        cand_raw = 0.1
        cand_adj = 0.06  # < champion 0.45 -> adj_score_no_beat
        before = inbox_marker()
        # Direct deploy path: pretend bucket routing placed this at elites[0].
        is_new_best = pop._gate_new_best(cand_raw, cand_adj)
        assert is_new_best is False, "S1: gate must veto adj_score_no_beat"
        veto_reason = pop._last_veto_reason
        pop._save_fleet(
            "name: cand_s1\n_sharpe: 0.1\n_trades: 30\n",
            is_new_best,
            veto_reason,
            candidate_id="cand_s1",
        )
    finally:
        if odin.backtest_drift is not None:
            odin.backtest_drift.get_gate_bonus = original_bonus
            odin.backtest_drift.get_veto_signal = original_veto

    post_mtime = os.path.getmtime(path)
    post_bytes = open(path, "rb").read()
    assert post_mtime == pre_mtime, \
        f"S1: best_strategy.yaml mtime changed ({pre_mtime} -> {post_mtime})"
    assert post_bytes == pre_bytes, \
        "S1: best_strategy.yaml CONTENT changed despite gate veto"

    new = new_inbox_entries(before)
    matches = [e for e in new
               if e.get("kind") == "deploy_skipped"
               and e.get("league") == league
               and e.get("candidate_id") == "cand_s1"
               and e.get("reason") == "adj_score_no_beat"]
    assert matches, f"S1: expected deploy_skipped(adj_score_no_beat) for cand_s1; got {new}"
    print("S1 PASS: gate=False -> best_strategy.yaml untouched + deploy_skipped emitted.")


# ---------------------------------------------------------------------------
# S2: legitimate champion clears Session 2's gate -> best_strategy.yaml written.
# ---------------------------------------------------------------------------
def test_s2_legitimate_champion_deploys():
    """Use a throwaway league dir so we don't perturb live futures_day.
    A clean Population with an empty bucket sees the candidate via the
    cold-start path (or beats an existing-but-weaker champion); is_new_best
    returns True and _save_fleet writes best_strategy.yaml."""
    import tempfile
    league = "_smoke_s2"
    league_dir = os.path.join("/root/.openclaw/workspace/research", league)
    os.makedirs(league_dir, exist_ok=True)
    target = os.path.join(league_dir, "best_strategy.yaml")
    if os.path.exists(target):
        os.remove(target)

    pop = Population(league)
    pop.elites = []  # cold-start
    cand_raw = 0.85
    cand_adj = adj_score(cand_raw, 30, league=league)
    is_new_best = pop._gate_new_best(cand_raw, cand_adj)
    assert is_new_best is True, "S2: cold-start positive raw must clear gate"
    yaml_text = (
        "name: cand_s2\n"
        "league: _smoke_s2\n"
        "pairs:\n- BTC/USD\n"
        "_sharpe: 0.85\n_trades: 30\n"
    )
    pop._save_fleet(yaml_text, is_new_best, None, candidate_id="cand_s2")
    assert os.path.exists(target), "S2: best_strategy.yaml must be written"
    with open(target) as f:
        body = f.read()
    assert "cand_s2" in body, f"S2: deployed YAML missing candidate name; got:\n{body}"
    # Cleanup
    for fn in os.listdir(league_dir):
        os.remove(os.path.join(league_dir, fn))
    os.rmdir(league_dir)
    print("S2 PASS: gate=True candidate written to best_strategy.yaml.")


# ---------------------------------------------------------------------------
# S3: replay the futures_day -2.5267 promotion event under the unified path.
# ---------------------------------------------------------------------------
def test_s3_replay_negative_2_5267():
    league = "futures_day"
    path = best_strategy_path(league)
    assert os.path.exists(path), f"S3: precondition — {path} must exist"
    pre_mtime = os.path.getmtime(path)
    pre_bytes = open(path, "rb").read()

    pop = Population(league)
    # Cold-start replay: same scenario that produced the -2.5267 deploy.
    pop.elites = []
    cand_raw = -2.5267
    cand_adj = adj_score(cand_raw, 30, league=league)
    before = inbox_marker()
    is_new_best = pop._gate_new_best(cand_raw, cand_adj)
    assert is_new_best is False, "S3: raw=-2.5267 must be vetoed by gate"
    pop._save_fleet(
        "name: cand_s3\n_sharpe: -2.5267\n_trades: 30\n",
        is_new_best,
        pop._last_veto_reason,
        candidate_id="cand_s3",
    )
    post_mtime = os.path.getmtime(path)
    post_bytes = open(path, "rb").read()
    assert post_mtime == pre_mtime, \
        f"S3: best_strategy.yaml mtime changed under replay ({pre_mtime} -> {post_mtime})"
    assert post_bytes == pre_bytes, \
        "S3: best_strategy.yaml CONTENT changed under replay"

    new = new_inbox_entries(before)
    matches = [e for e in new
               if e.get("kind") == "deploy_skipped"
               and e.get("candidate_id") == "cand_s3"
               and e.get("reason") == "raw_sharpe_negative"]
    assert matches, f"S3: expected deploy_skipped(raw_sharpe_negative); got {new}"
    print("S3 PASS: -2.5267 replay -> best_strategy.yaml untouched + deploy_skipped.")


def main():
    test_s1_raw_positive_no_adj_no_deploy()
    test_s2_legitimate_champion_deploys()
    test_s3_replay_negative_2_5267()
    print("\nALL UNIFIED DEPLOY GATE SMOKE TESTS PASSED.")


if __name__ == "__main__":
    main()
