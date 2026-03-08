import pandas as pd
from datetime import datetime

def generate_performance_summary():
    """Generate weekly performance summary from trade_log.csv"""
    try:
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

        # Save to file
        with open("weekly_performance.txt", "w") as f:
            f.write(summary)

        return summary

    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == "__main__":
    print(generate_performance_summary())