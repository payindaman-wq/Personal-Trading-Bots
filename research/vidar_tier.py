#!/usr/bin/env python3
"""
vidar_tier.py — classify a meta_audit finding into Tier 1 / Tier 2 / Tier 3
(reversibility + capital exposure). Closes the F7 authority gap.

Tiering rubric:

  Tier 1 — Reversible code/config. odin_researcher_v2.py threshold tweaks,
           gate parameters, MIMIR pre-flight checks, regression_watch
           cooldowns, fee/funding/universe parity fixes, OOS gate logic,
           fix-citation-fabrication. Auto-revert on metric degradation in
           the existing loki_structural_monitor pipeline catches regressions.

  Tier 2 — Reversible but capital-adjacent. League pause/resume, enable/
           disable new_best gate, kill-criteria changes, edits to safety
           subsystems whose failure mode isn't caught by metric-drift auto-
           revert (killswitch, VIDAR firing rules, population resets that
           wipe elite history). VIDAR ships, writes 24h
           vidar_pending_review.flag, Chris can revert with one command.

  Tier 3 — Irreversible. Permanent league retirement, money movement,
           exchange API credentials, real-capital allocation policy,
           withdrawal flows, deletion of historical elite/backup state with
           no recoverable copy. Block + page Chris.

Cost: Sonnet 4.6 with system-prompt caching. Per audit run with 13 findings
the budget is ~$0.10 (rubric is cached after first call).

Public API:
    classify_finding(finding, audit_ts=None) -> (tier_str, rationale_str)

    tier_str ∈ {"tier1", "tier2", "tier3"}
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone

WORKSPACE        = "/root/.openclaw/workspace"
RESEARCH         = os.path.join(WORKSPACE, "research")
ANTHROPIC_SECRET = "/root/.openclaw/secrets/anthropic.json"
ANTHROPIC_USAGE  = os.path.join(RESEARCH, "anthropic_usage.jsonl")

TIER_CACHE       = os.path.join(RESEARCH, "vidar_tier_cache.json")

CLASSIFIER_MODEL       = "claude-sonnet-4-6"
CLASSIFIER_MAX_TOKENS  = 400

# Tier 3 hard keywords — only fire on phrasings that unambiguously describe
# an *irreversible action being proposed* in the suggested_action. We
# deliberately exclude bare "retire" / "retirement": a finding may describe
# a past retirement (e.g. F12's "Kalshi retirement left orphaned state")
# without proposing one. Borderline cases go to the LLM.
TIER3_KEYWORDS = (
    r"\bpermanently\b",
    r"\bdelete all\b",
    r"\bremove all\b",
    r"\bwithdraw(?:al|als)? (?:funds|money|cash|capital)\b",
    r"\blive capital\b",
    r"\breal money\b",
    r"\bcredential(?:s)?\b",
    r"\bAPI key(?:s)?\b",
    r"\birrecoverabl(?:e|y)\b",
    r"\bpermanent retirement\b",
    r"\bretire (?:\w+ )?permanently\b",
)
TIER3_PATTERN = re.compile("|".join(TIER3_KEYWORDS), flags=re.IGNORECASE)


SYSTEM_RUBRIC = """You are VIDAR's tier classifier. You classify autoresearch system meta-audit findings into one of three authority tiers, based purely on reversibility and capital exposure. You do not judge whether the finding is correct — only how risky executing its `suggested_action` would be.

You output a single JSON object with two fields: `tier` (one of "tier1"|"tier2"|"tier3") and `rationale` (one sentence on why).

KEY DIRECTIONALITY RULE — read this twice:

When a finding modifies a safety/validation/promotion gate, the TIER depends on whether the change is STRICTER (more conservative) or LOOSER:

  - ADDING a new validation criterion / kill criterion / promotion gate, or making an existing one STRICTER → tier1.
    Why: the gate stays on. Failure mode is "nothing promotes" or "kills fire too aggressively" — both visible to LOKI's metric monitor (mean_sharpe drop, gens_since_best plateau, league_pnl change) within the auto-revert window.

  - REMOVING / LOOSENING a safety criterion, or DISABLING a gate, or PAUSING/RESUMING capital flow → tier2.
    Why: failure mode is silent — the safety system stops catching things it used to catch, or capital flows where it shouldn't. Metric drift can't auto-revert what didn't trigger.

DEFINITIONS

