#!/usr/bin/env python3
"""
strategy_sync.py — Friend-side champion strategy sync from upstream.

Pulls published champion strategies from Mother's upstream repo (via git pull
--rebase upstream main) so lite-mode VPS instances execute the latest research
without paying for AI.

Early-exit if config.mode != "lite" (only friend VPS syncs; Mother publishes).

NJORD strategy_source contract (Session Q):
  mode=lite -> published/<league>/champion.yaml  (this script keeps it current)
  mode=full -> research/<league>/best_strategy.yaml  (ODIN keeps it current)

Failure handling: after 3+ consecutive hours of sync failures, writes a
syn_inbox entry with tg_allowed:true so the operator is paged.

State: competition/strategy_sync_state.json

Cron: 15 */4 * * * python3 /root/.openclaw/workspace/strategy_sync.py >> /root/.openclaw/workspace/competition/strategy_sync.log 2>&1
  (15-min offset from publisher avoids race condition)

CLI: python3 strategy_sync.py [--dry-run]
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

WORKSPACE   = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
PUBLISHED   = os.path.join(WORKSPACE, "published")
COMPETITION = os.path.join(WORKSPACE, "competition")
STATE_FILE  = os.path.join(COMPETITION, "strategy_sync_state.json")
LOCK_FILE   = os.path.join(COMPETITION, "strategy_sync.lock")
SYN_INBOX   = os.path.join(WORKSPACE, "syn_inbox.jsonl")

FAILURE_ALERT_HOURS = 3
UPSTREAM_REMOTE     = "upstream"
MAX_CHAMPION_AGE_H  = 24    # WARN if champion is older than this


def _ts_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _log(msg: str) -> None:
    print(f"[sync] {_ts_iso()} {msg}", flush=True)


def _load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {
        "last_success_ts": None,
        "consecutive_failures": 0,
        "last_failure_ts": None,
        "alert_sent_ts": None,
    }


def _save_state(state: dict) -> None:
    os.makedirs(COMPETITION, exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)


def _run(cmd: list, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=WORKSPACE, capture_output=capture, text=True, timeout=120)


def _write_syn_inbox(entry: dict) -> None:
    try:
        with open(SYN_INBOX, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        _log(f"WARN could not write syn_inbox: {e}")


def _check_upstream_remote() -> bool:
    result = _run(["git", "remote"], capture=True)
    return UPSTREAM_REMOTE in result.stdout.split()


def _check_champion_freshness(leagues: list) -> None:
    now = datetime.now(timezone.utc)
    for league in leagues:
        meta_path = os.path.join(PUBLISHED, league, "champion.meta.json")
        if not os.path.exists(meta_path):
            _log(f"WARN {league}: champion.meta.json missing")
            continue
        try:
            meta = json.load(open(meta_path))
            ts_str = meta.get("ts", "")
            if not ts_str:
                continue
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            age_h = (now - ts).total_seconds() / 3600
            if age_h > MAX_CHAMPION_AGE_H:
                _log(f"WARN {league}: champion is {age_h:.1f}h old (>{MAX_CHAMPION_AGE_H}h) -- Mother may be down")
        except Exception:
            pass


def _record_failure(state: dict, reason: str) -> None:
    state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
    state["last_failure_ts"] = _ts_iso()
    _log(f"failure #{state['consecutive_failures']}: {reason}")
    _save_state(state)


def _maybe_alert(state: dict, leagues: list) -> None:
    if not state.get("last_failure_ts"):
        return

    last_success = state.get("last_success_ts")
    if last_success:
        try:
            last_ok = datetime.fromisoformat(last_success.replace("Z", "+00:00"))
            hours_since = (datetime.now(timezone.utc) - last_ok).total_seconds() / 3600
        except Exception:
            hours_since = 99.0
    else:
        hours_since = 99.0

    if hours_since < FAILURE_ALERT_HOURS:
        return

    alert_sent = state.get("alert_sent_ts")
    if alert_sent:
        try:
            sent_dt = datetime.fromisoformat(alert_sent.replace("Z", "+00:00"))
            if (datetime.now(timezone.utc) - sent_dt).total_seconds() < 3600 * 6:
                return   # already alerted within 6h
        except Exception:
            pass

    entry = {
        "ts": _ts_iso(),
        "source": "strategy_sync",
        "severity": "warning",
        "anomaly": "sync_failure",
        "message": (
            f"strategy_sync has been failing for {hours_since:.1f}h -- "
            f"lite-mode VPS is running stale strategies. Leagues: {leagues}"
        ),
        "tg_allowed": True,
    }
    _write_syn_inbox(entry)
    state["alert_sent_ts"] = _ts_iso()
    _log(f"wrote syn_inbox alert after {hours_since:.1f}h of failures")
    _save_state(state)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync champion strategies from upstream repo.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be synced without pulling.")
    args = parser.parse_args()

    sys.path.insert(0, WORKSPACE)
    from config_loader import config

    mode = getattr(config, "mode", "full")
    upstream_branch = config.upstream.branch
    if mode != "lite":
        _log(f"mode={mode} -- exiting (only mode=lite syncs from upstream)")
        sys.exit(0)

    leagues = list(getattr(config.fleet, "leagues_enabled", []))
    if not leagues:
        _log("no leagues_enabled in config -- nothing to sync")
        sys.exit(0)

    if not args.dry_run:
        lock_fd = open(LOCK_FILE, "w")
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _log("another sync instance is running -- exiting")
            sys.exit(0)

    state = _load_state()

    if args.dry_run:
        upstream_ok = _check_upstream_remote()
        if not upstream_ok:
            _log(f"WARN: '{UPSTREAM_REMOTE}' remote not configured -- friend VPS needs: git remote add upstream {config.upstream.repo}")
        _log(f"[dry-run] would: git fetch {UPSTREAM_REMOTE} {upstream_branch} && git pull --rebase {UPSTREAM_REMOTE} {upstream_branch}")
        for league in leagues:
            champion = os.path.join(PUBLISHED, league, "champion.yaml")
            meta_path = os.path.join(PUBLISHED, league, "champion.meta.json")
            status = "MISSING (will appear after first Mother publish)"
            if os.path.exists(champion):
                if os.path.exists(meta_path):
                    try:
                        import json as _j
                        meta = _j.load(open(meta_path))
                        status = f"present sharpe={meta.get('source_sharpe')} gen={meta.get('source_gen')}"
                    except Exception:
                        status = "present"
                else:
                    status = "present"
            _log(f"[dry-run] {league}: {status}")
        sys.exit(0)

    if not _check_upstream_remote():
        _log(f"ERROR: '{UPSTREAM_REMOTE}' remote not configured.")
        _log(f"  Run: git remote add upstream {config.upstream.repo}")
        _record_failure(state, "no upstream remote")
        sys.exit(1)

    fetch = _run(["git", "fetch", UPSTREAM_REMOTE, upstream_branch], capture=True)
    if fetch.returncode != 0:
        _log(f"ERROR git fetch failed: {fetch.stderr.strip()}")
        _record_failure(state, f"git fetch: {fetch.stderr.strip()[:120]}")
        _maybe_alert(state, leagues)
        sys.exit(1)

    pull = _run(["git", "pull", "--rebase", UPSTREAM_REMOTE, upstream_branch], capture=True)
    if pull.returncode != 0:
        _log(f"ERROR git pull --rebase failed: {pull.stderr.strip()}")
        _record_failure(state, f"git pull: {pull.stderr.strip()[:120]}")
        _maybe_alert(state, leagues)
        sys.exit(1)

    _log(f"git pull: {pull.stdout.strip()[:120] or 'already up to date'}")

    updated = []
    missing = []
    for league in leagues:
        champion = os.path.join(PUBLISHED, league, "champion.yaml")
        if os.path.exists(champion):
            updated.append(league)
        else:
            _log(f"WARN {league}: published/{league}/champion.yaml missing -- no strategy from Mother yet")
            missing.append(league)

    if updated:
        _check_champion_freshness(updated)

    _log(f"sync complete -- {len(updated)} leagues: {updated}" + (f" | missing: {missing}" if missing else ""))

    state["last_success_ts"] = _ts_iso()
    state["consecutive_failures"] = 0
    state["alert_sent_ts"] = None
    _save_state(state)


if __name__ == "__main__":
    main()
