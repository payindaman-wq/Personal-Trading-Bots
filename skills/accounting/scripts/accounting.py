#!/usr/bin/env python3
"""
Accounting Bot — Fleet trade ledger, cost basis tracking, tax reporting.

Records every trade executed by any fleet bot, computes realized gains/losses
using FIFO cost basis, routes profits to tax/operating/reinvestment reserves,
and generates IRS Form 8949-compatible output.

Usage:
  accounting.py init
  accounting.py record --bot <n> --pair <p> --side <BUY|SELL> --qty <q> --price <p> --fee <f>
  accounting.py reserves
  accounting.py daily [--date YYYY-MM-DD]
  accounting.py export 8949 [--year YYYY]
  accounting.py export summary [--year YYYY]
  accounting.py export ledger
  accounting.py wash-sales [--year YYYY]
  accounting.py config [--set key=value]
"""

import json
import csv
import uuid
import os
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- Base paths ---
WORKSPACE = Path(os.environ.get("WORKSPACE", "/root/.openclaw/workspace"))
ACCOUNTING_DIR = WORKSPACE / "competition" / "accounting"
TAX_DIR = WORKSPACE / "tax"

LEDGER_FILE    = ACCOUNTING_DIR / "ledger.json"
OPEN_LOTS_FILE = ACCOUNTING_DIR / "open_lots.json"
RESERVES_FILE  = ACCOUNTING_DIR / "reserves.json"
CONFIG_FILE    = ACCOUNTING_DIR / "config.json"

# --- Defaults ---
DEFAULT_CONFIG = {
    "tax_reserve_pct":        0.30,   # 30% of net gain → tax reserve
    "operating_reserve_pct":  0.10,   # 10% of net gain → operating buffer
    "reinvestment_pct":       0.60,   # 60% of net gain → back into competition pool
    "default_tax_rate":       0.37,   # assumed federal bracket (short-term)
    "cost_basis_method":      "FIFO",
    "exchange":               "Kraken",
    "wash_sale_window_days":  30,
}

