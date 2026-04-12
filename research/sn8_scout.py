#!/usr/bin/env python3
"""
sn8_scout.py — Read-only research tool for Bittensor SN8 (Proprietary Trading Network)

Probes public APIs to assess:
  1. What SN8 data is accessible without installing the bittensor SDK
  2. Whether top-miner signals show predictive quality against our OHLCV data
  3. Whether integration is worth pursuing

Usage:
  python3 /root/.openclaw/workspace/research/sn8_scout.py
  python3 /root/.openclaw/workspace/research/sn8_scout.py --days 14
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

WORKSPACE   = "/root/.openclaw/workspace"
DATA_DIR    = os.path.join(WORKSPACE, "research", "data")
REPORT_PATH = os.path.join(WORKSPACE, "research", "sn8_report.json")

SN8_NETUID = 8

# -----------------------------------------------------------------------
# API probing
# -----------------------------------------------------------------------

def fetch_json(url, timeout=15, headers=None):
    """Return (parsed_data, error_string). One of them will be None."""
    hdrs = {"User-Agent": "sn8-scout/1.0", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"URLError: {e.reason}"
    except json.JSONDecodeError as e:
        return None, f"JSONDecodeError: {e}"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def probe_taostats():
    """
    taostats.io public REST API — no auth required.
    Docs: https://api.taostats.io/docs
    Returns miner trust scores, emission rates, stake for SN8.
    """
    base = "https://api.taostats.io/api"
    endpoints = {
        "subnet":    f"{base}/subnet?netuid={SN8_NETUID}",
        "metagraph": f"{base}/metagraph/latest?netuid={SN8_NETUID}&limit=50",
    }
    results = {}
    for name, url in endpoints.items():
        data, err = fetch_json(url)
        results[name] = {"url": url, "ok": data is not None, "data": data, "error": err}
    return results


def probe_taoshi_ptn():
    """
    Taoshi runs SN8. They expose a public REST API for PTN signal data.
    Trying known endpoints — the API may require auth for live signals.
    """
    base = "https://api.taoshi.io"
    endpoints = {
        "v1_signals":       f"{base}/v1/signals",
        "v1_miners":        f"{base}/v1/miners",
        "v1_leaderboard":   f"{base}/v1/leaderboard",
        "signals":          f"{base}/signals",
        "request_network":  f"{base}/request-network/v1/signals",
    }
    results = {}
    for name, url in endpoints.items():
        data, err = fetch_json(url)
        results[name] = {"url": url, "ok": data is not None, "data": data, "error": err}
    return results


def probe_subtensor():
    """
    Opentensor Foundation exposes a public REST shim over their blockchain.
    Useful for reading metagraph state directly without the SDK.
    """
    endpoints = {
        "finney_metagraph": f"https://api.taostats.io/api/metagraph/latest?netuid={SN8_NETUID}",
    }
    results = {}
    for name, url in endpoints.items():
        data, err = fetch_json(url)
        results[name] = {"url": url, "ok": data is not None, "data": data, "error": err}
    return results


# -----------------------------------------------------------------------
# OHLCV helpers
# -----------------------------------------------------------------------

def load_ohlcv(pair, timeframe="5m", days=7):
    symbol = pair.replace("/", "_")
    path   = os.path.join(DATA_DIR, f"{symbol}_{timeframe}.csv")
    if not os.path.exists(path):
        return []
    cutoff_ms = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp() * 1000)
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ts = int(row["timestamp"])
            if ts >= cutoff_ms:
                rows.append({
                    "ts":    ts,
                    "open":  float(row["open"]),
                    "high":  float(row["high"]),
                    "low":   float(row["low"]),
                    "close": float(row["close"]),
                })
    return rows


# -----------------------------------------------------------------------
# Signal quality analysis
# -----------------------------------------------------------------------

def analyze_signals(signals, ohlcv_map, forward_candles=12):
    """
    signals: list of {pair, direction ("long"/"short"/"flat"), timestamp_ms}
    ohlcv_map: dict pair -> sorted list of OHLCV rows
    forward_candles: how many 5m candles ahead to measure (12 = 1 hour)

    Returns a dict with win rate, avg returns, and per-direction breakdowns.
    """
    long_rets, short_rets = [], []
    skipped = flat = 0

    for sig in signals:
        pair      = sig.get("pair", "BTC/USD")
        direction = str(sig.get("direction", "flat")).lower()
        ts        = sig.get("timestamp_ms", 0)

        if direction == "flat":
            flat += 1
            continue

        candles = ohlcv_map.get(pair, [])
        # binary search for entry candle
        entry_idx = None
        for i, c in enumerate(candles):
            if c["ts"] >= ts:
                entry_idx = i
                break

        if entry_idx is None or entry_idx + forward_candles >= len(candles):
            skipped += 1
            continue

        entry = candles[entry_idx]["close"]
        exit_ = candles[entry_idx + forward_candles]["close"]
        pct   = (exit_ - entry) / entry * 100

        if direction == "long":
            long_rets.append(pct)
        elif direction == "short":
            short_rets.append(-pct)   # profit when price falls

    def stats(rets):
        if not rets:
            return None
        wins = sum(1 for r in rets if r > 0)
        return {
            "count":    len(rets),
            "win_rate": round(wins / len(rets), 4),
            "avg_ret":  round(sum(rets) / len(rets), 4),
            "best":     round(max(rets), 4),
            "worst":    round(min(rets), 4),
        }

    total_analyzed = len(long_rets) + len(short_rets)
    total_wins     = sum(1 for r in long_rets + short_rets if r > 0)

    return {
        "total_signals":  len(signals),
        "flat":           flat,
        "skipped":        skipped,
        "analyzed":       total_analyzed,
        "overall_win_rate": round(total_wins / total_analyzed, 4) if total_analyzed else None,
        "long":           stats(long_rets),
        "short":          stats(short_rets),
        "forward_window": f"{forward_candles * 5}m",
    }


# -----------------------------------------------------------------------
# Metagraph summary helpers
# -----------------------------------------------------------------------

def summarize_metagraph(data):
    """Pull top-10 miners by trust from raw taostats metagraph response."""
    # taostats returns either list or {"data": [...]}
    rows = data if isinstance(data, list) else data.get("data", [])
    if not rows:
        return []

    miners = []
    for r in rows:
        trust    = float(r.get("trust", r.get("validator_trust", 0)) or 0)
        emission = float(r.get("emission", 0) or 0)
        stake    = float(r.get("stake", 0) or 0)
        uid      = r.get("uid", r.get("hotkey", "?"))
        miners.append({"uid": uid, "trust": trust, "emission": emission, "stake": stake})

    miners.sort(key=lambda m: m["trust"], reverse=True)
    return miners[:10]


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SN8 scout — no bittensor SDK required")
    parser.add_argument("--days", type=int, default=7, help="Days of OHLCV data to analyze")
    args = parser.parse_args()

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "days_analyzed": args.days,
        "api_access": {},
        "top_miners": [],
        "signal_analysis": None,
        "recommendation": "",
        "next_steps": [],
    }

    print("=" * 58)
    print("SN8 Scout — Bittensor Proprietary Trading Network")
    print("=" * 58)

    # ---- 1. taostats ----
    print("\n[1/3] taostats API (subnet metagraph)...")
    ts_results = probe_taostats()
    report["api_access"]["taostats"] = {}
    for name, r in ts_results.items():
        status = "OK" if r["ok"] else f"FAIL ({r['error']})"
        print(f"  {name:20s} {status}")
        report["api_access"]["taostats"][name] = {"ok": r["ok"], "error": r["error"]}

        if r["ok"] and name == "metagraph" and r["data"]:
            top = summarize_metagraph(r["data"])
            report["top_miners"] = top
            if top:
                print(f"  Top miners by trust:")
                for m in top[:5]:
                    print(f"    uid={m['uid']}  trust={m['trust']:.4f}  emission={m['emission']:.4f}")

    # ---- 2. Taoshi PTN API ----
    print("\n[2/3] Taoshi PTN API (live signals)...")
    ptn_results = probe_taoshi_ptn()
    report["api_access"]["taoshi_ptn"] = {}
    signal_data = None
    for name, r in ptn_results.items():
        status = "OK" if r["ok"] else f"FAIL ({r['error']})"
        print(f"  {name:24s} {status}")
        report["api_access"]["taoshi_ptn"][name] = {"ok": r["ok"], "error": r["error"]}
        if r["ok"] and r["data"] and signal_data is None:
            signal_data = r["data"]
            print(f"    --> Got data from {name}")

    # ---- 3. Signal quality analysis ----
    print("\n[3/3] Signal quality analysis...")
    if signal_data:
        # Normalize to our format
        raw = signal_data if isinstance(signal_data, list) else signal_data.get("data", [])
        signals = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            pair = (item.get("trade_pair") or item.get("pair") or "BTC/USD").replace("-", "/")
            direction = str(item.get("signal") or item.get("direction") or "flat").lower()
            ts_ms = int(item.get("timestamp") or item.get("ts") or time.time() * 1000)
            signals.append({"pair": pair, "direction": direction, "timestamp_ms": ts_ms})

        if signals:
            pairs_needed = set(s["pair"] for s in signals)
            ohlcv_map = {}
            for pair in pairs_needed:
                data = load_ohlcv(pair, days=args.days)
                if data:
                    ohlcv_map[pair] = data

            analysis = analyze_signals(signals, ohlcv_map)
            report["signal_analysis"] = analysis
            print(f"  Total signals:   {analysis['total_signals']}")
            print(f"  Analyzed:        {analysis['analyzed']}")
            if analysis["overall_win_rate"] is not None:
                print(f"  Win rate (1h):   {analysis['overall_win_rate']:.1%}")
            if analysis["long"]:
                print(f"  Long avg return: {analysis['long']['avg_ret']:+.3f}%")
            if analysis["short"]:
                print(f"  Short avg return:{analysis['short']['avg_ret']:+.3f}%")
        else:
            print("  Signal data received but no parseable entries.")
            report["signal_analysis"] = {"note": "Unparseable format", "raw_type": str(type(raw))}
    else:
        print("  No signal data from public APIs — auth likely required.")
        report["signal_analysis"] = {
            "note": "No public unauthenticated signal endpoint found.",
            "implication": "Taoshi PTN signals require API key or validator stake.",
        }

    # ---- Recommendation ----
    taostats_ok = any(r["ok"] for r in ts_results.values())
    taoshi_ok   = any(r["ok"] for r in ptn_results.values())
    sig_analysis = report["signal_analysis"] or {}
    win_rate = sig_analysis.get("overall_win_rate")

    if win_rate and win_rate > 0.55:
        rec = (
            f"SN8 signals show meaningful edge ({win_rate:.1%} win rate 1h forward). "
            "Build a signal ingestion layer and run a 30-day shadow comparison against your day bots."
        )
        next_steps = [
            "Obtain Taoshi PTN API key (api.taoshi.io)",
            "Build sn8_signal_feeder.py: poll signals every 5m, write to local cache",
            "Add SN8 consensus signal as a feature input to ODIN's strategy optimizer",
            "Shadow-trade for 30 days before live use",
        ]
    elif taoshi_ok and signal_data:
        rec = (
            f"SN8 data accessible but signals show no clear edge ({win_rate:.1%} win rate). "
            "Not worth integrating now. Re-evaluate in 60 days."
        )
        next_steps = ["Set calendar reminder to re-run this scout in 60 days."]
    elif taostats_ok:
        rec = (
            "Metagraph accessible (miner trust/emission rankings). "
            "Signal data requires Taoshi API key or bittensor SDK with validator stake. "
            "Metagraph alone useful for subnet participation cost analysis."
        )
        next_steps = [
            "Request Taoshi PTN API key at api.taoshi.io (free tier may exist)",
            "OR: pip3 install bittensor (500MB) to query signals via SDK",
            "Re-run this scout after gaining access to signal endpoints",
        ]
    else:
        rec = (
            "No public APIs reachable. Check network/firewall, then consider: "
            "pip3 install bittensor for direct on-chain access."
        )
        next_steps = [
            "Verify VPS can reach api.taostats.io (curl test)",
            "pip3 install bittensor if taostats unreachable",
        ]

    report["recommendation"] = rec
    report["next_steps"]     = next_steps

    print("\n" + "-" * 58)
    print("RECOMMENDATION:")
    print(f"  {rec}")
    print("\nNEXT STEPS:")
    for i, s in enumerate(next_steps, 1):
        print(f"  {i}. {s}")
    print("-" * 58)

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nFull report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
