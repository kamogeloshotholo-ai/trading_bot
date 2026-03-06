import MetaTrader5 as mt5
from asian_range import get_asian_range
from datetime import datetime


LONDON_START = 7
LONDON_END = 16


def check_london_session():

    now = datetime.now()

    if LONDON_START <= now.hour <= LONDON_END:
        return True

    return False


def get_trade_signal(symbol, bias):

    asian_high, asian_low = get_asian_range(symbol)

    if asian_high is None:
        return None

    tick = mt5.symbol_info_tick(symbol)
    price = tick.bid

    if not check_london_session():
        print("Outside London session")
        return None

    print("Asian High:", asian_high)
    print("Asian Low:", asian_low)
    print("Current Price:", price)

    if bias == "UP":

        if price < asian_low:
            print("Asian low sweep detected -> BUY setup")
            return "BUY"

    if bias == "DOWN":

        if price > asian_high:
            print("Asian high sweep detected -> SELL setup")
            return "SELL"

    return None