import time
import MetaTrader5 as mt5
from datetime import datetime

from candle_logic import get_candle_type
from structure_detector import detect_structure
from strategy_engine import get_h4_bias
from trade_executor import execute_trade
from trade_manager import manage_open_trades


# Pairs the bot will trade
symbols = ["EURUSD", "XAUUSD", "NAS100"]


# Risk control
max_trades_per_day = 2
trades_today = 0


# Track last candle
last_candle_time = None


def connect():

    if not mt5.initialize():
        print("MT5 initialization failed")
        quit()

    print("MT5 connected")


def new_candle(symbol):

    global last_candle_time

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)

    # Prevent crash if market closed
    if rates is None or len(rates) == 0:
        print("Waiting for market data...")
        return False

    candle_time = rates[0]["time"]

    if last_candle_time is None:
        last_candle_time = candle_time
        return False

    if candle_time != last_candle_time:
        last_candle_time = candle_time
        return True

    return False


def check_trade_signal(symbol):

    bias = get_h4_bias(symbol)
    structure = detect_structure(symbol)
    candle = get_candle_type(symbol)

    print(symbol, "| Bias:", bias, "| Structure:", structure, "| Candle:", candle)

    if bias == "UP" and structure == "UP" and candle == "Bullish":
        return "BUY"

    if bias == "DOWN" and structure == "DOWN" and candle == "Bearish":
        return "SELL"

    return None


def run_bot():

    global trades_today

    connect()

    print("BOT STARTED")

    while True:

        manage_open_trades()

        if trades_today >= max_trades_per_day:
            print("Daily trade limit reached")
            time.sleep(60)
            continue

        for symbol in symbols:

            if not new_candle(symbol):
                continue

            print("New M5 candle detected on", symbol)

            signal = check_trade_signal(symbol)

            if signal:

                print(symbol, "Trade signal:", signal)

                execute_trade(symbol, signal)

                trades_today += 1

                print("Trades today:", trades_today)

            else:

                print(symbol, "No trade setup")

        time.sleep(300)


run_bot()