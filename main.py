import pandas as panda

from src.ohlc_analysor import ohlc_analysis
from config import MARKET_DATA_FILE_PATH

dataFrame = panda.read_csv(MARKET_DATA_FILE_PATH, sep="\t")
print(dataFrame.columns)
ohlc_analysis(dataFrame)