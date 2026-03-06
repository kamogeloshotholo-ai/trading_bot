import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# starting balance for tests
START_BALANCE = 1000

# timeframe used for testing
TIMEFRAME = mt5.TIMEFRAME_M5

# number of candles to load
CANDLES = 5000


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


def run_backtest(symbol, stop_loss_pips, take_profit_pips):

    connect()

    data = get_data(symbol)

    if data is None:
        return {"balance": START_BALANCE, "wins": 0, "losses": 0}

    balance = START_BALANCE
    wins = 0
    losses = 0

    print(f"\nRunning backtest for {symbol}")
    print(f"SL={stop_loss_pips} TP={take_profit_pips}")

    for i in range(50, len(data) - 20):

        candle = data.iloc[i]

        price = candle["close"]

        # simple breakout logic placeholder
        if price > data["high"].iloc[i - 10:i].max():

            entry = price
            sl = entry + (stop_loss_pips * 0.0001)
            tp = entry - (take_profit_pips * 0.0001)

            future = data.iloc[i:i + 20]

            for _, f in future.iterrows():

                if f["high"] >= sl:
                    balance -= 10
                    losses += 1
                    break

                if f["low"] <= tp:
                    balance += 20
                    wins += 1
                    break

    total = wins + losses

    winrate = 0
    if total > 0:
        winrate = (wins / total) * 100

    print("Results:")
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

    # quick test run
    result = run_backtest("EURUSD", 20, 40)

    print("\nTest run finished")
    print(result)