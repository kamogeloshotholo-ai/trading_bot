import MetaTrader5 as mt5
from trade_logger import log_trade


def execute_trade(symbol, signal):

    account = mt5.account_info()

    balance = account.balance

    # RISK SETTINGS
    risk_percent = 0.01   # 1% risk per trade

    risk_amount = balance * risk_percent


    tick = mt5.symbol_info_tick(symbol)

    pip = 0.0001
    stop_loss_pips = 20
    take_profit_pips = 40


    pip_value_per_lot = 10

    lot = risk_amount / (stop_loss_pips * pip_value_per_lot)

    lot = round(lot, 2)


    deviation = 20
    magic = 123456


    if signal == "BUY":

        price = tick.ask
        sl = price - (stop_loss_pips * pip)
        tp = price + (take_profit_pips * pip)
        order_type = mt5.ORDER_TYPE_BUY


    elif signal == "SELL":

        price = tick.bid
        sl = price + (stop_loss_pips * pip)
        tp = price - (take_profit_pips * pip)
        order_type = mt5.ORDER_TYPE_SELL


    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": "Python Algo Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    result = mt5.order_send(request)

    print("Trade result:", result)

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        log_trade(symbol, signal, price, sl, tp, lot)

    mt5.shutdown()