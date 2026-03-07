import time
import MetaTrader5 as mt5
from datetime import datetime

from liquidity_sweep import detect_liquidity_sweep
from retest_detector import detect_retest
from trade_executor import execute_trade
from trade_manager import manage_open_trades
from sweep_memory import reset_sweep_memory, sweep_already_detected, store_sweep


# -----------------------------
# SYMBOLS
# -----------------------------

symbols = ["EURUSD", "XAUUSD", "NAS100", "BTCUSD"]


# -----------------------------
# RISK SETTINGS
# -----------------------------

max_trades_per_day = 2
trades_today = 0


# -----------------------------
# MEMORY
# -----------------------------

last_candle_time = {}
sweep_setups = {}

current_day = datetime.now().day


# -----------------------------
# CONNECT MT5
# -----------------------------

def connect():

    print("Connecting to MT5...")

    if not mt5.initialize():
        print("MT5 initialization failed")
        quit()

    print("MT5 connected")

    account = mt5.account_info()

    if account is not None:
        print("Account balance:", account.balance)
    else:
        print("Account info not available")


# -----------------------------
# NEW CANDLE DETECTION
# -----------------------------

def new_candle(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)

    if rates is None or len(rates) == 0:
        return False

    candle_time = rates[0]["time"]

    if symbol not in last_candle_time:
        last_candle_time[symbol] = candle_time
        return False

    if candle_time != last_candle_time[symbol]:
        last_candle_time[symbol] = candle_time
        return True

    return False


# -----------------------------
# RESET DAILY TRADES
# -----------------------------

def reset_daily_trades():

    global trades_today
    global current_day

    now = datetime.now()

    if now.day != current_day:

        trades_today = 0
        current_day = now.day

        print("Daily trades reset")


# -----------------------------
# MAIN BOT
# -----------------------------

def run_bot():

    global trades_today
    global sweep_setups

    connect()

    print("BOT STARTED")

    while True:

        reset_daily_trades()
        reset_sweep_memory()

        manage_open_trades()

        if trades_today >= max_trades_per_day:

            print("Daily trade limit reached")
            time.sleep(60)
            continue


        for symbol in symbols:

            if not new_candle(symbol):
                continue

            print("New M5 candle detected on", symbol)

            sweep = detect_liquidity_sweep(symbol)

            if sweep:

                if sweep_already_detected(symbol):

                    print(symbol, "Sweep already detected")
                    continue

                print(symbol, "Liquidity sweep detected")

                store_sweep(symbol, sweep)

                sweep_setups[symbol] = sweep


            if symbol in sweep_setups:

                signal = detect_retest(symbol, sweep_setups[symbol])

                if signal:

                    print(symbol, "Trade signal:", signal)

                    execute_trade(symbol, signal, sweep_setups[symbol])

                    trades_today += 1

                    print("Trades today:", trades_today)

                    del sweep_setups[symbol]


        print("Waiting for next candle...")

        time.sleep(30)


run_bot()