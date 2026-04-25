#!/usr/bin/env python3
"""
ledger_phase2_soak_check.py — one-shot soak verdict for Phase-2 cycle ledger.

Scheduled via `at` for 2026-04-30 10:00 PST (5 days post-ship of commit
65397ea on 2026-04-25). Routes the verdict to syn_inbox.jsonl with
source="ledger_soak" severity="critical" so sys_heartbeat surfaces it on
Chris's Telegram.

Decision rule:
  GREENLIGHT Phase 3 if
    - zero ledger_vs_state_drift entries since 2026-04-25, AND
    - zero ledger_drift_check_failed entries, AND
    - drift() empty across all 5 leagues, AND
    - sprint_integrity reports OK, AND
    - day league has >=4 sprint_started events since 2026-04-25 (24h sprints
      should produce ~5 by then; allow 4 for jitter)
  HOLD otherwise — list what fired/diverged.
"""
import datetime as _dt
import json
import os
import subprocess
import sys

WORKSPACE   = "/root/.openclaw/workspace"
SHIP_TS     = "2026-04-25T00:00"  # post-ship cutoff (UTC)
SYN_INBOX   = os.path.join(WORKSPACE, "syn_inbox.jsonl")
LEAGUES     = ["day", "swing", "futures_day", "futures_swing", "polymarket"]

sys.path.insert(0, WORKSPACE)
import cycle_ledger as cl  # noqa: E402


def ts_now():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M")


def jsonl_iter(path):
    if not os.path.isfile(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def find_drift_anomalies():
    """Scan inbox + maintenance + self-heal logs for ledger anomaly kinds since SHIP_TS."""
    paths = [
        os.path.join(WORKSPACE, "syn_inbox.jsonl"),
        os.path.join(WORKSPACE, "maintenance_log.jsonl"),
        os.path.join(WORKSPACE, "competition", "self_heal_log.jsonl"),
    ]
    kinds = ("ledger_vs_state_drift", "ledger_drift_check_failed")
    hits = []
    for p in paths:
        for rec in jsonl_iter(p):
            ts = rec.get("ts", "")
            if ts < SHIP_TS:
                continue
            # The kind may be encoded directly (maintenance/self_heal logs) or
            # buried inside the syn_inbox msg/detail. Match both.
            kind = rec.get("kind") or ""
            msg  = rec.get("msg") or rec.get("detail") or ""
            for k in kinds:
                if kind == k or k in msg:
                    hits.append({
                        "src":  os.path.basename(p),
                        "ts":   ts,
                        "kind": k,
                        "league": rec.get("league") or "",
                        "snippet": (msg or json.dumps(rec))[:200],
                    })
                    break
    return hits


def count_emits_per_league():
    counts = {}
    for league in LEAGUES:
        path = cl._ledger_path(league)
        c_total = 0
        c_recent = 0
        by_type_recent = {}
        for ev in jsonl_iter(path):
            c_total += 1
            ts = ev.get("ts", "")
            if ts >= SHIP_TS and ev.get("type") != "cycle_baseline":
                c_recent += 1
                by_type_recent[ev.get("type", "?")] = by_type_recent.get(ev.get("type", "?"), 0) + 1
        counts[league] = {"total": c_total, "since_ship": c_recent, "by_type": by_type_recent}
    return counts


def current_drift():
    return {league: cl.drift(league) for league in LEAGUES}


def run_integrity_check():
    try:
        out = subprocess.run(
            ["python3", os.path.join(WORKSPACE, "sprint_integrity_check.py")],
            capture_output=True, text=True, timeout=60,
        )
        return (out.stdout + out.stderr).strip()
    except Exception as e:
        return f"sprint_integrity_check failed to run: {e}"


def decide(drift_anoms, drift_now, emit_counts, integrity):
    # Day league should have produced multiple sprint_started events in 5 days.
    day_starts = emit_counts["day"]["by_type"].get("sprint_started", 0)
    fdy_starts = emit_counts["futures_day"]["by_type"].get("sprint_started", 0)
    drift_dirty = any(v for v in drift_now.values())
    integrity_ok = integrity.startswith("[sprint_integrity] OK")
    enough_traffic = day_starts >= 4 and fdy_starts >= 4

    if not drift_anoms and not drift_dirty and integrity_ok and enough_traffic:
        return "GREENLIGHT", "All checks pass — propose Phase 3 (source-of-truth promotion + direct-mutation removal). See workspace/design/cycle_ledger_redesign.md."
    reasons = []
    if drift_anoms:
        reasons.append(f"{len(drift_anoms)} ledger_vs_state_drift / ledger_drift_check_failed entries")
    if drift_dirty:
        bad = {L: v for L, v in drift_now.items() if v}
        reasons.append(f"live drift in {list(bad)}: {bad}")
    if not integrity_ok:
        reasons.append(f"integrity check not OK: {integrity[:120]}")
    if not enough_traffic:
        reasons.append(f"insufficient sprint_started traffic (day={day_starts}, futures_day={fdy_starts}, need >=4 each)")
    return "HOLD", "; ".join(reasons)


def main():
    drift_anoms = find_drift_anomalies()
    drift_now   = current_drift()
    emit_counts = count_emits_per_league()
    integrity   = run_integrity_check()
    verdict, reason = decide(drift_anoms, drift_now, emit_counts, integrity)

    # Compose terse Telegram-ready report (HTML — sys_heartbeat already uses HTML).
    lines = [f"<b>SYN: ledger Phase-2 soak verdict — {verdict}</b>"]
    lines.append(f"Reason: {reason}")
    lines.append("")
    lines.append("<b>Emits since 2026-04-25:</b>")
    for L in LEAGUES:
        c = emit_counts[L]
        bt = ", ".join(f"{k}={v}" for k, v in sorted(c["by_type"].items())) or "—"
        lines.append(f"  {L}: {c['since_ship']} events ({bt})")
    lines.append("")
    lines.append("<b>Live drift:</b>")
    for L, d in drift_now.items():
        lines.append(f"  {L}: {'OK' if not d else d}")
    lines.append("")
    lines.append(f"<b>Anomalies:</b> {len(drift_anoms)}")
    for h in drift_anoms[:5]:
        lines.append(f"  [{h['ts']}] {h['kind']} ({h['league']}) — {h['snippet'][:80]}")
    lines.append("")
    lines.append(f"<b>Integrity:</b> {integrity[:160]}")
    lines.append("")
    if verdict == "GREENLIGHT":
        lines.append("Next: ship Phase 3 — promote write_state(), strip direct cycle_state.json mutations from the 11 writers.")
    else:
        lines.append("Next: investigate divergence before promoting. See competition/<league>/cycle_events.jsonl + cycle_state.json side-by-side.")

    msg = "\n".join(lines)

    rec = {
        "ts":       ts_now(),
        "source":   "ledger_soak",
        "severity": "critical",
        "msg":      msg[:2000],
    }
    with open(SYN_INBOX, "a") as f:
        f.write(json.dumps(rec) + "\n")

    # Stash full report to disk too — useful if Telegram fails or msg got truncated.
    report_path = os.path.join(WORKSPACE, f"ledger_phase2_soak_report_{_dt.datetime.now(_dt.timezone.utc).strftime('%Y%m%d_%H%M')}.txt")
    with open(report_path, "w") as f:
        f.write(msg)
    print(f"VERDICT: {verdict}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
