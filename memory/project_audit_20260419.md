# Post-Audit P1/P2 Fix Wave — 2026-04-19 Audit Queue

Audit queue opened 2026-04-19. Post-ship verdict stable 2026-04-20.
MIMIR output audit + data-source integrity drift shipped 2026-04-22 (commit 72bdd9b).
P1/P2 structural fix wave shipped 2026-04-26 across 5 sessions.

## P1/P2 Commit SHAs by Session

- Session 1 (P1-B): 6376b9c — new_best gate uses adj_score + raw-Sharpe veto (meta_audit F1)
- Session 2 (P1-C deploy gap): 6e2c365 — unified deployment gate — _save_fleet consults Session 2 gate
- Session 3.5 (P1-A mode-collapse): 5e0c0e3 — per-archetype elite pool — structural mode-collapse fix (meta_audit F3)
- Session 4 (spot drift tracker): 8b68216 — backtest_sharpe in per_sprint records for spot leagues
- Session 5 (P2-B drawdown ceiling): f2b2b46 — Sortino floor + max-drawdown ceiling on new_best gate (audit-item-4)

## Baselines written by Session 6
- research/data/futures_day_post_p1_seed.json — futures_day archetype distribution at reseed
- research/data/day_post_p1_seed.json — day league archetype distribution at reseed

14-day verifier scheduled (one-time, fires 2026-05-10 17:00 UTC, routine: odin_p1_p2_14day_verifier; covers futures_day + day league).

## Session 9 — 2026-04-26 — Option C recovery from Session 6 failure

