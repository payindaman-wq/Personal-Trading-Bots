# Troubleshooting

Common errors and how to fix them. Start with `getting_started.md` if you have not completed setup.

---

## "config.yaml missing" or setup prompts appear again

**Cause:** `config.yaml` does not exist or is in the wrong directory.

**Fix:** Run setup from the repo root directory:

```bash
cd /root/my-trading-toolkit
./scripts/setup.sh --mode lite
```

If you are unsure which directory you are in, run `pwd` to print the current path.

---

## "Anthropic API call failed" (full mode only)

**Cause:** The Anthropic API key is wrong, expired, or the account has hit its daily budget.

**Steps:**

1. Check that the key in `config.yaml` matches the one in your Anthropic console (console.anthropic.com).
2. Check your Anthropic account for any billing issues.
3. The system enforces a `daily_budget_usd` cap in `config.yaml`. If the cap was hit today, AI calls will fail until midnight UTC when the counter resets. Check `competition/anthropic_usage.jsonl` for today's spend.

**This error does not appear in lite mode** — lite mode does not use the Anthropic API.

---

## "No champion.yaml in published/" (lite mode)

**Cause:** Your local copy of the repo is missing the published strategy files. This happens when the initial sync did not complete, or when the upstream Mother server has not published yet.

**Fix:** Manually pull the latest files from upstream:

```bash
cd /root/my-trading-toolkit
git fetch upstream && git pull upstream main
```

If this command fails with a "remote not found" error:

```bash
git remote add upstream https://github.com/payindaman-wq/crypto-trading-toolkit
git fetch upstream && git pull upstream main
```

If the published files still do not appear after pulling, Mother's publisher may be temporarily down. Wait 4-8 hours and try again. You will receive a Telegram alert automatically if the sync has been failing for more than 3 hours.

---

## "NJORD won't start" or no NJORD cycles in the log

Check the following in order:

**1. Is NJORD enabled in config.yaml?**

```bash
grep -A5 "^njord:" /root/my-trading-toolkit/config.yaml
```

You should see `enabled: true`. If it says `enabled: false`, edit config.yaml and change it to `true`.

**2. Is the cron entry present?**

```bash
crontab -l | grep njord
```

You should see a line containing `njord.py run`. If nothing appears, add it:

```bash
crontab -e
```

Add at the bottom:
```
*/30 * * * * python3 /root/my-trading-toolkit/research/njord.py run >> /root/my-trading-toolkit/competition/njord.log 2>&1
```

**3. Are Kraken keys present (live mode only)?**

If `njord.mode` is `"live"`, Kraken keys are required. Check that `kraken.api_key` and `kraken.api_secret` are filled in `config.yaml`. In paper mode, Kraken keys are not required.

**4. Is mode set correctly?**

If you are past the paper trading period and want live trading, confirm `njord.mode: "live"` in `config.yaml`.

**5. Check the log for errors:**

```bash
tail -50 /root/my-trading-toolkit/competition/njord.log
```

Read the last 50 lines. Any Python traceback will point to the specific problem.

---

## "Telegram alerts not arriving"

**Steps in order:**

1. **Did you start a chat with your bot?** Open Telegram, search for your bot's username, and press Start if you have not. Bots cannot message you until you initiate contact.

2. **Is the bot token correct?** Check `telegram.bot_token` in `config.yaml`. It should look like `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`.

3. **Is the chat ID correct?** Check `telegram.chat_id` in `config.yaml`. It should be a plain number like `123456789`. Get it from `@userinfobot` if unsure.

4. **Run the telegram test:**

   ```bash
   cd /root/my-trading-toolkit
   ./scripts/sanity_check.sh
   ```

   Look for `[GREEN] Telegram reachable` or a `[RED]` line with the error.

5. **Check your phone's notification settings.** The message may be arriving but silently — open Telegram and look in the bot's chat directly.

---

## "I'm losing money"

First: take a breath. All trading systems go through periods of loss. The question is whether the loss is within expected parameters or a sign of something broken.

**Steps:**

1. **Check the log:**

   ```bash
   tail -100 /root/my-trading-toolkit/competition/njord.log
   ```

   Look for any errors or unusual messages.

2. **Check if the killswitch has fired:**

   ```bash
   python3 /root/my-trading-toolkit/research/njord.py status
   ```

   If a league has triggered the 15% drawdown killswitch, it will show as paused. This is working as intended — the system stopped the bleeding automatically.

3. **Consider switching back to paper mode:**

   Edit `config.yaml` and set `njord.mode: "paper"`. NJORD will stop placing live orders and resume paper simulation. This is always safe to do.

   ```yaml
   njord:
     enabled: true
     mode: "paper"
   ```

4. **Review the champion strategy:**

   Check when the champion last changed by looking at `published/<league>/champion.meta.json`:

   ```bash
   cat /root/my-trading-toolkit/published/day/champion.meta.json
   ```

   If `ts` is very recent, the strategy was just updated. Give it a day or two to establish a baseline.

5. **Do not change anything in panic.** Strategy fluctuation over days is normal. A sustained loss over multiple weeks is worth investigating more deeply.

---

## General debugging approach

If something is not covered above:

1. Run `./scripts/sanity_check.sh` and read every `[RED]` and `[YELLOW]` line.
2. Check the relevant log file in `competition/` (e.g. `njord.log`, `strategy_sync.log`).
3. Run `python3 research/njord.py status` for a summary of NJORD's current state.
4. Look at recent Telegram messages — the system sends a message when it detects a problem.
