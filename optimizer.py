import itertools
from backtester import run_backtest

symbols = ["EURUSD", "XAUUSD", "NAS100"]

stop_losses = [10, 15, 20, 25]
take_profits = [20, 30, 40, 50]

best_balance = 0
best_params = None
best_symbol = None

def optimize():

    global best_balance, best_params, best_symbol

    for symbol in symbols:

        print(f"\nTesting symbol: {symbol}")

        for sl, tp in itertools.product(stop_losses, take_profits):

            print(f"Testing SL={sl} TP={tp}")

            result = run_backtest(symbol, sl, tp)

            balance = result["balance"]

            if balance > best_balance:

                best_balance = balance
                best_params = (sl, tp)
                best_symbol = symbol

    print("\nBEST RESULT")
    print("Symbol:", best_symbol)
    print("Balance:", best_balance)
    print("Best Parameters:", best_params)


if __name__ == "__main__":
    optimize()