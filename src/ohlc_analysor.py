import numpy as num
import pandas as panda


def ohlc_analysis(dataFrame):
    dataFrame["<DATETIME>"] = panda.to_datetime(
        dataFrame["<DATE>"] + " " + dataFrame["<TIME>"],
        format="%Y.%m.%d %H:%M:%S"
    )
    dataFrame = dataFrame.sort_values("<DATETIME>").reset_index(drop=True)

    returns = dataFrame["<RETURNS>"] = dataFrame["<CLOSE>"].pct_change()
    dataFrame["<LOG_RETURNS>"] = num.log(dataFrame["<CLOSE>"]/dataFrame["<CLOSE>"].shift(1))
    dataFrame["<RANGE>"] = dataFrame["<HIGH>"] - dataFrame["<LOW>"]
    dataFrame["<BODY>"] = (dataFrame["<OPEN>"] - dataFrame["<CLOSE>"]).abs()
    dataFrame["<CANDLE_EFFICIENCY>"] = dataFrame["<BODY>"] / dataFrame["<RANGE>"].replace(0, num.nan)
    volatility = dataFrame["<VOLATILITY>"] = dataFrame["<LOG_RETURNS>"].rolling(40).std()
    dataFrame["<AVERAGE_RANGE>"] = dataFrame["<RANGE>"].rolling(40).mean()
    z_scores = dataFrame["<Z_SCORES>"] = (dataFrame["<RETURNS>"] - dataFrame["<RETURNS>"].rolling(40).mean())/dataFrame["<RETURNS>"].rolling(40).std(ddof=1)
    dataFrame["<VOLATILITY_REGIMES>"] = num.where(
                                                volatility > volatility.quantile(0.90),
                                                "<HIGH_VOLATILITY>",
                                                "<NORMAL_VOLATILITY>"
                                            )
    dataFrame["<TRENDING_REGIMES>"] = num.select(
                                                [(z_scores > z_scores.quantile(0.90)), (z_scores < z_scores.quantile(0.10))],
                                                ["<UPTREND>","<DOWNTREND>"],
                                                default="<SIDEWAYS>"
                                            )
    dataFrame["<MEAN_REVERTING>"] = num.where(
                                            z_scores.abs() > z_scores.abs().quantile(0.90),
                                            "<STRETCHED>",
                                            "<NORMAL>" 
                                        )


    print(dataFrame.tail(40))

    print("\nStatistical summary:")
    print(dataFrame[[
        "<RETURNS>",
        "<LOG_RETURNS>",
        "<RANGE>",
        "<CANDLE_EFFICIENCY>",
        "<VOLATILITY>",
        "<Z_SCORES>",
        "<VOLATILITY_REGIMES>",
        "<TRENDING_REGIMES>"
    ]].describe())
