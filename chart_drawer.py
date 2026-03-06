import MetaTrader5 as mt5


def draw_asian_levels(symbol, asian_high, asian_low):

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return

    chart_id = mt5.chart_id()

    if chart_id is None:
        print("No chart found")
        return

    # delete old levels
    mt5.chart_object_delete(chart_id, "AsianHigh")
    mt5.chart_object_delete(chart_id, "AsianLow")

    # draw Asian High
    mt5.chart_object_create(
        chart_id,
        "AsianHigh",
        mt5.CHART_HLINE,
        0,
        0,
        asian_high
    )

    # draw Asian Low
    mt5.chart_object_create(
        chart_id,
        "AsianLow",
        mt5.CHART_HLINE,
        0,
        0,
        asian_low
    )

    print("Asian levels drawn on chart")


def draw_trade_arrow(symbol, direction):

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return

    price = tick.ask if direction == "BUY" else tick.bid

    chart_id = mt5.chart_id()

    if chart_id is None:
        return

    name = f"TradeArrow_{direction}"

    mt5.chart_object_create(
        chart_id,
        name,
        mt5.CHART_ARROW,
        0,
        0,
        price
    )

    print("Trade arrow drawn on chart")