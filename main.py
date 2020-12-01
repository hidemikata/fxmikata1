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
from Controller.webserver import start_server

logging.basicConfig(format='%(levelname)s:%(asctime)s :%(message)s', level=logging.DEBUG)

def main():

    start_server()

    if settings.backtest:
        start_getter = BackTest()
    else:
        start_getter = OandaStreamPricingGetter(AlgSimpleMovingAverageCrossAlgorithm())

    start_getter.start_getter()
    #mustunit数を福利にする
    #must取引終了時刻がきたら強制決済をかける
    #must取引前にとりあえず強制決済をかける
    #エラーになった時に強制決済をして終了するようにする。
    #rasberypiにいれるなら、OSの起動と終了時に強制決済


if __name__ == '__main__':
    main()
