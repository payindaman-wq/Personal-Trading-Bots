#!/usr/bin/env python3
"""
spread_cointegration_check.py -- Post-sprint cointegration health check for Spread League pairs.

For each active ratio pair, computes:
  - Pearson correlation of log returns (base vs quote)
  - Half-life of mean reversion via AR(1) OLS regression on ratio changes
  - Hurst exponent via variance ratio method (H < 0.5 = mean-reverting)
  - Ratio volatility (coefficient of variation)

Verdicts:
  STRONG  -- passes all tests: corr >= 0.65, half-life <= 120h, Hurst <= 0.50
  WATCH   -- borderline on 1 metric
  WEAK    -- fails 2 metrics
  RETIRE  -- fails 3+ metrics or half-life > sprint length

Also scans all available pairs as candidates and ranks by composite score.
Outputs: competition/spread/cointegration_report.json + stdout summary.
Sends Telegram alert if any RETIRE pairs are found.
"""

import json, math, os, sys
from datetime import datetime, timezone

import numpy as np

WORKSPACE    = "/root/.openclaw/workspace"
PRICE_DIR    = os.path.join(WORKSPACE, "competition", "swing", "price_history")
REPORT_PATH  = os.path.join(WORKSPACE, "competition", "spread", "cointegration_report.json")
SPRINT_HOURS = 168   # 7-day sprints
LOOKBACK     = 720   # candles (30 days of hourly data)

# Current active ratio pairs
ACTIVE_PAIRS = {
    "ETH_BTC_RATIO":   ("ETH/USD", "BTC/USD"),
    "SOL_ETH_RATIO":   ("SOL/USD", "ETH/USD"),
    "SOL_BTC_RATIO":   ("SOL/USD", "BTC/USD"),
    "AVAX_ETH_RATIO":  ("AVAX/USD", "ETH/USD"),
    "AVAX_SOL_RATIO":  ("AVAX/USD", "SOL/USD"),
    "LINK_ETH_RATIO":  ("LINK/USD", "ETH/USD"),
    "AAVE_ETH_RATIO":  ("AAVE/USD", "ETH/USD"),
    "AAVE_LINK_RATIO": ("AAVE/USD", "LINK/USD"),
}

# All assets available in price_history
ALL_ASSETS = ["BTC", "ETH", "SOL", "AVAX", "LINK", "AAVE", "DOGE", "XRP",
              "NEAR", "APT", "ARB", "OP", "SUI", "WIF"]

THRESHOLDS = {
    "min_corr":         0.65,
    "max_half_life":    120,    # hours -- must revert within ~5 days
    "max_hurst":        0.50,   # H < 0.5 = mean-reverting tendency
    "retire_half_life": SPRINT_HOURS,
}


# -- Data loading --------------------------------------------------------------

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


def align_series(a_prices, b_prices):
    n = min(len(a_prices), len(b_prices))
    return np.array(a_prices[-n:]), np.array(b_prices[-n:])


# -- Statistical tests ---------------------------------------------------------

def pearson_corr(x, y):
    if len(x) < 30:
        return None
    lx = np.diff(np.log(x + 1e-12))
    ly = np.diff(np.log(y + 1e-12))
    if np.std(lx) == 0 or np.std(ly) == 0:
        return 0.0
    return float(np.corrcoef(lx, ly)[0, 1])


def half_life(ratio):
    """
    Half-life of mean reversion via AR(1) OLS.
    Regress delta_ratio(t) on ratio(t-1): dy = lambda * y_{t-1} + const
    Half-life = -ln(2) / lambda  (lambda must be negative)
    """
    if len(ratio) < 30:
        return None
    y   = ratio[1:]
    y_l = ratio[:-1]
    dy  = y - y_l
    X   = np.column_stack([y_l, np.ones(len(y_l))])
    try:
        coef, _, _, _ = np.linalg.lstsq(X, dy, rcond=None)
        lam = coef[0]
    except Exception:
        return None
    if lam >= 0:
        return None  # non-mean-reverting
    hl = -math.log(2) / lam
    return round(hl, 1) if hl > 0 else None


def hurst_exponent(series):
    """
    Variance ratio method. H < 0.5 = mean-reverting.
    """
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
    n    = len(log_lags)
    xm   = sum(log_lags) / n
    ym   = sum(log_vars) / n
    num  = sum((x - xm) * (y - ym) for x, y in zip(log_lags, log_vars))
    den  = sum((x - xm) ** 2 for x in log_lags)
    if den == 0:
        return None
    H = (num / den) / 2.0
    return round(H, 3)


