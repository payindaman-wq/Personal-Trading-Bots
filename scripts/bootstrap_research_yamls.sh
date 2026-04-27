#!/usr/bin/env bash
# Materializes best_strategy.yaml from seed_strategy.yaml for each research league.
# Idempotent: skips leagues where best_strategy.yaml already exists.
# Called by scripts/setup.sh on first run; safe to re-run at any time.

set -euo pipefail

WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEAGUES=(day swing futures_day futures_swing pm)

echo "Bootstrapping research strategy files..."
for league in "${LEAGUES[@]}"; do
    dir="${WORKSPACE}/research/${league}"
    seed="${dir}/seed_strategy.yaml"
    live="${dir}/best_strategy.yaml"

    if [[ ! -f "${seed}" ]]; then
        echo "  SKIP ${league}: no seed_strategy.yaml found"
        continue
    fi

    if [[ -f "${live}" ]]; then
        echo "  SKIP ${league}: best_strategy.yaml already exists (preserving live state)"
    else
        cp "${seed}" "${live}"
        echo "  CREATED ${league}/best_strategy.yaml from seed"
    fi
done

echo "Bootstrap complete."
