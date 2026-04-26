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
