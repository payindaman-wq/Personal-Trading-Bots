#!/usr/bin/env bash
set -euo pipefail

CONFIG="config.yaml"

prompt_value() {
    local label="$1" var="$2" default="${3:-}" secret="${4:-no}"
    if [[ "$secret" == "yes" ]]; then
        read -rsp "  $label${default:+ [$default]}: " val
        echo
    else
        read -rp  "  $label${default:+ [$default]}: " val
    fi
    if [[ -z "$val" && -n "$default" ]]; then val="$default"; fi
    printf -v "$var" '%s' "$val"
}

echo ""
echo "crypto-trading-toolkit setup"
echo "----------------------------"
echo "This script writes config.yaml (gitignored). Re-running overwrites after confirmation."
echo ""

if [[ -f "$CONFIG" ]]; then
    read -rp "config.yaml already exists. Overwrite? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
fi

echo ""
echo "Required keys:"
prompt_value "Anthropic API key" ANTHROPIC_KEY "" yes
prompt_value "Gemini API key" GEMINI_KEY "" yes

echo ""
echo "Optional -- Kraken live trading (leave blank to skip):"
prompt_value "Kraken API key" KRAKEN_KEY "" yes
prompt_value "Kraken API secret" KRAKEN_SECRET "" yes

echo ""
echo "Optional -- Telegram alerts (leave blank to skip):"
prompt_value "Telegram bot token" TG_TOKEN "" yes
prompt_value "Telegram chat ID" TG_CHAT ""

echo ""
echo "Infrastructure:"
prompt_value "VPS host (user@host or host)" VPS_HOST ""
prompt_value "Dashboard domain (optional)" DASHBOARD_DOMAIN ""
prompt_value "Anthropic daily budget USD" ANTHROPIC_BUDGET "10"

errors=0
if [[ -z "$ANTHROPIC_KEY" ]]; then echo "ERROR: Anthropic API key is required."; errors=1; fi
if [[ -z "$GEMINI_KEY" ]];    then echo "ERROR: Gemini API key is required."; errors=1; fi
if [[ -z "$VPS_HOST" ]];      then echo "ERROR: VPS host is required."; errors=1; fi
if [[ $errors -ne 0 ]]; then exit 1; fi

cat > "$CONFIG" <<'CONFIGEOF'
config_version: 1

anthropic_api_key: "ANTHROPIC_KEY_PLACEHOLDER"
gemini_api_key: "GEMINI_KEY_PLACEHOLDER"

kraken_api_key: "KRAKEN_KEY_PLACEHOLDER"
kraken_api_secret: "KRAKEN_SECRET_PLACEHOLDER"

telegram_bot_token: "TG_TOKEN_PLACEHOLDER"
telegram_chat_id: "TG_CHAT_PLACEHOLDER"

vps_host: "VPS_HOST_PLACEHOLDER"
dashboard_domain: "DASHBOARD_DOMAIN_PLACEHOLDER"

anthropic_daily_budget: ANTHROPIC_BUDGET_PLACEHOLDER
CONFIGEOF

# Substitute placeholders with actual values
sed -i \
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
echo "Next step: ./scripts/sanity_check.sh"
