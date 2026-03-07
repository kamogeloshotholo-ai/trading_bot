import MetaTrader5 as mt5
from datetime import datetime


def get_asian_range(symbol):

    # Asian session 00:00 → 06:00 server time
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 200)

    if rates is None or len(rates) == 0:
        return None, None

    asian_high = None
    asian_low = None

    for candle in rates:

        candle_time = datetime.fromtimestamp(candle["time"])

        if 0 <= candle_time.hour < 6:

            high = candle["high"]
            low = candle["low"]

            if asian_high is None or high > asian_high:
                asian_high = high

            if asian_low is None or low < asian_low:
                asian_low = low

    if asian_high is None or asian_low is None:
        return None, None

    print("Asian Range:", asian_high, "-", asian_low)

    return asian_high, asian_low