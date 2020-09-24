from Model.pricing import FxDataUsdJpy1M
from Controller.technical import sma
from Controller.api import OandaApi

class Order(object):

    def test(self):
        pass

    def start(self, data):
        short_avr = 5
        long_avr = 25

        sma_short = sma(data, short_avr)
        sma_long = sma(data, long_avr)
        num = len(sma_short)
        if num < long_avr + 2:
            #25までの平均が25個目になる、25, 26で比べる
            return

        sma_short_last_1 = sma_short[-1]
        sma_short_last_2 = sma_short[-2]
        sma_long_last_1 = sma_long[-1]
        sma_long_last_2 = sma_long[-2]

        #ゴールデンクロス
        if sma_short_last_2 < sma_long_last_2 and \
                sma_short_last_1 > sma_short_last_1:
            buy = OandaApi()
            buy.order_nariyuki(1000)

        #デッドクロス
        if sma_short_last_2 > sma_long_last_2 and \
                sma_short_last_1 < sma_short_last_1:
            buy = OandaApi()
            buy.order_nariyuki(-1000)



def start_order(data):
    order = Order()
    order.start(data)
