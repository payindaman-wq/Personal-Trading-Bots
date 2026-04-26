#!/usr/bin/env python3
"""
data_integrity_check.py - per-league write-path audit (SYN/data_integrity).

Compares gen_state.json.gen vs max(results.tsv.gen) per league. If drift
exceeds DRIFT_THRESHOLD the write path (odin_researcher_v2.log_result) is
silently failing - gen counter advances but rows don't land in the TSV.
This is the 2026-04-19 futures write-gap pattern (gen climbed 5027->9087
while results.tsv got ~0 rows for 5 days).

Writes source=data_integrity to syn_inbox.jsonl (gateway allowlist excludes
this source per feedback_syn_telegram_chris_action_only - VIDAR routes).
Dedups via competition/data_integrity_state.json: alerts once per league
per drift event; posts a RECOVERED info when drift returns below threshold.
"""
import json
import os
from datetime import datetime, timezone

WORKSPACE = "/root/.openclaw/workspace"
LEAGUES = ["day", "swing", "futures_day", "futures_swing", "pm"]
DRIFT_THRESHOLD = 100
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"
STATE_FILE = f"{WORKSPACE}/competition/data_integrity_state.json"


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, indent=2)
    os.replace(tmp, STATE_FILE)


def max_results_gen(tsv_path):
    if not os.path.isfile(tsv_path):
        return None
    max_gen = -1
    with open(tsv_path) as f:
        next(f, None)
        for line in f:
            parts = line.split("\t", 1)
            if not parts:
                continue
            try:
                g = int(parts[0])
                if g > max_gen:
                    max_gen = g
            except ValueError:
                continue
    return max_gen if max_gen >= 0 else None


def inbox_write(msg, severity="error"):
    rec = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "source":   "data_integrity",
        "severity": severity,
        "msg":      msg[:2000],
    }
    with open(INBOX, "a") as f:
        f.write(json.dumps(rec) + "\n")


def check_league(league):
    gs_path = f"{WORKSPACE}/research/{league}/gen_state.json"
    tsv_path = f"{WORKSPACE}/research/{league}/results.tsv"
    if not os.path.isfile(gs_path):
        return None
    try:
        gs = json.load(open(gs_path))
    except Exception:
        return {"state_gen": None, "tsv_gen": None, "drift": None}
    state_gen = gs.get("gen")
    tsv_gen = max_results_gen(tsv_path)
    if state_gen is None or tsv_gen is None:
        return {"state_gen": state_gen, "tsv_gen": tsv_gen, "drift": None}
    return {"state_gen": state_gen, "tsv_gen": tsv_gen, "drift": state_gen - tsv_gen}


def main():
    state = load_state()
    summary = []
    for league in LEAGUES:
        r = check_league(league)
        if r is None:
            summary.append(f"{league}:skip")
            continue
        if r.get("drift") is None:
            summary.append(f"{league}:partial")
            continue
        drift = r["drift"]
        prev = state.get(league, {"alerted": False})
        if drift > DRIFT_THRESHOLD:
            summary.append(f"{league}:DRIFT={drift}")
            if not prev.get("alerted"):
                inbox_write(
                    f"[OPS/data_integrity] write-path drift on {league}: "
                    f"gen_state.gen={r['state_gen']} vs max(results.tsv.gen)={r['tsv_gen']} "
                    f"(drift={drift} > threshold={DRIFT_THRESHOLD}). "
                    f"Same pattern as the 2026-04-19 futures write-gap incident.",
                    severity="error",
                )
                state[league] = {"alerted": True, "since": datetime.now(timezone.utc).isoformat(), "drift": drift}
            else:
                state[league]["drift"] = drift
        else:
            summary.append(f"{league}:ok({drift})")
            if prev.get("alerted"):
                inbox_write(
                    f"[OPS/data_integrity] {league} write-path RECOVERED: drift={drift} <= {DRIFT_THRESHOLD}.",
                    severity="info",
                )
                state[league] = {"alerted": False, "recovered": datetime.now(timezone.utc).isoformat(), "drift": drift}
    save_state(state)
    ts = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    print(f"[{ts}] " + " | ".join(summary))


if __name__ == "__main__":
    main()
