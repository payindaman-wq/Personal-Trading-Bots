# Migration Runbook: coldstoneadmin → payindaman-wq

**Estimated time:** 30-45 minutes
**What this does:** Migrates the active repo from `coldstoneadmin/crypto-trading-toolkit`
to two new repos under your `payindaman-wq` GitHub account — a public template friends
fork, and a private personal repo the VPS deploys from.
**Prerequisites:**
- Logged into github.com as `payindaman-wq`
- SSH access to `YOUR_VPS_IP` working from your laptop
- Approximately 30-45 minutes of uninterrupted focus
- A new GitHub Personal Access Token (PAT) from your `payindaman-wq` account with `repo`
  scope — create one at https://github.com/settings/tokens before you start

**Placeholder:** Every command that contains `<NEW_PAT>` requires you to substitute your
real token. Never commit the token into any file. Keep it in a password manager or a
temporary scratch document on your local machine only.

---

## Pre-flight checks

Run these before touching anything. They confirm the source repo is clean and matches
what this runbook expects.

**Check working tree and recent commits:**

```bash
ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && git status && echo '---' && git log --oneline -5"
```

Expected: `Your branch is up to date with 'origin/master'.` and `nothing to commit`
(untracked runtime files are fine — they are gitignored). The top commit should be
`0325adb docs: add complete beginner onboarding suite (Session S)` or a later commit.

**Confirm config.yaml is gitignored:**

```bash
ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && git check-ignore config.yaml && echo 'OK: config.yaml is ignored'"
```

Expected output: `config.yaml` followed by `OK: config.yaml is ignored`. If this
command produces no output, stop — config.yaml is NOT ignored and you risk pushing
secrets to a public repo.

**Confirm config.yaml is not tracked in the source repo:**

```bash
ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && git ls-files | grep config.yaml"
```

Expected: no output. If `config.yaml` appears in the output, stop — it has been
accidentally committed and will push to the public template in Step 2.

**Confirm current origin:**

```bash
ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && git remote -v"
```

Expected: `origin https://ghp_...@github.com/coldstoneadmin/crypto-trading-toolkit.git`

**Save the old PAT for rollback.** Copy the full URL from the command above and keep
it in a safe place before proceeding.

**Wave 1 verifier timing note:** The automated Wave 1 verifier is scheduled to run
Monday 2026-04-27 at 23:00 UTC. If you are running this runbook before that report
comes back green, you are accepting extra risk. The system is functional, but the
verifier confirms all Wave 1 executors are wired correctly. Waiting until Tuesday
2026-04-28 after checking the report is the lower-risk option.

---

## Step 1 — Create the two new GitHub repos (browser, ~5 min)

Log into github.com as `payindaman-wq`.

**Create the public template repo:**

1. Go to https://github.com/new
2. Repository name: `crypto-trading-toolkit`
3. Visibility: **Public**
4. Leave "Add a README file", "Add .gitignore", and "Choose a license" all **unchecked**
   — the repo must be empty so the push in Step 2 does not conflict
5. Click **Create repository**

**Create the private personal repo:**

1. Go to https://github.com/new
2. Repository name: `Herbal-Nectars-Trading`
3. Visibility: **Private**
4. Leave all "Initialize this repository" options **unchecked**
5. Click **Create repository**

**Verify both exist:**

- https://github.com/payindaman-wq/Personal-Trading-Bots — should show "Quick setup"
  (empty repo)
- https://github.com/payindaman-wq/Herbal-Nectars-Trading — same

---

## Step 2 — Push the public template to payindaman-wq/Personal-Trading-Bots (~5 min)

This pushes the current master branch from the VPS to the new public repo. Origin is
not changed here — you are adding a temporary remote for the one-shot push only.

```bash
ssh root@YOUR_VPS_IP
```

Once connected:

```bash
cd /root/.openclaw/workspace

git remote add public https://<NEW_PAT>@github.com/payindaman-wq/Personal-Trading-Bots.git
git push public master
git remote remove public
```

The push may take 15-30 seconds. When it completes, visit
https://github.com/payindaman-wq/Personal-Trading-Bots — you should see the full
codebase with README, LICENSE, and docs/.

**Verify config.yaml is absent from the public repo:**

Browse to https://github.com/payindaman-wq/Personal-Trading-Bots/blob/master/config.yaml

