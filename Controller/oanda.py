from Controller.api import OandaApi
import datetime
from Model.pricing import FxDataUsdJpy1M
import settings
from threading import Thread
from Controller.order import start_order
import logging

logger = logging.getLogger(__name__)


class OandaStreamPricingGetter(object):
    api = OandaApi()

    def __init__(self):
        pass

    def start_getter(self):
        OandaStreamPricingGetter.api.streaming_price(self.stream_getter_callback)

    def stream_getter_callback(self, time, bids, asks):
        avr_price = (bids + asks) / 2
        is_create = FxDataUsdJpy1M.update(time, avr_price)

        if is_create:
            data = FxDataUsdJpy1M.get_close_data(limit=28)  # getできるのは同一スレッドのみ
            orderThread = Thread(target=start_order, args=(data,))  # タプルにするとき,がないと単なる括弧。
            orderThread.start()
            orderThread.join()


class BackTestEvent(object):
    buy_price = None
    buy_date = None
    kessai_price = None
    kessai_date = None


class BackTest(object):
    algorizm = None

    def start_getter(self):
        events = []
        short_sma = 5
        long_sma = 25
        data_margin = 2
        using_calc_data_num = long_sma + data_margin
        # データ取ってくる
        filter_list = []
        for t in range(4, 8):#１3時から１6時
            filter_time = '%-%-% ' + str(t).zfill(2) + ':%:%'
            filter_list.append(FxDataUsdJpy1M.time.like(filter_time))

        count = FxDataUsdJpy1M.get_count(filter_time=filter_list)
        print(count)
        # 動作確認は
        # count = 2000
        offset = count - using_calc_data_num
        latest_date = None
        for i in range(offset, 0, -1):
            r = FxDataUsdJpy1M.get_close_past_date(limit=using_calc_data_num, past_offset=i, filter_time=filter_list)

            r_close = [j.close for j in r]
            from Controller.technical import sma
            short_sma_data = sma(r_close, short_sma)
            long_sma_data = sma(r_close, long_sma)

            from Controller.technical import sma_cross_check
            cross = sma_cross_check(short_sma_data, long_sma_data)

            if cross == 'GC':
                e = BackTestEvent()
                e.buy_price = r_close[-1]
                e.buy_date = r[-1].time
                events.append(e)

            elif cross == 'DC':
                if events == [] or events[-1].kessai_price != None or events[-1].buy_price == None:
                    # nothing to do
                    pass
                else:
                    events[-1].kessai_price = r_close[-1]
                    events[-1].kessai_date = r[-1].time

            elif latest_date != None and \
                    latest_date == r[-1].time and \
                    events[-1].kessai_price == None and \
                    events[-1].buy_price != None:
                # 日付が超えてたら強制決済.１時間しかとらないので。
                events[-1].kessai_price = r_close[-1]
                events[-1].kessai_date = r[-1].time
                print('date change', str(r[-1].time))

            else:
                # nothing to do
                pass

            latest_date = str(r[-1].time).split()[0]

        if events == []:
            print('nothing')
            return

        total_profit = 0
        monthly_profit = 0
        check_month = str(events[0].buy_date).split()[0][0:7]
        for i in events:
            if i.kessai_price is not None:
                profit = i.kessai_price - i.buy_price
                total_profit = total_profit + profit

                if check_month in str(i.buy_date):
                    monthly_profit = monthly_profit + profit
                else:
                    print('monthly', check_month, monthly_profit)
                    check_month = str(i.buy_date).split()[0][0:7]
                    monthly_profit = 0

        print('monthly', check_month, monthly_profit)
        print('total', total_profit)
        events = []

# こいつが常にゲットしてDBに保存する。


if settings.backtest:
    start_getter = BackTest()
else:
    start_getter = OandaStreamPricingGetter()
