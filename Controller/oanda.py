from Controller.api import OandaApi
import datetime
from Model.pricing import FxDataUsdJpy1M
import settings


class OandaStreamPricingGetter(object):
    api = OandaApi(settings.oanda_token, settings.oanda_id)

    def __init__(self):
        pass

    def start_stream_getter(self):
        OandaStreamPricingGetter.api.streaming_price(self.stream_getter_callback)

    def stream_getter_callback(self, time, bids, asks):
        avr_price = (bids + asks) / 2
        FxDataUsdJpy1M.update(time, avr_price)

        # ここでテーブルに追加する。
        # trankateの実装が必要




# こいつが常にゲットしてDBに保存する。
oanda_stream_priceing_gettere = OandaStreamPricingGetter()
