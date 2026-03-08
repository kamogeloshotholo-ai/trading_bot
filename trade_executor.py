import os

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

if not DEMO_MODE:
    import MetaTrader5 as mt5
    ORDER_TYPE_BUY = mt5.ORDER_TYPE_BUY
    ORDER_TYPE_SELL = mt5.ORDER_TYPE_SELL
    TRADE_ACTION_DEAL = mt5.TRADE_ACTION_DEAL
    ORDER_TIME_GTC = mt5.ORDER_TIME_GTC
    ORDER_FILLING_IOC = mt5.ORDER_FILLING_IOC
else:
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    TRADE_ACTION_DEAL = 1
    ORDER_TIME_GTC = 0
    ORDER_FILLING_IOC = 0


def execute_trade(symbol, direction, sweep):

    if DEMO_MODE:
        print(f"DEMO: Executing {direction} trade on {symbol}")
        return

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
        "action": TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": ORDER_TYPE_BUY if direction == "BUY" else ORDER_TYPE_SELL,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,
        "magic": 10001,
        "comment": "AI Liquidity Bot",
        "type_time": ORDER_TIME_GTC,
        "type_filling": ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    # log the trade locally regardless of MT5 response
    try:
        from trade_logger import log_trade
        log_trade(symbol, direction, price, stop_loss, take_profit, lot)
    except Exception as e:
        print("Failed to log trade:", e)

    print("Trade executed:", result)