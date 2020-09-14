import settings
import logging
from Controller.api import OandaApi
import Model.pricing as pricing

logging.basicConfig(format='%(levelname)s:%(asctime)s :%(message)s', level=logging.DEBUG)


def main():
    #logging.info('hoge')

    o = OandaApi(settings.oanda_token, settings.oanda_id)
    # res = o.summary()
    # print(res)

    #print(o.pricing())
    #print(o.order())
    #print(o.ordering())

    pricing.testadd()
    pricing.testget()


if __name__ == '__main__':
    main()
