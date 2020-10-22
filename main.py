import settings
import logging
import datetime
from Controller.api import OandaApi
from Model.pricing import FxDataUsdJpy1M
from Controller.oanda import OandaStreamPricingGetter
from Controller.technical import sma
from datetime import datetime
from Controller.backtest import BackTest
from Controller.algsmacross import AlgSimpleMovingAverageCrossAlgorithm

logging.basicConfig(format='%(levelname)s:%(asctime)s :%(message)s', level=logging.DEBUG)

def main():
    if settings.backtest:
        start_getter = BackTest()
    else:
        start_getter = OandaStreamPricingGetter(AlgSimpleMovingAverageCrossAlgorithm())

    start_getter.start_getter()


if __name__ == '__main__':
    main()
