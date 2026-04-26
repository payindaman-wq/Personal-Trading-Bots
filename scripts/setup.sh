#!/usr/bin/env bash
# setup.sh -- initial configuration for crypto-trading-toolkit
#
# Usage:
#   ./scripts/setup.sh                   full mode (all AI officers)
#   ./scripts/setup.sh --mode lite       lite mode (no AI, sync strategies from upstream)
#   ./scripts/setup.sh --mode full       explicit full mode
#   ./scripts/setup.sh --non-interactive read values from TOOLKIT_* env vars (CI/automation)
#   ./scripts/setup.sh --no-cron         skip crontab modification
#   ./scripts/setup.sh --help            show this help

set -euo pipefail

CONFIG="config.yaml"
WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_URL="https://github.com/coldstoneadmin/crypto-trading-toolkit"

# TOOLKIT_MODE env var sets default; --mode flag takes explicit precedence.
MODE="${TOOLKIT_MODE:-full}"
NON_INTERACTIVE=0
NO_CRON=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --mode) MODE="$2"; shift 2 ;;
        --mode=*) MODE="${1#--mode=}"; shift ;;
        --non-interactive) NON_INTERACTIVE=1; shift ;;
        --no-cron) NO_CRON=1; shift ;;
        --help|-h)
            cat << 'HELPEOF'
Usage: scripts/setup.sh [OPTIONS]

Options:
  --mode lite|full         Mode: lite (no AI, sync from upstream) or full (all officers). Default: full.
  --non-interactive        Read all values from TOOLKIT_* env vars instead of prompting.
  --no-cron                Skip crontab modification (useful in sandboxed envs).
  --help, -h               Show this help.

Non-interactive env vars (used with --non-interactive):
  TOOLKIT_MODE             Mode override (lite or full). --mode flag takes precedence.
  TOOLKIT_ANTHROPIC_KEY    Anthropic API key (required in full mode).
  TOOLKIT_GEMINI_KEY       Gemini API key (required in full mode).
  TOOLKIT_KRAKEN_KEY       Kraken API key (optional in lite mode).
  TOOLKIT_KRAKEN_SECRET    Kraken API secret (optional in lite mode).
  TOOLKIT_TG_TOKEN         Telegram bot token (optional).
  TOOLKIT_TG_CHAT          Telegram chat ID (optional).
  TOOLKIT_VPS_HOST         VPS host user@host or IP (optional in lite mode).
  TOOLKIT_DASHBOARD_DOMAIN Dashboard domain (optional).
  TOOLKIT_ANTHROPIC_BUDGET Anthropic daily budget USD (default: 10).

Examples:
  # Lite mode CI setup (no keys required):
  TOOLKIT_MODE=lite bash scripts/setup.sh --non-interactive

  # Full mode with explicit keys:
  TOOLKIT_ANTHROPIC_KEY=sk-ant-... TOOLKIT_GEMINI_KEY=AI... \
    TOOLKIT_VPS_HOST=root@1.2.3.4 bash scripts/setup.sh --mode full --non-interactive
HELPEOF
            exit 0
            ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

if [[ "$MODE" != "full" && "$MODE" != "lite" ]]; then
    echo "ERROR: --mode must be 'full' or 'lite'"; exit 1
fi

prompt_value() {
    local label="$1" var="$2" default="${3:-}" secret="${4:-no}"
    if [[ "$secret" == "yes" ]]; then
        read -rsp "  $label${default:+ [$default]}: " val; echo
    else
        read -rp  "  $label${default:+ [$default]}: " val
    fi
    [[ -z "$val" && -n "$default" ]] && val="$default"
    printf -v "$var" '%s' "$val"
}

echo ""
echo "crypto-trading-toolkit setup -- mode: $MODE"
echo "------------------------------------------"
echo "This script writes config.yaml (gitignored). Re-running overwrites after confirmation."
echo ""

