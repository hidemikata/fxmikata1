import settings
import logging
from Controller.api import OandaApi
from Model.pricing import test
logging.basicConfig(format='%(levelname)s:%(asctime)s :%(message)s', level=logging.DEBUG)


def main():
    logging.info('hoge')

    o = OandaApi(settings.oanda_token, settings.oanda_id)
    # res = o.summary()
    # print(res)

    #print(o.pricing())
    #print(o.order())
    #print(o.ordering())

    test()


if __name__ == '__main__':
    main()