DEFAULT_RESERVES = {
    "tax_reserve":                   0.0,
    "operating_reserve":             0.0,
    "reinvestment_pool":             0.0,
    "lifetime_gains":                0.0,
    "lifetime_losses":               0.0,
    "total_contributed_to_tax":      0.0,
    "total_contributed_to_operating": 0.0,
    "last_updated":                  None,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_dirs():
    ACCOUNTING_DIR.mkdir(parents=True, exist_ok=True)
    TAX_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default() if callable(default) else default


def _save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, default=str))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_dt(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def load_config()    -> dict: return _load_json(CONFIG_FILE,    dict(DEFAULT_CONFIG))
def load_ledger()    -> list: return _load_json(LEDGER_FILE,    list)
def load_open_lots() -> dict: return _load_json(OPEN_LOTS_FILE, dict)
def load_reserves()  -> dict:
    d = _load_json(RESERVES_FILE, dict(DEFAULT_RESERVES))
    for k, v in DEFAULT_RESERVES.items():
        d.setdefault(k, v)
    return d


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_init(args):
    _ensure_dirs()
    created = []
    for path, default in [
        (CONFIG_FILE,    DEFAULT_CONFIG),
        (LEDGER_FILE,    []),
        (OPEN_LOTS_FILE, {}),
        (RESERVES_FILE,  DEFAULT_RESERVES),
    ]:
        if not path.exists():
            _save_json(path, default)
            created.append(str(path))

    print(json.dumps({
        "status":          "ok",
        "accounting_dir":  str(ACCOUNTING_DIR),
        "tax_dir":         str(TAX_DIR),
        "files_created":   created,
        "note":            "Run 'accounting.py config' to review reserve percentages.",
    }, indent=2))


# ---------------------------------------------------------------------------

def cmd_record(args):
    _ensure_dirs()
    config    = load_config()
    ledger    = load_ledger()
    open_lots = load_open_lots()
    reserves  = load_reserves()

    pair     = args.pair.upper().replace("-", "/")
    asset    = pair.split("/")[0]          # BTC from BTC/USD
    side     = args.side.upper()
    qty      = float(args.qty)
    price    = float(args.price)
    fee      = float(args.fee)
    bot      = args.bot
    exchange = getattr(args, "exchange", None) or config["exchange"]
    ts       = args.timestamp or _now_iso()
    trade_id = str(uuid.uuid4())[:8]

    base_entry = {
        "trade_id": trade_id,
        "bot":      bot,
        "pair":     pair,
        "asset":    asset,
        "side":     side,
        "quantity": qty,
        "price":    price,
        "fee":      fee,
        "timestamp": ts,
        "exchange": exchange,
    }

    # ---- BUY ----------------------------------------------------------------
    if side == "BUY":
        cost_basis = round(qty * price + fee, 2)
        lot = {
            "trade_id":  trade_id,
            "bot":       bot,
            "quantity":  qty,
            "price":     price,
            "fee":       fee,
            "cost_basis": cost_basis,
            "timestamp": ts,
        }
        open_lots.setdefault(asset, []).append(lot)

        entry = {**base_entry, "cost_basis": cost_basis,
                 "proceeds": None, "gain_loss": None,
                 "holding_period": None, "matched_lots": [],
                 "profit_routing": None}

        _save_json(OPEN_LOTS_FILE, open_lots)
        ledger.append(entry)
        _save_json(LEDGER_FILE, ledger)

        print(json.dumps({
            "status":     "ok",
            "trade_id":   trade_id,
            "side":       "BUY",
            "asset":      asset,
            "qty":        qty,
            "cost_basis": cost_basis,
            "open_lots":  len(open_lots.get(asset, [])),
        }))

    # ---- SELL ---------------------------------------------------------------
    elif side == "SELL":
        proceeds     = round(qty * price - fee, 2)
        lots_queue   = open_lots.get(asset, [])
        remaining    = qty
        total_cost   = 0.0
        matched      = []
        holding_term = "SHORT"
        warnings     = []

        while remaining > 0.000001 and lots_queue:
            lot = lots_queue[0]

            if lot["quantity"] <= remaining + 0.000001:
                # Consume full lot
                used_qty  = lot["quantity"]
                used_cost = round(lot["cost_basis"], 2)
                total_cost += used_cost
                remaining  -= used_qty

                acquired_dt = _parse_dt(lot["timestamp"])
                sold_dt     = _parse_dt(ts)
                if (sold_dt - acquired_dt).days > 365:
                    holding_term = "LONG"

                matched.append({
                    "lot_trade_id": lot["trade_id"],
                    "bot":          lot["bot"],
                    "quantity":     round(used_qty, 8),
                    "cost_basis":   used_cost,
                    "acquired":     lot["timestamp"],
                })
                lots_queue.pop(0)

            else:
                # Partial lot
                frac      = remaining / lot["quantity"]
                used_cost = round(lot["cost_basis"] * frac, 2)
                total_cost += used_cost

                acquired_dt = _parse_dt(lot["timestamp"])
                sold_dt     = _parse_dt(ts)
                if (sold_dt - acquired_dt).days > 365:
                    holding_term = "LONG"

                matched.append({
                    "lot_trade_id": lot["trade_id"],
                    "bot":          lot["bot"],
                    "quantity":     round(remaining, 8),
                    "cost_basis":   used_cost,
                    "acquired":     lot["timestamp"],
                })
                lot["quantity"]  = round(lot["quantity"] - remaining, 8)
                lot["cost_basis"] = round(lot["cost_basis"] - used_cost, 2)
                remaining = 0

        if remaining > 0.0001:
            warnings.append(
                f"No open lots for {remaining:.6f} units of {asset} — cost basis set to 0."
            )

        open_lots[asset] = lots_queue
        total_cost = round(total_cost, 2)
        gain_loss  = round(proceeds - total_cost, 2)

        # Profit routing
        routing = {}
        if gain_loss > 0:
            routing["tax_reserve"]       = round(gain_loss * config["tax_reserve_pct"], 2)
            routing["operating_reserve"] = round(gain_loss * config["operating_reserve_pct"], 2)
            routing["reinvestment_pool"] = round(gain_loss * config["reinvestment_pct"], 2)

            reserves["tax_reserve"]       = round(reserves["tax_reserve"] + routing["tax_reserve"], 2)
            reserves["operating_reserve"] = round(reserves["operating_reserve"] + routing["operating_reserve"], 2)
            reserves["reinvestment_pool"] = round(reserves["reinvestment_pool"] + routing["reinvestment_pool"], 2)
            reserves["lifetime_gains"]    = round(reserves["lifetime_gains"] + gain_loss, 2)
            reserves["total_contributed_to_tax"]      = round(reserves.get("total_contributed_to_tax", 0) + routing["tax_reserve"], 2)
            reserves["total_contributed_to_operating"] = round(reserves.get("total_contributed_to_operating", 0) + routing["operating_reserve"], 2)
        else:
            routing["tax_reserve"]       = 0.0
            routing["operating_reserve"] = 0.0
            routing["reinvestment_pool"] = gain_loss  # loss reduces pool
            reserves["lifetime_losses"]  = round(reserves["lifetime_losses"] + abs(gain_loss), 2)

        reserves["last_updated"] = ts

        # Wash sale flag: loss + same asset may be repurchased within 30 days
        wash_warning = None
        if gain_loss < 0:
            wash_warning = (
                f"LOSS ${abs(gain_loss):.2f} on {asset} — potential wash sale if "
                f"{asset} is bought within {config['wash_sale_window_days']} days. "
                f"Loss may be disallowed by IRS. Consult tax advisor."
            )

        entry = {
            **base_entry,
            "cost_basis":     total_cost,
            "proceeds":       proceeds,
            "gain_loss":      gain_loss,
            "holding_period": holding_term,
            "matched_lots":   matched,
            "profit_routing": routing,
        }
        if warnings:      entry["warnings"]          = warnings
        if wash_warning:  entry["wash_sale_warning"] = wash_warning

        _save_json(OPEN_LOTS_FILE, open_lots)
        _save_json(RESERVES_FILE, reserves)
        ledger.append(entry)
        _save_json(LEDGER_FILE, ledger)

        result = {
            "status":         "ok",
            "trade_id":       trade_id,
            "side":           "SELL",
            "asset":          asset,
            "proceeds":       proceeds,
            "cost_basis":     total_cost,
            "gain_loss":      gain_loss,
            "holding_period": holding_term,
            "profit_routing": routing,
        }
        if wash_warning: result["wash_sale_warning"] = wash_warning
        if warnings:     result["warnings"]          = warnings
        print(json.dumps(result))

    else:
        print(json.dumps({"error": f"Unknown side: {side}. Use BUY or SELL."}))
        sys.exit(1)


# ---------------------------------------------------------------------------

def cmd_reserves(args):
    reserves = load_reserves()
    config   = load_config()
    net      = round(reserves["lifetime_gains"] - reserves["lifetime_losses"], 2)
    print(json.dumps({
        "balances": {
            "tax_reserve":       reserves["tax_reserve"],
            "operating_reserve": reserves["operating_reserve"],
            "reinvestment_pool": reserves["reinvestment_pool"],
        },
        "lifetime": {
            "gains":       reserves["lifetime_gains"],
            "losses":      reserves["lifetime_losses"],
            "net":         net,
        },
        "routing_config": {
            "tax_reserve_pct":       config["tax_reserve_pct"],
            "operating_reserve_pct": config["operating_reserve_pct"],
            "reinvestment_pct":      config["reinvestment_pct"],
        },
        "last_updated": reserves["last_updated"],
    }, indent=2))


# ---------------------------------------------------------------------------

def cmd_daily(args):
    ledger      = load_ledger()
    target_date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    sells = [
        e for e in ledger
        if e["side"] == "SELL"
        and e.get("timestamp", "").startswith(target_date)
        and e.get("gain_loss") is not None
    ]

    total_gains  = sum(e["gain_loss"] for e in sells if e["gain_loss"] > 0)
    total_losses = sum(e["gain_loss"] for e in sells if e["gain_loss"] < 0)
    net_pnl      = round(total_gains + total_losses, 2)

    by_bot = {}
    for e in sells:
        b = e["bot"]
        by_bot.setdefault(b, {"trades": 0, "gains": 0.0, "losses": 0.0, "net": 0.0, "wins": 0, "losses_count": 0})
        by_bot[b]["trades"] += 1
        by_bot[b]["net"]    = round(by_bot[b]["net"] + e["gain_loss"], 2)
        if e["gain_loss"] > 0:
            by_bot[b]["gains"] = round(by_bot[b]["gains"] + e["gain_loss"], 2)
            by_bot[b]["wins"] += 1
        else:
            by_bot[b]["losses"]       = round(by_bot[b]["losses"] + e["gain_loss"], 2)
            by_bot[b]["losses_count"] += 1

    reserves = load_reserves()
    print(json.dumps({
        "date":             target_date,
        "realized_trades":  len(sells),
        "total_gains":      round(total_gains, 2),
        "total_losses":     round(total_losses, 2),
        "net_pnl":          net_pnl,
        "by_bot":           by_bot,
        "reserve_balances": {
            "tax_reserve":       reserves["tax_reserve"],
            "operating_reserve": reserves["operating_reserve"],
            "reinvestment_pool": reserves["reinvestment_pool"],
        },
    }, indent=2))


# ---------------------------------------------------------------------------

def cmd_export(args):
    _ensure_dirs()
    ledger = load_ledger()
    year   = str(getattr(args, "year", None) or datetime.now(timezone.utc).year)

    # -- Form 8949 ------------------------------------------------------------
    if args.report_type == "8949":
        path  = TAX_DIR / f"8949_{year}.csv"
        sells = [
            e for e in ledger
            if e["side"] == "SELL"
            and e.get("timestamp", "").startswith(year)
            and e.get("gain_loss") is not None
        ]
        # IRS 8949 groups: Part I = short-term, Part II = long-term
        sells.sort(key=lambda e: (e.get("holding_period", "SHORT") == "LONG", e["timestamp"]))

        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "Description of Property",
                "Date Acquired",
                "Date Sold or Disposed",
                "Proceeds (Sales Price)",
                "Cost or Other Basis",
                "Adjustment Code",
                "Gain or (Loss)",
                "Term (SHORT/LONG)",
            ])
            for e in sells:
                acquired = (
                    e["matched_lots"][0]["acquired"][:10]
                    if e.get("matched_lots") else "VARIOUS"
                )
                description = f"{e['asset']} ({e['quantity']} units) [{e['bot']}]"
                adj_code    = "W" if e.get("wash_sale") else ""
                w.writerow([
                    description,
                    acquired,
                    e["timestamp"][:10],
                    f"{e['proceeds']:.2f}",
                    f"{e['cost_basis']:.2f}",
                    adj_code,
                    f"{e['gain_loss']:.2f}",
                    e.get("holding_period", "SHORT"),
                ])

        short_total = sum(e["gain_loss"] for e in sells if e.get("holding_period", "SHORT") == "SHORT")
        long_total  = sum(e["gain_loss"] for e in sells if e.get("holding_period") == "LONG")
        print(json.dumps({
            "status":            "ok",
            "file":              str(path),
            "year":              year,
            "total_rows":        len(sells),
            "short_term_net":    round(short_total, 2),
            "long_term_net":     round(long_total, 2),
            "combined_net":      round(short_total + long_total, 2),
        }, indent=2))

    # -- Annual Summary -------------------------------------------------------
    elif args.report_type == "summary":
        path  = TAX_DIR / f"summary_{year}.csv"
        sells = [
            e for e in ledger
            if e["side"] == "SELL"
            and e.get("timestamp", "").startswith(year)
            and e.get("gain_loss") is not None
        ]

        groups = {}
        for e in sells:
            key = (e["bot"], e["asset"], e.get("holding_period", "SHORT"))
            groups.setdefault(key, {"trades": 0, "proceeds": 0.0, "cost_basis": 0.0,
                                    "gain_loss": 0.0, "fees": 0.0})
            g = groups[key]
            g["trades"]     += 1
            g["proceeds"]   += e.get("proceeds", 0) or 0
            g["cost_basis"] += e.get("cost_basis", 0) or 0
            g["gain_loss"]  += e.get("gain_loss", 0) or 0
            g["fees"]       += e.get("fee", 0) or 0

        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Bot", "Asset", "Term", "Trades", "Proceeds", "Cost Basis", "Fees", "Net Gain/(Loss)"])
            for (bot, asset, term), g in sorted(groups.items()):
                w.writerow([
                    bot, asset, term, g["trades"],
                    f"{g['proceeds']:.2f}", f"{g['cost_basis']:.2f}",
                    f"{g['fees']:.2f}",     f"{g['gain_loss']:.2f}",
                ])

        print(json.dumps({
            "status":     "ok",
            "file":       str(path),
            "year":       year,
            "total_rows": len(groups),
        }, indent=2))

    # -- Full Ledger CSV ------------------------------------------------------
    elif args.report_type == "ledger":
        path = ACCOUNTING_DIR / "ledger.csv"
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "trade_id", "bot", "pair", "asset", "side", "quantity",
                "price", "fee", "timestamp", "exchange",
                "cost_basis", "proceeds", "gain_loss", "holding_period",
            ])
            for e in ledger:
                w.writerow([
                    e.get("trade_id"), e.get("bot"),      e.get("pair"),   e.get("asset"),
                    e.get("side"),     e.get("quantity"),  e.get("price"),  e.get("fee"),
                    e.get("timestamp"),e.get("exchange"),
                    e.get("cost_basis"), e.get("proceeds"), e.get("gain_loss"), e.get("holding_period"),
                ])
        print(json.dumps({
            "status":     "ok",
            "file":       str(path),
            "total_rows": len(ledger),
        }, indent=2))


