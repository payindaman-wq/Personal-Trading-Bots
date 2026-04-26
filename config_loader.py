#!/usr/bin/env python3
"""
config_loader.py — Central configuration loader for crypto-trading-toolkit.

Usage:
    from config_loader import config
    token = config.telegram.bot_token
    chat  = config.telegram.chat_id

Config file: config.yaml in the workspace root directory.
Copy config.example.yaml to config.yaml and fill in your values.
"""
import os
import sys
import yaml
from types import SimpleNamespace

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
CONFIG_PATH = os.environ.get("CONFIG_PATH", os.path.join(WORKSPACE, "config.yaml"))
SUPPORTED_VERSION = 1


def _to_namespace(obj):
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: _to_namespace(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_to_namespace(i) for i in obj]
    return obj


def _load_config():
    if not os.path.exists(CONFIG_PATH):
        print(
            f"ERROR: config.yaml not found at {CONFIG_PATH}\n"
            f"  → Copy config.example.yaml to {os.path.dirname(CONFIG_PATH)}/config.yaml and fill in your values.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        print("ERROR: config.yaml is empty or not a valid YAML mapping.", file=sys.stderr)
        sys.exit(1)

    version = raw.get("config_version")
    if version is None:
        print(
            "ERROR: config.yaml is missing required key 'config_version'.\n"
            "  → The first key in config.yaml must be: config_version: 1",
            file=sys.stderr,
        )
        sys.exit(1)

    if not isinstance(version, int) or version < 1:
        print(f"ERROR: config_version must be a positive integer, got: {version!r}", file=sys.stderr)
        sys.exit(1)

    if version > SUPPORTED_VERSION:
        print(
            f"ERROR: config.yaml version {version} is newer than this loader (supports v{SUPPORTED_VERSION}).\n"
            f"  → Update config_loader.py or downgrade your config.yaml.",
            file=sys.stderr,
        )
        sys.exit(1)

    if version < SUPPORTED_VERSION:
        print(
            f"ERROR: config.yaml version {version} is outdated.\n"
            f"  → Run scripts/migrate_config.sh to upgrade from v{version} to v{SUPPORTED_VERSION}.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Environment variable overrides (useful for CI / testing without a config file)
    tg = raw.setdefault("telegram", {})
    if os.environ.get("TELEGRAM_BOT_TOKEN"):
        tg["bot_token"] = os.environ["TELEGRAM_BOT_TOKEN"]
    if os.environ.get("TELEGRAM_CHAT_ID"):
        tg["chat_id"] = os.environ["TELEGRAM_CHAT_ID"]

    ant = raw.setdefault("anthropic", {})
    if os.environ.get("ANTHROPIC_API_KEY"):
        ant["api_key"] = os.environ["ANTHROPIC_API_KEY"]

    gem = raw.setdefault("gemini", {})
    if os.environ.get("GEMINI_API_KEY"):
        gem["api_key"] = os.environ["GEMINI_API_KEY"]

    kr = raw.setdefault("kraken", {})
    if os.environ.get("KRAKEN_API_KEY"):
        kr["api_key"] = os.environ["KRAKEN_API_KEY"]
    if os.environ.get("KRAKEN_API_SECRET"):
        kr["api_secret"] = os.environ["KRAKEN_API_SECRET"]


    up = raw.setdefault("upstream", {})
    up.setdefault("repo", "https://github.com/coldstoneadmin/crypto-trading-toolkit")
    up.setdefault("branch", "master")
    up.setdefault("pat", "")
    if os.environ.get("UPSTREAM_PAT"):
        up["pat"] = os.environ["UPSTREAM_PAT"]

    return _to_namespace(raw)


config = _load_config()
