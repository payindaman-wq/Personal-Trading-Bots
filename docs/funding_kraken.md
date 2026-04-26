# Kraken Account Setup

Kraken is the crypto exchange this framework uses for live trading. The bots place orders on Kraken on your behalf. This guide walks through creating an account, generating API keys, and funding it.

This is not financial advice. Kraken is used because it is the exchange the framework's execution layer is built against — specifically Kraken Derivatives US for futures contracts.

---

## 1 — Create a Kraken account

- ✅ **1.1** Go to kraken.com and click "Create Account."
- ✅ **1.2** Enter your email and choose a strong password. Write the password down somewhere safe.
- ✅ **1.3** Verify your email address.

---

## 2 — Complete identity verification (KYC)

**KYC (Know Your Customer)** is a legal requirement. Kraken must verify your identity before you can deposit money or trade. This takes 1-3 business days.

- ✅ **2.1** Log in and click on your account name (top right) then "Verification."
- ✅ **2.2** Select the verification tier that allows ACH or wire deposit. For most US users this is "Intermediate" verification.
- ✅ **2.3** Upload a government-issued photo ID and a selfie as prompted.
- ✅ **2.4** Wait for approval. Kraken will email you when verification is complete.

**Start this step first — it is the slowest part of the whole setup.**

---

## 3 — Create API keys

An **API key** is a password that lets your trading bot connect to Kraken without you having to log in manually. The bot uses it to check prices and place orders.

You will create two separate strings:
- **API Key** — like a username
- **API Secret** — like a password

The secret is shown exactly once. Write it down immediately — Kraken will not show it again.

### Which permissions to enable

When creating the key, enable only these permissions:

| Permission | Enable? | Why |
|---|---|---|
| Query Funds | Yes | Bot needs to know your balance |
| Create & Modify Orders | Yes | Bot places trades |
| Cancel & Close Orders | Yes | Bot exits positions |
| Access WebSockets token | Yes | Required for real-time data |
| Export data | No | Not needed |
| Manage Subaccounts | No | Not needed |
| **Withdraw Funds** | **No — do not enable** | Security — bot should never move money out |

### Steps

- ✅ **3.1** Log in to Kraken. Go to the hamburger menu (top right) > Security > API.
- ✅ **3.2** Click "Generate New Key."
- ✅ **3.3** Give it a name like "trading-bot."
- ✅ **3.4** Enable only the permissions listed above. Make sure "Withdraw Funds" is NOT enabled.
- ✅ **3.5** Click "Generate Key."
- ✅ **3.6** Copy both the API Key and the API Secret somewhere safe (a password manager is ideal). The secret disappears when you close the dialog.

### Security rules

- Never share your API Key or Secret with anyone, including people who offer to help you.
- Never paste them into chat, email, or GitHub.
- If you suspect they were exposed, delete the key immediately in Kraken's API settings and generate a new one.
- The secret is like the password to your Kraken account — treat it that way.

---

## 4 — Fund your account

The framework is designed to start with a small amount. Recommended starting balance: **$200-500**.

**Use ACH or wire transfer, not crypto deposits.** Crypto deposits require you to own crypto already and add extra steps where errors are easy to make. ACH and wire are simpler.

### ACH (US bank account, free, 3-5 business days)

- ✅ **4.1** In Kraken, go to Funding > Deposit.
- ✅ **4.2** Select "USD" then "Bank transfer (ACH / Plaid)."
- ✅ **4.3** Connect your US bank account via Plaid (Kraken's bank connection service).
- ✅ **4.4** Enter the deposit amount. Kraken ACH deposits typically settle in 3-5 business days.

### Wire transfer (faster, may have bank fees)

- ✅ **4.1** In Kraken, go to Funding > Deposit.
- ✅ **4.2** Select "USD" then "Wire transfer."
- ✅ **4.3** Kraken will show you bank routing details. Send the wire from your bank using those details.
- ✅ **4.4** Domestic wires typically arrive in 1-2 business days. Your bank may charge a wire fee ($15-30 is typical).

### How to verify the deposit arrived

Go to Funding > Account Overview. You should see a USD balance once the transfer clears.

---

## 5 — A note on starting balance

NJORD (the capital allocation component) spreads your balance across multiple bot slots. The config option `per_bot_max_pct: 10` means no single bot ever holds more than 10% of your total. With a $300 balance, that caps each bot at $30 — a reasonable amount for testing.

Starting with more than $500 before you have watched the paper trading for two weeks is not recommended. The paper trading period in `getting_started.md` is there for a reason.

See `docs/njord.md` for details on how allocation math works.
