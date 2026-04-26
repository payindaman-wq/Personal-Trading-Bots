# Staying in Sync with Upstream

If you forked `coldstoneadmin/crypto-trading-toolkit`, use this guide to pull improvements while keeping your local customizations intact.

## Add Upstream as a Remote

Do this once after forking:

```bash
git remote add upstream https://github.com/coldstoneadmin/crypto-trading-toolkit
git fetch upstream
```

## Check What Has Changed

```bash
git fetch upstream
git log HEAD..upstream/main --oneline
```

Read the new entries in `CHANGELOG.md` before pulling. If any entry is tagged **Major**, a migration step is required (see below).

## Pull Upstream Changes

```bash
git pull upstream main
```

If there are conflicts:

- `config.yaml` is gitignored and will never conflict.
- `config.example.yaml` may have new keys -- merge it manually and add the new keys to your `config.yaml`.
- Custom strategy files under `fleet/` may conflict if upstream changed the same bot. Resolve manually; your tuned values take precedence.
- Everything else (officer scripts, executors, tick loops) should merge cleanly unless you made local edits to framework code.

## When to Run `scripts/migrate_config.sh`

Run this script after pulling a **Major** version bump listed in `CHANGELOG.md`. It reads your existing `config.yaml`, applies schema changes, and writes the updated file. It is idempotent -- safe to run more than once.

```bash
scripts/migrate_config.sh
```

The script checks `config_version` in your `config.yaml` and applies only the migrations needed to bring it to the current version. After migration, restart your services.

## Keeping a Private Fork Clean

If you have personal customizations (custom strategy names, private branding, private exchange credentials), keep them in files that are already gitignored (`config.yaml`, files under `tax/`, agent memory files). Avoid editing framework files directly -- patch the behavior via config or subclass the relevant officer -- so upstream pulls remain conflict-free.
