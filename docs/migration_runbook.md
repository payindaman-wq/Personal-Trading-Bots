# Migration Runbook: coldstoneadmin → payindaman-wq

**Estimated time:** 30-45 minutes
**What this does:** Migrates the active repo from `coldstoneadmin/crypto-trading-toolkit`
to two new repos under your `payindaman-wq` GitHub account — a public template friends
fork, and a private personal repo the VPS deploys from.
**Prerequisites:**
- Logged into github.com as `payindaman-wq`
- SSH access to `204.168.167.19` working from your laptop
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
ssh root@204.168.167.19 "cd /root/.openclaw/workspace && git status && echo '---' && git log --oneline -5"
```

Expected: `Your branch is up to date with 'origin/master'.` and `nothing to commit`
(untracked runtime files are fine — they are gitignored). The top commit should be
`0325adb docs: add complete beginner onboarding suite (Session S)` or a later commit.

**Confirm config.yaml is gitignored:**

```bash
ssh root@204.168.167.19 "cd /root/.openclaw/workspace && git check-ignore config.yaml && echo 'OK: config.yaml is ignored'"
```

Expected output: `config.yaml` followed by `OK: config.yaml is ignored`. If this
command produces no output, stop — config.yaml is NOT ignored and you risk pushing
secrets to a public repo.

**Confirm current origin:**

```bash
ssh root@204.168.167.19 "cd /root/.openclaw/workspace && git remote -v"
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
2. Repository name: `trading-toolkit-personal`
3. Visibility: **Private**
4. Leave all "Initialize this repository" options **unchecked**
5. Click **Create repository**

**Verify both exist:**

- https://github.com/payindaman-wq/crypto-trading-toolkit — should show "Quick setup"
  (empty repo)
- https://github.com/payindaman-wq/trading-toolkit-personal — same

---

## Step 2 — Push the public template to payindaman-wq/crypto-trading-toolkit (~5 min)

This pushes the current master branch from the VPS to the new public repo. Origin is
not changed here — you are adding a temporary remote for the one-shot push only.

```bash
ssh root@204.168.167.19
```

Once connected:

```bash
cd /root/.openclaw/workspace

git remote add public https://<NEW_PAT>@github.com/payindaman-wq/crypto-trading-toolkit.git
git push public master
git remote remove public
```

The push may take 15-30 seconds. When it completes, visit
https://github.com/payindaman-wq/crypto-trading-toolkit — you should see the full
codebase with README, LICENSE, and docs/.

**Verify config.yaml is absent from the public repo:**

Browse to https://github.com/payindaman-wq/crypto-trading-toolkit/blob/master/config.yaml

