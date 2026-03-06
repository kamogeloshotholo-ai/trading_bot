import MetaTrader5 as mt5
from datetime import datetime


def detect_sweep_and_retest(symbol, asian_high, asian_low, bias):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 20)

    if rates is None:
        return None

    last_candle = rates[-1]
    prev_candle = rates[-2]

    last_high = last_candle['high']
    last_low = last_candle['low']
    last_close = last_candle['close']

    prev_high = prev_candle['high']
    prev_low = prev_candle['low']

    # BUY logic (Asian Low sweep)
    if bias == "UP":

        if prev_low < asian_low and last_close > asian_low:
            print("Sweep and retest of Asian LOW detected")
            return "BUY"

    # SELL logic (Asian High sweep)
    if bias == "DOWN":

        if prev_high > asian_high and last_close < asian_high:
            print("Sweep and retest of Asian HIGH detected")
            return "SELL"

    return None