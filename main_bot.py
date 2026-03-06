import time
import MetaTrader5 as mt5

from strategy_engine import get_h4_bias
from asian_range import get_asian_range
from structure_detector import get_market_structure
from trade_executor import execute_trade
from chart_drawer import draw_asian_levels


symbol = "EURUSD"


def run_bot():

    if not mt5.initialize():
        print("MT5 initialization failed")
        return

    print("BOT STARTED")

    while True:

        bias = get_h4_bias(symbol)

        asian_high, asian_low = get_asian_range(symbol)

        if asian_high is None:
            print("Asian range not ready")
            time.sleep(60)
            continue

        draw_asian_levels(symbol, asian_high, asian_low)

        structure = get_market_structure(symbol)

        print("Bias:", bias)
        print("Structure:", structure)

        if bias == "UP" and structure == "BULLISH_BOS":
            print("BUY SIGNAL")
            execute_trade(symbol, "BUY")

        elif bias == "DOWN" and structure == "BEARISH_BOS":
            print("SELL SIGNAL")
            execute_trade(symbol, "SELL")

        time.sleep(60)


if __name__ == "__main__":
    run_bot()