import MetaTrader5 as mt5
from structure_detector import get_recent_swing, get_liquidity_target


RISK_PERCENT = 0.01


def calculate_lot(symbol, stop_distance):

    account = mt5.account_info()

    balance = account.balance

    risk_amount = balance * RISK_PERCENT

    pip_value = 10

    lot = risk_amount / (stop_distance * pip_value)

    lot = max(0.01, round(lot, 2))

    return lot


def execute_trade(symbol, signal):

    tick = mt5.symbol_info_tick(symbol)

    if signal == "BUY":
        entry = tick.ask
    else:
        entry = tick.bid

    swing_high, swing_low = get_recent_swing(symbol, mt5.TIMEFRAME_M5)

    if signal == "BUY":
        stop_loss = swing_low
    else:
        stop_loss = swing_high

    stop_distance = abs(entry - stop_loss) * 10000

    lot = calculate_lot(symbol, stop_distance)

    tp = get_liquidity_target(symbol, mt5.TIMEFRAME_M5, signal)

    if tp is None:
        print(symbol, "No liquidity target found — skipping trade")
        return

    risk = abs(entry - stop_loss)
    reward = abs(tp - entry)

    if reward / risk < 1.5:
        print(symbol, "Risk reward too small — skipping trade")
        return

    if signal == "BUY":
        order_type = mt5.ORDER_TYPE_BUY
        price = entry
    else:
        order_type = mt5.ORDER_TYPE_SELL
        price = entry

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": stop_loss,
        "tp": tp,
        "deviation": 20,
        "magic": 1001,
        "comment": "AI_BOT",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    result = mt5.order_send(request)

    print(symbol, "Trade result:", result)