if [[ -f "$CONFIG" ]]; then
    if [[ $NON_INTERACTIVE -eq 0 ]]; then
        read -rp "config.yaml already exists. Overwrite? [y/N] " confirm
        [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
    fi
fi

if [[ $NON_INTERACTIVE -eq 1 ]]; then
    ANTHROPIC_KEY="${TOOLKIT_ANTHROPIC_KEY:-}"
    GEMINI_KEY="${TOOLKIT_GEMINI_KEY:-}"
    KRAKEN_KEY="${TOOLKIT_KRAKEN_KEY:-}"
    KRAKEN_SECRET="${TOOLKIT_KRAKEN_SECRET:-}"
    TG_TOKEN="${TOOLKIT_TG_TOKEN:-}"
    TG_CHAT="${TOOLKIT_TG_CHAT:-}"
    VPS_HOST="${TOOLKIT_VPS_HOST:-}"
    DASHBOARD_DOMAIN="${TOOLKIT_DASHBOARD_DOMAIN:-}"
    ANTHROPIC_BUDGET="${TOOLKIT_ANTHROPIC_BUDGET:-10}"
else
    if [[ "$MODE" == "full" ]]; then
        echo "Required keys (full mode):"
        prompt_value "Anthropic API key" ANTHROPIC_KEY "" yes
        prompt_value "Gemini API key"    GEMINI_KEY    "" yes
    else
        ANTHROPIC_KEY=""
        GEMINI_KEY=""
        echo "(Lite mode: Anthropic + Gemini keys not required -- strategies pulled from upstream)"
    fi

    echo ""
    echo "Kraken trading keys:"
    prompt_value "Kraken API key"    KRAKEN_KEY    "" yes
    prompt_value "Kraken API secret" KRAKEN_SECRET "" yes

    echo ""
    echo "Telegram alerts (leave blank to skip):"
    prompt_value "Telegram bot token" TG_TOKEN "" yes
    prompt_value "Telegram chat ID"   TG_CHAT  ""

    echo ""
    echo "Infrastructure:"
    prompt_value "VPS host (user@host or IP)"   VPS_HOST         ""
    prompt_value "Dashboard domain (optional)"  DASHBOARD_DOMAIN ""
    prompt_value "Anthropic daily budget USD"   ANTHROPIC_BUDGET "10"
fi

errors=0
if [[ "$MODE" == "full" ]]; then
    [[ -z "$ANTHROPIC_KEY" ]] && { echo "ERROR: Anthropic API key required in full mode."; errors=1; }
    [[ -z "$GEMINI_KEY" ]]    && { echo "ERROR: Gemini API key required in full mode.";    errors=1; }
    [[ -z "$VPS_HOST" ]]      && { echo "ERROR: VPS host is required in full mode.";       errors=1; }
fi
[[ $errors -ne 0 ]] && exit 1

cat > "$CONFIG" << 'CONFIGEOF'
config_version: 1

mode: "MODE_PLACEHOLDER"

anthropic:
  api_key: "ANTHROPIC_KEY_PLACEHOLDER"
  daily_budget_usd: ANTHROPIC_BUDGET_PLACEHOLDER
  throttle_at_pct: 80

gemini:
  api_key: "GEMINI_KEY_PLACEHOLDER"

kraken:
  api_key: "KRAKEN_KEY_PLACEHOLDER"
  api_secret: "KRAKEN_SECRET_PLACEHOLDER"

telegram:
  bot_token: "TG_TOKEN_PLACEHOLDER"
  chat_id: "TG_CHAT_PLACEHOLDER"

vps:
  host: "VPS_HOST_PLACEHOLDER"
  workspace: "/root/.openclaw/workspace"

dashboard:
  domain: "DASHBOARD_DOMAIN_PLACEHOLDER"
  branding: "Trading Toolkit"

mission:
  target: "Define your own profit target"

fleet:
  leagues_enabled:
    - day
    - swing
    - futures_day
    - futures_swing
    - polymarket

njord:
  enabled: false
  mode: "paper"
  total_capital_usd: 0
  per_bot_max_pct: 10
  drawdown_kill_pct: 15
  league_weights:
    day: 0.35
    swing: 0.25
    futures_day: 0.20
    futures_swing: 0.10
    polymarket: 0.10
  telegram_required_for_tier3: true
CONFIGEOF

sed -i \
    -e "s|MODE_PLACEHOLDER|${MODE}|" \
    -e "s|ANTHROPIC_KEY_PLACEHOLDER|${ANTHROPIC_KEY}|" \
    -e "s|GEMINI_KEY_PLACEHOLDER|${GEMINI_KEY}|" \
    -e "s|KRAKEN_KEY_PLACEHOLDER|${KRAKEN_KEY}|" \
    -e "s|KRAKEN_SECRET_PLACEHOLDER|${KRAKEN_SECRET}|" \
    -e "s|TG_TOKEN_PLACEHOLDER|${TG_TOKEN}|" \
    -e "s|TG_CHAT_PLACEHOLDER|${TG_CHAT}|" \
    -e "s|VPS_HOST_PLACEHOLDER|${VPS_HOST}|" \
    -e "s|DASHBOARD_DOMAIN_PLACEHOLDER|${DASHBOARD_DOMAIN}|" \
    -e "s|ANTHROPIC_BUDGET_PLACEHOLDER|${ANTHROPIC_BUDGET}|" \
    "$CONFIG"

echo ""
echo "config.yaml written."

# ----- Mode-specific post-setup -----

if [[ "$MODE" == "lite" ]]; then
    echo ""
    echo "Lite mode: configuring upstream remote..."

    # Add upstream remote (idempotent)
    if git remote get-url upstream &>/dev/null 2>&1; then
        echo "  upstream remote already configured."
    else
        git remote add upstream "$UPSTREAM_URL"
        echo "  Added upstream remote: $UPSTREAM_URL"
    fi

    # Initial pull to get published/ champions (non-fatal: cron will sync on first run)
    echo "  Fetching initial champion strategies from upstream..."
    git fetch upstream main || echo "  WARN: could not reach upstream. Strategies will sync on first cron run."
    git pull --rebase upstream main || echo "  WARN: initial pull failed. Run manually: git pull --rebase upstream main"

    if [[ $NO_CRON -eq 0 ]]; then
        # Install strategy_sync cron (idempotent)
        SYNC_CRON="15 */4 * * * python3 ${WORKSPACE}/strategy_sync.py >> ${WORKSPACE}/competition/strategy_sync.log 2>&1"
        if crontab -l 2>/dev/null | grep -qF "strategy_sync.py"; then
            echo "  strategy_sync cron already installed."
        else
            (crontab -l 2>/dev/null; echo "# Hub-and-spoke: sync champion strategies from upstream every 4h"; echo "$SYNC_CRON") | crontab -
            echo "  Installed strategy_sync cron: $SYNC_CRON"
        fi
    else
        echo "  --no-cron: skipping strategy_sync cron installation."
    fi

    echo ""
    echo "Lite mode setup complete. Your VPS will pull champion strategies from:"
    echo "  $UPSTREAM_URL"
    echo ""
    echo "NJORD is disabled by default. To start paper trading:"
    echo "  Edit config.yaml: set njord.enabled = true"
    echo "  Then run NJORD manually or add to systemd."
    echo ""
    echo "See docs/lite_mode.md for the full guide."

elif [[ "$MODE" == "full" ]]; then
    echo ""
    echo "Full mode: checking upstream push access for strategy_publisher..."

    if git push --dry-run origin master &>/dev/null 2>&1; then
        if [[ $NO_CRON -eq 0 ]]; then
            PUB_CRON="0 */4 * * * python3 ${WORKSPACE}/strategy_publisher.py >> ${WORKSPACE}/competition/strategy_publisher.log 2>&1"
            if crontab -l 2>/dev/null | grep -qF "strategy_publisher.py"; then
                echo "  strategy_publisher cron already installed."
            else
                (crontab -l 2>/dev/null; echo "# Hub-and-spoke: publish champion strategies to upstream every 4h"; echo "$PUB_CRON") | crontab -
                echo "  Installed strategy_publisher cron: $PUB_CRON"
            fi
        else
            echo "  --no-cron: skipping strategy_publisher cron installation."
        fi
    else
        echo "  WARN: push access to origin not confirmed."
        echo "  strategy_publisher cron NOT installed. Check repo permissions, then run:"
        echo "    crontab -e"
        echo "    Add: 0 */4 * * * python3 ${WORKSPACE}/strategy_publisher.py >> ${WORKSPACE}/competition/strategy_publisher.log 2>&1"
    fi
fi

echo ""
echo "Next step: ./scripts/sanity_check.sh"