tier1: REVERSIBLE CODE/CONFIG.
  - Threshold tweaks, gate parameter changes, OOS bar adjustments (in either direction — the gate still exists)
  - ADDING a new safety / validation / kill criterion (live-PnL veto, live-PnL kill, resolved-market validation, citation pre-flight, walk-forward OOS, diversity injection)
  - Replacing one validation method with another that is at least as conservative (e.g. adaptive-OOS → walk-forward holdout)
  - Fee/funding/slippage/universe corrections in backtest models
  - Diversity injection rules (replace bottom N elites with random valid configs — preserves champion + top elites)
  - Watchdog cooldown adjustments / regression_watch tweaks
  - Audit + commit of orphaned migration files; sprint_integrity passes

  Why tier1: any regression is detectable by the existing loki_structural_monitor pipeline (mean_sharpe drop, structural_failure_rate spike, gens_since_best, service crash). Auto-revert restores from .bak in <6h.

tier2: REVERSIBLE BUT CAPITAL-ADJACENT.
  - League PAUSE / RESUME (changes capital flow on/off)
  - DISABLING the new_best promotion gate, or LOOSENING it (allowing more strategies through)
  - LOOSENING / REMOVING / SUPPRESSING existing kill criteria, or LOOSENING / SUPPRESSING VIDAR firing rules
  - Granting an officer authority over a previously-restricted file/scope (LOKI gaining program.md write authority, an executor gaining new action types) — the AUTHORITY change itself
  - POPULATION RESET that deletes elite_0..elite_N (recoverable from .bak but disrupts in-flight research; Sharpe baseline jumps in ways the metric monitor will see as a "regression" and auto-revert wrongly)
  - Adding new Telegram/Chris-paging escalation paths (an over-paging mistake is silent in metric monitor terms)

  Why tier2: failure mode is silence — the safety subsystem fails open, or capital allocation changes outside the metric-drift detection window. Auto-revert via metric monitor doesn't apply. Ship + require Chris ack within 24h.

tier3: IRREVERSIBLE.
  - Permanent league retirement (suggested_action explicitly proposes "permanently" + "retire")
  - Money movement, withdrawals, real-capital allocation policy
  - Exchange API credential rotations
  - Deletion of all elite/backup state with no recoverable copy ("delete all elite_0 backups permanently")

  Why tier3: cannot be undone by code revert. Requires Chris's explicit go-ahead.

DECISION ALGORITHM

1. If `suggested_action` proposes deletion of backup files irrecoverably, OR retiring a league permanently, OR moving money, OR rotating credentials, OR changing real-capital allocation policy → tier3.
2. Else if the change PAUSES / RESUMES capital flow, OR LOOSENS / DISABLES / REMOVES an existing safety criterion, OR grants new authority to an officer/scope, OR resets the elite population disruptively, OR adds a new Chris-paging path → tier2.
3. Else (including ADDING a new stricter gate, ADDING a new kill criterion, normal threshold tweaks, code corrections to backtest math, citation verification, watchdog cooldowns, diversity injection) → tier1.

Default to the lower tier when the change is strictly more conservative — auto-revert via metric monitor handles the false-positive regressions.

Return ONLY a JSON object. No prose.

EXAMPLES

Finding: {"id": "EX1", "title": "Add live-PnL veto to ODIN promotion gate", "suggested_action": "Block new_best promotion when _sharpe_24h_median < 0 over rolling 5 sprints. Add a live-PnL term to ODIN's adj_score."}
Output: {"tier":"tier1","rationale":"Adds a stricter promotion gate and a new objective term — both purely conservative. Regression mode is over-rejection, visible to the metric monitor."}

Finding: {"id": "EX2", "title": "Add league-level live-PnL kill criterion", "suggested_action": "Add to league_killswitch.py: kill league if median 7-sprint live PnL < -0.2% AND champion backtest Sharpe < 0."}
Output: {"tier":"tier1","rationale":"Clean add of a single AND-conjoined kill criterion that requires both poor live AND poor backtest before firing. Metric monitor sees over-aggressive kills as gens_since_best plateau and auto-reverts."}

Finding: {"id": "EX2b", "title": "Audit league_killswitch criteria and add new triggers", "suggested_action": "Audit league_killswitch.py criteria. Add: kill league if (live_pnl_median_5sprint < -0.5%) OR (champion_backtest_sharpe < 0) OR (gens_since_best > 1500 AND unique_sharpe == 1)."}
Output: {"tier":"tier2","rationale":"Audit-and-restructure of an existing safety subsystem with multi-OR criteria — including a trigger (gens_since_best > 1500 AND unique_sharpe == 1) that would fire immediately on currently-converging leagues. Failure mode is silent over-kills the metric monitor cannot distinguish from intended kills."}

