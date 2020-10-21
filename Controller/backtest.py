from Model.pricing import FxDataUsdJpy1M


class BackTestEvent(object):
    buy_price = None
    buy_date = None
    kessai_price = None
    kessai_date = None


class BackTest(object):

    def start_getter(self):
        events = []
        short_sma = 5
        long_sma = 10
        data_margin = 2
        using_calc_data_num = long_sma + data_margin
        # データ取ってくる
        filter_list = []
        for t in range(4, 8):  # １3時から１6時
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

            new_latest_date = str(r[-1].time).split()[0]

            from Controller.technical import sma
            short_sma_data = sma(r_close, short_sma)
            long_sma_data = sma(r_close, long_sma)

            from Controller.technical import sma_cross_check
            cross = sma_cross_check(short_sma_data, long_sma_data)

            all_times = [j.time.strftime('%Y%m%d') for j in r]
            same_date = all(all_times[0] == t for t in all_times[1:]) if all_times else False

            if cross == 'GC' and same_date:
                e = BackTestEvent()
                e.buy_price = r_close[-1]
                e.buy_date = r[-1].time
                events.append(e)

            elif cross == 'DC':
                if events == [] or events[-1].kessai_price is not None or events[-1].buy_price is None:
                    # nothing to do
                    pass
                else:
                    events[-1].kessai_price = r_close[-1]
                    events[-1].kessai_date = r[-1].time

            elif latest_date is not None and \
                    latest_date != new_latest_date and \
                    len(events) > 0 and \
                    events[-1].kessai_price is None and \
                    events[-1].buy_price is not None:
                # 日付が超えてたら強制決済.
                events[-1].kessai_price = r_close[-1]
                events[-1].kessai_date = r[-1].time
                print('date change', str(r[-1].time))

            else:
                # nothing to do
                pass

            latest_date = new_latest_date

        if not events:
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
