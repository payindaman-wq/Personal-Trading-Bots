# Lite Mode

Lite mode lets you run the trading toolkit with zero AI cost by pulling
champion strategies that Mother's full-mode VPS researches and publishes.

## How it works

Mother's VPS (mode: full) runs ODIN, MIMIR, VIDAR, and LOKI continuously,
evolving strategies via evolutionary search + deep analysis. Every 4 hours it
publishes the current champion strategy for each league to
`published/<league>/champion.yaml` in this repo and pushes to GitHub.

Your lite-mode VPS fetches those files every 4 hours via `strategy_sync.py`.
NJORD (your capital allocation officer) reads `published/<league>/champion.yaml`
and executes against your Kraken account.

**AI workload is fixed**: Mother pays the same Anthropic + Gemini bill whether
one friend or fifty friends pull. Friends in lite mode pay $0 for AI.

## What's running on your VPS

| Component | Status | Why |
|---|---|---|
| competition ticks (all leagues) | running | market execution, free |
| league_watchdog | running | auto-restart stale ticks, free |
| NJORD (paper or live) | running | strategy execution on your Kraken |
| strategy_sync (cron) | running | pulls latest champions every 4h |
| killswitch | running | 15% drawdown protection |
| sys_heartbeat (SYN) | running | health + Telegram alerts |
| exchange_health | running | Kraken reachability monitor |
| TYR (risk officer) | running | macro regime, free (Gemini-lite) |
| HEIMDALL | running | market intelligence, free (Gemini-lite) |
| ODIN (4 services) | **stopped** | evolutionary research needs AI keys |
| FREYA | **stopped** | prediction markets research needs AI keys |
| MIMIR | **noop** | deep analysis, spawned by ODIN (which is stopped) |
| LOKI | **noop** | exits cleanly if mode=lite |
| VIDAR/vidar_executor | **noop** | meta-audit + arbitration, exits if mode=lite |
| meta_audit | **noop** | exits cleanly if mode=lite |

## Setup

```bash
./scripts/setup.sh --mode lite
```

This will:
1. Write config.yaml with `mode: lite` and your Kraken keys
2. Add the `upstream` remote pointing to the Mother repo
3. Install the `strategy_sync` cron entry
4. Run the initial `git pull upstream main` to get current champions

## Switching to full mode

If you want your own AI research (independent of Mother's strategies):

1. Edit config.yaml, set `mode: "full"`
2. Fill in `anthropic.api_key` and `gemini.api_key`
3. Run: `systemctl enable --now odin_day odin_swing odin_futures_day odin_futures_swing freya`
4. Remove the `strategy_sync` cron entry (no longer needed)

## Trust model

In lite mode you are running Mother's strategies without independent
verification. Recommended approach for the first sprint cycle:

- Leave NJORD in paper mode (`njord.mode: paper`) for one full sprint cycle
- Compare paper results against the published champion's `source_sharpe`
- Switch to live (`njord.mode: live`) once you trust the output

If you see the champion not changing for >24 hours, Mother's publisher may
be down. `strategy_sync.py` will write a syn_inbox alert after 3 hours of
sync failures, which your sys_heartbeat will forward to Telegram.

## Sync latency

Strategies publish every 4 hours (Mother) and sync every 4 hours (you, offset
15 minutes). Maximum staleness: 8 hours. Adjust cron frequency in
`competition/strategy_sync_state.json` if you need fresher data, but avoid
syncing more than once per hour to avoid hammering GitHub.

## The published/ directory

```
published/
  day/
    champion.yaml         sanitized strategy (no internal _fields)
    champion.meta.json    { ts, source_gen, source_sharpe, source_oos_sharpe, sanitization_version }
  swing/
    champion.yaml
    champion.meta.json
  futures_day/
    champion.yaml
    champion.meta.json
  futures_swing/
    champion.yaml
    champion.meta.json
```

Mother's `strategy_publisher.py` writes and commits these files.
Only `published/` is committed; no research state, no API keys.
