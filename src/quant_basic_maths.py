import numpy as num

def quant_basic_math(returns):
    print("Mean: ",returns.mean())
    print("Median: ", returns.median())
    print("Population Variance: ", returns.var())
    print("Sample Variance: ", returns.var(ddof=1))
    print("Population Standard Deviation: ",returns.std())
    print("Sample Standard Deviation: ", returns.std(ddof=1))


def z_scores_calc(returns):
    mean = returns.mean()
    std = returns.std(ddof=1)

    return (returns - mean)/std