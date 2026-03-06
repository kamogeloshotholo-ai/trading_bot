import time
import MetaTrader5 as mt5
from datetime import datetime

from strategy_engine import get_h4_bias
from asian_range import get_asian_range
from structure_detector import detect_retest
from trade_executor import execute_trade


symbol = "EURUSD"

last_trade_day = None


def run_bot():

    global last_trade_day

    if not mt5.initialize():
        print("MT5 initialization failed")
        return

    print("BOT STARTED")

    while True:

        now = datetime.now()
        today = now.date()

        # Wait for Asian session to finish (before 06:00)
        if now.hour < 6:
            print("Asian session still running... waiting")
            time.sleep(60)
            continue

        # Reset once per day
        if last_trade_day != today:
            print("New day detected → resetting Asian range")
            last_trade_day = today

        # Get Asian session range
        asian_high, asian_low = get_asian_range(symbol)

        if asian_high is None:
            print("Asian range not ready")
            time.sleep(60)
            continue

        print("Asian High:", asian_high)
        print("Asian Low:", asian_low)

        # Get H4 bias
        bias = get_h4_bias(symbol)
        print("Bias:", bias)

        # Detect sweep + retest
        signal = detect_retest(symbol, asian_high, asian_low, bias)

        if signal is None:
            print("Waiting for sweep + retest...")
        else:
            print("Trade signal:", signal)

            execute_trade(symbol, signal)

            print("TRADE EXECUTED:", signal)

        time.sleep(60)


run_bot()