#!/usr/bin/env python3
"""
Patch odin_researcher_v2.py, odin_backtest.py, mimir.py, loki.py, and
weekly_league_restart.py to support futures_day and futures_swing leagues.
"""
import re

WORKSPACE = '/root/.openclaw/workspace'
RESEARCH  = WORKSPACE + '/research'


# ═══════════════════════════════════════════════════════════════
# 1. odin_researcher_v2.py
# ═══════════════════════════════════════════════════════════════
path = RESEARCH + '/odin_researcher_v2.py'
code = open(path).read()

# a) Add futures leagues to argparse choices
old_choices = 'choices=["day", "swing"]'
new_choices = 'choices=["day", "swing", "futures_day", "futures_swing"]'
assert old_choices in code, 'argparse choices not found'
code = code.replace(old_choices, new_choices)

# b) Add futures ranges after SWING_RANGES
old_ranges_end = (
    'SWING_RANGES = {\n'
    '    "take_profit_pct": (3.0, 12.0),\n'
    '    "stop_loss_pct": (2.0, 5.0),\n'
    '    "timeout_hours": (48, 240),\n'
    '    "size_pct": (15, 30),\n'
    '    "max_open": (1, 3),\n'
    '}'
)
new_ranges_end = (
    old_ranges_end + '\n'
    'FUTURES_DAY_RANGES = {\n'
    '    "take_profit_pct": (0.8, 5.0),\n'
    '    "stop_loss_pct":   (0.5, 3.0),\n'
    '    "timeout_minutes": (30, 480),\n'
    '    "size_pct":        (8, 20),\n'
    '    "max_open":        (1, 4),\n'
    '    "leverage":        (1.5, 3.0),\n'
    '}\n'
    'FUTURES_SWING_RANGES = {\n'
    '    "take_profit_pct": (3.0, 10.0),\n'
    '    "stop_loss_pct":   (1.5, 4.0),\n'
    '    "timeout_hours":   (48, 192),\n'
    '    "size_pct":        (10, 25),\n'
    '    "max_open":        (1, 3),\n'
    '    "leverage":        (1.5, 3.0),\n'
    '}'
)
assert old_ranges_end in code, 'SWING_RANGES not found'
code = code.replace(old_ranges_end, new_ranges_end)

# c) Update get_fleet_path for futures leagues
old_fleet = (
    'def get_fleet_path(league):\n'
    '    if league == "day":\n'
    '        return os.path.join(WORKSPACE, "fleet", "autobotday", "strategy.yaml")\n'
    '    elif league == "swing":\n'
    '        return os.path.join(WORKSPACE, "fleet", "swing", "autobotswing", "strategy.yaml")\n'
    '    return None'
)
new_fleet = (
    'def get_fleet_path(league):\n'
    '    if league == "day":\n'
    '        return os.path.join(WORKSPACE, "fleet", "autobotday", "strategy.yaml")\n'
    '    elif league == "swing":\n'
    '        return os.path.join(WORKSPACE, "fleet", "swing", "autobotswing", "strategy.yaml")\n'
    '    elif league == "futures_day":\n'
    '        return os.path.join(WORKSPACE, "fleet", "futures_day", "autobotdayfutures", "strategy.yaml")\n'
    '    elif league == "futures_swing":\n'
    '        return os.path.join(WORKSPACE, "fleet", "futures_swing", "autobotswingfutures", "strategy.yaml")\n'
    '    return None'
)
assert old_fleet in code, 'get_fleet_path not found'
code = code.replace(old_fleet, new_fleet)

# d) Update get_ranges for futures leagues
old_get_ranges = 'def get_ranges(league):\n    return DAY_RANGES if league == "day" else SWING_RANGES'
new_get_ranges = (
    'def get_ranges(league):\n'
    '    if league == "futures_day":   return FUTURES_DAY_RANGES\n'
    '    if league == "futures_swing": return FUTURES_SWING_RANGES\n'
    '    return DAY_RANGES if league == "day" else SWING_RANGES'
)
assert old_get_ranges in code, 'get_ranges not found'
code = code.replace(old_get_ranges, new_get_ranges)

# e) Update MIN_TRADES for futures leagues
old_min = 'MIN_TRADES = {"day": 250, "swing": 30}'
new_min = 'MIN_TRADES = {"day": 250, "swing": 30, "futures_day": 200, "futures_swing": 25}'
assert old_min in code, 'MIN_TRADES not found'
code = code.replace(old_min, new_min)

# f) Update timeout key logic for futures leagues
old_to_key1 = (
    '    to_key = "timeout_minutes" if league == "day" else "timeout_hours"\n'
    '    if to_key == "timeout_hours":'
)
new_to_key1 = (
    '    to_key = "timeout_minutes" if league in ("day", "futures_day") else "timeout_hours"\n'
    '    if to_key == "timeout_hours":'
)
if old_to_key1 in code:
    code = code.replace(old_to_key1, new_to_key1)

