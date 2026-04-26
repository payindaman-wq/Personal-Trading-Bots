# Renting a VPS

A **VPS (Virtual Private Server)** is a Linux computer in a data center that you rent for a monthly fee. It runs 24 hours a day, 7 days a week, even when your laptop is closed. Your trading system needs a VPS because it must be online continuously to check prices and place orders.

You do not need to understand Linux deeply to use one — this guide covers exactly what to do.

---

## Recommended providers

| Provider | Price | Notes |
|---|---|---|
| Hetzner | ~$5/mo | Best value, European data centers (works fine for US traders) |
| DigitalOcean | ~$6/mo | US data centers, simple interface, good docs |
| Linode / Akamai | ~$5/mo | US data centers, solid reliability |

**Avoid AWS for personal use.** AWS billing is complex and easy to misconfigure in ways that result in unexpectedly large bills. The providers above have simple flat monthly pricing.

---

## What specs to order

When ordering, select:

- **RAM:** 2 GB minimum (4 GB if the provider's pricing allows it for similar cost)
- **Disk:** 20 GB minimum
- **OS:** Ubuntu 24.04 LTS (the version matters — scripts are tested on this)
- **Location:** Any data center. Closer to you or to your exchange (Kraken is US-based) is slightly better, but any location works.

Example on Hetzner: "CX22" (~$5/mo) gives 2 vCPU, 4 GB RAM, 40 GB disk — plenty of headroom.

---

## Ordering (Hetzner example)

The steps are similar across providers.

- ✅ **1.1** Go to hetzner.com and create an account.
- ✅ **1.2** Go to Cloud > Servers > Create Server.
- ✅ **1.3** Select a location, then select "Ubuntu 24.04" as the image.
- ✅ **1.4** Select the CX22 (or equivalent ~$5/mo) plan.
- ✅ **1.5** Under "SSH Keys," paste your public key (from `getting_started.md` Phase 3). This lets you log in without a password.
- ✅ **1.6** Click "Create & Buy Now."
- ✅ **1.7** Note the public IPv4 address shown on the server dashboard. You will use this to connect.

### How to verify it worked

Open a terminal on your laptop and run:

```bash
ssh root@YOUR_SERVER_IP
```

If you see a Linux command prompt (something like `root@ubuntu-server:~#`), your server is ready.

---

## Initial server hardening

These are one-time steps that make your server harder to break into. Do them before installing the toolkit.

### Disable password login (SSH key only)

Once your SSH key login is working, disable password login so attackers cannot brute-force the root password:

```bash
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh
```

### Enable the firewall

**UFW** is a simple firewall tool that blocks all incoming traffic except what you explicitly allow. Run:

```bash
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable
```

This allows SSH connections (port 22) and web traffic (for the dashboard). Everything else is blocked.

### Install fail2ban

**fail2ban** watches for repeated failed login attempts and automatically blocks those IP addresses:

```bash
apt-get install -y fail2ban
systemctl enable --now fail2ban
```

### Enable automatic security updates

This ensures the operating system patches itself for known security vulnerabilities without you having to do anything:

```bash
apt-get install -y unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

Select "Yes" when prompted.

- ✅ **2.1** All four hardening steps complete.

---

## Dashboard access

The trading system runs a web dashboard at `http://YOUR_SERVER_IP/`. You access it by typing your server's IP address directly into a browser — no domain name needed.

If you want a proper domain name (e.g. `dashboard.mytrading.io`) you can point a domain's DNS A-record to your server IP, then update `dashboard.domain` in `config.yaml`. This is optional and can be done any time after setup.

---

## Monthly cost summary

| Item | Monthly cost |
|---|---|
| VPS (Hetzner CX22 or equivalent) | ~$5 |
| Lite mode AI: Anthropic + Gemini | $0 |
| Full mode AI: Anthropic + Gemini | ~$5-15 (varies) |
| Kraken trading fees | Per trade (varies) |

Total for lite mode: approximately $5/month.
