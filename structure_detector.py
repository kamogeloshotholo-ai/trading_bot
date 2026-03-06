import MetaTrader5 as mt5


def get_market_structure(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 20)

    if rates is None or len(rates) < 10:
        return None

    highs = [candle['high'] for candle in rates]
    lows = [candle['low'] for candle in rates]

    last_high = highs[-1]
    prev_high = highs[-2]

    last_low = lows[-1]
    prev_low = lows[-2]

    # Bullish Break Of Structure
    if last_high > prev_high:
        return "BULLISH_BOS"

    # Bearish Break Of Structure
    if last_low < prev_low:
        return "BEARISH_BOS"

    return "NO_STRUCTURE"