#!/bin/bash
# Deferred work order (set 2026-04-19): recompute brandr regression stats
# once ~4 more sprints of data are in, then decide whether to escalate to MIMIR.
# Baseline was cycle 1 pinned 2026-04-18 15:44 PST. Initial signal: n=6, z=-4.34.
set -u
WORKSPACE=/root/.openclaw/workspace
QUEUE=$WORKSPACE/research/syn_mimir_queue.jsonl
LOG=$WORKSPACE/research/brandr_recheck_$(date -u +%F).log
exec >>"$LOG" 2>&1
echo "=== brandr regression recheck $(date -u -Iseconds) ==="

python3 - <<'PY'
import json, os, glob, statistics, sys, datetime, pathlib
WORKSPACE = "/root/.openclaw/workspace"
QUEUE = f"{WORKSPACE}/research/syn_mimir_queue.jsonl"
BOT = "brandr"
LEAGUE = "futures_day"

results_dir = f"{WORKSPACE}/competition/{LEAGUE}/results"
score_files = sorted(glob.glob(f"{results_dir}/*_score.json"))
returns = []
for sf in score_files:
    try:
        d = json.load(open(sf))
        for row in d.get("scores", []):
            if row.get("bot") == BOT:
                r = row.get("total_pnl_pct")
                if isinstance(r, (int, float)):
                    returns.append((os.path.basename(sf), r))
                break
    except Exception as e:
        print(f"  parse_err {sf}: {e}")

n = len(returns)
print(f"n={n} brandr per-sprint returns:")
for name, r in returns[-12:]:
    print(f"  {name}  {r}")

if n < 10:
    print(f"insufficient data (n={n} < 10). No escalation queued.")
    sys.exit(0)

last10 = [r for _, r in returns[-10:]]
mean = statistics.mean(last10)
stdev = statistics.pstdev(last10) if len(last10) > 1 else 0
expected = -0.175  # per-sprint from backtest
z = (mean - expected) / stdev if stdev > 0 else 0

print(f"last-10 mean={mean:.3f} stdev={stdev:.3f} z={z:.2f}")

if z > -3 or mean > -2:
    print("regression resolved or within tolerance. No escalation queued.")
    sys.exit(0)

msg = (f"[SYN/regression] brandr (futures_day) regression persists after deferred recheck. "
       f"n={n}, last-10 mean={mean:.3f}%/sprint (expected {expected}), z={z:.2f}. "
       f"Baseline cycle 1 pinned 2026-04-18 15:44 PST.")
entry = {
    "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M"),
    "source": "syn_regression_recheck",
    "league": LEAGUE,
    "error_type": "regression_persistent",
    "message": msg,
    "context": {"bot": BOT, "n": n, "last10_mean": mean, "last10_stdev": stdev,
                "z": z, "expected_per_sprint": expected,
                "returns_tail": [r for _, r in returns[-10:]]},
    "processed": False,
}
pathlib.Path(os.path.dirname(QUEUE)).mkdir(parents=True, exist_ok=True)
with open(QUEUE, "a") as f:
    f.write(json.dumps(entry) + "\n")
print(f"queued to syn_mimir_queue.jsonl: {msg}")
PY
echo "=== done ==="
