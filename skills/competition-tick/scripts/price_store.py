#!/usr/bin/env python3
"""
price_store.py - Append current prices to competition price history.
Keeps a rolling window of price ticks for indicator calculation.
Each tick stores: ts, last (close price), vwap (optional).
"""
import json
import os
from datetime import datetime, timezone, timedelta


MAX_HISTORY_HOURS = 5


def load_history(comp_dir):
    path = os.path.join(comp_dir, "price_history.json")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def save_history(comp_dir, history):
    path = os.path.join(comp_dir, "price_history.json")
    with open(path, "w") as f:
        json.dump(history, f)


def append_prices(comp_dir, prices):
    """
    prices: dict like {"BTC/USD": {"last": 68250.0, "vwap": 67900.0}, ...}
    vwap is optional -- stored if present, omitted if not.
    """
    history = load_history(comp_dir)
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    cutoff = (now - timedelta(hours=MAX_HISTORY_HOURS)).isoformat()

    for pair, data in prices.items():
        if pair not in history:
            history[pair] = []
        tick = {"ts": now_iso, "last": data["last"]}
        if "vwap" in data and data["vwap"] is not None:
            tick["vwap"] = data["vwap"]
        if "volume" in data and data["volume"] is not None:
            tick["volume"] = data["volume"]
        history[pair].append(tick)
        history[pair] = [t for t in history[pair] if t["ts"] >= cutoff]

    save_history(comp_dir, history)
    return history


def get_price_n_minutes_ago(history, pair, minutes):
    if pair not in history or not history[pair]:
        return None
    now = datetime.now(timezone.utc)
    target_iso = (now - timedelta(minutes=minutes)).isoformat()
    past_ticks = [t for t in history[pair] if t["ts"] <= target_iso]
    if not past_ticks:
        return None
    return past_ticks[-1]["last"]


def get_current_price(history, pair):
    if pair not in history or not history[pair]:
        return None
    return history[pair][-1]["last"]


def get_current_vwap(history, pair):
    """Returns most recent VWAP for pair, or None if unavailable."""
    if pair not in history or not history[pair]:
        return None
    for tick in reversed(history[pair]):
        if "vwap" in tick:
            return tick["vwap"]
    return None
