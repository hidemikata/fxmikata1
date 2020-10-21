from Model.pricing import FxDataUsdJpy1M
from Controller.technical import sma
from Controller.technical import sma_cross_check
from Controller.api import OandaApi


class Order(object):

    def test(self):
        pass

    def start(self, algo, data):
        same_date = all(data[0] == t for t in data[1:]) if data else False

        short_avr_day = 5
        long_avr_day = 10
        data_margin = 2

        if len(data) < long_avr_day + data_margin:
            return

        sma_short = sma(data, short_avr_day)
        sma_long = sma(data, long_avr_day)
        cross = sma_cross_check(short_sma_data=sma_short, long_sma_data=sma_long)


        # ゴールデンクロス
        if cross == 'GC':
            buy = OandaApi()
            buy.order_nariyuki(1000)
        # デッドクロス
        elif cross == 'DC':
            buy = OandaApi()
            buy.position_all_cancel()


def start_order(data):
    order = Order()
    order.start(data)
