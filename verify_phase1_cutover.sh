#!/bin/bash
# Phase-1 fixed-sizing cutover verification — runs once via 'at' scheduler
# Writes result to syn_inbox.jsonl (info=clean, error=problem → sys_heartbeat → Telegram)
set -u
WS=/root/.openclaw/workspace
INBOX=$WS/syn_inbox.jsonl
TS=$(date -u +%Y-%m-%dT%H:%M)
CUTOVER_EPOCH=$(date -u -d '2026-04-24 08:55:00' +%s)

problems=()
not_rotated=()
verified=()

check_portfolio_meta() {
  local league=$1
  local active_dir=$2
  local newest=$(ls -1t "$active_dir" 2>/dev/null | head -1)
  if [ -z "$newest" ]; then
    problems+=("$league: no active sprint dir under $active_dir")
    return
  fi
  local sprint_dir="$active_dir/$newest"
  local meta="$sprint_dir/meta.json"
  local start_epoch
  start_epoch=$(python3 -c "import json,datetime as d; m=json.load(open('$meta')); print(int(d.datetime.fromisoformat(m['started_at'].replace('Z','+00:00')).timestamp()))" 2>/dev/null || echo 0)
  if [ "$start_epoch" -le "$CUTOVER_EPOCH" ]; then
    not_rotated+=("$league: $newest (pre-cutover, still running)")
    return
  fi
  local has_meta_flag
  has_meta_flag=$(python3 -c "import json; m=json.load(open('$meta')); print(m.get('fixed_sizing', False))" 2>/dev/null)
  local sample_port
  sample_port=$(ls -1 "$sprint_dir"/portfolio-*.json 2>/dev/null | head -1)
  local has_port_flag=False
  if [ -n "$sample_port" ]; then
    has_port_flag=$(python3 -c "import json; p=json.load(open('$sample_port')); print(p.get('fixed_sizing', False))" 2>/dev/null)
  fi
  if [ "$has_meta_flag" = "True" ] && [ "$has_port_flag" = "True" ]; then
    verified+=("$league ($newest)")
  else
    problems+=("$league: $newest rotated post-cutover but fixed_sizing missing (meta=$has_meta_flag port=$has_port_flag)")
  fi
}

check_portfolio_meta day            "$WS/competition/active"
check_portfolio_meta swing          "$WS/competition/swing/active"
check_portfolio_meta futures_day    "$WS/competition/futures_day/active"
check_portfolio_meta futures_swing  "$WS/competition/futures_swing/active"

# Polymarket — check auto_state.json top-level bot
pm_sprint=$(python3 -c "import json; s=json.load(open('$WS/competition/polymarket/auto_state.json')); print(s.get('sprint_id',''), s.get('sprint_started_at',''))" 2>/dev/null)
pm_start_epoch=$(python3 -c "import json,datetime as d; s=json.load(open('$WS/competition/polymarket/auto_state.json')); print(int(d.datetime.fromisoformat(s['sprint_started_at'].replace('Z','+00:00')).timestamp()))" 2>/dev/null || echo 0)
if [ "$pm_start_epoch" -le "$CUTOVER_EPOCH" ]; then
  not_rotated+=("polymarket: $pm_sprint (pre-cutover, still running)")
else
  pm_flag=$(python3 -c "import json; s=json.load(open('$WS/competition/polymarket/auto_state.json')); print(all(b.get('fixed_sizing', False) for b in s.get('bots',[])))" 2>/dev/null)
  if [ "$pm_flag" = "True" ]; then
    verified+=("polymarket ($pm_sprint)")
  else
    problems+=("polymarket: $pm_sprint rotated post-cutover but fixed_sizing missing from bots")
  fi
fi

# ODIN research tracebacks since cutover
odin_errors=$(grep -l -E 'Traceback|Exception' $WS/research/{day,futures_day,swing,futures_swing}/*.log 2>/dev/null | while read f; do
  newest_err_epoch=$(stat -c %Y "$f")
  if [ "$newest_err_epoch" -gt "$CUTOVER_EPOCH" ]; then echo "$f"; fi
done | head -5)

if [ -n "$odin_errors" ]; then
  problems+=("ODIN backtest errors found in: $(echo $odin_errors | tr '\n' ' ')")
fi

# Emit to syn_inbox
if [ ${#problems[@]} -eq 0 ]; then
  summary="phase-1 cutover verified: ${verified[*]:-none yet rotated}"
  if [ ${#not_rotated[@]} -gt 0 ]; then summary+=" | pending rotation: ${not_rotated[*]}"; fi
  python3 -c "import json; open('$INBOX','a').write(json.dumps({'ts':'$TS','source':'phase1_verify','severity':'info','msg':'[SYN/phase1_verify] $summary'})+chr(10))"
else
  details=$(printf '%s; ' "${problems[@]}")
  python3 -c "import json; open('$INBOX','a').write(json.dumps({'ts':'$TS','source':'phase1_verify','severity':'error','msg':'[SYN/phase1_verify] cutover problems: $details'})+chr(10))"
fi
