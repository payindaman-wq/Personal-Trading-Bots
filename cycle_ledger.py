"""
cycle_ledger.py — append-only event ledger for cycle/sprint state.

Phase 1 (shadow mode): writers call emit() AFTER their existing cycle_state.json
writes so the ledger tracks events passively. materialize() can re-derive
cycle_state from the ledger. SYN compares the two and flags drift.

Phase 2 (future): promote to source-of-truth — writers call emit() then
write_state() which overwrites cycle_state.json from materialize().

Event types:
- cycle_baseline     — seed event from one-shot migration (captures prior state)
- sprint_started     — new comp_id created
- sprint_archived    — sprint moved to results with score
- cycle_completed    — reached sprints_per_cycle (awaiting_review)
- cycle_advanced     — cycle N -> N+1

Ledger location: competition/<league>/cycle_events.jsonl (append-only JSONL).
"""
import json
import os
from datetime import datetime, timezone
from typing import Optional

WORKSPACE = "/root/.openclaw/workspace"

# Per-league paths — keep consistent with sprint_integrity_check.py LEAGUES config.
LEAGUE_PATHS = {
    "day": {
        "ledger":      f"{WORKSPACE}/competition/cycle_events.jsonl",
        "cycle_state": f"{WORKSPACE}/competition/cycle_state.json",
    },
    "swing": {
        "ledger":      f"{WORKSPACE}/competition/swing/cycle_events.jsonl",
        "cycle_state": f"{WORKSPACE}/competition/swing/swing_cycle_state.json",
    },
    "futures_day": {
        "ledger":      f"{WORKSPACE}/competition/futures_day/cycle_events.jsonl",
        "cycle_state": f"{WORKSPACE}/competition/futures_day/cycle_state.json",
    },
    "futures_swing": {
        "ledger":      f"{WORKSPACE}/competition/futures_swing/cycle_events.jsonl",
        "cycle_state": f"{WORKSPACE}/competition/futures_swing/cycle_state.json",
    },
    "polymarket": {
        "ledger":      f"{WORKSPACE}/competition/polymarket/cycle_events.jsonl",
        "cycle_state": f"{WORKSPACE}/competition/polymarket/polymarket_cycle_state.json",
    },
}


def _ledger_path(league: str) -> str:
    if league not in LEAGUE_PATHS:
        raise ValueError(f"unknown league: {league}")
    return LEAGUE_PATHS[league]["ledger"]


def _cycle_state_path(league: str) -> str:
    if league not in LEAGUE_PATHS:
        raise ValueError(f"unknown league: {league}")
    return LEAGUE_PATHS[league]["cycle_state"]


def emit(league: str, event_type: str, ts: Optional[str] = None, **payload) -> dict:
    """Append one event to the league's ledger. Returns the event dict."""
    if league not in LEAGUE_PATHS:
        raise ValueError(f"unknown league: {league}")
    valid_types = {"cycle_baseline", "sprint_started", "sprint_archived",
                   "cycle_completed", "cycle_advanced"}
    if event_type not in valid_types:
        raise ValueError(f"unknown event_type: {event_type}")

    event = {
        "ts":       ts or datetime.now(timezone.utc).isoformat(),
        "league":   league,
        "type":     event_type,
    }
    event.update(payload)

    path = _ledger_path(league)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event


def read_ledger(league: str) -> list:
    """Return all events in league's ledger, chronological order."""
    path = _ledger_path(league)
    if not os.path.isfile(path):
        return []
    events = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except Exception:
                pass
    return events


