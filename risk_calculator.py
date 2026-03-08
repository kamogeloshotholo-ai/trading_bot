import MetaTrader5 as mt5

# default values for risk calculations
DEFAULT_RISK_PERCENT = 1.0  # percent of account balance to risk per trade
PIP_VALUE_PER_LOT = 10      # typical pip value for a standard lot


def calculate_lot_size(symbol, stop_loss_price, entry_price, risk_percent=DEFAULT_RISK_PERCENT):
    """Calculate a lot size based on account balance and stop loss distance.

    Args:
        symbol (str): Trading symbol (e.g. "EURUSD").
        stop_loss_price (float): Price level of the stop loss.
        entry_price (float): Price at which the order will be placed.
        risk_percent (float): Percentage of account balance to risk (default 1%).

    Returns:
        float: Lot size rounded to two decimals (minimum 0.01).
    """

    account = mt5.account_info()
    if account is None:
        print("Unable to retrieve account info, defaulting to 0.01 lot")
        return 0.01

    balance = account.balance
    risk_amount = balance * (risk_percent / 100.0)

    info = mt5.symbol_info(symbol)
    if info is None or info.point == 0:
        print("Symbol info unavailable, defaulting to 0.01 lot")
        return 0.01

    # convert price difference to pips
    stop_loss_distance = abs(entry_price - stop_loss_price)
    stop_loss_pips = stop_loss_distance / info.point

    if stop_loss_pips == 0:
        return 0.01

    lot = risk_amount / (stop_loss_pips * PIP_VALUE_PER_LOT)
    lot = max(0.01, lot)
    return round(lot, 2)


if __name__ == "__main__":
    # simple interactive mode for manual calculations
    try:
        account_balance = float(input("Account balance: "))
        risk_percent = float(input("Risk percent (e.g. 1 for 1%): "))
        stop_loss_pips = float(input("Stop loss (pips): "))

        risk_amount = account_balance * (risk_percent / 100)
        lot_size = risk_amount / (stop_loss_pips * PIP_VALUE_PER_LOT)

        print("Risk amount:", risk_amount)
        print("Lot size:", round(lot_size, 2))
    except Exception as e:
        print("Error in interactive mode:", e)