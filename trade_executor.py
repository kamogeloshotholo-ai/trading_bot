import MetaTrader5 as mt5
from risk_calculator import calculate_lot_size


def execute_trade(symbol, direction, sweep):

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        print("No tick data for", symbol)
        return

    if direction == "BUY":
        price = tick.ask
    else:
        price = tick.bid


    # Stop loss from sweep candle
    sweep_high = sweep.get("sweep_high")
    sweep_low = sweep.get("sweep_low")

    if direction == "SELL":
        stop_loss = sweep_high
        take_profit = price - (stop_loss - price) * 2

    else:
        stop_loss = sweep_low
        take_profit = price + (price - stop_loss) * 2


    lot = calculate_lot_size(symbol, stop_loss, price)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,
        "magic": 10001,
        "comment": "AI Liquidity Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    print("Trade executed:", result)