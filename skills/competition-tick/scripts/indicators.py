#!/usr/bin/env python3
"""
indicators.py - Compute trading indicators from price history.

All functions return None if insufficient history exists.
The tick engine treats None as "signal not available -- skip entry check."

Available indicators:
  price_change_pct     -- % change over period_minutes
  trend                -- up | down | flat over period_minutes
  momentum_accelerating -- True if recent half stronger than prior half
  price_vs_vwap        -- above | below | at relative to stored VWAP
  rsi                  -- 0-100 RSI value (period_minutes / 5 = n_periods)
  price_vs_ema         -- above | below | at relative to EMA
  bollinger_position   -- above_upper | below_lower | inside Bollinger Bands
  macd_signal          -- bullish | bearish | neutral (MACD line vs signal line)
                          period_minutes = slow period (standard: 130 = 26 x 5min)
"""
from datetime import datetime, timezone, timedelta
from price_store import get_current_price, get_current_vwap


FLAT_THRESHOLD_PCT = 0.15


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


def _get_price_n_minutes_ago(history, pair, minutes):
    """Price at approximately N minutes ago using real clock."""
    if pair not in history or not history[pair]:
        return None
    target_iso = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()
    past = [t for t in history[pair] if t["ts"] <= target_iso]
    return past[-1]["last"] if past else None


def _get_price_series(history, pair, n_points, interval_minutes=5):
    """
    Returns list of n_points prices sampled at interval_minutes spacing,
    ordered oldest-first. Returns None if insufficient history.
    """
    prices = []
    for i in range(n_points):
        if i == 0:
            price = get_current_price(history, pair)
        else:
            price = _get_price_n_minutes_ago(history, pair, i * interval_minutes)
        if price is None:
            return None
        prices.append(price)
    return list(reversed(prices))  # oldest -> newest


# ---------------------------------------------------------------------------
# Indicators
# ---------------------------------------------------------------------------

def price_change_pct(history, pair, period_minutes):
    current = get_current_price(history, pair)
    past = _get_price_n_minutes_ago(history, pair, period_minutes)
    if current is None or past is None or past == 0:
        return None
    return (current - past) / past * 100


def trend(history, pair, period_minutes):
    change = price_change_pct(history, pair, period_minutes)
    if change is None:
        return None
    if change > FLAT_THRESHOLD_PCT:
        return "up"
    if change < -FLAT_THRESHOLD_PCT:
        return "down"
    return "flat"


def momentum_accelerating(history, pair, period_minutes):
    half = period_minutes // 2
    if half < 1:
        return None
    current = get_current_price(history, pair)
    mid = _get_price_n_minutes_ago(history, pair, half)
    start = _get_price_n_minutes_ago(history, pair, period_minutes)
    if any(v is None or v == 0 for v in [current, mid, start]):
        return None
    recent = abs((current - mid) / mid * 100)
    prior = abs((mid - start) / start * 100)
    return recent > prior


def price_vs_vwap(history, pair, period_minutes=0):
    current = get_current_price(history, pair)
    vwap = get_current_vwap(history, pair)
    if current is None or vwap is None or vwap == 0:
        return None
    diff_pct = (current - vwap) / vwap * 100
    if diff_pct > 0.05:
        return "above"
    if diff_pct < -0.05:
        return "below"
    return "at"


