from Controller.api import OandaApi
from Model.pricing import FxDataUsdJpy1M
import settings


class OandaStreamPricingGetter(object):
    api = OandaApi(settings.oanda_token, settings.oanda_id)
    def __init__(self):
        pass

    def start_stream_getter(self):
        OandaStreamPricingGetter.api.streaming_price(self.stream_getter_callback)

    def stream_getter_callback(self, bids, asks):
        print(bids, asks)


#こいつが常にゲットしてDBに保存する。
oanda_stream_priceing_gettere = OandaStreamPricingGetter()


