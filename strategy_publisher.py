#!/usr/bin/env python3
"""
strategy_publisher.py — Mother-side champion strategy publisher.

Reads research/<league>/best_strategy.yaml for each enabled league, sanitizes
(strips _-prefixed fields and debug metadata), and publishes to published/<league>/
in the git repo. Commits and pushes to origin so friend forks can pull.

Early-exit if config.mode != "full" (only Mother publishes).
Idempotent: skips the commit when no strategy has changed since last publish.

NJORD strategy_source contract (Session Q):
  mode=full -> research/<league>/best_strategy.yaml
  mode=lite -> published/<league>/champion.yaml
  NJORD reads these paths directly. strategy_sync.py keeps the lite path current.

Cron: 0 */4 * * * python3 /root/.openclaw/workspace/strategy_publisher.py >> /root/.openclaw/workspace/competition/strategy_publisher.log 2>&1

CLI: python3 strategy_publisher.py [--dry-run]
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

import yaml

WORKSPACE   = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
RESEARCH    = os.path.join(WORKSPACE, "research")
PUBLISHED   = os.path.join(WORKSPACE, "published")
COMPETITION = os.path.join(WORKSPACE, "competition")
STATE_FILE  = os.path.join(COMPETITION, "strategy_publisher_state.json")
LOCK_FILE   = os.path.join(COMPETITION, "strategy_publisher.lock")

SANITIZATION_VERSION = 1
MIN_PUBLISH_SECONDS  = 3600   # 1 hour between pushes to avoid spamming upstream

_STRIP_PREFIXES = ("_",)       # strip any key starting with _


def _ts_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _log(msg: str) -> None:
    print(f"[publisher] {_ts_iso()} {msg}", flush=True)


def _load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"last_published_ts": None, "last_hashes": {}}


def _save_state(state: dict) -> None:
    os.makedirs(COMPETITION, exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)


def _sanitize(raw: dict) -> dict:
    out = {}
    for k, v in raw.items():
        if any(k.startswith(p) for p in _STRIP_PREFIXES):
            continue
        out[k] = _sanitize(v) if isinstance(v, dict) else v
    return out


def _yaml_hash(obj: dict) -> str:
    content = yaml.dump(obj, default_flow_style=False, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _run(cmd: list, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=WORKSPACE, capture_output=capture, text=True)


def _publish_league(league: str, now_ts: str, dry_run: bool) -> tuple:
    src = os.path.join(RESEARCH, league, "best_strategy.yaml")
    if not os.path.exists(src):
        _log(f"{league}: no best_strategy.yaml -- skipping")
        return False, None

    with open(src) as f:
        raw = yaml.safe_load(f)
    if not isinstance(raw, dict):
        _log(f"{league}: invalid YAML -- skipping")
        return False, None

    clean = _sanitize(raw)

    meta_src = {}
    meta_path = os.path.join(RESEARCH, league, "best_strategy.meta.json")
    if os.path.exists(meta_path):
        try:
            meta_src = json.load(open(meta_path))
        except Exception:
            pass

    gen_state = {}
    gen_path = os.path.join(RESEARCH, league, "gen_state.json")
    if os.path.exists(gen_path):
        try:
            gen_state = json.load(open(gen_path))
        except Exception:
            pass

    champion_meta = {
        "ts": now_ts,
        "source_gen": gen_state.get("gen"),
        "source_sharpe": meta_src.get("sharpe"),
        "source_oos_sharpe": meta_src.get("oos_sharpe"),
        "sanitization_version": SANITIZATION_VERSION,
    }

    stripped = [k for k in raw if k not in clean]
    _log(f"{league}: sharpe={champion_meta['source_sharpe']} gen={champion_meta['source_gen']} stripped={stripped or 'none'}")

    if dry_run:
        return True, champion_meta

    pub_dir = os.path.join(PUBLISHED, league)
    os.makedirs(pub_dir, exist_ok=True)

    with open(os.path.join(pub_dir, "champion.yaml"), "w") as f:
        f.write(yaml.dump(clean, default_flow_style=False, allow_unicode=True))

    tmp = os.path.join(pub_dir, "champion.meta.json.tmp")
    with open(tmp, "w") as f:
        json.dump(champion_meta, f, indent=2)
    os.replace(tmp, os.path.join(pub_dir, "champion.meta.json"))

    return True, champion_meta


def _build_push_url(cfg) -> str:
    """Return authenticated URL for the upstream_pub transient remote."""
    upstream = getattr(cfg, "upstream", None)
    repo = (getattr(upstream, "repo", "https://github.com/payindaman-wq/Personal-Trading-Bots")
            if upstream else "https://github.com/payindaman-wq/Personal-Trading-Bots")
    pat = getattr(upstream, "pat", "") if upstream else ""
    pat = pat or os.environ.get("UPSTREAM_PAT", "")
    if not pat:
        r = subprocess.run(["git", "remote", "get-url", "origin"],
                           cwd=WORKSPACE, capture_output=True, text=True)
        m = re.search(r"https://([^@\s]+)@", r.stdout)
        if m:
            pat = m.group(1)
    if pat and "://" in repo and "@" not in repo:
        repo = repo.replace("://", f"://{pat}@", 1)
    return repo

def main() -> None:
    parser = argparse.ArgumentParser(description="Publish champion strategies to upstream repo.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be published without writing or committing.")
    args = parser.parse_args()

    sys.path.insert(0, WORKSPACE)
    from config_loader import config

    mode = getattr(config, "mode", "full")
    if mode != "full":
        _log(f"mode={mode} -- exiting (only mode=full publishes)")
        sys.exit(0)

    leagues = list(getattr(config.fleet, "leagues_enabled", []))
    if not leagues:
        _log("no leagues_enabled in config -- nothing to publish")
        sys.exit(0)

    if not args.dry_run:
        lock_fd = open(LOCK_FILE, "w")
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _log("another publisher instance is running -- exiting")
            sys.exit(0)

    state = _load_state()

    if not args.dry_run and state.get("last_published_ts"):
        last = datetime.fromisoformat(state["last_published_ts"].replace("Z", "+00:00"))
        elapsed = (datetime.now(timezone.utc) - last).total_seconds()
        if elapsed < MIN_PUBLISH_SECONDS:
            _log(f"last publish was {int(elapsed)}s ago (min {MIN_PUBLISH_SECONDS}s) -- skipping")
            sys.exit(0)

    now_ts = _ts_iso()
    touched = []
    new_hashes = {}

    for league in leagues:
        src = os.path.join(RESEARCH, league, "best_strategy.yaml")
        if not os.path.exists(src):
            continue

        with open(src) as f:
            raw = yaml.safe_load(f)
        if not isinstance(raw, dict):
            continue

        clean = _sanitize(raw)
        h = _yaml_hash(clean)
        new_hashes[league] = h

        if not args.dry_run and state["last_hashes"].get(league) == h:
            _log(f"{league}: unchanged (hash={h}) -- skipping")
            continue

        ok, meta = _publish_league(league, now_ts, args.dry_run)
        if ok:
            touched.append(league)

    if not touched:
        _log("nothing changed -- no commit")
        sys.exit(0)

    if args.dry_run:
        _log(f"[dry-run] would commit+push: {touched}")
        sys.exit(0)

    # Stage only published/ -- never git add -A
    _run(["git", "add", "published/"])

    commit_msg = f"[publish] {' '.join(touched)} @ {now_ts}"
    result = _run(["git", "commit", "-m", commit_msg], capture=True)
    if result.returncode != 0:
        if "nothing to commit" in (result.stdout + result.stderr):
            _log("git: nothing to commit -- skipping push")
            sys.exit(0)
        _log(f"ERROR git commit failed: {result.stderr.strip()}")
        sys.exit(1)

    _log(f"committed: {commit_msg}")

    upstream_branch = getattr(config.upstream, "branch", "master")
    repo_display = getattr(config.upstream, "repo", "upstream")
    push_url = _build_push_url(config)
    _run(["git", "remote", "remove", "upstream_pub"], capture=True)  # remove stale if any
    _run(["git", "remote", "add", "upstream_pub", push_url])
    push = _run(["git", "push", "upstream_pub", f"HEAD:{upstream_branch}"], capture=True)
    _run(["git", "remote", "remove", "upstream_pub"], capture=True)  # cleanup
    if push.returncode != 0:
        _log(f"ERROR git push failed: {push.stderr.strip()}")
        sys.exit(1)

    _log(f"pushed {len(touched)} league(s) to {repo_display}: {touched}")

    state["last_published_ts"] = now_ts
    state["last_hashes"].update(new_hashes)
    _save_state(state)


if __name__ == "__main__":
    main()