old_to_key2 = '    to_key = "timeout_minutes" if league == "day" else "timeout_hours"'
new_to_key2 = '    to_key = "timeout_minutes" if league in ("day", "futures_day") else "timeout_hours"'
code = code.replace(old_to_key2, new_to_key2)

# g) Update pause/stop defaults for futures leagues
old_pause = '            "pause_if_down_pct": 4 if league == "day" else 8,'
new_pause = '            "pause_if_down_pct": 5 if league in ("day", "futures_day") else 8,'
code = code.replace(old_pause, new_pause)

old_stop = '            "stop_if_down_pct": 10 if league == "day" else 18,'
new_stop = '            "stop_if_down_pct": 12 if league in ("day", "futures_day") else 18,'
code = code.replace(old_stop, new_stop)

# h) Update league_dir to handle underscore leagues (already works via os.path.join)
# Nothing needed — league_dir uses league string directly which is fine

open(path, 'w').write(code)
print('odin_researcher_v2.py patched')


# ═══════════════════════════════════════════════════════════════
# 2. odin_backtest.py — add futures mechanics
# ═══════════════════════════════════════════════════════════════
path = RESEARCH + '/odin_backtest.py'
code = open(path).read()

# a) Update run_backtest signature to handle futures leagues
old_interval = (
    '    interval_minutes = 5 if league == "day" else 60\n'
    '    vwap_window      = 288 if league == "day" else 24\n'
    '    interval_label   = "5m" if league == "day" else "1h"\n'
    '    max_history_min  = 10_200 if league == "swing" else 400'
)
new_interval = (
    '    is_futures       = league.startswith("futures_")\n'
    '    base_league      = "day" if "day" in league else "swing"\n'
    '    interval_minutes = 5 if base_league == "day" else 60\n'
    '    vwap_window      = 288 if base_league == "day" else 24\n'
    '    interval_label   = "5m" if base_league == "day" else "1h"\n'
    '    max_history_min  = 10_200 if base_league == "swing" else 400\n'
    '    leverage         = float(strategy.get("leverage", 1.0)) if is_futures else 1.0\n'
    '    FUNDING_RATE_8H  = 0.0001  # 0.01% per 8h default\n'
    '    funding_ticks    = (8 * 60) // interval_minutes  # ticks per 8h funding period\n'
    '    MAINTENANCE_MARGIN = 0.05\n'
    '    liq_threshold    = (1.0 / leverage) * (1 - MAINTENANCE_MARGIN) if is_futures else 999.0'
)
assert old_interval in code, 'interval block not found'
code = code.replace(old_interval, new_interval)

# b) Update snap_every to use base_league
old_snap = '    snap_every = 12 if league == "day" else 1'
new_snap  = '    snap_every = 12 if base_league == "day" else 1'
assert old_snap in code, 'snap_every not found'
code = code.replace(old_snap, new_snap)

# c) Update pnl_r check to include liquidation and leverage
old_exit_block = (
    '            pnl_r     = (current - entry) / entry if direction == "long" else (entry - current) / entry\n'
    '            reason = None\n'
    '            if pnl_r >= tp_pct:\n'
    '                reason = "target"\n'
    '            elif pnl_r <= -sl_pct:\n'
    '                reason = "stop"\n'
    '            elif age_min >= timeout_min:\n'
    '                reason = "timeout"\n'
    '            if reason:\n'
    '                close_pos(portfolio, pair, current, reason, ts_iso)'
)
new_exit_block = (
    '            pnl_r     = (current - entry) / entry if direction == "long" else (entry - current) / entry\n'
    '            reason = None\n'
    '            if is_futures and pnl_r <= -liq_threshold:\n'
    '                reason = "liquidated"\n'
    '            elif pnl_r >= tp_pct:\n'
    '                reason = "target"\n'
    '            elif pnl_r <= -sl_pct:\n'
    '                reason = "stop"\n'
    '            elif age_min >= timeout_min:\n'
    '                reason = "timeout"\n'
    '            if reason:\n'
    '                close_pos(portfolio, pair, current, reason, ts_iso)\n'
    '                if is_futures:\n'
    '                    # Apply leverage to the last closed trade P&L\n'
    '                    if portfolio["closed_trades"]:\n'
    '                        t = portfolio["closed_trades"][-1]\n'
    '                        age_h = age_min / 60\n'
    '                        funding_cost = FUNDING_RATE_8H * leverage * t.get("cost_basis", 0) * int(age_h / 8)\n'
    '                        lev_gain = t["pnl_usd"] * (leverage - 1)\n'
    '                        t["pnl_usd"] = round(t["pnl_usd"] * leverage - funding_cost, 4)\n'
    '                        t["won"] = t["pnl_usd"] > 0\n'
    '                        # Correct portfolio cash\n'
    '                        portfolio["cash"] = round(portfolio["cash"] + lev_gain - funding_cost, 4)'
)
assert old_exit_block in code, 'exit block not found'
code = code.replace(old_exit_block, new_exit_block)

