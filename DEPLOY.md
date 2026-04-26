# Deployment Guide

This framework is designed to be cloned and deployed independently by any
operator. Each deployment is fully isolated — your API keys, wallet, and
personal config never touch this repository.

## Overview

```
This repo (framework)           Your private repo (your deployment)
crypto-trading-toolkit    →     your-username/my-trading-fleet
- Strategies                    - .env (your real keys)
- Competition engine            - Custom bot roster (optional)
- Accounting bot                - Your competition results
- Skills                        - Your tax records
No personal data                Everything personal stays here
```

## Prerequisites

- Linux VPS (Ubuntu 22.04+ recommended, 2GB+ RAM)
- Python 3.10+
- Node.js 18+ (for OpenClaw)
- Git
- A Telegram bot token (from @BotFather)
- A Kraken account (for live trading — not needed for paper trading)

## Step 1: Create Your Private Deployment Repo

Create a new **private** repository on GitHub. This is where your live
deployment config and personal data will live. Do not use this repo for that.

```bash
# On your VPS
git clone https://github.com/YOUR_USERNAME/my-trading-fleet /root/workspace
cd /root/workspace
```

Or copy the framework into your private repo:

```bash
git clone https://github.com/YOUR_USERNAME/crypto-trading-toolkit /tmp/framework
cp -r /tmp/framework/* /root/workspace/
cd /root/workspace
git init && git remote add origin https://github.com/YOUR_USERNAME/my-trading-fleet
```

## Step 2: Configure Environment

```bash
cp .env.example .env
nano .env   # fill in your real values
```

Required for paper trading:
- `WORKSPACE` — path to your deployed workspace directory
- `SKILLS_DIR` — path to your skills directory
- `TELEGRAM_BOT_TOKEN` — your bot token
- `TELEGRAM_CHAT_ID` — your personal chat ID

Required for live trading (add when ready):
- `KRAKEN_API_KEY`
- `KRAKEN_API_SECRET`

Load the env vars (add to your shell profile or systemd service):

```bash
source .env
# or add to /etc/environment for system-wide availability
```

## Step 3: Install OpenClaw

```bash
npm install -g openclaw
openclaw init
```

Configure OpenClaw to use your Telegram bot and set `WORKSPACE` in its config.

## Step 4: Deploy Skills

Copy skills from the framework into your OpenClaw skills directory:

```bash
cp -r skills/* $SKILLS_DIR/
```

Or symlink them from your workspace:

```bash
ln -s $WORKSPACE/skills/accounting $SKILLS_DIR/accounting
ln -s $WORKSPACE/skills/competition-start $SKILLS_DIR/competition-start
# etc.
```

## Step 5: Initialize Accounting

```bash
python3 $SKILLS_DIR/accounting/scripts/accounting.py init
```

## Step 6: Set Up Cron Jobs

Paper trading competition ticks (every 5 min for day league):

```bash
crontab -e
```

Add:
```
# Day trading tick (every 5 min)
*/5 * * * * WORKSPACE=/root/.openclaw/workspace python3 /root/.openclaw/skills/competition-tick/scripts/competition_tick.py >> /root/.openclaw/workspace/competition/cron.log 2>&1

# Swing tick (every 30 min)
*/30 * * * * WORKSPACE=/root/.openclaw/workspace python3 /root/.openclaw/workspace/swing_competition_tick.py >> /root/.openclaw/workspace/competition/cron.log 2>&1

# Swing price store (every hour)
0 * * * * WORKSPACE=/root/.openclaw/workspace python3 /root/.openclaw/workspace/swing_price_store.py >> /root/.openclaw/workspace/competition/cron.log 2>&1
```

## Step 7: Start a Competition

Via Telegram (ask SYN):
```
start a 4 hour competition
```

Or directly:
```bash
python3 $SKILLS_DIR/competition-start/scripts/competition_start.py 4
```

## Step 8: Go Live (When Ready)

Before going live with real capital:

1. [ ] LLC formed and EIN obtained
2. [ ] Kraken business account opened under LLC
3. [ ] `KRAKEN_API_KEY` and `KRAKEN_API_SECRET` set in `.env`
4. [ ] Accounting bot initialized and tested
5. [ ] At least one bot with 10+ sprint history and consistent profitability
6. [ ] Operator (you) has reviewed competition results and approved funding
7. [ ] `trade-execute` skill installed and tested in dry-run mode
8. [ ] Kill switch endpoint bookmarked

**Do not skip these steps. Real money is involved.**

## Customizing Your Fleet

Edit bot strategy files in `fleet/` to adjust entry/exit logic, pairs,
position sizing, and risk parameters. Each bot's behavior is fully defined
by its `strategy.yaml` — no code changes needed for strategy tuning.

See `fleet/floki/strategy.yaml` for a documented example.

## Keeping Up With Framework Updates

When the framework repo gets updates:

```bash
# In your private repo
git remote add framework https://github.com/YOUR_USERNAME/crypto-trading-toolkit
git fetch framework
git merge framework/master --allow-unrelated-histories
# Resolve any conflicts, keeping your .env and personal config
```

## Directory Structure

```
workspace/
├── fleet/                  # Bot strategy YAML files
│   ├── floki/strategy.yaml
│   ├── swing/egil/strategy.yaml
│   └── ...
├── competition/
│   ├── active/             # Live sprint state
│   ├── results/            # Archived sprint results
│   ├── swing/              # Swing league data
│   └── accounting/         # Trade ledger and reserves
├── tax/                    # IRS 8949 exports (year-end)
├── skills/                 # OpenClaw skill definitions
├── roles/                  # Job descriptions for each bot role
└── .env                    # YOUR secrets (never committed)
```
