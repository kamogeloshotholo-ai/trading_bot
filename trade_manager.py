import MetaTrader5 as mt5


def manage_open_trades():

    positions = mt5.positions_get()

    if positions is None:
        return

    for position in positions:

        symbol = position.symbol
        ticket = position.ticket
        sl = position.sl
        tp = position.tp

        if sl == 0 or tp == 0:

            print(symbol, "Trade missing SL or TP — fixing")

            tick = mt5.symbol_info_tick(symbol)

            if position.type == mt5.POSITION_TYPE_BUY:
                price = tick.ask
                sl = price - 0.0020
                tp = price + 0.0040

            else:
                price = tick.bid
                sl = price + 0.0020
                tp = price - 0.0040

            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": ticket,
                "sl": sl,
                "tp": tp,
            }

            mt5.order_send(request)

        print(symbol, "Trade monitored | SL:", sl, "| TP:", tp)