# d) Update stop_pct check to use base_league
old_stop_risk = '    stop_pct  = float(strategy.get("risk", {}).get("stop_if_down_pct", 15))'
new_stop_risk = '    stop_pct  = float(strategy.get("risk", {}).get("stop_if_down_pct", 12 if is_futures else 15))'
code = code.replace(old_stop_risk, new_stop_risk)

open(path, 'w').write(code)
print('odin_backtest.py patched')


# ═══════════════════════════════════════════════════════════════
# 3. mimir.py — add futures leagues
# ═══════════════════════════════════════════════════════════════
path = RESEARCH + '/mimir.py'
code = open(path).read()

# a) Add futures leagues to choices
old_mimir_choices = 'choices=["day", "swing", "pm"]'
new_mimir_choices = 'choices=["day", "swing", "pm", "futures_day", "futures_swing"]'
assert old_mimir_choices in code, 'mimir choices not found'
code = code.replace(old_mimir_choices, new_mimir_choices)

# b) Add futures sprint results dirs
old_swing_results = 'SWING_RESULTS_DIR = os.path.join(WORKSPACE, "competition", "swing", "results")'
new_swing_results = (
    'SWING_RESULTS_DIR         = os.path.join(WORKSPACE, "competition", "swing", "results")\n'
    'FUTURES_DAY_RESULTS_DIR   = os.path.join(WORKSPACE, "competition", "futures_day", "results")\n'
    'FUTURES_SWING_RESULTS_DIR = os.path.join(WORKSPACE, "competition", "futures_swing", "results")'
)
assert old_swing_results in code, 'SWING_RESULTS_DIR not found'
code = code.replace(old_swing_results, new_swing_results)

# c) Update load_sprint_results to handle futures leagues
old_sprint_dir = (
    '    results_dir = DAY_RESULTS_DIR if league == "day" else SWING_RESULTS_DIR'
)
new_sprint_dir = (
    '    if league == "day":              results_dir = DAY_RESULTS_DIR\n'
    '    elif league == "futures_day":    results_dir = FUTURES_DAY_RESULTS_DIR\n'
    '    elif league == "futures_swing":  results_dir = FUTURES_SWING_RESULTS_DIR\n'
    '    else:                            results_dir = SWING_RESULTS_DIR'
)
assert old_sprint_dir in code, 'load_sprint_results dir not found'
code = code.replace(old_sprint_dir, new_sprint_dir)

# d) Update build_prompt bot_name and timeframe for futures
old_bot_name = (
    '    bot_name  = "AutoBotDay"  if league == "day"   else "AutoBotSwing"\n'
    '    timeframe = "5-minute (day trading)" if league == "day" else "1-hour (swing trading)"'
)
new_bot_name = (
    '    if league == "day":              bot_name = "AutoBotDay";    timeframe = "5-minute (day trading)"\n'
    '    elif league == "swing":          bot_name = "AutoBotSwing";  timeframe = "1-hour (swing trading)"\n'
    '    elif league == "futures_day":    bot_name = "AutoBotDayFutures";   timeframe = "5-minute (futures day, 2x leverage)"\n'
    '    elif league == "futures_swing":  bot_name = "AutoBotSwingFutures"; timeframe = "1-hour (futures swing, 2x leverage)"\n'
    '    else:                            bot_name = "AutoBot";       timeframe = "unknown"'
)
assert old_bot_name in code, 'build_prompt bot_name not found'
code = code.replace(old_bot_name, new_bot_name)

# e) Update bot_name in main() for futures leagues
old_autobot = (
    '        bot_name      = "autobotday" if league == "day" else "autobotswing"'
)
new_autobot = (
    '        if league == "day":             bot_name = "autobotday"\n'
    '        elif league == "swing":         bot_name = "autobotswing"\n'
    '        elif league == "futures_day":   bot_name = "autobotdayfutures"\n'
    '        elif league == "futures_swing": bot_name = "autobotswingfutures"\n'
    '        else:                           bot_name = "autobotday"'
)
assert old_autobot in code, 'main bot_name not found'
code = code.replace(old_autobot, new_autobot)

open(path, 'w').write(code)
print('mimir.py patched')


