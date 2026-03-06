import MetaTrader5 as mt5


def get_candle_type(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)

    if rates is None or len(rates) == 0:
        return None

    open_price = rates[0]['open']
    close_price = rates[0]['close']

    if close_price > open_price:
        return "Bullish"

    elif close_price < open_price:
        return "Bearish"

    else:
        return "Doji"