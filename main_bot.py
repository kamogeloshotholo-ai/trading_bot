import time
import MetaTrader5 as mt5

from candle_logic import get_candle_type
from structure_detector import detect_structure
from strategy_engine import get_h4_bias
from trade_executor import execute_trade
from trade_manager import manage_open_trades


# CONNECT TO MT5
if not mt5.initialize():
    print("MT5 initialization failed")
    quit()

print("MT5 connected successfully")


# PAIRS TO TRADE
pairs = ["EURUSD"]


# TRADE LIMIT
trades_today = 0
max_trades_per_day = 2


# TRACK LAST CANDLE
last_candle_time = None


print("BOT STARTED")


def check_trade_signal(symbol):

    bias = get_h4_bias(symbol)
    structure = detect_structure(symbol)
    candle = get_candle_type(symbol)

    print("H4 Bias:", bias)
    print("H1 Structure:", structure)
    print("M5 Candle:", candle)

    if bias != "DOWN" and structure == "UP" and candle == "Bullish":
        return "BUY"

    elif bias == "DOWN" and structure == "DOWN" and candle == "Bearish":
        return "SELL"

    else:
        print("NO TRADE")
        return None


while True:

    # GET CURRENT M5 CANDLE
    rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M5, 0, 1)

    if rates is None:
        print("Failed to get market data")
        time.sleep(5)
        continue

    current_candle_time = rates[0]['time']

    # WAIT FOR NEW CANDLE
    if last_candle_time == current_candle_time:
        time.sleep(5)
        continue

    last_candle_time = current_candle_time

    print("\nNEW M5 CANDLE DETECTED\n")

    manage_open_trades()

    for symbol in pairs:

        if trades_today >= max_trades_per_day:
            print("Max trades reached today")
            break

        signal = check_trade_signal(symbol)

        if signal == "BUY":

            print(symbol, "BUY signal detected")

            execute_trade(symbol, "BUY")

            trades_today += 1

        elif signal == "SELL":

            print(symbol, "SELL signal detected")

            execute_trade(symbol, "SELL")

            trades_today += 1