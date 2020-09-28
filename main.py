import settings
import logging
import datetime
from Controller.api import OandaApi
from Model.pricing import FxDataUsdJpy1M
from Controller.oanda import start_getter
from Controller.technical import sma


logging.basicConfig(format='%(levelname)s:%(asctime)s :%(message)s', level=logging.DEBUG)


def main():
    start_getter.start_getter()


if __name__ == '__main__':
    main()
