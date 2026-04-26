# Getting Started

**Reading time:** 15 minutes  
**Setup time:** 60-90 minutes to paper trading  
**Paper trading period:** 1-2 weeks before you consider live funding

You are setting up a copy of an automated trading system that runs on a cloud server 24 hours a day. Once it is running, you do not need to be at your computer. This guide walks you through every step.

---

## Before you begin: pick a mode

There are two ways to run this system:

| | Lite mode | Full mode |
|---|---|---|
| AI research cost | $0 (you use Chris's strategies) | $5-15/month (your own AI) |
| Setup complexity | Lower | Higher |
| Who controls the strategy | Chris's "Mother" server | You |
| Good for | Most people | Advanced users who want independence |

**Recommendation: choose lite mode.** If you have never set up a server before, start with lite. You can switch later.

---

## Phase overview

```
Phase 1: Create accounts       (~20 min)
Phase 2: Rent a server         (~15 min, then wait for provisioning)
Phase 3: Connect to server     (~10 min)
Phase 4: Install the toolkit   (~20 min)
Phase 5: Paper trading         (1-2 weeks, passive)
Phase 6: Fund and go live      (~10 min when ready)
```

---

## Phase 1 — Create accounts

- ✅ **1.1** Create a Kraken account and complete identity verification.  
  Full guide: [docs/funding_kraken.md](funding_kraken.md)  
  Note: Kraken's identity check (KYC) takes 1-3 business days. Do this first so it is approved by the time you need it.

- ✅ **1.2** Create a Telegram bot for alerts.  
  Full guide: [docs/telegram_setup.md](telegram_setup.md)  
  This lets the system send you a message when something goes wrong.

---

## Phase 2 — Rent a server

A **VPS (Virtual Private Server)** is a Linux computer in a data center that you rent by the month. Your trading system runs on it around the clock so you do not need to leave your laptop on.

Full guide: [docs/vps_rental.md](vps_rental.md) — covers provider choice, specs, and initial hardening.

- ✅ **2.1** Rent a VPS with at least 2 GB RAM, 20 GB disk, running Ubuntu 24.04.  
  Cost: around $5-6/month. Write down the IP address the provider gives you.

### How to verify it worked

Log in to your provider's web console. You should see your server listed with a public IP address and status "Running" (or similar).

---

## Phase 3 — Connect to your server

**SSH** is a secure way to type commands on a remote Linux computer from your own machine, like a remote control for the server.

### Generate an SSH key pair

An SSH key is a password-free login credential — a matched pair of a private key (stays on your machine) and a public key (goes on the server). Do not share the private key file with anyone.

Open a terminal on your computer (Terminal on Mac, Windows Terminal or Git Bash on Windows) and run:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

When asked where to save it, press Enter to accept the default (`~/.ssh/id_ed25519`).  
When asked for a passphrase, either set one (more secure) or press Enter twice to skip.

This creates two files:
- `~/.ssh/id_ed25519` — your private key. Never share this file.
- `~/.ssh/id_ed25519.pub` — your public key. This is what goes on the server.

### Copy your public key to the server

Most VPS providers let you paste a public key during setup, or provide a root password for first login. To print your public key so you can copy it:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519`). In your VPS provider's dashboard, paste it into the "SSH keys" or "Authorized keys" field.

If your provider gave you a root password instead, log in with:

```bash
ssh root@YOUR_SERVER_IP
```

Then paste your public key into `~/.ssh/authorized_keys` on the server (create the file if it does not exist) and set correct permissions:

```bash
mkdir -p ~/.ssh
echo "PASTE_YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

- ✅ **3.1** SSH key generated and added to server.

### Test the connection

```bash
ssh root@YOUR_SERVER_IP
```

If you see a Linux command prompt, you are connected.

- ✅ **3.2** Verified SSH login works.

---

## Phase 4 — Install the toolkit

You will do the following steps while connected via SSH to your server.

### 4.1 — Create a private copy of the repo

A **repository (repo)** is a folder of code stored on GitHub. You need your own private copy so your API keys and configuration never become public.

You will need a free GitHub account. Once you have one, create a private fork:

```bash
# Install the GitHub CLI if it is not present
apt-get update -y && apt-get install -y gh git

# Authenticate GitHub CLI (follow the prompts — it will open a browser)
gh auth login

# Create a private repo from the template
gh repo create my-trading-toolkit \
  --private \
  --template payindaman-wq/crypto-trading-toolkit \
  --clone
cd my-trading-toolkit
```

This creates a private copy of the code under your GitHub account and clones it to the server.

- ✅ **4.1** Repo cloned to `/root/my-trading-toolkit` (or wherever you chose).

### How to verify it worked

```bash
ls /root/my-trading-toolkit
```

You should see files including `README.md`, `config.example.yaml`, and a `scripts/` folder.

### 4.2 — Run setup

```bash
cd /root/my-trading-toolkit
./scripts/setup.sh --mode lite
```

The script will ask you a series of questions. Here is what each prompt means:

| Prompt | What to enter |
|---|---|
| Kraken API key | The key you created in Phase 1 (from funding_kraken.md) |
| Kraken API secret | The secret paired with the key above |
| Telegram bot token | The token you got from @BotFather (from telegram_setup.md) |
| Telegram chat ID | Your numeric chat ID (from telegram_setup.md) |
| VPS host | Your server's IP address (e.g. `203.0.113.42`) |
| Dashboard domain | Press Enter to use the default (your raw IP is fine) |

The script writes a file called `config.yaml` that is never uploaded to GitHub — it stays on your server only.

- ✅ **4.2** `setup.sh` completed without errors.

### 4.3 — Run sanity check

```bash
./scripts/sanity_check.sh
```

This tests whether the configuration is valid and all external services are reachable. Read the output:

| Color code | Meaning |
|---|---|
| `[GREEN]` | That item is working correctly. |
| `[YELLOW]` | A warning — the system will run but something may need attention. |
| `[RED]` | A failure — the system will not work until this is fixed. |

For lite mode you expect GREEN on: config, Kraken API, Telegram. Anthropic and Gemini checks will be skipped (not needed in lite mode).

- ✅ **4.3** Sanity check passes with no RED items.

### How to verify it worked

At the end of `sanity_check.sh` you should see a summary line with 0 failures. You should also receive a test message in your Telegram app.

---

## Phase 5 — Enable NJORD in paper mode

**NJORD** is the Capital Allocation Officer — the component that reads the champion strategy and decides how much of your balance to allocate to each bot. **Paper mode** means it simulates trades with fake money, so you can watch it work for 1-2 weeks before risking real money.

### Edit config.yaml

Open the config file in a text editor on the server:

```bash
nano /root/my-trading-toolkit/config.yaml
```

Find the `njord:` section and change it to:

```yaml
njord:
  enabled: true
  mode: "paper"
  total_capital_usd: 1000   # simulated paper balance
```

Save and exit (`Ctrl+X`, then `Y`, then Enter in nano).

### Add NJORD to the cron scheduler

**Cron** is a Linux scheduler that runs programs automatically on a timer. Run:

```bash
crontab -e
```

If asked which editor to use, pick `nano` (usually option 1).

Add this line at the bottom:

```
*/30 * * * * python3 /root/my-trading-toolkit/research/njord.py run >> /root/my-trading-toolkit/competition/njord.log 2>&1
```

Save and exit.

- ✅ **5.1** NJORD enabled in paper mode and cron entry added.

### How to verify it worked

Wait up to 30 minutes for the first NJORD cycle, then check:

```bash
python3 /root/my-trading-toolkit/research/njord.py status
```

You should see a one-screen summary showing a paper portfolio with allocations across active leagues.

---

## Phase 6 — Paper trading period (1-2 weeks)

Leave the system running. During this time:

- Check `competition/njord.log` a few times per day to see what NJORD is doing.
- Pay attention to any Telegram alerts — they mean something needs your attention.
- Review `docs/troubleshooting.md` if something looks wrong.

Do not add real money until you have watched the paper trading for at least one full week and are comfortable with what you see.

---

## Phase 7 — Fund Kraken and switch to live

After at least one week of paper trading:

- ✅ **7.1** Fund your Kraken account. Recommended starting amount: $200-500.  
  See [docs/funding_kraken.md](funding_kraken.md) for ACH/wire instructions.

- ✅ **7.2** Switch NJORD to live mode. Edit `config.yaml`:

```yaml
njord:
  enabled: true
  mode: "live"
  total_capital_usd: 300   # match what you funded, e.g. 300
```

Save the file. NJORD picks up the change on its next 30-minute cycle.

- ✅ **7.3** Verify in `competition/njord.log` that NJORD is now showing live balance, not paper balance.

---

## Daily monitoring

Once live, you mostly do not need to do anything. The system monitors itself. However:

- **Check Telegram** when you get an alert. Alerts only fire when the system needs a human decision — routine operations are silent.
- **Check the dashboard** by navigating to `http://YOUR_SERVER_IP/` in a browser. You should see live league standings.
- **Once a week:** run `python3 /root/my-trading-toolkit/research/njord.py status` to review capital allocations.

The **killswitch** automatically pauses a league if it draws down 15% from its peak. You will receive a Telegram alert when this happens.

---

## If something breaks

See [docs/troubleshooting.md](troubleshooting.md) for solutions to common errors.

If the troubleshooting guide does not resolve the issue, check the GitHub Discussions page for the repo or contact Chris.
