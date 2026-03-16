#!/usr/bin/env python3
"""
spread_start_cycle.py — Start a new Spread League cycle.

Run at the beginning of each new cycle (after spread_cycle_advance.py completes).
  1. Runs pair health check — auto-replaces any RETIRE pairs
  2. Starts a new 7-day sprint

Usage: python3 spread_start_cycle.py [--dry-run]
"""
import argparse, os, sys, subprocess
from datetime import datetime, timezone

WORKSPACE = "/root/.openclaw/workspace"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without modifying files")
    args = parser.parse_args()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"\n{'='*60}")
    print(f"  SPREAD START CYCLE  |  {now_str}")
    if args.dry_run:
        print("  DRY RUN — no changes will be made")
    print(f"{'='*60}\n")

    # ── 1. Pair health check ──────────────────────────────────────────────
    print("Step 1: Running pair health check...")
    health_cmd = [
        sys.executable,
        os.path.join(WORKSPACE, "pair_health_check.py"),
        "--league", "spread",
        "--auto-replace",
    ]
    if args.dry_run:
        health_cmd.append("--dry-run")

    result = subprocess.run(health_cmd)
    if result.returncode != 0:
        print("  ERROR: pair health check failed — aborting sprint start")
        sys.exit(1)

    if args.dry_run:
        print("\n[dry-run] Would now start sprint via spread_competition_start.py")
        print(f"{'='*60}")
        print("  DRY RUN complete — no files modified.")
        print(f"{'='*60}\n")
        return

    # ── 2. Start sprint ───────────────────────────────────────────────────
    print("\nStep 2: Starting new sprint...")
    start_cmd = [
        sys.executable,
        os.path.join(WORKSPACE, "spread_competition_start.py"),
    ]
    result = subprocess.run(start_cmd)
    if result.returncode != 0:
        print("  ERROR: spread_competition_start.py failed")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("  Spread cycle started successfully.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
