import csv
from datetime import datetime

def log_trade(symbol, direction, entry, sl, tp, volume):

    file = "trade_log.csv"

    with open(file, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now(),
            symbol,
            direction,
            entry,
            sl,
            tp,
            volume
        ])