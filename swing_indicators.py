#!/usr/bin/env python3
"""
swing_indicators.py - Compute trading indicators from hourly candle history.

All periods are in HOURS (not minutes like the day trading version).
All functions return None if insufficient history exists.

Available indicators:
  price_change_pct      -- % change over period_hours
  trend                 -- up | down | flat over period_hours
  momentum_accelerating -- True if recent half stronger than prior half
  price_vs_vwap         -- above | below | at relative to 24h VWAP
  rsi                   -- 0-100 RSI (standard 14-period = period_hours: 14)
  price_vs_ema          -- above | below | at relative to EMA
  bollinger_position    -- above_upper | below_lower | inside Bollinger Bands
  macd_signal           -- bullish | bearish | neutral
                          (standard: slow=26h, period_hours: 26)
"""
from swing_price_store import (
    get_current_price,
    get_price_n_hours_ago,
    get_price_series,
    get_vwap,
)

FLAT_THRESHOLD_PCT = 1.0   # wider flat band for swing (vs 0.15% for day trading)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _calc_ema(prices, n):
    """EMA over price list (oldest-first). n = number of periods."""
    k = 2 / (n + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema


# ---------------------------------------------------------------------------
# Indicators
# ---------------------------------------------------------------------------

def price_change_pct(pair, period_hours):
    current = get_current_price(pair)
    past    = get_price_n_hours_ago(pair, period_hours)
    if current is None or past is None or past == 0:
        return None
    return (current - past) / past * 100


def trend(pair, period_hours):
    change = price_change_pct(pair, period_hours)
    if change is None:
        return None
    if change > FLAT_THRESHOLD_PCT:
        return "up"
    if change < -FLAT_THRESHOLD_PCT:
        return "down"
    return "flat"


def momentum_accelerating(pair, period_hours):
    half = period_hours // 2
    if half < 1:
        return None
    current = get_current_price(pair)
    mid     = get_price_n_hours_ago(pair, half)
    start   = get_price_n_hours_ago(pair, period_hours)
    if any(v is None or v == 0 for v in [current, mid, start]):
        return None
    recent = abs((current - mid) / mid * 100)
    prior  = abs((mid - start) / start * 100)
    return recent > prior


def price_vs_vwap(pair, period_hours=24):
    current = get_current_price(pair)
    vwap    = get_vwap(pair, period_hours=period_hours if period_hours > 0 else 24)
    if current is None or vwap is None or vwap == 0:
        return None
    diff_pct = (current - vwap) / vwap * 100
    if diff_pct > 0.5:
        return "above"
    if diff_pct < -0.5:
        return "below"
    return "at"


def rsi(pair, period_hours):
    """Standard 14-period RSI = period_hours: 14."""
    n = max(period_hours, 2)
    prices = get_price_series(pair, n + 1, interval_hours=1)
    if prices is None:
        return None
    changes  = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
    gains    = [max(c, 0) for c in changes]
    losses   = [abs(min(c, 0)) for c in changes]
    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def price_vs_ema(pair, period_hours):
    """Standard 20-period EMA = period_hours: 20."""
    n = max(period_hours, 2)
    prices = get_price_series(pair, n, interval_hours=1)
    if prices is None:
        return None
    ema_val = _calc_ema(prices, n)
    current = get_current_price(pair)
    if current is None:
        return None
    diff = (current - ema_val) / ema_val * 100
    if diff > 0.5:
        return "above"
    if diff < -0.5:
        return "below"
    return "at"


def bollinger_position(pair, period_hours):
    """Standard 20-period BB = period_hours: 20."""
    n = max(period_hours, 2)
    prices = get_price_series(pair, n, interval_hours=1)
    if prices is None:
        return None
    mean     = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    std      = variance ** 0.5
    if std == 0:
        return "inside"
    upper   = mean + 2 * std
    lower   = mean - 2 * std
    current = get_current_price(pair)
    if current is None:
        return None
    if current > upper:
        return "above_upper"
    if current < lower:
        return "below_lower"
    return "inside"


def macd_signal(pair, period_hours):
    """
    MACD using hourly candles.
    period_hours = slow EMA period (standard: 26).
    Fast = 12h, Signal = 9h.
    """
    slow_n   = max(period_hours, 4)
    fast_n   = max(slow_n * 12 // 26, 2)
    signal_n = max(slow_n * 9 // 26, 2)
    total    = slow_n + signal_n - 1
    prices   = get_price_series(pair, total, interval_hours=1)
    if prices is None:
        return None
    macd_values = []
    for i in range(signal_n):
        window   = prices[i:i + slow_n]
        slow_ema = _calc_ema(window, slow_n)
        fast_ema = _calc_ema(window[slow_n - fast_n:], fast_n)
        macd_values.append(fast_ema - slow_ema)
    signal_line = _calc_ema(macd_values, signal_n)
    histogram   = macd_values[-1] - signal_line
    if histogram > 0:
        return "bullish"
    if histogram < 0:
        return "bearish"
    return "neutral"


# ---------------------------------------------------------------------------
# Dispatch + evaluation
# ---------------------------------------------------------------------------

def compute_indicator(name, pair, period_hours):
    if name == "price_change_pct":
        return price_change_pct(pair, period_hours)
    if name == "trend":
        return trend(pair, period_hours)
    if name == "momentum_accelerating":
        return momentum_accelerating(pair, period_hours)
    if name == "price_vs_vwap":
        return price_vs_vwap(pair, period_hours)
    if name == "rsi":
        return rsi(pair, period_hours)
    if name == "price_vs_ema":
        return price_vs_ema(pair, period_hours)
    if name == "bollinger_position":
        return bollinger_position(pair, period_hours)
    if name == "macd_signal":
        return macd_signal(pair, period_hours)
    raise ValueError(f"Unknown indicator: {name}")


def evaluate_condition(cond, pair):
    name     = cond["indicator"]
    period   = cond.get("period_hours", 24)
    operator = cond["operator"]
    expected = cond["value"]
    eval_pair = cond.get("pair", pair)  # per-condition pair override (for dual-confirmation strategies)
    actual   = compute_indicator(name, eval_pair, period)
    if actual is None:
        return None
    if isinstance(expected, str):
        if expected.lower() == "true":
            expected = True
        elif expected.lower() == "false":
            expected = False
    if operator == "lt":  return actual < expected
    if operator == "gt":  return actual > expected
    if operator == "lte": return actual <= expected
    if operator == "gte": return actual >= expected
    if operator == "eq":  return actual == expected
    if operator == "in":  return actual in expected
    raise ValueError(f"Unknown operator: {operator}")


def evaluate_entry(conditions, pair):
    results = [evaluate_condition(c, pair) for c in conditions]
    if None in results:
        return None
    return all(results)
