account_balance = float(input("Account balance: "))
risk_percent = float(input("Risk percent: "))
stop_loss_pips = float(input("Stop loss (pips): "))

risk_amount = account_balance * (risk_percent / 100)

pip_value_per_lot = 10
lot_size = risk_amount / (stop_loss_pips * pip_value_per_lot)

print("Risk amount:", risk_amount)
print("Lot size:", round(lot_size, 2))