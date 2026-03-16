#!/usr/bin/env python3
"""
pair_health_check.py — Shared cointegration health check for Spread and Arb leagues.

Runs at the START of each new cycle (before sprint 1) to ensure all active
pairs are statistically valid for mean-reversion trading.

Actions:
  RETIRE  (hl > sprint length): auto-replace with best available candidate
  WEAK    (2 metric failures): warn only — caller decides
  STRONG/WATCH: no action

Usage:
  python3 pair_health_check.py --league spread [--auto-replace] [--dry-run]
  python3 pair_health_check.py --league arb    [--auto-replace] [--dry-run]

Returns exit code 0 always. Prints structured summary.
Caller reads the returned report for replacement details.
"""
import argparse, json, math, os, sys
from datetime import datetime, timezone
import numpy as np

WORKSPACE   = "/root/.openclaw/workspace"
PRICE_DIR   = os.path.join(WORKSPACE, "competition", "swing", "price_history")
SPRINT_HOURS = 168

THRESHOLDS = {
    "min_corr":         0.65,
    "max_half_life":    120,
    "max_hurst":        0.50,
    "retire_half_life": SPRINT_HOURS,
}

LOOKBACK = 720   # 30 days of hourly candles

ALL_ASSETS = ["BTC", "ETH", "SOL", "AVAX", "LINK", "AAVE", "DOGE", "XRP",
              "NEAR", "APT", "ARB", "OP", "SUI", "WIF"]


# ── League config ─────────────────────────────────────────────────────────────

def league_config(league):
    base = {
        "spread": {
            "fleet_dir":   os.path.join(WORKSPACE, "fleet", "spread"),
            "report_path": os.path.join(WORKSPACE, "competition", "spread",
                                        "cointegration_report.json"),
        },
        "arb": {
            "fleet_dir":   os.path.join(WORKSPACE, "fleet", "arb"),
            "report_path": os.path.join(WORKSPACE, "competition", "arb",
                                        "cointegration_report.json"),
        },
    }
    return base.get(league)


# ── Fleet pair loading ────────────────────────────────────────────────────────

def load_fleet_pairs(fleet_dir, league):
    """Return {bot: {base, quote, analysis_pair}} from strategy.yaml files."""
    try:
        import yaml
    except ImportError:
        print("ERROR: pyyaml required — pip install pyyaml", file=sys.stderr)
        return {}

    result = {}
    if not os.path.isdir(fleet_dir):
        return result
    for bot in os.listdir(fleet_dir):
        path = os.path.join(fleet_dir, bot, "strategy.yaml")
        if not os.path.isfile(path):
            continue
        try:
            with open(path) as f:
                d = yaml.safe_load(f)
            if league == "spread":
                sp = d.get("spread", {})
                base  = sp.get("base", "")
                quote = sp.get("quote", "")
                ap    = sp.get("analysis_pair", "")
            else:  # arb
                base  = d.get("pair_a", "")
                quote = d.get("pair_b", "")
                b_sym = base.replace("/USD", "")
                q_sym = quote.replace("/USD", "")
                ap    = f"{b_sym}_{q_sym}_RATIO"
            if base and quote:
                result[bot] = {"base": base, "quote": quote, "analysis_pair": ap}
        except Exception:
            pass
    return result


def update_strategy_pair(path, league, new_base, new_quote):
    """Update a bot's strategy.yaml with a new pair."""
    try:
        import yaml
    except ImportError:
        return False
    try:
        with open(path) as f:
            d = yaml.safe_load(f)
        b_sym = new_base.replace("/USD", "")
        q_sym = new_quote.replace("/USD", "")
        ap    = f"{b_sym}_{q_sym}_RATIO"
        if league == "spread":
            d.setdefault("spread", {})
            d["spread"]["base"]          = new_base
            d["spread"]["quote"]         = new_quote
            d["spread"]["analysis_pair"] = ap
        else:  # arb
            d["pair_a"] = new_base
            d["pair_b"] = new_quote
        with open(path, "w") as f:
            yaml.dump(d, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"  ERROR updating {path}: {e}")
        return False


# ── Statistical tests (same as spread_cointegration_check.py) ────────────────

def load_closes(asset):
    sym  = asset.replace("/USD", "").replace("/", "")
    path = os.path.join(PRICE_DIR, f"{sym}-USD.json")
    if not os.path.exists(path):
        return []
    try:
        candles = json.load(open(path))
        return [c["close"] for c in candles[-LOOKBACK:] if "close" in c]
    except Exception:
        return []


def align_series(a, b):
    n = min(len(a), len(b))
    return np.array(a[-n:]), np.array(b[-n:])


def pearson_corr(x, y):
    if len(x) < 30:
        return None
    lx = np.diff(np.log(x + 1e-12))
    ly = np.diff(np.log(y + 1e-12))
    if np.std(lx) == 0 or np.std(ly) == 0:
        return 0.0
    return float(np.corrcoef(lx, ly)[0, 1])


