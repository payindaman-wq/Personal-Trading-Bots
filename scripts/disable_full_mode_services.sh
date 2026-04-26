#!/usr/bin/env bash
# disable_full_mode_services.sh
# Run this on a lite-mode VPS to stop and disable all full-mode AI services.
# Safe to run multiple times (idempotent).
#
# What this disables:
#   - ODIN systemd services (4 leagues x odin_researcher_v2.py)
#   - FREYA systemd service (prediction markets researcher)
#
# MIMIR, VIDAR/vidar_executor, meta_audit, LOKI, TYR, HEIMDALL are
# cron-driven. They already exit cleanly if config.mode != "full".
# If you want to remove those cron entries entirely, see:
#   crontab -e   and comment out the lines labeled AI_OFFICER_FULLMODE

set -euo pipefail

FULL_MODE_SERVICES="odin_day odin_swing odin_futures_day odin_futures_swing freya"

echo ""
echo "Disabling full-mode AI services..."
echo "(These services require Anthropic/Gemini API keys and are inactive in lite mode.)"
echo ""

for svc in $FULL_MODE_SERVICES; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        systemctl stop "$svc"
        echo "  stopped: $svc"
    fi
    if systemctl is-enabled --quiet "$svc" 2>/dev/null; then
        systemctl disable "$svc"
        echo "  disabled: $svc"
    else
        echo "  already disabled: $svc"
    fi
done

echo ""
echo "Done. Cron-driven officers (LOKI, TYR, HEIMDALL, vidar_executor, meta_audit)"
echo "will exit at startup because config.mode=lite -- no further action needed."
echo ""
echo "To re-enable (switch to full mode):"
echo "  1. Set mode: 'full' in config.yaml"
echo "  2. Fill in anthropic.api_key and gemini.api_key in config.yaml"
echo "  3. Run: systemctl enable --now odin_day odin_swing odin_futures_day odin_futures_swing freya"
