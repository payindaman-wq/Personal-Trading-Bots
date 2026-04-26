# Architecture Overview

## Officer Pattern

The framework delegates each major concern to a dedicated AI agent called an **officer**. Officers are Python processes with a defined model tier, firing cadence, and communication contract. They do not call each other directly -- they read from and write to structured files (inboxes, queues, state JSON) so failures in one officer do not cascade.

| Officer | Role | Trigger |
|---------|------|--------|
| Strategy | Evolves trading strategies via LLM-guided mutation and backtesting | Continuous loop |
| Analysis | Deep review of strategy cohort at generation milestones | Every N generations + breakthrough |
| Strategic Arbitration | Resolves implementation conflicts, handles escalations, deep-dive audits | On reverts, oscillation, or manual trigger |
| Implementation | Applies safe changes autonomously without human approval | Every 15 minutes |
| Risk | Macro regime detection, position-size multiplier | Every 30 minutes |
| Market Intelligence | Trending tokens and hot sectors | Every 30 minutes |
| Operations | Composite health monitor -- aggregates all subsystem health, sole Telegram path | Every 30 minutes |
| Capital Allocation | Allocates capital across leagues based on performance (pending live rollout) | On live trading activation |

All inter-officer communication routes through a central inbox file (`syn_inbox.jsonl`). The Operations officer is the only process permitted to send Telegram alerts -- every other module writes findings to the inbox, and Operations decides what requires human attention.

## Executor Pattern and Tier Model

Auto-execute logic sits below the officer layer. Executors run on cron and consume from the same inbox. They are the mechanism by which the system heals itself before a human ever sees an alert.

**Tier 1 -- Immediate auto-fix**: Well-understood, low-risk failures. Applied within seconds of detection. Examples: stale tick restart, dead service restart, simple config drift correction.

**Tier 2 -- Structured fix with review window**: Changes that are safe but warrant a 24-hour observation window. Applied automatically; flagged in a pending-review store. A human can inspect or revert within the window; after 24 hours with no reversion the change is considered accepted.

**Tier 3 -- Cascading / complex failure**: Multiple simultaneous anomalies, cross-component drift, or resource exhaustion. The executor applies what it safely can and escalates the remainder to the Operations officer for human attention.

## Configuration Schema

All configuration lives in `config.yaml` at the repo root. The file is gitignored and must never be committed. A versioned schema reference is in `config.example.yaml`.

The `config_version` key at the top of `config.yaml` is used by migration scripts to detect schema differences after pulling a Major version bump. When `CHANGELOG.md` lists a breaking change, run `scripts/migrate_config.sh` before restarting services.

`config_loader.py` at the repo root is the single point of entry for reading config. All Python scripts import from it rather than parsing YAML directly, so schema changes require updates in one place.

## Leagues

Bots compete in paper-trading leagues. Each league has an independent sprint cadence, bot fleet, and research cohort.

| League | Sprint | Tick | Assets |
|--------|--------|------|-------|
| Day | 24 hours | 5 min | Spot crypto |
| Swing | 7 days | 30 min | Spot crypto |
| Futures Day | 24 hours | 5 min | BTC/ETH/SOL perpetuals |
| Futures Swing | 7 days | 30 min | BTC/ETH/SOL perpetuals |
| Prediction Markets | 7 days | 15 min | Binary outcome markets |

Bots are defined entirely by `strategy.yaml` files under `fleet/`. No code changes are required to tune strategy parameters.

## Kill Switch

A drawdown-based kill switch halts all activity when cumulative loss from peak exceeds the configured threshold (default 15%). The switch is checked by the Operations officer and can be tripped automatically or manually.
