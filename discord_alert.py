import requests
import os
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(message):
    """Send a message to Discord via webhook."""
    if not DISCORD_WEBHOOK_URL:
        print(f"[{datetime.now()}] Discord webhook not set, skipping alert")
        return

    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print(f"[{datetime.now()}] Discord alert sent: {message}")
        else:
            print(f"[{datetime.now()}] Failed to send Discord alert: {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] Error sending Discord alert: {e}")

def alert_sweep_detected(symbol, sweep_info):
    """Send alert for sweep detection."""
    direction = sweep_info.get("direction")
    level = sweep_info.get("level")
    message = f"🚨 **Sweep Detected** 🚨\nSymbol: {symbol}\nDirection: {direction}\nLevel: {level}\nTime: {datetime.now()}"
    send_discord_alert(message)

def alert_trade_executed(symbol, signal, entry_price):
    """Send alert for trade execution."""
    message = f"💰 **Trade Executed** 💰\nSymbol: {symbol}\nSignal: {signal}\nEntry: {entry_price}\nTime: {datetime.now()}"
    send_discord_alert(message)