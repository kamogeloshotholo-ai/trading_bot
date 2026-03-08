import optuna
from backtester import run_backtest

symbols = ["EURUSD", "XAUUSD", "NAS100"]

def objective(trial):
    symbol = trial.suggest_categorical("symbol", symbols)
    stop_loss = trial.suggest_int("stop_loss", 5, 50, step=5)  # pips
    take_profit = trial.suggest_int("take_profit", 10, 100, step=10)  # pips

    result = run_backtest(symbol, stop_loss, take_profit)
    balance = result["balance"]

    return balance  # maximize balance

def optimize():
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=50)  # run 50 trials

    best_trial = study.best_trial
    print("\nBEST RESULT")
    print("Symbol:", best_trial.params["symbol"])
    print("Stop Loss:", best_trial.params["stop_loss"])
    print("Take Profit:", best_trial.params["take_profit"])
    print("Balance:", best_trial.value)

    # Save study for later analysis
    study.trials_dataframe().to_csv("optimization_results.csv", index=False)
    print("Optimization results saved to optimization_results.csv")

if __name__ == "__main__":
    optimize()