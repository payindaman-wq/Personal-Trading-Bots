#!/usr/bin/env python3
"""
njord_allocator.py - pure-function allocation logic. No IO.

Public:
  Action                       dataclass with .to_dict() and .to_finding()
  compute_targets              league weights -> per-bot target USD
  compute_drawdown_pct         (current, peak) -> %
  build_action_list            diff current vs target -> list[Action]

Action types and their canonical tier (NJORD source-of-truth fallback):
  rebalance            tier1   - within tolerances, no league/total change
  pause_bot            tier1   - drawdown trip on a single bot (reversible)
  wake_bot             tier2   - resumes capital flow to a paused bot
  shift_league_weight  tier2   - capital-adjacent reallocation across leagues
  reduce_total         tier2   - shrink deployed capital after losses
  wallet_op            tier3   - real-money deposit/withdraw at exchange
  key_change           tier3   - rotate Kraken API credentials
  retire_league        tier3   - permanently retire a whole league
  total_change_25pct   tier3   - total-capital change exceeds 25% threshold
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

REBALANCE_TOLERANCE_PCT = 2.0


@dataclass
class Action:
    type: str
    bot: str = ""
    league: str = ""
    from_usd: float = 0.0
    to_usd: float = 0.0
    reason: str = ""

    def to_dict(self):
        return asdict(self)

    def to_finding(self):
        """Render as a vidar_tier-shaped finding for the classifier."""
        title = "NJORD: " + self.type + ((" " + self.bot) if self.bot else "")
        return {
            "id":               "njord-" + self.type + "-" + (self.bot or self.league or "global"),
            "severity":         "info",
            "title":            title[:200],
            "evidence":         self.reason[:500],
            "suggested_action": self._suggested_action_text()[:600],
        }

    def _suggested_action_text(self):
        t = self.type
        if t == "rebalance":
            return ("Rebalance bot " + self.bot + " from $" + format(self.from_usd, ".2f")
                    + " to $" + format(self.to_usd, ".2f")
                    + ". Threshold tweak inside per_bot_max_pct cap.")
        if t == "pause_bot":
            return ("Pause bot " + self.bot + " after drawdown trip ("
                    + format(self.from_usd, ".2f") + "% from peak). Reversible kill flag.")
        if t == "wake_bot":
            return ("Wake previously paused bot " + self.bot
                    + "; resumes capital flow to the strategy.")
        if t == "shift_league_weight":
            return ("Shift league weight for " + self.league + ": $"
                    + format(self.from_usd, ".2f") + " -> $" + format(self.to_usd, ".2f")
                    + ". Capital-adjacent reallocation, reversible.")
        if t == "reduce_total":
            return ("Reduce total deployed capital from $" + format(self.from_usd, ".2f")
                    + " to $" + format(self.to_usd, ".2f") + " after series of losses.")
        if t == "wallet_op":
            return ("Wallet operation: deposit or withdraw funds at exchange - "
                    "real money movement requiring Chris ack.")
        if t == "key_change":
            return ("Rotate Kraken API key and credentials - "
                    "irreversible credential change requiring Chris ack.")
        if t == "retire_league":
            return ("Permanently retire league " + self.league + " and remove it from "
                    "capital allocation policy.")
        if t == "total_change_25pct":
            return ("Total-capital change exceeds 25%: $" + format(self.from_usd, ".2f")
                    + " -> $" + format(self.to_usd, ".2f")
                    + ". Real-capital allocation policy change - Chris ack required.")
        return self.reason


def compute_targets(total_capital, league_weights, bots_per_league, per_bot_max_pct):
    """Compute target USD per bot.

    league_weights:    {league: weight_fraction}
    bots_per_league:   {league: [bot_names]}
    per_bot_max_pct:   cap on any single bot as % of total_capital
    Returns: {bot_name: target_usd}
    """
    out = {}
    if total_capital <= 0:
        for league, bots in bots_per_league.items():
            for b in bots:
                out[b] = 0.0
        return out
    cap_per_bot = total_capital * float(per_bot_max_pct) / 100.0
    for league, bots in bots_per_league.items():
        weight = float(league_weights.get(league, 0.0) or 0.0)
        if not bots or weight <= 0:
            for b in bots:
                out[b] = 0.0
            continue
        per_bot = (total_capital * weight) / len(bots)
        per_bot = min(per_bot, cap_per_bot)
        for b in bots:
            out[b] = round(per_bot, 2)
    return out


def compute_drawdown_pct(current_value, peak_value):
    if peak_value <= 0:
        return 0.0
    drop = peak_value - current_value
    if drop <= 0:
        return 0.0
    return round(100.0 * drop / peak_value, 2)


def build_action_list(current_table, target_table, killed_leagues,
                      drawdown_kill_pct, total_capital, last_total_capital,
                      bot_to_league=None, rebalance_tolerance_pct=REBALANCE_TOLERANCE_PCT):
    """Diff current vs target; return ordered list[Action]."""
    actions = []
    bot_to_league = bot_to_league or {}
    killed = set(killed_leagues or ())

    if last_total_capital and last_total_capital > 0:
        delta_pct = abs(total_capital - last_total_capital) / last_total_capital * 100.0
        if delta_pct > 25.0:
            actions.append(Action(
                type="total_change_25pct",
                from_usd=last_total_capital,
                to_usd=total_capital,
                reason="Total capital changed by " + format(delta_pct, ".1f")
                       + "% - exceeds 25% threshold.",
            ))

    for bot, target_usd in target_table.items():
        cur = current_table.get(bot, {}) or {}
        cur_alloc = float(cur.get("allocated_usd", 0.0) or 0.0)
        cur_value = float(cur.get("current_value_usd", cur_alloc) or 0.0)
        peak = max(cur_alloc, cur_value, float(cur.get("peak_value_usd", 0.0) or 0.0))
        kill_state = (cur.get("kill_state") or "active")
        league = bot_to_league.get(bot, "")

        if league in killed and cur_alloc > 0:
            actions.append(Action(
                type="rebalance",
                bot=bot,
                league=league,
                from_usd=cur_alloc,
                to_usd=0.0,
                reason="League " + league + " is killed by league_killswitch; zero-out bot.",
            ))
            continue

        dd = compute_drawdown_pct(cur_value, peak)
        if dd >= drawdown_kill_pct and kill_state == "active":
            actions.append(Action(
                type="pause_bot",
                bot=bot,
                league=league,
                from_usd=dd,
                to_usd=0.0,
                reason="Drawdown " + format(dd, ".1f") + "% >= kill threshold "
                       + str(drawdown_kill_pct) + "%.",
            ))
            continue

        if kill_state == "paused" and dd < (drawdown_kill_pct / 2.0):
            actions.append(Action(
                type="wake_bot",
                bot=bot,
                league=league,
                from_usd=cur_alloc,
                to_usd=target_usd,
                reason="Drawdown recovered to " + format(dd, ".1f") + "% (<50% of threshold).",
            ))
            continue

        if target_usd <= 0 and cur_alloc <= 0:
            continue
        denom = max(target_usd, 1.0)
        diff_pct = abs(cur_alloc - target_usd) / denom * 100.0
        if diff_pct > rebalance_tolerance_pct:
            actions.append(Action(
                type="rebalance",
                bot=bot,
                league=league,
                from_usd=cur_alloc,
                to_usd=target_usd,
                reason="Allocation drift " + format(diff_pct, ".1f")
                       + "% > tolerance " + format(rebalance_tolerance_pct, ".1f") + "%.",
            ))

    return actions