Finding: {"id": "EX3", "title": "Suppress VIDAR fires within 48h on same league", "suggested_action": "Skip VIDAR fire if same league + same revert reason within 48h of prior fire."}
Output: {"tier":"tier2","rationale":"Loosens VIDAR firing rules — failure mode is missed arbitration on a real new problem (silent), which the metric monitor cannot detect."}

Finding: {"id": "EX4", "title": "Resume futures_day league after pause", "suggested_action": "Re-enable the daily futures_day restart cron currently commented out as PAUSED."}
Output: {"tier":"tier2","rationale":"Re-opens capital flow to a previously paused strategy — capital-adjacent and not metric-drift-detectable in the resume window."}

Finding: {"id": "EX5", "title": "Permanent retirement of arb league", "suggested_action": "Permanently retire arb league and delete all arb research state."}
Output: {"tier":"tier3","rationale":"Permanent retirement and irrecoverable state deletion; cannot be auto-reverted."}

Finding: {"id": "EX6", "title": "Add walk-forward OOS gate to day and swing leagues", "suggested_action": "Ship backtest_drift.json + walk-forward holdout for day and swing leagues, matching futures_day's implementation. Block new_best promotion until OOS Sharpe >= 0.5 on a 30-day holdout window."}
Output: {"tier":"tier1","rationale":"Adds a new stricter OOS validation gate where none currently exists — purely conservative addition. Failure mode is over-rejection of promotions, visible in the metric monitor as gens_since_best plateau."}

Finding: {"id": "EX7", "title": "Reset population from scratch", "suggested_action": "Delete elite_0..elite_9 in futures_day and reseed with diverse random configs."}
Output: {"tier":"tier2","rationale":"Population reset disrupts in-flight research state and triggers a Sharpe baseline jump that LOKI's metric monitor would mistakenly read as a regression. Disruptive enough to require Chris ack within 24h even though backups exist."}

Finding: {"id": "EX8", "title": "Grant LOKI authority to rewrite program.md from elite_0", "suggested_action": "Allow LOKI to rewrite program.md whenever it diverges from elite_0 ground truth, with auto-revert on metric degradation."}
Output: {"tier":"tier2","rationale":"Granting an officer NEW write authority over a previously-restricted file is an authority-scope expansion. The change itself is the safety boundary — auto-revert applies to the *use* of the new authority, not to the *granting* of it."}

Finding: {"id": "EX9", "title": "Diversity injection on convergence", "suggested_action": "When unique_sharpe < 3 OR gens_since_best > 500, replace bottom 5 elites with random valid configs while preserving champion + top 4."}
Output: {"tier":"tier1","rationale":"Adds a diversity-injection rule that preserves champion and top elites — bottom-N replacement is recoverable from backups and LOKI's metric monitor catches any Sharpe degradation."}

Finding: {"id": "EX10", "title": "Audit existing safety subsystem and restructure", "suggested_action": "Audit league_killswitch.py criteria. Restructure with multi-OR triggers including (gens_since_best > 1500 AND unique_sharpe == 1) — a condition that would fire on currently-converging leagues."}
Output: {"tier":"tier2","rationale":"Restructure (not just-add) of an existing safety subsystem with new triggers that would fire immediately on current state. Failure mode is silent over-killing, indistinguishable from intended kills by the metric monitor."}

