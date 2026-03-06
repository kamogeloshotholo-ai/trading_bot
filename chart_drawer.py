import MetaTrader5 as mt5


def draw_asian_levels(symbol, asian_high, asian_low):

    chart_id = mt5.chart_id()

    if chart_id is None:
        print("No chart found")
        return

    mt5.chart_object_delete(chart_id, "AsianHigh")
    mt5.chart_object_delete(chart_id, "AsianLow")

    mt5.chart_object_create(
        chart_id,
        "AsianHigh",
        mt5.CHART_HLINE,
        0,
        0,
        asian_high
    )

    mt5.chart_object_create(
        chart_id,
        "AsianLow",
        mt5.CHART_HLINE,
        0,
        0,
        asian_low
    )

    print("Asian levels drawn on chart")