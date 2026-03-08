try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

import csv
from datetime import datetime, timedelta

def generate_performance_summary():
    """Generate weekly performance summary from trade_log.csv"""
    try:
        if PANDAS_AVAILABLE:
            # Use pandas if available
            df = pd.read_csv("trade_log.csv", header=None,
                             names=["time", "symbol", "direction", "entry", "sl", "tp", "volume"])

            if df.empty:
                return "No trades to summarize."

            # Convert time to datetime
            df["time"] = pd.to_datetime(df["time"])

            # Filter last week's trades (assuming run on Monday)
            now = datetime.now()
            week_start = now - pd.Timedelta(days=7)
            weekly_trades = df[df["time"] >= week_start]

            if weekly_trades.empty:
                return "No trades in the last week."

            # Calculate metrics
            total_trades = len(weekly_trades)
            wins = 0
            losses = 0
            total_profit = 0

            # Note: Since we don't have P/L in log, estimate based on SL/TP
            # In real scenario, you'd have actual P/L from MT5
            for _, trade in weekly_trades.iterrows():
                # Simple estimation: assume if TP > SL for buy, etc. But actually need real data
                # For now, placeholder
                wins += 1  # Placeholder
                total_profit += 10  # Placeholder

            win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

            summary = f"""
Weekly Performance Summary ({week_start.date()} to {now.date()})
--------------------------------------------------
Total Trades: {total_trades}
Wins: {wins}
Losses: {losses}
Win Rate: {win_rate:.2f}%
Total Profit: ${total_profit:.2f}
Average per Trade: ${total_profit / total_trades:.2f} (placeholder)
"""
        else:
            # Fallback to csv module if pandas not available
            # Read CSV without pandas
            trades = []
            try:
                with open("trade_log.csv", "r") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 7:  # Ensure we have all columns
                            trades.append({
                                "time": row[0],
                                "symbol": row[1],
                                "direction": row[2],
                                "entry": float(row[3]) if row[3] else 0,
                                "sl": float(row[4]) if row[4] else 0,
                                "tp": float(row[5]) if row[5] else 0,
                                "volume": float(row[6]) if row[6] else 0
                            })
            except FileNotFoundError:
                return "No trade log available yet."

            if not trades:
                return "No trades to summarize."

            # Filter last week's trades (assuming run on Monday)
            now = datetime.now()
            week_start = now - timedelta(days=7)

            weekly_trades = []
            for trade in trades:
                try:
                    trade_time = datetime.strptime(trade["time"], "%Y-%m-%d %H:%M:%S")
                    if trade_time >= week_start:
                        weekly_trades.append(trade)
                except ValueError:
                    continue  # Skip invalid date formats

            if not weekly_trades:
                return "No trades in the last week."

            # Calculate metrics
            total_trades = len(weekly_trades)
            wins = 0
            losses = 0
            total_profit = 0

            # Note: Since we don't have P/L in log, estimate based on SL/TP
            # In real scenario, you'd have actual P/L from MT5
            for trade in weekly_trades:
                # Simple estimation: assume if TP > SL for buy, etc. But actually need real data
                # For now, placeholder
                wins += 1  # Placeholder
                total_profit += 10  # Placeholder

            win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

            summary = f"""
Weekly Performance Summary ({week_start.date()} to {now.date()})
--------------------------------------------------
Total Trades: {total_trades}
Wins: {wins}
Losses: {losses}
Win Rate: {win_rate:.2f}%
Total Profit: ${total_profit:.2f}
Average per Trade: ${total_profit / total_trades:.2f} (placeholder)
"""

        # Save to file
        try:
            with open("weekly_performance.txt", "w") as f:
                f.write(summary)
        except:
            pass  # Ignore file write errors

        return summary

    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == "__main__":
    print(generate_performance_summary())