def materialize(league: str) -> dict:
    """Fold ledger events into cycle_state.json-shape dict.

    Rules:
    - Start from most recent `cycle_baseline` event (captures sprints_per_cycle + any
      existing sprints[] + cycle at seed time).
    - Walk forward applying each event:
      - cycle_advanced: cycle=to, sprints=[], sprint_in_cycle=0, cycle_started_at=ts, status=active
      - sprint_started: append comp_id to sprints, inc sprint_in_cycle. If first
        sprint of the cycle and cycle_started_at is None, set it to this event's ts.
      - sprint_archived: no state change (tracked for audit; the archive is
        visible via filesystem and the sprint stays in sprints[] as part of this cycle).
      - cycle_completed: status=awaiting_review.
    """
    events = read_ledger(league)
    state = {
        "cycle": 1,
        "sprint_in_cycle": 0,
        "sprints_per_cycle": 7,  # overridden by baseline
        "status": "active",
        "cycle_started_at": None,
        "sprints": [],
    }
    # Find the most recent cycle_baseline as our starting point.
    baseline_idx = -1
    for i in range(len(events) - 1, -1, -1):
        if events[i].get("type") == "cycle_baseline":
            baseline_idx = i
            break
    if baseline_idx >= 0:
        b = events[baseline_idx]
        state["cycle"]             = b.get("cycle", 1)
        state["sprint_in_cycle"]   = b.get("sprint_in_cycle", 0)
        state["sprints_per_cycle"] = b.get("sprints_per_cycle", 7)
        state["status"]            = b.get("status", "active")
        state["cycle_started_at"]  = b.get("cycle_started_at")
        state["sprints"]           = list(b.get("sprints", []))
        walk = events[baseline_idx + 1:]
    else:
        walk = events

    for e in walk:
        t = e.get("type")
        if t == "cycle_advanced":
            state["cycle"]            = e.get("to", state["cycle"] + 1)
            state["sprints"]          = []
            state["sprint_in_cycle"]  = 0
            state["cycle_started_at"] = e.get("ts")
            state["status"]           = "active"
        elif t == "sprint_started":
            cid = e.get("comp_id")
            if cid and cid not in state["sprints"]:
                state["sprints"].append(cid)
            state["sprint_in_cycle"] = len(state["sprints"])
            if state["cycle_started_at"] is None:
                state["cycle_started_at"] = e.get("ts")
        elif t == "sprint_archived":
            # Audit-only in this model; presence in sprints[] is what counts.
            pass
        elif t == "cycle_completed":
            state["status"] = "awaiting_review"
        # cycle_baseline beyond the starting one is treated as idempotent re-seed
        elif t == "cycle_baseline":
            state["cycle"]             = e.get("cycle", state["cycle"])
            state["sprint_in_cycle"]   = e.get("sprint_in_cycle", state["sprint_in_cycle"])
            state["sprints_per_cycle"] = e.get("sprints_per_cycle", state["sprints_per_cycle"])
            state["status"]            = e.get("status", state["status"])
            state["cycle_started_at"]  = e.get("cycle_started_at", state["cycle_started_at"])
            state["sprints"]           = list(e.get("sprints", state["sprints"]))

    return state


def current_on_disk(league: str) -> dict:
    """Load the authoritative on-disk cycle_state.json for comparison."""
    path = _cycle_state_path(league)
    if not os.path.isfile(path):
        return {}
    with open(path) as f:
        return json.load(f)


def drift(league: str) -> dict:
    """Compare materialized-from-ledger vs. on-disk cycle_state.
    Returns dict of field-name -> (ledger_value, disk_value) for mismatches.
    Empty dict = no drift."""
    want = materialize(league)
    have = current_on_disk(league)
    mismatches = {}
    for field in ("cycle", "sprint_in_cycle", "sprints_per_cycle", "status",
                  "cycle_started_at", "sprints"):
        if want.get(field) != have.get(field):
            mismatches[field] = (want.get(field), have.get(field))
    return mismatches


def write_state(league: str) -> dict:
    """Phase-2 promotion hook — not used in shadow mode. Writes materialized
    state over cycle_state.json. Callers in Phase 2 will use this after emit()."""
    state = materialize(league)
    path = _cycle_state_path(league)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(state, f, indent=2)
    return state
