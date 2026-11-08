import pandas as panda
import numpy as num

from src.ohlc_analysor import ohlc_analysis, next_returns_ohlc
from config import MARKET_DATA_FILE_PATH
from src.quant_basic_maths import quant_basic_math

dataFrame = panda.read_csv(MARKET_DATA_FILE_PATH, sep="\t")
# df = ohlc_analysis(dataFrame)
# print(df.tail(40))
# quant_basic_math(df["<RETURNS>"])

next_returns_ohlc(dataFrame)

# from src.quant_basic_maths import quant_basic_math, z_scores_calc

# returns = num.array([0.01, -0.02, 0.03, -0.01, 0.02])
# quant_basic_math(returns)
# evaluation = z_scores_calc(returns)
# print(evaluation)