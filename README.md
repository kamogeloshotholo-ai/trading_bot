# AI Trading Bot Web Interface

This repository contains a simple algorithmic trading bot built on MetaTrader 5 and a Streamlit-based web dashboard for control and testing.

## Features

- **AI-Powered Optimizer**: Uses Bayesian optimization (via Optuna) to intelligently search for best stop-loss/take-profit combinations across symbols, learning from trial results for efficient parameter tuning.
- Asian range liquidity sweep strategy with retest entries
- Connection to MetaTrader5 for live trading
- Backtesting and optimizer utilities
- Streamlit web app with:
  - Start/stop controls for the bot
  - Real-time output monitoring from the bot process
  - Recent trade history
  - Buttons to run backtest and optimization and display results

## Getting Started

### Prerequisites

- Python 3.8+
- MetaTrader5 installed and account configured
- `pip` available

### Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   source venv/bin/activate     # macOS/Linux
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** the `MetaTrader5` package requires the MetaTrader 5 client to be installed and logged in.

### Running the Web App

Start the Streamlit dashboard:

```bash
streamlit run web_app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser. You can then start the trading bot, view logs, run backtests, etc.

### Sharing for Testing

- Package the repository or deploy to a server that has MT5 installed.
- Make sure the environment has access to the same symbols and a demo account for safe testing.
- Colleagues only need to install the requirements and launch `streamlit run web_app.py`.

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t trading-bot .
   ```

2. Run the container (ensure MT5 is accessible; may need volume mounts for MT5 data):
   ```bash
   docker run -p 8501:8501 trading-bot
   ```

3. Access the web app at `http://localhost:8501`.

> **Note:** MetaTrader5 requires the MT5 client to be installed. For Docker, you may need to use a host-mounted volume or a custom base image with MT5 pre-installed. This setup assumes a demo environment.

## Project Structure

```
│  asian_range.py
│  backtester.py
│  candle_logic.py
│  candles.py
│  liquidity_sweep.py
│  live_price.py
│  main_bot.py        # core bot logic
│  optimizer.py
│  requirements.txt
│  retest_detector.py
│  risk_calculator.py
│  strategy_engine.py
│  structure_detector.py
│  sweep_memory.py
│  trade_executor.py
│  trade_log.csv      # generated at runtime
│  trade_logger.py
│  trade_manager.py
│  web_app.py         # Streamlit interface
```

### Environment Variables

Set the following environment variables for security:

- `TRADING_BOT_PASSWORD`: Password for web app access (default: "tradingbot2026")

Feel free to modify the strategy, add configuration controls, or integrate authentication for wider sharing.
