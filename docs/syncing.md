# Staying in Sync with Upstream

If you forked `YOUR_USERNAME/crypto-trading-toolkit`, use this guide to pull improvements while keeping your local customizations intact.

## Add Upstream as a Remote

Do this once after forking:

```bash
git remote add upstream https://github.com/YOUR_USERNAME/crypto-trading-toolkit
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


## Upstream Config Keys

`strategy_publisher.py` (Mother) and `strategy_sync.py` (friend VPS) both read three
keys from `config.yaml`:

```yaml
upstream:
  repo: "https://github.com/MOTHER_USERNAME/crypto-trading-toolkit"  # public template
  branch: "master"
  pat: ""  # GitHub PAT with public_repo scope (or set UPSTREAM_PAT env var)
```

**Mother** (`mode: full`): set `upstream.repo` to the public template you forked from.
The publisher creates a transient `upstream_pub` remote using this URL + PAT and pushes
`published/<league>/champion.yaml` there every 4 hours.

**Friend VPS** (`mode: lite`): set `upstream.repo` to the same public template. Add the
remote once after cloning:

```bash
git remote add upstream https://github.com/MOTHER_USERNAME/crypto-trading-toolkit
```

**PAT storage:** `config.yaml` is gitignored -- the PAT is never committed. Alternatively
export `UPSTREAM_PAT` in your VPS environment. The publisher falls back to extracting
the token from origin's URL if neither is set.


## Personal Data Hygiene

This repo includes a CI check (`scripts/scrub_check.sh`) that scans tracked files for strings
that must not appear in a public template: VPS IPs, GitHub PATs, Telegram bot tokens, and
personal account handles. It runs automatically on every push and pull request to master.

Run it locally at any time:

```bash
bash scripts/scrub_check.sh
```

Exit 0 means clean. Exit 1 prints `FAIL [LABEL]: file:line:content` for each violation.

### Adding an allowlist entry

If a match is legitimate (for example, a doc that explains what a Telegram bot token looks
like, or a migration runbook that intentionally references your VPS IP), add a regex to
`.scrub_allowlist` at the repo root:

```
# Brief explanation of why this match is safe
path/to/file\.md:.*your_pattern_here
```

Each line is matched against the full `file:line:content` string. Lines starting with `#`
are comments.

### Running your own fork

When you fork this repo, extend the forbidden list with your own identifiers so accidental
commits do not leak your infrastructure details:

1. Open `scripts/scrub_check.sh` and add your VPS IP, personal GitHub handle, etc. to the
   `check_pattern` calls in the **Global patterns** section.
2. If you rename the upstream (for example, to your own GitHub username), add
   `check_pattern "HANDLE" 'yourusername'` and add any legitimate existing uses to
   `.scrub_allowlist`.
3. The CI workflow (`.github/workflows/scrub-check.yml`) enforces these checks on every
   push and pull request automatically.