def ratio_volatility(ratio):
    if len(ratio) < 10:
        return None
    return round(float(np.std(ratio) / np.mean(ratio)), 4)


# -- Scoring -------------------------------------------------------------------

def score_pair(base_asset, quote_asset):
    a_sym    = base_asset.replace("/USD", "")
    b_sym    = quote_asset.replace("/USD", "")
    a_prices = load_closes(a_sym)
    b_prices = load_closes(b_sym)

    if len(a_prices) < 50 or len(b_prices) < 50:
        return {"error": "insufficient_data"}

    a, b  = align_series(a_prices, b_prices)
    ratio = a / b

    corr  = pearson_corr(a, b)
    hl    = half_life(ratio)
    hurst = hurst_exponent(ratio)
    vol   = ratio_volatility(ratio)

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
    if n_issues == 0:
        verdict = "STRONG"
    elif n_issues == 1:
        verdict = "WATCH"
    elif n_issues == 2:
        verdict = "WEAK"
    else:
        verdict = "RETIRE"
    if hl is not None and hl > THRESHOLDS["retire_half_life"]:
        verdict = "RETIRE"
    if hl is None and (corr is None or corr < THRESHOLDS["min_corr"]):
        verdict = "RETIRE"

    # Composite score -- lower = stronger pair
    corr_score  = max(0.0, (1.0 - (corr or 0.0)) * 30)
    hl_norm     = (hl or 999) / THRESHOLDS["max_half_life"]
    hl_score    = min(40.0, hl_norm * 40) if hl else 40.0
    hurst_score = max(0.0, ((hurst or 0.5) - 0.3) / 0.2 * 30) if hurst else 15.0
    composite   = round(corr_score + hl_score + hurst_score, 1)

    return {
        "base":      base_asset,
        "quote":     quote_asset,
        "candles":   len(ratio),
        "corr":      round(corr, 3) if corr is not None else None,
        "half_life": hl,
        "hurst":     hurst,
        "vol_cv":    vol,
        "issues":    issues,
        "verdict":   verdict,
        "score":     composite,
    }



# -- Main ----------------------------------------------------------------------