GitHub should return a 404 or "File not found". If it is present, stop — do not
proceed until you understand why. (This would mean config.yaml was accidentally
committed at some point in the source repo's history.)

---

## Step 3 — Set up the private personal Mother repo (~10 min)

The personal repo is what the VPS deploys from. It holds the same code as the public
template. `config.yaml` stays gitignored and lives only on the VPS filesystem — it is
never committed to either repo.

### 3.1 — Re-point origin to the personal repo

```bash
# Still on the VPS, still in /root/.openclaw/workspace
git remote set-url origin https://<NEW_PAT>@github.com/payindaman-wq/Herbal-Nectars-Trading.git
git push -u origin master
```

Wait for the push to complete. The personal repo now has the full codebase.

### 3.2 — Back up config.yaml outside git

`config.yaml` is gitignored in both repos and must stay that way. It lives only on
the VPS filesystem at `/root/.openclaw/workspace/config.yaml`. To protect against
accidental loss (disk failure, re-clone, misconfiguration), encrypt and save a copy
outside git using the provided backup script:

```bash
bash /root/.openclaw/workspace/scripts/backup_secrets.sh
```

The script prompts for a passphrase, encrypts `config.yaml` with AES-256 GPG, and
saves the result to `/root/.config-backup/`. It keeps the last 7 daily backups and
deletes older ones automatically. Store the passphrase in a password manager — it is
not saved anywhere on the VPS.

**Confirm config.yaml is NOT tracked after re-pointing origin:**

```bash
git ls-files config.yaml | wc -l
```

Expected output: `0`. If it returns `1`, config.yaml was accidentally committed at
some point in the repo history — stop and investigate before pushing to the public
template.

---

## Step 4 — Update GitHub Actions secrets in the personal repo (~5 min)

The deploy workflow (`.github/workflows/deploy.yml`) triggers on every push to master
and SSH's into the VPS to run `git reset --hard origin/master`. The workflow was
copied into the personal repo in Step 3. It needs two GitHub secrets to authenticate.

**Navigate to the secrets page:**

https://github.com/payindaman-wq/Herbal-Nectars-Trading/settings/secrets/actions

Add the following two secrets (click "New repository secret" for each):

| Secret name | Value |
|---|---|
| `VPS_HOST` | `YOUR_VPS_IP` |
| `VPS_SSH_KEY` | Contents of the deploy private key on the VPS (see below) |

**To find the deploy SSH key:**

```bash
ssh root@YOUR_VPS_IP "ls ~/.ssh/"
```

Look for a key whose public half is in `~/.ssh/authorized_keys`. To print the private
key contents for pasting:

```bash
ssh root@YOUR_VPS_IP "cat ~/.ssh/id_ed25519"
```

Copy the entire output including the `-----BEGIN OPENSSH PRIVATE KEY-----` and
`-----END OPENSSH PRIVATE KEY-----` lines. Paste it as the value for `VPS_SSH_KEY`.

---

## Step 5 — Update upstream config for strategy publishing (~2 min)

Open  on the VPS (or via your laptop SSH session) and add the 
block with the public template URL and your new PAT:



 reads these values and pushes champion strategies to the public
template repo regardless of where  points. No crontab changes are needed.

## Step 6 — First end-to-end deploy test (~5 min)

Verify the new deploy chain works. Make a trivial commit and push, then watch the
Actions tab.

```bash
ssh root@YOUR_VPS_IP
cd /root/.openclaw/workspace

echo "# migrated $(date -u +%Y-%m-%d)" >> CHANGELOG.md
git add CHANGELOG.md
git commit -m "test: verify deploy chain after migration to payindaman-wq"
git push origin master
```

Open the Actions tab:

https://github.com/payindaman-wq/Herbal-Nectars-Trading/actions

You should see a workflow run start within a few seconds. It should complete green
within 60-90 seconds. Click into the run and expand "Deploy to VPS" — you should see
`Deploy complete` at the end of the log.

If the workflow fails with an SSH authentication error, the `VPS_SSH_KEY` secret may
have copy-paste whitespace issues. Re-paste the key in the secrets page, making sure
the full key including all newlines was captured (the header and footer lines must be
present and unmodified).

---

## Step 7 — Archive the old coldstoneadmin repo (~2 min)

Do this only after the deploy test in Step 6 passes green and you have checked every
item in the verification checklist below.

1. Browse to https://github.com/coldstoneadmin/crypto-trading-toolkit/settings
2. Scroll to the **Danger Zone** section at the bottom
3. Click **Archive this repository**
4. Type the repo name to confirm, then click **I understand the consequences, archive
   this repository**

Archiving makes the repo read-only. Existing URLs continue to resolve. Any forks Bryan
or others made before archiving remain accessible in read-only mode. No data is lost.

---

## Step 8 — Branch protection on Personal-Trading-Bots (~3 min)

This step applies to the **public template** only. Branch protection prevents direct
pushes that bypass CI status checks, ensuring no scrub-check or smoke failures slip
into the public repo.

### Set the protection rule (GitHub browser UI)

1. Go to https://github.com/payindaman-wq/Personal-Trading-Bots/settings/branches
2. Click **Add branch protection rule**
3. Branch name pattern: `master`
4. Enable: **Require status checks to pass before merging**
   - In the search box, add these checks (they appear in the dropdown after the first
     push triggers each workflow):
     - `scrub-check` (from `.github/workflows/scrub-check.yml`)
     - `smoke` (from `.github/workflows/smoke.yml`)
   - Enable: **Require branches to be up to date before merging**
5. Enable: **Do not allow bypassing the above settings** (applies to admins — bypass
   via the UI when genuinely needed; this is rare)
6. Click **Save changes**

**Note:** This rule applies only to merges via pull request. The `strategy_publisher`
uses a PAT to push directly to master with admin override, which is unaffected. For
fork users pulling updates from upstream, this gate ensures incoming template changes
are scrub-clean before they land.

### Step 8.1 — Configure publisher PAT to bypass branch protection

If you want to be explicit about who can push directly:

1. On https://github.com/payindaman-wq/Personal-Trading-Bots/settings/branches,
   expand the new rule
2. Under **Restrict who can push to matching branches**, add the `payindaman-wq`
   account (or the bot account associated with the publisher PAT)
3. If `payindaman-wq` is the only pusher and you are the repo owner, the admin bypass
   already covers this — this sub-step is informational

---

## Step 9 — Cutover verification (~2 min)

Run this one-liner from any terminal with VPS SSH access to confirm you are fully cut
over to payindaman-wq:

```bash
ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && \
  echo '== origin ==' && git remote -v | grep -E 'origin' && \
  echo '== publisher upstream ==' && grep -A1 '^upstream:' config.yaml | grep 'repo:' && \
  echo '== any coldstoneadmin refs left? ==' && grep -rn 'coldstoneadmin' --include='*.py' --include='*.yaml'
--include='*.md' . 2>/dev/null | grep -v -E 'CHANGELOG|migration_runbook' || echo 'NONE (good)'"
```

You are fully on payindaman-wq when:
- origin URL contains `payindaman-wq/Herbal-Nectars-Trading`
- `repo:` line under `upstream:` contains `payindaman-wq/Personal-Trading-Bots`
- The third check prints `NONE (good)` — CHANGELOG and migration_runbook are
  exempt because they retain historical references

If any check fails, do NOT archive `coldstoneadmin/crypto-trading-toolkit` yet — fix
the pointer and re-run, otherwise you lose your rollback target.

---

## Step 10 — Bryan access cleanup (~3 min)

The old repo is now archived and Bryan retains read-only access to it automatically.
No action is needed on the old repo.

Do **not** add Bryan to either new repo. Send him the public template URL so he can
fork it like any other friend would:

```
https://github.com/payindaman-wq/Personal-Trading-Bots
```

The `docs/getting_started.md` in that repo explains the full setup flow.

---

## Step 11 — Update laptop clone (if applicable)

If you have a clone of the old repo on your Windows laptop, update it to point at the
personal repo. Open Git Bash or Windows Terminal in that directory and run:

```bash
git remote set-url origin https://github.com/payindaman-wq/Herbal-Nectars-Trading.git
git fetch origin
git pull origin master
```

Add the public remote on the laptop too if you ever push strategy fixes from there:

```bash
git remote add public https://<NEW_PAT>@github.com/payindaman-wq/Personal-Trading-Bots.git
```

---

## Verification checklist

Tick each item before calling the migration complete.

- [ ] `ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && git remote -v"` shows
  `origin` pointing at `payindaman-wq/Herbal-Nectars-Trading`
- [ ] Deploy test from Step 6 ran green in GitHub Actions
- [ ] https://github.com/coldstoneadmin/crypto-trading-toolkit shows an "Archived"
  banner at the top of the page
- [ ] https://github.com/payindaman-wq/Personal-Trading-Bots is public, shows README
  and LICENSE, and does **not** contain `config.yaml`
- [ ] config.yaml is NOT tracked in Herbal-Nectars-Trading:

  ```bash
  ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && git ls-files config.yaml | wc -l"
  ```

  Expected: `0`
- [ ] Branch protection rule active on Personal-Trading-Bots master, requiring
  scrub-check and smoke status checks
- [ ] Cutover verification one-liner from Step 9 prints all three GREEN markers
- [ ] `strategy_sync.py` no longer references `coldstoneadmin` — confirmed by:

  ```bash
  ssh root@YOUR_VPS_IP "grep coldstoneadmin /root/.openclaw/workspace/strategy_sync.py"
  ```

  Expected: no output.

- [ ] Sanity check passes:

  ```bash
  ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && bash scripts/sanity_check.sh"
  ```

---

## Rollback plan

**Before archiving the old repo (Step 7):** Re-point origin back to the original and
you are fully reverted:

```bash
ssh root@YOUR_VPS_IP "cd /root/.openclaw/workspace && git remote set-url origin https://<OLD_PAT>@github.com/coldstoneadmin/crypto-trading-toolkit.git"
```

Use the old URL you saved during the pre-flight checks.

**After archiving (Step 7):** Rollback requires un-archiving via the old repo's settings
page. The Danger Zone will show "Unarchive this repository". This is reversible but
requires admin access to the `coldstoneadmin` account. Do not archive until the deploy
test is green and the checklist is complete.
