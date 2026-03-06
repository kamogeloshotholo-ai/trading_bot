import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

START_BALANCE = 1000
TIMEFRAME = mt5.TIMEFRAME_M5
CANDLES = 20000


def connect():
    if not mt5.initialize():
        print("MT5 initialization failed")
        quit()


def get_data(symbol):

    rates = mt5.copy_rates_from_pos(
        symbol,
        TIMEFRAME,
        0,
        CANDLES
    )

    if rates is None:
        print("No data for", symbol)
        return None

    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(df["time"], unit="s")

    return df


def get_h4_bias(symbol, time_index):

    rates = mt5.copy_rates_from_pos(
        symbol,
        mt5.TIMEFRAME_H4,
        time_index,
        3
    )

    if rates is None or len(rates) < 3:
        return None

    high1 = rates[0]["high"]
    high2 = rates[1]["high"]

    low1 = rates[0]["low"]
    low2 = rates[1]["low"]

    if high1 > high2 and low1 > low2:
        return "UP"

    if high1 < high2 and low1 < low2:
        return "DOWN"

    return "NONE"


def calculate_asian_range(day_data):

    asian = day_data[
        (day_data["time"].dt.hour >= 0) &
        (day_data["time"].dt.hour < 6)
    ]

    if len(asian) == 0:
        return None, None

    asian_high = asian["high"].max()
    asian_low = asian["low"].min()

    return asian_high, asian_low


def run_backtest(symbol, stop_loss_pips, take_profit_pips):

    connect()

    data = get_data(symbol)

    if data is None:
        return {"balance": START_BALANCE, "wins": 0, "losses": 0}

    balance = START_BALANCE
    wins = 0
    losses = 0

    data["date"] = data["time"].dt.date

    for day in data["date"].unique():

        day_data = data[data["date"] == day]

        asian_high, asian_low = calculate_asian_range(day_data)

        if asian_high is None:
            continue

        trade_taken = False

        for i in range(len(day_data)):

            candle = day_data.iloc[i]

            price_high = candle["high"]
            price_low = candle["low"]
            price_close = candle["close"]

            if candle["time"].hour < 6:
                continue

            if trade_taken:
                break

            bias = get_h4_bias(symbol, 0)

            # SELL setup
            if bias == "DOWN" and price_high > asian_high:

                entry = price_close
                sl = entry + (stop_loss_pips * 0.0001)
                tp = entry - (take_profit_pips * 0.0001)

                future = day_data.iloc[i:i+30]

                for _, f in future.iterrows():

                    if f["high"] >= sl:
                        balance -= 10
                        losses += 1
                        trade_taken = True
                        break

                    if f["low"] <= tp:
                        balance += 20
                        wins += 1
                        trade_taken = True
                        break

            # BUY setup
            if bias == "UP" and price_low < asian_low:

                entry = price_close
                sl = entry - (stop_loss_pips * 0.0001)
                tp = entry + (take_profit_pips * 0.0001)

                future = day_data.iloc[i:i+30]

                for _, f in future.iterrows():

                    if f["low"] <= sl:
                        balance -= 10
                        losses += 1
                        trade_taken = True
                        break

                    if f["high"] >= tp:
                        balance += 20
                        wins += 1
                        trade_taken = True
                        break

    total = wins + losses

    winrate = 0
    if total > 0:
        winrate = (wins / total) * 100

    print("\nBacktest Results")
    print("----------------")
    print("Symbol:", symbol)
    print("Balance:", balance)
    print("Wins:", wins)
    print("Losses:", losses)
    print("Winrate:", round(winrate, 2), "%")

    return {
        "balance": balance,
        "wins": wins,
        "losses": losses
    }


if __name__ == "__main__":

    run_backtest("EURUSD", 20, 40)