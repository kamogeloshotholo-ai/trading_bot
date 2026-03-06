import MetaTrader5 as mt5


def get_h4_bias(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 0, 4)

    if rates is None or len(rates) < 4:
        return None

    high1 = rates[0]['high']
    high2 = rates[1]['high']
    high3 = rates[2]['high']

    low1 = rates[0]['low']
    low2 = rates[1]['low']
    low3 = rates[2]['low']

    # Uptrend: Higher highs and higher lows
    if high1 > high2 > high3 and low1 > low2 > low3:
        return "UP"

    # Downtrend: Lower highs and lower lows
    elif high1 < high2 < high3 and low1 < low2 < low3:
        return "DOWN"

    else:
        return "NONE"