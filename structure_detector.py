import MetaTrader5 as mt5


def detect_retest(symbol, asian_high, asian_low, bias):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 10)

    if rates is None or len(rates) < 5:
        return None

    last = rates[-1]
    prev = rates[-2]

    last_close = last['close']
    prev_low = prev['low']
    prev_high = prev['high']

    # Sweep Asian LOW
    if prev_low < asian_low and last_close > asian_low:
        print("Retest after Asian LOW sweep")
        return "BUY"

    # Sweep Asian HIGH
    if prev_high > asian_high and last_close < asian_high:
        print("Retest after Asian HIGH sweep")
        return "SELL"

    return None