# ---------------------------------------------------------------------------

def cmd_wash_sales(args):
    ledger = load_ledger()
    config = load_config()
    year   = str(getattr(args, "year", None) or datetime.now(timezone.utc).year)
    window = config.get("wash_sale_window_days", 30)

    loss_sales = [
        e for e in ledger
        if e["side"] == "SELL"
        and e.get("timestamp", "").startswith(year)
        and (e.get("gain_loss") or 0) < 0
    ]

    buys    = [e for e in ledger if e["side"] == "BUY"]
    flagged = []

    for sale in loss_sales:
        sale_dt = _parse_dt(sale["timestamp"])
        asset   = sale["asset"]

        for buy in buys:
            if buy["asset"] != asset:
                continue
            buy_dt   = _parse_dt(buy["timestamp"])
            days_diff = abs((buy_dt - sale_dt).days)

            # Skip the buy lots that were matched against this sale
            matched_ids = {m.get("lot_trade_id") for m in sale.get("matched_lots", [])}
            if buy["trade_id"] in matched_ids:
                continue

            if days_diff <= window:
                flagged.append({
                    "loss_trade_id":      sale["trade_id"],
                    "loss_bot":           sale["bot"],
                    "asset":              asset,
                    "loss_amount":        sale["gain_loss"],
                    "sale_date":          sale["timestamp"][:10],
                    "repurchase_trade_id": buy["trade_id"],
                    "repurchase_bot":     buy["bot"],
                    "repurchase_date":    buy["timestamp"][:10],
                    "days_apart":         days_diff,
                    "note": (
                        "Potential wash sale — disallowed loss must be added to cost basis "
                        "of new position. Consult tax advisor."
                    ),
                })

    print(json.dumps({
        "year":               year,
        "loss_sales_checked": len(loss_sales),
        "flagged":            len(flagged),
        "items":              flagged,
    }, indent=2))


