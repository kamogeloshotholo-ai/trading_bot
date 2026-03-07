import time
import MetaTrader5 as mt5
from datetime import datetime

from liquidity_sweep import detect_liquidity_sweep
from retest_detector import detect_retest
from trade_executor import execute_trade
from trade_manager import manage_open_trades


# Symbols the bot trades
symbols = ["EURUSD", "XAUUSD", "NAS100"]


# Risk controls
max_trades_per_day = 2
trades_today = 0


# Track last candle
last_candle_time = {}


# Track day reset
current_day = datetime.now().day


# Store sweeps waiting for retest
sweep_setups = {}


# -----------------------------
# CONNECT TO MT5
# -----------------------------

def connect():

    print("Connecting to MT5...")

    if not mt5.initialize():
        print("MT5 initialization failed")
        quit()

    print("MT5 connected")

    # Wait until MT5 provides account info
    for i in range(10):

        account = mt5.account_info()

        if account is not None:
            print("Account balance:", account.balance)
            return

        print("Waiting for MT5 account info...")
        time.sleep(1)

    print("Could not read account info, but continuing...")


# -----------------------------
# NEW CANDLE DETECTION
# -----------------------------

def new_candle(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)

    if rates is None or len(rates) == 0:
        print("Waiting for market data...")
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
# ASIAN SESSION FILTER
# -----------------------------

def asian_session_running():

    now = datetime.now()

    if now.hour < 7:
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

        print("Daily trade counter reset")


# -----------------------------
# MAIN BOT LOOP
# -----------------------------

def run_bot():

    global trades_today
    global sweep_setups

    connect()

    print("BOT STARTED")

    while True:

        reset_daily_trades()

        if asian_session_running():

            print("Asian session running... waiting for London")

            time.sleep(300)
            continue


        manage_open_trades()


        if trades_today >= max_trades_per_day:

            print("Daily trade limit reached")

            time.sleep(300)
            continue


        for symbol in symbols:

            if not new_candle(symbol):
                continue


            print("New M5 candle detected on", symbol)


            sweep = detect_liquidity_sweep(symbol)

            if sweep:

                print(symbol, "Liquidity sweep detected")

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

        time.sleep(300)


run_bot()