import datetime as datetime
import oandapyV20
from oandapyV20.endpoints import accounts
from oandapyV20.endpoints import pricing
from oandapyV20.endpoints import orders
from oandapyV20.endpoints import positions
from datetime import datetime
import dateutil.parser
import settings


class OandaApi(object):
    def __init__(self):
        self.token = settings.oanda_token
        self.id = settings.oanda_id
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

    def _streaming_price_bits_asks(self, data):

        if data['type'] == 'HEARTBEAT':
            return None
        time = data['time']
        bids = data['bids'][0]['price']
        asks = data['asks'][0]['price']
        return {'time':time, 'bids':bids, 'asks':asks}

    def streaming_price(self, callback):
        p = {
                "instruments": "USD_JPY"
            }
        r = pricing.PricingStream(self.id, params=p)

        api = oandapyV20.API(self.token)
        rv = self.client.request(r)

        for ticks in rv:
            price = self._streaming_price_bits_asks(ticks)
            if price is not None:
                price['time'] = price['time'].split('.')[0]
                price['time'] = price['time'].replace('T', ' ')
                print(price['time'])

                callback(datetime.strptime(price['time'], '%Y-%m-%d %H:%M:%S'),
                         float(price['bids']),
                         float(price['asks']))

            #ストリーム終了
            #r.terminate('maxrecs record recieved')

    #成り行き注文
    def order_nariyuki(self, units):
        d = {
            "order": {
                "instrument": "USD_JPY",
                "units": units,
                "type": "MARKET",
            }
        }
        r = orders.OrderCreate(self.id, data=d)
        return self.req(r)

    # 注文
    def order(self):
        d = {
            "order": {
                "price": 120.000,
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
    def ordering(self, ticket):
        r = orders.OrderDetails(self.id, orderID=ticket)
        return self.req(r)

    #注文中一覧
    def ordering_all(self):
        r = orders.OrdersPending(self.id)
        return self.req(r)


    #ポジション一覧
    def position_all(self):
        r = positions.OpenPositions(self.id)
        return self.req(r)


    #全ポジション解消
    def position_all_cancel(self):
        d = {
          "longUnits": "ALL"
        }
        r = positions.PositionClose(self.id,
                                    instrument="USD_JPY",
                                    data=d)
        return self.req(r)

