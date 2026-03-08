import time
import MetaTrader5 as mt5
from datetime import datetime
import os

# Demo mode flag - set to True to run without MT5 (for testing)
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

from liquidity_sweep import detect_liquidity_sweep
from retest_detector import detect_retest
from trade_executor import execute_trade
from trade_manager import manage_open_trades
from sweep_memory import reset_sweep_memory, sweep_already_detected, store_sweep
from performance_summary import generate_performance_summary


# -----------------------------
# SESSION MANAGEMENT
# -----------------------------

SESSIONS = {
    "ASIAN": {"start": 0, "end": 6, "active_symbols": ["XAUUSD", "BTCUSD"]},  # Low activity, focus on gold/crypto
    "LONDON": {"start": 8, "end": 16, "active_symbols": ["EURUSD", "GBPUSD"]},  # High activity for EUR/GBP
    "NEW_YORK": {"start": 13.5, "end": 20, "active_symbols": ["EURUSD", "USDJPY", "NAS100"]},  # High activity
}

def get_current_session():
    now = datetime.now()
    hour = now.hour + now.minute / 60.0  # decimal hour

    for session, times in SESSIONS.items():
        if times["start"] <= hour < times["end"]:
            return session, times
    return "OFF_HOURS", {"active_symbols": []}  # Low activity, scan all but less frequently

def get_scan_interval(session):
    if session in ["LONDON", "NEW_YORK"]:
        return 15  # Scan every 15s during active
    elif session == "ASIAN":
        return 60  # Slower during Asian
    else:
        return 120  # Very slow off hours


# -----------------------------
# H4 BIAS CHECK
# -----------------------------

def get_h4_bias(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 0, 3)

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


# -----------------------------
# SYMBOLS
# -----------------------------

symbols = ["EURUSD", "XAUUSD", "NAS100", "BTCUSD"]

# Liquidity source: "ASIAN", "DAILY", "WEEKLY", "CUSTOM"
LIQUIDITY_SOURCE = os.getenv("LIQUIDITY_SOURCE", "ASIAN")


# -----------------------------
# RISK SETTINGS
# -----------------------------

max_trades_per_day = 2
trades_today = 0


# -----------------------------
# MEMORY
# -----------------------------

last_candle_time = {}
sweep_setups = {}

current_day = datetime.now().day
current_week = datetime.now().isocalendar()[1]  # Week number


# -----------------------------
# CONNECT MT5
# -----------------------------

def connect():

    if DEMO_MODE:
        print(f"[{datetime.now()}] DEMO MODE: Skipping MT5 connection")
        return

    print(f"[{datetime.now()}] Connecting to MT5...")

    if not mt5.initialize():
        print(f"[{datetime.now()}] MT5 initialization failed")
        quit()

    print(f"[{datetime.now()}] MT5 connected")

    account = mt5.account_info()

    if account is not None:
        print(f"[{datetime.now()}] Account balance: {account.balance}")
    else:
        print(f"[{datetime.now()}] Account info not available")


# -----------------------------
# NEW CANDLE DETECTION
# -----------------------------

def new_candle(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)

    if rates is None or len(rates) == 0:
        return False

    candle_time = rates[0]["time"]

    if symbol not in last_candle_time:
        last_candle_time[symbol] = candle_time
        return False

    if candle_time != last_candle_time[symbol]:
        last_candle_time[symbol] = candle_time
        return True

    return False


# -----------------------------
# RESET DAILY TRADES
# -----------------------------

def reset_daily_trades():

    global trades_today
    global current_day
    global sweep_setups
    global current_week

    now = datetime.now()
    week = now.isocalendar()[1]

    if week != current_week:
        # New week: generate performance summary
        summary = generate_performance_summary()
        print(f"[{datetime.now()}] Weekly Performance Summary:\n{summary}")
        current_week = week

    if now.day != current_day:

        trades_today = 0
        current_day = now.day
        # forget any stored setups from previous day
        sweep_setups.clear()

        print(f"[{datetime.now()}] Daily trades reset")


# -----------------------------
# MAIN BOT
# -----------------------------

def run_bot():

    global trades_today
    global sweep_setups

    connect()

    print(f"[{datetime.now()}] BOT STARTED")

    while True:

        reset_daily_trades()
        reset_sweep_memory()

        manage_open_trades()

        session, session_info = get_current_session()
        active_symbols = session_info["active_symbols"] or symbols  # Use session-specific or all
        scan_interval = get_scan_interval(session)

        print(f"[{datetime.now()}] Current session: {session}, Active symbols: {active_symbols}, Scan interval: {scan_interval}s")

        if trades_today >= max_trades_per_day:
            print(f"[{datetime.now()}] Daily trade limit reached ({trades_today}/{max_trades_per_day})")
            time.sleep(scan_interval)
            continue

        for symbol in active_symbols:

            print(f"[{datetime.now()}] Checking {symbol}...")

            if not new_candle(symbol):
                print(f"[{datetime.now()}] No new candle on {symbol}")
                continue

            print(f"[{datetime.now()}] New M5 candle detected on {symbol}")

            sweep = detect_liquidity_sweep(symbol, LIQUIDITY_SOURCE)

            if sweep:
                print(f"[{datetime.now()}] {symbol} Sweep detected: {sweep}")

                if sweep_already_detected(symbol):
                    print(f"[{datetime.now()}] {symbol} Sweep already processed, skipping")
                    continue

                print(f"[{datetime.now()}] {symbol} Storing new sweep")
                store_sweep(symbol, sweep)
                sweep_setups[symbol] = sweep
            else:
                print(f"[{datetime.now()}] {symbol} No sweep detected")

            if symbol in sweep_setups:
                print(f"[{datetime.now()}] {symbol} Checking for retest on existing sweep")

                signal = detect_retest(symbol, sweep_setups[symbol])

                if signal:
                    print(f"[{datetime.now()}] {symbol} Retest signal: {signal}")

                    # Check H4 bias for high probability
                    bias = get_h4_bias(symbol)
                    required_bias = "UP" if signal == "BUY" else "DOWN"

                    if bias != required_bias:
                        print(f"[{datetime.now()}] {symbol} Bias {bias} not matching required {required_bias}, skipping trade")
                        continue

                    # Check if position already open
                    positions = mt5.positions_get(symbol=symbol)
                    if positions and len(positions) > 0:
                        print(f"[{datetime.now()}] {symbol} Position already open, skipping trade")
                        continue

                    execute_trade(symbol, signal, sweep_setups[symbol])

                    trades_today += 1

                    print(f"[{datetime.now()}] {symbol} Trade executed. Trades today: {trades_today}")

                    del sweep_setups[symbol]
                else:
                    print(f"[{datetime.now()}] {symbol} No retest signal")
            else:
                print(f"[{datetime.now()}] {symbol} No active sweep setup")

        print(f"[{datetime.now()}] Waiting for next scan ({scan_interval}s)...")
        time.sleep(scan_interval)


run_bot()