def rsi(history, pair, period_minutes):
    """
    RSI over period_minutes. Uses 5-min sampling so n_periods = period_minutes / 5.
    Standard 14-period RSI = period_minutes: 70.
    Returns 0-100 float or None.
    """
    n = max(period_minutes // 5, 2)
    prices = _get_price_series(history, pair, n + 1)
    if prices is None:
        return None
    changes = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
    gains = [max(c, 0) for c in changes]
    losses = [abs(min(c, 0)) for c in changes]
    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def price_vs_ema(history, pair, period_minutes):
    """
    Price position relative to EMA. n_periods = period_minutes / 5.
    Standard 10-period EMA = period_minutes: 50.
    Returns: above | below | at
    """
    n = max(period_minutes // 5, 2)
    prices = _get_price_series(history, pair, n)
    if prices is None:
        return None
    ema_val = _calc_ema(prices, n)
    current = get_current_price(history, pair)
    if current is None:
        return None
    diff = (current - ema_val) / ema_val * 100
    if diff > 0.05:
        return "above"
    if diff < -0.05:
        return "below"
    return "at"


def bollinger_position(history, pair, period_minutes):
    """
    Price position relative to 2-std-dev Bollinger Bands.
    n_periods = period_minutes / 5.
    Standard 20-period BB = period_minutes: 100.
    Returns: above_upper | below_lower | inside
    """
    n = max(period_minutes // 5, 2)
    prices = _get_price_series(history, pair, n)
    if prices is None:
        return None
    mean = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    std = variance ** 0.5
    if std == 0:
        return "inside"
    upper = mean + 2 * std
    lower = mean - 2 * std
    current = get_current_price(history, pair)
    if current is None:
        return None
    if current > upper:
        return "above_upper"
    if current < lower:
        return "below_lower"
    return "inside"


def macd_signal(history, pair, period_minutes):
    """
    MACD signal direction relative to signal line.
    period_minutes = slow EMA period in minutes (standard: 130 = 26 x 5min candles).
    Fast period = slow * 12/26. Signal period = slow * 9/26.
    Returns: bullish (MACD > signal) | bearish (MACD < signal) | neutral
    Requires: (slow_n + signal_n - 1) * 5 minutes of history.
    Standard config: period_minutes=130 needs ~170 minutes of history.
    """
    slow_n = max(period_minutes // 5, 4)
    fast_n = max(slow_n * 12 // 26, 2)
    signal_n = max(slow_n * 9 // 26, 2)
    total_needed = slow_n + signal_n - 1
    prices = _get_price_series(history, pair, total_needed)
    if prices is None:
        return None
    # Compute MACD line at each of the last signal_n points, then EMA of those
    macd_values = []
    for i in range(signal_n):
        window = prices[i:i + slow_n]
        slow_ema = _calc_ema(window, slow_n)
        fast_ema = _calc_ema(window[slow_n - fast_n:], fast_n)
        macd_values.append(fast_ema - slow_ema)
    signal_line = _calc_ema(macd_values, signal_n)
    macd_line = macd_values[-1]
    histogram = macd_line - signal_line
    if histogram > 0:
        return "bullish"
    if histogram < 0:
        return "bearish"
    return "neutral"


# ---------------------------------------------------------------------------
# Dispatch + evaluation
# ---------------------------------------------------------------------------

def compute_indicator(name, history, pair, period_minutes):
    if name == "price_change_pct":
        return price_change_pct(history, pair, period_minutes)
    if name == "trend":
        return trend(history, pair, period_minutes)
    if name == "momentum_accelerating":
        return momentum_accelerating(history, pair, period_minutes)
    if name == "price_vs_vwap":
        return price_vs_vwap(history, pair, period_minutes)
    if name == "rsi":
        return rsi(history, pair, period_minutes)
    if name == "price_vs_ema":
        return price_vs_ema(history, pair, period_minutes)
    if name == "bollinger_position":
        return bollinger_position(history, pair, period_minutes)
    if name == "macd_signal":
        return macd_signal(history, pair, period_minutes)
    raise ValueError(f"Unknown indicator: {name}")


def evaluate_condition(cond, history, pair):
    indicator_name = cond["indicator"]
    period = cond.get("period_minutes", 5)
    operator = cond["operator"]
    expected = cond["value"]
    actual = compute_indicator(indicator_name, history, pair, period)
    if actual is None:
        return None
    if isinstance(expected, str):
        if expected.lower() == "true":
            expected = True
        elif expected.lower() == "false":
            expected = False
    if operator == "lt":
        return actual < expected
    if operator == "gt":
        return actual > expected
    if operator == "lte":
        return actual <= expected
    if operator == "gte":
        return actual >= expected
    if operator == "eq":
        return actual == expected
    if operator == "in":
        return actual in expected
    raise ValueError(f"Unknown operator: {operator}")


def evaluate_entry(conditions, history, pair):
    results = [evaluate_condition(c, history, pair) for c in conditions]
    if None in results:
        return None
    return all(results)
