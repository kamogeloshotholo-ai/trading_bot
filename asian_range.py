import MetaTrader5 as mt5
from datetime import datetime

last_day = None
asian_high = None
asian_low = None


def get_asian_range(symbol):

    global last_day, asian_high, asian_low

    today = datetime.now().date()

    # Reset every new day
    if last_day != today:
        asian_high = None
        asian_low = None
        last_day = today
        print("New day detected → resetting Asian range")

    # If already calculated today, return stored values
    if asian_high is not None and asian_low is not None:
        return asian_high, asian_low

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 96)

    if rates is None or len(rates) == 0:
        return None, None

    highs = [candle['high'] for candle in rates]
    lows = [candle['low'] for candle in rates]

    asian_high = max(highs)
    asian_low = min(lows)

    print("Asian High:", asian_high)
    print("Asian Low:", asian_low)

    return asian_high, asian_low