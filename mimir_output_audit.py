#!/usr/bin/env python3
"""
mimir_output_audit.py - fact-check MIMIR analyses (SYN/mimir_audit).

Reads new entries from research/mimir_log.jsonl (byte-offset tracked),
extracts (gen, Sharpe) citation pairs, and verifies they appear in the
corresponding league's results.tsv.

Catches the 2026-04-19 fabrication pattern: when MIMIR is served stale or
sparse data, it invents per-gen rows (e.g. "Sharpe 2.3680 at gen 9000")
that LOKI may act on. Only PAIRED citations (gen + sharpe in close
proximity) are flagged, to cut false positives from freeform prose.

Writes source=mimir_audit to syn_inbox.jsonl (gateway allowlist excludes
this source - VIDAR consumer routes). State in
competition/mimir_audit_state.json.
"""
import json
import os
import re
from datetime import datetime, timezone

WORKSPACE = "/root/.openclaw/workspace"
MIMIR_LOG = f"{WORKSPACE}/research/mimir_log.jsonl"
INBOX = f"{WORKSPACE}/syn_inbox.jsonl"
STATE_FILE = f"{WORKSPACE}/competition/mimir_audit_state.json"

SHARPE_TOLERANCE = 0.1
MAX_FINDINGS_PER_RUN = 5
MIN_CITED_GEN = 100

GEN_RE = re.compile(r"\b(?:gen(?:eration)?s?)\s+(\d+)", re.IGNORECASE)
SHARPE_RE = re.compile(r"Sharpe[\s=:]*(-?\d+\.\d+)", re.IGNORECASE)


def load_state():
    if os.path.isfile(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except Exception:
            pass
    return {"offset": 0, "last_audit_ts": None}


def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, indent=2)
    os.replace(tmp, STATE_FILE)


def load_results_map(league):
    path = f"{WORKSPACE}/research/{league}/results.tsv"
    if not os.path.isfile(path):
        return None
    out = {}
    with open(path) as f:
        header = next(f, None)
        if not header:
            return {}
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            try:
                g = int(parts[0])
                s = float(parts[1])
            except ValueError:
                continue
            out[g] = s
    return out


def inbox_write(msg, severity="warning"):
    rec = {
        "ts":       datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "source":   "mimir_audit",
        "severity": severity,
        "msg":      msg[:2000],
    }
    with open(INBOX, "a") as f:
        f.write(json.dumps(rec) + "\n")


def extract_paired_cites(text):
    """Yield (gen, sharpe) for each gen citation that has a Sharpe within
    60 chars (before or after). Conservative to avoid freeform-prose FPs."""
    paired = []
    for gm in GEN_RE.finditer(text):
        try:
            g = int(gm.group(1))
        except ValueError:
            continue
        if g < MIN_CITED_GEN:
            continue
        start = max(0, gm.start() - 60)
        end   = min(len(text), gm.end() + 60)
        window = text[start:end]
        nearest = None
        nearest_dist = 999
        for sm in SHARPE_RE.finditer(window):
            win_offset = start + sm.start()
            dist = abs(win_offset - gm.start())
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = float(sm.group(1))
        if nearest is not None:
            paired.append((g, nearest))
    return paired


def audit_entry(entry, results_cache):
    league = entry.get("league")
    analysis = entry.get("analysis", "")
    gen_at_fire = entry.get("generation")
    if not league or not analysis:
        return []
    if league not in results_cache:
        rmap = load_results_map(league)
        results_cache[league] = {
            "map": rmap,
            "min_gen": min(rmap.keys()) if rmap else None,
        }
    cache = results_cache.get(league)
    rmap = cache["map"] if cache else None
    if not rmap:
        return []
    min_tsv_gen = cache["min_gen"]
    findings = []
    seen = set()
    for g, cited_sharpe in extract_paired_cites(analysis):
        if (g, cited_sharpe) in seen:
            continue
        seen.add((g, cited_sharpe))
        if gen_at_fire and g > gen_at_fire:
            continue
        if min_tsv_gen is not None and g < min_tsv_gen:
            continue
        if g not in rmap:
            findings.append(f"gen {g} (cited Sharpe={cited_sharpe:.4f}) NOT IN results.tsv")
            continue
        actual = rmap[g]
        if abs(actual - cited_sharpe) > SHARPE_TOLERANCE:
            findings.append(
                f"gen {g}: cited={cited_sharpe:.4f} actual={actual:.4f} "
                f"diff={abs(actual-cited_sharpe):.4f}"
            )
    return findings


def main():
    state = load_state()
    offset = state.get("offset", 0)
    if not os.path.isfile(MIMIR_LOG):
        print(f"[mimir_audit] no log at {MIMIR_LOG}")
        return

    size = os.path.getsize(MIMIR_LOG)
    if offset > size:
        offset = 0

    findings_total = []
    entries_scanned = 0
    results_cache = {}

    with open(MIMIR_LOG) as f:
        f.seek(offset)
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries_scanned += 1
            try:
                entry = json.loads(line)
            except Exception:
                continue
            findings = audit_entry(entry, results_cache)
            if findings:
                findings_total.append({
                    "league": entry.get("league"),
                    "generation": entry.get("generation"),
                    "mimir_ts": entry.get("ts"),
                    "findings": findings,
                })
        offset = f.tell()

    state["offset"] = offset
    state["last_audit_ts"] = datetime.now(timezone.utc).isoformat()

    if findings_total:
        summary = []
        for fr in findings_total[:MAX_FINDINGS_PER_RUN]:
            summary.append(
                f"- {fr['league']} @ gen {fr['generation']} ({fr['mimir_ts']}): "
                + "; ".join(fr['findings'][:3])
            )
        extra = len(findings_total) - MAX_FINDINGS_PER_RUN
        trail = f"\n(+{extra} more analyses with findings)" if extra > 0 else ""
        msg = (
            f"[OPS/mimir_audit] {len(findings_total)} MIMIR analyses have "
            f"unverifiable (gen, Sharpe) citations (scanned={entries_scanned}):\n"
            + "\n".join(summary)
            + trail
            + "\nReview: research/mimir_log.jsonl"
        )
        inbox_write(msg, severity="warning")

    save_state(state)
    ts = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    print(f"[{ts}] scanned={entries_scanned} findings={len(findings_total)} offset={offset}")


if __name__ == "__main__":
    main()
