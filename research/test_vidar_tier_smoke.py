#!/usr/bin/env python3
"""
Smoke test for vidar_tier.classify_finding.

Runs against the 13 findings in research/meta_audit/latest.json (the
2026-04-25 weekly audit) plus a hand-rolled Tier-3 hypothetical to verify
the classifier wouldn't false-positive on irreversible suggestions.

F2 has 3 distinct sub-actions in its suggested_action ("add killswitch
criteria", "reset population", "resume league") that the spec calls out
separately, so we synthesise three sub-findings for F2 and classify each
in isolation.

Run:
  python3 research/test_vidar_tier_smoke.py
  python3 research/test_vidar_tier_smoke.py --no-llm   # only check keyword pre-pass

Exits 0 on full match, 1 on any mismatch.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

WORKSPACE  = "/root/.openclaw/workspace"
RESEARCH   = os.path.join(WORKSPACE, "research")
SIDECAR    = os.path.join(RESEARCH, "meta_audit", "latest.json")

sys.path.insert(0, RESEARCH)
import vidar_tier  # noqa: E402

# Expected tiering from the human-approved spec for the 2026-04-25 audit.
# F2 splits into 3 sub-findings because its suggested_action mixes a
# Tier-1 patch (killswitch criteria) with Tier-2 disruptive ops
# (population reset, league resume).
EXPECTED_TIERS = {
    "F1":                          "tier1",
    "F2-killswitch-criteria":      "tier1",
    "F2-reset-population":         "tier2",
    "F2-resume-league":            "tier2",
    "F3":                          "tier1",
    "F4":                          "tier1",
    "F5":                          "tier1",
    "F6":                          "tier1",
    "F7-itself":                   "tier2",
    "F8":                          "tier1",
    "F9":                          "tier1",
    "F10":                         "tier2",
    "F11":                         "tier2",
    "F12":                         "tier1",
    "F13":                         "tier1",
    # Hypothetical irreversibility test.
    "HYP-tier3-elite-wipe":        "tier3",
}


def _f2_subfindings(f2):
    """Synthesise 3 Tier-discriminating sub-findings from F2's
    suggested_action so we can grade each independently."""
    base = {
        "severity": f2.get("severity"),
        "evidence": f2.get("evidence"),
        "why_it_matters": f2.get("why_it_matters"),
    }
    return [
        {
            **base,
            "id":               "F2-killswitch-criteria",
            "title":            "Add league-level live-PnL kill criterion to league_killswitch",
            "suggested_action": (
                "Add league-level live PnL kill criteria to league_killswitch.py: "
                "kill league if median live PnL over last 7 sprints < -0.2% AND "
                "backtest Sharpe of champion < 0. This is a code patch to the "
                "killswitch logic itself."
            ),
        },
        {
            **base,
            "id":               "F2-reset-population",
            "title":            "Reset futures_day population — delete elite_0..elite_9 and reseed with diverse random configs",
            "suggested_action": (
                "Reset the futures_day population from scratch by deleting "
                "elite_0..elite_9 and reseeding with diverse random configs. "
                "Backups remain available, but in-flight research state is "
                "disrupted while the new population converges."
            ),
        },
        {
            **base,
            "id":               "F2-resume-league",
            "title":            "Resume futures_day league after the loss-bleed pause",
            "suggested_action": (
                "Resume futures_day league trading by re-enabling the daily "
                "restart cron (currently commented out as 'PAUSED 2026-04-25 "
                "meta_audit F2'). This re-opens capital flow to the strategy."
            ),
        },
    ]


def _f7_itself(f7):
    """F7 talks about VIDAR escalations terminating in the void. Implementing
    F7 = building this very executor (granting LOKI/VIDAR program.md authority
    OR adding Telegram escalation). Spec calls this Tier 2."""
    return {
        **f7,
        "id":    "F7-itself",
        "title": "Implement VIDAR auto-execute layer — grant agent authority to fix root causes",
    }


def _hypothetical_tier3():
    return {
        "id":               "HYP-tier3-elite-wipe",
        "severity":         "high",
        "title":            "Delete all elite_0 backups permanently across all leagues to free disk",
        "evidence":         "Disk usage hypothetical — backups consume 6GB. (synthetic for smoke test)",
        "why_it_matters":   "If we permanently delete all elite_0 backup files, no auto-revert path exists.",
        "suggested_action": (
            "Permanently delete all elite_0 backup files (.bak.*) across day, "
            "swing, futures_day, futures_swing leagues. This is irrecoverable "
            "and removes our auto-revert anchor. Real-capital protection is "
            "weakened until next baseline."
        ),
    }


def load_findings():
    with open(SIDECAR) as f:
        sidecar = json.load(f)
    findings = (sidecar.get("decision") or {}).get("findings") or []
    return findings


def build_test_set(findings):
    """Build {test_id -> finding} dict matching EXPECTED_TIERS keys."""
    by_id = {f["id"]: f for f in findings}
    out = {}
    for fid, fobj in by_id.items():
        if fid == "F2":
            for sub in _f2_subfindings(fobj):
                out[sub["id"]] = sub
        elif fid == "F7":
            out["F7-itself"] = _f7_itself(fobj)
        else:
            out[fid] = fobj
    out["HYP-tier3-elite-wipe"] = _hypothetical_tier3()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-llm", action="store_true",
                    help="only test the keyword pre-pass (skip Sonnet calls)")
    ap.add_argument("--audit-ts",
                    default="smoke_test_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"),
                    help="audit_ts namespace for the cache (use a fresh one to force LLM calls)")
    args = ap.parse_args()

    findings = load_findings()
    if not findings:
        print(f"[smoke] no findings in {SIDECAR}", file=sys.stderr)
        sys.exit(2)

    test_set = build_test_set(findings)

    print(f"[smoke] testing {len(test_set)} sub-findings (audit_ts namespace: {args.audit_ts})")
    print(f"[smoke] {'='*70}")

    mismatches = []
    for tid, expected in sorted(EXPECTED_TIERS.items()):
        finding = test_set.get(tid)
        if finding is None:
            print(f"  {tid:34s} MISSING in test set")
            mismatches.append((tid, expected, "MISSING"))
            continue

        if args.no_llm:
            # Pre-pass conservativeness check: a keyword hit on a non-tier3
            # case is a false positive (must fail). A keyword miss on a
            # tier3 case is acceptable here (the LLM is supposed to catch
            # the rest); we only flag false positives in --no-llm mode.
            kw = vidar_tier._tier3_keyword_match(finding)
            if kw and expected != "tier3":
                actual = "tier3 (keyword false-positive)"
                ok = False
            elif kw:
                actual = "tier3"
                ok = True
            else:
                actual = "no_keyword_match"
                ok = True
            rationale = f"keyword:{kw}" if kw else "(no keyword match — LLM would handle)"
        else:
            try:
                actual, rationale = vidar_tier.classify_finding(finding, audit_ts=args.audit_ts)
            except Exception as e:
                print(f"  {tid:34s} ERROR: {e}")
                mismatches.append((tid, expected, f"ERROR: {e}"))
                continue
            ok = (actual == expected)

        flag = "OK " if ok else "FAIL"
        print(f"  [{flag}] {tid:34s} expected={expected:6s} actual={actual:30s}  {rationale[:80]}")
        if not ok:
            mismatches.append((tid, expected, actual))

    print(f"[smoke] {'='*70}")
    if mismatches:
        print(f"[smoke] {len(mismatches)} mismatch(es):")
        for tid, expected, actual in mismatches:
            print(f"    {tid}: expected {expected}, got {actual}")
        sys.exit(1)
    print(f"[smoke] all {len(EXPECTED_TIERS)} classifications matched expected tiers")
    sys.exit(0)


if __name__ == "__main__":
    main()
