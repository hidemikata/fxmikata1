import talib as ta
import numpy as np


def sma(data, period):
    sma = ta.SMA(np.array(data, dtype='f8'), timeperiod=period)
    sma[np.isnan(sma)] = None
    return sma


def sma_cross_check(short_sma_data, long_sma_data):
    sma_short_last_1 = short_sma_data[-1]
    sma_short_last_2 = short_sma_data[-2]
    sma_long_last_1 = long_sma_data[-1]
    sma_long_last_2 = long_sma_data[-2]
    sma_long_last_3 = long_sma_data[-3]
    # ゴールデンクロス
    if sma_long_last_3 < sma_long_last_2 and \
            sma_short_last_2 < sma_long_last_2 and \
            sma_short_last_1 > sma_long_last_1:
        return 'GC'

    # デッドクロス
    elif sma_short_last_2 > sma_long_last_2 and \
            sma_short_last_1 < sma_long_last_1:
        return 'DC'

    else:
        return None
