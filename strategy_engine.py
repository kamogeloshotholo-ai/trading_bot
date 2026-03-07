import MetaTrader5 as mt5


def get_h4_bias(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 0, 10)

    if rates is None or len(rates) < 10:
        return None

    highs = [r['high'] for r in rates]
    lows = [r['low'] for r in rates]

    higher_highs = 0
    lower_lows = 0

    for i in range(len(highs) - 1):

        if highs[i] > highs[i + 1]:
            higher_highs += 1

        if lows[i] < lows[i + 1]:
            lower_lows += 1

    if higher_highs >= 6 and lower_lows >= 6:
        return "UP"

    if higher_highs <= 3 and lower_lows <= 3:
        return "DOWN"

    return "NONE"