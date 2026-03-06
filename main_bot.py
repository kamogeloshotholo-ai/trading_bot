import time
import MetaTrader5 as mt5
from datetime import datetime

from strategy_engine import get_h4_bias
from asian_range import get_asian_range
from structure_detector import detect_retest
from trade_executor import execute_trade
from chart_drawer import draw_asian_levels, draw_trade_arrow


symbol = "EURUSD"

last_trade_day = None


def run_bot():

    global last_trade_day

    if not mt5.initialize():
        print("MT5 initialization failed")
        return

    print("BOT STARTED")

    while True:

        today = datetime.now().date()

        bias = get_h4_bias(symbol)

        asian_high, asian_low = get_asian_range(symbol)

        if asian_high is None:
            print("Asian range not ready")
            time.sleep(60)
            continue

        draw_asian_levels(symbol, asian_high, asian_low)

        signal = detect_retest(symbol, asian_high, asian_low)

        print("Bias:", bias)
        print("Signal:", signal)

        # Only one trade per day
        if last_trade_day == today:
            print("Trade already taken today")
            time.sleep(60)
            continue

        if bias == "UP" and signal == "BUY":

            print("BUY SIGNAL")

            execute_trade(symbol, "BUY")

            last_trade_day = today

        elif bias == "DOWN" and signal == "SELL":

            print("SELL SIGNAL")

            execute_trade(symbol, "SELL")

            last_trade_day = today

        time.sleep(60)


if __name__ == "__main__":
    run_bot()