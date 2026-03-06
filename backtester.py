import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime


symbol = "EURUSD"
lot = 0.01
stop_loss_pips = 20
take_profit_pips = 40


def connect():
    if not mt5.initialize():
        print("MT5 failed")
        quit()


def get_data():

    rates = mt5.copy_rates_from_pos(
        symbol,
        mt5.TIMEFRAME_M5,
        0,
        5000
    )

    df = pd.DataFrame(rates)

    df['time'] = pd.to_datetime(df['time'], unit='s')

    return df


def backtest():

    connect()

    data = get_data()

    balance = 1000
    wins = 0
    losses = 0

    for i in range(50, len(data)):

        candle = data.iloc[i]

        price = candle['close']

        # Fake signal example
        if price > data['high'].iloc[i-10:i].max():

            entry = price
            sl = entry + 0.0020
            tp = entry - 0.0040

            future = data.iloc[i:i+20]

            for _, f in future.iterrows():

                if f['high'] >= sl:
                    balance -= 10
                    losses += 1
                    break

                if f['low'] <= tp:
                    balance += 20
                    wins += 1
                    break

    print("Backtest Results")
    print("----------------")
    print("Balance:", balance)
    print("Wins:", wins)
    print("Losses:", losses)

    total = wins + losses

    if total > 0:
        winrate = (wins / total) * 100
        print("Winrate:", round(winrate,2), "%")


backtest()