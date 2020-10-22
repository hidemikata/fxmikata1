from Model.pricing import FxDataUsdJpy1M
from Controller.api import OandaApi


class Order(object):

    def __init__(self, algo, data):
        self.algo = algo
        self.data = data

    def start(self):

        judge = self.algo.judge(self.data)

        if judge == 'buy':
            buy = OandaApi()
            buy.order_nariyuki(1000)

        elif judge == 'sell':
            buy = OandaApi()
            buy.position_all_cancel()


def start_order(algo, data):
    order = Order(algo, data)
    order.start()
