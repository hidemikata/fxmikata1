import settings
import logging
from Controller.api import OandaApi
import Model.pricing as pricing
from Controller.oanda import oanda_stream_priceing_gettere

logging.basicConfig(format='%(levelname)s:%(asctime)s :%(message)s', level=logging.DEBUG)


def main():
    #logging.info('hoge')

    o = OandaApi(settings.oanda_token, settings.oanda_id)
    # res = o.summary()
    # print(res)

    #print(o.pricing())
    #print(o.order())
    #print(o.ordering())
    #pricing.testadd()
    #pricing.testget()
    #o.streaming_price(callback=call)
    #print(o.ordering(212))
    #print(o.position_all())
    #print(o.ordering_all())
    #print(o.position_all_cancel())

    oanda_stream_priceing_gettere.start_stream_getter()


if __name__ == '__main__':
    main()