def half_life(ratio):
    if len(ratio) < 30:
        return None
    y, y_l = ratio[1:], ratio[:-1]
    dy = y - y_l
    X  = np.column_stack([y_l, np.ones(len(y_l))])
    try:
        coef, _, _, _ = np.linalg.lstsq(X, dy, rcond=None)
        lam = coef[0]
    except Exception:
        return None
    if lam >= 0:
        return None
    hl = -math.log(2) / lam
    return round(hl, 1) if hl > 0 else None


def hurst_exponent(series):
    if len(series) < 100:
        return None
    series = np.array(series)
    lags   = [2, 4, 8, 16, 32, 64]
    variances = []
    for lag in lags:
        diff = series[lag:] - series[:-lag]
        var  = np.var(diff)
        if var > 0:
            variances.append((lag, var))
    if len(variances) < 4:
        return None
    log_lags = [math.log(l) for l, _ in variances]
    log_vars = [math.log(v) for _, v in variances]
    n  = len(log_lags)
    xm = sum(log_lags) / n
    ym = sum(log_vars) / n
    num = sum((x - xm) * (y - ym) for x, y in zip(log_lags, log_vars))
    den = sum((x - xm) ** 2 for x in log_lags)
    if den == 0:
        return None
    return round((num / den) / 2.0, 3)


