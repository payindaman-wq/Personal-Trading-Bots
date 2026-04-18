#!/usr/bin/env python3
"""One-off: backfill missing gens 3652-5166 in futures_day/results.tsv from researcher.log."""
import re, shutil, sys
from datetime import datetime, timedelta

LOG  = "/root/.openclaw/workspace/research/futures_day/researcher.log"
TSV  = "/root/.openclaw/workspace/research/futures_day/results.tsv"
BAK  = TSV + ".pre_backfill_20260418"

GAP_START = 3652
GAP_END   = 5166

GEN_RE = re.compile(r'^\[(\d{2}):(\d{2}):(\d{2})\]\s+Gen\s+(\d+)\s+\|\s+best=(-?[\d.]+)\s+\|\s+stall=\d+\s+\|\s+(\S+)\s+\|\s+(.*)$')

def parse_rest(rest):
    """Return (status, sharpe, win_rate, pnl_pct, trades)."""
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

# --- load anchors from existing tsv ---
anchors = {}  # gen -> datetime
with open(TSV) as f:
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) >= 8 and parts[0].isdigit():
            try:
                anchors[int(parts[0])] = datetime.strptime(parts[7], '%Y-%m-%dT%H:%M')
            except ValueError:
                pass

# --- parse log, assign date offsets by midnight rollover ---
entries = []  # list of dicts
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

# --- anchor date: find a gen present in both ---
base_date = None
for e in entries:
    if e["gen"] in anchors:
        anchor_ts = anchors[e["gen"]]
        entry_day_midnight = anchor_ts.replace(hour=0, minute=0, second=0) - timedelta(days=e["date_offset"])
        base_date = entry_day_midnight
        break

if base_date is None:
    sys.exit("no anchor gen found")

print(f"[backfill] base_date={base_date.date()}, {len(entries)} log entries")

# --- filter to gap gens, dedup (keep last occurrence) ---
gap = {}
for e in entries:
    if GAP_START <= e["gen"] <= GAP_END:
        gap[e["gen"]] = e

print(f"[backfill] {len(gap)} gap gens recovered")

# --- build tsv rows ---
new_rows = []
for gen in sorted(gap.keys()):
    e = gap[gen]
    dt = base_date + timedelta(days=e["date_offset"], hours=e["hh"], minutes=e["mm"], seconds=e["ss"])
    ts_str = dt.strftime('%Y-%m-%dT%H:%M')
    desc = f"{e['mutation']} (log backfill)"
    row = f"{gen}\t{e['sharpe']:.4f}\t{e['win']:.1f}\t{e['pnl']:.2f}\t{e['trades']}\t{e['status']}\t{desc}\t{ts_str}\n"
    new_rows.append((gen, row))

# --- merge with existing tsv ---
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
for g, l in new_rows:
    if g not in merged:
        merged[g] = l

# Preserve rows without valid gen (edge)
misc = [l for g, l in parsed_body if g < 0]

shutil.copy2(TSV, BAK)
print(f"[backfill] backup: {BAK}")

with open(TSV, 'w') as f:
    f.write(header)
    for g in sorted(merged.keys()):
        f.write(merged[g])
    for l in misc:
        f.write(l)

print(f"[backfill] wrote {len(merged)} total rows")
