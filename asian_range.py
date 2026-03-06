import MetaTrader5 as mt5
from datetime import datetime

# Asian session hours (broker time)
ASIAN_START = 0
ASIAN_END = 6

asian_high = None
asian_low = None
asian_day = None


def get_asian_range(symbol):

    global asian_high, asian_low, asian_day

    now = datetime.now()

    # Reset every new day
    if asian_day != now.date():
        asian_high = None
        asian_low = None
        asian_day = now.date()

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 200)

    if rates is None:
        return None, None

    for candle in rates:

        candle_time = datetime.fromtimestamp(candle['time'])

        if ASIAN_START <= candle_time.hour < ASIAN_END:

            high = candle['high']
            low = candle['low']

            if asian_high is None or high > asian_high:
                asian_high = high

            if asian_low is None or low < asian_low:
                asian_low = low

    return asian_high, asian_low