GitHub should return a 404 or "File not found". If it is present, stop — do not
proceed until you understand why. (This would mean config.yaml was accidentally
committed at some point in the source repo's history.)

---

## Step 3 — Set up the private personal Mother repo (~10 min)

The personal repo is what the VPS deploys from. It holds the same code as the public
template, plus your `config.yaml` tracked privately.

### 3.1 — Re-point origin to the personal repo

```bash
# Still on the VPS, still in /root/.openclaw/workspace
git remote set-url origin https://<NEW_PAT>@github.com/payindaman-wq/trading-toolkit-personal.git
git push -u origin master
```

Wait for the push to complete. The personal repo now has the full codebase.

### 3.2 — Track config.yaml in the personal repo only

`config.yaml` is listed in `.gitignore`, which prevents it from being committed. The
`.gitignore` itself is tracked and shared with the public template, so you must not
modify `.gitignore` to allow `config.yaml` — that change would propagate upstream when
you pull future improvements.

Instead, use the per-clone exclude file. This is local to this clone only and is never
committed or pushed:

```bash
# Tell this clone to treat !config.yaml as an override to .gitignore
echo '!config.yaml' >> .git/info/exclude

# Now git can see config.yaml — add and commit it
git add config.yaml
git commit -m "personal: track config.yaml in private Mother repo"
git push origin master
```

**Why .git/info/exclude instead of modifying .gitignore:**
`.git/info/exclude` lives inside the hidden `.git/` directory and is never committed.
It applies only to this specific clone on this VPS. If you ever re-clone the personal
repo from scratch, repeat this `echo` line before running `git add config.yaml`. The
Mother instance is the only deployment of the personal repo, so this is a one-time
concern.

**Verify config.yaml is tracked:**

```bash
git ls-files config.yaml
```

Expected output: `config.yaml`. If blank, the add/commit above did not succeed — check
for errors in the prior output.

---

## Step 4 — Update GitHub Actions secrets in the personal repo (~5 min)

The deploy workflow (`.github/workflows/deploy.yml`) triggers on every push to master
and SSH's into the VPS to run `git reset --hard origin/master`. The workflow was
copied into the personal repo in Step 3. It needs two GitHub secrets to authenticate.

**Navigate to the secrets page:**

https://github.com/payindaman-wq/trading-toolkit-personal/settings/secrets/actions

Add the following two secrets (click "New repository secret" for each):

| Secret name | Value |
|---|---|
| `VPS_HOST` | `204.168.167.19` |
| `VPS_SSH_KEY` | Contents of the deploy private key on the VPS (see below) |

**To find the deploy SSH key:**

```bash
ssh root@204.168.167.19 "ls ~/.ssh/"
```

Look for a key whose public half is in `~/.ssh/authorized_keys`. To print the private
key contents for pasting:

```bash
ssh root@204.168.167.19 "cat ~/.ssh/id_ed25519"
```

Copy the entire output including the `-----BEGIN OPENSSH PRIVATE KEY-----` and
`-----END OPENSSH PRIVATE KEY-----` lines. Paste it as the value for `VPS_SSH_KEY`.

---

## Step 5 — Add a persistent public remote for strategy publishing (~5 min)

**This step corrects a design gap that would otherwise break friend syncing.**

`strategy_publisher.py` pushes published champion strategies to `origin master`. After
Step 3, `origin` is the *private* personal repo. Friends who fork the public template
run `strategy_sync.py`, which pulls from the *public* template repo — a private origin
means they can never pull your published strategies.

The fix: add a permanent `public` remote on the VPS pointing at the public template.

```bash
ssh root@204.168.167.19
cd /root/.openclaw/workspace

git remote add public https://<NEW_PAT>@github.com/payindaman-wq/crypto-trading-toolkit.git
```

Verify:

```bash
git remote -v
```

You should see: `origin` (personal, for fetch and push) and `public` (public template,
for fetch and push).

**Note on PAT storage:** The PAT embedded in the `public` remote URL is stored in
plaintext in `.git/config`. This file is inside the `.git/` directory and is never
committed, so it will not be pushed to GitHub. Use a PAT with `public_repo` scope only
(narrower than `repo`) and rotate it when you rotate your other tokens.

**Update the strategy publisher crontab to mirror to public after each run:**

```bash
crontab -e
```

Find the existing publisher cron line:

```
0 */4 * * * python3 /root/.openclaw/workspace/strategy_publisher.py >> /root/.openclaw/workspace/competition/strategy_publisher.log 2>&1
```

Replace it with (keep as one line):

```
0 */4 * * * python3 /root/.openclaw/workspace/strategy_publisher.py >> /root/.openclaw/workspace/competition/strategy_publisher.log 2>&1 && git -C /root/.openclaw/workspace push public master >> /root/.openclaw/workspace/competition/strategy_publisher.log 2>&1
```

Save and exit. Now every 4-hour publish cycle pushes the updated `published/` files to
both the personal repo (via `origin`, done by the script) and the public template (via
the appended `git push public master`).

**Update strategy_sync.py's hard-coded URL** so the instructions friends receive when
running `strategy_sync.py --status` point at the new public repo:

```bash
sed -i 's|github.com/coldstoneadmin/crypto-trading-toolkit|github.com/payindaman-wq/crypto-trading-toolkit|g' /root/.openclaw/workspace/strategy_sync.py
```

Verify:

```bash
grep 'payindaman-wq' /root/.openclaw/workspace/strategy_sync.py
```

Expected: two lines containing `payindaman-wq/crypto-trading-toolkit`. Then commit and
push to both remotes:

```bash
git add strategy_sync.py
git commit -m "fix(sync): update upstream URL to payindaman-wq/crypto-trading-toolkit"
git push origin master
git push public master
```

---

## Step 6 — First end-to-end deploy test (~5 min)

Verify the new deploy chain works. Make a trivial commit and push, then watch the
Actions tab.

```bash
ssh root@204.168.167.19
cd /root/.openclaw/workspace

echo "# migrated $(date -u +%Y-%m-%d)" >> CHANGELOG.md
git add CHANGELOG.md
git commit -m "test: verify deploy chain after migration to payindaman-wq"
git push origin master
```

Open the Actions tab:

https://github.com/payindaman-wq/trading-toolkit-personal/actions

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

## Step 8 — Bryan access cleanup (~3 min)

The old repo is now archived and Bryan retains read-only access to it automatically.
No action is needed on the old repo.

Do **not** add Bryan to either new repo. Send him the public template URL so he can
fork it like any other friend would:

```
https://github.com/payindaman-wq/crypto-trading-toolkit
```

The `docs/getting_started.md` in that repo explains the full setup flow.

---

## Step 9 — Update laptop clone (if applicable)

If you have a clone of the old repo on your Windows laptop, update it to point at the
personal repo. Open Git Bash or Windows Terminal in that directory and run:

```bash
git remote set-url origin https://github.com/payindaman-wq/trading-toolkit-personal.git
git fetch origin
git pull origin master
```

Add the public remote on the laptop too if you ever push strategy fixes from there:

```bash
git remote add public https://<NEW_PAT>@github.com/payindaman-wq/crypto-trading-toolkit.git
```

---

## Verification checklist

Tick each item before calling the migration complete.

- [ ] `ssh root@204.168.167.19 "cd /root/.openclaw/workspace && git remote -v"` shows
  `origin` pointing at `payindaman-wq/trading-toolkit-personal`
- [ ] Same command shows `public` pointing at `payindaman-wq/crypto-trading-toolkit`
- [ ] Deploy test from Step 6 ran green in GitHub Actions
- [ ] https://github.com/coldstoneadmin/crypto-trading-toolkit shows an "Archived"
  banner at the top of the page
- [ ] https://github.com/payindaman-wq/crypto-trading-toolkit is public, shows README
  and LICENSE, and does **not** contain `config.yaml`
- [ ] https://github.com/payindaman-wq/trading-toolkit-personal is private and contains
  `config.yaml` (browse to the file directly to confirm it is tracked)
- [ ] `strategy_sync.py` no longer references `coldstoneadmin` — confirmed by:

  ```bash
  ssh root@204.168.167.19 "grep coldstoneadmin /root/.openclaw/workspace/strategy_sync.py"
  ```

  Expected: no output.

- [ ] Sanity check passes:

  ```bash
  ssh root@204.168.167.19 "cd /root/.openclaw/workspace && bash scripts/sanity_check.sh"
  ```

---

## Rollback plan

**Before archiving the old repo (Step 7):** Re-point origin back to the original and
you are fully reverted:

```bash
ssh root@204.168.167.19 "cd /root/.openclaw/workspace && git remote set-url origin https://<OLD_PAT>@github.com/coldstoneadmin/crypto-trading-toolkit.git"
```

Use the old URL you saved during the pre-flight checks.

**After archiving (Step 7):** Rollback requires un-archiving via the old repo's settings
page. The Danger Zone will show "Unarchive this repository". This is reversible but
requires admin access to the `coldstoneadmin` account. Do not archive until the deploy
test is green and the checklist is complete.