# ═══════════════════════════════════════════════════════════════
# 4. loki.py — handle futures leagues same as day/swing
# ═══════════════════════════════════════════════════════════════
path = RESEARCH + '/loki.py'
code = open(path).read()

# a) Add futures league service restart mapping
old_restart = (
    'def restart_service(league):\n'
    '    service = f"odin_{league}.service"'
)
# Just check it exists — no change needed, f-string handles futures_day -> odin_futures_day.service
# but we also need to make sure the service files exist. For now, just note it.
# The service restart will fail gracefully if service doesn't exist.

# b) Add futures to ALLOWED_CONSTS check if it does league-specific filtering
# loki.py uses league string as-is for program.md path (via RESEARCH + league + '/program.md')
# This already works for futures_day and futures_swing since league_dir uses the string directly.

# c) Make sure futures leagues don't fall into pm handling
old_process = (
    'def process_entry(entry):\n'
    '    league = entry.get("league", "")\n'
    '    if league == "pm":\n'
    '        process_pm_entry(entry)\n'
    '        return'
)
new_process = (
    'def process_entry(entry):\n'
    '    league = entry.get("league", "")\n'
    '    if league == "pm":\n'
    '        process_pm_entry(entry)\n'
    '        return\n'
    '    # futures leagues handled same as spot leagues below'
)
if old_process in code:
    code = code.replace(old_process, new_process)

open(path, 'w').write(code)
print('loki.py patched')


# ═══════════════════════════════════════════════════════════════
# 5. weekly_league_restart.py — add futures swing
# ═══════════════════════════════════════════════════════════════
path = WORKSPACE + '/weekly_league_restart.py'
code = open(path).read()

# Find where it calls swing restart and add futures swing after
# Look for pattern that restarts swing
if 'futures_swing_restart' not in code:
    # Find the last import subprocess or similar call to add our restart
    # Look for a line that starts futures leagues
    old_marker = '    print("[weekly] Done.")'
    new_marker = (
        '    # Futures swing weekly restart\n'
        '    print("[weekly] Restarting futures swing league...")\n'
        '    result = subprocess.run(\n'
        '        [sys.executable, os.path.join(WORKSPACE, "futures_swing_restart.py")],\n'
        '        capture_output=True, text=True, cwd=WORKSPACE,\n'
        '    )\n'
        '    print(result.stdout or result.stderr or "  (no output)")\n\n'
        '    print("[weekly] Done.")'
    )
    if old_marker in code:
        code = code.replace(old_marker, new_marker)
        print('weekly_league_restart.py patched')
    else:
        print('WARNING: weekly_league_restart.py marker not found — manual add needed')
else:
    print('weekly_league_restart.py already has futures_swing — skipping')

open(path, 'w').write(code)


# ═══════════════════════════════════════════════════════════════
# 6. league_watchdog.py — add futures leagues
# ═══════════════════════════════════════════════════════════════
path = WORKSPACE + '/league_watchdog.py'
code = open(path).read()

if 'futures_day' not in code:
    # Find where leagues are defined
    old_leagues_def = None
    # Search for a dict or list with 'swing' and add futures entries
    # Most watchdogs have a LEAGUES dict like:
    # LEAGUES = { 'day': {...}, 'swing': {...}, ... }
    # Let's find it
    import re as _re
    match = _re.search(r'(LEAGUES\s*=\s*\{[^}]+\})', code, _re.DOTALL)
    if match:
        old_block = match.group(1)
        # Add futures entries before closing brace
        futures_entries = (
            '\n    "futures_day": {\n'
            '        "active_dir":  os.path.join(WORKSPACE, "competition", "futures_day", "active"),\n'
            '        "restart_script": os.path.join(WORKSPACE, "futures_day_restart.py"),\n'
            '        "tick_script": os.path.join(WORKSPACE, "futures_day_competition_tick.py"),\n'
            '        "duration_hours": 24,\n'
            '    },\n'
            '    "futures_swing": {\n'
            '        "active_dir":  os.path.join(WORKSPACE, "competition", "futures_swing", "active"),\n'
            '        "restart_script": os.path.join(WORKSPACE, "futures_swing_restart.py"),\n'
            '        "tick_script": os.path.join(WORKSPACE, "futures_swing_competition_tick.py"),\n'
            '        "duration_hours": 168,\n'
            '    },'
        )
        new_block = old_block.rstrip('}') + futures_entries + '}'
        code = code.replace(old_block, new_block)
        print('league_watchdog.py LEAGUES block patched')
    else:
        print('WARNING: league_watchdog.py LEAGUES not found in expected format')
        # Try a simpler approach — find restart calls and add futures
else:
    print('league_watchdog.py already has futures_day — skipping')

open(path, 'w').write(code)

print('\nAll patches applied.')
