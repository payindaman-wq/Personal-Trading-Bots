# NJORD - Capital Allocation Officer

NJORD translates the strategy decisions emitted by upstream officers into
per-bot capital allocations on Kraken. It is **disabled by default** and
designed for a phased activation: paper-trading first, live only after the
operator has watched a paper run for at least one week.

## What NJORD does each cycle

Every 30 minutes (when enabled via cron), NJORD:

1. Reads `config.njord` and discovers the bot fleet under
   `fleet/<league>/<bot>/strategy.yaml`.
2. Pulls account balance from Kraken (live mode) or uses
   `config.njord.total_capital_usd` as the paper-mode balance.
3. Computes per-bot target USD using `league_weights` and
   `per_bot_max_pct`.
4. Diffs targets against `competition/njord_allocation.json` and emits a
   list of actions (rebalance, pause_bot, wake_bot, shift_league_weight,
   etc.).
5. Classifies each action into Tier 1 / 2 / 3 using
   `research/vidar_tier.classify_finding`. When no Anthropic key is
   configured (or `NJORD_NO_LLM_CLASSIFY=1`), falls back to a built-in
   action-type table.
6. Routes by tier:
   - **Tier 1** auto-applied: rebalance within tolerances, individual-bot
     drawdown kill at `drawdown_kill_pct` (reversible).
   - **Tier 2** queued in `competition/njord_pending_review.flag` with a
     24h auto-stay window; revert via
     `python3 research/njord.py revert <finding_id>`.
   - **Tier 3** never executes - written to `syn_inbox.jsonl` with
     `severity=critical` and `tg_allowed=true`. `sys_heartbeat` surfaces
     these to Telegram via `TG_ALLOWED_SOURCES` (when
     `telegram_required_for_tier3=true`).

Wallet operations (deposit/withdraw), API key rotations, permanent league
retirements, and total-capital changes greater than 25% are all Tier 3.

## Tier 1 / Tier 2 / Tier 3 action map

| Action type           | Tier  | Notes                                    |
|-----------------------|-------|------------------------------------------|
| rebalance             | 1     | Within `per_bot_max_pct` cap             |
| pause_bot             | 1     | Drawdown trip (reversible kill flag)     |
| wake_bot              | 2     | Resumes capital flow                     |
| shift_league_weight   | 2     | Capital-adjacent reallocation            |
| reduce_total          | 2     | Shrink deployed capital                  |
| wallet_op             | 3     | Real money movement at exchange          |
| key_change            | 3     | Rotate Kraken API credentials            |
| retire_league         | 3     | Permanent league retirement              |
| total_change_25pct    | 3     | Total-capital change > 25%               |

## Activation flow

NJORD ships disabled. The progression is:

1. **Paper-trading bring-up.** In `config.yaml`:
   ```yaml
   njord:
     enabled: true
     mode: "paper"
     total_capital_usd: 1000   # the paper balance to simulate against
   ```
   No Kraken keys are required for paper mode.
2. **Add the cron entry.**
   ```cron
   */30 * * * * python3 /root/.openclaw/workspace/research/njord.py run >> /root/.openclaw/workspace/competition/njord.log 2>&1
   ```
3. **Watch for at least one week.** Review
   `competition/njord.log`, `competition/njord_allocation.json`, and any
   entries in `competition/njord_pending_review.flag`. The
   `python3 research/njord.py status` command prints a one-screen summary.
4. **Switch to live.** Only after paper validation:
   - Deposit funds to your Kraken account.
   - Set `kraken.api_key` and `kraken.api_secret` in `config.yaml`.
   - Set `njord.mode: "live"` and `njord.total_capital_usd` to the live
     balance you intend to allocate.
   - Live mode pulls actual balance from Kraken on each cycle. Live order
     placement (`_live_balance_usd` and `_live_market_order` in
     `research/njord_kraken.py`) raises `NotImplementedError` in the
     public template - wire these through `krakenex` or `ccxt` in your
     fork before flipping to live.

## Files

| Path                                          | Purpose                                  |
|-----------------------------------------------|------------------------------------------|
| `research/njord.py`                           | Orchestrator (CLI entry point)           |
| `research/njord_kraken.py`                    | Paper / live Kraken adapter              |
| `research/njord_allocator.py`                 | Pure allocation math                     |
| `research/test_njord_smoke.py`                | Sandboxed paper-mode smoke test          |
| `competition/njord_allocation.json`           | Per-bot allocation table (runtime state) |
| `competition/njord_paper_state.json`          | Paper-mode portfolio state               |
| `competition/njord_pending_review.flag`       | Tier-2 24h auto-stay queue               |
| `competition/njord.log`                       | Cycle log                                |

## Smoke test

```bash
python3 research/test_njord_smoke.py
```

Runs in a sandboxed `WORKSPACE` (system tempdir) without touching the live
configuration or hitting the network. Exits 0 on full pass.
