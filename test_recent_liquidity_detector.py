"""Simple unit tests for recent_liquidity_detector logic."""
import os
# run tests in DEMO_MODE to avoid requiring MetaTrader5
os.environ["DEMO_MODE"] = "true"
import recent_liquidity_detector


class DummyMT5:
    def __init__(self, m1_data, m5_data):
        self._m1 = m1_data
        self._m5 = m5_data

    def copy_rates_from_pos(self, symbol, timeframe, pos, count):
        if timeframe == recent_liquidity_detector.TIMEFRAME_M1:
            return self._m1
        if timeframe == recent_liquidity_detector.TIMEFRAME_M5:
            return self._m5
        return None


def setup_dummy(m1, m5, high_level, low_level):
    recent_liquidity_detector.DEMO_MODE = False
    recent_liquidity_detector.mt5 = DummyMT5(m1, m5)
    recent_liquidity_detector.get_liquidity_levels = lambda s, src="ASIAN": (
        high_level, low_level
    )


def test_reversal_above():
    # high touches level then closes below -> reversal
    m1 = [{'high': 1, 'low': 1} for _ in range(60)]
    m5 = [
        {'high': 1, 'low': 1, 'close': 0.99},
        {'high': 1.05, 'low': 1.0, 'close': 0.999},
    ]
    setup_dummy(m1, m5, 1.0, 0.95)
    sweep = recent_liquidity_detector.detect_recent_liquidity_sweep("SYM")
    assert sweep is not None
    assert sweep['direction'] == 'SELL'
    assert sweep['reversal'] is True


def test_breakout_above():
    # high touches level then closes above -> breakout -> NO sweep returned
    m1 = [{'high': 1, 'low': 1} for _ in range(60)]
    m5 = [
        {'high': 1, 'low': 1, 'close': 1.01},
        {'high': 1.05, 'low': 1.0, 'close': 1.02},
    ]
    setup_dummy(m1, m5, 1.0, 0.95)
    sweep = recent_liquidity_detector.detect_recent_liquidity_sweep("SYM")
    assert sweep is None  # breakout should NOT return sweep


def test_reversal_below():
    m1 = [{'high': 1, 'low': 1} for _ in range(60)]
    m5 = [
        {'high': 1, 'low': 1.1, 'close': 1.1},
        {'high': 0.95, 'low': 0.9, 'close': 1.05},
    ]
    setup_dummy(m1, m5, 1.2, 1.0)
    sweep = recent_liquidity_detector.detect_recent_liquidity_sweep("SYM")
    assert sweep is not None
    assert sweep['direction'] == 'BUY'
    assert sweep['reversal'] is True


def test_breakout_below():
    # low touches level then closes below -> breakout -> NO sweep returned
    m1 = [{'high': 1, 'low': 1} for _ in range(60)]
    m5 = [
        {'high': 1, 'low': 1.2, 'close': 1.3},
        {'high': 0.95, 'low': 0.9, 'close': 0.85},
    ]
    setup_dummy(m1, m5, 1.2, 1.0)
    sweep = recent_liquidity_detector.detect_recent_liquidity_sweep("SYM")
    assert sweep is None  # breakout should NOT return sweep


if __name__ == "__main__":
    # simple run
    test_reversal_above()
    test_breakout_above()
    test_reversal_below()
    test_breakout_below()
    print("All tests passed")
