import MetaTrader5 as mt5


def detect_structure(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 3)

    if rates is None or len(rates) < 3:
        return None

    high1 = rates[0]['high']
    high2 = rates[1]['high']

    low1 = rates[0]['low']
    low2 = rates[1]['low']

    if high1 > high2 and low1 > low2:
        return "UP"

    if high1 < high2 and low1 < low2:
        return "DOWN"

    return "NONE"


def get_recent_swing(symbol, timeframe, bars=20):

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

    highs = [r['high'] for r in rates]
    lows = [r['low'] for r in rates]

    swing_high = max(highs)
    swing_low = min(lows)

    return swing_high, swing_low


def get_liquidity_target(symbol, timeframe, direction, bars=50):

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

    highs = [r['high'] for r in rates]
    lows = [r['low'] for r in rates]

    current_price = rates[0]['close']

    if direction == "BUY":

        targets = [h for h in highs if h > current_price]

        if targets:
            return min(targets)

    if direction == "SELL":

        targets = [l for l in lows if l < current_price]

        if targets:
            return max(targets)

    return None