import MetaTrader5 as mt5

# connect to MetaTrader 5
mt5.initialize()

symbol = "EURUSD"

tick = mt5.symbol_info_tick(symbol)

print("Symbol:", symbol)
print("Bid:", tick.bid)
print("Ask:", tick.ask)

mt5.shutdown()