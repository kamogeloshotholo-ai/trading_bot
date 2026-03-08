import os

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

if not DEMO_MODE:
    import MetaTrader5 as mt5
    POSITION_TYPE_BUY = mt5.POSITION_TYPE_BUY
    TRADE_ACTION_SLTP = mt5.TRADE_ACTION_SLTP
else:
    POSITION_TYPE_BUY = 0
    TRADE_ACTION_SLTP = 6


def manage_open_trades():

    if DEMO_MODE:
        print("DEMO: Managing open trades (none)")
        return

    positions = mt5.positions_get()

    if positions is None:
        return

    for position in positions:

        symbol = position.symbol
        ticket = position.ticket
        sl = position.sl
        tp = position.tp

        if sl == 0 or tp == 0:

            print(f"{symbol} Trade MISSING SL or TP — attempting fix (ticket: {ticket})")

            # CRITICAL: Ensure symbol is selected for trading
            if not mt5.symbol_select(symbol, True):
                print(f"⚠️ {symbol} ERROR: Cannot select symbol for trading")
                continue

            tick = mt5.symbol_info_tick(symbol)
            
            if tick is None:
                print(f"{symbol} ERROR: Cannot get tick data, skipping SL/TP fix")
                continue

            # Get symbol info to respect precision and minimum distance
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                print(f"{symbol} ERROR: Cannot get symbol info, skipping SL/TP fix")
                continue

            point = symbol_info.point
            digits = symbol_info.digits
            stop_level = symbol_info.trade_stops_level  # Minimum stop distance in points

            # Ensure SL/TP distances meet minimum requirements
            min_sl_distance = max(500, stop_level)
            min_tp_distance = max(1000, stop_level)

            if position.type == POSITION_TYPE_BUY:
                price = tick.ask
                sl = round(price - min_sl_distance * point, digits)
                tp = round(price + min_tp_distance * point, digits)
            else:
                price = tick.bid
                sl = round(price + min_sl_distance * point, digits)
                tp = round(price - min_tp_distance * point, digits)

            request = {
                "action": TRADE_ACTION_SLTP,
                "position": ticket,
                "sl": sl,
                "tp": tp,
            }

            print(f"   Sending: SL={sl}, TP={tp}, Price={price}")
            
            result = mt5.order_send(request)
            
            # Check if the order was successful
            if result is None:
                print(f"⚠️ {symbol} ERROR: order_send returned None (ticket: {ticket})")
            elif hasattr(result, 'retcode'):
                if result.retcode == 10009:  # TRADE_RETCODE_DONE
                    print(f"✓ {symbol} SL/TP FIXED successfully | SL: {sl} | TP: {tp}")
                else:
                    # Show actual error code and comment
                    error_msg = f"{result.retcode}"
                    if hasattr(result, 'comment'):
                        error_msg += f" - {result.comment}"
                    print(f"⚠️ {symbol} ERROR CODE {error_msg} (ticket: {ticket})")
                    print(f"   Debug: SL={sl}, TP={tp}, Price={price}")
            else:
                print(f"⚠️ {symbol} ERROR: Unexpected response from order_send")

        else:
            print(f"{symbol} Trade OK | SL: {sl} | TP: {tp}")