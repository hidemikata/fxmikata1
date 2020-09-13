import oandapyV20
from oandapyV20.endpoints import accounts
from oandapyV20.endpoints import pricing
from oandapyV20.endpoints import orders
import settings


class OandaApi(object):
    def __init__(self, token, id):
        self.token = token
        self.id = id
        self.client = oandapyV20.API(self.token)

    def req(self, r):
        self.client.request(r)
        return r.response

    # 口座サマリー
    def summary(self):
        r = accounts.AccountSummary(self.id)
        return self.req(r)

    # 値段
    def pricing(self):
        p = {
            "instruments": "USD_JPY"
        }
        r = pricing.PricingInfo(self.id, params=p)
        return self.req(r)

    # 注文
    def order(self):
        d = {
            "order": {
                "price": 100.000,
                "timeInForce": "GTC",
                "instrument": "USD_JPY",
                "units": "120",
                "type": "LIMIT",
                "positionFill": "DEFAULT"
            }
        }

        r = orders.OrderCreate(self.id, data=d)
        return self.req(r)
    #注文状況取得
    def ordering(self):
        ticket = 229

        r = orders.OrderDetails(self.id, orderID=ticket)

        return self.req(r)



