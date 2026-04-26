# Telegram Bot Setup

Telegram is a messaging app. The trading system uses a Telegram bot to send you alerts when something needs your attention — for example, if a service crashes, a league hits its drawdown limit, or a configuration problem is detected.

Alerts only fire when human action is needed. Routine activity is silent.

You will need the Telegram app on your phone (or desktop). It is free.

---

## 1 — Get a bot token from BotFather

**@BotFather** is Telegram's official bot for creating other bots. It gives you a **bot token** — a long string of characters that identifies your bot and lets your server send messages through it.

- ✅ **1.1** Install Telegram on your phone or desktop if you have not already.
- ✅ **1.2** Open Telegram and search for `@BotFather` (with the blue checkmark — it is the official one).
- ✅ **1.3** Start a chat with BotFather and send `/newbot`.
- ✅ **1.4** BotFather will ask for a name (e.g. `My Trading Alerts`) and a username ending in `bot` (e.g. `mytrading_alertbot`).
- ✅ **1.5** BotFather will respond with your bot token. It looks like:
  ```
  110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
  ```
  Copy this and save it somewhere safe — you will need it in a moment.

---

## 2 — Get your chat ID

Your **chat ID** is a number that tells the bot which conversation to send messages to. You need this so alerts arrive in your personal chat, not lost in some unknown Telegram room.

- ✅ **2.1** In Telegram, search for `@userinfobot` and start a chat.
- ✅ **2.2** Send it any message (e.g. `/start`).
- ✅ **2.3** It will reply with your numeric user ID. It looks like `123456789`. Copy this number.

Alternatively, visit `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates` in a browser after sending yourself a message via the bot — the `chat.id` field in the response is your ID. The userinfobot method is simpler.

---

## 3 — Start a chat with your new bot

Before the bot can message you, you need to start a conversation with it first (Telegram blocks bots from messaging people who have never talked to them).

- ✅ **3.1** In Telegram, search for your bot's username (e.g. `@mytrading_alertbot`).
- ✅ **3.2** Open it and press "Start" or send `/start`.

---

## 4 — Add credentials to config.yaml

During `setup.sh` (see `getting_started.md` Phase 4.2), you will be prompted:

```
Telegram bot token: 
Telegram chat ID:
```

Enter the token and chat ID you collected above.

If you have already run setup, you can edit `config.yaml` directly:

```bash
nano /root/my-trading-toolkit/config.yaml
```

Find the `telegram:` section and fill in:

```yaml
telegram:
  bot_token: "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
  chat_id: "123456789"
```

Save and exit (`Ctrl+X`, `Y`, Enter).

---

## 5 — Verify it works

Run the sanity check:

```bash
cd /root/my-trading-toolkit
./scripts/sanity_check.sh
```

The script sends a test message through your bot. You should receive a Telegram notification within a few seconds. If the check shows `[GREEN] Telegram reachable`, you are done.

### If you do not receive the test message

1. Confirm you started a chat with your bot (Step 3 above — this is the most common cause).
2. Double-check the bot token and chat ID in `config.yaml` (no extra spaces or quotes).
3. Check that your Telegram notifications are not muted.
4. Re-run `sanity_check.sh` and read any `[RED]` lines for specific error messages.
