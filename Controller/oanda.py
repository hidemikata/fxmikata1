from Controller.api import OandaApi
import datetime
from Model.pricing import FxDataUsdJpy1M
import settings
from threading import Thread
from Controller.order import start_order
import logging

logger = logging.getLogger(__name__)


class OandaStreamPricingGetter(object):
    api = OandaApi()

    def __init__(self):
        pass

    def start_getter(self):
        OandaStreamPricingGetter.api.streaming_price(self.stream_getter_callback)

    def stream_getter_callback(self, time, bids, asks):
        avr_price = (bids + asks) / 2
        is_create = FxDataUsdJpy1M.update(time, avr_price)

        if is_create:
            data = FxDataUsdJpy1M.get_close_data(limit=28)  # getできるのは同一スレッドのみ
            orderThread = Thread(target=start_order, args=(data,))  # タプルにするとき,がないと単なる括弧。
            orderThread.start()
            orderThread.join()


class BackTest(object):
    algorizm = None

    def start_getter(self):
        short_sma = 5
        long_sma = 25
        data_margin = 1
        using_calc_data_num = long_sma + data_margin
        # データ取ってくる
        count = FxDataUsdJpy1M.get_count()
        #動作確認は
        #count=1000とか

        offset = count - using_calc_data_num

        #for i in range(offset, 0, -1):
        r = FxDataUsdJpy1M.get_close_past_date(limit=using_calc_data_num, past_offset=offset)
        from Controller.technical import sma
        short_sma_data = sma(r, short_sma)
        long_sma_data = sma(r, long_sma)

        sma_short_last_1 = short_sma_data[-1]
        sma_short_last_2 = short_sma_data[-2]
        sma_long_last_1 = long_sma_data[-1]
        sma_long_last_2 = long_sma_data[-2]

        # ゴールデンクロス
        if sma_short_last_2 < sma_long_last_2 and \
                sma_short_last_1 > sma_long_last_1:
            pass

        # デッドクロス
        if sma_short_last_2 > sma_long_last_2 and \
                sma_short_last_1 < sma_long_last_1:
            pass



        # 注文→けっさいを繰り返す
        # 前の注文から決済までのをおぼえておいて足していく。

        pass

    # こいつが常にゲットしてDBに保存する。

if settings.backtest:
    start_getter = BackTest()
else:
    start_getter = OandaStreamPricingGetter()
