#!/usr/bin/env python3
"""
sn8_scout.py — Read-only research tool for Bittensor SN8 (Proprietary Trading Network)

Queries Bittensor chain directly via substrate-interface (no SDK, no stake required).
Reports miner/validator rankings, economics, and integration recommendation.

Usage:
  python3 /root/.openclaw/workspace/research/sn8_scout.py
  python3 /root/.openclaw/workspace/research/sn8_scout.py --top 20
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

WORKSPACE   = "/root/.openclaw/workspace"
REPORT_PATH = os.path.join(WORKSPACE, "research", "sn8_report.json")

SN8_NETUID    = 8
SCALE_U16     = 65535.0
RAO_PER_TAO   = 1_000_000_000
BLOCKS_PER_SEC = 12
FINNEY_ENDPOINTS = [
    "wss://entrypoint-finney.opentensor.ai:443",
    "wss://bittensor-finney.api.onfinality.io/public-ws",
]


def connect():
    from substrateinterface import SubstrateInterface
    for ep in FINNEY_ENDPOINTS:
        try:
            print(f"  Connecting {ep} ...", end=" ", flush=True)
            si = SubstrateInterface(url=ep, ss58_format=42, use_remote_preset=True)
            print("OK")
            return si, ep
        except Exception as e:
            print(f"FAIL ({e})")
    raise ConnectionError("All Bittensor endpoints failed.")


def fetch_array(si, field, netuid):
    """Fetch a per-neuron array field (stored as Map<netuid> -> Vec<u16|u64>)."""
    try:
        result = si.query("SubtensorModule", field, [netuid])
        return result.value or []
    except Exception:
        return []


def fetch_scalar(si, field, netuid):
    try:
        result = si.query("SubtensorModule", field, [netuid])
        return result.value
    except Exception:
        return None


def build_metagraph(si, netuid):
    """Return list of neuron dicts and epoch metadata."""
    n        = fetch_scalar(si, "SubnetworkN",    netuid) or 0
    burn_rao = fetch_scalar(si, "Burn",           netuid) or 0
    tempo    = fetch_scalar(si, "Tempo",           netuid) or 360

    incentive = fetch_array(si, "Incentive",      netuid)
    emission  = fetch_array(si, "Emission",       netuid)
    consensus = fetch_array(si, "Consensus",      netuid)
    vtrust    = fetch_array(si, "ValidatorTrust", netuid)
    dividends = fetch_array(si, "Dividends",      netuid)
    v_permit  = fetch_array(si, "ValidatorPermit",netuid)

    neurons = []
    for uid in range(n):
        is_v = bool(v_permit[uid]) if uid < len(v_permit) else False
        neurons.append({
            "uid":        uid,
            "incentive":  incentive[uid] / SCALE_U16 if uid < len(incentive)  else 0.0,
            "emission":   emission[uid]              if uid < len(emission)   else 0,
            "consensus":  consensus[uid] / SCALE_U16 if uid < len(consensus)  else 0.0,
            "vtrust":     vtrust[uid]    / SCALE_U16 if uid < len(vtrust)     else 0.0,
            "dividends":  dividends[uid] / SCALE_U16 if uid < len(dividends)  else 0.0,
            "is_validator": is_v,
        })

    return neurons, {
        "n_neurons":    n,
        "burn_rao":     burn_rao,
        "burn_tao":     burn_rao / RAO_PER_TAO,
        "tempo_blocks": tempo,
        "epoch_seconds": tempo * BLOCKS_PER_SEC,
        "epochs_per_day": round(86400 / (tempo * BLOCKS_PER_SEC), 2),
    }


def analyze(neurons, epoch_meta):
    """Split miners vs validators, compute emission economics."""
    miners     = sorted([n for n in neurons if not n["is_validator"] and n["emission"] > 0],
                        key=lambda x: x["incentive"], reverse=True)
    validators = sorted([n for n in neurons if n["is_validator"]],
                        key=lambda x: x["dividends"], reverse=True)

    total_emission_rao = sum(n["emission"] for n in neurons)
    miner_emission_rao = sum(n["emission"] for n in neurons if not n["is_validator"])

    epd = epoch_meta["epochs_per_day"]
    avg_miner_rao = (miner_emission_rao / len(miners)) if miners else 0

    top5_incentive = [m["incentive"] for m in miners[:5]]
    top5_share     = sum(m["emission"] for m in miners[:5]) / miner_emission_rao if miner_emission_rao else 0

    return {
        "miners":             miners,
        "validators":         validators,
        "n_active_miners":    len(miners),
        "n_validators":       len(validators),
        "total_emission_tao": total_emission_rao / RAO_PER_TAO,
        "miner_pool_tao":     miner_emission_rao / RAO_PER_TAO,
        "miner_pool_daily_tao": (miner_emission_rao / RAO_PER_TAO) * epd,
        "avg_miner_epoch_tao":  avg_miner_rao / RAO_PER_TAO,
        "avg_miner_daily_tao":  (avg_miner_rao / RAO_PER_TAO) * epd,
        "top_miner_epoch_tao":  miners[0]["emission"] / RAO_PER_TAO if miners else 0,
        "top_miner_daily_tao":  (miners[0]["emission"] / RAO_PER_TAO) * epd if miners else 0,
        "top5_emission_share":  round(top5_share, 4),
        "burn_recovery_days_avg": epoch_meta["burn_tao"] / ((avg_miner_rao / RAO_PER_TAO) * epd) if avg_miner_rao > 0 else 999,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=15)
    args = parser.parse_args()

    print("=" * 62)
    print("SN8 Scout — Bittensor Proprietary Trading Network (Taoshi)")
    print("=" * 62)

    print("\n[1/3] Connecting to Bittensor chain...")
    try:
        si, ep = connect()
    except ConnectionError as e:
        print(f"FATAL: {e}")
        return 1

    print("\n[2/3] Querying SN8 metagraph...")
    neurons, epoch_meta = build_metagraph(si, SN8_NETUID)
    stats = analyze(neurons, epoch_meta)

    miners     = stats["miners"]
    validators = stats["validators"]

    # ---- Print subnet overview ----
    print(f"\n  Subnet stats:")
    print(f"    Total neuron slots:   {epoch_meta['n_neurons']}")
    print(f"    Active miners:        {stats['n_active_miners']}")
    print(f"    Validators:           {stats['n_validators']}")
    print(f"    Inactive slots:       {epoch_meta['n_neurons'] - stats['n_active_miners'] - stats['n_validators']}")
    print(f"    Registration cost:    {epoch_meta['burn_tao']:.4f} TAO")
    print(f"    Tempo:                {epoch_meta['tempo_blocks']} blocks ({epoch_meta['epoch_seconds']/60:.0f} min/epoch)")
    print(f"    Epochs per day:       {epoch_meta['epochs_per_day']}")

    print(f"\n  Emission economics (NOTE: Dynamic TAO — values in subnet alpha tokens):")
    print(f"    Total SN8 per epoch:  {stats['total_emission_tao']:.4f} TAO-alpha")
    print(f"    Miner pool per epoch: {stats['miner_pool_tao']:.4f} TAO-alpha")
    print(f"    Miner pool per day:   {stats['miner_pool_daily_tao']:.4f} TAO-alpha")
    print(f"    Top miner per day:    {stats['top_miner_daily_tao']:.4f} TAO-alpha")
    print(f"    Avg active miner/day: {stats['avg_miner_daily_tao']:.4f} TAO-alpha")
    print(f"    Top 5 miner share:    {stats['top5_emission_share']:.1%} of miner pool")
    print(f"    Days to recover reg:  {stats['burn_recovery_days_avg']:.2f} (avg miner)")

    # ---- Miner leaderboard ----
    print(f"\n  Top {min(args.top, len(miners))} miners by incentive:")
    print(f"  {'UID':>5} {'Incentive':>10} {'Consensus':>10} {'Epoch emission':>16}")
    print(f"  {'-'*5} {'-'*10} {'-'*10} {'-'*16}")
    for m in miners[:args.top]:
        em_tao = m["emission"] / RAO_PER_TAO
        print(f"  {m['uid']:>5} {m['incentive']:>10.4f} {m['consensus']:>10.4f} {em_tao:>14.4f} a")

    # ---- Validator leaderboard ----
    print(f"\n  Top validators (earn dividends, not incentive):")
    print(f"  {'UID':>5} {'Dividends':>10} {'VTrust':>8} {'Epoch emission':>16}")
    for v in validators[:5]:
        em_tao = v["emission"] / RAO_PER_TAO
        print(f"  {v['uid']:>5} {v['dividends']:>10.4f} {v['vtrust']:>8.4f} {em_tao:>14.4f} a")

    # ---- Competition assessment ----
    print("\n[3/3] Integration assessment...")

    # Competitiveness: how concentrated is incentive at top?
    if stats["top5_emission_share"] > 0.8:
        competition = "EXTREME — top 5 take {:.0%} of miner pool. Everyone else earns near-zero.".format(
            stats["top5_emission_share"])
    elif stats["top5_emission_share"] > 0.5:
        competition = "HIGH — top 5 take {:.0%} of miner pool. Mid-tier earns modestly.".format(
            stats["top5_emission_share"])
    else:
        competition = "MODERATE — emission distributed more evenly."

    # Economics verdict
    if stats["burn_recovery_days_avg"] < 1:
        econ = "Entry cost negligible ({:.4f} TAO). Recoverable in <1 day at avg rank.".format(
            epoch_meta["burn_tao"])
    elif stats["burn_recovery_days_avg"] < 7:
        econ = "Entry cost recoverable in ~{:.1f} days at average rank.".format(
            stats["burn_recovery_days_avg"])
    else:
        econ = "Entry cost takes {:.0f}+ days to recover at average rank.".format(
            stats["burn_recovery_days_avg"])

    rec = (
        "Registration is dirt cheap ({:.4f} TAO). However: only {} of 256 slots are "
        "active miners, and the top 5 take {:.0%} of the miner pool. The remaining "
        "{} miners share barely {:.4f} TAO-alpha/day. Your day bots are not yet "
        "Kraken-validated — submitting to SN8 before Phase 2 is premature. "
        "Signal ingestion (using SN8 outputs as inputs) requires Taoshi API access "
        "— no free public endpoint exists. Recommended: wait for Phase 2 validation, "
        "then evaluate SN8 entry with a proven live-performance bot."
    ).format(
        epoch_meta["burn_tao"],
        stats["n_active_miners"],
        stats["top5_emission_share"],
        stats["n_active_miners"] - 5,
        stats["miner_pool_daily_tao"] * (1 - stats["top5_emission_share"]),
    )

    next_steps = [
        "Complete Phase 2 Kraken validation — SN8 entry only makes sense with a live-proven bot",
        "Request Taoshi PTN API key (https://docs.taoshi.io) to consume SN8 signals as input",
        "Re-run this scout weekly to track competition/emission changes: "
        "python3 /root/.openclaw/workspace/research/sn8_scout.py",
        "If Taoshi API key obtained: build sn8_signal_feeder.py to shadow-trade against your bots",
        "Watch burn cost — currently {:.4f} TAO (very cheap). Enter during low-cost windows.".format(
            epoch_meta["burn_tao"]),
    ]

    print(f"\n  Competition: {competition}")
    print(f"  Economics:   {econ}")

    print("\n" + "=" * 62)
    print("RECOMMENDATION:")
    for line in rec.split(". "):
        if line:
            print("  " + line.strip() + ".")
    print("\nNEXT STEPS:")
    for i, s in enumerate(next_steps, 1):
        print(f"  {i}. {s}")
    print("=" * 62)

    # Save report
    report = {
        "generated_utc":   datetime.now(timezone.utc).isoformat(),
        "subnet":          "SN8 — Proprietary Trading Network (Taoshi)",
        "chain_endpoint":  ep,
        "epoch_meta":      epoch_meta,
        "stats":           {k: v for k, v in stats.items() if k not in ("miners", "validators")},
        "top_miners":      [{"uid": m["uid"], "incentive": m["incentive"],
                             "consensus": m["consensus"],
                             "emission_tao": m["emission"]/RAO_PER_TAO}
                            for m in miners[:20]],
        "top_validators":  [{"uid": v["uid"], "dividends": v["dividends"],
                             "vtrust": v["vtrust"],
                             "emission_tao": v["emission"]/RAO_PER_TAO}
                            for v in validators[:5]],
        "competition":     competition,
        "economics":       econ,
        "recommendation":  rec,
        "next_steps":      next_steps,
    }
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nFull report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
