import MetaTrader5 as mt5


def detect_sweep_and_structure(symbol, asian_high, asian_low):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 30)

    if rates is None or len(rates) < 5:
        return None

    last = rates[-1]
    prev = rates[-2]

    last_high = last['high']
    last_low = last['low']
    last_close = last['close']

    prev_high = prev['high']
    prev_low = prev['low']

    # Sweep Asian LOW
    if prev_low < asian_low and last_close > asian_low:
        print("Asian LOW sweep detected")
        return "BULLISH_SWEEP"

    # Sweep Asian HIGH
    if prev_high > asian_high and last_close < asian_high:
        print("Asian HIGH sweep detected")
        return "BEARISH_SWEEP"

    return None