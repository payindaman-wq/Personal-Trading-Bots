# Cycle/Sprint Ledger Redesign — Design Spec

## Context
Cycle and sprint counting has produced the most frequent class of bugs in the
system (Chris's assessment 2026-04-24). Today's Futures Day C3S0 incident is the
latest: LOKI inline-advance wiped `cycle_state.json` while a sprint was already
live, leaving sprints[]=[] and sprint_in_cycle=0 even though the active sprint
was logically cycle 3 sprint 1. SYN's `sprint_integrity_check` did not catch
it because the wipe is *internally consistent* (0 == len([])).

## Root cause (generalized)
`cycle_state.json` is a mutable scoreboard with ~8 distinct writers:
- `futures_day_restart.py`, `futures_swing_restart.py`
- `day_daily_restart.py`
- `swing_competition_tick.py`
- `cycle_advance.py`, `swing_cycle_advance.py`, `polymarket_cycle_advance.py`
- `research/loki.py` (inline advance branch)

Any one of them can desync the counter. `sprint_in_cycle` is a stored field
instead of a derivable function, so single-writer bugs produce silent
divergence.

## Proposed design: append-only event ledger + derived projection

### Ledger format
Per-league append-only JSONL at `competition/<league>/cycle_events.jsonl`:

    {"ts":"2026-04-23T09:00:00+00:00","league":"futures_day","type":"sprint_started","comp_id":"fut-day-20260423-0900","cycle":2}
    {"ts":"2026-04-24T07:03:00+00:00","league":"futures_day","type":"cycle_advanced","from":2,"to":3}
    {"ts":"2026-04-24T09:00:00+00:00","league":"futures_day","type":"sprint_archived","comp_id":"fut-day-20260423-0900","cycle":2}

Event types (exhaustive):
- `sprint_started` — new comp_id created
- `sprint_archived` — moved to results/ with score file
- `cycle_completed` — reached sprints_per_cycle (await LOKI review)
- `cycle_advanced` — LOKI or advance script bumped cycle N -> N+1

### Reducer
Single module `cycle_ledger.py` exposes:
- `emit(league, event_type, **payload)` — appends to ledger with server time
- `materialize(league) -> dict` — folds ledger into `cycle_state.json` shape
- `write_state(league)` — calls `materialize` and overwrites `cycle_state.json`

Reducer rules:
- `cycle` = most recent `cycle_advanced`.to (or 1 if none)
- `sprint_in_cycle` = count of `sprint_started` events AFTER that cycle_advanced ts (or all if none)
- `sprints` = list of those sprint_started comp_ids in order
- `cycle_started_at` = ts of that cycle_advanced event (or ts of first sprint_started if none)
- `status` = "awaiting_review" if `sprint_in_cycle >= sprints_per_cycle` and no later `cycle_advanced`; else "active"

### Writer migration
Each writer is edited to:
1. Do its work (start a sprint, archive, etc.)
2. Call `cycle_ledger.emit(league, event_type, ...)` for the state change
3. Call `cycle_ledger.write_state(league)` to re-materialize

LOKI's inline advance becomes a single `emit(..., "cycle_advanced", from=N, to=N+1)` —
no direct `cs["sprints"] = []` mutation. The active sprint's prior
`sprint_started` event stays in the ledger; the reducer just counts forward
from the new cycle_advanced timestamp.

### SYN integration
`sprint_integrity_check.py` gains a three-way invariant check:
1. `cycle_state.json` (on-disk materialized view)
2. `cycle_ledger.materialize(league)` (re-derived from ledger)
3. Filesystem reality (active dirs + results score files)

Any two-way mismatch between (1)(2) => `state_stale` anomaly
(auto-fixable: re-run `write_state`).
Any two-way mismatch between (2)(3) => `ledger_reality_drift` anomaly
(needs human review — means a writer bypassed the ledger).

### One-time migration
`scripts/seed_cycle_ledger.py` reads each league's existing `cycle_state.json`
+ `results/` + archive to back-fill historical events. Produces one-shot ledger;
normal operation takes over after.

### Rollout
1. Ship `cycle_ledger.py` + `write_state` + `materialize` + seed script.
2. Run seed; verify `materialize(league) == on-disk cycle_state` for all 5 leagues.
3. Edit writers one at a time, verifying after each.
4. Ship SYN three-way check.
5. Mark direct `cycle_state.json` writes as deprecated; leave a warning if detected.

## Scope estimate
- ~600-900 LoC: `cycle_ledger.py` (~200), writer edits across 8 files (~300), SYN
  extension (~100), seed script (~200).
- Risk: moderate. All 5 leagues depend on cycle_state. Phased rollout + idempotent
  migration mitigate.
- Budget: zero Anthropic-API spend to implement (done in-conversation with Chris).

## Quick wins already shipped 2026-04-24 (pre-redesign)
- LOKI inline-advance seeds `sprints[]` with live active sprint instead of wiping
  (research/loki.py)
- SYN `cycle_state_wiped` anomaly when cycle>1 + sprints=[] + null started_at
  while active dir or recent score files exist
- SYN `undercount_vs_results` for futures leagues: score files dated >
  cycle_started_at + 5min buffer vs len(sprints)
- Manual repair of Futures Day cycle_state to C3S1

## Status
- Design: draft (this doc)
- Implementation: NOT STARTED — pick up next session at zero API cost
- Owner: Chris + Claude (in-conversation)
