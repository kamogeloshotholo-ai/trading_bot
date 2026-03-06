import MetaTrader5 as mt5
from datetime import datetime

asian_high = None
asian_low = None
range_day = None


def get_asian_range(symbol):

    global asian_high
    global asian_low
    global range_day

    now = datetime.now()
    today = now.date()

    # Reset range when a new day starts
    if range_day != today:
        asian_high = None
        asian_low = None
        range_day = today
        print("New trading day detected — resetting Asian range")

    # If range already calculated today, return it
    if asian_high is not None and asian_low is not None:
        return asian_high, asian_low

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

    print("Asian Range Set")
    print("Asian High:", asian_high)
    print("Asian Low:", asian_low)

    return asian_high, asian_low