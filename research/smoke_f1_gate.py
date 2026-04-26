#!/usr/bin/env python3
"""Smoke test for F1 new_best gate (meta_audit 2026-04-26).

Acceptance:
  T1. Replay last 10 futures_day sprints. Assert current champion (-2.5267)
      would have been vetoed at promotion under the new gate.
  T2. Candidate {raw=0.5, adj=0.4, champion_adj=0.45} — reject on adj_score.
  T3. Candidate {raw=-0.1, adj=0.8} — reject on raw veto.

Run: python3 /root/.openclaw/workspace/research/smoke_f1_gate.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, "/root/.openclaw/workspace")
sys.path.insert(0, "/root/.openclaw/workspace/research")

from odin_researcher_v2 import Population, adj_score, SYN_INBOX_PATH
import odin_researcher_v2 as odin


def reset_inbox_marker():
    """Snapshot the inbox length so we can detect new veto entries."""
    if not os.path.exists(SYN_INBOX_PATH):
        return 0
    with open(SYN_INBOX_PATH) as f:
        return sum(1 for _ in f)


def new_inbox_entries(start_count, source="odin"):
    if not os.path.exists(SYN_INBOX_PATH):
        return []
    with open(SYN_INBOX_PATH) as f:
        lines = f.readlines()
    out = []
    for line in lines[start_count:]:
        try:
            rec = json.loads(line)
            if rec.get("source") == source:
                out.append(rec)
        except json.JSONDecodeError:
            continue
    return out


# ---------------------------------------------------------------------------
# T1: replay — current futures_day champion (raw=-2.5267) vetoed at promotion.
# ---------------------------------------------------------------------------
def test_t1_negative_champion_vetoed():
    """The -2.5267 raw champion that exists today must NOT pass _gate_new_best
    under the new gate. We exercise both the cold-start path (no elites) and
    the contested path (existing positive elite present).
    """
    pop = Population("futures_day")
    pop.elites = []  # cold-start
    inbox_before = reset_inbox_marker()
    cand_adj = adj_score(-2.5267, 30, league="futures_day")
    is_new_best = pop._gate_new_best(-2.5267, cand_adj)
    assert is_new_best is False, "T1a: cold-start raw=-2.5267 should be vetoed"
    new = new_inbox_entries(inbox_before)
    assert any(e["kind"] == "new_best_veto" and "raw_sharpe_negative" in e["reason"]
               for e in new), f"T1a: expected raw_sharpe_negative veto in inbox; got {new}"

    # Contested path: -2.5267 challenger vs an existing positive champion.
    pop.elites = [(0.4, {"_sharpe": 0.5, "_trades": 30}, "name: stub\n")]
    inbox_before = reset_inbox_marker()
    is_new_best = pop._gate_new_best(-2.5267, cand_adj)
    assert is_new_best is False, "T1b: contested raw=-2.5267 should be vetoed"
    new = new_inbox_entries(inbox_before)
    assert any("raw_sharpe_negative" in e["reason"] for e in new), \
        f"T1b: expected raw_sharpe_negative veto; got {new}"
    print("T1 PASS: raw=-2.5267 vetoed in both cold-start and contested paths.")


# ---------------------------------------------------------------------------
# T2: candidate {raw=0.5, adj=0.4, champion_adj=0.45} → reject on adj_score.
# ---------------------------------------------------------------------------
def test_t2_adj_score_no_beat():
    """Candidate has positive raw (passes hard veto) but adj_score doesn't
    beat the champion adj_score → reject with adj_score_no_beat.
    Forces the non-sparse path by monkey-patching _live_history_sparse and
    backtest_drift.get_gate_bonus to 0.0."""
    pop = Population("futures_day")
    pop.elites = [(0.45, {"_sharpe": 0.6, "_trades": 30}, "name: stub\n")]
    pop._live_history_sparse = lambda: False
    if odin.backtest_drift is not None:
        original_bonus = odin.backtest_drift.get_gate_bonus
        original_veto = odin.backtest_drift.get_veto_signal
        odin.backtest_drift.get_gate_bonus = lambda lg: 0.0
        odin.backtest_drift.get_veto_signal = lambda lg: False
    try:
        inbox_before = reset_inbox_marker()
        is_new_best = pop._gate_new_best(0.5, 0.4)
        assert is_new_best is False, "T2: cand_adj=0.4 < champ_adj=0.45 should reject"
        new = new_inbox_entries(inbox_before)
        assert any("adj_score_no_beat" in e["reason"] for e in new), \
            f"T2: expected adj_score_no_beat veto; got {new}"
        print("T2 PASS: cand_adj=0.4 < champ_adj=0.45 rejected on adj_score.")
    finally:
        if odin.backtest_drift is not None:
            odin.backtest_drift.get_gate_bonus = original_bonus
            odin.backtest_drift.get_veto_signal = original_veto


# ---------------------------------------------------------------------------
# T3: candidate {raw=-0.1, adj=0.8} → reject on raw veto regardless of adj.
# ---------------------------------------------------------------------------
def test_t3_raw_veto_overrides_high_adj():
    pop = Population("futures_day")
    pop.elites = [(0.3, {"_sharpe": 0.4, "_trades": 30}, "name: stub\n")]
    inbox_before = reset_inbox_marker()
    is_new_best = pop._gate_new_best(-0.1, 0.8)
    assert is_new_best is False, "T3: raw=-0.1 should be vetoed despite adj=0.8"
    new = new_inbox_entries(inbox_before)
    assert any("raw_sharpe_negative" in e["reason"] for e in new), \
        f"T3: expected raw_sharpe_negative veto; got {new}"
    print("T3 PASS: raw=-0.1 vetoed despite adj=0.8 (HARD RULE holds).")


# ---------------------------------------------------------------------------
# T4 (bonus): _save_fleet refuses to deploy a raw<0 top elite.
# ---------------------------------------------------------------------------
def test_t4_save_fleet_blocks_negative_top():
    """End-to-end: even if bucket routing places a raw<0 elite at the top,
    _save_fleet must refuse to write best_strategy.yaml.
    """
    pop = Population("futures_day")
    inbox_before = reset_inbox_marker()
    pop._save_fleet("name: bad\n_sharpe: -2.5267\n_trades: 30\n")
    new = new_inbox_entries(inbox_before)
    assert any("fleet_sync_blocked_raw_negative" in e["reason"] for e in new), \
        f"T4: expected fleet_sync_blocked_raw_negative veto; got {new}"
    print("T4 PASS: _save_fleet refused to deploy raw=-2.5267 top elite.")


def main():
    test_t1_negative_champion_vetoed()
    test_t2_adj_score_no_beat()
    test_t3_raw_veto_overrides_high_adj()
    test_t4_save_fleet_blocks_negative_top()
    print("\nALL F1 GATE SMOKE TESTS PASSED.")


if __name__ == "__main__":
    main()
