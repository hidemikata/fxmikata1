
from datetime import datetime

class AlgSimpleMovingAverageCrossAlgorithm(object):
    short_sma = 5
    long_sma = 10
    data_margin = 2
    num_of_using_data = long_sma + data_margin

    def validation(self, data):
        if self.num_of_data(data) == False:
            print('invalid num')
            return False
        if self.time_valid(data) == False:
            print('invalid time')
            return False
        return True

    def num_of_data(self, data):
        return True if len(data) == self.num_of_using_data else False

    def time_valid(self, data):
        time_format = '%Y-%m-%d'
        time = [datetime.strftime(i.time, time_format) for i in data]
        time_valid = all(time[0] == t for t in time[1:]) if time else False#日付でvalidationするようにする。
        return time_valid



