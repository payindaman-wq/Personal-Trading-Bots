"""SYN/meta_audit — weekly strategic audit of the autoresearch pipeline.

Not an officer. A SYN sub-module. Scheduled Saturday 10:00 UTC via cron.

Role: question whether the research SYSTEM is structurally sound. MIMIR tunes
program.md inside a league; LOKI reverts bad patches; VIDAR arbitrates
events. None of them question the research frame itself.

Flow:
  1. Build a comprehensive snapshot (crontab, per-league gen_state + program
     + elite summary + results tail + drift state, LOKI reverts, leaderboards,
     Anthropic spend).
  2. Invoke research/vidar.py --mode meta_audit --snapshot <path>, which runs
     the Opus 4.7 analysis and writes a review + sidecar.
  3. Read the sidecar, route findings to syn_inbox.jsonl.

Routing rules (syn_inbox consumers: sys_heartbeat gateway + VIDAR next fire):
  - LOW         -> dashboard only (source=meta_audit, severity=info)
  - MEDIUM      -> dashboard + VIDAR queue (severity=warning)
  - HIGH        -> VIDAR immediate + dashboard (severity=error)
  - CRITICAL    -> VIDAR immediate + Chris via Telegram (severity=critical).
                   Carve-out in sys_heartbeat TG_ALLOWED_SOURCES for this
                   specific (source=meta_audit, severity=critical) pair.

VIDAR consumes meta_audit inbox rows on its next fire and decides:
  - delegable_to_loki=true  -> write LOKI work order
  - delegable_to_loki=false -> escalate via its own Telegram path

Only CRITICAL severity pages Chris directly. All other severities flow
through VIDAR arbitration per the existing SYN policy.
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

WORKSPACE         = "/root/.openclaw/workspace"
RESEARCH          = os.path.join(WORKSPACE, "research")
VIDAR             = os.path.join(RESEARCH, "vidar.py")
META_AUDIT_DIR    = os.path.join(RESEARCH, "meta_audit")
LATEST_SIDECAR    = os.path.join(META_AUDIT_DIR, "latest.json")
SYN_INBOX         = os.path.join(WORKSPACE, "syn_inbox.jsonl")
ANTHROPIC_USAGE   = os.path.join(RESEARCH, "anthropic_usage.jsonl")

LEAGUES_CRYPTO = ("day", "swing", "futures_day", "futures_swing")
LEAGUES_PM     = ("pm",)

VIDAR_TIMEOUT_SEC = 1200  # 20 minutes; Opus 4.7 with thinking on a large snapshot


ROLE_SUMMARY = (
    "Executive staff (agents that run the autoresearch system):\n"
    "- ODIN: crypto strategy researcher (Gemini Flash Lite). Proposes mutations, scores via 2yr backtest Sharpe. odin_researcher_v2.py. Per-league instance.\n"
    "- MIMIR: analysis officer (Sonnet 4.6 min). Every 200 gens rewrites program.md. mimir.py.\n"
    "- LOKI: implementation officer. Picks up Mimir output, applies code/config changes, auto-reverts on metric degradation. loki.py.\n"
    "- FREYA: prediction markets researcher (pm league). freya_researcher.py.\n"
    "- TYR: risk officer -- macro regime -> position size multiplier.\n"
    "- HEIMDALL: market intelligence -- trending tokens, sectors.\n"
    "- VIDAR: strategic arbiter (Opus 4.7). Fires on LOKI reverts, oscillation, manual deep-dive, and (new) scheduled meta_audit.\n"
    "- SYN: operations officer -- composite watchdog. This meta_audit module is a SYN sub-module.\n"
    "- NJORD: pending, activates when live trading begins (capital allocation).\n"
    "\n"
    "Flow: ODIN/FREYA propose -> backtest -> new_best -> MIMIR rewrites program -> LOKI ships -> live sprint -> (repeat).\n"
    "Nothing in this loop questions the loop itself.\n"
)

MISSION_SUMMARY = (
    "Mission: 5 BTC by end of 2027 via fully-automated system.\n"
    "Current: Phase 1 (day trading) funding $200-500 Kraken. Phase 7 (Polymarket/Kalshi) in progress.\n"
    "Kraken Derivatives US universe: BTC/ETH/SOL only (per-symbol leverage caps via kraken_leverage.py).\n"
    "Leagues: Spot Day, Futures Day (24h sprints); Spot Swing, Futures Swing (7d sprints); Prediction Markets.\n"
    "Kill switch: 15% drawdown from peak = auto-pause.\n"
    "Known ongoing issues (as of module creation):\n"
    "  - ODIN elite populations mode-collapsed to monocultures (fix pending).\n"
    "  - Live-vs-backtest Sharpe drift tracker shipped for futures, pending for spot.\n"
    "  - MIMIR/LOKI operate inside each league's frame, never question the frame.\n"
)


def _tail(path, n=50):
    try:
        with open(path) as f:
            lines = f.readlines()
        return "".join(lines[-n:])
    except (OSError, UnicodeDecodeError):
        return "<missing or unreadable: " + path + ">"


def _read(path, max_chars=20000):
    try:
        with open(path) as f:
            s = f.read()
        if len(s) <= max_chars:
            return s
        return s[:max_chars] + "\n... [truncated, " + str(len(s) - max_chars) + " chars remaining]"
    except (OSError, UnicodeDecodeError):
        return "<missing or unreadable: " + path + ">"


def _json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _age_minutes(path):
    try:
        import time as _t
        return round((_t.time() - os.path.getmtime(path)) / 60.0, 1)
    except OSError:
        return None


def _systemctl_status(unit):
    try:
        r = subprocess.run(["systemctl", "is-active", unit],
                           capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return "unknown"


def _elite_summary(league):
    d = os.path.join(RESEARCH, league, "population")
    sharpes, trades = [], []
    for i in range(20):
        p = os.path.join(d, "elite_" + str(i) + ".yaml")
        if not os.path.exists(p):
            break
        try:
            with open(p) as f:
                for line in f:
                    if line.startswith("_sharpe:"):
                        sharpes.append(float(line.split(":", 1)[1].strip()))
                    elif line.startswith("_trades:"):
                        trades.append(int(line.split(":", 1)[1].strip()))
        except (OSError, ValueError):
            continue
    if not sharpes:
        return "empty"
    unique_sharpe = len(set(sharpes))
    tr = "[" + str(min(trades)) + "," + str(max(trades)) + "]" if trades else "n/a"
    return (
        "n=" + str(len(sharpes)) +
        " sharpe_range=[" + ("%.4f" % min(sharpes)) + "," + ("%.4f" % max(sharpes)) + "]" +
        " unique_sharpe=" + str(unique_sharpe) +
        " trades_range=" + tr
    )


def _crontab():
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        return r.stdout if r.returncode == 0 else "<no crontab>"
    except (subprocess.SubprocessError, OSError):
        return "<crontab unavailable>"


def _layer_self_heal():
    """Self-heal + officer operations state."""
    out = ["\n=== LAYER 2: SELF-HEAL + OFFICER OPS ===\n"]

    out.append("--- self_heal_state.json ---")
    sh = _json(os.path.join(WORKSPACE, "competition", "self_heal_state.json"))
    out.append(json.dumps(sh, indent=2)[:4000] if sh else "absent")

    out.append("--- self_heal_readiness.log (last 60) ---")
    out.append(_tail(os.path.join(RESEARCH, "self_heal_readiness.log"), n=60))

    out.append("--- vidar_log.jsonl (last 20 fires) ---")
    out.append(_tail(os.path.join(RESEARCH, "vidar_log.jsonl"), n=20))

    out.append("--- vidar_decisions.jsonl (last 20) ---")
    out.append(_tail(os.path.join(RESEARCH, "vidar_decisions.jsonl"), n=20))

    out.append("--- loki_structural_monitor.json ---")
    lsm = _json(os.path.join(RESEARCH, "loki_structural_monitor.json"))
    out.append(json.dumps(lsm, indent=2)[:3000] if lsm else "absent")

    out.append("--- loki_structural_pauses.json ---")
    lsp = _json(os.path.join(RESEARCH, "loki_structural_pauses.json"))
    out.append(json.dumps(lsp, indent=2)[:2000] if lsp else "absent")

    out.append("--- vidar_inbox_consumer_state.json ---")
    vic = _json(os.path.join(WORKSPACE, "competition", "vidar_inbox_consumer_state.json"))
    out.append(json.dumps(vic, indent=2)[:2000] if vic else "absent")

    out.append("--- vidar_inbox_decisions.jsonl (last 20) ---")
    out.append(_tail(os.path.join(RESEARCH, "vidar_inbox_decisions.jsonl"), n=20))

    out.append("--- tyr_state.json ---")
    ts = _json(os.path.join(RESEARCH, "tyr_state.json"))
    out.append(json.dumps(ts, indent=2)[:2000] if ts else "absent")

    out.append("--- heimdall_state.json ---")
    hs = _json(os.path.join(RESEARCH, "heimdall_state.json"))
    out.append(json.dumps(hs, indent=2)[:2000] if hs else "absent")

    out.append("--- syn_inbox.jsonl (last 40 rows — what SYN saw recently) ---")
    out.append(_tail(os.path.join(WORKSPACE, "syn_inbox.jsonl"), n=40))

    out.append("--- freshness_state.json (research freshness watchdog) ---")
    fs = _json(os.path.join(WORKSPACE, "competition", "freshness_state.json"))
    out.append(json.dumps(fs, indent=2)[:2000] if fs else "absent")

    out.append("--- heartbeat_syn_state.json ---")
    hb = _json(os.path.join(WORKSPACE, "competition", "heartbeat_syn_state.json"))
    out.append(json.dumps(hb, indent=2)[:2000] if hb else "absent")

    out.append("--- sprint_integrity_state.json ---")
    si = _json(os.path.join(WORKSPACE, "competition", "sprint_integrity_state.json"))
    out.append(json.dumps(si, indent=2)[:2000] if si else "absent")

    return "\n".join(out)


def _layer_infrastructure():
    """Services, crons, spend, exchange health, git, dashboard freshness."""
    out = ["\n=== LAYER 3: INFRASTRUCTURE ===\n"]

    out.append("--- systemd unit health ---")
    units = [
        "odin_day.service", "odin_swing.service",
        "odin_futures_day.service", "odin_futures_swing.service",
        "freya.service", "polymarket_syn.service", "kalshi_copy.service",
    ]
    for u in units:
        out.append("  " + u + ": " + _systemctl_status(u))

    out.append("\n--- exchange_health_state.json ---")
    eh = _json(os.path.join(WORKSPACE, "competition", "exchange_health_state.json"))
    out.append(json.dumps(eh, indent=2)[:2500] if eh else "absent")

    out.append("--- anthropic_health_state.json ---")
    ah = _json(os.path.join(WORKSPACE, "competition", "anthropic_health_state.json"))
    out.append(json.dumps(ah, indent=2)[:2500] if ah else "absent")

    out.append("--- gemini_health_state.json ---")
    gh = _json(os.path.join(WORKSPACE, "competition", "gemini_health_state.json"))
    out.append(json.dumps(gh, indent=2)[:2500] if gh else "absent")

    out.append("--- cron_health_state.json ---")
    ch = _json(os.path.join(WORKSPACE, "competition", "cron_health_state.json"))
    out.append(json.dumps(ch, indent=2)[:2500] if ch else "absent")

    out.append("--- crashloop_state.json ---")
    cl = _json(os.path.join(WORKSPACE, "competition", "crashloop_state.json"))
    out.append(json.dumps(cl, indent=2)[:2000] if cl else "absent")

    out.append("--- regression_watch_state.json ---")
    rw = _json(os.path.join(WORKSPACE, "competition", "regression_watch_state.json"))
    out.append(json.dumps(rw, indent=2)[:2000] if rw else "absent")

    out.append("--- odin_memory_state.json ---")
    om = _json(os.path.join(WORKSPACE, "competition", "odin_memory_state.json"))
    out.append(json.dumps(om, indent=2)[:2000] if om else "absent")

    out.append("--- dashboard freshness ---")
    dash_age = _age_minutes("/var/www/dashboard/api/dashboard.json")
    out.append("  dashboard.json age_minutes: " + str(dash_age))

    out.append("--- git state (workspace repo) ---")
    try:
        r = subprocess.run(["git", "-C", WORKSPACE, "status", "--porcelain=1", "-b"],
                           capture_output=True, text=True, timeout=10)
        out.append(r.stdout[:3000])
    except (subprocess.SubprocessError, OSError) as e:
        out.append("git status failed: " + str(e))
    try:
        r = subprocess.run(["git", "-C", WORKSPACE, "log", "--oneline", "-10"],
                           capture_output=True, text=True, timeout=10)
        out.append("recent commits:\n" + r.stdout)
    except (subprocess.SubprocessError, OSError):
        pass

    out.append("--- disk usage (workspace) ---")
    try:
        r = subprocess.run(["du", "-sh", WORKSPACE], capture_output=True, text=True, timeout=15)
        out.append(r.stdout.strip())
    except (subprocess.SubprocessError, OSError):
        pass

    out.append("--- anthropic_usage.jsonl daily totals (last 7d) ---")
    try:
        from collections import defaultdict
        totals = defaultdict(lambda: {"in": 0, "out": 0, "cache_r": 0, "cache_c": 0, "calls": 0})
        with open(ANTHROPIC_USAGE) as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                day = (rec.get("ts") or "")[:10]
                if not day:
                    continue
                t = totals[day]
                t["calls"]   += 1
                t["in"]      += rec.get("input_tokens", 0) or 0
                t["out"]     += rec.get("output_tokens", 0) or 0
                t["cache_r"] += rec.get("cache_read_input_tokens", 0) or 0
                t["cache_c"] += rec.get("cache_creation_input_tokens", 0) or 0
        days = sorted(totals.keys())[-7:]
        for d in days:
            out.append("  " + d + " " + json.dumps(dict(totals[d])))
    except OSError:
        out.append("anthropic_usage.jsonl unreadable")

    return "\n".join(out)


def build_snapshot():
    parts = [ROLE_SUMMARY, MISSION_SUMMARY, ""]

    parts.append("=== CRONTAB (what is actually scheduled) ===")
    parts.append(_crontab())
    parts.append("")

    for L in LEAGUES_CRYPTO:
        parts.append("=== LEAGUE: " + L + " ===")
        gs = _json(os.path.join(RESEARCH, L, "gen_state.json"))
        parts.append("gen_state.json: " + (json.dumps(gs) if gs else "missing"))
        parts.append("elite pop summary: " + _elite_summary(L))
        drift = _json(os.path.join(RESEARCH, L, "backtest_drift.json"))
        parts.append("backtest_drift.json: " + (json.dumps(drift, indent=2) if drift else "absent"))
        parts.append("--- program.md (first 8k) ---")
        parts.append(_read(os.path.join(RESEARCH, L, "program.md"), max_chars=8000))
        parts.append("--- best_strategy.yaml ---")
        parts.append(_read(os.path.join(RESEARCH, L, "best_strategy.yaml"), max_chars=3000))
        parts.append("--- results.tsv (last 40 rows) ---")
        parts.append(_tail(os.path.join(RESEARCH, L, "results.tsv"), n=40))
        parts.append("")

    for L in LEAGUES_PM:
        parts.append("=== LEAGUE: " + L + " (FREYA/prediction markets) ===")
        parts.append("--- best_strategy.yaml ---")
        parts.append(_read(os.path.join(RESEARCH, L, "best_strategy.yaml"), max_chars=3000))
        parts.append("--- results.tsv (last 40 rows) ---")
        parts.append(_tail(os.path.join(RESEARCH, L, "results.tsv"), n=40))
        parts.append("")

    parts.append("=== LOKI RECENT REVERT HISTORY ===")
    rh = _json(os.path.join(RESEARCH, "loki_revert_history.json"))
    parts.append(json.dumps(rh, indent=2) if rh else "no reverts logged")
    parts.append("")

    parts.append("=== LOKI RECENT LOG (last 80 lines) ===")
    parts.append(_tail(os.path.join(RESEARCH, "loki.log"), n=80))
    parts.append("")

    parts.append("=== ANTHROPIC API SPEND (last 30 calls) ===")
    parts.append(_tail(ANTHROPIC_USAGE, n=30))
    parts.append("")

    parts.append(_layer_self_heal())
    parts.append(_layer_infrastructure())

    parts.append("=== LEADERBOARDS (rankings) ===")
    for L in LEAGUES_CRYPTO:
        lb = _json(os.path.join(WORKSPACE, "competition", L, L + "_leaderboard.json"))
        if lb:
            keep = {k: v for k, v in lb.items() if k != "sprint_history"}
            parts.append("--- " + L + " ---")
            parts.append(json.dumps(keep, indent=1)[:6000])
    parts.append("")

    return "\n".join(parts)


def dispatch_vidar(snapshot_path):
    cmd = ["python3", VIDAR, "--mode", "meta_audit", "--snapshot", snapshot_path]
    print("[meta_audit] dispatching: " + " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=VIDAR_TIMEOUT_SEC)
    if r.stdout:
        print(r.stdout)
    if r.returncode != 0:
        raise RuntimeError(
            "vidar meta_audit exited " + str(r.returncode) +
            " stderr: " + (r.stderr or "")[:2000]
        )


def overall_severity(sev_counts):
    if sev_counts.get("critical", 0) > 0:
        return "critical"
    if sev_counts.get("high", 0) > 0:
        return "error"
    if sev_counts.get("medium", 0) > 0:
        return "warning"
    return "info"


def route_to_inbox(sidecar):
    audit_ts     = sidecar.get("audit_ts")
    review_path  = sidecar.get("review_path")
    decision     = sidecar.get("decision") or {}
    parse_ok     = sidecar.get("parse_ok", bool(sidecar.get("decision")))
    sev_counts   = decision.get("severity_counts") or {}
    findings     = decision.get("findings") or []

    # If VIDAR could not parse structured findings (max_tokens cut, malformed
    # JSON, refusal), route a single error row pointing at the review file so
    # Chris can read the raw reasoning on the dashboard or via the file path.
    if not parse_ok:
        with open(SYN_INBOX, "a") as ib:
            ib.write(json.dumps({
                "ts":       datetime.now(timezone.utc).isoformat(),
                "source":   "meta_audit",
                "severity": "error",
                "audit_ts": audit_ts,
                "summary":  "meta_audit produced unstructured output (parse failed); see review file",
                "review":   review_path,
            }) + "\n")
        return 1

    now = datetime.now(timezone.utc).isoformat()
    rows = []

    # One header row per audit.
    rows.append({
        "ts":        now,
        "source":    "meta_audit",
        "severity":  overall_severity(sev_counts),
        "audit_ts":  audit_ts,
        "summary":   decision.get("summary", ""),
        "counts":    sev_counts,
        "review":    review_path,
    })

    # One row per critical finding (these alone page Chris via the narrow
    # sys_heartbeat carve-out; non-critical rows stay inbox-only for VIDAR).
    for f in findings:
        if f.get("severity") == "critical":
            rows.append({
                "ts":              now,
                "source":          "meta_audit",
                "severity":        "critical",
                "audit_ts":        audit_ts,
                "finding_id":      f.get("id"),
                "title":           f.get("title"),
                "evidence":        f.get("evidence"),
                "action":          f.get("suggested_action"),
                "delegable_to_loki": bool(f.get("delegable_to_loki", False)),
                "review":          review_path,
            })

    with open(SYN_INBOX, "a") as ib:
        for r in rows:
            ib.write(json.dumps(r) + "\n")
    return len(rows)


def run():
    os.makedirs(META_AUDIT_DIR, exist_ok=True)

    snapshot = build_snapshot()
    # Persist snapshot alongside review for forensic reproducibility.
    ts_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snap_path = os.path.join(META_AUDIT_DIR, "snapshot_" + ts_str + ".txt")
    # F3: atomic write — guarantees vidar dispatch sees a complete file.
    snap_tmp = snap_path + ".tmp"
    with open(snap_tmp, "w") as sf:
        sf.write(snapshot)
        sf.flush()
        os.fsync(sf.fileno())
    os.replace(snap_tmp, snap_path)
    print("[meta_audit] snapshot: " + snap_path + " (" + str(len(snapshot)) + " chars)")

    dispatch_vidar(snap_path)

    if not os.path.exists(LATEST_SIDECAR):
        raise RuntimeError("vidar meta_audit did not write " + LATEST_SIDECAR)
    with open(LATEST_SIDECAR) as f:
        sidecar = json.load(f)

    n = route_to_inbox(sidecar)
    counts = (sidecar.get("decision") or {}).get("severity_counts", {})
    print("[meta_audit] routed " + str(n) + " rows to syn_inbox; counts=" + json.dumps(counts))
    return sidecar


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        err = {
            "ts":       datetime.now(timezone.utc).isoformat(),
            "source":   "meta_audit",
            "severity": "error",
            "summary":  "meta_audit run failed: " + type(e).__name__ + ": " + str(e),
        }
        try:
            with open(SYN_INBOX, "a") as ib:
                ib.write(json.dumps(err) + "\n")
        except OSError:
            pass
        raise
