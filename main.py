import settings
import logging
import datetime
from Controller.api import OandaApi
from Model.pricing import FxDataUsdJpy1M
from Controller.oanda import oanda_stream_priceing_gettere

logging.basicConfig(format='%(levelname)s:%(asctime)s :%(message)s', level=logging.DEBUG)


def main():
    # logging.info('hoge')

    #print(FxDataUsdJpy1M.get_latest())
    #now = datetime.datetime.now()
    #FxDataUsdJpy1M.add_price(time=now, open=1, high=2, low=3, close=4)
#    latest = FxDataUsdJpy1M.get_latest()
#    print(latest.open)
    now = datetime.datetime.now()
    FxDataUsdJpy1M.update(time=now, price=6)

    exit()

    o = OandaApi(settings.oanda_token, settings.oanda_id)
    # res = o.summary()
    # print(res)

    # print(o.pricing())
    # print(o.order())
    # print(o.ordering())
    # pricing.testadd()
    # pricing.testget()
    # o.streaming_price(callback=call)
    # print(o.ordering(212))
    # print(o.position_all())
    # print(o.ordering_all())
    # print(o.position_all_cancel())

    oanda_stream_priceing_gettere.start_stream_getter()


if __name__ == '__main__':
    main()
