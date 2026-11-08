import numpy as num
import pandas as panda


def ohlc_analysis(df):
    dataFrame = df.copy()

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

    print("\nStatistical summary:")
    print(dataFrame[[
        "<RETURNS>",
        "<LOG_RETURNS>",
        "<RANGE>",
        "<CANDLE_EFFICIENCY>",
        "<VOLATILITY>",
        "<Z_SCORES>"
    ]].describe())

    print(
        "Observations above 2: ", (z_scores > 2).sum(),
        "Observations below -2: ", (z_scores < -2).sum()
    )


    return dataFrame

def next_returns_ohlc(df):
    dataFrame = df.copy()

    dataFrame["<DATETIME>"] = panda.to_datetime(
        dataFrame["<DATE>"] + " " + dataFrame["<TIME>"],
        format="%Y.%m.%d %H:%M:%S"
    )
    dataFrame = dataFrame.sort_values("<DATETIME>").reset_index(drop=True)

    # DIRECTIONAL CONTINUATION

    dataFrame["<CURRENT_DIRECTION>"] = num.sign(dataFrame["<OPEN>"] - dataFrame["<CLOSE>"])
    dataFrame["<NEXT_DIRECTION>"] = num.sign(dataFrame["<OPEN>"].shift(-1) - dataFrame["<CLOSE>"].shift(-1))
    dataFrame["<CONTINUATION>"] = (dataFrame["<CURRENT_DIRECTION>"] == dataFrame["<NEXT_DIRECTION>"])

    dataFrame["<RANGE>"] = dataFrame["<HIGH>"] - dataFrame["<LOW>"]
    dataFrame["<BODY>"] = (dataFrame["<CLOSE>"] - dataFrame["<OPEN>"]).abs()
    dataFrame["<CANDLE_EFFICIENCY>"] = dataFrame["<BODY>"] / dataFrame["<RANGE>"].replace(0, num.nan)

    dataFrame["<VARIABLE_Y>"] = (dataFrame["<CLOSE>"].shift(-1) / dataFrame["<CLOSE>"] ) - 1
    dataFrame["<VARIABLE_Y_VALUE_CAP>"] = (dataFrame["<VARIABLE_Y>"] > 0)

    dataFrame["<MOVING_AVERAGE>"] = dataFrame["<CLOSE>"].mean()
    dataFrame["<AVERAGE_SLOPE>"] = dataFrame["<MOVING_AVERAGE>"].diff(5)
    dataFrame["<TREND>"] = num.where(dataFrame["<AVERAGE_SLOPE>"] > 0, "<UPTREND>","<DOWNTREND>")

    dataFrame.loc[dataFrame["<AVERAGE_SLOPE>"] == 0, "<TREND>"] = "<FLAT>"

    research_data = dataFrame[
                                (dataFrame["<CURRENT_DIRECTION>"] != 0) & (dataFrame["<NEXT_DIRECTION>"] != 0)
                            ].dropna(subset=["<CANDLE_EFFICIENCY>","<VARIABLE_Y_VALUE_CAP>"]).copy()

    research_data["<CANDLE_EFFICIENCY_GROUP>"] = panda.qcut(research_data["<CANDLE_EFFICIENCY>"],q=5,labels=False,duplicates="drop")
    
    print(
        research_data.groupby("<CANDLE_EFFICIENCY_GROUP>")[
            "<VARIABLE_Y>"
        ].agg(["count", "mean", "median", "std"])
    )

    print(
        research_data.groupby("<CANDLE_EFFICIENCY_GROUP>")[
            "<VARIABLE_Y_VALUE_CAP>"
        ].mean()
    )

    print(
        research_data.groupby("<CANDLE_EFFICIENCY_GROUP>")[
            "<CONTINUATION>"
        ].mean()
    )

    print(
        research_data["<TREND>"]
    )