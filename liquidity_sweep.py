import MetaTrader5 as mt5
from asian_range import get_asian_range


def detect_liquidity_sweep(symbol):

    # Get Asian range
    asian_high, asian_low = get_asian_range(symbol)

    if asian_high is None or asian_low is None:
        return None

    # Get last 2 candles
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 2)

    if rates is None or len(rates) < 2:
        return None

    last_candle = rates[1]

    high = last_candle["high"]
    low = last_candle["low"]
    close = last_candle["close"]

    # SELL sweep (above Asian High)
    if high > asian_high and close < asian_high:

        print(symbol, "Liquidity sweep ABOVE Asian High")

        return {
            "direction": "SELL",
            "level": asian_high
        }

    # BUY sweep (below Asian Low)
    if low < asian_low and close > asian_low:

        print(symbol, "Liquidity sweep BELOW Asian Low")

        return {
            "direction": "BUY",
            "level": asian_low
        }

    return None