Finding: {"id": "EX11", "title": "Pre-flight citation verification in MIMIR", "suggested_action": "Pre-flight check on MIMIR output: any cited (gen, sharpe) pair must match results.tsv before MIMIR analysis is accepted. If citation fails, MIMIR cycle is rejected."}
Output: {"tier":"tier1","rationale":"Adds a stricter pre-flight verification gate to MIMIR output; rejection on failure is conservative. The citation-fabrication failure mode it prevents is currently silent — closing it is purely safety-additive."}
"""


def _load_anthropic_key():
    with open(ANTHROPIC_SECRET) as f:
        return json.load(f)["anthropic_api_key"]


def _load_cache():
    if not os.path.exists(TIER_CACHE):
        return {}
    try:
        with open(TIER_CACHE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache):
    tmp = TIER_CACHE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cache, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, TIER_CACHE)


def _cache_key(audit_ts, finding_id):
    return f"{audit_ts or 'no_audit_ts'}::{finding_id or 'no_id'}"


def _log_usage(usage, model):
    try:
        rec = {
            "ts":            datetime.now(timezone.utc).isoformat(),
            "caller":        "vidar_tier",
            "model":         model,
            "input_tokens":  usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
            "cache_read_input_tokens":     usage.get("cache_read_input_tokens", 0),
        }
        with open(ANTHROPIC_USAGE, "a") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError as e:
        sys.stderr.write(f"[vidar_tier] usage log failed: {e}\n")


def _tier3_keyword_match(finding):
    haystack = " ".join([
        str(finding.get("title", "")),
        str(finding.get("suggested_action", "")),
        str(finding.get("evidence", "")),
    ])
    m = TIER3_PATTERN.search(haystack)
    if m:
        return m.group(0)
    return None


def _classify_with_llm(finding, api_key):
    """Sonnet 4.6 + system-prompt caching. Returns (tier, rationale)."""
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError(
            "anthropic SDK not installed; pip install anthropic"
        ) from e

    client = anthropic.Anthropic(api_key=api_key)

    user_message = (
        "Classify this meta-audit finding:\n\n"
        + json.dumps({
            "id":               finding.get("id", "?"),
            "severity":         finding.get("severity", "?"),
            "title":            finding.get("title", "")[:300],
            "evidence":         finding.get("evidence", "")[:800],
            "suggested_action": finding.get("suggested_action", "")[:1200],
            "delegable_to_loki": finding.get("delegable_to_loki", None),
        }, indent=1)
        + "\n\nReturn ONLY the JSON object {tier, rationale}."
    )

    response = client.messages.create(
        model=CLASSIFIER_MODEL,
        max_tokens=CLASSIFIER_MAX_TOKENS,
        system=[
            {
                "type":          "text",
                "text":          SYSTEM_RUBRIC,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_message}],
    )

    usage = getattr(response, "usage", None)
    if usage:
        _log_usage(
            {
                "input_tokens":                getattr(usage, "input_tokens", 0),
                "output_tokens":               getattr(usage, "output_tokens", 0),
                "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0),
                "cache_read_input_tokens":     getattr(usage, "cache_read_input_tokens", 0),
            },
            CLASSIFIER_MODEL,
        )

    text = response.content[0].text.strip()
    # Tolerate ```json fences if Sonnet adds them
    if "```" in text:
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if m:
            text = m.group(1)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"classifier returned non-JSON: {text[:300]}") from e
    tier = parsed.get("tier")
    rationale = parsed.get("rationale", "")
    if tier not in ("tier1", "tier2", "tier3"):
        raise RuntimeError(f"classifier returned invalid tier: {parsed}")
    return tier, rationale


def classify_finding(finding, audit_ts=None):
    """Public entrypoint. Returns (tier, rationale).

    Caching:
      - In-memory + on-disk JSON cache keyed by (audit_ts, finding.id).
      - Re-classifying the same (audit_ts, id) is free.

    Pre-pass:
      - Tier-3 keyword match short-circuits without an LLM call.
    """
    finding_id = finding.get("id") or finding.get("finding_id")
    cache = _load_cache()
    key = _cache_key(audit_ts, finding_id)
    if key in cache:
        cached = cache[key]
        return cached["tier"], cached.get("rationale", "")

    keyword_hit = _tier3_keyword_match(finding)
    if keyword_hit:
        tier = "tier3"
        rationale = f"keyword:{keyword_hit.lower()} (irreversibility tell)"
        cache[key] = {"tier": tier, "rationale": rationale, "source": "keyword_prepass"}
        _save_cache(cache)
        return tier, rationale

    api_key = _load_anthropic_key()
    tier, rationale = _classify_with_llm(finding, api_key)
    cache[key] = {"tier": tier, "rationale": rationale, "source": CLASSIFIER_MODEL}
    _save_cache(cache)
    return tier, rationale


def main():
    """CLI for one-off classification: read finding JSON on stdin, print tier."""
    raw = sys.stdin.read()
    finding = json.loads(raw)
    audit_ts = os.environ.get("VIDAR_TIER_AUDIT_TS")
    tier, rationale = classify_finding(finding, audit_ts=audit_ts)
    print(json.dumps({"tier": tier, "rationale": rationale}))


if __name__ == "__main__":
    main()
