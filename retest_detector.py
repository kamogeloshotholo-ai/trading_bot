import os

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

if not DEMO_MODE:
    import MetaTrader5 as mt5
    TIMEFRAME_M5 = mt5.TIMEFRAME_M5
else:
    TIMEFRAME_M5 = 5


def detect_retest(symbol, sweep):

    if sweep is None:
        return None

    if DEMO_MODE:
        # Mock retest
        import random
        if random.choice([True, False]):
            return sweep["direction"]
        else:
            return None

    direction = sweep["direction"]
    level = sweep["level"]

    rates = mt5.copy_rates_from_pos(symbol, TIMEFRAME_M5, 0, 1)

    if rates is None or len(rates) == 0:
        return None

    candle = rates[0]

    high = candle["high"]
    low = candle["low"]
    close = candle["close"]

    # SELL retest
    if direction == "SELL":

        if high >= level and close < level:
            print(symbol, "Retest confirmed for SELL")
            return "SELL"

    # BUY retest
    if direction == "BUY":

        if low <= level and close > level:
            print(symbol, "Retest confirmed for BUY")
            return "BUY"

    return None