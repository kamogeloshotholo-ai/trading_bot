import MetaTrader5 as mt5
from liquidity_map import get_liquidity_levels


def detect_liquidity_sweep(symbol, liquidity_source="ASIAN"):

    # Get liquidity levels
    liquidity_high, liquidity_low = get_liquidity_levels(symbol, liquidity_source)

    if liquidity_high is None or liquidity_low is None:
        return None

    # Get last 2 candles
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 2)

    if rates is None or len(rates) < 2:
        return None

    candle = rates[1]

    high = candle["high"]
    low = candle["low"]
    close = candle["close"]

    # Sweep ABOVE liquidity high
    if high > liquidity_high and close < liquidity_high:

        print(symbol, "Liquidity sweep ABOVE high")

        return {
            "direction": "SELL",
            "level": liquidity_high,
            "sweep_high": high,
            "sweep_low": low
        }

    # Sweep BELOW liquidity low
    if low < liquidity_low and close > liquidity_low:

        print(symbol, "Liquidity sweep BELOW low")

        return {
            "direction": "BUY",
            "level": liquidity_low,
            "sweep_high": high,
            "sweep_low": low
        }

    return None