import talib as ta
import numpy as np


def sma(data, period):
    sma = ta.SMA(np.array(data, dtype='f8'), timeperiod=period)
    sma[np.isnan(sma)] = None
    return sma
