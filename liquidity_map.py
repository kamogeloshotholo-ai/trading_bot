import MetaTrader5 as mt5
from datetime import datetime, timedelta

# Configurable liquidity sources
LIQUIDITY_SOURCES = {
    "ASIAN": "asian_range",
    "DAILY": "daily_range",
    "WEEKLY": "weekly_range",
    "CUSTOM": "custom_range"
}

# Default to Asian for now
DEFAULT_SOURCE = "ASIAN"

def get_liquidity_levels(symbol, source=DEFAULT_SOURCE):
    """Get liquidity high and low for the symbol based on source."""
    if source == "ASIAN":
        return get_asian_range(symbol)
    elif source == "DAILY":
        return get_daily_range(symbol)
    elif source == "WEEKLY":
        return get_weekly_range(symbol)
    elif source == "CUSTOM":
        return get_custom_range(symbol)
    else:
        print(f"Unknown liquidity source: {source}")
        return None, None

def get_asian_range(symbol):
    """Original Asian range logic."""
    now = datetime.now()
    today = now.date()

    # Asian session time
    asian_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    asian_end = now.replace(hour=6, minute=0, second=0, microsecond=0)

    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, asian_start, asian_end)

    if rates is None or len(rates) == 0:
        print("Asian session not complete yet")
        return None, None

    highs = [candle['high'] for candle in rates]
    lows = [candle['low'] for candle in rates]

    asian_high = max(highs)
    asian_low = min(lows)

    print("Asian Liquidity Set")
    print("High:", asian_high)
    print("Low:", asian_low)

    return asian_high, asian_low

def get_daily_range(symbol):
    """Use previous day's high/low as liquidity."""
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)

    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, start, end)

    if rates is None or len(rates) == 0:
        return None, None

    highs = [r['high'] for r in rates]
    lows = [r['low'] for r in rates]

    daily_high = max(highs)
    daily_low = min(lows)

    print("Daily Liquidity Set")
    print("High:", daily_high)
    print("Low:", daily_low)

    return daily_high, daily_low

def get_weekly_range(symbol):
    """Use previous week's high/low."""
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday() + 7)  # Last Monday
    week_end = week_start + timedelta(days=6, hours=23, minutes=59)

    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, week_start, week_end)

    if rates is None or len(rates) == 0:
        return None, None

    highs = [r['high'] for r in rates]
    lows = [r['low'] for r in rates]

    weekly_high = max(highs)
    weekly_low = min(lows)

    print("Weekly Liquidity Set")
    print("High:", weekly_high)
    print("Low:", weekly_low)

    return weekly_high, weekly_low

def get_custom_range(symbol):
    """Placeholder for custom logic, e.g., from structure."""
    # Could use structure_detector for swing levels
    from structure_detector import get_recent_swing
    swing_high, swing_low = get_recent_swing(symbol, mt5.TIMEFRAME_H1, bars=100)
    print("Custom Liquidity (Swing) Set")
    print("High:", swing_high)
    print("Low:", swing_low)
    return swing_high, swing_low