def score_pair(base, quote):
    a_prices = load_closes(base.replace("/USD", ""))
    b_prices = load_closes(quote.replace("/USD", ""))
    if len(a_prices) < 50 or len(b_prices) < 50:
        return {"error": "insufficient_data"}

    a, b   = align_series(a_prices, b_prices)
    ratio  = a / b
    corr   = pearson_corr(a, b)
    hl     = half_life(ratio)
    hurst  = hurst_exponent(ratio)
    vol    = round(float(np.std(ratio) / np.mean(ratio)), 4) if len(ratio) > 10 else None

    issues = []
    if corr is not None and corr < THRESHOLDS["min_corr"]:
        issues.append(f"low_corr({corr:.2f})")
    if hl is None:
        issues.append("no_mean_reversion")
    elif hl > THRESHOLDS["retire_half_life"]:
        issues.append(f"hl_too_long({hl:.0f}h)")
    elif hl > THRESHOLDS["max_half_life"]:
        issues.append(f"slow_reversion({hl:.0f}h)")
    if hurst is not None and hurst > THRESHOLDS["max_hurst"]:
        issues.append(f"trending(H={hurst:.2f})")

    n_issues = len(issues)
    verdict  = ("STRONG" if n_issues == 0 else "WATCH" if n_issues == 1
                else "WEAK" if n_issues == 2 else "RETIRE")
    if hl is not None and hl > THRESHOLDS["retire_half_life"]:
        verdict = "RETIRE"
    if hl is None and (corr is None or corr < THRESHOLDS["min_corr"]):
        verdict = "RETIRE"

    corr_score  = max(0.0, (1.0 - (corr or 0.0)) * 30)
    hl_score    = min(40.0, ((hl or 999) / THRESHOLDS["max_half_life"]) * 40)
    hurst_score = max(0.0, ((hurst or 0.5) - 0.3) / 0.2 * 30) if hurst else 15.0
    composite   = round(corr_score + hl_score + hurst_score, 1)

    return {
        "base": base, "quote": quote,
        "candles": len(ratio),
        "corr":      round(corr, 3) if corr is not None else None,
        "half_life": hl,
        "hurst":     hurst,
        "vol_cv":    vol,
        "issues":    issues,
        "verdict":   verdict,
        "score":     composite,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def run(league, auto_replace=False, dry_run=False):
    cfg       = league_config(league)
    fleet_dir = cfg["fleet_dir"]
    rpt_path  = cfg["report_path"]

    ts = datetime.now(timezone.utc).isoformat()
    print(f"\n{'='*62}")
    print(f"  PAIR HEALTH CHECK [{league.upper()}]  |  {ts[:16]} UTC")
    if dry_run:
        print("  DRY RUN")
    print(f"{'='*62}\n")

    # Load current fleet assignments
    fleet = load_fleet_pairs(fleet_dir, league)
    if not fleet:
        print("ERROR: no bots found in fleet")
        return {}

    # Build unique active pairs
    active_pairs = {}  # analysis_pair → {base, quote, bots: [...]}
    for bot, m in fleet.items():
        ap = m["analysis_pair"]
        if ap not in active_pairs:
            active_pairs[ap] = {"base": m["base"], "quote": m["quote"], "bots": []}
        active_pairs[ap]["bots"].append(bot)

    # Score active pairs
    print("ACTIVE PAIRS")
    print("-" * 62)
    active_results = {}
    for ap, info in sorted(active_pairs.items()):
        r = score_pair(info["base"], info["quote"])
        r["bots"] = info["bots"]
        active_results[ap] = r
        if "error" in r:
            print(f"  {ap:<24}  ERROR: {r['error']}")
            continue
        corr_s  = f"{r['corr']:.3f}"    if r["corr"]      is not None else " N/A"
        hl_s    = f"{r['half_life']:.0f}h" if r["half_life"] is not None else " N/A"
        hurst_s = f"{r['hurst']:.3f}"   if r["hurst"]     is not None else " N/A"
        flag    = "  *** RETIRE ***" if r["verdict"] == "RETIRE" else "  ! WEAK" if r["verdict"] == "WEAK" else ""
        print(f"  {ap:<24}  [{r['verdict']:<7}]  "
              f"corr={corr_s}  hl={hl_s:>7}  H={hurst_s}  "
              f"bots={','.join(r['bots'])}{flag}")
        if r["issues"]:
            print(f"    issues: {', '.join(r['issues'])}")

    # Scan candidates (all pairs not currently active)
    used = set((v["base"], v["quote"]) for v in active_pairs.values())
    assets    = [a for a in ALL_ASSETS
                 if os.path.exists(os.path.join(PRICE_DIR, f"{a}-USD.json"))]
    candidates = []
    for i, a in enumerate(assets):
        for b in assets[i+1:]:
            base, quote = f"{a}/USD", f"{b}/USD"
            if (base, quote) in used or (quote, base) in used:
                continue
            r = score_pair(base, quote)
            if "error" not in r:
                candidates.append(r)
    candidates.sort(key=lambda x: x["score"])

    # Summary
    retire = [k for k, v in active_results.items() if v.get("verdict") == "RETIRE"]
    weak   = [k for k, v in active_results.items() if v.get("verdict") == "WEAK"]
    watch  = [k for k, v in active_results.items() if v.get("verdict") == "WATCH"]
    strong = [k for k, v in active_results.items() if v.get("verdict") == "STRONG"]

    print(f"\nSUMMARY: STRONG:{len(strong)}  WATCH:{len(watch)}  WEAK:{len(weak)}  RETIRE:{len(retire)}")

    # Auto-replace RETIRE pairs
    replacements = []
    if auto_replace and retire:
        print(f"\nAUTO-REPLACING {len(retire)} RETIRE pair(s)...")
        assigned = set(used)
        for ap in retire:
            info = active_pairs[ap]
            bots = info["bots"]
            # Find best available candidate
            replacement = None
            for cand in candidates:
                b, q = cand["base"], cand["quote"]
                if (b, q) in assigned or (q, b) in assigned:
                    continue
                if cand["verdict"] not in ("STRONG", "WATCH"):
                    continue
                replacement = cand
                assigned.add((b, q))
                break
            if not replacement:
                print(f"  WARNING: no replacement found for {ap}")
                continue
            new_base  = replacement["base"]
            new_quote = replacement["quote"]
            new_pair  = f"{new_base.replace('/USD','')}/{new_quote.replace('/USD','')}"
            for bot in bots:
                path = os.path.join(fleet_dir, bot, "strategy.yaml")
                print(f"  {bot}: {ap} -> {new_pair}  (hl={replacement['half_life']:.0f}h  score={replacement['score']:.1f})")
                if not dry_run:
                    update_strategy_pair(path, league, new_base, new_quote)
                replacements.append({
                    "bot": bot, "old_pair": ap,
                    "new_pair": new_pair,
                    "new_base": new_base, "new_quote": new_quote,
                    "half_life": replacement["half_life"],
                })

    if weak:
        print(f"\nWEAK pairs (monitor — will auto-replace if WEAK again next cycle):")
        for ap in weak:
            bots = active_pairs[ap]["bots"]
            r    = active_results[ap]
            print(f"  {ap}  [{', '.join(bots)}]  issues: {', '.join(r.get('issues', []))}")

    # Save report
    report = {
        "generated_at":  ts,
        "league":        league,
        "active_pairs":  active_results,
        "candidates":    candidates[:20],
        "summary":       {"strong": strong, "watch": watch, "weak": weak, "retire": retire},
        "replacements":  replacements,
        "thresholds":    THRESHOLDS,
    }
    os.makedirs(os.path.dirname(rpt_path), exist_ok=True)
    with open(rpt_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  Report saved: {rpt_path}")

    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league",       choices=["spread", "arb"], required=True)
    parser.add_argument("--auto-replace", action="store_true",
                        help="Auto-replace RETIRE pairs in strategy.yaml")
    parser.add_argument("--dry-run",      action="store_true",
                        help="Show what would happen without modifying files")
    args = parser.parse_args()
    run(args.league, auto_replace=args.auto_replace, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