def run():
    ts = datetime.now(timezone.utc).isoformat()
    print(chr(10) + chr(61)*60)
    print(f"  SPREAD COINTEGRATION CHECK  |  {ts[:16]} UTC")
    print(chr(61)*60 + chr(10))

    active_results = {}
    print("ACTIVE PAIRS" + chr(10) + chr(45)*60)
    for ratio_name, (base, quote) in ACTIVE_PAIRS.items():
        r = score_pair(base, quote)
        active_results[ratio_name] = r
        err = r.get("error")
        if err:
            print(f"  {ratio_name:<22}  ERROR: {err}")
            continue
        corr_v  = r.get("corr")
        hl_v    = r.get("half_life")
        hurst_v = r.get("hurst")
        vol_v   = r.get("vol_cv")
        verdict = r.get("verdict", "")
        issues  = r.get("issues", [])
        corr_s  = f"{corr_v:.3f}"  if corr_v  is not None else " N/A"
        hl_s    = f"{hl_v:.0f}h" if hl_v    is not None else " N/A"
        hurst_s = f"{hurst_v:.3f}" if hurst_v is not None else " N/A"
        vol_s   = f"{vol_v:.4f}" if vol_v   is not None else " N/A"
        flag    = "  *** RETIRE ***" if verdict == "RETIRE"              else "  ! WEAK"         if verdict == "WEAK"   else ""
        print(f"  {ratio_name:<22}  [{verdict:<7}]  corr={corr_s}  hl={hl_s:>7}  H={hurst_s}  cv={vol_s}{flag}")
        if issues:
            print(f"    issues: {', '.join(issues)}")

    active_set = set()
    for base, quote in ACTIVE_PAIRS.values():
        a = base.replace("/USD", "")
        b = quote.replace("/USD", "")
        active_set.add((a, b))
        active_set.add((b, a))

    assets     = [a for a in ALL_ASSETS
                  if os.path.exists(os.path.join(PRICE_DIR, f"{a}-USD.json"))]
    candidates = []
    for i, a in enumerate(assets):
        for b in assets[i+1:]:
            if (a, b) in active_set:
                continue
            r = score_pair(f"{a}/USD", f"{b}/USD")
            if "error" not in r:
                candidates.append(r)

    candidates.sort(key=lambda x: x["score"])

    print(chr(10) + "CANDIDATE REPLACEMENTS (top 10 by composite score)" + chr(10) + chr(45)*60)
    for r in candidates[:10]:
        base_s  = r.get("base",  "").replace("/USD", "")
        quote_s = r.get("quote", "").replace("/USD", "")
        pair_s  = f"{base_s}/{quote_s}"
        corr_v  = r.get("corr")
        hl_v    = r.get("half_life")
        hurst_v = r.get("hurst")
        verdict = r.get("verdict", "")
        score_v = r.get("score", 0)
        corr_s  = f"{corr_v:.3f}"       if corr_v  is not None else " N/A"
        hl_s    = f"{hl_v:.0f}h" if hl_v    is not None else " N/A"
        hurst_s = f"{hurst_v:.3f}"      if hurst_v is not None else " N/A"
        print(f"  {pair_s:<14}  [{verdict:<7}]  corr={corr_s}  hl={hl_s:>7}  H={hurst_s}  score={score_v:.1f}")

    retire = [k for k, v in active_results.items() if v.get("verdict") == "RETIRE"]
    weak   = [k for k, v in active_results.items() if v.get("verdict") == "WEAK"]
    watch  = [k for k, v in active_results.items() if v.get("verdict") == "WATCH"]
    strong = [k for k, v in active_results.items() if v.get("verdict") == "STRONG"]

    print(chr(10) + "SUMMARY" + chr(10) + chr(45)*60)
    print(f"  STRONG:{len(strong)}  WATCH:{len(watch)}  WEAK:{len(weak)}  RETIRE:{len(retire)}")
    if retire:
        print(f"  ACTION REQUIRED -- retire: {', '.join(retire)}")
        top_repl = []
        for r in candidates[:len(retire)]:
            b = r.get("base",  "").replace("/USD", "")
            q = r.get("quote", "").replace("/USD", "")
            top_repl.append(f"{b}/{q}")
        print(f"  Suggested replacements: {', '.join(top_repl)}")

    report = {
        "generated_at": ts,
        "active_pairs": active_results,
        "candidates":   candidates[:20],
        "summary": {
            "strong": strong, "watch": watch,
            "weak": weak, "retire": retire,
        },
        "thresholds": THRESHOLDS,
    }
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(chr(10) + f"  Report saved: {REPORT_PATH}" + chr(10))

    # Telegram alert
    try:
        import urllib.request as _ur
        BOT_TOKEN = "8491792848:AAEPeXKViSH6eBAtbjYxi77DIGfzwtdiYkY"
        CHAT_ID   = "8154505910"
        tok = BOT_TOKEN; cid = CHAT_ID

        lines = ["*Spread League: Pair Health Check*\n"]

        if retire:
            lines.append("*ACTION NOW — RETIRE these pairs (half-life > sprint):*")
            for k in retire:
                r = active_results[k]
                lines.append(f"  RETIRE: `{k}` — {', '.join(r.get('issues', []))}")
            repl = [f"{r['base'].replace('/USD', '')}/{r['quote'].replace('/USD', '')}"
                    for r in candidates[:len(retire)]]
            lines.append(f"  Replace with: {', '.join(repl)}")

        if weak:
            lines.append("\n*WATCH — review at cycle end:*")
            for k in weak:
                r = active_results[k]
                lines.append(f"  WEAK: `{k}` — {', '.join(r.get('issues', []))}")

        if not retire and not weak:
            lines.append(f"All {len(strong)} active pairs healthy.")

        lines.append(f"\nSTRONG:{len(strong)}  WATCH:{len(watch)}  WEAK:{len(weak)}  RETIRE:{len(retire)}")

        msg  = "\n".join(lines)
        import urllib.request
        url  = f"https://api.telegram.org/bot{tok}/sendMessage"
        data = json.dumps({"chat_id": cid, "text": msg, "parse_mode": "Markdown"}).encode()
        req  = urllib.request.Request(url, data=data,
                                      headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
        print("  Telegram alert sent." + chr(10))
    except Exception as e:
        print(f"  Telegram alert failed: {e}" + chr(10))

    return report


if __name__ == "__main__":
    run()