# ---------------------------------------------------------------------------

def cmd_config(args):
    _ensure_dirs()
    config = load_config()

    if getattr(args, "set_kv", None):
        key, val = args.set_kv.split("=", 1)
        try:
            val = float(val)
        except ValueError:
            pass
        config[key] = val
        _save_json(CONFIG_FILE, config)
        print(json.dumps({"status": "ok", "updated": {key: val}}))
    else:
        print(json.dumps(config, indent=2))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Accounting Bot — fleet trade ledger and tax reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    # init
    sub.add_parser("init", help="Initialize data files")

    # record
    rec = sub.add_parser("record", help="Record a BUY or SELL trade")
    rec.add_argument("--bot",       required=True, help="Bot name (e.g. floki)")
    rec.add_argument("--pair",      required=True, help="Trading pair (e.g. BTC/USD)")
    rec.add_argument("--side",      required=True, choices=["BUY","SELL","buy","sell"])
    rec.add_argument("--qty",       required=True, type=float, help="Quantity of asset")
    rec.add_argument("--price",     required=True, type=float, help="Execution price in USD")
    rec.add_argument("--fee",       required=True, type=float, help="Fee paid in USD")
    rec.add_argument("--timestamp", default=None,  help="ISO 8601 UTC (default: now)")
    rec.add_argument("--exchange",  default=None,  help="Exchange name (default: from config)")

    # reserves
    sub.add_parser("reserves", help="Show current reserve balances")

    # daily
    day = sub.add_parser("daily", help="Daily realized P&L summary")
    day.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")

    # export
    exp = sub.add_parser("export", help="Export tax reports or ledger CSV")
    exp.add_argument("report_type", choices=["8949", "summary", "ledger"])
    exp.add_argument("--year", type=int, default=None, help="Tax year (default: current)")

    # wash-sales
    ws = sub.add_parser("wash-sales", help="Scan for potential wash sale violations")
    ws.add_argument("--year", type=int, default=None)

    # config
    cfg = sub.add_parser("config", help="View or update accounting config")
    cfg.add_argument("--set", dest="set_kv", default=None, metavar="key=value",
                     help="e.g. --set tax_reserve_pct=0.35")

    args = parser.parse_args()

    dispatch = {
        "init":        cmd_init,
        "record":      cmd_record,
        "reserves":    cmd_reserves,
        "daily":       cmd_daily,
        "export":      cmd_export,
        "wash-sales":  cmd_wash_sales,
        "config":      cmd_config,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
