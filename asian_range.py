import MetaTrader5 as mt5
from datetime import datetime


def get_asian_range(symbol):

    # get last 300 M5 candles
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 300)

    if rates is None or len(rates) == 0:
        print("No candle data")
        return None, None

    asian_high = None
    asian_low = None

    for candle in rates:

        candle_time = datetime.fromtimestamp(candle["time"])

        # Asian session (00:00 - 06:00)
        if 0 <= candle_time.hour < 6:

            high = candle["high"]
            low = candle["low"]

            if asian_high is None or high > asian_high:
                asian_high = high

            if asian_low is None or low < asian_low:
                asian_low = low

    if asian_high is None or asian_low is None:
        print("Asian session candles not found")
        return None, None

    print(f"Asian Range for {symbol}: {asian_high} - {asian_low}")

    return asian_high, asian_low