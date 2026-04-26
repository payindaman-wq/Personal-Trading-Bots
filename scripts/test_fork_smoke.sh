#!/usr/bin/env bash
# test_fork_smoke.sh -- zero-to-paper smoke test for fork validation.
#
# Simulates a friend cloning the repo, running non-interactive lite-mode setup,
# validating config + reachability, checking Python imports, and running the
# NJORD paper smoke test. Exits 0 only if every step passes.
# Leaves TMPDIR intact on failure for inspection.
#
# Usage:
#   bash scripts/test_fork_smoke.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SMOKE_TMP="$(mktemp -d)"
FORK_DIR="$SMOKE_TMP/fork"
START_TS="$(date +%s)"

banner() { echo ""; echo "[smoke] === $* ==="; }
step()   { echo "[smoke] $*"; }

on_fail() {
    echo ""
    echo "[smoke] FAILED -- inspect: $FORK_DIR"
    exit 1
}
trap on_fail ERR

banner "Setup"
step "FORK_DIR=$FORK_DIR"
step "cloning repo..."
git clone "$REPO_ROOT" "$FORK_DIR"

cd "$FORK_DIR"

# Export these so config_loader and all Python modules use the fork's config.
export WORKSPACE="$FORK_DIR"
export CONFIG_PATH="$FORK_DIR/config.yaml"

banner "Step 1: non-interactive lite-mode setup"
TOOLKIT_MODE=lite \
TOOLKIT_TG_TOKEN="" \
TOOLKIT_TG_CHAT="" \
TOOLKIT_KRAKEN_KEY="" \
TOOLKIT_KRAKEN_SECRET="" \
TOOLKIT_VPS_HOST="" \
TOOLKIT_ANTHROPIC_KEY="" \
TOOLKIT_GEMINI_KEY="" \
bash scripts/setup.sh --non-interactive --no-cron
step "setup.sh exited 0"

banner "Step 2: sanity_check.sh"
bash scripts/sanity_check.sh
step "sanity_check.sh exited 0"

banner "Step 3: Python imports"
python3 - << 'PYEOF'
import sys, os
sys.path.insert(0, ".")
sys.path.insert(0, "./research")
import config_loader
import strategy_sync
from research import njord, njord_allocator
print("imports OK: config_loader, strategy_sync, research.njord, research.njord_allocator")
PYEOF

banner "Step 4: NJORD paper smoke test"
python3 research/test_njord_smoke.py

banner "Done"
END_TS="$(date +%s)"
echo "[smoke] all steps passed in $((END_TS - START_TS))s"
rm -rf "$SMOKE_TMP"
