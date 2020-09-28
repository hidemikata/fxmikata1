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

class BackTestEvent(object):
    buy_price = None
    kessai_price = None

class BackTest(object):
    algorizm = None

    def start_getter(self):
        events = []
        short_sma = 5
        long_sma = 25
        data_margin = 1
        using_calc_data_num = long_sma + data_margin
        # データ取ってくる
        count = FxDataUsdJpy1M.get_count()
        # 動作確認は
        # count = 500とか
        count = 500
        offset = count - using_calc_data_num

        for i in range(offset, 0, -1):
            r = FxDataUsdJpy1M.get_close_past_date(limit=using_calc_data_num, past_offset=offset)
            from Controller.technical import sma
            short_sma_data = sma(r, short_sma)
            long_sma_data = sma(r, long_sma)

            from Controller.technical import sma_cross_check
            cross = sma_cross_check(short_sma_data, long_sma_data)

            if cross is 'GC':
                e = BackTestEvent
                e.buy_price = r[-1].close
                events.append(e)

            elif cross is 'DC':
                if events == [] or events[-1].kessai_price != None or events[-1].buy_price == None:
                    #nothing to do
                    pass
                events[-1].kessai_price = r[-1].close
            else:
                #nothing to do
                pass

        print(events)


    # こいつが常にゲットしてDBに保存する。


if settings.backtest:
    start_getter = BackTest()
else:
    start_getter = OandaStreamPricingGetter()
