from datetime import datetime
from Controller.AbstractAlgorithm import AbstractAlgorithm
from Controller.technical import sma
from Controller.technical import sma_cross_check


class AlgSimpleMovingAverageCrossAlgorithm(AbstractAlgorithm):
    short_sma = 5
    long_sma = 10
    data_margin = 2

    def number_of_using_data(self):
        return AlgSimpleMovingAverageCrossAlgorithm.long_sma + AlgSimpleMovingAverageCrossAlgorithm.data_margin

    def validation(self, data):
        if not self.num_of_data(data):
            print('invalid num')
            return False
        if not self.is_data_today(data):
            print('not today')
            return False
        if not self.day_same_valid(data):
            print('invalid day')
            return False
        if not self.is_trade_hour(data):
            print('invalid time')
            return False

        return True

    def is_data_today(self, data):
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        first = datetime.strftime(data[0].time, '%Y-%m-%d')
        if today != first:
            return False
        return True

    def is_trade_hour(self, data):
        start_time = datetime.strftime(datetime.now(), '%Y-%m-%d 04:00')
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')

        first_data_time = datetime.strftime(data[0].time, '%Y-%m-%d %H:%M')
        first_data_time = datetime.strptime(first_data_time, '%Y-%m-%d %H:%M')

        end_time = datetime.strftime(datetime.now(), '%Y-%m-%d 08:00')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')

        end_data_time = datetime.strftime(data[-1].time, '%Y-%m-%d %H:%M')
        end_data_time = datetime.strptime(end_data_time, '%Y-%m-%d %H:%M')


        if start_time.timestamp() < first_data_time.timestamp() and \
                end_time.timestamp() > end_data_time.timestamp():
            return True

        return False

    def num_of_data(self, data):
        return True if len(data) == self.number_of_using_data() else False

    def day_same_valid(self, data):
        time_format = '%Y-%m-%d'
        time = [datetime.strftime(i.time, time_format) for i in data]
        time_valid = all(time[0] == t for t in time[1:]) if time else False  # 日付でvalidationするようにする。
        return time_valid

    def judge(self, data):
        data = [i.close for i in data]
        sma_short = sma(data, AlgSimpleMovingAverageCrossAlgorithm.short_sma)
        sma_long = sma(data, AlgSimpleMovingAverageCrossAlgorithm.long_sma)
        cross = sma_cross_check(short_sma_data=sma_short, long_sma_data=sma_long)

        judge = None
        if cross == 'GC':
            judge = 'buy'
        elif cross == 'DC':
            judge = 'sell'
        else:
            judge = None

        return judge
