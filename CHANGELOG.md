# Changelog

All notable changes documented here. Semver-style versioning:

- **Major** (breaking config schema, removed officers, restructured directories) -- requires running `scripts/migrate_config.sh` after pull.
- **Minor** (new features, new optional config keys) -- safe to pull, no migration needed.
- **Patch** (bug fixes, performance, internal refactors) -- safe to pull.

## [Unreleased]

- (add entries here as commits land)

## [0.1.0] -- 2026-04-25

- Initial public template release.
- Officer layer: Strategy, Analysis, Strategic Arbitration, Implementation, Risk, Market Intelligence, Operations, Capital Allocation (pending).
- Wave 1 auto-execute executors: watchdog executor, sprint integrity executor.
- Tier 3 self-heal: cascading-failure and resource-exhaustion recovery.
- Meta-audit cron: weekly strategic review with auto-execute action queueing.
- `config_version: 1` -- initial schema (see `config.example.yaml`).
# migrated 2026-04-26
