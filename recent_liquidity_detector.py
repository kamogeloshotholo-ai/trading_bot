import os
from datetime import datetime, timedelta

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

if not DEMO_MODE:
    import MetaTrader5 as mt5
    TIMEFRAME_M1 = mt5.TIMEFRAME_M1
    TIMEFRAME_M5 = mt5.TIMEFRAME_M5
else:
    TIMEFRAME_M1 = 1
    TIMEFRAME_M5 = 5

from liquidity_map import get_liquidity_levels


def detect_recent_liquidity_sweep(symbol, liquidity_source="ASIAN"):
    """Enhanced liquidity sweep detection with recent activity confirmation"""

    # Get traditional liquidity levels
    liquidity_high, liquidity_low = get_liquidity_levels(symbol, liquidity_source)

    if liquidity_high is None or liquidity_low is None:
        return None

    if DEMO_MODE:
        # Mock enhanced sweep for demo
        import random
        if random.choice([True, False]):
            return {
                "direction": "SELL",
                "level": liquidity_high,
                "sweep_high": liquidity_high + 0.01,
                "sweep_low": liquidity_high - 0.01,
                "recent_activity": True,
                "confidence": "High"
            }
        else:
            return None

    # Get recent M1 data to check for recent activity
    recent_rates = mt5.copy_rates_from_pos(symbol, TIMEFRAME_M1, 0, 60)  # Last hour

    # Get current price data
    rates = mt5.copy_rates_from_pos(symbol, TIMEFRAME_M5, 0, 2)

    if rates is None or len(rates) < 2:
        return None

    candle = rates[1]
    high = candle["high"]
    low = candle["low"]
    close = candle["close"]

    sweep_info = None

    # Enhanced sweep detection with recent activity confirmation
    if high > liquidity_high and close < liquidity_high:
        # Check for recent activity near the level
        recent_activity = False
        if recent_rates is not None:
            for rate in recent_rates[-20:]:  # Last 20 minutes
                if abs(rate['high'] - liquidity_high) < 0.001 or abs(rate['low'] - liquidity_high) < 0.001:
                    recent_activity = True
                    break

        confidence = "High" if recent_activity else "Medium"
        print(f"{symbol} Enhanced liquidity sweep ABOVE high (Confidence: {confidence})")

        sweep_info = {
            "direction": "SELL",
            "level": liquidity_high,
            "sweep_high": high,
            "sweep_low": low,
            "recent_activity": recent_activity,
            "confidence": confidence
        }

    elif low < liquidity_low and close > liquidity_low:
        # Check for recent activity near the level
        recent_activity = False
        if recent_rates is not None:
            for rate in recent_rates[-20:]:  # Last 20 minutes
                if abs(rate['high'] - liquidity_low) < 0.001 or abs(rate['low'] - liquidity_low) < 0.001:
                    recent_activity = True
                    break

        confidence = "High" if recent_activity else "Medium"
        print(f"{symbol} Enhanced liquidity sweep BELOW low (Confidence: {confidence})")

        sweep_info = {
            "direction": "BUY",
            "level": liquidity_low,
            "sweep_high": high,
            "sweep_low": low,
            "recent_activity": recent_activity,
            "confidence": confidence
        }

    return sweep_info


def get_recent_liquidity_summary(symbol):
    """Get a summary of recent liquidity conditions"""
    # Get traditional liquidity levels
    traditional_high, traditional_low = get_liquidity_levels(symbol, "ASIAN")

    summary = {
        'symbol': symbol,
        'volume_clusters_count': 0,  # Placeholder for future enhancement
        'rejection_signals_count': 0,  # Placeholder for future enhancement
        'order_flow_imbalance': None,  # Placeholder for future enhancement
        'last_update': datetime.now()
    }

    if traditional_high and traditional_low:
        summary['traditional_high'] = traditional_high
        summary['traditional_low'] = traditional_low

    return summary


# Backwards compatibility
def detect_liquidity_sweep(symbol, liquidity_source="ASIAN"):
    """Backwards compatible function that uses enhanced detection"""
    return detect_recent_liquidity_sweep(symbol, liquidity_source)