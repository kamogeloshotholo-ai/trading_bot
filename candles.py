import MetaTrader5 as mt5
from datetime import datetime

# connect to MetaTrader
mt5.initialize()

symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M5

# get last 10 candles
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 10)

for rate in rates:
    time = datetime.fromtimestamp(rate['time'])
    print("Time:", time)
    print("Open:", rate['open'])
    print("High:", rate['high'])
    print("Low:", rate['low'])
    print("Close:", rate['close'])
    print("----------------------")

mt5.shutdown()