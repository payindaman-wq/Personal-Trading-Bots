#!/usr/bin/env python3
"""Generalized head-of-TSV backfill from researcher.log.

Recovers generations that are missing from the HEAD of a league's
results.tsv (i.e., gens below the current min-gen in the TSV) by parsing
the researcher.log for that league.

Usage:
    backfill_odin_tsv_general.py --league <day|futures_day|swing|futures_swing>
                                 [--gap-start N] [--gap-end N] [--dry-run]

If --gap-start/--gap-end are omitted, backfills [1, min_tsv_gen - 1].
"""
import argparse, re, shutil, sys
from datetime import datetime, timedelta

RESEARCH = "/root/.openclaw/workspace/research"

GEN_RE = re.compile(r'^\[(\d{2}):(\d{2}):(\d{2})\]\s+Gen\s+(\d+)\s+\|\s+best=(-?[\d.]+)\s+\|\s+stall=\d+\s+\|\s+(\S+)\s+\|\s+(.*)$')


def parse_rest(rest):
    m = re.search(r'\*\*\* NEW BEST: adj=-?[\d.]+ sharpe=(-?[\d.]+) win=([\d.]+)% pnl=(-?[\d.]+)% trades=(\d+)', rest)
    if m:
        return "new_best", float(m.group(1)), float(m.group(2)), float(m.group(3)), int(m.group(4))
    m = re.search(r'POISON_FP: sharpe=(-?[\d.]+)', rest)
    if m:
        return "poison_reject", float(m.group(1)), 0.0, 0.0, 0
    m = re.search(r'sharpe=(-?[\d.]+)\s+win=([\d.]+)%\s+trades=(\d+)\s+\[disc\]', rest)
    if m:
        return "discarded", float(m.group(1)), float(m.group(2)), 0.0, int(m.group(3))
    m = re.search(r'sharpe=(-?[\d.]+)\s+trades=(\d+)\s+\[low_trades\]', rest)
    if m:
        return "low_trades", float(m.group(1)), 0.0, 0.0, int(m.group(2))
    m = re.search(r'sharpe=(-?[\d.]+)\s+\[new_elite\]', rest)
    if m:
        return "new_elite", float(m.group(1)), 0.0, 0.0, 0
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--league", required=True)
    ap.add_argument("--gap-start", type=int, default=None)
    ap.add_argument("--gap-end", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    LOG = f"{RESEARCH}/{args.league}/researcher.log"
    TSV = f"{RESEARCH}/{args.league}/results.tsv"
    BAK = TSV + ".pre_backfill_" + datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    anchors = {}
    with open(TSV) as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if len(parts) >= 8 and parts[0].isdigit():
                try:
                    anchors[int(parts[0])] = datetime.strptime(parts[7], '%Y-%m-%dT%H:%M')
                except ValueError:
                    pass
    if not anchors:
        sys.exit(f"no anchor gens in {TSV}")

    min_tsv = min(anchors)
    gap_start = args.gap_start if args.gap_start is not None else 1
    gap_end = args.gap_end if args.gap_end is not None else min_tsv - 1
    if gap_end < gap_start:
        sys.exit(f"no gap to fill: tsv min={min_tsv}, requested [{gap_start},{gap_end}]")
    print(f"[backfill:{args.league}] gap=[{gap_start},{gap_end}] (tsv min_gen={min_tsv})")

    entries = []
    date_offset = 0
    prev_secs = -1
    with open(LOG) as f:
        for raw in f:
            m = GEN_RE.match(raw.rstrip('\n'))
            if not m:
                continue
            hh, mm, ss = int(m.group(1)), int(m.group(2)), int(m.group(3))
            gen = int(m.group(4))
            mutation = m.group(6)
            rest = m.group(7)
            secs = hh*3600 + mm*60 + ss
            if prev_secs != -1 and secs + 3600 < prev_secs:
                date_offset += 1
            prev_secs = secs
            parsed = parse_rest(rest)
            if not parsed:
                continue
            status, sharpe, win, pnl, trades = parsed
            entries.append({
                "gen": gen, "hh": hh, "mm": mm, "ss": ss,
                "date_offset": date_offset, "status": status,
                "sharpe": sharpe, "win": win, "pnl": pnl, "trades": trades,
                "mutation": mutation,
            })
    if not entries:
        sys.exit("no log entries parsed")

    base_date = None
    for e in entries:
        if e["gen"] in anchors:
            anchor_ts = anchors[e["gen"]]
            base_date = anchor_ts.replace(hour=0, minute=0, second=0) - timedelta(days=e["date_offset"])
            break
    if base_date is None:
        sys.exit("no anchor gen found in both TSV and log — cannot align timestamps")
    print(f"[backfill:{args.league}] base_date={base_date.date()}, {len(entries)} log entries parsed")

    gap = {}
    for e in entries:
        if gap_start <= e["gen"] <= gap_end:
            gap[e["gen"]] = e
    print(f"[backfill:{args.league}] {len(gap)} gap gens recovered from log")

    new_rows = []
    for gen in sorted(gap.keys()):
        e = gap[gen]
        dt = base_date + timedelta(days=e["date_offset"], hours=e["hh"], minutes=e["mm"], seconds=e["ss"])
        ts_str = dt.strftime('%Y-%m-%dT%H:%M')
        desc = f"{e['mutation']} (log backfill)"
        row = f"{gen}\t{e['sharpe']:.4f}\t{e['win']:.1f}\t{e['pnl']:.2f}\t{e['trades']}\t{e['status']}\t{desc}\t{ts_str}\n"
        new_rows.append((gen, row))

    with open(TSV) as f:
        existing = f.readlines()
    header = existing[0]
    body = existing[1:]
    parsed_body = []
    for line in body:
        parts = line.split('\t')
        if len(parts) >= 1 and parts[0].isdigit():
            parsed_body.append((int(parts[0]), line))
        else:
            parsed_body.append((-1, line))

    merged = {g: l for g, l in parsed_body if g >= 0}
    added = 0
    for g, l in new_rows:
        if g not in merged:
            merged[g] = l
            added += 1
    misc = [l for g, l in parsed_body if g < 0]

    if args.dry_run:
        print(f"[backfill:{args.league}] DRY RUN — would add {added} new rows, total would be {len(merged)}")
        return

    shutil.copy2(TSV, BAK)
    print(f"[backfill:{args.league}] backup: {BAK}")
    with open(TSV, 'w') as f:
        f.write(header)
        for g in sorted(merged.keys()):
            f.write(merged[g])
        for l in misc:
            f.write(l)
    print(f"[backfill:{args.league}] wrote {len(merged)} total rows (+{added} new)")


if __name__ == "__main__":
    main()
