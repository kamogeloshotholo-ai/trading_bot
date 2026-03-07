import MetaTrader5 as mt5
from datetime import datetime
from asian_range import get_asian_range


def detect_liquidity_sweep(symbol):

    asian_high, asian_low = get_asian_range(symbol)

    if asian_high is None or asian_low is None:
        return None

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 2)

    if rates is None or len(rates) < 2:
        return None

    last_candle = rates[1]

    high = last_candle["high"]
    low = last_candle["low"]
    close = last_candle["close"]

    # SELL setup (sweep above Asian high)
    if high > asian_high and close < asian_high:

        print(symbol, "Liquidity sweep ABOVE Asian High")

        return {
            "direction": "SELL",
            "level": asian_high
        }

    # BUY setup (sweep below Asian low)
    if low < asian_low and close > asian_low:

        print(symbol, "Liquidity sweep BELOW Asian Low")

        return {
            "direction": "BUY",
            "level": asian_low
        }

    return None