P1+P2 wave shipped 2026-04-26 (Sessions 1, 2, 3.5, 4, 5 — SHAs in prior entry). Reseed failed (Session 6) due to two operational bugs: (a) random seeder produces strategies that cannot clear the new unified gate, which is correct behavior of the gate but wrong recipe for the seeder; (b) sys_heartbeat race condition restarted ODIN services mid-reseed, ignoring Session 6's pause flags. Recovery via Option C (Session 9) on 2026-04-26: stripped negative-Sharpe champions from both futures_day and day best_strategy.yaml (raw_sharpe=-2.5267 and _sharpe_24h_median=-0.2132 respectively), placeholder state deployed, ODIN's normal generation cycle now responsible for organic champion promotion under the unified gate. forensic backups: best_strategy.yaml.bak.session9_20260426 + Session 6's .bak.p2_reseed_2026042{6}T*. Option A follow-up audit (random seeder uses successful-strategy DNA + sys_heartbeat maintenance.lock honoring) deferred — see Session 10's scheduled routine. 14-day verifier (Session 7, fires 2026-05-10) covers organic-promotion outcome on both leagues.
Option A audit scheduled (one-time, fires 2026-05-03 17:00 UTC, routine: odin_option_a_seeder_and_watchdog_audit; addresses Session 6's seeder + sys_heartbeat race bugs).

Option A v2 Part D scope extended on 2026-04-26 (Session 10.5) — Session 14 found the rmtree-on-destination is the actual data-destruction mechanism; Part D now removes the rmtree entirely and adds a destination-exists guard, applied to futures_swing/spot_swing/day.

## Session 15 — 2026-04-26 — futures_day pair filter + day MIN_TRADES regime

Fixed two distinct ODIN failures Session 13 surfaced. (A) futures_day pair-filter mode collapse — random pair-selection (`get_pairs(league)` + `random_strategy`) now constrained to per-league universe (Kraken Derivatives US for futures = BTC/ETH/SOL); spot leagues unchanged. Backtest entry rejects any candidate carrying pairs outside the universe. Forensic backup of pre-fix elites at `research/futures_day/population/elites_pre_session15.tar.gz`. After service stop, `watchdog_executor` auto-restarted ODIN at 21:55 UTC, which reseeded from `best_strategy.yaml` (BTC/ETH/SOL, 578 trades) and the population recovered organically; first post-restart perturb child (gen 7876) hit 386 trades with [disc] status, proving Bug A fix is working. The parallel cold-reseed script generated 10 random-strategy seeds that all produced trades=0 (sparsity artifact: random condition thresholds rarely fire on a 3-pair universe), so the script was killed and live ODIN's organic state was preserved. (B) day MIN_TRADES lowered 280 -> 150 to match current low-frequency regime (Session 13 observed all post-restart gens producing <253 trades, 100% rejected). 150 is conservative: high enough to filter genuine ghost-traders, low enough to escape current attractor. Day elite pool NOT flushed (uncorrupted, just attractor-stuck; lowered floor lets it escape organically). Commits: 2e5a74a (bug A), 17e3ca2 (bug B). Open follow-up: `random_strategy` on a 3-pair universe is sparse; the random mutation type is effectively wasted on futures_day until either the universe expands or random_strategy is biased toward higher-trigger thresholds for tiny-universe leagues. Defer until measurable problem.

Option A v2 Part A scope extended on 2026-04-26 (Session 10.6) — Session 15 surfaced that random_strategy produces 0 trades on tiny universes (3-pair Kraken Derivatives US); Part A now includes mutation-layer sparsity handling for universe_size < 5.

Both scheduled routines (Option A v2 + 14-day verifier) scrubbed of status Telegrams on 2026-04-26 (Session 16). Telegrams now fire only on Chris-action conditions per feedback_syn_telegram_chris_action_only.md.

## Session 19 — 2026-04-26 — day league fleet restore + gitignore prevention

Restored 12 day-league bot strategies (floki, bjorn, lagertha, ragnar, leif, gunnar, harald, freydis, sigurd, astrid, ulf, bjarne) from commit f62ad49 after upstream template scrub commit 0694c9d + deploy.yml reset wiped them at 09:00 UTC. Added `fleet/*/strategy.yaml` to .gitignore on Mother VPS so future deploy resets dont repeat. Public template (Personal-Trading-Bots) keeps the .gitkeep posture — fork-friendly. Day league returns to 12 bots at next 09:00 UTC sprint launch. In-flight sprint comp-20260426-0900 untouched (still autobotday-only until end). deploy.yml uses git reset --hard origin/master only — no git clean — so untracked/ignored files survive. Commit: 850de95 (chore gitignore).

## Session 17 — 2026-04-26 — Session 9 strip persistence fix

Investigated why Session 9's 21:24 placeholder strip on research/day/best_strategy.yaml + research/futures_day/best_strategy.yaml didn't persist. Classification: B (second writer reverted, but writer is infra-level not code-level). Root cause: best_strategy.yaml is git-tracked; .github/workflows/deploy.yml runs git reset --hard origin/master via appleboy/ssh-action on every push to master, reverting unstaged yaml changes back to HEAD content (last committed pre-strip champion). meta.json files survived because they are untracked. Same root cause as Session 19's just-shipped fleet/*/strategy.yaml gitignore fix (commit 850de95) but for research/*/best_strategy.yaml — Session 19 didn't address research yamls. Unified gate (odin_researcher_v2.py:857 _save_fleet) remains the only active code-level writer; all 4 other writers checked are inactive (legacy v1 odin_researcher.py:98, volva_researcher.py:62, odin_grid_search.py:168 writes different file, smoke_deploy_gate.py is test-only). Plug: committed placeholder yaml to HEAD (commit 76fe811) so future deploy resets land on placeholder content rather than reverting it. Verified placeholder survived T+0, T+5min, and 6+ ODIN gen cycles (mtime unchanged at 23:24:56 — _save_fleet's is_new_best=True path not triggered for either league). Pre-existing post-promotion-revert issue (ODIN's organic champion writes get reverted on next push since file is git-tracked) is OUT OF SCOPE; needs separate session to gitignore research/*/best_strategy.yaml + add seed_strategy.yaml fork-bootstrap shim. Commits: 76fe811 (placeholder fix), this memory.
