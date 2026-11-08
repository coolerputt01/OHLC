import numpy as num
import pandas as panda


def ohlc_analysis(dataFrame):
    dataFrame["<DATETIME>"] = panda.to_datetime(
        dataFrame["<DATE>"] + " " + dataFrame["<TIME>"],
        format="%Y.%m.%d %H:%M:%S"
    )
    dataFrame = dataFrame.sort_values("<DATETIME>").reset_index(drop=True)

    dataFrame["<RETURNS>"] = dataFrame["<CLOSE>"].pct_change()
    dataFrame["<LOG_RETURNS>"] = num.log(dataFrame["<CLOSE>"]/dataFrame["<CLOSE>"].shift(1))
    dataFrame["<RANGE>"] = dataFrame["<HIGH>"] - dataFrame["<LOW>"]
    dataFrame["<BODY>"] = (dataFrame["<OPEN>"] - dataFrame["<CLOSE>"]).abs()
    dataFrame["<CANDLE_EFFICIENCY>"] = dataFrame["<BODY>"] / dataFrame["<RANGE>"].replace(0, num.nan)
    dataFrame["<VOLATILITY>"] = dataFrame["<LOG_RETURNS>"].rolling(40).std()
    dataFrame["<AVERAGE_RANGE>"] = dataFrame["<RANGE>"].rolling(40).mean()

    print(dataFrame.tail(40))

    print("\nStatistical summary:")
    print(dataFrame[[
        "<RETURNS>",
        "<LOG_RETURNS>",
        "<RANGE>",
        "<CANDLE_EFFICIENCY>",
        "<VOLATILITY>"
    ]].describe())
