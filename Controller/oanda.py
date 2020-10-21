from Controller.api import OandaApi
import datetime
from Model.pricing import FxDataUsdJpy1M
import settings
from threading import Thread
from Controller.order import start_order
from Controller.backtest import BackTest
from Controller.algsmacross import AlgSimpleMovingAverageCrossAlgorithm
import logging

logger = logging.getLogger(__name__)


class OandaStreamPricingGetter(object):
    api = OandaApi()

    def __init__(self, algo):
        self.algo = algo
        pass

    def start_getter(self):
        OandaStreamPricingGetter.api.streaming_price(self.stream_getter_callback)

    def stream_getter_callback(self, time, bids, asks):
        avr_price = (bids + asks) / 2
        is_create = FxDataUsdJpy1M.update(time, avr_price)

        if is_create:
            filte_time = []
            filte_time.append(FxDataUsdJpy1M.time.like('%-%-% %:%:%'))#time.likeを後で調べる
            data = FxDataUsdJpy1M.get_close_past_date(limit=self.algo.num_of_using_data, past_offset=1, filter_time=filte_time)  # getできるのは同一スレッドのみ
            if self.algo.validation(data):#algoをインタフェースでていぎするとよい
                orderThread = Thread(target=start_order, args=(self.algo, data, ))  # タプルにするとき,がないと単なる括弧。
                orderThread.start()
                orderThread.join()


if settings.backtest == True:
    start_getter = BackTest()
else:
    start_getter = OandaStreamPricingGetter(AlgSimpleMovingAverageCrossAlgorithm())
