# crypto-trading-toolkit

An autonomous crypto and prediction-markets trading framework built for systematic strategy research, self-healing operations, and hands-off execution. Bots compete in paper-trading leagues; winners graduate to live funding on supported exchanges. The system runs 24/7 on a Linux VPS with no manual intervention required under normal conditions.

---

**First time here? Start with [docs/getting_started.md](docs/getting_started.md).**  
It walks you from zero to a running paper-trading bot in 60-90 minutes, no prior experience required.

---

## Two ways to run

```
LITE MODE (recommended for most people)
----------------------------------------
Cost:         ~$5/month (VPS only — no AI fees)
What you run: execution layer + capital allocation (NJORD)
Strategy:     pulled automatically from Mother every 4 hours
AI required:  no

FULL MODE (for advanced users who want independent research)
------------------------------------------------------------
Cost:         ~$10-20/month (VPS + Anthropic + Gemini API fees)
What you run: everything in lite mode PLUS the full officer stack
Strategy:     your own evolutionary research (ODIN, MIMIR, VIDAR)
AI required:  yes (Anthropic + Gemini API keys)
```

**If you don't know which to pick, choose lite mode.** You can switch to full mode later if you decide you want it.

See [docs/lite_mode.md](docs/lite_mode.md) for a full breakdown of what runs in each mode.

---

## What this is

A production-grade framework that runs a fleet of rule-based trading bots across multiple leagues (day, swing, prediction markets). A multi-tier AI officer layer handles strategy research, analysis, autonomous implementation of safe changes, risk management, market intelligence, and operations monitoring. Three tiers of auto-execute logic detect and resolve common failure modes without human involvement.

## What this is NOT

- Investment advice of any kind
- A guarantee of profit or performance
- Supported software with an SLA -- use at your own risk, read the license

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/crypto-trading-toolkit
cd crypto-trading-toolkit
./scripts/setup.sh --mode lite   # or --mode full if you want independent AI research
./scripts/sanity_check.sh        # validates config and tests external reachability
```

For a guided walkthrough see [docs/getting_started.md](docs/getting_started.md).

## What You Will Need

**Lite mode (most people):**
- A Kraken trading account (for live trading; not needed for paper trading)
- A Telegram bot + chat ID (for operational alerts)
- A Linux VPS ($5/month, Ubuntu 24.04)

**Full mode (adds):**
- Anthropic API key -- powers the analysis and implementation officers
- Gemini API key -- powers the strategy research officers (significantly cheaper at scale)

---

## Architecture

The framework is organized around an **officer pattern**: each major operational concern is handled by a dedicated AI agent with a defined scope, model, and firing cadence. Officers do not act on each other directly -- they communicate through structured inboxes and queues so failures stay isolated.

Current officers: Strategy (crypto research), Analysis (milestone review), Strategic Arbitration (conflict resolution and deep-dive), Implementation (autonomous safe changes), Risk (macro regime + position sizing), Market Intelligence (trending assets), Operations (composite health monitor), and Capital Allocation (NJORD). Each officer is a Python process managed by cron or systemd.

Auto-execute logic is layered into three tiers. **Tier 1** resolves well-known, low-risk failures immediately (stale ticks, dead services, simple config drift). **Tier 2** applies structured fixes with a 24-hour review window before they are treated as permanent. **Tier 3** handles cascading failures, cross-component drift, and resource exhaustion -- it escalates to human attention only when no safe automated fix exists. Together these tiers eliminate the majority of operational Telegram noise.

See [docs/architecture.md](docs/architecture.md) for a full breakdown.

## Repository Layout

```
scripts/             setup and sanity-check utilities
docs/                architecture overview and operator guides
fleet/               per-bot strategy YAML files
research/            officer scripts and research output
  <league>/
    seed_strategy.yaml   stable seed shipped with the repo (fork-safe)
    best_strategy.yaml   live runtime state materialized from seed at setup (gitignored)
competition/         runtime league state (gitignored on your deployment)
published/           champion strategies published by Mother (lite mode source)
config.yaml          your local config (gitignored -- never committed)
config.example.yaml  schema reference and defaults
```

`best_strategy.yaml` is never committed — it is runtime state materialized from `seed_strategy.yaml` when you run `scripts/setup.sh`. Pulling upstream updates does not overwrite your live strategy files.

## Staying in Sync with Upstream

If you forked this repo, see [docs/syncing.md](docs/syncing.md) for how to pull upstream improvements, detect breaking changes, and run migration scripts when required.

## Disclaimer

This software is provided for educational and research purposes only. Nothing in this repository constitutes financial or investment advice. Crypto trading carries substantial risk of loss. The authors and contributors are not responsible for any losses incurred through use of this software. **USE AT YOUR OWN RISK.**

## License

MIT -- see [LICENSE](LICENSE).
