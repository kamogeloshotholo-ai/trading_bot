import MetaTrader5 as mt5


def get_h4_bias(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 0, 3)

    if rates is None or len(rates) < 3:
        return None

    high1 = rates[0]['high']
    high2 = rates[1]['high']

    low1 = rates[0]['low']
    low2 = rates[1]['low']

    # Uptrend
    if high1 > high2 and low1 > low2:
        return "UP"

    # Downtrend
    elif high1 < high2 and low1 < low2:
        return "DOWN"

    else:
        return "NONE"