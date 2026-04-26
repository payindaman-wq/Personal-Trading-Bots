# crypto-trading-toolkit

An autonomous crypto and prediction-markets trading framework built for systematic strategy research, self-healing operations, and hands-off execution. Bots compete in paper-trading leagues; winners graduate to live funding on supported exchanges. The system runs 24/7 on a Linux VPS with no manual intervention required under normal conditions.

## What this is

A production-grade framework that runs a fleet of rule-based trading bots across multiple leagues (day, swing, prediction markets). A multi-tier AI officer layer handles strategy research, analysis, autonomous implementation of safe changes, risk management, market intelligence, and operations monitoring. Three tiers of auto-execute logic detect and resolve common failure modes without human involvement.

## What this is NOT

- Investment advice of any kind
- A guarantee of profit or performance
- Supported software with an SLA -- use at your own risk, read the license

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/crypto-trading-toolkit
cd crypto-trading-toolkit
./scripts/setup.sh        # interactive -- prompts for API keys, writes config.yaml
./scripts/sanity_check.sh # validates config and tests external reachability
```

## What You Will Need

- **Anthropic API key** -- powers the analysis and implementation officers
- **Gemini API key** -- powers the strategy research officers (significantly cheaper at scale)
- **Kraken trading account** -- optional; required only for live trading (Kraken Derivatives US for futures)
- **Telegram bot + chat ID** -- optional; used for operational alerts requiring human attention
- **Linux VPS** -- Ubuntu 22.04+ recommended, 2 vCPU / 4 GB RAM minimum

## Architecture

The framework is organized around an **officer pattern**: each major operational concern is handled by a dedicated AI agent with a defined scope, model, and firing cadence. Officers do not act on each other directly -- they communicate through structured inboxes and queues so failures stay isolated.

Current officers: Strategy (crypto research), Analysis (milestone review), Strategic Arbitration (conflict resolution and deep-dive), Implementation (autonomous safe changes), Risk (macro regime + position sizing), Market Intelligence (trending assets), Operations (composite health monitor), and Capital Allocation (pending live rollout). Each officer is a Python process managed by cron or systemd.

Auto-execute logic is layered into three tiers. **Tier 1** resolves well-known, low-risk failures immediately (stale ticks, dead services, simple config drift). **Tier 2** applies structured fixes with a 24-hour review window before they are treated as permanent. **Tier 3** handles cascading failures, cross-component drift, and resource exhaustion -- it escalates to human attention only when no safe automated fix exists. Together these tiers eliminate the majority of operational Telegram noise.

See [docs/architecture.md](docs/architecture.md) for a full breakdown.

## Repository Layout

```
scripts/             setup and sanity-check utilities
docs/                architecture overview and operator guides
fleet/               per-bot strategy YAML files
research/            officer scripts and research output
competition/         runtime league state (gitignored on your deployment)
config.yaml          your local config (gitignored -- never committed)
config.example.yaml  schema reference and defaults
```

## Staying in Sync with Upstream

If you forked this repo, see [docs/syncing.md](docs/syncing.md) for how to pull upstream improvements, detect breaking changes, and run migration scripts when required.

## Disclaimer

This software is provided for educational and research purposes only. Nothing in this repository constitutes financial or investment advice. Crypto trading carries substantial risk of loss. The authors and contributors are not responsible for any losses incurred through use of this software. **USE AT YOUR OWN RISK.**

## License

MIT -- see [LICENSE](LICENSE).
