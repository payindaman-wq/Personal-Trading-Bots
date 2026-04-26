#!/usr/bin/env python3
"""
njord_kraken.py - Kraken adapter for NJORD Capital Allocation Officer.

Two modes, auto-selected by key presence:
  - paper: no API keys required. Balance = config.njord.total_capital_usd.
           Market orders are simulated at the last observed tick price and
           persisted to competition/njord_paper_state.json so allocation
           tables can reflect realistic portfolio drift across cycles.
  - live:  requires kraken.api_key + kraken.api_secret in config. The live
           Balance/AddOrder paths raise NotImplementedError in the public
           template - wire them through krakenex/ccxt in your fork.

The adapter exposes a uniform interface so the orchestrator never branches
on mode. A `tick_provider` hook lets tests inject deterministic prices
without touching the network.
"""
from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

WORKSPACE = os.environ.get("WORKSPACE", "/root/.openclaw/workspace")
PAPER_STATE_PATH = os.path.join(WORKSPACE, "competition", "njord_paper_state.json")

KRAKEN_TICKER_URL = "https://api.kraken.com/0/public/Ticker"


def _ts_iso():
    return datetime.now(timezone.utc).isoformat()


def _has_keys(api_key, api_secret):
    return bool(api_key) and bool(api_secret)


class KrakenAdapter:
    """Uniform Kraken interface. Mode auto-selects from key presence."""

    def __init__(self, api_key="", api_secret="", paper_balance_usd=0.0,
                 paper_state_path=None, tick_provider=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_state_path = paper_state_path or PAPER_STATE_PATH
        self.paper_balance_usd = float(paper_balance_usd or 0.0)
        self.is_paper = not _has_keys(api_key, api_secret)
        self.tick_provider = tick_provider
        if self.is_paper:
            self._load_paper_state()

    @property
    def mode(self):
        return "paper" if self.is_paper else "live"

    # paper state
    def _load_paper_state(self):
        if os.path.exists(self.paper_state_path):
            try:
                with open(self.paper_state_path) as f:
                    self._paper = json.load(f)
                return
            except (OSError, json.JSONDecodeError):
                pass
        self._paper = self._fresh_paper()

    def _fresh_paper(self):
        return {
            "cash_usd":   self.paper_balance_usd,
            "positions":  {},
            "fills":      [],
            "created_ts": _ts_iso(),
        }

    def _save_paper_state(self):
        os.makedirs(os.path.dirname(self.paper_state_path), exist_ok=True)
        tmp = self.paper_state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self._paper, f, indent=2)
        os.replace(tmp, self.paper_state_path)

    # balance
    def get_balance_usd(self):
        if self.is_paper:
            cash = float(self._paper.get("cash_usd", 0.0))
            positions_value = 0.0
            for sym, pos in self._paper.get("positions", {}).items():
                px = self.get_last_tick(sym) or 0.0
                positions_value += float(pos.get("qty", 0.0)) * px
            return cash + positions_value
        return self._live_balance_usd()

    def _live_balance_usd(self):
        raise NotImplementedError(
            "Live balance requires authenticated Kraken endpoint; install "
            "krakenex/ccxt and implement _live_balance_usd in your fork."
        )

    # ticks
    def get_last_tick(self, symbol):
        """Return last price for symbol (Kraken pair, e.g. XBTUSD) or None."""
        if not symbol:
            return None
        if self.tick_provider is not None:
            try:
                px = self.tick_provider(symbol)
                return float(px) if px is not None else None
            except (TypeError, ValueError):
                return None
        try:
            req = urllib.request.Request(
                KRAKEN_TICKER_URL + "?pair=" + symbol,
                headers={"User-Agent": "njord/0.1"},
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read().decode())
            for _, pair_data in (data.get("result") or {}).items():
                last = (pair_data.get("c") or [None])[0]
                if last is not None:
                    return float(last)
        except (urllib.error.URLError, json.JSONDecodeError, ValueError, OSError):
            return None
        return None

    # orders
    def place_market_order(self, symbol, side, usd_amount):
        """side: 'buy' | 'sell'. Returns dict {filled_usd, filled_qty, price}."""
        if usd_amount <= 0:
            return {"filled_usd": 0.0, "filled_qty": 0.0, "price": 0.0,
                    "skipped": "non_positive_amount"}
        if not symbol:
            return {"filled_usd": 0.0, "filled_qty": 0.0, "price": 0.0,
                    "skipped": "no_symbol"}
        price = self.get_last_tick(symbol) or 0.0
        if price <= 0:
            return {"filled_usd": 0.0, "filled_qty": 0.0, "price": 0.0,
                    "skipped": "no_last_tick"}
        qty = usd_amount / price
        if self.is_paper:
            return self._paper_fill(symbol, side, usd_amount, qty, price)
        return self._live_market_order(symbol, side, usd_amount, qty, price)

    def _paper_fill(self, symbol, side, usd_amount, qty, price):
        pos = self._paper["positions"].setdefault(symbol, {"qty": 0.0, "cost_basis_usd": 0.0})
        if side == "buy":
            self._paper["cash_usd"] -= usd_amount
            pos["qty"] += qty
            pos["cost_basis_usd"] += usd_amount
        else:
            self._paper["cash_usd"] += usd_amount
            pos["qty"] -= qty
            pos["cost_basis_usd"] = max(0.0, pos["cost_basis_usd"] - usd_amount)
        fill = {
            "ts":     _ts_iso(),
            "symbol": symbol,
            "side":   side,
            "usd":    usd_amount,
            "qty":    qty,
            "price":  price,
            "mode":   "paper",
        }
        self._paper["fills"].append(fill)
        self._paper["fills"] = self._paper["fills"][-200:]
        self._save_paper_state()
        return {"filled_usd": usd_amount, "filled_qty": qty, "price": price}

    def _live_market_order(self, symbol, side, usd_amount, qty, price):
        raise NotImplementedError(
            "Live order placement requires authenticated Kraken AddOrder; "
            "install krakenex/ccxt and implement _live_market_order in your fork."
        )


def from_config(config):
    """Construct an adapter from a config namespace."""
    api_key    = getattr(config.kraken, "api_key", "") or ""
    api_secret = getattr(config.kraken, "api_secret", "") or ""
    njord = getattr(config, "njord", None)
    paper_balance = 0.0
    if njord is not None:
        paper_balance = float(getattr(njord, "total_capital_usd", 0) or 0)
        if getattr(njord, "mode", "paper") == "live" and not _has_keys(api_key, api_secret):
            raise RuntimeError(
                "njord.mode=live but kraken.api_key/api_secret are empty; "
                "either set keys or switch njord.mode back to 'paper'."
            )
    return KrakenAdapter(api_key=api_key, api_secret=api_secret,
                         paper_balance_usd=paper_balance)
