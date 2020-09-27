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

    def start_stream_getter(self):
        OandaStreamPricingGetter.api.streaming_price(self.stream_getter_callback)

    def stream_getter_callback(self, time, bids, asks):
        avr_price = (bids + asks) / 2
        is_create = FxDataUsdJpy1M.update(time, avr_price)

        if is_create:
            data = FxDataUsdJpy1M.get_close_data(limit=28)#getできるのは同一スレッドのみ
            orderThread = Thread(target=start_order, args=(data, ))#タプルにするとき,がないと単なる括弧。
            orderThread.start()
            orderThread.join()



# こいつが常にゲットしてDBに保存する。
oanda_stream_priceing_gettere = OandaStreamPricingGetter()
