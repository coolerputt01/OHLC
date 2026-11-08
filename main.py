import pandas as panda
import numpy as num

from src.ohlc_analysor import ohlc_analysis
from config import MARKET_DATA_FILE_PATH

dataFrame = panda.read_csv(MARKET_DATA_FILE_PATH, sep="\t")
print(dataFrame.columns)
ohlc_analysis(dataFrame)

# from src.quant_basic_maths import quant_basic_math, z_scores_calc

# returns = num.array([0.01, -0.02, 0.03, -0.01, 0.02])
# quant_basic_math(returns)
# evaluation = z_scores_calc(returns)
# print(evaluation)