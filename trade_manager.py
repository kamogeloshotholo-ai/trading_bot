import MetaTrader5 as mt5


def manage_open_trades():

    positions = mt5.positions_get()

    if positions is None:
        return

    for position in positions:

        symbol = position.symbol
        ticket = position.ticket
        price_open = position.price_open

        print("Managing trade:", ticket, symbol)